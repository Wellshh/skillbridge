from __future__ import annotations

import re
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"
TOKEN_PATTERN = re.compile(r"[A-Z]+(?=[A-Z][a-z0-9]|\b)|[A-Z][a-z0-9]*|[a-z0-9]+")


def run_allegro() -> None: ...


def _split_api_tokens(api_name: str) -> list[str]:
    if "_" in api_name:
        parts: list[str] = []
        for segment in api_name.split("_"):
            parts.extend(TOKEN_PATTERN.findall(segment))
        return parts
    return TOKEN_PATTERN.findall(api_name)


def _extract_apis(assets_dir: Path | str = ASSETS_DIR) -> list[str]:
    return (Path(assets_dir) / "api_names.txt").read_text(encoding="utf-8").splitlines()


def extract_api_domains(apis: list[str] | None = None) -> set[str]:
    """Return Allegro API domain prefixes (the token following 'axl').

    Examples:
        'axlDBGetDesign' -> domain 'db'
        'axlCNSGetSpacing' -> domain 'cns'
        'axlGeoDistance' -> domain 'geo'

    Returns:
        Lowercase API domain prefixes.
    """
    if apis is None:
        apis = _extract_apis()

    domains: set[str] = set()
    for api in apis:
        tokens = _split_api_tokens(api)
        domain = tokens[1].lower() if len(tokens) > 1 and tokens[0].lower() == "axl" else "root"
        domains.add(domain)

    return domains


def build_snake_to_axl_map(apis: list[str] | None = None) -> dict[str, str]:
    """Build a comprehensive lookup dictionary mapping snake_case names to exact Allegro APIs.

    Supports:
        - Domain + action: 'db_get_design' -> 'axlDBGetDesign'
        - Full prefix: 'axl_db_get_design' -> 'axlDBGetDesign'
        - Exact name: 'axlDBGetDesign' -> 'axlDBGetDesign'

    Returns:
        Snake-case and exact-name lookup entries for Allegro APIs.
    """
    if apis is None:
        apis = _extract_apis()

    mapping: dict[str, str] = {}
    for api in apis:
        tokens = _split_api_tokens(api)
        lower_tokens = [t.lower() for t in tokens]

        mapping["_".join(lower_tokens)] = api

        if lower_tokens and lower_tokens[0] == "axl":
            mapping["_".join(lower_tokens[1:])] = api

        mapping[api] = api

    return mapping
