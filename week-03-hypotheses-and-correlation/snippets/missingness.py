# What listwise deletion costs, for the variables the model actually uses.
scales = ["toptim", "tmast", "tposaff", "tnegaff", "tlifesat",
          "tpstress", "tslfest", "tmarlow", "tpcoiss"]

everything = m9.missingness(survey, scales)
print(everything.attrs["summary"])

two_only = m9.missingness(survey, ["tpcoiss", "tpstress"])
print(two_only.attrs["summary"])
