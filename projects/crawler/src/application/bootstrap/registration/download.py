from application.config.model import ApplicationConfig
from core.request.download.factory import DownloadStrategyFactory
from core.request.download.resume.store import ResumeStore
from core.provider import ProviderBuilder
from core.request.download.resume.local import LocalResumeStore
from core.request.middleware.fingerprint.provider import FingerprintProvider

def register_download(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_factory(
        ResumeStore,
        lambda resolver: LocalResumeStore(
            directory=config.resume.directory,
        ),
    )

    builder.add_factory(
        DownloadStrategyFactory,
        lambda resolver: DownloadStrategyFactory(
            resume_store=resolver.resolve(
                ResumeStore,
            ),
            fingerprint_provider=resolver.resolve(
                FingerprintProvider,
            ),
        ),
    )

