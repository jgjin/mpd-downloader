from pydantic_settings import BaseSettings

from queues.task_queue import TaskQueue


class WorkerSettings(BaseSettings):
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"

    task_queue: TaskQueue

    clearkey_id: str
    clearkey_value: str

    shaka_packager_path: str


_global_instance: WorkerSettings | None = None


def get_worker_settings() -> WorkerSettings:
    global _global_instance
    if _global_instance is None:
        _global_instance = WorkerSettings()

    return _global_instance
