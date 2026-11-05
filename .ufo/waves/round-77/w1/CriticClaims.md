# CriticClaims — round-77 w1 — falsify the two frozen claims as claims

Seat: CriticClaims (leaf, critic). Scope: claim shape, do-nothing control adequacy, §9 sizing,
freeze-before-data, sourced-claim duty. The frozen code is attacked by ReviewC1/ReviewC2/MutC1;
this report attacks the claims. Freeze commit `539a43877809bd90b6f506e8fd24a6d871598cd5`
(HEAD at review time; parent = base `2e53fc74776824898b5c5eb914aeddc19a091157`, verified
`git rev-parse`). All findings are routed defects — nothing was edited, no predicate rewritten.

Method: read-only git (`show|log|rev-parse|ls-tree|diff|status`) over the lane; live re-runs of
the committed controls in scratch `TMPDIR=/fast/scratch/hyaku/kasegi-r77/CriticClaims`; no tool
installed or upgraded (none needed — pacman untouched). Scratch removed before yield.

## Findings

### F1 — MAJOR — C1's A2 binds two trees; the wave spec lands one commit
`claims.json` C1 `predicate.A2`: primary literal `entries=91 … exit0_foreign=69 …` "on the
amended bytes **at the C1-landing tree** … byte-identical to the base receipt", drift limb
"per R124 **once C2 lands at the final tree**: entries=92, exit0_foreign=70". `kill_rule`:
"Any of A1-A6 false **at the landing commit** = claim fails". The wave spec
(`w1-spec.json` context) says the L1 "applies every change, lands **and commits** through the
helper after WAVE-DONE" — singular. If the helper produces one landing commit carrying both the
amended counter and C2's knowledge file, no commit exists where the amended counter prints
`entries=91/exit0_foreign=69`: A2's primary is false at the only landing commit and the frozen
kill rule fires — C1 fails by its own text with correct work. Precedent is in-lane: round-73's
C1 held on the C1-only tree but its clause was falsified on the merged tree
(`entries=89 exit0_foreign=67`, SCORECARD round-73 section) and routed. QUALITY R124 ("an exact
baseline value and a population drift cannot both bind one tree") and R111 ("a claim's
after-state lands in ONE commit, or the report names the commit that carries each counter's
value") govern. The coupling inside A2 is honest R124 machinery; the hidden conjunction risk is
purely the landing mechanics.
**Smallest safe correction (process, not bytes):** the L1 lands C1 first (amended counter +
SKILL.md/corpus/instruments/README.md pin moves) as its own commit, re-measures A1–A3 there,
then lands C2; the report names the commit carrying each counter value (R111/R121). If the
helper cannot stage two commits, this escalates to a BLOCKER at integration time (unsatisfiable
freeze as written). No predicate text is rewritten.

### F2 — MAJOR — the freeze record's `frozen_at` postdates its containing commit (R44 class)
`claims.json:4` declares `"frozen_at": "2026-11-05T12:45:00Z"`. The containing commit's stamps:
author `2026-11-05T09:07:37-03:00` (= 12:07:37Z), committer `2026-11-05T09:35:02-03:00`
(= 12:35:02Z). The label is a **+9m58s future label against the committer stamp**. QUALITY R44
mints exactly this defect: "a label later than its own containing commit (the r43 mine:
round-42 `claims.json` `frozen_at_utc` … a 65-minute future label) reads as no freeze record —
K19 at base prints `K19 payload=freeze=absent,order=bad,sha=mismatch`". Corroborating provenance
split: the capture's `fetched_utc` is `2026-11-05T12:22:10Z` (manifest S112 record), which also
postdates the author date — the commit was authored before its own capture existed and was
recommitted at 12:35:02Z; the freeze label was then written ten minutes after that.
**Smallest safe correction:** none post-freeze (append-only; the bytes stay frozen and no
predicate reads the label). The round lesson records the process miss per the R80 pattern
("report the process miss rather than silently calling it conformant"). Rated MAJOR, not
BLOCKER: zero frozen-byte drift (see V4) and no predicate depends on the label.

