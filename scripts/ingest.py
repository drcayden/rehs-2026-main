"""Thin runner for the ingest pipeline.

    python scripts/ingest.py

Keep this file dumb: it just calls into src/ingest/ingest.py so the real logic is
testable and importable. All the work lives in the module, not here.
"""

import sys
from pathlib import Path

# Run from anywhere: put the repo root on the path so `python scripts/ingest.py`
# finds the `src/` package without needing `-m`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingest.ingest import run


def main() -> None:
    # TODO(week-05): add CLI flags if you need them (e.g. --limit, --out-dir).
    run()


if __name__ == "__main__":
    main()
