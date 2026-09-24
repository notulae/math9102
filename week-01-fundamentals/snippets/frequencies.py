# For a categorical variable there is one honest summary: how many, what share.
m9.frequency(salaries, "rank")

# Two categoricals give a contingency table.
m9.crosstab(salaries, "discipline", "rank")

# Percentages within rows: of the people in this discipline, what share are at
# each rank? Column-wise answers a different question. Always say which.
m9.crosstab(salaries, "discipline", "rank", normalize="index")
