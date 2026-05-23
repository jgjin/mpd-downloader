from abc import abstractmethod
from types import TracebackType
from typing import Protocol, Self, Type


class ReadableStream(Protocol):
    @abstractmethod
    def read(self, size: int | None = None) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        self.close()

        return None


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
