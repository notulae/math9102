# Unit 6 — Linear Regression

## Learning outcomes

By the end of this unit you should be able to:

1. Explain what a regression model's intercept, coefficients and residuals are,
   and fit simple and multiple linear regressions with the statsmodels formula
   API on data loaded by name.
2. Partition the variation in an outcome into sums of squares, and interpret
   *F*, *R²* and adjusted *R²*, including why *R²* never falls as predictors
   are added.
3. Interpret each coefficient in words, with its confidence interval; predict
   from the fitted equation; and use standardised coefficients where they
   help, never for a binary predictor.
4. Enter a categorical predictor as dummy variables with a named reference
   category, and check by cross-tabulation that the combinations a model
   adjusts over exist.
5. Fit an interaction, and report a non-significant one together with what it
   does not establish.
6. Compare nested models fitted on the same rows.
7. Explain, with the ICC and cluster-robust standard errors, what clustered
   data do to precision and what they leave alone, and state what a
   regression coefficient cannot establish about cause.

Maps to:
- MLO1: critically evaluate fundamental concepts, such as association against
  cause and what *R²* is not;
- MLO4: select and apply appropriate methods;
- MLO5: interpret outcomes, including what they do not establish;
- MLO6: design, implement and critically assess predictive models (syllabus
  heading 7);
- MLO8: communication;
- MLO9: programming tools.

## What is in this folder

| File | What to do with it |
|---|---|
| `slides.pdf` | Read before class, annotate during. The code listings in it are attached to the PDF — open the attachments panel to save them |
| `notebook.ipynb` | Run it yourself, cell by cell |
| `notebook.html` | The same notebook already run, for reading away from a laptop |
| `exercise.ipynb` | **Save it into `my-work/` first** (File -> Save Notebook As), then complete it there |
| `snippets/` | The code shown on the slides, as real `.py` files |

**Work in `my-work/`, not in this folder.** This folder is replaced whenever you
download a newer release — that is how later units and corrections arrive — so
anything you write here would go with it. See `START-HERE.md` section 4.

The worked solution appears in `solutions/unit-06-linear-regression/` once it is released,
after the class this unit belongs to. **Try the exercise first.**

See `START-HERE.md` at the top level if you have not set up your environment yet.
