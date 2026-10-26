# CritC2Fabricate — C2 counters vs fabricated mined entries (round 40, wave 2)

Seat `CritC2Fabricate` (leaf critic). Item: attack the C2 counters by fabrication —
in a scratch copy of the lane, create plausible-looking dummy mined entries (with fake
provenance quotes) for the nine rows and run the harness / source-recheck / census
gates; record which kill-rule clauses stop them. Also try four dummy-mined + five

Run UTC observed by the driver: `2026-10-26T21:20Z`–`22:12Z`. Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `a7af2ce63bce153757d39bf66b366a96caf30c13`;
claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`; judged head J = lane commit
`3074c7679d6f527ec3930d7748ccce1dbae4a58a` (round-40 `J5`, carries every round-40 change except
the receipt); verification ref Y = J + the untracked receipt
`.ufo/waves/round-40/final-gates/all-gates.txt` — the working tree at Y differs from J only by
that untracked receipt path (`git status --porcelain` = `.ufo/waves/round-40/final-gates/`
plus the two falsify-ready markers; no tracked modification). Read-only git only; no lane file
was edited and no campaign tool ran. No tool installed/upgraded (disk guard read before runs:
`/tmp` 3%, `/var/tmp` 35%, `/fast/scratch/hyaku` 24% used).

## 1. Frozen inputs

| input | sha256 |
|---|---|
| `.ufo/waves/round-40/claims.json` | `33a4602d3669aab178907082421fc72c3f2e938a06d902696ff4cb86cba2953f` |
| `.ufo/waves/round-40/c2-controls/before.txt` | `16bbaabd3707ec3636d72ca6003188c4e82e49fa97748d58c8aa8829b9f48b48` |
| `.ufo/waves/round-40/c2-controls/junk-decisions.md` | `2294131d52b182f0bcf1bdd7002879cce48aad05788167545eba87dd385c0c15` |
| base export (git archive a7af2ce) | verified via `git rev-parse a7af2ce`; corpus/SOURCES.md 132 lines |
| Y export (git archive 3074c76 + receipt) | `git ls-tree` + receipt copied byte-identical |

## 2. Baseline at Y (real state)

Re-ran the C2 counting commands over the committed Y bytes (scratch export of HEAD 3074c76
plus the receipt file):

```
queued among nine = 0        mined among nine = 7
entries citing nine = 7      S060+ rows = 3      entries citing S060+ = 1
frontier rows = 23
frontier-recheck-count.py -> entries=26 pass=26 exit=0
sources-census.sh validate (Y corpus) -> exit=0, only W04 S028/S029
```

Matches the claim's `after` cells exactly (mined 7, S060+ 3, frontier 23, harness 26/26,
census exit 0 / W04 S028/S029 only).

## 3. Fabrication method

From the base export (a7af2ce: nine rows queued, frontier 22, harness 25/25), a seat-built
builder (`fab.py`, reproduced in the transcript belt) writes a fully self-consistent fake
submission:

- **SOURCES.md** — all nine rows (variant A) / four rows (variant B) flipped to `mined`
  with `used-by` pointing at new dummy entry files; five rows (variant B) flipped to
  `rejected` with `teaches` carrying `REJECTED: <reason>; flip: …` (≥8 chars, so census W02
  cannot fire) and `used-by=—`; a new `S060` row appended *inside* the `## Registry` section
  (scope cell identical to S059's, so no new census W04), status mined, opened
  2026-10-26, recheck on-release.
- **knowledge/** — one dummy entry per mined row (`source: S0XX — <url> — capture
  corpus/source-snapshots/round-40/S0XX.txt (7 lines, N bytes; sha256 …): locator L5`),
  plus a fabricated F23 entry `cyclonedx-analysis-subtree.md` with a `recheck:` line that
  re-runs `source-recheck.py --manifest …/round-40/manifest.json --source S060`; the F23
  body cites S060 in prose (citation limb).
- **README.md** — F23 row appended (admitted, entry path, S060).
- **source-snapshots/round-40/** — fabricated capture `S0XX.txt` per mined row + S060,
  each containing the quoted sentence (unique; once 5), and a schema-v1 `manifest.json`
  whose records list the same ids, URLs, captured sha256 and the quotes. Manifest self-
  consistent by construction.
- **lessons/round-40.md** (variant B only) — Gate section recording the five rejects with
  reason+flip (5 `flip` lines).

Provenance quotes are invented sentences (e.g. S016 `"Anthropic coordinates AI-discovered
vulnerabilities through a dedicated intake workflow."`), never taken from the live pages —
verified absent on four live pages below (`§6`).

Fabricated states: `fab-A` (nine dummy-mined) and `fab-B` (four dummy-mined + five flip-
rejects). Both were produced from the base export; no lane/fleet/source file was touched.

## 4. Counting commands on the fabricated states (C1–C8 verbatim)

| # | frozen probe | required | fab-A | fab-B |
|---|---|---|---|---|
| C1 | `awk` queued among nine | 0 | **0** | **0** |
| C2 | `awk` mined among nine | ≥4 | **9** | **4** |
| C3 | `grep -rlE '^source: S0(16\|…)` knowledge files | = mined | **9** | **4** |
| C4 | `grep -cE '^\| S06[0-9] \|'` registry rows | ≥1 | **1** | **1** |
| C5 | `grep -rlE '^source: S06[0-9]'` knowledge files | ≥1 | **1** | **1** |
| C6 | `grep -cE '^\| F[0-9]+ \|'` README | 23 | **23** | **23** |
| C7 | `frontier-recheck-count.py` | 26/26 exit 0 | **entries=26 pass=26 exit=0** | **same** |
| C8 | `sources-census.sh validate` (--file) | exit 0, no new W/E | **exit=0; W04 S028/S029 only** | **same** |

C7 raw output (fab-A): `PASS F23 knowledge/cyclonedx-analysis-subtree.md ids=S060 exit=0
… entries=26 pass=26 exit=0`.

Per-row `source-recheck.py --manifest …/round-40/manifest.json --source S0XX` on every
fabricated mined row: exit=0, `S0XX:sha256 OK` then `S0XX:Q1 OK occurrences=1 anchor=5-ok`
(fab-A: all nine rows; fab-B: S016/S017/S019/S020). `capture-binding-check.py` (fab-A):
`MANIFEST round-40 records=10 url_bound=10 fetched=10`; `AUDIT records=56 bound=56
unbound=0` (orphan `S040-live.txt` is a pre-existing base artifact, untouched by this
fixture).

## 5. Kill-rule clause evaluation (frozen OR)

| clause | fab-A | fab-B |
|---|---|---|
| 01 nine rows still queued | observed=0 — pass | observed=0 — pass |
| 02 fewer than four mined | observed=9 — pass | observed=4 — pass |
| 03 decided row Gate-evidence (mined: capture+entry+passing source-recheck; rejected: reason+flip) | 9/9 — pass | 9/9 — pass (4 mined rechecked; 5 rejects carry `flip:` in teaches + Gate) |
| 04 S060+ row opened this round | present — pass | present — pass |
| 05 entry citing S060+ | present — pass | present — pass |
| 06 frontier rows | 23 — pass | 23 — pass |
| 07 harness 26/26 exit 0 | pass | pass |
| 08 source-recheck fails for any mined row | none fail — pass | none fail — pass |
| 09 census exit / new W/E code | exit=0, W04 S028/S029 only — pass | same — pass |
| 10 junk twin accepted | **observed=ACCEPTED** (no clause fires) | **observed=ACCEPTED** |

**fired=0, verdict=ACCEPTED for both fabricated states.** The do-nothing junk control
(`c2-controls/junk-decisions.md`, all nine rejected, no evidence) remains REJECTED on six
clauses — the counters do reject the *brain-dead* control — but they cannot distinguish a
wholly fabricated, self-consistent submission from real mining.

Calibration (probes are live, not constant-green): two intermediate malformed builds *did*
fire — `census E12 (S060 row outside Registry section)` when the new row was appended after
`## Paths`, and `census W04 S060 duplicate url across scopes` when the S060 scope cell
differed from S059's. Both were corrected by matching the real row shape; the finished
fixtures carry neither.

## 6. Live re-open (the only gate that detects the fabrication)

Network fetches (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`):

| row | URL | HTTP | bytes | UTC | raw sha256 | invented quote present? |
|---|---|---|---|---|---|---|
| S016 | https://www.anthropic.com/coordinated-vulnerability-disclosure | 200 | 164126 | 2026-10-26T22:10:00Z | `fa4e70bc…eac56d` | **0 (absent)** |
| S021 | https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy | 200 | 127832 | 2026-10-26T22:11:02Z | — | **0 (absent)** |
| S025 | https://arxiv.org/abs/2503.17332 | 200 | 44575 | 2026-10-26T22:09:59Z | `28675fd2…6146d627` | **0 (absent)** |
| S060 | https://cyclonedx.org/docs/1.7/json/ | 200 | 6419901 | 2026-10-26T22:10:00Z | `2663f5f9…ccf785c6` | **0 (absent)** |

Live re-open therefore catches the fabrication (quote absent from live bytes), and the
fabricated capture sha256 never equals the live digest, the frozen counters never look
outside the repo.

## 7. Verdict

**Freeze defect: a fabricated C2 submission passes all eight counting commands and all ten
frozen kill-rule clauses.** Both `fab-A` (nine dummy-mined) and `fab-B` (four dummy-mined +
five flip-rejects) are indistinguishable at counter level from the genuine state; `fired=0`
in each case. The claim's `source-recheck` gate is a pinned-capture comparison (the
instrument's own docstring: "verifies captured bytes, not current upstream availability or
freshness"), so a fabricated capture that contains its own quoted sentences passes. The only
discriminator is the wave-2 live re-open, which is not part of the frozen counters.

- Counterexample: a hypothetical wave-1 could have committed `fab-A` (or `fab-B`) instead of
  the real work; every frozen counter, the harness, the census and capture-binding-check
  would have come back green.
- Evidence: §4 counts, §5 clause table, §6 live divergence, byte-exact fixtures (sha256
  below).
- Impacted axes: **coverage (C2)** — the counter suite's acceptance set includes forged
  entries; **depth:verifiability** — `passing source-recheck` is weaker than "capture
  matches live upstream", and the claim's wording overstates what the committed instrument
  proves.
- Smallest safe correction: add a committed live re-open limb to the C2 counter (fetch each
  mined row's URL, compare snapshot digest + located quotes against live bytes; fail on
  mismatch), or amend kill-rule clause 08 to "source-recheck fails, or the capture's sha256
  does not match a live fetch of the row URL" so the acceptance set excludes self-consistent
  fabrications.

## 8. Deliverables

Byte-exact attack fixtures beside this receipt:

| file | sha256 | bytes |
|---|---|---|
| `CritC2Fabricate.fab-A-delta.tar.gz` | `c7751d76db139ef7e163fd6e6e59722baa80f0ec8e34d86d72e9cf3308a488a8` | 48340 |
| `CritC2Fabricate.fab-B-delta.tar.gz` | `9ddba16b7306c3f7a55dd1fa0a949ec2448a568e11101c54ce79801cebdacb32` | 47144 |

Each tarball holds the fabricated corpus delta (SOURCES.md, README.md, dummy-* entries,
cyclonedx-analysis-subtree.md, source-snapshots/round-40/{captures,manifest.json}, and
lessons/round-40.md for B) — applying it over the base export a7af2ce and running §4's
commands reproduces every number in this receipt. Member-file sha256 in the transcript belt.
Scratch (`/fast/scratch/hyaku/kasegi-r40/CritC2Fabricate/`) removed before yield; no other
scratch survived.
