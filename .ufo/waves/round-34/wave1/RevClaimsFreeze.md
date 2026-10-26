# RevClaimsFreeze — round 34 wave1 receipt

Seat: RevClaimsFreeze (reviewer, leaf of the L2 wave). Assignment: verify the claim freeze —
(a) claims.json at the freeze commit 29f606db hashes identically to the tip version; (b) the
predicate sentences in the wave context match claims.json; (c) every counting command in
claims.json is runnable and the after-values match the receipts; (d) the kill rules are the
same sentences as in the plan and the counter code. Report any divergence. This seat authored
none of the verified changes; every command below was run by this seat against the lane
working copy at /home/vgpnk/Projects/shokunin/kasegi-shokunin, outputs quoted verbatim.

## Report

### 0. Method and environment

- Read-only git plumbing only (`git show`, `git archive`, `sha256sum`); no `git
  add/commit/push`, no jj mutations, no writes outside this receipt and the scratch dir
  `/fast/scratch/hyaku/kasegi-r34/RevClaimsFreeze-2/` (deleted before yield — see §7).
- No tooling installed or upgraded (operator tooling authorization unused; nothing to record).
- **The wave was in flight for the whole verification window.** The C1 instruments changed
  under this seat at least three times (§6). Every value below is stamped with the instrument
  digest it was measured against; the final battery (§3) is the authoritative one.

### 1. Freeze identity — PASS

```
$ git show 29f606dbdd28aff6fd4573ab4b90788bbb90af13:.ufo/waves/round-34/claims.json | sha256sum
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  -
$ sha256sum .ufo/waves/round-34/claims.json
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json
$ git show 29f606db...:claims.json | wc -c ; wc -c claims.json
9004 / 9004
```

Byte-identical (digest + length). Independently corroborated by
`.ufo/waves/round-34/wave1/RevC2BeforeAfter.md` (same digest, quoted in its §Method).

### 2. Predicate sentences: wave context vs claims.json — faithful compression, not verbatim

The wave context (`wave1-spec.json` `.context`, identical to the dispatch prompt) carries
compressed C1/C2 bullets, not the claims.json predicate sentences. Token-level comparison of
every load-bearing fragment:

| fragment | in context | in claims.json predicate |
|---|---|---|
| `closed=9/9 exit=0` | yes | yes |
| `cases=9 failures=0` | yes | yes |
| `selftest cases=N failures=0` / `N>=19` | yes | yes |
| `survivors=0` | yes | yes |
| `entries=20 pass=20 exit=0` | yes | yes |
| `PASS F17 ids=S051` | yes | yes |
| `source: S051` / `opened 2026-10-26` / `16->17` | yes | yes |
| `<LANE_HASH>` | yes (C1 bullet) | **no** — lives in C1 `kill_rule` + `counting_commands` + after-list, not in the predicate sentence |

Differences found: (i) the context bullets are summaries (predicate + after-list merged),
not the verbatim predicate sentences; (ii) `<LANE_HASH>` placement as above; (iii) cosmetic
en-dash `R1–R9` (context) vs hyphen `R1-R9` (claims.json). **No semantic divergence**: every
quantitative token agrees; nothing in the context contradicts claims.json. Corroborating:
ScoutDatawalk.md F-5 found the context carries **no kill-rule text at all** — the kill rules
are authoritative in claims.json only (verified: `suite missing (ls_exit=2)`, `survivors>0`,
`frontier_admitted != 17`, `S051_row != 1`, `N<19 or any failure` each occur in exactly one
lane file, claims.json; the plan/spec/dispatch reference claims.json by path 66× and
operationalize the rules in seat tasks, e.g. "kill-rule-check.py -> survivors=0",
"grep -c '<LANE_HASH>' SCORECARD.md (0)", "selftest (cases=N>=19 failures=0)").

