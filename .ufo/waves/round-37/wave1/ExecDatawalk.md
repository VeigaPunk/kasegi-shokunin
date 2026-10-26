# ExecDatawalk — round-37 C2 after-state data walk (F20 / S054)

Seat: `ExecDatawalk` (executor, leaf; no subagent, no swarm, no background job). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, observed HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0`
with 7 porcelain paths, all `.ufo/waves/round-37/*` (wave in flight; none of them mine). Judged axis:
`coverage`. Milestone: round-37.

Writes: this receipt and `/fast/scratch/hyaku/kasegi-r37/ExecDatawalk/` only. No lane, fleet, sibling-lane
or source-tree file was edited; no mutating git/jj command was run (only `git archive`, `rev-parse`,
`status`); no tool was installed. Scratch removed after the receipt was written.

Assignment: produce the complete C2 after-state data walk — the exact appended blocks the L1 lands (F20
frontier row, round-37 README admission section, PROVINCE F20 line, S054 registry row, knowledge-expected
line) — and confirm each append is end-of-file / R6-safe. Every reading below is a run over a scratch
`git archive` export of base `b56a41680cefd391868c1c370dc063c69d827e7d` (`$S/base`, no `.git`), never
over the live worktree, plus one read-only extraction of the capture seat's byte-exact receipt block.

## 0. URL correction applied (claims erratum 1)

The frozen C2 names the capture URL `https://certcc.github.io/SSVC/`; `.ufo/waves/round-37/claims-erratum-1.md`
corrects it to `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` (the "What is SSVC?" overview
tutorial). Every block below uses the corrected URL. My own pre-erratum home-page fetch is retained as
provenance only and enters no block:

```
$ curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0' https://certcc.github.io/SSVC/     # 2026-10-26T17:04:41Z
status=200 bytes=105807 redirects=0  last-modified: Fri, 23 Oct 2026 16:21:47 GMT
$ sha256sum raw.html raw2.html      # two independent fetches, 3 min apart
60c00968563c688e4ffafb7a5b9fcedf097db8459114b92185c37cd4482112ed  raw.html
60c00968563c688e4ffafb7a5b9fcedf097db8459114b92185c37cd4482112ed  raw2.html
$ python3 -c '... capture-source.py html_to_text() on each raw body ...'
7730 bytes / 286 lines / sha256 a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56
```

The raw-body digest matches ExecC2Capture's recorded home-page fetch (`ExecC2Capture.md` §0), so the home page was a
correctly-captured wrong target, not a divergent fetch — the erratum's reason holds and my pre-erratum
line numbers (L203/L204/L107-L123/L178) are retired with it.

## 1. Bytes under test

| object | measured value |
|---|---|
| lane base | `b56a4168…` → `git archive \| tar -x -C $S/base`, `export_ok`, `git rev-parse --show-toplevel` → `fatal: not a git repository` |
| `corpus/source-snapshots/round-37/S054.txt` | extracted from `.ufo/waves/round-37/wave1/ExecC2Capture.md` §3 fenced block → **32623 bytes, 518 lines, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`**, i.e. the receipt block reproduces the landed bytes exactly |
| `corpus/source-snapshots/round-37/manifest.json` | extracted from the same receipt §4 → 3989 bytes, sha256 `fabc3163dbd31d33bff6e0bccf8b86b94e081b06b3ab1f00538dd9c0a57df642`; record `url` = corrected URL, `fetched_utc` `2026-10-26T17:02:19Z`, `fetched_bytes` 143053, `snapshot_bytes` 32623, `lines` 518, quotes Q1 L259 / Q2 L277 / Q3 L473 / Q4 L68 |
| F20 entry | **stub** authored in scratch by this seat purely to exercise the instruments (`source: S054 — …`, `ground: F20`, `recheck:` cd-pinned). The real entry is `ScribeEntryF20`'s; nothing in this receipt judges its body. |

Pre-state counters on that export (the C2 predicate's own readings):

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                  -> 19
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md  -> 53
$ ls corpus/knowledge/*.md | wc -l                             -> 48
$ wc -l corpus/instruments/knowledge-expected.txt              -> 50   (48 entries + 2 comment lines; entries sorted: True)
$ python3 corpus/instruments/frontier-recheck-count.py --root $S/base | tail -1
entries=22 pass=22 exit=0
$ python3 corpus/instruments/capture-binding-check.py --root $S/base | tail -1
records=43 bound=43 unbound=0
$ python3 corpus/instruments/recheck-audit.py --root $S/base --cdroot $S/base --quiet | tail -2
expect=present expected=48 missing=0 unexpected=0 exit=0
```

(`--cdroot` alignment is needed only because 47 entries `cd` to the live lane path; on an untouched
mirror the audit prints `exit=1` from `cdroot_fail=47` with the same `pass` count — see §4.)

## 2. The five blocks to land (verbatim)

### 2.1 `corpus/README.md` — Frontier F20 row (inside the round-37 section's own frontier table)

```markdown
| F20 | SSVC: Stakeholder-Specific Vulnerability Categorization (CERT/CC, Carnegie Mellon) — stakeholder-tailored prioritization by decision points, distinct from severity and exploitability scoring | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | Read the role first, then the table: SSVC rates a vulnerability on risk to the concerned stakeholder rather than on technical severity or exploitability (S054.txt:247), and the same page ends Suppliers and Deployers at Defer, Scheduled, Out-of-cycle and Immediate (S054.txt:262-265) while Coordinators triage to Decline to act, Track, or Coordinate a response (S054.txt:270-272) and publish to Don't publish or Publish (S054.txt:274-275), so a category label means nothing without the model that produced it. A decision point is not itself a risk value — decision points and decision outcomes must be explainable to the non-expert (S054.txt:277) — and stakeholders may define their own decision points and timeframes (S054.txt:249), so cite the model and its version instead of porting a category across roles. |
```

6 cells (`awk -F'|'` → `NF=8`), no `|` inside any cell, and it matches the counter regex
`^\| F[0-9]+ \|` exactly (single space after the leading pipe).

### 2.2 `corpus/README.md` — round-37 admission section, appended at end of file (27 lines)

```markdown
## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-37 entry
`knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (Frontier F20, source S054;
source basis: CERT/CC's own "What is SSVC?" overview tutorial at
https://certcc.github.io/SSVC/tutorials/ssvc_overview/, captured
2026-10-26 under `corpus/source-snapshots/round-37/`) is recorded here as an appended amendment so
every existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F20 frontier row is listed here on the same table shape as the frontier
above.

| Area | Entry | Source basis |
|---|---|---|
| Stakeholder-specific vulnerability prioritization — SSVC (round 37) | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F20 | SSVC: Stakeholder-Specific Vulnerability Categorization (CERT/CC, Carnegie Mellon) — stakeholder-tailored prioritization by decision points, distinct from severity and exploitability scoring | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | Read the role first, then the table: SSVC rates a vulnerability on risk to the concerned stakeholder rather than on technical severity or exploitability (S054.txt:247), and the same page ends Suppliers and Deployers at Defer, Scheduled, Out-of-cycle and Immediate (S054.txt:262-265) while Coordinators triage to Decline to act, Track, or Coordinate a response (S054.txt:270-272) and publish to Don't publish or Publish (S054.txt:274-275), so a category label means nothing without the model that produced it. A decision point is not itself a risk value — decision points and decision outcomes must be explainable to the non-expert (S054.txt:277) — and stakeholders may define their own decision points and timeframes (S054.txt:249), so cite the model and its version instead of porting a category across roles. |

[r37 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 37 the frontier stands at **20/20 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at round
37. The 0/18 sentence is untouched: the lost-domain denominator still holds 0 of 18 surfaces
present, and the frontier count stays outside it.
```

### 2.3 `PROVINCE.md` — F20 line, appended at end of file

```markdown
[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — SSVC (Stakeholder-Specific Vulnerability Categorization) decision-point-based prioritization — admitted round 37; entry `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (source S054)
```

### 2.4 `corpus/SOURCES.md` — S054 registry row, inserted as line 60 (immediately after S053 at line 59, before the blank line and `## Paths`)

```markdown
| S054 | SSVC: Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ | docs | A | CERT/CC's own SSVC documentation: decision-point-based prioritization for vulnerability management, as the What is SSVC? overview tutorial states it and nothing the pages it links to state | capture corpus/source-snapshots/round-37/S054.txt (sha256 ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21, 32623 bytes, 518 lines): Q1 L259 the definition sentence (SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders); Q2 L277 the rule binding decision points and decision outcomes to explainability; Q3 L473 the contrast with other vulnerability scoring systems; Q4 L68 the CISA BOD 26-04 Response Model navigation entry, a navigation-only mention with no body sentence on this page; L247 the technical-severity and exploitability contrast in fuller form; L261-L275 the Supplier, Deployer and Coordinator prioritization categories; L249 the caveat that stakeholders define their own decision points and timeframes; manifest corpus/source-snapshots/round-37/manifest.json binds this file by sha256 and carries the four pinned quotes | SSVC is a stakeholder-tailored decision-point system for prioritizing vulnerability-management actions — it rates risk to the concerned stakeholder rather than technical severity or exploitability, and gives Suppliers and Deployers different outcome categories than Coordinators, so cite the model and its version rather than porting a category across roles | mined | 2026-10-26 | 90d | corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |
```

11 cells (`awk -F'|'` → `NF=13`), no `|` inside any cell, and the source cell carries exactly one
`https://` token — `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` — byte-equal to the manifest
record's `url`, which is what `capture-binding-check.py` rule B5 requires.

### 2.5 `corpus/instruments/knowledge-expected.txt` — one line at line 40

```text
corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
```

Sorted position, measured: line 39 `corpus/knowledge/source-tree-loss-2026-09-28.md`, line 40 the new
entry, line 41 `corpus/knowledge/statutory-authorization-and-unauthorized-access.md`; the list's
`sorted?` invariant stays `True` and the file becomes 51 lines / 49 entries.

## 3. Append shape — R6 confirmed per file (measured diffs, 0 deletions)

```
$ for f in corpus/README.md PROVINCE.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt; do
    printf '%-45s %s deleted=%s\n' "$f" "$(diff base/$f mirror/$f | head -1)" "$(diff base/$f mirror/$f | grep -c '^<')"
  done
corpus/README.md                              hunk=398a399,425 deleted=0
PROVINCE.md                                   hunk=78a79     deleted=0
corpus/SOURCES.md                             hunk=59a60     deleted=0
corpus/instruments/knowledge-expected.txt     hunk=39a40     deleted=0
```

| block | shape | R6 verdict |
|---|---|---|
| 2.1 F20 row | new row inside a table created by 2.2, at EOF of the file's last line+1 | **EOF-safe** — no pre-existing line is edited, moved, or reflowed |
| 2.2 README section | `398a399,425` = pure append after the file's last line (the r35 amendment paragraph) | **EOF-safe**; the r35/r33/r31 paragraphs keep their line numbers |
| 2.3 PROVINCE line | `78a79` = pure append after the F19 line | **EOF-safe** |
| 2.4 S054 row | `59a60` = one row inserted at the end of the registry table | **table-append**: no existing row changes; lines after 60 shift by one, exactly as every earlier registry append did (r36: `SOURCES.md +5`) |
| 2.5 expected line | `39a40` = sorted insertion | **not** EOF, deliberately: the file's header states "Sorted list from the working tree" and `sorted?` measures `True`; an EOF append leaves the audit green (`expected_mismatch` is set-based) but breaks the file's own invariant, so sorted insertion is the only conforming shape. Measured both ways in §4. |

## 4. Instrument readings — base vs assembled tree

| counter (frozen C2 command) | base `b56a4168` | assembled | note |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 19 | **20** | F20 row |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 53 | **54** | S054 row |
| `grep -rlE '^source: S054 ' corpus/knowledge \| wc -l` | 0 | **1** | requires a trailing space after the id (see §5.1) |
| `ls corpus/knowledge/*.md \| wc -l` | 48 | **49** | |
| `knowledge-expected.txt` lines / entries | 50 / 48 | **51 / 49** | §3 |
| `frontier-recheck-count.py --root … \| tail -1` | `entries=22 pass=22 exit=0` | **`entries=23 pass=23 exit=0`**, with `PASS F20 knowledge/ssvc-… ids=S054 exit=0` | |
| `capture-binding-check.py --root … \| tail -1` | `records=43 bound=43 unbound=0` | **`records=44 bound=44 unbound=0`**; `MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0` | B5 binds my row to the manifest URL |
| `source-recheck.py --manifest …/round-37/manifest.json --source S054` | n/a | **exit 0**: `S054:sha256 OK`, `Q1 OK occurrences=1 anchor=259-ok`, `Q2 … 277-ok`, `Q3 … 473-ok`, `Q4 … 68-ok` | four pins verify against the landed capture |
| `recheck-audit.py --quiet` (cdroot-aligned) | `strict pass=48/48 … expected=48 exit=0` (`pass=48/48`) | **`strict pass=49/49 cdroot_fail=0 … pass=49/49 … expected=49 missing=0 unexpected=0 exit=0`** | the C2 counter shape |

Two controls, both on scratch copies of the assembled tree:

```
# A — entry landed but expected list NOT regenerated
expect=present expected=48 missing=0 unexpected=1 exit=1        # the sync is load-bearing
# B — expected line appended at EOF instead of sorted
eofappend entries sorted? False count 49
expect=present expected=49 missing=0 unexpected=0 exit=1        # audit is set-based, so only the file's invariant fails
```

## 5. Cross-seat constraints measured while assembling (the L1 lands under these)

1. **The entry's `source:` header needs a trailing space after the id.** `grep -rlE '^source: S054 '` (the
   frozen counter) matched **0** files with a header of exactly `source: S054` and **1** with
   `source: S054 — <url> — capture …` (F19's shape). `frontier-recheck-count.py`'s own `SOURCE_LINE` regex
   (`^source:\s*(S\d{3,})`) accepts either, so only the claim's counter forces the space.
2. **The entry's `recheck:` line must be cd-pinned to the lane root** (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 …`,
   as F19 has it). With an unpinned stub the audit's `cwd` limb fails (`cwd_fail=1`, `foreign_exit=2`,
   `strict pass=48/49`); with the pin, `cwd_fail=0` and `strict pass=49/49`. That limb gates the claim's
   `recheck-audit --quiet` exit 0.
3. **Rule B5 binds the row to the manifest, not the other way round**: the manifest record's `url` must
   byte-equal the single `https://` token in the row's source cell. A row carrying the home URL (or two
   tokens) is rejected even with correct capture bytes — which is why the corrected URL is load-bearing in
   block 2.4.
4. **Pins**: Q1 L259, Q2 L277, Q3 L473, Q4 L68 all report `occurrences=1` and `anchor=<n>-ok` against the
   32623-byte capture. Q4 is a **navigation-only** mention ("CISA BOD 26-04 Response Model"); the page
   carries no BOD 26-04 body sentence, and my blocks claim none.
5. **`used-by` must land in the same commit** as the row: `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`.
6. **"modular" does not occur in the capture** (`grep -ciF modular` → 0). My teaches cell therefore says
   "decision-point system", not "modular decision-point system"; if the prescribed scribe wording keeps
   "modular", it is an inference (supportable from the "Compound Decision Points" / "Decision Point Groups"
   navigation entries) and should be marked as one rather than quoted.

## 6. Risks and limits

- **Capture authority.** Every number in block 2.4 (sha256, 32623 bytes, 518 lines, L259/L277/L473/L68) is
  taken from ExecC2Capture's byte-exact receipt, and I re-derived the capture digest from that receipt's
  fenced block, so the block and the bytes agree today. If the L1 lands different bytes, the row's four
  numeric fields must be re-derived (`sha256sum` + `wc -l` + `grep -n`), not pasted.
- **Pre-existing gap I did not close:** `corpus/README.md` never recorded the 19/19 frontier state (r36
  added the F19 row and a trailing blank line, no amendment paragraph and no F19 coverage-map row). My
  section states 20/20 with `F19 at round 36, F20 at round 37` and adds a coverage-map row only for F20;
  retro-adding an F19 coverage row would edit the historical record, so it is left as it stands.
- **The audit's `--cdroot` dependency** (47 entries cd to the live lane path) means a mirror never reaches
  `exit=0` without rewriting those paths; I report the assembled `strict pass=49/49 … exit=0` from a
  scratch copy whose 47 lane paths were rewritten to the mirror root, and the untouched-mirror reading
  (`strict pass=2/49 cdroot_fail=47`, `pass=49/49`, `cwd_fail=0`, `exit=1`) alongside it. The `pass` count —
  the one that moves with the blocks — is 49/49 in both, and nothing about the five blocks depends on the
  rewrite. Base under the same alignment reads `strict pass=48/48 cdroot_fail=0 … exit=0`.
- Not measured here, by design: the F20 entry's body (ScribeEntryF20), the junk twin, the census instrument,
  the C1 suite, and the capture's freshness upstream. No claim is made on them.

## 7. Tooling and scratch

No tool installed or upgraded (`pacman` never invoked). Scratch `/fast/scratch/hyaku/kasegi-r37/ExecDatawalk/`
(export, mirrors, controls, extracted capture/manifest) removed after this receipt was written.

Artifact: `.ufo/waves/round-37/wave1/ExecDatawalk.md`.
