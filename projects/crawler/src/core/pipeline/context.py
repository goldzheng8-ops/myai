from dataclasses import dataclass


@dataclass(slots=True)
class PipelineContext:
    """
    Pipeline上下文基类。

    不包含任何业务字段，仅作为泛型约束。
    """