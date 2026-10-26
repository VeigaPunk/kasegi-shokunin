# ExecC2Harness — frontier-recheck harness: base baseline and F20 closure (round 37, C2 / coverage)

Seat: `ExecC2Harness` (leaf, executor). Item: establish the frontier-recheck harness baseline, then prove in
scratch that the planned F20 additions close the harness for C2.

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — **no lane file was written by this seat**; the only
writes are this receipt and scratch under `/fast/scratch/hyaku/kasegi-r37/ExecC2Harness/`. No mutating git
command was run (only `rev-parse`, `log`, `merge-base --is-ancestor`, `archive`, `status`). Fleet root,
sibling lanes and source trees untouched. No tool was installed or upgraded.
Base `b56a41680cefd391868c1c370dc063c69d827e7d`; lane head at spawn `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(round-37 freeze `224df74` + `claims-erratum-1`); claims frozen in `.ufo/waves/round-37/claims.json`.

**Bottom line.** Harness needs **no code change**. On the base export it prints `entries=22 pass=22 exit=0`
(`--selftest`: `cases=6 failures=0`). In the scratch mirror carrying only the planned data additions
(F20 README row + S054 registry row + stub entry + synthetic S054 capture + manifest) it prints
`entries=23 pass=23 exit=0` with `PASS F20 knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
ids=S054 exit=0`, and `source-recheck.py --source S054` exits 0. Every limb is shown load-bearing by an
isolating variant. One measured caveat matters for how the claim is read (§6): all 22 existing rows, and a
Q10-conforming F20 row, execute their recheck against the **live lane** because the line carries an absolute
`cd` prefix — the counter is a live-tree measurement, not an export measurement.

## 1. What the committed harness checks, per frontier row

Read from `corpus/instruments/frontier-recheck-count.py` (sha256
`1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249`; identical in the base export and in the
mirror — I changed no byte of it). Its own docstring states limbs A–F; these are the exact code paths:

| step | code | what it binds |
|---|---|---|
| row discovery | `FRONTIER_ROW = ^\|\s*(F\d+)\s*\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|\s*`?([^\|`]+?)`?\s*\|` over `corpus/README.md` | row id (`F<digits>`), topic, status, entry cell. **Any** table row in README with that shape counts; the Coverage-map rows do not match because their first cell is not `F<digits>`. |
| admission filter | `admitted = [r for r in rows if r[2] == "admitted"]` | the status cell must equal the literal `admitted`; any other value drops the row from the denominator entirely (variant G). |
| entry cell | `for entry in cell.split(",")` | a cell may name several entries (`F09`/`F10`/`F11` each name two), one record per path. |
| entry resolution | `root/<entry>` else `root/corpus/<entry>`; `None` → `missing-entry` | README names entries corpus-relative (`knowledge/…`). A path that resolves to neither fails closed with the row id and path printed (variant I). |
| declaration set A | `SOURCE_LINE = ^source:\s*(S\d{3,})` (header) ∪ `EVIDENCE_LINE = ^(?:[-*]\|\d+[.)])\s+(S\d{3,})\b` (per-source evidence bullet) | the entry's **own** declared source ids, both shapes the corpus uses. |
| recheck shape C | `RECHECK_LINE = ^recheck:\s*(.+)$` (first line wins); must contain `source-recheck.py` and not `--selftest` | a `true`, a URL, or a `--selftest` line is `not-a-recheck-invocation` (variant A). |
| source ids | `RECHECK_SOURCE = --source\s+(S\d{3,})`, `RECHECK_MANIFEST = --manifest\s+(\S+)` (quotes stripped) | the selected ids and the named manifest. |
| bidirectional A | `declared_set ⊆ recheck_ids` and `recheck_ids ⊆ declared_set` where `declared_set = set(declared) \| set(evidence)` | no dropped id (`header-sources-not-rechecked`, variant D) and no undeclared id (`selection-not-declared-by-entry`). |
| citation limb | every `S\d{3,}` on lines that are not declaration/recheck lines; `recheck_ids ⊆ cited` | a copied-in recheck whose id the entry never mentions fails (`selection-not-cited-by-entry`, variant L2). |
| manifest B | `manifest_ids()`: file at `root/<manifest>`, JSON object, `schema_version == 1` (int), `sources[]` list of dicts → id set; must cover `recheck_ids` | `manifest-unreadable` / `manifest-missing-ids` (variant C). |
| execution D | `subprocess.run(["bash","-c",recheck], cwd=root)` only when `problems == []`; exit code must be 0 | the row's own command is what decides; a non-zero exit is `recheck-exit-N` (variant M). |
| global fail-closed | duplicate realpath across records → `DUPLICATE-ENTRY`; `not records` → exit 1; `passed != len(records)` → exit 1; `read_frontier` `OSError` → exit 2 | exit is `1 if fail_closed else 0` regardless of the printed pass count (variant F prints `pass=23` and still exits 1). |

