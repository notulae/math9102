"""Generated result narratives.

This module exists to enforce the project's first principle: **no statistic is
ever typed into prose**. Every formatter here derives its numbers from the data
and from a live result object, and returns rendered Markdown.

The legacy module hand-typed 221 statistics into narrative text across 21 files,
and they drifted. Its week 4 report printed "M = 33.20 ... M = 33.64" for
"self-esteem" directly beneath its own rendered output showing means of 27.04 and
26.34 for perceived stress; week 11 reported Cramer's V = .01 where its own
chi-square gives 0.112; week 8 gave a single coefficient two different p-values.
Generating the sentence from the result object makes that class of error
impossible rather than merely unlikely.

Descriptive statistics are recomputed here from the supplied data, so the
descriptives quoted in a sentence always match the data analysed. The test
statistic must be passed in, so the notebook still visibly performs the test.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from IPython.display import Markdown

from . import effects

__all__ = [
    "fmt_p",
    "fmt",
    "md",
    "report_normality",
    "report_ttest",
    "report_mannwhitney",
    "report_correlation",
    "report_anova",
    "report_chisquare",
    "report_regression",
    "report_logistic",
]


def fmt_p(p: float) -> str:
    """Format a p-value to APA convention.

    Probabilities are reported without a leading zero, and anything below .001 is
    reported as an inequality rather than as a spuriously precise number - the
    convention the module's own hypothesis-testing lecture states.
    """
    p = float(p)
    if not np.isfinite(p):
        return "p = NA"
    if p < 0.001:
        return "*p* < .001"
    return f"*p* = {p:.3f}".replace("0.", ".", 1)


def fmt(value: float, dp: int = 2) -> str:
    """Format a statistic to a fixed number of decimal places."""
    if value is None or not np.isfinite(float(value)):
        return "NA"
    return f"{float(value):.{dp}f}"


def md(text: str) -> Markdown:
    """Render a generated string as Markdown output."""
    return Markdown(text)


def _groups(data: pd.DataFrame, outcome: str, group: str, order: list | None = None):
    """Split an outcome by a two-level grouping variable, dropping missing pairs.

    Levels are sorted unless an explicit `order` is given, so the generated
    sentence does not change when the row order of the data changes.
    """
    sub = data[[outcome, group]].dropna()
    levels = list(order) if order else sorted(pd.unique(sub[group]), key=str)
    if len(levels) != 2:
        raise ValueError(f"{group!r} has {len(levels)} levels; expected exactly 2")
    missing = [lv for lv in levels if lv not in set(sub[group])]
    if missing:
        raise ValueError(f"level(s) not present in {group!r}: {missing}")
    return sub, levels, [sub.loc[sub[group] == lv, outcome] for lv in levels]


def _describe(series: pd.Series) -> tuple[int, float, float]:
    return len(series), float(series.mean()), float(series.std(ddof=1))


# --------------------------------------------------------------------- normality


def report_normality(data: pd.DataFrame, column: str, label: str | None = None) -> Markdown:
    """Narrate a normality assessment, visual first and sample-size aware.

    The legacy material assessed normality with standardised skew and kurtosis
    ratios and Shapiro-Wilk at n of roughly 400, where both are near-certain to
    flag, then argued around the result in identical wording in about eight
    files. Here the sample-size dependence is stated as part of the finding.
    """
    from scipy import stats as sps

    label = label or column
    x = data[column].dropna()
    n = len(x)
    skew, kurt = float(sps.skew(x, bias=False)), float(sps.kurtosis(x, bias=False))
    se_skew = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    se_kurt = 2 * se_skew * np.sqrt((n**2 - 1) / ((n - 3) * (n + 5)))
    z_skew, z_kurt = skew / se_skew, kurt / se_kurt

    pct_329 = float((np.abs((x - x.mean()) / x.std(ddof=1)) > 3.29).mean() * 100)

    sensitivity = (
        "At this sample size the standardised ratios are highly sensitive, so they "
        "are reported as descriptions of shape rather than as a pass/fail test"
        if n >= 200
        else "The sample is small enough that these ratios have limited power, so "
        "the visual evidence carries most of the weight"
    )

    return md(
        f"{label} was assessed for normality using the histogram and Q-Q plot above, "
        f"supported by shape statistics (*N* = {n}, *M* = {fmt(x.mean())}, "
        f"*SD* = {fmt(x.std(ddof=1))}). Skewness was {fmt(skew)} "
        f"(standardised {fmt(z_skew)}) and kurtosis {fmt(kurt)} "
        f"(standardised {fmt(z_kurt)}). {sensitivity}. "
        f"{fmt(pct_329, 1)}% of standardised scores fell beyond ±3.29, against "
        f"about 0.1% expected under normality."
    )


# ------------------------------------------------------------------- comparisons


def report_ttest(
    data: pd.DataFrame,
    outcome: str,
    group: str,
    result,
    *,
    outcome_label: str | None = None,
    group_labels: dict[str, str] | None = None,
    order: list | None = None,
    welch: bool = True,
) -> Markdown:
    """Narrate an independent-samples t-test.

    `result` is a scipy ttest_ind result; group descriptives are recomputed from
    `data` so they cannot disagree with the data actually analysed. The direction
    of the difference is stated in words rather than left to the sign of *t*,
    which depends on the order the caller passed the groups to scipy.
    """
    outcome_label = outcome_label or outcome
    sub, levels, series = _groups(data, outcome, group, order)
    labels = [(group_labels or {}).get(lv, str(lv).lower()) for lv in levels]
    (n1, m1, s1), (n2, m2, s2) = (_describe(s) for s in series)

    d = effects.cohens_d(series[0], series[1])
    df = float(getattr(result, "df", n1 + n2 - 2))
    t, p = float(result.statistic), float(result.pvalue)
    significant = p < 0.05
    verdict = "a statistically significant" if significant else "no statistically significant"
    kind = (
        "Welch's independent-samples *t*-test"
        if welch
        else "An independent-samples *t*-test (pooled variance)"
    )
    direction = (
        f" {labels[0].capitalize()} scored {fmt(abs(m1 - m2))} points "
        f"{'higher' if m1 > m2 else 'lower'} on average."
        if significant
        else ""
    )

    return md(
        f"{kind} was conducted to compare {outcome_label} between "
        f"{labels[0]} (*n* = {n1}, *M* = {fmt(m1)}, *SD* = {fmt(s1)}) and "
        f"{labels[1]} (*n* = {n2}, *M* = {fmt(m2)}, *SD* = {fmt(s2)}). "
        f"There was {verdict} difference, "
        f"*t*({fmt(df, 1)}) = {fmt(abs(t))}, {fmt_p(p)}, "
        f"Cohen's *d* = {fmt(abs(d))} ({effects.interpret(d, 'd')}).{direction}"
    )


def report_mannwhitney(
    data: pd.DataFrame,
    outcome: str,
    group: str,
    result,
    *,
    outcome_label: str | None = None,
    group_labels: dict[str, str] | None = None,
    order: list | None = None,
) -> Markdown:
    """Narrate a Mann-Whitney U test, reporting medians and rank-biserial r."""
    outcome_label = outcome_label or outcome
    sub, levels, series = _groups(data, outcome, group, order)
    labels = [(group_labels or {}).get(lv, str(lv).lower()) for lv in levels]

    r = effects.rank_biserial(series[0], series[1])
    u, p = float(result.statistic), float(result.pvalue)
    verdict = "a statistically significant" if p < 0.05 else "no statistically significant"
    described = [
        f"{lab} (*Mdn* = {fmt(s.median())}, *IQR* = {fmt(s.quantile(.75) - s.quantile(.25))})"
        for lab, s in zip(labels, series)
    ]
    stats_txt = " and ".join(described)

    return md(
        f"A Mann-Whitney *U* test was conducted to compare {outcome_label} between "
        f"{stats_txt}. There was {verdict} difference, "
        f"*U* = {fmt(u, 1)}, {fmt_p(p)}, rank-biserial *r* = {fmt(r)} "
        f"({effects.interpret(r, 'r')}). The test compares the whole distributions, "
        f"so it supports a conclusion about which group tends to score higher rather "
        f"than about the medians alone."
    )


def report_correlation(
    data: pd.DataFrame,
    x: str,
    y: str,
    result,
    *,
    method: str = "Pearson",
    x_label: str | None = None,
    y_label: str | None = None,
) -> Markdown:
    """Narrate a correlation, with n taken from the complete pairs actually used."""
    n = len(data[[x, y]].dropna())
    r, p = float(result.statistic), float(result.pvalue)
    direction = "positive" if r > 0 else "negative"
    verdict = "statistically significant" if p < 0.05 else "not statistically significant"

    return md(
        f"The relationship between {x_label or x} and {y_label or y} was examined using "
        f"a {method} correlation. There was a {effects.interpret(r, 'r')} {direction} "
        f"correlation, which was {verdict}: *r*({n - 2}) = {fmt(r)}, {fmt_p(p)}, "
        f"*n* = {n}. The correlation describes association only and does not on its "
        f"own establish that one variable causes the other."
    )


def report_anova(
    data: pd.DataFrame,
    outcome: str,
    group: str,
    result,
    *,
    outcome_label: str | None = None,
    welch: bool = True,
) -> Markdown:
    """Narrate a one-way ANOVA.

    The legacy week 5 report printed three degrees of freedom in F(...) and gave
    the F statistic where the p-value belonged. Deriving both from the result
    object removes the opportunity for that.
    """
    outcome_label = outcome_label or outcome
    sub = data[[outcome, group]].dropna()
    groups = [g[outcome] for _, g in sub.groupby(group)]
    names = [str(k) for k, _ in sub.groupby(group)]

    f, p = float(result.statistic), float(result.pvalue)
    df1 = len(groups) - 1
    df2 = float(getattr(result, "df", len(sub) - len(groups)))
    eta2 = effects.eta_squared(groups)
    verdict = "a statistically significant" if p < 0.05 else "no statistically significant"
    kind = "A Welch one-way ANOVA" if welch else "A one-way between-groups ANOVA"

    desc = "; ".join(
        f"{nm} (*n* = {len(g)}, *M* = {fmt(g.mean())}, *SD* = {fmt(g.std(ddof=1))})"
        for nm, g in zip(names, groups)
    )

    return md(
        f"{kind} was conducted to compare {outcome_label} across {len(groups)} groups: "
        f"{desc}. There was {verdict} difference between groups, "
        f"*F*({df1}, {fmt(df2, 1)}) = {fmt(f)}, {fmt_p(p)}, "
        f"η² = {fmt(eta2, 3)} ({effects.interpret(eta2, 'eta2')})."
    )


def report_chisquare(
    table: pd.DataFrame,
    result,
    *,
    row_label: str = "the row variable",
    col_label: str = "the column variable",
) -> Markdown:
    """Narrate a chi-square test of independence with Cramer's V computed, not quoted."""
    chi2, p, dof = float(result[0]), float(result[1]), int(result[2])
    expected = np.asarray(result[3])
    n = int(np.asarray(table).sum())
    v = effects.cramers_v(table)

    verdict = "a statistically significant" if p < 0.05 else "no statistically significant"
    small = int((expected < 5).sum())
    caveat = (
        f" {small} of {expected.size} expected counts were below 5, so the "
        f"chi-square approximation should be treated with caution."
        if small
        else ""
    )

    return md(
        f"A chi-square test of independence examined the association between "
        f"{row_label} and {col_label}. There was {verdict} association, "
        f"χ²({dof}, *N* = {n:,}) = {fmt(chi2)}, {fmt_p(p)}, "
        f"Cramér's *V* = {fmt(v, 3)} ({effects.interpret(v, 'v')}).{caveat}"
    )


