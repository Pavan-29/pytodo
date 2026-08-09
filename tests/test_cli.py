from pytodo import storage
from pytodo.cli import main


def test_add_then_list(tmp_path, capsys):
    store = tmp_path / "tasks.json"
    assert main(["--file", str(store), "add", "write", "tests"]) == 0
    assert main(["--file", str(store), "list"]) == 0
    out = capsys.readouterr().out
    assert "write tests" in out


def test_done_hides_task_from_default_list(tmp_path, capsys):
    store = tmp_path / "tasks.json"
    main(["--file", str(store), "add", "temporary"])
    main(["--file", str(store), "done", "1"])
    capsys.readouterr()

    main(["--file", str(store), "list"])
    assert "nothing to do" in capsys.readouterr().out

    main(["--file", str(store), "list", "--all"])
    assert "[x]" in capsys.readouterr().out


def test_unknown_id_exits_nonzero(tmp_path, capsys):
    store = tmp_path / "tasks.json"
    assert main(["--file", str(store), "done", "42"]) == 1
    assert "no task with id 42" in capsys.readouterr().err


def test_storage_roundtrip(tmp_path):
    store = tmp_path / "nested" / "tasks.json"
    storage.save([{"id": 1, "text": "hi", "done": False}], store)
    assert storage.load(store)[0]["text"] == "hi"
