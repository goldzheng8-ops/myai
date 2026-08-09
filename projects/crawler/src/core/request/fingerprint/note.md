DefaultFingerprint
NormalizedFingerprint
ScrapyCompatibleFingerprint
CustomFingerprint

FingerprintMiddleware
        │
        ▼
FingerprintStrategy
        │
        ├── normalize_url()
        ├── normalize_params()
        └── normalize_body()

FingerprintMiddleware
        │
        │ 计算
        ▼
     fingerprint
        │
        ▼
DeduplicateMiddleware
        │
        │ 查询
        ▼
    是否正在执行？

Middleware 我建议至少有下面这些测试：

1. 相同 Request → 相同 fingerprint

2. URL 不同 → fingerprint 不同

3. Method 不同 → fingerprint 不同

4. Params 不同 → fingerprint 不同

5. Body 不同 → fingerprint 不同

6. Params key 顺序不同 → fingerprint 相同

7. Mapping body key 顺序不同 → fingerprint 相同

8. Sequence 顺序不同 → fingerprint 不同

9. Header 不同 → fingerprint 相同

10. Cookie 不同 → fingerprint 相同

11. Proxy 不同 → fingerprint 相同

12. Middleware 将 fingerprint 写入 context.meta

13. Middleware 调用 next()

14. Middleware 无共享状态，可并发执行