# ReviewC2 — round-70 C2 re-measurement from committed bytes (wave w1)

Seat: ReviewC2 (leaf reviewer, C2 only). Measured 2026-11-04 on the lane host.
Revisions: base `e7c02bddaa32a4a70afb2e6278f108e03dca067c`; C2 landing `b4afd8a0206b23a69d8cd65d92070cdfcd4680a7`
(verified direct child of base); claims frozen at `e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`
(`.ufo/waves/round-70/claims.json` and `.ufo/waves/round-70/controls/pins-r70.txt` read first).
Method: `git -C <lane> archive <rev> | tar -x -C <scratch>` into `/fast/scratch/hyaku/kasegi-r70/ReviewC2/base`
(13992 files) and `.../ReviewC2/export` (13995 files); every command below ran inside those exports against
committed bytes only. No lane file written except this report; no git/jj mutation; no tool installed or
upgraded (pacman guard respected, none needed). Binaries the counters resolved: python3 3.14.8,
sort -> /usr/bin/sort (GNU coreutils 9.12), git 2.56.0 — same host binaries the frozen measurements used.

## 0. Pin verification (exported bytes vs controls/pins-r70.txt)

```
9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350  export/corpus/source-snapshots/round-70/S105.txt
d479c4954675b52c1ae49901efb1c780f686d686c96f6f24e4ab31d660fea72f  export/corpus/knowledge/github-advisory-database-curation-semantics.md
```
Both match the frozen pins. `wc -c`/`wc -l` S105.txt: 22791 bytes, 656 lines — matches the S105 anchor cell,
manifest (`bytes: 616388` is fetched bytes; snapshot 22791) and entry header.

## 1. Frozen counting commands — BASE e7c02bd (before)

```
$ python3 corpus/instruments/frontier-recheck-count.py
FRONTIER-CENSUS rows=47 admitted=47 closed=47 problem-rows=0 registry=103
FRONTIER-PASS F01 ids=S001,S002
  ... F02..F46 elided: byte-identical to the landing run (mechanical diff in §3) ...
FRONTIER-PASS F47 ids=S103
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
  ... PASS F02..F47 elided (identical between runs); no F48 line ...
PASS     F47  knowledge/github-global-security-advisories-rest-api.md ids=S103        exit=0
entries=50 pass=50 exit=0
[exit=0]
$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
  ... round-24..round-69 elided: byte-identical between runs (mechanical diff in §3); 42 MANIFEST lines, no round-70 ...
MANIFEST round-69 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=83 with_url=83 with_fetched_utc=45 with_archival=38 snapshot_dirs=42 manifest_dirs=42 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=83 bound=83 unbound=0
[exit=0]
$ wc -l < corpus/instruments/knowledge-expected.txt
87
$ grep -vc '^#' corpus/instruments/knowledge-expected.txt
85
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
(no output)
[exit=0]
$ ls corpus/knowledge/*.md | wc -l
85
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md
47
```

## 2. Frozen counting commands — LANDING b4afd8a0 (after)

```
$ python3 corpus/instruments/frontier-recheck-count.py
FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105
FRONTIER-PASS F01 ids=S001,S002
  ... F02..F47 elided: byte-identical to the base run ...
FRONTIER-PASS F47 ids=S103
FRONTIER-PASS F48 ids=S105
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
  ... PASS F02..F47 elided (identical between runs) ...
PASS     F48  knowledge/github-advisory-database-curation-semantics.md ids=S105        exit=0
entries=51 pass=51 exit=0
[exit=0]
$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
  ... round-24..round-69 elided (identical between runs) ...
MANIFEST round-69 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-70 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=84 with_url=84 with_fetched_utc=46 with_archival=38 snapshot_dirs=43 manifest_dirs=43 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=84 bound=84 unbound=0
[exit=0]
$ wc -l < corpus/instruments/knowledge-expected.txt
88
$ grep -vc '^#' corpus/instruments/knowledge-expected.txt
86
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
(no output)
[exit=0]
$ ls corpus/knowledge/*.md | wc -l
86
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md
48
```

## 3. Mechanical diff of the two counter runs (whole outputs diffed; only deltas shown)

```
--- frontier-recheck-count.py BASE -> LANDING
-FRONTIER-CENSUS rows=47 admitted=47 closed=47 problem-rows=0 registry=103
+FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105
+FRONTIER-PASS F48 ids=S105
+PASS     F48  knowledge/github-advisory-database-curation-semantics.md ids=S105   exit=0
-entries=50 pass=50 exit=0
+entries=51 pass=51 exit=0
--- capture-binding-check.py BASE -> LANDING
+MANIFEST round-70 records=1 url_bound=1 fetched=1 archival=0
-AUDIT records=83 with_url=83 with_fetched_utc=45 with_archival=38 snapshot_dirs=42 manifest_dirs=42 ...
+AUDIT records=84 with_url=84 with_fetched_utc=46 with_archival=38 snapshot_dirs=43 manifest_dirs=43 ...
-records=83 bound=83 unbound=0
+records=84 bound=84 unbound=0
```
F01–F47 and MANIFEST round-23..round-69 lines are byte-identical between the runs; nothing else moved.