What it does **not** read — measured, not inferred:

- **Not `corpus/SOURCES.md`.** Deleting the S054 registry row leaves `F20 … PASS` and `entries=23 pass=23 exit=0` (variant K).
- **Not the README `sources` cell.** Replacing `S054` with `S999` in the F20 row leaves `PASS … ids=S054` (variant J) — source ids come from the entry, never the table cell.
- **Not the manifest `url`, `fetched_utc`, `fetched_bytes`, `http` block, `location`, or `normalized`** — `manifest_ids()` reads only `schema_version` and `sources[].id`; the executed `source-recheck.py` reads `sha256` and `quotes[]`.
- **Not the knowledge count or the registry row count.** "knowledge 48→49" and "registry 53→54" are not harness-measured quantities; §8 measures them with plain counts.

## 2. Baseline (pre-state)

### 2.1 Export of base `b56a416` (the r36 verifier spot-check)

```console
$ git archive b56a41680cefd391868c1c370dc063c69d827e7d | tar -x -C $S --one-top-level=lane-base
$ cd $S/lane-base && python3 corpus/instruments/frontier-recheck-count.py --root $S/lane-base --json $S/base-receipt.json
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
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
entries=22 pass=22 exit=0
EXIT=0
```

Note the denominator: **19 admitted README rows → 22 entry records** (F09, F10, F11 each name two entries).

### 2.2 Harness selftest (fixture lanes, not the corpus)

```console
$ python3 corpus/instruments/frontier-recheck-count.py --selftest --scratch $S/hyaku
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0
EXIT=0
```

### 2.3 Live lane head `b362068` (read-only; no `--json`, so nothing was written into the lane)

```console
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py --root .
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
entries=22 pass=22 exit=0
EXIT=0
```

Both pre-states: **entries=22 pass=22 exit=0**.

## 3. Mirror: the planned C2 additions

`git archive b56a416… | tar -x --one-top-level=lane-mirror` in scratch, then four additions and no others.
`diff -u` against the base export is exactly one inserted line in `corpus/README.md` and one inserted line in
`corpus/SOURCES.md`; three new files under `corpus/`.

### 3.1 `corpus/README.md` — one inserted row, directly after F19 (now L390)

```markdown
| F20 | SSVC — Stakeholder-Specific Vulnerability Categorization (CERT/CC, Carnegie Mellon University) | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | Keep the categorization attached to the stakeholder the procedure names: SSVC separates exploitation status, technical impact and the stakeholder's mission and well-being impact into decision points and returns Track/Track*/Attend/Act, so read it as a decision procedure distinct from a CVSS severity score (the capture's own L15 says it does not replace CVSS). |
```

```diff
@@ -387,6 +387,7 @@
 | F19 | FIRST EPSS exploitation-likelihood scoring | admitted | knowledge/epss-exploit-prediction-scoring.md | S053 | EPSS estimates … |
+| F20 | SSVC — Stakeholder-Specific Vulnerability Categorization (CERT/CC, Carnegie Mellon University) | admitted | … |
 
 [r35 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
```

