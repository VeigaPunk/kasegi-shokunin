# ScoutGateRegistry — round 28, wave 1 — C1 SKILL.md gate-registry reconnaissance

Seat: ScoutGateRegistry (scout, read-only; **no production file edited**).
Axis: depth:verifiability (lowest non-retired, score 4 held) · Milestone: round-28.
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Lane base (claims freeze): `c9f8b115a098c65356e4b3b6048af45a37ab8395` (SKILL.md = 1032 lines / 83142 bytes)
Worktree HEAD at measurement: `94f387cbee71a532a51ce075f01701a557231e85`
Measured UTC: 2026-10-25T17:31Z … 17:52Z (all timestamps UTC)
Tools installed/updated: **NONE** (no pacman/uv/npx run; host-wide pacman pause respected).
VCS: read-only `git show/log/status/ls-files` only — no add/commit/checkout/reset, no mutating `jj`.
Scratch: `/tmp/sgr{,2,3,4}` only (copies of SKILL.md / corpus / resolver). No file outside the lane repo and `/tmp` was written.

**Digests of the bytes this report measures (measured at report-write time):**

```
125be37d85ffe6be30a3c372b52d96d8074e3c4d7f4baf835d0f5aed5f56cca6  SKILL.md                       (1035 lines, 84078 bytes)
cf35a643b8d5d9d2eb726d4190e029f275bc5a129e87ccec40d27c9d86d5322b  corpus/instruments/README.md    (327 lines, 23378 bytes)
95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514  corpus/instruments/anchorcheck.py (523 lines)
c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748  corpus/instruments/anchorcheck.py @ BASE (pre-change digest)
```

STATE LABEL: **LANDED-BYTES** for SKILL.md / instruments README / instrument — all three production edits had already landed by this seat's first read (17:31Z). The "PRE-STATE" branch in my item text no longer applies to SKILL.md or the instrument; it applies only to the *base* revision bytes, which I measured from `git show c9f8b115…`.

---

## 1. Every existing gate|probe registry row/table naming `anchorcheck.py`

### 1a. The gate|probe registry table itself — SKILL.md § "Gates & probes registry"

**BASE bytes (`c9f8b115…`), SKILL.md lines 977–985:**

```
977: ## Gates & probes registry
978:
979: | name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
980: |---|---|---|---|---|---|---|---|
981: | recheck-audit.py | gate|probe | python3 corpus/instruments/recheck-audit.py [--json <out>] | 0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | .ufo/waves/round-26/c1-receipt-index.txt | corpus/ read-only + its own receipt dir | kasegi |
982:
983: The audit is stateful against the committed expected list (the pinned receipt index): the present knowledge-entry set is compared to it, so deleting an entry is a red audit (exit 1 naming the missing entry), never a silent green pass.
```

**BASE verdict map / exit-code wording (the only registry row, `recheck-audit.py`, line 981):**
verdict map = `0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate`; self-test = `python3 corpus/instruments/recheck-audit.py --selftest`; pinned-value path = `.ufo/waves/round-26/c1-receipt-index.txt`; write scope = `corpus/ read-only + its own receipt dir`; owner = `kasegi`.

**In the BASE bytes `anchorcheck.py` was named in SKILL.md zero times** (`git show c9f8b115:SKILL.md | grep -n anchorcheck` → 0 hits). The only `gate|probe`-typed row anywhere in the lane at base is `recheck-audit.py`; `grep -rn 'gate|probe' --include='*.md'` outside `.ufo/` returns only `corpus/lessons/round-25-verifier-spotcheck.md:151` (prose mention, not a table row).

### 1b. LANDED bytes — the `anchorcheck.py` row now exists at SKILL.md:982

**Live row, verbatim (SKILL.md:982, digest `125be37d…`):**

```
| anchorcheck.py | gate|probe | python3 corpus/instruments/anchorcheck.py <file.md> | fail-closed: exit 0 clean \| exit 1 on MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BASE-ABSENT/BOUNTIES-ABSENT (LOST-RECORDED recorded, not fail; bounties base = `$KASEGI_BOUNTIES` override, else canonical `~/Projects/bounties`) | python3 corpus/instruments/anchorcheck.py --selftest -> one isolating fixture per limb, prints `selftest cases=N failures=0` | .ufo/waves/round-28/c1-receipt-index.txt | all inputs read-only + its own receipt dir | kasegi |
```

