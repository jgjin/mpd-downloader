import asyncio

import structlog
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker

from queues.task_queue import TaskQueue
from queues.worker_config import QUEUE_WORKER_CONFIG
from settings.worker_settings import global_instance as worker_settings


async def main(task_queue: TaskQueue):
    logger = structlog.get_logger()

    client = await Client.connect(
        worker_settings.temporal_host,
        namespace=worker_settings.temporal_namespace,
        data_converter=pydantic_data_converter,
    )
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
    asyncio.run(main(worker_settings.task_queue))
