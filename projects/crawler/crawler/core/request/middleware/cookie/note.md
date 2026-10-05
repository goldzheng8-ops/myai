还有一个建议：不要在 CookieJar 里做 PSL

现在我不建议你在这里加入：

.com
.co.uk
.github.io

这种 Public Suffix List 判断。

RFC 确实要求用户代理对 public suffix 有额外处理，而且建议使用维护中的 PSL；但这应该属于后续独立的 CookieDomainPolicy / PublicSuffixMatcher 能力，而不是让 CookieJar 自己维护 PSL。

你现在框架的分层最好保持：

SetCookieParser
    │
    ├── syntax parsing
    ├── default domain/path
    └── basic domain validation
             │
             ▼
          Cookie
             │
             ▼
        CookieJar
             │
             ├── identity
             ├── replacement
             ├── deletion
             ├── domain matching
             ├── path matching
             ├── secure matching
             └── expiration

未来如果需要：

CookieDomainPolicy
        │
        └── Public Suffix List

再插进去。

还有一个我建议现在一起改掉的问题

你的 Cookie 现在：

expires: datetime | None

最好明确规定：

Framework 内部所有 datetime 必须是 timezone-aware UTC。

也就是说，在 Cookie 创建边界统一：

expires = expires.astimezone(
    timezone.utc,
)

不要允许：

datetime(2026, 9, 27, 12, 0)

这种 naive datetime 进入 Cookie。

否则以后：

cookie.expires <= now

很容易出现：

TypeError:
can't compare offset-naive and offset-aware datetimes

这应该成为 Cookie 模型的 invariant，而不是每个 Downloader 自己处理。