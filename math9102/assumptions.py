"""Model diagnostics.

Replaces the R `performance::check_*` family, which has no direct Python
equivalent, and avoids three common errors (C3, C4, C2):

* ``residuals / sd(residuals)`` is not a standardised residual: the correct
  denominator is ``s * sqrt(1 - h_ii)``, which varies case by case, so the
  shortcut gets the ranges wrong.
* Influence on coefficients screened with ``dfbeta()`` (unstandardised)
  against the ``|1|`` threshold is wrong: that threshold belongs to the
  standardised ``dfbetas()``.
* Normality is assessed on model residuals, not on the pooled outcome, and
  Shapiro-Wilk at n of a few hundred is not treated as a verdict.
* A non-significant test is never reported as confirming an assumption (C11):
  it found no evidence of a problem, which is a weaker statement.
* Collinearity is measured per *term*, so a categorical predictor's dummies
  are one block whose number does not depend on the reference category (G72).
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as sps

from .plots import PALETTE, qq_plot

__all__ = [
    "Check",
    "check_normality",
    "check_homoscedasticity",
    "check_collinearity",
    "check_influence",
    "check_model",
    "residual_panel",
]


@dataclass
class Check:
    """One assumption check: what was tested, the numbers, and what it means."""

    name: str
    statistic: float | None
    p_value: float | None
    passed: bool | None
    message: str

    def __repr__(self) -> str:  # pragma: no cover - display only
        mark = {True: "ok", False: "warn", None: "--"}[self.passed]
        return f"[{mark:>4}] {self.name}: {self.message}"


LARGE_N = 200


def _p4(p: float) -> str:
    """A check message's p to four places, floored: "p = 0.0000" reads as zero."""
    return "p < 0.0001" if p < 0.0001 else f"p = {p:.4f}"


def _at_threshold(p: float, alpha: float = 0.05) -> bool:
    """True when p reports as alpha itself, "p = .050", to three places.

    Either verdict then contradicts the number the reader is shown: "no
    evidence" beside a p that reads as the line, or "evidence" beside one that
    does not read as below it. Such a p is reported as at the conventional
    threshold, with no verdict, and the plot decides.
    """
    return bool(np.isfinite(p)) and f"{p:.3f}" == f"{alpha:.3f}"


def check_normality(model, alpha: float = 0.05) -> Check:
    """Shapiro-Wilk on the model residuals, reported with its sample-size caveat.

    From LARGE_N residuals up, `passed` is None, not a verdict (ADR-049). At
    that size the test detects departures too small to affect the regression,
    so the Q-Q plot decides, and a flag that read "warn" on a test the
    message itself discounts would contradict the message. Below it the flag
    is the test's, with the test's limits.
    """
    resid = np.asarray(model.resid, dtype=float)
    n = len(resid)

    if n > 5000:
        stat, p = sps.normaltest(resid)
        test, symbol = "D'Agostino-Pearson", "K²"
    else:
        stat, p = sps.shapiro(resid)
        test, symbol = "Shapiro-Wilk", "W"

    large = n >= LARGE_N
    if _at_threshold(p, alpha):
        caveat = (" The test sits at the conventional threshold, which is no verdict "
                  "either way: the Q-Q plot decides the question.")
    elif large and p < alpha:
        caveat = (" The test found a departure, but at this sample size it detects "
                  "departures too small to affect the regression, so the Q-Q plot "
                  "decides the question.")
    elif large:
        caveat = (" The test found no departure; at this sample size the Q-Q plot "
                  "decides the question either way.")
    else:
        caveat = " A non-significant result is no evidence of a problem, not proof of normality."
    return Check(
        "Normality of residuals",
        float(stat),
        float(p),
        None if large or _at_threshold(p, alpha) else bool(p >= alpha),
        f"{test} {symbol} = {stat:.3f}, {_p4(p)} on {n} residuals.{caveat}",
    )


