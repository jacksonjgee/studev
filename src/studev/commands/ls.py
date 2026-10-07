import sys
from pathlib import Path

def run(args):
    path = Path(args.path)
    validate_args(path) # Validates path 
    depth = args.depth if args.depth is not None else float('inf')

    tree_search(path, depth, args.verbose)

def validate_args(path: Path) -> None:
    if not path.exists():
        print(f"studev: '{path}' does not exist")
        sys.exit(1)
    if not path.is_dir():
        print(f"studev: '{path}' is a file, not a folder")
        sys.exit(1)

def tree_search(path: Path, depth: float, verbose: bool) -> None:
    print(path.resolve().name)
    stack = children_of(path, prefix="", depth=1)

    while stack:
        item, prefix, is_last, curr_depth = stack.pop()
        connector = "└── " if is_last else "├── "
        name = item.name + "/" if item.is_dir() else item.name
        print(prefix + connector + name)

        if item.is_dir() and not item.is_symlink() and curr_depth < depth:
            child_prefix = prefix + ("    " if is_last else "│   ")
            stack.extend(children_of(item, child_prefix, curr_depth + 1))


def children_of(folder: Path, prefix: str, depth: int) -> list:
    """Return stack entries for a folder's children, reversed so they pop in order."""
    try:
        entries = sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        return []
    last = len(entries) - 1
    items = [(entry, prefix, i == last, depth) for i, entry in enumerate(entries)]
    return items[::-1]