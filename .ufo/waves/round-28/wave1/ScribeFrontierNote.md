# ScribeFrontierNote — round-28 frontier continuity (read-only seat)

**Scope.** No production edit. Consumed by `ScribeReadmeC2` (owner of `corpus/README.md`) and
by the L1. Every number below comes from a command recorded here or in
`.ufo/waves/round-28/receipts/ScribeFrontierNote.txt` (Rev 2).

**Bytes assessed.**

| snapshot | sha256 | lines | state |
|---|---|---|---|
| pre-landing, `17:25:48Z` | `e38ba5673c0f6789d3de33cf688ccfa3bc88684ed24fd48afe1b891fe7a815a4` | 243 | F12 row + 12/12 amendment landed; entry absent |
| **final, `17:28:20Z`** | **`5f458a7a26b8dfc2dd2ee2e46e11380d5697e51e77213772bce7b59253363180`** | **245** | entry + harness landed; 45-day suffix added |

Lane base `261a6651b7e52c58e9ad0ceaef6f3bd0bf2d904f` (claims freeze). Read-only
`git show`/`diff`; no VCS write, no tool installed, no pacman attempted.

---

## 1. State of the Frontier at the final snapshot

| Counter (frozen command) | Base `261a665` | Final `5f458a7a` | C2 after-value |
|---|---|---|---|
| `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | 11 | **12** | 12 ✓ |
| same, row count (`$2 ~ /^ *F[0-9]+ /`) | 11 | **12** | — |
| `python3 corpus/instruments/frontier-recheck-count.py` | `entries=14 pass=14 exit=0` (r27 control) | **`entries=15 pass=15 exit=0`**, F12 `PASS … ids=S041,S042 exit=0` | 15/15 exit=0 ✓ |
| `test -f corpus/knowledge/japanese-domestic-disclosure-workflow.md` | absent | **present**, 18 452 B; `source: S041`, `source: S042`, `recheck:` one line (both ids, round-28 manifest), `ground: F12` | present ✓ |
| `wc -l corpus/instruments/knowledge-expected.txt` / `grep -vc '^#'` | 41 / 39 | **41 / 39 (unchanged)** | 42 / 40 **← open item, §5** |

The **landed F12 row** (`corpus/README.md:213`, verbatim at `5f458a7a`):

```text
| F12 | Japanese state-coordinated disclosure workflow | admitted | knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | Use 起算日 — the day the guideline's Ⅳ.4.2) notification was first attempted (S041 footnote 4), not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02. The same 45-day figure is triggered differently on each side: S041's publication date is a 目安 of 45 days from 起算日 (Ⅳ.3)), CERT/CC's 45 days runs from the initial report (S004, F02). |
```

Shape mirrors F11 (six columns, entry path relative to `corpus/`, comma-separated source ids);
`next` = 65 words / 393 characters / no `|` (table-safe). The entry's `ground: F12` closes the
staged package's `ground: F13` off-by-one (round-27 spotcheck routed defect 2).

---

## 2. The F12 `next` cell — wording proposed, and the landed text judged

### 2.1 What the cell must carry

C2 freezes the topic to *"F12 Japanese state-coordinated disclosure workflow"*; F02
(`coordinated-disclosure-timelines.md` §Rule) requires a timeline record to name the
policy/coordinator, **the event that starts its clock**, the interval, the patch/publication
relationship and any extension. For one *next* cell the transferable minimum is four elements:

1. the Japanese column is keyed to `起算日`;
2. `起算日` is defined by its trigger — the first **attempted** Ⅳ.4.2) notification to the
   developer (manifest S041 Q1 = `S041.txt:340`: *"本ガイドラインのⅣ．４．2)において規定された
   連絡を最初に試みた日を起算日とします。"*);
3. it is **not** the finder's report to IPA and **not** the developer's acknowledgement
   (S042 Q1 = `S042.txt:145`: JPCERT/CC notifies IPA that contact was *started*);
4. the column exists to be compared against F02's coordinator records, each keeping its own
   attribution.

### 2.2 Verdict on the landed cell: PASS (all four elements, one row)

- Element 1-3 are the first sentence, with the anchoring evidence named (`S041 footnote 4`;
  `S041.txt:340` is the footnote text, located at Ⅳ.6.4) 注釈 4 in the capture).
- Element 4 is "*as the Japanese column when comparing coordinator timelines against F02*".
- The second sentence is the **optional** strengthening this seat proposed (see below),
  accepted by `ScribeReadmeC2`. Its two grounds check out:
  `S041.txt:648`, repeated at `:786` — *"…（起算日、２．注釈 4 を参照）から 45 日後を目安とします。"*
  (45 days **from 起算日**); `coordinated-disclosure-timelines.md:22` (S004) — *"Vulnerabilities
  reported to the CERT/CC will be disclosed to the public 45 days after the initial report"*
  (45 days **from the initial report**). Same number, different trigger: exactly the transplant
  trap F02 forbids.
- Deliberately **not** in the cell: the 7-day receipt acknowledgement (S041 Q5, `S041.txt:1916`)
  and the one-year withdrawal rule (S041 Q6, `S041.txt:305`). Both are response/withdrawal
  clocks, not the disclosure clock the column compares; the entry carries them.

No further change is required. The cell is a paraphrase with one short quoted fragment per side,
not a republished quote.

### 2.3 Text churn observed (recorded, not judged)

| read at | F12 `next` cell |
|---|---|
| pre-landing, first read | `Use 起算日 — the first *attempted* developer contact, not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02.` |
| pre-landing, `e38ba567` `17:25:48Z` | `Use 起算日 — the day the guideline's Ⅳ.4.2) notification was first attempted (S041 footnote 4), not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02.` |
| **final `5f458a7a`** | the row above — §2.2 form **plus** the 45-day trigger-contrast sentence |