def check_homoscedasticity(model, alpha: float = 0.05) -> Check:
    """Breusch-Pagan test for non-constant residual variance.

    This is Koenker's studentised version on the model's predictors, statsmodels'
    default, which does not assume the residuals are normal (ADR-049). R's
    `performance::check_heteroscedasticity` runs the original test on the
    fitted values, so its p-value differs by design. Either way, a
    non-significant result is no evidence of changing variance, not proof of
    constant variance: the residuals-against-fitted plot is read as well.
    """
    from statsmodels.stats.diagnostic import het_breuschpagan

    lm_stat, lm_p, _, _ = het_breuschpagan(model.resid, model.model.exog)
    df = int(np.linalg.matrix_rank(model.model.exog)) - 1
    passed = None if _at_threshold(lm_p, alpha) else bool(lm_p >= alpha)
    return Check(
        "Homoscedasticity",
        float(lm_stat),
        float(lm_p),
        passed,
        f"Breusch-Pagan (Koenker) LM = {lm_stat:.3f} on {df} df, {_p4(lm_p)}. "
        + {
            True: "No evidence that the residual variance changes with the predictors; "
            "read the residuals-against-fitted plot as well.",
            False: "The residual variance changes with the predictors, so the ordinary "
            "standard errors are unreliable; consider robust (HC3) standard errors.",
            None: "At the conventional threshold, which is no verdict either way: read "
            "the residuals-against-fitted plot, and compare robust (HC3) standard errors.",
        }[passed],
    )


def _term_columns(model) -> dict[str, list[int]]:
    """Each model term's columns in the design matrix, intercept left out.

    A formula model knows which dummy columns make up one categorical term;
    a model fitted on arrays has one column per term.
    """
    names = list(model.model.exog_names)
    design = getattr(model.model.data, "design_info", None)
    if design is not None:
        terms = {
            name: list(range(sl.start, sl.stop))
            for name, sl in design.term_name_slices.items()
        }
    else:
        terms = {name: [i] for i, name in enumerate(names)}
    return {t: cols for t, cols in terms.items() if t.lower() not in {"intercept", "const"}}


def check_collinearity(model, warn: float = 5.0) -> pd.DataFrame:
    """Collinearity per model term: VIF, or the generalised VIF for a block.

    A categorical predictor enters as several dummies, and a VIF per dummy
    depends on which category is the reference: a small reference group makes
    every dummy look collinear with the others (G72). So each *term* gets one
    number, Fox and Monette's (1992) generalised VIF:

        GVIF = det(R_term) * det(R_rest) / det(R)

    on the correlation matrix R of the predictors. For a one-column term it is
    the ordinary VIF. For a term of df columns, the `VIF` column holds
    GVIF^(1/df) - the square of Fox and Monette's GVIF^(1/(2 df)) - so that the
    usual conventions read the same way for every term: above 5 warrants
    investigation and above 10 is serious. Tolerance is 1/VIF. The intercept
    is excluded, since its VIF is not interpretable.
    """
    exog = np.asarray(model.model.exog, dtype=float)
    terms = _term_columns(model)
    columns = [c for cols in terms.values() for c in cols]
    rows = []
    if columns:
        corr = np.atleast_2d(np.corrcoef(exog[:, columns], rowvar=False))
        position = {c: i for i, c in enumerate(columns)}
        det_all = np.linalg.det(corr)
        for term, cols in terms.items():
            inside = [position[c] for c in cols]
            outside = [i for i in range(len(columns)) if i not in inside]
            det_rest = np.linalg.det(corr[np.ix_(outside, outside)]) if outside else 1.0
            gvif = float(np.linalg.det(corr[np.ix_(inside, inside)]) * det_rest / det_all)
            df = len(cols)
            vif = gvif ** (1 / df)
            rows.append(
                {
                    "predictor": term,
                    "df": df,
                    "VIF": round(vif, 3),
                    "tolerance": round(1 / vif, 3),
                    "GVIF": round(gvif, 3),
                    "concern": "serious" if vif > 10 else "investigate" if vif > warn else "ok",
                }
            )
    return pd.DataFrame(rows, columns=["predictor", "df", "VIF", "tolerance", "GVIF", "concern"])


