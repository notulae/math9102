# Predictions for three new pupils: one SD below the mean, at it, above it.
new_pupils = pd.DataFrame({"standlrt": [-1, 0, 1]})
model1.predict(new_pupils)
