# pytodo

A tiny command line todo list. No dependencies, tasks stored as JSON.

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```bash
pytodo add buy milk          # added 1: buy milk
pytodo add write the report
pytodo list                  # pending tasks
pytodo done 1                # mark complete
pytodo list --all            # include completed
pytodo rm 2                  # delete
```

Tasks live in `~/.pytodo.json`. Override with `--file path.json` or the
`PYTODO_FILE` environment variable.

## Development

```bash
pytest
```

Layout:

- `src/pytodo/core.py` — task operations, no I/O
- `src/pytodo/storage.py` — atomic JSON load/save
- `src/pytodo/cli.py` — argument parsing and output

## License

MIT
