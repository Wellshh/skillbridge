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
    ArgumentDoc,
    ExampleSegment,
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


def test_build_api_specs_parses_full_document_sections(tmp_path: Path) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlRich', 'axlPlain'],
        {
            'apis.md': """
### axlRich

`axlRich(t_padstack l_anchorPoint [t_netName]) => l_result/nil`

#### Description

Creates a via in the layout. The via is added to the
database immediately.

Mirroring applies before rotation.

#### Arguments

|  |
| --- | ---
| `t_padstack` | Padstack name. Searched in the libraries
| specified by PADPATH when missing.
| `l_anchorPoint` | Layout coordinates.
| `t_netName` | Net name; `nil` → stand-alone.

#### Value Returned

|  |
| --- | ---
| `l_result` | List: (`car`) dbid of the via. (`cadr`) `t` if DRCs are created.
| `nil` | Nothing is created.

#### Note

Testpoints need a dedicated function.

#### Example

> ```
> myvia = axlRich("pad1", 5600:4200, "sclkl")    ⇒ (dbid:526745 nil)
> ```

Adds a standalone via.

### axlPlain

`axlPlain() => t/nil`

#### Description

Does nothing.

#### Arguments

None.
""",
        },
    )

    specs = {spec.name: spec for spec in build_api_specs(api_names_path, reference_root)}

    rich = specs['axlRich']
    assert rich.quality == 'exact'
    assert rich.doc.description == (
        ('Creates a via in the layout. The via is added to the database immediately.',),
        ('Mirroring applies before rotation.',),
    )
    assert rich.doc.arguments == (
        ArgumentDoc(
            't_padstack',
            'Padstack name. Searched in the libraries specified by PADPATH when missing.',
        ),
        ArgumentDoc('l_anchorPoint', 'Layout coordinates.'),
        ArgumentDoc('t_netName', 'Net name; `nil` → stand-alone.'),
    )
    assert rich.doc.returns == (
        ArgumentDoc('l_result', 'List: (`car`) dbid of the via. (`cadr`) `t` if DRCs are created.'),
        ArgumentDoc('nil', 'Nothing is created.'),
    )
    assert rich.doc.examples == (
        ExampleSegment(
            'code', ('myvia = axlRich("pad1", 5600:4200, "sclkl")    ⇒ (dbid:526745 nil)',)
        ),
        ExampleSegment('prose', ('Adds a standalone via.',)),
    )

    plain = specs['axlPlain']
    assert plain.doc.description == (('Does nothing.',),)
    assert plain.doc.arguments == ()
    assert plain.doc.returns == ()
    assert plain.doc.examples == ()


