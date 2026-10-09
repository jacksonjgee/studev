from rich.prompt import Confirm

from studev.core.authoring import remove_problem
from studev.core.errors import StudevError
from studev.core.problems import USER_DIR
from studev.commands.display import console, print_removed


def run(args):
    if not (USER_DIR / args.problem).is_dir():
        # let core give the right error message (built-in vs doesn't exist)
        try:
            remove_problem(args.problem)
        except StudevError as e:
            console.print(f"[red]studev:[/] {e}")
        return

    if not Confirm.ask(f"Remove [bold]{args.problem}[/] from your problem set?", default=False):
        console.print("[dim]Nothing removed.[/]")
        return

    try:
        problem = remove_problem(args.problem)
    except StudevError as e:
        console.print(f"[red]studev:[/] {e}")
        return
    print_removed(problem)