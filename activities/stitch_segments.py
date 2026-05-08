import structlog
from temporalio import activity

from schemas.video import DownloadedSegment, DownloadedVideo

logger = structlog.get_logger()


@activity.defn
async def stitch_segments(
    video_id: str, downloaded_segments: list[DownloadedSegment]
) -> DownloadedVideo:
    logger.info("stitching segments", video_id=video_id, count=len(downloaded_segments))

    return DownloadedVideo(id=video_id, downloaded_path=f"/tmp/{video_id}_final.mp4")
