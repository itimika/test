# Flet Calculator App

A responsive calculator built with [Flet](https://flet.dev/) using Decimal-based
arithmetic for reliable results. The UI fits narrow screens without wrapping and
supports AC / C / backspace / sign toggle / percent / decimal input alongside
standard operators.

## Prerequisites

- Python 3.10+
- Make
- (Optional) WSL2 or Linux shell for the provided scripts

## Setup

```bash
make venv
```

This command creates `.venv`, upgrades `pip`, and installs `flet[all]` and
`pytest`. The process also writes a pinned `requirements.txt`.

## Running the App

```bash
make dev
```

The `scripts/dev.sh` helper activates `.venv` and launches the app. By default
it attempts to serve at `http://127.0.0.1:8550`. If socket binding is restricted
in your environment, set `FLET_APP_PORT` to an available port or run
`python main.py` directly in a permissive environment.

## Tests

```bash
make test
```

Runs `pytest` against `tests/test_logic.py`, covering arithmetic precedence,
Decimal rounding (`ROUND_HALF_UP`), percent conversion, zero-division handling,
large-number formatting fallbacks, and edge-case parsing.

## Project Structure

- `main.py` – Flet entrypoint and page configuration
- `app/logic.py` – Pure calculation helpers (parsing, precedence, formatting)
- `app/state.py` – State machine managing input, chaining, memory, error states
- `app/ui.py` – UI factory wiring events to state manager
- `tests/test_logic.py` – Logic unit tests
- `scripts/` – Shell helpers for dev server and tests
- `Makefile` – Convenience targets for setup, testing, and running

## Future Enhancements

1. Enable keyboard input via `Page.on_keyboard_event`
2. Add memory buttons (MC/MR/M+/M−) to the UI and expose state feedback
3. Provide a scrollable calculation history panel
4. Offer theme toggles (dark / light)
