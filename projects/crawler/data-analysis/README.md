# 数据分析 Notebook 框架说明

本文档对应的核心实现位于 `data-analysis/notebooks/notebook_framework.py`。该模块是一个面向数据分析与报表展示的 Python 工具集，主要用于：

- 统一定位和加载项目中的数据文件
- 使用 DuckDB 执行 SQL 查询
- 对表格数据做汇总、趋势、相关性和分布分析
- 处理漏斗、归因、用户分群、AB 测试等业务分析场景
- 构建仪表盘和各类图表

## 1. 模块总体职责

这个文件提供了一组“分析器 + 可视化工具 + 仪表盘构建器”，核心分为几类：

1. 数据加载与查询层：`NotebookProject`、`load_data`、`query`、`query_df`、`query_file`、`query_csv`
2. 数据汇总与描述层：`summarize_by`、`top_by`、`describe_numeric`、`correlation_matrix`、`time_series_summary`
3. 业务分析层：`funnel_analysis`、`user_segmentation`、`attribution_summary`、`conversion_rate_by`、`cohort_analysis`、`ab_test_summary`、`funnel_comparison`、`attribution_breakdown`
4. 统计与预测层：`linear_regression`、`forecast_metric`、`distribution_summary`、`period_over_period_growth`
5. 绘图与报表层：`plot`、`plot_summary`、`plot_metric_comparison`、`kpi_monitor_table`、`build_report_table`
6. 仪表盘生成层：`build_growth_dashboard`、`build_operational_dashboard`

---

## 2. API 文档索引（函数索引 + 参数说明）

下面按“函数分类 + 参数清单”的方式整理，适合直接作为 API 参考文档使用。

### 2.1 数据加载与查询类

| 函数 | 签名 | 作用 | 关键参数 |
| --- | --- | --- | --- |
| `NotebookProject` | `NotebookProject(repo_root, data_dir=None)` | 项目级数据入口 | `repo_root`, `data_dir` |
| `resolve_data_file` | `resolve_data_file(filename)` | 在项目中搜索数据文件 | `filename` |
| `load_data` | `load_data(filename, *, kind=None, sheet_name=0, **kwargs)` | 自动识别文件类型并读取 | `filename`, `kind`, `sheet_name` |
| `query` | `query(sql, *, tables=None)` | 执行多表 DuckDB SQL | `sql`, `tables` |
| `query_df` | `query_df(sql, data, *, name="data")` | 对内存 DataFrame 执行 SQL | `sql`, `data`, `name` |
| `query_file` | `query_file(sql, filename)` | 对文件路径执行 SQL 读取逻辑 | `sql`, `filename` |
| `query_csv` | `query_csv(sql, filename)` | 读取 CSV 并转成 DuckDB 视图 | `sql`, `filename` |
| `plot` | `plot(data, *, x_col, y_col, kind="bar", title=None, xlabel=None, ylabel=None, figsize=(8, 5))` | 画通用基础图表 | `data`, `x_col`, `y_col`, `kind` |

#### 关键参数说明

- `repo_root`: 仓库根目录，通常为 `Path`。
- `data_dir`: 自定义数据目录，若为空则默认使用 `repo_root / "data"`。
- `kind`: 手工指定读取类型，可覆盖文件扩展名推断。
- `tables`: 传入 `{table_name: DataFrame}`，用于 SQL 联表查询。
- `sheet_name`: 用于 Excel 读取时指定工作表。
- `kind` 支持：`"csv"`, `"json"`, `"jsonl"`, `"xlsx"`, `"xls"`。

#### 典型调用

```python
from pathlib import Path
from data_analysis.notebooks.notebook_framework import NotebookProject

project = NotebookProject(repo_root=Path("."), data_dir=Path("data"))

df = project.load_data("news.csv")
result = project.query_df(
    "SELECT channel, SUM(revenue) AS total_revenue FROM data GROUP BY channel",
    df,
    name="data",
)
```

---

### 2.2 汇总与描述类

