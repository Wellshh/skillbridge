#!/usr/bin/env python3
"""Convert the Cadence Allegro SKILL reference HTML sources to markdown.

Regenerates the ``algroskill/`` body corpus from the CHM-exported HTML under
``docs/html/algroskill/``. The previous HTML-to-markdown pass lost the
whitespace between signature parameters (``o_dbidg_layer`` for
``o_dbid g_layer``); in the HTML source that whitespace is encoded as ``<dd>``
separator tags inside the declaration blocks, so extracting the declaration
text with ``<dd>`` mapped to a space restores the signatures exactly.

The converter is fail-closed: every rendered entry is run through the
``check_signatures`` gate and the build aborts on any error-severity finding,
so a glued signature can never be written to the corpus again.

Output conventions (unchanged, consumed by build_reference_indexes.py):
  - one ``<stem>.md`` per chapter, ``<stem>.partNN.md`` when a chapter exceeds
    the part token target, split on API-entry boundaries;
  - ``### <api>`` headings followed by an inline backtick declaration;
  - ``#### Description / Arguments / Value Returns / Examples / See Also``;
  - the TOC/APL markdown files are left untouched (navigation only).
"""

from __future__ import annotations

import argparse
import math
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

from build_reference_indexes import CHARS_PER_TOKEN
from check_signatures import (
    ARGUMENT_NAME,
    PREFIXED_ATOM,
    BodyEntry,
    check_signature_shape,
    _parameter_text,
    _split_atoms,
)

