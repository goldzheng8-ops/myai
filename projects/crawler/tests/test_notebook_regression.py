import pandas as pd
import numpy as np
from data_analysis.notebooks.notebook_framework import linear_regression, NotebookProject


def test_linear_regression_numeric():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
    res = linear_regression(df, x_col="x", y_col="y")
    assert abs(res["slope"] - 2.0) < 1e-6
    assert abs(res["intercept"] - 0.0) < 1e-6
    assert isinstance(res["fitted"], pd.Series)


def test_linear_regression_datetime():
    dates = pd.date_range("2020-01-01", periods=5, freq="D")
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    df = pd.DataFrame({"ds": dates, "y": y})
    res = linear_regression(df, x_col="ds", y_col="y")
    assert "slope" in res and "intercept" in res and "r2" in res


def test_notebookproject_regression_wrapper():
    dates = pd.date_range("2020-01-01", periods=5, freq="D")
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    df = pd.DataFrame({"ds": dates, "y": y})
    proj = NotebookProject(repo_root=".")
    res = proj.regression(df, x_col="ds", y_col="y")
    assert "slope" in res
