# Mann-Whitney U compares ranks, so describe the groups with medians and IQRs.
x = bdi.loc[bdi.drink == "DrinkX", "bdiwed"]
y = bdi.loc[bdi.drink == "DrinkY", "bdiwed"]

mw = stats.mannwhitneyu(x, y, alternative="two-sided")

# Two different quantities are both written r for this test. Say which you used.
print(f"rank-biserial r = {m9.rank_biserial(x, y):.3f}")
print(f"Rosenthal's r = {m9.wilcoxon_r(x, y):.3f}")
