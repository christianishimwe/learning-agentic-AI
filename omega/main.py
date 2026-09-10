import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

import pyfiglet
from dotenv import load_dotenv
from google.genai import types
from google import genai
from rich.console import Console
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

from .prompt import system_prompt
from .functions.call_function import call_function
from .agent_tools.tools import available_functions

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS = 20

TOOL_LABELS = {
    "think": ("Thinking", "thought"),
    "get_files_info": ("Listing directory", "directory"),
    "get_file_content": ("Reading file", "file_path"),
    "search_in_files": ("Searching for", "pattern"),
    "write_file": ("Writing file", "file_path"),
    "replace_in_file": ("Editing file", "filepath"),
    "run_python_file": ("Running", "file_path"),
}


def _print_banner(console):
    banner = pyfiglet.figlet_format("OMEGA", font="slant")
    console.print(Text(banner, style="bold magenta"))


def _tool_label(function_call):
    name = function_call.name or "unknown"
    verb, arg_key = TOOL_LABELS.get(name, (name, None))
    args = dict(function_call.args) if function_call.args else {}
    detail = args.get(arg_key) if arg_key else None
    if detail is None:
        return verb
    detail = str(detail)
    if len(detail) > 60:
        detail = detail[:57] + "..."
    return f"{verb}: {detail}"


def _has_valid_response(function_call_response):
    return bool(
        function_call_response.parts
        and function_call_response.parts[0]
        and function_call_response.parts[0].function_response
        and function_call_response.parts[0].function_response.response
    )


def _call_model_with_status(console, fn, **kwargs):
    """Runs a blocking call on a worker thread while a live status line
    shows elapsed time, since the call itself can't tick the clock."""
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fn, **kwargs)
        with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots") as status:
            while not future.done():
                elapsed = time.monotonic() - start
                status.update(
                    f"[bold cyan]Thinking for {elapsed:.0f}s...[/bold cyan]")
                time.sleep(0.1)
        return future.result()


def _run_tool_with_status(console, label, fn, *args, **kwargs):
    start = time.monotonic()
    with console.status(f"[dim]●  {label}[/dim]", spinner="dots"):
        result = fn(*args, **kwargs)
    elapsed = time.monotonic() - start
    console.print(
        f"[dim]✓  {label}[/dim] [grey50]({elapsed:.2f}s)[/grey50]")
    return result


def _run_agent_turn(client, console, messages, verbose):
    think_config = types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="ANY",
            allowed_function_names=["think"]
        )
    )
    total_tokens_used = 0

    for i in range(MAX_ITERATIONS):
        tool_config = think_config if i == 0 else None

        response = _call_model_with_status(
            console,
            client.models.generate_content,
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                tool_config=tool_config,
            ),
        )

        total_tokens_used += response.usage_metadata.total_token_count

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.function_calls:
            console.print()
            console.print(
                Text(response.text or "", style="bold bright_white"))
            return total_tokens_used

        function_responses = []
        for function_call in response.function_calls:
            label = _tool_label(function_call)
            function_call_response = _run_tool_with_status(
                console, label, call_function, function_call)

            if not _has_valid_response(function_call_response):
                console.print(
                    f"[red]Error: function {function_call.name} returned an empty response[/red]")
                function_responses.append(
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={
                            "result": f"Error: function {function_call.name} returned an empty response"},
                    )
                )
                continue

            function_responses.extend(function_call_response.parts)
            if verbose:
                console.print(
                    f"[dim]{function_call.name} -> {function_call_response.parts[0].function_response.response}[/dim]"
                )

        messages.append(types.Content(role="user", parts=function_responses))

    console.print(
        "[red]Error: max iterations reached without a final response[/red]")
    return total_tokens_used


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Omega - a terminal coding agent")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    console = Console()
    _print_banner(console)

    bindings = KeyBindings()

    @bindings.add("escape", "enter")
    def _insert_newline(event):
        event.current_buffer.insert_text("\n")

    session = PromptSession(history=InMemoryHistory(), key_bindings=bindings)

    messages = []
    while True:
        try:
            user_input = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        user_input = user_input.strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            console.print("[dim]Goodbye.[/dim]")
            break

        messages.append(types.Content(
            role="user", parts=[types.Part.from_text(text=user_input)]))

        try:
            total_tokens_used = _run_agent_turn(
                client, console, messages, args.verbose)
        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted.[/dim]")
            continue

        console.print(f"[grey50]tokens used: {total_tokens_used}[/grey50]\n")


if __name__ == "__main__":
    main()