def test_build_api_specs_parses_section_heading_variants_and_cleaning(tmp_path: Path) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlBold', 'axlNumbered', 'axlBullets'],
        {
            'apis.md': """
### axlBold

`axlBold(t_name) => t/nil`

**Description**

Uses the ALT\\_SYMBOL list; see [axlAltSymbolOK](07dbaccs.html#739212 "6") for checks.

> `'(s_name...) t_mode/s_mode` quoted form.

**Net Attributes**

| `attr` | meaning

**Arguments**

| `t_name` | may be compdef or a refdes name

#### Value Returns

| `t` | is legal
| `nil` | error or not legal

### axlNumbered

`axlNumbered() => t/nil`

#### Description

Numbered examples.

#### Example 1

`axlNumbered()`

First form.

#### Example 2

> > ```
> > axlNumbered()
> > ```

### axlBullets

`axlBullets(x_template) => x_result/nil`

#### Description

Bullet returns.

#### Arguments

`x_template`

#### Value Returned

* `x_result` - new result block

* Returned when the command fails outright.
""",
        },
    )

    specs = {spec.name: spec for spec in build_api_specs(api_names_path, reference_root)}

    bold = specs['axlBold']
    assert bold.quality == 'exact'
    assert bold.doc.description == (
        ('Uses the ALT_SYMBOL list; see axlAltSymbolOK for checks.',),
        ("`'(s_name...) t_mode/s_mode` quoted form.",),
        ('**Net Attributes**',),
        ('| `attr` | meaning',),
    )
    assert bold.doc.arguments == (ArgumentDoc('t_name', 'may be compdef or a refdes name'),)
    assert bold.doc.returns == (
        ArgumentDoc('t', 'is legal'),
        ArgumentDoc('nil', 'error or not legal'),
    )

    numbered = specs['axlNumbered']
    assert numbered.doc.examples == (
        ExampleSegment('code', ('axlNumbered()',)),
        ExampleSegment('prose', ('First form.',)),
        ExampleSegment('code', ('axlNumbered()',)),
    )

    bullets = specs['axlBullets']
    assert bullets.doc.arguments == ()
    assert bullets.doc.returns == (
        ArgumentDoc('x_result', 'new result block'),
        ArgumentDoc('', 'Returned when the command fails outright.'),
    )


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

    via = by_name['axlDBCreateVia'].doc
    assert via.description == (
        ('Creates a via in the layout as specified by the arguments described below.',),
    )
    assert via.arguments == (
        ArgumentDoc(
            't_padstack',
            'Padstack name. If a padstack definition with this name is not already in the '
            'layout, the function searches in order the libraries specified by`PADPATH` and '
            'loads the definition into the database.',
        ),
        ArgumentDoc('o_padstackDbid', 'a padstack dbid'),
        ArgumentDoc('l_anchorPoint', 'Layout coordinates of the location to create the via.'),
        ArgumentDoc(
            't_netName',
            'Name of the net to which the via is to belong; `nil` → via is stand-alone.',
        ),
        ArgumentDoc(
            'g_mirror',
            '`t` → create via mirrored. `nil` → create via unmirrored. '
            '`` `GEOMETRY `` → only geometry is mirrored.',
        ),
        ArgumentDoc('f_rotation', 'Rotation of via in degrees.'),
        ArgumentDoc(
            'o_parent',
            '`DBID`of the object to which to attach the via. Use a symbol instance or use '
            '`nil` to specify the design itself.',
        ),
    )
    assert via.returns == (
        ArgumentDoc(
            'l_result',
            'List: (`car`) `DBID`of the via created. (`cadr`) `t`if DRCs are created. '
            '`nil`if DRCs are not created.',
        ),
        ArgumentDoc('nil', 'Nothing is created.'),
    )
    assert via.examples[0].kind == 'code'
    assert via.examples[0].lines == (
        (
            'myvia = axlDBCreateVia( "pad1", 5600:4200,    "sclkl", t, 45., nil)    ⇒ '
            '(dbid:526745 nil)'
        ),
    )
    assert via.examples[-1].kind == 'prose'

    mks = by_name['axlMKSConvert'].doc
    assert mks.description[0] == (
        (
            'Converts any allowable unit to any other allowable unit. It operates in several '
            'ways, depending on the arguments.'
        ),
    )
    assert [doc.name for doc in mks.arguments] == ['n_input', 't_inUnits', 't_outUnits']
    mks_code = [
        line for segment in mks.examples if segment.kind == 'code' for line in segment.lines
    ]
    assert 'axlMKSConvert(.5 "design" "INCHES") => 0.0005' in mks_code

    text_block = by_name['axlDBTextBlockCreate'].doc
    assert text_block.arguments == ()
    assert text_block.returns == (
        ArgumentDoc('x_textBlock', 'new text block'),
        ArgumentDoc(
            'nil',
            'Returned if the command fails. Typically, this happens when you have exhausted '
            'the number block Allegro provides, or one of the parameters is not of the '
            'correct data type.',
        ),
    )
    assert text_block.examples[-1] == ExampleSegment(
        'code',
        ('blockNum = axlDBTextBlockCreate(1 ?width 15.0 ?height 16.0)',),
    )

    alt_symbol = by_name['axlAltSymbolOK'].doc
    assert alt_symbol.description == (
        (
            (
                'This verifies that symbol is legal for component. Must be in the ALT_SYMBOL '
                'list with the correct layer.'
            ),
        ),
    )
    assert [doc.name for doc in alt_symbol.returns] == ['t', 'nil']


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
    assert 'Args:' in first
    assert 'Returns:' in first
    assert '```' in first


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
    assert specs[-1].doc.description == ()
    report = render_report(specs)
    assert 'total=9' in report
    assert 'fallback axlTrailing algroskill/malformed.md:2' in report


def test_render_stub_disambiguates_duplicate_parameter_names(tmp_path: Path) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlDup'],
        {'apis.md': '### axlDup\n`axlDup(l_point lPoint) => t`\n'},
    )
    (spec,) = build_api_specs(api_names_path, reference_root)

    stub = render_stub([spec])

    assert 'def __call__(self, l_point: SkillList, l_point_2: Skill, /) -> bool:' in stub