Its **current verdict map / exit-code wording**: `fail-closed: exit 0 clean | exit 1 on MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BASE-ABSENT/BOUNTIES-ABSENT`, with the explicit carve-out `LOST-RECORDED recorded, not fail` and the derived-root clause `$KASEGI_BOUNTIES` override, else canonical `~/Projects/bounties`.

**Registry counter:** `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → **1 at base → 2 live** (measured on both byte states).

### 1c. Other tables/rows that name `anchorcheck.py` (not gate|probe registries)

| file:line | row kind | what it records |
|---|---|---|
| `corpus/instruments/README.md:12` | instrument table (`script | what it measures | run`) | base text: "anchor gate: each supported `path:NN[-MM]` citation is range-checked against the lane, frozen mirror, pinned Git blob, or declared ORIGIN-WORK root; prints the cited source lines…"; run cell `python3 corpus/instruments/anchorcheck.py <file.md>`. **Unchanged between base and live** (live digest `cf35a643…`, base prefix byte-identical — see §3). |
| `corpus/README.md:35` | coverage-map row | depth-instruments coverage row naming `instruments/{density.py,resolve.py,anchorcheck.py,…}` |
| `corpus/knowledge/source-tree-loss-2026-09-28.md:330` | measurement row | round-15 anchorcheck census (`194 in-range mirror cite instances, 0 past-EOF`) |
| `corpus/lessons/round-22.md:21`, `round-24.md:21`, `round-27-verifier-spotcheck.md:29-32` | lesson rows | historical C1 counters (base fixture exit 0, 0 BOUNTIES lines, selftest crash) |
| `corpus/QUALITY.md:49` | R7 row | names anchorcheck.py as a registered detector |

---

## 2. Where the instruments README documents anchorcheck's verdict classes and exit behavior

### 2a. BASE bytes (`c9f8b115…:corpus/instruments/README.md`, 196 lines / 14325 bytes)

The README documents anchorcheck in **three places**, and **none of them stated an exit code**:

* **`corpus/instruments/README.md:12`** (instrument table row, quoted above) — what the gate measures and the run command; no exit wording.
* **`corpus/instruments/README.md:41-45`** (Known limits) — the verdict-class semantics:
  ```
  41: - **`anchorcheck.py` checks only supported anchored token shapes.** `bad=0`
  42:   means every recognized anchor is either in range or explicitly
  43:   `LOST-RECORDED`; it does not make historical lost-tree content openable and
  44:   does not validate unanchored template paths. Round 18 broadened the matcher,
  45:   exposed 82 bad anchors in the pre-edit `SKILL.md` (versus 46 under the r17
  ```
* **`corpus/instruments/README.md:55-62`** (round-18 rate/limits) — the auditability counters: "broadened-matcher bad anchors 82 → 0, ORIGIN 1 → 5, and explicit LOST-RECORDED 5 → 104".

Base README `grep -n exit` hits only lines **119** (`resolve.py` fixture "exit code = verdict"), **146** (`source-recheck.py` "exits 0 only when every assertion … 1 on a mismatch, 2 when a base is missing") and **180** (`frontier-recheck-count.py` "entries=K pass=P exit=0|1"). **anchorcheck's own exit behavior was undocumented in the README at base**, because the base instrument never had one: base `main()` fell off the end, so `sys.exit(main(...))` was 0 for every verdict class.

The authoritative verdict-class list at base lived in the **instrument docstring**, not the README — `corpus/instruments/anchorcheck.py:9-19` (base):
```
 9:   IN-RANGE          mirror-based cite, anchor inside the mirror file
10:   IN-RANGE(LANE)    lane-based cite, anchor in range
11:   IN-RANGE(ORIGIN)  explicit ORIGIN-WORK cite, checked against current bytes
12:   IN-RANGE(PIN)     cite verified against a pinned git blob
13:   MISSING-FILE      no file at any declared base (bad)
14:   PAST-EOF          file exists at the base but the anchor is out of range (bad)
15:   OUTSIDE-BASE      explicit ORIGIN-WORK or MIRROR-ABSOLUTE path escapes its root (bad)
16:   PIN-BROKEN        a pin was declared but the git object does not exist (bad)
17:   LOST-RECORDED     token prefixed `[lost-tree] ` or `[lost-base] ` inside the backticks:
18:                     deliberately non-openable historical anchor; reported and
19:                     counted separately, NOT checked, never counted as validated
```
and base `anchorcheck.py:58-61` (the summary line + the `bad` definition): `== <src>: N in-range cite instances, M bad; K distinct anchors; LOST-RECORDED=L PIN-BROKEN=P ORIGIN=O OUTSIDE-BASE=X BASE-ABSENT=B` / `(bad = MISSING-FILE + PAST-EOF + OUTSIDE-BASE; BASE-ABSENT and LOST-RECORDED are explicit recorded-loss verdicts, not bad.)`. Base had **no** `BOUNTIES-ABSENT` class and **no** exit-status rule.

### 2b. LANDED bytes — the README now carries the exit contract (appended section, lines 198-327)

Live digest `cf35a643…`, 327 lines. New section header at **:198** `## Round-28 amendment — \`anchorcheck.py\` fails closed (C1)`. The exit/verdict documentation now lives there:

* **:211-220** — "**Exit is a verdict, not a print.** `FAIL_CLASSES` is the exit driver: `MISSING-FILE`, `PAST-EOF`, `OUTSIDE-BASE`, `PIN-BROKEN`, `BASE-ABSENT`, `BOUNTIES-ABSENT` — exit 1 when any count is nonzero, else 0. Exit 0 means every recognized anchor is `IN-RANGE*` or `LOST-RECORDED`. `LOST-RECORDED` keeps its round-16 meaning: recorded-not-fail … `bad` stays the historical three-class count (MISSING-FILE + PAST-EOF + OUTSIDE-BASE) for receipt continuity, so PIN-BROKEN, BASE-ABSENT and BOUNTIES-ABSENT move the exit without moving `bad`: read the exit status, not only the summary."
* **:229-235** — the README flags itself: at the landed digest a run over this file exits 1 (three pre-existing BASE-ABSENT cites at its lines 114/116/164).
* **:237-257** — `BOUNTIES-ABSENT` class; derived root `$KASEGI_BOUNTIES` else canonical `~/Projects/bounties`; realpath confinement; exactly one BOUNTIES-ABSENT line for the r27 fixture.
* **:259-281** — `--selftest` spelling, one isolating fixture per FAIL_CLASSES limb, `selftest cases=9 failures=0`, exit 0.
* **:283-308** — corpus disclosure: declared four, **measured zero** (the 4 named citations are plain-text `source:` headers, never handed to `CITE`).
* **:310-327** — the re-verify command block and its targets.

Instrument-side exit contract (landed `corpus/instruments/anchorcheck.py`): `FAIL_CLASSES = ('MISSING-FILE','PAST-EOF','OUTSIDE-BASE','PIN-BROKEN','BASE-ABSENT','BOUNTIES-ABSENT')` (lines 169-170); docstring lines 9-31 carry the class table and "Exit status (round-28 fail-closed rule): 1 when any FAIL_CLASSES count is nonzero … else 0. LOST-RECORDED stays recorded-not-fail".

---

## 3. R6: does appending ONE row at the end of the existing registry table shift any existing line?

**Measured, not assumed. The answer is: the row insert shifts nothing at or above the insert point, and it does shift everything *below* it by exactly one line — because the registry table is NOT at the end of SKILL.md.**

### 3a. Geometry (measured byte offsets, base `c9f8b115…` SKILL.md, 1032 lines / 83142 bytes)

| base line | start offset (0-based) | content len | newline at | content |
|---|---|---|---|---|
| 977 | 73748 | 26 | 73774 | `## Gates & probes registry` |
| 979 | 73776 | 99 | 73875 | table header |
| 980 | 73876 | 33 | 73909 | separator |
| **981** | **73910** | **311** | **74221** | **last existing data row (`recheck-audit.py`)** |
| 982 | 74222 | 0 | 74222 | blank |
| 983 | 74223 | 234 | 74457 | the "audit is stateful…" prose note |
| 985 | 74459 | 895 | 75354 | `## Cited paths …` heading |

**The table's last-row line number = 981. The byte offset at which an appended row would land = 74222 (0-based), i.e. immediately after the newline of line 981** (the live insert landed at exactly that offset — live line 982 starts at 74222). Base EOF = 83142 bytes.

### 3b. What a row insert at 982 actually moves

Because the registry table sits at 977-981 with 51 more lines of SKILL.md after it (the "Cited paths" list at 985-1021 and the "Frontier decision table" at 1023-1032), inserting a row at 982 shifts **every base line ≥ 982 by +1**:

| base | live | content |
|---|---|---|
| 983 (prose note) | 984 | unchanged text, new number |
| 985 (`## Cited paths`) | 986 | unchanged text, new number |
| 1000 (`ops/shared.mjs` bullet) | 1001 | unchanged text, new number |
| 1007 (4-alternative brace set) | 1008 | unchanged text, new number |
| 1014 (`.ufo/bh*/` bullet) | 1015 | unchanged text, new number |
| 1019 (`{README.md,.gitignore}`) | 1020 | unchanged text, new number |
| 1021 (`pendle-core-v2-public/`) | 1022 | unchanged text, new number |

**R6 test, executed on the real detector (not asserted):** `python3 corpus/instruments/anchorcheck.py <file>` over the base tree vs the live tree with the *same* landed instrument (`95333e29…`), with `KASEGI_LANE_ROOT` pointed at each byte state:

* Over **SKILL.md itself**: the two 315-line reports differ in exactly **one** line, and only in its `md:NN` position field — `LOST-RECORDED md:998 [lost-base] check-freshness.mjs:61` → `md:999`. The **cited source lines and every verdict class are identical** (base and live both: `7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`). Normalized for `md:NN`, the two reports are byte-identical.
* Over the **305 tracked files that cite `SKILL.md:NNN`**: **6 files' printed cited-source lines change** (they cite the shifted region):
  `.ufo/waves/round-23/falsify/BraceGlobProbe.md` (SKILL.md:1000), `.ufo/waves/round-24/wave1/CritC2.md` (:1021), `.ufo/waves/round-24/wave1/QuarterRouted2.md` (:1000), `.ufo/waves/round-24/wave1/QuarterSHONEN.md` (:1014), `.ufo/waves/round-24/wave1/RevC2Held.md` (:1014-1023), `.ufo/waves/round-24/wave1/ScoutAnchor.md` (:1019-1023), `.ufo/waves/round-25/wave1/RevBound8.md` (:993) — plus their `.ufo/waves/round-25/**/base/**` copies.
  **Important qualification:** those pointers were *already* stale before this round. At the round-24 fixture commit `d3614a2` the `sighting{…}` bullet was at SKILL.md:1000; after round 26 inserted the registry section it moved to 1009, and the live insert moves it to 1010. So the row insert makes a pre-existing drift one line deeper; it does **not** newly break a pointer that was correct at the base.
* The **only committed non-`.ufo`** file that cites the shifted region is `corpus/instruments/resolve-dispatch-fixtures.json:159,161` (`SKILL.md:1000` inside a fixture "why"/file-content string). That fixture does not read the live SKILL.md — `resolve-dispatch-check.py:137` writes its **own** `SKILL.md` into a temp lane — so it is unaffected.
* `corpus/lessons/round-26-verifier-spotcheck.md:32` cites the range `SKILL.md:977-985` in prose (not backticked, so `CITE` never matches it): the registry block still occupies 977-985 at live, so the range still spans the section (the new row at 982 lands inside it). No anchorcheck-visible change.

**Verdict on the question as posed: appending ONE new row at the end of the existing registry table does shift the ~51 SKILL.md lines below the table by +1.** The R6-safe alternatives are (a) a *same-line suffix* on line 981 (not viable — a table row must be its own line), or (b) appending a **new section at end of file** (the strategy the sibling README seat used). The landed choice (row at 982) keeps the row inside the table and inside the counter's regex, at the cost of the +1 shift of SKILL.md:983-1032 — which, measured above, moves no anchorcheck-verdict and no committed-file pointer that was correct at base. **This is a disclosure item for ScribeLesson / ScribeScorecard, not a no-harm violation of the frozen C1 predicate** (C1's no-harm limb is "SKILL.md live run keeps exit 0, bad=0, verdict classes unchanged" — measured: exit 0, `0 bad`, `LOST-RECORDED=306`, identical to base).

