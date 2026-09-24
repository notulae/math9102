"""Descriptive statistics.

Replaces psych::describeBy and pastecs::stat.desc with a single table that
carries the statistics the module actually reports, including missingness -
which the legacy descriptive output omitted, so students never saw how much data
a later listwise deletion would discard.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sps

__all__ = ["describe", "describe_by", "frequency", "crosstab", "missingness"]


def _stats(x: pd.Series) -> dict:
    values = x.dropna()
    n = len(values)
    sd = float(values.std(ddof=1)) if n > 1 else np.nan
    return {
        "n": n,
        "missing": int(x.isna().sum()),
        "mean": float(values.mean()) if n else np.nan,
        "sd": sd,
        "se": sd / np.sqrt(n) if n > 1 else np.nan,
        "median": float(values.median()) if n else np.nan,
        "iqr": float(values.quantile(0.75) - values.quantile(0.25)) if n else np.nan,
        "min": float(values.min()) if n else np.nan,
        "max": float(values.max()) if n else np.nan,
        "skew": float(sps.skew(values, bias=False)) if n > 2 else np.nan,
        "kurtosis": float(sps.kurtosis(values, bias=False)) if n > 3 else np.nan,
    }


def describe(data: pd.DataFrame | pd.Series, columns: list[str] | None = None) -> pd.DataFrame:
    """Descriptive statistics for one or more numeric variables."""
    if isinstance(data, pd.Series):
        return pd.DataFrame([_stats(data)], index=[data.name or "value"]).round(3)

    columns = columns or [c for c in data.columns if pd.api.types.is_numeric_dtype(data[c])]
    return pd.DataFrame([_stats(data[c]) for c in columns], index=columns).round(3)


def describe_by(data: pd.DataFrame, outcome: str, group: str) -> pd.DataFrame:
    """Descriptive statistics for one variable split by a grouping variable."""
    sub = data[[outcome, group]].dropna(subset=[group])
    rows = {str(level): _stats(chunk[outcome]) for level, chunk in sub.groupby(group)}
    out = pd.DataFrame(rows).T
    out.index.name = group
    return out.round(3)


def frequency(data: pd.DataFrame, column: str, dropna: bool = False) -> pd.DataFrame:
    """Frequency table with counts, percentages and valid (non-missing) percentages.

    Follows the usual convention: `percent` is over all rows, `valid_percent` is
    over non-missing rows only and is left undefined for the missing category, so
    the valid percentages sum to 100.
    """
    counts = data[column].value_counts(dropna=dropna).sort_index()
    n_valid = int(data[column].notna().sum())

    valid_percent = counts / n_valid * 100
    valid_percent[counts.index.isna()] = np.nan

    out = pd.DataFrame(
        {
            "count": counts,
            "percent": (counts / len(data) * 100).round(2),
            "valid_percent": valid_percent.round(2),
        }
    )
    out.index.name = column
    return out


def crosstab(data: pd.DataFrame, row: str, col: str, normalize: str | None = None) -> pd.DataFrame:
    """Contingency table, optionally as percentages ('index', 'columns' or 'all')."""
    table = pd.crosstab(data[row], data[col])
    if normalize:
        table = (pd.crosstab(data[row], data[col], normalize=normalize) * 100).round(1)
    return table


def missingness(data: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Missingness per column plus the cost of listwise deletion across them.

    The legacy week 9 notebook ran na.omit() over all 134 columns of the survey,
    discarding 106 of 439 rows - 79 of them because of `smokenum`, a variable in
    none of its models. The models needed only 422 complete cases. This table is
    intended to make that cost visible before the decision is taken.
    """
    columns = list(columns or data.columns)
    sub = data[columns]
    rows = [
        {
            "column": c,
            "missing": int(sub[c].isna().sum()),
            "percent": round(sub[c].isna().mean() * 100, 2),
        }
        for c in columns
    ]
    out = pd.DataFrame(rows).sort_values("missing", ascending=False).reset_index(drop=True)

    complete = int(sub.dropna().shape[0])
    out.attrs["complete_cases"] = complete
    out.attrs["listwise_loss"] = len(sub) - complete
    out.attrs["summary"] = (
        f"Listwise deletion across these {len(columns)} column(s) keeps "
        f"{complete} of {len(sub)} rows (loses {len(sub) - complete}, "
        f"{(len(sub) - complete) / len(sub) * 100:.1f}%)."
    )
    return out
