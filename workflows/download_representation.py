import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.concatenate_segments import concatenate_segments
    from activities.download_segment import download_segment
    from schemas.video import (
        ConcatenatedRepresentation,
        RepresentationToDownload,
        SegmentsToConcatenate,
        SegmentToDownload,
    )


@workflow.defn
class DownloadRepresentation:
    @workflow.run
    async def run(
        self, representation: RepresentationToDownload
    ) -> ConcatenatedRepresentation:
        storage_bucket_name = representation.storage_bucket_name
        download_each_segment = [
            workflow.execute_activity(
                download_segment,
                args=[
                    SegmentToDownload(
                        video_id=representation.video_id,
                        content_type=representation.content_type,
                        index=index,
                        download_url=download_url,
                    ),
                    storage_bucket_name,
                ],
                start_to_close_timeout=timedelta(minutes=6),
            )
            for index, download_url in enumerate(representation.segment_download_urls)
        ]

        downloaded_paths = await asyncio.gather(*download_each_segment)

        return await workflow.execute_activity(
            concatenate_segments,
            args=[
                SegmentsToConcatenate(
                    video_id=representation.video_id,
                    content_type=representation.content_type,
                    segment_paths=downloaded_paths,
                ),
                storage_bucket_name,
            ],
            start_to_close_timeout=timedelta(minutes=6),
        )