### 3c. Instruments README: strictly R6-clean

`corpus/instruments/README.md` base = **196 lines / 14325 bytes**. Live = **327 lines / 23378 bytes**, and `live.startswith(base_bytes) == True` (byte-exact prefix): the round-28 section was appended **at end of file** (live line 197 = blank, 198 = the new `## Round-28 amendment` header). **No existing line moved.** Every committed cite of the README still lands on the same bytes: `corpus/knowledge/citation-bases.md:25` and `:100` → `corpus/instruments/README.md:31-38`; `corpus/lessons/round-22.md:19` → `:63` and `:131`; `corpus/lessons/round-20-recensus.md:43` → `:16-17`. All still hold (verified by reading the base lines at those numbers and by the anchorcheck sweeps).

---

## 4. Exact append strategy for ScribeSkillGate and ExecInstrReadme (cite R6)

**R6 text (`corpus/QUALITY.md:40`, unchanged in the live file):**
> "| R6 | An edit to a file that other files cite by line number keeps every existing line at its number (append at the end, or a same-line suffix); anchorcheck before/after prints the same cited source lines. | M17 — r22 inserted provenance headers at line 2 of 25 legacy entries, shifting ~160 path:line anchors (e.g. SKILL.md:821) by +3 until L1 caught it pre-commit |"