DOCUMENT = "algroskill"
PART_TOKEN_TARGET = 13_500
EXPECTED_APL_LINKS = 817  # 818 APL links minus the one bare page-number label
SECTION_LABELS = {
    "description": "Description",
    "argument": "Arguments",
    "arguments": "Arguments",
    "value returned": "Value Returns",
    "value returns": "Value Returns",
    "example": "Examples",
    "examples": "Examples",
    "see also": "See Also",
}
TABLE_HEADER_CELLS = {"argument", "name", "valid values", "description", "value", "returns"}
# bare paragraphs that separate overloaded declarations inside the printed
# declaration zone (``axlDBCreateSymbolSkeleton`` has two forms split by "or")
DECL_SEPARATORS = {"or", "and", "...", ""}
KEEP_FILES = (f"{DOCUMENT}TOC.md", f"{DOCUMENT}APL.md")
SKIP_STEMS = (f"{DOCUMENT}TOC", f"{DOCUMENT}APL", "titlecopy")
# Source-document defects where the printed declaration names the wrong
# function or drops/garbles parameters. Keyed by (chapter stem, anchor, API
# name); the corrected declaration follows the documented Arguments table of
# the same section.
SIGNATURE_OVERRIDES: Dict[Tuple[str, str, str], "str | List[str]"] = {
    # the printed declaration carries axlDB2Path's callee (copy-paste defect)
    ("03dbcre8", "895775", "axlPathOffset"): "axlPathOffset( r_path xy ) => r_path",
    # printed declaration has a stray "))" and names the return od_propDictEntry
    # while the section's Value Returns table documents o_propDictEntry
    ("03dbcre8", "367783", "axlDBCreatePropDictEntry"):
        "axlDBCreatePropDictEntry( t_name t_type lt_objects/t [ ln_range ] [ t_units ] [ g_hidden ] ) => o_propDictEntry/nil",
    # the second overload's printed declaration carries axlDBGridGet's callee
    # (copy-paste defect); parameters per the section's Arguments table
    ("04parmgt", "1167420", "axlPadSuppressGet"): [
        "axlPadSuppressGet( nil ) => ll_LayerPadSuppress",
        "axlPadSuppressGet( t_layer/x_layerNumber ) => l_LayerPadSuppress",
    ],
    # the printed declaration carries axlBondWireDelete's callee
    ("06intedt", "832534", "axlDeleteBondWire"): "axlDeleteBondWire( lo_dbid [lo_dbidsKeep] ) => x_count/nil",
    # the printed declaration is missing its opening parenthesis
    ("04parmgt", "1066845", "axlDBGetLayerType"): "axlDBGetLayerType( t_layerName ) => t_layertype/nil",
    # the printed declaration truncates the return after "(x_list"; the shape
    # of the returned list is documented under Value Returns
    ("06intedt", "832246", "axlSmoothItems"):
        "axlSmoothItems( lo_clineList ) => (x_change lo_dbids)/nil",
    # the printed declaration ends with a stray ")" before the arrow
    ("06intedt", "821370", "axlTransformObject"):
        "axlTransformObject( lo_dbid/o_dbid ?move l_deltaPoint ?mirror t/nil/'GEOMETRY ?angle f_angle ?origin l_rotatePoint ?allOrNone t/nil ) => lo_dbid/nil",
    # the printed declaration carries axlShapeAutoVoid's callee (copy-paste
    # defect); parameters per the section's Arguments table
    ("06intedt", "823700", "axlShapeDeleteVoids"):
        "axlShapeDeleteVoids( o_shapeId/o_voidId/lo_voidid ) => t/nil",
    # the printed declaration drops "Logic" from the callee (sibling
    # axlGetModuleInstanceMethod)
    ("07dbaccs", "719496", "axlGetModuleInstanceLogicMethod"):
        "axlGetModuleInstanceLogicMethod( o_modinst ) => i_logic/nil",
    # the printed declaration carries axlAltSymbolOK's callee (copy-paste
    # defect); parameters per the section's Arguments table
    ("07dbaccs", "739374", "axlAltSymbolReplace"):
        "axlAltSymbolReplace( t_name/o_dbid t_symbol ) => t/nil",
    # the printed declaration carries axlTempFile's callee (copy-paste
    # defect); the parameter is documented as g_mode
    ("09cmdshl", "897865", "axlJournal"): "axlJournal( g_mode ) => t_tempFileName",
    # the printed declaration is missing its closing parenthesis
    ("10usrint", "381730", "axlMeterCreate"):
        "axlMeterCreate( t_title t_infoString g_enableCancel [t_formname] [t_infoString2] [g_formCallback] ) => t/nil",
    # the printed declaration drops the "t" prefix of t_alias ("_alias");
    # the Arguments table documents t_alias
    ("09cmdshl", "895632", "axlSetFunckey"):
        "axlSetFunckey( t_alias g_value ) => t/nil",
    # the printed declaration carries axlUIDisableQuit's callee; the section
    # title, TOC, and APL all spell axlUIWDisableQuit
    ("10usrint", "379963", "axlUIWDisableQuit"): "axlUIWDisableQuit( o_window ) => t/nil",
    # the printed declaration writes the dummy callback name formCallback;
    # the API name follows the heading/APL
    ("11frmint", "469106", "axlFormCallback"): "axlFormCallback( [ r_form ] ) => t",
    # the printed declaration carries axlDBDellLock's callee (extra "l")
    ("14dsnctl", "708657", "axlDBDelLock"): "axlDBDelLock( [ t_password ] ) => t/nil",
    # the printed declaration glues "enabled" onto the callee
    ("18consmgt", "1096005", "axlCNSSetViaZEnabled"):
        "axlCNSSetViaZEnabled( g_value ) => t",
    # the printed declaration carries axlReportRegister's callee (copy-paste
    # defect); the section documents the report listing
    ("22extrct", "672158", "axlReportList"): "axlReportList( ) => ll_reportList/nil",
    # the printed declaration is the prose heading of two calling conventions;
    # parameters per the section's Arguments table
    ("23utils", "929803", "axlHistory"):
        "axlHistory( [x_num] [s_operation t_filename] ) => t/nil",
    # the printed declaration carries axlIsPointInsideBox's callee
    ("23utils", "941335", "axlISProductStarted"):
        "axlISProductStarted( t_productName ) => t/nil",
    # the printed declaration carries axlVersionIdPrintd's callee (extra "d")
    ("23utils", "912635", "axlVersionIdPrint"):
        "axlVersionIdPrint( x_time/t_time ) => t_printTime/nil",
    # printed declaration is missing its opening parenthesis and mangles the
    # mode argument ("top |bottom"); the parameter is documented as g_mode
    ("25dbmisc", "1073615", "axlTestPoint"):
        "axlTestPoint( o_dbid g_mode ) => t/nil/s_error",
    # the printed signature says o_dbid_net while the Arguments table
    # documents o_dbid
    ("25dbmisc", "1077976", "axlDBGetManhattan"):
        "axlDBGetManhattan( o_dbid ) => l_result/nil",
    # the printed declaration carries axlUIWTimerRemoveSet's callee
    # (copy-paste defect); the section removes a timer added by axlUIWTimerAdd
    ("10usrint", "380248", "axlUIWTimerRemove"):
        "axlUIWTimerRemove( o_timerId ) => t/nil",
    # the printed declaration spells the refdes arguments t_old_name/t_new_name
    # while the Arguments table spells them t_oldName/t_newName; the table is
    # the cross-check ground truth
    ("26logacc", "1075491", "axlRenameRefdes"):
        "axlRenameRefdes( t_oldName/o_oldCompDbid t_newName/o_newCompDbid ) => t/nil",
    # the printed declaration carries pprint's callee; the description says
    # pprintln prints a newline after the item
    ("27langexten", "1065539", "pprintln"): "pprintln( g_item [p_port] ) => t/nil",
    # the printed declaration carries axlDllCall's callee (copy-paste defect)
    ("27plugin", "1091355", "axlDllCallList"):
        "axlDllCallList( ) => ll_pluginFuncs/nil",
    # the printed declaration carries axlSetDieData's callee (copy-paste
    # defect); parameters per the section's Arguments table
    ("sipapd", "1076715", "axlSetDieStackData"):
        "axlSetDieStackData( g_stackId s_dataType g_newValue ) => t/nil",
    # the printed declaration prints the callee without the trailing "s"
    # (title/TOC/APL all spell axlPurgePadstacks)
    ("06intedt", "821249", "axlPurgePadstacks"):
        "axlPurgePadstacks( S_mode ) => x_cnt",
    # the second overload prints its quoted-symbol argument as "status'"
    # (apostrophe after the word); the call takes the quoted symbol 'status
    ("07dbaccs", "739500", "axlBackdrillGet"): [
        "axlBackdrillGet( o_dbidPinOrVia ) => lt_backdrillData/nil",
        "axlBackdrillGet( 'status ) => g_status",
    ],
    # the printed declaration lists only g_option while the Arguments table
    # documents the dbid/subclass/position calling conventions
    ("04parmgt", "1169205", "axlXSectionDelete"):
        "axlXSectionDelete( g_option/o_xsectionDBID/t_etchSubclass/x_position ) => lt_types",
    # the printed declaration garbles the mode argument ("[ g_mode ]/[l g_mode ]");
    # the Arguments table documents the option and list-of-options forms
    ("17dbtran", "1065349", "axlDBCloak"):
        "axlDBCloak( g_func [ s_mode/ls_mode ] ) => g_return",
    # the printed declaration has a stray ")" closing the parameter group
    # before ?xhatch, then a second stray ")" at the end
    ("20plyopr", "1076123", "axlPolyFromDB"):
        "axlPolyFromDB( o_dbid/r_path ?endCapType s_endCapType ?layer t_layer ?padType s_padType ?holes t/nil ?line2poly t/nil ?xhatch t/nil ) => lo_polygon/nil",
    # the printed declaration calls the first parameter t_fileType while the
    # Arguments table and Description document it as t_id ("from fileops.txt")
    ("21filacc", "650496", "axlDMFileBrowse"):
        "axlDMFileBrowse( t_id g_writeFlag [?defaultName t_defaultName ] [?helpTag t_helpTag ] [?directorySet g_directorySet ] [?noDirectoryButton g_noDirectoryButton ] [?mainFile g_mainFile ] [?noSticky g_noSticky ] [?title t_title ] [?optFilters t_filters ] ) => t_fileName/nil",
    # the printed declaration says g_spacerId while the Arguments table
    # documents g_spacerName ("name or dbid of the spacer")
    ("sipapd", "1078110", "axlSetSpacerData"):
        "axlSetSpacerData( g_spacerName s_dataType g_newValue ) => t/nil",
    # the printed declaration drops the "=>" arrow (") t/nil"); parameters per
    # the section's Arguments table
    ("05selfnd", "580660", "axlSetFindFilter"):
        "axlSetFindFilter( ?enabled lt_enabled ?onButtons lt_filterOn ) => t/nil",
    # the printed declaration drops the "=>" arrow (") lt_symbols/nil")
    ("07dbaccs", "739212", "axlAltSymbolList"):
        "axlAltSymbolList( t_name/o_dbid g_layer ) => lt_symbols/nil",
    # the printed declaration drops the "=>" arrow (") t/nil")
    ("08intprm", "624549", "axlDesignFlip"):
        "axlDesignFlip( g_flip ) => t/nil",
    # the printed declaration drops the "=>" arrow (") t/nil")
    ("10usrint", "390814", "axlUIMenuDelete"):
        "axlUIMenuDelete( x_menuId ) => t/nil",
    # the printed declaration drops the "=>" arrow (") r_form/nil")
    ("11frmint", "477426", "axlFormTest"):
        "axlFormTest( t_formName ) => r_form/nil",
    # the printed declaration drops the "=>" arrow (") g_currentValue/ls_names")
    ("14dsnctl", "690074", "axlDBControl"):
        "axlDBControl( s_name [g_value] ) => g_currentValue/ls_names",
    # the printed declaration drops the "=>" arrow (") t/nil"); the argument
    # is the literal t or nil per the Arguments table
    ("23utils", "756141", "axlDebug"):
        "axlDebug( t/nil ) => t/nil",
    # the printed declaration is C-style ("list axlGetWireProfileDefinition(profileName)");
    # nil queries all profiles per the Description, and failure returns an
    # error string per Value Returned
    ("sipapd", "1078975", "axlGetWireProfileDefinition"):
        "axlGetWireProfileDefinition( t_profileName/nil ) => l_profileDef/t_errorString",
}
# Entries exempt from the arguments-table cross-check (R4) because the source
# document's table rows are not parameters of this call form at all, or the
# source itself wobbles between two spellings of the same parameter.
TABLE_SKIP_R4: set = {
    # g_form/t_callback/s_callback are rows of the g_formAction "Action
    # Options" sub-table, not parameters of axlFormCreate
    ("11frmint", "414342", "axlFormCreate"),
    # the source table spells the title/filters options g_title/g_filters
    # while the declaration spells them ?title t_title / ?optFilters t_filters
    ("21filacc", "650496", "axlDMFileBrowse"),
    # the source table documents the two alternate call forms generically
    # (l_point / ll_line) while the declaration names the points l_point1/2
    ("24mthutl", "1085632", "axlDistance"),
    # the source table documents the net arguments generically (o_net/t_net)
    # while the declaration names the pair o_net1/t_net1/o_net2/t_net2
    ("26logacc", "1075197", "axlDiffPair"),
}


