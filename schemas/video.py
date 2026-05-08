from typing import Literal

from pydantic import BaseModel


class VideoToDownload(BaseModel):
    id: str

    mpd_path: str


class ClearKey(BaseModel):
    video_id: str

    key_id: str
    key_value: str


ContentType = Literal["video", "audio"]


class SegmentToDownload(BaseModel):
    video_id: str
    content_type: ContentType
    index: int

    download_url: str


class ExtractedSegments(BaseModel):
    video_id: str

    video_segments: list[SegmentToDownload]
    audio_segments: list[SegmentToDownload]


class DownloadedSegment(BaseModel):
    video_id: str
    content_type: ContentType
    index: int

    downloaded_path: str


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
