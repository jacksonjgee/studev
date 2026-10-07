import argparse

from studev.commands import ls, explain, help


def main():
    parser = argparse.ArgumentParser(description="command-line tool for students in CS")
    subparser = parser.add_subparsers(dest="commands")

    # command: studev ls
    ls_parser = subparser.add_parser("ls", help="view a folder as a tree")
    ls_parser.add_argument("--depth","-d", type=int, help="depth of displayed tree")
    ls_parser.add_argument("--verbose","-v", action="store_true", help="Show all the files in each directory")
    ls_parser.add_argument("path", nargs="?", default=".", help="folder to show (default: current folder)")

    subparser.add_parser("explain", help="explain a native command")

    args = parser.parse_args()

    if args.commands == "ls":
        ls.run(args)
    elif args.commands == "explain":
        explain.run(args)
    else:
       help.run(args)