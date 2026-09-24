# MATH9102 — Fundamentals of Data Analysis

Welcome. This folder contains everything you need for the module: the lecture
slides, a worked notebook for each week, an exercise, the datasets, and a small
Python package that supplies the datasets and the reporting helpers.

**Read this page once, set up your environment, and then work week by week.**

---

## 1. Setting up

> ### Do this before the first lab, not during it
>
> Setting up takes **20–30 minutes and about 3 GB of disk**, most of it
> downloading. Thirty people doing that simultaneously on lecture-room wifi does
> not work, and it costs everyone the session.
>
> Do it at home, on a connection you trust, and then run the checker described
> below. If it fails, bring **the output** to the lab and we will fix it in two
> minutes instead of twenty.

**The lab machines already have conda installed.** If you are working in a lab,
skip to step 2 of Path A — there is nothing to install. The paths below are for
your own laptop.

You need **Python 3.11 or newer** and a way to run notebooks. There are three
ways to get there, and they are not equal.

> ### Take Path A unless you have a specific reason not to
>
> **Path A (Miniforge) is highly recommended.** It is the route these
> materials are written for: every instruction assumes it, the troubleshooting
> section covers it, and it is what everyone else in the room will be running.
> It installs its own Python, so nothing already on your machine can break it —
> which matters, because the Python that came with your Mac is almost certainly
> too old (macOS ships 3.9 or older and Apple does not update it).
>
> **Paths B and C exist for two specific situations**, and you should be able to
> say which one applies to you before choosing either:
>
> | | Take it only if |
> |---|---|
> | **B — Colab** | you are not allowed to install software on the machine you have, or your laptop is too old to run this at all |
> | **C — venv** | you already have a working Python 3.11+ that you rely on for other work and would rather not add conda beside it |
>
> "Path A looked like a lot of steps" is not one of those reasons. It is four
> commands and it is the one we can help you with quickly.

---

### Path A — Miniforge (highly recommended; works on old Macs and Windows)

Miniforge installs its own Python and every package the module needs, so it does
not matter what is already on your machine.

**Already have Anaconda or Miniconda from another module?** You do not need
Miniforge as well. Skip to step 2 and use your existing installation — the
`environment.yml` asks for the conda-forge channel explicitly, so it will build
the right environment either way.

**1. Install Miniforge** from
<https://conda-forge.org/download/>. Take the installer for your
machine:

| Your machine | Installer |
|---|---|
| Mac, Apple Silicon (M1/M2/M3/M4) | macOS arm64 |
| Mac, Intel | macOS x86_64 |
| Windows | Windows x86_64 |

Accept the defaults, **with one exception you must not accept**.

On a **Mac or Linux**, near the end the installer asks:

```
Do you wish to update your shell profile to automatically initialize conda?
...
Proceed with initialization? [yes|no]
[no] >>>
```

**Type `yes` and press Enter.** The default is `no`, and taking it leaves the
`conda` command unavailable in your terminal — step 3 below will then fail with
`conda: command not found`. This is the one prompt where the default is the
wrong answer for this module.

On **Windows** you are not asked. The installer gives you a **Miniforge
Prompt** in the Start menu — use that, not the ordinary Command Prompt.

**2. Open a *new* terminal** (Terminal on a Mac, Miniforge Prompt on Windows).
It has to be a new one: the initialisation you just agreed to only takes effect
in terminals opened afterwards, so if you ran the installer in a terminal
window, close it. Check you are set up with `conda --version`, then change into **this folder** — the one containing this file. If you
downloaded the ZIP from the green **Code** button, unzipping it gave you a
folder called `math9102-main`:

```bash
cd path/to/math9102-main
```

*Tip: on a Mac you can type `cd ` and then drag the folder onto the terminal
window. On Windows, right-click the folder in Explorer and choose "Copy as
path".*

**3. Create the environment.** One command, and it installs everything:

```bash
conda env create -f environment.yml
```

