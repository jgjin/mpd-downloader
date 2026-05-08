from typing import Literal

from pydantic import BaseModel


class VideoToDownload(BaseModel):
    id: str

    mpd_path: str


SegmentType = Literal["video", "audio"]


class SegmentToDownload(BaseModel):
    video_id: str
    segment_type: SegmentType
    index: int

    download_url: str


class DownloadedSegment(BaseModel):
    video_id: str
    segment_type: SegmentType
    index: int

    downloaded_path: str


class DownloadedVideo(BaseModel):
    id: str

    downloaded_path: str
