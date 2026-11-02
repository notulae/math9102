# A Series holds many values of one kind. Arithmetic applies to all of them.
age = pd.Series([28, 48, 47, 71, 22, 80, 48, 30, 31])
purchase = pd.Series([20, 59, 2, 12, 22, 160, 34, 34, 29])

# A DataFrame holds several Series side by side: one row per case.
techsales = pd.DataFrame({"age": age, "purchase": purchase})

# Select rows by a condition, not by position.
techsales[techsales.age > 40]
