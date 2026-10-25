# r1-digest-lineage — round-25 receipt lineage, pinned digest mismatch

Seat: `L1Kasegi26.RevDigestLineage` (revenger, read-only). Wave 1, round 26.
UTC access time: 2026-10-25 (all checks below run this day).
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `1b076fa7f2fb5e7dd9d87449514eba526043421b`.

## 1. Round-25 tip instrument bytes and digest

- Round-25 tip commit: `41a77b83f3a338053fa69629d753546b8d592617`
  ("round-25: pin lane head in iteration log", 2026-10-25 06:08:41 -0300).
- The instrument was introduced in `98261ebaf06b6415badaec362c69623d0e1db880`
  ("round-25: repair rechecks and assimilate vendor policies"); blob at the
  round-25 tip is `146d349480419ec5c920cbdc739e0820a432cfd7`
  (`git ls-tree 41a77b8 corpus/instruments/`).
- Byte reconstruction:

  ```
  $ git show 41a77b8:corpus/instruments/recheck-audit.py | sha256sum
  c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  -
  ```

- Pinned digest file `c1-instrument-digest.txt` line 1 (verbatim):

  ```
  instrument=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f
  ```

  → the reconstructed round-25 tip bytes hash to exactly the pinned digest;
  the pin is correct. The same content digest `c3c19adc…` is attested at every
  commit that touches the file: `e8de75a8ab00a74d900e99556c23ac48259ff1a7`,
  `9aa322618885bce7beb997eb81dabe20b07293a2`, `98261ebaf06b6415badaec362c69623d0e1db880`,
  `60bad6ce879bdd5a494a1abd38efffe5565a34ff` (each `git show <c>:corpus/instruments/recheck-audit.py | sha256sum` = `c3c19adc…`).

## 2. Working tree == round-25 committed bytes (no silent drift before e1)

  ```
  $ git show 41a77b8:corpus/instruments/recheck-audit.py > /tmp/r25-instr.py
  $ cmp /tmp/r25-instr.py corpus/instruments/recheck-audit.py
  [no output — IDENTICAL]
  $ sha256sum /tmp/r25-instr.py corpus/instruments/recheck-audit.py
  c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  /tmp/r25-instr.py
  c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f  corpus/instruments/recheck-audit.py
  ```

Working-tree bytes are byte-identical to the round-25 committed bytes and hash to
`c3c19adc…`. No silent drift existed before this round's e1 change
(`ExecAuditFix`, sole owner of the instrument) — the pre-change baseline is the
round-25 pinned bytes. `git status --porcelain` shows no tracked file modified;
the only untracked paths are round-26 orchestrator-owned planning files
(`.ufo/waves/round-26/{assimilation/,build-wave1-spec.py,wave1-*.json}`, `corpus/source-snapshots/round-26/`).

## 3. Receipt index line 4 and the wave2 cross-reference contradiction

`grep -nc selftest .ufo/waves/round-25/c1-receipt-index.txt` → `0`. The index
contains NO selftest line (13 lines total: one digest pin + three receipt blocks).
A sweep of `.ufo/waves/round-25/` for `selftest cases=` finds only copies of the
instrument itself inside mutant trees (`wave1/mut-skip/{pristine,c1,c2abs,c2tilde,c3,c4,c5,c6}/corpus/instruments/recheck-audit.py`, `variant-*.py`) — no receipt file carries a selftest line.

Index line 4 (verbatim, pulled with line numbers):

```
4:executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
```

It is the `c1-before-strict` summary line, not a selftest line.

wave2/C1InstrumentDigest.md claims otherwise (verbatim):

- Section heading: `### 3. Selftest at the pinned digest (index line 4 claims `cases=14 failures=0 exit=0`)`
- After quoting the selftest run: `Matches `c1-receipt-index.txt:4` exactly.`

Contradiction: the index has no selftest line anywhere, so nothing in it can
"claim `cases=14 failures=0 exit=0`", and index line 4 (`executes=12 gated=0
broken=23 …`) is not the selftest summary. The wave2 report's own selftest run is
genuine and reproduces today:

```
selftest cases=14 failures=0 exit=0
```

(14 cases, `exit=0`; matches the round-25 lesson's "(14 cases, `failures=0`)",
round-25.md line 59-60). The defect is the cross-reference line number, not the
digest: the instrument pin `c3c19adc…` is verified correct in §1-2. This is the
R25-2 cross-reference defect C1 of round 26 is charged with fixing
(claims.json C1 predicate (b): "a committed selftest receipt line `selftest cases=… failures=0`
exists in .ufo/waves/round-26/c1-receipt-index.txt at the instrument's own sha256
(fixes R25-2 cross-reference)").

## 4. What the round-26 receipt must contain, and what must stay untouched

Per the frozen C1 predicate and the `ExecReceiptIndex` task, the round-26
`c1-receipt-index.txt` must contain:

1. `instrument_sha256=<sha256 of the post-e1 instrument at write time>` (computed
   with sha256sum), plus a control line printing the base (pre-change) digest
   `c3c19adc…`.
2. A **selftest line** `selftest cases=15 failures=0 exit=0` — the line the
   round-25 index lacked — recorded only after `python3 corpus/instruments/recheck-audit.py --selftest`
   passes 15 cases (e1 adds two fixtures; today's pre-change run is 14). If any
   fixture fails, the failing lines must be quoted verbatim and 0 failures must
   not be claimed.
3. The live lane audit summary line (`lines/total/pass_strict/exit`) from
   `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-26/c1-live.json --cdroot <lane root>`.
4. A note line correcting the round-25 cross-reference: the old index had no
   selftest line at :4 (wave2/C1InstrumentDigest.md said otherwise); the new
   index carries the selftest receipt at the new digest.
5. `c1-instrument-digest.txt` (new sha256 + old-digest note).

Round-25 files that must remain untouched (no edits, corrections land as separate
appended files): `.ufo/waves/round-25/c1-receipt-index.txt`,
`.ufo/waves/round-25/c1-instrument-digest.txt`,
`.ufo/waves/round-25/wave2/C1InstrumentDigest.md`, the round-25 lesson(s)
(`corpus/lessons/round-25.md`, `round-25-verifier-spotcheck.md`), and both
`claims.json` files (round-25 and the frozen round-26).

## Evidence chain

| # | check | result |
|---|---|---|
| 1 | `git show 41a77b8:corpus/instruments/recheck-audit.py \| sha256sum` | `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` |
| 2 | `c1-instrument-digest.txt:1` | `instrument=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` — matches #1 |
| 3 | `cmp` committed vs working tree | IDENTICAL |
| 4 | `sha256sum corpus/instruments/recheck-audit.py` | `c3c19adc…` — equals #1 |
| 5 | `grep -nc selftest .ufo/waves/round-25/c1-receipt-index.txt` | `0` (no selftest line) |
| 6 | index line 4 | `executes=12 gated=0 broken=23  (gated = …)` — not a selftest line |
| 7 | `python3 corpus/instruments/recheck-audit.py --selftest` | `selftest cases=14 failures=0 exit=0`, `EXIT=0` |
| 8 | wave2/C1InstrumentDigest.md | claims "Matches `c1-receipt-index.txt:4` exactly" — contradicted by #5/#6 |

Instrument blob at round-25 tip: `146d349480419ec5c920cbdc739e0820a432cfd7` (tree `41a77b8`, mode 100755).
