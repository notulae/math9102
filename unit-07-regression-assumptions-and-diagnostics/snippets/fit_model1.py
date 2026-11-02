import statsmodels.formula.api as smf

model1 = smf.ols("tpstress ~ tpcoiss + tmarlow", data=rows).fit()
print(model1.summary())
