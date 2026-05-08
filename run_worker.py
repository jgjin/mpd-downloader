import asyncio

import structlog
from temporalio.client import Client
from temporalio.worker import Worker

from activities.concatenate_segments import concatenate_segments
from activities.decrypt_representation import decrypt_representation
from activities.download_segment import download_segment
from activities.extract_segments import extract_segments
from activities.get_clearkey import get_clearkey
from activities.list_videos import list_videos
from activities.merge_representations import merge_representations
from workflows.download_video import DownloadVideo
from workflows.download_videos import DownloadVideos


async def main():
    logger = structlog.get_logger()

    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(
        client,
        task_queue="download-videos-task-queue",
        workflows=[DownloadVideos, DownloadVideo],
        activities=[
            list_videos,
            get_clearkey,
            extract_segments,
            download_segment,
            concatenate_segments,
            decrypt_representation,
            merge_representations,
        ],
    )

    logger.info("running worker")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
