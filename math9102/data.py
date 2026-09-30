"""Dataset loaders.

Every dataset exists exactly once, in data/processed/, built by
tools/build_data.py. Notebooks call a loader rather than a path, so no notebook
ever hardcodes a location. The legacy module hardcoded an absolute Windows path
belonging to a different machine in 50 of its 53 practical files, which is why
none of it ran anywhere else.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import pandas as pd

__all__ = [
    "data_dir",
    "available",
    "load",
    "load_survey",
    "load_sleep",
    "load_youthcohort",
    "load_regression",
    "load_raq",
    "load_bullying",
    "load_experim",
    "load_wine",
    "load_bdi",
    "load_websatisfaction",
    "load_salaries",
    "load_msleep",
    "load_festival",
    "load_romcom",
    "load_facebook_narcissism",
    "manifest",
]


def data_dir() -> Path:
    """Locate data/processed/, whatever way the package was installed.

    Three strategies, in order, because students install this three different
    ways and each one breaks a different assumption:

    1. `MATH9102_DATA`, if set. Always wins, and is the documented escape hatch.
    2. Upwards from the package file. Works in the repository and after an
       editable install, where the package still sits beside the data.
    3. Upwards from the working directory. Works after an ordinary `pip
       install`, in a conda environment, and on Colab - anywhere the package
       lives in site-packages but the notebook is being run from inside the
       course folder.

    Strategy 3 is what makes the student distribution independent of the install
    method. Without it, an ordinary non-editable install silently loses the
    datasets, and the error surfaces in week 1 as a FileNotFoundError with no
    obvious cause.
    """
    override = os.environ.get("MATH9102_DATA")
    if override:
        resolved = Path(override).expanduser().resolve()
        if not resolved.is_dir():
            raise FileNotFoundError(
                f"MATH9102_DATA points at {resolved}, which is not a directory."
            )
        return resolved

    for start in (Path(__file__).resolve(), Path.cwd().resolve()):
        for parent in (start, *start.parents):
            candidate = parent / "data" / "processed"
            if candidate.is_dir():
                return candidate

    raise FileNotFoundError(
        "Could not locate data/processed/.\n"
        "  If you are a student: open the notebook from inside the MATH9102\n"
        "  folder, or set MATH9102_DATA to the full path of data/processed.\n"
        "  If you are building the course: run 'make data'."
    )


def available() -> list[str]:
    """Names accepted by load()."""
    return sorted(p.stem for p in data_dir().glob("*.csv"))


@lru_cache(maxsize=None)
def _read(name: str) -> pd.DataFrame:
    path = data_dir() / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"No dataset named {name!r}. Available: {', '.join(available())}"
        )
    return pd.read_csv(path)


def load(name: str) -> pd.DataFrame:
    """Load a dataset by name. Returns a copy, so edits cannot leak between cells."""
    return _read(name).copy()


def manifest() -> pd.DataFrame:
    """Provenance for every dataset: source path, checksum, shape, notes."""
    return pd.read_csv(data_dir().parent / "MANIFEST.csv")


# Named loaders. These are the documented entry points used in the notebooks;
# the docstrings carry the study context students need for interpretation.


def load_survey() -> pd.DataFrame:
    """Pallant wellbeing survey (439 x 134).

    Responses from 439 members of the general public in Melbourne, Australia,
    measuring self-esteem, optimism, perceived control, perceived stress,
    positive and negative affect, life satisfaction and social desirability.
    Scale totals are prefixed 't' (tpstress, tpcoiss, toptim, tslfest, tmarlow).
    """
    return load("survey")


def load_sleep() -> pd.DataFrame:
    """Pallant sleep study (271 x 55).

    University staff in Melbourne reporting sleep behaviour, sleep problems and
    their impact. 'totsas' is the total sleepiness and associated sensation scale.
    """
    return load("sleep")


def load_youthcohort() -> pd.DataFrame:
    """UK Youth Cohort Study (13201 x 27), via Connolly.

    Demographic, educational and attitudinal measures for young people in the UK,
    including GCSE subject entry and grades, parental education and school type.
    """
    return load("youthcohort")


def load_regression() -> pd.DataFrame:
    """Goldstein et al. exam results (4059 x 15).

    Warning: these data are clustered - 4059 students within 65 schools, with an
    intraclass correlation of about 0.15 for normexam. Ordinary least squares
    treats the observations as independent and understates the standard errors by
    roughly a factor of two. See docs/DECISIONS.md ADR-007.
    """
    return load("regression")


def load_raq() -> pd.DataFrame:
    """Field R-anxiety questionnaire (2571 x 23), 23 Likert items."""
    return load("raq")


def load_bullying() -> pd.DataFrame:
    """School bullying survey (819 x 11)."""
    return load("bullying")


def load_experim(expanded: bool = False) -> pd.DataFrame:
    """Experimental study (30 x 18), or the expanded 300-row version used in week 6."""
    return load("experim_clean" if expanded else "experim")


def load_wine() -> pd.DataFrame:
    """UCI wine recognition data (178 x 14)."""
    return load("wine")


def load_bdi() -> pd.DataFrame:
    """Field BDI drink study (20 x 4). Constructed to be non-normal."""
    return load("bdi")


def load_festival(with_outlier: bool = True) -> pd.DataFrame:
    """Download Festival hygiene scores (810 x 5).

    Hygiene rated on each of three festival days for 810 attendees, split by
    whether they live in a city or a rural area.

    Two features make it week 2's working dataset. Day 1 contains a genuine
    data-entry outlier - a score far outside the scale - so the effect of one
    bad value on a mean, a density plot and a boxplot can be shown rather than
    asserted. And days 2 and 3 are heavily incomplete, because people went home;
    that missingness is real attrition, not a defect.

    `with_outlier=False` returns the corrected version, for the comparison.
    """
    return load("festival" if with_outlier else "festival_no_outlier")


def load_romcom(by: str = "location") -> pd.DataFrame:
    """Film interest by group (40 x 3).

    Forty students, half of whom watched a romantic comedy and half a thriller,
    rating their interest. `by="location"` splits city against rural;
    `by="gender"` is the same design with the other grouping variable.
    """
    if by not in {"location", "gender"}:
        raise ValueError("by must be 'location' or 'gender'")
    return load("romcom_urbanrural" if by == "location" else "romcom")


def load_facebook_narcissism() -> pd.DataFrame:
    """Facebook profile picture ratings (776 x 4).

    Each profile picture is rated on four dimensions (cool, fashionable,
    attractive, glamorous) and paired with the poster's narcissism score. Note
    that there are four rows per person, one per rating type - so the rows are
    not independent, which matters later.
    """
    return load("facebook_narcissism")


def load_salaries() -> pd.DataFrame:
    """US academic salaries, 2008-09 (397 x 6).

    Nine-month salaries for assistant professors, associate professors and
    professors at one US college, with rank, discipline (A theoretical, B
    applied), years since PhD, years of service and sex. From carData::Salaries
    (Fox & Weisberg); R's dotted names are underscored here, so the columns are
    yrs_since_phd and yrs_service.

    Week 1's worked example. Salary is right-skewed, which is what makes the
    mean-versus-median lesson land on real data rather than on an invented one.
    """
    return load("salaries")


def load_msleep() -> pd.DataFrame:
    """Mammal sleep times (83 x 11).

    Total sleep, REM sleep, sleep cycle length, brain weight and body weight for
    83 mammals, with diet (vore) and conservation status. From ggplot2::msleep,
    after Savage & West (2007).

    Week 1's lab. Chosen partly because it is genuinely incomplete: vore,
    conservation, sleep_rem, sleep_cycle and brainwt all have missing values, so
    students meet missingness in the first week rather than being protected from
    it.
    """
    return load("msleep")


def load_websatisfaction() -> pd.DataFrame:
    """Web design satisfaction survey (73 x 31), used by CA Phase 2 Task 4."""
    return load("websatisfaction")
