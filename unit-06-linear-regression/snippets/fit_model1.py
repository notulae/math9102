import statsmodels.formula.api as smf

regression = m9.load_regression()

# Outcome on the left of the tilde, predictor on the right.
model1 = smf.ols("normexam ~ standlrt", data=regression).fit()
print(model1.summary())
