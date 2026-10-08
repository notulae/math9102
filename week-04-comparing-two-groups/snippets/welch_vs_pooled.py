# Welch is the default. The pooled test is shown only for comparison -
# never choose between them on the outcome of a variance test.
welch = stats.ttest_ind(no, yes, equal_var=False)
pooled = stats.ttest_ind(no, yes, equal_var=True)

print(f"Welch: t = {welch.statistic:.4f}, p = {welch.pvalue:.4f}")
print(f"Pooled: t = {pooled.statistic:.4f}, p = {pooled.pvalue:.4f}")
