# Unit 7 — Regression Assumptions and Diagnostics

## Learning outcomes

By the end of this unit you should be able to:

1. Compute and report a partial correlation beside the zero-order one, and say
   how it differs from a semi-partial correlation.
2. Select a model's variables before dropping missing rows, and show what the
   choice costs.
3. Say what each regression assumption is about — the mean, the residuals, the
   design, individual cases, the predictors — and check each with the
   appropriate plot or statistic, plots first.
4. Distinguish outliers, leverage points and influential cases; compute
   standardised residuals, the Bonferroni outlier test, Cook's distance and
   standardised DFBETAS; and decide what to do with a flagged case by running
   the model twice.
5. Check constant variance with a residual plot and a named Breusch–Pagan
   test, and apply robust standard errors or a transformation, interpreting a
   transformed outcome.
6. Assess collinearity with VIF and tolerance, including the generalised VIF
   for a categorical predictor, and say what collinearity does and does not do.
7. Judge independence from the design, and write a diagnostic paragraph that
   reports what each check found and claims nothing more.

Maps to:
- MLO1: critically evaluate fundamental concepts — what an assumption is about,
  and what a non-significant test does not establish;
- MLO4: select and apply appropriate methods;
- MLO5: interpret outcomes, including what they do not establish;
- MLO6: design, implement and critically assess predictive models;
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

The worked solution appears in `solutions/unit-07-regression-assumptions-and-diagnostics/` once it is released,
after the class this unit belongs to. **Try the exercise first.**

See `START-HERE.md` at the top level if you have not set up your environment yet.
