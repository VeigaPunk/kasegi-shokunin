# AttackA5 — C1d deletion-mutant suite on the LANDED instrument

- Seat: `L1Kasegi26.AttackA5` (leaf, read-only; no dispatch).
- Date (UTC): 2026-10-25T12:52Z.
- Attacked claim: C1 AFTER state `deletion_fixture_exit=1` +
  `deletion_fixture_missing` (deletion soundness), on the landed instrument
  digest `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`
  with the committed `corpus/instruments/knowledge-expected.txt` (39 entries).
- Full run log with verbatim tails: `wave2/a5.md`; raw logs:
  `c1-controls/a5-{E,A,B,C,D,F}.txt`; machine receipts: `/tmp/a5/<label>/receipt.json`.

## Method

Six scratch fixtures under `/tmp/a5/`, each a `cp -a` copy of the landed
`corpus/` with exactly one mutation (verified `diff -rq` vs clean; see a5.md
§Deltas). Every run used the landed instrument:

```
python3 corpus/instruments/recheck-audit.py --root /tmp/a5/<label> --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json /tmp/a5/<label>/receipt.json
```

All receipts confirm `instrument_sha256=3fc0d751…` (landed bytes executed).

## Results summary

| fixture | mutation | exit | expect | missing | unexpected | notes |
|---|---|---|---|---|---|---|
| E | none (clean) | 0 | present expected=39 | 0 | 0 | lines=39 total=39 pass=39 |
| A | deleted `multiparty-vulnerability-coordination.md` | 1 | present expected=39 | 1 (`missing=corpus/knowledge/multiparty-vulnerability-coordination.md`) | 0 | lines=38 total=38 |
| B | removed `recheck:` line from `operator-queue.md` | 1 | present expected=39 | 0 | 0 | completeness red: lines=38 total=39 |
| C | renamed `multiparty-vulnerability-coordination.md` → `…-renamed.md` | 1 | present expected=39 | 1 | 1 (`unexpected=…-renamed.md`) | lines=39 total=39 |
| D | added stray `stray-extra.md` (no recheck) | 1 | present expected=39 | 0 | 1 (`unexpected=corpus/knowledge/stray-extra.md`) | lines=39 total=40 |
| F | same as A, expected list removed | 0 | absent | 0 | 0 | old green pass reproduced (fallback) |

Verbatim tail lines for each run (including `EXIT=`) are recorded in `c1-controls/a5-*.txt` and quoted in full in `a5.md`.

## Verdict

- Mutant A **killed**: exit 1, `missing=corpus/knowledge/multiparty-vulnerability-coordination.md` (C1's exact AFTER value).
- Mutant B **killed**: exit 1 via the completeness rule (38/39), no silent shrink of the audited set.
- Mutant C **killed**: exit 1 with both `missing=` and `unexpected=` naming the old/new names.
- Mutant D **killed**: exit 1 with `unexpected=corpus/knowledge/stray-extra.md`.
- Control E **green**: exit 0, `expect=present expected=39 missing=0 unexpected=0`.
- Fallback F **documented**: without the committed list (`expect=absent`) the audit reverts to glob-based completeness and mutant A passes green (exit 0) — the deletion-soundness gain is carried by the committed expected list. This matches C1's `before` (`deletion_fixture_exit=0`).

C1d **holds on the landed bytes**: no surviving mutant, no fabricated verdict
(all numbers are verbatim tails of the control logs). Landed instrument sha256
and knowledge count (39) unchanged after all runs; no lane bytes modified outside
`c1-controls/` and `wave2/`.

Evidence pointers:
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/wave2/a5.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/c1-controls/a5-E.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/c1-controls/a5-A.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/c1-controls/a5-B.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/c1-controls/a5-C.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/c1-controls/a5-D.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/c1-controls/a5-F.txt`
- `/tmp/a5/{E,A,B,C,D,F}/receipt.json` (machine receipts)
