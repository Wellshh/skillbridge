# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import ast
import runpy
import sys
from pathlib import Path

import pytest

from scripts import generate_axl_stubs as generator
from scripts.generate_axl_stubs import (
    build_api_specs,
    render_report,
    render_stub,
    summarize_specs,
)

REFERENCE_ROOT = (
    Path(__file__).parents[2]
    / '.agents'
    / 'skills'
    / 'cadence-skill-agent'
    / 'skill-references'
    / 'algroskill'
)
API_NAMES_PATH = Path(__file__).parents[2] / 'allegrobridge' / 'assets' / 'api_names.txt'


def _write_sources(
    tmp_path: Path, names: list[str], documents: dict[str, str]
) -> tuple[Path, Path]:
    api_names_path = tmp_path / 'api_names.txt'
    api_names_path.write_text('\n'.join(names) + '\n', encoding='utf-8')
    reference_root = tmp_path / 'algroskill'
    reference_root.mkdir()
    for filename, content in documents.items():
        (reference_root / filename).write_text(content, encoding='utf-8')
    return api_names_path, reference_root


def test_build_api_specs_parses_documented_parameter_forms(tmp_path: Path) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlFind', 'axlCreate', 'axlKeyword'],
        {
            'apis.md': """
### axlFind

`axlFind(s_typet_name) => o_dbid/nil`

#### Description

Finds an object.

#### Arguments

| `s_type` | Type symbol.
| `t_name` | Object name.

#### Value Returned

| `o_dbid` | Object or nil.

### axlCreate

`axlCreate(t_padstack/o_padstackDbidl_anchorPoint[t_netName][g_mirror]) ⇒ l_result/nil`

#### Description

Creates an object.

#### Arguments

| `t_padstack` | Padstack name.
| `o_padstackDbid` | Padstack dbid.
| `l_anchorPoint` | Location.
| `t_netName` | Optional net.
| `g_mirror` | Optional mirror.

### axlKeyword

`axlKeyword(x_template?width f_width?lineSpace f_lineSpace) ==> x_result/nil`

#### Description

Creates a value.

#### Arguments

`x_template`
""",
        },
    )

    specs = {spec.name: spec for spec in build_api_specs(api_names_path, reference_root)}

    assert specs['axlFind'].quality == 'exact'
    assert [parameter.name for parameter in specs['axlFind'].declarations[0].parameters] == [
        's_type',
        't_name',
    ]
    create_parameters = specs['axlCreate'].declarations[0].parameters
    assert [(parameter.name, parameter.optional) for parameter in create_parameters] == [
        ('t_padstack/o_padstackDbid', False),
        ('l_anchorPoint', False),
        ('t_netName', True),
        ('g_mirror', True),
    ]
    keyword_parameters = specs['axlKeyword'].declarations[0].parameters
    assert [
        (parameter.name, parameter.value_name, parameter.kind) for parameter in keyword_parameters
    ] == [
        ('x_template', None, 'positional'),
        ('width', 'f_width', 'keyword'),
        ('lineSpace', 'f_lineSpace', 'keyword'),
    ]


def test_build_api_specs_classifies_duplicates_conflicts_and_missing_entries(
    tmp_path: Path,
) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlSame', 'axlConflict', 'axlDamaged', 'axlMissing'],
        {
            'part01.md': """
### axlSame
`axlSame() => t/nil`
#### Description
Same declaration.

### axlConflict
`axlConflict() => t/nil`
#### Description
First declaration.

### axlDamaged
`axlDifferent(t_name) => t/nil`
#### Description
Wrong function name.
""",
            'part02.md': """
### axlSame
`axlSame() => t/nil`
#### Description
Same declaration.

### axlConflict
`axlConflict(t_name) => t/nil`
#### Description
Different declaration.
#### Arguments
| `t_name` | Name.
""",
        },
    )

    specs = {spec.name: spec for spec in build_api_specs(api_names_path, reference_root)}

    assert specs['axlSame'].quality == 'exact'
    assert len(specs['axlSame'].declarations) == 1
    assert specs['axlConflict'].quality == 'conflict'
    assert specs['axlConflict'].declarations == ()
    assert specs['axlDamaged'].quality == 'fallback'
    assert specs['axlDamaged'].declarations == ()
    assert specs['axlMissing'].quality == 'missing'
    assert specs['axlMissing'].source_path is None

    report = summarize_specs(specs.values())
    assert (
        report.total,
        report.exact,
        report.fallback,
        report.conflict,
        report.missing,
        report.document_only,
    ) == (
        4,
        1,
        1,
        1,
        1,
        0,
    )