### 3.2 `corpus/SOURCES.md` — one inserted registry row, directly after S053 (now L60), 11 cells

```markdown
| S054 | SSVC — Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ | docs | A | CERT/CC's own statement of its SSVC decision-tree method: the decision points it names and the outcome vocabulary, scoped to a named stakeholder | capture corpus/source-snapshots/round-37/S054.txt (SYNTHETIC ExecC2Harness fixture, not a live fetch; sha256 9f427dd9300b84c78f6d22f82afa7664a50c2c1ddfbd40d443e0e68e799b8bc8, 15 lines): title L1; purpose L6-L7; decision points L10-L11; outcomes L14-L15 | Read SSVC as a stakeholder-scoped decision procedure: exploitation status, technical impact and stakeholder impact stay separate axes and the outcome is a category, not a severity score. | mined | 2026-10-26 | 90d | corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |
```

The URL is `claims-erratum-1.md`'s corrected literal (`https://certcc.github.io/SSVC/tutorials/ssvc_overview/`),
not the frozen home-page literal; the harness reads neither cell, so this changes no measurement (§1, J/K).

### 3.3 `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (stub, 75 lines, sha256 `06254fb8ddf90f10ca3ecfc73e1cb2eccbca8c19ccccd3badf262ae080499107`)

Q1 header shape (three lines), `ground:`, `recheck:` relative to `root` so the mirror is what is measured:

```markdown
# SSVC — Stakeholder-Specific Vulnerability Categorization: a decision-tree procedure scoped to a named stakeholder (CERT/CC, Carnegie Mellon University)

source: S054 — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — capture corpus/source-snapshots/round-37/S054.txt (15 lines, sha256 9f427dd9300b84c78f6d22f82afa7664a50c2c1ddfbd40d443e0e68e799b8bc8; SYNTHETIC fixture capture written in the ExecC2Harness scratch mirror to exercise the planned C2 additions, not a fetch of the live page): title L1, purpose L6-L7, decision points L10-L11, outcomes L14-L15
verified-at: 2026-10-26
ground: F20
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054   # prints S054:sha256 OK then one S054:Q<n> OK line per pinned quote (occurrences=1, anchor=N-ok); exits 2 when the manifest or capture is absent and 1 when the digest differs or a quote moved; a pinned-capture comparison, not a fresh network check
```

Body sketch (Q-valid shape; the landed entry replaces the synthetic quotes with the overview-page pins):

- `## Attribution` — S054 stated as CERT/CC's own statement (Q4), no credential/session/private URL (Q6), and
  S054 is mentioned in prose so the citation limb is satisfied by the entry, not by the recheck line.
- `## Claim 1` — quote L6 (decision-tree method → stakeholder-specific categorization outcomes).
- `## Claim 2` — quote L7 (exploitation status / technical impact / stakeholder impact are separate axes).
- `## Claim 3` — quote L14 (Track, Track*, Attend, Act) plus the L15 boundary sentence.
- `## What the capture does not contain` — no numeric score, no CVSS vector, no reward figure, no deployment guidance.
- `## Falsifiable rule and checks` — three falsifiers (a)(b)(c) keyed to L6/L7/L14, and FC-1 (`grep -cF`, expected `1 1 1`).
- `## Scope and limits of the pin` — the pin pair (capture + manifest) and the explicit note that the capture is synthetic.

### 3.4 `corpus/source-snapshots/round-37/S054.txt` (15 lines, 746 bytes, sha256 `9f427dd9…99b8bc8`) — SYNTHETIC fixture

The capture is hand-written in scratch and says so on its own L3 (`SYNTHETIC FIXTURE CAPTURE — ExecC2Harness
scratch mirror … not a fetch of the live page`). It exists only so the capture→manifest→recheck binding can be
measured; the landed round-37 capture is the sibling seat's pinned overview-page bytes. Bytes:

