## Round 78 — draft SCORECARD section (kasegi, attempt 1)

**Landing note.** This is the L1's landing draft for the `SCORECARD.md` round-78 section. The measured
commit is the literal token `LANDING_HASH`; the L1 replaces it with the landing commit hash. The two claim
verdict cells are left as the L1's to fill — this seat does not score claims. Every other number below is a
measured value with its command.

Frozen claims: `.ufo/waves/round-78/claims.json` (freeze `2d81fe84506b323fb32beb137d5bd21db6a5c13d`, base
`0687cca8645884aba30c8eb5fa2d8ecaca7245cf`). Attempt 1; wave `w1` (one v1 wave, 12 seats; attack seats 5/12:
reviewer×2, critic, mutation-tester, sentinel). Receipts `.ufo/waves/round-78/w1/` and
`.ufo/waves/round-78/controls/`.

| Axis | Score before r78 | Score after r78 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability (lowest) | 4 | 4 (held; C1 not landed as of this draft) | Base counter unchanged at sha256 `e666ae11…`. Base selftest `cases=6 failures=0` rc 0; base nonexistent-TMPDIR run rc 1 with a `FileNotFoundError` traceback (`controls/c1-base-missing-tmpdir-r78.txt`). Build candidate `.ufo/waves/round-78/w1/successor/recheck-cwd-census.py` (sha256 `f68499715f38b6e74f368c441766954a240d7f5036d68157110e5017c8457db1`): selftest `cases=13 failures=0` rc 0, TMPDIR refusal rc 2 with `recheck-cwd: TMPDIR …`, real-tree census `entries=91 … restoration_only=0` conformant rc 0 — but the named-kill set measures 7/8: K-X2 exits 0 with `cases=13 failures=0`, so P3's kill rule is not met on these bytes. | r77 (held r78) |
| coverage | 8 | 8 (held; C2 admission is the L1's to land) | S112 row `corpus/SOURCES.md:124` `queued` -> `mined` at `LANDING_HASH`, `used-by —` -> `corpus/knowledge/osv-post-batch-query-contract.md`; one row changed, none added or removed, registry stays 112. Manifest `corpus/source-snapshots/round-78/manifest.json` carries seven quotes (Q01, Q02, Q03, Q09, Q10, Q11, Q13) on exact snapshot lines 24, 24, 24, 166, 168, 169, 195; `source-recheck.py` prints `S112:sha256 OK` and seven `OK occurrences=1 anchor=<n>-ok` lines rc 0 (`controls/c2-prerecheck-r78.txt`). B6: 0 of 91 admitted entries contain any of the seven quotes as a literal substring. Knowledge 91 -> 92; frontier `rows=53` -> `rows=54`. | r77 (held r78) |
| depth:density | 9 | 9 (not targeted; not re-measured) | — | r15 (held) |

**Counting commands, per claim.** Each command is runnable as written; `<scratch>` is a seat scratch
directory that exists, and `<lane>` is the lane root.

C1 (depth:verifiability) — `TMPDIR=<scratch>/tmp python3 -B corpus/instruments/recheck-cwd-census.py --selftest`
(the P1 selftest; base bytes print `selftest cases=6 failures=0`, the landing bytes print
`selftest cases=13 failures=0`, both rc 0);
`TMPDIR=<scratch>/tmp python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>`
(the P2 real-tree census; prints `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` and `RECHECK-CWD-RESULT conformant`, rc 0);
`TMPDIR=/nonexistent-kasegi-r78 python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>`
(the P4 refusal; base bytes rc 1 with a traceback, landing bytes rc 2 with a line beginning
`recheck-cwd: TMPDIR` and no traceback);
and the named-kill set, P3: `for m in K-M1 K-M2 K-M3 K-M4 K-M5 K-X1 K-X2 K-M8; do TMPDIR=<scratch>/tmp python3 -B <mutant-$m.py> --selftest >/dev/null 2>&1; echo "$m rc=$?"; done` —
killed = count of rc != 0 with a `FAIL` line. On the build candidate bytes this measures 7 of 8: K-M1 rc 1
(failures 3), K-M2 rc 1 (failures 1, `gate-negpolarity FAIL neg_ok=True`), K-M3 rc 1 (failures 2, the logged
exception class), K-M4 rc 1 (failures 1), K-M5 rc 1 (failures 1, `gate-checkids FAIL missing=['both-headers']`),
K-X1 rc 1 (failures 1), K-M8 rc 1 (failures 1), and K-X2 rc 0 (`cases=13 failures=0`) — a survivor. The
frozen table's K-X2 anchor text is absent from the candidate bytes and the natural adaptation of the
transform also survives; receipts in `.ufo/waves/round-78/w1/ScribeLesson-evidence-r78.txt` §4. The review
seat reaches the same verdict independently and re-derives the mutant byte-identically
(`w1/ReviewC1.md` Finding 1, BLOCKER). A landing commit that fixes this must re-measure the same eight
commands.

C2 (coverage) — `python3 corpus/instruments/frontier-recheck-count.py` (the B3 frontier census; before
`FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112`, after `rows=54 admitted=54
closed=54 problem-rows=0 registry=112`, rc 0);
`ls corpus/knowledge/*.md | wc -l` (the B2 knowledge count; 91 before, 92 after);
`wc -l corpus/instruments/knowledge-expected.txt` (B2; 93 lines / 91 `.md` rows before, 94 lines / 92 `.md`
rows after);
`grep -cE '^[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` (the B1 registry count; 112 before and
after);
`git diff 0687cca8645884aba30c8eb5fa2d8ecaca7245cf..LANDING_HASH -- corpus/SOURCES.md` (B1; exactly one
changed row, zero added, zero removed);
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112`
(B0/B5; `S112:sha256 OK` and seven anchored OK lines, rc 0);
`python3 corpus/instruments/capture-binding-check.py` (B4; `records=92 bound=92 unbound=0`, rc 0);
`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (B7; rc 0 with the six
inherited W04 duplicate-url warnings S028, S029, S072, S076, S080, S085 and no new finding);
and the B6 sweep, run per claimed quote over `corpus/knowledge/*.md` excluding the new entry, which returns
zero files for all seven. The paraphrase half of B6 is recorded per clause in the lesson's `## Gate`
(`w1/ScoutDistinct.md` §1): 3 novel (Q01, Q03, Q11), 4 partly-held scope overlaps (Q02, Q09, Q10, Q13), 0 held
— no claimed clause restates admitted F51 ground.

**Registry change, old -> new.** `corpus/SOURCES.md:124` (S112): status `queued` -> `mined`; used-by `—` ->
`corpus/knowledge/osv-post-batch-query-contract.md`. One row changed; the registry row count stays 112.

**Claim verdicts.** L1 to fill: C1 <VERIFIED|NOT VERIFIED as declared> — note the P3 kill-set measurement of
7 of 8 on the build candidate bytes (K-X2 survives; see the L1 open items in
`.ufo/waves/round-78/w1/lesson-round-78.md`). C2 <VERIFIED|NOT VERIFIED as declared> — B0 through B7 measure
true on the current tree with the seven frozen clauses.

**Measured commit.** `LANDING_HASH` (to be filled by the L1 with the round-78 landing commit).

**Capabilities:** none entered. **Saturation:** line 9/10 held; no retirement, split or nudge waiver.

### Round-78 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 78 | depth:verifiability | census selftest `cases=6`; nonexistent TMPDIR -> rc 1 traceback | candidate selftest `cases=13 failures=0`; nonexistent/non-directory TMPDIR -> rc 2 with `recheck-cwd: TMPDIR`; named-kill set 7 of 8 (K-X2 survives) | `.ufo/waves/round-78/w1/successor/` (candidate + mutant receipts); `.ufo/waves/round-78/w1/ScribeLesson-evidence-r78.txt` §4; `controls/c1-base-missing-tmpdir-r78.txt` |
| 78 | coverage | registry 112 with S112 `queued`; knowledge 91; frontier 53 | registry 112 with S112 `mined`; knowledge 92; frontier 54 | `corpus/SOURCES.md:124`; `corpus/source-snapshots/round-78/`; `controls/c2-prerecheck-r78.txt` |
| 78 | calibration | round-77 M77-5 (distinctness sweep not run before freeze) and M77-3 (TMPDIR fragility) open | M77-3 carried as this round's mined mistake and closed by the C1 successor refusal; the r78 manifest drops the six F51-restating clauses, so M77-5's class does not recur | `corpus/lessons/round-78.md` § Mistakes (draft: `.ufo/waves/round-78/w1/lesson-round-78.md`) |

**Planned after round 78 (not frozen):** (1) depth:verifiability — a successor in which the `gate-consume`
check body is asserted by a second, independent check, so that neutering `gate-consume` still fails on the
case-6 RESULT limb; the round-78 K-X2 survivor is the red-before for that claim, and the frozen mutant
table's K-X2 anchor must be re-pinned to the landing bytes; (2) coverage — one of the three remaining live
OSV.dev endpoint pages (R-77-F), each with its own capture, its own located quotes and its own distinctness
sweep; (3) calibration — the L0 rulings on R-77-D (the anchor-window semantics) and R-77-E (the staged
`S112`/`TC260` id collision) remain the precondition for any assimilation append.
