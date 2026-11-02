"""Effect sizes.

Each function is a plain, testable computation, written to avoid a known pitfall
(the defect register's ids in brackets):

* cohens_d uses the unequal-n pooled form. The shortcut d = 2t/sqrt(df) assumes
  equal group sizes, so with unequal groups it is only an approximation, however
  often it is stated as exact (C6).
* cramers_v is computed from the table rather than transcribed, because a typed
  V cannot be checked against the chi-square it came from (A3).
* omega_squared sits beside eta_squared because eta squared is the share of
  variance in *this sample*, and overstates the population share most when the
  groups are small.
* icc says how alike observations in one cluster are, and so how far a
  standard error that treats them as independent overstates the precision
  (D3, ADR-007).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

__all__ = [
    "cohens_d",
    "hedges_g",
    "eta_squared_from_t",
    "eta_squared",
    "omega_squared",
    "eta_squared_h",
    "cramers_v",
    "rank_biserial",
    "pseudo_r2",
    "icc",
    "interpret",
]


def cohens_d(x, y) -> float:
    """Cohen's d for two independent samples, pooled SD, unequal n allowed."""
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    y = np.asarray(pd.Series(y).dropna(), dtype=float)
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        raise ValueError("each group needs at least two observations")
    pooled_var = ((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2)
    return float((x.mean() - y.mean()) / np.sqrt(pooled_var))


def hedges_g(x, y) -> float:
    """Cohen's d with the small-sample bias correction."""
    x = pd.Series(x).dropna()
    y = pd.Series(y).dropna()
    n = len(x) + len(y)
    return float(cohens_d(x, y) * (1 - 3 / (4 * n - 9)))


def eta_squared_from_t(t: float, df: float) -> float:
    """Eta squared from a t statistic: t^2 / (t^2 + df)."""
    return float(t**2 / (t**2 + df))


def eta_squared(groups) -> float:
    """Eta squared for one-way ANOVA: between-group SS over total SS."""
    arrays = [np.asarray(pd.Series(g).dropna(), dtype=float) for g in groups]
    all_values = np.concatenate(arrays)
    grand_mean = all_values.mean()
    ss_between = sum(len(a) * (a.mean() - grand_mean) ** 2 for a in arrays)
    ss_total = ((all_values - grand_mean) ** 2).sum()
    return float(ss_between / ss_total)


def omega_squared(groups) -> float:
    """Omega squared for one-way ANOVA: the population share of variance.

    (SS_between - (k - 1) MS_within) / (SS_total + MS_within). It corrects eta
    squared's upward bias, which is largest for small groups, and can come out
    slightly negative when the group means differ by less than chance predicts;
    that is reported as it is, not clipped to zero.
    """
    arrays = [np.asarray(pd.Series(g).dropna(), dtype=float) for g in groups]
    all_values = np.concatenate(arrays)
    grand_mean = all_values.mean()
    k, n = len(arrays), len(all_values)
    ss_between = sum(len(a) * (a.mean() - grand_mean) ** 2 for a in arrays)
    ss_total = ((all_values - grand_mean) ** 2).sum()
    ms_within = (ss_total - ss_between) / (n - k)
    return float((ss_between - (k - 1) * ms_within) / (ss_total + ms_within))


def eta_squared_h(h: float, k: int, n: int) -> float:
    """Eta squared for a Kruskal-Wallis test: (H - k + 1) / (n - k).

    The rank-based share of variance (Tomczak and Tomczak, 2014) - what
    rstatix::kruskal_effsize reports. Read it against the same benchmarks as
    eta squared.
    """
    return float((h - k + 1) / (n - k))


def cramers_v(table, correct: bool = False) -> float:
    """Cramer's V for a contingency table.

    correct=True applies the Bergsma bias correction, which matters for small
    tables; the uncorrected form is what the module's textbooks report.
    """
    table = np.asarray(table, dtype=float)
    chi2 = stats.chi2_contingency(table, correction=False)[0]
    n = table.sum()
    r, k = table.shape

    if not correct:
        return float(np.sqrt(chi2 / (n * (min(r, k) - 1))))

    phi2 = max(0.0, chi2 / n - (k - 1) * (r - 1) / (n - 1))
    r_c = r - (r - 1) ** 2 / (n - 1)
    k_c = k - (k - 1) ** 2 / (n - 1)
    return float(np.sqrt(phi2 / (min(r_c, k_c) - 1)))


def rank_biserial(x, y) -> float:
    """Rank-biserial correlation: the effect size for a Mann-Whitney test.

    Computed from U directly, so it is stable when ties are present, and it has a
    direct reading: (rank_biserial + 1) / 2 is the probability that a randomly
    chosen member of the first group scores above one from the second.

    Note this is *not* the same quantity as `wilcoxon_r`, although both are
    conventionally written 'r'. See that function for the distinction.
    """
    x = pd.Series(x).dropna()
    y = pd.Series(y).dropna()
    u = stats.mannwhitneyu(x, y, alternative="two-sided").statistic
    return float(2 * u / (len(x) * len(y)) - 1)


def wilcoxon_r(x, y) -> float:
    """Rosenthal's r = |z| / sqrt(N) for a Mann-Whitney test.

    This is the older convention, and the one rstatix::wilcox_effsize reports.
    It is here because you will meet it in textbooks and in R output.

    It is not interchangeable with `rank_biserial`: on the module's week 4
    example this returns about 0.78 where the rank-biserial correlation is 0.92.
    Report whichever you choose, name it, and do not mix the two.
    """
    x = pd.Series(x).dropna()
    y = pd.Series(y).dropna()
    n = len(x) + len(y)

    n1, n2 = len(x), len(y)
    u = stats.mannwhitneyu(x, y, alternative="two-sided").statistic
    mean_u = n1 * n2 / 2

    # Tie-corrected standard deviation of U.
    ranks = stats.rankdata(np.concatenate([x, y]))
    _, tie_counts = np.unique(ranks, return_counts=True)
    tie_term = (tie_counts**3 - tie_counts).sum()
    sd_u = np.sqrt((n1 * n2 / 12) * ((n + 1) - tie_term / (n * (n - 1))))

    z = (u - mean_u) / sd_u
    return float(abs(z) / np.sqrt(n))


def pseudo_r2(model) -> dict[str, float]:
    """Cox-Snell, Nagelkerke and Tjur pseudo-R^2 for a fitted statsmodels GLM/Logit.

    Replaces DescTools::PseudoR2 and performance::r2. Computing all three from
    one model object means they cannot come from different models (B11).
    """
    n = int(model.nobs)
    llf, llnull = float(model.llf), float(model.llnull)

    cox_snell = 1 - np.exp((2 / n) * (llnull - llf))
    nagelkerke = cox_snell / (1 - np.exp((2 / n) * llnull))

    y = np.asarray(model.model.endog, dtype=float)
    fitted = np.asarray(model.fittedvalues, dtype=float)
    if fitted.min() < 0 or fitted.max() > 1:  # Logit exposes the linear predictor
        fitted = np.asarray(model.predict(), dtype=float)
    tjur = float(fitted[y == 1].mean() - fitted[y == 0].mean())

    return {"cox_snell": float(cox_snell), "nagelkerke": float(nagelkerke), "tjur": tjur}


def icc(data: pd.DataFrame, outcome: str, cluster: str) -> dict[str, float]:
    """ICC(1) of `outcome` within `cluster`, and the design effect it implies.

    ICC(1) is estimated from the one-way ANOVA mean squares, with the average
    cluster size n0 adjusted for unequal clusters:

        ICC = (MSB - MSW) / (MSB + (n0 - 1) MSW)

    It can come out slightly below zero when clusters differ less than chance
    alone would make them. The design effect is Kish's 1 + (m - 1) ICC, with m
    the mean cluster size: roughly how many times larger the sampling variance
    is than a simple random sample of the same size would give. Its square root
    is the factor an OLS standard error understates by, for a predictor that
    varies only between clusters.

    Rows missing the outcome or the cluster are dropped first. The regression
    data's 4,059 pupils in 65 schools are the case this exists for: OLS treats
    them as 4,059 independent observations (D3).
    """
    sub = data[[outcome, cluster]].dropna()
    by_cluster = sub.groupby(cluster)[outcome]
    k, n, sizes = by_cluster.ngroups, len(sub), by_cluster.size()
    if k < 2:
        raise ValueError(f"icc needs at least two clusters; {cluster!r} has {k}")
    msb = (sizes * (by_cluster.mean() - sub[outcome].mean()) ** 2).sum() / (k - 1)
    msw = ((sub[outcome] - by_cluster.transform("mean")) ** 2).sum() / (n - k)
    n0 = (n - (sizes**2).sum() / n) / (k - 1)
    value = (msb - msw) / (msb + (n0 - 1) * msw)
    mean_size = float(sizes.mean())
    return {
        "icc": float(value),
        "n_clusters": int(k),
        "mean_cluster_size": mean_size,
        "design_effect": float(1 + (mean_size - 1) * value),
    }


# Cohen's conventions. Deliberately returned as words with the benchmark visible,
# so students report a magnitude rather than treating a threshold as a verdict.
_BENCHMARKS: dict[str, list[tuple[float, str]]] = {
    "d": [(0.2, "negligible"), (0.5, "small"), (0.8, "medium"), (np.inf, "large")],
    "r": [(0.1, "negligible"), (0.3, "small"), (0.5, "medium"), (np.inf, "large")],
    "eta2": [(0.01, "negligible"), (0.06, "small"), (0.14, "medium"), (np.inf, "large")],
    "v": [(0.1, "negligible"), (0.3, "small"), (0.5, "medium"), (np.inf, "large")],
    "r2": [(0.02, "negligible"), (0.13, "small"), (0.26, "medium"), (np.inf, "large")],
}


def interpret(value: float, kind: str = "d") -> str:
    """Describe an effect size using Cohen's conventions.

    kind is one of 'd', 'r', 'eta2', 'v', 'r2'. Use 'eta2' for eta squared, omega
    squared and the Kruskal-Wallis eta squared alike: all three are shares of
    variance and share Cohen's .01 / .06 / .14.

    The 'v' benchmarks (.1 / .3 / .5) are Cohen's w, and they hold for a table
    whose smaller side is 2 - every contingency table this module reports. They
    shrink with the smaller side: for a table k columns or rows across, divide
    them by sqrt(k - 1), so .1/.3/.5 becomes .07/.21/.35 at k = 3. Week 4's
    effect-size slide carries the table. Passing a V from a larger table here
    would overstate how small the association is.

    The 'r2' benchmarks (.02 / .13 / .26) are a regression model's R squared,
    converted from Cohen's f squared of .02 / .15 / .35 (Cohen, 1992, "A power
    primer", Psychological Bulletin 112, 155-159) by R^2 = f^2 / (1 + f^2).
    They describe how much of the outcome's variation the model accounts for,
    not how large any one predictor's effect is, so report them as "by Cohen's
    convention for R squared".
    """
    if kind not in _BENCHMARKS:
        raise ValueError(f"kind must be one of {sorted(_BENCHMARKS)}")
    magnitude = abs(float(value))
    for threshold, label in _BENCHMARKS[kind]:
        if magnitude < threshold:
            return label
    return "large"
