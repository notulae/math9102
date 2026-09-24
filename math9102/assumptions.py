"""Model diagnostics.

Replaces the R `performance::check_*` family, which has no direct Python
equivalent, and corrects three defects carried by the legacy material:

* Standardised residuals were computed as ``residuals / sd(residuals)`` in six
  files. That is not a standardised residual: the correct denominator divides by
  ``s * sqrt(1 - h_ii)``, which varies case by case. Reported ranges were wrong.
* Influence on coefficients was screened with ``dfbeta()`` (unstandardised)
  against the ``|1|`` threshold, which belongs to standardised ``dfbetas()``.
* Normality was assessed on the pooled outcome rather than on model residuals,
  and Shapiro-Wilk at n of roughly 400 was treated as a verdict.
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


def check_normality(model, alpha: float = 0.05) -> Check:
    """Shapiro-Wilk on the model residuals, reported with its sample-size caveat."""
    resid = np.asarray(model.resid, dtype=float)
    n = len(resid)

    if n > 5000:
        stat, p = sps.normaltest(resid)
        test = "D'Agostino-Pearson"
    else:
        stat, p = sps.shapiro(resid)
        test = "Shapiro-Wilk"

    caveat = (
        " At this sample size the test detects departures too small to affect the "
        "regression, so the Q-Q plot should decide the question."
        if n >= 200
        else ""
    )
    return Check(
        "Normality of residuals",
        float(stat),
        float(p),
        bool(p >= alpha),
        f"{test} W = {stat:.3f}, p = {p:.4f} on {n} residuals.{caveat}",
    )


def check_homoscedasticity(model, alpha: float = 0.05) -> Check:
    """Breusch-Pagan test for non-constant residual variance."""
    from statsmodels.stats.diagnostic import het_breuschpagan

    lm_stat, lm_p, _, _ = het_breuschpagan(model.resid, model.model.exog)
    passed = bool(lm_p >= alpha)
    return Check(
        "Homoscedasticity",
        float(lm_stat),
        float(lm_p),
        passed,
        f"Breusch-Pagan LM = {lm_stat:.3f}, p = {lm_p:.4f}. "
        + (
            "Residual variance is consistent with being constant."
            if passed
            else "Residual variance changes with the fitted values; consider robust "
            "(HC3) standard errors."
        ),
    )


def check_collinearity(model, warn: float = 5.0) -> pd.DataFrame:
    """Variance inflation factors and tolerances for each predictor.

    VIF above 5 warrants investigation and above 10 is serious; tolerance is
    simply 1/VIF. The intercept is excluded, since its VIF is not interpretable.
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    exog = model.model.exog
    names = list(model.model.exog_names)
    rows = []
    for i, name in enumerate(names):
        if name.lower() in {"intercept", "const"}:
            continue
        vif = float(variance_inflation_factor(exog, i))
        rows.append(
            {
                "predictor": name,
                "VIF": round(vif, 3),
                "tolerance": round(1 / vif, 3),
                "concern": "serious" if vif > 10 else "investigate" if vif > warn else "ok",
            }
        )
    return pd.DataFrame(rows)


def check_influence(model, top: int = 10) -> pd.DataFrame:
    """Per-case influence diagnostics.

    Returns the most influential cases ranked by Cook's distance, with correctly
    computed internally studentised residuals, leverage, and *standardised*
    DFBETAS - the quantity the |1| threshold actually applies to.
    """
    infl = model.get_influence()
    n = int(model.nobs)
    k = int(model.df_model) + 1

    cooks = infl.cooks_distance[0]
    leverage = infl.hat_matrix_diag
    student = infl.resid_studentized_internal
    dfbetas = np.abs(infl.dfbetas).max(axis=1)  # standardised, worst coefficient

    lev_threshold = 2 * k / n
    out = pd.DataFrame(
        {
            "case": np.arange(n),
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
    """The four standard regression diagnostic plots in one figure."""
    fitted = np.asarray(model.fittedvalues, dtype=float)
    infl = model.get_influence()
    student = infl.resid_studentized_internal
    leverage = infl.hat_matrix_diag
    cooks = infl.cooks_distance[0]

    fig, axes = plt.subplots(2, 2, figsize=figsize)

    axes[0, 0].scatter(fitted, model.resid, s=12, alpha=0.4, color=PALETTE[0], edgecolor="none")
    axes[0, 0].axhline(0, color=PALETTE[3], lw=1.5, ls="--")
    axes[0, 0].set(xlabel="Fitted values", ylabel="Residuals", title="Residuals vs fitted")

    qq_plot(student, ax=axes[0, 1], title="Normal Q-Q (studentised)")

    axes[1, 0].scatter(
        fitted, np.sqrt(np.abs(student)), s=12, alpha=0.4, color=PALETTE[0], edgecolor="none"
    )
    axes[1, 0].set(xlabel="Fitted values", ylabel="√|studentised residual|", title="Scale-location")

    axes[1, 1].scatter(leverage, student, s=12, alpha=0.4, color=PALETTE[0], edgecolor="none")
    axes[1, 1].axhline(0, color=PALETTE[3], lw=1, ls="--")
    threshold = 2 * (int(model.df_model) + 1) / int(model.nobs)
    axes[1, 1].axvline(threshold, color=PALETTE[1], lw=1, ls=":")
    axes[1, 1].set(xlabel="Leverage", ylabel="Studentised residual", title="Residuals vs leverage")

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
