from enum import Enum


class JobType(str, Enum):

    REPOSITORY_INDEX = "repository_index"


class JobStatus(str, Enum):

    QUEUED = "queued"

    CLAIMED = "claimed"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"