| 函数 | 签名 | 作用 | 关键参数 |
| --- | --- | --- | --- |
| `summarize_by` | `summarize_by(data, *, group_by, value_col, ascending=False, agg="sum")` | 按分组汇总数值字段 | `group_by`, `value_col`, `agg` |
| `top_by` | `top_by(data, *, group_by, value_col, top_n=5, ascending=False, agg="sum")` | 取 Top N 分组 | `top_n` |
| `describe_numeric` | `describe_numeric(data, *, columns=None)` | 输出数值列统计摘要 | `columns` |
| `correlation_matrix` | `correlation_matrix(data, *, columns=None, method="pearson")` | 计算相关系数矩阵 | `method` |
| `time_series_summary` | `time_series_summary(data, *, date_col, value_col, group_by=None, freq="D", aggfunc="sum")` | 按时间聚合指标 | `date_col`, `freq`, `group_by` |
| `distribution_summary` | `distribution_summary(data, *, column, bins=10, include_lowest=True)` | 统计分箱分布 | `column`, `bins` |
| `crosstab_summary` | `crosstab_summary(data, *, index_col, columns_col, values_col, aggfunc="sum", fill_value=0)` | 生成交叉表 | `index_col`, `columns_col` |
| `share_of_total` | `share_of_total(data, *, group_by, value_col)` | 计算份额占比 | `group_by`, `value_col` |
| `moving_average` | `moving_average(data, *, date_col, value_col, window=7, group_by=None)` | 计算移动平均 | `window` |
| `period_over_period_growth` | `period_over_period_growth(data, *, date_col, value_col, periods=1, group_by=None)` | 计算环比/同比增长率 | `periods` |

#### 典型调用

```python
summary = summarize_by(df, group_by="channel", value_col="revenue", agg="sum")
print(summary)

stats = describe_numeric(df)
print(stats)

trend = time_series_summary(
    df,
    date_col="date",
    value_col="revenue",
    group_by="channel",
    freq="M",
    aggfunc="sum",
)
```

---

### 2.3 业务分析类

| 函数 | 签名 | 作用 | 关键参数 |
| --- | --- | --- | --- |
| `funnel_analysis` | `funnel_analysis(data, *, user_id_col, stage_col, stages=None)` | 漏斗转化分析 | `user_id_col`, `stage_col` |
| `funnel_comparison` | `funnel_comparison(data, *, user_id_col, stage_col, variant_col, stages=None)` | 对比不同分组的漏斗 | `variant_col` |
| `user_segmentation` | `user_segmentation(data, *, user_id_col, value_col, thresholds=(0.0, 200.0, 500.0), labels=("low", "mid", "high", "vip"))` | 用户价值分层 | `thresholds`, `labels` |
| `attribution_summary` | `attribution_summary(data, *, user_id_col, channel_col, value_col="revenue", conversion_col="converted", method="last_touch", session_order_col="session_order")` | 渠道归因分析 | `method` |
| `attribution_breakdown` | `attribution_breakdown(data, *, user_id_col, channel_col, value_col="revenue", conversion_col="converted", method="last_touch", session_order_col="session_order")` | 归因占比拆解 | `method` |
| `conversion_rate_by` | `conversion_rate_by(data, *, group_by, visits_col="visits", orders_col="orders")` | 分组转化率 | `group_by` |
| `cohort_analysis` | `cohort_analysis(data, *, user_id_col, date_col, value_col, period="M")` | cohort 留存与分群分析 | `period` |
| `ab_test_summary` | `ab_test_summary(data, *, variant_col, metric_col, baseline_variant=None, metric_type="mean")` | A/B 测试效果汇总 | `baseline_variant`, `metric_type` |

#### 典型调用

```python
funnel = funnel_analysis(
    df,
    user_id_col="user_id",
    stage_col="stage",
    stages=["visit", "signup", "purchase"],
)

segments = user_segmentation(
    df,
    user_id_col="user_id",
    value_col="revenue",
)

attribution = attribution_summary(
    df,
    user_id_col="user_id",
    channel_col="channel",
    value_col="revenue",
    conversion_col="converted",
    method="last_touch",
)
```

