# A centre means little without a spread.
print(f"range = {salary.max() - salary.min():,.0f}")
print(f"IQR = {salary.quantile(.75) - salary.quantile(.25):,.0f}")
print(f"SD = {salary.std(ddof=1):,.0f}")

# ddof is the divisor correction. pandas defaults to 1, numpy defaults to 0,
# and they will silently disagree. Know which you are using.
print(f"pandas std = {salary.std():.3f}")
print(f"numpy std = {np.std(salary):.3f}")