@pytest.mark.skipif(not REFERENCE_ROOT.is_dir(), reason='Cadence reference docs not available')
def test_real_allegro_references_cover_the_supported_inventory() -> None:
    specs = build_api_specs(API_NAMES_PATH, REFERENCE_ROOT)
    by_name = {spec.name: spec for spec in specs}

    assert len(specs) == 792
    assert len(by_name) == 792
    report = summarize_specs(specs)
    assert (
        report.total,
        report.exact,
        report.fallback,
        report.conflict,
        report.missing,
        report.document_only,
    ) == (
        792,
        782,
        3,
        0,
        1,
        6,
    )
    assert by_name['axlDBGetDesign'].quality == 'exact'
    assert by_name['axlDBGetDesign'].declarations[0].parameters == ()
    assert [
        parameter.name for parameter in by_name['axlDBFindByName'].declarations[0].parameters
    ] == ['s_type', 't_name']
    assert by_name['axlDBCreateVia'].source_path == 'algroskill/03dbcre8.part02.md'
    assert [
        parameter.name
        for parameter in by_name['axlDBTextBlockCreate'].declarations[0].parameters
        if parameter.kind == 'keyword'
    ] == ['width', 'height', 'lineSpace', 'charSpace', 'photoWidth']
    assert len(by_name['axlDBCreatePropDictEntry'].declarations) == 2
    assert by_name['axlAirGap'].quality == 'exact'
    assert [
        (parameter.name, parameter.optional)
        for parameter in by_name['axlAirGap'].declarations[0].parameters
    ] == [
        ('o_item1DBID', False),
        ('o_item2DBID/l_xy', False),
        ('t_layer/nil', True),
        ('s_mode', True),
    ]
    assert by_name['axlAltSymbolReplace'].quality == 'exact'
    assert by_name['axl_ol_ol2'].quality == 'missing'
    assert by_name['axlReportList'].quality == 'exact'
    assert by_name['axlPurgePadstacks'].quality == 'exact'
    assert by_name['axlSpreadsheetDoc'].quality == 'document_only'
    assert by_name['axlcreate'].quality == 'exact'
    assert by_name['axlDBCreateFilmRec'].quality == 'fallback'
    assert by_name['axlISProductStarted'].quality == 'fallback'
    assert by_name['axlIgnoreFixed'].quality == 'fallback'
    assert [
        parameter.name
        for parameter in by_name['axlAddSimpleMoveDynamics'].declarations[0].parameters
        if parameter.kind == 'positional'
    ] == ['l_origin', 'r_path', 't_type']

    document_only = {spec.name for spec in specs if spec.quality == 'document_only'}
    assert document_only == generator.DOCUMENT_ONLY_NAMES

    msg_parameters = by_name['axlMsgPut'].declarations[0].parameters
    assert [(parameter.name, parameter.kind) for parameter in msg_parameters] == [
        ('g_messageFormat', 'positional'),
        ('g_args', 'var_positional'),
    ]
    assert by_name['axlXSectionModify'].declarations[0].parameters[0].kind == 'var_keyword'

    assert [
        declaration.raw_signature for declaration in by_name['axlSetBondWireProfile'].declarations
    ] == ['axlSetBondWireProfile(bondWires profileName) => t/nil']
    assert [
        parameter.name for parameter in by_name['axlTransformObject'].declarations[0].parameters
    ] == [
        'lo_dbid/o_dbid',
        'move',
        'mirror',
        'angle',
        'origin',
        'allOrNone',
    ]


