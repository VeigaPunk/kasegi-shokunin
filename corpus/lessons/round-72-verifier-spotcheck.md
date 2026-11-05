# kasegi round 72 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Round under review: kasegi lane-round 72, base `87d84a28b5a0711230d723e4eda423790e081212`,
tip `8782f727d90d4e99f7d4cc990310ed44d65ac027`. Report `.ufo/reports/round-72/kasegi.md`
(fleet commit `3b32a990ca0944ac815dd90c62f08b4ea5ec3715`, author `kasegi-shokunin`).
Dispatch/complete digest (copied into the closure notes):
`2026-11-05T00:43:02-03:00 launch kasegi round=72 pgid=1743267 driver=hyaku-inline attempt=1`;
`2026-11-05T01:56:42-03:00 complete kasegi round=72; hyaku-inline attempt=1`.

## 1. Step-1 conformance

- Report committed by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-72/kasegi.md`
  → `kasegi-shokunin 3b32a990…`; `## SHONEN` heading present (`grep -c '^## SHONEN'` → 1) with one
  `[~]`/`[ ]` line per box, no `[x]`.
- Cited lane commits: `a34ce4c`, `123796a9e05c8a5666073c2dc28c1f56cb25b2ac`,
  `dd9f55e70772760d8ec9cb60d1e0057ba1f49c29`, `9869931aa5c70238af4b24295428d31869d20d23`,
  `50b85212c04f10a6dd56edd9cebe123a73ea941e`, `8782f727d90d4e99f7d4cc990310ed44d65ac027` — all exist
  and `git merge-base --is-ancestor <hash> master` holds for each (master = `8782f727`).
- Lane state: `scripts/hyaku/jj-lane.sh state` → `ahead=0 behind=0`, local = remote = `8782f727`;
  `git status --porcelain` empty. No uncommitted round work; pushed.
- Prompt `.ufo/prompts/kasegi-round-72.md` renders `templates/round-prompt.md` §1–§5 verbatim plus the
  §6 hyaku addendum (all round-level items and the five child-lane items present: report path,
  commit-before-report, SHONEN heading, hash-citation rule, write scope at line 448).
- Round commits `a34ce4c`…`8782f72` (7 commits) all authored `kasegi-shokunin <kasegi@shokunin.local>`;
  diff touches only lane files and `.ufo/waves/round-72/` — no `.ufo/state/` or `watchdog.log` bytes.
- Not a marker: real committed work, evidence pointers, resolvable hashes.

## 2. Claim re-checks (re-measured by me over committed bytes at `8782f727`)

### C1 — `depth:verifiability` — frozen predicate re-derived; universal sentence weakened

Method: executed the lane's committed census counter `corpus/instruments/derive-head-census.py`
(sha256 `255fd407…`, unchanged since `a34ce4c`) against the tip tree with a private `TMPDIR`:

```
CENSUS heads=45 write_class_pairs=5 READMITTED=0
ALIAS-PROBE verdict=refused rc=2 FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
POSITIVE admitted=2/2
CENSUS-RESULT ok
EXIT=0
```

Byte-identical verdict to `controls/c1-census-final-r72.txt`. Base side: `git show a34ce4c:…/figure-audit.py`
sha256 = `182f4ef7…` and `git show 8782f72:…/figure-audit.py` sha256 = `4f59bda4…`, both matching the
committed receipts; the do-nothing receipt `controls/c1-census-donothing-r72.txt` records
`READMITTED=19` / `ALIAS-PROBE admitted rc=1` / `CENSUS-RESULT defect` exit 1 on the base gate.

