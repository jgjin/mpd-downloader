import structlog
from temporalio import activity

from schemas.video import VideoToDownload

logger = structlog.get_logger()


@activity.defn
async def list_videos() -> list[VideoToDownload]:
    logger.info("listing videos")

    return [
        VideoToDownload(id="v1", mpd_path="/path/to/v1.mpd"),
        VideoToDownload(id="v2", mpd_path="/path/to/v2.mpd"),
    ]