All three satisfy §2.1; the final is the strongest. `ScribeReadmeC2` owns the file and logs
old→new in its own receipt (Rev 2); this table exists so the L1 knows which text it is judging.

---

## 3. Topic-string collision check

**Candidate / landed string:** `Japanese state-coordinated disclosure workflow` — byte-equal to
the pinned string in `.ufo/waves/round-28/claims.json` C2 (`topic substring of C2 name: True`)
and to `build-wave1-spec.py:404`.

**Method** (script in receipt): parse every `| F<n> | …` row; compare candidate vs each topic
(a) byte-exact, (b) case-folded, (c) token subsets in either direction (`[a-z0-9]+` after
splitting `/` and `-`), (d) Jaccard on token sets.

**Result (12 rows):**

| comparison | result |
|---|---|
| exact / casefold equality with an existing row | **none** (only its own F12 row matches itself) |
| token subset or superset of another row's topic | **none** |
| nearest neighbour | **F02** `Coordinated-disclosure timelines` — shared `{coordinated, disclosure}`, Jaccard 0.333 |
| next nearest | **F10** `Vendor-side disclosure policies as corpus objects` — shared `{disclosure}`, Jaccard 0.091 |
| an `F13` row | **none** (no id collision either) |

**Verdict: no collision.** F02's overlap names the *method* (a coordinator-timeline comparison);
F12 names a *national state-coordinated workflow* that feeds it. F11 is a different axis (ISO/IEC
29147:2014 vs 30111:2013 division of labour): F12 sharing source **S041** with F11 is expected —
F11 anchors 付録6 §2 (`S041.txt:1667-1678`), F12 anchors 起算日/図1 (`S041.txt:340`, `:212`,
`:249`), and the S041 registry row's `used-by` now lists all three entries (verified, `SOURCES.md:47`).

