# The same model, with standard errors that let pupils in one school be alike.
model4_cl = smf.ols(
    "normexam ~ standlrt + girl + C(schgend, Treatment('mixedsch'))",
    data=regression,
).fit(
    cov_type="cluster", cov_kwds={"groups": regression["school"]}, use_t=True,
)

# How much wider each standard error is. The coefficients do not move.
model4_cl.bse / model4.bse
