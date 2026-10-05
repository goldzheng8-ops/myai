from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.base import AuthCredentials, BaseAuthProvider
from core.request.middleware.auth.auth_provider.config import OAuth2CredentialsProviderConfig

from core.request.middleware.auth.auth_provider.oauth2.initial import OAuth2InitialTokenLoader
from core.request.middleware.auth.auth_provider.oauth2.refresher import OAuth2TokenRefresher



class OAuth2CredentialsProvider(
    BaseAuthProvider[OAuth2CredentialsProviderConfig],
):

    def __init__(
        self,
        token_refresher: OAuth2TokenRefresher,
        initial_token_loader: OAuth2InitialTokenLoader,
        config: OAuth2CredentialsProviderConfig,
    ) -> None:
        super().__init__(config)

        self._token_refresher = token_refresher
        self._initial_token_loader = initial_token_loader

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials | None:

        session_id = context.session_id

        if session_id is None:
            return None

        token_set = await self._token_refresher.get_valid(
            session_id=session_id,
            key=self._config.provider_key,
            initial_token_loader=(
                lambda: self._initial_token_loader.load(
                    context,
                )
            ),
            leeway=self._config.refresh_leeway,
        )

        return AuthCredentials(
            headers={
                "Authorization": (
                    f"{token_set.token_type} "
                    f"{token_set.access_token}"
                ),
            },
        )