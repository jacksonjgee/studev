import argparse
from importlib.metadata import metadata, version

from studev.commands import list_problems, new, show, test, add, remove, solution, submit, info


def build_parser():
    parser = argparse.ArgumentParser(description=metadata("studev")["Summary"])
    parser.add_argument("--version", action="version", version=f"studev {version('studev')}")
    subparsers = parser.add_subparsers(dest="command")

    DIFFICULTIES = ["easy", "medium", "hard"]

    # studev list
    list_parser = subparsers.add_parser("list", help="list all problems")
    list_parser.add_argument("--difficulty", "-d", type=str.lower, choices=DIFFICULTIES, help="filter by difficulty")
    list_parser.add_argument("--topic", "-t", help="filter by topic")
    list_parser.add_argument("--starred", "-s", action="store_true", help="only show starred problems")
    list_parser.add_argument("--mine", "-m", action="store_true", help="only show your own problems")

    # studev show <problem name>
    show_parser = subparsers.add_parser("show", help="show a problem's description")
    show_parser.add_argument("problem", nargs="?", help="problem name, e.g. two-sum")
    show_parser.add_argument("--random", "-r", action="store_true", help="show a random problem")
    show_parser.add_argument("--difficulty", "-d", type=str.lower, choices=DIFFICULTIES, help="filter the random pick by difficulty")
    show_parser.add_argument("--topic", "-t", help="filter the random pick by topic")
    show_parser.add_argument("--starred", "-s", action="store_true", help="only show starred problems")
    show_parser.add_argument("--mine", "-m", action="store_true", help="only show your own problems")

    # studev info <problem name>
    info_parser = subparsers.add_parser("info", help="show a problem's details (difficulty, topics, stats)")
    info_parser.add_argument("problem", help="problem name, e.g. two-sum")
    info_parser.add_argument("--random", "-r", action="store_true", help="show details of a random problem")

    # studev test <problem name> <your_solution>
    test_parser = subparsers.add_parser("test", help="quick check: run your solution against the sample tests")
    test_parser.add_argument("problem", help="problem name, e.g. two-sum")
    test_parser.add_argument("solution", help="your solution file")

    # studev submit <problem name> <your_solution>
    submit_parser = subparsers.add_parser("submit", help="full check: run your solution against all tests")
    submit_parser.add_argument("problem", help="problem name, e.g. two-sum")
    submit_parser.add_argument("solution", help="your solution file")

    # studev new <problem name> [--path folder]
    new_parser = subparsers.add_parser("new", help="create a problem template to fill out")
    new_parser.add_argument("problem", help="name for the new problem, e.g. reverse-words")
    new_parser.add_argument("--path", "-p", default=".", help="folder to create the template in (default: current folder)")

    # studev add [folder]
    add_parser = subparsers.add_parser("add", help="add or update one of your problems from a folder")
    add_parser.add_argument("folder", nargs="?", default=".", help="path to the problem folder (default: current folder)")

    # studev remove <problem name>
    remove_parser = subparsers.add_parser("remove", help="remove one of your own problems")
    remove_parser.add_argument("problem", help="problem name, e.g. reverse-words")

    # studev solution <problem name>
    solution_parser = subparsers.add_parser("solution", help="show the solution explanation for a problem")
    solution_parser.add_argument("problem", help="problem name, e.g. two-sum") 

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
    elif args.command == "info":
        info.run(args)
    else:
        parser.print_help()