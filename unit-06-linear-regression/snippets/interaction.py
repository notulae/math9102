# standlrt * girl means standlrt + girl + standlrt:girl.
# The product is built by the formula, so it always matches its parts.
model3 = smf.ols("normexam ~ standlrt * girl", data=regression).fit()
model3.params
model3.pvalues["standlrt:girl[T.girl]"]
