SimpleDownloadStrategy
        ↓
body_bytes

StreamingDownloadStrategy
        ↓
body_stream

ResumableDownloadStrategy
        ↓
最终 body_bytes

例如：

class DownloadStrategyType(StrEnum):
    SIMPLE = "simple"
    RESUMABLE = "resumable"

配置：

download:
  strategy: resumable

或者：

download:
  strategy: simple

于是：

DownloadSpiderConfig
        │
        └── download.strategy

而不是：

DownloaderType

里增加：

httpx
httpx_resumable
httpx_stream
httpx_resume_stream
...

我建议下一步先不要做 S3 断点续传。**先把 SimpleDownloadStrategy + LocalResumeStore + ResumableDownloadStrategy 跑通，并把 DownloadRequestTemplate 改成调用 DownloadStrategy。等这一层稳定后，再决定是否增加 StreamingDownloadStrategy；否则现在同时处理 Range、stream、S3 multipart，会让架构一次跨太多边界。

另外，你当前 ResumableDownloadStrategy 还有一个值得马上修正的地方：**206 的 body 追加以后，应该验证 Content-Range 的起始位置确实等于 downloaded，否则可能出现服务端返回了错误 Range、重复追加数据但最终仍然看起来“下载完成”的情况。**这应该在下一步把 ResumableDownloadStrategy 完整收紧时一起处理。
8. 最后一个建议：ResumeStore 最好再增加 clear

你现在：

size()
append()
read()
delete()

已经够用。

但以后如果加入：

checksum
ETag
Last-Modified
.part 文件
.meta 文件

我建议接口逐渐变成：

class ResumeStore(Protocol):

    async def size(
        self,
        key: str,
    ) -> int:
        ...

    async def append(
        self,
        key: str,
        body: bytes,
    ) -> None:
        ...

    async def read(
        self,
        key: str,
    ) -> bytes:
        ...

    async def exists(
        self,
        key: str,
    ) -> bool:
        ...

    async def delete(
        self,
        key: str,
    ) -> None:
        ...

暂时不要加入过多方法。
这一层次现在已经比较稳定了。 下一步如果继续扩展，我建议不是再增加 Downloader，而是把 ResumableDownloadStrategy 的 ETag / Last-Modified / .part 元数据一致性补上。这样断点续传才真正从“能续”变成“安全地续”