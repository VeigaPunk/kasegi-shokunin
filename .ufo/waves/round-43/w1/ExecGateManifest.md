# ExecGateManifest — R-FILES, R-MANIFEST, R-REDACT (kasegi round 43, wave 1)

Seat: executor, leaf. Item: implement the package-shape half of the new
claim-package gate. Claims read first: `.ufo/waves/round-43/claims.json`
(C2, capability-acquisition; C1 read for context; never edited). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`
(the round-43 freeze commit on base `ab98fac9dce87130bc4f66de89e30650d63943dc`).
No mutating git/jj command was run; the only git commands were `rev-parse --short`/
`rev-parse HEAD` (read-only).

## Deliverables (in `.ufo/waves/round-43/w1/`)

| File | Lines | Bytes | sha256 |
|---|---|---|---|
| `ExecGateManifest.rules.py` | 386 | 14379 | `e8131998f246684a9876d4a18769e544379a70146bf72f817bf929811b18a81b` |
| `ExecGateManifest.transcript.txt` | 86 | 4813 | `ee439faa00edef7894f0548ffb16c7bb4127bc7d5a9e126a93852c721cbb5d87` |

`ExecGateManifest.rules.py` is the splice-safe fragment for
`corpus/instruments/claim-package-check.py` (rules 1–3 of the eight, in gate
order). Drop `main()` and the `__main__` block when splicing; the three rule
functions have no import-time side effects (proved: `probe.py` imports the
module and calls each function, transcript lines 10–15).

## Interface (for the integrating CLI)

```python
rule_files(root)                 -> {"id": "R-FILES",    "verdict": "pass"|"fail",
rule_manifest(root[, manifest])  ->  "detail": "<k=v ...>", "counts": {...},
rule_redact(root[, manifest])    ->  "reasons": [...]}          # R-MANIFEST / R-REDACT
emit(result)                     # prints: RULE <id> verdict=<v> detail=<...>
run(root)                        # the three results, gate order
```

The optional `manifest` argument lets the CLI parse `evidence/manifest.json`
once and hand the parsed object to R-MANIFEST and R-REDACT; each rule still
loads and fails closed on its own when it is not given one.

## Rule predicates as implemented (contract text first)

**R-FILES** — `corpus/knowledge/claim-package-contract.md`, table rows:
`report.md`, `claim_checklist.md`, `evidence/manifest.json`,
`custodian-receipts.json`, `provenance.json`, `status.json`.
Each must be a regular file under the package root. A symlink or a directory
at one of those paths fails (`claim-check.mjs` banned blanket symlinks in its
walk loop, `claim-gates.md` "Blanket symlink ban"). Counts:
`files=<k>/6 missing=<n> notregular=<n>`; reasons `missing-file`,
`not-regular-file`.

**R-MANIFEST** — contract: "`schema_version: "evidence-manifest/v1"`. Per-artifact
sha256 + `polarity` ∈ {positive, negative}; ≥1 positive required. … Artifact
paths are relative to `evidence/`, must stay inside the package, no symlink
traversal."
- `schema_version` must equal `evidence-manifest/v1` exactly.
- `expected_head_sha256` must be present and non-empty (its *value* is
  R-CUSTODIAN's three-way binding, not this rule's).
- `artifacts[]` non-empty; every entry an object with `path`, `sha256`,
  `polarity`.
- Path: non-empty, relative (an absolute path or a leading `\` fails), **no
  `..` component even when it would resolve inside** (the mutation-tester item
  expects this), every component from `evidence/` down lstat'ed for a symlink,
  `realpath` confined to the package root, and the target an existing regular
  file. Escapes count `escape=`; absent files count `missing=`; a non-string or
  empty path counts `shape=`.
- Digest: `sha256` recomputed over the artifact bytes and compared with the
  declared value; the declared digest is never trusted. A malformed declared
  digest, an unreadable file, or a byte-level mismatch counts `digest-bad=`
  (this last is what makes K-style "trust the recorded digest" mutations
  visible).
- Polarity counted over the enum; anything else is `shape=`; `positive=0` with
  a non-empty artifact list fails (`no-positive`).
- Counts, always printed: `artifacts= positive= negative= digest-bad= escape=
  missing= shape=`.

**R-REDACT** — contract: "`redactions[]`: one same-digest receipt per artifact
with nonempty, distinct producer/verifier identities. `redactions:[]` is never
claim-ready."
- `redactions` must be a list and non-empty (`empty-redactions`; this is the
  literal "never claim-ready" clause).
- Every artifact entry with a valid declared digest must have at least one
  receipt whose `artifact_sha256` equals it; when
  `scanned_artifact_sha256` is present it must equal the same digest (the key
  is optional because the contract does not name it, but `claim-gates.md`
  L60–63 bound both to `a.sha256`, so a present-but-different value fails).
- Receipts bind manifest digests: a receipt whose digest no artifact declares
  counts `unbound=`. Duplicate receipts for one artifact are accepted and
  counted (the lost `claim-check.mjs` required *a* receipt per artifact, not
  exactly one); this is the one place the rule is more permissive than the
  table's wording and it is deliberate.
- Identities: `producer`/`producer_identity` and `verifier`/`verifier_identity`
  are read (first non-empty wins); empty, whitespace, or equal identities
  count `identity-bad=` and the receipt cannot make its artifact covered.
- Counts: `redactions= artifacts= covered= unbound= identity-bad= digest-bad=`;
  `uncovered=` appears when artifacts remain uncovered. Coverage is counted
  per artifact entry, so two artifacts with identical bytes need one receipt
  digest and both count as covered.

Every rule fails closed: an unreadable/unparsable manifest or receipts block,
a non-dict entry, or an unusable package root yields `verdict=fail`, never a
pass and never a traceback (the truncated-manifest probe at transcript lines
65–69 shows both
R-MANIFEST and R-REDACT failing on a truncated manifest).

## Evidence actually run

Scratch: `/fast/scratch/hyaku/kasegi-r43/ExecGateManifest` (removed before
yield). `rules.py` in the transcript is a byte-identical copy of the
deliverable — `sha256sum` of both printed
`e8131998…a81b`, and `cmp -s` printed `scratch copy identical`.

Driver (one unedited tee of one run):

```
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 bash drive.sh > transcript.txt 2>&1   # rc=0
```

`build.py` writes a good package (`pkg-good`) and eleven mutated twins; each
case is run as `python3 rules.py <pkg>` with the command echoed, its real
output, and its exit code. Transcript, in order:

```
$ python3 rules.py pkg-good
RULE R-FILES verdict=pass detail=files=6/6 missing=0 notregular=0
RULE R-MANIFEST verdict=pass detail=artifacts=2 positive=1 negative=1 digest-bad=0 escape=0 missing=0 shape=0
RULE R-REDACT verdict=pass detail=redactions=2 artifacts=2 covered=2 unbound=0 identity-bad=0 digest-bad=0
exit=0
```

| Mutation (six required + five controls) | Command | Named rule fired | Count printed |
|---|---|---|---|
| missing sixth file (`status.json` removed) | `rules.py pkg-m1-missing-file` | R-FILES | `files=5/6 missing=1` |
| wrong digest (artifact byte appended, recorded digest untouched) | `rules.py pkg-m2-wrong-digest` | R-MANIFEST | `digest-bad=1` |
| negative-only polarity | `rules.py pkg-m3-negative-only` | R-MANIFEST | `positive=0 negative=2` |
| escaping path (`../../outside.txt`, file created outside the package) | `rules.py pkg-m4-escape` | R-MANIFEST | `escape=1` |
| empty redactions | `rules.py pkg-m5-empty-redactions` | R-REDACT | `redactions=0 uncovered=2` |
| same producer and verifier | `rules.py pkg-m6-same-identity` | R-REDACT | `identity-bad=2` |
| extra: `..` that resolves inside (`sub/../artifact-positive.txt`) | `rules.py pkg-x7-dotdot-inside` | R-MANIFEST | `escape=1` |
| extra: artifact symlink inside the package | `rules.py pkg-x8-symlink` | R-MANIFEST | `escape=1` |
| extra: truncated manifest JSON (R30) | `rules.py pkg-x9-corrupt-manifest` | R-MANIFEST + R-REDACT | `fail=manifest-unparsable` both |
| extra: receipt `scanned_artifact_sha256` disagrees | `rules.py pkg-x10-scanned-digest` | R-REDACT | `digest-bad=1` |
| extra: `status.json` replaced by a symlink | `rules.py pkg-x11-symlinked-contract-file` | R-FILES | `notregular=1` |

Each mutation's other two rules stay `pass` (visible on the same three-line
block in the transcript), so each failure is attributable to the one delta.
`python3 rules.py no-such-package` prints `package=no-such-package
verdict=ERROR` and exits 2, matching the CLI contract for a missing package
dir.

Pre-landing sanity: `python3 -m py_compile ExecGateManifest.rules.py` → ok.
That check wrote a `__pycache__/` into the wave dir; I removed it immediately
(`rm -rf`), and the final `ls` of the wave dir shows no `__pycache__` or
`*.pyc`.

## Integration notes for ExecGateCore / the L1

- Gate order for the first three lines: `R-FILES`, `R-MANIFEST`, `R-REDACT`.
- `ExecGateProvReport.rules.py` (sibling, landed 13:41) uses the identical
  dict result shape, `_result`/`_detail`/`_Missing` helpers, and the same
  `detail=<k=v ...> fail=<codes>` grammar — these six rules concatenate with
  no adapter. `ExecGateChain.rules.py` instead returns `(ok, detail)` tuples
  from `rule_*` and `(id, ok, detail)` from `run`, so the CLI must normalize
  its two rules; that divergence is between the sibling modules, not mine.
- Key names R-MANIFEST depends on: `schema_version`, `expected_head_sha256`,
  `artifacts[].{path,sha256,polarity}`, `redactions[].{artifact_sha256,
  scanned_artifact_sha256?,producer|producer_identity,verifier|verifier_identity}`.
  If the exemplar/custodian seats use different receipt key names, reconcile
  in one place (`PRODUCER_KEYS`/`VERIFIER_KEYS`) rather than per fixture.
- `sequence` (a number in the recovered `claim-check.mjs`, `claim-gates.md`
  L39) is deliberately **not** required: the contract file does not state it,
  and requiring it would red an exemplar built from the contract text. If the
  CLI wants it, add it in R-MANIFEST's schema block, not in a fixture.
- Error strings never carry file paths or package text, so R-NOSECRET's
  "report only the rule, never the value" is not undermined by these lines.

## Limits / risks

- R-REDACT accepts duplicate receipts for one artifact (documented above).
  A reviewer testing "exactly one" will see a pass; the lost gate behaved the
  same way.
- R-FILES treats `evidence/manifest.json` as one fixed path; a package that
  also keeps a stray `manifest.json` at the root is not flagged (no contract
  row for it).
- The rule reads only under the package dir it is given; no network, no git.
- Nothing here asserts the exemplar exists or that the gate as a whole prints
  `rules=8`: those are the CLI/exemplar seats' bytes.

## Tooling / scratch

- Python 3.14.8 (host `python3 -V`). No tools installed; no pacman run; no
  PATH writes; no network fetch. No subagent or labrat was used — the work
  fit one seat.
- Scratch `/fast/scratch/hyaku/kasegi-r43/ExecGateManifest` is removed by this
  seat before yield (receipt and deliverables are the only wave-dir writes).
