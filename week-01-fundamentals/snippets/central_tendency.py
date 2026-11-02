# Three answers to "the typical value", and they disagree when data are skewed.
salary = salaries.salary

print(f"mean = {salary.mean():,.0f}")
print(f"median = {salary.median():,.0f}")
print(f"mode = {salary.mode().iloc[0]:,.0f}")

# Mean above median is the signature of a tail to the right.
