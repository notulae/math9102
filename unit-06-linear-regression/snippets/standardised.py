# Standardise inside the formula: both variables in SD units.
beta = smf.ols(
    "standardize(normexam) ~ standardize(standlrt)",
    data=regression,
).fit()
beta.params