---

### 2.4 统计回归与预测类

| 函数 | 签名 | 作用 | 关键参数 |
| --- | --- | --- | --- |
| `linear_regression` | `linear_regression(data, *, x_col, y_col)` | 线性回归拟合 | `x_col`, `y_col` |
| `trend_regression` | `trend_regression(data, *, x_col, y_col)` | 与线性回归等价的趋势拟合函数 | `x_col`, `y_col` |
| `forecast_metric` | `forecast_metric(data, *, date_col, value_col, periods=7, method="linear")` | 对未来周期做线性预测 | `periods`, `method` |

#### 关键说明

- `linear_regression` 返回字典，包含 `slope`、`intercept`、`r2` 和 `fitted`。
- `x_col` 支持时间序列或数值列。
- 当前 `forecast_metric` 仅支持 `method="linear"`。

---

### 2.5 绘图与报表类

| 函数 | 签名 | 作用 | 关键参数 |
| --- | --- | --- | --- |
| `plot_summary` | `plot_summary(summary, x_col, y_col, *, title, xlabel=None, ylabel=None, figsize=(8, 5), color="steelblue")` | 以条形图汇总展示 | `title`, `x_col`, `y_col` |
| `plot_metric_comparison` | `plot_metric_comparison(data, *, x_col, metrics, title, figsize=(10, 6), style="-o")` | 对比多个指标趋势 | `metrics`, `style` |
| `kpi_monitor_table` | `kpi_monitor_table(data, *, date_col, metrics, freq="D")` | 生成 KPI 时间序列表 | `date_col`, `metrics`, `freq` |
| `build_report_table` | `build_report_table(data, *, group_by, metrics, aggfunc="sum")` | 按分组生成汇总表 | `group_by`, `metrics` |
| `build_growth_dashboard` | `build_growth_dashboard(data, *, date_col, group_by, metrics=None, variant_col="channel", baseline_variant=None, freq="D")` | 生成增长型看板 | `metrics`, `freq` |
| `build_operational_dashboard` | `build_operational_dashboard(data, *, date_col, group_by, metrics=None, channel_col="channel", baseline_variant=None)` | 生成运营型看板 | `metrics`, `channel_col` |

#### 典型调用

```python
report = build_report_table(
    df,
    group_by="channel",
    metrics={"revenue_total": "revenue", "orders_total": "orders"},
    aggfunc="sum",
)

fig, ax = plot_summary(
    report,
    x_col="channel",
    y_col="revenue_total",
    title="渠道收入分布",
)
```

---

## 3. 数据访问与查询相关函数

### `NotebookProject`

用于表示一个分析项目的根目录和数据目录。其职责包括：

- 记录 `repo_root`（仓库根目录）和可选 `data_dir`
- 在初始化时规范化路径
- 解析文件名并在仓库内搜索数据文件
- 提供标准化的加载和查询入口

### `NotebookProject.resolve_data_file(filename)`

根据给定的文件名或路径，尝试在以下位置定位数据文件：

- 项目自定义数据目录
- 仓库根目录下的 `data/`
- `data-analysis/data/`
- 以及向上递归查找父目录中的 `data/`

如果找到则返回 `Path`，否则返回 `None`。

### `NotebookProject.load_data(...)`

按文件后缀自动选择读取方式，支持：

- CSV / TXT：`pandas.read_csv`
- JSON / JSONL：`pandas.read_json`
- XLSX / XLS：`pandas.read_excel`

可以通过 `kind` 参数强制指定类型，也可以把 `**kwargs` 传递给底层 pandas 读取函数。

### `NotebookProject.query(sql, tables=None)`

将一组 DataFrame 注册到 DuckDB 中，并执行一条 SQL 查询，返回查询结果 DataFrame。

适合用于：

