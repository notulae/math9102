# Studentised residuals, with Bonferroni-adjusted p-values,
# the most extreme first. The index is the row label in the
# data, so the case can be looked up.
tests = model1.outlier_test()
tests.sort_values("student_resid", key=abs, ascending=False).head(3)
