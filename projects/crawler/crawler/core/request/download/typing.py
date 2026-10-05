from enum import Enum


class DownloadStrategyType(str,Enum):
    SIMPLE = "simple"
    RESUMABLE = "resumable"
    STREAMING = "streaming"
    CHUNKED = "chunked"
    PARALLEL = "parallel"