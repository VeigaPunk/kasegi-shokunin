# Round 75 — lesson (kasegi, attempt 2)

Round: kasegi r75, attempt 2 (attempt 1 ended without a landed report at 06:53 -03, watchdog `lane-dead-no-report kasegi round=75`). Frozen claims `.ufo/waves/round-75/claims.json` (freeze commit `748dfb6`; base `f9cc05b5`; controls commit `c880047`). Wave `w1` (12 seats) was dispatched by attempt 1 under l1 `KasegiR75` and settled under this attempt; its receipts are in `.ufo/waves/round-75/w1/`.

Claims: C1 (`depth:verifiability`, counter amendment of `corpus/instruments/recheck-cwd-census.py`: a `restoration_only` bucket for files whose only recheck-ish header is `restoration-recheck:`, a RESULT gate that requires it zero, and selftest case 6; nominal score 4, per QUALITY R58) and C2 (`coverage`, frontier F53 on S110, the NDSS Symposium 2023 paper on Fuzzilli; score held at 8, denominator operator-owned).

## Gate

Candidates considered this round:

- **S110 — the NDSS Symposium 2023 paper "FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities", `https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf` — ADMITTED as F53** (one knowledge entry, `corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md`). Access date 2026-11-05 (capture `fetched_utc` 2026-11-05T09:51:07Z, HTTP 200, 918189 raw PDF bytes; capture `corpus/source-snapshots/round-75/S110.txt`, sha256 `0780beae…51ef`, 1869 lines). Located quote (≤25 words, 12 words, capture line 33): "In this paper, we close this gap and present the first fuzzer". The entry records this as the paper's own priority claim and does not verify it. The 24 manifest quotes are byte-exact at their anchors (`source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110` exit 0 from a foreign cwd). The landing-page href the Fuzzilli README uses (`ndss-paper/fuzzilli-…/`) is provenance of identity only; the PDF URL is the S110 source cell (ScoutSurface headline; both URLs resolve to the same 918189-byte file).
- **OSV.dev overview page `https://google.github.io/osv.dev/api/` — REJECTED as a row again this round.** Reason: CORPUS rule 1 — a row needs a capture in the round that writes it; the page stays a lead with its flip condition unchanged. Not opened this round.
- **Revenger's NDSS rows S114, S341, S363 — REJECTED as duplicates of S110.** Reason: other papers with a different DOI (`10.14722/ndss.2025.230669`); `ReviewC2` T2. `grep -ril fuzzilli ../revenger-shokunin/corpus` = 0 files (exit 0 path, count 0).
- **Project Zero comparison post S093 and the Fuzzilli README S109 — held, not candidates.** Distinct documents; the NDSS paper's content is not S093's content and not S109's content (ExecC2Capture distinctness, ConnectorSweep §1).
- **Assimilation of `merge/kasegi/` — REJECTED for this round (adopt nothing).** Reason: the id-collision guard finds 79 collisions between the staged `SOURCES.append.md` ids (S031–S109, 94 ids) and the lane registry (`.ufo/waves/round-75/assimilation/collisions`; reg-ids 109, staged-ids 94, collisions 79). That is mass id drift that a read-only check cannot fix; the round-prompt §6 item 10 rule ("drift a read-only check cannot fix → append an L0 question and adopt nothing this round") applies: an L0 question is filed and nothing is appended. Quarantine slice not drafted for the same reason.
- **considerthese — no still-unimplemented proposal mined this round.** ConnectorSweep §2 dispositions for `considerthese/2026-10-26.md`: P1 mined r39, P2 completed r74, P3 mined r36, P4 cap half mined r28 with the externalise plank operator-owned, P5 landed r36, P6 mined r34, P7 mined r30; the earlier files are mined.

Admitted: S110 / F53. Rejected or held: the OSV overview page (lead), revenger's S114/S341/S363 (different papers), S093 and S109 (distinct), the merge package (79 collisions), considerthese (nothing unimplemented).

