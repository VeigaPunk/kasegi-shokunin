# ScribeSkillGate — round 31 receipt

- **Seat:** `ScribeSkillGate` (role: `scribe`, leaf — no subagent dispatch, no background jobs of my own; two read-only poll loops were auto-backgrounded by the tool harness and are reported below)
- **Round/milestone:** kasegi-shokunin round 31, hyaku run 7, wave 1
- **Answering model actually run:** `devin/deepseek-v4-1-flash` (config route table decides; no model was passed by this seat)
- **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze commit `738a77999a00efbca129cfccb28a481037f6241f`; HEAD at run time `8a8916c7043bd873d191b30dd1744b241b91f4d9` (read-only `git log`)
- **Written by this seat:** `SKILL.md` (append-only, EOF) and this receipt only.
- **Skill read first:** `skill://godspeed` (named axes: depth:verifiability, coverage; cheapest parallel moves first).

## 1. PRE-STATE — SKILL.md before the append

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -l SKILL.md && sha256sum SKILL.md
```
```text
1057 SKILL.md
a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc  SKILL.md
```

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '; echo "EXIT=$?"
```
```text
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
EXIT=0
```

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/density.py SKILL.md --label r31
```
```text
# Density census — r31 (1057 lines, 23 blocks)
...
| | **mean dens** | | | | | | | | **171.1** |

Total path-citation instances: 662 across 23 blocks.
EXIT=0
```

Baseline for the item's density bar: mean **171.1** (r30 value, reproduced on the r31 label at the pre-append bytes).

## 2. Waiting for the gate receipt (item requirement)

Item: wait for `.ufo/waves/round-31/wave1/ExecLedgerMerge.md` (counter+ledger pass).

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && timeout 280 bash -c 'until [ -s .ufo/waves/round-31/wave1/ExecLedgerMerge.md ]; do sleep 20; done'; echo "poll_exit=$?"
```
Poll sequence (each a 20 s-interval read-only `until` loop; the harness auto-backgrounded four of them, so no busy-loop):

| poll | loop | observed result |
|---|---|---|
| 1 | `timeout 280 bash -c 'until [ -s … ]; do sleep 20; done'` | `poll_exit=124` after 280 s — receipt absent |
| 2 | same | `poll_exit=124` after 280 s |
| 3 | same | `poll_exit=124` after 280 s |
| 4 | same | `poll_exit=0` after 160 s — receipt appeared (23304 B, mtime `Oct 25 20:49`) |

Total wait ≈ 15 min, inside the 30-minute cap; no `BLOCKED:` line is due.

Receipt read in full (23304 B). It publishes FINAL digests: ledger `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be`, counter `cde7c2b6f74888dd2a841179002ad8583c3f57b4407db94b489063ce2747f275`, and both counter runs exiting 0 with `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`.

## 3. Counter run at append time (PRE-STATE label on the earlier pair)

First pair, run **before** the merge receipt existed while `ExecCounter` was still editing (PRE-STATE, non-comparative per M30-3):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json && time python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
```
```text
cde7c2b6f74888dd2a841179002ad8583c3f57b4407db94b489063ce2747f275  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
real	0m11.092s
counter_exit=0
```

Append-time (post-receipt) digests and run:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json corpus/instruments/recheck-audit.py corpus/instruments/source-recheck.py corpus/instruments/frontier-recheck-count.py corpus/instruments/score-gap.py SKILL.md
```
```text
f926bf75da3b734557bdd50a49c6c6d8aeac5bacfccc2dd0ad78fc4153428670  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb  corpus/instruments/score-gap.py
a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc  SKILL.md
```

The counter digest moved once more after the merge (`cde7c2b6…` → `f926bf75…`); both digests print the same 18 lines, so the registry row pins behaviour and names both digests.

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
```
```text
(13 identical `LIMB … verdict=killed` lines, 3 `CONTROL … ok=y` lines — same text as the block above)
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

Cwd independence (item asks for "exact invocation from any cwd"):

```sh
cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-mutation-check.py --ledger /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-ledger.json 2>&1 | tail -4; echo "exit=${PIPESTATUS[0]}"
```
```text
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
exit=0
```

