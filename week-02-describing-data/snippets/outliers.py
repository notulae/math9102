# The conventional fence: 1.5 x IQR beyond the quartiles.
q1, q3 = festival.day1.quantile([0.25, 0.75])
iqr = q3 - q1
fence = q3 + 1.5 * iqr

flagged = festival.loc[festival.day1 > fence, "day1"]
print(f"upper fence = {fence:.2f}, values beyond it: {len(flagged)}")
print(f"largest: {flagged.max():.2f}")

# Being beyond the fence is not a reason to delete a value. It is a reason to
# find out what it is.
