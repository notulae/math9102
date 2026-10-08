# The report sentence is generated from the data and the result object,
# so its numbers cannot drift from the analysis.
result = stats.ttest_ind(no, yes, equal_var=False)

m9.report_ttest(survey, "tpstress", "child", result,
                outcome_label="Total Perceived Stress",
                group_labels={"NO": "respondents without children",
                              "YES": "respondents with children"})
