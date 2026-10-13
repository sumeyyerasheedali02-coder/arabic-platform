"""Compatibility entry point: `python seed_database.py`.

Kept at this path because earlier deployment start commands ran it before
starting the server. It is now safe to run at every start: it fills an EMPTY
database with the base content and does nothing otherwise.

The real tool, with all options, is `python -m tools.seed --help`.
"""
import sys

from tools.seed import main

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
