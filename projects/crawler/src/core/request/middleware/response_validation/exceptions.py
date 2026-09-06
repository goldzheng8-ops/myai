class ResponseValidationError(RuntimeError):
    def __init__(
        self,
        *,
        url: str,
        reason: str,
        status_code: int | None = None,
    ) -> None:
        self.url = url
        self.reason = reason
        self.status_code = status_code

        super().__init__(
            "Response validation failed: "
            f"url={url!r}, "
            f"reason={reason}",
        )