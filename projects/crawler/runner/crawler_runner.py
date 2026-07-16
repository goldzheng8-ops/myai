


request = (
    RequestBuilder()
    .from_config(config.request)
    .build()
)

result = downloader_engine.download(
    request,
    downloader_type=config.downloader,
)

data = extractor.extract(
    result.response,
    config.fields,
)