This takes 10–20 minutes the first time and downloads roughly 1 GB. Leave it
running; it is not stuck.

**4. Make a folder for your own work.** In the same terminal, still in this
folder:

```bash
mkdir my-work
```

Everything you write goes in there. It is the one folder that is **not** part of
the download, which is what keeps your work safe when a new week is released —
see section 4.

**5. Every time you work on the module:**

```bash
conda activate math9102
jupyter lab
```

---

### Path B — Google Colab (fallback: nothing to install)

Use this if your laptop is very old, or is managed by an employer and will not
let you install software. **It is a fallback, not an equivalent choice** — see
the box at the top of this section. If Path A has simply defeated you, use this
to keep up with the week's work and bring the problem to the lab, rather than
settling here for the term.

Nothing to download. Open the week's notebook directly:

<https://colab.research.google.com/github/notulae/math9102/blob/main/week-01-fundamentals/notebook.ipynb>

Then run this in a new cell at the very top, once per session, to fetch the
datasets and the course package:

```python
!git clone -q https://github.com/notulae/math9102.git math9102-course
%cd math9102-course/week-01-fundamentals
!pip install -q ..
```

Change the week folder to whichever one you are working on. The `%cd` matters:
the package finds the datasets by looking upwards from wherever you are working.

**The catch.** Colab resets every time, so you repeat that cell each session,
and anything you write is lost unless you save a copy to your own Drive
(File -> Save a copy in Drive). It is a good fallback, not a good permanent
home.

---

### Path C — venv (only if you already have Python 3.11+ and want to keep it)

Check first:

```bash
python3 --version          # Mac / Linux
py --version               # Windows
```

If that says 3.11 or higher, you can use Python's built-in tool. If it says 3.9,
3.10, or "command not found", **use Path A instead** — do not try to upgrade
your system Python, it is more trouble than it is worth.

```bash
# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .

# Windows
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install .
```

Then `jupyter lab`. Next time, re-activate first (`source .venv/bin/activate`,
or `.venv\Scripts\activate` on Windows).

---

### Check it worked

Whichever path you took, run this from inside the `MATH9102` folder, with your
environment active:

```bash
python check-setup.py
```

It checks your Python version, every package the module needs, that the course
package imports, and that it can actually load a dataset. It tells you what to do
about anything that fails. **A green `READY.` at the end means you are done.**

