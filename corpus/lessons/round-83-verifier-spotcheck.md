# Round 83 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r83. Base `834bf78eaca70a69294f2ecfefa89b73c3fa85b8`, freeze `0cd499dbdfc0bf9ce3095681af9bc76588d76f31`, landing / lane HEAD `795f24da00348ee290378f679e4b23b5a5c80138`. Report `.ufo/reports/round-83/kasegi.md` (fleet repo, commit `cf84104fe2b82a2ee71c92b5459b7a8235c80cf7`, author `kasegi-shokunin`, 2026-11-06T20:27:45-03:00). Dispatched prompt `.ufo/prompts/kasegi-round-83.md` (fleet commits `c81bea24` attempt 1, `e963bd03` attempt 2).

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T18:42:33-03:00 launch kasegi round=83 pgid=3389712 driver=hyaku-inline attempt=1
2026-11-06T20:22:53-03:00 lane-dead-no-report kasegi round=83; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-83/kasegi.md)
2026-11-06T20:22:55-03:00 launch kasegi round=83 pgid=1593023 driver=hyaku-inline attempt=2
2026-11-06T20:27:55-03:00 complete kasegi round=83; hyaku-inline attempt=2
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-83/kasegi.md` (fleet) | `kasegi-shokunin <kasegi@shokunin.local> cf84104f… 2026-11-06T20:27:45-03:00` (after landing commit 20:26:52) | ok |
| `SHONEN` heading, one line per box | read report § SHONEN | 4 lines (`[~]`, `[ ]`, `[~]`, `[~]`) | ok |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 834bf78e, 0cd499db, 795f24da | `commit` ×3, `anc-ok` ×3 | ok |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state kasegi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `795f24da…` | ok |
| prompt carries the template contract | `diff <(sed -n 1,140p prompt) templates/round-prompt.md` | differences are only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §§1–5 present, hyaku §6 addendum appended | ok |
| frozen bytes unchanged freeze → landing | `git diff --stat 0cd499db 795f24da -- .ufo/waves/round-83/{c1,c2,controls,claims.json} corpus/source-snapshots/round-83` | empty | ok |

Conformance notes (status-neutral): (a) attempt 1 died mid-receipt (`lane-dead-no-report`); attempt 2 re-verified and landed the inherited tree, kept the partial receipt `l1/L1-landing-r83-attempt1-partial.txt`, and changed no frozen byte. (b) The landing receipt `l1/L1-landing-r83.txt` (header 2026-11-06T23:23:32Z) was measured over the uncommitted worktree before commit `795f24da`, not over the cited commit; the re-measurements in §2 over committed bytes close that gap for every pinned value. (c) Fleet commit `e963bd03` (dispatch evidence, author `kasegi-shokunin`) also carries other lanes' prompts, reports and MANIFEST rows — a driver commit-scope matter, not lane work; routed to the operator side.

## 2. Claims — re-check

Re-measured = a plain git/sha256sum/grep/wc measurement run by this closure over committed bytes. Evidence-verified = the lane gate's committed receipt read, not executed (PROTOCOL §Gate standard, Closure consequence).

### C1 — depth:verifiability (recheck-cwd census successor)

Re-measured:
- `git show <rev>:corpus/instruments/recheck-cwd-census.py | sha256sum`: base `81677e9d…3e050`, freeze `81677e9d…3e050`, landing `343b21e4…08c9`; `git show 0cd499db:.ufo/waves/round-83/c1/recheck-cwd-census.py | sha256sum` = `343b21e4…08c9` (P2: landed = frozen candidate).
- Counter/table/builder at landing: `2f7c49d4…1cb7d`, `5b1d99f5…6f44`, `890fff2c…0b69` — equal to the claims.json pins.
- Table: 67 rows, ids `G1 G2 G3 G4` present (python over `git show 795f24da:.ufo/waves/round-83/c1/mutant-table.json`).
- Census diff 834bf78e→795f24da adds `check("bucket-other"`, `check("bucket-over"`, `check("main-verbose"` and docstrings `cases=24` → `cases=27`.
- P8: `grep recheck-cwd | grep -o cases=N` over SKILL.md and corpus/instruments/README.md: `cases=24`/`cases=24` at base and freeze → `cases=27`/`cases=27` at landing.
- SKILL.md row correction (exit_other may be nonzero; buckets sum to entries) matches `conform_ok()` at `recheck-cwd-census.py:267-271`, which does not require `exit_other == 0`.

Evidence-verified (`.ufo/waves/round-83/l1/L1-landing-r83.txt`): 11× `FROZEN-OK`; P1 `selftest cases=27 failures=0` rc 0; P3 `MUTBAT target_sha256=343b21e4… baseline=ok rows=67 killed=64 survived=0 … neutral_ok=3/3 decoy=ok` rc 0; P4 twelve `FORGERY` lines — F9 r82 rc 0 → r83 rc 1 `killed=0`, F10/F11 r82 rc 0 → r83 rc 1 `decoy=broken`, F6/F7 rc 1 both, F8 r83 rc 0; P5 `RECHECK-CWD entries=97 … exit_other=0 …` / `conformant` rc 0; P6 `mutbat selftest ok` with `r83_forgeries={'count': (True, False), 'hashwl': (True, False), 'path': (True, False)}`; P7 do-nothing and stub `last=rc=1 survived_G=4`. Controls `controls/c1-donothing-r83.txt` and `c1-stub-r83.txt` were committed in the freeze.

Ruling: C1 verifies (P1–P8 true; frozen bytes unchanged). Score 4 → 4 nominal (R58); the measured move (60 → 64 case-matched kills, F9–F11 newly rejected) grades `improved`. Disclosed limits, agreed: CriticClaims F12 (marker-aware) and F13 (F11 + comment strip) pass the r83 counter (`w1/CriticClaims.md:40,65,202`), and P3 reads the summary line, which a target controls — so the claim's class phrase "count forgeries" holds for F11's bytes only (M83-1 recurrence). This bounds the prose, not the predicates.

### C2 — coverage (F59 on S117)

Re-measured:
- `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'`: 96 (base, freeze) → 97 (landing).
- `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`: 116 base → 117 freeze → 117 landing.
- `git diff -U0 0cd499db 795f24da -- corpus/SOURCES.md`: one `-`/`+` row pair (S117) plus one registry-changes note line; landing S117 status `mined`, used-by `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` (B1).
- `knowledge-expected.txt` diff: `+corpus/knowledge/osv-faq-post-import-record-lifecycle.md` only (B2).
- `corpus/README.md` Frontier rows `grep -cE '^\|[[:space:]]*F[0-9]+'`: 60 → 61; `| F59 |` row at README:1271.
- Snapshot `git show 795f24da:corpus/source-snapshots/round-83/S117.txt | sha256sum` = `0a5fa51c…e53e` (manifest pin).
- Entry `recheck:` line = `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` + the B0 command (read at entry:5).

Evidence-verified (landing receipt): B0 `S117:sha256 OK` + six `OK occurrences=1 anchor=<n>-ok`; B3 `FRONTIER-CENSUS rows=59 admitted=59 closed=59 problem-rows=0 registry=117`, `FRONTIER-PASS F59 ids=S117`; B4 `records=97 bound=97 unbound=0`; B5 `foreign rc=0`; B6 `literal_sweep_total 0 files 96`; B8 `ruleless=0 untied=0`, `ENTRY-GATE-RESULT pass`, and filler/crosscite/copyrule rc 0 under r82 → rc 1 `untied=1` under r83. The same control block records admitted F57 (`osv-importfindings-record-quality-feedback.md`) at `untied=1` under r83 — the disclosed M83-2 false positive; agreed it shows G6 is lexical, and it does not falsify B8 (which names the new entry and the three forgeries).

Ruling: C2 verifies (B0–B8 true). Score 8 → 8 (denominator operator-owned); frontier 58 → 59 grades `improved`.

### Harm check

- `git diff 834bf78e 795f24da -- SCORECARD.md`: additions only (22 lines, 0 deleted): `## Round 83`, move log, planned r84.
- `git diff --numstat` LOG.md 13/0, PROVINCE.md 2/0, corpus/QUALITY.md 1/0, corpus/README.md 14/0, corpus/SOURCES.md 2/0 (one row rewrite counted as +1/−1 in the row pair), SKILL.md 1/1 (pin-row widening).
- depth:density: receipt § harm `272.8 → 273.2` (evidence-verified; the only SKILL.md change is the one pin row) — `unchanged` (9 → 9).
- Census (B7), run by this closure: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`, six inherited W04 (S028 S029 S072 S076 S080 S085), rc 0.
- The SCORECARD move log also lists a `calibration` row (SKILL/README recheck-cwd rows corrected). It is not a frozen claim; this closure verified the correction is true (see C1) and does not credit it as an axis move.

No owned axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | improved | C1 re-measured (sha/pins/checks) + evidence-verified (P1, P3–P7) |
| coverage | improved | C2 re-measured (knowledge 96→97, frontier rows 60→61, S117 mined) + evidence-verified (B0, B3–B6, B8) |
| depth:density | unchanged | SKILL.md one-row diff; receipt 272.8 → 273.2, score 9 → 9 |

## 4. Discernment spot-check (`corpus/lessons/round-83.md` § Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| F59 `osv-faq-post-import-record-lifecycle.md` on S117 | admit | `curl https://google.github.io/osv.dev/faq/` → HTTP 200, 34381 B (byte size equal to the lane's raw capture); the six manifest quotes searched in tag-stripped text | agree | Q01, Q02, Q04, Q05, Q06 each occur exactly once; Q03 ("if more than 10% of records are about to be marked as withdrawn, OSV.dev aborts and does not proceed.") is present in the raw `<li>GCS sources…` item, split only by a `<code>withdrawn</code>` tag (my stripper's spacing artefact); snapshot `S117.txt:121` carries it. The quotes are the project's own statements of post-import behaviour, distinct from F57/F58. |
| "Managing the Perishability of OSV Records" (r82 lead) | reject (no public copy) | `curl https://raw.githubusercontent.com/google/osv.dev/master/docs/data_quality.md` line 13 (names it as a future companion, no link); `api.github.com/search/issues?q=repo:google/osv.dev+Perishability` → `total_count 0`; repo tree `git/trees/master?recursive=1` → 1760 paths, none containing "perish"; web search for the exact title found only the forward reference | agree | Only the title exists; a title with no openable document is a lead, not a source (SOURCES contract: a lead is never a row). Flip condition (a captured public copy) is correctly stated. |

SOURCES row re-opened: S117 (`corpus/SOURCES.md`, the round's one new row). The row carries no inline quote; its anchor cell points to `corpus/source-snapshots/round-83/manifest.json`, whose six quotes are 11, 6, 19, 12, 17, 12 words (max 19 ≤ 25), each located once on its anchor line (B0) and re-found live above. Teaches/scope cells match the entry and exclude F57/F58 ground. Conformant.

## 5. Trend verdicts

- **expansion: improved** — knowledge 96 → 97, Frontier F58 → F59, registry 116 → 117 with S117 mined; literal sweep 0 over the other 96 entries.
- **quality: improved** — landed census kills 64/64 case-matched rows including G1–G4 that r82 bytes and the stub let survive; counter rejects F9–F11 that r82 accepted; selftest 24 → 27.
- **discernment: improved** — both spot-checked gate decisions agree on re-open; wave falsifications of the lane's own prose (F12/F13, G6 false positive on F57) were recorded as M83-1/M83-2 and QUALITY R134 rather than hidden; r82 routed defects 1, 2, 3, 6 answered.

## 6. Routed defects (lane fixes next round)

1. C1 counter: F12 (marker-aware) and F13 (comment-stripping count) pass the r83 counter; adopt the rename-based D3 decoy or declare both beside F8 and add them to `mutbat --selftest` (`w1/CriticClaims.md:202-211`).
2. C1 predicate P3 reads only the `MUTBAT` summary suffix, which the target controls; add a per-row verdict or `target_sha256` limb.
3. Counter selftest does not exercise the `extra` limb (MutCounter M09).
4. Entry gate G6 is lexical: six echo rules pass and admitted F57 Claim 2 fails (`untied=1`); land a non-lexical tie per R134, and record F57's G6 status.
5. MutEntryGate 8/16 survivors (6 behaviour-changing); MutC1Hunt r83 gaps.
6. `comment_lines` latent f-string issue (ReviewC1 Major 1).
7. Landing receipts must be measured over the cited commit (or carry its hash), not a pre-commit worktree.
8. Carried from r82: defect 4 partly answered, 5 and 7 carried (`corpus/lessons/round-83.md` § Routed-defect disposition).

## 7. Operator notes

SHONEN boxes: three `[~]` and one `[ ]` (no end-to-end domain task logged); none is fully checkable by a non-author from this round's evidence. No promotion signal.
