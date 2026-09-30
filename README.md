# MATH9102 — Fundamentals of Data Analysis

Lecture slides, a worked notebook for each week, an exercise, the datasets, and
a small Python package that supplies them.

**Follow the four steps below, in order.**

> **Do this at home before the first lab if possible.**

---

## Step 1 — Download the materials

At the top of this page: green **Code** button → **Download ZIP**.

No GitHub account needed. Unzip it somewhere you will find again — your
Documents folder is fine, your Downloads folder is not. You will get a folder
called `math9102-main`; everything else happens inside it.

## Step 2 — Install Python with Miniforge

**This is highly recommended, and it is the only route these materials are
written for.** Miniforge installs its own Python, so it works on an old Mac or a
locked-down Windows machine no matter what is already there — and the Python
that came with your Mac is almost certainly too old (macOS ships 3.9 or older
and Apple does not update it).

1. Install Miniforge from <https://conda-forge.org/download/> — take the
   installer for your machine and accept the defaults, **except** the question
   *"Do you wish to update your shell profile to automatically initialize
   conda?"* on Mac and Linux. Answer **yes** there; its default is `no`, and
   taking it leaves `conda` unavailable in your terminal. Windows does not ask.
2. Open a **new** terminal (**Terminal** on a Mac, **Miniforge Prompt** on
   Windows) — the initialisation only affects terminals opened after it. Check
   it took with `conda --version`, then `cd` into the `math9102-main` folder you
   unzipped.
3. Run `conda env create -f environment.yml`, then `conda activate math9102`.

**[START-HERE.md](START-HERE.md) Path A has this with every command spelled
out.** Follow it there if any of the above is unfamiliar.

> **If you already have Anaconda or Miniconda**, you do not need
> Miniforge as well — skip item 1 and start at item 2 above. **On a lab
> machine?** Conda is already installed; same thing, start at item 2.
>
> There are two other ways to set up, in START-HERE.md as Paths B and C.
> **Use them only if you have a specific reason/preference** — a machine you are
> not allowed to install software on, or a working Python 3.11+ you already rely
> on. Otherwise Path A is the one to take: it is what the instructions assume,
> what the troubleshooting covers, and what most people will be running.

## Step 3 — Check it worked

In the same terminal, in the same folder, with the environment active:

```bash
conda activate math9102
python check-setup.py
```

It checks your Python version, every package, the course package and a real
dataset load, and tells you what to do about anything it finds. **Do not move on
until this passes.**

## Step 4 — Read the guide, then start week 1

**→ [START-HERE.md](START-HERE.md)** — read it once. It covers how to work a
week, the three rules the module runs on, and troubleshooting.

Then open `week-01-fundamentals/` and start with `slides.pdf` and `notebook.ipynb`.

---

## What is here

| | Topic | Folder | |
|---|---|---|---|
| **Week 1** | Fundamentals | `week-01-fundamentals/` | 58 slides |
| **Week 2** | Describing Data | `week-02-describing-data/` | 57 slides |
| **Week 3** | Hypotheses and Correlation | `week-03-hypotheses-and-correlation/` | 50 slides |

More weeks are added as the module runs.

Each week folder holds `slides.pdf`, `notebook.ipynb` (run it yourself),
`notebook.html` (the same thing already run, for reading), `exercise.ipynb`, and
the code shown on the slides as real `.py` files.

Worked solutions are released after the class they belong to.

**Coming back for a new week?** Download the ZIP again and drag everything in it
into your existing course folder, saying **Replace** to anything it asks. Your
own work lives in `my-work/`, which is not part of the download and so is never
replaced. START-HERE.md section 4 has the detail.

## If you genuinely cannot install anything

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/notulae/math9102/blob/main/week-01-fundamentals/notebook.ipynb)

Colab runs in a browser and needs nothing installed, so it will get you through
a lab. It is a **fallback, not the normal route**: it resets every session, and
anything you write is lost unless you save a copy to your own Drive. Use it if
your laptop is very old, or is managed by an employer who will not let you
install software. Details in START-HERE.md, Path B.
