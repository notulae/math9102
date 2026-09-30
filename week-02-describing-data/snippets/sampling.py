# The standard error is the SD of the sampling distribution of the mean.
# From one sample you can compute it, or bootstrap it: resample your sample
# with replacement, many times, and see how much the mean moves.
rng = np.random.default_rng(0)
sample = m9.load_festival(with_outlier=False).day1.dropna()

se_formula = sample.std(ddof=1) / np.sqrt(len(sample))
resampled = [rng.choice(sample, len(sample), replace=True).mean() for _ in range(2000)]

print(f"SE from the formula = {se_formula:.4f}")
print(f"SD of 2000 bootstrap means = {np.std(resampled, ddof=1):.4f}")
