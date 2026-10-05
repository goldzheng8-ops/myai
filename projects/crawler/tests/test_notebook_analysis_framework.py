import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "data-analysis" / "notebooks"
if str(NOTEBOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOKS_DIR))

from notebook_framework import (
    NotebookProject,
    ab_test_summary,
    attribution_breakdown,
    attribution_summary,
    build_growth_dashboard,
    build_operational_dashboard,
    build_report_table,
    cohort_analysis,
    conversion_rate_by,
    crosstab_summary,
    correlation_matrix,
    describe_numeric,
    distribution_summary,
    forecast_metric,
    funnel_analysis,
    funnel_comparison,
    kpi_monitor_table,
    moving_average,
    period_over_period_growth,
    plot_metric_comparison,
    share_of_total,
    summarize_by,
    time_series_summary,
    top_by,
    trend_regression,
    user_segmentation,
)


def test_notebook_project_finds_demo_data_and_builds_summary():
    project = NotebookProject(repo_root=ROOT)

    csv_path = project.resolve_data_file("notebook_env_demo.csv")

    assert csv_path is not None
    assert csv_path.exists()

    df = project.load_csv(csv_path)
    summary = summarize_by(df, group_by="source", value_col="visits")

    assert not summary.empty
    assert list(summary.columns) == ["source", "total_visits"]
    assert summary["total_visits"].sum() > 0


def test_notebook_framework_supports_descriptive_and_correlation_analysis():
    project = NotebookProject(repo_root=ROOT)
    df = project.load_csv("notebook_env_demo.csv")

    stats = describe_numeric(df, columns=["visits", "orders", "revenue"])
    assert {"visits", "orders", "revenue"}.issubset(set(stats.index))

    top_sources = top_by(df, group_by="source", value_col="visits", top_n=2)
    assert len(top_sources) <= 2

    corr = correlation_matrix(df, columns=["visits", "orders", "revenue"])
    assert "visits" in corr.columns
    assert corr.loc["visits", "orders"] > 0
    assert corr.loc["orders", "revenue"] > 0


def test_notebook_framework_supports_business_analysis_helpers():
    project = NotebookProject(repo_root=ROOT)
    df = project.load_csv("notebook_env_demo.csv")
    df["date"] = pd.to_datetime(df["date"])

    ts = time_series_summary(df, date_col="date", value_col="visits")
    assert list(ts.columns) == ["date", "total_visits"]
    assert len(ts) == df["date"].nunique()

    trend = trend_regression(df, x_col="date", y_col="visits")
    assert "slope" in trend
    assert trend["slope"] > 0

    growth = period_over_period_growth(df, date_col="date", value_col="visits", periods=7)
    assert "growth_rate" in growth.columns
    assert growth["growth_rate"].notna().any()

    rolling = moving_average(df, date_col="date", value_col="visits", window=3)
    assert "rolling_visits_3d" in rolling.columns
    assert rolling["rolling_visits_3d"].notna().any()

    by_source = conversion_rate_by(df, group_by="source", visits_col="visits", orders_col="orders")
    assert "conversion_rate" in by_source.columns
    assert by_source["conversion_rate"].between(0, 1).all()

    cross = crosstab_summary(df, index_col="source", columns_col="region", values_col="visits", aggfunc="sum")
    assert "search" in cross.index
    assert cross.shape[0] >= 1


def test_notebook_framework_supports_operational_growth_analysis():
    funnel_df = pd.DataFrame(
        {
            "user_id": ["u1", "u1", "u1", "u2", "u2", "u3", "u4", "u4"],
            "stage": ["view", "cart", "checkout", "view", "cart", "view", "view", "purchase"],
        }
    )
    funnel = funnel_analysis(funnel_df, user_id_col="user_id", stage_col="stage")
    assert set(funnel["stage"]) == {"view", "cart", "checkout", "purchase"}
    assert funnel.iloc[0]["user_count"] >= funnel.iloc[1]["user_count"]

    segment_df = pd.DataFrame(
        {
            "user_id": ["u1", "u2", "u3", "u4"],
            "revenue": [40, 180, 650, 1200],
        }
    )
    segments = user_segmentation(segment_df, user_id_col="user_id", value_col="revenue")
    assert "segment" in segments.columns
    assert set(segments["segment"]).issubset({"low", "mid", "high", "vip"})

    attribution_df = pd.DataFrame(
        {
            "user_id": ["u1", "u1", "u2", "u2", "u3", "u4"],
            "channel": ["search", "email", "search", "search", "social", "email"],
            "converted": [0, 1, 1, 1, 1, 0],
            "revenue": [20, 120, 180, 200, 560, 0],
            "session_order": [1, 2, 1, 2, 1, 1],
        }
    )
    attribution = attribution_summary(
        attribution_df,
        user_id_col="user_id",
        channel_col="channel",
        value_col="revenue",
        conversion_col="converted",
        method="last_touch",
    )
    assert "channel" in attribution.columns
    assert attribution["converted_users"].sum() >= 3


