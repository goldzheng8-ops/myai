from enum import Enum


class DownloadStrategyType(str,Enum):
    SIMPLE = "simple"
    RESUMABLE = "resumable"