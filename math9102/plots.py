"""Shared figure helpers and a single house style.

All figures in the module are generated from code rather than pasted as images.
The legacy decks carried 517 embedded images, mostly RStudio and website
screenshots that a Python edition invalidates, plus scanned textbook figures.
Regenerating from data keeps every figure consistent with the analysis, matched
to the slide theme, and free of third-party copyright.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as sps

__all__ = [
    "use_house_style",
    "PALETTE",
    "PALETTE_SCREEN",
    "PALETTE_PRINT",
    "histogram_with_normal",
    "qq_plot",
    "normality_panel",
    "scatter_with_fit",
    "grouped_box",
]

# Screen palette: colour-blind safe, for notebooks and HTML.
PALETTE_SCREEN = ["#3B6FB6", "#D1701C", "#4B9B6E", "#B5484A", "#7A5AA3", "#7F7F7F"]

# Print palette: greyscale, matching the Beamer decks. The lecture slides are
# deliberately monochrome (see slides/preamble.tex), so figures destined for them
# are generated in grey rather than converted afterwards, which keeps contrast
# under control.
#
# Luminances are spread evenly (26, 77, 102, 128, 153, 179 - gaps of at least 25)
# so no two series are hard to tell apart, and the first two entries, which carry
# the common two-group comparison, are the furthest apart of any adjacent pair.
# tests/test_helpers.py pins both properties.
PALETTE_PRINT = ["#1A1A1A", "#808080", "#4D4D4D", "#B3B3B3", "#666666", "#999999"]

# The active palette. `PALETTE` is what callers reference; use_house_style swaps it.
PALETTE = list(PALETTE_SCREEN)
_NORMAL_CURVE = "#B5484A"

_MODE = "screen"


def use_house_style(mode: str = "screen") -> None:
    """Apply the module's figure style.

    Call once at the top of a notebook. `mode` is 'screen' for notebooks and
    HTML, or 'print' for figures that will be embedded in the greyscale Beamer
    decks.
    """
    global PALETTE, _NORMAL_CURVE, _MODE
    if mode not in {"screen", "print"}:
        raise ValueError("mode must be 'screen' or 'print'")

    _MODE = mode
    PALETTE[:] = PALETTE_SCREEN if mode == "screen" else PALETTE_PRINT
    # In greyscale the reference curve must read as emphasis, not as a colour.
    _NORMAL_CURVE = "#B5484A" if mode == "screen" else "#111111"

    plt.rcParams.update(
        {
            "figure.figsize": (7.0, 4.2),
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linewidth": 0.6,
            "legend.frameon": False,
            "axes.prop_cycle": plt.cycler(color=PALETTE),
        }
    )


def histogram_with_normal(
    data, *, xlabel: str = "", bins: int | str = "auto", ax=None, title: str = ""
):
    """Histogram on the density scale with a fitted normal curve overlaid.

    The curve is drawn on the density scale deliberately. Two legacy notebooks
    overlaid a normal density on a *count* histogram, which puts the curve flat
    against the axis and makes the comparison invisible.
    """
    x = pd.Series(data).dropna()
    if ax is None:
        _, ax = plt.subplots()

    ax.hist(x, bins=bins, density=True, color=PALETTE[0], edgecolor="white", alpha=0.85)
    grid = np.linspace(x.min(), x.max(), 200)
    ax.plot(grid, sps.norm.pdf(grid, x.mean(), x.std(ddof=1)), color=_NORMAL_CURVE, lw=2)
    ax.set_xlabel(xlabel or getattr(data, "name", ""))
    ax.set_ylabel("Density")
    if title:
        ax.set_title(title)
    return ax


def qq_plot(data, *, ax=None, title: str = ""):
    """Normal Q-Q plot with a reference line through the quartiles."""
    x = pd.Series(data).dropna()
    if ax is None:
        _, ax = plt.subplots()
    sps.probplot(x, dist="norm", plot=ax)
    ax.get_lines()[0].set(marker="o", markersize=3, alpha=0.6, color=PALETTE[0], linestyle="none")
    ax.get_lines()[1].set(color=_NORMAL_CURVE, lw=2)
    ax.set_title(title or "Normal Q-Q plot")
    ax.set_xlabel("Theoretical quantiles")
    ax.set_ylabel("Sample quantiles")
    return ax


def normality_panel(data, *, label: str = "", figsize=(11, 4.0)):
    """Histogram and Q-Q plot side by side - the standard visual normality check."""
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    histogram_with_normal(data, xlabel=label, ax=axes[0], title=f"Distribution of {label}".strip())
    qq_plot(data, ax=axes[1], title=f"Q-Q plot: {label}".strip(": "))
    fig.tight_layout()
    return fig


def scatter_with_fit(data: pd.DataFrame, x: str, y: str, *, xlabel="", ylabel="", ax=None):
    """Scatterplot with a least-squares line and its 95% confidence band."""
    sub = data[[x, y]].dropna()
    if ax is None:
        _, ax = plt.subplots()

    ax.scatter(sub[x], sub[y], s=14, alpha=0.45, color=PALETTE[0], edgecolor="none")
    slope, intercept, *_ = sps.linregress(sub[x], sub[y])
    grid = np.linspace(sub[x].min(), sub[x].max(), 100)
    ax.plot(grid, intercept + slope * grid, color=_NORMAL_CURVE, lw=2)

    n = len(sub)
    resid = sub[y] - (intercept + slope * sub[x])
    se = np.sqrt((resid**2).sum() / (n - 2))
    sxx = ((sub[x] - sub[x].mean()) ** 2).sum()
    band = sps.t.ppf(0.975, n - 2) * se * np.sqrt(1 / n + (grid - sub[x].mean()) ** 2 / sxx)
    ax.fill_between(
        grid, intercept + slope * grid - band, intercept + slope * grid + band,
        color=_NORMAL_CURVE, alpha=0.15, lw=0,
    )
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    return ax


def grouped_box(data: pd.DataFrame, outcome: str, group: str, *, ylabel="", ax=None,
                order: list | None = None):
    """Boxplot by group with the individual observations jittered behind it.

    Levels are sorted unless `order` is given, matching the ordering used by
    math9102.report, so a figure and the sentence describing it agree.
    """
    sub = data[[outcome, group]].dropna()
    levels = list(order) if order else sorted(pd.unique(sub[group]), key=str)
    series = [sub.loc[sub[group] == lv, outcome].to_numpy() for lv in levels]
    if ax is None:
        _, ax = plt.subplots()

    rng = np.random.default_rng(0)  # fixed so the figure is reproducible
    for i, values in enumerate(series, start=1):
        ax.scatter(
            i + rng.uniform(-0.09, 0.09, len(values)), values,
            s=10, alpha=0.3, color=PALETTE[0], edgecolor="none", zorder=1,
        )
    bp = ax.boxplot(series, tick_labels=[str(lv) for lv in levels], widths=0.5, patch_artist=True, zorder=2)
    for patch in bp["boxes"]:
        patch.set(facecolor="white", alpha=0.85, edgecolor=PALETTE[0])
    for median in bp["medians"]:
        median.set(color=_NORMAL_CURVE, lw=2)

    ax.set_ylabel(ylabel or outcome)
    ax.set_xlabel(group)
    return ax
