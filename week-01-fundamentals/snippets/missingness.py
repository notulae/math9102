# What a complete-case analysis would cost, for the variables you are using -
# never for the whole dataframe.
cheap = m9.missingness(msleep, ["sleep_total", "vore"])
print(cheap.attrs["summary"])

expensive = m9.missingness(msleep, ["sleep_cycle", "brainwt", "vore"])
print(expensive.attrs["summary"])

# Same data, same function. Choose the variables first, then count the cost.
