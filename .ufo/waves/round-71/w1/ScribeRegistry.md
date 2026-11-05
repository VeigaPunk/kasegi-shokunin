# ScribeRegistry — round-71 registry and frontier bookkeeping for F49 / S106

Seat scope (the only four production files this seat may edit, under
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`): `corpus/SOURCES.md`,
`corpus/README.md`, `corpus/instruments/knowledge-expected.txt`, `PROVINCE.md`.
No commit, push, checkout, reset, or mutating `jj` command was run by this seat.

## 1. What landed (diff vs base `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`)

`git diff --numstat 4e33119… -- <four files>`:

```
2	0	PROVINCE.md
23	0	corpus/README.md
2	0	corpus/SOURCES.md
1	0	corpus/instruments/knowledge-expected.txt
```

Per file (added / removed lines):

| file | + | − | tip line count | tip sha256 |
|---|---|---|---|---|
| `corpus/SOURCES.md` | 2 | 0 | 262 | `1d4d4e747ce11f8cbfb798d9ddc8f9a1080757c5bbe14e5c1a4dfcf1b84fc7f1` |
| `corpus/README.md` | 23 | 0 | 1120 | `85715e2f8e37de5dfc158ef3b304429e755f367fd3aa1cb848749f3c6e93e034` |
| `corpus/instruments/knowledge-expected.txt` | 1 | 0 | 89 | `644160c94c5ec774e24742edbdddca7893a634e1cd9069b3ff027338465b7d59` |
| `PROVINCE.md` | 2 | 0 | 215 | `cb328ed292cfc398671886859b522bb3e5f05abb035c6dc8b1cb1cbd7dbc610b` |

The two `corpus/SOURCES.md` additions are (a) the `| S106 |` registry row and (b) one
`## Registry changes` bullet. The two `PROVINCE.md` additions are a blank separator plus
the single `[r71 Frontier amendment, appended 2026-11-05] F49 - …` line.

## 2. `corpus/SOURCES.md` — the S106 row

Appended as the last row of the `## Registry` table (tip line 118), in the 11-column
shape `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck |
used-by`. Measured shape (`awk -F'|'` on the row): `NF=13`, i.e. 11 cells, and no cell
contains a literal `|` (checked cell-by-cell; none printed). The source cell carries
exactly one `https://` token, `https://www.zerodayinitiative.com/about/`, matching the
manifest's `url` and `capture_url` byte-for-byte (capture-binding rule B5).

| cell | value |
|---|---|
| id | `S106` |
| source | `TrendAI Zero Day Initiative (ZDI), About — https://www.zerodayinitiative.com/about/` |
| kind | `docs` |
| tier | `A` |
| scope | ZDI's own statements about its vendor-agnostic acquisition programme's disclosure process and vendor coordination (120-day standard window; 30/60/90-day shortening for flaws from incomplete or problematic patches; escalation to a limited public advisory after 15 business days of vendor silence; full-advisory-after-a-patch vs limited-advisory-when-no-fix; researcher validation → formal monetary offer → payment → vendor coordination → credit or anonymity); explicitly not a platform severity ladder, not a coordinator's statutory timeline, not any single advisory instance |
| anchor | capture `corpus/source-snapshots/round-71/S106.txt` (sha256 `291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db`, 148 lines, 15004 snapshot bytes, fetched 2026-11-05T01:27:03Z); 15 pinned quotes Q01-scope L28, Q02-acquisition L31, Q03-guarantee L47, Q04-validation L49, Q05-window L70, Q06-shortened L70, Q07-escalation L70, Q08-limited L52, Q09-full L51, Q10-offer L60, Q11-nobacklog L62, Q12-credit L61, Q13-dossier L69, Q14-refusal L72, Q15-nolimit L60; the served page shows no visible publication or revision date, the only date signal being a 2026 copyright line at L127 |
| teaches | Read an acquisition programme's own disclosure-process statements as that programme's policy, not as a universal deadline: the 120-day standard window and the 30/60/90-day shortening for incomplete or problematic patches come from the same vendor-coordination paragraph (S106.txt:70), the 15-business-day escalation is ZDI's own statement (S106.txt:70), and the advisory form follows the patch outcome (S106.txt:51, S106.txt:52) |
| status | `mined` |
| opened | `2026-11-05` |
| recheck | `180d` |
| used-by | `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` |

### The Fuzzilli lead was NOT retired

`## Leads (unopened)` still carries exactly one line, unchanged:

```
- Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.
```

Judgment recorded: S106 is TrendAI ZDI's About page, not the Fuzzilli primary
documentation, so the Fuzzilli lead is not opened by this round and stays a lead. The
`## Registry changes` bullet says so explicitly. (The spec's parenthetical "it is NOT —
leave it" agrees with this reading; the judgment is stated rather than assumed.)

### `## Registry changes` bullet

One bullet appended at end of file, recording old → new (registry 105 → 106), the capture
digest `291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db`, the anchor
path and its 15 quote anchors, `registry 105->106, knowledge 86->87`, the F49 admission,
the not-retired Fuzzilli lead, and "No pre-existing status, recheck, used-by, id or URL
cell changed."

## 3. `corpus/README.md` — Round-71 admission section

Appended at end of file (never inserted). `git diff` shows the first 1097 lines
byte-identical to base, and the F47 and F48 rows byte-identical (both checked with
`==` on the extracted rows) — the round-70 M70-1 defect shape (a whole-row replacement
that drops the prior row) is not reproduced.

The appended block is 23 lines: heading `## Round-71 admission — coverage map row and
Frontier F49 (2026-11-05)`, an R6 amendment paragraph, the three-cell coverage-map row
(`| Area | Entry | Source basis |` + the round-71 row), the six-cell frontier table
(`| id | topic | status | entry | sources | next |`) carrying the `| F49 |` row in F48's
shape, a scope-limit paragraph, and a `[r71 amendment, appended 2026-11-05] The frontier
as of round 71 is F01-F49 admitted: F48 at round 70 and F49 at round 71.` line.

The F49 row: topic = TrendAI ZDI's own disclosure process and vendor coordination
(acquisition-programme flow; 120-day standard window with its 30/60/90-day shortening for
flaws from incomplete or problematic patches; escalation to a limited public advisory
after 15 business days of vendor silence; full advisory after a patch vs limited
advisory when no fix arrives); status `admitted`; entry
`knowledge/zdi-disclosure-process-and-vendor-coordination.md`; sources `S106`; next =
read the three vendor-coordination numbers in their own paragraph (S106.txt:70) and the
advisory form from the patch outcome (S106.txt:51, S106.txt:52), with F02/S075, F13 and
F11/F38 retaining their held ground.

### R104 (row-count before/after)

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md      # before (base 4e33119)
48
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md      # after
49
```

48 → 49, exactly before+1. No pre-existing row disappeared: a set comparison of the 48
base `| F<n> |` rows against the 49 tip rows reports `base F rows missing at tip: []`
and `new F rows: ['| F49 |']`.

## 4. `corpus/instruments/knowledge-expected.txt`

`corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` inserted in the
file's sort order, directly after `corpus/knowledge/zdi-disclosure-policy.md` (C-locale
byte order: `zdi-disclosure-policy.md` < `zdi-disclosure-process-and-…`, since `p` < `r`
at the first differing byte after `zdi-disclosure-p`).

```
$ wc -l < corpus/instruments/knowledge-expected.txt
89
$ grep -vc '^#' corpus/instruments/knowledge-expected.txt
87
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt ; echo $?
0
```

88 → 89 lines, 86 → 87 entries, sort exit 0. Set comparison: `missing entries: []`,
`new entries: ['corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md']`.

## 5. `PROVINCE.md`

One line appended at end of file (R6), after a blank separator:

```
[r71 Frontier amendment, appended 2026-11-05] F49 - TrendAI ZDI's own disclosure process and vendor coordination on its About page (the 120-day standard coordination window, the 30/60/90-day shortening for flaws from incomplete or problematic patches, the 15-business-day escalation to a limited public advisory, the full-advisory-after-a-patch against the limited-advisory-when-no-fix choice, and the researcher flow of validation, formal monetary offer, payment, vendor coordination and credit or anonymity); admitted on source S106 in corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md. Scope limit: one acquisition programme's own statements — not a platform severity ladder, not a coordinator's statutory timeline, and not any single advisory instance; F02/S075 keeps the ZDI policy body, F13/S043-S045 keep the platform ladders and F11/F38 keep the ISO division of labour. Documentation only; live-target testing remains refused.
```

`base[:213] == tip[:213]` → `True` (every pre-existing line keeps its number and bytes).
The separator is the ASCII hyphen-minus `-` as the spec's template shows
(`[r71 Frontier amendment, appended 2026-11-05] F49 - ...`); the 29 pre-existing
amendment lines in this file use an em dash, so this line is the one hyphen-form line —
flagged here rather than silently harmonized, because the spec fixed the string.

## 6. Verification commands and exit codes (all measured on the landed tree)

| command | exit | observed output |
|---|---|---|
| `python3 corpus/instruments/frontier-recheck-count.py` | **0** | `FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106`; `FRONTIER-PASS F49 ids=S106`; `entries=52 pass=52 exit=0` |
| `python3 corpus/instruments/capture-binding-check.py` | **0** | `AUDIT records=85 with_url=85 with_fetched_utc=47 with_archival=38 snapshot_dirs=44 manifest_dirs=44 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt`; `records=85 bound=85 unbound=0` (the round-71 record is now `url_bound=1`; base had `no-row record=S106` → exit 1) |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **0** | `106` (base 105) |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **0** | 6 inherited `W04` lines (S028, S029, S072, S076, S080, S085) + `kasegi ok …/corpus/SOURCES.md`. No `E01`–`E12` line. The census's E11 used-by limb passes because `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` now exists on disk (ScribeF49's file, sha256 `6f304a052190d988b189ed82d547b0ba53562fc6837fa3dd52a8dbfb87986684`). |

Supporting counts: `sources-census.sh census` on the tip tree prints `rows 106`
(`tier.A 95 / tier.B 5 / tier.C 6`, `status.mined 87 / status.rejected 19`); the same
command on a base-`4e33119` clone prints `rows 105` (`tier.A 94`, `status.mined 86`).
`ls corpus/knowledge/*.md | wc -l` = 87 (base 86).

**No non-zero census exit and no blocker.** Every required command exits 0.

### Frozen C2 after-values all reproduce

`FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106` ✓;
`entries=52 pass=52 exit=0` ✓; `records=85 bound=85 unbound=0` ✓; knowledge-expected
89 lines / 87 entries, `sort -c` exit 0 ✓; 87 files under `corpus/knowledge/` ✓;
frontier rows 49 ✓; registry rows 106 ✓; census exit 0 ✓. F49 is present in
`corpus/README.md` naming `S106` and `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`
(grep: 1 hit for the entry path, and the F49 row's sources cell is `S106`).

## 7. R6 line-shift disclosure (measured, not asserted)

The `| S106 |` row is inserted at the end of the `## Registry` table (tip line 118), so
every line below it moves down by one. Measured against base `4e33119`:

* `base[:117] == tip[:117]` → `True` (nothing above the insert changed).
* Cited SOURCES.md lines are byte-identical, one number lower:
  base 137 → tip 138 (exact-line sha256 `dbd3f08e97adf982…` at both), base 142 → tip 143
  (`01ba4719c80b6fe9…` at both), base 157 → tip 158 (`01ba4719c80b6fe9…`), base 246 →
  tip 247 (`01ba4719c80b6fe9…`), and the `## Leads (unopened)` Fuzzilli lead base 169 →
  tip 170 (`0dd9b02c6cbc9c9a…` at both).
* `anchorcheck.py` verdict classes are unchanged. Base clone and tip both print
  `corpus/SOURCES.md: 10 in-range cite instances, 0 bad; … BASE-ABSENT=1` and
  `corpus/README.md: 4 in-range cite instances, 0 bad; … BASE-ABSENT=34`; `PROVINCE.md`
  is 0/0 at both. The `exit=1` on `corpus/README.md` and `corpus/SOURCES.md` is
  pre-existing at base (BASE-ABSENT=34 / =1 come from `S0xx.txt` cites under the absent
  `/home/vgpnk/Projects/the-bounty-hunter` mirror), not introduced here.
* The lane's own precedent for this shape is the round-58 S091 bullet ("141 at base, 142
  at tip after the one-row insert; exact-line sha256 … at base and tip") and the round-70
  S104/S105 two-row insert; the `## Registry changes` bullet follows that convention and
  states the shift with the per-line digests.

One consequence worth flagging to the L1: three `corpus/README.md` cites
(`corpus/SOURCES.md:137` at README:857 and README:921, `corpus/SOURCES.md:142` at
README:887) now resolve one line earlier than before the insert. Their *anchor* text
still points at the same lead/sweep content in the sense the cites were written for
(the round-47 lead line and the CISA-ADP list-page lead both live in the `## Search log`
/ `## Leads` region and are unchanged byte-for-byte), but the literal printed line at
`corpus/SOURCES.md:137` is now the "2025 CWE Top 25 method and interpretation" bullet
rather than the "Round-23 official-text follow-up" bullet, and `:142` is now the "CISA
known-exploited-vulnerabilities sweep" bullet rather than an empty line. Re-pointing
those three cites would mean editing existing lines of another file's cited anchors;
this seat owns `corpus/README.md`, so it could do it, but the cites were authored as
"round-47 lead at `corpus/SOURCES.md:137`" / "list-page lead at `corpus/SOURCES.md:142`"
and the *lead* content they describe is not what lives at those numbers now (it was
already not at those numbers at base — the same +N drift exists at base from the
round-55/58/67/70 inserts). I did not renumber them: the pre-existing drift is a
round-55-era artifact, and renumbering only this round's +1 would leave the cites
pointing at the same content they pointed at before, which is what the R6 invariant
requires. Recorded here so the L1 can decide.

## 8. Dependency and coordination

* The F49 row, the S106 `used-by` cell, the knowledge-expected path and the README F49
  row all depend on `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`
  existing on disk. That file is owned by seat **ScribeF49** and landed during this wave
  (256 lines, sha256 `6f304a052190d988b189ed82d547b0ba53562fc6837fa3dd52a8dbfb87986684`);
  its header is `source: S106 — https://www.zerodayinitiative.com/about/ — …` and its
  `recheck:` line selects `--manifest corpus/source-snapshots/round-71/manifest.json
  --source S106`, which is why `FRONTIER-PASS F49 ids=S106` binds. This seat wrote no
  byte of that file.
* Manifest quote cross-check performed by this seat against the committed capture
  (read-only): all 15 quotes occur on their manifest anchor line. Q01-scope's 7-word
  text occurs at line 28 (its anchor) **and** again at line 102; the other 14 occur
  exactly once, each on its anchor line. This is a property of the committed capture and
  manifest (both pre-existing in `4e33119`), not of my edit — the registry row names the
  anchor lines only.
* L1 died on a provider failure and the run-15 wrap-up exported the working tree as
  commit `453275f` ("preserve in-flight work at hyaku run-15 wrap-up; not a landed
  round"). That commit captured my four files mid-flight, which is why `HEAD` moved from
  `4e33119` to `453275f` during this seat's run and why `git status` shows only
  `M corpus/SOURCES.md` (the `## Registry changes` bullet, appended after the export).
  This seat made no commit; `453275f` was not created by this seat. The L1 must
  integrate the `M corpus/SOURCES.md` change together with the four files as they
  currently stand.

## 9. Out of scope / not done by this seat

* `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` — ScribeF49's file;
  not written or edited here.
* `## Leads (unopened)` Fuzzilli line — deliberately left in place (not retired).
* The three `corpus/README.md` cites of `corpus/SOURCES.md:137` / `:142` — not renumbered;
  see §7 for the measurement and the reason.
* `corpus/lessons/round-71.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md` — not
  touched by this seat.

## 10. Tooling

No package was installed or upgraded by this seat, so no tool/version/channel row is
owed. Everything above used the host's existing `git`, `python3` (3.14.8),
`awk`/`grep`/`sed`, and the lane's own `corpus/instruments/*.py` plus the fleet's
`scripts/sources-census.sh`. All scratch work lived under
`/fast/scratch/hyaku/kasegi-r71/ScribeRegistry/` (a `--shared` clone of the lane at
`4e33119` for base measurements, plus base/tip exports) and was removed before this
report was written; nothing outside the four named files and this report was written.
