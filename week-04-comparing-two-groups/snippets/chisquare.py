# Chi-square of independence. correction=True applies Yates, which is what you
# want for a 2x2 table; scipy applies it only to 2x2 tables in any case.
table = m9.crosstab(bully.dropna(subset=["ubullsch", "ubulloth"]),
                    "ubullsch", "ubulloth")

chi2, p, dof, expected = stats.chi2_contingency(table, correction=True)

# Check the assumption before you read the result, not after.
print(f"smallest expected count: {expected.min():.1f}")
print(f"Cramer's V = {m9.cramers_v(table):.3f}")
