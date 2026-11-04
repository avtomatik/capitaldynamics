"""Compatibility entry point: ``python -m capitaldynamics.retirement``."""

import sys

from capitaldynamics.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["retirement", *sys.argv[1:]]))
