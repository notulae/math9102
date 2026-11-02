# The pooled form works for unequal group sizes. Use it.
d = m9.cohens_d(no, yes)
print(f"Cohen's d = {d:.3f} ({m9.interpret(d, 'd')})")

# The textbook shortcut assumes n1 == n2, so it is an approximation here.
approx = 2 * pooled.statistic / np.sqrt(len(no) + len(yes) - 2)
print(f"2t/sqrt(df) = {approx:.3f}")

# Eta squared: the share of variance in the outcome the grouping accounts for.
print(f"eta squared = {m9.eta_squared_from_t(pooled.statistic, pooled.df):.4f}")
