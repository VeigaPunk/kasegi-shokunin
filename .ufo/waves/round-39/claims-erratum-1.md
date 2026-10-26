# Round 39 — claims erratum 1 (append-only; freeze text stands as written)

Author: L1 KasegiR39. Date: 2026-10-26. Supersedes the corresponding numbers in
`.ufo/waves/round-39/claims.json` (commit `dcd31701`) for measurement and closure
purposes; the frozen predicate sentences otherwise stand unchanged.

## E1 — registry after-count is 59, not 58 (C2)

`claims.json` C2 counts `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58`
reflected an arithmetic slip in the L1's freeze draft: the round appends FOUR rows —
S057 (mined) plus S056/S058/S059 (rejected) — so 55 → **59**. The kill-rule row
`registry != 58` reads as `registry != 59`. Every instrument that reads the registry
(census, audit, harness) counts the four rows; the spot-check list labels the
measured 59 versus the as-frozen 58 and cites this erratum.

## E2 — r38 judged-head hash corrected to the full 40-char form (C1)

The freeze text and the wave-1 prompts truncated the r38 judged head to
`66703aca50529a35be49aa8759d04140720ad` (37 chars, invalid object name). The real
r38 judged head J is `66703acaaff50529a35be49aa8759d04140720ad` (40 chars) per
`.ufo/waves/round-38/final-gates/all-gates.txt` `export-ref=` and the round-38
verifier spot-check. All `--export-ref 66703aca…` control runs (base-red proof for
C1, CritBaseControl do-nothing control) MUST use the 40-char hash; the suite's own
kill rule is unchanged (r38 judged-head export red).

## E3 — measured values recorded at erratum time

- Registry rows at base: 55 (S001–S055, unique).
- Intended after-state: 59 rows (S056–S059 added), frontier 22, knowledge 51.
- r38 judged head: `66703acaaff50529a35be49aa8759d04140720ad`.

## E4 — verification ref for the C1 counting command (R1 class, resolved)

The freeze C1 counting command `bash corpus/instruments/r39-closure.sh --export-ref <J> -> closed=8/8` is
unsatisfiable at J as written: G2 requires the receipt to be inside the export, and the judged-head
rule defines J as the commit that carries every round-39 change EXCEPT the receipt (so at J the G2
receipt limb is 0 and the run prints closed=7/8 exit=1 by construction — the round-38 verifier R1
class). Resolution, matching G2 as written and the round-38 precedent:
- The verification ref is **Y** = J + the receipt only (`git diff --name-only J Y` = the receipt).
- `--export-ref Y` prints `closed=8/8 exit=0` and `--selftest --export-ref Y` prints
  `selftest cases=8 failures=0` with eight graded case lines.
- A run at J prints `closed=7/8 exit=1` with the G2 payload `receipt=0`; this is expected and
  documented in the receipt, not a kill.
- The kill rule's reds stand unchanged: base 480b1a505a2dfc14a4f718d16d63808247214d0a and r38
  judged head 66703acaaff50529a35be49aa8759d04140720ad exports print closed<8/8 exit=1.
- Wave-2 suite-run items use `<Y>` as the verification ref; RevC1Receipt checks both the J-run
  (7/8, receipt=0) and the Y-run (8/8).

## E5 — non-vacuous measurement semantics (from CritFreezeAudit, pre-implementation)

Adopted from the independent freeze audit `wave1/CritFreezeAudit.md` (spec-level, before any seat scored), to
keep the frozen counters discriminating. Counting commands and kill rules read with these semantics:

1. Graded case lines: every `selftest case=G<n>` line carries `mutants=n/n` with n >= 1 (no `mutants=0/0`) and
   non-empty `payload=` fields; the kill rule counts `mutants=0/0` as a failure.
2. G1: `declared-blocks.txt` must declare BOTH front doors (PROVINCE.md, corpus/README.md) and every added tail
   (if a file gained lines since base, its declaration must be present and exact); empty declarations with
   additions are RED.
3. G4: at least one tracked `.ufo/waves/round-39/*-dispatch.json` must exist (a round with zero commits dispatch
   files is RED).
4. G5: the SCORECARD.md `## Round 39` section must exist, and SHONEN.md must carry round-39 lines; both with
   zero `Final lane commit:` lines and the judged head named by reference only.
5. G7: anchor after the existing `## Round-37 dispositions — filled (round 38)` heading in
   `corpus/knowledge/considerthese-proposals-ledger.md`; the `## Round-39 dispositions` section carries >= 1
   proposal row (this round mines proposal 1 and carries proposal 3, so >= 2) and one `Correction (round 39)` line.
6. G3 scope: only lines ADDED since base (`git diff <base> REF` over SCORECARD.md, SHONEN.md, LOG.md,
   corpus/lessons/round-38.md) are scanned for quoted `--export-ref <hash> -> closed=K/K` runs; every such quote
   needs a committed transcript under `.ufo/waves/round-39/final-gates/` or an explicit `report-only` label. The
   round report is bound by the same rule (the L1 files it with committed transcripts or report-only labels).
7. R2 correction counting command: `grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md
   SCORECARD.md SHONEN.md` — at least 1 per file at the judged head.
8. R4 counting command: `grep -cE 'M38-5|M38-7' corpus/QUALITY.md` — at least 1 at the judged head (R36 row).
9. C2 content binding: the F22 frontier row names entry `knowledge/cisa-when-to-issue-vex.md` and sources
   `S057`; the S057 row is NF=13 with `status mined` and its source cell carries exactly
   `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`; the S056/S058/S059 rows are
   `status rejected` with a `flip:` token in `teaches`; the S057-citing entry has a substantive body (>= 10
   lines) beyond the provenance trio.
