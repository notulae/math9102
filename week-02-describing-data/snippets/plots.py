# One plot per question. The bin width is a choice you are making, so make it
# deliberately and try more than one.
m9.histogram_with_normal(festival.day1, xlabel="Hygiene, day 1")

# Comparing groups: a boxplot shows centre, spread, skew and outliers at once.
m9.grouped_box(festival, "day1", "location", ylabel="Hygiene, day 1")
