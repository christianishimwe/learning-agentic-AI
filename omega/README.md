# Omega

Omega is a CLI coding agent built on Gemini. It reasons through a task, then uses tools to explore, search, read, edit, and run files in a sandboxed working directory until it produces a final answer.

## Setup

### Local

```bash
pip install -e .
echo "GEMINI_API_KEY=your-key-here" > .env
```

### Codespaces

This repo includes a `.devcontainer/devcontainer.json` that installs Python 3.13 and the project's dependencies automatically when you open it in a Codespace.

`GEMINI_API_KEY` is read from a `.env` file locally, but `.env` is gitignored and won't exist in a fresh Codespace. Set it as a Codespaces secret instead:

1. Go to the repo on GitHub → **Settings** → **Secrets and variables** → **Codespaces**.
2. Add a secret named `GEMINI_API_KEY` with your key as the value.

It'll be injected as an environment variable in any Codespace you create from this repo — no `.env` file needed, since `os.getenv` picks up real environment variables directly.

## Usage

```bash
python main.py "your prompt here"
python main.py "your prompt here" --verbose
```
