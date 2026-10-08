import argparse

from studev.practice import commands as practice
from studev.terminal import ls


def main():
    parser = argparse.ArgumentParser(description="command-line tool for students in CS")
    subparser = parser.add_subparsers(dest="commands")

    # PRACTICE
    practice_parser = subparser.add_parser("practice", help="practice coding problems")
    practice_sub = practice_parser.add_subparsers(dest="action")

    # studev practice list
    list_parser = practice_sub.add_parser("list", help="list all problems")
    list_parser.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    list_parser.set_defaults(func=practice.list_problems)

    # studev practice show two-sum
    show_parser = practice_sub.add_parser("show", help="show a problem's description")
    show_parser.add_argument("problem", help="problem name, e.g. two-sum")
    show_parser.set_defaults(func=practice.show)

    # studev practice random --difficulty easy
    random_parser = practice_sub.add_parser("random", help="pick a random problem")
    random_parser.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    random_parser.set_defaults(func=practice.random_problem)

    # studev practice test two-sum solution.py
    test_parser = practice_sub.add_parser("test", help="test your solution")
    test_parser.add_argument("problem", help="problem name, e.g. two-sum")
    test_parser.add_argument("file", help="your solution file")
    test_parser.set_defaults(func=practice.test)

    # TERMINAL
    terminal_parser = subparser.add_parser("terminal", help="terminal tools and skills")
    terminal_sub = terminal_parser.add_subparsers(dest="action")

    # studev terminal ls
    ls_parser = terminal_sub.add_parser("ls", help="view a folder as a tree")
    ls_parser.add_argument("path", nargs="?", default=".", help="folder to show (default: current folder)")
    ls_parser.add_argument("--depth", "-d", type=int, help="depth of displayed tree")
    ls_parser.add_argument("--verbose", "-v", action="store_true", help="show all files, including hidden ones")
    ls_parser.set_defaults(func=ls.run)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()