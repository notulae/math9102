# Every number in the paragraph comes from the fitted model.
m9.report_regression(
    model1,
    outcome_label="exam score at 16",
    predictor_labels={"standlrt": "reading score at 11"},
)
