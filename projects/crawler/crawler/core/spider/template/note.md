class OutputEngine:

    def __init__(
        self,
        resolver: OutputResolver,
    ) -> None:
        self._resolver = resolver

    async def write(
        self,
        item: OutputItem,
        outputs: Sequence[str],
    ) -> None:

        for name in outputs:
            sink = self._resolver.resolve(name)
            await sink.write(item)
-----------------------------------------------
@dataclass(frozen=True, slots=True)
class ExtractionResult:
    item: Mapping[str, Any]
    outputs: tuple[str, ...] = ()
----------------------------------------------------
class SpiderResult:
    item: OutputItem
    outputs: tuple[str, ...]
-------------------------------------------------
result = await self._extractor.extract(...)

item = OutputItem(
    data=result.data,
    spider=spider.name,
    request=context.descriptor,
)

await self._output.write(
    item,
    outputs=result.outputs,
)