Gate diff re-read (`87d84a2..8782f72 -- corpus/instruments/figure-audit.py`): `PY_DENIED_ANY` gains
`--work`,`--scratch`; `python_head_ok` keys the policy on `basename(realpath(target))` before flag
policing; `derive-head-census.py` joins `PY_SCRIPT_CENSUS`; `EXPECTED_CASES` 106 → 110 with four new
`python-work/scratch` selftest cases; mutbat m7/m9 anchors repointed to the new containment `if`.
`SKILL.md` gate row pin updated to `selftest cases=110`. Committed evidence verified, not executed:
`controls/c1-selftest-final-r72.txt` (`cases=110 failures=0`), `controls/c1-mutbat-final-r72.txt`
(`killed=5/5 survivors=0 invalid=0 controls=pass`), `controls/c1-census-kill-matrix-r72.txt` (4/4
killed), `controls/parity-final-r72.txt` (247 identical / 0 different / 0 regressions over committed
ledgers). The census counter itself was executed (it is a plain measurement instrument, not the gate
under test); the gate selftest/mutbat/battery were evidence-verified per §Gate standard.

Weakenings confirmed from committed bytes and seat reports (not re-executed): the universal sentence
"every write-class option a head declares" is falsified off-tree — the census reads `add_argument`
literals only (`K72Falsify` n7, `K72AttackCensus` §2 confirms no manual argv parsing in shipped heads);
kill clauses "prints exactly"/"at the measured commit" are weakened (L72-5); `--json`/`--root` sit
outside `WRITE_CLASS` (R-1); `probes()` copies from `dirname(--gate)` not the `--gate` file (L72-11,
routed). R-5 realpath semantics admitted a non-census name resolving to a census head — documented,
flags still policed.

### C2 — `coverage` — counters re-derived; declared target falsified in one clause

Re-measured by me over committed bytes at the tip (plain counters, no lane gate):

```
FRONTIER-CENSUS rows=50 admitted=50 closed=50 problem-rows=0 registry=107
FRONTIER-PASS F50 ids=S107 … entries=53 pass=53 exit=0
capture-binding-check: records=86 bound=86 unbound=0 exit=0
knowledge-expected.txt: 90 lines / 88 non-comment rows, LC_ALL=C sort -c clean; 88 corpus/knowledge/*.md files
SOURCES.md registry rows: 107; malformed-row awk count: 0
source-recheck.py --manifest …/round-72/manifest.json --source S107 → sha256 OK, Q01–Q17 all anchor-ok
sources-census.sh validate --root … kasegi → exit 0 (six inherited W04 duplicate-url warnings, unchanged)
```

Before-side receipts `controls/c2-base-counters-r72.txt` (rows=49 registry=106 entries=52 capture=85
knowledge=89/87) are consistent with the round-71 closure's own re-measurement.

Falsification confirmed: `grep -n -i 'api_key\|api key\|authentication\|secur'` on the committed capture
`corpus/source-snapshots/round-72/S107.txt` (sha256 `0b944ea1…`, 1176 lines — matches the manifest and
the S107 row) returns nothing; the only token sentence is the per-bug `update_token` (S107.txt:297).
The frozen target's `api_key` clause is not grounded in S107 — the lane's NOT VERIFIED AS DECLARED
ruling is correct, and the dated amendment `.ufo/waves/round-72/claims-amendment-c2.json` preserves
the frozen text and records the narrowed target for the operator. The entry
`corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` honestly records both absences in its Limits
section; every manifest quote re-verified at its anchor.

### Owned axes harmed?

`git diff 87d84a2 8782f72 -- SCORECARD.md` adds the round-72 section only (score table, verdicts,
late-seat and parent-ruling amendments, move log, planned). No prior score row was lowered; C1
reverses the round-71 measured harm (READMITTED 19 → 0, alias refused) with parity 247/247 identical
and kill matrix 4/4. `depth:density` is not an owned axis of this lane and was not a claim target.
No axis regressed.