- 直接在 Python 中用 SQL 对多个表联合分析
- 不依赖磁盘文件的临时数据分析

### `NotebookProject.query_df(sql, data, name="data")`

将单个 DataFrame 作为命名表注册到 DuckDB，然后执行 SQL。

这是一个非常实用的“内存表查询”接口，适合在 notebook 中快速试验 SQL。

### `NotebookProject.query_file(sql, filename)`

先解析文件路径，再将对应的文件路径作为参数传给 DuckDB SQL，常用于从文件路径直接执行 SQL 读取操作。

### `NotebookProject.query_csv(sql, filename)`

将 CSV 文件注册为 DuckDB 的视图，然后在其上执行 SQL 查询。

适合在不需要先把 CSV 读入 Pandas 的情况下直接用 SQL 做聚合或筛选。

### `NotebookProject.plot(...)`

用于快速绘制基础图表。支持：

- `bar`：柱状图
- `line`：折线图
- `scatter`：散点图
- `pie`：饼图

会校验 X/Y 列是否存在，并返回 Matplotlib 的 `Figure` 和 `Axes`，方便后续自定义样式或保存图片。

---

## 3. 汇总与统计分析函数

### `_normalize_frequency(freq)`

这是一个内部辅助函数，用于把类似 `M`、`Q`、`Y`、`A` 这样的时间频率别名标准化成 Pandas 可识别的频率字符串：

- `M -> ME`
- `Q -> QE`
- `Y / A -> YE`

它保证后续按时间分组的逻辑能正常工作。

### `summarize_by(data, group_by, value_col, ascending=False, agg="sum")`

按某个分组字段聚合数值列，并返回汇总结果。

典型场景：

- 按国家统计销售额
- 按渠道汇总访问量
- 按日期分组统计订单数

返回结果中默认命名为 `total_<value_col>`.

### `top_by(data, group_by, value_col, top_n=5, ascending=False, agg="sum")`

对 `summarize_by` 结果取前 N 项，适合用于“Top 5 / Top 10”排行榜。

### `describe_numeric(data, columns=None)`

筛选出数字型列并返回它们的描述统计信息，例如：

- count
- mean
- std
- min
- 25%
- 50%
- 75%
- max

适合快速观测数据分布与离群值。

### `correlation_matrix(data, columns=None, method="pearson")`

计算数据集中数值列之间的相关系数矩阵。

支持的相关度方法包括：

- `pearson`
- `kendall`
- `spearman`

通常用于分析变量之间是否存在强相关关系。

### `time_series_summary(data, date_col, value_col, group_by=None, freq="D", aggfunc="sum")`

按时间维度对数据做汇总。

功能包括：

- 将 `date_col` 转成时间格式
- 按日期分桶（按天、周、月等）统计
- 可按 `group_by` 再按分组字段聚合
- 支持 `sum`、`mean`、`median` 等聚合方式

这是一类常用的趋势分析工具。

### `distribution_summary(data, column, bins=10, include_lowest=True)`

对连续数值列做分箱统计，返回每个 bin 的：

- 区间名称（如 `(0, 10]`）
- 计数
- 最小值
- 最大值

常用于查看分布密度和是否存在偏态或异常值。

### `crosstab_summary(data, index_col, columns_col, values_col, aggfunc="sum", fill_value=0)`

将数据整理成交叉表（pivot table）。

它常用于：

- 统计不同维度的交叉分布
- 例如“地区 x 渠道”的销售汇总
- 例如“月份 x 品类”的订单量矩阵

### `share_of_total(data, group_by, value_col)`

将每个分组的数值占总量的比例计算出来，返回：

- 分组名称
- 分组总值
- `share_of_total` 占比

这适合做“贡献度分析”。

### `moving_average(data, date_col, value_col, window=7, group_by=None)`

计算移动平均值，用于平滑时间序列。

当传入 `group_by` 时，会按分组分别计算各自的滚动均值。

### `period_over_period_growth(data, date_col, value_col, periods=1, group_by=None)`

