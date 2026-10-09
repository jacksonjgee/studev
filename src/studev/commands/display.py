from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()

DIFFICULTY_COLOURS = {"easy": "green", "medium": "yellow", "hard": "red"}

def print_problem_table(problems):
    table = Table(title="Problems")
    table.add_column("Name", style="bold")
    table.add_column("Title")
    table.add_column("Difficulty")
    table.add_column("Topics", style="dim")

    for p in problems:
        colour = DIFFICULTY_COLOURS.get(p.difficulty, "white")
        table.add_row(p.slug, p.title, f"[{colour}]{p.difficulty}[/]", ", ".join(p.topics))

    console.print("\n")
    console.print(table)
    if problems:
            console.print(f"[dim]Tip: read a problem with[/] [bold blue]studev show {problems[0].slug}[/]")
            console.print("\n")

def print_problem(problem):
    colour = DIFFICULTY_COLOURS.get(problem.difficulty, "white")
    console.rule(f"[bold]{problem.title}[/]")
    console.print(f"[{colour}]{problem.difficulty}[/] · {', '.join(problem.topics)}")
    console.print("\n")
    console.print(Markdown(problem.description()))
    console.rule()
    console.print(f"[dim]Test it with[/] [bold blue]studev test {problem.slug} <your-file>[/]")