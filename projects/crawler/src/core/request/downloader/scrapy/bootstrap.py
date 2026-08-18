from scrapy.utils.reactor import install_reactor

def install_scrapy_reactor() -> None:
    install_reactor(
        "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    )