Not a collision, recorded so it is not mistaken for one: the entry H1 is *"The Japanese domestic
disclosure workflow"* while the row topic is *"Japanese state-coordinated disclosure workflow"*.
The row topic names the distinguishing property; the entry cell makes the file traceable.
Precedent: F09's topic differs from both its entry titles.

**Post-landing remap check (round-27 spotcheck routed defect 2): closed.**
`grep '^ground:' corpus/knowledge/japanese-domestic-disclosure-workflow.md` → `ground: F12 — …`;
no `F13` reference in the file.

---

## 4. Coverage-map paragraph — denominator wording verified

**The three sentences, verbatim at `5f458a7a`:**

- `:215` — `The original domain-root map is exhausted: 0/18 surfaces are present.`
- `:217-218` (history, unchanged from base) — `public-practice frontier above is a separate
  denominator (11/11 admitted at round 26; F01-F08 at round 23, F09 at round 24, F10 at round 25,
  F11 at round 26) and is not counted into the 0/18 figure.`
- `:220-224` (r28 amendment) — `… at round 28 the frontier stands at **12/12 admitted** — F01-F08
  at round 23, F09 at round 24, F10 at round 25, F11 at round 26, F12 at round 28. The 0/18
  sentence is untouched: the lost-domain denominator still holds 0 of 18 surfaces present, and the
  frontier count stays outside it.`

**Check 1 — frontier figure matches the table.** 12 rows / 12 `admitted` (frozen counter, §1);
base was 11/11. The `11/11 … at round 26` figure is corroborated by `SCORECARD.md` round-26 C2
(`frontier admitted 10 → 11`). Each number is true of its own round.

**Check 2 — no `11/12`.** `grep -n '11/12' corpus/README.md` → **NONE**. This matters because the
seat brief phrases the target as "the 11/12 admitted public-practice frontier". `11/12` (eleven
admitted of twelve rows) is **not a reachable at-rest state**: without F12 the counter is 11/11;
with F12 admitted it is 12/12. A final text reading `11/12` would assert one unadmitted row and
contradict both the table and the C2 after-value. The landed wording avoids it — do not "correct"
`12/12` to `11/12`.

