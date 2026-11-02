# Everything at once, for the variables you name.
m9.describe(salaries, ["salary", "yrs_since_phd", "yrs_service"])

# skew and kurtosis describe SHAPE. They are descriptions, not verdicts.
m9.describe_by(salaries, "salary", "discipline")
