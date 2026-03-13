# mini-claude-code

A terminal-based AI coding agent powered by the Gemini API. Point it at a codebase and ask it questions, debug issues, or make changes — it will explore the code, reason about it, and take action autonomously.

## What it does

- Lists and reads files in a working directory
- Writes and modifies files
- Runs Python files and inspects output
- Iterates autonomously using a tool-calling loop until it has a final answer

## Project structure
```
mini-claude-code/
├── main.py                         # Entry point and agent loop
├── prompts.py                      # System prompt versions
├── config.py                       # Configuration (e.g. MAX_CHARS)
├── functions/
│   ├── get_files_info.py           # List files in a directory
│   ├── get_file_content.py         # Read file contents
│   ├── write_file.py               # Write or overwrite a file
│   ├── run_python_file.py          # Execute a Python file
│   └── genai/
│       └── call_function.py        # Tool dispatcher and schema registry
├── calculator/                     # Sample codebase the agent works on
│   ├── main.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── test_get_file_content.py
├── test_get_files_info.py
├── test_run_python_file.py
└── test_write_file.py
```

## Setup

**Prerequisites:** Python 3.12+, [uv](https://github.com/astral-sh/uv)

1. Clone the repo and install dependencies:
```bash
git clone <repo-url>
cd mini-claude-code
uv sync
```

2. Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```
```
GEMINI_API_KEY=your_key_here
```

Get a key at [aistudio.google.com](https://aistudio.google.com).

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

## Usage
```bash
uv run main.py "<your question or instruction>"
```

**Examples:**
```bash
uv run main.py "how does the calculator render results to the console?"
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20"
uv run main.py "Add input validation to the calculator" --verbose
```

**Flags:**
- `--verbose` — prints token usage and raw function responses each iteration
- `--system v1|v2` — choose which system prompt to use (default: `v2`)

## Limitations

Currently the agent is hardcoded to work on the `calculator/` directory. To use it on a different codebase, update the `working_directory` value in `functions/genai/call_function.py` and add the codebase you want to work on inside this directory. A `--working-dir` CLI flag to make this configurable at runtime is planned.

## Rate limits

The free tier of the Gemini API allows 5 requests per minute and 20 per day on `gemini-2.5-flash`. The agent handles rate limit errors automatically by waiting and retrying. For heavier use, add billing at [aistudio.google.com](https://aistudio.google.com).

## Running tests
```bash
uv run pytest
```