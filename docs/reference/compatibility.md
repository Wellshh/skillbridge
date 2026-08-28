# Compatibility

Verified combinations. Blank cells mean untested, not broken — behavior and
UI may differ between Allegro versions.

| Allegro | OS | Python | Transport | Status |
| --- | --- | --- | --- | --- |
| 17.2 | Windows | 3.10 – 3.13 | TCP | Tested |
| 17.2 | Linux | 3.10 – 3.13 | Unix / TCP | Partial |
| Allegro X | — | — | — | Unknown |

!!! note "Python floor"
    The package requires Python >= 3.10. The documentation toolchain
    (MkDocs, mkdocstrings) is development-only and tracks newer Python.

See [Installation](../getting-started/installation.md) for transport setup and
[Process lifecycle](../guide/lifecycle.md) for how a connection is established
and verified.
