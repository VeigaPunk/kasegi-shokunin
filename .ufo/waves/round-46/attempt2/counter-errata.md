# Round 46 (attempt 2) — counter errata

Frozen at `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` (`.ufo/waves/round-46/attempt2/freeze.txt`):
`claims.json` sha256 `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0`,
`r46-mutbat.py` v1 sha256 `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`,
`r46-f29-gate.py` v1 sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`.
`claims.json` is byte-identical at the tip: `diff <(git show fe0f56b7:.ufo/waves/round-46/attempt2/claims.json) .ufo/waves/round-46/attempt2/claims.json` prints nothing. No claim sentence, before-value, after-value, target or kill rule was edited.

## Classification

Erratum, not a changed rule: the C1 predicate sentence ("caught + equivalent == mutants, uncaught == 0,
baseline failures=0") and the C2 target (29 admitted rows, 66 entries, S074 mined) are unchanged; the
changed instruments are ADDITIONS or coverage extensions that keep every v1 reading reproducible:

- the battery's before-value receipt (`controls/mutbat-before.txt`) remains reproducible at the base
  export with the v1 table semantics (`--counter c1` / `--counter c2` on unextended selftests);
- the attempt-1 counters `r46-c1-gate.py` / `r46-c2-gate.py` are not edited by this round at all
  (verify: `git diff fe0f56b7..HEAD -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py`
  must be empty at landing, except the separately-logged v1.3 ledger-exemption amendment if the wave
  verifies it — that amendment keeps G6's limb sentence and its recorded readings reproducible, see §E3).

## Changes

### E1 — r46-mutbat.py v1 -> v1.1 (landed at integration; draft by ExecMutbatF29, amended by the L1)

| id | v1 | v1.1 | reason |
|---|---|---|---|
| E1-a | counters c1/c2 only | `F29_MUTANTS` table (the same 21 mutants as controls/f29-r50-receipt.txt) + `--counter f29` (grader: the committed r46-selftest-f29.py, fixture fallback) and `--counter all` | the claims' C1 after-state extends the caught-or-equivalent predicate to the f29 gate; the f29 mutants were already defined pre-freeze (R50 receipt), so no predicate text changes |
| E1-b | — | `--counter both` keeps its exact v1 semantics (c1+c2 only; `all` adds f29) | the frozen C1 `counter_cmd` and the before-value replay stay byte-stable |
| E1-c | `--equivalent` default None | defaults to the committed map `corpus/instruments/r46-mutant-equivalents.json` (beside the tool) | the frozen `counter_cmd` passes no `--equivalent`; the after-state requires every equivalent verdict to name a committed proof, so the default must be the committed map (M14 for c1; G6b/G7a/G7c for c2 — proofs in `corpus/instruments/r46-mutant-equivalents/`) |

Plain re-derivation not using v1.1: the c1/c2 before-value lines of `controls/mutbat-before.txt`
reproduce under v1 bytes (`git show fe0f56b7:corpus/instruments/r46-mutbat.py`).

### E2 — selftest extensions (landed at integration; drafts by ExecSelftestC1 and ExecSelftestC2, the latter merged with ExecGatePinAmend's v1.3 mirror)

`r46-counters-selftest-c1.py` 76 -> 83 cases; `r46-counters-selftest-c2.py` 137 -> 147 cases and
mirrors the v1.3 content-exempt set (LEDGER/EXEMPT_ENTRIES). Baselines stay failures=0; the new
cases fail under their targeted battery mutants (ExecSelftestC1 receipts `03-mutant-*.txt`;
ExecSelftestC2 `per-mutant-verification.txt`). Label note (MutSelfC1a finding, accepted): under
M13 the L6-attribution marker text (`unmutated-copy-not-green`) is the very clause the mutant
removes, and under M19 the limb-flip class has no dedicated verdict label — the failures COUNT is
the attribution the battery predicate uses; the selftest's per-case labels for those two read
UNEXPECTED while the catch is real. Both dead `--pure` defaults now point at the committed map
pattern (SentScratch F1 fix: `--pure` required, no dead absolute default).

### E3 — r46-c2-gate.py v1.2 -> v1.3 (landed at integration; draft by ExecGatePinAmend, plus the junk-row conjunct from RevPriorEscapes)

CONTENT_EXEMPT gains `considerthese-proposals-ledger.md` (name pinned, size may grow never shrink
— `EXEMPT_BASE_SIZE[...] = 30696`); `PINS["base-knowledge-content"]` re-derived over the 61
non-exempt files; the c2 selftest mirrors the exemption. ADDITIONALLY (RevPriorEscapes Finding 1):
g2 now requires `junk == 0` — every table-shaped line in the entry must be a header, a separator
or a counted row, so the prior attempt's junk-filler falsifier tree (which v1.1/v1.2 tolerated
while `(counted real rows - 6) > 0`) reads red. The prior receipts stay reproducible: the v1.3
bytes at the era export `eb874bc` read `c2-gate fixed=7/7 exit=0` (receipt in final-measure), and
the v1.2 bytes at `eb874bc` are untouched history. At THIS round's tip the v1.3 counter reads
5/7 (G1 28->29, G6 65->66) — moved BY this round's C2 landing; the new after-state is graded by
`r46-f29-gate.py`, not by the attempt-1 instrument.

### E4 — r46-f29-gate.py v1 -> v1.1 (landed at integration; the wave-1 reviewer findings)

The wave-1 attackers found tree-level false-greens the R50 counter-mutant pass could not see
(M46-5): H1 F1 (indented duplicate frontier rows invisible to the strict parse), H1 F3 (entry-cell
substring aliasing), H2 F1 (recheck trailing comment carrying shell text), H3 F3 (redirector-wrapped
URL), H3 F5 (line locator bound to the wrong file), H5 F2 (frozen core inside a mid-line HTML
comment counted as live text), H6H7 F5/F6 (a duplicated `## Registry` section — empty or with
fabricated rows — invisible to the fleet census and relayed green by H7). Fixes: H1 parses rows
loose-indent and requires `frontier_anywhere(root) == len(rows)` (fence-stripped, zero-width-
normalized lines matching `\| *F\d+ *\|` anywhere) and the entry cell must name exactly ENTRY
(backtick decoration stripped); H2's comment tail admits only `[ 0-9A-Za-z./_-]+` (no shell
metacharacters); H3 requires every URL in the source cell to equal the canonical URL and the line
locator to be bound to this capture's path (`lines? N-M of <path>`); `live_lines` strips mid-line
HTML comments; H7 requires exactly one `## Registry` heading. H5 F1/F3 (paragraph-boundary
stitches; loose citation ranges) are disclosed mechanical limits — the located text is still
verbatim capture text and the <= 25-word / <= 12-line / in-body bounds hold; the closure's
re-open is the semantic check. R50 disclosures (a),(b),(d),(e) are graded by the committed
`r46-selftest-f29.py` with rebuilt PINS.

## Plain re-derivations (no changed instrument needed)

- C1 before: `controls/mutbat-before.txt` lines (c1 uncaught=7, c2 uncaught=13) reproduce from the
  base export with the frozen v1 battery.
- C2 before: `controls/f29-gate-at-base.txt` (`fixed=1/7` at the base export) and the live-lane
  reading `fixed=2/7` reproduce from the committed v1 gate.
- Both after-states carry plain second measures in `claims.json` `plain` (grep/wc lines, selftest
  tallies, absence sweep) that no battery or gate change touches.