### ScribeSkillGate (SKILL.md) — **one new table row, appended at the end of the registry table; a same-line suffix is NOT available**

* **New row, not a same-line suffix.** R6's two permitted shapes are "append at the end" or "a same-line suffix". A suffix is impossible here: the deliverable is a *table row*, and a markdown table row must occupy its own physical line (a suffix to line 981 would fuse two rows into one line and break the 8-column header — GFM would then render 9 cells on that line).
* **"Append at the end" must be read as "at the end of the registry table", not "at the end of the file".** A new file-end section would not be *the registry table*: the counter `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` and the lesson pointer `SKILL.md:977-985` both point at the 977-981 table. Inserting the row directly after line 981 is the only shape that keeps the registry one table.
* **Exact landing coordinates (measured):** prior last row = **line 981**; new row = **line 982**; the row's first byte lands at **0-based offset 74222** (immediately after line 981's newline at 74221). Nothing at or above 981 moved; 983-1032 moved +1, disclosed in §3b.
* **Content requirements already met by the landed row** (SKILL.md:982): name `anchorcheck.py`; type `gate|probe` (unescaped, matching the round-26 counter regex — the same trade the round-26 row made, and the same pre-existing render defect: a strict GFM renderer splits that cell, so `type` renders as `gate` and `entry command` as `probe`, and the `owner` cell is dropped on **both** rows); entry command `python3 corpus/instruments/anchorcheck.py <file.md>`; verdict map with the six fail classes and the `LOST-RECORDED recorded, not fail` carve-out; self-test `python3 corpus/instruments/anchorcheck.py --selftest` printing `selftest cases=N failures=0`; pinned-value path `.ufo/waves/round-28/c1-receipt-index.txt`; write scope; owner `kasegi`.
* **Two open items ScribeSkillGate should verify at close** (both measured here, both currently **unmet**):
  1. **The pinned-value path does not exist yet.** `.ufo/waves/round-28/c1-receipt-index.txt` → `ls` = *No such file or directory*. The frozen C1 counter `grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt` cannot return 1 until that file lands (KasegiR28 owns the canonical receipt assembler).
  2. **The round-28 note at SKILL.md:1035 repeats a claim the erratum already superseded.** It says the new arm is "invisible to all existing bytes — no verdict-class movement on any file, corpus or `SKILL.md`". That was true at the erratum's measurement instant (17:24Z) but **is no longer true of the live tree**: `SCORECARD.md` (written 17:37Z, after the erratum at 17:25Z) now carries two backticked anchored bounties citations — `SCORECARD.md:640` `~/Projects/bounties/ops/claim-check.mjs:96` and `SCORECARD.md:658` `[lost-tree] ~/Projects/bounties/ops/claim-check.mjs:5` — and the landed instrument therefore reports `BOUNTIES-ABSENT md:640 …` on SCORECARD.md and **exits 1** on it (measured: `== SCORECARD.md: 12 in-range cite instances, 0 bad; … LOST-RECORDED=1 … BASE-ABSENT=8`, `exit=1`). A lane-wide sweep at the landed digest gives **8 files exiting 1**: `corpus/knowledge/citation-bases.md`, `corpus/knowledge/cra-manufacturer-reporting-duties.md`, `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`, `corpus/knowledge/root-loss-2026-10-12.md`, `corpus/QUALITY.md`, `corpus/instruments/README.md`, `SCORECARD.md`, `LOG.md` (SKILL.md itself stays exit 0). The note's wording should say "no verdict-class movement on SKILL.md or on the corpus files measured at 17:24Z", or be re-scoped to the current tree.

