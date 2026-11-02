# Spearman ranks the data, so it measures monotonic association rather than
# linear association. Kendall counts concordant and discordant pairs.
rho = stats.spearmanr(pairs.tpcoiss, pairs.tpstress)
tau = stats.kendalltau(pairs.tpcoiss, pairs.tpstress)

print(f"Spearman rho = {rho.statistic:.3f}, p = {rho.pvalue:.3g}")
print(f"Kendall tau = {tau.statistic:.3f}, p = {tau.pvalue:.3g}")

# Tied values are ordinary in questionnaire data. Both functions correct for
# them automatically. Ties are not an error, and they are not missing data.
print(f"tied values in tpcoiss: {pairs.tpcoiss.duplicated().sum()}")
