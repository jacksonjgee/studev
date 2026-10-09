import argparse
from pathlib import Path

from rich import box
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

console = Console(highlight=False)  # stop rich auto-colouring numbers etc.

# ---------------------------------------------------------------- theme
# Change these to restyle all of studev in one place.
ACCENT = "dim"           # borders of normal panels and tables
HEADING = "medium_purple1"  # section titles (purple, no underline)
GOOD = "bold green"      # command names, success
TIP = "bold blue"        # the one highlighted command under each screen
NAME = "bold"            # problem slugs, argument names, flags
MUTED = "grey70"         # secondary text

DIFFICULTY_COLOURS = {"easy": "green", "medium": "yellow", "hard": "red"}

STATUS = {
    "passed":  ("✓", "green",  "passed"),
    "wrong":   ("✗", "red",    "wrong answer"),
    "error":   ("✗", "red",    "crashed"),
    "timeout": ("✗", "yellow", "too slow"),
}


# ---------------------------------------------------------------- helpers

def colour_of(problem):
    return DIFFICULTY_COLOURS.get(problem.difficulty, "white")


def difficulty_badge(difficulty):
    """e.g. ' easy ' in black on green. All badges are the same width."""
    colour = DIFFICULTY_COLOURS.get(difficulty, "white")
    return Text.assemble((f" {difficulty:^6} ", f"bold black on {colour}"), justify="left")


def meta_line(problem):
    """Difficulty badge followed by the topics."""
    line = difficulty_badge(problem.difficulty)
    if problem.topics:
        line.append("  " + " · ".join(problem.topics), style=MUTED)
    return line


def tip(message, command):
    console.print(f" [{MUTED}]{message}[/] [{TIP}]{command}[/]")
    console.print()


def section(content, title):
    """A neutral rounded panel with a heading-style title."""
    heading = Text(title, style=f"{HEADING} not dim")  # "not dim" so the dim border doesn't fade it
    return Panel(content, title=heading, title_align="left",
                 border_style=ACCENT, box=box.ROUNDED, padding=(1, 2))


def command_text(command):
    """'studev show <problem>' -> dim 'studev', green 'show', dim '<problem>'."""
    parts = command.split(" ", 2)          # ["studev", "show", "<problem>"]
    text = Text(parts[0], style=MUTED)
    if len(parts) > 1:
        text.append(" " + parts[1], style=GOOD)
    if len(parts) > 2:
        text.append(" " + parts[2], style=MUTED)
    return text


# ---------------------------------------------------------------- list

def print_problem_table(problems):
    table = Table(
        title="[bold]Problems[/]",
        caption=f"{len(problems)} problem{'s' if len(problems) != 1 else ''}",
        box=box.ROUNDED,
        border_style=ACCENT,
        header_style="bold",
        padding=(0, 1),
    )
    table.add_column("Name", style=NAME, no_wrap=True)
    table.add_column("Title")
    table.add_column("Difficulty", justify="center")
    table.add_column("Topics", style=MUTED)

    for p in problems:
        table.add_row(p.slug, p.title, Align.center(difficulty_badge(p.difficulty)), ", ".join(p.topics))

    console.print()
    if not problems:
        console.print(Panel(f"[{MUTED}]No problems match those filters.[/]",
                            border_style=ACCENT, box=box.ROUNDED, expand=False))
        console.print()
        return

    console.print(table)
    tip("Read a problem with", f"studev show {problems[0].slug}")


# ---------------------------------------------------------------- show

