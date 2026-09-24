"""Effect sizes.

Each function is a plain, testable computation. Several correct defects in the
legacy material:

* cohens_d uses the unequal-n pooled form. The legacy decks teach d = 2t/sqrt(df),
  which assumes equal group sizes. On the module's own worked example (n = 183
  and 249) the approximation gives -0.1182 against a true -0.1193, so it is
  harmless there, but it is stated as if exact and the deck then reports 0.06.
* cramers_v is computed here rather than transcribed. The legacy week 11 report
  states V = .01 where its own chi-square of 165.05 on N = 13201 gives V = 0.112.
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
    "cramers_v",
    "rank_biserial",
    "pseudo_r2",
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

    This is the older convention, and the one the legacy module reported via
    rstatix::wilcox_effsize. It is retained because students following the
    module's textbooks will meet it, and because it is what earlier cohorts'
    worked examples show.

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
    one model object removes the legacy defect where the week 11 Model 2 section
    reported Model 1's Tjur R^2.
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


# Cohen's conventions. Deliberately returned as words with the benchmark visible,
# so students report a magnitude rather than treating a threshold as a verdict.
_BENCHMARKS: dict[str, list[tuple[float, str]]] = {
    "d": [(0.2, "negligible"), (0.5, "small"), (0.8, "medium"), (np.inf, "large")],
    "r": [(0.1, "negligible"), (0.3, "small"), (0.5, "medium"), (np.inf, "large")],
    "eta2": [(0.01, "negligible"), (0.06, "small"), (0.14, "medium"), (np.inf, "large")],
    "v": [(0.1, "negligible"), (0.3, "small"), (0.5, "medium"), (np.inf, "large")],
}


def interpret(value: float, kind: str = "d") -> str:
    """Describe an effect size using Cohen's conventions.

    kind is one of 'd', 'r', 'eta2', 'v'.
    """
    if kind not in _BENCHMARKS:
        raise ValueError(f"kind must be one of {sorted(_BENCHMARKS)}")
    magnitude = abs(float(value))
    for threshold, label in _BENCHMARKS[kind]:
        if magnitude < threshold:
            return label
    return "large"
