from temporalio import activity

from schemas.video import ClearKey, VideoToDownload
from settings.worker_settings import global_instance as worker_settings


@activity.defn
async def get_clearkey(video_to_download: VideoToDownload) -> ClearKey:
    video_id = video_to_download.id

    return ClearKey(
        video_id=video_id,
        key_id=worker_settings.clearkey_id,
        key_value=worker_settings.clearkey_value,
    )
