"""Generated result narratives.

This module exists to enforce the project's first principle: **no statistic is
ever typed into prose**. Every formatter here derives its numbers from the data
and from a live result object, and returns rendered Markdown.

Statistics typed by hand into prose drift from the analysis they describe: a
report can quote means for the wrong variable directly beneath output showing
the right ones, or an effect size its own test statistic contradicts (A1, A3).
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
    "report_partial_correlation",
    "report_anova",
    "report_kruskal",
    "report_chisquare",
    "report_regression",
    "report_model_comparison",
    "report_diagnostics",
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


def _bounded(value: float, dp: int = 2) -> str:
    """Format a statistic that cannot exceed one in size without its leading zero.

    APA drops the zero wherever a statistic cannot be greater than one - *r*,
    *R²*, η², ω², Cramér's *V* - as ``fmt_p`` already does for *p*; *d*, *b*, an
    odds ratio and Cook's distance can exceed one and keep it (ADR-050). The sign
    stays an ASCII hyphen, so a value copied out of a report still reads as a
    number.
    """
    text = fmt(value, dp)
    if text.startswith("0."):
        return text[1:]
    if text.startswith("-0."):
        return "-" + text[2:]
    return text


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

    Skew and kurtosis ratios and Shapiro-Wilk are near-certain to flag at n of a
    few hundred, so a verdict from them alone says more about the sample size than
    the shape (C2). Here the sample-size dependence is stated as part of the
    finding.
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
        f"*U* = {fmt(u, 1)}, {fmt_p(p)}, rank-biserial *r* = {_bounded(r)} "
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
        f"correlation, which was {verdict}: *r*({n - 2}) = {_bounded(r)}, {fmt_p(p)}, "
        f"*n* = {n}. The correlation describes association only and does not on its "
        f"own establish that one variable causes the other."
    )


def report_partial_correlation(
    data: pd.DataFrame,
    x: str,
    y: str,
    covar: str | list[str],
    result,
    *,
    x_label: str | None = None,
    y_label: str | None = None,
    covar_label: str | None = None,
) -> Markdown:
    """Narrate a partial correlation beside the zero-order one, on the same rows.

    `result` is pingouin's `partial_corr(data, x, y, covar=...)`. The partial
    correlation is recomputed here and must agree: a semi-partial correlation
    (pingouin's `x_covar` or `y_covar`, ppcor's `spcor`) removes the covariate
    from one variable only, and has been reported as a partial one (B19). The
    zero-order correlation is computed on the same complete cases, so the two
    can be compared, and the degrees of freedom are n - 2 - k for k covariates.
    """
    import pingouin as pg

    covars = [covar] if isinstance(covar, str) else list(covar)
    sub = data[[x, y, *covars]].dropna()
    n, k = len(sub), len(covars)
    r = float(result["r"].iloc[0])
    p_col = "p_val" if "p_val" in result.columns else "p-val"
    p = float(result[p_col].iloc[0])

    partial = float(pg.partial_corr(sub, x, y, covar=covars)["r"].iloc[0])
    if abs(partial - r) > 1e-6 or int(result["n"].iloc[0]) != n:
        raise ValueError(
            f"this result (r = {r:.3f}, n = {int(result['n'].iloc[0])}) is not the partial "
            f"correlation of {x} and {y} controlling for {', '.join(covars)} on the complete "
            f"cases (r = {partial:.3f}, n = {n}). A semi-partial correlation removes the "
            "covariate from one variable only; pass partial_corr(..., covar=...)"
        )

    zero = float(np.corrcoef(sub[x], sub[y])[0, 1])
    x_label, y_label = x_label or x, y_label or y
    covar_label = covar_label or ", ".join(covars)
    verdict = "statistically significant" if p < 0.05 else "not statistically significant"
    direction = "positive" if r > 0 else "negative"
    shift = abs(zero) - abs(r)
    moved = (
        f"controlling for {covar_label} moved it {fmt(abs(shift))} towards zero"
        if shift > 0
        else f"controlling for {covar_label} moved it {fmt(abs(shift))} away from zero"
    )

    return md(
        f"The partial correlation between {x_label} and {y_label}, controlling for "
        f"{covar_label}, was {verdict}: *r*({n - 2 - k}) = {_bounded(r)}, {fmt_p(p)}, *n* = {n}, "
        f"a {effects.interpret(r, 'r')} {direction} association. On the same {n} cases "
        f"the zero-order correlation was *r* = {_bounded(zero)}, so {moved}. A partial "
        f"correlation removes {covar_label} from both variables. It describes association "
        f"only, and controlling for one measured variable does not rule out others."
    )


def _levels(data: pd.DataFrame, outcome: str, group: str, order: list | None = None):
    """Split an outcome by a grouping variable of any number of levels.

    The many-group counterpart of `_groups`. Sorting is a poor default for many
    real groupings - "<= 37" sorts after "51+" - so pass `order` whenever the
    levels have one.
    """
    sub = data[[outcome, group]].dropna()
    present = set(sub[group])
    levels = list(order) if order else sorted(present, key=str)
    missing = [lv for lv in levels if lv not in present]
    if missing:
        raise ValueError(f"level(s) not present in {group!r}: {missing}")
    unlisted = sorted(present - set(levels), key=str)
    if unlisted:
        raise ValueError(f"`order` leaves out level(s) of {group!r}: {unlisted}")
    return sub, levels, [sub.loc[sub[group] == lv, outcome] for lv in levels]


def _oneway_f(groups) -> tuple[float, float, float]:
    """The classic F, Welch's F, and Welch's denominator df, from the data.

    scipy's `f_oneway(..., equal_var=False)` returns Welch's F and p but no
    degrees of freedom, so the df a report prints has to come from here.
    """
    arrays = [np.asarray(g, dtype=float) for g in groups]
    k = len(arrays)
    n = np.array([len(a) for a in arrays], dtype=float)
    means = np.array([a.mean() for a in arrays])
    variances = np.array([a.var(ddof=1) for a in arrays])

    grand = np.concatenate(arrays).mean()
    ms_between = (n * (means - grand) ** 2).sum() / (k - 1)
    ms_within = ((n - 1) * variances).sum() / (n.sum() - k)
    classic = ms_between / ms_within

    w = n / variances
    weighted_mean = (w * means).sum() / w.sum()
    spread = (w * (means - weighted_mean) ** 2).sum() / (k - 1)
    lam = ((1 - w / w.sum()) ** 2 / (n - 1)).sum()
    welch = spread / (1 + 2 * (k - 2) * lam / (k**2 - 1))
    return float(classic), float(welch), float((k**2 - 1) / (3 * lam))


def report_anova(
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
    """Narrate a one-way ANOVA, Welch's by default (ADR-001).

    A typed F(...) can carry the wrong degrees of freedom, or the F statistic
    where the p-value belongs (A7). Here F and p come from the result object and
    both df from the data.

    The F in `result` is checked against the one the data give. scipy's Welch
    result carries no df, and an earlier version of this function fell back to
    n - k - the classic denominator - so it would have printed a Welch F beside
    the wrong df. A mismatch now raises rather than narrating the wrong test:
    passing the classic F with welch=True is the mistake it catches.
    """
    outcome_label = outcome_label or outcome
    sub, levels, series = _levels(data, outcome, group, order)
    labels = [(group_labels or {}).get(lv, str(lv)) for lv in levels]
    k = len(series)

    classic, welch_f, welch_df2 = _oneway_f(series)
    f, p = float(result.statistic), float(result.pvalue)
    expected = welch_f if welch else classic
    if not np.isclose(f, expected, rtol=1e-6):
        which = "Welch's" if welch else "the classic"
        raise ValueError(
            f"result.statistic = {f:.4f} is not {which} F for these data "
            f"({expected:.4f}). Pass welch={not welch} if that is the test you ran."
        )
    df2 = fmt(welch_df2, 1) if welch else str(len(sub) - k)

    eta2 = effects.eta_squared(series)
    omega2 = effects.omega_squared(series)
    significant = p < 0.05
    verdict = "a statistically significant" if significant else "no statistically significant"
    kind = "Welch's one-way ANOVA" if welch else "A one-way between-groups ANOVA"
    desc = "; ".join(
        f"{lab} (*n* = {len(g)}, *M* = {fmt(g.mean())}, *SD* = {fmt(g.std(ddof=1))})"
        for lab, g in zip(labels, series)
    )
    limit = (
        "The test establishes that the group means are not all equal; it does not "
        "say which of them differ, which is what the post-hoc comparisons are for."
        if significant
        else "This is not evidence that the group means are equal: the data do not "
        "provide sufficient evidence that they differ."
    )

    return md(
        f"{kind} was conducted to compare {outcome_label} across {k} groups: "
        f"{desc}. There was {verdict} difference between the groups, "
        f"*F*({k - 1}, {df2}) = {fmt(f)}, {fmt_p(p)}, "
        f"η² = {_bounded(eta2, 3)}, ω² = {_bounded(omega2, 3)} "
        f"({effects.interpret(omega2, 'eta2')}). {limit}"
    )


def _quantile_label(series: pd.Series, q: float, value_labels: dict) -> str:
    """A quantile of coded ordinal data, named by its category.

    A quantile falling between two codes is named as lying between them rather
    than rounded to one, which would claim a precision the data do not have.
    """
    v = float(series.quantile(q))
    if v.is_integer():
        return str(value_labels[int(v)])
    lo, hi = int(np.floor(v)), int(np.ceil(v))
    return f"between {value_labels[lo]} and {value_labels[hi]}"


def report_kruskal(
    data: pd.DataFrame,
    outcome: str,
    group: str,
    result,
    *,
    outcome_label: str | None = None,
    group_labels: dict[str, str] | None = None,
    order: list | None = None,
    value_labels: dict | None = None,
) -> Markdown:
    """Narrate a Kruskal-Wallis test, with medians and IQRs and eta squared (H).

    `value_labels` maps the codes of an ordinal outcome to its categories, so a
    median grade is reported as a grade rather than as a code. The statistic is
    always printed, and the test is not described as comparing medians, which it
    does not (A10).
    """
    outcome_label = outcome_label or outcome
    sub, levels, series = _levels(data, outcome, group, order)
    labels = [(group_labels or {}).get(lv, str(lv)) for lv in levels]
    k, n = len(series), len(sub)

    h, p = float(result.statistic), float(result.pvalue)
    eta2h = effects.eta_squared_h(h, k, n)
    verdict = "a statistically significant" if p < 0.05 else "no statistically significant"

    if value_labels:
        desc = "; ".join(
            f"{lab} (*n* = {len(s):,}, *Mdn* = {_quantile_label(s, .5, value_labels)}, "
            f"middle half from {_quantile_label(s, .25, value_labels)} "
            f"to {_quantile_label(s, .75, value_labels)})"
            for lab, s in zip(labels, series)
        )
    else:
        desc = "; ".join(
            f"{lab} (*n* = {len(s):,}, *Mdn* = {fmt(s.median())}, "
            f"*IQR* = {fmt(s.quantile(.75) - s.quantile(.25))})"
            for lab, s in zip(labels, series)
        )

    return md(
        f"A Kruskal-Wallis test was conducted to compare {outcome_label} across "
        f"{k} groups: {desc}. There was {verdict} difference between the groups, "
        f"*H*({k - 1}) = {fmt(h)}, {fmt_p(p)}, η²(*H*) = {_bounded(eta2h, 3)} "
        f"({effects.interpret(eta2h, 'eta2')}). The test compares whole "
        f"distributions of ranks, so it supports a conclusion about which groups "
        f"tend to score higher, not about the medians alone."
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
        f"Cramér's *V* = {_bounded(v, 3)} ({effects.interpret(v, 'v')}).{caveat}"
    )


# ------------------------------------------------------------------------ models


_SE_KIND = {"cluster": "cluster-robust", "HAC": "autocorrelation-robust (HAC)"}


def _label(term: str, labels: dict) -> str:
    return labels.get(term, term)


def _blocks(terms: list[str], labels: dict) -> list[str]:
    """Name a categorical predictor once, not dummy by dummy.

    `marital[T.b]` and `marital[T.c]` become "marital (2 dummies)"; a term with
    its own entry in `labels`, or a lone dummy, keeps its own name.
    """
    stems: dict[str, list[str]] = {}
    for term in terms:
        stems.setdefault(term.split("[T.")[0] if "[T." in term else term, []).append(term)
    named = []
    for stem, members in stems.items():
        if len(members) > 1 and not any(m in labels for m in members):
            named.append(f"{labels.get(stem, stem)} ({len(members)} dummies)")
        else:
            named.extend(_label(m, labels) for m in members)
    return named


def _listing(items: list[str]) -> str:
    """'a', 'a and b', 'a, b and c'."""
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} and {items[-1]}"


def report_regression(model, *, outcome_label: str, predictor_labels: dict | None = None) -> Markdown:
    """Narrate a fitted statsmodels OLS model, including the fitted equation.

    What the paragraph carries, and why:

    * *R²* is what the model "accounts for" in this sample, with its magnitude
      named as Cohen's convention for *R²*, not as "a large effect" - it
      describes the model, not any one predictor. Adjusted *R²* sits beside
      it at the same precision; it is an estimate for the population, and it
      is not what the model accounts for here (A6).
    * Every coefficient carries its 95% confidence interval.
    * "Holding the others constant" appears only when there are others to
      hold. With an interaction in the model, a main effect is read where the
      terms it interacts with are zero, and the paragraph says so (A11).
    * A closing sentence says what the model does not establish: cause (C9).
    * Robust or cluster-robust standard errors are named, and *F* is given
      with the degrees of freedom its test actually used.
    """
    labels = predictor_labels or {}
    params, pvals, ci = model.params, model.pvalues, model.conf_int()
    terms = [t for t in params.index if t != "Intercept"]

    equation = f"{fmt(params.get('Intercept', 0.0), 3)}" + "".join(
        f" {'+' if params[t] >= 0 else '-'} {fmt(abs(params[t]), 3)} × {_label(t, labels)}"
        for t in terms
    )
    coefs = "; ".join(
        f"{_label(t, labels)}, *b* = {fmt(params[t], 3)} "
        f"[{fmt(ci.loc[t, 0], 3)}, {fmt(ci.loc[t, 1], 3)}], {fmt_p(pvals[t])}"
        for t in terms
    )
    verdict = "statistically significant" if model.f_pvalue < 0.05 else "not statistically significant"
    df_denom = int(getattr(model, "df_resid_inference", None) or model.df_resid)
    r2 = float(model.rsquared)

    se_kind = _SE_KIND.get(model.cov_type, f"heteroscedasticity-robust ({model.cov_type})")
    se_note = "" if model.cov_type == "nonrobust" else f" Standard errors are {se_kind}."
    if any(":" in t for t in terms):
        reading = (
            " With an interaction in the model, each main-effect coefficient is that "
            "predictor's difference where the terms it interacts with are zero."
        )
    elif len(terms) > 1:
        reading = " Each coefficient is read holding the other predictors constant."
    else:
        reading = ""
    subject = (
        f"that {_label(terms[0], labels)} causes"
        if len(terms) == 1
        else "that any of these predictors causes"
    )

    return md(
        f"A linear regression model was fitted to predict {outcome_label} from "
        f"{len(terms)} predictor term{'s' if len(terms) != 1 else ''} "
        f"(*N* = {int(model.nobs):,}). The overall model was {verdict}, "
        f"*F*({int(model.df_model)}, {df_denom}) = {fmt(model.fvalue)}, "
        f"{fmt_p(model.f_pvalue)}. *R²* = {_bounded(r2, 3)}: the model accounts for "
        f"{fmt(r2 * 100, 1)}% of the variance in {outcome_label} in this sample, "
        f"{effects.interpret(r2, 'r2')} by Cohen's convention for *R²* "
        f"(adjusted *R²* = {_bounded(model.rsquared_adj, 3)}).{se_note}\n\n"
        f"Coefficients, with 95% confidence intervals: {coefs}.{reading}\n\n"
        f"Fitted equation: {outcome_label} = {equation}\n\n"
        f"The model describes an association in these data. It does not establish "
        f"{subject} {outcome_label}."
    )


def _same_rows(smaller, larger) -> bool:
    rows_s, rows_l = smaller.model.data.row_labels, larger.model.data.row_labels
    if rows_s is None or rows_l is None or len(rows_s) != len(rows_l):
        return False
    return bool(pd.Index(rows_s).equals(pd.Index(rows_l))) and np.array_equal(
        np.asarray(smaller.model.endog), np.asarray(larger.model.endog)
    )


def report_model_comparison(smaller, larger, *, predictor_labels: dict | None = None) -> Markdown:
    """Compare two nested models fitted on the same rows.

    For OLS, the nested *F*-test and the change in *R²*; for a logistic model
    (GLM or Logit), the likelihood-ratio χ². The test is computed here with
    statsmodels' `anova_lm` (OLS) or from the two log-likelihoods (logistic),
    so it is the standard test, narrated.

    **It refuses two models fitted on different rows** (B20). Models fitted on
    different rows differ in their data as well as their predictors, so
    neither *F* nor the change in *R²* compares the predictors. The check is
    on the row labels *and* the outcome values, so a reloaded or altered
    outcome with the same index is refused too. Select every variable either
    model uses, drop missing rows once, and fit both on that.

    It also refuses models of different outcomes, a pair that is not nested,
    and robust-SE fits, whose classical nested *F* would not match the
    standard errors they report.
    """
    labels = predictor_labels or {}
    ols = hasattr(smaller, "ssr")
    if ols != hasattr(larger, "ssr"):
        raise ValueError("compare two OLS models or two logistic models, not one of each")
    if smaller.model.endog_names != larger.model.endog_names:
        raise ValueError(
            f"the models predict different outcomes ({smaller.model.endog_names!r} and "
            f"{larger.model.endog_names!r}); a nested comparison needs one outcome"
        )
    if not _same_rows(smaller, larger):
        raise ValueError(
            f"the models were not fitted on the same rows (n = {int(smaller.nobs)} and "
            f"n = {int(larger.nobs)}), so their difference mixes a change of data with "
            "a change of predictors. Select every variable either model uses, drop "
            "missing rows once, and fit both models on that"
        )
    small_terms, large_terms = list(smaller.model.exog_names), list(larger.model.exog_names)
    if not set(small_terms) < set(large_terms):
        raise ValueError(
            "the models are not nested: every term of the smaller model must be in the "
            "larger one, and the larger must add at least one"
        )
    if ols and (smaller.cov_type != "nonrobust" or larger.cov_type != "nonrobust"):
        raise ValueError(
            "compare the models fitted with ordinary standard errors: the nested F-test "
            "assumes them. For robust standard errors use larger.wald_test(...) instead"
        )

    added = [t for t in large_terms if t not in small_terms]
    added_text = _listing(_blocks(added, labels))
    kept = [t for t in small_terms if t != "Intercept"]
    base = _listing(_blocks(kept, labels)) if kept else "the intercept alone"
    n = int(larger.nobs)

    if ols:
        import statsmodels.api as sm

        table = sm.stats.anova_lm(smaller, larger)
        f, p = float(table["F"].iloc[1]), float(table["Pr(>F)"].iloc[1])
        df_num, df_den = int(table["df_diff"].iloc[1]), int(table["df_resid"].iloc[1])
        r2_s, r2_l = float(smaller.rsquared), float(larger.rsquared)
        verdict = "a statistically significant" if p < 0.05 else "not a statistically significant"
        return md(
            f"Adding {added_text} to the model with {base} (both fitted on the same "
            f"*N* = {n:,} rows) changed *R²* by {_bounded(r2_l - r2_s, 3)}, from "
            f"{_bounded(r2_s, 3)} to {_bounded(r2_l, 3)}. This was {verdict} improvement, "
            f"*F*({df_num}, {df_den}) = {fmt(f)}, {fmt_p(p)}."
        )

    from scipy import stats

    chi2 = 2 * (float(larger.llf) - float(smaller.llf))
    df = int(round(float(larger.df_model) - float(smaller.df_model)))
    p = float(stats.chi2.sf(chi2, df))
    verdict = "a statistically significant" if p < 0.05 else "not a statistically significant"
    return md(
        f"Adding {added_text} to the model with {base} (both fitted on the same "
        f"*N* = {n:,} rows) was {verdict} improvement by the likelihood-ratio test, "
        f"χ²({df}) = {fmt(chi2)}, {fmt_p(p)}; the log-likelihood rose from "
        f"{fmt(float(smaller.llf))} to {fmt(float(larger.llf))}."
    )


def report_diagnostics(
    model, *, plots: str, design: str | None = None, predictor_labels: dict | None = None
) -> Markdown:
    """The diagnostic paragraph for a fitted OLS model, generated after fitting.

    It reports what each check found, and never more (A8, C11):

    * `plots` is your own reading of the residual plots, in a sentence. It is
      required: the plots are the primary evidence, and no function can look at
      them for you. It comes first, as inspection comes before the tests.
    * A non-significant test is reported as no evidence of a problem, never as
      confirming an assumption, and a test whose *p* reports as .050 as at the
      conventional threshold, with no verdict either way.
    * Standardised residuals are internally studentised, e / (s sqrt(1 - h)),
      not e / sd(e) (C3), and the case named by the Bonferroni outlier test is
      the data's own row label, which you can look up.
    * Influence on the coefficients uses standardised DFBETAS against 1
      (ADR-003), beside Cook's distance against 1.
    * Collinearity is per term, generalised for categorical blocks (G72).
    * Independence is a property of how the data were collected, and none of
      these checks tests it. Say how in `design`; without it, the paragraph says
      independence was not examined.
    """
    from scipy import stats
    from statsmodels.stats.diagnostic import het_breuschpagan

    from . import assumptions

    n = int(model.nobs)
    k = int(model.df_model) + 1
    infl = model.get_influence()
    student = np.asarray(infl.resid_studentized_internal)
    external = np.asarray(infl.resid_studentized_external)
    cooks = np.asarray(infl.cooks_distance[0])
    dfbetas = np.abs(np.asarray(infl.dfbetas))
    leverage = np.asarray(infl.hat_matrix_diag)
    labels = model.model.data.row_labels
    labels = list(labels) if labels is not None else list(range(n))

    normal = assumptions.check_normality(model)
    test = "Shapiro–Wilk" if n <= 5000 else "D'Agostino–Pearson"
    symbol = "*W*" if n <= 5000 else "*K*²"
    large = n >= assumptions.LARGE_N
    if assumptions._at_threshold(normal.p_value):
        normal_reading = ("the test sits at the conventional threshold, which is no verdict "
                          "either way, so the plots are the evidence.")
    elif large and normal.p_value < 0.05:
        normal_reading = ("the test found a departure, but at this sample size it detects "
                          "departures too small to affect the model, so the plots are the "
                          "evidence.")
    elif large:
        normal_reading = ("the test found no departure, and at this sample size the plots "
                          "are the evidence either way.")
    elif normal.p_value >= 0.05:
        normal_reading = ("the test found no evidence of non-normality, which is not proof "
                          "of normality.")
    else:
        normal_reading = "the test found evidence of non-normality."
    normal_text = (
        f"{test} {symbol} = {(_bounded if n <= 5000 else fmt)(normal.statistic, 3)}, "
        f"{fmt_p(normal.p_value)} on {n} residuals; {normal_reading}"
    )

    worst = int(np.argmax(np.abs(external)))
    p_unadj = 2 * stats.t.sf(abs(external[worst]), model.df_resid - 1)
    p_bonf = min(1.0, p_unadj * n)
    beyond_329 = int((np.abs(student) > 3.29).sum())
    share_196 = float((np.abs(student) > 1.96).mean())
    outlier_text = (
        f"Standardised residuals ranged from {fmt(student.min())} to {fmt(student.max())}; "
        + ("no case" if beyond_329 == 0 else f"{beyond_329} case{'s' if beyond_329 != 1 else ''}")
        + " lay beyond ±3.29, and "
        f"{fmt(share_196 * 100, 1)}% beyond ±1.96, against the 5% expected. The most extreme "
        f"case (row {labels[worst]}) gave a Bonferroni-adjusted outlier test "
        f"{fmt_p(p_bonf)}"
        + (", so it is an outlier by that test." if p_bonf < 0.05 else ".")
    )

    over_cook, over_dfbetas = int((cooks > 1).sum()), int((dfbetas.max(axis=1) > 1).sum())
    lev_cut = 2 * k / n
    over_lev = int((leverage > lev_cut).sum())
    influence_text = (
        f"The largest Cook's distance was {fmt(cooks.max(), 3)} "
        + ("(none above 1)" if over_cook == 0 else f"({over_cook} above 1)")
        + f", and the largest standardised DFBETAS {fmt(dfbetas.max(), 2)} "
        + ("(none above 1)" if over_dfbetas == 0 else f"({over_dfbetas} above 1)")
        + f"; {over_lev} case{'s' if over_lev != 1 else ''} had leverage above 2*k*/*n* = "
        f"{_bounded(lev_cut, 3)}."
    )

    lm_stat, lm_p, _, _ = het_breuschpagan(model.resid, model.model.exog)
    bp_df = int(np.linalg.matrix_rank(model.model.exog)) - 1
    variance_text = (
        f"A Breusch–Pagan test (Koenker's version) gave χ²({bp_df}) = {fmt(lm_stat)}, "
        f"{fmt_p(lm_p)}: "
        + (
            "at the conventional threshold, which is no verdict either way; the "
            "residual plot, and a refit with robust standard errors, are the evidence."
            if assumptions._at_threshold(lm_p)
            else "no evidence that the residual variance changes with the predictors."
            if lm_p >= 0.05
            else "evidence that the residual variance changes with the predictors, so the "
            "ordinary standard errors are unreliable."
        )
    )

    vif = assumptions.check_collinearity(model)
    if len(vif):
        top = vif.loc[vif["VIF"].idxmax()]
        collinear_text = (
            f"The largest variance inflation factor was {fmt(top['VIF'])} "
            f"({(predictor_labels or {}).get(top['predictor'], top['predictor'])}"
            + (", generalised for a categorical block" if int(top["df"]) > 1 else "")
            + f"), tolerance {_bounded(top['tolerance'])}."
        )
    else:
        collinear_text = "With one predictor there is no collinearity to assess."

    independence_text = (
        f"On independence: {design.strip().rstrip('.')}."
        if design
        else "Independence was not examined: it depends on how the observations were "
        "collected, which none of these checks can see."
    )

    return md(
        f"{plots.strip().rstrip('.')}. {normal_text} {outlier_text} {influence_text} "
        f"{variance_text} {collinear_text} {independence_text}"
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
        f"{fmt_p(lr_p)}. Pseudo-*R²* values were Cox–Snell = {_bounded(r2['cox_snell'], 3)}, "
        f"Nagelkerke = {_bounded(r2['nagelkerke'], 3)}, Tjur = {_bounded(r2['tjur'], 3)}. "
        f"Odds ratios: {ors}."
    )
