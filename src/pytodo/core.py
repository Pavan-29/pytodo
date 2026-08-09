"""Task operations, kept free of I/O so they are easy to test."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

Task = dict[str, Any]


class TaskNotFound(Exception):
    """Raised when an id does not match any task."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def next_id(tasks: list[Task]) -> int:
    return max((task["id"] for task in tasks), default=0) + 1


def add(tasks: list[Task], text: str) -> Task:
    text = text.strip()
    if not text:
        raise ValueError("task text must not be empty")
    task: Task = {
        "id": next_id(tasks),
        "text": text,
        "done": False,
        "created": _now(),
    }
    tasks.append(task)
    return task


def find(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise TaskNotFound(f"no task with id {task_id}")


def complete(tasks: list[Task], task_id: int) -> Task:
    task = find(tasks, task_id)
    task["done"] = True
    task["completed"] = _now()
    return task


def remove(tasks: list[Task], task_id: int) -> Task:
    task = find(tasks, task_id)
    tasks.remove(task)
    return task


def filtered(tasks: list[Task], show_all: bool = False) -> list[Task]:
    """Pending tasks by default; everything when show_all is set."""
    if show_all:
        return list(tasks)
    return [task for task in tasks if not task["done"]]
