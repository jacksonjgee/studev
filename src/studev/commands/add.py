from studev.core.authoring import add_problem
from studev.core.errors import StudevError
from studev.commands.display import console, print_added


def run(args):
    try:
        problem, updated, warnings = add_problem(args.folder)
    except StudevError as e:
        console.print(f"[red]studev:[/] {e}")
        return
    print_added(problem, updated, warnings)