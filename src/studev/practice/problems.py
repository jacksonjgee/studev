import json
from dataclasses import dataclass
from importlib.resources import files

PROBLEMS_DIR = files("studev") / "data" / "problems"


@dataclass
class Problem:
    slug: str
    title: str
    difficulty: str
    topics: list
    path: object  # the problem's folder

    def description(self) -> str:
        return (self.path / "problem.md").read_text()


def load_problem(slug: str) -> Problem:
    folder = PROBLEMS_DIR / slug
    meta_file = folder / "meta.json"
    if not meta_file.is_file():
        raise ValueError(f"no problem called '{slug}'")

    meta = json.loads(meta_file.read_text())
    return Problem(
        slug=slug,
        title=meta["title"],
        difficulty=meta["difficulty"],
        topics=meta.get("topics", []),
        path=folder,
    )


def all_problems() -> list:
    problems = []
    for folder in PROBLEMS_DIR.iterdir():
        if folder.is_dir() and (folder / "meta.json").is_file():
            problems.append(load_problem(folder.name))
    return problems