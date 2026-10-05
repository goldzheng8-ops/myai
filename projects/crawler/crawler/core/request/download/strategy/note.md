SimpleDownloadStrategy
ResumableDownloadStrategy
StreamingDownloadStrategy
ChunkedDownloadStrategy
ParallelDownloadStrategy

但是：

except DownloadError:
    return await self._fallback_to_full_download(...)

意味着：

任何 DownloadError 都自动 fallback。

例如：

chunk 0 下载成功
chunk 1 下载成功
chunk 2 磁盘写入失败
chunk 3 ...

如果 _chunk_store.write() 因为磁盘权限、磁盘满等原因最终被包装成 DownloadError，你的代码可能会重新执行一次完整 GET。

这不是理想行为。

所以我更建议把异常分成：

RangeUnsupportedError
ChunkDownloadError
DownloadStorageError
DownloadIncompleteError

其中只有真正属于：

Range 协议不可靠

的错误才 fallback。