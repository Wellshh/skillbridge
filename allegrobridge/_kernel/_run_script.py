from __future__ import annotations

import sys
from runpy import run_path


def main() -> None:
    script = sys.argv[1]
    sys.argv[:] = sys.argv[1:]
    run_path(script, run_name='__main__')


if __name__ == '__main__':
    main()
