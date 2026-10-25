# ExecC2Counters — round-28 wave 1, frozen C2 counter re-run

Seat: read-only counter seat (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Measured at lane HEAD `94f387cbee71a532a51ce075f01701a557231e85`; claims-freeze base
`c9f8b115a098c65356e4b3b6048af45a37ab8395` verified ancestor (`merge-base --is-ancestor` exit 0).
Production edits: **none**. Tooling installs: **none**.

## What ran

Two measured passes of the five frozen C2 counters (claims.json `counter_commands`, executed from the
lane root), all read-only:

| pass | window (UTC) | label |
| --- | --- | --- |
| 1 | 2026-10-25T17:21:57Z–17:21:58Z | PRE-STATE |
| 2 | 2026-10-25T17:22:28Z–17:22:29Z | PRE-STATE (captures landed, consumers not) |

## Results (verbatim in `.ufo/waves/round-28/receipts/ExecC2Counters.txt`)

| # | counter | pass 1 | pass 2 | after target | label |
| --- | --- | --- | --- | --- | --- |
| 1 | admitted frontier rows (README awk) | 11 | 11 | 12 | PRE-STATE |
| 2 | entries citing `source: S042` | 0 | 0 | 1 | PRE-STATE |
| 3 | S042 registry rows | 0 | 0 | 1 | PRE-STATE |
| 4 | sources census validate | exit=0 (41 rows; W04 S028/S029 duplicate-url warnings, `ok`) | exit=0 (41 rows, same) | exit=0 with S042 row present | exit matches; after-state unreached → PRE-STATE |
| 5 | frontier-recheck-count.py | entries=14 pass=14 exit=0 | entries=14 pass=14 exit=0 | entries=15 pass=15 exit=0 | PRE-STATE |

No counter reaches its after value; the frozen do-nothing control holds. Every counter is stable across
both passes, so no partial landing moved a measured value.

## Landing state observed (not inferred)

- `corpus/source-snapshots/round-28/S042.txt` present at pass 1: 60508 B,
  sha256 `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`.
- `corpus/source-snapshots/round-28/S041.txt` absent at pass 1, present at pass 2: 147267 B,
  sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`.
- `manifest.json`, `corpus/knowledge/japanese-domestic-disclosure-workflow.md`, the S042 registry row,
  and the F12 README row are all still absent — so counters 1–3 and 5 remain PRE-STATE.

## Exact post-change re-run (L1, from the lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
echo "C1 $(date -u +%Y-%m-%dT%H:%M:%SZ)"; awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md; \
echo "C2 $(date -u +%Y-%m-%dT%H:%M:%SZ)"; grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l; \
echo "C3 $(date -u +%Y-%m-%dT%H:%M:%SZ)"; grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md; \
echo "C4 $(date -u +%Y-%m-%dT%H:%M:%SZ)"; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"; \
echo "C5 $(date -u +%Y-%m-%dT%H:%M:%SZ)"; python3 corpus/instruments/frontier-recheck-count.py
```

Required post-change values: **C1=12, C2=1, C3=1, C4 census_exit=0 with 42 rows, C5 entries=15 pass=15 exit=0.**

## Residual C2 conditions these counters do not test

Not measured here, so not claimed: manifest.json Q9-bound quote assertions exactly-once; entry recheck
`--source` ids equal to the declared `S041`/`S042` headers (harness checks A/B once the entry exists);
S042 row tier A / mined / opened 2026-10-25 / used-by exactly the entry; S041 used-by gain with old→new
log; `source-recheck.py` exit 0 on both ids; assimilation Gate ≥1 admit + ≥1 reject with ≤25-word inline
quotes; R14 landing. L1 must verify each directly.

## Risks / blockers

- Risk: counters measured before consumers landed; if the entry/registry/manifest land later, the values
  above are snapshots, not the round-end verdict. Re-run the block above at round end.
- Risk: census W04 duplicate-url warnings for S028/S029 are pre-existing and exit 0 — do not read them as
  C2 failures.
- Blockers: none.

## Files changed by this seat

- `.ufo/waves/round-28/receipts/ExecC2Counters.txt` (receipt)
- `.ufo/waves/round-28/wave1/ExecC2Counters.md` (this report)
