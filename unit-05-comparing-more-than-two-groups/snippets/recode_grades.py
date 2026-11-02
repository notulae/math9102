# An ordinal outcome stored as text. Write the order out in full,
# then check that the recode lost nothing it should not have.
grades = ["A*", "A", "B", "C", "D", "E", "F", "G", "Fail"]
youth["mathcode"] = youth.gradmath.map({g: i + 1 for i, g in enumerate(grades)})

lost = youth.gradmath.notna() & youth.mathcode.isna()
print(f"grades lost to the recode: {lost.sum()}")
