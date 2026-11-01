# round-55 routed-defect erratum — DF-1 (the "0 mentions" prose vs the do-nothing receipt's 2; appended file; no filed byte edited)

Filed by round 55 against base `ed60637394b170a4120fda501b9b9c5387f2df24`, addressing the round-54
non-author closure's routed defect DF-1 (`corpus/lessons/round-54-verifier-spotcheck.md` §2, DF-1:
"number drift in report/freeze prose, contradicted by the lane's own receipt"; status-neutral).
R9 form: a numerical erratum naming its base and superseded literals, appended as a NEW file — the
corrected records' bytes are never rewritten. The companion DF-2 receipt (the never-committed
`.ufo/waves/round-54/controls/d53-base-greps-r54.txt`, cited by cfdf059) is regenerated and lands in
this same commit, so both routed pointers now resolve.

## DF-1 — the base-SCORECARD mention count (prose 0 vs receipt 2)

- Filed literals: the round-54 report (`shokunin-clone/shokunin/.ufo/reports/round-54/kasegi.md`,
  C1 measurement bullet) reads "exit 128 and **0 mentions** in base SCORECARD/LOG/knowledge-expected
  (`controls/c1-donothing-r54.txt` …)"; the frozen round-54 C1 sentence
  (`.ufo/waves/round-54/claims.json`, C1 `frozen_sentence` clause (d)) reads "'figure-audit' appears
  **0 times in the base SCORECARD.md**".
- Measured value: the SAME committed receipt they cite prints **2** for the SCORECARD limb —
  `.ufo/waves/round-54/controls/c1-donothing-r54.txt`: `$ git show
  32782bd:SCORECARD.md | grep -c 'figure-audit'` → `2` (receipt lines 12-14) — and re-derives
  from base bytes: `git show 32782bd6b564f80454af853b38868603a4140e79:SCORECARD.md | grep -c
  'figure-audit'` → `2` (SCORECARD.md:2102 and :2158 — the r52-planned / r53-routed
  "figure-audit sibling" text, i.e. the defect routing that demanded the instrument, not a
  pre-existing capability). The LOG and knowledge-expected limbs of the prose are correct as
  filed (0 and 0).
- Disposition: the SCORECARD mention figure in both filed artifacts is **superseded by 2**. The
  round-54 report is fleet-repo record (not rewritten here); the frozen claims.json is a
  freeze-commit record (never amended, R44/R39). The substantive do-nothing claim (the capability
  absent at base: `git cat-file -e` exit 128) was and stays true — the judge re-derived it; only
  the prose count was wrong. Fix, both in round 55: this erratum (the record of the correction),
  and machine-catching ledger entries — `figure-audit-mentions-base-scorecard` (want 2),
  `figure-audit-mentions-base-log` (want 0), `figure-audit-mentions-base-knowledge-expected`
  (want 0) in `corpus/instruments/figure-audit-ledger.json` (round-55 C1), so this exact drift
  class is machine-caught from now on. Mined in `corpus/lessons/round-55.md` § Mistakes.
- Ironic class (the closure's own note): this is exactly the D53 number-drift family the round-54
  round made machine-catchable — the round's own prose drifted from its own receipt the same way
  the r53 trailer had.

## Closure check (bash -n parseable; run from the lane root)

```sh
cd "$(git rev-parse --show-toplevel)" || exit 9
r=.ufo/waves/round-54/controls/c1-donothing-r54.txt
e=.ufo/waves/round-55/controls/df1-mentions-erratum.md
g=.ufo/waves/round-54/controls/d53-base-greps-r54.txt
ok=1
grep -q '0 mentions' "$e" || ok=0
grep -q 'superseded by 2' "$e" || ok=0
[ "$(git show 32782bd6b564f80454af853b38868603a4140e79:SCORECARD.md | grep -c 'figure-audit')" = "2" ] || ok=0
[ "$(git show 32782bd6b564f80454af853b38868603a4140e79:LOG.md | awk '/figure-audit/{n++} END{print n+0}')" = "0" ] || ok=0
[ "$(git show 32782bd6b564f80454af853b38868603a4140e79:corpus/instruments/knowledge-expected.txt | awk '/figure-audit/{n++} END{print n+0}')" = "0" ] || ok=0
[ "$(grep -A1 "grep -c 'figure-audit'" "$r" | grep -cx '2')" = "1" ] || ok=0
[ -f "$g" ] || ok=0
grep -q 'DF-2' "$e" || ok=0
[ "$ok" -eq 1 ] && { echo "df1-erratum=closed"; exit 0; }
echo "df1-erratum=open"; exit 1
```

Exit 0 only when the superseded literal and its measured value are both named AND the base bytes
re-derive 2/0/0 AND the cited receipt itself prints 2 AND the DF-2 receipt exists; non-zero while
any limb fails.