class Block(NamedTuple):
    kind: str  # "h3", "h4", "decl", "p", "table", "example"
    anchor: Optional[str]
    payload: object


class Entry(NamedTuple):
    name: str
    anchor: str
    declarations: List[str]
    sections: Dict[str, List[Block]]


def _render_inline(runs: Sequence[Tuple[str, bool]]) -> str:
    """Render inline runs to markdown, wrapping Courier runs in backticks."""
    parts: List[str] = []
    for text, is_code in runs:
        text = text.replace("\xa0", " ")
        if not text:
            continue
        if is_code:
            parts.append(f"`{text.strip()}`" if text.strip() else "")
        else:
            parts.append(text)
    rendered = "".join(parts)
    rendered = re.sub(r"`\s+`", " ", rendered)
    rendered = re.sub(r"\s+`", " `", rendered)
    rendered = re.sub(r"`\s+", "` ", rendered)
    return re.sub(r"[ \t]{2,}", " ", rendered).strip()


def _normalize_declaration(text: str) -> str:
    declaration = re.sub(r"\s+", " ", text).strip()
    # stray backticks in the printed sources are markup artifacts; a printed
    # ``}`` closes an optional-argument bracket (e.g. ``[`line}` → ``['line]``)
    declaration = declaration.replace("`", "").replace("}", "]")
    declaration = (
        declaration.replace("==>", "=>").replace("⇒", "=>").replace("-->", "=>").replace("->", "=>")
    )
    declaration = re.sub(r"\s*=>\s*", " => ", declaration)
    declaration = re.sub(r"([A-Za-z0-9_\)\]])\s*\?", r"\1 ?", declaration)
    # the printed "repeatable pairs" marker is a four-dot ellipsis
    declaration = re.sub(r"\.{4,}", "...", declaration)
    return declaration.strip()


def _repair_declaration(declaration: str) -> str:
    """Repair printed signatures whose parens were lost in the HTML export."""
    if "(" not in declaration and ")" in declaration:
        declaration = re.sub(r"^([A-Za-z][A-Za-z0-9_]*)\s*", r"\1( ", declaration, count=1)
    if declaration.count("(") > declaration.count(")"):
        declaration = re.sub(r"\s*=>\s*", " ) => ", declaration, count=1)
    return declaration


def _is_bullet_table(rows: Sequence[Sequence[str]]) -> bool:
    """True for the CHM bullet-point layout tables that caption overloads.

    They carry one or two rows whose first cell holds only the bullet image,
    unlike content tables (Arguments etc.) whose first cells are header text.
    """
    return len(rows) <= 2 and all(not row[0].strip() for row in rows if row)


