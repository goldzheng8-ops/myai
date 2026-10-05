from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

Aggregation = Literal[
    "sum",
    "mean",
    "median",
    "min",
    "max",
    "count",
    "nunique",
]

CorrelationMethod = Literal[
    "pearson",
    "kendall",
    "spearman",
]

@dataclass(slots=True)
class NotebookProject:
    repo_root: Path
    data_dir: Path | None = None

    def __post_init__(self) -> None:
        self.repo_root = self.repo_root.resolve()

        if self.data_dir is None:
            self.data_dir = self.repo_root / "data"
        else:
            self.data_dir = self.data_dir.resolve()

    def resolve_data_file(self, filename: str | Path) -> Path | None:
        target = Path(filename)

        if target.is_absolute():
            return target if target.exists() else None

        data_dir = self.data_dir
        assert data_dir is not None

        candidates = [
            data_dir / target,
            self.repo_root / "data" / target,
            self.repo_root / "data-analysis" / "data" / target,
        ]

        for root in (self.repo_root, *self.repo_root.parents):
            candidates.extend(
                (
                    root / "data" / target,
                    root / "data-analysis" / "data" / target,
                )
            )

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return None

    def load_data(
        self,
        filename: str | Path,
        *,
        kind: str | None = None,
        sheet_name: str | int = 0,
        **kwargs: Any,
    ) -> pd.DataFrame:
        path = self.resolve_data_file(filename)

        if path is None:
            raise FileNotFoundError(
                f"Unable to locate data file: {filename}"
            )

        resolved_kind = (
            kind
            or path.suffix.lower().lstrip(".")
            or "csv"
        ).lower()

        if resolved_kind in {"csv", "txt"}:
            return pd.read_csv(path, **kwargs)

        if resolved_kind in {"json", "jsonl"}:
            return pd.read_json(path, **kwargs)

        if resolved_kind in {"xlsx", "xls"}:
            return pd.read_excel(
                path,
                sheet_name=sheet_name,
                **kwargs,
            )

        raise ValueError(
            f"Unsupported data format: {resolved_kind}"
        )


def _normalize_frequency(freq: str) -> str:
    aliases = {
        "M": "ME",
        "Q": "QE",
        "Y": "YE",
        "A": "YE",
    }
    normalized = str(freq).upper()
    return aliases.get(normalized, normalized)


def summarize_by(
    data: pd.DataFrame,
    *,
    group_by: str,
    value_col: str,
    ascending: bool = False,
    agg: Aggregation  = "sum",
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in (group_by, value_col)
        if column not in data.columns
    ]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    output_col = f"total_{value_col}"

    summary = (
        data.groupby(group_by, as_index=False)
        .agg(**{output_col: (value_col, agg)})
        .sort_values(
            by=output_col,
            ascending=ascending,
            kind="stable",
        )
        .reset_index(drop=True)
    )

    return summary


def top_by(
    data: pd.DataFrame,
    *,
    group_by: str,
    value_col: str,
    top_n: int = 5,
    ascending: bool = False,
    agg: Aggregation  = "sum",
) -> pd.DataFrame:
    return summarize_by(
        data,
        group_by=group_by,
        value_col=value_col,
        ascending=ascending,
        agg=agg,
    ).head(top_n)


def describe_numeric(
    data: pd.DataFrame,
    *,
    columns: Iterable[str] | None = None,
) -> pd.DataFrame:
    selected = data if columns is None else data[list(columns)]
    numeric = selected.select_dtypes(include=["number"])
    if numeric.empty:
        raise ValueError("No numeric columns available for descriptive analysis.")
    return numeric.describe().T


def correlation_matrix(
    data: pd.DataFrame,
    *,
    columns: Iterable[str] | None = None,
    method: CorrelationMethod = "pearson",
) -> pd.DataFrame:
    selected = data if columns is None else data[list(columns)]
    numeric = selected.select_dtypes(include=["number"])
    if numeric.empty:
        raise ValueError("No numeric columns available for correlation analysis.")
    return numeric.corr(method=method)


