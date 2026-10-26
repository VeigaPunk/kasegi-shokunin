# ExecC2Harness — frontier-harness delta for F21 (round 38, C2 coverage)

Seat: ExecC2Harness (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, claims-freeze mirror `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`.
Scratch: `/fast/scratch/hyaku/kasegi-r38/ExecC2Harness/` (removed before yield). No network fetch, no tool install, no lane write outside this receipt.

## 1. What `corpus/instruments/frontier-recheck-count.py` requires per admitted F-row

Read in full (433 lines). Flags: `--root`, `--json`, `--selftest`, `--scratch` (`--help` above). Per admitted Frontier row it requires:

1. **Row shape** — `corpus/README.md`, `FRONTIER_ROW = ^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|`; cell 3 must be exactly `admitted`; cell 4 is the entry path, resolved as `root/<cell>` and then `root/corpus/<cell>` (README rows therefore carry `knowledge/…`), and one row may name several entries comma-separated. A row whose entry file is absent is a named-row `missing-entry` failure, never a traceback; two rows resolving to one realpath are `DUPLICATE-ENTRY`.
2. **Entry file** — must carry at least one header declaration line `source: S\d{3,}` (`SOURCE_LINE`) and, per additional source, either another `source:` line or a per-source evidence bullet `- S002, …` (`EVIDENCE_LINE`). The declared set is `header ∪ evidence`.
3. **`recheck:` line** — `^recheck:\s*(.+)$`, first one wins; it must contain `source-recheck.py`, must not contain `--selftest`, must carry `--manifest <path>` (`RECHECK_MANIFEST`) and at least one `--source S\d{3,}` (`RECHECK_SOURCE`).
4. **ids, both directions** — `--source` set must equal the declared set: a declared id missing from the line is `header-sources-not-rechecked`; a selected id the entry never declares is `selection-not-declared-by-entry`; a selected id not mentioned anywhere else in the entry is `selection-not-cited-by-entry` (the header/`recheck:` lines themselves are excluded from "cited", so the limb is not vacuous).
5. **Manifest + capture** — `<root>/<manifest>` must be readable JSON with `schema_version == 1` and a `sources[]` list (`manifest_ids`; else `manifest-unreadable`), and must list every `--source` id (`manifest-missing-ids`). The capture itself is only reached when the line is executed: `source-recheck.py` resolves `path` relative to the manifest directory, requires `Path(path).stem == id` (B1), a 64-hex `sha256` that matches the bytes, and ≥1 `quotes[]` entry with a normalized length ≥ 12 chars; occurrences > 1 need a verifying `anchor`.
6. **Execution** — only when no problem fired, the line runs `bash -c <line>` with `cwd = --root`; a non-zero exit becomes `recheck-exit-N`. Summary is `entries=N pass=M exit=X`, exit 1 if any record failed or a duplicate realpath exists, 2 on a harness/read error.

## 2. Base measurement

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive a173b0c2b98c5ae39599fa9be76027fbbead0b9e | tar -x -C $S/base
$ python3 corpus/instruments/frontier-recheck-count.py --root $S/base
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
entries=23 pass=23 exit=0
```

Base counts (same export): `grep -cE '^\| F[0-9]+ \|' corpus/README.md` -> 20; registry rows -> 54. The 23 records come from 20 admitted rows (F09/F10/F11 name two entries each), matching the C2 before-control `entries=23 pass=23 exit=0`.

## 3. Mirror delta (claims-freeze export + planned F21 files)

```
$ git -C …/kasegi-shokunin archive 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b | tar -x -C $S/m   # 7294 files
```

Added in the mirror only — no lane write:

- `corpus/README.md`: one row appended directly under the F20 row in the same 6-column table (`awk` pipe-split: F20 line has 6 data cells, F21 line has 6):
  `| F21 | OASIS CSAF 2.0 (Common Security Advisory Framework) — VEX product-status categories and machine-readable not-affected justification flags | admitted | knowledge/csaf-vex-product-status-and-justifications.md | S055 | PLUMBING STUB for the round-38 harness delta: this cell carries no reading yet; the capture seat replaces it with the entry's own VEX reading once S055 is fetched and pinned. |`
- `corpus/SOURCES.md`: one `S055` registry row appended after `S054` (`spec | A | … | mined | 2026-10-26 | 180d |`), anchor/teaches cells explicitly marked `STUB row` because only the capture seat's fetch can fill them.
- `corpus/knowledge/csaf-vex-product-status-and-justifications.md`: stub entry, header exactly §5 below except that its `recheck:` line is **root-relative** (`python3 corpus/instruments/source-recheck.py --manifest … --source S055`, no `cd` prefix) so the `--root` mirror genuinely binds the run; prose cites `S055` once (citation limb), body marked as a stub.
- `corpus/source-snapshots/round-38/S055.txt` + `manifest.json`: two-line stub capture (`282 bytes`, `sha256 975d04208a9c2450c7ef718be87112998134a50c7641bfe93bfcbc9271ca69ec`), schema-1 manifest with one record `{id: S055, path: S055.txt, sha256: <capture>, quotes: [Q1 anchor 2]}` and `stub: true`. It is a fixture, **not** a fetch: the statement it contains is plumbing text, and the capture seat's real S055 capture and manifest replace both files.

Mirror counts: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` -> 21; registry rows -> 55.

## 4. Mirror harness run — expected delta reached

```
$ python3 corpus/instruments/frontier-recheck-count.py --root $S/m --json $S/mirror-harness.json
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
entries=24 pass=24 exit=0
```

`diff` of the mirror output minus the F21 line and the summary against the base output minus its summary: `IDENTICAL_PREFIX` — the 23 pre-existing records are byte-identical, so the whole 23->24 delta is the added F21 binding, not a shift in another row.

JSON receipt record for F21 (`mirror-harness.json`):

```json
{"frontier":"F21","entry":"knowledge/csaf-vex-product-status-and-justifications.md",
 "declared_ids":["S055"],"evidence_declared_ids":[],"cited_ids":["S055"],
 "recheck_ids":["S055"],"manifest":"corpus/source-snapshots/round-38/manifest.json",
 "exit":0,"problems":[],"status":"PASS",
 "realpath":"/fast/scratch/hyaku/kasegi-r38/ExecC2Harness/m/corpus/knowledge/csaf-vex-product-status-and-justifications.md"}
```

Direct capture limb in the mirror (`cwd=$S/m`):

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2-ok
(exits 0)
```

## 5. Rejection matrix — the harness refuses F21 when a limb is cut

Six reflink clones of `$S/m`, one mutation each, same command (`--root` at the clone):

| # | mutation | F21 line | summary | exit |
|---|---|---|---|---|
| r1 | entry file deleted, row kept | `FAIL F21 … ids=- exit=- problems=missing-entry` | `entries=24 pass=23 exit=1` | 1 |
| r2 | `round-38/manifest.json` deleted (entry + capture kept) | `FAIL F21 … ids=S055 exit=- problems=manifest-unreadable` | `entries=24 pass=23 exit=1` | 1 |
| r3 | `round-38/S055.txt` deleted (manifest kept) | `FAIL F21 … ids=S055 exit=2 problems=recheck-exit-2` | `entries=24 pass=23 exit=1` | 1 |
| r4 | recheck selects `--source S054`, header still `S055` | `FAIL F21 … ids=S055 exit=- problems=header-sources-not-rechecked,selection-not-declared-by-entry,manifest-missing-ids` | `entries=24 pass=23 exit=1` | 1 |
| r5 | whole binding moved to `S054` (header + recheck, self-consistent) | `FAIL F21 … ids=S054 exit=- problems=manifest-missing-ids` | `entries=24 pass=23 exit=1` | 1 |
| r6 | control: `S054` mentioned once in prose, binding stays `S055` | `PASS F21 … ids=S055 exit=0` | `entries=24 pass=24 exit=0` | 0 |

Reading: (a) row-without-entry -> `missing-entry`; (b) entry without manifest -> `manifest-unreadable`, entry without capture -> `recheck-exit-2` (the fail-closed capture limb, not a pass); (c) an F21 entry carrying `S054` -> rejected in both forms — a swapped selection fails the declared-set limbs, and a self-consistent `S054` binding fails because the round-38 manifest lists only `S055`. r6 shows the rejection is about the *binding*, not the string: citing `S054` as a cross-reference passes. r5's self-consistency is why the manifest limb matters for the round-38 row.

## 6. DELIVERABLE — exact header lines for `corpus/knowledge/csaf-vex-product-status-and-justifications.md`

4 lines, 349 bytes; sha256 `b3cf225f60ea1da7def2af5cc702da85bb846c54a812f84a45bc9bef3db1e82c`.

```text
source: S055 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html — capture corpus/source-snapshots/round-38/S055.txt
verified-at: 2026-10-26
ground: F21
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
```

Validation of those bytes:

- `source:` — matches `SOURCE_LINE ^source:\s*(S\d{3,})` -> declared `S055`, exactly the id the round-38 manifest must list; the URL is the claims' S055 registry URL; the anchor is the exact capture path.
- `recheck:` — `bash -n` -> exit 0 (Q10 parse); carries the lane-root `cd` prefix (Q10); contains `source-recheck.py`, `--manifest corpus/source-snapshots/round-38/manifest.json` and `--source S055`; no `--selftest`. Its `--manifest`/`--source` tokens are byte-identical to the mirror line that passed, so the declared-equals-selected limb passes with `S055` as the only id. Authored as a single executable command with no `#` note, so nothing can drift from its output.
- `ground: F21` — the F18/F19/F20 header convention; not read by the harness.
- The long form of the same `source:` line (with `(2 lines, 282 bytes; sha256 …): …` on it) was run as r7 and also yields `entries=24 pass=24 exit=0`, so the capture seat can append its measured size/sha256 and section map to that line without changing the harness verdict.

## 7. Handoff for the capture/entry seat

- The manifest the line names does not exist in the lane yet: running the delivered line **today** in the lane prints `manifest UNAVAILABLE reason=missing` and exits 2 — fail-closed pre-landing, as intended. It goes green only when `corpus/source-snapshots/round-38/manifest.json` with an `S055` record (`schema_version: 1`, `sources[{id, path, sha256, quotes[]}]`, `path` stem `S055`, quoted text ≥ 12 normalized chars) and `corpus/source-snapshots/round-38/S055.txt` land.
- Keep `--source S055` as the only selection and keep `S055` out of any second declaration line; a second `source:` line or an evidence bullet naming another id requires that id on the recheck line too.
- The entry body must mention `S055` at least once outside the header/`recheck:` lines (e.g. `(S055.txt:<line>)`), else `selection-not-cited-by-entry`.
- Append the measured `(N lines, B bytes; sha256 …)` and section map to the `source:` line; do not rename the file — the README cell here and the planned row are `knowledge/csaf-vex-product-status-and-justifications.md`.

## 8. Risks and observations

- Pre-existing property, not introduced here: every committed frontier entry's `recheck:` line begins `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`, so under `--root <export|mirror>` those lines still execute against the lane, not the export; only the rules A/B/C bindings are root-scoped. F21 inherits the committed convention (Q10 requires the `cd` prefix), and the mirror test therefore used the root-relative variant to keep the pass attributable to the mirror. Flagged for the L1; not changed by this seat.
- The stub capture/manifest are fixtures. Neither was fetched; their bytes and `sha256 975d04…` are plumbing only and must not be cited as S055 evidence. No entry text or registry anchor was invented as fact — the mirror's row and row cells are explicitly marked STUB.
- `[INFERENCE]` The harness counts a row's entries, not rows, so F21's single entry takes the count 23 -> 24; the claims' expected `pass=24` therefore needs no other row change. Measured: 24 records, 24 pass.
- No blockers. Lane untouched: only this receipt was written under `.ufo/waves/round-38/wave1/`.

## 9. Tooling / scratch

No installs, no upgrades, no network. `/fast/scratch/hyaku/kasegi-r38/ExecC2Harness/` removed before yield (`trap`-equivalent `rm -rf` after copying evidence here); the six clones, the mirror and the base export were all under that root.
