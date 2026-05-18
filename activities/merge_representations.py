import heapq
import tempfile
from typing import Generator

import av
from temporalio import activity

from schemas.storage import StoragePath
from schemas.video import DownloadedVideo, RepresentationsToMerge
from storage.get_storage_bucket import get_storage_bucket
from storage.storage_bucket_name import StorageBucketName


@activity.defn
async def merge_representations(
    representations_to_merge: RepresentationsToMerge,
    storage_bucket_name: StorageBucketName,
) -> DownloadedVideo:
    video_id = representations_to_merge.video_id
    video_rep_storage_path = representations_to_merge.video_representation_storage_path
    audio_rep_storage_path = representations_to_merge.audio_representation_storage_path

    with tempfile.NamedTemporaryFile() as tmp:
        tmp_path = tmp.name
        with (
            av.open(
                get_storage_bucket(
                    video_rep_storage_path.storage_bucket_name
                ).read_file(video_rep_storage_path.path),
                "r",
            ) as video_input,
            av.open(
                get_storage_bucket(
                    audio_rep_storage_path.storage_bucket_name
                ).read_file(audio_rep_storage_path.path),
                "r",
            ) as audio_input,
            av.open(
                tmp_path, mode="w", format="mp4", options={"movflags": "faststart"}
            ) as output,
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
                video_packets, audio_packets, key=lambda p: p.dts * p.time_base
            ):
                output.mux(packet)

        storage_bucket = get_storage_bucket(storage_bucket_name)
        target_path = f"{video_id}.mp4"
        with open(tmp_path, "rb") as readable_stream:
            downloaded_path = storage_bucket.write_file(readable_stream, target_path)

        return DownloadedVideo(
            id=video_id,
            downloaded_storage_path=StoragePath(
                storage_bucket_name=storage_bucket_name,
                path=downloaded_path,
            ),
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
