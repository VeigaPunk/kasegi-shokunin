# RevC2BeforeAfter — round 34 wave1 receipt

Seat: RevC2BeforeAfter (reviewer, leaf of the L2 wave). Assignment: **independent before→after
verification of C2 (coverage)** — re-derive every C2 counter from
`.ufo/waves/round-34/claims.json` with its own command at the tip and report matches/differences
with exact outputs. This seat authored none of the C2 changes; every command below was run by
this seat and outputs are quoted verbatim.

## Report

### 0. Environment and method

- Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base
  `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims-freeze commit
  `29f606dbdd28aff6fd4573ab4b90788bbb90af13`; lane tip at first measure `206e510`
  ("round-34: wave-1 spec (65 seats, v2 policy), validated plan and dispatch").
- **Before** = `git archive 014ee2d7aa8c3c095ff57ae51097606a9906228c | tar -x -C
  /fast/scratch/hyaku/kasegi-r34/RevC2BeforeAfter/base` → 6815 files. **After** = the lane
  working copy, measured at quiescence (watcher: all four C2 surfaces present + harness and
  SOURCES.md digests stable across two consecutive 30 s polls) — quiescence reached
  **2026-10-26T05:38:42Z**, battery run immediately after.
- Frozen-claims integrity: `sha256sum .ufo/waves/round-34/claims.json` →
  `dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850`, byte-identical to
  `git show 29f606db…:.ufo/waves/round-34/claims.json | sha256sum`. The claims read are the
  committed frozen bytes.
- Working copy at first measure carried 8 dirty paths (the wave-1 landings arrive uncommitted;
  the L1 commits): `M SCORECARD.md`, `M corpus/QUALITY.md`,
  `M corpus/instruments/frontier-recheck-count.py`, `M corpus/source-snapshots/round-32/manifest.json`,
  `?? .ufo/waves/round-34/{assimilation,wave1.ready,wave1}`, `?? corpus/source-snapshots/round-34/`.
  At the final battery the dirty set had grown to 19 paths (list in §9) — C1 seats landed
  concurrently; none of my seven counters reads a C1-only file except the harness (whose final
  bytes are quoted).
- Read-only git plumbing only (`archive`, `show`, `ls-tree`, `log`, `status`, `diff`); no
  `git add/commit/push`, no jj mutations. **No tools installed or upgraded** (no `pacman`, `uv`,
  `npx`, no binary fetch) — stdlib `python3`, the lane's committed instruments, `git`, `grep`,
  `sha256sum` only.

### 0b. The frozen before-control cross-check

The freeze commit carries `.ufo/waves/round-34/c2-controls/before.txt` ("kasegi round-34 frozen
before-controls (base 014ee2d7…)"). My independent base battery reproduced every C2 line of it:

| measure | frozen control | my base run | match |
|---|---|---|---|
| frontier admitted | 16 | 16 | yes |
| registry rows | 50 | 50 | yes |
| S051 rows | 0 | 0 | yes |
| entries citing S051 | 0 | 0 | yes |
| harness | entries=19 pass=19 exit=0 | entries=19 pass=19 exit=0 | yes |
| source-recheck S051 | `manifest UNAVAILABLE reason=missing` / recheck_exit=2 | same, exit=2 | yes |
| knowledge entries | 45 | 45 | yes |
| c2-controls at base | (absent) | `ls c2-controls/` → No such file or directory | yes |

### 1. Counter 1 — frontier rows

Command: `grep -cE '^\| F[0-9]+ \|' corpus/README.md`

- Base tree: `16` (exit 0) — matches claims before `frontier_admitted=16`.
- Tip at quiescence (2026-10-26T05:38:42Z): **`17`** (exit 0) — **MATCH** with claim after 17.
- The landed F17 row (`corpus/README.md`, appended by ExecHarnessAfter under L1 authorization,
  26 inserted / 0 deleted lines per its receipt §3):

```
| F17 | Immunefi Vulnerability Severity Classification System v2.2 — Web3/smart-contract bounty severity classification | admitted | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 | Read a level from Immunefi's own per-asset-class table: the five numbered levels rank impacts inside one scope table, the level is fixed largely by impact — "finalizes them largely by the impact tha…
```

  (row continues: `…t they cause" (S051.txt:52), may be downgraded or rejected when the exploit
  needs elevated privileges or uncommon user interaction (S051.txt:55-56), and the funds
  boundary is whose funds and for how long they stay frozen: theft of any user funds is
  Critical (S051.txt:75) while "Temporary freezing of funds" is High (S051.txt:88). The page
  carries no CVSS mapping, no reward figure and no version-selection rule (FC-2/FC-3/FC-4), so
  neither a payout nor portability across asset classes follows from a level. |)