def time_series_summary(
    data: pd.DataFrame,
    *,
    date_col: str,
    value_col: str,
    group_by: str | None = None,
    freq: str = "D",
    aggfunc: Aggregation = "sum",
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in (date_col, value_col)
        if column not in data.columns
    ]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    working = data.copy()
    working[date_col] = pd.to_datetime(working[date_col])
    normalized_freq = _normalize_frequency(freq)

    output_col = f"total_{value_col}"

    if group_by is not None:
        if group_by not in working.columns:
            raise KeyError(
                f"Missing grouping column: {group_by}"
            )

        summary = (
            working
            .groupby(
                [
                    group_by,
                    pd.Grouper(
                        key=date_col,
                        freq=normalized_freq,
                    ),
                ],
                as_index=False,
            )
            .agg(**{
                output_col: (value_col, aggfunc),
            })
            .sort_values(
                [group_by, date_col],
                kind="stable",
            )
            .reset_index(drop=True)
        )

        return summary

    summary = (
        working
        .groupby(
            pd.Grouper(
                key=date_col,
                freq=normalized_freq,
            ),
            as_index=False,
        )
        .agg(**{
            output_col: (value_col, aggfunc),
        })
        .sort_values(
            date_col,
            kind="stable",
        )
        .reset_index(drop=True)
    )

    return summary

def trend_regression(
    data: pd.DataFrame,
    *,
    x_col: str,
    y_col: str,
) -> dict[str, float | pd.Series]:
    missing_columns = [column for column in (x_col, y_col) if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    x_values = data[x_col]
    y_values = pd.to_numeric(data[y_col], errors="raise")

    if pd.api.types.is_datetime64_any_dtype(x_values):
        datetime_values = pd.to_datetime(x_values)
        x_numeric = (
            (datetime_values - datetime_values.min())
            .dt.total_seconds()
            .to_numpy(dtype=float)
            / 86400.0
        )
    else:
        x_numeric = pd.to_numeric(x_values, errors="raise").to_numpy(dtype=float)

    y_numeric = y_values.to_numpy(dtype=float)

    if len(x_numeric) < 2:
        raise ValueError("Trend regression requires at least two rows of data.")

    coefficients = np.polyfit(x_numeric, y_numeric, 1)
    slope = float(coefficients[0])
    intercept = float(coefficients[1])
    fitted = intercept + slope * x_numeric
    ss_res = float(np.sum((y_numeric - fitted) ** 2))
    ss_tot = float(np.sum((y_numeric - y_numeric.mean()) ** 2))
    r_squared = 1.0 if ss_tot == 0 else 1.0 - (ss_res / ss_tot)

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r_squared),
        "fitted": pd.Series(fitted, index=data.index, name="trend"),
    }


def crosstab_summary(
    data: pd.DataFrame,
    *,
    index_col: str,
    columns_col: str,
    values_col: str,
    aggfunc: Aggregation = "sum",
    fill_value: float | int | None = 0,
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in (index_col, columns_col, values_col)
        if column not in data.columns
    ]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    summary: pd.DataFrame = pd.pivot_table(
        data,
        index=index_col,
        columns=columns_col,
        values=values_col,
        aggfunc=aggfunc,
        fill_value=fill_value,
    )
    return summary


def funnel_analysis(
    data: pd.DataFrame,
    *,
    user_id_col: str,
    stage_col: str,
    stages: Iterable[str] | None = None,
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in (user_id_col, stage_col)
        if column not in data.columns
    ]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    working = data[[user_id_col, stage_col]].drop_duplicates().copy()
    ordered_stages = (
        list(stages)
        if stages is not None
        else list(dict.fromkeys(working[stage_col].dropna().tolist()))
    )

    summary = (
        working[working[stage_col].isin(ordered_stages)]
        .groupby(stage_col, as_index=False)[[user_id_col]]
        .nunique()
        .rename(columns={user_id_col: "user_count", stage_col: "stage"})
    )
    summary["stage"] = pd.Categorical(summary["stage"], categories=ordered_stages, ordered=True)
    summary = summary.sort_values("stage", kind="stable").reset_index(drop=True)

    if summary.empty:
        return summary.assign(conversion_rate=0.0, cumulative_rate=0.0)

    total_users = float(summary["user_count"].iloc[0])
    summary["conversion_rate"] = summary["user_count"] / total_users if total_users else 0.0
    summary["cumulative_rate"] = summary["user_count"].cumsum() / total_users if total_users else 0.0

    result: pd.DataFrame = summary[["stage", "user_count", "conversion_rate", "cumulative_rate"]]
    return result.reset_index(drop=True)