# ------------------------------------------------------------------------ models


def report_regression(model, *, outcome_label: str, predictor_labels: dict | None = None) -> Markdown:
    """Narrate a fitted statsmodels OLS model, including the fitted equation."""
    labels = predictor_labels or {}
    params, pvals = model.params, model.pvalues
    terms = [t for t in params.index if t != "Intercept"]

    equation = f"{fmt(params.get('Intercept', 0.0), 3)}" + "".join(
        f" {'+' if params[t] >= 0 else '−'} {fmt(abs(params[t]), 3)} × {labels.get(t, t)}"
        for t in terms
    )
    coefs = "; ".join(
        f"{labels.get(t, t)} (*b* = {fmt(params[t], 3)}, {fmt_p(pvals[t])})" for t in terms
    )
    verdict = "statistically significant" if model.f_pvalue < 0.05 else "not statistically significant"

    return md(
        f"A linear regression model was fitted to predict {outcome_label} from "
        f"{len(terms)} predictor(s) (*N* = {int(model.nobs)}). The overall model was "
        f"{verdict}, *F*({int(model.df_model)}, {int(model.df_resid)}) = "
        f"{fmt(model.fvalue)}, {fmt_p(model.f_pvalue)}, "
        f"adjusted *R²* = {fmt(model.rsquared_adj, 3)}, meaning the predictors account "
        f"for {fmt(model.rsquared_adj * 100, 1)}% of the variance in {outcome_label}. "
        f"Coefficients: {coefs}.\n\n"
        f"Fitted equation: {outcome_label} = {equation}"
    )


