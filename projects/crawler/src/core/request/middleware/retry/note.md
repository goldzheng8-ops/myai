一个生产级建议：现在先不要加指数退避

你后面很可能会想到：

delay
backoff
jitter

但我建议暂时不要把它们塞进 RetryMiddleware。

以后可以演进成：

RetryPolicy
    │
    ├── max_attempts
    └── RetryDelayStrategy
             │
             ├── Fixed
             ├── Exponential
             └── ExponentialJitter

现在：

delay: float

只是一个最小可用实现。

这样未来升级不会破坏：

RetryMiddleware

本身的职责。