@pytest.mark.skipif(not REFERENCE_ROOT.is_dir(), reason='Cadence reference docs not available')
def test_render_stub_is_deterministic_and_excludes_document_sections() -> None:
    specs = build_api_specs(API_NAMES_PATH, REFERENCE_ROOT)

    first = render_stub(specs)
    second = render_stub(specs)

    assert first == second
    ast.parse(first)
    assert 'class _AxlDBGetDesign(LiteralRemoteFunction):' in first
    assert 'db_get_design: _AxlDBGetDesign' in first
    assert 'get_design: _AxlDBGetDesign' in first
    assert 'item: Literal["axlDBGetDesign"]' in first
    assert 'class _AxlColorDoc(' not in first
    assert 'class _AxlOlOl2(LiteralRemoteFunction):' in first
    assert generator._snake_name('is') == 'is_'
    assert '"""\n        ...' not in first


def test_build_api_specs_downgrades_malformed_declarations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    names = [
        'axlTrailing',
        'axlNoArrow',
        'axlEmptyReturn',
        'axlBadCall',
        'axlBadKeyword',
        'axlBadBracket',
        'axlBadToken',
        'axlBadSlash',
        'axlDuplicateDecl',
    ]
    api_names_path, reference_root = _write_sources(
        tmp_path,
        names,
        {
            'malformed.md': """
### axlTrailing
#### Arguments
| `t_name` | Name.

### axlNoArrow

### axlEmptyReturn

### axlBadCall

### axlBadKeyword
#### Arguments
| `t_name` | Name.

### axlBadBracket
#### Arguments
| `t_name` | Name.

### axlBadToken

### axlBadSlash

### axlDuplicateDecl
`axlDuplicateDecl() => t`
`axlDuplicateDecl() => t`
""",
        },
    )
    overrides = {
        'axlTrailing': ('axlTrailing(t_name/) => t',),
        'axlNoArrow': ('axlNoArrow()',),
        'axlEmptyReturn': ('axlEmptyReturn() =>',),
        'axlBadCall': ('axlBadCall t_name => t',),
        'axlBadKeyword': ('axlBadKeyword(t_name?width) => t',),
        'axlBadBracket': ('axlBadBracket([t_name) => t',),
        'axlBadToken': ('axlBadToken(t_name bad!) => t',),
        'axlBadSlash': ('axlBadSlash(t_name//g_value) => t',),
    }
    monkeypatch.setattr(generator, 'SIGNATURE_OVERRIDES', overrides)

    specs = build_api_specs(api_names_path, reference_root)

    assert [spec.quality for spec in specs[:-1]] == ['fallback'] * 8
    assert specs[-1].quality == 'exact'
    assert not specs[-1].description
    report = render_report(specs)
    assert 'total=9' in report
    assert 'fallback axlTrailing algroskill/malformed.md:2' in report


def test_build_api_specs_rejects_duplicate_inventory(tmp_path: Path) -> None:
    api_names_path, reference_root = _write_sources(tmp_path, ['axlSame', 'axlSame'], {})

    with pytest.raises(ValueError, match='duplicate names'):
        build_api_specs(api_names_path, reference_root)


def test_main_reports_quality_and_checks_inventory(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlOnly'],
        {'api.md': '### axlOnly\n`axlOnly() => t`\n'},
    )
    output = tmp_path / '_axl_stubs.pyi'
    args = [
        '--api-names',
        str(api_names_path),
        '--references',
        str(reference_root),
        '--output',
        str(output),
    ]

    assert generator.main(args) == 0
    assert 'total=1' in capsys.readouterr().out
    assert output.is_file()
    assert generator.main([*args, '--check']) == 1

    monkeypatch.setattr(generator, 'EXPECTED_API_COUNT', 1)
    assert generator.main([*args, '--check']) == 0
    output.write_text('stale\n', encoding='utf-8')
    assert generator.main([*args, '--check']) == 1

    monkeypatch.setattr(sys, 'argv', ['generate_axl_stubs.py', *args])
    with pytest.raises(SystemExit, match='0'):
        runpy.run_path(str(Path(generator.__file__)), run_name='__main__')