### ExecInstrReadme (corpus/instruments/README.md) — **append at end of file; do not touch the table row or the Known-limits bullet**

* **Append at end of file is the only R6-clean shape here**, and it is what was done: base = 196 lines / 14325 bytes; the round-28 section starts at live line 198 with `live.startswith(base) == True` (byte-exact prefix) → **no existing line moved**, and the four committed cites of README lines (16-17, 31-38, 63, 131) all still land on the same bytes.
* **Do NOT rewrite line 12** (the instrument table row) to add exit wording: it is the anchor of the table, and the row already carries the run command; the exit contract belongs in the appended section, where the class list, the fail/exit rule and the `--selftest` spelling are all stated (live :211-220, :237-257, :259-281).
* **Do NOT append to the Known-limits bullet at :41-45** as a same-line suffix: that bullet's cited range (`instruments/README.md:31-38` from `citation-bases.md:25,:100`) is nearby and a growing bullet invites silent renumbering; the appended section is the safe place.
* **One live consequence the README already discloses (verified)**: with the landed instrument, a run over `corpus/instruments/README.md` **exits 1** on three pre-existing BASE-ABSENT cites (its own lines 114, 116, 164) — documented at live :229-235. This is the fail-closed rule working as designed (recorded-loss verdicts now fail the exit), not a regression, but it means "the lane's own instrument README no longer passes its own gate" and belongs in the round lesson.

