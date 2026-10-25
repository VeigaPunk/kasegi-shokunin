# Q7ControlsClaim — independent re-derivation of the Q7 fail-closed controls

Seat: `L1Kasegi23.Q7ControlsClaim-2` (leaf critic, round-23 FALSIFY wave).
Attacked bytes: HEAD `953c27880a97e8d3aaf8fac44c97e0252cddcddf`
(`round-23: mirror-fallback confinement with matrix receipts; admit F06-F08 with pinned-source rechecks`),
read through `git show HEAD:<path>` into `/tmp/kasegi-r23-falsify-Q7ControlsClaim/`.
Tested instrument: `sha256sum head-source-recheck.py` →
`f743942d9643c930453c415414fd4468486140049541e3f7babc935581ae888d` (the HEAD blob).

No production file was edited; no commit, push, admission, or score claim. All mutation happened on
copies under `/tmp/kasegi-r23-falsify-Q7ControlsClaim/head/<case>/`. No tool was installed.

Q7 text under test (`corpus/QUALITY.md:48`):
> An executable recheck field contains a command, not prose beginning “On each”. Its successful output
> names what was checked: a pinned captured-source comparison is not a fresh network verification.
> At least one missing/corrupted-source control must fail.

## 0. Baseline — the three published rechecks, HEAD-pinned

```
python3 head-source-recheck.py --manifest head/clean/manifest.json --source S018  → 7 lines, exit 0
python3 head-source-recheck.py --manifest head/clean/manifest.json --source S029  → 7 lines, exit 0
python3 head-source-recheck.py --manifest head/clean/manifest.json --source S030  → 8 lines, exit 0
python3 head-source-recheck.py --manifest head/clean/manifest.json              → 22 lines, exit 0
```
`ctrl-A.txt` sha256 `683eeaf21fd24e6b6b2a42531a8ada5bfc2f7a824667298b12547ec8b830f2da`.

Three-way digest on HEAD bytes (manifest pin vs `opened-source-snapshots.json` vs recomputed sha256)
is equal for all three sources: S018 `d366bf40…ab4` 8372 B / 6 quotes, S029 `82514478…b8c` 19900 B /
6 quotes, S030 `673526db…019` 26660 B / 7 quotes. The pinned baseline is self-consistent before any mutation.

## 1. Assigned result — every control re-derived (digest, missing source, fabricated quote, plus 9 more)

Each row: mutation applied to the copy, observed stdout, exit code. Commands are
`python3 head-source-recheck.py --manifest head/<case>/manifest.json [--source <id>]`.

| # | control | mutation | observed stdout | exit |
|---|---|---|---|---|
| A | clean all | none | 22 × `S0xx:<id> OK` | 0 |
| B | **digest mismatch** | `printf 'x' >> digest/S018.txt` (manifest pin unchanged) | `S018:sha256 MISMATCH expected=d366bf40…ab4 actual=950eb7df…1da` | **1** |
| C | **missing source** | `rm missing/S029.txt` | `S029:source UNAVAILABLE reason=missing` | **2** |
| D | **fabricated quote** | add `{"id":"fabricated","quote":"CNAs MUST publish the finder's contact details."}` to S030 | `S030:sha256 OK` then `S030:fabricated MISMATCH reason=quote-not-found` and the 7 real quotes `OK` | **1** |
| D2 | fabricated quote, other source | same on S018 with id `fabricated-control` | `S018:fabricated-control MISMATCH reason=quote-not-found` | 1 |
| E | fabricated *location* | S029 `location` → `Article 999, page 99999` (digest+quote untouched) | 7 × `OK` | **0** ← see §4 |
| F | corrupt bytes + re-pinned digest | append byte to `repin/S030.txt`, rewrite S030 `sha256` to the new digest | 8 × `OK` | **0** ← see §4 |
| G | symlink escape | `path` → symlink to `/etc/hostname` | `S018:source UNAVAILABLE reason=outside-manifest-directory` | 2 |
| H | absolute path | `path` → `/etc/hostname` | `S018:manifest UNAVAILABLE reason=invalid-path` | 2 |
| I | missing manifest | `--manifest head/clean/absent.json` | `manifest UNAVAILABLE reason=missing` | 2 |
| J | unlisted source | `--source S999` | `S999:source UNAVAILABLE reason=not-listed` | 2 |
| K | no arguments | — | (usage) | 2 |
| L | `--selftest` | — | `SELFTEST {clean,corrupt,missing-source,missing-manifest} PASS` | 0 |