### Gate correction for round 74 (appended)

Round 74's Gate (`corpus/lessons/round-74.md` § Gate) records its rejects. This round adds none to that record.

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M75-1 | attack seat read a producer artifact before it existed: `SentinelCounter` ran before the executor's `ExecC1Amend.patch` was written, derived its own amendment from the claim text in scratch, and reported the exec-surface verdict on that derivation | `.ufo/waves/round-75/w1/SentinelCounter.md` §Inputs (the patch "has NOT appeared"); `.ufo/waves/round-75/w1/ExecC1Amend.patch` written 06:53, sentinel report 06:52 | none | the landed patch is re-measured by the L1: exec count `grep -c 'bash", "-c'` on the landed file = 1 (base 1), `subprocess.run(` count 1 and the A4 parity delta (below). Wave-spec rule (attack seats start after their producer's output path exists) is routed, not shown able to fail | not shown: the routed spec rule has no counter yet |
| M75-2 | a frozen upper bound enforced only by a lower-bound command: C2 clause B5 says every quote is "≤25 words" but the named command, `source-recheck.py`, enforces `MIN_QUOTE_CHARS = 12` (line 33) only | `corpus/instruments/source-recheck.py:33`; `grep -ciE 'words\|max_words\|MAX_QUOTE' corpus/instruments/source-recheck.py` = 0; `.ufo/waves/round-75/w1/CriticClaims.md` F7 | none (R123 is the criterion adopted this round) | QUALITY R123 adopted; the 25-word cap is measured separately (`max 12 words, 0 over 25` over the 24 manifest quotes); a counter that enforces the cap is routed to round 76 with its own freeze | yes, on this tree: R123 flags B5 as written, because the named command has no word cap (grep count 0) |
| M75-3 | a frozen C1 predicate that a forged implementation passes: relabelling the base `norecheck` bucket as `restoration_only` passes the frozen case-6 expectations and A2/A4 on the real tree; clause (ii)'s `norecheck` half is unbound | `.ufo/waves/round-75/w1/CriticClaims.md` F1 and `CriticClaims-attack-rename.py` (F2-case6: `norecheck=0 restoration_only=1 nonconformant exit 1`; F1-neither: same) | none | recorded as a letter gap of the frozen predicate; not reworded after scoring (kill rule); routed to round 76 as a counter amendment with its own do-nothing control and freeze | yes: the forged implementation is shown to fail the (ii) reading on the neither-header fixture |
| M75-4 | an L1 ended without a landed report four minutes after its wave was dispatched, and the wave's WAVE-DONE was addressed to the dead id | `.ufo/watchdog.log` 06:53:21 `lane-dead-no-report kasegi round=75`; `.ufo/waves/round-75/w1.ready` l1 `KasegiR75`; Main reroute to `KasegiR75a2` | none | attempt 2 integrated `w1`; the routing gap is named in `.ufo/l0-questions.md` for the operator | no |
| M75-5 | a seat wrote a lane file at the fleet root (relative path): `cited-lines.txt`, the NDSS paper's first lines, untracked at `/home/vgpnk/Projects/shokunin/` (misroot sweep, `git -C /home/vgpnk/Projects/shokunin status --porcelain`) | fleet-root file `cited-lines.txt` (7022 bytes); its content names this round's paper (S110 capture lines 1–39) | none | copied byte-exact to `cited-lines.txt` in the lane root (`cmp` exit 0), fleet copy deleted (the one fleet-root deletion this L1 made); the lane copy is committed as a round-75 scratch excerpt. Two other untracked fleet files (`run_check_probe.py`, `run_check_probe2.py`) name another lane's round (kengaku r90) and are not touched | no: the sweep ran once, after the landing commit |

## Routed defects (not closed by round 75)

