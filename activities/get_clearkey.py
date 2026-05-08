import structlog
from temporalio import activity

from schemas.video import ClearKey, VideoToDownload

logger = structlog.get_logger()


@activity.defn
async def get_clearkey(video_to_download: VideoToDownload) -> ClearKey:
    video_id = video_to_download.id
    mpd_path = video_to_download.mpd_path

    logger.info("getting ClearKey", video_id=video_id, mpd_path=mpd_path)

    return ClearKey(video_id=video_id, key_id="key_id", key_value="key_value")
