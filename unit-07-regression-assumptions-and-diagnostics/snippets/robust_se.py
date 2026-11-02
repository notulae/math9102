salaries = m9.load_salaries()
formula = "salary ~ yrs_since_phd"

ols = smf.ols(formula, data=salaries).fit()
hc3 = smf.ols(formula, data=salaries).fit(cov_type="HC3")
pd.DataFrame({"b": ols.params, "SE, OLS": ols.bse, "SE, HC3": hc3.bse})
