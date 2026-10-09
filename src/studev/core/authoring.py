"""Creating and adding user problems (studev new / studev add).

No printing here - functions return data or raise StudevError,
so both the CLI and a future TUI can use them.
"""
import json
import re
import shutil
from pathlib import Path

from studev.core.errors import StudevError
from studev.core.problems import BUILTIN_DIR, USER_DIR, load_problem

TEMPLATE_PROBLEM = """Describe what the program should do in one or two sentences.

## Input

- Line 1: ...

## Output

What to print.

## Example

```
in:  ...
out: ...
```

## Notes

- Limits, e.g. 1 to 10,000 numbers.
- Optional hint.
"""

TEMPLATE_SOLUTION = """## Idea

Explain the approach in plain words.

## Why it works

...

## Speed

O(?) time, O(?) space.
"""


# ---------------------------------------------------------------- studev new

def create_template(name, path="."):
    """Make a new problem folder at path/name. Returns the folder path."""
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        raise StudevError(f"'{name}' isn't a valid name. Use lowercase letters, numbers "
                          "and dashes, e.g. reverse-words")

    folder = Path(path).expanduser().resolve() / name
    if folder.exists():
        raise StudevError(f"{folder} already exists")

    (folder / "data" / "sample").mkdir(parents=True)
    (folder / "data" / "secret").mkdir(parents=True)

    meta = {"title": name.replace("-", " ").title(), "difficulty": "easy", "topics": []}
    (folder / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (folder / "problem.md").write_text(TEMPLATE_PROBLEM, encoding="utf-8")
    (folder / "solution.md").write_text(TEMPLATE_SOLUTION, encoding="utf-8")

    for kind in ("sample", "secret"):
        (folder / "data" / kind / "1.in").write_text("", encoding="utf-8")
        (folder / "data" / kind / "1.out").write_text("", encoding="utf-8")

    return folder


# ---------------------------------------------------------------- studev add

def check_tests(folder):
    """Every .in needs a matching .out. Returns (sample_count, secret_count)."""
    counts = []
    for kind in ("sample", "secret"):
        inputs = list((folder / "data" / kind).glob("*.in"))
        for inp in inputs:
            if not inp.with_suffix(".out").exists():
                raise StudevError(f"data/{kind}/{inp.name} has no matching .out file")
        counts.append(len(inputs))
    return counts


def add_problem(folder):
    """Validate a problem folder and copy it into the user's problem set.

    Returns (problem, updated, warnings).
    """
    folder = Path(folder).expanduser().resolve()
    slug = folder.name
    dest = USER_DIR / slug

    # 1. Is it a valid problem? (load_problem checks the folder and meta.json)
    load_problem(folder)
    if not (folder / "problem.md").exists():
        raise StudevError(f"'{slug}' is missing problem.md")

    # 2. Does it have tests?
    sample, secret = check_tests(folder)
    if sample == 0:
        raise StudevError(f"'{slug}' needs at least one sample test in data/sample/")

    # 3. Don't clash with a built-in, and don't copy a folder onto itself
    if (BUILTIN_DIR / slug).is_dir():
        raise StudevError(f"'{slug}' is a built-in problem. Pick a different folder name.")
    if folder == dest.resolve():
        raise StudevError("That folder is already in your problem set.")

    # 4. Copy it in (replace the old copy if updating)
    updated = dest.exists()
    if updated:
        shutil.rmtree(dest)
    USER_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(folder, dest, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))

    # 5. Friendly warnings (not errors)
    warnings = []
    if secret == 0:
        warnings.append("No secret tests. 'submit' will only run the samples.")
    if not (folder / "solution.md").exists():
        warnings.append("No solution.md. 'studev solution' won't work for this one.")

    return load_problem(dest, user_created=True), updated, warnings

# ---------------------------------------------------------------- studev remove

def remove_problem(name):
    """Delete one of the user's problems from ~/.studev/problems.

    Returns the removed problem (loaded before deleting, so its title can be shown).
    """
    dest = USER_DIR / name

    if not dest.is_dir():
        if (BUILTIN_DIR / name).is_dir():
            raise StudevError(f"'{name}' is a built-in problem and can't be removed.")
        raise StudevError(f"You don't have a problem called '{name}'.")

    problem = load_problem(dest, user_created=True)
    shutil.rmtree(dest)
    return problem