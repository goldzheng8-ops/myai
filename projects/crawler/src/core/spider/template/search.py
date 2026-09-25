from core.request.browser.interaction.context import BrowserInteractionContext
from core.request.middleware.session.middleware import SESSION_RUNTIME_KEY
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
        session = request.runtime.get(
            SESSION_RUNTIME_KEY,
        )
        if not isinstance(session, Session):
            raise RuntimeError(
                "Browser interaction requires "
                "an active session.",
            )
        page = await self._runtime_manager.get_page(
            session_id=session.id,
        )
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