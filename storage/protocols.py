from abc import abstractmethod
from typing import Protocol


class Storage(Protocol):
    @abstractmethod
    def list_directory(self, directory: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def read_file(self, file_path: str) -> str:
        raise NotImplementedError
