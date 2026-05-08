from pathlib import Path

from storage.protocols import Storage


class LocalStorage(Storage):
    def list_directory(self, directory: str) -> list[str]:
        path = Path(directory)
        if not path.is_dir():
            return []

        return [str(f) for f in path.iterdir() if f.is_file()]

    def read_file(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.is_file():
            return ""

        return path.read_text(encoding="utf-8")
