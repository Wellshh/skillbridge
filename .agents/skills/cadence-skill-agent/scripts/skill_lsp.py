#!/usr/bin/env python3
"""A minimal language server for SKILL, backed by the corpus validators.

Thin JSON-RPC shell over the existing analysis primitives - no parsing or
scoring logic lives here:

- **diagnostics** come from ``validate_skill_api.validate_text`` (unknown
  ``axl*`` API, arity, unknown-keyword), recomputed on open/change.
- **hover** and **completion** come from the corpus indexes via
  ``search_api`` (signature, ``source:line``, description snippet).

Severity layering matters: the corpus has known gaps (genuine Allegro APIs
such as ``axlXSection*`` are absent), so ``unknown-api`` diagnostics keep the
validator's message that names the escape hatch (``isCallable`` on the target
Windows Allegro) instead of asserting the symbol does not exist.  The real
authority remains the Windows gate; this server is the fast inner loop.

Scope (deliberately small): full-document sync, hover, completion,
diagnostics.  No workspace symbols, no formatting, no cross-file analysis.

Run over stdio::

    python3 .claude/scripts/skill_lsp.py

Configure an editor with ``.il``/``.ils`` filetypes pointing at this command.
"""

from __future__ import annotations

import json
import re
import sys
from operator import itemgetter
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from search_api import _load_index, attach_descriptions
from validate_skill_api import (
    IDENTIFIER,
    load_corpus,
    load_verified_callables,
    validate_text,
)

# LSP DiagnosticSeverity
_SEVERITY = {"error": 1, "warning": 2, "information": 3, "hint": 4}

MAX_COMPLETIONS = 50
HOVER_DESCRIPTION_LIMIT = 300

_IDENTIFIER_CHAR = re.compile(r"[A-Za-z0-9_!?<>*+\-]")


def _identifier_at(line_text: str, character: int) -> Optional[Tuple[str, int, int]]:
    """The identifier spanning (or touching) ``character`` in a 0-based line.

    Returns (name, start, end) with offsets into ``line_text``, or None when
    the cursor is not on an identifier.
    """
    character = min(character, len(line_text))
    for match in re.finditer(IDENTIFIER, line_text):
        if match.start() <= character <= match.end():
            return match.group(0), match.start(), match.end()
    return None


def _word_prefix(line_text: str, character: int) -> str:
    """The partial identifier ending at the cursor, for completion."""
    prefix = []
    for char in reversed(line_text[:character]):
        if _IDENTIFIER_CHAR.match(char):
            prefix.append(char)
        else:
            break
    return "".join(reversed(prefix))


