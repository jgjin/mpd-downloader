import asyncio
from datetime import timedelta

from temporalio import workflow

# Import activities and workflows, passing them through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities.decrypt_representation import decrypt_representation
    from activities.extract_representations import extract_representations
    from activities.get_clearkey import get_clearkey
    from activities.merge_representations import merge_representations
    from schemas.video import DownloadedVideo, Representation, VideoToDownload
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

        concatenated_video_rep, concatenated_audio_rep = await asyncio.gather(
            workflow.execute_child_workflow(
                DownloadRepresentation.run,
                Representation(
                    video_id=video.id,
                    content_type="video",
                    segment_download_urls=extracted_representations.video_segment_download_urls,
                ),
            ),
            workflow.execute_child_workflow(
                DownloadRepresentation.run,
                Representation(
                    video_id=video.id,
                    content_type="audio",
                    segment_download_urls=extracted_representations.audio_segment_download_urls,
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
            ),
            workflow.execute_activity(
                decrypt_representation,
                args=[concatenated_audio_rep, clearkey],
                start_to_close_timeout=timedelta(minutes=6),
            ),
        )

        return await workflow.execute_activity(
            merge_representations,
            args=[video.id, decrypted_video_rep, decrypted_audio_rep],
            start_to_close_timeout=timedelta(minutes=6),
        )
