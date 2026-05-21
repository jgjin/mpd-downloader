from storage.local import LocalStorageBucket
from storage.protocols import StorageBucket
from storage.storage_bucket_name import StorageBucketName


def get_storage_bucket(storage_bucket_name: StorageBucketName) -> StorageBucket:
    return LocalStorageBucket(storage_bucket_name.value)