### F3 — NOTE — the frozen anchor-set names S112.txt:194, where no quote anchors
`claims.json` C2 B6 and `located_anchors` list "S112.txt lines 24, 30, 31, 34, 35, 36, 166, 168,
169, 170, **194** and 195 (manifest Q01-Q13)". The 13 manifest quotes anchor at
{24×3, 30, 31, 34, 35, 36, 166, 168, 169, 170, 195} — 11 distinct lines, **194 unused**
(manifest Q09–Q13; `controls/c2-prerecheck-r77.txt`; my re-run below). `S112.txt:194` is real
batch ground — "Notice that each result has a distinct next_page_token and that the third result
does not include a next_page_token. …" — but carries no frozen quote. Consequence: an entry
clause cited at 194 is unpinnable (Q3 needs a verbatim quote; B0 forbids adding quotes "after
any seat has scored"); a verifier re-deriving the frozen anchor set trips on the stale literal
(R22/R25 pre-freeze-satisfiability class — the literal should have been run against the capture
before the freeze).
**Smallest safe correction:** the F54 entry cites only the 13 pinned anchors; the round lesson
records line 194 as a stale anchor-set line. Predicate bytes stay frozen.

### F4 — NOTE — control-receipt composition vs R37/R39, with a demonstrated ambiguity cost
(a) `controls/c1-base-realtree-census-r77.txt` is two bare stdout lines — no command, no lane
value, no rc — unlike its siblings (`c1-donothing-selftest-r77.txt` carries `# command:` /
`# rc=` headers). (b) `controls/c2-prerecheck-r77.txt` opens with two hand-written comment lines
and carries no run-utc (R37: "its `run-utc` is printed by the run itself"). (c)
`controls/c2-base-counters-r77.txt` is a composed multi-window annotated transcript (`-> value`
lines), not one run's tee (R39's letter). Under R37/R39 strictly these are not clean receipts;
the house style has used this shape across r74–r77, so this is a standards note, not a blocker.
The ambiguity has a demonstrated cost: A2's placeholder command `--root <lane> --lane <lane>`
plus the bare receipt let this seat substitute the lane NAME (`--lane kasegi`) for the lane
root on first run — `recheck-cwd-census.py:85` builds the expected prefix from the `--lane`
value (`prefix = "cd %s && " % lane`; `:100` `noprefix = not value.startswith(prefix)`), so the
run read `noprefix=91 … RESULT nonconformant` rc=1, a **false red** against the committed
receipt. The corrected invocation (below) reproduces the receipt byte-identically.
**Smallest safe correction:** future instruments print their own header lines (command, lane
value, run-utc) so receipts carry their invocation; this freeze's receipts stay as committed.

## Verification results (attacks that did NOT land)

### V1 — claim shape: exactly 2 causally-separable claims on distinct axes — HOLDS
- Exactly 2 claims (`claims.json` C1, C2); dispatch declares 13 seats (`w1-dispatch.json`
  `counts.spawn=13`).
- Axis levels verified from SCORECARD's latest (round-76) table: "depth:verifiability, lowest |
  … | 4 -> 4 nominal R58"; coverage "8 -> 8"; depth:density 9 (not targeted, not lower). So
  depth:verifiability 4 IS the lowest non-retired axis and coverage 8 matches the claim
  labels; C1's `axis_score` carries the R58 nominal disclosure ("the scored resolve.py census
  is not read by this counter").
- Separability: C1's predicates touch only the instrument, the r76 wave file (A4), and the
  registry pins; C2's (B0–B7) never read `recheck-cwd-census.py`. C1 lands without C2 (drift
  limb dormant) and C2 without C1 — modulo F1's landing mechanics.
- Registry pins are truthful: `grep 'selftest cases=6'` hits SKILL.md:982 and
  corpus/instruments/README.md:354, so the R113 same-commit pin move is real work.
- Digests reproduce: reference `18bfc439…88a33` ✓, S112.txt `f3ca0465…0907` ✓ (manifest pin),
  base counter `e666ae11…a21a` ✓ (= working-tree bytes; the amendment is correctly not yet
  applied).
- The five committed mutant receipts match the frozen transform table exactly:
  m1 `gate-regs FAIL registered=[]` + two `no-registration` FAILs, no traceback; m2
  `gate-consume ok clean_ok=True` + `gate-negpolarity FAIL neg_ok=True` (THE required m2b-class
  kill, assertion not NameError — R127-compliant); m3 `gate-consume FAIL
  exception=NameError("name 'out6' is not defined")` logged as the exception class, distinct
  from assertion kills; m4 `gate-negpolarity FAIL neg_ok=False`; m5
  `gate-checkids FAIL missing=['both-headers']`, `cases=11 failures=1`.

### V2 — do-nothing control adequacy: no after-counter reachable without the work — HOLDS
Every after-state is base+work: C1 A1 wants `cases=12` vs base `cases=6`; C2 wants rows
111→112, knowledge 91→92, expected 93/91→94/92, frontier rows 53→54, registry 111→112, entries
56→57, records 90→91 (all measured at base in `controls/c2-base-counters-r77.txt`). B7's
pre-round id check verified: `git show 2e53fc74:corpus/SOURCES.md | grep -c 'S112'` → 0.
Live reproductions (my runs, scratch TMPDIR):
- Base selftest: `selftest cases=6 failures=0`, rc=0 — matches the do-nothing receipt.
- Red-before: `.ufo/waves/round-76/controls/m2b-conjunct-removed.py --selftest` →
  `selftest cases=8 failures=0`, rc=0 — the m2b survivor class is still alive on the prior
  design, so the gate delta is real (A4 stands).
- B0/B5: `python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-77/manifest.json --source S112` → `S112:sha256 OK` + 13×
  `OK occurrences=1 anchor=<n>-ok`, rc=0.
