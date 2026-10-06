# 项目 API 参考约束

## 版本基线

```text
pandas = "3.0.6"
duckdb = "1.5.6"
matplotlib = "3.11.2"
```

以后如果让 AI 微调代码，最好严格以这三个版本的官方文档为准，不要让它凭经验去套用其他版本的 API。

---

## 结论

我查了官方文档，这三个版本都能直接对应到官方资料，因此可以作为当前项目的稳定技术参考源。

---

## 1. pandas 3.0.6

### 官方链接

- API Reference: https://pandas.pydata.org/docs/reference/index.html
- User Guide: https://pandas.pydata.org/docs/user_guide/index.html
- 版本首页: https://pandas.pydata.org/pandas-docs/stable/index.html

### 说明

这部分适用于当前项目中所有 DataFrame / Series / GroupBy / Resampling / IO 相关的操作。

官方也特别说明：

- `pandas.core` 和 `pandas.compat` 属于私有 API
- 不应作为项目代码的依据

此外，pandas 3.0 版本中还包括：

- 迁移说明
- 默认 string dtype 相关变化
- 相关 API 行为调整

这意味着以后微调代码时，AI 必须优先参考 3.0.6 对应官方文档，而不是混用旧版本习惯。

---

## 2. DuckDB 1.5.6

### 官方链接

- Python API: https://duckdb.org/docs/current/clients/python/overview

### 说明

这份文档非常适合当前项目，因为它正好覆盖了我们现在会用到的语法：

- `duckdb.connect()`
- `duckdb.sql()`
- `connection.sql()`
- `connection.execute()`
- `connection.register()`
- `relation.df()`

同时也涵盖了：

- DataFrame
- Arrow
- Polars
- CSV / Parquet / JSON
- 参数绑定
- 持久化 `.duckdb`
- in-memory database
- connection 生命周期

官方建议实际应用中使用 `duckdb.connect()` 创建独立 connection，而不是依赖模块级全局连接对象。

---

## 3. Matplotlib 3.11.2

### 官方链接

- API Reference: https://matplotlib.org/3.11.2/api/index.html
- 官方首页: https://matplotlib.org/stable/index.html

### 说明

这份文档对当前项目非常关键，因为我们刚设计的：

```python
project.plot(...)
```

最终就是建立在这里的 API 之上。

Matplotlib 官方文档明确区分了两套接口：

### Object-oriented API

```python
fig, ax = plt.subplots()
ax.plot(...)
ax.set_title(...)
```

### pyplot API

```python
plt.plot(...)
plt.title(...)
```

对于这个项目，建议统一优先使用 Object-oriented API。官方文档也默认以 `Figure` 和 `Axes` 作为显式对象接口。

此外，Matplotlib 3.11 也存在一些 API 行为变化，因此以后微调代码时，最好不要让 AI 根据旧版习惯直接修改。

---

## 4. 项目技术分层约束

可以把整个数据分析项目抽象为这样一个简单规则：

```text
Python
├── pandas 3.0.6
│   └── 数据处理 / DataFrame
├── DuckDB 1.5.6
│   └── SQL / 数据查询
└── Matplotlib 3.11.2
    └── 可视化
```

---

## 5. AI 修改代码的统一约束

以后 AI 修改代码时，可以直接使用这条统一约束：

> 本项目严格使用 pandas 3.0.6、DuckDB 1.5.6、Matplotlib 3.11.2。涉及这三个库的 API 时，优先依据对应版本的官方 API Reference，而不是根据其他版本的 API 猜测。保持现有代码风格，优先修正类型问题和 API 使用方式，不进行无必要的架构重构。

---

## 6. 实际工作方式建议

这套方式非常适合当前的协作模式：

- 你负责判断“要改什么”
- AI 负责根据官方文档确认“怎么改”

在具体修正时，直接针对这些 API 逐项查官方文档即可：

- `DataFrame.groupby()`
- `read_excel()`
- `duckdb.Connection.execute()`
- `Axes.plot()`

这样能最大程度减少 API 误用和版本不一致带来的问题。

---

## 7. 结论

这三个官方文档已经足够作为当前项目的主要技术参考，不必把整个文档库下载进项目。后续每次针对具体 API 做修改时，都直接对照对应版本的官方文档来调整即可。