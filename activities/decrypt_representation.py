import io
import os
import subprocess
import tempfile

import structlog
from temporalio import activity

from schemas.video import ClearKey, ConcatenatedRepresentation, DecryptedRepresentation
from storage.get_storage import get_storage

logger = structlog.get_logger()


@activity.defn
async def decrypt_representation(
    representation: ConcatenatedRepresentation, clearkey: ClearKey
) -> DecryptedRepresentation:
    video_id = representation.video_id
    content_type = representation.content_type
    concatenated_path = representation.concatenated_path

    storage = get_storage()
    with (
        tempfile.NamedTemporaryFile(suffix=".mp4") as tmp_in,
        tempfile.NamedTemporaryFile(suffix=".mp4") as tmp_out,
    ):
        concatenated_stream = storage.read_file(concatenated_path)
        if not concatenated_stream:
            raise ValueError(f"no concatenated content at {concatenated_path}")

        tmp_in_path = tmp_in.name
        with concatenated_stream, open(tmp_in_path, "wb") as w:
            while chunk := concatenated_stream.read(io.DEFAULT_BUFFER_SIZE):
                w.write(chunk)

        tmp_out_path = tmp_out.name
        decrypt_command = [os.environ["SHAKA_PACKAGER_PATH"]]
        decrypt_command.append(
            ",".join(
                [
                    f"input={tmp_in_path}",
                    f"stream={content_type}",
                    f"output={tmp_out_path}",
                ]
            )
        )
        decrypt_command.extend(
            [
                "--enable_raw_key_decryption",
                f"--key={clearkey.key_value}",
                f"--key_id={clearkey.key_id}",
            ]
        )

        result = subprocess.run(decrypt_command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(
                "decryption failed",
                concatenated_path=concatenated_path,
                decrypt_command=decrypt_command,
                stderr=result.stderr,
            )
            raise RuntimeError(f"decryption of {concatenated_path} failed")

        target_path = f"segments/{video_id}/{content_type}/decrypted.mp4"
        with open(tmp_out_path, "rb") as readable_stream:
            decrypted_path = storage.write_file(readable_stream, target_path)

        return DecryptedRepresentation(
            video_id=video_id,
            content_type=content_type,
            decrypted_path=decrypted_path,
        )
