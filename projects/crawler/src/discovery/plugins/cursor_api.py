

from discovery.base import DiscoveryPlugin
from enums.discovery_type import DiscoveryType


class CursorApiDiscovery(
    DiscoveryPlugin
):

    type = DiscoveryType.CURSOR_API


    async def discover(
        ...
    ):

        cursor = extract_cursor(
            response
        )


        descriptor = self.factory.api(
            url=config.url,
            params={
                "cursor":cursor
            },
            profile=config.profile,
        )


        return DiscoveryResult(
            requests=[
                descriptor
            ]
        )