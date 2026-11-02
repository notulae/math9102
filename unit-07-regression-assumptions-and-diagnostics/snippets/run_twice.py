# Fit without the case, and compare. Never delete it silently.
worst = model1.outlier_test()["student_resid"].abs().idxmax()
without = smf.ols("tpstress ~ tpcoiss + tmarlow",
                  data=rows.drop(index=worst)).fit()
pd.DataFrame({"with": model1.params, "without": without.params})
