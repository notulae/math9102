#!/usr/bin/env python3
"""Check that this machine is ready for MATH9102.

Run this BEFORE the first lab:

    python check-setup.py

It uses nothing but the Python standard library, and it is written to run on
very old Python versions on purpose - if your Python is too old for the module,
this script still has to be able to start up and tell you so.

Every failure it reports comes with what to do about it.
"""

import importlib
import os
import shutil
import sys

MIN_PYTHON = (3, 11)

# (import name, human name, why the module needs it)
PACKAGES = [
    ("numpy", "NumPy", "arrays and numerical work"),
    ("pandas", "pandas", "dataframes - every week uses this"),
    ("scipy", "SciPy", "the statistical tests"),
    ("matplotlib", "Matplotlib", "figures"),
    ("seaborn", "seaborn", "figure styling"),
    ("statsmodels", "statsmodels", "regression, from week 8"),
    ("pingouin", "Pingouin", "effect sizes and post-hoc tests"),
    ("sklearn", "scikit-learn", "dimension reduction, from week 10"),
    ("factor_analyzer", "factor_analyzer", "factor analysis, week 10"),
    ("pyreadstat", "pyreadstat", "reading SPSS files"),
]

PASS = "  ok   "
FAIL = "  FAIL "
WARN = "  note "


def report(status, message, advice=None):
    print(status + message)
    if advice:
        for line in advice.strip().splitlines():
            print("         " + line.strip())


def check_python():
    version = sys.version_info
    shown = "%d.%d.%d" % version[:3]
    if version[:2] >= MIN_PYTHON:
        report(PASS, "Python %s" % shown)
        return True
    report(
        FAIL,
        "Python %s is too old (the module needs %d.%d or newer)" % (
            shown, MIN_PYTHON[0], MIN_PYTHON[1]),
        """
        This is the commonest problem, and it is usually the Python that came
        with your Mac. Do not try to upgrade it.
        Follow Path A in START-HERE.md: install Miniforge, which brings its own
        Python, then run:   conda env create -f environment.yml
        """,
    )
    return False


def check_packages():
    missing = []
    for module, name, why in PACKAGES:
        try:
            found = importlib.import_module(module)
        except Exception:
            missing.append((name, why))
            continue
        version = getattr(found, "__version__", None) or "installed"
        report(PASS, "%-16s %s" % (name, version))
    if missing:
        print("")
        for name, why in missing:
            report(FAIL, "%-16s missing - needed for %s" % (name, why))
        report(
            WARN,
            "one or more packages are missing",
            """
            Your environment is not active, or was never created.
            Miniforge:  conda activate math9102
            venv:       source .venv/bin/activate    (Windows: .venv\\Scripts\\activate)
            If you have not created it yet, see START-HERE.md section 1.
            """,
        )
    return not missing


def check_jupyter():
    """Check for the command, not the package.

    `import jupyterlab` succeeding does not mean `jupyter lab` will start, and
    starting it is the only thing a student actually needs it for.
    """
    if shutil.which("jupyter") or shutil.which("jupyter.exe"):
        report(PASS, "the `jupyter` command is available")
        return True
    report(
        FAIL,
        "the `jupyter` command was not found",
        """
        You will not be able to open the notebooks. Install it into the
        environment you are using:   pip install jupyterlab
        If you meant to use a different environment, activate that one first.
        """,
    )
    return False


def check_package_and_data():
    try:
        import math9102
    except Exception as exc:
        report(
            FAIL,
            "the math9102 package will not import (%s)" % exc.__class__.__name__,
            """
            The course package is not installed into the environment you are
            using. From inside the MATH9102 folder, run:   pip install .
            """,
        )
        return False

    report(PASS, "math9102 package imports")

    try:
        where = math9102.data_dir()
    except Exception as exc:
        report(
            FAIL,
            "the datasets cannot be found",
            """
            %s
            You are probably running this from outside the MATH9102 folder.
            Change into it first, then run this script again.
            """ % exc,
        )
        return False

    report(PASS, "datasets found in %s" % where)

    try:
        survey = math9102.load_survey()
        rows, cols = survey.shape
    except Exception as exc:
        report(FAIL, "a dataset would not load: %s" % exc)
        return False

    report(PASS, "loaded the survey dataset (%d rows, %d columns)" % (rows, cols))
    report(PASS, "%d datasets available" % len(math9102.available()))
    return True


def check_where_you_are():
    """Warn early about the mistake that produces the most confusing error."""
    here = os.path.abspath(os.getcwd())
    if os.path.isdir(os.path.join(here, "data", "processed")):
        return True
    parent_has = any(
        os.path.isdir(os.path.join(p, "data", "processed"))
        for p in (os.path.abspath(os.path.join(here, *([".."] * n)))
                  for n in range(1, 4))
    )
    if parent_has:
        return True
    report(
        WARN,
        "this does not look like the MATH9102 folder",
        """
        Change into the folder containing START-HERE.md and run this again.
        Notebooks must also be opened from inside that folder - that is how the
        package finds the datasets.
        """,
    )
    return False


def check_work_folder(in_course_folder):
    """Make sure my-work/ exists, because it is what keeps a student's work.

    Everything in the download is replaced when a newer release is unzipped over
    it - that is how later weeks and corrections arrive. `my-work/` is the one
    folder that is not part of the download, so it is the only safe place to
    write. Creating it here means it exists before there is anything to lose,
    rather than depending on the student having read section 4 first.

    Only ever created in the course folder itself: called with False, this does
    nothing, so running the checker from the wrong directory cannot scatter
    empty my-work folders around the filesystem.
    """
    if not in_course_folder:
        return
    path = os.path.join(os.path.abspath(os.getcwd()), "my-work")
    if os.path.isdir(path):
        report(PASS, "my-work/ is there - save your own work into it")
        return
    try:
        os.makedirs(path)
    except OSError as exc:
        report(
            WARN,
            "could not create my-work/ (" + exc.strerror + ")",
            """
            Make a folder called my-work here by hand, and save your own
            notebooks into it. It is the one folder a new download never
            replaces.
            """,
        )
        return
    report(
        PASS,
        "created my-work/ - save your own work into it",
        """
        When a new week is released you unzip the download over this folder,
        which replaces the week folders. my-work/ is not in the download, so
        nothing you save there is ever overwritten.
        """,
    )


def main():
    print("")
    print("MATH9102 - environment check")
    print("=" * 58)
    print("")

    ok = check_python()
    if not ok:
        # Nothing below can succeed, and the messages would only be noise.
        print("")
        print("=" * 58)
        print("NOT READY. Fix your Python version first - see above.")
        print("")
        return 1

    in_course_folder = check_where_you_are()
    check_work_folder(in_course_folder)
    print("")
    packages_ok = check_packages()
    print("")
    jupyter_ok = check_jupyter()
    data_ok = check_package_and_data()

    print("")
    print("=" * 58)
    if packages_ok and jupyter_ok and data_ok:
        print("READY. Open week-01-fundamentals/notebook.ipynb and start.")
        print("")
        return 0

    print("NOT READY. Work through the failures above, in order - the first")
    print("one usually explains the rest. If you are still stuck, bring this")
    print("output to the lab session.")
    print("")
    return 1


if __name__ == "__main__":
    sys.exit(main())
