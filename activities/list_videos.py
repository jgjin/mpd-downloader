from pathlib import Path

from temporalio import activity

from schemas.video import VideoToDownload
from storage.get_storage import get_storage


@activity.defn
async def list_videos() -> list[VideoToDownload]:
    return [
        VideoToDownload(id=Path(mpd_path).stem, mpd_path=mpd_path)
        for mpd_path in get_storage().list_directory("mpds/")
    ]
