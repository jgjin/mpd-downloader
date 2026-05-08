import structlog
from temporalio import activity

from schemas.video import ClearKey, ConcatenatedRepresentation, DecryptedRepresentation

logger = structlog.get_logger()


@activity.defn
async def decrypt_representation(
    representation: ConcatenatedRepresentation, clearkey: ClearKey
) -> DecryptedRepresentation:
    video_id = representation.video_id
    content_type = representation.content_type

    logger.info(
        "decrypting representation",
        video_id=video_id,
        content_type=content_type,
        key_id=clearkey.key_id,
    )

    return DecryptedRepresentation(
        video_id=video_id,
        content_type=content_type,
        decrypted_path="decrypted_path",
    )
