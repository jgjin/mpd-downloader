from temporalio import activity

from schemas.storage import StoragePath
from schemas.video import ConcatenatedRepresentation, SegmentsToConcatenate
from storage.get_storage_bucket import get_storage_bucket
from storage.storage_bucket_name import StorageBucketName


@activity.defn
async def concatenate_segments(
    segments_to_concatenate: SegmentsToConcatenate,
    storage_bucket_name: StorageBucketName,
) -> ConcatenatedRepresentation:
    video_id = segments_to_concatenate.video_id
    content_type = segments_to_concatenate.content_type
    segment_paths = segments_to_concatenate.segment_paths

    target_path = f"{video_id}/{content_type}/concatenated.mp4"
    concatenated_path = get_storage_bucket(storage_bucket_name).concat_files(
        segment_paths, target_path
    )

    return ConcatenatedRepresentation(
        video_id=video_id,
        content_type=content_type,
        concatenated_storage_path=StoragePath(
            storage_bucket_name=storage_bucket_name,
            path=concatenated_path,
        ),
    )
