import asyncio
import os

import structlog
from temporalio.client import Client
from temporalio.worker import Worker

from queues.task_queue import TaskQueue
from queues.worker_config import QUEUE_WORKER_CONFIG


async def main(task_queue: TaskQueue):
    logger = structlog.get_logger()

    client = await Client.connect("localhost:7233", namespace="default")
    worker_config = QUEUE_WORKER_CONFIG[task_queue]
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=worker_config.workflows,
        activities=worker_config.activities,
    )

    logger.info("running worker", task_queue=task_queue)
    await worker.run()


if __name__ == "__main__":
    task_queue = TaskQueue(os.environ["TASK_QUEUE"])

    asyncio.run(main(task_queue))
