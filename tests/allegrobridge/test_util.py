# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import re
from pathlib import Path

from pytest import raises

import allegrobridge.server
from allegrobridge import Allegro
from allegrobridge.util import (
    _extract_apis,  # ruff: ignore[import-private-name]
    build_snake_to_axl_map,
    extract_api_domains,
)


def test_extract_apis_reads_asset_lines(tmp_path: Path) -> None:
    (tmp_path / 'api_names.txt').write_text(
        'axlGeoRotatePt\naxlDBGetDesign\n',
        encoding='utf-8',
    )

    assert _extract_apis(tmp_path) == ['axlGeoRotatePt', 'axlDBGetDesign']


def test_extract_apis_fails_when_assets_are_missing(tmp_path: Path) -> None:
    missing = tmp_path / 'missing-assets'

    with raises(FileNotFoundError, match=re.escape(missing.name)):
        _extract_apis(missing)


def test_build_map_supports_exact_and_snake_names() -> None:
    mapping = build_snake_to_axl_map(['axlDBGetDesign'])

    assert mapping['db_get_design'] == 'axlDBGetDesign'
    assert mapping['axl_db_get_design'] == 'axlDBGetDesign'
    assert mapping['axlDBGetDesign'] == 'axlDBGetDesign'


def test_extract_api_domains_groups_by_domain() -> None:
    domains = extract_api_domains(['axlDBGetDesign', 'axlGeoRotatePt', 'not_an_axl_api'])

    assert domains == {
        'db',
        'geo',
        'root',
    }


def test_build_map_contains_real_assets() -> None:
    apis = _extract_apis()
    mapping = build_snake_to_axl_map()

    assert len(apis) == 792
    assert apis == sorted(set(apis))
    assert mapping['geo_rotate_pt'] == 'axlGeoRotatePt'
    assert mapping['axl_cns_add_via'] == 'axlCnsAddVia'


def test_allegro_server_skill_file_is_packaged() -> None:
    server_file = Path(allegrobridge.server.__file__).with_name('allegro_server.il')

    assert server_file.is_file()


def test_allegro_open_validates_mode() -> None:
    with raises(ValueError, match="mode must be 'cli' or 'manual'"):
        Allegro.open(mode='invalid')  # type: ignore[arg-type]
