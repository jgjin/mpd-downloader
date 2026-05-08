import io
from pathlib import Path

from storage.protocols import ReadableStream, Storage


class LocalStorage(Storage):
    def list_directory(self, directory: str) -> list[str]:
        path = Path(directory)
        if not path.is_dir():
            return []

        return [str(f) for f in path.iterdir() if f.is_file()]

    def read_file(self, file_path: str) -> ReadableStream | None:
        path = Path(file_path)
        if not path.is_file():
            return None

        return path.open("rb")

    def write_file(self, readable_stream: ReadableStream, target_path: str) -> str:
        path = Path(target_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with readable_stream as r, path.open("wb") as w:
            while chunk := r.read(io.DEFAULT_BUFFER_SIZE):
                w.write(chunk)

        return str(path)

    def concat_files(self, part_paths: list[str], target_path: str) -> str:
        path = Path(target_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as w:
            for part_path in part_paths:
                with self.read_file(part_path) as r:
                    while chunk := r.read(io.DEFAULT_BUFFER_SIZE):
                        w.write(chunk)

        return str(path)
