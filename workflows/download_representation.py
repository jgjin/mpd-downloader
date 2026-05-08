import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.concatenate_segments import concatenate_segments
    from activities.download_segment import download_segment
    from schemas.video import (
        ConcatenatedRepresentation,
        Representation,
        SegmentToDownload,
    )


@workflow.defn
class DownloadRepresentation:
    @workflow.run
    async def run(self, representation: Representation) -> ConcatenatedRepresentation:
        download_each_segment = [
            workflow.execute_activity(
                download_segment,
                SegmentToDownload(
                    video_id=representation.video_id,
                    content_type=representation.content_type,
                    index=index,
                    download_url=download_url,
                ),
                start_to_close_timeout=timedelta(minutes=6),
            )
            for index, download_url in enumerate(representation.segment_download_urls)
        ]

        downloaded_paths = await asyncio.gather(*download_each_segment)

        return await workflow.execute_activity(
            concatenate_segments,
            args=[
                representation.video_id,
                representation.content_type,
                downloaded_paths,
            ],
            start_to_close_timeout=timedelta(minutes=6),
        )
