from __future__ import annotations

from dataclasses import dataclass
from functools import update_wrapper, wraps
from inspect import signature
from typing import TYPE_CHECKING, Callable, Generic, Tuple, TypeVar, overload

from pydantic import TypeAdapter, ValidationError
from typing_extensions import Concatenate, ParamSpec, TypeAlias

from allegrobridge.client.api._record import AllegroProtocolError
from skillbridge.client.hints import Skill, SkillCode

if TYPE_CHECKING:  # pragma: no cover
    from allegrobridge.client.session.session import Session

RpcArgs: TypeAlias = Tuple[Skill, ...]

P = ParamSpec('P')
T = TypeVar('T')
ApiT = TypeVar('ApiT', bound='SessionApi')


@dataclass(frozen=True)
class SessionApi:
    _session: Session


@dataclass(frozen=True)
class Command(Generic[T]):
    _session: Session
    expression: SkillCode
    procedure: str
    _adapter: TypeAdapter[T]
    _none_as_empty: bool = False

    def _execute(self, *, preview: bool = False) -> T:
        transaction = self._session.raw.transaction
        payload = transaction.preview(self.expression) if preview else transaction(self.expression)
        return _validate(
            payload,
            self._adapter,
            self._session,
            self.procedure,
            none_as_empty=self._none_as_empty,
        )


def _validate(
    payload: object,
    adapter: TypeAdapter[T],
    session: Session,
    procedure: str,
    *,
    none_as_empty: bool = False,
) -> T:
    if payload is None and none_as_empty:
        payload = []
    if isinstance(payload, dict):
        payload = {**payload, 'session_generation': session.generation}
    elif isinstance(payload, list):
        payload = [
            {**item, 'session_generation': session.generation} if isinstance(item, dict) else item
            for item in payload
        ]
    try:
        return adapter.validate_python(payload, strict=True)
    except ValidationError as error:
        raise AllegroProtocolError(f'{procedure} returned an invalid payload') from error


def read(
    procedure: str,
    adapter: TypeAdapter[T],
    *,
    none_as_empty: bool = False,
) -> Callable[
    [Callable[Concatenate[ApiT, P], RpcArgs]],
    Callable[Concatenate[ApiT, P], T],
]:
    def decorate(
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
    ) -> Callable[Concatenate[ApiT, P], T]:
        @wraps(build_args)
        def call(self: ApiT, *args: P.args, **kwargs: P.kwargs) -> T:
            rpc_args = build_args(self, *args, **kwargs)
            payload = self._session.raw[procedure](*rpc_args)
            return _validate(
                payload,
                adapter,
                self._session,
                procedure,
                none_as_empty=none_as_empty,
            )

        return call

    return decorate


class _BoundWrite(Generic[ApiT, P, T]):
    def __init__(self, operation: _Write[ApiT, P, T], instance: ApiT) -> None:
        self._operation = operation
        self._instance = instance
        update_wrapper(self, operation.declaration)
        declared = signature(operation.declaration)
        self.__signature__ = declared.replace(parameters=list(declared.parameters.values())[1:])

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.command(*args, **kwargs)._execute()

    def preview(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.command(*args, **kwargs)._execute(preview=True)

    def command(self, *args: P.args, **kwargs: P.kwargs) -> Command[T]:
        return self._operation.command(self._instance, *args, **kwargs)


class _Write(Generic[ApiT, P, T]):
    def __init__(
        self,
        procedure: str,
        adapter: TypeAdapter[T],
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
        none_as_empty: bool,
    ) -> None:
        self.procedure = procedure
        self._adapter = adapter
        self._build_args = build_args
        self._none_as_empty = none_as_empty

    @property
    def declaration(self) -> Callable[Concatenate[ApiT, P], RpcArgs]:
        return self._build_args

    def command(
        self,
        instance: ApiT,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Command[T]:
        rpc_args = self._build_args(instance, *args, **kwargs)
        expression = instance._session.raw[self.procedure].lazy(*rpc_args)
        return Command(
            instance._session,
            expression,
            self.procedure,
            self._adapter,
            self._none_as_empty,
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
    procedure: str,
    adapter: TypeAdapter[T],
    *,
    none_as_empty: bool = False,
) -> Callable[
    [Callable[Concatenate[ApiT, P], RpcArgs]],
    _Write[ApiT, P, T],
]:
    def decorate(
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
    ) -> _Write[ApiT, P, T]:
        return _Write(procedure, adapter, build_args, none_as_empty)

    return decorate
