# ScribeSpotCheckList — round-39 non-author spot-check readiness list

Seat: `ScribeSpotCheckList`, scribe, leaf (no dispatch). Axis: coverage (C2); C1 appears only as the
receipt-reading path in item 8. Milestone: round-39. Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `480b1a505a2dfc14a4f718d16d63808247214d0a`,
claims freeze `dcd31701720a6a4929a32471a62011ed87103421`, wave1 spec/dispatch `d65d823`, HEAD
`d65d823e7c84813c192b20ee757a8761f878a61f` (lane tree still pre-integration: frontier 21, registry 55,
knowledge 50, no `corpus/instruments/r39-closure.sh`, no `final-gates/`).

## Deliverable

`.ufo/waves/round-39/wave1/ScribeSpotCheckList.checklist.md` — 19 lines, 9,131 bytes, sha256
`a86efe6a0addbadb721958fe4004938b361a0d83d9f2b3b2e67ac1effdc7dc14`. One heading
(`### Spot-check readiness (what a non-author can re-derive from committed bytes)`, the lesson section
line the L1 lands) and nine numbered items; no tables, no validation notes, no claim prose. Each item's
command strings were either executed here or taken verbatim from the frozen predicate / erratum.

## 1. Measured vs claim-derived (nothing upgraded silently)

The lane tree has none of the round-39 artifacts yet, so an after-value can only be observed on wave-1
deliverable bytes or on a scratch mirror. Labelled accordingly:

| item | status | how it was read |
|---|---|---|
| 1 capture identity | measured | `sha256sum`/`wc` on `wave1/ExecFrontierCapture.S057.txt`; manifest record read in full |
| 2 quote pins | measured | `source-recheck.py --source S057` over a scratch dir holding the capture as `S057.txt` + the manifest |
| 3 row/registry | measured (row bytes, E12, census) | row file measured; 59 re-derived on a mirror; E12 reproduced |
| 4 frontier row | measured (NF, text, cites) | append file measured; each `L<n>` cite re-read in the capture |
| 5 harness | claim (25/25); base measured (24/24) | the entry's `recheck:` line `cd`s to the real lane, so a mirror run is not representative |
| 6 binding | measured (46/46 on mirror; 45/45 at base) | `capture-binding-check.py --root <mirror>` |
| 6 audit | count measured (expected=51), exit claim | mirror run prints `expected=51 missing=0 unexpected=0` but `exit=1` because every line's `cd` targets the real lane (`cdroot_fail=50`); the lane run is the claim's counter |
| 6 census | measured on mirror (exit 0) | after entry + all four rows + round-39 capture in the mirror |
| 7 junk red | measured | re-derived 4x MISMATCH + exit 1 from the delivered manifest + capture |
| 8 C1 receipts | claim + erratum E4 | `r39-closure.sh` absent at my read; the item prints the E4/suite-author ref shape |
| 9 quiescence | measured at read time | see §3 |

## 2. Evidence — the commands and their real output

### 2.1 Base readings (lane tree)
```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                              -> 21
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md    -> 55 (S001..S055, distinct ids = 55)
$ ls corpus/knowledge/*.md | wc -l                                        -> 50
$ python3 corpus/instruments/frontier-recheck-count.py | tail -1          -> entries=24 pass=24 exit=0
$ python3 corpus/instruments/capture-binding-check.py | tail -1           -> records=45 bound=45 unbound=0
$ python3 corpus/instruments/recheck-audit.py --quiet | tail -1           -> expect=present expected=50 missing=0 unexpected=0 exit=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin kasegi | tail -1               -> exit=0 (W04 S028, W04 S029 only)
$ ls corpus/instruments/r39-closure.sh                                    -> No such file or directory
$ ls corpus/source-snapshots/round-39                                     -> No such file or directory
$ git cat-file -t 66703aca50529a35be49aa8759d04140720ad                   -> fatal: Not a valid object name
$ git cat-file -t 66703acaaff50529a35be49aa8759d04140720ad                -> commit
```

### 2.2 Capture, manifest, quotes (wave-1 bytes)
```
$ sha256sum .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt
11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
$ wc -lc .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt
275 17971
$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK occurrences=1 anchor=184-ok
exit=0
```
Manifest record: `url` = the CISA landing page; `capture_url` = `http.final_url` =
`…/2023-11/When-to-Issue-a-VEX-508c.pdf` (status 200, 235,270 raw bytes, `raw_sha256`
`cbcbd77a…50d99`, fetch `2026-10-26T19:30:55Z`, `last-modified` `2023-11-06`); `landing_page` =
54,453 raw bytes sha256 `4e6aa483…`, snapshot 3,497 bytes / 135 lines sha256 `c868f04a…`;
`sha256` == `snapshot_sha256` == the capture digest; `snapshot_bytes` 17,971; `lines` 275.
`source-recheck.py:128` reads `sha256` (`expected = record.get("sha256")`), so the
`snapshot_sha256`-named field in the capture item spec would not satisfy it on its own.

