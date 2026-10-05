为什么不急着定义很多 Protocol？

因为目前 Downloader 的核心抽象已经是：

DownloaderPlugin

后面如果确实需要：

BrowserManager
RequestClient
ResponseBuilder

再定义对应 Protocol。

五、这里暂时不要加入 __aenter__

例如不要现在就：

async with downloader:

因为 Registry 以后管理的是多个 Downloader。

生命周期到底由：

Application
Runner
DownloaderManager
Registry

哪个组件负责，我们可以在三个 Downloader 实现完成后再确定。

现在只冻结：

start()
close()

就足够。