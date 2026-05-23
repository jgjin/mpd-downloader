from settings.worker_settings import get_worker_settings
from storage.local import LocalStorageBucket
from storage.protocols import StorageBucket
from storage.s3 import S3StorageBucket
from storage.storage_bucket_name import StorageBucketName


def get_storage_bucket(storage_bucket_name: StorageBucketName) -> StorageBucket:
    settings = get_worker_settings()
    if settings.s3_bucket_suffix:
        return S3StorageBucket(
            f"{storage_bucket_name.value}-{settings.s3_bucket_suffix}"
        )

    return LocalStorageBucket(storage_bucket_name.value)
