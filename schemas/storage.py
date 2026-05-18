from pydantic import BaseModel

from storage.storage_bucket_name import StorageBucketName


class StoragePath(BaseModel):
    storage_bucket_name: StorageBucketName
    path: str
