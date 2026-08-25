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
]


class AllegroError(SkillBridgeError):
    code: ClassVar[str] = 'allegro_error'


class AllegroProtocolError(AllegroError, ProtocolError, RuntimeError):
    code = 'allegro_protocol_error'


class AllegroLaunchError(AllegroError, RuntimeError):
    code = 'allegro_launch_error'


class AllegroFileNotFoundError(AllegroLaunchError, FileNotFoundError):
    code = 'allegro_file_not_found'


class AllegroServerIdentityError(AllegroLaunchError):
    code = 'allegro_server_identity_error'


class AllegroTimeoutError(AllegroLaunchError, TimeoutError):
    code = 'allegro_timeout'
