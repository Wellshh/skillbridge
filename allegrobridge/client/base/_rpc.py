# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import update_wrapper, wraps
from inspect import signature
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    Literal,
    TypeAlias,
    TypeVar,
    overload,
)
from weakref import ref

from pydantic import TypeAdapter
from typing_extensions import ParamSpec, Self

from allegrobridge._kernel.client.hints import Skill, SkillCode
from allegrobridge.client.base._future import Cmd, CmdResult, _validate
from allegrobridge.client.base._record import _ID
from allegrobridge.exceptions import AllegroProtocolError

if TYPE_CHECKING:  # pragma: no cover
    from allegrobridge.client.session.session import Session

RpcArgs: TypeAlias = tuple[Skill, ...]

P = ParamSpec('P')
T = TypeVar('T')
ApiT = TypeVar('ApiT', bound='SessionApi')


@dataclass(frozen=True, slots=True)
class RpcDef:
    kind: Literal['read', 'direct', 'write']
    proc: str


@dataclass(frozen=True)
class SessionApi:
    _session: Session


_CORE_APIS: list[type[SessionApi]] = []


# Note: Procedures registered via @_core_api are collected into `Workspace._ensure_core_runtime()`
# and verified on every Workspace connection. Only mark procedures that are strictly
# essential for basic sessions here. Heavy or optional domain APIs should use lazy loading.
def _core_api(api: type[ApiT]) -> type[ApiT]:
    """Register a built-in API class and its underlying SKILL procedures."""
    if api not in _CORE_APIS:
        _CORE_APIS.append(api)
    return api


def _api_procedures(api: type[SessionApi]) -> tuple[str, ...]:
    # Collect visible SKILL procedures declared across the API's MRO.
    visible: dict[str, object] = {}
    for base in api.__mro__:
        for name, member in vars(base).items():
            visible.setdefault(name, member)
    return tuple(
        dict.fromkeys(
            spec.proc
            for member in visible.values()
            if isinstance(spec := getattr(member, 'spec', None), RpcDef)
        )
    )


def _core_procedures() -> tuple[str, ...]:
    return tuple(dict.fromkeys(proc for api in _CORE_APIS for proc in _api_procedures(api)))


