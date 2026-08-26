# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

from typing import ClassVar

from skillbridge.exception import ProtocolError, SkillBridgeError

__all__ = [
    'AllegroError',
    'AllegroFileNotFoundError',
    'AllegroLaunchError',
    'AllegroProtocolError',
    'AllegroServerIdentityError',
    'AllegroTimeoutError',
    'ExtensionError',
]


class AllegroError(SkillBridgeError):
    code: ClassVar[str] = 'allegro_error'


class AllegroProtocolError(AllegroError, ProtocolError):
    code = 'allegro_protocol_error'


class AllegroLaunchError(AllegroError, RuntimeError):
    code = 'allegro_launch_error'


class AllegroFileNotFoundError(AllegroLaunchError, FileNotFoundError):
    code = 'allegro_file_not_found'


class AllegroServerIdentityError(AllegroLaunchError):
    code = 'allegro_server_identity_error'


class AllegroTimeoutError(AllegroLaunchError, TimeoutError):
    code = 'allegro_timeout'


class ExtensionError(AllegroError, RuntimeError):
    code = 'extension_error'