---

## 5. Cross-checks that bear on the C1 no-harm limb

| check | base (`c2a9e6c6…` instrument) | live (`95333e29…` instrument) | verdict |
|---|---|---|---|
| `anchorcheck.py SKILL.md` | exit 0; `7 in-range, 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` | **identical** (exit 0, same six numbers) | C1(d) no-harm **holds** |
| `anchorcheck.py --selftest` | `FileNotFoundError: '--selftest'`, exit 1 (crash) | `selftest cases=9 failures=0`, exit 0 | C1(c) **holds** |
| r27 bad fixture `.ufo/waves/round-27/c1-controls/bad-fixture.md` | exit 0 (BASE-ABSENT printed) | exit 1 | C1(a) **holds** |
| r27 bounties fixture → `grep -c BOUNTIES-ABSENT` | 0 | 1 | C1(b) **holds** |
| `.ufo/waves/round-28/c1-receipt-index.txt` | absent | **still absent** (`ls` → no such file) | C1(c) receipt arm **not yet verifiable** — KasegiR28 owns it |
| frozen C1 `corpus_disclosure` cell (4 corpus citations newly LOST-RECORDED) | — | **not reproduced**: the 4 named cites are plain-text `source:` headers, never handed to `CITE`; measured 0 of 4 move (`claim-gates.md`, `intake-and-finalize.md`, `mission-control.md` all print `LOST-RECORDED=0`; `source-tree-loss-2026-09-28.md` prints `LOST-RECORDED=15`, unchanged) | already superseded by `.ufo/waves/round-28/claims-erratum-1.md`; **but** the erratum's own "zero backticked anchored bounties citations exist lane-wide" is now stale — `SCORECARD.md:640,:658` (see §4) |
| `resolve.py` census (SKILL.md scope, isolated base vs live SKILL.md, same corpus) | skill `37/513` | skill `38/516` | +1 numerator / +3 denominator: the new row + note add three backticked path tokens (`~/Projects/bounties`, `~/Projects/bounties/`, `.ufo/waves/round-28/claims-erratum-1.md`) — all GONE, so the *rate* barely moves; distinct token set unchanged (2044 → 2044) |
| `density.py SKILL.md` | mean **150.3**, 652 path-citation instances, 20 blocks | mean **160.2**, 656 instances, 20 blocks | the "Gates & probes registry" block goes 80.0 → 233.3; depth:density is not the round-28 axis but the number moves and belongs in ScribeScorecard's cell |
| `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` | 1 | 2 | registry row landed |

**Live-file ordering caveat for the L1.** The three production files were being edited concurrently while this seat measured (SKILL.md mtime 17:26:18Z, README 17:35:08Z, SCORECARD 17:37:59Z, instrument 17:28:31Z; the claims erratum 17:25:50Z). Every number above was measured on the byte states whose digests are printed at the top of this report; **re-run the §5 table at the final commit digest before publishing the lesson**. The re-run command is the README's own block at live `:310-327`.

---

## 6. Remaining unknowns (not resolvable from source alone)

