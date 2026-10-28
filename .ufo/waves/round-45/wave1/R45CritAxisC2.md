VERDICT: HOLDS

Scope: "coverage 8 — which denominator, and does F27 move it?" Read-only. Base = dc5bb8c (lane export), freeze = 8cf62c8. No edits, no git mutation; scratch removed on exit.

## 1. The criterion the score 8 rests on

`SCORECARD.md:1549-1553` (the r22 measure, round-39 section):

> `(20 + F_admitted) / (20 + F_total) = 1.000`, with `F_total` = frontier rows in `corpus/README.md` § Frontier plus every `corpus/SOURCES.md` registry row still `queued`, `F_admitted` = frontier rows whose status cell is `admitted`, and every admitted row's entry passing `frontier-recheck-count.py` (`pass` equal to `entries`, exit 0). The Core term stays 20 ... so it holds and the frontier and queued terms carry the move.

Three readings of "coverage", measured at base:

| Reading | Source | Base value | After F27 (real entry, S071 mined) | Δ |
|---|---|---|---|---|
| D1 r22 ratio (criterion) | SCORECARD:1549-1553 | 46/46 = 1.0000 | 47/47 = 1.0000 (arithmetic; see §3 limit) | 0 |
| D2 frontier-only | SCORECARD:1553 | 1.000 by construction | 1.000 | 0 (SCORECARD itself calls it non-discriminating) |
| D3 adopted r15 domain denominator | corpus/README.md:215-218; PROVINCE.md:121-122 | 0/18 surfaces present | 0/18 | 0 (frontier count explicitly kept outside 0/18) |

Answer to the axis question: **F27 is frontier ground in the criterion's literal sense** (it enters `F_admitted` and `F_total` as a matched pair once its row is `admitted` and its entry passes `frontier-recheck-count.py`), **but it is expansion-trend only with respect to the score**: no reading of the score changes value when an admitted row is added.

## 2. Measured (commands run; output quoted)

Counter: `measure.py <root>` reads `corpus/README.md` rows `^\| F\d+ \|` (cell 2 = status) and `corpus/SOURCES.md` rows `^\|\s*S\d{3,}\s*\|` (cell 9 = status), then prints `(20+adm)/(20+rows+queued)`.

- Base (do-nothing control): `root=base F_rows=26 F_admitted=26 registry=70 queued=0 criterion=(20+26)/(20+26)=1.0000`
- Registry status census at base: `grep -E '^\| *S[0-9]{3} *\|' corpus/SOURCES.md | awk -F'|' '{gsub(/^ +| +$/,"",$9); print $9}' | sort | uniq -c` → `56 mined` / `14 rejected`; zero `queued`.
- Control, junk queued registry row appended: `root=ctl-junkq F_rows=26 F_admitted=26 registry=71 queued=1 criterion=(20+26)/(20+27)=0.9787`. The ratio moves, but only through a queued row.
- Control, admitted `F27` row with no entry file: `root=ctl-f27noentry F_rows=27 F_admitted=27 registry=70 queued=0 criterion=(20+27)/(20+27)=1.0000`. The ratio stays 1.0000; `frontier-recheck-count.py` prints `FAIL     F27  knowledge/fixture-absent.md ids=- exit=- problems=missing-entry` and `entries=30 pass=29 exit=1` (exit 1 captured directly from the command).
- Base `frontier-recheck-count.py`: `entries=29 pass=29 exit=0` (exit 0).
- Base `r44-frontier-count.py --root . --expect 27`: `frontier expected=27 admitted=26 verdict=SHORT exit=1`. Without `--expect`: `frontier rows=26 admitted=26`, exit 0.
- Frozen C2 gate (`r45-c2-gate.py`, from freeze export 8cf62c8) on base: `c2-gate fixed=1/7 exit=1`, matching `expect_before` in `.ufo/waves/round-45/claims.json` and the frozen do-nothing control in `controls/freeze-controls.txt`. Gate lines: G1 `rows=26 admitted=26`, G7 `census-rc=0` pass; G2-G6 fail.
- Kernel grant at base: `grep -rliE 'security-bugs|linux kernel|kernel\.org' corpus/knowledge corpus/SOURCES.md corpus/README.md` → no output, exit 1. The claims' "before" statement holds.

Score history (why the 7→8 move was a queued-row event, not a frontier event):
- `SCORECARD.md:1557`: `coverage 41/50 = 0.820 strict, 41/41 = 1.000 frontier-only`
- `SCORECARD.md:1596` (round 40): `coverage 7 → 8 ... Nine queued rows decided ... measure 43/43 = 1.000`. The move came from the queued term going 9 → 0, not from adding admitted rows.

## 3. Naming defect (report must not hide)

- `SCORECARD.md:1549` describes the D1 criterion as "the r22 measure ... planned for adoption at `SCORECARD.md:178` and never adopted — round 23 kept the r15 denominator (`corpus/lessons/round-23.md:176-177`)". `grep -n adopt SCORECARD.md` returns lines 178, 332, 491, 1217, 1549 only; no later text adopts it. The round-40 score-8 row (`:1596`) does not state adoption either.
- So the current "coverage 8" is held on a ratio the SCORECARD itself says was never adopted. The adopted denominator (D3) is still 0/18 and is unchanged (`corpus/README.md:215`, `:218`).
- The score is therefore a corpus-facing ratio whose value is saturated at 1.000 whenever queued = 0 and every admitted row passes; the Core constant 20 cancels there (`(20+a)/(20+a)`).

## 4. What the report may honestly say

- **Allowed:** "coverage score held at 8; F27 adds one admitted frontier row (26 → 27, expansion trend); the r22 ratio is 1.000 before and after; no coverage score movement is claimed." Name the denominator as the r22 corpus-facing ratio (`SCORECARD.md:1549-1553`), flagged unadopted, with the adopted r15 0/18 cap unchanged.
- **Not allowed:** "coverage 8 → 9", "F27 moves coverage", "coverage moved". No denominator in the lane moves on an admitted row.
- **Downside only:** the criterion is a conjunction. If F27's entry fails `frontier-recheck-count.py` (control above: exit 1), or if S071 lands `queued` (control above: 0.9787), the coverage-8 criterion fails. F27 cannot raise the score; it can only break it.
- The claims file labels C2 as axis `coverage`, but its counters (`r45-c2-gate.py`, `r44-frontier-count.py --expect 27`) measure frontier-row count and entry shape. They do not measure the score. The C2 report row must state "score delta 0".

## 5. Limitations

- No real F27 row, entry, or S071 registry row exists in the lane tree yet (builders have not landed them; `wave1/` holds only `R45ExecFreezeA.draft` and `R45ScribeRowsB.draft`). The "After F27" column is the arithmetic applied to fixtures, not a measurement of a landed F27. The ratio depends only on status cells and row counts, which the no-entry fixture shows; entry content affects only term 3 (the recheck), which the no-entry control exercised by failing it.
- The junk-queued fixture is my own control, not the frozen `c2-junk-row` control (`freeze-controls.txt`: `fixed=4/7`). `r45-c2-gate.py` gave `fixed=0/7` on it; I did not reproduce the frozen 4/7 control.
- I did not run `recheck-audit.py`, `sources-census.sh`, or the full harness. I did not re-derive the historical r40–r44 measurements beyond the quoted SCORECARD lines.
- The Core constant 20 is taken as the SCORECARD states it (`:1551`); it cannot affect a ratio at 1.000 with queued = 0.
- Scratch (`$HYAKU_SCRATCH/kasegi-r45/R45CritAxisC2`: base copy, fixtures, freeze export, measure.py) removed on exit. No lane file was modified.
