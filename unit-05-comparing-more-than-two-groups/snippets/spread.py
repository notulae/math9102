# Step 3. Describe the spread in each group. Do not branch on it.
opt = survey[["toptim", "agegp3"]].dropna()
groups = [opt.loc[opt.agegp3 == a, "toptim"] for a in ages]

sds = [g.std(ddof=1) for g in groups]
print(f"largest SD / smallest SD = {max(sds) / min(sds):.2f}")

levene = stats.levene(*groups, center="median")
print(f"Levene (median-centred): p = {levene.pvalue:.3f}")
