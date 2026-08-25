"""Parse bundled Allegro API references for static stub generation."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from typing_extensions import Literal

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_API_NAMES = ROOT / 'allegrobridge' / 'assets' / 'api_names.txt'
DEFAULT_REFERENCES = (
    ROOT / '.agents' / 'skills' / 'cadence-skill-agent' / 'skill-references' / 'algroskill'
)
EXPECTED_API_COUNT = 792
ARROWS = ('⇒', '==>', '=>', '-=>', '-->', '->')
API_NAME = re.compile(r'\baxl[A-Za-z0-9_]+\b')
ARGUMENT_CELL = re.compile(r'^\|\s*`?(?P<cell>[^`|\n]+)`?\s*\|')
PLAIN_ARGUMENT = re.compile(r'^`(?P<name>[A-Za-z_][A-Za-z0-9_]*)`$')
ARGUMENT_NAME = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
KEYWORD_ARGUMENT = re.compile(r'\?([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z0-9_/\']+)')

Quality = Literal['exact', 'fallback', 'conflict', 'missing', 'document_only']
ParameterKind = Literal['positional', 'keyword', 'var_positional', 'var_keyword']

# SKILL Hungarian prefix pattern
HUNGARIAN_PREFIXES = (
    'lo',
    'lt',
    'lx',
    'ls',
    'ln',
    'lg',
    'lr',
    'la',
    'ld',
    'od',
    'so',
    'ts',
    'll',
    'l',
    't',
    'o',
    'r',
    'g',
    'f',
    'x',
    's',
    'b',
    'd',
    'n',
    'a',
    'c',
    'e',
    'k',
    'm',
    'p',
    'u',
    'v',
    'w',
    'y',
    'z',
)
HUNGARIAN_PATTERN = '|'.join(sorted(HUNGARIAN_PREFIXES, key=len, reverse=True))

# Only use an override when the body of the indexed entry supplies enough
# argument and return information to reconstruct the declaration.  A typo in
# a heading is not evidence for a guessed signature; those entries remain
# fallback until a parser rule can preserve all documented forms.
SIGNATURE_OVERRIDES: dict[str, tuple[str, ...]] = {
    'axlAirGap': (
        (
            'axlAirGap(o_item1DBID o_item2DBID/l_xy [t_layer/nil] [s_mode]) '
            '=> l_airGapData/nil/(s_error l_airGapData/l_errorData)'
        ),
    ),
    'axlBackdrillGet': (
        "axlBackdrillGet(o_dbidPinOrVia/'status) => lt_backdrillData/g_status/nil",
    ),
    'axlCancelOff': ('axlCancelOff() => t',),
    'axlCancelTest': ('axlCancelTest() => t/nil',),
    'axlChangeLayer': (
        ('axlChangeLayer(lo_dbid/o_dbid t_newLayer [o_padStackDbid/t_padStackName]) => t/nil'),
    ),
    'axlColorOnSet': ('axlColorOnSet(g_item g_state) => t',),
    'axlCopyObject': (
        (
            'axlCopyObject(lo_dbid/o_dbid ?move l_deltaPoint ?mirror t/nil '
            '?angle f_angle ?origin l_rotatePoint ?allOrNone t/nil ?retainNet t/nil) '
            '=> lo_dbid/nil'
        ),
    ),
    'axlCreateBondFinger': (
        (
            'axlCreateBondFinger(parentSymbol [fingerName] l_fingerData l_placementData) '
            '=> o_dbid/nil'
        ),
    ),
    'axlCreateBondWire': (
        'axlCreateBondWire(parentSymbol [l_wireStart] l_wireEnd l_wirePhysical) => o_dbid/nil',
    ),
    'axlDBCloak': ('axlDBCloak(g_func [g_mode/lg_mode]) => g_return',),
    'axlDBCreateLine': (
        (
            "axlDBCreateLine(l_points [f_width] [t_layer] [t_netName/'line] [o_parent] "
            '[s_font]) => l_result/nil'
        ),
    ),
    'axlDBCreatePath': (
        (
            "axlDBCreatePath(r_path [t_layer] [t_netName/'line] [o_parent] [lo_props] "
            '[s_font]) => l_result/nil'
        ),
    ),
    'axlDeleteBondWire': ('axlDeleteBondWire(bondWires [deleteFingers]) => t/nil',),
    'axlDllCall': ('axlDllCall(o_pluginFunc [*g_args]) => nil/x_value/lg_data',),
    'axlFormCreate': (
        (
            'axlFormCreate(s_formHandle g_formSource [lt_placement] g_formAction '
            'g_nonBlock [g_stringOption]) => r_form/nil'
        ),
    ),
    'axlFormGridEvents': ('axlFormGridEvents(r_form t_field g_events) => t/nil',),
    'axlFormListOptions': ('axlFormListOptions(r_form t_field g_options) => t/nil',),
    'axlFormMsg': ('axlFormMsg(r_form t_messageLabel [*g_args]) => t_msg/nil',),
    'axlGetWireProfileDefinition': (
        'axlGetWireProfileDefinition(profileName) => l_definition/s_error',
    ),
    'axlJournal': ('axlJournal(g_option) => g_result/nil',),
    'axlMKSConvert': (
        'axlMKSConvert(n_input t_inUnits [t_outUnits]) => f_output/nil',
        'axlMKSConvert(t_input [t_outUnits]) => f_output/nil',
        'axlMKSConvert(nil t_inUnits) => t/nil',
        'axlMKSConvert(n_input) => f_output/nil',
    ),
    'axlMakeDynamicsPath': ('axlMakeDynamicsPath(l_formattedList) => r_path/nil',),
    'axlMiniStatusLoad': (
        (
            'axlMiniStatusLoad(s_formHandle g_formSource g_formAction [g_stringOption] '
            '[t_restrict]) => r_form/nil'
        ),
    ),
    'axlMsgContextStart': ('axlMsgContextStart(g_formatString [*g_args]) => r_context',),
    'axlMsgPut': ('axlMsgPut(g_messageFormat [*g_args]) => t',),
    'axlPadstackEdit': (
        'axlPadstackEdit(g_padstack g_attributes) => l_attributes/t/nil',
        'axlPadstackEdit(g_padstack s_name g_value) => t/nil',
    ),
    'axlPathArcAngle': (
        'axlPathArcAngle(r_path f_width l_endPoint g_clockwise f_angle) => r_path/nil',
    ),
    'axlPathArcRadius': (
        ('axlPathArcRadius(r_path f_width l_endPoint g_clockwise g_bigarc f_radius) => r_path/nil'),
    ),
    'axlPurgePadstacks': ('axlPurgePadstacks(s_mode g_option) => x_cnt',),
    'axlReportList': ('axlReportList() => ll_reportList/nil',),
    'axlUIMenuChange': ('axlUIMenuChange(x_menuId [*g_optionPairs]) => t/nil',),
    'axlUIPrompt': ('axlUIPrompt(t_message [g_defaultOrPassword]) => t_response/nil',),
    'axlUIWHelpRegister': (
        'axlUIWHelpRegister(t_cmd t_helpFile) => t/nil',
        'axlUIWHelpRegister(g_command) => t_file/lt_cmds/t/nil',
    ),
    'axlUIWPrint': ('axlUIWPrint(r_window/nil t_formatString [*g_args]) => t/nil',),
    'axlXSectionModify': ('axlXSectionModify(**g_attributes) => g_xsectionDefstruct/nil',),
    'axlcreate': ('axlcreate() => t_filmName/nil',),
    'axlDBCreatePropDictEntry': (
        (
            'axlDBCreatePropDictEntry(t_name t_type lt_objects/t [ln_range] [t_units] [g_hidden]) '
            '=> od_propDictEntry/nil'
        ),
        'axlDBCreatePropDictEntry(nil) => lt_availbeObject',
    ),
    'axlAltSymbolReplace': ('axlAltSymbolReplace(t_name/o_dbid t_symbol) => t/nil',),
    'axlAltSymbolList': ('axlAltSymbolList(t_name/o_dbid g_layer) => lt_symbols/nil',),
    'axlDesignFlip': ('axlDesignFlip(g_flip) => t/nil',),
    'axlSetBondWireProfile': ('axlSetBondWireProfile(bondWires profileName) => t/nil',),
    'axlSetDieStackData': ('axlSetDieStackData(g_stackId s_dataType g_newValue) => t/nil',),
    'axlSetFindFilter': ('axlSetFindFilter(?enabled lt_enabled ?onButtons lt_onButtons) => t/nil',),
    'axlShapeDeleteVoids': ('axlShapeDeleteVoids(o_shapeId/o_voidId/lo_voidid) => t/nil',),
    'axlTestPoint': ('axlTestPoint(o_dbid g_mode) => t/nil/s_error',),
    'axlUIMenuDelete': ('axlUIMenuDelete(x_menuId) => t/nil',),
    'axlUIWDisableQuit': ('axlUIWDisableQuit(o_window) => t/nil',),
    'axlUIWRedraw': ('axlUIWRedraw(r_window/nil) => t/nil',),
    'axlUIWTimerRemove': ('axlUIWTimerRemove(o_timerId) => t/nil',),
    'axlVersionIdPrint': ('axlVersionIdPrint(x_time/t_time) => t_printTime/nil',),
    'axlPolyOperation': (
        (
            'axlPolyOperation(o_polygon1/lo_polygon1 o_polygon2/lo_polygon2 s_operation) '
            '=> lo_polygon/nil'
        ),
    ),
    'axlDBDelLock': ('axlDBDelLock([t_password]) => t/nil',),
    'axlDBGetDrillPlating': ('axlDBGetDrillPlating(t_padstackname) => s_plating/nil',),
    'axlDBGetLayerType': ('axlDBGetLayerType(t_layername) => t_layertype/nil',),
    'axlDllCallList': ('axlDllCallList(o_pluginFunc l_args) => nil/x_value/lg_data',),
    'axlGetModuleInstanceLogicMethod': (
        'axlGetModuleInstanceLogicMethod(o_modinst) => i_logic/nil',
    ),
    'axlMKSAlias': ('axlMKSAlias(t_mksAlias) => t_def/nil',),
    'axlPathOffset': ('axlPathOffset(r_path offset) => r_path',),
    'axlMeterCreate': (
        (
            'axlMeterCreate(t_title t_infoString g_enableCancel [t_formname] [t_infoString2] '
            '[g_formCallback]) => t/nil'
        ),
    ),
    'axlGetDynamicsSegs': ('axlGetDynamicsSegs(point1 point2 lastPath) => l_pointList/nil',),
    'axlPolyFromDB': (
        (
            'axlPolyFromDB(o_dbid/r_path ?endCapType s_endCapType ?layer t_layer ?padType '
            's_padType ?holes t/nil ?line2poly t/nil ?xhatch t/nil) => lo_polygon/nil'
        ),
    ),
    'axlTransformObject': (
        (
            "axlTransformObject(lo_dbid/o_dbid ?move l_deltaPoint ?mirror t/nil/'GEOMETRY "
            '?angle f_angle ?origin l_rotatePoint ?allOrNone t/nil) => lo_dbid/nil'
        ),
    ),
    'axlRunBatchDBProgram': (
        (
            'axlRunBatchDBProgram(t_prog t_cmdFmt ?logfile t_logfile ?startMsg t_startMsg '
            '?reloadDB t/nil ?noUnload t/nil ?silent t/nil ?noProgress t/nil '
            '?warnProgram t/nil) => t/x_error'
        ),
    ),
    'axlZoomCenter': ('axlZoomCenter(x_window xy) => t/nil',),
    'axlZoomControl': ('axlZoomControl(s_option [g_arg]) => g_return',),
    'axlHistory': (
        'axlHistory([x_num]) => t',
        'axlHistory(s_operation t_filename) => t/nil',
    ),
    'axlCNSSetViaZEnabled': ('axlCNSSetViaZEnabled(g_value) => t',),
    'axlDMDirectoryBrowse': (
        (
            'axlDMDirectoryBrowse(t_startingDirectory g_writeFlag ?helpTag t_helpTag '
            '?title t_title) => t_dirName/nil'
        ),
    ),
    'axlDMFileBrowse': (
        (
            'axlDMFileBrowse(t_fileType g_writeFlag ?defaultName t_defaultName ?helpTag '
            't_helpTag ?directorySet g_directorySet ?noDirectoryButton g_noDirectoryButton '
            '?mainFile g_mainFile ?noSticky g_noSticky ?title t_title ?optFilters t_filters) '
            '=> t_fileName/nil'
        ),
    ),
}

DOCUMENT_ONLY_NAMES = frozenset({
    'axlColorDoc',
    'axlFormBNFDoc',
    'axlFormCallback',
    'axlMathConstants',
    'axlParamFilletDoc',
    'axlSpreadsheetDoc',
})


@dataclass(frozen=True)
class ParameterSpec:
    name: str
    value_name: str | None
    kind: ParameterKind
    optional: bool


@dataclass(frozen=True)
class DeclarationSpec:
    raw_signature: str
    parameters: tuple[ParameterSpec, ...]
    raw_return: str


@dataclass(frozen=True)
class ApiSpec:
    name: str
    declarations: tuple[DeclarationSpec, ...]
    description: str
    source_path: str | None
    source_line: int | None
    quality: Quality
    issues: tuple[str, ...]


@dataclass(frozen=True)
class QualityReport:
    total: int
    exact: int
    fallback: int
    conflict: int
    missing: int
    document_only: int


@dataclass(frozen=True)
class _SourceEntry:
    declarations: tuple[DeclarationSpec, ...]
    description: str
    source_path: str
    source_line: int
    issues: tuple[str, ...]


def _normalize(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('`', '').strip())


def _before_description(lines: Sequence[str]) -> Sequence[str]:
    for index, line in enumerate(lines):
        if line.strip().lower().startswith('#### description'):
            return lines[:index]
    return lines


def _declaration_candidates(name: str, lines: Sequence[str]) -> tuple[str, ...]:
    candidates: list[str] = []
    current: list[str] = []
    before = _before_description(lines)
    for line in before:
        candidate = line.strip()
        if not candidate or candidate.startswith('```'):
            continue
        plain = _normalize(candidate)
        if not current and re.search(rf'\b{re.escape(name)}\s*\(', plain) is None:
            continue
        current.append(plain)
        declaration = _normalize(' '.join(current))
        if any(arrow in declaration for arrow in ARROWS):
            candidates.append(declaration)
            current = []
        elif ')' in declaration and not any(arrow in declaration for arrow in ARROWS):
            after_paren = declaration.split(')', 1)[1].strip()
            if after_paren and not after_paren.startswith('('):
                candidates.append(declaration.replace(')', ') => ', 1))
                current = []
    return tuple(candidates)


def _argument_names(lines: Sequence[str]) -> tuple[str, ...]:
    in_arguments = False
    names: list[str] = []
    for line in lines:
        normalized = line.strip()
        lowered = normalized.lower()
        if lowered.startswith(('#### argument', '**argument')):
            in_arguments = True
            continue
        if not in_arguments:
            continue
        if 'value returned' in lowered or 'value returns' in lowered:
            break
        if normalized.startswith('#### ') and 'argument' not in lowered:
            break
        cell = ARGUMENT_CELL.match(normalized)
        plain = PLAIN_ARGUMENT.match(normalized)
        candidates = ARGUMENT_NAME.findall(cell.group('cell')) if cell is not None else []
        if plain is not None:
            candidates.append(plain.group('name'))
        for name in candidates:
            if name not in {'nil', 't', 'or'} and name not in names:
                names.append(name)
    return tuple(names)


def _positional_segments(raw: str) -> tuple[tuple[str, bool], ...] | None:
    normalized = raw.strip().strip(',')
    if not normalized:
        return ()
    segments: list[tuple[str, bool]] = []
    position = 0
    for match in re.finditer(r'\[([^\[\]]*)\]', normalized):
        if match.start() > position:
            segments.append((normalized[position : match.start()], False))
        segments.append((match.group(1), True))
        position = match.end()
    if position < len(normalized):
        segments.append((normalized[position:], False))
    if any(character in ''.join(value for value, _ in segments) for character in '[]'):
        return None
    return tuple(
        (segment.strip(' ,'), optional) for segment, optional in segments if segment.strip()
    )


def _parse_explicit_tokens(
    tokens: Sequence[str],
    optional: bool,
    argument_names: Sequence[str],
) -> tuple[ParameterSpec, ...] | None:
    parameters: list[ParameterSpec] = []
    for token in tokens:
        parsed = _parse_positional_segment(token, optional, argument_names)
        if parsed is None:
            return None
        parameters.extend(parsed)
    return tuple(parameters)


def _parse_variadic_parameter(raw: str) -> ParameterSpec | None:
    if raw.startswith('**') and ARGUMENT_NAME.fullmatch(raw[2:]):
        return ParameterSpec(raw[2:], None, 'var_keyword', optional=False)
    if raw.startswith('*') and ARGUMENT_NAME.fullmatch(raw[1:]):
        return ParameterSpec(raw[1:], None, 'var_positional', optional=False)
    return None


def _build_fuzzy_regex_for_name(name: str) -> str:
    chars = []
    for c in name:
        if c == '_':
            chars.append('_?')
        elif c.isupper():
            chars.append(f'_?[{c.lower()}{c}]')
        else:
            chars.append(f'[{c}{c.upper()}]')
    return ''.join(chars)


def _parse_positional_segment(
    raw: str,
    optional: bool,
    argument_names: Sequence[str],
) -> tuple[ParameterSpec, ...] | None:
    raw = re.sub(r'\s*/\s*', '/', raw)
    tokens = tuple(token for token in re.split(r'[\s,]+', raw) if token)
    if len(tokens) > 1:
        return _parse_explicit_tokens(tokens, optional, argument_names)

    variadic = _parse_variadic_parameter(raw)
    if variadic is not None:
        return (variadic,)

    atom_patterns = [
        *(
            _build_fuzzy_regex_for_name(name)
            for name in sorted(set(argument_names), key=len, reverse=True)
        ),
        rf'(?:{HUNGARIAN_PATTERN})_[A-Za-z0-9_]+',
        r"'[A-Za-z0-9_]+",
        r'nil|t|/',
    ]

    combined_pattern = '|'.join(atom_patterns)
    parts = re.findall(combined_pattern, raw)
    if ''.join(parts) != raw:
        parts = re.findall(rf"(?:{HUNGARIAN_PATTERN})_[A-Za-z0-9]+|'?[A-Za-z0-9_]+|/", raw)
        if ''.join(parts) != raw:
            return None

    groups: list[list[str]] = []
    alternative = False
    for part in parts:
        if part == '/':
            if not groups or alternative:
                return None
            alternative = True
        elif alternative:
            groups[-1].append(part)
            alternative = False
        else:
            groups.append([part])
    if alternative:
        return None
    return tuple(
        ParameterSpec(
            name='/'.join(group),
            value_name=None,
            kind='positional',
            optional=optional,
        )
        for group in groups
    )


def _parse_positional_parameters(
    raw: str,
    argument_names: Sequence[str],
) -> tuple[ParameterSpec, ...] | None:
    segments = _positional_segments(raw)
    if segments is None:
        return None
    parameters: list[ParameterSpec] = []
    for segment, optional in segments:
        parsed = _parse_positional_segment(segment, optional, argument_names)
        if parsed is None:
            return None
        parameters.extend(parsed)
    return tuple(parameters)


def _parse_parameters(
    raw: str,
    argument_names: Sequence[str],
) -> tuple[ParameterSpec, ...] | None:
    keyword_start = raw.find('?')
    positional_raw = raw if keyword_start < 0 else raw[:keyword_start]
    keyword_raw = '' if keyword_start < 0 else raw[keyword_start:]
    positional = _parse_positional_parameters(positional_raw, argument_names)
    if positional is None:
        return None

    keyword_parameters = tuple(
        ParameterSpec(name=name, value_name=value_name, kind='keyword', optional=True)
        for name, value_name in KEYWORD_ARGUMENT.findall(keyword_raw)
    )
    remaining = KEYWORD_ARGUMENT.sub('', keyword_raw)
    if re.sub(r'\s+', '', remaining):
        return None
    return positional + keyword_parameters


def _parse_declaration(
    name: str,
    raw_signature: str,
    argument_names: Sequence[str],
) -> DeclarationSpec | None:
    normalized = _normalize(raw_signature)
    arrow = next((value for value in ARROWS if value in normalized), None)
    if arrow is None:
        return None
    call, raw_return = normalized.split(arrow, maxsplit=1)
    match = re.fullmatch(r'(?P<name>axl[A-Za-z0-9_]+)\s*\((?P<args>.*)\)', call.strip())
    if match is None or match.group('name') != name:
        return None
    parameters = _parse_parameters(match.group('args'), argument_names)
    if parameters is None or not raw_return.strip():
        return None
    return DeclarationSpec(normalized, parameters, raw_return.strip())


def _description(lines: Sequence[str]) -> str:
    start = next(
        (
            index + 1
            for index, line in enumerate(lines)
            if line.strip().lower().startswith('#### description')
        ),
        None,
    )
    if start is None:
        return ''
    parts: list[str] = []
    for line in lines[start:]:
        normalized = line.strip()
        if normalized.startswith(('#### ', '### ')):
            break
        if not normalized:
            if parts:
                break
        else:
            parts.append(_normalize(normalized))
    return ' '.join(parts)


def _parse_source_entry(
    name: str,
    path: Path,
    line: int,
    section: Sequence[str],
    reference_root: Path,
) -> _SourceEntry:
    argument_names = _argument_names(section)
    candidates = SIGNATURE_OVERRIDES.get(name, _declaration_candidates(name, section))
    declarations: list[DeclarationSpec] = []
    issues: list[str] = []
    for candidate in candidates:
        parsed = _parse_declaration(name, candidate, argument_names)
        if parsed is None:
            issues.append(f'unparsed declaration: {candidate}')
        elif parsed not in declarations:
            declarations.append(parsed)
    if not candidates:
        issues.append('documented declaration is missing or names another function')
    source_path = path.relative_to(reference_root.parent).as_posix()
    return _SourceEntry(
        declarations=tuple(declarations),
        description=_description(section),
        source_path=source_path,
        source_line=line,
        issues=tuple(issues),
    )


def _source_entries(
    reference_root: Path,
    supported_names: set[str],
) -> dict[str, list[_SourceEntry]]:
    entries: dict[str, list[_SourceEntry]] = {name: [] for name in supported_names}
    for path in sorted(reference_root.glob('*.md')):
        lines = path.read_text(encoding='utf-8').splitlines()
        headings = [index for index, line in enumerate(lines) if line.startswith('### ')]
        for position, heading_index in enumerate(headings):
            end = headings[position + 1] if position + 1 < len(headings) else len(lines)
            names = [
                name
                for name in API_NAME.findall(_normalize(lines[heading_index][4:]))
                if name in supported_names
            ]
            section = lines[heading_index + 1 : end]
            for name in names:
                entries[name].append(
                    _parse_source_entry(name, path, heading_index + 1, section, reference_root)
                )
    return entries


def _build_api_spec(name: str, entries: Sequence[_SourceEntry]) -> ApiSpec:
    if not entries:
        return ApiSpec(name, (), '', None, None, 'missing', ('documentation entry is missing',))

    source = entries[0]
    if name in DOCUMENT_ONLY_NAMES:
        return ApiSpec(
            name,
            (),
            source.description,
            source.source_path,
            source.source_line,
            'document_only',
            ('documentation section is not a callable API',),
        )
    issues = tuple(issue for entry in entries for issue in entry.issues)
    if issues or any(not entry.declarations for entry in entries):
        return ApiSpec(
            name,
            (),
            source.description,
            source.source_path,
            source.source_line,
            'fallback',
            issues,
        )

    declaration_sets = {entry.declarations for entry in entries}
    if len(declaration_sets) != 1:
        sources = ', '.join(entry.source_path for entry in entries)
        return ApiSpec(
            name,
            (),
            source.description,
            source.source_path,
            source.source_line,
            'conflict',
            (f'conflicting declarations in {sources}',),
        )

    return ApiSpec(
        name,
        source.declarations,
        source.description,
        source.source_path,
        source.source_line,
        'exact',
        (),
    )


def build_api_specs(api_names_path: Path, reference_root: Path) -> tuple[ApiSpec, ...]:
    names = api_names_path.read_text(encoding='utf-8').splitlines()
    if len(names) != len(set(names)):
        raise ValueError('api_names.txt contains duplicate names')
    entries = _source_entries(reference_root, set(names))
    return tuple(_build_api_spec(name, entries[name]) for name in names)


def summarize_specs(specs: Iterable[ApiSpec]) -> QualityReport:
    values = tuple(specs)
    counts = Counter(spec.quality for spec in values)
    return QualityReport(
        total=len(values),
        exact=counts['exact'],
        fallback=counts['fallback'],
        conflict=counts['conflict'],
        missing=counts['missing'],
        document_only=counts['document_only'],
    )


def render_report(specs: Sequence[ApiSpec]) -> str:
    report = summarize_specs(specs)
    lines = [
        f'total={report.total}',
        f'exact={report.exact}',
        f'fallback={report.fallback}',
        f'conflict={report.conflict}',
        f'missing={report.missing}',
        f'document_only={report.document_only}',
    ]
    for quality in ('fallback', 'conflict', 'missing', 'document_only'):
        for spec in specs:
            if spec.quality != quality:
                continue
            location = (
                f'{spec.source_path}:{spec.source_line}'
                if spec.source_path is not None
                else 'no-source'
            )
            lines.append(f'{quality} {spec.name} {location} {"; ".join(spec.issues)}')
    return '\n'.join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-names', type=Path, default=DEFAULT_API_NAMES)
    parser.add_argument('--references', type=Path, default=DEFAULT_REFERENCES)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)

    specs = build_api_specs(args.api_names, args.references)
    print(render_report(specs))
    if args.check and len(specs) != EXPECTED_API_COUNT:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
