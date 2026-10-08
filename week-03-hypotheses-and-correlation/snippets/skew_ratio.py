# The standardised skew ratio: skew divided by its standard error.
x = survey.tpcoiss.dropna()
n = len(x)

skew = stats.skew(x, bias=False)
se_skew = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))

print(f"skew = {skew:.3f}, standardised = {skew / se_skew:.2f}")

# The SE depends only on n, so the ratio grows with n for a fixed shape.
