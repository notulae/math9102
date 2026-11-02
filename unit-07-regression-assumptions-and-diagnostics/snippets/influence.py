# The cases the model leans on most: Cook's distance, leverage,
# standardised residuals and the largest standardised DFBETAS.
m9.check_influence(model1, top=5)
