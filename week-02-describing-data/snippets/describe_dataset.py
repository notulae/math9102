# The description a reader needs, in the order they need it.
survey = m9.load_survey()

m9.missingness(survey, ["toptim", "tlifesat", "tpstress", "tslfest"])
m9.frequency(survey, "sex")
m9.describe(survey, ["age", "toptim", "tlifesat", "tpstress", "tslfest"])
