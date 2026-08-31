import argparse
import sys
from pathlib import Path

PAIRS = {"(": ")", "[": "]"}


def scan_string(text: str, i: int, n: int, col: int) -> tuple:
    i += 1
    col += 1
    while i < n:
        char = text[i]
        if char in '"\n':
            break
        if char == "\\" and i + 1 < n and text[i + 1] != "\n":
            i += 2
            col += 2
        else:
            i += 1
            col += 1
    closed = i < n and text[i] == '"'
    return closed, i, col


def close_bracket(errors: list, stack: list, char: str, line: int, col: int) -> None:
    if not stack:
        errors.append((line, col, f"unmatched '{char}'"))
        return
    opener, opener_line, opener_col = stack.pop()
    if PAIRS[opener] != char:
        errors.append((opener_line, opener_col, f"'{char}' closes '{opener}'"))


def lint_text(text: str) -> list:
    errors = []
    stack = []
    line, col = 1, 0
    i, n = 0, len(text)
    while i < n:
        char = text[i]
        if char == "\n":
            line += 1
            col = 0
        elif char == ";":
            i = text.find("\n", i)
            if i == -1:
                break
            continue
        else:
            col += 1
            if char == '"':
                quote_col = col
                closed, i, col = scan_string(text, i, n, col)
                if not closed:
                    errors.append((line, quote_col, "unterminated string"))
                    continue
            elif char in PAIRS:
                stack.append((char, line, col))
            elif char in ")]":
                close_bracket(errors, stack, char, line, col)
        i += 1
    for opener, opener_line, opener_col in stack:
        errors.append((opener_line, opener_col, f"unclosed '{opener}'"))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static SKILL .il syntax linter.")
    parser.add_argument("file")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    text = Path(args.file).read_text(encoding="utf-8")
    errors = lint_text(text)
    if not args.quiet:
        for line, col, message in errors:
            print(f"{args.file}:{line}:{col}: ERROR {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
