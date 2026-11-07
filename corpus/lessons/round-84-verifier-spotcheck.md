# Round 84 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r84. Base `a089ff3d601b4d53a5515e52720ba27e5ec72c3d`, freeze `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b`, landing `c91c944fde0b2c9d62db14901c0aec2edb072950`, lane HEAD `e4593d6c992bd8e8668abf5be8503f86424be82d`. Report `.ufo/reports/round-84/kasegi.md` (fleet repo, commit `9b25b70da3be9a7fa02ca27de90349de89308a41`, author `kasegi-shokunin <kasegi@shokunin.local>`, 2026-11-06T21:12:50-03:00). Prompt `.ufo/prompts/kasegi-round-84.md` (commit `cfb5ecbb87253badc6c61760ff50520d30ed3b9e`, 929 lines).

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T20:32:33-03:00 launch kasegi round=84 pgid=3613247 driver=hyaku-inline attempt=1
2026-11-06T21:13:21-03:00 complete kasegi round=84; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-84/kasegi.md` | `kasegi-shokunin 9b25b70d…` (one commit, 31 s before the `complete` line) | ok |
| `SHONEN` heading, one line per box | read report §SHONEN vs `SHONEN.md` | heading present; 4 lines `[~] [ ] [~] [~]` for 4 boxes, matching `SHONEN.md` at HEAD | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for a089ff3d, 7f76b7eb, c91c944f, e4593d6c | all `commit`, all ancestors | ok |
| Lane pushed, clean | `jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain \| wc -l` | `local=remote=e4593d6c… ahead=0 behind=0 tracked=0 untracked=0`; `0`; `ls-remote origin refs/heads/master` = `e4593d6c…` | ok |
| Prompt carries template contract | grep of the prompt | §1 MISSION/AXES binding, §2 1–3 claims + lowest axis, §2b frontier step, §3 L2 floor, §4 report path + SHONEN, §5 commit/push scope/L0, write scope (l.448), commit order and report-lands-last (l.462–516), §6 hyaku addendum | ok |
| Report vs marker | report cites three real lane commits with work | real report | status `ok` |

Conformance defects (status-neutral):

- D-a: `claims.json` `controls` names `c1-candidate-r84.raw`; the committed control is `controls/c1-candidate-r84.txt` (no `.raw` in the tree at 7f76b7eb or e4593d6c). Contents match P3.
- D-b: the report states C2 "VERIFIED (B0–B8)" and the landing receipt is "over git archive of c91c944f", but B8 printed `header=bad … ENTRY-GATE-RESULT fail rc=1` on the extract; the passing B8 is a worktree re-run after `cmp` equality (appended section of `l1/L1-landing-r84.txt`). The reason (r83 entry-gate builds the recheck line from the manifest path relative to `--lane`) is disclosed. B8 is therefore not measured over the cited commit's extract; byte equality makes it equivalent, not identical, evidence.

## 2. Claims — re-check

### C1 — depth:verifiability (recheck-cwd census successor; nominal)

Re-measured by me over committed bytes (plain git/sha256/grep):

- P2: `git show <rev>:corpus/instruments/recheck-cwd-census.py | sha256sum` → base `343b21e4…08c9`; landing and HEAD `e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e`; frozen candidate `.ufo/waves/round-84/c1/recheck-cwd-census.py` at 7f76b7eb same hash. Holds.
- Frozen bytes: `git diff --stat 7f76b7eb c91c944f -- .ufo/waves/round-84/c1 controls/c1-stub-r84.py controls/c1-counter-mutants-r84.py` → empty. Landing hashes mutbat.py `c67e6912…`, mutant-table.json `daf05bac…`, build-table.py `4352368e…` equal `claims.json`. Kill rule's frozen-bytes limb holds.
- P8: `grep -i recheck-cwd | grep -c cases=33|cases=27` in SKILL.md and corpus/instruments/README.md → base `c33=0 c27=1` each; landing `c33=1 c27=0` each. Holds.
- P7: `grep -cE '^MUTANT H(0[1-9]|1[0-2]) verdict=SURVIVED'` → `c1-donothing-r84.txt` 12, last line `rc=1` (MUTBAT `target_sha256=343b21e4… killed=64 survived=12`); `c1-stub-r84.txt` 12, `rc=1` (`target_sha256=e77bd5f6… killed=64 survived=12 neutral_ok=3/3`). Holds.
- Selftest scope: landed census lists the six new check ids (`noprefix-only, summary-fields, entry-bare-pass, argv-values, verbose-order, entry-set`, l.320–321, checks at l.743–835) and the docstring `cases=33`.
- P3 per-row counts over the committed candidate control `controls/c1-candidate-r84.txt`: `grep -cE '^MUTANT [^ ]+ verdict=(KILLED|EXCEPTION-KILL) '` = 76; `grep -cE '^MUTANT H(0[1-9]|1[0-2]) verdict=KILLED '` = 12; MUTBAT `target_sha256=e5f2e4bd… baseline=ok rows=79 killed=76 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok`, `rc=0`.

Evidence-verified (lane-owned gate/counter runs; not executed by me per §Gate standard): `.ufo/waves/round-84/l1/L1-landing-r84.txt` (timestamp 2026-11-07T00:08:08Z, after c91c944f 21:08:00-03 and before e4593d6c 21:11:54-03) shows P1 `selftest cases=33 failures=0 rc=0`; P3 the same MUTBAT line plus `killed_lines=76 h_killed=12` (summary only — the per-row lines live in the freeze control); P4 `mutbat selftest ok`, `r84_limbs` all True, rc 0; P5 M09/M10/M12 `rc=0 selftest=ok` under r83 and `rc=1 selftest=FAIL` under r84, `as-expected`; P6 `entries=98 … RECHECK-CWD-RESULT conformant rc=0`.

Verdict: claim verifies. The scored meter (`resolve.py`/`anchorcheck.py`) does not read this instrument; score 4 → 4 nominal, disclosed by the lane (CriticTrend). Axis grade `improved` on the claim's own falsifiable before→after (kill set 64 → 76 of 76, selftest 27 → 33, counter limbs kill M09/M10/M12), consistent with r82/r83 closures; the nominal-move pattern is routed (§6).

### C2 — coverage (F60 on S118)

Re-measured by me:

| Measure | Command | base a089ff3d | freeze 7f76b7eb | HEAD e4593d6c | Reported |
|---|---|---|---|---|---|
| knowledge entries | `git ls-tree --name-only <r> corpus/knowledge/ \| grep -c '\.md$'` | 97 | 97 | 98 | 97 → 98 |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 117 | 118 | 118 | 117 → 118 |
| S118 status / used-by | S118 row cells | absent | `queued` / `—` | `mined` / `corpus/knowledge/osv-gcs-data-dump-layout.md` | queued → mined |
| distinct frontier ids | `grep -oE '\bF[0-9]{1,3}\b' corpus/README.md \| sort -u \| wc -l` | — | 59 | 60 | 59 → 60 |
| F60 in README / PROVINCE | `grep -c F60` | 0 / 0 | 0 / 0 | 4 / 1 | added |

Snapshot `corpus/source-snapshots/round-84/S118.txt` sha256 `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359` = manifest. Line 102 carries Q01 verbatim. Live re-open (below) finds all six manifest quotes once each. The landed entry no longer says "finds nothing" (`grep -c` = 0; M84-2 fix landed). Evidence-verified from the landing receipt: B0 six `OK occurrences=1`, B3 `FRONTIER-CENSUS rows=60 admitted=60 closed=60 problem-rows=0 registry=118`, `FRONTIER-PASS F60 ids=S118`, B4 `unbound=0`, B5 `recheck_exact=yes foreign rc=0`, B6 `literal_sweep_total 0 files 97`, B7 rc 0, B8 worktree `ruleless=0 untied=0 header=ok pass` (extract `fail`, see D-b).

Verdict: claim verifies. Coverage `improved` (score 8 → 8; denominator operator-owned). Claim 4 overlap with F59 is disclosed; the entry adds five layout statements F59 does not hold.

### Harm check

- `git diff --numstat a089ff3d e4593d6c -- SCORECARD.md LOG.md …` → SCORECARD `+24 -0`, LOG `+20 -0`, QUALITY `+1 -0`, README `+14 -0`, SOURCES `+2 -0`, PROVINCE `+2 -0`, SKILL `+1 -1` (pin row 27 → 33), SHONEN `+2 -2` (evidence pointers only, no box state change). Additions only in append-only files.
- depth:density: SKILL.md mean 273.2 → 273.2 (receipt § harm); SKILL change is one pin-row token. `unchanged`.
- No admitted entry fails its re-check (P6 98/98 conformant; census `kasegi ok`).

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | C1 P1–P8 hold (P2/P7/P8 + frozen bytes + per-row counts re-measured; P1/P3–P6 evidence-verified); nominal, score 4 → 4 |
| coverage | improved | C2 counts re-measured 97 → 98, F59 → F60, S118 queued → mined; live quotes re-found |
| depth:density | unchanged | 273.2 → 273.2; one pin-row token edit |

## 4. Discernment spot-check (`corpus/lessons/round-84.md` § Gate)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S118 OSV.dev Data sources → F60 | admit | `curl -sSL https://google.github.io/osv.dev/data/` → 200, final URL unchanged, 27419 bytes (= manifest raw size) | agree | All six manifest quotes occur exactly once in the live page after tag-strip/entity-decode/whitespace collapse; S118.txt:102 carries Q01 verbatim; tier A `docs` is the project's own page; claims scoped to export layout, F59 overlap disclosed |
| OSV data-quality initiatives post quote "Thereafter, we will begin gating record imports…" | reject (as pin) | `curl -sSL https://osv.dev/blog/posts/announcing-data-quality-initiatives/` → 200, 9941 bytes | agree | The sentence exists live (count 1) but the raw HTML wraps it across lines (`<p>Thereafter, … meet the quality` ends l.71), so a one-line snapshot pin cannot hold it; rejecting it as a pin and keeping the post as a lead is correct, and the flip condition (a 12-word one-line sentence) is concrete |