## 4. Frozen value check (claims.json C2 vs measured)

| limb | frozen before | measured base | frozen after | measured landing |
|---|---|---|---|---|
| FRONTIER-CENSUS | rows=47 admitted=47 registry=103 | rows=47 admitted=47 closed=47 problem-rows=0 registry=103 | rows=48 admitted=48 closed=48 problem-rows=0 registry=105 | rows=48 admitted=48 closed=48 problem-rows=0 registry=105 |
| entries | 50 pass=50 | entries=50 pass=50 exit=0 | entries=51 pass=51 exit=0 | entries=51 pass=51 exit=0 |
| records | 83 bound=83 | records=83 bound=83 unbound=0 | records=84 bound=84 unbound=0 | records=84 bound=84 unbound=0 |
| knowledge-expected | 87/85 | 87/85, sort -c exit 0 | 88/86 sort-clean | 88/86, sort -c exit 0 |
| knowledge files | 85 | 85 | 86 | 86 |
| frontier rows grep | 47 | 47 | 48 | 48 |
| census validate | exit 0, six W04 | exit 0, six W04 (§7) | exit 0 | exit 0, six W04 (§7) |

Every frozen after-value reproduces from the landed commit; every before-value reproduces from base.

## 5. SOURCES.md S104/S105 row audit (landing export)

`awk -F'|` NF on both rows: 13 (= 11 columns; an embedded `|` would push NF≥14, so no pipe inside any cell).
Id continuity: base ids exactly `S001..S103` (103, contiguous, 0 dupes); landing exactly `S001..S105`
(105, contiguous, 0 dupes) — S104/S105 are the next unused ids. Cells:

```
S104: docs | C | "Whether ENISA's EU Vulnerability Database publishes a line-anchorable API reference..." |
      anchor: Live fetch 2026-11-05 (HTTP 200, 3062 bytes, sha256 6fb32b61...a38d5): SPA shell, zero
      "endpoint"/"/api/" occurrences; byte-identical to the round-69 receipt |
      teaches: REJECTED: ... flip: statically served/line-anchorable rendering appears ... |
      rejected | 2026-11-05 | 180d | —
S105: docs | A | curation semantics scope ... not REST S103, not instance S068 |
      anchor: capture corpus/source-snapshots/round-70/S105.txt (sha256 9dd51a8e...e3350, 656 lines,
      22791 snapshot bytes over 616388 fetched, fetched 2026-11-05T00:14:43Z; classes L568-608, sources
      L573-582, review gate L584-585, ecosystems L586-597, GHSA L611-616, CVSS L621-628, EPSS L639-640,
      community L642-643) |
      teaches: class before fields; NVD imports "not checked for validity or completion" (:602); malware
      no fix version (:571); EPSS percentiles refresh only when significantly different (:639) |
      mined | 2026-11-05 | 180d | corpus/knowledge/github-advisory-database-curation-semantics.md
```

Round's claimed cells (SOURCES.md round-70 changelog): S104 "(docs, scoped tier C, rejected, opened
2026-11-05, recheck 180d, used-by —)"; S105 "(docs, scoped tier A, mined, opened 2026-11-05, recheck 180d,
used-by corpus/knowledge/github-advisory-database-curation-semantics.md)". Measured tier/status/opened/
recheck/used-by match both rows exactly. used-by resolution: the entry file exists in the export (8726
bytes) and census validate raises no E11; S105's entry header cites `source: S105` with the pinned sha.

## 6. corpus/README.md F48/F47 (landing export)

`grep -n '^| F4[78] ' corpus/README.md` → F47 at :1087, F48 at :1097. The appended section
"## Round-70 admission — Frontier F48 (2026-11-05)" carries the F48 row naming
`S105` and `knowledge/github-advisory-database-curation-semantics.md`; the counter's PASS F48 line agrees.
F47 row diff (entire README row change, base → landing) is one clause of the `next` cell:

```
- ... database curation semantics ("About the GitHub Advisory database") are unopened and are not ground here. |
+ ... database curation semantics ("About the GitHub Advisory database") are held by F48/S105. |
```

No other byte of the F47 row changed (git diff shows this single-line replacement). The round's record of
the handoff: the new entry's `ground:` line — "F47/S103 holds the REST read interface and its filter
defaults; this entry is the curation semantics F47 explicitly left unopened" — and F47's own next cell;
the SOURCES.md changelog records "Frontier F48 admitted in corpus/README.md ... No pre-existing status,
recheck, used-by, id or URL cell changed" (its enumeration omits `next`, so it stays literally true).
Observation (non-blocking): the changelog never names the F47 `next`-cell clause explicitly.

## 7. Census limb — sources-census.sh validate (script at /home/vgpnk/Projects/shokunin/scripts/sources-census.sh)

The frozen command's `--root` targets the live fleet root (the lane export carries no fleet shokunin.conf),
so the census ran two ways:

