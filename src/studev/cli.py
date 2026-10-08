import argparse

from studev.commands import list_problems, new, show, test, add, remove, solution

def build_parser():
    parser = argparse.ArgumentParser(description="command-line tool for students in CS")
    subparsers = parser.add_subparsers(dest="command")

    # studev list
    list_parser = subparsers.add_parser("list", help="list all problems")

    # studev show <problem name>
    show_parser = subparsers.add_parser("show", help="show a problem's description")
    
    # studev test two-sum <your_solution.py>
    test_parser = subparsers.add_parser("test", help="test your solution")

    # studev new <problem name>
    new_parser = subparsers.add_parser("new", help="creates an problem template to fill out externally")

    # studev add <folder>
    add_parser = subparsers.add_parser("add", help="adds/updates an external problem to your problem set")

    # studev remove <problem name>
    remove_parser = subparsers.add_parser("remove", help="removes a user-created problem") 

    # studev solution <problem name>
    solution = subparsers.add_parser("solution", help="Gives a solution statement for a problem") 

    return parser
    

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args == "list":
        list_problems.run(args)
    elif args == "show":
        show.run(args)
    elif args == "remove":
        remove.run(args)
    elif args == "test":
        test.run(args)
    elif args == "new":
        new.run(args)
    elif args == "add":
        add.run(args)
    elif args == "solution":
        solution.run(args)
    else:
        parser.print_help()