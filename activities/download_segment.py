import structlog
from temporalio import activity

from schemas.video import SegmentToDownload

logger = structlog.get_logger()


@activity.defn
async def download_segment(segment_to_download: SegmentToDownload) -> str:
    video_id = segment_to_download.video_id
    content_type = segment_to_download.content_type
    index = segment_to_download.index
    download_url = segment_to_download.download_url

    logger.info(
        "downloading segment",
        video_id=video_id,
        content_type=content_type,
        index=index,
        download_url=download_url,
    )

    return "downloaded_path"