```
1) verbatim:  sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
     kasegi W04 S028 / S029 / S072 / S076 / S080 / S085 (six inherited W04 warnings)
     kasegi ok .../kasegi-shokunin/corpus/SOURCES.md      exit=0
2) committed bytes: mini fleet root /fast/scratch/hyaku/kasegi-r70/ReviewC2/fleetroot{,-base}/ with a
   one-lane shokunin.conf (kasegi row copied verbatim from fleet shokunin.conf:46) and the export as
   kasegi-shokunin/:
     landing: same six W04 + ok line, exit=0
     base:    same six W04 + ok line, exit=0
```
Census exits 0 at round end from committed bytes (landing), from base, and verbatim against the live root;
exactly the six inherited W04 warnings at all three, no E-codes.

## 8. 19 pinned quotes — source-recheck (landing export)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-70/manifest.json --source S105
S105:sha256 OK
S105:Q01-purpose OK occurrences=1 anchor=558-ok
S105:Q02-osv OK occurrences=1 anchor=567-ok
S105:Q03-sources OK occurrences=1 anchor=573-ok
S105:Q04-reviewed-gate OK occurrences=1 anchor=584-ok
S105:Q05-registry-gate OK occurrences=1 anchor=585-ok
S105:Q06-swift OK occurrences=1 anchor=597-ok
S105:Q07-unreviewed-auto OK occurrences=1 anchor=601-ok
S105:Q08-unreviewed-noalert OK occurrences=1 anchor=602-ok
S105:Q09-malware-source OK occurrences=1 anchor=604-ok
S105:Q10-type-malware OK occurrences=1 anchor=606-ok
S105:Q11-substitution OK occurrences=1 anchor=607-ok
S105:Q12-scoped OK occurrences=1 anchor=607-ok
S105:Q13-ghsa-format OK occurrences=1 anchor=612-ok
S105:Q14-cvss-versions OK occurrences=1 anchor=621-ok
S105:Q15-cve-provenance OK occurrences=1 anchor=628-ok
S105:Q16-epss-sync OK occurrences=1 anchor=639-ok
S105:Q17-epss-first OK occurrences=1 anchor=640-ok
S105:Q18-community OK occurrences=1 anchor=642-ok
S105:Q19-credit OK occurrences=1 anchor=643-ok
[exit=0]
```
19/19 quotes locate exactly once at their pinned anchors; capture sha matches; manifest pins the same
sha256 and 19 quotes. knowledge-expected.txt diff base→landing is exactly one added line: the new entry.

## 9. Whole-tree scope of the landing

```
$ git diff --name-status e7c02bd b4afd8a0
M corpus/README.md
M corpus/SOURCES.md
M corpus/instruments/knowledge-expected.txt
A corpus/knowledge/github-advisory-database-curation-semantics.md
A corpus/source-snapshots/round-70/S105.txt
A corpus/source-snapshots/round-70/manifest.json
```
`diff -rq` between the exports reports five extra differing files under
`.ufo/waves/round-31/wave1/ExecCensusDry/validate/*/corpus/instruments/knowledge-expected.txt`; those are
committed symlinks (`instruments -> ../../corpus/instruments`) resolving to the one changed instrument —
the paths exist as no blob in either revision (`git rev-parse <rev>:<path>` fatal both sides). No content
moved outside the six paths above.

## 10. Verdicts (per limb)

| # | limb | verdict |
|---|---|---|
| 1 | FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105 | VERIFIED |
| 2 | entries=51 pass=51 exit=0 | VERIFIED |
| 3 | records=84 bound=84 unbound=0 | VERIFIED |
| 4 | knowledge-expected 88 lines / 86 entries, LC_ALL=C sort -c exit 0 | VERIFIED |
| 5 | 86 files under corpus/knowledge/ | VERIFIED |
| 6 | F48 in README naming S105 + knowledge/github-advisory-database-curation-semantics.md | VERIFIED |
| 7 | sources-census.sh validate exit 0 | VERIFIED (committed bytes + verbatim live run) |
| 8 | S104/S105: NF=13, next unused ids, no `|` in cells, used-by resolves, tier/status/opened/recheck as claimed | VERIFIED |
| 9 | F48 row names S105+entry; F47 altered only in the one recorded next-cell clause | VERIFIED |
| 10 | 19 pinned quotes re-locate at anchors, exit 0 | VERIFIED |

**C2: VERIFIED.** No frozen after-value failed to reproduce; the kill rule is not triggered. Base
before-values also reproduce in full.

## 11. Residual risk / verification gaps

- Census replication used a minimal one-lane fleet root (kasegi conf row verbatim); the frozen command's
  absolute `--root` was also run verbatim (exit 0, same six W04). Fleet-wide FLEET.* metrics were not part
  of validate output and were not evaluated.
- No network re-fetch: S105's 616388 fetched bytes and S104's 3062-byte SPA-shell/round-69 byte-identity
  rest on committed receipts, not re-measured here (out of this item's scope).
- The SOURCES.md round-70 changelog does not name the F47 `next`-cell clause explicitly (§6 observation).
- Live lane working tree is at 7f6e39a (past both landings); verbatim live census still exits 0 today —
  no post-landing registry drift observed.
