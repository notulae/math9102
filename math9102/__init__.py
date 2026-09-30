"""MATH9102 Fundamentals of Data Analysis - course support package.

A thin layer over the standard scientific Python stack. Notebooks perform their
analysis with scipy, statsmodels and pingouin directly, so students learn the
standard tools; this package supplies only what would otherwise be copied from
week to week: dataset loaders, descriptive and diagnostic panels, effect sizes,
a shared figure style, and generated result narratives.

Typical use at the top of a notebook::

    import math9102 as m9
    m9.use_house_style()
    survey = m9.load_survey()

Design rules, recorded in docs/DECISIONS.md:

1. No statistic is ever typed into prose - `report.*` generates it from the data
   and a live result object.
2. Datasets are loaded by name, never by path.
3. Helpers stay thin enough to read; nothing here hides a decision a student
   should be making.
"""

from __future__ import annotations

__version__ = "0.1.0"

from .data import (  # noqa: F401
    available,
    data_dir,
    load,
    load_bdi,
    load_bullying,
    load_experim,
    load_facebook_narcissism,
    load_festival,
    load_msleep,
    load_raq,
    load_regression,
    load_romcom,
    load_salaries,
    load_sleep,
    load_survey,
    load_websatisfaction,
    load_wine,
    load_youthcohort,
    manifest,
)
from .descriptives import (  # noqa: F401
    crosstab,
    describe,
    describe_by,
    frequency,
    missingness,
)
from .effects import (  # noqa: F401
    cohens_d,
    cramers_v,
    eta_squared,
    eta_squared_from_t,
    hedges_g,
    interpret,
    pseudo_r2,
    rank_biserial,
    wilcoxon_r,
)
from .assumptions import (  # noqa: F401
    check_collinearity,
    check_homoscedasticity,
    check_influence,
    check_model,
    check_normality,
    residual_panel,
)
from .plots import (  # noqa: F401
    PALETTE,
    grouped_box,
    histogram_with_normal,
    normality_panel,
    qq_plot,
    scatter_with_fit,
    use_house_style,
)
from .report import (  # noqa: F401
    fmt,
    fmt_p,
    md,
    report_anova,
    report_chisquare,
    report_correlation,
    report_logistic,
    report_mannwhitney,
    report_normality,
    report_regression,
    report_ttest,
)

__all__ = [n for n in dir() if not n.startswith("_")]
