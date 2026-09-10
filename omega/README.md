# Omega

Omega is a terminal coding agent built on Gemini. Launch it with `omega` and you're dropped into an interactive session — type instructions directly at the prompt and it reasons through the task, using tools to explore, search, read, edit, and run files in a sandboxed working directory until it produces an answer.

## Setup

### Local

```bash
pip install -e .
echo -e "GEMINI_API_KEY=your-key-here\nMAX_CHARS=10000" > .env
```

This installs Omega in editable mode and registers the `omega` command globally (via `console_scripts` in `pyproject.toml`), so it works from any directory. The `.env` file lives in the repo root and is found automatically regardless of where you run `omega` from.

For a cleaner global install that isolates Omega's dependencies from your other Python projects, use [pipx](https://pipx.pypa.io/) instead:

```bash
pipx install .
```

Note: `pipx install .` performs a non-editable install, so it only works reliably if you've already set `GEMINI_API_KEY` (and `MAX_CHARS`) as real environment variables rather than relying on the repo's `.env` file. Prefer `pip install -e .` for local development.

### Codespaces

This repo includes a `.devcontainer/devcontainer.json` that installs Python 3.13 and the project's dependencies automatically when you open it in a Codespace.

`GEMINI_API_KEY` is read from a `.env` file locally, but `.env` is gitignored and won't exist in a fresh Codespace. Set it as a Codespaces secret instead:

1. Go to the repo on GitHub → **Settings** → **Secrets and variables** → **Codespaces**.
2. Add a secret named `GEMINI_API_KEY` with your key as the value.

It'll be injected as an environment variable in any Codespace you create from this repo — no `.env` file needed, since `os.getenv` picks up real environment variables directly.

## Usage

```bash
omega
```

This drops you into an interactive prompt. Type your instruction and press Enter to send it; press `Alt+Enter` (or `Esc` then `Enter`) to insert a newline for multi-line input. Use the up/down arrows to browse command history. Type `exit`, `quit`, or press `Ctrl+C` at the prompt to leave.

Pass `--verbose` to also print each tool call's raw response:

```bash
omega --verbose
```
