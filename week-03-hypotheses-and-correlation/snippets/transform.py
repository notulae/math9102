# If a variable is badly skewed you can transform it - but check the result,
# and remember the transformed variable is what you will be interpreting.
skewed = survey.tnegaff.dropna()
logged = np.log(skewed + 1)

for name, x in [("raw", skewed), ("log(x + 1)", logged)]:
    print(f"{name}: skew = {stats.skew(x, bias=False):+.3f}")

# A transformation that does not help is a transformation you do not apply.
