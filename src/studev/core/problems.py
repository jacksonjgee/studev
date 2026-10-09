from pathlib import Path
from importlib.resources import files
from studev.core.errors import StudevError
import json
import random

BUILTIN_DIR = files("studev") / "problems"          # shipped with studev
USER_DIR = Path.home() / ".studev" / "problems"      # added with `studev add`


class Problem:
    """One problem: its info plus methods to read its files."""
    def __init__(self, slug, title, difficulty, topics, user_created, path):
        self.slug = slug
        self.title = title
        self.difficulty = difficulty
        self.topics = topics
        self.user_created = user_created
        self.path = path

    def description(self) -> str:
        file = self.path / "problem.md"
        if not file.is_file():
            raise StudevError(f"'{self.slug}' has no problem.md")
        return file.read_text(encoding="utf-8")

    def solution(self) -> str:           # reads solution.md (StudevError if missing)
        pass

    def test_cases(self, sample_only) -> list:   # [(input, expected), ...] from data/
        pass



def load_problem(folder: Path, user_created: bool = False) -> Problem:
    """Build one Problem from a folder: read meta.json, check it's valid."""
    if not folder.is_dir():
        raise StudevError(f"'{folder}' is not a folder")
    
    meta_file = folder / "meta.json"
    if not meta_file.is_file():
        raise StudevError(f"'{folder.name}' has no meta.json")

    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise StudevError(f"'{folder.name}/meta.json' is not valid JSON")

    for key in ("title", "difficulty"):
        if key not in meta:
            raise StudevError(f"'{folder.name}/meta.json' is missing '{key}'")

    if meta["difficulty"] not in ("easy", "medium", "hard"):
        raise StudevError(f"'{folder.name}' has an invalid difficulty: {meta['difficulty']}")

    return Problem(
        slug=folder.name,
        title=meta["title"],
        difficulty=meta["difficulty"],
        topics=meta.get("topics", []),
        user_created=user_created,
        path=folder,
    )


def all_problems() -> list[Problem]:
    """load_problem() on every folder in BUILTIN_DIR and USER_DIR."""
    problems = []
    
    if BUILTIN_DIR.exists():
        for folder in BUILTIN_DIR.iterdir():
            if folder.is_dir() and (folder / "meta.json").exists():
                problems.append(load_problem(folder, user_created=False))
    return problems
    if USER_DIR.exists():
        for folder in USER_DIR.iterdir(): 
            problems.append(load_problem(folder, user_created=True))
    # return problems

def get_problem(name) -> Problem:
    """Find one problem by name. StudevError if it doesn't exist."""
    for problem in all_problems():
        if problem.slug == name:
            return problem
    raise StudevError(f"No problem called '{name}'. See all problems with: studev list")

def find_problems(difficulty=None, topic=None) -> list[Problem]:
    """all_problems(), keeping only those matching the filters."""
    filters = {"difficulty": difficulty,
               "topic": topic
               }

    return  [problem for problem in all_problems() if filtered_criteria(problem, filters)]

def filtered_criteria(problem, filters: dict) -> bool:
    if filters["difficulty"] is not None and not filters["difficulty"] == problem.difficulty:
        return False
    if filters["topic"] is not None and filters["topic"] not in problem.topics:
        return False
    return True

def random_problem(difficulty=None, topic=None) -> Problem:
    """random.choice() from find_problems(). StudevError if none match."""
    matches = find_problems(difficulty=difficulty, topic=topic)
    if not matches:
        raise StudevError("No problems match those filters.")
    return random.choice(matches)