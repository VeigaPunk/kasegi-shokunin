# ExecCensusAfter — round 30 C2 census

## Scope and byte state

Ran after the F14 entry existed and the registry count reached 47. The assigned checks were read-only; no tools installed and no live target contacted. The initial row-count poll returned 45; after waiting for the wave's S046/S047 rows, the measured registry count was 47. The F14 knowledge entry was present before the final census.

## Exact outputs

```text
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
47

$ tier histogram (awk over registry rows)
A 44
B 1
C 2

$ status histogram (awk over registry rows)
mined 35
queued 9
rejected 3

$ malformed registry rows (column count, tier/status fields)
malformed_count=0

$ duplicate ids
none

$ enum violations (tier/status)
none

$ missing mined used-by paths (filesystem existence scan)
none

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi\tW04\tS028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi\tW04\tS029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi\tok\t/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

The W04 lines are the validator's duplicate-URL warnings for already recorded S028/S029 across scopes; the validator nevertheless reports the registry `ok` and exits 0. No enum violations, malformed rows, duplicate IDs, or missing mined used-by paths were observed.

## Files changed

- `.ufo/waves/round-30/wave1/ExecCensusAfter.md` — this scoped evidence receipt.

## Risks / blockers

None for the assigned census. No test/build/lint run; none was requested for this seat.
