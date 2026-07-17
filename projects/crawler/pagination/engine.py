class PaginationEngine:

    def __init__(self):
        self.registry = PaginationRegistry()

    async def paginate(
        self,
        response,
        request,
        configs,
    ):
        result = PaginationResult()

        for config in configs:

            plugin = self.registry.get(config.type)

            r = await plugin.paginate(
                response,
                request,
                config,
            )

            result.requests.extend(r.requests)

            result.has_next |= r.has_next

        return result