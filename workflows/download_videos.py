import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.list_videos import list_videos
    from schemas.video import DownloadedVideo
    from storage.storage_bucket_name import StorageBucketName
    from workflows.download_video import DownloadVideo


@workflow.defn
class DownloadVideos:
    @workflow.run
    async def run(self) -> list[DownloadedVideo]:
        videos = await workflow.execute_activity(
            list_videos,
            args=[StorageBucketName.MPDS],
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
