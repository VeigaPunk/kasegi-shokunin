# ExecHarnessUpdate — round-40 wave-1 receipt (knowledge-expected list sync)

Seat: executor, leaf. Item: deliver the full new `corpus/instruments/knowledge-expected.txt` bytes after the
round's knowledge additions, and record the audit against a scratch mirror if the target state exists.
Axes: depth:verifiability (the audit's expected-set equality is a C2 counter), coverage (expected count must rise
51 -> 59 with the round's eight entries).

## Deliverable

`.ufo/waves/round-40/wave1/ExecHarnessUpdate.knowledge-expected.txt` — land at
`corpus/instruments/knowledge-expected.txt`.

- 61 lines: 2 comment lines (byte-identical to HEAD) + 59 entry lines.
- sha256 `328041466810f72e7900669e811d36d0434991503e57bec4f1817921b31714a2`.
- C-locale sorted, one lane-relative `corpus/knowledge/<entry>.md` path per line:
  `diff <(grep -v '^#' F) <(grep -v '^#' F | LC_ALL=C sort)` -> empty, exit 0.
- Header lines deliberately unchanged (they still read "round 30"; nothing parses them, and r31-r39 kept them,
  so the diff is insertions only). The audit requires set equality, not the round number.

Delta = +8 insertions, 0 deletions. Lines 4, 8, 9, 21, 24, 25, 39, 45 of the file:

```
4:corpus/knowledge/anthropic-cvd-provenance-and-pacing.md
8:corpus/knowledge/cisa-bod-20-01-vdp-minimums.md
9:corpus/knowledge/cisa-cvd-program-stages.md
21:corpus/knowledge/cve-bench-agent-exploitation-benchmark.md
24:corpus/knowledge/cyclonedx-analysis-subtree.md
25:corpus/knowledge/doj-vdp-framework-scope-and-authorization.md
39:corpus/knowledge/nist-sp800-216-vdp-framework.md
45:corpus/knowledge/pz-reporting-transparency-trial.md
```

## Why exactly these eight names

The basenames are not guesses: each is the `used-by` cell the row scribe committed in
`ScribeRows.decisions.txt` (S016/S017/S019/S020/S021/S023/S025) and `ScribeNewRows.txt` (S060), and each entry
scribe then named its deliverable with that exact slug. Registry contract and entry filename agree in all eight
cases.

| id | used-by path (registry) | delivering seat | entry deliverable (lines / sha256) |
|---|---|---|---|
| S016 | corpus/knowledge/anthropic-cvd-provenance-and-pacing.md | ScribeEntriesG1 | 132 / 9536e1b321dd285a1e3f3552a26edd5d6e4f8c6c58d8620446b4c4331ea01f38 |
| S017 | corpus/knowledge/pz-reporting-transparency-trial.md | ScribeEntriesG1 | 136 / 270b6a0a73061d85063a463a120c87c6786a6bf03a7cc492a949383034408c1a |
| S019 | corpus/knowledge/nist-sp800-216-vdp-framework.md | ScribeEntriesG1 | 121 / 757058a5d8e03c83c61c6b7c22852400bcbea1b252504a9e8f5c7a56da79d596 |
| S020 | corpus/knowledge/doj-vdp-framework-scope-and-authorization.md | ScribeEntriesG2 | 139 / 25f357f1458cd15ea25b73afafc8bf9caf4a81bfcc35aad0c6abab20cf372e48 |
| S021 | corpus/knowledge/cisa-bod-20-01-vdp-minimums.md | ScribeEntriesG2 | 162 / f83a03cd9307fae0ffbdbbd6dc3cfb40d03725a13fa0e2247ed00a9a9910274c |
| S023 | corpus/knowledge/cisa-cvd-program-stages.md | ScribeEntriesG2 | 134 / 3fd49ca4b5bb2a17f65aa92c8762f2473796cdfe06be16174dad430c5233b4a4 |
| S025 | corpus/knowledge/cve-bench-agent-exploitation-benchmark.md | ScribeEntriesG2 | 141 / dd6c780e82c51a2b4dd11229d7cf5174c9709c241d052b5d6eb754c199c20c19 |
| S060 (F23) | corpus/knowledge/cyclonedx-analysis-subtree.md | ScribeF23 | 322 / 5a549e312237372a639931cc980ea697f60d383999790b9d48d5df4bd5d1978c |

No other knowledge entry is added this round: `ScribeNewRows.txt` carries `used-by` `—` for S061 and S062 (no
entry), and the assimilation seat adopted zero staged rows (`ExecAssimilation.txt`: "**Adopted: 0. Adoptable under
PROVINCE/QUALITY this round: 0.**"). So N = 8 and 51 + 8 = 59, matching the formula ExecAuditRun circulated.

## Method (no lane writes; all work in scratch)

1. Baseline: `LC_ALL=C diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt) <(ls corpus/knowledge/*.md | LC_ALL=C sort)`
   -> empty; `grep -v '^#' ... | LC_ALL=C sort -c` -> exit 0. The committed list already equals the tree at HEAD.
2. Derivation rule, implemented once (`regen-expected.py`, scratch): keep the `#` header lines, then one
   `corpus/knowledge/<entry>.md` per globbed entry, sorted on the encoded bytes. Run against HEAD it reproduced
   the committed 53-line file byte-for-byte (`REGEN_IDENTICAL_TO_COMMITTED`), so the rule is the one the file was
   built with, not a new convention.
3. Scratch mirror of the integration state: `git -C <lane> archive HEAD | tar -x -C full`, then
   `assemble-manifest.py` wrote `corpus/source-snapshots/round-40/` from the scouts' own records and captures
   (8 sources: S016, S017, S019, S020, S021, S023, S025, S060; S025's record is already wrapped in
   `{"schema_version":1,"purpose":..,"sources":[..]}`, the rest are bare source records and were wrapped).
4. The eight entry deliverables were copied to their `used-by` basenames under `full/corpus/knowledge/`, and the
   expected list was regenerated from that tree: it is byte-identical to the delivered file
   (`diff full.txt <deliverable>` -> empty, `DELIVERABLE_EQUALS_TREE_DERIVED_59`). The deliverable is therefore
   tree-derived, not incremented by hand.

## Measurements

Lane tree as it stands (pre-integration, 51 entries, committed expected list):

```
$ python3 corpus/instruments/recheck-audit.py --quiet --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
strict pass=51/51 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=27 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=51 total=51 pass=51 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=51 missing=0 unexpected=0 exit=0
rc=0
```

Full mirror = HEAD tree + round-40 captures/manifest + the eight entries + the delivered list:

```
$ python3 full/corpus/instruments/recheck-audit.py --quiet --root $S/full \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin
strict pass=59/59 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=27 gated=32 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=59 total=59 pass=59 fail-closed=32 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=59 missing=0 unexpected=0 exit=0
rc=0
```

(`--cdroot <lane>` because every `recheck:` line `cd`s to the real lane; the mirror alone would fail the strict
`cdroot` limb by construction — the entries carry the lane's absolute path, as the round-39 counter requires.
`--root $S/full` is what makes `paths` and the expected-set equality read the integration tree.)

Intermediate states, same instrument: F23 entry alone -> `strict pass=52/52 ... expect=present expected=52
missing=0 unexpected=0 exit=0`; F23 + the three G1 entries -> `strict pass=55/55 ... expected=55 missing=0
unexpected=0 exit=0`.

All eight new entries pass every strict limb and the expected-set equality; each is reported `gated`
(`lane=2`) because its `recheck:` line `cd`s to the lane, which has no `corpus/source-snapshots/round-40/manifest.json`
until the L1 lands the captures. Per-entry lines from the full mirror:

```
anthropic-cvd-provenance-and-pacing.md                     frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
cisa-bod-20-01-vdp-minimums.md                             frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
cisa-cvd-program-stages.md                                 frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
cve-bench-agent-exploitation-benchmark.md                  frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
cyclonedx-analysis-subtree.md                              frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
doj-vdp-framework-scope-and-authorization.md               frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
nist-sp800-216-vdp-framework.md                            frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
pz-reporting-transparency-trial.md                         frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
```

The gated class is the manifest dependency, not a defect in the list: run against the mirror manifest, the same
pinned-quote comparison each entry's line wraps returns green for all eight sources:

```
S016 rc=0 lines=4 first=S016:sha256 OK
S017 rc=0 lines=4 first=S017:sha256 OK
S019 rc=0 lines=4 first=S019:sha256 OK
S020 rc=0 lines=2 first=S020:sha256 OK
S021 rc=0 lines=2 first=S021:sha256 OK
S023 rc=0 lines=3 first=S023:sha256 OK
S025 rc=0 lines=3 first=S025:sha256 OK
S060 rc=0 lines=4 first=S060:sha256 OK
```
(`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source <id>`
inside the mirror.)

## Integration notes / risks

- Land the expected file with the eight entries. If only some entries land, regenerate instead of trusting 59:
  `{ grep '^#' corpus/instruments/knowledge-expected.txt; ls corpus/knowledge/*.md | LC_ALL=C sort; } > /tmp/e && mv /tmp/e corpus/instruments/knowledge-expected.txt`
  then `python3 corpus/instruments/recheck-audit.py --quiet` must print `expected=<entries> missing=0 unexpected=0 exit=0`.
  Landing entries without this file is the failure mode it prevents (`unexpected=8`).
- The new entries stay `gated` until `corpus/source-snapshots/round-40/manifest.json` exists in the lane. The mirror
  proves the manifests the scouts produced are sufficient: 8 records, `sha256 OK` and every pinned quote
  `occurrences=... anchor=N-ok`. Two landmines the L1 should keep: S025's manifest record is already
  schema-wrapped (do not wrap twice), and ScoutF23Lead used the provisional id **S060** — if the F23 row is
  renumbered, the `S060.txt` capture name, the record `id`/`path`, and that entry's `source:`/`recheck:` lines must
  move together; the expected-list basename (`cyclonedx-analysis-subtree.md`) is content-derived and survives a
  renumber.
- `S019.txt` is the NIST landing page, not the SP 800-216 PDF (`ScribeRows.decisions.txt` records that). That is a
  coverage judgement for the mining seat, not an expected-list question; the name is already fixed by `used-by`.
- I wrote only this receipt and `ExecHarnessUpdate.knowledge-expected.txt` in the wave dir. `corpus/knowledge/`
  gained nothing from me (`git ls-files --others --exclude-standard corpus/knowledge` -> 0), and
  `git diff HEAD -- corpus/instruments/knowledge-expected.txt` is empty: the list is delivered, not landed.

## Tooling

Nothing installed or upgraded. Read-only git (`archive`, `diff`, `ls-files`) only; no mutating git/jj command.
Disk guard was green before the heavy steps (`/fast/scratch/hyaku` 26%).

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ExecHarnessUpdate/` (mirrors, manifest assembler, regen script, projected/full
lists) removed after the receipts and deliverable were in the wave dir.
