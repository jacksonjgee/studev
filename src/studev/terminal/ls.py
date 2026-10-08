import sys
from pathlib import Path

IGNORED = {".git", "__pycache__", ".venv", "venv", "node_modules", ".DS_Store"}

def run(args):
    path = Path(args.path)
    validate_args(path) # Validates path 
    depth = args.depth if args.depth is not None else float('inf')
    verbose = args.verbose
    tree_search(path, depth, verbose)


def validate_args(path):
    if not path.exists():
        print(f"studev: {path} does not exist")
        sys.exit(1)
    if not path.is_dir():
        print(f"studev: {path} is not a directory")
        sys.exit(1)


def tree_search(path: Path, depth: float, verbose: bool) -> None:
    print(path.resolve().name)
    stack = children_of(path, "", 1, verbose)

    while stack:
        item, prefix, is_last, curr_depth = stack.pop()
        connector = "└── " if is_last else "├── "
        name = item.name + "/" if item.is_dir() else item.name
        print(prefix + connector + name)

        if item.is_dir() and not item.is_symlink() and curr_depth < depth:
            child_prefix = prefix + ("    " if is_last else "│   ")
            stack.extend(children_of(item, child_prefix, curr_depth + 1, verbose))


def children_of(folder: Path, prefix: str, depth: int, verbose: bool) -> list:
    """Return stack entries for a folder's children, reversed so they pop in order."""
    try:
        entries = list(folder.iterdir())
    except PermissionError:
        return []

    if not verbose:
        entries = [e for e in entries if not is_hidden(e)]

    entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    last = len(entries) - 1
    items = [(entry, prefix, i == last, depth) for i, entry in enumerate(entries)]
    return items[::-1]


def is_hidden(entry: Path) -> bool:
    return entry.name in IGNORED or entry.name.startswith(".")