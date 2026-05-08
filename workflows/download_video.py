import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.download_segment import download_segment
    from activities.extract_segments import extract_segments
    from activities.stitch_segments import stitch_segments
    from schemas.video import (
        DownloadedSegment,
        DownloadedVideo,
        SegmentToDownload,
        VideoToDownload,
    )


@workflow.defn
class DownloadVideo:
    @workflow.run
    async def run(self, video: VideoToDownload) -> DownloadedVideo:
        segments: list[SegmentToDownload] = await workflow.execute_activity(
            extract_segments,
            video,
            start_to_close_timeout=timedelta(minutes=6),
        )

        download_each_segment = [
            workflow.execute_activity(
                download_segment,
                segment,
                start_to_close_timeout=timedelta(minutes=6),
            )
            for segment in segments
        ]
        downloaded_segments: list[DownloadedSegment] = await asyncio.gather(
            *download_each_segment
        )

        return await workflow.execute_activity(
            stitch_segments,
            args=[video.id, downloaded_segments],
            start_to_close_timeout=timedelta(minutes=6),
        )