If something fails, work through the failures in order — the first one usually
explains the rest — and see [Troubleshooting](#7-troubleshooting). If you are
still stuck, **copy the whole output** and bring it to the lab.

**One rule that matters for all three paths: open the notebooks from inside the
`MATH9102` folder.** The package finds the datasets by looking upwards from
where you are working, so a notebook copied out to your desktop will not find
them.

## 2. What is in each week folder

| | Topic | Folder | |
|---|---|---|---|
| **Week 1** | Fundamentals | `week-01-fundamentals/` | 58 slides |
| **Week 2** | Describing Data | `week-02-describing-data/` | 57 slides |
| **Week 3** | Hypotheses and Correlation | `week-03-hypotheses-and-correlation/` | 50 slides |

More weeks are added as the module runs.


Each `week-NN-*/` folder contains:

| File | What it is | What to do with it |
|---|---|---|
| `slides.pdf` | The lecture deck | Read before class, annotate during |
| `notebook.ipynb` | The lecture companion — every idea from the slides, worked in code | **Run it yourself**, cell by cell. Change things and see what happens |
| `notebook.html` | The same notebook, already run | Read on a phone or tablet, or check what your output *should* have looked like |
| `exercise.ipynb` | The week's exercise | Complete it. This is the practice that the assessment is built on |
| `README.md` | The week's learning outcomes | Check yourself against it before moving on |
| `snippets/` | The code shown on the slides, as real `.py` files | Copy from here rather than retyping from the PDF |

**Worked solutions are released after the class the week belongs to**, and
appear in a top-level `solutions/` folder in the download from then on. If you
do not see that folder, the solutions for the weeks you have are not out yet.
They are written to be read *after* an attempt — they explain the reasoning, not
just the answer, and several spend more time on why a choice was wrong than on
the arithmetic. **Try the exercise first.**

### The slides also carry their own code

Every code listing in a slide deck is **attached to the PDF**. In most PDF
readers you can open the attachments panel and save the exact `.py` file. That
is there so a copy-and-paste from a slide never fails on a stray character.

---

## 3. How to work a week

1. **Read the slides.** Skim before the lecture, properly after.
2. **Run the notebook.** Do not just read it. Execute each cell, and when a cell
   produces a number or a plot, ask yourself what it is telling you before you
   move on.
3. **Break something.** Change a variable, a bin width, a group. Nothing in a
   week folder is precious — a fresh download replaces it.
4. **Do the exercise — in your own copy.** Open `exercise.ipynb`, then
   **File → Save Notebook As…** and save it into `my-work/` before you type
   anything. Write your answers in the empty cells. Where a question asks for
   sentences, write sentences.

   > **Why the copy matters.** Week folders get replaced when you download a
   > newer release — including corrections to a week you have already done.
   > Anything you wrote *inside* one would go with it. Nothing in `my-work/` is
   > ever touched, because it is not part of the download.
5. **Then read the solution**, and compare your reasoning against it — not just
   your numbers.

Expect the exercise to take longer than the notebook. That is the right way
round: the notebook shows you the moves, the exercise is where you learn them.

---

## 4. When a new week is released

Weeks are added to the same download as the module runs. Updating is three
steps, and it is the same three whether one week was added or four.

1. Download the ZIP again — green **Code** button, **Download ZIP**.
2. Unzip it, open the new `math9102-main` folder, and drag **everything inside
   it** into your existing course folder.
3. Say **Replace** (or **Merge**) to anything it asks about.

That is safe because of one rule:

> ### Everything in the download is disposable. Everything you write is in `my-work/`.

`my-work/` is not in the ZIP, so nothing you have written is ever replaced. And
because your work is never inside a week folder, the week folders can be
overwritten freely — which means you do not have to work out which ones are new,
and you automatically pick up corrections to weeks you have already done.

**Do not delete your course folder and start again.** `my-work/` is in it.

**You do not need to touch conda.** The datasets and the `math9102` package are
the same in every release, so the environment you built in section 1 keeps
working. If that ever changes it will be announced — it is not something to
check for.

---

## 5. Three rules this module works by

These are not style preferences. They are how the work is judged.

### Every statistic you report is generated by code

You will never type a number into a sentence. The module's helpers produce the
sentence for you, from the data and the live result:

```python
m9.report_ttest(survey, "tpstress", "child", result)
```

**Why.** A typed number goes stale silently. When the data change, or the
analysis is re-run, the prose does not follow — and nobody proofreads a number
they wrote three weeks ago. You will see a worked example of exactly this
failure in week 4.

### Datasets are loaded by name, never by path

```python
survey = m9.load_survey()          # yes
survey = pd.read_csv("C:/Users/me/data/survey.dat")   # no
```

A file path is a fact about one computer. A dataset name is a fact about the
analysis, and it works on your machine, on mine, and on the marker's.

To see everything available: `m9.available()`, and `m9.manifest()` for where
each dataset came from.

### The work is in the justification, not the test

Running a test is one line of code. Choosing the right one with stated evidence,
checking what it assumes, reporting it properly and drawing a defensible
conclusion — that is the work.

---

## 6. The module package

`math9102` is deliberately thin. It gives you:

| What | Examples |
|---|---|
| The datasets | `m9.load_survey()`, `m9.load_msleep()`, `m9.available()` |
| Descriptives | `m9.describe()`, `m9.describe_by()`, `m9.frequency()`, `m9.crosstab()`, `m9.missingness()` |
| Plots in a consistent style | `m9.histogram_with_normal()`, `m9.qq_plot()`, `m9.grouped_box()`, `m9.scatter_with_fit()`, `m9.normality_panel()` |
| Effect sizes | `m9.cohens_d()`, `m9.cramers_v()`, `m9.rank_biserial()`, `m9.interpret()` |
| Generated report sentences | `m9.report_ttest()`, `m9.report_correlation()`, `m9.report_normality()`, `m9.report_chisquare()` |

Everything statistical is done with **scipy**, **statsmodels** and **pingouin**
directly. That is on purpose: those are the tools you will still be using after
this module ends, and the package deliberately hides no decision that you should
be making.

Any function's documentation is one line away:

```python
help(m9.load_survey)
m9.describe_by?                    # in Jupyter
```

---

## 7. Assessment

The module is **100% continuous assessment. There is no examination.**

| Part | Weight | Due | What it asks for |
|---|---|---|---|
| Phase 1 | 40% | Week 8 | Evaluate a dataset's suitability for multivariate analysis; explore and summarise it; justify your methodological choices |
| Phase 2 | 60% | Week 14 | Design and implement a data science workflow; apply multivariate techniques; evaluate the workflow critically |

Read the verbs in that table: *evaluate*, *justify*, *critically assess*,
*communicate*. None of them is *compute*.

The full specifications and rubrics are published separately. Everything in
these weekly exercises is practice for them.

---

## 8. Troubleshooting

**`conda: command not found`** (Mac or Linux)
The installer asked whether to initialise your shell and the answer was `no` —
its default. Fix it without reinstalling:

```bash
~/miniforge3/bin/conda init "$(basename "$SHELL")"
```

Then **close the terminal and open a new one**, and `conda --version` will
work. If Miniforge is somewhere else, use that path instead of `~/miniforge3`.

**`ModuleNotFoundError: No module named 'math9102'`**
Your virtual environment is not active, or `pip install -e .` was not run from
this folder. Activate it and re-run the install.

**`FileNotFoundError: Could not locate data/processed/`**
The notebook is being run from outside the `MATH9102` folder — most often
because it was copied to the desktop or to a Downloads folder on its own. Move
it back beside the other weeks. If you genuinely need it elsewhere, say where
the data is:

```python
import os
os.environ["MATH9102_DATA"] = "/full/path/to/MATH9102/data/processed"
import math9102 as m9
```

**Jupyter cannot see the environment, or the kernel is the wrong Python**
Register it as a kernel, then pick it from Jupyter's kernel menu:

```bash
conda activate math9102          # or activate your venv
python -m ipykernel install --user --name math9102 --display-name "MATH9102"
```

**`ERROR: Could not find a version that satisfies the requirement ...`**
Your Python is too old for one of the packages. This is the commonest failure on
an older Mac. **Use Path A (Miniforge)** — it installs its own Python and the
problem disappears.

**Windows: `python` opens the Microsoft Store, or `pip` is not recognised**
Use the **Miniforge Prompt** from the Start menu rather than Command Prompt or
PowerShell. If you are on Path C, use `py` instead of `python`.

**Windows: the install fails inside OneDrive**
OneDrive syncing can lock files mid-install. Put the `MATH9102` folder somewhere
outside OneDrive — `C:\Users\you\MATH9102` is fine.

**A plot does not appear**
Make sure the cell ends with the plotting call, and that you have run
`m9.use_house_style()` near the top of the notebook.

**Something else**
Run `python check-setup.py` and bring **its full output** to the lab session,
along with the exact error message you saw. A description of an error is much
harder to help with than the error.

---

## 9. A note on how these materials were built

Every figure in every deck is generated from the data by code that ships with
the module — none is a screenshot. Every code listing on a slide is a real,
runnable file. Every number in every worked narrative is produced by code at the
moment the notebook runs.

This is not fussiness. It means that if you find a number in these materials
that looks wrong, it is wrong *in the analysis*, and it is worth telling us
about. Please do.
