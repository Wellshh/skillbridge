# Exceptions

All AllegroBridge exceptions derive from `AllegroError` (which derives from
the kernel's `SkillBridgeError`). Each carries a machine-readable `code`
class attribute.

::: allegrobridge.exceptions
    options:
      members:
        - AllegroError
        - AllegroProtocolError
        - AllegroLaunchError
        - AllegroFileNotFoundError
        - AllegroServerIdentityError
        - AllegroTimeoutError
        - ExtensionError
