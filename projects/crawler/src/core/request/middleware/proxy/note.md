不要把这个逻辑散落到每个 Downloader。

可以提供一个小的辅助函数

def get_proxy(
    context: RequestContext,
) -> ProxyConfig | None:

    value = context.runtime.get(
        PROXY_RUNTIME_KEY,
    )

    if value is None:
        return None

    if not isinstance(value, ProxyConfig):
        raise TypeError(
            "Invalid request proxy runtime value."
        )

    return value

不过这个辅助函数应该属于 request runtime / transport infrastructure，而不是 ProxyMiddleware。