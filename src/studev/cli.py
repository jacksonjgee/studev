import argparse
from importlib.metadata import metadata, version

from studev.commands import list_problems, new, show, test, add, remove, solution, submit


def build_parser():
    parser = argparse.ArgumentParser(description=metadata("studev")["Summary"])
    parser.add_argument("--version", action="version", version=f"studev {version('studev')}")
    subparsers = parser.add_subparsers(dest="command")

    # studev list
    list_parser = subparsers.add_parser("list", help="list all problems")

    # studev show <problem name>
    show_parser = subparsers.add_parser("show", help="show a problem's description")
    
    # studev test <problem name> <your_solution>
    test_parser = subparsers.add_parser("test", help="Unoffical testing of solution, fast against sample data")

    # studev new <problem name>
    new_parser = subparsers.add_parser("new", help="creates an problem template to fill out externally")

    # studev add <folder>
    add_parser = subparsers.add_parser("add", help="adds/updates an external problem to your problem set")

    # studev remove <problem name>
    remove_parser = subparsers.add_parser("remove", help="removes a user-created problem") 

    # studev solution <problem name>
    solution_parser = subparsers.add_parser("solution", help="Gives a solution statement for a problem") 

    # studev submit <problem name> <your_solution>
    submit_parser = subparsers.add_parser("submit", help="Official submittion of solution, tests against all test cases.") 

    return parser
    

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        list_problems.run(args)
    elif args.command == "show":
        show.run(args)
    elif args.command == "remove":
        remove.run(args)
    elif args.command == "test":
        test.run(args)
    elif args.command == "submit":
        submit.run(args)
    elif args.command == "new":
        new.run(args)
    elif args.command == "add":
        add.run(args)
    elif args.command == "solution":
        solution.run(args)
    else:
        parser.print_help()