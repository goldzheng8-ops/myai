from application.config.model import ApplicationConfig
from core.request.download.chunk.local import LocalChunkStore
from core.request.download.chunk.planner import ChunkPlanner, FixedChunkPlanner
from core.request.download.chunk.store import ChunkStore
from core.request.download.factory import DownloadStrategyFactory
from core.request.download.range.parser import RangeParser
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
        ChunkStore,
        lambda resolver: LocalChunkStore(
            directory=config.chunk.directory,
        ),
    )
    builder.add_type(
        ChunkPlanner,
        FixedChunkPlanner,
    )
    builder.add_type(
        RangeParser,
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
            range_parser=resolver.resolve(
                RangeParser,
            ),
            chunk_planner=resolver.resolve(
                ChunkPlanner,
            ),
            chunk_store=resolver.resolve(
                ChunkStore,
            ),
            chunk_size=config.download_strategy.chunk_size,
            parallel_max_concurrency=config.download_strategy.parallel_max_concurrency
        ),
    )

