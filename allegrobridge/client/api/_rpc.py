from __future__ import annotations

from dataclasses import dataclass
from functools import update_wrapper, wraps
from inspect import signature
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Generic, Tuple, TypeVar, cast, overload

from pydantic import TypeAdapter, ValidationError
from typing_extensions import Concatenate, ParamSpec, Self, TypeAlias

from allegrobridge.exceptions import AllegroProtocolError
from skillbridge.client.hints import Skill, SkillCode

if TYPE_CHECKING:  # pragma: no cover
    from allegrobridge.client.session.session import Session

RpcArgs: TypeAlias = Tuple[Skill, ...]

P = ParamSpec('P')
T = TypeVar('T')
ApiT = TypeVar('ApiT', bound='SessionApi')
_CORE_PROCEDURES: list[str] = []


@dataclass(frozen=True)
class SessionApi:
    _session: Session


def core_api(api: type[ApiT]) -> type[ApiT]:
    """Register an API class and its underlying SKILL procedures as core extensions."""
    for member in vars(api).values():
        procedure = getattr(member, 'procedure', None)
        if isinstance(procedure, str) and procedure not in _CORE_PROCEDURES:
            _CORE_PROCEDURES.append(procedure)
    return api


def _core_procedures() -> tuple[str, ...]:
    return tuple(_CORE_PROCEDURES)


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
        return self._validate(payload)

    def _validate(self, payload: object) -> T:
        return _validate(
            payload,
            self._adapter,
            self._session,
            self.procedure,
            none_as_empty=self._none_as_empty,
        )


_PENDING = object()


class CommandResult(Generic[T]):
    def __init__(self) -> None:
        self._value: object = _PENDING
        self._error: BaseException | None = None

    @property
    def value(self) -> T:
        if self._error is not None:
            raise self._error
        if self._value is _PENDING:
            raise RuntimeError('batch result is pending')
        return cast('T', self._value)

    def _resolve(self, value: T) -> None:
        self._value = value

    def _fail(self, error: BaseException) -> None:
        self._error = error


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
        self._commands: list[Command[Any]] = []
        self._results: list[CommandResult[Any]] = []
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

    def add(self, command: Command[T]) -> CommandResult[T]:
        if not self._active:
            raise RuntimeError('batch is not active')
        if command._session is not self._session:
            raise ValueError('command belongs to another Session')
        result = CommandResult[T]()
        self._commands.append(command)
        self._results.append(result)
        return result

    def _execute(self) -> None:
        if not self._commands:
            return
        expression = self._compile()
        transaction = self._session.raw.transaction
        payload = transaction.preview(expression) if self.dry_run else transaction(expression)
        if not isinstance(payload, list) or len(payload) != len(self._commands):
            raise AllegroProtocolError('batch returned an invalid payload')
        values = [command._validate(item) for command, item in zip(self._commands, payload)]
        for result, value in zip(self._results, values):
            result._resolve(value)

    def _compile(self) -> SkillCode:
        operations = ' '.join(
            f'results = cons({command.expression} results)' for command in self._commands
        )
        return SkillCode(f'let((results) progn({operations} reverse(results)))')

    def _fail(self, error: BaseException) -> None:
        for result in self._results:
            result._fail(error)


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
    """Decorate a read-only API method to query SKILL and validate the returned payload."""

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

        call.procedure = procedure  # type: ignore[attr-defined]
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
    """Decorate a state-modifying API method to support execution, dry-run, and batching."""

    def decorate(
        build_args: Callable[Concatenate[ApiT, P], RpcArgs],
    ) -> _Write[ApiT, P, T]:
        return _Write(procedure, adapter, build_args, none_as_empty)

    return decorate
