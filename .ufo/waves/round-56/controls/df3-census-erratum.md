# round-56 routed-defect erratum — DF-3 (the "CENSUS-FRESH=ok" prose vs the receipt it cites printing "CENSUS-FRESH=stale [exit=1]"; appended file; no filed byte edited)

Filed by round 56 against base `e166f1bba49446e67de317bff62d3c0b84eb1d7c`, addressing the round-55
non-author closure's routed defect DF-3 (`corpus/lessons/round-55-verifier-spotcheck.md` §3:
"`CENSUS-FRESH=ok` prose contradicted by the receipt it cites (the DF-1 class, recurring in the
round that fixed it)"; status-neutral). R9 form: a numerical/status erratum naming its base and
superseded literals, appended as a NEW file — the corrected records' bytes are never rewritten.

## DF-3 — the gate receipt's freshness status (prose "ok" vs the receipt's printed "stale [exit=1]")

- Filed literals: the round-55 report (`shokunin-clone/shokunin/.ufo/reports/round-55/kasegi.md`,
  Sources & frontier section) reads "Census of record (gate receipt `controls/gate-final-r55.txt`,
  **`CENSUS-FRESH=ok`**, fixed point confirmed over two identical runs)"; the SCORECARD round-55
  census cell reads "the round-55 tip reads the figures in the gate receipt `controls/gate-final-r55.txt`
  (**`CENSUS-FRESH=ok`**), measured after the last corpus/SCORECARD/LOG edit"; the LOG round-55
  entry reads "(**`CENSUS-FRESH=ok`**, exit 0)".
- Measured value: the SAME committed receipt they cite prints the opposite —
  `.ufo/waves/round-55/controls/gate-final-r55.txt` line 8: `CENSUS-FRESH=stale
  files=citation-survival.md+citation-survival.tsv (committed bytes differ from what resolve.py
  generates over the current tree; regenerate the census or repair the tree)` with `[exit=1]` —
  and the gate re-run at the tip reproduces it (`python corpus/instruments/census-freshness-check.py .`
  → `CENSUS-FRESH=stale`, exit 1; the round-55 closure verifier ran the same command and got the
  same answer, which is how DF-3 was routed).
- Root cause (the closure's §3, held): the self-referential citation. The round-55 lesson cites the
  receipt path `.ufo/waves/round-55/controls/gate-final-r55.txt`; the committed census pair was
  generated BEFORE the receipt file existed, so the pair counts that path GONE; once the receipt
  exists, a regeneration counts it INTERNAL. The receipt's limb-1 summary (internal=1118,
  gone=3883, all=1130/5013) matches the committed pair because it was captured in the same
  pre-receipt generation — so the receipt header's "the census pair is the regeneration FIXED
  POINT" and the report's "fixed point confirmed over two identical runs" do not hold at byte
  level over the truly final tree: exactly one citation (the receipt path cited by the lesson)
  moves between generations.
- Disposition: the freshness-status literal `CENSUS-FRESH=ok` in the three filed artifacts is
  **superseded by `CENSUS-FRESH=stale … [exit=1]` as of the round-55 tip** (the receipt's own
  printed limb is the superseding fact). The round-55 report is fleet-repo record (not rewritten
  here); the SCORECARD/LOG bytes are historical round-record (never rewritten, R6/R8). The QUOTED
  census figures themselves (internal=1118, gone=3883, 1130/5013 = 22.54%) were correct for the
  committed pair they cite — the wrong literal was only the freshness status and the fixed-point
  claim. Fix, all in round 56: (1) this erratum; (2) the fixed-point regeneration receipt
  `.ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt` — resolve.py re-run over a
  reconstruction of the round-55 tip that CONTAINS the committed receipt prints the post-receipt
  fixed point internal=1119 gone=3882 all=1131/5013 = 22.56% (distinct=5013 resolves=12
  unchanged), a second run is identical, and the freshness gate then reads ok over that tree —
  the one-iteration convergence; (3) machine-catching ledger entries in
  `corpus/instruments/figure-audit-ledger.json` (round-56 C1): `census-fresh-literal-r55`
  (want `stale`), `census-internal-r55-receipt` (want 1118), `census-gone-r55-receipt` (want
  3883), `census-fixedpoint-internal-r55` (want 1119), `census-fixedpoint-gone-r55` (want 3882),
  plus a red control carrying the filed prose literal AS FILED (want `ok` → stale, exit 1), so
  this exact prose-vs-receipt class AND the two-generation figure confusion are machine-caught
  from now on; (4) the class cannot recur in the round-56 form: the final gate receipt is
  produced by a true tee (the receipt file exists from the run's first byte, so the census pair
  regenerated inside it already counts the receipt's citations INTERNAL and the freshness limb
  reads ok at the fixed point), and no corpus/SCORECARD/LOG edit follows that receipt.
- Ironic class (the closure's own note, doubled): this is the DF-1 prose-vs-receipt family —
  the round-55 round fixed DF-1 with an erratum plus machine-catching ledger entries, and its own
  freshness prose drifted from its own receipt the same way. The red control's first entry IS the
  round-55 prose literal, and it reads stale forever by construction: the audit proves the
  supersession instead of trusting it.

## Closure check (bash -n parseable; run from the lane root)

```sh
cd "$(git rev-parse --show-toplevel)" || exit 9
r=.ufo/waves/round-55/controls/gate-final-r55.txt
e=.ufo/waves/round-56/controls/df3-census-erratum.md
f=.ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt
ok=1
[ "$(grep -c 'CENSUS-FRESH=stale' "$r")" = "1" ] || ok=0
grep -q 'CENSUS-FRESH=ok' "$e" || ok=0
grep -q 'superseded by .CENSUS-FRESH=stale' "$e" || ok=0
[ "$(git show 133c575394099abf28ddf1b0125c53aefde3e0fa:SCORECARD.md | grep -cF 'controls/gate-final-r55.txt` (`CENSUS-FRESH=ok`)')" = "1" ] || ok=0
[ "$(git show 133c575394099abf28ddf1b0125c53aefde3e0fa:LOG.md | grep -cF 'CENSUS-FRESH=ok`, exit 0')" = "1" ] || ok=0
[ "$(git show 133c575394099abf28ddf1b0125c53aefde3e0fa:corpus/instruments/citation-survival.md | grep -cE '\| INTERNAL \| 1118 \|')" = "1" ] || ok=0
[ "$(git show 133c575394099abf28ddf1b0125c53aefde3e0fa:corpus/instruments/citation-survival.md | grep -cE '\| GONE \| 3883 \|')" = "1" ] || ok=0
[ -f "$f" ] || ok=0
[ "$(grep -oE 'internal=[0-9]+' "$f" | tail -1 | cut -d= -f2)" = "1119" ] || ok=0
[ "$(grep -oE 'gone=[0-9]+' "$f" | tail -1 | cut -d= -f2)" = "3882" ] || ok=0
grep -q 'all=1131/5013' "$f" || ok=0
grep -q 'CENSUS-FRESH=ok' "$f" || ok=0
[ "$ok" -eq 1 ] && { echo "df3-erratum=closed"; exit 0; }
echo "df3-erratum=open"; exit 1
```

Exit 0 only when the receipt's printed stale limb is exactly once AND the erratum names both
literals AND the filed SCORECARD/census bytes stand unrepaired at the round-55 tip (the "ok" prose
exactly once; the committed pair still reading 1118/3883) AND the fixed-point receipt exists and
prints the post-receipt fixed point (internal=1119, gone=3882, all=1131/5013) with a green
freshness limb; non-zero while any limb fails.