def report_logistic(model, *, outcome_label: str, predictor_labels: dict | None = None) -> Markdown:
    """Narrate a fitted statsmodels logistic model with odds ratios and pseudo-R^2."""
    labels = predictor_labels or {}
    params, pvals = model.params, model.pvalues
    terms = [t for t in params.index if t != "Intercept"]
    r2 = effects.pseudo_r2(model)

    lr_p = float(model.llr_pvalue)
    verdict = "statistically significant" if lr_p < 0.05 else "not statistically significant"
    ors = "; ".join(
        f"{labels.get(t, t)} (*OR* = {fmt(np.exp(params[t]))}, {fmt_p(pvals[t])})"
        for t in terms
    )

    return md(
        f"A binary logistic regression was fitted to predict {outcome_label} "
        f"(*N* = {int(model.nobs):,}). The model was {verdict} against the "
        f"intercept-only model, χ²({int(model.df_model)}) = {fmt(model.llr)}, "
        f"{fmt_p(lr_p)}. Pseudo-*R²* values were Cox–Snell = {fmt(r2['cox_snell'], 3)}, "
        f"Nagelkerke = {fmt(r2['nagelkerke'], 3)}, Tjur = {fmt(r2['tjur'], 3)}. "
        f"Odds ratios: {ors}."
    )
