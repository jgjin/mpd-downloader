import structlog
from temporalio import activity

from schemas.video import SegmentToDownload, VideoToDownload

logger = structlog.get_logger()


@activity.defn
async def extract_segments(
    video_to_download: VideoToDownload,
) -> list[SegmentToDownload]:
    video_id = video_to_download.id
    logger.info("extracting segments", video_id=video_id)

    return [
        SegmentToDownload(
            video_id=video_id,
            segment_type="video",
            index=1,
            download_url=f"https://example.com/{video_id}/video/seg1.m4s",
        ),
        SegmentToDownload(
            video_id=video_id,
            segment_type="audio",
            index=1,
            download_url=f"https://example.com/{video_id}/audio/seg1.m4s",
        ),
    ]