def user_segmentation(
    data: pd.DataFrame,
    *,
    user_id_col: str,
    value_col: str,
    thresholds: tuple[float, ...] = (0.0, 200.0, 500.0),
    labels: tuple[str, ...] = ("low", "mid", "high", "vip"),
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in (user_id_col, value_col)
        if column not in data.columns
    ]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    if len(thresholds) + 1 != len(labels):
        raise ValueError("The number of thresholds must be one less than the number of labels.")

    summary = (
        data.groupby(user_id_col, as_index=False)[[value_col]]
        .sum()
        .rename(columns={value_col: "total_value"})
    )

    bins = [-np.inf, *list(thresholds), np.inf]
    summary["segment"] = pd.cut(
        summary["total_value"],
        bins=bins,
        labels=labels,
        right=True,
        include_lowest=True,
    )

    result: pd.DataFrame = summary[[user_id_col, "total_value", "segment"]]
    return result.reset_index(drop=True)


def attribution_summary(
    data: pd.DataFrame,
    *,
    user_id_col: str,
    channel_col: str,
    value_col: str = "revenue",
    conversion_col: str = "converted",
    method: str = "last_touch",
    session_order_col: str = "session_order",
) -> pd.DataFrame:
    missing_columns = [column for column in (user_id_col, channel_col, value_col, conversion_col) if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    working = data.copy()
    if session_order_col not in working.columns:
        working[session_order_col] = working.groupby(user_id_col).cumcount() + 1

    method = method.lower()
    if method not in {"first_touch", "last_touch"}:
        raise ValueError("method must be either 'first_touch' or 'last_touch'")

    ordered = working.sort_values([user_id_col, session_order_col], kind="stable")
    selected = ordered.drop_duplicates(subset=[user_id_col], keep="last" if method == "last_touch" else "first")
    converted = selected[selected[conversion_col].astype(bool)].copy()
    if converted.empty:
        return pd.DataFrame(columns=[channel_col, "converted_users", "revenue"]).astype({"converted_users": "int64"})

    result = (
        converted.groupby(channel_col, as_index=False)
        .agg(converted_users=(user_id_col, "nunique"), revenue=(value_col, "sum"))
        .sort_values(["converted_users", "revenue"], ascending=[False, False], kind="stable")
        .reset_index(drop=True)
    )
    return result


def conversion_rate_by(
    data: pd.DataFrame,
    *,
    group_by: str,
    visits_col: str = "visits",
    orders_col: str = "orders",
) -> pd.DataFrame:
    missing_columns = [column for column in (group_by, visits_col, orders_col) if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    result = (
        data.groupby(group_by, as_index=False)
        .agg({visits_col: "sum", orders_col: "sum"})
        .assign(conversion_rate=lambda frame: frame[orders_col] / frame[visits_col])
        .sort_values("conversion_rate", ascending=False, kind="stable")
        .reset_index(drop=True)
    )
    return result


def moving_average(
    data: pd.DataFrame,
    *,
    date_col: str,
    value_col: str,
    window: int = 7,
    group_by: str | None = None,
) -> pd.DataFrame:
    if window <= 0:
        raise ValueError("window must be greater than 0")

    working = data.copy().sort_values(date_col)
    working[date_col] = pd.to_datetime(working[date_col])

    if group_by is not None:
        if group_by not in working.columns:
            raise KeyError(f"Missing grouping column: {group_by}")
        result = working.groupby(group_by, group_keys=False).apply(
            lambda frame: frame.assign(
                **{f"rolling_{value_col}_{window}d": frame[value_col].rolling(window=window, min_periods=1).mean()}
            )
        )
        return result.reset_index(drop=True)

    result = working.copy()
    result[f"rolling_{value_col}_{window}d"] = result[value_col].rolling(window=window, min_periods=1).mean()
    return result.reset_index(drop=True)


def period_over_period_growth(
    data: pd.DataFrame,
    *,
    date_col: str,
    value_col: str,
    periods: int = 1,
    group_by: str | None = None,
) -> pd.DataFrame:
    if periods <= 0:
        raise ValueError("periods must be greater than 0")

    working = data.copy()
    working[date_col] = pd.to_datetime(working[date_col])

    if group_by is not None:
        if group_by not in working.columns:
            raise KeyError(f"Missing grouping column: {group_by}")

        summary = (
            working.groupby([group_by, date_col], as_index=False)[[value_col]]
            .sum()
            .sort_values([group_by, date_col], kind="stable")
        )
        summary["growth_rate"] = summary.groupby(group_by)[value_col].pct_change(periods=periods)
        return summary.reset_index(drop=True)

    summary = (
        working.groupby(date_col, as_index=False)[[value_col]]
        .sum()
        .sort_values(date_col, kind="stable")
        .reset_index(drop=True)
    )
    summary["growth_rate"] = summary[value_col].pct_change(periods=periods)
    return summary


def share_of_total(
    data: pd.DataFrame,
    *,
    group_by: str,
    value_col: str,
) -> pd.DataFrame:
    missing_columns = [
        column
        for column in (group_by, value_col)
        if column not in data.columns
    ]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    summary = (
        data.groupby(group_by, as_index=False)[[value_col]]
        .sum()
        .rename(columns={value_col: "total_value"})
        .sort_values("total_value", ascending=False, kind="stable")
        .reset_index(drop=True)
    )
    total_value = float(summary["total_value"].sum())
    summary["share_of_total"] = summary["total_value"] / total_value if total_value else 0.0
    return summary


def distribution_summary(
    data: pd.DataFrame,
    *,
    column: str,
    bins: int = 10,
    include_lowest: bool = True,
) -> pd.DataFrame:
    if column not in data.columns:
        raise KeyError(f"Missing required column: {column}")

    if bins <= 0:
        raise ValueError("bins must be greater than 0")

    values = (
        pd.to_numeric(
            data[column],
            errors="coerce",
        )
        .dropna()
    )

    if values.empty:
        return pd.DataFrame(
            columns=[
                "bin",
                "count",
                "min_value",
                "max_value",
            ]
        )

    bins_series = pd.cut(
        values,
        bins=bins,
        include_lowest=include_lowest,
        duplicates="drop",
    )

    counts = bins_series.value_counts(sort=False)

    summary = pd.DataFrame(
        {
            "bin": counts.index.map(str),
            "count": counts.to_numpy(dtype=int),
        }
    )

    intervals = counts.index

    min_values: list[float] = []
    max_values: list[float] = []

    for interval in intervals:
        if isinstance(interval, pd.Interval):
            min_values.append(float(interval.left))
            max_values.append(float(interval.right))
        else:
            min_values.append(float("nan"))
            max_values.append(float("nan"))

    summary["min_value"] = min_values
    summary["max_value"] = max_values

    return summary[
        ["bin", "count", "min_value", "max_value"]
    ].reset_index(drop=True)

def cohort_analysis(
    data: pd.DataFrame,
    *,
    user_id_col: str,
    date_col: str,
    value_col: str,
    period: str = "M",
) -> pd.DataFrame:
    if date_col not in data.columns:
        raise KeyError(f"Missing required columns: {date_col}")
    if value_col not in data.columns:
        raise KeyError(f"Missing required columns: {value_col}")

    working = data.copy()
    if user_id_col not in working.columns:
        working[user_id_col] = [f"synthetic_user_{index}" for index in working.index]

    working = working[[user_id_col, date_col, value_col]].copy()
    working[date_col] = pd.to_datetime(working[date_col])
    working["_user_first_seen"] = working.groupby(user_id_col)[date_col].transform("min")
    working["cohort"] = working["_user_first_seen"].dt.to_period(period).dt.strftime("%Y-%m")
    working["month"] = working[date_col].dt.to_period(period).dt.strftime("%Y-%m")

    summary = (
        working.groupby(["cohort", "month"], as_index=False)
        .agg(users=(user_id_col, "nunique"), revenue=(value_col, "sum"))
        .sort_values(["cohort", "month"], kind="stable")
        .reset_index(drop=True)
    )
    return summary


def ab_test_summary(
    data: pd.DataFrame,
    *,
    variant_col: str,
    metric_col: str,
    baseline_variant: str | None = None,
    metric_type: str = "mean",
) -> pd.DataFrame:
    if variant_col not in data.columns:
        raise KeyError(f"Missing required column: {variant_col}")
    if metric_col not in data.columns:
        raise KeyError(f"Missing required column: {metric_col}")

    working = data[[variant_col, metric_col]].copy()
    working[metric_col] = pd.to_numeric(working[metric_col], errors="coerce")
    summary = (
        working.groupby(variant_col, as_index=False)
        .agg(
            sample_size=(metric_col, "size"),
            metric_value=(metric_col, metric_type),
        )
        .rename(columns={variant_col: "variant"})
        .sort_values("metric_value", ascending=False, kind="stable")
        .reset_index(drop=True)
    )

    if baseline_variant is not None and baseline_variant in summary["variant"].tolist():
        baseline_value = float(summary.loc[summary["variant"] == baseline_variant, "metric_value"].iloc[0])
        summary["uplift"] = (summary["metric_value"] - baseline_value) / baseline_value if baseline_value else 0.0
    else:
        summary["uplift"] = 0.0

    return summary[["variant", "sample_size", "metric_value", "uplift"]]


def funnel_comparison(
    data: pd.DataFrame,
    *,
    user_id_col: str,
    stage_col: str,
    variant_col: str,
    stages: Iterable[str] | None = None,
) -> pd.DataFrame:
    if user_id_col not in data.columns:
        raise KeyError(f"Missing required column: {user_id_col}")
    if stage_col not in data.columns:
        raise KeyError(f"Missing required column: {stage_col}")
    if variant_col not in data.columns:
        raise KeyError(f"Missing required column: {variant_col}")

    working = data[[user_id_col, stage_col, variant_col]].drop_duplicates().copy()
    ordered_stages = (
        list(stages)
        if stages is not None
        else list(dict.fromkeys(working[stage_col].dropna().tolist()))
    )

    summary = (
        working[working[stage_col].isin(ordered_stages)]
        .groupby([variant_col, stage_col], as_index=False)[[user_id_col]]
        .nunique()
        .rename(columns={user_id_col: "user_count"})
    )
    total_by_variant = (
        summary.groupby(variant_col, as_index=False)[["user_count"]]
        .sum()
        .rename(columns={"user_count": "total_users"})
    )

    result: pd.DataFrame = summary.merge(total_by_variant, on=variant_col, how="left")
    result = result.rename(columns={variant_col: "variant"})
    result["conversion_rate"] = result["user_count"] / result["total_users"]
    result["stage"] = result[stage_col]

    output: pd.DataFrame = result[["variant", "stage", "user_count", "total_users", "conversion_rate"]]
    return output.sort_values(["variant", "stage"], kind="stable").reset_index(drop=True)


def attribution_breakdown(
    data: pd.DataFrame,
    *,
    user_id_col: str,
    channel_col: str,
    value_col: str = "revenue",
    conversion_col: str = "converted",
    method: str = "last_touch",
    session_order_col: str = "session_order",
) -> pd.DataFrame:
    if channel_col not in data.columns:
        raise KeyError(f"Missing required column: {channel_col}")
    if value_col not in data.columns:
        raise KeyError(f"Missing required column: {value_col}")
    if conversion_col not in data.columns:
        raise KeyError(f"Missing required column: {conversion_col}")

    working = data.copy()
    if user_id_col not in working.columns:
        working[user_id_col] = [f"synthetic_user_{index}" for index in working.index]

    result = attribution_summary(
        working,
        user_id_col=user_id_col,
        channel_col=channel_col,
        value_col=value_col,
        conversion_col=conversion_col,
        method=method,
        session_order_col=session_order_col,
    )
    if result.empty:
        return result.assign(revenue_share=0.0)
    total_revenue = float(result["revenue"].sum()) if "revenue" in result.columns else 0.0
    result["revenue_share"] = result["revenue"] / total_revenue if total_revenue else 0.0
    return result


def forecast_metric(
    data: pd.DataFrame,
    *,
    date_col: str,
    value_col: str,
    periods: int = 7,
    method: str = "linear",
) -> pd.DataFrame:
    if date_col not in data.columns:
        raise KeyError(f"Missing required column: {date_col}")
    if value_col not in data.columns:
        raise KeyError(f"Missing required column: {value_col}")
    if periods <= 0:
        raise ValueError("periods must be greater than 0")

    working = data[[date_col, value_col]].copy()
    working[date_col] = pd.to_datetime(working[date_col])
    working = working.sort_values(date_col, kind="stable").reset_index(drop=True)
    working[value_col] = pd.to_numeric(working[value_col], errors="coerce")

    if method.lower() != "linear":
        raise ValueError("Only linear forecasting is supported")

    if len(working) < 2:
        raise ValueError("Forecasting requires at least two observations")

    x_values = np.arange(len(working), dtype=float)
    y_values = working[value_col].to_numpy(dtype=float)
    coefficients = np.polyfit(x_values, y_values, 1)
    slope = float(coefficients[0])
    intercept = float(coefficients[1])
    last_date = working[date_col].iloc[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq="D")
    forecast_values = intercept + slope * (
        len(working) + np.arange(periods, dtype=float)
    )
    forecast_df = pd.DataFrame({date_col: forecast_dates, "forecast": forecast_values})
    summary = working.rename(columns={value_col: "actual"})
    summary["forecast"] = np.nan
    return pd.concat([summary, forecast_df], ignore_index=True)


def plot_summary(
    summary: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    title: str,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[int, int] = (8, 5),
    color: str = "steelblue",
) -> tuple[Figure, Axes]:
    fig, axis = plt.subplots(figsize=figsize)
    axis.bar(summary[x_col], summary[y_col], color=color)
    axis.set_title(title)
    if xlabel is not None:
        axis.set_xlabel(xlabel)
    if ylabel is not None:
        axis.set_ylabel(ylabel)
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    return fig, axis


def kpi_monitor_table(
    data: pd.DataFrame,
    *,
    date_col: str,
    metrics: dict[str, str],
    freq: str = "D",
) -> pd.DataFrame:
    if not metrics:
        raise ValueError("At least one metric must be supplied")
    if date_col not in data.columns:
        raise KeyError(f"Missing required column: {date_col}")

    missing_columns = [column for column in metrics.values() if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    working = data[[date_col, *metrics.values()]].copy()
    working[date_col] = pd.to_datetime(working[date_col])
    aggregation = {source_col: "sum" for source_col in metrics.values()}
    normalized_freq = _normalize_frequency(freq)
    result = working.groupby(pd.Grouper(key=date_col, freq=normalized_freq), as_index=False).agg(aggregation)
    rename_map = {source_col: output_col for output_col, source_col in metrics.items()}
    result = result.rename(columns=rename_map)
    return result.sort_values(date_col, kind="stable").reset_index(drop=True)


def build_report_table(
    data: pd.DataFrame,
    *,
    group_by: str,
    metrics: dict[str, str],
    aggfunc: str = "sum",
) -> pd.DataFrame:
    if not metrics:
        raise ValueError("At least one metric must be supplied")

    missing_columns = [column for column in (group_by, *metrics.values()) if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    aggregation = {source_col: aggfunc for source_col in metrics.values()}
    result = data.groupby(group_by, as_index=False).agg(aggregation)
    rename_map = {source_col: output_col for output_col, source_col in metrics.items()}
    result = result.rename(columns=rename_map)

    first_metric = next(iter(metrics))
    return result.sort_values(by=first_metric, ascending=False, kind="stable").reset_index(drop=True)


def build_growth_dashboard(
    data: pd.DataFrame,
    *,
    date_col: str,
    group_by: str,
    metrics: dict[str, str] | None = None,
    variant_col: str = "channel",
    baseline_variant: str | None = None,
    freq: str = "D",
) -> dict[str, pd.DataFrame]:
    selected_metrics = metrics or {"visits": "visits", "orders": "orders", "revenue": "revenue"}
    summary = build_report_table(data, group_by=group_by, metrics=selected_metrics)
    primary_metric = next(iter(selected_metrics.values()))
    trend = time_series_summary(data, date_col=date_col, value_col=primary_metric, group_by=group_by, freq=freq)
    ab_summary = ab_test_summary(
        data,
        variant_col=variant_col,
        metric_col=primary_metric,
        baseline_variant=baseline_variant,
    )
    return {"summary": summary, "trend": trend, "ab_summary": ab_summary}


def build_operational_dashboard(
    data: pd.DataFrame,
    *,
    date_col: str,
    group_by: str,
    metrics: dict[str, str] | None = None,
    channel_col: str = "channel",
    baseline_variant: str | None = None,
) -> dict[str, pd.DataFrame]:
    selected_metrics = metrics or {"visits": "visits", "orders": "orders", "revenue": "revenue"}
    summary = build_report_table(data, group_by=group_by, metrics=selected_metrics)
    weekly_summary = time_series_summary(
        data,
        date_col=date_col,
        value_col=next(iter(selected_metrics.values())),
        group_by=group_by,
        freq="W-MON",
    )
    monthly_summary = time_series_summary(
        data,
        date_col=date_col,
        value_col=next(iter(selected_metrics.values())),
        group_by=group_by,
        freq="M",
    )
    channel_summary = build_report_table(data, group_by=channel_col, metrics=selected_metrics)
    ab_summary = ab_test_summary(
        data,
        variant_col=channel_col,
        metric_col=next(iter(selected_metrics.values())),
        baseline_variant=baseline_variant,
    )
    return {
        "summary": summary,
        "weekly_summary": weekly_summary,
        "monthly_summary": monthly_summary,
        "channel_summary": channel_summary,
        "ab_summary": ab_summary,
    }


def plot_metric_comparison(
    data: pd.DataFrame,
    *,
    x_col: str,
    metrics: list[str],
    title: str,
    figsize: tuple[int, int] = (10, 6),
    style: str = "-o",
) -> tuple[Figure, Axes]:
    if not metrics:
        raise ValueError("At least one metric must be supplied")

    fig, axis = plt.subplots(figsize=figsize)
    for metric in metrics:
        if metric not in data.columns:
            raise KeyError(f"Missing metric column: {metric}")
        axis.plot(data[x_col].astype(str), data[metric], style, linewidth=2, markersize=5, label=metric)

    axis.set_title(title)
    axis.set_xlabel(x_col)
    axis.set_ylabel("Metric")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    return fig, axis


__all__ = [
    "NotebookProject",
    "summarize_by",
    "top_by",
    "describe_numeric",
    "correlation_matrix",
    "time_series_summary",
    "trend_regression",
    "crosstab_summary",
    "funnel_analysis",
    "user_segmentation",
    "attribution_summary",
    "attribution_breakdown",
    "conversion_rate_by",
    "moving_average",
    "period_over_period_growth",
    "share_of_total",
    "distribution_summary",
    "cohort_analysis",
    "ab_test_summary",
    "funnel_comparison",
    "forecast_metric",
    "build_report_table",
    "build_growth_dashboard",
    "build_operational_dashboard",
    "kpi_monitor_table",
    "plot_metric_comparison",
    "plot_summary",
]
