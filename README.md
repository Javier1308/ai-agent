# AI Agent

A command-line AI coding agent built on Google's Gemini API. Give it a natural-language task and it plans, calls tools to inspect and modify files in a sandboxed working directory, and iterates until it has a final answer — all from your terminal.

Built as part of the [Boot.dev](https://boot.dev) "Build an AI Agent" course.

## How it works

The agent runs an iterative function-calling loop:

1. Your prompt is sent to Gemini (`gemini-2.5-flash`) along with a system prompt and a set of available tools.
2. If the model responds with plain text, that's the final answer — printed and done.
3. If the model requests one or more tool calls, the agent executes them locally, feeds the results back into the conversation, and loops again so the model can react to what it learned.
4. The loop is capped (default: 20 iterations) so a confused agent can't spin forever burning tokens.

## Tools available to the agent

All tools operate relative to a sandboxed working directory — the agent can't read or write outside of it.

| Tool | Description |
|---|---|
| `get_files_info` | Lists files/directories with size and type info |
| `get_file_content` | Reads a file's contents (truncated to `MAX_CHARS`) |
| `write_file` | Writes/overwrites a file |
| `run_python_file` | Executes a Python file with optional CLI args, returns stdout/stderr |

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file in the project root with a [Gemini API key](https://aistudio.google.com/apikey):

```
GEMINI_API_KEY=your-key-here
```

## Usage

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to see token usage and each tool call/result:

```bash
uv run main.py "Explain how the calculator renders the result to the console." --verbose
```

## Project structure

```
main.py              # entry point: agent loop
call_function.py      # dispatches model tool-call requests to the actual functions
prompts.py            # system prompt
config.py             # shared constants (e.g. MAX_CHARS)
functions/             # the tools exposed to the model
calculator/            # sample project used as the agent's sandboxed working directory
```

## Running tests

```bash
uv run pytest
```
