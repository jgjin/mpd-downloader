from pathlib import Path

from temporalio import activity

from schemas.storage import StoragePath
from schemas.video import VideoToDownload
from storage.get_storage_bucket import get_storage_bucket
from storage.storage_bucket_name import StorageBucketName


@activity.defn
async def list_videos(storage_bucket_name: StorageBucketName) -> list[VideoToDownload]:
    storage_bucket = get_storage_bucket(storage_bucket_name)

    return [
        VideoToDownload(
            id=Path(mpd_path).stem,
            mpd_storage_path=StoragePath(
                storage_bucket_name=storage_bucket_name,
                path=mpd_path,
            ),
        )
        for mpd_path in storage_bucket.list_files()
    ]
