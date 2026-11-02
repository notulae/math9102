# Workbook 1 — Auditing an Analysis

A session you work through yourself, in class. Everything you need is in this
folder.

## Which version is yours

There are three versions of the same analysis, each with different defects:
`variant-B`, `variant-F` and `variant-J`. Take yours from the **last digit of
your student number**:

| Last digit | Variant |
|---|---|
| 0, 1, 2 or 3 | `variant-B` |
| 4, 5 or 6 | `variant-F` |
| 7, 8 or 9 | `variant-J` |

Finished with time to spare? Take the next one round: B, then F, then J, then B.

## What is in this folder

| File | What to do with it |
|---|---|
| `BRIEF.md` | The task. Read it first |
| `variant-B/analysis.ipynb`, `variant-F/…`, `variant-J/…` | The analysis to audit, already run. **Save yours into `my-work/` first** (File -> Save Notebook As), then work on it there |

## How to work

1. Read `BRIEF.md`.
2. Open your variant's `analysis.ipynb`, and save it into `my-work/` before you
   run or change anything. It runs from there exactly as it does here.
3. Write your findings in `my-work/` too, in a notebook or a document.

**Work in `my-work/`, not in this folder.** This folder is replaced whenever you
download a newer release, so anything you write here would go with it. See
`START-HERE.md` section 4.

## Checking yourself

Every defect is a place where the analysis is wrong about itself: a sentence that
disagrees with the output above it, code that does something it should not, or a
picture read wrongly. So you can confirm a finding before anyone tells you: find
the output it contradicts, re-run the cell, or compute the number yourself. If
you cannot show it from the notebook or the data, it is not yet a finding.

## When you are stuck

- Read the prose against the output, one cell at a time.
- Look back at Units 1 to 4. Everything in this analysis was taught there.
- Ask the person next to you what they make of the same cell.

## When you have finished

What was wrong in each variant appears in
`solutions/workbook-1-auditing-an-analysis/` after the session, as a unit's
solution does. Check your findings against it then. It also lists what a careful
audit notices beyond the three, and what is often flagged that is not wrong.