All three Q7-required controls fail closed on the real committed bytes, not just on the synthetic
`S900` fixture: digest mismatch exit 1, missing source exit 2, fabricated quote exit 1. The
`--selftest` synthetic cases (exit 0/1/2/2) reproduce the same branches. Instrument verdict:
**sound for what it claims**.

## 2. Does the committed evidence record those control outputs? **Yes** — the omission hypothesis fails

- `corpus/lessons/round-23.md:161-165` (HEAD) records exactly three control outcomes:
  `flipped digest → S018:sha256 MISMATCH, exit 1; missing source path → S029:source UNAVAILABLE reason=missing, exit 2; fabricated quote → S030:fabricated MISMATCH reason=quote-not-found, exit 1`.
- `LOG.md:1133-1136` records the same as `failing controls exit 1/2/1 (flipped digest, missing source, fabricated quote)`.
- `corpus/lessons/round-23.md:188` (M11) records `three exit-0 runs plus three failing controls recorded`.
- Synthetic-fixture control evidence also exists: `.ufo/waves/round-23/build/OverlapWeb.md:51`
  (`--selftest exited 0. Controls: clean 0, corrupt 1, missing source 2, missing manifest 2`) and
  `considerthese/2026-10-21.md:16,92` (`all four PASS`).

My independent run reproduces B, C and D on the committed manifest and snapshots, with the same
strings and the same 1/2/1 exit codes (B's stdout additionally carries `expected=… actual=…`, which
the lesson elides). Therefore the controls are **recorded and accurate**, and their absence is **not**
a defect in this round's record.

Residual thinness, not a Q7 breach: the records are paraphrase, not archived stdout. No committed file
holds the verbatim control transcript; the raw per-source receipts
`.ufo/waves/round-23/c2-recheck-S0{18,29,30}.txt` are **untracked** additions written after HEAD by a
sibling seat, so a verifier must re-run to diff stdout. Q7 asks only that a control fail, which it does.

## 3. Falsifiable finding F1 — Q7 remains unmet for the five entries Q7 was written to fix

The measured counterexample: the five admitted entries `F01–F05` — the exact five in Q7's grounding —
now carry recheck commands that can **never** succeed, and the round's record does not say so.

- Grounding being tested: `claims.json` `supporting_corrections` names “M2 five prose rechecks” as a
  correction this round undertakes; `corpus/lessons/round-23.md:16` grounds Q7 on
  “five r22 new rechecks exit 2”.
- HEAD `line 4` of those five entries (via `git show HEAD:…`):
  - `cvss-v4-severity-and-vector.md` → `--source S001 && … --source S002`
  - `coordinated-disclosure-timelines.md` → `S003 && S004 && S005`
  - `authorization-safe-harbor-and-scope.md` → `S006 && S007 && S008`
  - `ai-assisted-finding-validation.md` → `S009 && S010 && S011 && S012`
  - `cwe-top25-2025-methodology.md` → `S013 && S014 && S015`

  all against `corpus/source-snapshots/round-23/manifest.json`.
- That manifest lists only `["S018","S029","S030"]`; the snapshot directory holds only
  `S018.txt`, `S029.txt`, `S030.txt`. Observed:
  ```
  python3 source-recheck.py --manifest …/manifest.json --source S001 → S001:source UNAVAILABLE reason=not-listed, exit 2
  … S003 → exit 2   … S006 → exit 2   … S009 → exit 2   … S013 → exit 2
  ```
  (identical from the working-tree manifest, whose ids are still S018/S029/S030).
- Consequence for Q7, the criterion this round itself minted: clause 2 (“Its successful output names
  what was checked”) is *unsatisfiable* for all five. There is no successful run to inspect, and the
  observed exit code is **2** — the same code the r22 verifier used to flag M2. The round changed the
  fields from prose to commands without giving them a resolvable base; the admission bar for F01–F05
  is therefore still unexecutable while those rows read `admitted` (`corpus/README.md:195-199`).
