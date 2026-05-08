import asyncio

import structlog
from temporalio.client import Client
from temporalio.worker import Worker

from activities.download_segment import download_segment
from activities.extract_segments import extract_segments
from activities.list_videos import list_videos
from activities.stitch_segments import stitch_segments
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
            extract_segments,
            download_segment,
            stitch_segments,
        ],
    )

    logger.info("running worker")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