计算同比/环比增长率。

- 对每个时间点，计算与前 `periods` 个周期的增长率
- 若指定 `group_by`，则按分组分别计算增长率

返回结果会带上 `growth_rate` 列。

---

## 4. 回归与预测函数

### `linear_regression(data, x_col, y_col)`

执行简单线性回归，拟合公式：

$$
y = intercept + slope \times x
$$

返回结果包含：

- `slope`：斜率
- `intercept`：截距
- `r2`：确定系数
- `fitted`：拟合值序列

支持 `x_col` 为时间类型或数值类型。

### `trend_regression(data, x_col, y_col)`

这是 `linear_regression` 的别名，目的在于对“趋势分析”场景使用更直观的函数名。

### `forecast_metric(data, date_col, value_col, periods=7, method="linear")`

基于线性趋势对未来若干期进行预测。

它会：

- 按时间排序
- 对 `value_col` 做线性回归
- 生成未来 `periods` 个时间点的预测值
- 返回一个包含历史值和未来 forecast 的 DataFrame

当前仅支持 `method="linear"`。

---

## 5. 业务分析函数

### `funnel_analysis(data, user_id_col, stage_col, stages=None)`

用于漏斗分析，观察用户在各阶段的数量变化。

它会：

- 去重用户与阶段记录
- 按指定阶段顺序或自然出现顺序排序
- 统计每个阶段的用户数
- 计算 `conversion_rate` 和 `cumulative_rate`

适合分析转化漏斗。

### `funnel_comparison(data, user_id_col, stage_col, variant_col, stages=None)`

对多个分组（例如 A/B 方案、渠道、版本）进行漏斗对比。

返回每个 Variant 在每个阶段的：

- 用户数
- 总用户数
- 转化率

可用于比较不同实验组的漏斗表现。

### `user_segmentation(data, user_id_col, value_col, thresholds=(0.0, 200.0, 500.0), labels=("low", "mid", "high", "vip"))`

按用户累计价值划分分群。

功能：

- 按用户汇总总价值
- 用阈值区间给用户打标签
- 返回用户、总值和对应 segment

适合做用户价值分层。

### `attribution_summary(data, user_id_col, channel_col, value_col="revenue", conversion_col="converted", method="last_touch", session_order_col="session_order")`

归因分析函数，用于将转化用户归因到某个渠道。

支持：

- `first_touch`：按照首次接触归因
- `last_touch`：按照最后一次接触归因

返回的结果包含每个渠道的：

- 转化用户数
- 收入

### `attribution_breakdown(data, user_id_col, channel_col, value_col="revenue", conversion_col="converted", method="last_touch", session_order_col="session_order")`

在 `attribution_summary` 的基础上计算各渠道的收入占比。

返回字段包括：

- `channel`
- `converted_users`
- `revenue`
- `revenue_share`

适合用于渠道贡献度分析。

### `conversion_rate_by(data, group_by, visits_col="visits", orders_col="orders")`

按分组计算转化率：

- `conversion_rate = orders / visits`

返回每组的访问量、订单量和转化率。

### `cohort_analysis(data, user_id_col, date_col, value_col, period="M")`

用于 cohort（人群）分析。

它会：

- 找出每个用户第一次出现的时间
- 将用户归到 cohort
- 按 cohort + 时间周期统计用户数和业务指标

常用于分析“留存”与“用户生命周期”。

### `ab_test_summary(data, variant_col, metric_col, baseline_variant=None, metric_type="mean")`

对 A/B 测试结果做快速汇总。

输出包括：

- 每个变体样本量
- 对应指标均值
- 相对基线的 uplift

适合展示不同版本的业务表现差异。

---

## 6. 其他分析和报表函数

### `plot_summary(summary, x_col, y_col, title, xlabel=None, ylabel=None, figsize=(8, 5), color="steelblue")`

给定汇总后的 DataFrame，快速绘制条形图。

适合把汇总表直接画出来，常用于看板与报表展示。

