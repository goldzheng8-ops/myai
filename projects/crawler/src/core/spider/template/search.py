from core.request.browser.interaction.context import BrowserInteractionContext
from core.spider.typing import SpiderTemplate
from core.request.context import RequestContext
from core.spider.context import SpiderContext
from core.spider.step import RequestStep
from core.spider.config import SearchSpiderConfig
from core.spider.template.base import RequestTemplate



class SearchRequestTemplate(
    RequestTemplate[SearchSpiderConfig],
):

    plugin_type = SpiderTemplate.SEARCH

    async def process(
        self,
        *,
        context: SpiderContext[SearchSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        interaction_context = (
            BrowserInteractionContext[
                SearchSpiderConfig
            ](
                request=request,
                config=context.config,
            )
        )

        await self._services.browser_interaction_engine.execute(
            interaction_context,
        )

        return RequestStep(
            request=request,
            outputs=context.config.outputs,
        )