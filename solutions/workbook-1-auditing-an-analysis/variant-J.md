# Workbook 1, variant J: what was wrong

Read this after you have made your own findings, not instead of them. The
analysis has **3 defects** that change what it concludes. Each is below:
where it is, what is wrong and why, and the correction.

---

## 1. A normal curve drawn over a count histogram

**Where:** section 1, *The data*: the cell after the data are loaded.

**What is wrong, and why.** The histogram is drawn on the **count** scale, with bars in the tens, while the normal density is a probability density integrating to 1, so it never rises above about 0.07. The curve is not flat because the data are non-normal; it is flat because the two are on scales differing by three orders of magnitude. The comment draws a conclusion about the distribution from an artefact of the plot.

**The correction.** Put the histogram on the density scale - `plt.hist(x, bins=25, density=True)` - or use `m9.histogram_with_normal`, which does it by construction. The comparison then means something, and the conclusion drawn from it has to be revisited.

## 2. Levene's test used as a gate to choose the t-test

**Where:** section 4, *Choosing the test*: the cell that runs the test.

**What is wrong, and why.** Choosing which test to run based on the outcome of another test distorts the error rate of the test you care about, because the reported p-value does not account for the selection step. The rule is also brittle: Levene here gives p = 0.07506, and nothing about the two samples changes as that number crosses .05 - the analysis switches from one test to another on a threshold the data know nothing about. And the branch is unnecessary - Welch costs almost nothing when the variances really are equal.

**The correction.** Use Welch's test unconditionally. Report Levene and the two group standard deviations as a description of the data, and do not branch on them.

## 3. Cohen's d reported as half its value

**Where:** section 6, *Results*: the paragraph.

**What is wrong, and why.** The effect size cell prints 0.1193. The paragraph reports 0.06 - exactly half. Both are negligible here, so the conclusion happens to survive, but the reported number does not match the notebook's own output and on a larger effect the same slip would change the interpretation.

**The correction.** Report the value the notebook computed: d = 0.12. If a number in the prose disagrees with the output above it, the prose is wrong.

---

## Also worth noticing

Real, though not among the 3. A careful audit mentions them.

- Every number in the prose is typed in rather than generated from the output, so none of it can be checked without re-running the notebook. That is how defects like these get in.
- The report gives no confidence interval, for the difference or for *d*, so it cannot say how large a difference the data rule out.
- A non-significant result is reported with no comment on statistical power.

## Not wrong

Often flagged, and correct as written.

- Treating the scale totals as continuous: a defensible convention, which the notebook is entitled to.
- The two groups being unequal in size: on its own, that invalidates neither test.
- Judging normality from the plots rather than from a test: deliberate, and right at this sample size.
