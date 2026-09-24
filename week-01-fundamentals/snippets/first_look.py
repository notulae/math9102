# Datasets are loaded by name, never by path. A path is a fact about one
# computer; a name is a fact about the analysis.
salaries = m9.load_salaries()

print(salaries.shape)
salaries.dtypes

# dtypes tell you how Python stores the column. They do NOT tell you the level
# of measurement - that is your judgement, and it decides what is legitimate.
salaries.head()