def check_influence(model, top: int = 10) -> pd.DataFrame:
    """Per-case influence diagnostics.

    Returns the most influential cases ranked by Cook's distance, with correctly
    computed internally studentised residuals, leverage, and *standardised*
    DFBETAS - the quantity the |1| threshold actually applies to.

    `case` is the row label in the data the model was fitted on, as
    `model.outlier_test()` uses, so a case can be looked up with `data.loc`. A
    position in the model's rows refers to nothing in the data once rows have
    been dropped (G75).
    """
    infl = model.get_influence()
    n = int(model.nobs)
    k = int(model.df_model) + 1

    cooks = infl.cooks_distance[0]
    leverage = infl.hat_matrix_diag
    student = infl.resid_studentized_internal
    dfbetas = np.abs(infl.dfbetas).max(axis=1)  # standardised, worst coefficient

    lev_threshold = 2 * k / n
    labels = model.model.data.row_labels
    out = pd.DataFrame(
        {
            "case": np.asarray(labels) if labels is not None else np.arange(n),
            "cooks_d": np.round(cooks, 5),
            "leverage": np.round(leverage, 5),
            "std_residual": np.round(student, 3),
            "max_abs_dfbetas": np.round(dfbetas, 3),
            "flag": [
                ", ".join(
                    f
                    for f in (
                        "cook>1" if c > 1 else "",
                        f"leverage>{lev_threshold:.3f}" if h > lev_threshold else "",
                        "|resid|>3.29" if abs(r) > 3.29 else "",
                        "|dfbetas|>1" if d > 1 else "",
                    )
                    if f
                )
                for c, h, r, d in zip(cooks, leverage, student, dfbetas)
            ],
        }
    )
    return out.sort_values("cooks_d", ascending=False).head(top).reset_index(drop=True)


def check_model(model) -> list[Check]:
    """Run the standard assumption battery and return the findings."""
    checks = [check_normality(model), check_homoscedasticity(model)]

    vif = check_collinearity(model)
    if len(vif):
        worst = vif.loc[vif["VIF"].idxmax()]
        checks.append(
            Check(
                "Multicollinearity",
                float(worst["VIF"]),
                None,
                bool(worst["VIF"] <= 5),
                f"Highest VIF is {worst['VIF']:.2f} ({worst['predictor']}), "
                f"tolerance {worst['tolerance']:.2f}.",
            )
        )

    infl = model.get_influence()
    max_cook = float(infl.cooks_distance[0].max())
    n_extreme = int((np.abs(infl.resid_studentized_internal) > 3.29).sum())
    checks.append(
        Check(
            "Influential cases",
            max_cook,
            None,
            bool(max_cook < 1),
            f"Largest Cook's distance is {max_cook:.4f}; {n_extreme} case(s) have "
            f"standardised residuals beyond ±3.29.",
        )
    )
    return checks


def residual_panel(model, figsize=(11, 8)):
    """The four standard regression diagnostic plots in one figure.

    The residuals are standardised (statsmodels' internally studentised ones,
    R's `rstandard`): each divided by its own standard error, using the model's
    *s*. The outlier test's studentised residuals leave the case out of *s*.
    """
    fitted = np.asarray(model.fittedvalues, dtype=float)
    infl = model.get_influence()
    student = infl.resid_studentized_internal
    leverage = infl.hat_matrix_diag
    cooks = infl.cooks_distance[0]

    fig, axes = plt.subplots(2, 2, figsize=figsize)

    axes[0, 0].scatter(fitted, model.resid, s=12, alpha=0.4, color=PALETTE[0], edgecolor="none")
    axes[0, 0].axhline(0, color=PALETTE[3], lw=1.5, ls="--")
    axes[0, 0].set(xlabel="Fitted values", ylabel="Residuals", title="Residuals vs fitted")

    qq_plot(student, ax=axes[0, 1], title="Normal Q-Q (standardised)")

    axes[1, 0].scatter(
        fitted, np.sqrt(np.abs(student)), s=12, alpha=0.4, color=PALETTE[0], edgecolor="none"
    )
    axes[1, 0].set(xlabel="Fitted values", ylabel="√|standardised residual|", title="Scale-location")

    axes[1, 1].scatter(leverage, student, s=12, alpha=0.4, color=PALETTE[0], edgecolor="none")
    axes[1, 1].axhline(0, color=PALETTE[3], lw=1, ls="--")
    threshold = 2 * (int(model.df_model) + 1) / int(model.nobs)
    axes[1, 1].axvline(threshold, color=PALETTE[1], lw=1, ls=":")
    axes[1, 1].set(xlabel="Leverage", ylabel="Standardised residual", title="Residuals vs leverage")

    worst = int(np.argmax(cooks))
    axes[1, 1].annotate(
        f"max Cook's D = {cooks[worst]:.3f}",
        xy=(leverage[worst], student[worst]),
        xytext=(0.55, 0.06),
        textcoords="axes fraction",
        fontsize=9,
        arrowprops=dict(arrowstyle="->", lw=0.8, color="0.4"),
    )

    fig.tight_layout()
    return fig