def test_notebook_framework_supports_dashboard_report_and_plotting():
    project = NotebookProject(repo_root=ROOT)
    df = project.load_csv("notebook_env_demo.csv")

    report = build_report_table(
        df,
        group_by="source",
        metrics={"visits": "visits", "orders": "orders", "revenue": "revenue"},
    )
    assert {"source", "visits", "orders", "revenue"}.issubset(set(report.columns))
    assert report["visits"].sum() > 0

    fig, axis = plot_metric_comparison(
        report,
        x_col="source",
        metrics=["visits", "orders"],
        title="Business comparison",
    )
    assert axis is not None
    assert len(axis.lines) >= 1


def test_notebook_framework_supports_additional_analytics_methods():
    project = NotebookProject(repo_root=ROOT)
    df = project.load_csv("notebook_env_demo.csv")
    df["date"] = pd.to_datetime(df["date"])

    mix = share_of_total(df, group_by="source", value_col="revenue")
    assert "share_of_total" in mix.columns
    assert mix["share_of_total"].between(0, 1).all()

    dist = distribution_summary(df, column="revenue", bins=4)
    assert "bin" in dist.columns
    assert not dist.empty

    cohort = cohort_analysis(
        df,
        user_id_col="user_id",
        date_col="date",
        value_col="revenue",
        period="M",
    )
    assert {"cohort", "month", "users", "revenue"}.issubset(set(cohort.columns))
    assert not cohort.empty


def test_notebook_framework_supports_operational_growth_methods():
    project = NotebookProject(repo_root=ROOT)
    df = project.load_csv("notebook_env_demo.csv")
    df["date"] = pd.to_datetime(df["date"])

    ab = ab_test_summary(
        df,
        variant_col="channel",
        metric_col="orders",
        baseline_variant="organic",
    )
    assert {"variant", "sample_size", "metric_value", "uplift"}.issubset(set(ab.columns))
    assert not ab.empty

    funnel = funnel_comparison(
        df.assign(user_id=df.index.astype(str)),
        user_id_col="user_id",
        stage_col="source",
        variant_col="channel",
    )
    assert "variant" in funnel.columns
    assert not funnel.empty

    attribution = attribution_breakdown(
        df,
        user_id_col="user_id",
        channel_col="channel",
        value_col="revenue",
        conversion_col="orders",
        method="last_touch",
    )
    assert {"channel", "converted_users", "revenue", "revenue_share"}.issubset(set(attribution.columns))

    forecast = forecast_metric(
        df,
        date_col="date",
        value_col="visits",
        periods=7,
    )
    assert "forecast" in forecast.columns
    assert forecast["forecast"].notna().any()


def test_notebook_framework_supports_growth_template_helpers():
    project = NotebookProject(repo_root=ROOT)
    df = project.load_csv("notebook_env_demo.csv")
    df["date"] = pd.to_datetime(df["date"])

    kpi = kpi_monitor_table(
        df,
        date_col="date",
        metrics={"visits": "visits", "orders": "orders", "revenue": "revenue"},
    )
    assert {"date", "visits", "orders", "revenue"}.issubset(set(kpi.columns))
    assert not kpi.empty

    report = build_growth_dashboard(
        df,
        date_col="date",
        group_by="source",
        metrics={"visits": "visits", "orders": "orders", "revenue": "revenue"},
    )
    assert {"summary", "trend", "ab_summary"}.issubset(set(report))
    assert not report["summary"].empty

    dashboard = build_operational_dashboard(
        df,
        date_col="date",
        group_by="source",
        metrics={"visits": "visits", "orders": "orders", "revenue": "revenue"},
    )
    assert {"summary", "weekly_summary", "monthly_summary", "channel_summary"}.issubset(set(dashboard))
    assert not dashboard["weekly_summary"].empty
    assert not dashboard["monthly_summary"].empty
