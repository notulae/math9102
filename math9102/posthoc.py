"""Post-hoc comparisons the standard stack does not provide.

Games-Howell and Tukey are in pingouin and scipy, and the notebooks call them
there. Dunn's test - the follow-up to a Kruskal-Wallis test, and the one SPSS
and R's FSA and rstatix report - is in none of scipy, statsmodels or pingouin,
so it is here, short enough to read.

The correction for multiple comparisons is a required argument with no default.
Which correction you applied is part of the result, and a default would make it
a decision nobody took.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

__all__ = ["dunn"]


def dunn(
    data: pd.DataFrame,
    outcome: str,
    group: str,
    *,
    p_adjust: str,
    order: list | None = None,
) -> pd.DataFrame:
    """Dunn's pairwise test on the ranks a Kruskal-Wallis test used.

    Every pair is compared on its mean rank in the *pooled* ranking, with the
    standard error corrected for ties, so the follow-up answers the question the
    omnibus asked. (Pairwise Mann-Whitney tests re-rank each pair separately and
    can disagree with it.)

    p_adjust is any method statsmodels' multipletests accepts: "holm" and
    "bonferroni" are the two this module teaches.

    Returns one row per pair: the two groups, their mean ranks, z, and the
    unadjusted and adjusted p-values.
    """
    sub = data[[outcome, group]].dropna()
    levels = list(order) if order else sorted(pd.unique(sub[group]), key=str)

    ranks = stats.rankdata(sub[outcome])
    n = len(ranks)
    _, ties = np.unique(ranks, return_counts=True)
    variance = n * (n + 1) / 12 - (ties**3 - ties).sum() / (12 * (n - 1))

    mean_rank = {lv: ranks[(sub[group] == lv).to_numpy()].mean() for lv in levels}
    size = {lv: int((sub[group] == lv).sum()) for lv in levels}

    rows = []
    for a, b in combinations(levels, 2):
        se = np.sqrt(variance * (1 / size[a] + 1 / size[b]))
        z = (mean_rank[a] - mean_rank[b]) / se
        rows.append({"A": a, "B": b, "mean_rank_A": mean_rank[a],
                     "mean_rank_B": mean_rank[b], "z": z,
                     "p_unadj": 2 * stats.norm.sf(abs(z))})

    out = pd.DataFrame(rows)
    out["p_adj"] = multipletests(out["p_unadj"], method=p_adjust)[1]
    out.attrs["p_adjust"] = p_adjust
    return out
