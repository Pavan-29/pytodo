"""JSON-backed persistence for tasks."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(os.environ.get("PYTODO_FILE", Path.home() / ".pytodo.json"))


def load(path: Path = DEFAULT_PATH) -> list[dict[str, Any]]:
    """Return the stored tasks, or an empty list if nothing is saved yet."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(f"{path} does not contain a task list")
    return data


def save(tasks: list[dict[str, Any]], path: Path = DEFAULT_PATH) -> None:
    """Write tasks to disk atomically so a crash can't truncate the file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(tasks, fh, indent=2)
        fh.write("\n")
    tmp.replace(path)
