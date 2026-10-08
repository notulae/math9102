# Step 4b. Where is the difference? Games-Howell does not assume equal
# variances, so it is the follow-up that matches Welch's F.
gh = pg.pairwise_gameshowell(data=opt, dv="toptim", between="agegp3")
gh[["A", "B", "diff", "pval", "hedges"]]

# Tukey's HSD assumes equal variances. Shown for comparison only.
print(stats.tukey_hsd(*groups))