### 2.3 Row, frontier, E12, junk
```
$ awk -F'|' '{print NF}' .ufo/waves/round-39/wave1/ScribeRowS057.row.md            -> 13
$ grep -o 'https\?://[^ |]*' .ufo/waves/round-39/wave1/ScribeRowS057.row.md | wc -l -> 1
$ sha256sum .ufo/waves/round-39/wave1/ScribeRowS057.row.md
176762ea6a22ecffcd28e926ae026044bbbf59c40c530cf53a00c741e5d3c8d9  (1 line, 948 bytes)
$ for f in ScribeRowsRejected.S0{56,58,59}.row.md; do awk -F'|' '{print NF}' "$f"; grep -c 'REJECTED:' "$f"; grep -c 'flip:' "$f"; done
13 1 1  / 13 1 1  / 13 1 1
$ awk -F'|' '/^\| F22 \|/{print NF}' .ufo/waves/round-39/wave1/ScribeFrontierF22.readme.append.md -> 8
$ grep -cE '^\| F[0-9]+ \|' .ufo/waves/round-39/wave1/ScribeFrontierF22.readme.append.md            -> 1
```
Cites re-read in the capture (lines printed by me, not copied): L12-L14 `…Whether, and when, to issue
VEX information is a business decision …`; L79-L81 `…are not determined by a strict protocol.`;
L132-L135 `under_investigation` → `affected`/`not_affected` lifecycle; L136-L138 timestamp-only
reaffirmation; L183-L186 `Strictly speaking, consumers should not assume the status of an upstream
component applies …`.

Junk twin, re-derived from the delivered manifest and a byte copy of the capture:
```
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
exit=1
```

E12 (position rule), on a copy of the mirror registry with the S059 row appended after `## Paths`:
```
file  E12  S059 row outside Registry section
census_exit=1
```

### 2.4 After-state mirror (read-only copies; no lane write)
Mirror = `corpus/source-snapshots/` + `corpus/knowledge/` + `corpus/instruments/` copied from the lane,
the four row files inserted inside `## Registry` before `## Paths` (59 rows), the F22 entry at
`corpus/knowledge/cisa-when-to-issue-vex.md`, and `corpus/source-snapshots/round-39/{S057.txt,manifest.json}`:
```
$ python3 corpus/instruments/capture-binding-check.py --root <mirror> | tail -2
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
records=46 bound=46 unbound=0   exit=0
$ bash scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md | tail -3
file  W04 S028 … / file  W04 S029 … / file  ok  <mirror>/corpus/SOURCES.md   census_exit=0
$ python3 corpus/instruments/recheck-audit.py --root <mirror> --quiet | tail -3
strict pass=1/51 cdroot_fail=50 instrument_fail=0 own_fail=0
lines=51 total=51 pass=51 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=51 missing=0 unexpected=0 exit=1
```
Before the entry was copied in, the same census printed exactly one code, `E11 S057 missing used-by
corpus/knowledge/cisa-when-to-issue-vex.md` (exit 1) — so the four appends are E01-E10 clean and the
only missing piece was the entry. The audit's `exit=1`/`cdroot_fail=50` is a mirror artefact: every
entry's `recheck:` line `cd`s to the real lane, which has no round-39 capture yet. `knowledge-expected.txt`
insertion verified at line 8, between `cisa-kev-catalog.md` (L7) and `citation-bases.md` (L8);
`LC_ALL=C sort -c` on the base list → `sorted-ok`.

### 2.5 Pinned G8 digest (independent of the r39 suite)
```
$ git show 2387dcf6:corpus/instruments/r37-closure.sh | sha256sum
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d
$ sha256sum corpus/instruments/r37-closure.sh
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  (working copy identical)
```
`wave1/ExecPinnedG8Fixture.md` §2 records the same digest, `wc -lc` 1558/73132, and the round-37
receipt lines carrying it; `wave1/ExecGradedSelftestFixture.md` supplies the case-line contract I used
in item 8 (`selftest case=G<n> positive=pass mutants=<a>/<b> verdict=pass`, `selftest detail=…`,
`selftest cases=8 failures=0`).

## 3. Findings

1. **Frozen registry after-count 58 → 59.** `claims.json` C2 counted only the three rejected appends;
   four rows land (S057 + S056/S058/S059) so 55 → 59. `wave1/ScribeRowsRejected.registry-changes.md`
   already stated 55 → 59. I reported it to the L1 before writing; the L1 committed
   `.ufo/waves/round-39/claims-erratum-1.md` **E1** (after-count 59, kill-rule row reads `!= 59`). The
   checklist prints 59 and cites the erratum.
2. **The r38 judged-head hash was truncated in the frozen text.** `claims.json` counting_commands and
   the wave-1 prompts carry `66703aca50529a35be49aa8759d04140720ad` (37 chars);
   `git cat-file -t` → `fatal: Not a valid object name`. The real head is
   `66703acaaff50529a35be49aa8759d04140720ad` (40 chars) per `.ufo/waves/round-38/final-gates/all-gates.txt`
   `export-ref=` and `corpus/lessons/round-38-verifier-spotcheck.md`. Fixed by **E2**; the checklist
   uses the 40-char form.
