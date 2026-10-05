from enum import Enum


class StartMode(str, Enum):

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"


class StopMode(str, Enum):

    REVERSE = "reverse"

    PARALLEL = "parallel"