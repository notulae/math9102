# girl holds text, "boy" or "girl": the formula builds the dummy.
# The reference is the first level alphabetically, so boys.
model2 = smf.ols("normexam ~ standlrt + girl", data=regression).fit()
model2.params