def _call_docstrings(stub: str) -> dict[str, list[str]]:
    tree = ast.parse(stub)
    return {
        node.name: [
            ast.get_docstring(item) or ''
            for item in node.body
            if isinstance(item, ast.FunctionDef) and item.name == '__call__'
        ]
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name.startswith('_Axl')
    }


def test_render_stub_emits_enriched_google_style_docstrings(tmp_path: Path) -> None:
    api_names_path, reference_root = _write_sources(
        tmp_path,
        ['axlRich', 'axlKeyword', 'axlMiddle', 'axlFallback'],
        {
            'apis.md': """
### axlRich

`axlRich(t_padstack l_anchorPoint [t_netName]) => l_result/nil`

#### Description

Creates a via in the layout.

#### Arguments

|  |
| --- | ---
| `t_padstack` | Padstack name.
| `l_anchorPoint` | Layout coordinates.
| `t_netName` | Net name; `nil` → stand-alone.
| `o_unmatched` | Documented but not in the signature.

#### Value Returned

|  |
| --- | ---
| `l_result` | List: (`car`) dbid of the via.
| `nil` | Nothing is created.

#### Example

> ```
> myvia = axlRich("pad1", 5600:4200)
> printf("done\\n")
> ```

Adds a via.

### axlKeyword

`axlKeyword(x_blockTemplate ?width f_width ?height f_height) => x_block/nil`

#### Description

Creates a text block.

#### Arguments

|  |
| --- | ---
| `x_blockTemplate` | Template block number.
| `f_width` | Line width.
| `f_height` | Line height.

#### Value Returned

* `x_block` - new text block

* Command failed.

### axlMiddle

`axlMiddle(t_first [t_middle] t_last) => t/nil`

#### Description

Expands middle optionals.

#### Arguments

|  |
| --- | ---
| `t_first` | First.
| `t_middle` | Middle.
| `t_last` | Last.

### axlFallback

`axlFallback broken => t`

#### Description

This API is documented but its declaration is unparsable.

#### Value Returned

| `t` | Always succeeds.
""",
        },
    )
    specs = build_api_specs(api_names_path, reference_root)

    stub = render_stub(specs)
    docstrings = _call_docstrings(stub)

    assert docstrings['_AxlRich'] == [
        """\
Creates a via in the layout.

Args:
    t_padstack: Padstack name.
    l_anchor_point: Layout coordinates.
    t_net_name: Net name; `nil` → stand-alone.

Returns:
    l_result: List: (`car`) dbid of the via.
    nil: Nothing is created.

Example:
    ```
    myvia = axlRich("pad1", 5600:4200)
    printf("done\\n")
    ```

    Adds a via.

SKILL: axlRich(t_padstack l_anchorPoint [t_netName]) => l_result/nil
Version: Allegro 17.2-2016
Source: algroskill/apis.md:2""",
    ]

    assert docstrings['_AxlKeyword'] == [
        """\
Creates a text block.

Args:
    x_block_template: Template block number.
    width: Line width.
    height: Line height.

Returns:
    x_block: new text block
    - Command failed.

SKILL: axlKeyword(x_blockTemplate ?width f_width ?height f_height) => x_block/nil
Version: Allegro 17.2-2016
Source: algroskill/apis.md:35""",
    ]
    assert (
        'def __call__(self, x_block_template: int, /, *, width: float | None = ..., '
        'height: float | None = ...) -> int | None:' in stub
    )

    middle = docstrings['_AxlMiddle']
    assert len(middle) == 2
    assert (
        middle[0]
        == """\
Expands middle optionals.

Args:
    t_first: First.
    t_last: Last.

SKILL: axlMiddle(t_first [t_middle] t_last) => t/nil
Version: Allegro 17.2-2016
Source: algroskill/apis.md:57"""
    )
    assert (
        middle[1]
        == """\
Expands middle optionals.

Args:
    t_first: First.
    t_middle: Middle.
    t_last: Last.

SKILL: axlMiddle(t_first [t_middle] t_last) => t/nil
Version: Allegro 17.2-2016
Source: algroskill/apis.md:57"""
    )

    assert docstrings['_AxlFallback'] == [
        """\
This API is documented but its declaration is unparsable.

Returns:
    t: Always succeeds.

SKILL: signature unavailable; generic fallback
Version: Allegro 17.2-2016
Source: algroskill/apis.md:73""",
    ]


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
