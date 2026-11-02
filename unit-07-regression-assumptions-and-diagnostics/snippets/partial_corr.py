import pingouin as pg

# Social desirability removed from both variables: a partial correlation.
result = pg.partial_corr(rows, x="tpcoiss", y="tpstress", covar="tmarlow")
m9.report_partial_correlation(rows, "tpcoiss", "tpstress", "tmarlow", result)
