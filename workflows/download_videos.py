import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.list_videos import list_videos
    from schemas.video import DownloadedVideo, VideoToDownload
    from workflows.download_video import DownloadVideo


@workflow.defn
class DownloadVideos:
    @workflow.run
    async def run(self) -> list[DownloadedVideo]:
        videos: list[VideoToDownload] = await workflow.execute_activity(
            list_videos,
            start_to_close_timeout=timedelta(minutes=6),
        )

        download_each_video = [
            workflow.execute_child_workflow(
                DownloadVideo.run,
                video,
                id=f"download-video-{video.id}",
            )
            for video in videos
        ]

        return await asyncio.gather(*download_each_video)
