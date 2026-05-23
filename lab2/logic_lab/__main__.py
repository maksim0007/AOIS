from __future__ import annotations

import sys

from .cli import console_menu, process_expression


def main() -> None:
    if len(sys.argv) > 1:
        print(process_expression(sys.argv[1]))
    else:
        console_menu()


if __name__ == "__main__":
    main()
