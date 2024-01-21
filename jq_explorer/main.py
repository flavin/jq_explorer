#!/usr/bin/env python3
import argparse
import os
import readline
import subprocess
import sys
import tempfile
import json

from pygments import highlight, lexers, formatters

EMPTY_MESSAGE = "(EMPTY)"
INVALID_INPUT_MESSAGE = "Invalid input"
NO_INPUT_MESSAGE = "No input"
QUIT_COMMAND = "q"

cache = {}


def process_response(response, jq_string, args):
    processed_output = None
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(response)
    try:
        args = ' '.join(args)
        processed_output = subprocess.check_output(
            f"jq {args} '{jq_string}' {f.name}", shell=True
        )
    except subprocess.CalledProcessError as error:
        print(f"Command '{error.cmd}' returned non-zero exit status {error.returncode}.")
        print(f"Command output: {error.output}")
    finally:
        os.unlink(f.name)  # ensure the temporary file is deleted
    return processed_output.decode() if processed_output else None


def handle_input(label, prev_value=""):
    readline.set_startup_hook(
        lambda: readline.insert_text(prev_value if prev_value else "")
    )
    try:
        result = input(label)
    finally:
        readline.set_startup_hook()
    return result


def highlight_output(output, lexer):
    return highlight(output, lexer, formatters.TerminalFormatter())


def get_jq_command():
    if cache.get("last_jq") is not None:
        print("Latest jq: ", cache.get("last_jq", "None"))
    jq_string = handle_input(
        "Enter jq string to handle the output: ", cache.get("last_jq")
    )
    cache["last_jq"] = jq_string
    return jq_string


def handle_response(response, args):
    while True:
        jq_string = get_jq_command()
        if jq_string == QUIT_COMMAND:
            break

        processed_output = process_response(response, jq_string, args)
        if processed_output is None:
            print(EMPTY_MESSAGE)
            continue

        try:
            json.loads(processed_output)
            lexer = lexers.JsonLexer()
        except (json.decoder.JSONDecodeError, TypeError):
            lexer = lexers.HtmlLexer()

        print(highlight_output(processed_output, lexer))


def make_available_the_user_input():
    sys.stdin.close()
    sys.stdin = os.fdopen(1)


def main():
    response = sys.stdin.read().strip()  # read the data from the pipe

    if not response:
        print(NO_INPUT_MESSAGE)
        return

    parser = argparse.ArgumentParser()
    args, unknown = parser.parse_known_args()

    make_available_the_user_input()
    handle_response(response, unknown if unknown else ['-r'])


if __name__ == "__main__":
    main()