3. **C1's counting command was unsatisfiable at J (R1 class).** G2 requires the receipt inside the
   export, while J is defined as every change except the receipt, so `--export-ref J` is 7/8 by
   construction. `ExecSuiteBuild` independently confirmed the r38-resolved shape (8/8 at the
   receipt-bearing ref; `export-ref=` names its parent); the L1 appended **E4** (verification ref Y =
   J + receipt only, J-run 7/8 documented not a kill). Item 8 prints the E4 form.
4. **The manifest's binding key is `sha256`, not `snapshot_sha256`.** The capture item spec named
   `snapshot_sha256`; `source-recheck.py` reads `sha256` and reports `manifest UNAVAILABLE
   reason=invalid-sha256` otherwise. The landed manifest carries both, so nothing is broken; item 1
   names the key a spot-check re-reads.
5. **The junk red is content-specific.** The transcript's isolation control (same J1–J4 ids, same path
   and digest, genuine sentences) prints four `OK` exit 0, and its positive control prints Q1 `OK
   normalized=markup-whitespace occurrences=1` exit 0; item 7 records both so the red cannot be read
   as a manifest or path error.
6. **Position, not style.** A Registry row appended after `## Paths` reds as `E12` (measured); item 3
   states the section bounds (L3 to L63) so the four appends are placed, not just present.
7. **Q3 is a 42-word two-sentence block** (measured); the Gate quotes its first sentence. Item 2 notes
   the split so the ≤25-word expectation is not read against the manifest assertion.
8. **Live state at my read:** `git status --porcelain` shows only the L1's untracked round-39 dispatch
   artifacts under `.ufo/waves/round-39/` (no tracked modification); `/fast/scratch/hyaku/kasegi-r37`
   and `kasegi-r38` are absent; `kasegi-r39` holds one directory per live wave-1 seat (they remove
   their own; mine removed before yield). Item 9 is the check for the judged moment, not a claim about
   this instant.
9. **Two self-reference traps removed from the landable bytes.** (a) Quoting the suite's literal
   pending marker inside item 9 would have made `grep -c '<marker>' corpus/lessons/round-39.md` return
   1 once the L1 lands the section, i.e. the checklist would have fired the very kill rule it describes;
   item 9 now names the marker without reproducing it. (b) The frozen 37-char r38-head string is not
   reproduced in item 8 either — the section says the hash was truncated and cites erratum E2 — so a
   reader cannot copy a dead hash out of the lesson. Both verbatim strings stay in this receipt
   (findings 1 and 2 here), which is where a conflict is reported to the judge.

## 4. Gates

- **C2:** items 1-7. Measured here: capture identity and digest agreement, the four quote pins, the
  S057 row shape (NF=13, one URL token equal to the manifest `url`, cells), the rejected rows'
  `REJECTED`/`flip` cells, F22 `NF=8` and its cites, the junk red, the 59-row registry on a mirror,
  binding 46/46 on a mirror, census exit 0 on a mirror, E12. Claim-derived: harness 25/25 and audit
  `exit=0` on the landed lane (their commands run at base here: 24/24, expected=50).
- **C1:** item 8 only, as receipt-reading. No `closed=` line in the deliverable is presented as this
  seat's run — the suite does not exist in the lane at my read, and the item states the command, the
  expected line and the ref rule (Y, with the J-run 7/8 documented) so the value is reproduced or the
  defect is visible.
- **Item 9** is the G6 quiescence + clean-tree live reading.

## 5. Touched surfaces

- Wrote: `.ufo/waves/round-39/wave1/ScribeSpotCheckList.checklist.md` and this receipt only.
- Scratch (removed before yield): `/fast/scratch/hyaku/kasegi-r39/ScribeSpotCheckList/` — capture and
  manifest copies, junk manifest copy, after-state mirror, drafts.
- No lane/fleet/source-tree file edited; no git or jj mutation (reads only: `git status`, `git log`,
  `git show`, `git cat-file`, `git rev-parse`); no network fetch by this seat (all bytes read from
  wave-1 deliverables); no tool installed or upgraded; pacman never invoked.
- Out of scope, other seats: the r39 suite, the source row/entry/frontier/lesson files, the errata,
  wave-2 review, integration.

## 6. Open risks

- Item 5 `entries=25` and item 6 audit `exit=0` are claim values; if the entry's `recheck:` line or the
  `knowledge-expected.txt` insertion lands differently, they red at integration. The commands in the
  checklist are the detection.
- Item 4's `22` assumes the F22 row lands inside the EOF `## Round-39 admission` section as drafted; a
  second F-row copied into a base frontier table would print 23.
- Item 8 assumes the r39 suite keeps the r38 CLI (`--export-ref`, `--selftest`, `--lane`, `--work`,
  `--scratch-root`, plain run exit 2) and bumps the receipt sentinel to `all-gates v3` as the frozen
  G2 requires (r38 emitted `v2`). If the landed suite differs, item 8's command flags need one edit
  and its expected receipt header is the contract the suite must meet.
