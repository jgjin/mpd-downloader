import io
from pathlib import Path

from storage.protocols import ReadableStream, StorageBucket


class LocalStorageBucket(StorageBucket):
    def __init__(self, root: str):
        self.root = Path(root)

        self.root.mkdir(exist_ok=True)

    def list_files(self) -> list[str]:
        return [
            str(f.relative_to(self.root)) for f in self.root.iterdir() if f.is_file()
        ]

    def read_file(self, file_path: str) -> ReadableStream | None:
        path = self.root / file_path
        if not path.is_file():
            return None

        return path.open("rb")

    def write_file(self, readable_stream: ReadableStream, target_path: str) -> str:
        path = self.root / target_path
        path.parent.mkdir(parents=True, exist_ok=True)

        with readable_stream as r, path.open("wb") as w:
            while chunk := r.read(io.DEFAULT_BUFFER_SIZE):
                w.write(chunk)

        return str(path.relative_to(self.root))

    def concat_files(self, part_paths: list[str], target_path: str) -> str:
        path = self.root / target_path
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as w:
            for part_path in part_paths:
                with self.read_file(part_path) as r:
                    while chunk := r.read(io.DEFAULT_BUFFER_SIZE):
                        w.write(chunk)

        return str(path.relative_to(self.root))
