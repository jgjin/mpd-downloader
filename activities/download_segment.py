import requests
from temporalio import activity

from schemas.video import SegmentToDownload
from storage.get_storage import get_storage


@activity.defn
async def download_segment(segment_to_download: SegmentToDownload) -> str:
    video_id = segment_to_download.video_id
    content_type = segment_to_download.content_type
    index = segment_to_download.index
    download_url = segment_to_download.download_url

    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    target_path = f"segments/{video_id}/{content_type}/{index}.m4s"
    downloaded_path = get_storage().write_file(response.raw, target_path)

    return downloaded_path
