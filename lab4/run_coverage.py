from __future__ import annotations

import pathlib
import sys
import trace
import unittest


PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
TARGET_DIR = PROJECT_ROOT / "src"
IGNORE_DIRS = [sys.prefix, sys.exec_prefix]


def run_all_tests() -> unittest.result.TestResult:
    suite = unittest.defaultTestLoader.discover("tests")
    return unittest.TextTestRunner(verbosity=0).run(suite)


def main() -> int:
    tracer = trace.Trace(count=True, trace=False, ignoredirs=IGNORE_DIRS)
    result = tracer.runfunc(run_all_tests)
    if not result.wasSuccessful():
        return 1

    counts = tracer.results().counts
    covered_by_file: dict[pathlib.Path, set[int]] = {}
    for (filename, line_number), executions in counts.items():
        if filename.startswith("<"):
            continue

        file_path = pathlib.Path(filename).resolve()
        if TARGET_DIR not in file_path.parents:
            continue
        if executions > 0:
            covered_by_file.setdefault(file_path, set()).add(line_number)

    executable_lines = 0
    covered_lines = 0
    for file_path in TARGET_DIR.rglob("*.py"):
        source_lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, source_line in enumerate(source_lines, start=1):
            stripped = source_line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            executable_lines += 1
            if line_number in covered_by_file.get(file_path.resolve(), set()):
                covered_lines += 1

    coverage = 100.0 if executable_lines == 0 else covered_lines / executable_lines * 100
    print(f"Оценка покрытия (trace, только src): {coverage:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
