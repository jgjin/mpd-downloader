import structlog
from temporalio import activity

from schemas.video import DecryptedRepresentation, DownloadedVideo

logger = structlog.get_logger()


@activity.defn
async def merge_representations(
    video_id: str,
    video_representation: DecryptedRepresentation,
    audio_representation: DecryptedRepresentation,
) -> DownloadedVideo:
    logger.info(
        "merging representations",
        video_id=video_id,
    )

    # placeholder for actual muxing logic (e.g., ffmpeg -i video.mp4 -i audio.mp4 -c copy final.mp4)
    return DownloadedVideo(
        id=video_id,
        downloaded_path="downloaded_path",
    )
