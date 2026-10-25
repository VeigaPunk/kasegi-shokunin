# RecheckSources — scoped implementation report

## Scope and changed files

The implementation is in the required private clone at `/tmp/kasegi-r23-RecheckSources-5/corpus/instruments/source-recheck.py`, cloned at base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`. This seat changed no existing knowledge entries, source registry, manifest, or other production files. The only private-clone patch path is `corpus/instruments/source-recheck.py`. This report is the sole write outside that clone, at the assigned report path.

No tools were installed. No network access, build, test, linter, formatter, or `--selftest` run was performed; the integration owner requested no tests until integration.

## Implemented behavior

The stdlib-only CLI is:

```text
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018
```

The source selector is optional; omitting it checks every manifest source in stable ID order. The manifest is UTF-8 JSON with this schema (source `path` is relative to the manifest directory):

```json
{
  "schema_version": 1,
  "sources": [
    {
      "id": "S018",
      "path": "S018.txt",
      "sha256": "<64 lowercase hex characters>",
      "quotes": [
        {
          "id": "Q1",
          "quote": "<exact, non-empty quote substring>",
          "location": "<optional descriptive locator>"
        }
      ]
    }
  ]
}
```

`location` is accepted but intentionally not validated. The tool hashes exact local source bytes, then checks each quote as an exact substring of the UTF-8-decoded snapshot. It prints stable IDs such as `S018:sha256` and `S018:Q1`. A valid pin and every quote found yields exit 0; an available snapshot with a digest or quote mismatch yields 1; unavailable/malformed manifest, missing/unreadable/escaping source, or invalid UTF-8 yields 2. Missing data uses stable IDs (`manifest`, `S018:source`); malformed assertion IDs use a manifest/quote record ID. When checking multiple records, any unavailable result takes precedence over mismatch for the final exit.

Snapshot paths must be relative and their resolved realpaths must remain beneath the manifest directory, so `..` and symlink escapes cannot make the tool read arbitrary outside files. The code has no network client or network fallback. `--selftest` is implemented using an isolated temporary directory and subprocess CLI invocations. It pins these expected cases and IDs: clean `(0, S900:sha256 + S900:Q1)`, corrupt bytes `(1, S900:sha256)`, missing snapshot `(2, S900:source)`, and missing manifest `(2, manifest)`.

## Exact retained evidence

- `corpus/QUALITY.md:14-19` was read for Q1–Q6. It specifies provenance headers, opened tier-A/B support, exact located quotes of at most 25 words, attribution, a falsifiable local rule plus rejected generalization, and documentation-only/no credential material. `corpus/QUALITY.md:48` adds Q7: an executable recheck command, captured-source success distinguished from fresh network verification, and a failing missing/corrupt control. This instrument implements a local captured-source check; it does not adjudicate entry compliance with Q1–Q6.
- Read the H1/header area (lines 1–14/17) of all five round-22 entries: `corpus/knowledge/cvss-v4-severity-and-vector.md`, `coordinated-disclosure-timelines.md`, `authorization-safe-harbor-and-scope.md`, `ai-assisted-finding-validation.md`, and `cwe-top25-2025-methodology.md`. Each has `source:`, `verified-at:`, and `recheck:` headers, but the recheck text is prose (e.g. the CVSS entry begins “On each FIRST CVSS v4 document revision, reread…”), not an executable command. The round-22 verifier lesson `corpus/lessons/round-22-verifier-spotcheck.md:15-17` records this recheck gap.
- L1-provided `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/opened-source-snapshots.json` was read. It identifies normalized public-document reader excerpts (not raw HTTP bytes): S018 at `corpus/source-snapshots/round-23/S018.txt`, SHA-256 `d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4` (8,372 bytes); S029 at `corpus/source-snapshots/round-23/S029.txt`, SHA-256 `82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c` (19,900 bytes); and S030 at `corpus/source-snapshots/round-23/S030.txt`, SHA-256 `673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019` (26,660 bytes). The parent said S029 is the current CRA source and S030 the current CNA source; this implementation only consumes the manifest provided at integration and does not read or authenticate this metadata file.
- Read relevant sections of `corpus/instruments/README.md`, `resolve.py`, `anchorcheck.py`, `density.py`, and `test_resolve.py` to reuse the repository’s Python 3/std-lib instrument and isolated-fixture conventions. `resolve.py` writes its census outputs; this addition writes only temporary selftest fixtures.
- No LSP interface was exposed in the available tool inventory. This adds a standalone CLI and changes no existing symbol or callsite; the integration owner supplies the entry commands.

## Falsifiable finding and limits

For S018, changing one snapshot byte while retaining its declared digest must produce `S018:sha256 MISMATCH` and exit 1; removing the snapshot must produce `S018:source UNAVAILABLE` and exit 2; restoring exact pinned bytes with each quoted substring present must produce `S018:sha256 OK` plus one `S018:<quote-id> OK` per assertion and exit 0. The `--selftest` code encodes independent expected exit/ID controls for those classes, but these outcomes remain unobserved until the integration owner runs the selftest and the actual manifest commands.

This is a local integrity-and-substring recheck, not an upstream freshness check, provenance/authenticity proof for a manifest, validation that the `location` description is correct or unique, or a semantic/legal review of quotes. If both a snapshot and its manifest pin are changed together, this tool alone cannot identify the joint change. A successful run must be described as rechecking captured source bytes, not re-opening the source. No admission or axis credit is claimed.

## Integration checks for L1

After the tool and main-owned manifest land together, run `python3 corpus/instruments/source-recheck.py --selftest`, then the requested `--manifest corpus/source-snapshots/round-23/manifest.json --source S018`, `S029`, and `S030` invocations. For a focused falsifier, copy the manifest and source into a temporary directory, mutate one byte without changing the pin (expected exit 1), then remove a snapshot (expected exit 2); keep fixture outputs outside the canonical repository census.