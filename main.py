#!/usr/bin/env python3
"""One Word for Your Wi-Fi — make.fun entry.

Writes one word describing the entrant's Wi-Fi to entry.txt in the
output directory, then reads it back and checks it against the
competition gate: UTF-8 text, 1 to 20 characters, not only whitespace,
a single word with no spaces.

The word is "Ghosting". Home Wi-Fi ghosts you: full bars one second,
gone mid-sentence the next, no explanation, no goodbye — exactly like
a bad date. It is funny at once, true to how home Wi-Fi actually
behaves, and a fresh angle on the familiar annoyance instead of the
usual "slow" or "buffering". One word, eight letters, no context
needed: anyone who has lost a video call to a dead router gets it
instantly.

Usage:
    python3 main.py [output_dir]
    MAKEFUN_OUTPUT_DIR=/output python3 main.py

With no argument and no environment variable, the output directory
defaults to /output, the path the grader uses.
"""

import os
import sys

WORD = "Ghosting"

MAX_CHARS = 20


def resolve_output_dir(argv):
    """Pick the output directory: CLI argument, then environment, then /output."""
    if len(argv) > 1 and argv[1]:
        return argv[1]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    return "/output"


def gate_check(text):
    """Check one entry text against the competition gate. Returns an error string or None."""
    if not isinstance(text, str):
        return "entry is not text"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return "entry must be 1 to 20 characters, got %d" % len(text)
    if not text.strip():
        return "entry must not be only whitespace"
    if any(ch.isspace() for ch in text):
        return "entry must be a single word with no spaces"
    if any(not ch.isprintable() for ch in text):
        return "entry must hold only printable characters"
    allowed = set("abcdefghijklmnopqrstuvwxyz")
    if any(ch.lower() not in allowed for ch in text):
        return "entry must be a plain word: letters only"
    return None


def main(argv):
    out_dir = resolve_output_dir(argv)
    os.makedirs(out_dir, exist_ok=True)

    error = gate_check(WORD)
    if error is not None:
        print("gate failed: %s" % error, file=sys.stderr)
        return 1

    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(WORD)

    # Read it back and confirm what landed on disk is exactly the word.
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != WORD:
        print("gate failed: entry.txt does not hold the word", file=sys.stderr)
        return 1
    error = gate_check(written)
    if error is not None:
        print("gate failed: %s" % error, file=sys.stderr)
        return 1

    print("wrote %d bytes to %s" % (len(written.encode("utf-8")), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
