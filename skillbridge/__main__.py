from __future__ import annotations

from argparse import ArgumentParser
from code import interact
from pathlib import Path
from random import randrange
from typing import Any, Callable

from . import generate_static_completion

here = Path(__file__).parent.resolve()


def print_skill_script_location() -> None:
    skill_source = here / 'server' / 'python_server.il'

    print("Path to Skill server script:")
    print(skill_source)

    print()

    print("Type this into the Skill console:")
    print(f'load("{skill_source}")')


def shell_command(ws_id: str | None, ping: bool, force_tcp: bool) -> None:
    import skillbridge  # ruff: ignore[import-outside-top-level]

    variables = {name: getattr(skillbridge, name) for name in dir(skillbridge)}
    ws = skillbridge.Workspace.open(ws_id, force_tcp=force_tcp)
    variables['ws'] = ws

    if ping:
        x = randrange(1000)
        y = randrange(1000)

        assert ws['plus'](x, y) == x + y, "simple command failed"

    interact("Interactive Python interpreter with skillbridge Workspace `ws`", local=variables)


def main() -> None:
    parser = ArgumentParser(
        'skillbridge',
        description="""
        CLI utility for the various skillbridge management commands
        """,
    )

    sub = parser.add_subparsers(title='commands', dest='command')

    shell = sub.add_parser('shell', help="opens a python interpreter with a connected workspace")
    shell.add_argument('-i', '--id', help="id used to open the workspace", default=None)
    shell.add_argument('--force-tcp', help="force the use of tcp sockets", action='store_true')
    shell.add_argument(
        '-p',
        '--ping',
        help="ping the server and quit if it does not respond",
        action='store_true',
    )
    path = sub.add_parser('path', help="show the path to the skill script")
    generate = sub.add_parser('generate', help="generate static completion file")
    args = parser.parse_args()

    commands: dict[str | None, tuple[Any, Callable[[], None]]] = {
        None: (parser, parser.print_help),
        'path': (path, print_skill_script_location),
        'generate': (generate, generate_static_completion),
        'shell': (shell, lambda: shell_command(args.id, args.ping, args.force_tcp)),
    }

    sub_parser, func = commands[args.command]
    try:
        func()
    except RuntimeError as e:  # pragma: no cover
        sub_parser.error(str(e))


if __name__ == '__main__':  # pragma: no cover
    main()
