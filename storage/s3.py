import boto3
from botocore.client import BaseClient
from botocore.response import StreamingBody

from storage.protocols import ReadableStream, StorageBucket


class S3ReadableStream(ReadableStream):
    def __init__(self, streaming_body: StreamingBody):
        self.streaming_body = streaming_body

    def read(self, size: int | None = None) -> bytes:
        return self.streaming_body.read(size)

    def close(self) -> None:
        self.streaming_body.close()


# boto does not provide a more precise type for S3 client
S3Client = BaseClient


class S3ChainedReadableStream(ReadableStream):
    def __init__(self, s3_client: S3Client, bucket_name: str, part_paths: list[str]):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.part_paths = part_paths

        self.current_index = 0
        self.current_stream = self.read_part(self.current_index)

    def read(self, size: int | None = None) -> bytes:
        """
        Reads up to `size` bytes from parts or returns empty bytes if all parts fully read.
        """
        if size is None:
            raise ValueError("size must be specified")

        while self.current_stream is not None:
            if chunk := self.current_stream.read(size):
                return chunk

            self.current_stream.close()
            self.current_index += 1
            self.current_stream = self.read_part(self.current_index)

        return b""

    def close(self) -> None:
        if self.current_stream is not None:
            self.current_stream.close()
            self.current_stream = None

    def read_part(self, index: int) -> ReadableStream | None:
        if not (0 <= index < len(self.part_paths)):
            return None

        part_path = self.part_paths[index]
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=part_path)

        return S3ReadableStream(response["Body"])


class S3StorageBucket(StorageBucket):
    def __init__(self, bucket_name: str):
        self.s3_client: S3Client = boto3.client("s3")
        self.bucket_name = bucket_name

    def list_files(self) -> list[str]:
        files = []

        paginator = self.s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket_name):
            files.extend(
                [
                    obj["Key"]
                    for obj in page.get("Contents", [])
                    if not obj["Key"].endswith("/")
                ]
            )

        return files

    def read_file(self, file_path: str) -> ReadableStream | None:
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_path)

        return S3ReadableStream(response["Body"])

    def write_file(self, readable_stream: ReadableStream, target_path: str) -> str:
        with readable_stream as r:
            self.s3_client.upload_fileobj(r, self.bucket_name, target_path)

        return target_path

    def concat_files(self, part_paths: list[str], target_path: str) -> str:
        chained_readable_stream = S3ChainedReadableStream(
            self.s3_client, self.bucket_name, part_paths
        )
        with chained_readable_stream as r:
            self.s3_client.upload_fileobj(r, self.bucket_name, target_path)

        return target_path
