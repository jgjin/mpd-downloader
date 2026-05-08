from temporalio import activity

from schemas.video import ConcatenatedRepresentation, ContentType
from storage.get_storage import get_storage


@activity.defn
async def concatenate_segments(
    video_id: str,
    content_type: ContentType,
    downloaded_paths: list[str],
) -> ConcatenatedRepresentation:
    target_path = f"segments/{video_id}/{content_type}/concatenated.mp4"
    concatenated_path = get_storage().concat_files(downloaded_paths, target_path)

    return ConcatenatedRepresentation(
        video_id=video_id,
        content_type=content_type,
        concatenated_path=concatenated_path,
    )
