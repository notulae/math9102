# Dunn's test on the same pooled ranks. The correction is not optional:
# fifteen pairs at .05 would turn up a false positive more often than not.
pairs = m9.dunn(kw, "mathcode", "famsec", p_adjust="holm", order=classes)
pairs[["A", "B", "z", "p_unadj", "p_adj"]]
