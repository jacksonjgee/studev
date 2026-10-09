import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from studev.core.errors import StudevError

TIME_LIMIT = 2  # seconds


@dataclass
class TestResult:
    name: str          # e.g. "sample/1"
    status: str        # "passed", "wrong", "error", "timeout"
    input: str
    expected: str
    actual: str = ""
    error: str = ""    # stderr if it crashed


def normalise(text):
    """Ignore \\r\\n vs \\n and trailing spaces/blank lines."""
    lines = text.replace("\r\n", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines).strip()


def run_case(solution, name, inp_file, out_file):
    inp = inp_file.read_text(encoding="utf-8")
    expected = out_file.read_text(encoding="utf-8")
    try:
        result = subprocess.run(
            [sys.executable, str(solution)],
            input=inp, capture_output=True, text=True,
            encoding="utf-8", timeout=TIME_LIMIT,
        )
    except subprocess.TimeoutExpired:
        return TestResult(name, "timeout", inp, expected)

    if result.returncode != 0:
        return TestResult(name, "error", inp, expected, result.stdout, result.stderr)
    if normalise(result.stdout) == normalise(expected):
        return TestResult(name, "passed", inp, expected, result.stdout)
    return TestResult(name, "wrong", inp, expected, result.stdout)


def test_solution(problem, solution, sample_only=True):
    solution = Path(solution)
    if not solution.is_file():
        raise StudevError(f"Can't find your solution file: {solution}")

    cases = problem.test_cases(sample_only)
    if not cases:
        raise StudevError(f"'{problem.slug}' has no tests")

    return [run_case(solution, name, inp, out) for name, inp, out in cases]