# RevWaveEvidence — round-25 wave-1 receipt provenance

Seat: `L1Kasegi25.RevWaveEvidence` (reviewer, read-only).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` (= HEAD at cutoff).
Measurement window: `2026-10-25T08:22Z` … `2026-10-25T08:42Z`. Cutoff for the inventory below: **08:42:03Z**.
Excluded per ticket: `.ufo/waves/round-25/wave1/*.md` seat reports.

Question: does every committed receipt name the command that produced it, carry the input digest
it claims, and reproduce?

Method: I re-ran each receipt's own command where the run is side-effect-free (all JSON/text
outputs redirected to `/tmp`), and where a receipt measures a tree I no longer hold, I rebuilt that
tree read-only from git (`git archive <base> | tar -x -C /tmp/r25-before`) and ran against it.
No lane file was written by me; the only lane write is this report.

## Table

`Reproduced` = I ran the receipt's command and compared its output to the committed bytes.
`yes` = byte-identical (or identical modulo the receipt's own wrapper lines, noted in the last column).

| # | receipt | command (as recorded / as recovered) | reproduced | mismatch detail |
|---|---|---|---|---|
| 1 | `c1-before.json` | **not recorded in the file.** Recovered: `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-before.json` from the lane root at base rev. `claims.json` names only `--json c1-after.json`, so the before invocation is inference, not a recorded command. | **yes** | Ran against `/tmp/r25-before` (base bytes): all 35 entry records byte-identical, including `lane_output_sha256`/`foreign_output_sha256` (0/70 digest mismatches); summary `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`. Only `root` differs (surrogate path). |
| 2 | `c1-before.txt` | same as #1, without `--json` | **yes** | 35 verdict lines and the `lines=…` summary identical to the base-tree rerun; trailing `BEFORE_EXIT=1` equals the instrument's real exit status. File records no command, no root, no foreign cwd, no input digest. |
| 3 | `c1-instrument-digest.txt` | no command recorded (`sha256sum` implied) | **no (stale)** | At 08:26Z it read `d07af435…  corpus/instruments/recheck-audit.py` + `3e3eeb4e…  .ufo/waves/round-25/c1-before.json`; both matched the bytes on disk then. By cutoff it was rewritten (mtime 05:39:20 −0300) to a single line `6eb657c0…`, while the instrument on disk is `1ccee066…` (mtime 05:39:56 −0300). **The pin does not name the file it claims to pin.** The `c1-before.json` pin line was dropped. |
| 4 | `capture-log.txt` | recorded: `python3 corpus/instruments/capture-source.py --id <S0NN> --url <URL> --out corpus/source-snapshots/round-25/<S0NN>.txt`, run from the lane root; URLs in the table | **yes** | Re-fetched all five to `/tmp/r25-refetch`: `S036` 200/16900/4815/`022ca4f4…`, `S037` 200/89300/11194/`b204aa7f…`, `S038` 200/37806/3093/`09e077d3…`, `S039` 200/199797/37126/`657e7b4c…`, `S040` 200/94027/33463/`b7f7b55f…` — every field identical to the logged line. Snapshot mtimes (05:14 −0300) → `08:14:2xZ` match the logged `utc=` stamps. The side claim reproduces too: `curl -L` with a browser UA → `http=403`. |
| 5 | `c1-controls/base.{json,txt}` | recorded on line 1 of the `.txt`: `$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-controls/base --json .ufo/waves/round-25/c1-controls/base.json` | **yes** | JSON byte-identical including `root`; `.txt` identical after stripping the `$`/`EXIT=` wrapper lines; exit 1 as recorded. `diff -r` of the tree against `git archive` base: no differences. |
| 6 | `c1-controls/{M1-parse,M2-cwd,M3-paths,M4-degenerate}.{json,txt}` | same form, `--root`/`--json` per mutant | **yes** | 4/4 JSON byte-identical, 4/4 `.txt` identical modulo wrapper, exits 1 as recorded. Each mutant differs from `base` in exactly one knowledge file's `recheck:` line; all four mutants are pairwise distinct (1 differing file per pair). |
| 7 | `c1-controls/do-nothing.{json,txt}` | same form | **yes** | Reproduces; the `do-nothing` tree is byte-identical to `base` (JSON differs from `base.json` only in the `root` field), `diff-exit=0`. The control is the same measurement under a second directory name. |
| 8 | `c1-controls/mutants-diff.txt` | **no command recorded** (section headers only) | **partial** | Bodies reproduce with `diff -r -u <base> <mutant>`; the receipt's own header line reads `diff -r …` — one flag short of the invocation that produces its unified body (`diff -r` alone emits normal-format diffs, verified). The trailing `# recheck-manifest sha256 per tree` table is **not reproducible from its stated recipe** ("35 entry<TAB>line pairs, sorted"): 96 recipe variants (name/path/stem × 5 separators × prefix × sort key × trailing newline) plus lines-only all fail on `base 1f90e35f…`. No manifest artifact is committed. |
| 9 | `c1-controls/live-lane.json` | **no command, no `.txt` sibling, no input digest** | **no** | Point-in-time capture at 08:27:03Z: `pass=32`, `cwd_fail=3`, `lines=35`. The working tree has since moved (37 entries, `pass=37`); nothing in the receipt pins the bytes it measured, so the number cannot be re-derived. Superseded by #11. |
| 10 | `c1-before-strict.{json,txt}` | not recorded; recovered as `--root .ufo/waves/round-25/c1-controls/base --json .ufo/waves/round-25/c1-before-strict.json` | **yes** | Summary and all 35 entries byte-identical with the cutoff instrument; `.txt` identical modulo `BEFORE_EXIT=1`. `pass_strict=1/35`, `cdroot_fail=5` as recorded. |
| 11 | `c1-after.json` | not recorded; recovered as `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json` | **yes, today only** | Reproduces byte-identically (all summary keys + entries) with the instrument now on disk (`1ccee066…`), at `lines=37 total=37 pass=37 pass_strict=37 exit=0`. It carries **no exit status, no input digest, no instrument digest**, and measures uncommitted working-tree bytes. Its 05:33:43 version recorded `lines=36 pass=35 paths_fail=1 pass_strict=35` — the missing `corpus/source-snapshots/round-25/manifest.json` only landed at 05:37:35, so that version measured a half-written tree. |
| 12 | `c1-after.txt` | not recorded (no `$` line, unlike the control `.txt` files) | **yes** | 37 verdict lines + summary + `AFTER_EXIT=0` equal my rerun at cutoff. Omission: no command line. |
| 13 | `assimilation/ids/guard-proof.sh` + `guard-proof.txt` | self-documenting: the script prints each command and its exit before running it | **yes** | Ran from a `/tmp` copy (in-lane the script writes `fixture/*.ids`): transcript identical except the printed `lane root:` line. Exit 0. |
| 14 | `assimilation/ids/{reg-ids,staged-ids,collisions}` | no command recorded | **yes** | Re-derived: `reg-ids` = the 35 ids of `corpus/SOURCES.md`; `staged-ids` = the 94 ids of `shukuknow/merge/kasegi/SOURCES.append.md`; `collisions` = their intersection `S031…S035`. All three files match exactly. |
| 15 | `assimilation/ids/renumber-map.md` | no command recorded | **yes (by identity)** | All 5 staged→lane mappings resolve by URL against the staged package: S055→S036, S056→S037, S057→S038, S060→S039, S068→S040. |
| 16 | `assimilation/rows/SOURCES.append.block.md` | no command recorded | **partial** | 5 rows, all 5 URLs match the staged rows. Titles for S036–S039 differ from the staged title (vendor name added: サイボウズ / GMOペパボ), and the trailing columns differ — normalization is claimed but the transformation is not stated, so the rows are checkable by identity only, not by recipe. |
| 17 | `assimilation/rows/validate/corpus/SOURCES.md` | the block itself states the check: "Validate the mirror at assimilation/rows/validate/corpus/SOURCES.md" | **yes** | 40 rows = lane 35 + 5 appended; first 35 rows identical to `corpus/SOURCES.md`; `scripts/sources-census.sh validate --file …/validate/corpus/SOURCES.md` → exit 0 (only the pre-existing W04 S028/S029). |
| 18 | `wave1-spec.json` | generator present: `.ufo/waves/round-25/build-wave1-spec.py` (writes beside itself) | **yes** | Copied the generator to `/tmp/r25-spec` and ran it: output byte-identical to the lane file (38 items; role counter `reviewer 12, scout 7, executor 5, scribe 5, critic 4, mutation-tester 2, connector 1, sentinel 1, simplifier 1`). The spec file itself names no generator. |
| 19 | `wave1-dispatch.json` | **no generator in the repo** (schema `ufo-swarm-wave-dispatch-v1`; harness-emitted) | **not feasible** | Not reproducible by any command I can run. Internally consistent: `counts.total=38` = `spec.items` = `registry.members`, member sets identical. |
| 20 | `wave1/swarm-registry.json` | same (harness-emitted, `ufo-swarm-registry-v1`) | **not feasible** | Member set identical to `wave1-dispatch.json` (38/38, no extras either way). |
| 21 | `d24-3/receipt.txt` | recorded as `$` lines for both runs (`resolve-dispatch-check.py … --resolver .ufo/waves/round-25/d24-3/mut-bound8.py --json …/dispatch-mut8.json`; `mirror-containment-check.py … --json …/contain-mut8.json`) | **digests+counts yes; not re-run** | Every digest the receipt prints matches the bytes on disk: `resolver=88122e10…`, `checker=acbb6870…`, `matrix=fef0f02d…`, and the containment run's `matrix=d05b1e0c…` / `resolver_sha256=88122e10…`. Totals verified from the JSONs: `cases=8 pass=8 fail=0 exit=0` and `cases=24 escape=12 controls=12 pass=24 fail=0`. I did not re-execute the checkers because they materialise fixture trees; the recorded exit codes are therefore unverified, only the inputs and counts are. |
| 22 | `d24-3/digests.txt` | no command recorded | **yes** | Both lines match current bytes: `88122e10… mut-bound8.py`, `db5e0767… corpus/instruments/resolve.py`. |
| 23 | `d24-3/dispatch-mut8.json` | self-records `command`, `generated_at`, `resolver`/`resolver_sha256`, `matrix`/`matrix_sha256`, `checker_sha256` | **yes (self-consistent)** | The recorded `command` string is `…resolve-dispatch-check.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json` — it omits the `--resolver` flag that `receipt.txt` shows for the same run. Two receipts for one run disagree on the invocation. |
| 24 | `d24-3/contain-mut8.json` | self-records sha256s and `generated_at`, **no `command` field** | **partial** | Input digests all match; the command that produced it is not in the file (only in `receipt.txt`). |
| 25 | `build-manifest.py` (round-25 manifest generator) | usage recorded in its own docstring: `python3 .ufo/waves/round-25/build-manifest.py [--write]` | **not feasible (read-only seat)** | `--write` writes `corpus/source-snapshots/round-25/manifest.json`; I did not run it. The manifest exists (05:37:35) and the entry `recheck:` lines reference it. |
| 26 | `wave1-dispatch.err` | n/a | n/a | 0 bytes; nothing to check. |

## Findings

### P1 — the instrument pin was broken twice inside the wave (matches again as of 05:43:31)

`c1-instrument-digest.txt` is the only pin on `corpus/instruments/recheck-audit.py`, which is
**untracked** (`git status` → `?? corpus/instruments/recheck-audit.py`; absent from `b49948f`).
Observed chain:

| time (−0300) | instrument sha256 | bytes/lines | pin file says |
|---|---|---|---|
| 05:16:49 (pin written) | `d07af435…` | 8387 B / 216 | `d07af435…` + `3e3eeb4e… c1-before.json` — **matched** (I re-hashed at 08:26Z) |
| 05:34:28 | `4475d2e6…` | 13037 B / 288 | still `d07af435…` — stale |
| 05:39:20 (pin rewritten) | — | — | `6eb657c0…`, single line, `c1-before.json` line dropped |
| 05:39:56 | `1ccee066…` | current | stale again 36 s after the rewrite |

Consequences: (a) the before receipt reproduces only against the *behaviour* of the pinned
instrument — which I did verify, so its provenance holds — but a later verifier cannot recover
those bytes from the repo; (b) `c1-after.json` contains `pass_strict` / `strict_failing_limbs`
keys that the pinned instrument cannot emit, so the after receipt is provably **not** produced by
the pinned bytes; (c) the after receipt's own instrument digest is recorded nowhere. See the post-cutoff update
below: the pin matches the on-disk bytes again as of 05:43:31, but (a), (b) and (c) stand for the
earlier links in the chain.

### P1 — the after receipt measures uncommitted, still-moving bytes and records no anchor

`c1-after.json` (mtime 05:39:19, rewritten three times during my run: 05:33:43 `lines=36`,
05:37:59, 05:39:19 `lines=37`) reproduces byte-identically *right now*, but it records no exit
code, no digest of the 37 `recheck:` lines, and no instrument digest. The surface it measures grew
35 → 36 → 37 inside the wave (`vendor-disclosure-policies-as-corpus-objects.md` 05:37:04,
`vendor-disclosure-policy-commitments-crosswalk.md` 05:37:20), and the frozen predicate's literal
target is `lines=35 pass=35 exit=0`. **As frozen, C1's target denominator no longer exists**; the
after state needs either a re-freeze (surface = every `corpus/knowledge/*.md`) or an explicit
statement that the 35-line denominator is superseded. This is a closure blocker for C1, not a
defect of the receipt's arithmetic.

### P2 — `c1-controls/mutants-diff.txt` claims a digest table it cannot reproduce

The trailing table (`base 1f90e35f… 35`, `do-nothing` same, four distinct mutant digests) is
labelled "35 entry<TAB>line pairs, sorted" but no such recipe reproduces it, and the manifest it
digests is not committed. Its *intent* is nonetheless satisfied by evidence I did reproduce: base
and do-nothing are byte-identical, and each mutant differs from base in exactly one line and from
every other mutant. The digest column should be dropped or the recipe and the manifest committed.

### P2 — `c1-controls/live-lane.json` is unreproducible by construction

No command, no `.txt` sibling, no input digest; it records `pass=32 cwd_fail=3` at 08:27:03Z and
the tree has since changed. A point-in-time number with no anchor is not evidence; delete it or
add the 37-pair digest and the instrument digest it was taken with.

### P3 — before receipts omit their own invocation

`c1-before.json/.txt`, `c1-after.json/.txt`, `c1-before-strict.*` record neither the command nor
(for the `.txt` files) the root/foreign cwd. They are recoverable from `claims.json` plus the
instrument's docstring, but `claims.json`'s C1 counter string writes `c1-after.json`, not
`c1-before.json`, so the before invocation is inference. The control receipts got this right (the
`$ …` first line); the four primary receipts should follow the same convention.

### P3 — `mutants-diff.txt` header omits `-u`

The recorded `diff -r <a> <b>` line cannot produce the unified body beneath it; `diff -r` alone
emits normal-format diffs (verified). Reproduce with `diff -r -u`; the printed header should say so.

### P3 — `d24-3` receipts disagree on their own command

`dispatch-mut8.json` records `… --fixtures corpus/instruments/resolve-dispatch-fixtures.json` and
omits `--resolver …/mut-bound8.py`, which `receipt.txt` shows and which the JSON's own
`resolver_sha256` proves was used. `contain-mut8.json` records no `command` at all.

## Post-cutoff update (2026-10-25T08:46Z)

The pin was refreshed again while this report was being written, and this time it matches:

| time (−0300) | instrument sha256 | pin file |
|---|---|---|
| 05:43:26 / 05:43:31 | `8ab4dff7…` | `8ab4dff7…` — **matches** |

`c1-after.json` was regenerated at 05:43:31 and **still reproduces byte-identically** with the
current instrument (`lines=37 total=37 pass=37 pass_strict=37 exit=0`; `AFTER_EXIT=0`). So the
P1 finding narrows to two durable points rather than a live mismatch:

1. the pin is regenerated *after* each instrument edit, so every earlier pin in the chain was
   momentarily false — `d07af435…` (the bytes that produced the before receipt) and
   `4475d2e6…`/`1ccee066…` (the bytes that produced the 05:33 and 05:39 after receipts) exist
   nowhere in the repo; the before receipt's reproducibility rests on behaviour, not on bytes;
2. `c1-after.json` still records no exit code, no 37-pair input digest and no instrument digest,
   so its reproducibility is a property of the working tree at read time, not of the receipt.

Everything else in this report was measured against the files as they stood at the cutoff and is
unchanged by the later edits (the before receipts, capture log, controls, guard proof, id lists,
mirror registry, spec and d24-3 inputs all still hash as recorded in the table).

## Verdict on closure-checkability

**Before state and controls: closure-checkable. After state: not yet.**

- `c1-before.json` / `c1-before.txt` are checkable **today** and will stay checkable as long as
  (i) `b49948f` is reachable and (ii) the instrument bytes with digest `d07af435…` are recoverable.
  I reproduced the receipt exactly from `git archive b49948f` — all 35 entries, all 70 output
  digests, the summary line and the exit status. Condition (ii) currently fails: those bytes exist
  nowhere in the repo, and the pin file now names a third digest.
- The five control receipts, the strict-before receipt, the capture log, the guard proof, the id
  lists, the mirror registry, the spec and the d24-3 input digests all reproduce from their stated
  commands. That is a strong body of checkable evidence.
- The C1 *after* claim is not closure-checkable as frozen: the after receipt has no exit code and
  no input digest, its instrument is unpinned and was rewritten twice, and the measured surface
  (37) no longer matches the frozen denominator (35).
- C2's before limbs are checkable (`frontier=9` reproduces from `corpus/README.md`;
  entries citing S036+ = 0 on base bytes, 1 now), and the mirror registry validates exit 0 — but
  the *appended* rows do not yet exist in `corpus/SOURCES.md` (still 35 rows), so the C2 after
  state has no receipt to check.

Recommended minimal fixes, in order: commit the instrument and regenerate
`c1-instrument-digest.txt` from the committed file; add the command line to
`c1-before.json`/`c1-before.txt`/`c1-after.json`/`c1-after.txt` and `AFTER_EXIT`/`BEFORE_EXIT` into
the JSON receipts; record a 37-pair `recheck:`-line digest in `c1-after.json` (and the instrument
digest it ran with); drop or fix the `mutants-diff.txt` digest table and its `-u`; delete
`live-lane.json` or anchor it; state in `claims.json` whether the frozen `lines=35` surface is
superseded by "every `corpus/knowledge/*.md`".

## Residual risk and verification gaps

- I did **not** re-execute `resolve-dispatch-check.py` / `mirror-containment-check.py` (they
  materialise fixture trees); their `exit=0` claims are verified only through the committed JSON
  totals (`fail=0`, `pass=cases`), not through a live run.
- I did **not** run `build-manifest.py --write`; the round-25 manifest's own reproducibility is
  unchecked. Its presence at 05:37:35 is verified only by mtime and by the entries' `recheck:`
  lines resolving.
- The before reproduction used a `git archive` copy under `/tmp/r25-before`, not the lane root;
  `root` therefore differs in that JSON, and every other field matched. `/tmp` hit ENOSPC once
  during the session (host-wide, 36 GB of foreign scratch); my scratch dirs total < 2 MB.
- `wave1-dispatch.json` and `wave1/swarm-registry.json` are harness-emitted; I verified internal
  consistency (38 = 38 = 38, identical member sets) but not their provenance.
- Tooling: nothing installed or upgraded this seat.
