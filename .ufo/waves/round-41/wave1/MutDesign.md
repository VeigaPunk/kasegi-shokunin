# MutDesign — round-41 wave-1 receipt: CLAIM-to-CHECK mapping mutation test

Seat: `MutDesign` (mutation tester, leaf — no subagents dispatched). Lane: kasegi-shokunin
round 41, run-10 fresh-start. Item: mutation-test the C1 CLAIM-to-CHECK mapping — take
claims.json's I1-I12 list plus the routed-defect lists (r40 verifier spotcheck §5 D1-D6;
r40 wave-2 attack findings) and try to DROP or WEAKEN each mapping. For each I-check:
construct the defect state that exists if the check were a no-op, and verify whether a
DIFFERENT check would catch it. Score: every routed defect has exactly one owning check
(no orphan defects, no orphan checks). Receipt = the mapping matrix + orphan verdicts.

**Verdict up front: the mapping is 1:1 for 11 of the 14 routed units. Three routed
defects are ORPHANS (no owning check among I1-I12): D4, D5, D6. One check is an ORPHAN
CHECK (owns no routed defect): I12. One overlap (dual ownership) exists: I6∩I11 on the
scratch-scan classes T14/F1/F3/F4/F6. Details, drop-tests, and evidence below.**

Writes: this receipt only. No lane/fleet/source-tree bytes touched; no installs; no
network; no mutating git anywhere (read-only git only).

## 1. Authoritative inputs (and the two L1 freeze corrections applied)

1. `.ufo/waves/round-41/claims.json` (frozen, read-only) — C1 predicate names I1-I12 and
   their limbs; C1 kill_rule names the routed fixture set.
2. `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` (L1, mid-wave-1, AUTHORITATIVE) — two
   freeze corrections, both applied in this matrix:
   - **BASE HASH**: real base = 40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab`
     (prefix 5b29ea14). The 38-char literal `5b29ea1439450b712581edf5f0bf98dfb262ab`
     written in the freeze files resolves to NO git object. Verified:
     `git rev-parse --verify 5b29ea1439450b712581edf5f0f0bf98dfb262ab^{commit}` → resolves;
     the 38-char form → `fatal: Needed a single revision` (exit 128). Suites must report
     an unresolvable `--export-ref` as a distinct red (`ref-not-found`), never a vacuous
     `closed<12/12 exit=1`.
   - **I11 ESCAPE COUNT**: the committed `.ufo/waves/round-40/wave2/CritKillRule.md`
     carries EIGHT `### F` headings (F1-F8), not seven. Verified:
     `grep -c '^### F' …/CritKillRule.md` → `8`. I11's target = all eight committed
     states; the I11 payload must read `escapes=8` / `red=8` naming F1-F8. This matrix
     uses all eight.
3. `corpus/lessons/round-40-verifier-spotcheck.md` §5 — the routed list D1-D6 (+D7,
   protocol-lane, status-neutral — excluded).
4. r40 wave-2 receipts: `RevC1Counters.defeats.txt` (T1-T14 defeat transcripts),
   `MutH1H5.md`, `MutH6H10.md` (F1, D1, D2), `CritKillRule.md` (F1-F8).

## 2. Routed-defect universe (grounded in the committed bytes)

From spotcheck §5: D1, D2, D3 (nine sub-items), D4, D5, D6. From the wave-2 receipts:
T2, T3, T4, T7, T13, T14, MutH1H5 (count-relative forgery; payload-value sharing),
MutH6H10 D1 + D2, CritKillRule F1-F8. Byte-locations grounding D4-D6 (used in §5):

- D4: `grep -n '^## Gate' corpus/lessons/round-40.md` → `29:## Gate` and `31:## Gate`
  (duplicated heading); L27 reads "…Registry 59 → 62 rows; tier A +3?mined S016/…" (garbled).
- D5: lesson L9 reads "…wave 2 33/35 = 94%; round total 50/89" — dispatch JSON says
  reviewer 12 + critic 7 + mutation-tester 6 = 25/35, overall 42/89.
- D6: SKILL.md L1120 table separator, L1121 BLANK, L1122 the `r40-closure.sh` row — the
  blank line ends the Markdown table, so the row renders outside its header.

## 3. Method (the mutation probes)

Per I-check, two probes:
- **DROP**: revert the check to a no-op. Construct the exact defect state that re-opens
  (named from the r40 committed transcripts — e.g. I3 dropped ⇒ T2's `closed=7/80` /
  `failures=10` fixtures green again, the r40 observed `rc=0 payload=corrections=4,named=4`).
- **CROSS**: ask whether any OTHER I1-I12 limb would red that state. A cross-catch means
  dual ownership (flagged); no cross-catch confirms sole ownership.
