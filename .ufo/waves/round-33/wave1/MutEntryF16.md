# MutEntryF16 — mutation probe: F16 entry → frontier-recheck-count.py binding

Round 33 wave 1, seat MutEntryF16 (leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `690b69da`, freeze `6e55c8d5`. Scope: one mutation in an isolated scratch copy, same detector on pristine/mutated/restored bytes.

## Assignment (as dispatched)

- Mutate `{LANE}/corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`: drop the `source: S050` line — exactly one mutation.
- Run `python3 corpus/instruments/frontier-recheck-count.py` against the mutated lane (scratch root); item expects fail (exit 1, ids mismatch) "while the real entry passes (entries=19 pass=19)".
- Report killed|survivor. Write this receipt.

## Scratch (bounds 7, 12)

One live clone per seat, under `$HYAKU_SCRATCH/kasegi-r33/MutEntryF16/` (`HYAKU_SCRATCH` unset in env → default `/fast/scratch/hyaku`):

```
git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/lane"   # HEAD 53bfa59
cp -a /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/. "$S/lane/corpus/"   # overlay current working bytes
```

No tools installed this round (bound 5 record: none; preinstalled python3/git/coreutils only). No pacman. No git mutation in the lane (clone+overlay read the lane only). Seat wrote exactly one lane path: this receipt.

## PRE-STATE run (bound 6 label — never compared to after columns)

Before the F16 cluster landed (entry absent, no F16 README row), same command on the scratch overlay:

```
cd "$S/lane" && python3 corpus/instruments/frontier-recheck-count.py --root "$S/lane"; echo "PRE-STATE harness_exit=$?"
...
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
PRE-STATE harness_exit=0
```

Mechanics validated (detector runs end-to-end in scratch). Not evidence about F16.

## Subject landing (quiescence chain)

Entry byte history while wave seats iterated (all observed via `sha256sum`): owner-reported `d9b2acf2…` (21938 B) → `8d209995…` (21970 B) → `ce680d6c…` → owner-final `eebd5ea5…` (24318 B, receipt present) → `53c48b3b…` (306 lines; bytes of the first three-phase run, stable at t0 and t+45s) → **final digest `1f7ac0a2…` (306 lines, 24539 B; owner notified header/`recheck:` unchanged, edits confined to a Claim 1 question stem — verified here: `source:` lines on 3/4, `recheck:` on 7). The citable run below binds to `1f7ac0a2…`, stable at t0 and t+45s, equal to the lane file at citation time.** The `53c48b3b…` run is retained as an intermediate reproduction of the same verdict. F16 README row (ScribeReadmeF16), SOURCES S049/S050 rows (ExecRegistryAppend), and `corpus/source-snapshots/round-32/manifest.json` (ExecManifest32) all present before phase 1. Header on tested bytes: line 3 `source: S049 — …`, line 4 `source: S050 — …`, line 7 `recheck:` carrying both `--source S049` and `--source S050`.

## Phases 1–5 on intermediate digest `53c48b3b…` (verdict reproduced later on the final digest — see "Re-run on final digest")

## Phase 1 — pristine (intermediate digest)

```
$ cd "$S/lane" && python3 corpus/instruments/frontier-recheck-count.py --root "$S/lane"; echo "PRISTINE harness_exit=$?"
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
entries=19 pass=19 exit=0
PRISTINE harness_exit=0
```

Baseline PASSES → probe is conclusive (role rule: baseline failure = inconclusive). Before hash: `53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48`.

## Phase 2 — mutation (exactly one line dropped)

Single `edit` on the scratch copy: `old_string` = the full line-4 text `source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞处理和评分标准 V2.0 (2023.03.01), … S050.txt:69-71, 112, 113, 129, 418, 558, 591-593, 595-598, 601, 607, 611\n`, `new_string` empty.

```
MUTATED entry sha256 : c4b3e227b34218628a3aa452b6e80319b6047b7b867b0175175fbc455229b3f6
MUTATED line count   : 305 (pristine: 306)
MUTATED header lines : 1 (expect 1); S050-header occurrences: 0 (expect 0)
--- diff pristine -> mutated (exactly one deleted line):
@@ -1,7 +1,6 @@
 # Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC)
 
 source: S049 — https://zc.cnvd.org.cn/news/helpList — …
-source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞处理和评分标准 V2.0 (2023.03.01), … in capture corpus/source-snapshots/round-32/S050.txt:69-71, 112, 113, 129, 418, 558, 591-593, 595-598, 601, 607, 611
 verified-at: 2026-10-26
 ground: F16
 recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049 && python3 … --source S050   # 14 assertions …
```

`source: S049` and the `recheck:` line are untouched (visible as context lines in the diff).

## Phase 3 — mutated run

```
$ cd "$S/lane" && python3 corpus/instruments/frontier-recheck-count.py --root "$S/lane"; echo "MUTATED harness_exit=$?"
PASS     F01 … PASS     F15 (identical to phase 1)
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049           exit=0
entries=19 pass=19 exit=0
MUTATED harness_exit=0
```

The harness printed the weakened binding (`ids=S049` — proof it parsed the mutated header) and still counted the entry PASS: exit 0, no `problems=`, no ids-mismatch failure.

## Phase 4 — restoration evidence

```
$ cp -a "$S/entry.pristine.md" "$E"
RESTORED entry sha256: 53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48
RESTORED vs pristine diff bytes: identical   (cmp -s)
```

After-hash == before-hash, byte-identical (`cmp`). Scratch tree itself was pristine again at deletion (tasking declares the scratch copy disposable; bound 12 cleanup still applied).

## Phase 5 — restored run

```
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
RESTORED harness_exit=0
```

Detector reproduces the baseline on restored bytes.

## Re-run on final digest `1f7ac0a2…` (CITABLE — bounds 6/M30-3 re-run on quiescent bytes)

After the owner notified a further digest (`1f7ac0a2…`, edits confined to a Claim 1 question stem), scratch was recreated (same `git clone --shared` + `cp -a` overlay) and the full three-phase probe repeated on the settled bytes.

Phase 1 — pristine (before hash `1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1`, 306 lines, 24539 B):

```
$ cd "$S/lane" && python3 corpus/instruments/frontier-recheck-count.py --root "$S/lane"; echo "PRISTINE harness_exit=$?"
PASS     F01 … PASS     F15   (identical to the intermediate run, all exit=0)
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
PRISTINE harness_exit=0
```

Phase 2 — same single-line mutation (`source: S050` line dropped via one `edit`; `source: S049` and `recheck:` visible untouched as diff context):

```
MUTATED entry sha256 : 0144fc25165f54e0225e884b4d344599b511184ef074312a89553c6f00d63c22
MUTATED line count   : 305 (pristine: 306)
MUTATED header lines : 1 (expect 1); S050-header occurrences: 0 (expect 0)
--- diff pristine -> mutated (hunk header + deleted line only):
@@ -1,7 +1,6 @@
-source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞处理和评分标准 V2.0 (2023.03.01), … in capture corpus/source-snapshots/round-32/S050.txt:69-71, 112, 113, 129, 418, 558, 591-593, 595-598, 601, 607, 611
```

Phase 3 — mutated run:

```
$ cd "$S/lane" && python3 corpus/instruments/frontier-recheck-count.py --root "$S/lane"
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049           exit=0
entries=19 pass=19 exit=0
MUTATED harness_exit=0
```

Phase 4 — restoration:

```
$ cp -a "$S/entry.pristine.md" "$E"
RESTORED entry sha256: 1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1
RESTORED vs pristine: identical   (cmp -s)
```

Phase 5 — restored run:

```
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
RESTORED harness_exit=0
```

Lane stability at citation time: `1f7ac0a2…` at t0 and t+45s (`LANE_STABLE_AT_TESTED_BYTES=yes`).

## Verdict: SURVIVOR (coverage finding) — reproduced on both tested digests (`53c48b3b…`, `1f7ac0a2…`)

- Expected per item: exit 1, ids mismatch. Actual: `entries=19 pass=19 exit=0` on mutated bytes.
- Cause, read from `corpus/instruments/frontier-recheck-count.py` (read-only): rule A is implemented one-directionally — `header-sources-not-rechecked` fires only when `declared ⊄ recheck_ids`; there is no `recheck_ids ⊆ declared` check. The reverse direction is filtered through `selection-not-cited-by-entry`, but `cited` is every `S\d{3,}` occurrence in the whole file — always satisfied by the recheck line's own `--source S050`. Manifest and execution checks are unaffected by the header line.
- Paired control (peer-reported, ExecEntryF16, independent scratch): the mirror mutation — dropping `--source S050` from the recheck line — IS caught (`FAIL … problems=header-sources-not-rechecked`, exit 1). So the entry↔harness binding is enforced against dropping the recheck side but not against dropping the header side.
- Scope: this is a coverage finding on the instrument, not a defect in the entry (its header carries both `source:` lines on tested bytes) and not a license to change the contract (C2 frozen; corrections belong to the L1's append process). Note for C2 readers: the harness alone cannot detect a one-sided header-line drop; the complementary counter ("exactly 1 knowledge entry cites S049 and S050 on `source:` lines") is what covers this mutant.
- Detector limitation, recorded for honesty: the entry's `recheck:` line hardcodes `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`, so harness rule D executes against the real lane in every phase; the phase delta is therefore attributable solely to the static contract (rules A–C), which is where the mutation lives. Conditions of D were identical across all three runs.

## Lane integrity

No lane write by this seat (reads: `read`, `grep`, `sha256sum`, read-only `git rev-parse/ls-tree/log/status`; writes: scratch + this receipt). Lane entry hash at citation time t0 and t+45s: `1f7ac0a2…` (== tested bytes of the citable run; the earlier `53c48b3b…` run was equally stable against the lane bytes of its moment).

## Cleanup

```
rm -rf /fast/scratch/hyaku/kasegi-r33/MutEntryF16
ls /fast/scratch/hyaku/kasegi-r33/MutEntryF16   # No such file or directory
```
