# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path

here = Path(__file__).parent.resolve()


def print_skill_script_locations() -> None:
    python_server = (here / '_kernel' / 'server' / 'python_server.il').resolve()
    allegro_server = (here / 'server' / 'allegro_server.il').resolve()

    print('Type this into the Allegro SKILL console:')
    print(f'load("{python_server.as_posix()}")')
    print(f'load("{allegro_server.as_posix()}")')


def main(argv: Sequence[str] | None = None) -> None:
    parser = ArgumentParser(
        'allegrobridge',
        description='CLI utility for the allegrobridge management commands',
    )
    sub = parser.add_subparsers(title='commands', dest='command')
    sub.add_parser('path', help='show the load instructions for the SKILL server scripts')
    args = parser.parse_args(argv)

    if args.command == 'path':
        print_skill_script_locations()
    else:
        parser.print_help()


if __name__ == '__main__':  # pragma: no cover
    main()
