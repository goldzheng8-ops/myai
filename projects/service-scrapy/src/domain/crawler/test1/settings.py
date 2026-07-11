# Scrapy settings for test1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#
#http://books.toscrape.com/ 和 https://quotes.toscrape.com/
#

BOT_NAME = "test1"

SPIDER_MODULES = ["test1.spiders"]
NEWSPIDER_MODULE = "test1.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "test1 (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# ITEM_PIPELINES = {
#     'scrapy.pipelines.images.ImagesPipeline': 1,
# }

# IMAGES_STORE = 'downloaded_images'  # 下载图片保存到此目录（自动创建）

# 可选：限制图片最小大小
# IMAGES_MIN_WIDTH = 100
# IMAGES_MIN_HEIGHT = 100

# settings.py
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'test1.middlewares.RandomUAMiddleware':402,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    # "test1.middlewares.PlaywrightAutoMiddleware": 543,
    # "scrapy_playwright.middleware.ScrapyPlaywrightDownloadHandler": 725,
    # "scrapy_playwright.middleware.ScrapyPlaywrightDownloaderMiddleware": 543,



}


# 你的代理池列表（可以是 IP:PORT，支持 HTTP/HTTPS）
ROTATING_PROXY_LIST = [
    "http://192.168.0.9:1081",
    "https://192.168.0.9:1081",
]

LOG_LEVEL = "DEBUG"
DUPEFILTER_DEBUG = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "test1.middlewares.Test1SpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "test1.middlewares.Test1DownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "test1.pipelines.Test1Pipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# FEEDS={
#     "book.json":{
#         "format":"json",
#         "overwrite":True,
#     }
# }
# FEED_EXPORT_ENCODING = "utf-8"
# DEFAULT_REQUEST_HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
#     'Referer': 'https://www.dushu.com/',  # 图片来源页面
# }


###########################################---scrapy-playwright--#######################################################

# DOWNLOAD_HANDLERS = {
#     "http":  "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"          # 或 "firefox" / "webkit"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000

# FEEDS = {
#     "data.csv": {
#         "format": "csv",
#         "overwrite": True,
#         "encoding": "utf-8",
#     }
# }

# LOG_LEVEL = "DEBUG"

###########################################################################################################################