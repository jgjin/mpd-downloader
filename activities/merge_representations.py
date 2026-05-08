import tempfile

import av
from temporalio import activity

from schemas.video import DecryptedRepresentation, DownloadedVideo
from storage.get_storage import get_storage


@activity.defn
async def merge_representations(
    video_id: str,
    video_representation: DecryptedRepresentation,
    audio_representation: DecryptedRepresentation,
) -> DownloadedVideo:
    with tempfile.NamedTemporaryFile() as tmp:
        tmp_path = tmp.name

        with av.open(tmp_path, mode="w", format="mp4") as output:
            with av.open(video_representation.decrypted_path) as video_input:
                video_stream = next(s for s in video_input.streams if s.type == "video")
                out_video_stream = output.add_stream(template=video_stream)

                for packet in video_input.demux(video_stream):
                    packet.stream = out_video_stream
                    output.mux(packet)

            with av.open(audio_representation.decrypted_path) as audio_input:
                audio_stream = next(s for s in audio_input.streams if s.type == "audio")
                out_audio_stream = output.add_stream(template=audio_stream)

                for packet in audio_input.demux(audio_stream):
                    packet.stream = out_audio_stream
                    output.mux(packet)

        target_path = f"videos/{video_id}.mp4"
        with open(tmp_path, "rb") as readable_stream:
            downloaded_path = get_storage().write_file(readable_stream, target_path)

        return DownloadedVideo(
            id=video_id,
            downloaded_path=downloaded_path,
        )
