# Plot first, then test. Anscombe's quartet is the reason this order matters.
m9.scatter_with_fit(survey, "tpcoiss", "tpstress",
                    xlabel="Total perceived control",
                    ylabel="Total perceived stress")

pairs = survey[["tpcoiss", "tpstress"]].dropna()
result = stats.pearsonr(pairs.tpcoiss, pairs.tpstress)

m9.report_correlation(survey, "tpcoiss", "tpstress", result,
                      x_label="perceived control of internal states",
                      y_label="perceived stress")