```text
SSVC — Stakeholder-Specific Vulnerability Categorization (CERT/CC, Carnegie Mellon University)

SYNTHETIC FIXTURE CAPTURE — ExecC2Harness scratch mirror, 2026-10-26; not a fetch of the live page.

Purpose
SSVC is a decision-tree method that produces stakeholder-specific vulnerability categorization outcomes from a fixed set of decision points.
The method separates exploitation status from technical impact and from the stakeholder's mission and well-being impact.

Decision points
Exploitation status values are none, poc, and active.
Technical impact values are partial and total.

Outcomes
The decision outcomes are Track, Track*, Attend, and Act.
A stakeholder-specific categorization is not a severity score and does not replace CVSS.
```

### 3.5 `corpus/source-snapshots/round-37/manifest.json` (36 lines, 1270 bytes, sha256 `984effab42d7ccf7c60d9ce237aa75abda8faa37f147a4d3f0f983614e6fd714`)

Schema-1, one record `S054`, `path: S054.txt` (stem == id, Q9 B1), the capture digest, and Q1–Q3 with anchors 6/7/14:

```json
{
 "purpose": "Round-37 F20 fixture assertions for S054 (SSVC) — SYNTHETIC fixture capture built in the ExecC2Harness scratch mirror to exercise the planned C2 additions; not a live fetch.",
 "schema_version": 1,
 "sources": [
  {
   "fetched_utc": "2026-10-26T00:00:00Z",
   "id": "S054",
   "lines": 15,
   "normalized": "hand-written synthetic fixture text; UTF-8; final newline",
   "path": "S054.txt",
   "quotes": [
    {"anchor": 6,  "id": "Q1", "location": "L6; synthetic fixture line",  "quote": "SSVC is a decision-tree method that produces stakeholder-specific vulnerability categorization outcomes from a fixed set of decision points."},
    {"anchor": 7,  "id": "Q2", "location": "L7; synthetic fixture line",  "quote": "The method separates exploitation status from technical impact and from the stakeholder's mission and well-being impact."},
    {"anchor": 14, "id": "Q3", "location": "L14; synthetic fixture line", "quote": "The decision outcomes are Track, Track*, Attend, and Act."}
   ],
   "sha256": "9f427dd9300b84c78f6d22f82afa7664a50c2c1ddfbd40d443e0e68e799b8bc8",
   "snapshot_bytes": 746,
   "url": "https://certcc.github.io/SSVC/tutorials/ssvc_overview/"
  }
 ]
}
```

(The emitted file is the same object with keys sorted and one quote object per line; `source-recheck.py` requires
`sha256` + non-empty `quotes`, and reads neither `url` nor the `http` block, so a production manifest may add both.)

## 4. After-state in the mirror

### 4.1 The S054 recheck the entry's own line runs

```console
$ cd $S/lane-mirror && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=6-ok
S054:Q2 OK occurrences=1 anchor=7-ok
S054:Q3 OK occurrences=1 anchor=14-ok
EXIT=0
```

### 4.2 The harness over the mirror (canonical after-run, with `--json`)

```console
$ cd $S/lane-mirror && python3 corpus/instruments/frontier-recheck-count.py --root $S/lane-mirror --json $S/mirror-receipt.json
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
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
entries=23 pass=23 exit=0
EXIT=0
```

The `--json` record for F20 — all limbs empty of problems, `exit: 0`:

```json
{
 "entry": "knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md",
 "declared_ids": ["S054"],
 "evidence_declared_ids": [],
 "cited_ids": ["S054"],
 "recheck_ids": ["S054"],
 "manifest": "corpus/source-snapshots/round-37/manifest.json",
 "exit": 0,
 "problems": [],
 "status": "PASS"
}
entries=23 pass=23 duplicate=None
```

Re-ran twice (after the S053/S054 corruption experiments below were reverted) with the same `entries=23 pass=23
exit=0`; the run is deterministic on these bytes.

