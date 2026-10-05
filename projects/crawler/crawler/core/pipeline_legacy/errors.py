class PipelineError(Exception):
    """Base exception for pipeline-related errors."""


class PipelineStageError(PipelineError):
    """Raised when a stage cannot be resolved or executed."""


class PipelineNotFoundError(PipelineError, LookupError):
    """Raised when a pipeline or stage is missing from a registry/manager."""


class PipelineGraphCycleError(PipelineError):
    """Raised when a pipeline graph contains a dependency cycle."""

class PipelineBuildError(PipelineError):
    pass


class PipelineExecutionError(PipelineError):
    pass


class StageNotFoundError(PipelineError):
    pass


class StepNotFoundError(PipelineError):
    pass

class PipelineCancelledError(PipelineError):
    """
    Pipeline execution has been cancelled.
    """


class PipelineConfigurationError(PipelineError):
    """
    Invalid pipeline definition.
    """

