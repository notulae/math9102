# Step 2. The grouping variable, then the outcome within each group.
# Sorting is not an order: say what the order is once, and reuse it.
ages = ["18 - 29", "30 - 44", "45+"]
m9.frequency(survey, "agegp3")
m9.describe_by(survey, "toptim", "agegp3")

# What a complete-case analysis costs, on the model variables only.
missing = m9.missingness(survey, ["toptim", "agegp3"])
print(missing.attrs["summary"])
