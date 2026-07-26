

class ValueExtractor:

    def __init__(
        self,
        selector_engine: SelectorEngine,
    ) -> None:

        self._selector_engine = selector_engine

    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        config: FieldConfig,
    ) -> Any:
            return await self.resolve_source(
                response=response,
                context=context,
                config=config,
            )
    async def resolve_source(...):

        if config.selector is not None:

            return await self.select(...)

        return context.value