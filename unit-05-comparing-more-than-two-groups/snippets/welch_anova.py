# Step 4. Welch is the default. The classic F is shown only for comparison -
# never choose between them on the outcome of a variance test.
welch = stats.f_oneway(*groups, equal_var=False)
classic = stats.f_oneway(*groups)

print(f"Welch: F = {welch.statistic:.3f}, p = {welch.pvalue:.4f}")
print(f"Classic: F = {classic.statistic:.3f}, p = {classic.pvalue:.4f}")

# scipy gives F and p. pingouin also prints Welch's degrees of freedom.
pg.welch_anova(data=opt, dv="toptim", between="agegp3")
