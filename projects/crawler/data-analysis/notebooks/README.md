# Notebook analysis framework

This folder contains the reusable notebook layer for repository data analysis.

## Components

- `notebook_framework.py`
  - `NotebookProject`: resolves repo data paths and loads CSV/JSON/Excel files.
  - `summarize_by()`: groups rows and aggregates a numeric metric.
  - `top_by()`: returns the top categories after aggregation.
  - `describe_numeric()`: returns descriptive statistics for numeric columns.
  - `correlation_matrix()`: computes column correlations on numeric data.
  - `time_series_summary()`: aggregates values by a time frequency.
  - `trend_regression()`: estimates a linear trend across time or a numeric x axis.
  - `crosstab_summary()`: builds a pivot-table cross-tab from two categorical dimensions.
  - `plot_summary()`: renders a bar plot from summarized data.
- `kpi_monitor_table()`: builds a date-based KPI monitor for recurring product/ops reviews.
- `build_growth_dashboard()`: returns the common growth-report pack for summary, trend, and experiment comparison.
- `analysis_framework_demo.ipynb`
  - Example notebook that demonstrates the standard workflow.
- `growth_analysis_templates.ipynb`
  - Reusable growth-analysis notebook covering operations dashboard, experiment report, KPI monitoring, and multi-metric comparison templates.
- `operational_review_dashboard.ipynb`
  - Executive-style operational review report with KPI summary, weekly/monthly trend sections, channel decomposition, and recommendation-oriented conclusion notes.

## Typical workflow

```python
from pathlib import Path

from notebook_framework import (
    NotebookProject,
    correlation_matrix,
    crosstab_summary,
    describe_numeric,
    plot_summary,
    summarize_by,
    time_series_summary,
    top_by,
    trend_regression,
)

project = NotebookProject(Path.cwd().resolve().parent.parent)
df = project.load_csv("notebook_env_demo.csv")

summary = summarize_by(df, group_by="source", value_col="visits")
print(summary.head())

stats = describe_numeric(df, columns=["visits", "conversion"])
print(stats)

corr = correlation_matrix(df, columns=["visits", "conversion"])
print(corr)

series = time_series_summary(df, date_col="date", value_col="visits")
print(series.head())

trend = trend_regression(df, x_col="date", y_col="visits")
print(trend["slope"], trend["r2"])

cross = crosstab_summary(df, index_col="source", columns_col="date", values_col="visits")
print(cross.head())

fig, _ = plot_summary(summary, "source", "total_visits", title="Total visits by source")
```
