
class MiddlewareRegistry(
    MultiRegistry[
        PipelineStage,
        type[PipelineMiddleware],
    ],
):
    pass