def _is_declaration(text: str) -> bool:
    return "=>" in text or "->" in text or "⇒" in text


# a paragraph that opens a declaration printed without a <dl> wrapper
DECL_CALL_START = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*\(")


def _declaration_complete(text: str) -> bool:
    """True when the pending text is a full signature (arrow + balanced parens)."""
    normalized = _normalize_declaration(text)
    return "=>" in normalized and normalized.count("(") == normalized.count(")")


def _canonical_section(raw: str) -> Optional[str]:
    return SECTION_LABELS.get(raw.strip().rstrip(":").strip().casefold())


class _ChapterParser(HTMLParser):
    """Reduce one chapter HTML file into an ordered list of blocks.

    The declaration zone is everything between an anchored ``<h3>`` and the
    next ``<h3>``/``<h4>``; ``<dd>`` tags inside it are the encoded whitespace
    of the printed signature. Courier-faced ``<font>`` spans are inline code.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: List[Block] = []
        self.heading: Optional[List[object]] = None  # [level, anchor, runs]
        self.decl_parts: List[str] = []
        self.in_decl = False
        # while in_decl, a <p> is parked here until </p> reveals whether it
        # continues a split declaration, separates overloads ("or"), or opens
        # the prose zone
        self.decl_para: Optional[List[str]] = None
        # a <dl> after a caption paragraph may still carry the declaration;
        # it is buffered until </dl> proves an arrow is present
        self.dl_buffer: Optional[List[str]] = None
        self.had_decl_since_h3 = False
        self.seen_h4_since_h3 = False
        self.code_depth = 0
        self.example_depth = 0
        self.skip_depth = 0
        # table state is a stack: the CHM tables nest bullet-list tables inside
        # a cell, and only the outermost table is emitted as a table block
        self.tables: List[List[List[str]]] = []
        self.rows: List[Optional[List[str]]] = []
        self.cells: List[Optional[List[Tuple[str, bool]]]] = []
        self.runs: List[Tuple[str, bool]] = []

    def _flush_declaration(self) -> None:
        """Emit the pending declaration text as a decl block.

        The printed signature may be split across several ``<dl>`` elements
        (parameters in one, the return in another), so every ``<dl>`` in the
        declaration zone is kept and the pieces are reassembled later.  Parts
        are concatenated without separators: entity references like ``&#47;``
        split a single token into several data events, and the encoded
        whitespace is carried by the ``<dd>`` separator parts alone.
        """
        text = _normalize_declaration("".join(self.decl_parts))
        self.decl_parts = []
        if text:
            self.had_decl_since_h3 = True
            self.blocks.append(Block("decl", None, text))

    # -- tag handling ----------------------------------------------------
    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        attributes = dict(attrs or {})
        if self.skip_depth:
            if tag in ("script", "style"):
                self.skip_depth += 1
            return
        if tag in ("script", "style"):
            self.skip_depth += 1
            return
        if tag == "dd":
            if self.decl_para is not None:
                self.decl_para.append(" ")
            elif self.dl_buffer is not None:
                self.dl_buffer.append(" ")
            elif self.in_decl:
                self.decl_parts.append(" ")
            else:
                self.runs.append((" ", False))
            return
        if tag == "font":
            if "Courier" in attributes.get("face", ""):
                self.code_depth += 1
            return
        if tag == "a":
            name = attributes.get("name")
            if name and self.heading is not None:
                self.heading[1] = name
            return
        if tag in ("h1", "h2", "h3", "h4"):
            if tag == "h4":
                self.seen_h4_since_h3 = True
            self._close_declaration_zone()
            self.heading = [tag, None, []]
            return
        if tag == "p":
            if self.in_decl and (not self.cells or self.cells[-1] is None):
                # a paragraph interrupts the declaration zone; park its text
                # until </p> shows whether it continues a split declaration,
                # separates overloads ("or"), or opens the prose zone
                self.decl_para = []
            return
        if tag == "dl":
            if self.in_decl:
                # one printed declaration per <dl>; a section may document
                # several (e.g. the arc family under one heading)
                self._flush_declaration()
            elif (
                not self.seen_h4_since_h3
                and not self.had_decl_since_h3
                and self.dl_buffer is None
                and (not self.cells or self.cells[-1] is None)
            ):
                # a caption paragraph may have closed the declaration zone
                # before the declaration itself; buffer the <dl> until </dl>
                # proves whether it carries one
                self.dl_buffer = []
            return
        if tag == "table":
            self.tables.append([])
            self.rows.append(None)
            self.cells.append(None)
            return
        if tag == "tr":
            if self.tables:
                self.rows[-1] = []
            return
        if tag in ("td", "th"):
            if self.tables and self.rows[-1] is not None:
                self.cells[-1] = []
            return
        if tag == "blockquote":
            # examples never belong to the declaration zone
            self._close_declaration_zone()
            self.example_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.skip_depth:
            if tag in ("script", "style"):
                self.skip_depth -= 1
            return
        if tag in ("h1", "h2", "h3", "h4"):
            if self.heading is not None and self.heading[0] == tag:
                level, anchor, runs = self.heading
                self.heading = None
                text = _render_inline(runs)
                if anchor is not None and text:
                    self.blocks.append(Block(level, anchor, text))
                    if level == "h3":
                        self.in_decl = True
                        self.decl_parts = []
                        self.had_decl_since_h3 = False
                        self.seen_h4_since_h3 = False
                        self.dl_buffer = None
                elif level == "h3":
                    self.in_decl = False  # bare page furniture; drop
            return
        if tag == "font":
            if self.code_depth:
                self.code_depth -= 1
            return
        if tag == "p":
            if self.decl_para is not None:
                text = _normalize_declaration("".join(self.decl_para))
                self.decl_para = None
                if text.strip().casefold() in DECL_SEPARATORS:
                    return  # overload separator: stay in the declaration zone
                pending = _normalize_declaration("".join(self.decl_parts))
                if pending and not _declaration_complete(pending):
                    # the declaration is split across elements (the closing
                    # paren and return often live in their own <p>)
                    self.decl_parts.append(text)
                    return
                if not pending and not self.had_decl_since_h3 and DECL_CALL_START.match(text):
                    # the whole declaration is printed as plain paragraphs
                    self.decl_parts.append(text)
                    return
                self._flush_declaration()
                self.in_decl = False
                if text:
                    self.blocks.append(Block("p", None, text))
                return
            if (not self.cells or self.cells[-1] is None) and self.heading is None:
                text = self._flush_runs()
                if text:
                    self.blocks.append(Block("p", None, text))
            return
        if tag == "dl":
            if self.dl_buffer is not None:
                text = _normalize_declaration("".join(self.dl_buffer))
                self.dl_buffer = None
                if _is_declaration(text) or DECL_CALL_START.match(text):
                    # the buffered <dl> opens the declaration (the arrow may
                    # sit in a later fragment); re-enter the zone so the
                    # continuation <dl>s keep collecting
                    self.in_decl = True
                    self.decl_parts = [text]
                    self._flush_declaration()
                elif text:
                    self.runs.append((text, False))
            return
        if tag in ("td", "th"):
            if self.cells and self.cells[-1] is not None:
                rendered = _render_inline(self.cells[-1])
                self.cells[-1] = None
                if self.rows and self.rows[-1] is not None:
                    self.rows[-1].append(rendered)
            return
        if tag == "tr":
            if self.rows and self.rows[-1] is not None and self.tables:
                row = self.rows[-1]
                self.rows[-1] = None
                if any(cell for cell in row):
                    self.tables[-1].append(row)
            return
        if tag == "table":
            if self.tables:
                rows = self.tables.pop()
                self.rows.pop()
                self.cells.pop()
                if not rows:
                    return
                if self.tables:
                    # nested table: fold its text into the enclosing cell
                    flattened = "; ".join(
                        "; ".join(cell for cell in row if cell) for row in rows
                    )
                    if flattened and self.cells and self.cells[-1] is not None:
                        self.cells[-1].append((flattened, False))
                else:
                    if self.in_decl and _is_bullet_table(rows):
                        # bullet-layout label between overloaded declarations:
                        # keep the zone open and hold the caption as its own
                        # declaration-zone block
                        self._flush_declaration()
                        caption = " ".join(
                            cell.strip() for row in rows for cell in row if cell.strip()
                        )
                        if caption:
                            self.blocks.append(Block("decl", None, caption))
                        return
                    self._close_declaration_zone()
                    self.blocks.append(Block("table", None, rows))
            return
        if tag == "blockquote":
            if self.example_depth:
                self.example_depth -= 1
                text = self._flush_runs()
                if text:
                    self.blocks.append(Block("example", None, text))

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.heading is not None:
            self.heading[2].append((data, False))
            return
        if self.decl_para is not None:
            self.decl_para.append(re.sub(r"\s+", " ", data))
            return
        if self.dl_buffer is not None:
            self.dl_buffer.append(re.sub(r"\s+", " ", data))
            return
        # table cells come before the declaration zone: bullet-layout tables
        # sit inside it and must not leak their captions into the signature
        if self.cells and self.cells[-1] is not None:
            self.cells[-1].append((data, self.code_depth > 0))
            return
        if self.in_decl:
            self.decl_parts.append(re.sub(r"\s+", " ", data))
            return
        self.runs.append((data, self.code_depth > 0))

    # -- buffers ----------------------------------------------------------
    def _close_declaration_zone(self) -> None:
        """Flush the pending declaration zone and end it."""
        if not self.in_decl:
            return
        self.in_decl = False
        self._flush_declaration()
        if self.decl_para is not None:
            text = _normalize_declaration("".join(self.decl_para))
            self.decl_para = None
            if text and text.strip().casefold() not in DECL_SEPARATORS:
                self.blocks.append(Block("p", None, text))

    def _flush_runs(self) -> str:
        text = _render_inline(self.runs)
        self.runs = []
        return text

    def close(self) -> None:
        super().close()
        self._close_declaration_zone()
        text = self._flush_runs()
        if text:
            self.blocks.append(Block("p", None, text))


def parse_chapter(html_text: str) -> List[Block]:
    parser = _ChapterParser()
    parser.feed(html_text)
    parser.close()
    return parser.blocks


def collect_entries(blocks: Sequence[Block]) -> List[Entry]:
    entries: List[Entry] = []
    name: Optional[str] = None
    anchor: Optional[str] = None
    declarations: List[str] = []
    sections: Dict[str, List[Block]] = {}
    # prose before the first section label (redirect notes like "See
    # axlCancelOn.") belongs to the Description
    active: Optional[str] = "Description"
    for block in blocks:
        if block.kind == "h3":
            if name is not None and anchor is not None:
                entries.append(Entry(name, anchor, declarations, sections))
            name, anchor, declarations = str(block.payload), block.anchor, []
            sections, active = {}, "Description"
            continue
        if name is None:
            continue
        if block.kind == "decl":
            declarations.append(str(block.payload))
            continue
        if block.kind == "h4":
            active = _canonical_section(str(block.payload))
            if active is not None:
                sections.setdefault(active, [])
            continue
        if block.kind == "p":
            # some chapters mark the section label with <p> instead of <h4>
            promoted = _canonical_section(str(block.payload))
            if promoted is not None:
                active = promoted
                sections.setdefault(active, [])
                continue
        if active is not None:
            sections.setdefault(active, []).append(block)
    if name is not None and anchor is not None:
        entries.append(Entry(name, anchor, declarations, sections))
    return entries


def _redistribute_sibling_declarations(
    entries: List[Entry],
) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
    """Move sibling signatures from a combined section to their own entries.

    Function families print as consecutive bare ``<h3>`` headings whose
    declarations all sit in the last sibling's declaration zone (the
    ``axlPathArcRadius``/``Angle``/``Center`` pattern).  Attaching each
    declaration to the entry it names lets the index and the signature gate
    see every form.  Returns the moved declarations keyed by the donor
    entry's anchor (so the donor's arguments-table union still covers them)
    and a sibling-anchor → donor-anchor map (so the sibling's shape check can
    treat the family's shared Arguments table as its documented set).
    """
    moved: Dict[str, List[str]] = {}
    donor_of: Dict[str, str] = {}
    for index, donor in enumerate(entries):
        if not donor.declarations:
            continue
        # walk back over the run of bare headings immediately preceding the
        # donor; each joins the family when the donor carries its declaration
        cursor = index - 1
        while cursor >= 0:
            previous = entries[cursor]
            if previous.declarations or previous.sections:
                break
            matched = None
            for declaration in list(donor.declarations):
                repaired = _repair_declaration(declaration)
                callee = repaired.split("(", 1)[0].strip()
                if callee.casefold() == previous.name.casefold() and _is_declaration(repaired):
                    matched = declaration
                    break
            if matched is None:
                break
            previous.declarations.append(matched)
            donor.declarations.remove(matched)
            moved.setdefault(donor.anchor, []).append(matched)
            donor_of[previous.anchor] = donor.anchor
            cursor -= 1
    return moved, donor_of


def render_table(rows: Sequence[Sequence[str]]) -> List[str]:
    body = [row for row in rows if not _is_header_row(row)]
    if not body:
        return []
    # Bullet-list tables produced by the CHM exporter: the first cell holds the
    # bullet image (now empty after tag stripping) and the second cell holds the
    # list text. Render them as real Markdown lists instead of empty-Name tables.
    if all(not (row[0] if row else "").strip() for row in body if row):
        lines: List[str] = []
        for row in body:
            if not row:
                continue
            text = "; ".join(cell for cell in row[1:] if cell).strip()
            if text:
                lines.append(f"- {text}")
        return lines
    # Continuation rows (first column empty, often &nbsp;) belong to the
    # previous parameter; merge them into its Description cell.
    merged: List[List[str]] = []
    for row in body:
        if not row:
            continue
        name_cell = row[0].strip()
        description = "; ".join(cell for cell in row[1:] if cell).strip()
        if not name_cell and merged and description:
            merged[-1][1] += "<br><br>" + description
        elif name_cell:
            merged.append([name_cell, description])
        elif description:
            merged.append([name_cell, description])
    lines = ["| Name | Description |", "|---|---|"]
    for name_cell, description in merged:
        lines.append(f"| {name_cell} | {description} |")
    return lines


def _is_header_row(row: Sequence[str]) -> bool:
    return len(row) >= 2 and {
        row[0].strip().strip("`").casefold(),
        row[1].strip().strip("`").casefold(),
    } <= TABLE_HEADER_CELLS


def _table_parameter_names(entry: Entry) -> List[str]:
    """Backticked parameter names from the rendered Arguments tables.

    Optional-argument brackets (``[g_include_voids]``) are stripped first so
    the name inside them still matches the signature token.
    """
    names: List[str] = []
    for block in entry.sections.get("Arguments", []):
        if block.kind != "table":
            continue
        for row in block.payload:
            if row:
                # one cell may list alternatives (``o_dbid/lo_dbid``); each is
                # a documented parameter name
                for cell in row[0].replace("[", "").replace("]", "").split("/"):
                    names.extend(ARGUMENT_NAME.findall(cell))
    return names


def _missing_table_atoms(
    entry: Entry, table_names: Sequence[str], selected: Sequence[str] = ()
) -> List[str]:
    """Arguments-table parameters that no declaration in the section covers.

    ``selected`` holds the rendered (possibly overridden) signatures, which
    count as covering their documented parameters even when the printed
    declaration zones were garbled.
    """
    if not table_names:
        return []
    atoms: set = set()
    for declaration in list(entry.declarations) + list(selected):
        parameter_text = _parameter_text(declaration)
        if parameter_text is None:
            continue
        atoms |= {
            atom.casefold()
            for atom in _split_atoms(parameter_text)
            if PREFIXED_ATOM.match(atom)
        }
    table_atoms = {name.casefold() for name in table_names}
    return sorted(table_atoms - atoms)


def render_entry(entry: Entry, signature_items: Sequence[Tuple[str, str]]) -> str:
    """Render one API entry.

    ``signature_items`` is an ordered list of ``("signature", text)`` and
    ``("note", text)`` pairs; notes are the bullet captions the source prints
    between overloaded call forms.  A bare ``or`` separates two consecutive
    signatures with no caption of their own.
    """
    lines = [f"### {entry.name}", ""]
    previous: Optional[str] = None
    for kind, text in signature_items:
        if kind == "note":
            lines += [text, ""]
        else:
            if previous == "signature":
                lines += ["or", ""]
            lines += [f"`{text}`", ""]
        previous = kind
    if not signature_items and entry.declarations:
        # documentation-prose sections (callback interfaces, primitive
        # tables): the declaration zone holds prose, not a signature
        for declaration in entry.declarations:
            lines.append(declaration)
            lines.append("")
    for label in ("Description", "Arguments", "Value Returns", "Examples", "See Also"):
        blocks = entry.sections.get(label)
        if not blocks:
            continue
        lines.append(f"#### {label}")
        lines.append("")
        for block in blocks:
            if block.kind == "table":
                lines.extend(render_table(block.payload))
                lines.append("")
            else:
                lines.append(str(block.payload))
                lines.append("")
    return "\n".join(lines).rstrip() + "\n\n"


def _clean_heading(value: str) -> str:
    """Strip markup, obsolete qualifiers, and trailing () from a heading."""
    cleaned = value.replace("`", "").replace("\\_", "_").strip()
    cleaned = re.sub(r"\s+-\s+Obsolete.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\(\)\s*$", "", cleaned)
    return cleaned.strip()


API_HEADING = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*$"
)


def _is_api_heading(name: str) -> bool:
    """True when the heading text is one or more API identifiers.

    Headings like ``Callback Procedure: formCallback`` or ``Input/Output
    Data Primitives`` are documentation prose; they are rendered without a
    signature so the index builder never treats them as API entries.
    """
    return bool(API_HEADING.match(name))


def _matching_declarations(name: str, declarations: Sequence[str]) -> List[str]:
    """All well-formed declarations whose callee is the heading name.

    Overloaded APIs print one declaration per call form
    (``axlDBCreateSymbolSkeleton``); all of them belong in the rendered entry.
    Split-across-``<dl>`` fragments are not declarations on their own and are
    filtered out, leaving the concatenation fallback to
    ``_select_declaration``.
    """
    matches: List[str] = []
    for declaration in declarations:
        repaired = _repair_declaration(declaration)
        callee = repaired.split("(", 1)[0].strip()
        if callee.casefold() == name.casefold() and _is_declaration(repaired):
            matches.append(repaired)
    return matches


def _select_declaration(name: str, declarations: Sequence[str]) -> str:
    """Pick the best declaration for a heading from the section's ``<dl>``s.

    Preference order: a single complete declaration whose callee matches the
    heading (multi-function sections like the arc family); else the
    reassembled concatenation when it forms one signature (signatures split
    across ``<dl>`` elements - the closing paren and return often sit in
    their own ``<dl>``s); else the first complete declaration.
    """
    if not declarations:
        return ""
    for declaration in declarations:
        callee = declaration.split("(", 1)[0].strip().casefold()
        if callee == name.casefold() and _is_declaration(declaration):
            return _repair_declaration(declaration)
    # drop leading caption fragments (bullet labels) before reassembling
    start = 0
    for index, declaration in enumerate(declarations):
        if declaration.lstrip().startswith(name):
            start = index
            break
    combined = _repair_declaration(_normalize_declaration(" ".join(declarations[start:])))
    if _is_declaration(combined) and combined.count("=>") == 1:
        return combined
    for declaration in declarations:
        if declaration.startswith(name) and _is_declaration(declaration):
            return _repair_declaration(declaration)
    return _repair_declaration(declarations[0])


def _reassemble_declarations(
    name: str, declarations: Sequence[str]
) -> List[Tuple[str, str]]:
    """Reassemble declarations split across consecutive ``<dl>`` fragments.

    Bullet captions and fragment groups interleave (the axlDiffPair pattern):
    each call form prints as a ``name(`` fragment, parameter fragments, a
    ``)`` fragment, and the arrow fragment, with bullet captions between the
    groups. Fragments accumulate from each ``name``-starting fragment until
    the concatenation is a complete declaration; everything else (captions,
    incomplete tails) is kept as a note so overload captions still render.
    Returns ("signature" | "note", text) items in source order.
    """
    items: List[Tuple[str, str]] = []
    pending: List[str] = []
    for raw_declaration in declarations:
        text = _normalize_declaration(raw_declaration)
        if pending or text.lstrip().startswith(name):
            pending.append(text)
            combined = _repair_declaration(_normalize_declaration(" ".join(pending)))
            if _is_declaration(combined) and _declaration_complete(combined):
                callee = combined.split("(", 1)[0].strip()
                kind = "signature" if callee.casefold() == name.casefold() else "note"
                items.append((kind, combined))
                pending = []
        else:
            items.append(("note", _repair_declaration(text)))
    items.extend(("note", fragment) for fragment in pending)
    return items


def _apl_oracle(source_dir: Path) -> List[Tuple[str, str]]:
    """Parse (chapter, anchor) pairs from the APL HTML.

    APL labels that carry no name (bare page numbers like ``1236``) are
    navigation furniture, not APIs, and are excluded from the oracle.
    """
    text = (source_dir / f"{DOCUMENT}APL.html").read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(
        r'<a href="(?P<chapter>[0-9A-Za-z_]+)\.html#(?P<anchor>\d+)"[^>]*>(?P<label>.*?)</a>',
        re.DOTALL,
    )
    pairs: List[Tuple[str, str]] = []
    for match in pattern.finditer(text):
        label = re.sub(r"<[^>]+>", "", match.group("label")).strip()
        if not re.search(r"[A-Za-z_]", label):
            continue
        pairs.append((match.group("chapter"), match.group("anchor")))
    return pairs


def _estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def split_parts(source_stem: str, rendered_entries: Sequence[str]) -> List[Tuple[str, str]]:
    total = _estimate_tokens("".join(rendered_entries))
    if total <= PART_TOKEN_TARGET:
        return [(f"{source_stem}.md", "".join(rendered_entries))]
    chunks: List[List[str]] = [[]]
    current = 0
    for rendered in rendered_entries:
        size = _estimate_tokens(rendered)
        if chunks[-1] and current + size > PART_TOKEN_TARGET:
            chunks.append([])
            current = 0
        chunks[-1].append(rendered)
        current += size
    outputs: List[Tuple[str, str]] = []
    for index, chunk in enumerate(chunks, start=1):
        text = "".join(chunk)
        header = (
            "<!--\n"
            f"source: {DOCUMENT}/{source_stem}.md\n"
            f"part: {index}/{len(chunks)}\n"
            f"estimated_tokens: {_estimate_tokens(text)}\n"
            "-->\n\n"
        )
        outputs.append((f"{source_stem}.part{index:02d}.md", header + text))
    return outputs


def build(root: Path) -> Dict[str, str]:
    source_dir = root / "docs" / "html" / DOCUMENT
    if not source_dir.is_dir():
        raise RuntimeError(f"missing HTML source directory: {source_dir}")
    chapter_blocks: Dict[str, List[Block]] = {}
    for path in sorted(source_dir.glob("*.html")):
        if path.stem in SKIP_STEMS:
            continue
        chapter_blocks[path.stem] = parse_chapter(path.read_text(encoding="utf-8", errors="replace"))

    oracle = _apl_oracle(source_dir)
    if len(oracle) != EXPECTED_APL_LINKS:
        raise RuntimeError(
            f"APL anchor count changed: expected {EXPECTED_APL_LINKS}, found {len(oracle)}"
        )
    oracle_set = set(oracle)
    resolved: set = set()

    outputs: Dict[str, str] = {}
    gate_failures: List[str] = []
    gate_warnings: List[str] = []
    for stem, blocks in chapter_blocks.items():
        rendered: List[str] = []
        entries = collect_entries(blocks)
        redistributed, donor_of = _redistribute_sibling_declarations(entries)
        tables_by_anchor = {entry.anchor: _table_parameter_names(entry) for entry in entries}
        for entry in entries:
            is_indexed = (stem, entry.anchor) in oracle_set
            if is_indexed:
                resolved.add((stem, entry.anchor))
            name = _clean_heading(entry.name)
            if not _is_api_heading(name):
                rendered.append(render_entry(entry, ()))
                continue
            override = SIGNATURE_OVERRIDES.get((stem, entry.anchor, name))
            declaration = _select_declaration(name, entry.declarations)
            reassembled: List[Tuple[str, str]] = []
            if override is None and not _is_declaration(declaration):
                reassembled = _reassemble_declarations(name, entry.declarations)
                if not any(kind == "signature" for kind, _ in reassembled):
                    if not is_indexed and not entry.sections:
                        continue  # auxiliary prose heading with no content
                    rendered.append(render_entry(entry, ()))
                    continue
            if override is not None:
                signatures = [override] if isinstance(override, str) else list(override)
                signature_items = [("signature", text) for text in signatures]
            elif reassembled:
                signature_items = reassembled
                signatures = [text for kind, text in reassembled if kind == "signature"]
            else:
                signatures = _matching_declarations(name, entry.declarations)
                if not signatures:
                    signatures = [declaration]
                if len(signatures) > 1:
                    # keep the bullet captions printed between overloads
                    signature_items = []
                    for raw_declaration in entry.declarations:
                        repaired = _repair_declaration(raw_declaration)
                        callee = repaired.split("(", 1)[0].strip()
                        if callee.casefold() == name.casefold() and _is_declaration(repaired):
                            signature_items.append(("signature", repaired))
                        elif not _is_declaration(repaired):
                            signature_items.append(("note", repaired))
                else:
                    signature_items = [("signature", signatures[0])]
            entry = entry._replace(name=name)
            rendered.append(render_entry(entry, signature_items))
            if is_indexed:
                table_names = _table_parameter_names(entry)
                # a redistributed sibling shares the family section's
                # Arguments table as its documented set (shape check only;
                # the table cross-check stays against its own table)
                shape_table_names = table_names
                donor_anchor = donor_of.get(entry.anchor)
                if donor_anchor is not None:
                    shape_table_names = table_names + tables_by_anchor.get(donor_anchor, [])
                for signature in signatures:
                    check_entry = BodyEntry(
                        name=name,
                        signature=signature,
                        path=f"{DOCUMENT}/{stem}.md",
                        line=0,
                        is_axl=True,
                    )
                    for severity, reason in check_signature_shape(check_entry, shape_table_names):
                        if severity == "error":
                            gate_failures.append(f"{stem}#{entry.anchor} {name}: {reason}")
                # the Arguments table may document alternate/overload call
                # forms; the ground truth is the union of every declaration in
                # the section, so one straggler only warns while two or more
                # lost parameters mean the conversion dropped tokens
                if (stem, entry.anchor, name) in TABLE_SKIP_R4:
                    continue
                missing = _missing_table_atoms(
                    entry,
                    table_names,
                    selected=list(signatures) + redistributed.get(entry.anchor, []),
                )
                if len(missing) >= 2:
                    gate_failures.append(
                        f"{stem}#{entry.anchor} {name}: arguments table documents "
                        f"{sorted(missing)} missing from every signature"
                    )
                elif missing:
                    gate_warnings.append(
                        f"{stem}#{entry.anchor} {name}: arguments table documents "
                        f"{sorted(missing)} missing from every signature"
                    )
        for filename, content in split_parts(stem, rendered):
            outputs[f"{DOCUMENT}/{filename}"] = content

    missing = [pair for pair in oracle_set if pair not in resolved]
    if missing:
        raise RuntimeError(
            f"{len(missing)} APL anchors did not resolve to an API section, "
            f"first: {missing[:5]}"
        )
    if gate_warnings:
        for warning in gate_warnings:
            print(f"warning: {warning}")
    if gate_failures:
        raise RuntimeError(
            "signature gate rejected the conversion:\n  " + "\n  ".join(gate_failures)
        )
    return outputs


def check(root: Path) -> Tuple[bool, List[str]]:
    outputs = build(root)
    errors: List[str] = []
    for relative, content in sorted(outputs.items()):
        path = root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            errors.append(f"stale converted document: {relative}; run the converter again")
    return (not errors, errors)


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1] / "skill-references"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=_default_root())
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    if arguments.check:
        ok, errors = check(root)
        for error in errors:
            print(f"error: {error}")
        return 0 if ok else 1
    outputs = build(root)
    document_dir = root / DOCUMENT
    written = set()
    for relative, content in sorted(outputs.items()):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.add(target.name)
    for stale in sorted(document_dir.glob("*.md")):
        if stale.name not in written and stale.name not in KEEP_FILES:
            stale.unlink()
    print(f"converted {len(outputs)} documents under {document_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
