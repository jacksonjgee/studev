from studev.core.authoring import create_template
from studev.core.errors import StudevError
from studev.commands.display import console, print_created


def run(args):
    try:
        folder = create_template(args.problem, args.path)
    except StudevError as e:
        console.print(f"[red]studev:[/] {e}")
        return
    print_created(folder)