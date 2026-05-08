import structlog
from temporalio import activity

from schemas.video import ConcatenatedRepresentation, ContentType

logger = structlog.get_logger()


@activity.defn
async def concatenate_segments(
    video_id: str,
    content_type: ContentType,
    downloaded_paths: list[str],
) -> ConcatenatedRepresentation:
    logger.info(
        "concatenating segments",
        video_id=video_id,
        content_type=content_type,
        count=len(downloaded_paths),
    )

    return ConcatenatedRepresentation(
        video_id=video_id,
        content_type=content_type,
        concatenated_path="concatenated_path",
    )
