"""Command line entry point for pytodo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import core, storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pytodo", description="A tiny command line todo list."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=storage.DEFAULT_PATH,
        help="where tasks are stored (default: ~/.pytodo.json)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add_cmd = sub.add_parser("add", help="add a task")
    add_cmd.add_argument("text", nargs="+", help="what needs doing")

    list_cmd = sub.add_parser("list", help="list tasks")
    list_cmd.add_argument(
        "-a", "--all", action="store_true", help="include completed tasks"
    )

    done_cmd = sub.add_parser("done", help="mark a task complete")
    done_cmd.add_argument("id", type=int)

    rm_cmd = sub.add_parser("rm", help="delete a task")
    rm_cmd.add_argument("id", type=int)

    return parser


def format_task(task: core.Task) -> str:
    mark = "x" if task["done"] else " "
    return f"[{mark}] {task['id']:>3}  {task['text']}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tasks = storage.load(args.file)

    try:
        if args.command == "add":
            task = core.add(tasks, " ".join(args.text))
            storage.save(tasks, args.file)
            print(f"added {task['id']}: {task['text']}")

        elif args.command == "list":
            shown = core.filtered(tasks, show_all=args.all)
            if not shown:
                print("nothing to do")
            for task in shown:
                print(format_task(task))

        elif args.command == "done":
            task = core.complete(tasks, args.id)
            storage.save(tasks, args.file)
            print(f"completed {task['id']}: {task['text']}")

        elif args.command == "rm":
            task = core.remove(tasks, args.id)
            storage.save(tasks, args.file)
            print(f"removed {task['id']}: {task['text']}")

    except (core.TaskNotFound, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
