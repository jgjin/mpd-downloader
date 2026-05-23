from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from activities.concatenate_segments import concatenate_segments
from activities.decrypt_representation import decrypt_representation
from activities.download_segment import download_segment
from activities.extract_representations import extract_representations
from activities.get_clearkey import get_clearkey
from activities.list_videos import list_videos
from activities.merge_representations import merge_representations
from queues.task_queue import TaskQueue
from workflows.download_representation import DownloadRepresentation
from workflows.download_video import DownloadVideo
from workflows.download_videos import DownloadVideos


@dataclass
class WorkerConfig:
    workflows: Sequence[type] = field(default_factory=list)
    activities: Sequence[Callable[..., Any]] = field(default_factory=list)

    max_concurrent_activities: int


QUEUE_WORKER_CONFIG: Mapping[TaskQueue, WorkerConfig] = {
    TaskQueue.SMALL_IO: WorkerConfig(
        workflows=[DownloadVideos, DownloadVideo, DownloadRepresentation],
        activities=[
            list_videos,
            get_clearkey,
            extract_representations,
            download_segment,
            concatenate_segments,
        ],
        max_concurrent_activities=30,
    ),
    TaskQueue.LARGE_PROCESSING: WorkerConfig(
        activities=[
            decrypt_representation,
            merge_representations,
        ],
        max_concurrent_activities=1,
    ),
}
