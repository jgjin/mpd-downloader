from pydantic_settings import BaseSettings

from queues.task_queue import TaskQueue


class WorkerSettings(BaseSettings):
    task_queue: TaskQueue

    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"

    clearkey_id: str
    clearkey_value: str

    shaka_packager_path: str


global_instance = WorkerSettings()
