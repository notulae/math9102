# School type beside sex, mixed schools the reference. Each school-type
# coefficient compares one sex with the same sex at mixed schools.
model4 = smf.ols(
    "normexam ~ standlrt + girl + C(schgend, Treatment('mixedsch'))",
    data=regression,
).fit()
model4.params
