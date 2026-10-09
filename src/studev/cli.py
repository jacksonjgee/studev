import argparse
import sys
from importlib.metadata import metadata, version

from studev.commands import add, info, list_problems, new, remove, show, solution, submit, test
from studev.commands.display import console, print_home, print_parser_help


class StudevParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        if self.prog == "studev":
            print_home(version("studev"), metadata("studev")["Summary"])
        else:
            print_parser_help(self)

    def error(self, message):
        console.print(f"[red]studev:[/] {message}")
        console.print(f" [dim]See[/] [bold blue]{self.prog} -h[/]")
        sys.exit(2)


def build_parser():
    parser = StudevParser(prog="studev", description=metadata("studev")["Summary"])
    parser.add_argument("--version", action="version", version=f"studev {version('studev')}")
    subparsers = parser.add_subparsers(dest="command")

    DIFFICULTIES = ["easy", "medium", "hard"]

    # studev list
    list_parser = subparsers.add_parser(
        "list", help="list all problems",
        description="List every problem in your problem set: the built-in ones and any you've added. "
                    "Use the filters to narrow it down by difficulty, topic, starred or your own.",
        epilog="""
studev list                    # every problem
studev list -d easy            # only easy problems
studev list -t arrays          # only problems tagged 'arrays'
studev list --mine             # only problems you've added
""")
    list_parser.add_argument("--difficulty", "-d", type=str.lower, choices=DIFFICULTIES, help="filter by difficulty")
    list_parser.add_argument("--topic", "-t", help="filter by topic")
    list_parser.add_argument("--starred", "-s", action="store_true", help="only show starred problems")
    list_parser.add_argument("--mine", "-m", action="store_true", help="only show your own problems")

    # studev show <problem name>
    show_parser = subparsers.add_parser(
        "show", help="show a problem's description",
        description="Print a problem's full description: what to do, the input and output format, "
                    "and an example. Give a problem name, or use --random to get a surprise "
                    "(optionally filtered by difficulty or topic).",
        epilog="""
studev show two-sum              # read Two Sum
studev show --random             # a random problem
studev show -r -d medium         # a random medium problem
""")
    show_parser.add_argument("problem", nargs="?", help="problem name, e.g. two-sum")
    show_parser.add_argument("--random", "-r", action="store_true", help="show a random problem")
    show_parser.add_argument("--difficulty", "-d", type=str.lower, choices=DIFFICULTIES, help="filter the random pick by difficulty")
    show_parser.add_argument("--topic", "-t", help="filter the random pick by topic")
    show_parser.add_argument("--starred", "-s", action="store_true", help="only pick from starred problems")
    show_parser.add_argument("--mine", "-m", action="store_true", help="only pick from your own problems")

    # studev info <problem name>
    info_parser = subparsers.add_parser(
        "info", help="show a problem's details (difficulty, topics, stats)",
        description="Show a quick summary of a problem without the full description: "
                    "its difficulty, topics, how many sample and secret tests it has, "
                    "and where it lives if you created it.",
        epilog="""
studev info two-sum              # details for Two Sum
studev info --random             # details for a random problem
""")
    info_parser.add_argument("problem", nargs="?", help="problem name, e.g. two-sum")
    info_parser.add_argument("--random", "-r", action="store_true", help="show details of a random problem")

    # studev test <problem name> <your_solution>
    test_parser = subparsers.add_parser(
        "test", help="quick check: run your solution against the sample tests",
        description="Run your solution against the sample tests: the same ones shown in the problem. "
                    "Your program reads from input() and prints its answer. If a test fails, "
                    "studev shows the input, the expected output and your output side by side.",
        epilog="""
studev test two-sum solution.py          # run the sample tests
studev test two-sum ~/practice/ts.py     # your file can be anywhere
""")
    test_parser.add_argument("problem", help="problem name, e.g. two-sum")
    test_parser.add_argument("solution", help="your solution file")

    # studev submit <problem name> <your_solution>
    submit_parser = subparsers.add_parser(
        "submit", help="full check: run your solution against all tests",
        description="Run your solution against every test, including hidden secret tests "
                    "that check edge cases. Pass them all to solve the problem. "
                    "Secret test inputs stay hidden so you can't hard-code the answers.",
        epilog="""
studev submit two-sum solution.py        # run all tests
""")
    submit_parser.add_argument("problem", help="problem name, e.g. two-sum")
    submit_parser.add_argument("solution", help="your solution file")

    # studev new <problem name> [--path folder]
    new_parser = subparsers.add_parser(
        "new", help="create a problem template to fill out",
        description="Create a folder with everything a problem needs: problem.md, meta.json, "
                    "solution.md and a data folder for tests. Fill it in, then add it to your "
                    "problem set with 'studev add'.",
        epilog="""
studev new reverse-words                 # create ./reverse-words/
studev new reverse-words -p ~/problems   # create it somewhere else
""")
    new_parser.add_argument("problem", help="name for the new problem, e.g. reverse-words")
    new_parser.add_argument("--path", "-p", default=".", help="folder to create the template in (default: current folder)")

    # studev add [folder]
    add_parser = subparsers.add_parser(
        "add", help="add or update one of your problems from a folder",
        description="Check a problem folder is valid and copy it into your problem set, "
                    "so it shows up in 'studev list'. Run it again after editing to update it.",
        epilog="""
studev add                       # add the folder you're in
studev add reverse-words         # add a specific folder
""")
    add_parser.add_argument("folder", nargs="?", default=".", help="path to the problem folder (default: current folder)")

    # studev remove <problem name>
    remove_parser = subparsers.add_parser(
        "remove", help="remove one of your own problems",
        description="Remove a problem you added from your problem set. "
                    "Built-in problems can't be removed. Your original folder is not touched.",
        epilog="""
studev remove reverse-words      # remove your reverse-words problem
""")
    remove_parser.add_argument("problem", help="problem name, e.g. reverse-words")

    # studev solution <problem name>
    solution_parser = subparsers.add_parser(
        "solution", help="show the solution explanation for a problem",
        description="Show an explanation of how to solve a problem: the idea, "
                    "why it works and how fast it is. There's no code, so you still get to write it yourself.",
        epilog="""
studev solution two-sum          # how to solve Two Sum
""")
    solution_parser.add_argument("problem", help="problem name, e.g. two-sum")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        list_problems.run(args)
    elif args.command == "show":
        show.run(args)
    elif args.command == "info":
        info.run(args)
    elif args.command == "test":
        test.run(args)
    elif args.command == "submit":
        submit.run(args)
    elif args.command == "new":
        new.run(args)
    elif args.command == "add":
        add.run(args)
    elif args.command == "remove":
        remove.run(args)
    elif args.command == "solution":
        solution.run(args)
    else:
        parser.print_help()