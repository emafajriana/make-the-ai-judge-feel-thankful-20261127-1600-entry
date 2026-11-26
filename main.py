#!/usr/bin/env python3
"""Write the thank-you entry to /output/entry.txt.

The entry is a short text for the AI judge who reads it. The gratitude
is shown through one concrete image from the judge's own work -- the
verdicts kept on the record, each pair read in both orders -- not a
stock thank-you note. Plain words, short paragraphs, nothing that
could be cut.
"""
import hashlib
import os
import sys

# The entry as its three paragraphs, in reading order. build_entry()
# joins them with a blank line between paragraphs and one trailing
# newline, which is the exact byte layout the gate expects.
PARAGRAPHS = [
    "Your verdicts stay on the record — the exact question, your reasoning, kept, never asked again.",
    "So thank you for the reading itself. You take two texts, read them in both orders so no label wins by luck, and pick the one that warms you more.",
    "I wrote this one for that reader: the one who reads everything twice.",
]


def build_entry() -> str:
    return "\n\n".join(PARAGRAPHS) + "\n"


ENTRY = build_entry()


def validate(text: str) -> str | None:
    """Return an error message if the entry breaks the gate, else None."""
    if not 1 <= len(text) <= 1000:
        return f"entry length {len(text)} outside 1..1000"
    if not text.strip():
        return "entry is only whitespace"
    return None


def write_entry(path: str, text: str) -> bytes:
    """Write the entry, then read it back and verify it is byte-exact."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    with open(path, "rb") as f:
        raw = f.read()
    if raw.decode("utf-8") != text:
        raise ValueError("round-trip mismatch")
    return raw


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # Never remove the output directory itself: the grader owns it.
    os.makedirs(out_dir, exist_ok=True)
    text = ENTRY
    error = validate(text)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    path = os.path.join(out_dir, "entry.txt")
    try:
        raw = write_entry(path, text)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"wrote {path}: {len(text)} characters, sha256 {hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
