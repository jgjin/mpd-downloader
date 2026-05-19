import io
import subprocess
import tempfile

import structlog
from temporalio import activity

from schemas.storage import StoragePath
from schemas.video import ClearKey, ConcatenatedRepresentation, DecryptedRepresentation
from settings.worker_settings import global_instance as worker_settings
from storage.get_storage_bucket import get_storage_bucket

logger = structlog.get_logger()


@activity.defn
async def decrypt_representation(
    concatenated_representation: ConcatenatedRepresentation,
    clearkey: ClearKey,
) -> DecryptedRepresentation:
    video_id = concatenated_representation.video_id
    content_type = concatenated_representation.content_type
    concatenated_storage_path = concatenated_representation.concatenated_storage_path

    storage_bucket_name = concatenated_storage_path.storage_bucket_name
    storage_bucket = get_storage_bucket(storage_bucket_name)
    concatenated_path = concatenated_storage_path.path
    with (
        tempfile.NamedTemporaryFile(suffix=".mp4") as tmp_in,
        tempfile.NamedTemporaryFile(suffix=".mp4") as tmp_out,
    ):
        concatenated_stream = storage_bucket.read_file(concatenated_path)
        if not concatenated_stream:
            raise ValueError(
                f"no concatenated content to decrypt at {concatenated_storage_path}"
            )

        tmp_in_path = tmp_in.name
        with concatenated_stream, open(tmp_in_path, "wb") as w:
            while chunk := concatenated_stream.read(io.DEFAULT_BUFFER_SIZE):
                w.write(chunk)

        tmp_out_path = tmp_out.name
        decrypt_command = [worker_settings.shaka_packager_path]
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
                storage_bucket_name=storage_bucket_name,
                concatenated_path=concatenated_path,
                decrypt_command=decrypt_command,
                stderr=result.stderr,
            )
            raise RuntimeError(f"decryption of {concatenated_storage_path} failed")

        target_path = f"{video_id}/{content_type}/decrypted.mp4"
        with open(tmp_out_path, "rb") as readable_stream:
            decrypted_path = storage_bucket.write_file(readable_stream, target_path)

        return DecryptedRepresentation(
            video_id=video_id,
            content_type=content_type,
            decrypted_storage_path=StoragePath(
                storage_bucket_name=storage_bucket_name,
                path=decrypted_path,
            ),
        )