SOURCES row re-open: S118 (status `mined`, opened 2026-11-06, anchor "Data sources page, lines 99-123", used-by the F60 entry). The registry schema has no quote column; the row's ≤25-word pin is the lesson Gate quote at S118.txt:102 — `wc -w` = 17 words, verbatim on line 102 and live. ok.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → six inherited W04 (S028 S029 S072 S076 S080 S085), `kasegi ok`, rc 0 — matches the report's start/end receipts.

## 5. Trend verdicts

- expansion: improved — F60 is new ground (GCS export layout) on a newly mined tier-A source; knowledge 97 → 98, frontier 59 → 60.
- quality: improved — the landed census kills the twelve r83 survivors (64 → 76 of 76), the counter's selftest now fails M09/M10/M12, the landing receipt measures the cited commit's extract, and all 98 entries' rechecks stay conformant (P6); no entry found false or stale.
- discernment: improved — both spot-check items agree with the gate; M84-2 (captured-by none) became QUALITY R135 citing the lesson, with a check shown to fail on the draft and pass on the landing (`l1/r135-check-r84.txt`).

## 6. Routed defects (lane fixes next round)

1. D-b: make the C2 entry gate runnable over a `git archive` extract (manifest path not tied to `--lane`), so B8 is measured over the cited commit, not a cmp-equal worktree.
2. D-a: `claims.json` names `c1-candidate-r84.raw`; the committed file is `.txt`. Name controls by their committed path.
3. depth:verifiability has moved only nominally since r70 (CriticTrend); r85 must deliver the planned `resolve.py`/`anchorcheck.py`-read move or a recorded retire/split.
4. Carried C1 limits: MutC1Hunt r84 22 survivors; MutCounter 5 semantic survivors incl. M13 (`r84_ok` forced True — new limbs not self-protecting); CriticClaims A1 table-lookup forgery (F12 class); ExecC1RealTree exit 1 vs documented exit 2 on unreadable root.
5. P3's per-row counts are recorded only as a summary (`killed_lines=76 h_killed=12`) in the landing receipt; commit the per-row MUTANT lines of the landing run itself.
6. SHONEN box 2 (end-to-end domain task) still `[ ]`; considerthese proposal 2 planned for r85.

## 7. Operator notes

- SHONEN boxes 1, 3, 4 remain `[~]` with pointers to the r47 non-author spot-check; box 2 is unmet, so promotion is not yet checkable. Promotion is operator-owned.
