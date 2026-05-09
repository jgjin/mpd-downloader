import argparse
import asyncio

import structlog
from temporalio.client import Client
from temporalio.worker import Worker

from queues.mapping import QUEUE_MAPPING
from queues.task_queue import TaskQueue


async def main(task_queue: TaskQueue):
    logger = structlog.get_logger()

    client = await Client.connect("localhost:7233", namespace="default")
    coverage = QUEUE_MAPPING[task_queue]
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=coverage.workflows,
        activities=coverage.activities,
    )

    logger.info("running worker", task_queue=task_queue)
    await worker.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="runs a Temporal worker for a specific task queue"
    )
    parser.add_argument(
        "--task_queue",
        type=str,
        choices=[q.value for q in TaskQueue],
        required=True,
    )
    args = parser.parse_args()

    asyncio.run(main(TaskQueue(args.task_queue)))
