from studev.core.problems import find_problems
from studev.commands.display import print_problem_table

def run(args):
    problems = find_problems(args.difficulty, args.topic)
    print_problem_table(problems)