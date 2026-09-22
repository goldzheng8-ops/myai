# 安装 aria2c


aria2 本质上不是 HTTP response source，而是 download artifact source。

所以如果你的 ResponseAdapter 强制要求：

status_code
headers
cookies

那只是为了适配现有 pipeline。

我建议第一版允许它使用：

status_code = 200
headers = {}
cookies = {}

但在 meta 中明确：

{
    "downloader": "aria2",
    "transport": "aria2",
}

这样不会污染 HTTPX 的语义。

Aria2DownloaderConfig
│
├── RPC 配置
│   ├── rpc_url
│   └── rpc_secret
│
├── Downloader 调度配置
│   └── max_concurrency
│
├── 文件行为
│   ├── download_directory
│   ├── continue_download
│   ├── allow_overwrite
│   ├── auto_file_renaming
│   └── check_integrity
│
├── 网络
│   ├── proxy
│   └── connect_timeout
│
└── RPC timeout
    └── timeout