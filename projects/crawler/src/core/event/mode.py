from enum import Enum


class DispatchMode(str, Enum):

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"

class ProviderMode(str, Enum):

    TRANSIENT = "transient"

    SINGLETON = "singleton"