class SkillLanguageServer:
    """Method handlers; transport lives in :func:`serve` for testability."""

    def __init__(self, root: Path):
        self.root = root
        self._specs = None  # loaded lazily on first use
        self._verified_callables = None
        self._entries = None
        self.documents: Dict[str, str] = {}
        self.shutdown_requested = False

    @property
    def specs(self):
        if self._specs is None:
            self._specs = load_corpus(self.root)
        return self._specs

    @property
    def verified_callables(self):
        if self._verified_callables is None:
            self._verified_callables = load_verified_callables(self.root)
        return self._verified_callables

    @property
    def entries(self):
        if self._entries is None:
            entries = _load_index(self.root)
            attach_descriptions(self.root, entries)
            self._entries = entries
        return self._entries

    # -- message dispatch ------------------------------------------------

    def handle(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process one JSON-RPC message; return messages to send back."""
        method = message.get("method")
        params = message.get("params") or {}
        request_id = message.get("id")

        if method == "initialize":
            return [self._response(request_id, {
                "capabilities": {
                    # 1 = full-document sync: SKILL buffers are small and the
                    # validator is lexical, so incremental sync buys nothing
                    "textDocumentSync": {"openClose": True, "change": 1},
                    "hoverProvider": True,
                    "completionProvider": {"triggerCharacters": []},
                },
                "serverInfo": {"name": "skill-corpus-lsp"},
            })]
        if method == "shutdown":
            self.shutdown_requested = True
            return [self._response(request_id, None)]
        if method == "exit":
            return []
        if method == "textDocument/didOpen":
            document = params.get("textDocument", {})
            uri = document.get("uri", "")
            self.documents[uri] = document.get("text", "")
            return [self._diagnostics_notification(uri)]
        if method == "textDocument/didChange":
            uri = params.get("textDocument", {}).get("uri", "")
            changes = params.get("contentChanges", [])
            if changes:
                self.documents[uri] = changes[-1].get("text", "")
            return [self._diagnostics_notification(uri)]
        if method == "textDocument/didClose":
            uri = params.get("textDocument", {}).get("uri", "")
            self.documents.pop(uri, None)
            return [self._notification("textDocument/publishDiagnostics",
                                       {"uri": uri, "diagnostics": []})]
        if method == "textDocument/hover":
            return [self._response(request_id, self._hover(params))]
        if method == "textDocument/completion":
            return [self._response(request_id, self._completion(params))]
        # unknown requests get a MethodNotFound error; notifications are dropped
        if request_id is not None:
            return [{
                "jsonrpc": "2.0", "id": request_id,
                "error": {"code": -32601, "message": f"method not found: {method}"},
            }]
        return []

    @staticmethod
    def _response(request_id, result):
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _notification(method, params):
        return {"jsonrpc": "2.0", "method": method, "params": params}

    # -- features ----------------------------------------------------------

    def _diagnostics_notification(self, uri: str) -> Dict[str, Any]:
        text = self.documents.get(uri, "")
        findings = validate_text(text, self.specs, uri, self.verified_callables)
        diagnostics = []
        for finding in findings:
            line_index = max(finding.line - 1, 0)
            lines = text.splitlines()
            line_text = lines[line_index] if line_index < len(lines) else ""
            start = max(finding.column - 1, 0)
            token = _identifier_at(line_text, start)
            end = token[2] if token else start + 1
            diagnostics.append({
                "range": {
                    "start": {"line": line_index, "character": start},
                    "end": {"line": line_index, "character": end},
                },
                "severity": _SEVERITY.get(finding.severity, 2),
                "source": "skill-corpus",
                "code": finding.check,
                "message": finding.message,
            })
        return self._notification(
            "textDocument/publishDiagnostics", {"uri": uri, "diagnostics": diagnostics}
        )

    def _hover(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        uri = params.get("textDocument", {}).get("uri", "")
        position = params.get("position", {})
        text = self.documents.get(uri)
        if text is None:
            return None
        lines = text.splitlines()
        line_index = position.get("line", 0)
        if line_index >= len(lines):
            return None
        token = _identifier_at(lines[line_index], position.get("character", 0))
        if token is None:
            return None
        entry = self.entries.get(token[0].casefold())
        if entry is None:
            return None
        parts = [f"```\n{entry.signature}\n```", f"{entry.source}:{entry.line}"]
        if entry.description:
            snippet = entry.description[:HOVER_DESCRIPTION_LIMIT]
            if len(entry.description) > HOVER_DESCRIPTION_LIMIT:
                snippet += "..."
            parts.append(snippet)
        return {"contents": {"kind": "markdown", "value": "\n\n".join(parts)}}

    def _completion(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        uri = params.get("textDocument", {}).get("uri", "")
        position = params.get("position", {})
        text = self.documents.get(uri)
        if text is None:
            return []
        lines = text.splitlines()
        line_index = position.get("line", 0)
        line_text = lines[line_index] if line_index < len(lines) else ""
        prefix = _word_prefix(line_text, position.get("character", 0))
        if not prefix:
            return []
        lowered = prefix.casefold()
        items = []
        for key in sorted(self.entries):
            entry = self.entries[key]
            if key.startswith(lowered):
                items.append((
                    # Prefer the spelling the user actually typed.  This keeps
                    # ``axlDbidName`` visible for the natural ``axlDb`` prefix
                    # even though many ``axlDB*`` symbols sort before it.
                    not entry.name.startswith(prefix),
                    key,
                    {
                        "label": entry.name,
                        "kind": 3,  # CompletionItemKind.Function
                        "detail": entry.signature,
                        "documentation": f"{entry.source}:{entry.line}",
                    },
                ))
        items.sort(key=itemgetter(0, 1))
        return [item[2] for item in items[:MAX_COMPLETIONS]]


# ---------------------------------------------------------------------------
# stdio transport
# ---------------------------------------------------------------------------


def read_message(reader: BinaryIO) -> Optional[Dict[str, Any]]:
    """One Content-Length framed message; None on EOF."""
    content_length = None
    while True:
        header = reader.readline()
        if not header:
            return None
        header = header.strip()
        if not header:
            if content_length is not None:
                break
            continue
        if header.lower().startswith(b"content-length:"):
            content_length = int(header.split(b":", 1)[1].strip())
    if content_length is None:
        return None
    body = reader.read(content_length)
    if len(body) != content_length:
        return None
    return json.loads(body.decode("utf-8"))


def write_message(writer: BinaryIO, payload: Dict[str, Any]) -> None:
    body = json.dumps(payload).encode("utf-8")
    writer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
    writer.flush()


def serve(reader: BinaryIO, writer: BinaryIO, root: Path) -> int:
    server = SkillLanguageServer(root)
    while True:
        message = read_message(reader)
        if message is None:
            return 0  # client closed the channel
        if message.get("method") == "exit":
            return 0 if server.shutdown_requested else 1
        for outgoing in server.handle(message):
            write_message(writer, outgoing)


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path,
        default=Path(__file__).resolve().parents[1] / "skill-references",
    )
    arguments = parser.parse_args(argv)
    return serve(sys.stdin.buffer, sys.stdout.buffer, arguments.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
