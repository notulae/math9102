import statsmodels.api as sm

# The sums of squares, the mean squares and F, for the whole model.
sm.stats.anova_lm(model1)

# Or straight off the fit: F with both degrees of freedom, and R squared.
model1.fvalue, model1.df_model, model1.df_resid, model1.rsquared