Selftest (counts quoted from a live run, not retyped):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --selftest; echo "selftest_exit=$?"
```
```text
selftest killed                 verdict=killed               want=killed               ok
selftest survivor               verdict=survivor             want=survivor             ok
selftest invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
selftest invalid-noop           verdict=invalid:noop         want=invalid:noop         ok
selftest invalid-nocompile      verdict=invalid:nocompile    want=invalid:nocompile    ok
selftest invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
selftest invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
selftest invalid-nondeterministic verdict=invalid:live-baseline want=invalid:live-baseline ok
selftest validate-vacuous-signal rejected=True  want=True  ok
selftest validate-kill-reads-bytes rejected=True  want=True  ok
selftest validate-control-misbound rejected=True  want=True  ok
selftest validate-control-bound rejected=False want=False ok
selftest validate-valid-row     rejected=False want=False ok
selftest aggregate-green       ok
selftest aggregate-survivor    ok
selftest control-verdict-rule  ok
selftest cases=16 failures=0
selftest_exit=0
```

No-harm on the real corpus at the same bytes:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"; python3 corpus/instruments/source-recheck.py --selftest | tail -1; echo "sr_exit=${PIPESTATUS[0]}"; python3 corpus/instruments/frontier-recheck-count.py | tail -1; echo "harness_exit=${PIPESTATUS[0]}"
```
```text
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
audit_exit=0
selftest cases=10 failures=0
sr_exit=0
entries=18 pass=18 exit=0
harness_exit=0
```

## 4. score-gap.py run at append time (read-only; not a claim)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py | sed -n '6,25p'; echo "exit=${PIPESTATUS[0]}"
```
```text
source: SCORECARD.md sha256=5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=44 executes=20 gated=24 broken=0 exit=0
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- (lane total|SKILL\.md alone): ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
exit=0
```

```sh
cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py | head -3; echo "exit=${PIPESTATUS[0]}"
```
```text
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
exit=0
```

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py --selftest | tail -2; echo "selftest_exit=${PIPESTATUS[0]}"
```
```text
selftest exit2-no-threshold           ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE SCORECARD.md no longer names the score-5 threshold ('
selftest fields=7 failures=0
selftest_exit=0
```

Threshold location cross-checked independently (so the row does not retype a number from memory):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -n "unsupported current claims" SCORECARD.md | cut -c1-60
```
```text
331:| depth:verifiability (C1, lowest axis) | 4 | **4** | **Improved, score held.** 
```
(Only one hit in `SCORECARD.md`; the r25 tree had the same sentence at `:327`, so the line number is dynamic and the reporter prints it, never hard-codes it.)

## 5. The append

Append-only at EOF (R6). No existing line moved:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff --numstat SKILL.md && git diff -U0 SKILL.md | grep -c '^-[^-]' ; wc -l SKILL.md
```
```text
14	0	SKILL.md
0
1071 SKILL.md
```

`14 insertions / 0 deletions`, zero removed lines: pure EOF append, 1057 → 1071 lines. Section added: `## Round-31 Gates & probes registry addition (appended 2026-10-25)` — the same 8-column header as the round-29/30 sections, two rows, then three paragraphs.

Row 1 — `limb-mutation-check.py + limb-ledger.json`: entry command `cd <lane> && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json`; the five-step verdict order (`invalid:live-baseline` → `invalid:find-count` → `invalid:noop` → `invalid:nocompile` → `invalid:timeout` → `killed`/`survivor`) and the three exit codes (0 / 1 / 2); selftest `cases=16 failures=0`; pinned-value path `.ufo/waves/round-31/wave1/ExecLedgerMerge.md`; scratch-only, no git.

Row 2 — `score-gap.py`: type recorded as `reporter (read-only, NOT a claim)`; entry command `cd <lane> && python3 corpus/instruments/score-gap.py [--root DIR]`; exit map 0 (complete read, even when the gates it reads are red) / 2 (`score-gap: INPUT-UNREADABLE …`); selftest `fields=7 failures=0`; write scope none.

Paragraphs record, in the item's required order: what the counter proves (limbs load-bearing against the instruments' own selftest/fixtures, R13 in executable form); the 13-limb list with each limb's instrument and isolating fixture (`RA-parse`, `RA-cwd`, `RA-paths`, `RA-cdroot`, `RA-instrument`, `RA-own`, `RA-completeness`, `RA-expect-missing`, `RA-expect-unexpected` on `corpus/instruments/recheck-audit.py`; `SR-stem-mismatch`, `SR-occurrence-not-unique` on `corpus/instruments/source-recheck.py` via `corpus/instruments/limb-fixtures/sr/`; `FR-missing-entry`, `FR-duplicate-entry` on `corpus/instruments/frontier-recheck-count.py` via `corpus/instruments/limb-fixtures/fr/`); the byte-exact expected lines; the 3 controls and why a naive harness mislabels two of them; the measured digests and no-harm numbers; and the known limits (own-fixtures-only, limb-id-is-a-label/no `reach` field, `invalid:timeout` outside the frozen enum, equivalent mutants honestly `survivor`, scratch-only/git-free).

