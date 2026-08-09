import pytest

from pytodo import core


def test_add_assigns_sequential_ids():
    tasks = []
    assert core.add(tasks, "buy milk")["id"] == 1
    assert core.add(tasks, "walk dog")["id"] == 2
    assert len(tasks) == 2


def test_add_rejects_blank_text():
    with pytest.raises(ValueError):
        core.add([], "   ")


def test_ids_are_not_reused_after_delete():
    tasks = []
    core.add(tasks, "one")
    core.add(tasks, "two")
    core.remove(tasks, 2)
    assert core.add(tasks, "three")["id"] == 2


def test_complete_marks_done_and_stamps_time():
    tasks = []
    core.add(tasks, "ship it")
    task = core.complete(tasks, 1)
    assert task["done"] is True
    assert "completed" in task


def test_missing_id_raises():
    with pytest.raises(core.TaskNotFound):
        core.complete([], 99)


def test_filtered_hides_completed_by_default():
    tasks = []
    core.add(tasks, "pending")
    core.add(tasks, "finished")
    core.complete(tasks, 2)
    assert [t["id"] for t in core.filtered(tasks)] == [1]
    assert [t["id"] for t in core.filtered(tasks, show_all=True)] == [1, 2]
