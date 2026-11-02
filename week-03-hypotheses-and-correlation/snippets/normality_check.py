# Visual first. The panel is a histogram with a normal curve and a Q-Q plot.
m9.normality_panel(survey.tpcoiss.dropna(), label="Total perceived control")

# Then the numbers, as descriptions of shape rather than as a verdict.
m9.report_normality(survey, "tpcoiss", "Total perceived control")
