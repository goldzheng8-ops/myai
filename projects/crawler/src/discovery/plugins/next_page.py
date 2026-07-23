class NextPageDiscovery(
    DiscoveryPlugin
):

    type = DiscoveryType.NEXT_PAGE


    async def discover(
        self,
        *,
        response,
        context,
        config,
    ):

        next_url = await response.css(
            config.selector
        )

        return DiscoveryResult(
            requests=[
                self.factory.list(
                    url=next_url,
                    profile=context.profile,
                )
            ]
        )