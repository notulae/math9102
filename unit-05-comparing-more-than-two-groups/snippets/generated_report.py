# Step 6. Every number in the sentence comes from the data and the result,
# both degrees of freedom included - Welch's second one is not n - k.
m9.report_anova(survey, "toptim", "agegp3", welch,
                outcome_label="Total Optimism", order=ages)
