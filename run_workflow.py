import asyncio

import structlog
from temporalio.client import Client

from schemas.video import DownloadedVideo
from workflows.download_videos import DownloadVideos


async def main():
    logger = structlog.get_logger()

    client = await Client.connect("localhost:7233")
    downloaded_videos: list[DownloadedVideo] = await client.execute_workflow(
        DownloadVideos.run,
        id="download-videos",
        task_queue="download-videos-task-queue",
    )

    for video in downloaded_videos:
        logger.info(
            "downloaded video", video_id=video.id, downloaded_path=video.downloaded_path
        )


if __name__ == "__main__":
    asyncio.run(main())