class Batch:
    def __init__(
        self,
        session: Session,
        description: str = '',
        *,
        dry_run: bool = False,
    ) -> None:
        self.description = description
        self.dry_run = dry_run
        self._session = session
        self._id = _ID(ref(session), session.generation)
        self._cmds: list[Cmd[Any]] = []
        self._results: list[CmdResult[Any]] = []
        self._active = False
        self._used = False

    def __enter__(self) -> Self:
        if self._used:
            raise RuntimeError('batch was already used')
        self._used = True
        self._active = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._active = False
        if exc_value is not None:
            self._fail(exc_value)
            return
        try:
            self._execute()
        except BaseException as error:
            self._fail(error)
            raise

    def add(self, cmd: Cmd[T]) -> CmdResult[T]:
        if not self._active:
            raise RuntimeError('batch is not active')
        self._check_id()
        cmd._check_id(self._session)
        result = CmdResult[T]()
        self._cmds.append(cmd)
        self._results.append(result)
        return result

    @overload
    def call(
        self,
        operation: Callable[P, Cmd[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> CmdResult[T]: ...

    @overload
    def call(
        self,
        operation: _BoundWrite[ApiT, P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> CmdResult[T]: ...

    def call(self, operation: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(operation, _BoundWrite):
            return self.add(operation.command(*args, **kwargs))
        return self.add(operation(*args, **kwargs))

    def _execute(self) -> None:
        if not self._cmds:
            return
        self._check_id()
        expr = self._compile()
        transaction = self._session.workspace.transaction
        payload = transaction.preview(expr) if self.dry_run else transaction(expr)
        # catch Session.refresh()
        self._check_id()
        if not isinstance(payload, list) or len(payload) != len(self._cmds):
            raise AllegroProtocolError('batch returned an invalid payload')
        values = [cmd._validate(item) for cmd, item in zip(self._cmds, payload, strict=True)]
        for result, value in zip(self._results, values, strict=True):
            result._resolve(value)

    def _compile(self) -> SkillCode:
        operations = ' '.join(f'results = cons({cmd.expr} results)' for cmd in self._cmds)
        return SkillCode(f'let((results) progn({operations} reverse(results)))')

    def _fail(self, error: BaseException) -> None:
        for result in self._results:
            result._fail(error)

    def _check_id(self) -> None:
        self._id.check(self._session, 'Batch')


def read(
    proc: str,
    adapter: TypeAdapter[T],
) -> Callable[
    [Callable[Concatenate[ApiT, P], RpcArgs]],
    Callable[Concatenate[ApiT, P], T],
]:
    """Decorate a read-only API method to query SKILL and validate the returned payload."""
    return _rpc('read', proc, adapter)


def _rpc(
    kind: Literal['read', 'direct'],
    proc: str,
    adapter: TypeAdapter[T],
) -> Callable[
    [Callable[Concatenate[ApiT, P], RpcArgs]],
    Callable[Concatenate[ApiT, P], T],
]:
    spec = RpcDef(kind, proc)

    def decorate(
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
    ) -> Callable[Concatenate[ApiT, P], T]:
        @wraps(build_args)
        def call(self: ApiT, *args: P.args, **kwargs: P.kwargs) -> T:
            rpc_args = build_args(self, *args, **kwargs)
            payload = self._session.workspace[proc](*rpc_args)
            return _validate(
                payload,
                adapter,
                self._session,
                proc,
            )

        call.spec = spec  # type: ignore[attr-defined]
        return call

    return decorate


def direct(
    proc: str,
    adapter: TypeAdapter[T],
) -> Callable[
    [Callable[Concatenate[ApiT, P], RpcArgs]],
    Callable[Concatenate[ApiT, P], T],
]:
    """Decorate an immediate RPC operation without transaction affordances."""
    return _rpc('direct', proc, adapter)


#  ------------------ Descriptor pattern for transactional write operations ---------------------
# - `_Write`: Unbound class descriptor holding static RPC metadata and argument builder.
# - `_BoundWrite`: Instance-bound callable providing direct call, `.preview()`, and `.command()`.


class _BoundWrite(Generic[ApiT, P, T]):
    def __init__(self, operation: _Write[ApiT, P, T], instance: ApiT) -> None:
        self._operation = operation
        self._instance = instance
        update_wrapper(self, operation.declaration)
        self.spec = operation.spec
        declared = signature(operation.declaration)
        self.__signature__ = declared.replace(parameters=list(declared.parameters.values())[1:])

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.command(*args, **kwargs)._execute()

    def preview(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.command(*args, **kwargs)._execute(preview=True)

    def command(self, *args: P.args, **kwargs: P.kwargs) -> Cmd[T]:
        return self._operation.command(self._instance, *args, **kwargs)


class _Write(Generic[ApiT, P, T]):
    def __init__(
        self,
        proc: str,
        adapter: TypeAdapter[T],
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
    ) -> None:
        self.spec = RpcDef('write', proc)
        self._adapter = adapter
        self._build_args = build_args

    @property
    def declaration(self) -> Callable[Concatenate[ApiT, P], RpcArgs]:
        return self._build_args

    def command(
        self,
        instance: ApiT,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Cmd[T]:
        rpc_args = self._build_args(instance, *args, **kwargs)
        expr = instance._session.workspace[self.spec.proc].expr(*rpc_args).render()
        return Cmd(
            instance._session,
            expr,
            self.spec.proc,
            self._adapter,
        )

    @overload
    def __get__(
        self,
        instance: None,
        owner: type[ApiT],
    ) -> _Write[ApiT, P, T]: ...

    @overload
    def __get__(
        self,
        instance: ApiT,
        owner: type[ApiT] | None,
    ) -> _BoundWrite[ApiT, P, T]: ...

    def __get__(
        self,
        instance: ApiT | None,
        owner: type[ApiT] | None,
    ) -> object:
        if instance is None:
            return self
        return _BoundWrite(self, instance)


def write(
    proc: str,
    adapter: TypeAdapter[T],
) -> Callable[
    [Callable[Concatenate[ApiT, P], RpcArgs]],
    _Write[ApiT, P, T],
]:
    """Decorate a state-modifying API method to support execution, dry-run, and batching."""

    def decorate(
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
    ) -> _Write[ApiT, P, T]:
        return _Write(proc, adapter, build_args)

    return decorate
