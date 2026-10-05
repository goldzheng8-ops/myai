from core.request.context import RequestContext
from core.request.browser.runtime_manager import BrowserRuntimeManager
from core.request.middleware.auth.model import BrowserAuthState



    
class BrowserAuthStateProvider:

    def __init__(
        self,
        browser_runtime: BrowserRuntimeManager,
    ) -> None:
        self._browser_runtime = browser_runtime

    async def get_state(
        self,
        *,
        context: RequestContext,
    ) -> BrowserAuthState:

        session_id = context.session_id

        if session_id is None:
            return BrowserAuthState()

        session = await self._browser_runtime.get_session(
            session_id=session_id,
        )

        return BrowserAuthState(
            cookies=await self._browser_runtime.get_cookies(
                session,
                context.descriptor.url,
            ),
            local_storage=await self._browser_runtime.get_local_storage(
                session,
            ),
            session_storage=await self._browser_runtime.get_session_storage(
                session,
            ),
        )