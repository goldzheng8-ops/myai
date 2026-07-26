

class ExtractorPlugin(
    Plugin,
    Generic[ConfigT],
    ABC,
):

    extractor_type: ClassVar[ExtractorType]

    config_type: ClassVar[type[ConfigT]]

    @abstractmethod
    async def extract(...)