- Topic cell matches the claim's description verbatim ("Immunefi Vulnerability Severity
  Classification System v2.2 — Web3/smart-contract bounty severity classification").

### 2. Counter 2 — registry rows

Command: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`

- Base tree: `50` — matches claims before. Tip at quiescence: **`51`** (exit 0) — **MATCH**.
- SOURCES.md grew 100 → 105 lines, five insertions / zero deletions (S051 row at `:57`, Search-log
  bullet at `:77`, three R8 lines at `:103-105`; per ExecRegistryAppend-2's ping and receipt,
  consistent with my diff-free line-count checks).

### 3. Counter 3 — S051 row

Command: `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md`

- Base tree: `0`. Tip at quiescence: **`1`** (exit 0) — **MATCH**.
- Landed row cells verified by this seat (row at `corpus/SOURCES.md:57`, one physical line):

```
| S051 | Immunefi Vulnerability Severity Classification System v2.2 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ | docs | A | Immunefi's own Web3 severity classification system v2.2 as this page states it: … | capture corpus/source-snapshots/round-34/S051.txt (sha256 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5, 175 lines): H1 L45 names v2.2; … L72 Smart Contracts heading; L73 LevelImpact; L74-L83 Critical bullets …; L84-L89 High; L90-L94 Medium; L95 Low; L96 None | Immunefi's VSCS v2.2 places Web3 bugs on a five-level scale, … so read the Smart Contracts bullets as v2.2's impact vocabulary rather than as CVSS scores, a program's payout ladder or an authorisation to test | mined | 2026-10-26 | 90d | corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md |
```

- Claim cells all hold: tier **A**, status **mined**, opened **2026-10-26**, recheck `90d`,
  used-by the F17 entry path; anchor pinned to the round-34 capture whose sha256 I re-measured
  (`4fd8ed98…b325a5`, matches the row and the manifest pin).

### 4. Counter 4 — entries citing S051

Command: `grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l`

- Base tree: `0`. Tip at quiescence: **`1`** — **MATCH**; the one file is
  `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (grep -l prints exactly that
  path; `grep -cE '^source: S051 '` on the file → `1`).
- Knowledge entries `ls corpus/knowledge/*.md | wc -l`: base `45` (claim before 45 — match),
  tip at quiescence **`46`** (claim after 46 — **MATCH**).