- Real-tree census on base bytes (corrected invocation, lane root as `--lane`):
  `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22
  exit_other=0 norecheck=0 restoration_only=0` + `RECHECK-CWD-RESULT conformant`, rc=0 —
  byte-identical to `controls/c1-base-realtree-census-r77.txt`. (First run with
  `--lane kasegi` printed a false nonconformant — see F4; the false run is disclosed, not
  filed as a finding against the counter.)

### V3 — §9 sizing: no universal clause without an enumerator; one-round size — HOLDS
The §9 rule (operator goal addendum: `.scratch/goal-20261022-hyaku-12h.md:152-154`,
`goal-20261023-hyaku-24h.md:142-146`: "Use no universal clauses ('all', 'complete', 'every',
'no harm anywhere') unless the counting command enumerates the full set"; "Size it to what one
round can land and verify"; claims "a do-nothing control cannot reach"). Every after-state is
one-command re-derivable: A1 selftest run; A2 census run + named receipt + named drift
expectation; A3 five named mutant runs with kill classes; A4 one run over committed r76 bytes;
A6 git diff over five named functions; B0/B5 source-recheck command; B1 git diff; B2 three
counters + `sort -c`; B3/B4 instrument runs; B7 sources-census + grep. Targets match landed
precedent (r74: 5-case amendment; r75: 6-case; F51–F53 admissions), so 12 checks + gate + one
admission is one-round sized, not padded. Borderline, compliant-in-spirit: A5's exec-surface
universal ("no file outside mkdtemp honoring TMPDIR") names no counting command inside the
predicate — it is enumerable over 371 lines and SentinelC1's audit covers it this wave.

### V4 — freeze-before-data: bytes clean, order intact — HOLDS (residue F2)
All frozen paths are in `539a4387`'s tree (23-file commit listing: claims.json, reference,
transforms, 16 controls incl. the five mutants + outs, SOURCES.md +1 line, S112.txt,
manifest.json). `git diff 539a4387..HEAD --stat` is EMPTY (HEAD == freeze — no post-freeze
committed drift). `git status --porcelain` over the frozen paths is clean (only untracked
wave dispatch/spec/ready/w1 files, created after the freeze). Base field = freeze's parent
(`git rev-parse 539a4387^` = `2e53fc74…`). The B0 receipt is committed inside the freeze
commit, so it predates any seat scoring. C2's receipts carry the R121 two-state discipline
(base window + freeze-tree transitional block: rows=112, records=91 bound=91, frontier
unchanged 53/56). The working-tree SOURCES.md S112 row reads `… | queued | 2026-11-05 | 180d
| — |` — status queued as B1 states; the freeze diff adds exactly one line.

### V5 — sourced claim: C2's S112 duty satisfied; C1 correctly needs no row — HOLDS (residue F3)
S112 row opened 2026-11-05 this round (row cell), capture `fetched_utc 2026-11-05T12:22:10Z`,
manifest R20/R21 fields complete (url exactly matching the registry row URL, sha256, method
disclosed: "capture-source.py --kind html, default instrument UA …", byte-identical across two
fetches noted in the row). R126 pre-freeze recheck: receipt committed in the freeze commit and
reproduced live (13× `occurrences=1`, rc=0). Distinctness (R114 subject sweep + R125) checked
independently: `grep querybatch|next_page_token` over `corpus/knowledge/` hits only
`osv-post-v1-query-contract.md`, whose line 75 lists POST /v1/querybatch as "listed, not
described" — exactly the F51 handoff the claim names. The overlaps my sweep did find (version
rule content at `osv-post-v1-query-contract.md:21-23` = S108.txt:40-41; single-query pagination
basics at `:45-51`) are precisely the clauses B6 excludes as already-held-and-not-claimed, so
the frozen exclusion list matches the observed held ground. C1 is instrument work and needs no
source row (Q2 governs corpus/knowledge entries).

## Verdicts — the most likely way each claim FAILS at integration

- **C1:** F1. With the spec's single-commit landing language, A2's primary literal
  (`entries=91/exit0_foreign=69`) is false at the landing commit and the frozen kill rule fires
  — C1 reads NOT VERIFIED with correct work (r73 merged-tree precedent). Avoided only by
  landing C1 first as its own commit (or by naming per-commit trees per R111/R121). Secondary:
  the integration re-run of K-M2 must show the assertion kill (`gate-negpolarity FAIL`) — the
  committed receipt does; a NameError-only kill does not count (R127).
- **C2:** exact-absolute counters (B2/B3/B4: 112 / 94-92 / rows=54 admitted=54 registry=112 /
  entries=57 / records=91) break if the landing commit carries any unaccounted sibling tree
  change (e.g. an S111 flip or a second knowledge file) — R121's revision-naming must cover
  every value's tree. Plus F3: an entry clause cited at S112.txt:194 (or any line outside the
  13 pinned anchors) is unpinnable, because no quote may be added after seats have scored.

Report: .ufo/waves/round-77/w1/CriticClaims.md
