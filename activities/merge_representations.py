import heapq
import tempfile
from typing import Generator

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
    storage = get_storage()

    with tempfile.NamedTemporaryFile() as tmp:
        tmp_path = tmp.name

        with (
            av.open(
                storage.read_file(video_representation.decrypted_path), "r"
            ) as video_input,
            av.open(
                storage.read_file(audio_representation.decrypted_path), "r"
            ) as audio_input,
            av.open(tmp_path, mode="w", format="mp4") as output,
        ):
            in_video_stream = next(s for s in video_input.streams if s.type == "video")
            out_video_stream = output.add_stream_from_template(in_video_stream)
            out_video_stream.time_base = in_video_stream.time_base

            in_audio_stream = next(s for s in audio_input.streams if s.type == "audio")
            out_audio_stream = output.add_stream_from_template(in_audio_stream)
            out_audio_stream.time_base = in_audio_stream.time_base

            video_packets = get_packet_iterator(
                video_input, in_video_stream, out_video_stream
            )
            audio_packets = get_packet_iterator(
                audio_input, in_audio_stream, out_audio_stream
            )
            for packet in heapq.merge(
                video_packets, audio_packets, key=lambda p: p.dts
            ):
                output.mux(packet)

        target_path = f"videos/{video_id}.mp4"
        with open(tmp_path, "rb") as readable_stream:
            downloaded_path = storage.write_file(readable_stream, target_path)

        return DownloadedVideo(
            id=video_id,
            downloaded_path=downloaded_path,
        )


def get_packet_iterator(
    in_container: av.container.InputContainer,
    in_stream: av.stream.Stream,
    out_stream: av.stream.Stream,
) -> Generator[av.packet.Packet, None, None]:
    for packet in in_container.demux(in_stream):
        if packet.dts is not None:
            packet.stream = out_stream
            yield packet
