from __future__ import annotations

import pytest

from core.pipeline_framework import (
    Pipeline,
    PipelineBuilder,
    PipelineContext,
    PipelinePass,
    PipelineStage,
    PipelineStep,
)


class DemoContext(PipelineContext):
    pass


class AddValuePass(PipelinePass[DemoContext]):
    def __init__(self, key: str, value: int) -> None:
        super().__init__(name=f"add_{key}")
        self.key = key
        self.value = value

    async def process(self, context: DemoContext, next_step):
        context.data[self.key] = context.data.get(self.key, 0) + self.value
        return await next_step(context)


class MultiplyPass(PipelinePass[DemoContext]):
    async def process(self, context: DemoContext, next_step):
        context.data["total"] = context.data.get("total", 1) * 2
        return await next_step(context)


class FinalStep(PipelineStep[DemoContext]):
    async def execute(self, context: DemoContext) -> DemoContext:
        context.data["final"] = context.data.get("total", 0)
        return context


@pytest.mark.asyncio
async def test_pipeline_builder_and_execution() -> None:
    builder = PipelineBuilder[DemoContext]()
    builder.add_stage(
        PipelineStage[DemoContext](
            "demo",
            [
                AddValuePass("total", 3),
                MultiplyPass(),
            ],
        )
    )
    builder.add_step(FinalStep("final_step"))

    pipeline = builder.build()
    context = DemoContext(data={"total": 1})

    result = await pipeline.execute(context)

    assert result.data["total"] == 8
    assert result.data["final"] == 8


def test_pipeline_graph_and_registry_basic() -> None:
    stage1 = PipelineStage[DemoContext]("first")
    stage2 = PipelineStage[DemoContext]("second")

    stage1.add(AddValuePass("count", 1))
    stage2.add(MultiplyPass())

    graph = stage1.graph()
    graph.add_stage(stage2)
    graph.connect("first", "second")

    assert graph.contains("first")
    assert graph.contains("second")
    assert graph.topological_order() == ["first", "second"]