- Disclosure status: `LOG.md:1134` says only “The three published rechecks now exit 0 (S018, S029,
  S030)”; `corpus/lessons/round-23.md:188` says “three exit-0 runs”. Neither names the five red
  fields, and `corpus/lessons/round-23.md` contains no residual-debt line for F01–F05 (`grep -n
  "residual\|F01\|not-listed"` → only the unrelated C1 sentence at `:142`). The record is silent, not
  false, but `supporting_corrections` presents M2 as corrected.
- Prior prediction, not my finding: `.ufo/waves/round-23/build/Q1Executable.md:24` asked to “Close M2
  on the flagged files, not only the new ones … or record them as named residual debt — silent
  persistence contradicts supporting_corrections M2”. My contribution is the observed post-integration
  state and the exact exit codes; the prediction is that seat's.

Severity: **record-level / entry bar**, not a falsification of the C2 claim. C2 admits F06–F08 only,
and all three of those exit 0 with controls reproducing (§1, §2).

Secondary observation at HEAD, already fixed in the working tree: the F06–F08 commands work only from
the repository root. From `corpus/knowledge/` the command as written exits 2
(`python3: can't open file '…/corpus/knowledge/corpus/instruments/source-recheck.py'`). A sibling has
since prefixed `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` in the working tree; HEAD does not.

## 4. Finding F2 — the control set has no location control (bounded, not a Q7 breach)

Control E: changing S029's first quote `location` to `Article 999, page 99999` with digest and quote
untouched yields 7 × `OK`, exit 0. The instrument never reads `location`
(`check_source` tests `assertion["quote"] in source_text`), and its success lines name quote **ids**,
not locations. So the recheck cannot distinguish a correct locator from a fabricated one, and C2's
“exact located quotes” rests on human review (`S018Quotes`/`S029Quotes`/`S030Quotes`,
`EntryQuoteBinding`), not on the recheck.

Control F is the matching provenance limit: corrupting snapshot bytes and re-pinning the digest in the
same edit passes (8 × `OK`, exit 0). The pin proves integrity against accidental drift, not the
authenticity of the captured bytes.

Neither is a Q7 violation — Q7 requires digest and quote controls, which exist — but both bound what
“names what was checked” can mean. Live note: while this seat ran, a sibling amended the **working
tree** `manifest.json` `purpose` with a ceiling sentence disclosing exactly the location limit
(“quote-to-location binding is human-verified and is not machine-checked”). That text is **not** in
HEAD; `head-manifest.json` `purpose` ends at “This verifies captured bytes, not current upstream
freshness.” The ceiling IS disclosed in the build record
(`.ufo/waves/round-23/build/RecheckManifest.md`, `build/OverlapWeb.md`), so no false claim is made.

## 5. Smallest safe correction

1. F1: append one named residual-debt line to `corpus/lessons/round-23.md` (M2 or M11) stating that
   F01–F05's rewritten rechecks exit 2 `reason=not-listed` because the round-23 manifest carries only
   S018/S029/S030, so Q7 is closed for F06–F08 only. Larger alternative: snapshot S001–S015 with quote
   assertions. No admission flip, no score change.
2. F2: keep the working-tree `purpose` ceiling sentence on landing; do not describe the recheck as
   verifying quote locations. If location binding should be machine-checked, add a location control
   and a selftest case for it in the same instrument edit.

## 6. Scope limits

- Pinned to HEAD `953c278`; the working tree is being modified concurrently by sibling seats
  (`manifest.json` purpose, F06–F08 line 4 `cd` prefixes). F1 and F2 were evaluated on HEAD bytes and
  re-confirmed against the current working-tree manifest ids (still S018/S029/S030).
- Controls exercised only the F06–F08 manifest/snapshots and `source-recheck.py`; no verdict on C1
  `resolve.py`, the mirror matrix, `anchorcheck.py`, or any legacy lost-base recheck.
- No C1/C2 verdict, no admission, no score movement, no commit or push.
- Sibling overlap: `falsify/ControlsRerun.md` re-ran the same clean/corrupt matrix independently;
  `falsify/HashCheck.md:120` records `not-listed` for a fabricated id; `build/Q1Executable.md`
  predicted F1. This report's distinct contribution is the HEAD-pinned control matrix with exit codes,
  the three-way digest confirmation, the §2 answer to the recording question, and the observed F1
  state (five named entries, exact commands, exit 2).
