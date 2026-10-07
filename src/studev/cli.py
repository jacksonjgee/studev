import argparse

from studev.commands import ls, explain, help


def main():
    parser = argparse.ArgumentParser(description="command-line tool for students in CS")
    subparser = parser.add_subparsers(dest="commands")

    subparser.add_parser("ls", help="view a folder as a tree")
    subparser.add_parser("explain", help="explain a native command")

    args = parser.parse_args()

    if args.commands == "ls":
        ls.main(args)
    elif args.commands == "explain":
        explain.main(args)
    else:
       help.main(args)