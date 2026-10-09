import sys

from studev.core.errors import StudevError
from studev.core.problems import get_problem, random_problem
from studev.commands.display import console, print_problem_info


def run(args):
    if args.random == bool(args.problem):
        console.print("[red]studev:[/] give a problem name or --random (not both)")
        sys.exit(1)

    try:
        if args.random:
            problem = random_problem()
        else:
            problem = get_problem(args.problem)
    except StudevError as error:
        console.print(f"[red]studev:[/] {error}")
        sys.exit(1)

    print_problem_info(problem)