survey = m9.load_survey()

# The model's variables first, then the rows complete on those.
model_vars = ["tpstress", "tpcoiss", "tmarlow"]
print(m9.missingness(survey, model_vars).attrs["summary"])
rows = survey[model_vars].dropna()