## 5. Binding controls — each limb isolated by a variant that fails (or passes) exactly there

Each variant is a copy of the mirror with one mutation; command is the same harness invocation.

| variant | mutation | F20 line | exit | verdict |
|---|---|---|---|---|
| A `recheck-true` | `recheck: true` (the r24 forgery route) | `FAIL … exit=- problems=not-a-recheck-invocation,no-source-selection,no-manifest` | 1 | limb C load-bearing |
| B `header-dropped` | `source:` line removed, prose mention kept | `FAIL … ids=- problems=no-source-line` | 1 | declaration required (A) |
| C `manifest-no-S054` | manifest `sources: []` | `FAIL … problems=manifest-missing-ids` | 1 | limb B load-bearing |
| D `evidence-S055-unselected` | evidence bullet `- S055, …` added, recheck still `S054` | `FAIL … problems=header-sources-not-rechecked` | 1 | bidirectional A, forward direction |
| E `no-source-selection` | `--source S054` dropped from the line | `FAIL … problems=no-source-selection` | 1 | selection required |
| F `duplicate-entry` | F20 row points at `knowledge/epss-exploit-prediction-scoring.md` | `PASS F20 … ids=S053` + `DUPLICATE-ENTRY F19,F20 knowledge/epss-exploit-prediction-scoring.md` | **1** | global fail-closed: `entries=23 pass=23 exit=1` |
| G `status-candidate` | F20 status cell → `candidate` | row absent (no `F20` line) | 0 | non-`admitted` rows leave the denominator: `entries=22 pass=22 exit=0` |
| I `missing-entry-path` | row names `knowledge/ssvc-absent.md` | `FAIL … problems=missing-entry` | 1 | row id + path printed, no traceback |
| J `readme-sources-cell` | README `sources` cell `S054` → `S999` | `PASS … ids=S054` | 0 | README cells other than id/status/entry are unread |
| K `sources-row-ignored` | S054 registry row deleted from `SOURCES.md` | `PASS … ids=S054` | 0 | `SOURCES.md` is not read by this counter |
| L2 `no-citation-at-all` | every `S054` token outside the `source:`/`recheck:` lines replaced with `this source` | `FAIL … problems=selection-not-cited-by-entry` | 1 | citation limb has teeth |
| M `q10-absolute-cd` | recheck prefixed `cd /home/…/kasegi-shokunin &&` (QUALITY Q10 form) | `FAIL … exit=2 problems=recheck-exit-2` | 1 | see §6 — pre-landing the absolute form reads the live lane |

Verbatim transcripts:

```text
===== variant-A-recheck-true.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=-    problems=not-a-recheck-invocation,no-source-selection,no-manifest
entries=23 pass=22 exit=1
EXIT=1
===== variant-B-header-dropped.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=-              exit=-    problems=no-source-line
entries=23 pass=22 exit=1
EXIT=1
===== variant-C-manifest-no-S054.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=-    problems=manifest-missing-ids
entries=23 pass=22 exit=1
EXIT=1
===== variant-D-evidence-S055-unselected.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=-    problems=header-sources-not-rechecked
entries=23 pass=22 exit=1
EXIT=1
===== variant-E-no-source-selection.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=-    problems=no-source-selection
entries=23 pass=22 exit=1
EXIT=1
===== variant-F-duplicate-entry.txt
PASS     F20  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
DUPLICATE-ENTRY F19,F20 knowledge/epss-exploit-prediction-scoring.md
entries=23 pass=23 exit=1
EXIT=1
===== variant-G-status-candidate.txt
entries=22 pass=22 exit=0
EXIT=0
===== variant-I-missing-entry-path.txt
FAIL     F20  knowledge/ssvc-absent.md                             ids=-              exit=-    problems=missing-entry
entries=23 pass=22 exit=1
EXIT=1
===== variant-J-readme-sources-cell-ignored.txt
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
entries=23 pass=23 exit=0
EXIT=0
===== variant-K-sources-row-ignored.txt
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
entries=23 pass=23 exit=0
EXIT=0
===== variant-L2-no-citation-at-all.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=-    problems=selection-not-cited-by-entry
entries=23 pass=22 exit=1
EXIT=1
===== variant-M-q10-absolute-cd.txt
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=2    problems=recheck-exit-2
entries=23 pass=22 exit=1
EXIT=1
```

