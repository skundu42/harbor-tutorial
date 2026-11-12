"""A tiny custom agent with no LLM: it replays a fixed shell script per task
(including two realistic mistakes) and logs every step as an ATIF trajectory."""

import json

from harbor.agents.base import BaseAgent
from harbor.agents.capabilities import AgentCapabilities
from harbor.models.trajectories import (
    Agent, Observation, ObservationResult, Step, ToolCall, Trajectory,
)

PLAYBOOK = {
    "median()": [
        ("Read the buggy file.", "cat /app/stats.py"),
        ("Sort the list before indexing.",
         r"sed -i 's/    n = len(values)/    values.sort()\n    n = len(values)/' /app/stats.py"),
        ("Check one example.", "python3 -c 'from stats import median; print(median([3, 1, 2]))'"),
    ],
    "server.log": [
        ("Peek at the log.", "head -3 /app/server.log"),
        ("Count 5xx responses.", "awk '$5 >= 500' /app/server.log | wc -l"),
        ("Find the busiest IP.", "awk '{print $2}' /app/server.log | sort | uniq -c | sort -rn | head -1"),
        ("Find the slowest request.", "sort -k6 -r /app/server.log | head -1"),
        ("Write the answer.",
         """echo '{"errors": 4, "top_ip": "10.0.0.4", "slowest_path": "/api/orders"}' > /app/answer.json"""),
    ],
    "shop.db": [
        ("Write the query.",
         "echo 'SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id "
         "GROUP BY c.id ORDER BY SUM(o.amount) DESC LIMIT 1;' > /app/query.sql"),
    ],
}


class ScriptedAgent(BaseAgent):
    capabilities = AgentCapabilities(atif=True)

    @staticmethod
    def name() -> str:
        return "scripted-agent"

    def version(self) -> str:
        return "0.1.0"

    async def setup(self, environment) -> None:
        pass

    async def run(self, instruction, environment, context) -> None:
        script = next(s for key, s in PLAYBOOK.items() if key in instruction)
        steps = [Step(step_id=1, source="user", message=instruction)]

        for thought, command in script:
            result = await environment.exec(command=command)
            call_id = f"call-{len(steps)}"
            steps.append(Step(
                step_id=len(steps) + 1,
                source="agent",
                message=thought,
                tool_calls=[ToolCall(tool_call_id=call_id, function_name="bash",
                                     arguments={"command": command})],
                observation=Observation(results=[ObservationResult(
                    source_call_id=call_id,
                    content=(result.stdout or "") + (result.stderr or ""),
                )]),
            ))

        trajectory = Trajectory(agent=Agent(name=self.name(), version=self.version()), steps=steps)
        (self.logs_dir / "trajectory.json").write_text(
            json.dumps(trajectory.to_json_dict(), indent=2) + "\n"
        )
