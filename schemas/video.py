from typing import Literal

from pydantic import BaseModel


class VideoToDownload(BaseModel):
    id: str

    mpd_path: str


class ClearKey(BaseModel):
    video_id: str

    key_id: str
    key_value: str


class ExtractedRepresentations(BaseModel):
    video_id: str

    video_segment_download_urls: list[str]
    audio_segment_download_urls: list[str]


ContentType = Literal["video", "audio"]


class Representation(BaseModel):
    video_id: str
    content_type: ContentType

    segment_download_urls: list[str]


class SegmentToDownload(BaseModel):
    video_id: str
    content_type: ContentType
    index: int

    download_url: str


class ConcatenatedRepresentation(BaseModel):
    video_id: str
    content_type: ContentType

    concatenated_path: str


class DecryptedRepresentation(BaseModel):
    video_id: str
    content_type: ContentType

    decrypted_path: str


class DownloadedVideo(BaseModel):
    id: str

    downloaded_path: str
