from enum import StrEnum


class TaskQueue(StrEnum):
    SMALL_IO = "small-io-queue"
    LARGE_PROCESSING = "large-processing-queue"
