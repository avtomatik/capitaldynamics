"""Compatibility entry point: ``python -m capitaldynamics.acquisition``."""

import sys

from capitaldynamics.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["acquisition", *sys.argv[1:]]))
