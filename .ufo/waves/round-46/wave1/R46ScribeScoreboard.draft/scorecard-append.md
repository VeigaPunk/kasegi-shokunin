
## Round 46 result

DRAFT (seat R46ScribeScoreboard, not committed). Frozen at `.ufo/waves/round-46/claims.json` (freeze commit `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5`, base `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`; claims sha256 `e56ebf87…`). Freeze record `.ufo/waves/round-46/freeze.txt`; controls `.ufo/waves/round-46/controls/freeze-controls.txt` (total=9 red=9 green=0). Lane-tip measurement: `[[FILL-BY-L1: tip commit and .ufo/waves/round-46/controls/final-measure.txt path]]`. No score move is claimed in this block; every score below is held until the L1 measures at the tip.

| Axis | Score before r46 | Score after r46 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 held — pending L1 measurement (C1 target: gated 24 → ≤22; score 5 still needs 0 gated and the 25/25-chains audit) | C1 `python3 corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base-export>`: base `c1-gate fixed=1/7 exit=1`, freeze `c1-gate fixed=1/7 exit=1`, tip `[[FILL-BY-L1: c1-gate fixed=<k>/7 exit=<e>]]` | r46 (held) |
| coverage | 8 | 8 held — pending L1 measurement (C2 target: 27 → 28 admitted frontier rows, F28 = GitHub private vulnerability reporting; not a coverage-ratio move, see the limb below) | C2 `python3 corpus/instruments/r46-c2-gate.py --root <tree>`: base `c2-gate fixed=1/7 exit=1`, freeze `c2-gate fixed=2/7 exit=1`, tip `[[FILL-BY-L1: c2-gate fixed=<k>/7 exit=<e>]]` | r46 (held) |
| depth:density | 9 | 9 held — non-target guard; tip `[[FILL-BY-L1: density.py byte-identical to base? sha256 at tip]]` | `[[FILL-BY-L1: density.py measurement at tip]]` | r46 (held) |

### Round-46 held-axis promotion limbs (the next claim each held score targets)

Measured distances are printed command output. Source for the limbs: `## Distance-to-next-score` (`SCORECARD.md:1532-1557`).

**depth:verifiability, held at 4; target 4 → 5.** Two limbs, both must read at the judged head (`SCORECARD.md:1538-1541`).

1. *0 gated rechecks.* Measured at base and at freeze (identical): `python3 corpus/instruments/recheck-audit.py --root . --quiet | grep '^executes='` → `executes=40 gated=24 broken=0`; `python3 corpus/instruments/score-gap.py | grep '^gap:'` → `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`. Distance: **24 gated lines to 0**. The round-46 C1 claim is the first step of this limb only: it targets gated 24 → ≤22 (intended pair `corpus/knowledge/claim-package-contract.md` and `corpus/knowledge/claim-gates.md`, re-grounded on committed bytes). After the C1 target, **22 gated lines remain to 0**. The 23 `test -d ~/Projects/...` guards are unchanged by this claim.
2. *The score-5 audit bar.* `SCORECARD.md:331`: "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims." Not measured in round 46: no non-author audit of source chains exists for round 46 at base or freeze. `[[FILL-BY-L1: non-author 25/25 chains audit receipt, or "not run"]]`.

**coverage, held at 8; target 8 → 9.** The 7 → 8 criterion (`SCORECARD.md:1547-1555`), `(20 + F_admitted) / (20 + F_total)`, is already at 1.000 at base and at freeze, so it cannot move on the round-46 claim:

```
$ awk -F'|' '$2 ~ /^ *S[0-9]+ *$/ && $9 ~ /^ *queued *$/ {n++} END{print n+0}' corpus/SOURCES.md     # base and freeze
0
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                                           # base and freeze
27
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md      # base and freeze
27
$ (20+27)/(20+27+0) = 47/47 = 1.000
```

The r39 `queued` term (nine rows) is 0: S016/S017/S019/S020/S021/S023/S025 are `mined` and S022/S024 are `rejected` (`corpus/SOURCES.md`, 57 mined + 15 rejected = 72 rows). After C2 lands (F28 admitted, S073 `mined`, `queued` still 0) the same expression reads `(20+28)/(20+28+0) = 1.000`: **the criterion cannot register C2's +1 row.** The next coverage limb is therefore not the 7 → 8 criterion. `SCORECARD.md` states no 8 → 9 criterion (the `Distance-to-next-score` section covers 4 → 5 and 7 → 8 only); `[[FILL-BY-L1: adopt a stated 8 → 9 criterion in a re-based Distance section, or record that none is adopted]]`. The operator-owned half, `0/18` domain surfaces present (`corpus/README.md:55-56`, `PROVINCE.md:121-122`), is not an in-lane limb.

**depth:density, held at 9.** Non-target guard; no promotion limb is targeted by round 46. Appended registry rows do not move the density reading (`## Round 45 result`).

