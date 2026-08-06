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