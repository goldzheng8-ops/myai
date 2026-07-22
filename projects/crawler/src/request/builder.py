from discovery.delta import DiscoveryItem
from request.context import RequestContext
from request.enums import RequestTemplate


class RequestBuilder:

    _builders = {
        RequestTemplate.HTML: HtmlBuilder(),
        RequestTemplate.JSON_API: JsonApiBuilder(),
        RequestTemplate.GRAPHQL: GraphqlBuilder(),
        RequestTemplate.PLAYWRIGHT: PlaywrightBuilder(),
    }

    def build(
        self,
        parent: RequestContext,
        item: DiscoveryItem,
    ) -> RequestContext:

        builder = self._builders[item.template]

        return builder.build(parent, item)