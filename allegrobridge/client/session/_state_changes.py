# Portions of the transition protocol are adapted from SQLAlchemy's
# ``lib/sqlalchemy/orm/state_changes.py``. SQLAlchemy is distributed under
# the MIT License; retain the upstream attribution when redistributing this file.


"""State trakcing utilities.

This is adapted from @sqlalchemy: orm/state_changes.py session managment.
"""

from __future__ import annotations

import threading
from enum import Enum, auto
from typing import Any, Callable


class _State(Enum):
    "Base enum for lifecycle states and internal transition signals."


class _States(_State):
    ANY = auto()
    NO_CHANGE = auto()
    CHANGE_IN_PROGRESS = auto()


class _StateChange:
    """Validate and serialize lifecylce-changing method calls.

    Subclass must:
    1. assign ``self._state`` to one of their own ``_State`` enums;
    2. call :meth:`_init_state_change` during ``__init__``;
    3. set ``self._state`` explicitly on every successful or exceptional path
       whose outcome changes lifecycle state.
    """

    _state: _State
    _next_state: _State = _States.ANY

    _cur_fn: Callable[..., Any] | None = None

    _lock: threading.RLock

    def _init_state_change(
        self,
        *,
        lock: threading.RLock | None = None,
    ) -> None:
        # initialize all control fields explicitly so ownership
        # is unambigous and a single lock could be shared with
        # the subclass's existing lifecyle lock (that's why we use RLock).

        self._next_state = _States.ANY
        self._cur_fn = None
        self._lock = lock if lock is not None else threading.RLock()
