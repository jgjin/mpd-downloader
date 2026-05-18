import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.decrypt_representation import decrypt_representation
    from activities.extract_representations import extract_representations
    from activities.get_clearkey import get_clearkey
    from activities.merge_representations import merge_representations
    from queues.task_queue import TaskQueue
    from schemas.video import (
        DownloadedVideo,
        RepresentationsToMerge,
        RepresentationToDownload,
        VideoToDownload,
    )
    from storage.storage_bucket_name import StorageBucketName
    from workflows.download_representation import DownloadRepresentation


@workflow.defn
class DownloadVideo:
    @workflow.run
    async def run(self, video: VideoToDownload) -> DownloadedVideo:
        extracted_representations = await workflow.execute_activity(
            extract_representations,
            video,
            start_to_close_timeout=timedelta(minutes=6),
        )

        segments_storage_bucket = StorageBucketName.SEGMENTS
        concatenated_video_rep, concatenated_audio_rep = await asyncio.gather(
            workflow.execute_child_workflow(
                DownloadRepresentation.run,
                RepresentationToDownload(
                    video_id=video.id,
                    content_type="video",
                    segment_download_urls=extracted_representations.video_segment_download_urls,
                    storage_bucket_name=segments_storage_bucket,
                ),
            ),
            workflow.execute_child_workflow(
                DownloadRepresentation.run,
                RepresentationToDownload(
                    video_id=video.id,
                    content_type="audio",
                    segment_download_urls=extracted_representations.audio_segment_download_urls,
                    storage_bucket_name=segments_storage_bucket,
                ),
            ),
        )

        clearkey = await workflow.execute_activity(
            get_clearkey,
            video,
            start_to_close_timeout=timedelta(minutes=6),
        )

        decrypted_video_rep, decrypted_audio_rep = await asyncio.gather(
            workflow.execute_activity(
                decrypt_representation,
                args=[concatenated_video_rep, clearkey],
                start_to_close_timeout=timedelta(minutes=6),
                task_queue=TaskQueue.LARGE_PROCESSING,
            ),
            workflow.execute_activity(
                decrypt_representation,
                args=[concatenated_audio_rep, clearkey],
                start_to_close_timeout=timedelta(minutes=6),
                task_queue=TaskQueue.LARGE_PROCESSING,
            ),
        )

        return await workflow.execute_activity(
            merge_representations,
            args=[
                RepresentationsToMerge(
                    video_id=video.id,
                    video_representation_storage_path=decrypted_video_rep.decrypted_storage_path,
                    audio_representation_storage_path=decrypted_audio_rep.decrypted_storage_path,
                ),
                StorageBucketName.VIDEOS,
            ],
            start_to_close_timeout=timedelta(minutes=6),
            task_queue=TaskQueue.LARGE_PROCESSING,
        )