- **WEAKEN** (secondary): per-limb probes where the claims text leaves an ambiguity
  (e.g. does I1's limb exclude fenced corrections? — the claims text gives I1 no fence
  clause, so fence exclusion is I4's alone).

This is a design-level probe of the mapping as frozen; the suite bytes
(`corpus/instruments/r41-closure.sh`) are a wave-1 deliverable being built concurrently
and are not yet in the lane (verified: `ls corpus/instruments/` shows r40-closure.sh,
no r41-closure.sh).

## 4. THE MAPPING MATRIX

Notation: DROP = no-op state. CROSS = would another I-check red it? Owner basis = the
I-limb text in claims.json predicate (line "The twelve checks close…") + CORRECTIONS-L1.

| # | Routed unit (evidence) | Owning check | DROP state (defect re-opened) | CROSS | Verdict |
|---|---|---|---|---|---|
| 1 | D1 — r40 C1 graded "verified" while its kill rule fires (spotcheck §2/§5; SCORECARD/LOG/SHONEN/report) | **I1** | Correction (round 41) lines absent from SCORECARD/LOG/SHONEN, or grade r40 C1 verified, or fail to name the firing evidence (RevC1Counters.defeats.txt, CritKillRule.md, MutH6H10.md) | No limb of I2-I12 reads grading records; I12 is shape-only | SOLE |
| 2 | D2 — Y-level selftest tally quoted with no transcript (violates lane R37) | **I2** | Receipt at Y is not the teed transcript of BOTH the suite run and the graded selftest; run-utc ≠ ref committer instant; time-basis ≠ ref-commit | I9 grades the selftest but never binds the receipt's selftest section to a real run; I8 flags forgery variants, not teeing | SOLE |
| 3 | D3-a / T2 — H2 substring values: `closed=7/80`, `failures=10` accepted (RevC1Counters.defeats.txt T2, `rc=0`) | **I3** | Value limb reverts to substring matching; the committed T2 fixtures green | I9's selftest material is receipt payloads, not correction values; I12 tail-equality is content-based | SOLE |
| 4 | D3-b / T3+T4 — H3 fenced pseudo-row passes (`rc=0`); H2 fence tracking must generalize; EOF fence must be CLOSED | **I4** | Fenced correction/criterion lines satisfy line-anchored limbs; fence-open at EOF unnoticed | I1's stated limb carries NO fence clause (checked: claims predicate text); I7 checks table structure, not fences | SOLE |
| 5 | D3-c / T7 — H9 declaration symlinked outside the export passes (`valid=1` with bytes outside the export) | **I5** | Declared-block paths not readlink-canonicalized; out-of-export declaration greens | I12's whole-tail equality compares diff content, not canonical paths | SOLE |
| 6 | D3-d / T14 — H6 case/separator escape: `Kasegi-R40-stray`, `kasegi_r40-stray` green (`strays=0`) | **I6** + **I11** (F4) | Scan reverts to case-sensitive, separator-blind | YES — I11's committed F4 fixture (case/Unicode-separator variants) flips green ⇒ I11 fails ⇒ suite reds | DUAL |
| 7 | D3-e / F1 — nested leftover invisible (top-level-only scan) | **I6** + **I11** | Scan non-recursive | YES — I11's F1 fixture flips green ⇒ I11 fails | DUAL |
| 8 | D3-e / F2 — container geometry: work inside container hides every nested leftover | **I11** only | (n/a — I6's stated limbs do not name container geometry) | — | SOLE (I11) |
| 9 | D3-e / F3 — dotfile scratch dir escapes | **I6** + **I11** | Scan dot-exclusive | YES — I11's F3 fixture flips green ⇒ I11 fails | DUAL |
| 10 | D3-e / F4 — case / Unicode-separator name variants escape | **I6** + **I11** (same class as row 6) | Scan case/byte-literal | YES — I11's F4 fixture | DUAL |
| 11 | D3-e / F5 — ancestor-prefix tolerance without a clean chain | **I11** only | (I6's stated limbs do not name the tolerance chain) | — | SOLE (I11) |
| 12 | D3-e / F6 — nonexistent `--scratch-root` silently disables the scan (fail-open) | **I6** + **I11** | Scan fails open on a bad root | YES — I11's F6 fixture flips green ⇒ I11 fails | DUAL |
| 13 | D3-e / F7 — pending marker respelled (`〈pending`, `<pending`, case variants) dodges the literal grep | **I11** only | (no other I-check names the pending-marker clause) | — | SOLE (I11) |
| 14 | D3-e / F8 — git-status blindness: skip-worktree/assume-unchanged/ignored edits report "clean" | **I11** only (per CORRECTIONS-L1, I11 = F1-F8) | Working-tree-clean clause stays blind | — | SOLE (I11) |
| 15 | D3-f / T13 — H1 mention-only SKILL.md row passes (`registry=1` from a non-registry row) | **I7** | Mention-only row satisfies the registry limb; malformed row accepted | No other I-check reads the registry row's well-formedness | SOLE |
| 16 | D3-g — H5 forgery detection count-relative: `forged=rejected` only when `payload_matches(forged) < control` (MutH1H5 obs-1) | **I8** | Per-variant flags collapse to a count comparison; a variant is accepted when another payload is already mismatched | I9 isolates selftest payload values per case — different material; I2 is tee byte-identity | SOLE |
| 17 | D3-h — H7 payload-value comparison not isolated: reorder-receipt accepted once `cmp` removed; shared `payload_matches` degrades to presence-counting (MutH6H10 D1; MutH1H5 obs-2) | **I9** | Graded selftest does not isolate the value comparison per case; the cmp/value clause is removable without a fixture noticing | I2's byte-identity reds only committed-receipt tamper, not the selftest killability gap | SOLE |
| 18 | D3-i — H8 acceptance predicate unkillable; pristine accepts a leaf-capped green base 7/10 (MutH6H10 D2, M-H8a equivalent mutant) | **I10** | Negative-control acceptance loses its real numeric comparison; the M-H8a-class mutation survives the graded selftest | I12's "negative controls red at base/r40-head" is satisfied by the capped 7/10 print — it does not test the acceptance predicate's killability | SOLE |
| 19 | D4 — lesson hygiene: duplicated `## Gate` (L29/L31) + garbled census line (L27) in corpus/lessons/round-40.md | **NONE** | No I-check limb reads the lesson's headings or census line (I1's named files are SCORECARD/LOG/SHONEN only) | — | **ORPHAN DEFECT** |
| 20 | D5 — attack-tally error: lesson L9 "33/35 = 94%; 50/89" vs dispatch JSON 25/35, 42/89 | **NONE** | No I-check limb verifies the lesson tally | — | **ORPHAN DEFECT** |
| 21 | D6 — SKILL.md registry table broken: blank L1121 splits the r40 row from its header | **NONE** | I7's limb targets the r41 row's well-formedness and mention-only rejection; it does not verify the r40 row. I12 constrains the REPAIR to be append-only but does not verify it | — | **ORPHAN DEFECT** |

Counts: 21 routed units scored. Sole-owned: 16 (rows 1-5, 8, 13-18). Dual-owned: 5
(rows 6, 7, 9, 10, 12 — the T14/F1/F3/F4/F6 scratch-scan classes, I6∩I11). Orphan
defects: 3 (rows 19-21 — D4, D5, D6).

## 5. Orphan verdicts (flagged loudly)

1. **ORPHAN DEFECTS — D4, D5, D6 have no owning check in I1-I12.** The claim text says
   "The twelve checks close the round-40 verifier routed defects D1-D6"; strictly, the
   twelve checks close D1-D3 and the wave-2 findings. D4/D5/D6 are closed only by the
   L1-landed correction/erratum bytes (the milestone's separate "corrections/D4-D6
   repairs" line), verified by no suite limb — their verification is deferred to the
   round-41 closure's re-derivation by plain reads (the same pattern the r40 closure
   used for the r39 R-fixes). This is a real mapping hole in the frozen claim wording,
   not a suite defect. Two clean resolutions: (a) amend the claim wording to "I1-I12
   close D1-D3 and the wave-2 findings; D4-D6 close via the landed corrections", or
   (b) add suite limbs owning the three (lesson-heading census/erratum limb; tally
   limb; r40-row table-repair limb). If neither lands, the round-41 non-author closure
   MUST re-derive D4-D6 fixes from committed bytes explicitly or they are unverified.
2. **ORPHAN CHECK — I12 owns no routed defect.** Its limbs (negative controls red at
   base/r40-head; declared-blocks = whole-tail appends; SKILL/PROVINCE append-only;
   density.py byte-identical; zero deletions; census exit 0) are claim-integrity /
   counting-command properties, not closures of any D1-D6 or wave-2 item. The r40
   wave-2 deletion/append mutants M-H10a/M-H10b were KILLED in round 40, so they were
   never routed. Not harmful — I12 guards the C1/C2 kill-rule filing clauses — but by
   the seat's exactly-one-owner score it is an orphan check. Optional anchor: re-commit
   the M-H10a/M-H10b fixtures as I12 kill fixtures.
3. **DUAL OWNERSHIP — I6∩I11 on T14/F1/F3/F4/F6.** Dropping I6 leaves I11's committed
   escape-state fixtures still reding those classes (they flip green ⇒ I11 fails ⇒ the
   suite reds at Y); dropping I11 leaves I6's standing properties reding F1/F3/F4/F6
   while F2/F5/F7/F8 escape outright. Net: the defect state "suite greens the escape"
   requires dropping BOTH I6 and I11. Implement as one hardened scan (I6's four
   properties) + committed regression fixtures (I11, F1-F8), and record the dual
   ownership as intended defense-in-depth — it does not create orphans.
4. **Kill-rule clauses with no I-check owner (by design, filing-level):** "suite absent
   from the Y export" — covered by the counting command itself (exit 127; demonstrated
   by `c1-controls/do-nothing.txt`); "the lane working tree not clean at filing" —
   closure-level gate; its in-suite escape class F8 is owned by I11 per CORRECTIONS-L1.

## 6. Attack findings correctly NOT routed (excluded from the matrix, with reasons)

- **MutH1H5 H4 survivor** (selftest coverage gap on the located-quote date/quote
  conjuncts): the seat itself ruled it "a selftest-coverage improvement … not a false
  claim"; it appears in no spotcheck §5 D-line. No r41 I-limb corresponds to located
  quotes (I1-I12 are r41-state checks), so there is nothing to map it to. Landed at the
  L1's discretion, outside the mapping.
- **MutH6H10 F1** (selftest counting command not executable at the lane tip): structurally
  fixed in round 41 — the judged-head rule makes Y = J + receipt a real commit, so
  `--export-ref Y` resolves. Adjacent to I2 (which binds the receipt at Y) but not a
  routed defect.
- **D7** (S022/S024 teaches rewrite): explicitly "noted for the protocol lane …
  status-neutral for kasegi". Excluded.

## 7. Freeze-typo note (evidence for the correction this matrix applied)

- `git rev-parse --verify 5b29ea1439450b712581edf5f0f0bf98dfb262ab^{commit}` →
  `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (resolves; len 40).
- `git rev-parse --verify 5b29ea1439450b712581edf5f0bf98dfb262ab^{commit}` →
  `fatal: Needed a single revision` (exit 128; len 38 — the freeze typo).
- r40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd` and claims-freeze
  `fbba3d96cdf8d37c1ea41304a1ba35691329684b` both resolve (len 40 each).
- `grep -c '^### F' .ufo/waves/round-40/wave2/CritKillRule.md` → `8` (headings F1-F8
  listed verbatim in §1.2's source). Any I11 payload reading `escapes=7` would itself
  be a defect — the matrix requires `escapes=8`/`red=8`.

## 8. Evidence log (commands run, actual output)

All reads; lane/fleet/shokuknow untouched; no mutating git/jj; no installs (none
needed — pacman untouched, paused host-wide); no network fetches.

1. `mkdir -p /fast/scratch/hyaku/kasegi-r41/MutDesign` → scratch ready (cwd-bound for
   all work; TMPDIR not needed — no heavy pass).
2. Read `.ufo/waves/round-41/claims.json` (full; C1 predicate + kill_rule read raw —
   I1-I12 limbs and the fixture list captured verbatim).
3. Read `corpus/lessons/round-40-verifier-spotcheck.md` (§5 D1-D7 captured).
4. Read `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` (T1-T14 transcripts).
5. Read `wave2/MutH1H5.md` (4 killed/1 survived; obs-1 count-relative; obs-2 shared
   payload_matches), `wave2/MutH6H10.md` (F1; D1 reorder-receipt; D2 leaf-capped green
   base; M-H8a equivalence), `wave2/CritKillRule.md` (F1-F8, positive controls).
6. L1 IRC directive + `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` — base-hash and
   I11-count corrections applied (ack sent to KasegiR41).
7. Hash verifications and D4/D5/D6 byte grounding as quoted in §1, §2, §7.

## 9. Hygiene

- Writes: this receipt only
  (`.ufo/waves/round-41/wave1/MutDesign.md`). No deliverable file — receipt-only item.
- No lane tracked file, no fleet-root tracked file, no PATH dir, no sibling/source-tree
  write; lane git read-only.
- Scratch `/fast/scratch/hyaku/kasegi-r41/MutDesign` removed before yield (no
  `kasegi-r41*` sibling left by this seat).
- Disk guard: `/fast` 25% used, 611G free — green before and after (no heavy pass run).

## 10. Bottom line for the L1

Land the mapping as 16 sole-owned + 5 dual-owned (I6∩I11, intentional) + 3 orphan
defects (D4/D5/D6 — closed by corrections, verified by closure re-derivation, or add
limbs) + 1 orphan check (I12 — claim-integrity, optionally anchored). Every routed
wave-2 attack finding T2/T3/T4/T7/T13/T14, MutH1H5 count-relative forgery,
MutH6H10 D1/D2, and CritKillRule F1-F8 has at least one owning check; no routed defect
is left unguarded except the three lesson/registry hygiene items the suite does not
claim to read.
