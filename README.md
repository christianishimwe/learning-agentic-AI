# Omega

> 🎥 **[Watch the demo on Loom](https://www.loom.com/share/dd561cab437c42929b0050cbd41d6945)**

Omega is a terminal coding agent built on Gemini. Launch it with `omega` and you're dropped into an interactive session — type instructions directly at the prompt and it reasons through the task, using tools to explore, search, read, edit, and run files in a sandboxed working directory until it produces an answer.

## Setup

Clone the repo:

```bash
git clone https://github.com/christianishimwe/Omega.git
cd Omega/omega
```

Create a `.env` file with your Gemini API key and the max characters a file read can return:

```bash
echo -e "GEMINI_API_KEY=your-key-here\nMAX_CHARS=10000" > .env
```

Build and run the container:

```bash
docker compose build
docker compose run --rm omega
```

This mounts `../omega_working_directory` into the container as the agent's sandbox, so any files it creates or edits show up directly in your local repo.

## Usage

`docker compose run --rm omega` drops you into an interactive prompt. Type your instruction and press Enter to send it; press `Alt+Enter` (or `Esc` then `Enter`) to insert a newline for multi-line input. Use the up/down arrows to browse command history. Type `exit`, `quit`, or press `Ctrl+C` at the prompt to leave.

Pass `--verbose` to also print each tool call's raw response:

```bash
docker compose run --rm omega --verbose
```