## 3. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S107 Bugzilla REST API core v1 bug endpoints | admit (tier A, mined) | committed capture `S107.txt` + manifest Q01–Q17 via `source-recheck.py`; Gate located quote "The REST API for creating, changing, and getting the details of bugs." | **agree** | quote verbatim at `S107.txt:33` (13 words ≤25); all 17 pinned quotes re-verify at their anchors; first-party API reference for its own contract → tier A correct; entry's Limits honestly record the absent api_key/security-group rules rather than inventing them |
| S104 ENISA EUVD (carried reject; **this round's Gate produced no new reject**) | reject | live `https://euvd.enisa.europa.eu/apidoc` re-fetched 2026-11-05: HTTP 200, 3062 bytes, sha256 `6fb32b61a3f44c7aa137699de08cf3a240aab7315f0d68ec7012e69d0a0a38d5` — byte-identical to the S104 row's recorded digest; 0 occurrences of `endpoint`, 0 of `/api/` | **agree** | served body remains an SPA shell; no line-anchorable capture or located quote exists; flip condition not met. Marked as the carried reject because round 72 opened exactly one candidate (S107) and rejected none |

`corpus/SOURCES.md` row re-opened: S107 (line 119) — `teaches`/`anchor` cells carry path:line anchors
into the capture (`S107.txt:649`, `:797`, `:886`, `:1166-1168`), all resolving; `status=mined`,
`recheck=90d`, `used-by` = the new entry. `## Gate` records the access date, URL and the located
quote; the census (`sources-census.sh validate`) exits 0.

## 4. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | **unprovable-but-better** | frozen predicate re-derived green on the final bytes and the round-71 harm is measurably reversed, but the claim's universal sentence and two kill clauses are falsified/weakened off-tree (L72-4/L72-5); the operator rules on the sentence |
| coverage | **unprovable-but-better** | every after-counter reproduces and F50/S107 is genuinely new admitted ground, but the frozen target's `api_key` clause is falsified by the source it names (M72-5/L72-10) and the frozen kill rule is not the complement of its predicate (L72-6); the narrowed amendment awaits the operator |

No axis is `harmed`: nothing that was true at base is false at tip except the two falsified
*claim sentences*, which were never true of the tree.

## 5. Trend verdicts (verifier's, independent of the lane's)

- **expansion — improved.** One net new admitted `knowledge/` entry on ground the coverage map did
  not hold (a bug tracker's REST contract; no prior S###/F## row covers Bugzilla), citing its
  `mined` registry row S107; frontier 49 → 50, entries 52 → 53, capture records 85 → 86, registry
  106 → 107 — all reproduced above. The falsified `api_key` clause narrows the *claim*, not the
  admitted ground, which the entry itself scopes correctly.
- **quality — improved.** The derive gate's denial surface strictly grew (two global write-root
  denials, realpath-keyed policy, +4 selftest cases, census counter committed) and reverses a
  measured round-71 harm with 247/247 ledger parity and a 4/4 kill matrix; no corpus entry failed
  its re-check (53/53 frontier entries pass, 17/17 quotes re-verify). Residual: the universal
  sentence overstates the census's `add_argument`-only read — routed, not hidden.
- **discernment — harmed.** The frozen C2 target named an `api_key` requirement the source does not
  state, and the freeze (`a34ce4c`) preceded the S107 capture — a content clause frozen before its
  source was opened (M72-5); the frozen kill rule was not the complement of its predicate (L72-6).
  The lane caught both through its own attack seats and recorded them honestly, but the defect was
  in the round's own gatekeeping, so the trend is harmed, matching the lane's own verdict.
  Caveat: zero reject decisions this round; the spot-check's reject face re-opened the carried S104.

## 6. Routed defects the lane must fix next round (from the lesson; none closed by r72)

- R-1 `--json`/`--root` outside the census `WRITE_CLASS`; R-2 `freeze-check.py` `bash -c` exec;
  R-3 `sort -T` temp-directory writes; R-4 round-71 harm-count predicates (correction appended);
  R-5 realpath-alias census semantics (operator ruling requested); R-6 regular-file fixture-head
  keying; R-7 `capture-binding-check.py --root .` admission; L72-2/L72-3 counter self-test and
  mutant coverage; L72-11 `probes()` `--gate` file handling; L72-12 C2 amendment awaiting the
  operator. Operator rulings owed: C1 universal sentence (L72-4), C2 amended admission (L72-12).
