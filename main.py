#!/usr/bin/env python3
"""The 3AM Fridge Text entry for make.fun bounty
u-deysumbrella-the-3am-fridge-text-4c3e721d.

Writes one line of text (at most 140 characters) to
/output/entry.txt: the message a smart fridge sends its
owner at 3am. Standard library only, no network, no input
files: everything the program writes is in this file.
"""

import os
import sys

# The text: a fridge that has been awake all night, keeping
# count, and finally deciding this is the moment to speak.
# Fresh angle: not the milk, the ice or a door left open --
# the owner keeps opening the fridge and taking nothing, so
# the fridge calls out the shared loneliness instead.
TEXT = (
    "Hey. It's 3am. I counted: you've opened me four times "
    "and taken nothing. We're both just lonely, huh?"
)

MAX_CHARS = 140


def validate(text):
    """The gate accepts UTF-8 text of 1 to 140 characters."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("text must not be only whitespace")
    if len(stripped) > MAX_CHARS:
        raise ValueError(
            "text is %d characters, over the %d limit"
            % (len(stripped), MAX_CHARS)
        )
    # One line: a text message has no line breaks in it.
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("text must be a single line")
    return stripped


def output_path():
    """The grader sets MAKEFUN_OUTPUT_DIR; default is /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def verify_output(path, expected):
    """Re-read what was written and fail loudly if it is not the
    validated text: must decode as UTF-8, be one line, 1-140 chars,
    and match the text we meant to write."""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        written = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("output is not valid UTF-8: %s" % exc)
    if written != expected:
        raise ValueError("output does not match the validated text")
    if not 1 <= len(written) <= MAX_CHARS:
        raise ValueError(
            "output is %d characters, outside the 1-%d range"
            % (len(written), MAX_CHARS)
        )
    if "\n" in written or "\r" in written:
        raise ValueError("output must be a single line")


def main():
    text = validate(TEXT)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    verify_output(path, text)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
