# Kasegi: dynamic metadata can still require preservation

[PEP 643](https://peps.python.org/pep-0643/), created October 2020, introduced metadata 2.2 to distinguish absent information from values deferred until wheel building. A dynamic field could change or disappear.

[PyPA Core Metadata](https://packaging.python.org/specifications/core-metadata/), version 2.6, approved May 2026, narrows that freedom for multiple-use fields already present in a source distribution: wheel building may append values, but cannot remove, reorder or alter those supplied. Single-use dynamic fields retain broader freedom.

Read the metadata version before interpreting Dynamic. A source archive can now establish a preserved contribution without establishing the complete eventual value set. Conversely, a prebuilt wheel alone does not prove its metadata matches a particular source archive; the specification warns about wheels modified after building.

Selected primary sections, not a build or compatibility test. PEP 643 declares public-domain or CC0 terms; PyPA's guide declares attribution-sharealike 3.0. Original commentary only, no copied examples or code. Unassimilated.

Reviewed 2026-11-11. Destination: VeigaPunk/kasegi-shokunin, master, considerthese/2026-11-11-dynamic-metadata-preservation.md.