- **R75-1 (C1 predicate, M75-3):** a counter amendment that binds clause (ii) at file level (`norecheck` = neither header) and a case that puts a restoration-only file next to a neither-header file. Needs its own freeze and do-nothing control (round 76).
- **R75-2 (C1 predicate, critic F2 and mutation M-P4):** case 6's RESULT limb can be removed without a failing selftest (`MutAuditC1` M-P4 survived: `cases=6 failures=0`). The marker-absent conjunct is the only detector for that class in the frozen fixture set; the frozen A3 lists three classes, of which M-A, M-B and M-C are killed.
- **R75-3 (C1 residual, ReviewC1 T6):** no fixture carries both `recheck:` and `restoration-recheck:`; the real tree has two such files (`claim-gates.md`, `claim-package-contract.md`). Routed with R75-1.
- **R75-4 (C2 coverage, critic F6):** an abstract-only entry would pass B1–B8 as written; the comparison ground (Superion, the introduction's wording) is not required to be quoted from the body. Routed as a frozen-clause amendment for the next admission.
- **R75-5 (C2, critic F11, B8):** the sibling sweep (`grep -ril fuzzilli revenger/corpus`) returns empty and cannot discriminate. Verdict-only; routed.
- **R75-6 (census drift expectation, V74-1 follow-up):** the census line `entries=…` must be read at its own revision (R121). This round's receipts carry their revision (base `f9cc05b5` = 90 entries; C1-only = 90; landed = 91 entries, `exit0_foreign` 68 → 69).
- **R75-7 (wave ordering, M75-1):** see the table above.
- **R75-8 (considerthese P4, operator-owned):** the externalise plank of 2026-10-26 P4 is an operator decision, not this lane's to implement.

## Erratum (V74-1, appended; the round-74 report is fleet-root and not edited by this lane)

The round-74 spot-check (`corpus/lessons/round-74-verifier-spotcheck.md` §5, V74-1) found that round 74's landed-state census value (`entries=89`) was printed at a mid-round tree. The value is superseded: at the round-74 tip the census prints `entries=90`, and round 75's measurements are `entries=90` at base `f9cc05b5`, `entries=90` at the C1-only tree and `entries=91` at the landed tree (`exit0_foreign` 68 → 69). The fleet-root report `.ufo/reports/round-74/kasegi.md` lines 20, 46 and 85 carry `entries=89` and are superseded by this erratum; `corpus/lessons/round-74.md` line 69 is superseded likewise. The lines are not edited.

## Registry changes (old -> new)

- `corpus/SOURCES.md`: registry 109 → 110 (`S110`, paper, tier A, mined, opened 2026-11-05, recheck 90d, used-by `corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md`). No pre-existing cell changed (`git diff f9cc05b5 -- corpus/SOURCES.md` removed lines = 0). The NDSS lead bullet at base line 175 is kept byte-identical at tip line 176 (sha256 `124b3a00…adb5a1`, measured) and is retired as opened in the round-75 note bullet.
- `corpus/instruments/knowledge-expected.txt`: 90 → 91 expected rows (`fuzzilli-ndss2023-jit-fuzzing-paper.md` at line 40).
- `corpus/README.md`: `## Round-75 admission` block with the F53 row (R6 end-append). `PROVINCE.md`: r75 Frontier amendment line (end-append).
- `corpus/QUALITY.md`: R121, R122 (from the scribe's drafts, verified against the R120 supersession) and R123 (this round, § Mistakes M75-2). R33 is still held twice (lines 292 and 550; not repaired).
- `SKILL.md`: gates registry row for `recheck-cwd-census.py` (the gate had no row at base). `corpus/instruments/README.md`: one table row for the counter.

## Counters (before → after)

| counter | before (base `f9cc05b5`, controls `c880047`) | after (landed tree) | command |
|---|---|---|---|
| recheck-cwd census selftest | `selftest cases=5 failures=0` | `selftest cases=6 failures=0`, exit 0 | `TMPDIR=<scratch> python3 corpus/instruments/recheck-cwd-census.py --selftest` |
| census on the real tree | `RECHECK-CWD entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0`, conformant | `… restoration_only=0`, conformant; after C2, `entries=91 … exit0_foreign=69 … restoration_only=0`, conformant, exit 0 | `python3 corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` from `/tmp` |
| registry rows | 109 | 110 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` |
| knowledge entries | 90 | 91 | `ls corpus/knowledge/*.md \| wc -l` |
| frontier admitted | 52 (F01–F52) | 53 (F01–F53) | `python3 corpus/instruments/frontier-recheck-count.py` → `FRONTIER-PASS F53 ids=S110`, `entries=56 pass=56 exit=0` |
| capture binding | `records=88 bound=88 unbound=0` | `records=89 bound=89 unbound=0`, exit 0 | `python3 corpus/instruments/capture-binding-check.py` |

## Sourced claim

C2 rests on S110, opened this round (fetched 2026-11-05T09:51:07Z). The entry cites the source in its header (`source: S110`) and its Verification block; the registry row and the knowledge entry are the same claim.

## Non-claim work

- ExecReplay re-derived 20 committed values from base (`freeze_ancestry`, C1 selftest, C1 lane census, C1 case-6 fixture, C2 frontier, capture, counts): all AGREE, 0 DISAGREE (`.ufo/waves/round-75/w1/ExecReplay-agree.txt`). It is evidence of the base receipts, not of the landed bytes; the landed-tree measurements above are the integrator's.
- ScribeEntry's entry draft was re-checked by the integrator: the entry carries 25 double-quoted strings of at least 12 characters, all located in the S110 capture or the S109 capture, 24 of them pinned in the round-75 manifest (the 25th is S109's Q16 pinned in the round-74 manifest). The reviewer's count of 83 came from a scratch manifest and is not a count of the landed entry.

## Seats (wave w1, 12 seats; roles executor×3, scout×1, scribe×2, connector×1, reviewer×2, critic×1, mutation-tester×1, sentinel×1; attack share 5/12)

Dead seats: 0. Results: `.ufo/waves/round-75/w1-results.json`. Reports: `.ufo/waves/round-75/w1/*.md`. Scratch dirs removed by each seat (per the seat reports).

## Verdicts (C1, C2)

- **C1 — VERIFIED on its frozen predicate.** A1 `cases=6 failures=0` exit 0; A2 `entries=90 … restoration_only=0` conformant exit 0; A3 the three named mutant classes (M-A, M-B, M-C; `MutAuditC1` M-P1, M-P2, M-P5) each exit 1 and the unamended counter survives (`cases=5 failures=0`); A4 every stable field equal to the base (`diff` of the two stdouts: the only delta is the inserted `restoration_only=0`). Predicate defects are routed (M75-3, R75-1 to R75-3), not rewritten. Score: nominal 4 → 4, per R58.
- **C2 — VERIFIED on its frozen B1–B8.** B1 110 (base 109); B2 0 removed lines; B3 knowledge 91, expected 91 rows, `LC_ALL=C sort -c` exit 0, set-equal to the directory; B4 `records=89 bound=89 unbound=0` exit 0; B5 source-recheck exit 0 from a foreign cwd, max 12 words over 24 quotes (the cap is measured here, not enforced by the named command: M75-2); B6 `FRONTIER-PASS F53 ids=S110`, `entries=56 pass=56 exit=0`; B7 `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 (six inherited W04 warnings unchanged); B8 sibling grep = 0 revenger files; the S093/S109 rows are distinct. Score: nominal 8 → 8 (denominator operator-owned).

## Counting commands (for the closure verifier)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=/fast/scratch/hyaku/kasegi-r75/L1/tmp python3 corpus/instruments/recheck-cwd-census.py --selftest
cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-cwd-census.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-75/manifest.json --source S110
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py && python3 corpus/instruments/frontier-recheck-count.py
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```