**Check 3 — the frontier is never folded into the lost-domain denominator.** The 0/18 sentence is
byte-identical to base (`git show 261a665:corpus/README.md` lines 214-218 = current 215-219
content); the amendment restates the separation in its own words ("still holds 0 of 18 … stays
outside it"). No sentence adds 12 (or 11) to 18, and none derives a combined 12/30 or similar.

**Check 4 — R6/R9.** `git diff --numstat 261a665 -- corpus/README.md` → `28 0` (zero deletions);
hunks `@@ -212,0 +213 @@` and `@@ -217,0 +219,27 @@`; **lines 1-212 byte-identical** to base
(`diff` → `IDENTICAL 1-212`). Active citations into this file are `:5`, `:49`, `:54`, `:82`,
`:145`, `:168`, `:200-202`, `:211` (repo-wide `grep`, excluding `.ufo` snapshots and the
generated census) — **none ≥213**, so nothing cited shifts, and `citation-survival.md`'s two
pinned rows (`:49`, `:82`) keep both number and bytes. The `11/11` sentence is retained, not
rewritten (R9); the correction is dated and appended.

**Adjacent observations — reported, not blockers, not this seat's write scope:**

1. `corpus/README.md:5`'s last dated entry count is `r25 … 37`. The current basis is supplied by
   the reconciliation note (`41 lines = 39 entries + 2 comments` → `40 entries / 42 lines` after
   the entry lands). Line 5 is a dated statement, so it is not false, but a reader who takes 37
   as current is off by 3. If clarified, append after line 245; never edit line 5.
2. The reconciliation note correctly refuses to use **this index** as the count basis. Keep it
   explicit: coverage-map rows are **not** entries (40 data rows at the final snapshot vs 40
   knowledge files — the map also carries `Lessons`, `Depth instruments`, `Admission bar +
   source registry` rows), and the F11 entries never got map rows either. "Map rows" is a
   different denominator from the frontier's 12.
3. `PROVINCE.md:37-41` stops at F11 (`… F10 … 10/10 admitted). F11 — ISO/IEC 29147/30111 …
   admitted round 26`). It states no number that contradicts README, but it is stale: no F12 line
   and no deferral. `PROVINCE.md` is outside every wave-1 ownership cell — hand to the L1.

---

## 5. Open item at the final snapshot: expected list not regenerated (measured)

The entry landed *before* `corpus/instruments/knowledge-expected.txt` was refreshed, so the
audit's only failing limb is set equality. Measured, not quoted from a peer:

```console
$ wc -l corpus/instruments/knowledge-expected.txt ; grep -vc '^#' corpus/instruments/knowledge-expected.txt
41
39
$ timeout 240 python3 corpus/instruments/recheck-audit.py; echo exit=$?
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=24 broken=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=39 missing=0 unexpected=1 exit=1
unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md
exit=1
```

Read this precisely: every **form** limb is green (`strict pass=40/40`, `lines=40 total=40
pass=40`, `broken=0`); the single failure is `expected=39` vs a 40-file tree. The fix is to add
the new entry to `knowledge-expected.txt` (**40 entries / 42 lines**) and re-run; that file is in
**no** wave-1 ownership cell (`ExecExpectedList` ran PRE-STATE and its receipt states "The expected
list was NOT regenerated"), so the L1 must assign it. The README's reconciliation note (`:241-243`)
already records this exact measured state, so the README is not the defect — the missing
regeneration is.

Frontier-side re-run set (all green at `5f458a7a` except the last line):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
test -f corpus/knowledge/japanese-domestic-disclosure-workflow.md; echo $?          # 0
grep -nE '^source: S04[12] ' corpus/knowledge/japanese-domestic-disclosure-workflow.md   # 2 lines
grep -n '^ground:' corpus/knowledge/japanese-domestic-disclosure-workflow.md        # F12
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md   # 12
python3 corpus/instruments/frontier-recheck-count.py                                # entries=15 pass=15 exit=0
python3 corpus/instruments/recheck-audit.py                                         # expect=present expected=40 missing=0 unexpected=0 exit=0 (after the list refresh)
```

---

## 6. Routed items (no write scope in this seat)

1. **`corpus/instruments/knowledge-expected.txt` — regenerate (primary open item, §5).** Measured
   `unexpected=1 exit=1`; the README's `:241-243` already records it. Owner unassigned by the
   wave-1 map; L1 to assign (the natural owner is `ExecExpectedList`, whose receipt is PRE-STATE
   and explicitly says the list was not regenerated).
2. **`ScribeLesson` — R9 erratum candidate.** `lessons/round-24.md:83` and `lessons/round-26.md:55`
   give, among the refusal reasons for `chinese-criminal-thresholds-and-authorisation.md`,
   "`ground: F12` names no lane frontier item". F12 now names a real row (the Japanese workflow),
   so that phrasing is stale: the refused entry's `ground: F12` now points at the **wrong topic**
   rather than at nothing. The refusal is untouched (Q2 + Q4 + the `curl` 404 limb). Append a dated
   erratum to `lessons/round-28.md`; do not edit the historical lessons.
3. **`PROVINCE.md:37-41`** — add an F12 line or an explicit deferral (§4 adjacent item 3).
4. Resolved by the README owner, recorded here for the L1: the optional 45-day trigger-contrast
   suffix was accepted (§2.2), and the staged `ground: F13` was remapped to `F12` (§3).

---

## 7. Receipt

`.ufo/waves/round-28/receipts/ScribeFrontierNote.txt` (Rev 2) — every command with its output,
both assessed sha256 values, the timestamps, and the superseded pre-landing measurement labelled
PRE-STATE. No production file was written by this seat; the only files are this note and that
receipt.