def print_problem(problem):
    body = Group(meta_line(problem), Text(), Markdown(problem.description()))
    console.print()
    console.print(Panel(
        body,
        title=f"[bold]{problem.title}[/]",
        title_align="left",
        border_style=colour_of(problem),
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    tip("Test it with", f"studev test {problem.slug} <your-file>")


# ---------------------------------------------------------------- info

def print_problem_info(problem):
    grid = Table.grid(padding=(0, 3))
    grid.add_column(style=MUTED, justify="right")   # labels
    grid.add_column()                               # values

    sample, secret = problem.test_counts()

    grid.add_row("Difficulty", difficulty_badge(problem.difficulty))
    grid.add_row("Topics", ", ".join(problem.topics) or "-")
    grid.add_row("Tests", f"{sample} sample · {secret} secret")
    grid.add_row("Source", "[magenta]yours[/]" if problem.user_created else "built-in")

    if problem.user_created:
        location = str(problem.path).replace(str(Path.home()), "~")
        grid.add_row("Location", Text(location, style=MUTED))

    console.print()
    console.print(Panel(
        grid,
        title=f"[bold]{problem.title}[/]",
        title_align="left",
        border_style=colour_of(problem),
        box=box.ROUNDED,
        padding=(1, 2),
        expand=False,
    ))
    tip("Read it with", f"studev show {problem.slug}")


# ---------------------------------------------------------------- test / submit

def print_results(results, title="Test results"):
    failed = [r for r in results if r.status != "passed"]
    passed = len(results) - len(failed)
    all_passed = not failed

    rows = Table.grid(padding=(0, 2))
    rows.add_column()                 # icon
    rows.add_column(style="bold")     # test name
    rows.add_column()                 # status
    for r in results:
        icon, colour, label = STATUS[r.status]
        rows.add_row(f"[{colour}]{icon}[/]", r.name, f"[{colour}]{label}[/]")

    summary_colour = "green" if all_passed else "red"
    summary = (f"[bold green]All {passed} tests passed![/]" if all_passed
               else f"[bold red]{passed}/{len(results)} passed[/]")

    console.print()
    console.print(Panel(
        rows,
        title=f"[bold]{title}[/]",
        title_align="left",
        subtitle=summary,
        subtitle_align="right",
        border_style=summary_colour,
        box=box.ROUNDED,
        padding=(1, 2),
    ))

    first_sample_fail = next((r for r in failed if r.name.startswith("sample")), None)
    if first_sample_fail:
        print_failure(first_sample_fail)
    elif failed:
        console.print(Panel(
            f"[{MUTED}]Secret tests are hidden. Think about edge cases:\n"
            "empty input, very big numbers, duplicates, negatives.[/]",
            title="Hint", title_align="left", border_style="yellow",
            box=box.ROUNDED, expand=False,
        ))
    console.print()


def print_failure(r):
    icon, colour, label = STATUS[r.status]

    input_panel = Panel(Text(r.input.rstrip() or "(empty)"), title="Input",
                        title_align="left", border_style=ACCENT, box=box.ROUNDED)

    if r.status == "timeout":
        detail = Text("Your code took longer than the time limit. Infinite loop, or too slow?",
                      style="yellow")
    elif r.status == "error":
        last_lines = "\n".join(r.error.strip().splitlines()[-6:])
        detail = Panel(Text(last_lines), title="Error", title_align="left",
                       border_style="red", box=box.ROUNDED)
    else:
        compare = Table(box=box.ROUNDED, border_style=ACCENT, header_style="bold", expand=True)
        compare.add_column("Expected", style="green", ratio=1)
        compare.add_column("Your output", style="red", ratio=1)
        compare.add_row(Text(r.expected.rstrip()),
                        Text(r.actual.rstrip() or "(nothing printed)"))
        detail = compare

    console.print(Panel(
        Group(input_panel, detail),
        title=f"[bold {colour}]{icon} {r.name} · {label}[/]",
        title_align="left",
        border_style=colour,
        box=box.ROUNDED,
        padding=(0, 1),
    ))


# ---------------------------------------------------------------- solution

def print_solution(problem):
    console.print()
    console.print(Panel(
        Markdown(problem.solution()),
        title=f"[bold]{problem.title}[/] [{MUTED}]· solution[/]",
        title_align="left",
        border_style=ACCENT,
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    tip("Try it yourself with", f"studev test {problem.slug} <your-file>")

# ---------------------------------------------------------------- home screen (plain `studev`)

COMMAND_GROUPS = [
    ("Practice", [
        ("list", "see all problems"),
        ("show <problem>", "read a problem"),
        ("info <problem>", "difficulty, topics and tests"),
        ("solution <problem>", "read the solution explanation"),
    ]),
    ("Check your code", [
        ("test <problem> <file>", "run the sample tests"),
        ("submit <problem> <file>", "run all tests"),
    ]),
    ("Your own problems", [
        ("new <name>", "create a problem template"),
        ("add [folder]", "add it to your problem set"),
        ("remove <problem>", "remove one of your problems"),
    ]),
]


def print_home(version, description):
    console.print()
    console.print(Text.assemble((" studev", GOOD), (f" v{version}", MUTED)))
    console.print(f" [{MUTED}]{description}[/]")
    console.print()

    for title, commands in COMMAND_GROUPS:
        grid = Table.grid(padding=(0, 3))
        grid.add_column(no_wrap=True)
        grid.add_column()
        for cmd, desc in commands:
            grid.add_row(command_text(f"studev {cmd}"), desc)
        console.print(section(grid, title))

    console.print()
    tip("Start with", "studev show --random")
    console.print(f" [{MUTED}]Add[/] [bold]-h[/] [{MUTED}]to any command for its options.[/]")
    console.print()


# ---------------------------------------------------------------- help (studev <command> -h)

def print_parser_help(parser):
    """Draw any argparse parser's help in studev's panel style."""
    usage = parser.format_usage().replace("usage: ", "").strip()

    arguments = Table.grid(padding=(0, 3))
    arguments.add_column(style=NAME, no_wrap=True)
    arguments.add_column()

    options = Table.grid(padding=(0, 3))
    options.add_column(style=NAME, no_wrap=True)
    options.add_column()

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            continue
        help_text = action.help or ""
        if action.choices:
            help_text += f" ({', '.join(action.choices)})"

        if action.option_strings:                      # e.g. --difficulty, -d <difficulty>
            flags = ", ".join(action.option_strings)
            if action.nargs != 0:
                flags += f" <{action.metavar or action.dest}>"
            options.add_row(Text(flags), Text(help_text))
        else:                                          # positional, e.g. problem
            name = action.metavar or action.dest
            if action.nargs == "?":
                name = f"[{name}]"
            arguments.add_row(Text(name), Text(help_text))

    console.print()
    console.print(Text(" ") + command_text(parser.prog))
    if parser.description:
        console.print(f" [{MUTED}]{parser.description}[/]")
    console.print()

    console.print(section(command_text(usage), "Usage"))
    if arguments.row_count:
        console.print(section(arguments, "Arguments"))
    console.print(section(options, "Options"))

    if parser.epilog:                     # examples, one per line: "command  # what it does"
        examples = Table.grid(padding=(0, 3))
        examples.add_column(no_wrap=True)
        examples.add_column(style=MUTED)
        for line in parser.epilog.strip().splitlines():
            cmd, _, note = line.partition("#")
            examples.add_row(command_text(cmd.strip()), note.strip())
        console.print(section(examples, "Examples"))
    console.print()

def print_added(problem, updated, warnings):
    action = "Updated" if updated else "Added"
    body = Group(
        meta_line(problem),
        Text(),
        Text(f"{action} '{problem.slug}' in your problem set.", style="green"),
        *[Text(f"⚠ {w}", style="yellow") for w in warnings],
    )
    console.print()
    console.print(Panel(body, title=f"[bold green]✓ {problem.title}[/]", title_align="left",
                        border_style="green", box=box.ROUNDED, padding=(1, 2)))
    tip("Try it with", f"studev show {problem.slug}")

def print_created(folder):
    files = Table.grid(padding=(0, 3))
    files.add_column(style=NAME, no_wrap=True)
    files.add_column(style=MUTED)
    files.add_row("problem.md", "what to solve, input/output and an example")
    files.add_row("meta.json", "title, difficulty (easy/medium/hard) and topics")
    files.add_row("solution.md", "how to solve it (optional)")
    files.add_row("data/sample/", "tests shown to the student (1.in → 1.out)")
    files.add_row("data/secret/", "hidden tests for submit")

    location = str(folder).replace(str(Path.home()), "~")
    console.print()
    console.print(Panel(files, title=f"[bold green]✓ Created {folder.name}[/]",
                        subtitle=Text(location, style=MUTED), subtitle_align="right",
                        title_align="left", border_style="green", box=box.ROUNDED, padding=(1, 2)))
    tip("Fill it in, then run", f"studev add {location}")

def print_removed(problem):
    console.print()
    console.print(Panel(
        Text(f"Removed '{problem.slug}' from your problem set.", style=MUTED),
        title=f"[bold red]✗ {problem.title}[/]", title_align="left",
        border_style="red", box=box.ROUNDED, padding=(1, 2), expand=False,
    ))
    tip("Add it back any time with", f"studev add <folder>")