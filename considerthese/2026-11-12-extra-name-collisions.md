# Kasegi: extra spellings can collide

[PEP566](https://peps.python.org/pep-0566/), created December 2017, introduced Provides-Extra for metadata 2.1, requiring Python identifiers.

[PEP685](https://peps.python.org/pep-0685/), created March 2022, standardized extra-name comparison: lowercase names and replace each run of hyphens, underscores or dots with one hyphen. Metadata producers must reject user-specified extra names that collapse together.

[PyPA Core Metadata](https://packaging.python.org/en/latest/specifications/core-metadata/) dates stricter Provides-Extra spelling to version 2.3: lowercase ASCII letters and digits, separated by single hyphens. It also requires collision rejection when writing older metadata after normalization.

Invented example: `audit_mode` and `audit-mode` normalize alike.

For package-security claims, record metadata version and normalized feature identity before alleging unexpected dependency selection. This is format evidence, not a tested installer flaw, exploit or impact. PEP creation dates are not implementation-release dates.

PEP566 declares public-domain terms; PEP685 declares public-domain/CC0 terms. PyPA's guide declares CC BY-SA 3.0. Original commentary only; no copied code or source examples.

Destination: VeigaPunk/kasegi-shokunin, master, considerthese/2026-11-12-extra-name-collisions.md. No repository change, training or assimilation.