Quote discipline (CORPUS.md rule 1, Q3): the only quoted sentence is the score-5 bar, 15 words, location named (`SCORECARD.md` line 331) and independently grepped.

## 6. AFTER the append — the two gates the item names

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '; echo "anchorcheck_exit=${PIPESTATUS[0]}"
```
```text
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchorcheck_exit=0
```

Byte-identical to the PRE-STATE summary line in §1: same counts, same classes, exit 0. The append adds no anchored (backticked `:NN`) token — the one line-anchored location (`SCORECARD.md:331`) is deliberately written unbackticked so no new `CITE` instance appears, which is why the in-range count stays at 7 rather than drifting to 8.

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/density.py SKILL.md --label r31 | tail -5; echo "density_exit=${PIPESTATUS[0]}"
```
```text
| 23 | Round-30 Gates & probes registry addition (appended 2026-10-25) | 10 | 6 | 3 | 2 | 6 | 4 | 15 | 250.0 |
| 24 | Round-31 Gates & probes registry addition (appended 2026-10-25) | 12 | 8 | 27 | 2 | 18 | 6 | 53 | 662.5 |
| | **mean dens** | | | | | | | | **191.5** |

Total path-citation instances: 689 across 24 blocks.
density_exit=0
```

| measurement | before (1057 lines) | after (1071 lines) | bar |
|---|---|---|---|
| mean density | **171.1** | **191.5** | not lower than r30's 171.1 — met (+20.4) |
| blocks | 23 | 24 | — |
| path-citation instances | 662 | 689 (+27) | — |
| new block density | — | 662.5 (27 cites, 2 table rows, 18 unique numerics, 6 signatures, 8 non-blank lines) | — |
| `anchorcheck.py SKILL.md` | exit 0, 7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0 | identical line, exit 0 | same verdict classes — met |

Form was not gamed: the new block's 27 path citations are real lane paths and instrument names, its 18 unique numerics are the live measurements above (`44/44`, `20`, `24`, `18`, `13`, `16`, `7`, `2`, `9.05`, `6.32`, `1480`, `506`, `331`, `120`, `25/25`, `10`, `0`, `1`), and the two table rows carry digit-bearing cells. Nothing was reformatted to raise the score.

## 7. Known limits recorded in SKILL.md (and their provenance)

1. **Own-fixtures-only.** The ledger proves each limb load-bearing against the instrument's own `--selftest`/fixture trees; the SR/FR limbs run on `corpus/instruments/limb-fixtures/`, not on the 44 live recheck lines. A green ledger is not a statement about the live corpus. (Merge receipt §9-10.)
2. **Limb id is a label, not a proof of the patched line.** The frozen row schema has no `reach` field; mitigation is the per-row `note` plus the hand re-derivation of all 16 rows (merge receipt §7). A full `reach` gate is routed to the L1, not faked with a field the counter would drop.
3. **`invalid:timeout` is outside the frozen verdict enum** (counter emits it; routed, not exercised by any landed row).
4. **Equivalent mutants are honestly `survivor`** — `CTL-equivalent` is the proof that the counter does not inflate kills.
5. **Scratch-only, git-free.** The counter writes nothing into the lane and proves nothing about the lane's git state.
6. **score-gap.py is not a claim** and asserts no score move; its census field is the committed r18 census of record, not a live `resolve.py` re-run (that is a write owned by another seat).

## 8. Bounds compliance

- Writes: `SKILL.md` (append-only, EOF) and this receipt — both under the lane. Nothing written to the fleet root, sibling lanes, `templates/`, `scripts/`, `.ufo/state/`, `.ufo/watchdog.log`, `MANIFEST.json`, `.scratch/`, or `/home/vgpnk/Projects/shokuknow`.
- No git/jj mutation: only read-only `git log`, `git show`, `git diff`, `sha256sum`, `wc`. No commit/stash/checkout/reset, no jj command.
- No tool install or upgrade (none needed); no pacman transaction; no network fetch; no live bounty target contacted.
- Leaf role: no subagent dispatch, no delegation, no swarm. Four read-only poll loops were auto-backgrounded by the tool harness (each a bare `until [ -s … ]; do sleep 20; done`); no measurement or edit work was started in the background.
- Counter/score-gap runs touch only their own `tempfile.mkdtemp` scratch; nothing of mine remains outside the two written files.
- No credential material, session URL or vault reference appears in any byte written here.

## 9. Files changed by this seat

- `SKILL.md` (+14 lines, append-only at EOF; 1057 → 1071)
- `.ufo/waves/round-31/wave1/ScribeSkillGate.md` (this receipt)
