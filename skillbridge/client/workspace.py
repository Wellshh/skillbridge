# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from __future__ import annotations

import sys
from collections.abc import Iterable
from functools import partial
from logging import getLogger
from typing import Any, NoReturn, TypeVar, cast

from .channel import Channel, DirectChannel, create_channel_class
from .expr import Expr
from .functions import FunctionCollection, LiteralRemoteFunction
from .globals import DirectGlobals, Globals
from .hints import Symbol
from .objects import RemoteObject, RemoteTable, RemoteVector
from .translator import DefaultTranslator, Translator, snake_to_camel

__all__ = ['Workspace', 'current_workspace']

WorkspaceId = str | int | None
T = TypeVar('T')
_open_workspaces: dict[tuple[type[Workspace], WorkspaceId], Workspace] = {}


logger = getLogger(__name__)


class _NoWorkspace:
    id = object()
    is_current = False

    def __getattr__(self, item: Any) -> NoReturn:
        raise RuntimeError("No Workspace made current")


_no_workspace = cast('Workspace', _NoWorkspace())
current_workspace: Workspace
current_workspace = _no_workspace


_unbound = Symbol('unbound')


class Workspace:
    abe: FunctionCollection
    abs: FunctionCollection
    adp: FunctionCollection
    adpnl: FunctionCollection
    adt: FunctionCollection
    aed: FunctionCollection
    ael: FunctionCollection
    ahdl: FunctionCollection
    alm: FunctionCollection
    amse: FunctionCollection
    anc: FunctionCollection
    ann: FunctionCollection
    ans: FunctionCollection
    ap: FunctionCollection
    apa: FunctionCollection
    arm: FunctionCollection
    art: FunctionCollection
    asi: FunctionCollection
    auLvs: FunctionCollection  # ruff: ignore[mixed-case-variable-in-class-scope]
    awv: FunctionCollection
    axl: FunctionCollection
    bnd: FunctionCollection
    cal: FunctionCollection
    cci: FunctionCollection
    ccp: FunctionCollection
    cdf: FunctionCollection
    cds: FunctionCollection
    ci: FunctionCollection
    ciw: FunctionCollection
    conn: FunctionCollection
    cpf: FunctionCollection
    cpfe: FunctionCollection
    cph: FunctionCollection
    cst: FunctionCollection
    ct: FunctionCollection
    dag: FunctionCollection
    db: FunctionCollection
    dd: FunctionCollection
    dds: FunctionCollection
    de: FunctionCollection
    deo: FunctionCollection
    dl: FunctionCollection
    dm: FunctionCollection
    dmb: FunctionCollection
    dr: FunctionCollection
    drd: FunctionCollection
    drpl: FunctionCollection
    ead: FunctionCollection
    edi: FunctionCollection
    edif: FunctionCollection
    edifin: FunctionCollection
    edifout: FunctionCollection
    elec: FunctionCollection
    env: FunctionCollection
    fam: FunctionCollection
    fnl: FunctionCollection
    gdm: FunctionCollection
    ge: FunctionCollection
    get: FunctionCollection
    gpe: FunctionCollection
    hdb: FunctionCollection
    hdl: FunctionCollection
    he: FunctionCollection
    hi: FunctionCollection
    hnl: FunctionCollection
    hsm: FunctionCollection
    icc: FunctionCollection
    idf: FunctionCollection
    imp: FunctionCollection
    ipc: FunctionCollection
    ise: FunctionCollection
    lbui: FunctionCollection
    lce: FunctionCollection
    ldtr: FunctionCollection
    le: FunctionCollection
    lm: FunctionCollection
    lmgr: FunctionCollection
    lo: FunctionCollection
    lob: FunctionCollection
    lx: FunctionCollection
    mae: FunctionCollection
    mg: FunctionCollection
    mpt: FunctionCollection
    msp: FunctionCollection
    ncl: FunctionCollection
    nl: FunctionCollection
    nmp: FunctionCollection
    nr: FunctionCollection
    ocnxl: FunctionCollection
    odc: FunctionCollection
    opc: FunctionCollection
    par: FunctionCollection
    pc: FunctionCollection
    pcdb: FunctionCollection
    pi: FunctionCollection
    pipo: FunctionCollection
    po: FunctionCollection
    ps: FunctionCollection
    pte: FunctionCollection
    rdb: FunctionCollection
    rde: FunctionCollection
    relx: FunctionCollection
    rod: FunctionCollection
    rte: FunctionCollection
    sch: FunctionCollection
    sev: FunctionCollection
    sim: FunctionCollection
    soi: FunctionCollection
    tc: FunctionCollection
    tech: FunctionCollection
    tpa: FunctionCollection
    tx: FunctionCollection
    vdr: FunctionCollection
    verif: FunctionCollection
    vfo: FunctionCollection
    vfp: FunctionCollection
    vhdl: FunctionCollection
    vhms: FunctionCollection
    via: FunctionCollection
    viva: FunctionCollection
    vms: FunctionCollection
    vos: FunctionCollection
    vpa: FunctionCollection
    vsa: FunctionCollection
    vv: FunctionCollection
    we: FunctionCollection
    xoas: FunctionCollection
    xoasis: FunctionCollection
    xpc: FunctionCollection
    xst: FunctionCollection

    def __init__(
        self,
        channel: Channel,
        id_: WorkspaceId,
        translator: Translator | None = None,
    ) -> None:
        self._id = id_
        self._channel = channel
        self._translator = translator or self._prepare_default_translator()
        self.__ = DirectGlobals(channel, self._translator)

        for cls in reversed(self.__class__.__mro__):
            for key in getattr(cls, "__annotations__", {}):
                value = FunctionCollection(channel, key, self._translator)
                setattr(self, key, value)

        self.user = FunctionCollection(channel, 'user', self._translator)

    def _prepare_default_translator(self) -> DefaultTranslator:
        translator = DefaultTranslator()
        types = [('Remote', RemoteObject), ('Table', RemoteTable), ('Vector', RemoteVector)]

        for name, typ in types:
            construct = partial(typ, self._channel, translator)
            translator.register_remote_variable_type(name, construct)

        return translator

    def make_table(self, name: str, default: Any = _unbound) -> RemoteTable:
        t = self['makeTable'](name, default)
        assert isinstance(t, RemoteTable)
        return t

    def make_vector(self, length: int, default: Any = _unbound) -> RemoteVector:
        v = self['makeVector'](length, default)
        assert isinstance(v, RemoteVector)
        return v

    def globals(self, prefix: str) -> Globals:
        return Globals(self._channel, self._translator, prefix)

    def __getitem__(self, item: str) -> LiteralRemoteFunction:
        return LiteralRemoteFunction(self._channel, item, self._translator)

    @property
    def id(self) -> WorkspaceId:
        return self._id

    @property
    def epoch(self) -> int:
        return self._channel.epoch

    def eval(self, expr: Expr[T]) -> T:
        payload = self._channel.send(expr.render())
        return cast('T', self._translator.decode(payload))

    def flush(self) -> None:
        self._channel.flush()

    def define(self, name: str, args: Iterable[str], code: str) -> None:
        code = code.replace('\n', ' ')
        skill_name = snake_to_camel(name)
        skill_name = skill_name[0].upper() + skill_name[1:]
        arg_list = ' '.join(snake_to_camel(arg) for arg in args)
        code = f'defun(user{skill_name} ({arg_list}) {code})'
        cast('Symbol', self._translator.decode(self._channel.send(code)))

    @staticmethod
    def fix_completion() -> None:
        try:
            ip = get_ipython()  # type: ignore[name-defined]
        except NameError:
            pass
        else:
            ip.Completer.use_jedi = False
            ip.Completer.greedy = True

    @classmethod
    def _create_workspace(cls, channel: Channel, workspace_id: WorkspaceId) -> Workspace:
        return cls(channel, workspace_id)

    @classmethod
    def open(
        cls,
        workspace_id: WorkspaceId = None,
        direct: bool = False,
        *,
        force_tcp: bool = False,
    ) -> Workspace:
        """
        Establish a Workspace connection

        Args:
            workspace_id: id/port to use for communication between server and client.
                (needs to be numeric and between 0 and 65535, when using TCP sockets)
            direct: use direct communication mode
            force_tcp: use TCP sockets on UNIX Systems (incompatible with ``direct``)

        Returns:
            opened workspace

        Raises:
            RuntimeError: no server was found
            ValueError: options were in conflict
        """
        if force_tcp and direct:
            raise ValueError("tcp flag in conflict with direct mode")

        if direct and not sys.stdin.isatty():
            stdout = sys.stdout
            sys.stdout = sys.stderr

            return cls._create_workspace(DirectChannel(stdout), workspace_id)

        cache_key = (cls, workspace_id)
        if cache_key not in _open_workspaces:
            try:
                channel_class = create_channel_class(force_tcp)
                channel = channel_class(workspace_id)
            except FileNotFoundError:
                raise RuntimeError("No server found. Is it running?") from None

            try:
                _open_workspaces[cache_key] = cls._create_workspace(channel, workspace_id)
            except BaseException:
                try:
                    channel.close()
                except BaseException:
                    logger.exception("Failed to close channel after workspace creation failed")
                raise
        return _open_workspaces[cache_key]

    def close(self, log_exception: bool = True) -> None:
        try:
            self._channel.close()
        except:  # ruff: ignore[bare-except]
            if log_exception:
                logger.exception("Failed to close workspace")

        for cache_key, workspace in tuple(_open_workspaces.items()):
            if workspace is self:
                _open_workspaces.pop(cache_key)

        if current_workspace.__dict__ is self.__dict__:
            current_workspace.__class__ = cast('type[Workspace]', _NoWorkspace)
            current_workspace.__dict__ = {}

    @property
    def max_transmission_length(self) -> int:
        return self._channel.max_transmission_length

    @max_transmission_length.setter
    def max_transmission_length(self, value: int) -> None:
        self._channel.max_transmission_length = value

    def try_repair(self) -> Any:
        return self._channel.try_repair()

    def make_current(self) -> Workspace:
        current_workspace.__class__ = self.__class__
        current_workspace.__dict__ = self.__dict__
        return self

    @property
    def is_current(self) -> bool:
        return current_workspace.__dict__ is self.__dict__
