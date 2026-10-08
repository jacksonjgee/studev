from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

import sys

from studev.practice.problems import all_problems, load_problem

console = Console()

DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}
DIFFICULTY_COLOURS = {"easy": "green", "medium": "yellow", "hard": "red"}


def list_problems(args):
    problems = all_problems()

    if args.difficulty:
        problems = [p for p in problems if p.difficulty == args.difficulty]

    if not problems:
        level = f"{args.difficulty} " if args.difficulty else ""
        console.print(f"No {level}problems yet.")
        return

    problems.sort(key=lambda p: (DIFFICULTY_ORDER.get(p.difficulty, 99), p.title))

    table = Table()
    table.add_column("Name", style="bold")
    table.add_column("Title")
    table.add_column("Difficulty")
    table.add_column("Topics", style="dim")

    for p in problems:
        colour = DIFFICULTY_COLOURS.get(p.difficulty, "white")
        table.add_row(p.slug, p.title, f"[{colour}]{p.difficulty}[/]", ", ".join(p.topics))

    console.print(table)
    count = f"{len(problems)} problem" + ("" if len(problems) == 1 else "s")
    console.print(f"{count} · try: studev practice show {problems[0].slug}")

def show(args):
    try:
        problem = load_problem(args.problem)
    except ValueError as error:
        console.print(f"[red]studev:[/] {error}")
        console.print("See all problems with: studev practice list")
        sys.exit(1)

    colour = DIFFICULTY_COLOURS.get(problem.difficulty, "white")
    console.rule(f"[bold]{problem.title}[/]")
    console.print(f"[{colour}]{problem.difficulty}[/] · {', '.join(problem.topics)}")
    console.print(Markdown(problem.description()))
    console.rule()
    console.print(f"When you're ready: studev practice test {problem.slug} <your-file>")

def random_problem(args):
    print("random coming soon")

def test(args):
    print(f"testing {args.file} against {args.problem} coming soon")