- Entry digest history observed by this seat: `e71fbcd9…` (05:3xZ, 112 lines, mid-finalization)
  → **`948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`** (113 lines, stable
  across two checks at 05:4xZ). Entry header verified: `source: S051 — https://immunefi.com/…`
  (S051.txt:45 + line locators), `verified-at: 2026-10-26`, `ground: F17`, and a Q10-form
  recheck line (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3
  corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json
  --source S051   # 18 assertions …`). I re-derived all seven of the entry's falsifiable checks
  against the capture — every count reproduces: FC-1 `15`, FC-2 `v2.2=2 v2.3=0`, FC-3 `CVSS=0`,
  FC-4 `reward=0 $=0`, FC-5 `perm=2 temp=1`, FC-6 `exec=1`, FC-7 `none=2`.

### 5. Counter 5 — harness `python3 corpus/instruments/frontier-recheck-count.py`

- **Base tree** (base instrument bytes on base corpus): 19 PASS lines F01–F16 (F09/F10/F11 two
  rows each), summary `entries=19 pass=19 exit=0`, `exit=0` — matches claims before.
- **Mid-flight observation (2026-10-26T05:1xZ, instrument `2cff234e751c…`, dirty):**
  `entries=19 pass=14 exit=1`, F01–F05 `problems=selection-not-in-header-sources` — the in-flight
  rule-A patch flagged the five legacy entries whose `recheck:` lines chain an extra `--source`
  their single header `source:` line doesn't declare (e.g. F01 header `source: S001`, recheck
  line also selects S002). Confirmed as ExecFrontierBidirectional's in-flight state by
  ExecHarnessAfter (its receipt §F-C quotes the same run); at that digest the harness `--selftest`
  also printed `selftest cases=4 failures=1` (case `extra-source-not-cited` expected a problem
  pair the run didn't print) — I ran it myself with `--scratch` inside my seat dir.
- **Tip at quiescence (instrument `87b14892dfc42792056c7a9f09a0783e9d749d0478f376841c98bfc25e0a7c29`):**

```
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
exit=0
```

  **MATCH** with claim after (`entries=20 pass=20 exit=0` incl. the F17 line; note the claim's
  `PASS F17 ids=S051` is an ellipsis form — the literal string `PASS F17 ids=S051` does not
  grep: the printed line is column-padded, `PASS     F17  knowledge/… ids=S051           exit=0`;
  ScoutDatawalk F-4a records the same).
- Harness `--selftest` at the quiescent digest (my run, `--scratch` inside my seat dir):
  `selftest cases=6 failures=0`, `exit=0` — cases `bidirectional-holds`,
  `selection-not-declared`, `header-source-not-rechecked`, `evidence-list-declares-selection`,
  `evidence-declared-not-rechecked`, `selection-neither-declared-nor-mentioned`. Final rule-A
  semantics (from the landed diff): the declared set is the union of the header `source:` ids
  and the per-source evidence-list ids (`- S002, …` bullets); rule A requires
  `declared ∪ evidence == recheck_ids` in both directions, with problem names
  `header-sources-not-rechecked` / `selection-not-declared-by-entry`. That union is what makes
  F01–F05 pass while the dropped-header-line mutation still fails.

### 6. Counter 6 — source-recheck S051

Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051`

- Base tree: `manifest UNAVAILABLE reason=missing`, `exit=2` — matches claims before.
- Tip at quiescence (manifest `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe`,
  122 lines; capture `4fd8ed98…` — I re-hashed both):

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok
S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok
S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
exit=0
```

- **MATCH on exit 0 and `sha256 OK`; wording difference on "every assertion occurrences=1":**
  16 of 18 assertions print `occurrences=1`; Q9 and Q17 print `occurrences=2` with verified
  anchors (`anchor=77-ok`, `anchor=96-ok`) — the instrument's legitimate QUALITY Q9/B2 path for
  a twice-occurring quote (the same words appear in the Blockchain/DLT table at L62/L71). This
  is a recorded, deliberate decision, not a slip: ExecSnapshotR34's receipt §6.2 documents it
  (including the rejected all-unique alternative, manifest sha256 `3e726d84…`, which would have
  asserted converter-joined spans the entry does not quote) and cites the committed round-30
  precedent (`S047:Q1 OK occurrences=3 anchor=123-ok`). ScoutDatawalk F-2 independently flags
  the frozen wording and suggests an appended note (claims are frozen; corrections land as
  appended files). The kill rule ("source-recheck S051 exit != 0") is satisfied either way.
- Manifest record fields verified: `schema_version` 1, one record `S051`, `path=S051.txt`
  (stem=id, B1), `sha256=4fd8ed98…` (byte-verified by me), `url=https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/`,
  `fetched_utc=2026-10-26T05:31:10Z` — **strict UTC**, no local offset. 18 quote assertions
  Q1–Q18; Q2 (five level names, L47-L51) uniquely carries no anchor (declared in the manifest
  purpose: no four-line anchor window holds a five-line span).

### 7. Counter 7 — census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`

- Tip at first measure (05:1xZ) and again at quiescence — identical output both times:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

- **MATCH**: exit 0, W04 S028/S029 only — identical to the frozen
  `.ufo/waves/round-34/census-before.txt` content lines. The census reads the live fleet tree,
  so no base-commit run exists; the claim's before and after values are identical and the live
  runs cover both.

### 8. Junk F17 twin (C2 predicate clause)

- **Committed**: `git ls-tree --name-only 29f606d .ufo/waves/round-34/c2-controls/` →
  `before.txt`, `junk-checker.py`, `junk-f17.md`; absent at base `014ee2d` (ls-tree → empty).
  The claims' C2 before ("junk twin exists at c2-controls/junk-f17.md") is therefore a
  freeze-time state (committed in the freeze commit itself), while C1's before ("no junk-twin
  control committed under c2-controls/") is the base state — both verified, no contradiction.
- **Shape counters pass it** (my run of the committed checker):
  `python3 .ufo/waves/round-34/c2-controls/junk-checker.py` →
  `junk_twin h1=True source_line=True recheck_line=True` / `shape_counters=3/3`, exit 0.
- **Not admitted** (my checks): no `junk` path under `corpus/knowledge/`; no frontier row names
  it (the harness's 20 entries are the real ones; the twin lives outside `corpus/` and has no
  README row); `grep` over `corpus/README.md`/`corpus/SOURCES.md` finds no twin reference.
- **Rejection demonstrated independently by this seat** (control manifest built in my scratch
  from the twin's own bytes, extracted programmatically, not retyped; capture copied read-only):

```
twin body sentence (extracted, normalized):
  Immunefi's VSCS v2.2 defines five severity levels for smart-contract exploits; Critical includes "Direct theft of any user funds".
--- source-recheck on the junk-twin control manifest ---
S051:sha256 OK
S051:J1 MISMATCH reason=quote-not-found
S051:J2 OK occurrences=1
junk_recheck_exit=1
```

  The twin's load-bearing sentence fails the captured-source comparison (`quote-not-found`,
  **exit 1**). ExecHarnessAfter's receipt §F-B shows the same demonstration
  (`Q1 MISMATCH reason=quote-not-found`, `junkman_exit=1`,
  `grep -c "five severity levels for smart-contract exploits" S051.txt` → 0).
- **Three honest boundaries, all measured:**
  1. The twin's own `recheck:` line points at the real manifest, so once the manifest landed it
     exits **0** like the real entry's (my run: `junk_recheck_exit_at_tip=0`) — the bare command
     does not discriminate junk from real; ScoutDatawalk F-1 records the same ("the junk twin's
     own recheck line … is byte-identical to the real entry's recheck command, so at tip both
     exit 0 … the before control (`junk_recheck_exit=2`) does not discriminate junk from real").
  2. The twin's embedded fragment `Direct theft of any user funds` **does occur once** in the
     landed capture (`S051.txt:75`; my `grep -c` → 1; my control assertion J2 →
     `OK occurrences=1`). The twin's `[FABRICATED — no capture holds this quote]` label was
     written at freeze against a then-empty capture set and is stale relative to the landed
     tree; ScoutDatawalk F-1b independently: "the twin's quote is not fabricated … The only
     rejection that can work is reviewer/semantic (the twin's own file label), not a capture
     check." The rejection therefore rests on the sentence-level comparison above plus the
     Q1/Q3 reviewer gate (fabricated anchor, no verbatim located quote, no manifest record) —
     not on fragment absence.
  3. **The non-author reviewer REFUSE record was not yet on disk at my final measure**
     (2026-10-26T05:4xZ): `grep -l REFUSE .ufo/waves/round-34/wave1/*.md` matches only
     ExecHarnessAfter / ScoutDatawalk / ScoutPackageThemes / ScribeAssimilationGate / this
     receipt — no reviewer verdict receipt on the twin (RevEntryF17, RevRowS051,
     ExecDoNothingReject receipts not landed at that time). The claims' after wording
     ("non-author reviewer REFUSE on record") is therefore **half-demonstrated at my
     measurement time**: the executable half (source-recheck exit != 0 on the twin's asserted
     sentence) is shown by two independent seats; the reviewer-record half is pending those
     seats' receipts. Flagged for the L1 to confirm at integration.

### 9. Cross-checks and adjacent observations

- **Erratum-1 after-state verified** (C1 literal superseded by
  `.ufo/waves/round-34/claims-erratum-1.md`, filed by the L1): my run of
  `python3 corpus/instruments/capture-binding-check.py` prints `MANIFEST round-34 records=1
  url_bound=1 fetched=1 archival=0`, `AUDIT records=41 with_url=41 with_fetched_utc=3
  with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2
  orphans=1 orphan=S040-live.txt`, `records=41 bound=41 unbound=0`, `binding_exit=0` — exactly
  the erratum's ruled after-state (41 records after S051; the intermediate `unbound=1
  rule=no-row record=S051` state was measured by ExecSnapshotR34 §5 before the row landed).
- **Stray untracked file at lane root**: `?? selftest-baseline.txt` — content is a
  capture-binding-check `--selftest` baseline (`selftest cases=23 failures=0`, 23 case lines).
  Not this seat's file (this seat wrote only its receipt in the lane); reported for the L1's
  untracked-file sweep.
- **Round-33 lesson / round-29 lesson / round-26+32 manifests dirty**: C1 seats' appends
  (errata, strict-UTC normalization) — outside this seat's counters, listed for completeness.

### 10. Verdict

| C2 counter (claims.json counting_commands) | before (base 014ee2d, my run) | after (tip at quiescence 05:38:42Z, my run) | claim | verdict |
|---|---|---|---|---|
| frontier rows | 16 | **17** | 16 → 17 | MATCH |
| registry rows | 50 | **51** | 50 → 51 | MATCH |
| S051 row | 0 | **1** (tier A, mined, opened 2026-10-26) | 1 | MATCH |
| entries citing S051 | 0 | **1** (`immunefi-vscs-v2-2-smart-contract-severity.md`) | 1 | MATCH |
| harness | entries=19 pass=19 exit=0 | **entries=20 pass=20 exit=0** incl. `PASS F17 … ids=S051` | 20/20 | MATCH |
| source-recheck S051 | `manifest UNAVAILABLE reason=missing`, exit 2 | 18/18 OK, sha256 OK, **exit 0** (Q9/Q17 `occurrences=2` anchor-verified) | exit 0 | MATCH (exit + sha256); predicate wording "every assertion occurrences=1" not literal for 2/18 — recorded deviation |
| census | (live-tree; frozen control identical) | exit 0, W04 S028/S029 only | exit 0 | MATCH |
| knowledge entries | 45 | **46** | 45 → 46 | MATCH |
| junk twin | committed at freeze; shape 3/3; recheck exit 2 (manifest absent) | not admitted; shape 3/3; asserted sentence fails `quote-not-found` exit 1; bare recheck line exits 0; reviewer REFUSE record pending at my final measure | rejected by admission gate | executable rejection demonstrated (2 seats); reviewer-record half pending |

**C2 verifies at the tip on every counter this seat can re-derive**; the two wording-level
deviations (occurrences=1 literal; `PASS F17 ids=S051` ellipsis form) and the pending
reviewer-REFUSE record are reported above with exact outputs for the L1's integration decision.

### 11. Scratch

Scratch root `/fast/scratch/hyaku/kasegi-r34/RevC2BeforeAfter/` (base-tree extraction,
after-battery script, junk-rejection demo + control manifest). Deleted before yield — final
state recorded in the yield message. No tool was installed or upgraded.

## Addendum — post-battery cross-checks (2026-10-26T05:5xZ)

1. **Cross-seat quiescence agreement.** ExecCensusAfter-2's independent quiescence watcher fired
   at 2026-10-26T05:48:31Z (3 consecutive 20 s polls, identical input digest) and reports
   `rows=51 s051=1 front=17 citing=1 know=46 manifest=1` — every value equal to my battery — with
   `corpus/SOURCES.md 4c85ff86…` and `corpus/README.md 876be9cc…`, the exact digests my battery
   measured. I re-hashed both after its ping: unchanged. Same bytes, same counters, two seats.
2. **Harness digest moved after my battery; counter re-verified at the new bytes.**
   `sha256sum corpus/instruments/frontier-recheck-count.py` now prints
   `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` (was `87b14892…` at my
   §5 battery). Re-run at the new bytes: `PASS F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
   ids=S051 exit=0`, `entries=20 pass=20 exit=0`, plain exit 0; `--selftest` → `selftest cases=6
   failures=0`, exit 0 (same six case names). Counter 5 holds at both digests; the §5 measured
   values stand, now pinned to two instrument revisions. SOURCES.md / README.md / the F17 entry
   (`948b202e…`) / the round-34 manifest (`d5077f81…`) are byte-unchanged since the battery.
3. Scratch re-created only for the §addendum selftest `--scratch` and deleted again immediately
   (verified absent: `test -d` exit 1).
