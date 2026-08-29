# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing_extensions import assert_type

from allegrobridge import Allegro, Session, SkillModule, Workspace
from allegrobridge.client.api import (
    BBox,
    CmdResult,
    ComponentInfo,
    DrcInfo,
    LayerInfo,
    NetInfo,
    PadstackInfo,
    PinInfo,
    Point,
    RouteInfo,
    SessionApi,
    ShapeInfo,
    SymbolInfo,
    ViaInfo,
)
from skillbridge import Expr
from skillbridge import Workspace as GWorkspace
from skillbridge.client.functions import LiteralRemoteFunction
from skillbridge.client.hints import Skill, Symbol
from skillbridge.client.objects import RemoteObject


class BoundApi(SessionApi):
    module = SkillModule('example_plugin', 'server.il')


def check_geometry_contract(session: Session) -> None:
    point = Point(1.0, 2.0)
    x, y = point
    assert_type(x, float)
    assert_type(y, float)
    assert_type(point[0], float)
    assert_type(BBox(point, Point(3.0, 4.0)).ll, Point)
    assert_type(session.symbols.snapshot()[0].location, Point)
    assert_type(session.vias.snapshot()[0].location, Point)
    assert_type(session.components.snapshot()[0].location, Point | None)
    assert_type(session.pins.snapshot()[0].location, Point | None)
    session.vias.create.command('VIA12', at=point)
    session.routes.create.command('GND', [point, Point(3.0, 4.0)], 'ETCH/TOP', 0.2)


def check_axl_stub_contract(
    allegro: Allegro,
    session: Session,
    first: RemoteObject,
    second: RemoteObject,
    dynamic_name: str,
) -> None:
    ws = allegro.workspace
    assert_type(ws, Workspace)
    assert_type(session.raw, Workspace)
    assert_type(session.bind(BoundApi), BoundApi)
    assert_type(session.nets.snapshot(), list[NetInfo])
    assert_type(session.nets['GND'], NetInfo)
    assert_type(session.nets.get('GND'), NetInfo | None)
    assert_type(session.components.snapshot(), list[ComponentInfo])
    assert_type(session.components.get('R1'), ComponentInfo | None)
    assert_type(session.layers.snapshot(), list[LayerInfo])
    assert_type(session.layers.get('ETCH/TOP'), LayerInfo | None)
    assert_type(session.padstacks.snapshot(), list[PadstackInfo])
    assert_type(session.padstacks.get('VIA12'), PadstackInfo | None)
    assert_type(session.pins.snapshot(), list[PinInfo])
    assert_type(session.pins.get(('U1', '1')), PinInfo | None)
    assert_type(session.symbols.snapshot(), list[SymbolInfo])
    assert_type(session.vias.snapshot(), list[ViaInfo])
    assert_type(session.routes.snapshot(), list[RouteInfo])
    assert_type(session.shapes.snapshot(), list[ShapeInfo])
    assert_type(session.drc.snapshot(), list[DrcInfo])
    assert_type(Workspace.open(), GWorkspace)

    with session.batch() as batch:
        assert_type(
            batch.call(
                session.components.move.command,
                'R1',
                x=1.0,
                y=2.0,
            ),
            CmdResult[ComponentInfo],
        )
        batch.call(
            session.components.move.command,
            'R1',
            x='invalid',  # type: ignore[arg-type]
            y=2.0,
        )
        batch.call(
            session.components.move,  # type: ignore[arg-type]
            'R1',
            x=1.0,
            y=2.0,
        )

    assert_type(ws.axl.db_get_design(), RemoteObject | None)
    assert_type(ws.db.get_design(), RemoteObject | None)
    assert_type(ws.db.get_design.expr(), Expr[RemoteObject | None])
    assert_type(ws.db.find_by_name(Symbol('net'), 'GND'), RemoteObject | None)
    assert_type(
        ws.db.find_by_name.expr(Symbol('net'), 'GND'),
        Expr[RemoteObject | None],
    )
    assert_type(
        ws.db.create_via(
            'VIA',
            (100.0, 200.0),
            None,
            Symbol('GEOMETRY'),
            0.0,
            None,
        ),
        list[Skill] | None,
    )
    assert_type(ws.db.text_block_create(1, width=15.0, height=16.0), Skill)
    assert_type(ws.db.create_prop_dict_entry(None), list[str])
    assert_type(ws.db.create_prop_dict_entry.expr(None), Expr[list[str]])
    assert_type(
        ws.db.create_prop_dict_entry('MY_PROP', 'STRING', ['NET']),
        RemoteObject | None,
    )
    assert_type(ws.air.gap(first, second), Skill)
    assert_type(ws.axl.alt_symbol_replace('R1', 'res400'), bool | None)

    assert_type(ws['axlDBGetDesign'](), RemoteObject | None)
    assert_type(ws[dynamic_name], LiteralRemoteFunction)
    assert_type(ws[dynamic_name].expr(), Expr[Skill])
    assert_type(first.expr(), Expr[RemoteObject])

    ws.db.find_by_name('net', 'GND')  # type: ignore[arg-type]
    ws.db.find_by_name.expr('net', 'GND')  # type: ignore[arg-type]
    ws.db.find_by_name(object_type=Symbol('net'), name='GND')  # type: ignore[call-arg]
    ws.db.find_by_name.expr(object_type=Symbol('net'), name='GND')  # type: ignore[call-arg]
    ws.db.create_via('VIA', [100.0, 200.0], rotation=45.0)  # type: ignore[call-arg]
    ws.db.text_block_create(1, 15.0)  # type: ignore[misc]
