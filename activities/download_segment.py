import structlog
from temporalio import activity

from schemas.video import DownloadedSegment, SegmentToDownload

logger = structlog.get_logger()


@activity.defn
async def download_segment(segment_to_download: SegmentToDownload) -> DownloadedSegment:
    video_id = segment_to_download.video_id
    segment_type = segment_to_download.segment_type
    index = segment_to_download.index
    logger.info(
        "downloading segment", video_id=video_id, segment_type=segment_type, index=index
    )

    return DownloadedSegment(
        video_id=video_id,
        segment_type=segment_type,
        index=index,
        downloaded_path=f"/tmp/{video_id}_{segment_type}_{index}.m4s",
    )
