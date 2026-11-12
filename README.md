# Harbor Tutorial: forward-pass-bench

Code for the Forward Pass video **"Harbor Framework Tutorial: Evaluate AI Agents in Sandboxes"**.

A small custom benchmark for [Harbor](https://github.com/harbor-framework/harbor), the framework for evaluating AI agents
in sealed sandboxes. Each task gives the agent a Docker container, then a verifier checks what the agent actually
changed on that machine and writes a reward. Everything here runs locally in Docker with no API keys.

## What's inside

| Path | What it is |
| --- | --- |
| `forward-pass-bench/fix-the-bug` | Fix `median()` in `/app/stats.py` without modifying the input list. Verifier: pytest, reward 0 or 1 |
| `forward-pass-bench/log-detective` | Answer three questions about a web server log in `/app/answer.json`. Verifier: partial credit (1/3 per answer) in a separate verifier container |
| `forward-pass-bench/top-customer` | Write a SQL query for the customer with the highest total spend. Verifier: runs the query against the database |
| `agents/scripted_agent.py` | A custom Harbor agent with **no LLM**: it replays a fixed shell script per task, including two planted mistakes, and logs every step as an ATIF trajectory |
| `compare-agents.yaml` | A job config that runs three agents over the benchmark in one go |
| `rollouts.py` | Harbor's Python API: generate rollouts and collect rewards the way an RL training loop would |

Each task folder has the Harbor layout: `instruction.md`, `task.toml`, `environment/` (Dockerfile), `tests/`
(the verifier) and `solution/solve.sh` (the reference solution the `oracle` agent runs).

## Run it

You need Docker running and Python 3.12. We used Harbor 0.25.0, installed with [uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt
```

Then, from this folder:

```bash
harbor run -p forward-pass-bench/fix-the-bug -a oracle      # one task, reference solution
harbor run -p forward-pass-bench -a oracle                  # whole benchmark: should score 1.0
harbor run -p forward-pass-bench -a nop                     # an agent that does nothing: should score 0.0
PYTHONPATH=. harbor run -p forward-pass-bench -a agents.scripted_agent:ScriptedAgent

PYTHONPATH=. harbor run -c compare-agents.yaml              # oracle, nop and the scripted agent together
harbor run -p forward-pass-bench -a oracle -k 3 -n 9        # 3 attempts per task, 9 trials in parallel
PYTHONPATH=. python rollouts.py                             # rollouts + rewards from Python

harbor view jobs                                            # browse results and trajectories
```

## Our results

| Agent | fix-the-bug | log-detective | top-customer | Mean |
| --- | --- | --- | --- | --- |
| `oracle` | 1 | 1 | 1 | 1.000 |
| `nop` | 0 | 0 | 0 | 0.000 |
| scripted agent (no LLM) | 0 | 0.667 | 1 | 0.556 |

The scripted agent's two planted mistakes: it sorts the list in place (the task says not to modify it), and it sorts
the log's latency column as text, so it reports the wrong slowest request.

Running the oracle 3 times per task (9 trials) took 1m 40s one at a time (`-n 1`) and 19 s with 9 in parallel (`-n 9`)
on a laptop.

## A known weak verifier (on purpose)

`top-customer`'s verifier only checks that the query returns "Grace". A wrong query that picks the customer with the
single biggest order also returns Grace and gets full marks. The video uses this to show that a verifier is only as good
as its tests. Try fixing it: add a second customer whose many small orders beat Grace's total, or compare the query's
result with the reference query on a few different databases.
