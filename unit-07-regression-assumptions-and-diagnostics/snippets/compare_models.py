# The rows all three models share, then each model on them.
common = survey[["tpstress", "tpcoiss", "tmarlow", "toptim", "sex"]].dropna()
m1 = smf.ols("tpstress ~ tpcoiss + tmarlow", data=common).fit()
m2 = smf.ols("tpstress ~ tpcoiss + tmarlow + toptim", data=common).fit()
m9.report_model_comparison(m1, m2)
