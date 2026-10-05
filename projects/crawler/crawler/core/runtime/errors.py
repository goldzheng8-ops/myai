class ResolveError(Exception):
    pass


class InvalidExpressionError(
    ResolveError,
):
    pass


class AccessorNotFoundError(
    ResolveError,
):
    pass


class PathNotFoundError(
    ResolveError,
):
    pass

class ContextMergeConflictError(
    RuntimeError,
):
    """
    Raised when RuntimeContext merge encounters
    conflicting values.
    """

    def __init__(
        self,
        conflicts: tuple[str, ...],
    ) -> None:

        self.conflicts = conflicts

        super().__init__(
            "Context merge conflict for keys: "
            f"{conflicts!r}"
        )