**Measured limitation of the citation limb (L2 vs the first L control).** A first attempt that removed only the
prose sentence still passed, because `cited` is every `S\d{3,}` match outside declaration/recheck lines and the
capture-path token `corpus/source-snapshots/round-37/S054.txt` yields `S054`. So any entry that names its own
capture path satisfies the citation limb: the limb cannot catch a recheck line copied from another entry when
that entry also prints its capture path, and it only fires on an entry that never names the id at all (L2).
This is a property of the 22 existing rows too (each names its capture path), not of the planned changes.

## 6. Measured caveat: the counter is a live-lane measurement, not an export measurement

All **22** existing frontier entries carry an absolute prefix. Measured per entry:

```text
F01 … F19  recheck_lines=1 ABSOLUTE   (each line begins `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`)
entries 22    (the only non-absolute `recheck:` line in corpus/knowledge/ is root-loss-2026-10-12.md:76, not a frontier row)
```

So `bash -c <line>` with `cwd=<export>` still re-checks `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Proven
by corrupting the **export's** copy only:

```text
# mirror S053.txt (the F19 pin) corrupted in the mirror only: sha256 7b463e71019811da776ecc37bba76057837f383f9de60d5f16fa1aebdf549b67
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
entries=23 pass=23 exit=0
EXIT=0
# mirror S054.txt (my relative-form F20 pin) corrupted in the mirror only
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=1    problems=recheck-exit-1
entries=23 pass=22 exit=1
EXIT=1
# both restored to the recorded digests (S053 4ec61c59…, S054 9f427dd9…)
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
entries=23 pass=23 exit=0
EXIT=0
```

Consequences for reading the C2 claim:

1. `entries=22 pass=22` on the base export is **not** export-local evidence: every row re-verified the live lane.
   (It is still a true statement about the live lane at `b362068`, measured in §2.3.)
2. A Q10-conforming F20 entry (`cd <lane> && …`) behaves the same way. Variant M shows it here failing with
   `exit=2` only because the live lane does not yet carry `corpus/source-snapshots/round-37/manifest.json`:
   `manifest UNAVAILABLE reason=missing`. Post-landing the same line re-verifies the committed capture and exits 0
   — [INFERENCE] from the identical bytes exiting 0 under the relative form in §4.1; it cannot be measured from
   scratch without writing the lane.
3. Therefore the claim's `entries=23 pass=23` must be produced **after** the F20 files (row, registry row, entry,
   capture, manifest) are committed to the lane, which is how the frozen claim reads. A pre-landing run with the
   Q10 absolute form is red by construction (correctly: fail-closed on a missing manifest).

## 7. Code-change verdict

**No code change to `corpus/instruments/frontier-recheck-count.py` is needed** for the C2 claim. Evidence: it
reads `corpus/README.md` rows at run time and takes the entry path and source ids from the entry file
(§1); adding one admitted row plus one entry plus one manifest changed `entries` 22→23 and passed all limbs with
the instrument byte-identical to base (`sha256 1be79af6…cd48249` in both trees).

If export-local measurement of this counter were ever wanted, the minimal exact change would be in `main()`'s
execution step (`evaluate()` line `subprocess.run(["bash","-c",recheck], cwd=root …)`): reject or rewrite a
recheck line whose leading `cd` names an absolute path outside `os.path.realpath(root)` (e.g. a
`problems.append("recheck-cwd-outside-root")` before execution). That is **not** required by C2 and would flip all
22 legacy rows red on any export until their `cd` prefixes were migrated; the round-37 export instrument is C1's
`corpus/instruments/r37-closure.sh`, not this counter. Recommended instead: keep the harness as is, land F20 with
the Q10 `cd <lane> &&` prefix like its 22 siblings, and read the counter's number as a live-lane measurement
(§6).

## 8. Coverage counts the harness does not measure (corroboration for the C2 claim)

Plain counts on the base export vs the mirror, each reproducible with `ls`/`awk`:

| quantity | base `b56a416` | mirror (planned additions) | command |
|---|---|---|---|
| frontier README rows with status `admitted` | 19 | 20 | `grep -cE '^\| F[0-9]+ \|.*\| admitted \|' corpus/README.md` |
| harness entry records | 22 | 23 | the harness's own `entries=` line |
| `corpus/knowledge/*.md` files | 48 | 49 | `ls corpus/knowledge/*.md \| wc -l` |
| `corpus/SOURCES.md` registry rows | 53 | 54 | `grep -cE '^\| S[0-9]' corpus/SOURCES.md` |

So `knowledge 48→49` and `registry 53→54` are consistent with the planned addition; they are admission-ledger
facts, verified by the census/audit seats, **not** by this counter.

## 9. What this does not prove / risks

- **Fixture bytes, not the real capture.** The mirror's S054 capture is synthetic and says so; its quotes are not
  the overview page's. What is proven is the harness binding (row → entry → declared/selected/cited ids → manifest
  → executed recheck), which is independent of quote content. The landed entry's digest, anchors and quotes come
  from the capturing seat and must be refreshed together.
- **Live-lane dependence (§6).** `entries=23 pass=23` is true of the lane after landing; it is not a property of
  any `git archive` export, because every recheck line — including a Q10-conforming F20 line — targets the lane root.
- **Citation limb is path-satisfiable (§5).** An entry that prints `…/S054.txt` passes the citation limb even if its
  only real `S054` mention is that path; the limb cannot detect a cross-entry copy once a capture path is printed.
- **Pass counts and exit disagree by design.** Variant F prints `pass=23` with `exit=1`; a reader must read the exit
  code, not the pass count, for the duplicate-entry guard.
- **Loading order.** Running the counter on the lane before the round-37 manifest is committed gives F20
  `recheck-exit-2` (fail-closed) — expected, not a defect.
- **Unchanged pre-existing state.** The lane's `git status --porcelain` showed the same 6 round-37 wave entries
  before and after this seat (`assimilation/`, `wave1-plan.err`, `wave1-run.err`, `wave1.ready`,
  `wave1.ready.partial`, `wave1/`); nothing here added a lane change outside this receipt.

## 10. Reproduction (scratch, all paths under `/fast/scratch/hyaku/kasegi-r37/ExecC2Harness/`)

```sh
S=/fast/scratch/hyaku/kasegi-r37/ExecC2Harness; mkdir -p "$S"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive b56a41680cefd391868c1c370dc063c69d827e7d \
  | tar -x -C "$S" --one-top-level=lane-base
cd "$S/lane-base" && python3 corpus/instruments/frontier-recheck-count.py --root "$PWD"        # 22/22 exit 0
python3 corpus/instruments/frontier-recheck-count.py --selftest --scratch "$S/hyaku"           # 6/0
cp -a "$S/lane-base" "$S/lane-mirror"                                                          # then §3 additions
cd "$S/lane-mirror" && python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-37/manifest.json --source S054                      # exit 0
python3 corpus/instruments/frontier-recheck-count.py --root "$PWD"                             # 23/23 exit 0
```

Scratch hygiene: every work copy lived under `$S` (never `$TMPDIR`); `HYAKU_SCRATCH="$S/hyaku"` was exported for
every harness run so its selftest fixtures also stayed there. `$S` was removed with `rm -rf` after this receipt was
written; no `/tmp` file was created.

## 11. Tooling

None installed, none upgraded (nothing needed). No `pacman` was run.
