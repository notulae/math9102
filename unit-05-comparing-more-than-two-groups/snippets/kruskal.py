# Kruskal-Wallis uses only the ranks, so the codes need only be in order.
# Here 1 is A* and 9 is Fail: a LOW rank is a GOOD grade.
kw = youth.dropna(subset=["mathcode"])
by_class = [kw.loc[kw.famsec == c, "mathcode"] for c in classes]
h = stats.kruskal(*by_class)

eta2_h = m9.eta_squared_h(h.statistic, len(by_class), len(kw))
print(f"H = {h.statistic:.1f}, p = {h.pvalue:.3g}, eta squared (H) = {eta2_h:.3f}")
