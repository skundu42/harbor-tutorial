"""Generate rollouts with Harbor's Python API and collect the rewards,
the way an RL training loop would (no LLM: uses our scripted agent)."""

import asyncio

from harbor.job import Job
from harbor.models.job.config import DatasetConfig, JobConfig
from harbor.models.trial.config import AgentConfig


async def main():
    config = JobConfig(
        job_name="rollouts",
        n_attempts=2,  # rollouts per task
        n_concurrent_trials=6,
        quiet=True,
        agents=[AgentConfig(import_path="agents.scripted_agent:ScriptedAgent")],
        datasets=[DatasetConfig(path="forward-pass-bench")],
    )
    job = await Job.create(config)
    result = await job.run()

    for trial in sorted(result.trial_results, key=lambda t: t.task_name):
        reward = trial.verifier_result.rewards if trial.verifier_result else None
        print(f"{trial.task_name:28} {trial.trial_name:24} {reward}  valid={trial.reward_valid}")


asyncio.run(main())
