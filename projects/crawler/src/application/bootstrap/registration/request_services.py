
from core.event import EventDispatcher
from core.provider import ProviderBuilder
from core.request.downloader.manager import DownloaderManager
from core.request.executor import RequestExecutor
from core.request.executor.downloader import DownloaderRequestExecutor
from core.request.middleware.chain_builder import MiddlewareChainBuilder
from core.request.runner import RequestRunner


def register_request_services(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        RequestExecutor,
        lambda resolver: DownloaderRequestExecutor(
            manager=resolver.resolve(
                DownloaderManager,
            ),
        ),

    )
    builder.add_factory(
        RequestRunner,
        lambda resolver: RequestRunner(
            executor=resolver.resolve(RequestExecutor),
            middleware=resolver.resolve(MiddlewareChainBuilder),
            dispatcher=resolver.resolve(EventDispatcher),
        ),
    )

