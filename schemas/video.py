from typing import Literal

from pydantic import BaseModel

from schemas.storage import StoragePath
from storage.storage_bucket_name import StorageBucketName


class VideoToDownload(BaseModel):
    id: str

    mpd_storage_path: StoragePath


class ExtractedRepresentations(BaseModel):
    video_id: str

    video_segment_download_urls: list[str]
    audio_segment_download_urls: list[str]


ContentType = Literal["video", "audio"]


class RepresentationToDownload(BaseModel):
    video_id: str
    content_type: ContentType

    segment_download_urls: list[str]

    storage_bucket_name: StorageBucketName


class SegmentToDownload(BaseModel):
    video_id: str
    content_type: ContentType
    index: int

    download_url: str


class SegmentsToConcatenate(BaseModel):
    video_id: str
    content_type: ContentType

    segment_paths: list[str]


class ConcatenatedRepresentation(BaseModel):
    video_id: str
    content_type: ContentType

    concatenated_storage_path: StoragePath


class ClearKey(BaseModel):
    video_id: str

    key_id: str
    key_value: str


class DecryptedRepresentation(BaseModel):
    video_id: str
    content_type: ContentType

    decrypted_storage_path: StoragePath


class RepresentationsToMerge(BaseModel):
    video_id: str

    video_representation_storage_path: StoragePath
    audio_representation_storage_path: StoragePath


class DownloadedVideo(BaseModel):
    id: str

    downloaded_storage_path: StoragePath