### 3. Counting commands — all 13 runnable; final battery at instrument digests
`r-defect-closure.sh=7aca98b3…`, `capture-binding-check.py=3d9e5e0d…`,
`kill-rule-check.py=e33a300f…`

C1 (6 commands):

| # | command (verbatim from claims.json) | measured output | exit | claim after | verdict |
|---|---|---|---|---|---|
| 1 | `bash corpus/instruments/r-defect-closure.sh` | `closed=9/9 exit=0` (R1–R9 all `open=0`) | 0 | `closed=9/9 exit=0` | MATCH |
| 2 | `bash corpus/instruments/r-defect-closure.sh --selftest` | `selftest cases=9 failures=0`, 9× `live=pass fixture=rejected verdict=pass` | 0 | `cases=9 failures=0` | MATCH |
| 3 | `python3 corpus/instruments/capture-binding-check.py --selftest` | `selftest cases=23 failures=0`; all 9 named after-cases present (`per-file-orphan-detected/listed`, `nested-snapshot-dir`, `fetched-utc-pending-rejected`, `fetched-utc-local-offset-rejected`, `dup-record-in-manifest`, `double-https-row`, `rejected-row-anchor`, `summary-only-selftest-rejected`) | 0 | `cases=N failures=0, N>=19` | MATCH (N=23) |
| 4 | `python3 corpus/instruments/kill-rule-check.py` | `mutants=3 killed=3 survivors=0 invalid=0`, `gates=6 failed=0`, `controls=4 rejected=4`, `survivors=0` | 0 | `survivors=0` | MATCH |
| 5 | `grep -c '<LANE_HASH>' SCORECARD.md` | `0` | 1 (grep no-match semantics; the claim specifies the count `-> 0`, which holds) | `0` | MATCH |
| 6 | `python3 corpus/instruments/capture-binding-check.py` | `records=41 bound=41 unbound=0` | 0 | `records=40 bound=40 unbound=0` | **DIVERGENCE — disclosed, see D-1** |

C2 (7 commands):

| # | command | measured | exit | claim after | verdict |
|---|---|---|---|---|---|
| 7 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `17` | 0 | `17` | MATCH |
| 8 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `51` | 0 | `51` | MATCH |
| 9 | `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `1` | 0 | `1` | MATCH |
| 10 | `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `1` (`immunefi-vscs-v2-2-smart-contract-severity.md`) | 0 | `1` | MATCH |
| 11 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0`, incl. `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0` | 0 | `entries=20 pass=20 exit=0` | MATCH (note E-3 on the literal) |
| 12 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | `S051:sha256 OK`; 18 assertion lines all `OK`; **Q9 and Q17 print `occurrences=2 anchor=…-ok`**, the other 16 print `occurrences=1` | 0 | `every assertion occurrences=1, sha256 OK, exit 0` | **DIVERGENCE — undisclosed, see D-2** |
| 13 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028 …`, `W04 S029 …`, `ok …/corpus/SOURCES.md` | 0 | `exit 0 (W04 S028/S029 only)` | MATCH |

Base-tree behavior (C1 predicate clause "the suite fails on the base tree, `closed=0/9`"):
`git archive 014ee2d7…` extraction → `bash corpus/instruments/r-defect-closure.sh --root
<base>` → `closed=0/9 exit=1` ✓; `ls <base>/corpus/instruments/r-defect-closure.sh` →
`ls_exit=2` ✓ (before-list). Freeze-tree extraction (29f606db): suite → `closed=0/9 exit=1`;
`capture-binding-check.py` → `records=40 bound=40 unbound=0` exit 0 — **the frozen literal 40
was true at the freeze commit**; the 41 arrived with the post-freeze C2 round-34 manifest.

### 4. After-values vs receipts

