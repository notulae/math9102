# Step 2. Describe the grouping variable, then the outcome within each group.
# Group sizes come first: an effect size means little without them.
m9.frequency(survey, "child")
m9.describe_by(survey, "tpstress", "child")

# What a complete-case analysis costs, on the model variables only -
# never on the whole dataframe.
missing = m9.missingness(survey, ["tpstress", "child"])
print(missing.attrs["summary"])
