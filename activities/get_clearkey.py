import os

from temporalio import activity

from schemas.video import ClearKey, VideoToDownload


@activity.defn
async def get_clearkey(video_to_download: VideoToDownload) -> ClearKey:
    video_id = video_to_download.id

    return ClearKey(
        video_id=video_id,
        key_id=os.environ["CLEARKEY_ID"],
        key_value=os.environ["CLEARKEY_VALUE"],
    )
