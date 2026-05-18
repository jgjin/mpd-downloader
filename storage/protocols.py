from abc import abstractmethod
from typing import Protocol


class ReadableStream(Protocol):
    @abstractmethod
    def read(self, size: int | None = None) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class StorageBucket(Protocol):
    @abstractmethod
    def list_files(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def read_file(self, file_path: str) -> ReadableStream | None:
        raise NotImplementedError

    @abstractmethod
    def write_file(self, readable_stream: ReadableStream, target_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def concat_files(self, part_paths: list[str], target_path: str) -> str:
        raise NotImplementedError