- ExecCaptureBindingHarden.md: `selftest cases=23 failures=0` (×2, byte-identical runs) —
  matches my #3. It also documents the records=40→41 drift (§3: "`records=40 bound=40
  unbound=0 exit=0` cannot be the C1 target any more — the tree measures `records=41`") and
  the honest target `records=41 bound=41 unbound=0` — matches my #6.
- ExecRegistryAppend.md:162: "S051:Q1..Q18 OK (each occurrences=1 or anchor-ok; … Q9/Q17
  occurrences=2 anchored)" — the receipt records the occurrences=2 honestly; matches my #12
  and contradicts the frozen predicate's "every assertion occurrences=1" (D-2).
- ExecBeforeReceipts.md: base battery `records=40 bound=40 unbound=0`, `<LANE_HASH>` count 2 —
  matches claims before-list.
- Frozen before-controls `.ufo/waves/round-34/{c1-controls,c2-controls}/before.txt` and
  `census-before.txt`: every line matches the claims.json before-lists (ls_exit=2; selftest
  cases=11; both survivor-mutant descriptions; `<LANE_HASH>`=2; S049/S050
  `2026-10-25T23:14:00-03:00`; round-26 `records= 1 paths= ['S041.txt']`; R20 'exactly one'=1;
  frontier 16; registry 50; S051 0; entries-citing 0; harness 19/19; recheck
  `manifest UNAVAILABLE reason=missing` exit 2; knowledge 45; census W04 lines). One nuance
  already flagged by ScoutDatawalk F-3: the before-control line "round-33 lesson erratum
  present? 4" counts pre-existing capital-E `Erratum` lines, not an R7-specific marker —
  non-discriminating as a before-control, though the after-gate (check_r7's
  19→31/23→22/S050.txt:70 text) is specific.
- S051 row (`corpus/SOURCES.md`): tier `A`, status `mined`, date column `2026-10-26`, 90d,
  knowledge path — matches "row S051, tier A, status mined, opened 2026-10-26". Capture
  `corpus/source-snapshots/round-34/S051.txt` sha256
  `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` — matches the row text.
- Knowledge entries: `ls corpus/knowledge/*.md | wc -l` → 46 (claim after 46; before 45) ✓.

### 5. Kill rules vs counter code — clause-level check

C1 kill_rule (9 clauses) vs the landed counters — every clause is enforced behaviorally:

| clause | enforced by | verified |
|---|---|---|
| suite missing (ls_exit=2) | before-control records ls_exit=2 at base | §3 base check ✓ |
| `closed` != 9/9 | `run_plain` exits 0 iff K=9 | base `closed=0/9 exit=1`; tip `9/9 exit=0` ✓ |
| selftest <9 cases or any failure | `run_selftest` counts cases/failures, exit 0 iff failures=0 | tip `cases=9 failures=0 exit=0` ✓ |
| capture-binding selftest N<19 or any failure | `kill-rule-check.py` `floor=19 floor_met=1` (CASE_FLOOR) + capture-binding's own selftest | tip N=23 failures=0 ✓ |
| kill-rule-check prints survivors>0 | counter exits 0 iff survivors=0 ∧ no invalid ∧ gates hold | tip `survivors=0` + `CTL-equivalent` witness proves it can report survivors>0 (`witness_survivors=1 witness_exit=1`) ✓ |
| any single R-check exits 0 on a defect-bearing tree | suite's own --selftest broken-fixture runs | all 9 fixtures `rejected` ✓ |
| `<LANE_HASH>` still present | check_r1 | tip count 0 ✓ |
| round-32 manifest non-UTC fetched_utc | check_r8 (`^[0-9]{4}-…Z$`, no offset) | `strict-utc-ok=2` ✓ |
| S040-live.txt no record/orphan listing | check_r6 | open=0; AUDIT `orphans=1 orphan=S040-live.txt` (orphan-listing path) ✓ |

Coverage nuance (echoing ScoutDatawalk F-4c): the C1 kill_rule has no *direct* literal clause
for erratum 2 (R2), the QUALITY R20 note (R3), the R7 erratum, rule-A bidirectionality or the
junk twin's existence — those nine defects are covered *indirectly* through the suite clauses
(`closed` != 9/9 and the selftest), which is sound but worth knowing when reading the kill
rule alone.

C2 kill_rule (8 clauses): frontier 17 / rows 51 / S051 row 1 / citing 1 / harness 20-20 /
recheck exit 0 / census exit 0 all measured ✓ (§3). The eighth clause — "junk twin passes
source-recheck or is admitted" — **has no executable form as phrased** (ScoutDatawalk F-1,
corroborated): `source-recheck.py` takes `--manifest … --source S051`, never a markdown file;
the twin's `recheck:` line is byte-identical to the real entry's, so both exit 0 at tip, and
at before both exit 2 — the clause cannot discriminate. The rejection actually holds through
the reviewer limb (ExecHarnessAfter.md §: `RevEntryF17`'s per-quote grep against S051.txt +
non-admission to the frontier table) and the twin's own `[FABRICATED …]` label; note also
ScoutDatawalk F-1b: the twin's quoted sentence is NOT fabricated — `S051.txt:75` really
contains "Direct theft of any user funds", so even a quote check would pass it. `r-defect-
closure.sh` R9 only tests that the twin file EXISTS. No counter code contradicts the *other*
kill-rule clauses; the frozen sentence and the executable reality disagree only on this clause.

### 6. Divergences (the report's core)

- **D-1 (disclosed) — C1 counting literal `records=40 bound=40` is stale at tip.** Measured
  `records=41 bound=41 unbound=0 exit=0` (the post-freeze C2 round-34 manifest adds S051).
  Disclosed and ruled by the L1's `.ufo/waves/round-34/claims-erratum-1.md` (filed
  pre-integration): the literal 40 is a round-33 scope note; the invariant is
  `bound=records, unbound=0, exit 0`; ruled after-state `records=41 bound=41 unbound=0
  exit=0` — my measurement matches the ruled after-state exactly, and the frozen literal was
  true at the freeze tree (§3). No action needed beyond the erratum's own disclosure
  requirement ("disclosed on every surface that reads the C1 counter" — spot-checked present
  in ExecCaptureBindingHarden.md §3).
- **D-2 (undisclosed) — C2 predicate "source-recheck S051 prints every assertion
  occurrences=1" is false at tip.** Measured: 16 assertions `occurrences=1`, **Q9 and Q17
  `occurrences=2`** (both `OK`, anchor-verified `anchor=77-ok`/`anchor=96-ok` — the
  instrument's legitimate anchored path for twice-occurring quotes), `sha256 OK`, exit 0.
  The kill rule is unaffected (it keys on exit != 0, which holds), but the predicate sentence
  overstates the output — the same summarization-beyond-measured-evidence class the round
  itself files as M34-1. Receipts record it honestly (ExecRegistryAppend.md:162; 
  RevC2BeforeAfter.md counter 6; ScoutDatawalk F-2 recommends an appended note). **Recommended
  correction: an appended claims erratum rewording the clause to "every assertion OK
  (occurrences=1, or occurrences=2 with a verified anchor for Q9/Q17), sha256 OK, exit 0."**
  Claims are frozen; the correction lands as a separate appended file per the round rules.
- **D-3 (wording, no semantic conflict) — kill-rule sentences are not quoted anywhere
  outside claims.json.** The plan/spec/dispatch carry the rules operationally (seat-task
  sentences), the counter code enforces them behaviorally; no contradiction found (§5), but
  "the same sentences" is only true of claims.json itself. If the L1 wants a second verbatim
  copy, the natural home is the round-34 lesson or an appended erratum.
- **D-4 (mid-wave instrument churn — resolved, recorded for the L1).** During this seat's
  window the C1 suite changed at least three times: an earlier version's `--selftest` ran
  each "live" check against the *previous case's fixture root* (stale global `RD_ROOT`), so
  7/9 cases reported `live=open` with per-case fixture-state problems (e.g. R5
  `url-matching-two-rows … count=1`, R8 `non-strict-utc=S049:…-03:00,S050:…-03:00`) and the
  run crashed post-summary with `r-defect-closure.sh: line 1: scratch: unbound variable`
  (EXIT trap expanding a now-local `$scratch` under `set -u`); the same tree measured
  `closed=7/9`→`8/9`→`9/9` as sibling seats landed R7/R4. Current bytes
  (`7aca98b3…`) capture `live_root=$RD_ROOT` before the loop and expand the scratch path into
  the trap string — both defects fixed and re-verified (§3 battery). `kill-rule-check.py`
  also churned (`e1737783…` → `1af15e59…` → `e33a300f…`); `capture-binding-check.py` was
  stable at `3d9e5e0d…` across every run. Consequence for the freeze: any counting-command
  value measured before quiescence is against moving bytes; the §3 battery is this seat's
  authoritative measurement, and the headline values were stable across the last two
  instrument versions.
- **D-5 (observation) — `PASS F17 ids=S051` is not a grep-able literal** (ScoutDatawalk F-4a,
  corroborated): the harness prints aligned columns
  `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0`;
  `grep -c 'PASS F17 ids=S051'` = 0. The claims' after-list uses the ellipsis form
  (`PASS F17 ... ids=S051`) and is accurate as a description; only a literal-grep reading
  fails.

Non-claim frontier items spot-check: assimilation guard prep landed
(`.ufo/waves/round-34/assimilation/{collisions,guard-proof.txt,quarantine-slice,reg-ids,staged-ids,scratch-registry.md}`); the "Assimilation: none … verdicts recorded in the lesson Gate"
step is pending — `corpus/lessons/round-34.md` does not exist yet (scribe seats still
waiting). considerthese proposal 6 → QUALITY.md R23 landed (cites
`considerthese/2026-10-25.md:76`). M34-1 → QUALITY R24 grounding; M34-2 → QUALITY R22
grounding; both rows present.

### 7. Scratch and hygiene

- Scratch root `/fast/scratch/hyaku/kasegi-r34/RevClaimsFreeze-2/` (base/freeze `git archive`
  extractions, selftest scratch, traces). Deleted before yield via `rm -rf --` (verified
  absent post-deletion). No files left on disk — no defect to report on that ground.
- No writes outside the lane write scope; no subagents spawned; no `agent://all`; no campaign
  tools from shokuknow run; the census script was run exactly as claims.json specifies
  (read-only validate mode).

### File digests (sha256, at receipt-write time)

```
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json
6a3cd99e4dc9411293d9fa7b9cb3bb00473598b63ba31359be8c66c88f6bd1bd  .ufo/waves/round-34/claims-erratum-1.md
7aca98b344d4ca8718344cc09c63b67b2382fd327d579e6b6a2c713b351e08ab  corpus/instruments/r-defect-closure.sh
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
e33a300fc7341f8d6e254fc12441de1ba0ec6252483aeaf6e8806622dba0fc15  corpus/instruments/kill-rule-check.py
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
```

### Verdict (recommendation to the L1; this seat does not judge the round)

The freeze itself is sound: claims.json is byte-identical at freeze and tip; the wave-context
predicates are faithful compressions with every quantitative token matching; all 13 counting
commands are runnable; 11 of 13 after-values match the receipts and the live tree exactly,
and the two that do not are (D-1) disclosed and ruled by claims-erratum-1.md, and (D-2) a
one-clause overstatement ("every assertion occurrences=1" vs Q9/Q17 occurrences=2) that
deserves an appended claims erratum before scoring. Kill rules are enforced by the counter
code with one clause (junk-twin "source-recheck exit != 0") having no executable form — the
rejection holds through the reviewer limb instead. Residual risk: the instruments were
churning during the window; the L1 should re-run the §3 battery once the wave quiesces and
confirm `closed=9/9`, `cases=9 failures=0`, `survivors=0` on the committed bytes it scores.