### Round-46 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 46 | depth:verifiability | gated 24 of 64 (base and freeze); C1 `fixed=1/7` at both | `[[FILL-BY-L1: tip gated count and c1-gate fixed=<k>/7; target gated ≤22, fixed=7/7]]` | `corpus/instruments/r46-c1-gate.py`; `.ufo/waves/round-46/controls/freeze-controls.txt` |
| 46 | coverage | admitted F 27, SOURCES 72 (queued 0), knowledge 64; C2 `fixed=1/7` base, `fixed=2/7` freeze | `[[FILL-BY-L1: admitted F 28, SOURCES ≥73, knowledge 65, S073 sha256 OK + Q1-Q8 OK, c2-gate fixed=<k>/7]]` | `corpus/instruments/r46-c2-gate.py`; `corpus/source-snapshots/round-46/S073.txt`; `corpus/source-snapshots/round-46/manifest.json` |

### Round-46 counting commands (one per claim; base and freeze values printed by this seat)

Base = `/fast/scratch/hyaku/kasegi-r46/L1/pure` (copied). Freeze = `git archive 9f23aab…` of the full tree. Tip values are `[[FILL-BY-L1]]`.

- **C1 counter** — `python3 corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base-export>` → base `c1-gate fixed=1/7 exit=1`; freeze `c1-gate fixed=1/7 exit=1`; tip `[[FILL-BY-L1]]`. The seven limb lines at base and freeze are byte-identical to the do-nothing control in `freeze-controls.txt`.
- **C1 plain 1** — `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` → base `23`; freeze `23`; tip `[[FILL-BY-L1]]` (target ≤21).
- **C1 plain 2** — `python3 corpus/instruments/recheck-audit.py --root . --quiet | grep '^executes='` → base `executes=40 gated=24 broken=0`; freeze `executes=40 gated=24 broken=0`; tip `[[FILL-BY-L1]]` (target `gated≤22 broken=0`).
- **C1 plain 3** — `python3 corpus/instruments/score-gap.py | grep '^gap:'` → base and freeze `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`; tip `[[FILL-BY-L1]]`.
- **C2 counter** — `python3 corpus/instruments/r46-c2-gate.py --root <tree>` (the script takes `--root` only; `--baseline` is rejected with exit 2) → base `c2-gate fixed=1/7 exit=1`; freeze `c2-gate fixed=2/7 exit=1`; tip `[[FILL-BY-L1]]`.
- **C2 plain 1** — `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → base `27`; freeze `27`; tip `[[FILL-BY-L1]]` (target 28).
- **C2 plain 2** — `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → base `72`; freeze `72`; tip `[[FILL-BY-L1]]` (target ≥73).
- **C2 plain 3** — `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → base `64`; freeze `64`; tip `[[FILL-BY-L1]]` (target 65).
- **C2 plain 4** — `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` → base `manifest UNAVAILABLE reason=missing` (exit 2); freeze `S073:sha256 OK` and `S073:Q1 OK` … `S073:Q8 OK` (exit 0); tip `[[FILL-BY-L1]]`.
- **C2 plain 5** — `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → base empty; freeze empty; tip `[[FILL-BY-L1: README, SOURCES, the new entry]]`.
- **C2 secondary** — `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 28` → base `frontier expected=28 admitted=27 verdict=SHORT exit=1`; freeze the same; tip `[[FILL-BY-L1]]`.
- **Coverage criterion** — the awk/grep expression in the coverage limb above → `(20+27)/(20+27+0) = 1.000` at base and freeze; tip `[[FILL-BY-L1: (20+28)/(20+28+0) expected 1.000]]`.
- **Frontier entries** — `python3 corpus/instruments/frontier-recheck-count.py` → base `entries=30 pass=30 exit=0`; freeze `entries=30 pass=30 exit=0`; tip `[[FILL-BY-L1]]`.

### Round-46 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| `r46-landing-gate.py` (proposed) | Not demonstrated. No file of that name exists in the lane tree at base or freeze (`find <tree> -name '*landing-gate*'` printed nothing at either). No capability is claimed; the row is a proposal only. | none; `[[FILL-BY-L1: demonstration path and receipt, if one is built]]` | none yet (proposed) |

### Planned evidence gates for round 47

- `depth:verifiability`: name each claim's before-value at base and at the freeze tree (this block's counting commands are the template); run `python3 corpus/instruments/capture-binding-check.py --root <tree>` and the census before dispatching a wave; the 0-gated limb needs the remaining 22 gated lines re-grounded or re-based, not re-described; no score 5 claim until the non-author 25/25-chains audit has run and printed.
- `coverage`: the 7 → 8 criterion is already met and cannot discriminate the next claim; before any coverage statement, a stated 8 → 9 criterion (or an explicit "no criterion adopted") must be written into `## Distance-to-next-score`; a non-author admit/reject re-check of the round-46 admitted row(s) (F28, S073) is required before a coverage statement beyond the row count.
- Both axes: the tip values of every counting command above are recorded in `.ufo/waves/round-46/controls/final-measure.txt` before this block leaves `[[FILL-BY-L1]]`.
