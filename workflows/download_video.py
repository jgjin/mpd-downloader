import asyncio
from datetime import timedelta

from temporalio import workflow

# Import activities, passing them through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities.concatenate_segments import concatenate_segments
    from activities.decrypt_representation import decrypt_representation
    from activities.download_segment import download_segment
    from activities.extract_segments import extract_segments
    from activities.get_clearkey import get_clearkey
    from activities.merge_representations import merge_representations
    from schemas.video import DownloadedVideo, VideoToDownload


@workflow.defn
class DownloadVideo:
    @workflow.run
    async def run(self, video: VideoToDownload) -> DownloadedVideo:
        clearkey = await workflow.execute_activity(
            get_clearkey,
            video,
            start_to_close_timeout=timedelta(minutes=6),
        )

        extracted_segments = await workflow.execute_activity(
            extract_segments,
            video,
            start_to_close_timeout=timedelta(minutes=6),
        )

        download_each_video_segment = [
            workflow.execute_activity(
                download_segment,
                segment,
                start_to_close_timeout=timedelta(minutes=6),
            )
            for segment in extracted_segments.video_segments
        ]
        download_each_audio_segment = [
            workflow.execute_activity(
                download_segment,
                segment,
                start_to_close_timeout=timedelta(minutes=6),
            )
            for segment in extracted_segments.audio_segments
        ]
        downloaded_video_segments = await asyncio.gather(*download_each_video_segment)
        downloaded_audio_segments = await asyncio.gather(*download_each_audio_segment)

        concatenated_video_rep = await workflow.execute_activity(
            concatenate_segments,
            args=[video.id, "video", downloaded_video_segments],
            start_to_close_timeout=timedelta(minutes=6),
        )
        concatenated_audio_rep = await workflow.execute_activity(
            concatenate_segments,
            args=[video.id, "audio", downloaded_audio_segments],
            start_to_close_timeout=timedelta(minutes=6),
        )

        decrypted_video_rep = await workflow.execute_activity(
            decrypt_representation,
            args=[concatenated_video_rep, clearkey],
            start_to_close_timeout=timedelta(minutes=6),
        )
        decrypted_audio_rep = await workflow.execute_activity(
            decrypt_representation,
            args=[concatenated_audio_rep, clearkey],
            start_to_close_timeout=timedelta(minutes=6),
        )

        return await workflow.execute_activity(
            merge_representations,
            args=[video.id, decrypted_video_rep, decrypted_audio_rep],
            start_to_close_timeout=timedelta(minutes=6),
        )
