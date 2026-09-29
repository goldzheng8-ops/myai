from core.request.browser.interaction.context import BrowserInteractionContext
from core.request.browser.runtime_manager import BrowserRuntimeManager
from core.spider.services import SpiderServices
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

    def __init__(
        self,
        services: SpiderServices,
        manager: BrowserRuntimeManager,
    ) -> None:
        super().__init__(services)
        self._manager = manager

    async def process(
        self,
        *,
        context: SpiderContext[SearchSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:
        session_id=self._resolve_session_id(request)
        session_runtime=await self._manager.get_session(session_id=session_id)
        interaction_context = (
            BrowserInteractionContext[
                SearchSpiderConfig
            ](
                request=request,
                config=context.config,
                session_runtime=session_runtime
            )
        )

        await self._services.browser_interaction_engine.execute(
            interaction_context,
        )

        return RequestStep(
            request=request,
            outputs=context.config.outputs,
        )

    def _resolve_session_id(
        self,
        context: RequestContext,
    ) -> str:

        if context.session_id is not None:
            return context.session_id
        else:
            raise RuntimeError("require session id")

