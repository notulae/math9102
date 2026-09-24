# A z-score says how many standard deviations a value sits from the mean.
# Uninjured people average 92 with an SD of 6. Someone with a head injury scores 89.
z = (89 - 92) / 6

# The area below z is a tail probability. No printed table required.
print(f"z = {z:.2f}")
print(f"share of uninjured people this low or lower: {stats.norm.cdf(z):.4f}")

# The same idea on real data: respondents more than 2 SDs above the mean.
z_stress = (survey.tpstress - survey.tpstress.mean()) / survey.tpstress.std(ddof=1)
print(f"respondents above z = 2: {(z_stress > 2).sum()}")