### `plot_metric_comparison(data, x_col, metrics, title, figsize=(10, 6), style="-o")`

将多个指标在同一张图上绘制对比曲线。

适合：

- 多个 KPI 对比
- 不同时期指标趋势比较
- 业务指标周报/日报对照

### `kpi_monitor_table(data, date_col, metrics, freq="D")`

将一组指标按时间粒度聚合成监控表。

例如：

- `metrics = {"visits": "visits", "orders": "orders", "revenue": "revenue"}`

返回的 DataFrame 会按时间周期展示这些 KPI。

### `build_report_table(data, group_by, metrics, aggfunc="sum")`

根据分组字段和指标字典生成汇总表。

它会：

- 对目标指标做聚合
- 按字段名重命名输出列
- 按首个指标排序，方便做排行榜

### `build_growth_dashboard(data, date_col, group_by, metrics=None, variant_col="channel", baseline_variant=None, freq="D")`

构建增长型仪表盘。

返回字典包含：

- `summary`：汇总表
- `trend`：按时间趋势表
- `ab_summary`：AB 测试汇总

适合看“分组 + 时间趋势 + 实验效果”三位一体的增长分析。

### `build_operational_dashboard(data, date_col, group_by, metrics=None, channel_col="channel", baseline_variant=None)`

构建运营型仪表盘。

返回内容包括：

- `summary`：总体汇总
- `weekly_summary`：周汇总
- `monthly_summary`：月汇总
- `channel_summary`：渠道汇总
- `ab_summary`：渠道级 A/B 对比

适合团队运营监控与日常分析。

---

## 7. 典型使用方式

一个常见的工作流是：

1. 用 `NotebookProject` 解析数据路径
2. 用 `load_data` 加载 CSV / Excel / JSON
3. 用 `summarize_by`、`time_series_summary` 等函数做聚合
4. 用 `linear_regression`、`forecast_metric` 做趋势分析
5. 用 `plot`、`plot_metric_comparison` 或仪表盘生成函数进行展示

例如：

```python
from pathlib import Path
from data-analysis.notebooks.notebook_framework import NotebookProject

project = NotebookProject(repo_root=Path("."), data_dir=Path("data"))
df = project.load_data("news.csv")
summary = summarize_by(df, group_by="channel", value_col="revenue")
```

---

## 8. 设计特点

这个模块的优点是：

- 适合 notebooks 中快速做分析
- 统一了数据读取与 SQL 查询入口
- 把常见业务分析逻辑封装成函数
- 便于在分析脚本与报表中复用
- 内置了常见图表与监控仪表盘模板

它更偏“分析工作台”型工具库，而不是框架级的爬虫或工程控制层。使用时，通常是直接在 Jupyter / Python 交互环境中进行数据探索和汇报。

---

## 9. 函数总览

- `NotebookProject`
- `NotebookProject.resolve_data_file`
- `NotebookProject.load_data`
- `NotebookProject.query`
- `NotebookProject.query_df`
- `NotebookProject.query_file`
- `NotebookProject.query_csv`
- `NotebookProject.plot`
- `_normalize_frequency`
- `summarize_by`
- `top_by`
- `describe_numeric`
- `correlation_matrix`
- `time_series_summary`
- `distribution_summary`
- `crosstab_summary`
- `share_of_total`
- `moving_average`
- `period_over_period_growth`
- `linear_regression`
- `trend_regression`
- `forecast_metric`
- `funnel_analysis`
- `funnel_comparison`
- `user_segmentation`
- `attribution_summary`
- `attribution_breakdown`
- `conversion_rate_by`
- `cohort_analysis`
- `ab_test_summary`
- `plot_summary`
- `plot_metric_comparison`
- `kpi_monitor_table`
- `build_report_table`
- `build_growth_dashboard`
- `build_operational_dashboard`

以上是对该文件中主要函数职责的概览。实际使用时，可以根据分析场景逐一调用这些函数完成数据处理、建模、绘图和汇总。