from enum import StrEnum


class MergePolicy(StrEnum):

    MERGE = "merge"

    REPLACE = "replace"

    IGNORE = "ignore"

    REMOVE = "remove"