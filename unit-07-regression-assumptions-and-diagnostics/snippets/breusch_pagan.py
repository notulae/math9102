from statsmodels.stats.diagnostic import het_breuschpagan

# Koenker's version (statsmodels' default): LM statistic and its p-value.
lm, lm_p, f, f_p = het_breuschpagan(model1.resid, model1.model.exog)
m9.check_homoscedasticity(model1)
