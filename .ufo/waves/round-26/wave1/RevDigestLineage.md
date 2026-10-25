# RevDigestLineage — round-25 receipt lineage (scoped findings)

Seat `L1Kasegi26.RevDigestLineage` (revenger, read-only). Round 26, wave 1.
UTC access date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Full deliverable with hashes/quotes/commit ids:
`.ufo/waves/round-26/wave1/r1-digest-lineage.md`.

## Verdict

- The round-25 instrument digest pin is **correct**: `git show 41a77b8:corpus/instruments/recheck-audit.py | sha256sum` = `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` = `c1-instrument-digest.txt:1` (`instrument=c3c19adc…`).
- **No silent drift**: `cmp` of the committed round-25 tip bytes vs the working tree is IDENTICAL; both hash `c3c19adc…`. Pre-change baseline before e1 = round-25 pinned bytes.
- The known mismatch is a **cross-reference defect, not a digest defect**: `.ufo/waves/round-25/c1-receipt-index.txt` has NO selftest line (`grep -nc selftest …` → 0). Its line 4 is `executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)`. wave2/C1InstrumentDigest.md asserts "Index line 4 claims `cases=14 failures=0 exit=0`" and "Matches `c1-receipt-index.txt:4` exactly" — contradicted by the file (R25-2). The selftest itself is real and reproducible: `selftest cases=14 failures=0 exit=0` on the current pre-change bytes.

## Required round-26 receipt fix (per frozen C1 + ExecReceiptIndex)

`c1-receipt-index.txt` (round 26) must contain: `instrument_sha256=<new sha256>` + base-digest control line (`c3c19adc…`); the selftest line `selftest cases=15 failures=0 exit=0` (only after the post-e1 15-case selftest passes); the live audit summary; and a correcting note stating the round-25 index had no selftest line at :4. New `c1-instrument-digest.txt` with the new sha256 + old-digest note.

Untouched: all round-25 files (`c1-receipt-index.txt`, `c1-instrument-digest.txt`, `wave2/C1InstrumentDigest.md`, round-25 lessons, both claims.json); corrections land as separate appended files.

## Evidence (all run today)

1. `git show 41a77b8:corpus/instruments/recheck-audit.py | sha256sum` → `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`
2. `sha256sum corpus/instruments/recheck-audit.py` → `c3c19adc…` (equal)
3. `cmp <(git show 41a77b8:corpus/instruments/recheck-audit.py) corpus/instruments/recheck-audit.py` → IDENTICAL
4. `grep -nc selftest .ufo/waves/round-25/c1-receipt-index.txt` → 0
5. Index line 4 (verbatim): `executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)`
6. `python3 corpus/instruments/recheck-audit.py --selftest` → `selftest cases=14 failures=0 exit=0`, EXIT=0
7. Instrument blob at round-25 tip `41a77b83f3a338053fa69629d753546b8d592617`: `146d349480419ec5c920cbdc739e0820a432cfd7`; added in `98261ebaf06b6415badaec362c69623d0e1db880`.

No tool installs. No production edits; only the two owned report files written.
