# Compared models must be fitted on the same rows: select every
# variable either model uses, drop missing rows once, fit both on that.
assert model1.model.data.row_labels.equals(model2.model.data.row_labels)

# Does girl add anything? The F-test for the extra term.
sm.stats.anova_lm(model1, model2)

# And how much R squared moved.
model2.rsquared - model1.rsquared