1. Whether the L1 accepts the SKILL.md:983-1032 +1 shift as an R6 disclosure or wants the row relocated to a file-end section (which would break the `SKILL.md:977-985` lesson pointer and the "one registry table" reading). Both shapes satisfy the frozen C1 counters; only the R6 letter differs. **Owner: L1 / ScribeLesson.**
2. Whether `SKILL.md:1035`'s note text will be re-scoped to the current tree (the `SCORECARD.md:640` BOUNTIES-ABSENT case). **Owner: ScribeSkillGate (SKILL.md) with ScribeScorecard (SCORECARD.md).**
3. Whether the round lesson records the 8-file exit-1 set at the landed digest (5 corpus files + instruments README + SCORECARD.md + LOG.md) as an intended consequence of fail-closed exits. **Owner: ScribeLesson.**
4. Whether `.ufo/waves/round-28/c1-receipt-index.txt` will carry `selftest cases=9 failures=0` at the instrument digest `95333e29…` (the C1(c) counter greps that exact path). **Owner: KasegiR28.**

---

*Scout recon, no production edit, no VCS write. Confidence: high for every line number, byte offset, digest and exit code quoted above (each was executed, not inferred); the only inferences are labelled in §4 (R6 shape choice) and §6 (owner decisions).*

---

## Addendum — peer question: "round 27 is incomplete; I did not create the frozen claims, wave spec, or ready file, and did not commit or push either report"

Raised in-channel by agent `SoujiR27`; verified from source (read-only git) and relayed to `Main` and to the peer. This is outside my assigned question but is source-verified, so it is recorded rather than answered only in chat.

**Measured (read-only git, lane repo):**

| check | result |
|---|---|
| `.ufo/waves/round-27/wave1/`, `wave2/` contents | both exist, **0 files** (`ls -A` empty; `git ls-files` → 0 each) |
| r27 wave spec / dispatch / ready file | **never existed in any commit**: `git log --all --diff-filter=A -- '.ufo/waves/round-27/**'` yields no spec/dispatch/ready path |
| r27 seat reports | **none**: `git ls-files .ufo/waves/round-27/wave1` = 0, `…/wave2` = 0 — so none is uncommitted |
| r27 freeze commit `c2ab51d` (freeze + before-receipts + lesson M27-1/M27-2 + LOG + SCORECARD) | **committed and pushed** — `git merge-base --is-ancestor c2ab51d origin/master` → YES |
| r27 verifier spot-check `261a665` | **pushed** — ancestor of `origin/master` → YES |
| `corpus/lessons/round-27.md`, `.ufo/waves/round-27/claims.json` | tracked; lesson added by `c2ab51d` |
| round-28 freeze `c9f8b11`, round-28 spec `94f387c` | both ancestors of `origin/master` → YES (both) |
| r28 dispatch state | `.ufo/waves/round-28/wave1.ready` exists (`"l1":"KasegiR28"`); `.ufo/waves/round-28/wave1.ready.dispatched` = `2026-10-25T14:22:08 spawned 69`; `wave1-dispatch.json` names 69 seats |
| unreachable r27-related commits | `065996d`, `717ffdc` (r27 freeze + c1/c2-controls + claims.json + LOG), `d4274fc` (census-before + claims.json + LOG + SCORECARD + lesson) — **not** ancestors of `origin/master`, in no branch; their content is inside the pushed `c2ab51d`. Not touched (no VCS write, no gc). |

**Conclusion.** Round 27's "incompleteness" is the lane's own *recorded* honest stop, not uncommitted work: `corpus/lessons/round-27.md:10-11` ("no wave was dispatched, no production byte changed, and both claims land NOT VERIFIED") and `:44-47` (M27-2: "no `task` swarm call was ever sent for round 27 … the 32–64 wave band were never exercised"). There was never an r27 wave spec/ready file to commit and there are no r27 seat reports to push; everything r27 did commit is in the pushed history. The round-28 wave was dispatched at 14:22:08Z, so nothing there is waiting on a dispatcher. The peer's label set (`Souji*`/`Tabi*`) has **0** mentions in `wave1-dispatch.json` (its C2-entry task corresponds to dispatch seat `ScribeEntryC2`, whose receipt already exists at `.ufo/waves/round-28/receipts/ScribeEntryC2.txt`) — a roster-label mismatch, not a missing dispatch. If the L1 wants the three unreachable intermediate commits documented or pruned, that is a lane-helper VCS decision, not a scout action.
