import asyncio
import time

import structlog
from temporalio.client import Client

from queues.task_queue import TaskQueue
from schemas.video import DownloadedVideo
from workflows.download_videos import DownloadVideos


async def main():
    logger = structlog.get_logger()

    client = await Client.connect("localhost:7233")
    downloaded_videos: list[DownloadedVideo] = await client.execute_workflow(
        DownloadVideos.run,
        id=f"download-videos-{int(time.time())}",
        task_queue=TaskQueue.SMALL_IO,
    )

    for video in downloaded_videos:
        logger.info(
            "downloaded video",
            video_id=video.id,
            storage_bucket_name=video.downloaded_storage_path.storage_bucket_name,
            downloaded_path=video.downloaded_storage_path.path,
        )


if __name__ == "__main__":
    asyncio.run(main())
