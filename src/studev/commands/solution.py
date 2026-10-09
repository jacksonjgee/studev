import sys

from studev.core.errors import StudevError
from studev.core.problems import get_problem, random_problem
from studev.commands.display import console, print_solution


def run(args):
    try:        
        problem = get_problem(args.problem)
    except StudevError as error:
        console.print(f"[red]studev:[/] {error}")
        sys.exit(1)

    print_solution(problem)