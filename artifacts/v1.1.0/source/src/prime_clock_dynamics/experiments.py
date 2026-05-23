"""Shared helpers for experiment scripts."""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping, Sequence
from pathlib import Path


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    """Write mapping rows to ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(path: Path, metadata: Mapping[str, object]) -> None:
    """Write JSON metadata to ``path``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
