VERIFIED

Seat: ReviewC2 (round-69 w1, C2 falsification re-measurement from committed bytes).
Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin. All commands run in this seat; cwd was the fleet root /home/vgpnk/Projects/shokunin unless noted. Scratch /fast/scratch/hyaku/kasegi-r69/ReviewC2/ was removed before this report was finalized; receipts live beside this file under w1/ReviewC2/.

## 0. Frozen-bytes integrity first
- `git -C .../kasegi-shokunin rev-parse --verify <commit>^{commit}` for 981115648e…, 1bd01ee1e…, 656272cf6b… → all three printed themselves (commits exist).
- `git -C .../kasegi-shokunin diff --stat 9b877fd916308e948b865c44ebc76e6ad322d6a7 -- .ufo/waves/round-69/claims.json .ufo/waves/round-69/controls/pins-r69.txt` → empty output ("frozen-files-identical-to-working-tree"): the working-tree claims/pins I read are byte-identical to the freeze commit.
- `git -C .../kasegi-shokunin rev-parse 981115648e…^` → `1bd01ee1e6558925e23d3d27a4bb12b88f502656`: the diff in §5 is exactly the C2 landing commit.
- Exports (whole tree): `git -C .../kasegi-shokunin archive 981115648e… | tar -x -C .../ReviewC2/export` and `git archive 656272cf6b… | tar -x -C .../ReviewC2/base` → "archives-ok".
- `git -C .../kasegi-shokunin rev-parse HEAD` → `981115648e4108e1adf5aec010edadac285a0c78` (live lane HEAD = landing); `git status --porcelain` shows only ` M SKILL.md` and untracked .ufo/waves files — no corpus path dirty, so the live census in §4 read the landing registry.

## 1. Counter battery vs frozen claims (MATCH/MISMATCH per value)
Commands (run once per export; receipts landing-*.txt / base-*.txt):
`python3 -B corpus/instruments/frontier-recheck-count.py`; `python3 -B corpus/instruments/capture-binding-check.py`; `wc -l corpus/instruments/knowledge-expected.txt`; `grep -vc '^#' corpus/instruments/knowledge-expected.txt`; `LC_ALL=C /usr/bin/sort -c corpus/instruments/knowledge-expected.txt; echo $?` (cwd = the export dir; /usr/bin/sort used deliberately per host note).

| Value | Base export (mine) | Frozen before | Landing export (mine) | Frozen after | Verdict |
|---|---|---|---|---|---|
| FRONTIER-CENSUS | `rows=46 admitted=46 closed=46 problem-rows=0 registry=102` | rows=46 registry=102 | `rows=47 admitted=47 closed=47 problem-rows=0 registry=103` | rows=47 registry=103 | MATCH / MATCH |
| FRONTIER-PASS tail | ends `F46 ids=S102`, no F47 line; no S103 | F47 rows=0, S103 rows=0 | `FRONTIER-PASS F47 ids=S103` | F47 ids=S103 | MATCH / MATCH |
| entries/pass | `entries=49 pass=49 exit=0` | 49/49 | `entries=50 pass=50 exit=0` | 50/50 | MATCH / MATCH |
| capture binding | `records=82 bound=82 unbound=0` | 82 | `records=83 bound=83 unbound=0` | 83 | MATCH / MATCH |
| knowledge lines | `86 corpus/instruments/knowledge-expected.txt` | 86 lines | `87 corpus/instruments/knowledge-expected.txt` | 87 lines | MATCH / MATCH |
| knowledge entries | `84` (grep -vc '^#') | 84 | `85` | 85 | MATCH / MATCH |
| `LC_ALL=C /usr/bin/sort -c` rc | rc=0 | exit 0 | rc=0 | exit 0 | MATCH / MATCH |

No MISMATCH. My base run also reproduces the committed control receipt controls/c2-base-counters-r69.txt line-for-line where comparable (census, F46 ids=S102, entries 49, records 82, 86/84).

## 2. Live-lane census
`( /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "rc=$?" )` → last line `ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, `rc=0`. MATCH (frozen: census exit 0). Receipt lane-census.txt. Qualifications: (a) it ran on the live working tree, which is at HEAD=9811156 but not pristine — ` M SKILL.md` + untracked .ufo/waves artifacts; no corpus path differs from the landing commit, so the validated registry is the landing registry. (b) The census prints W04 duplicate-URL-across-scopes warnings (S028, S029, S072, S076, S080, S085) and still exits 0; I did not run a base census to compare the warning set (not required by the predicate — only the exit code is frozen).

## 3. S103 row conformance (registry line 115 of landing export)
`awk -F'|' 'NR==115{...}'` (receipt row-fields.txt):
- pipe fields = 13 → 11 columns. MATCH (spec: 13 `|`-fields / 11 columns).
- id `S103` is the next unused id: unique-id tail in landing = S100,S101,S102,S103 (no S104 anywhere); base registry tail = S101,S102 and `grep -c S103 base/corpus/SOURCES.md` = 0. MATCH.
- kind=`docs`, tier=`A`, status=`mined`, opened=`2026-11-04`. MATCH all four.
- recheck=`180d` — an established registry value (distribution: 36×90d, 31×180d, 29×on-release, 3×730d, 1 each annual/365d/30d/2027-05-03). MATCH ("recheck valid").
- used-by=`corpus/knowledge/github-global-security-advisories-rest-api.md` — exists (8355 bytes in export). MATCH.
- located quote: anchor cell names `"If no other parameters are defined, the request will return only GitHub-reviewed advisories that are not malware." (L275, 17 words)`. My own count: `printf '%s' <quote> | wc -w` → `17` (≤25, MATCH). `sed -n '275p' .../S103.txt | grep -cF '<quote>'` → `1`: the quote sits verbatim at line 275 of the committed capture (the full capture line is 27 words; the quoted span is its 17-word suffix). MATCH.

## 4. Capture pins (recomputed from committed bytes)
- `sha256sum export/corpus/source-snapshots/round-69/S103.txt` → `c531c1e9b3eb9b4443e9851edc479e137eff772fb41dca3db16d697ac514344f` = pin. `wc -l` → `585` = pin. MATCH / MATCH.
- `sha256sum export/corpus/source-snapshots/round-69/manifest.json` → `7de5742a5fbb09318e3780b1b70c3cc07127c5401e40b3cb679f5d7e1de11b0f` = pins-r69 s103_manifest. MATCH.
- `grep -c '"quote"' manifest.json` → `13` = the claimed 13 quotes. MATCH.
- manifest lines 7-8 pin `"url"` and `"capture_url"` = `https://docs.github.com/en/rest/security-advisories/global-advisories` — the frozen target, distinct from S087 (repository-advisory REST) and S068 (single instance); the landing counter admitted both `F36 ids=S087` and `F47 ids=S103` as separate rows. MATCH.
- Observation (not a defect): the capture text itself never contains the source URL verbatim — it is the page text extraction (title line 1 `REST API endpoints for global security advisories - GitHub Docs … API Version: 2026-03-10 (latest)`); URL provenance lives in the manifest. Consistent with the lane's capture style.

## 5. Landing-commit scope (C1→C2 diff)
`git -C .../kasegi-shokunin diff --stat 1bd01ee1e… 981115648e…` (receipt c2-diff-stat.txt):
```
 corpus/README.md                                   | 10 +++
 corpus/SOURCES.md                                  |  4 +
 corpus/instruments/knowledge-expected.txt          |  1 +
 .../github-global-security-advisories-rest-api.md  | 91 ++++++++++++++++++++++
 4 files changed, 106 insertions(+)
```
`--name-status`: M corpus/README.md, M corpus/SOURCES.md, M corpus/instruments/knowledge-expected.txt, A corpus/knowledge/github-global-security-advisories-rest-api.md. Exactly the four C2 files, insertions only; the S103 capture pair was already committed at the freeze commit (`git ls-tree 9b877fd -- corpus/source-snapshots/round-69/` lists both). MATCH.
- `git diff -U0 1bd01ee… 9811156… -- corpus/SOURCES.md` (receipt c2-sources-U0.diff): 0 deletion lines (`grep -c '^-[^-]'` = 0), 4 added lines in 3 pure-insert hunks (`@@ -114,0 +115 @@` = the S103 row; `@@ -160,0 +162,2 @@` = one changelog bullet + one blank line; `@@ -252,0 +256 @@` = second changelog bullet). No pre-existing registry cell changed. MATCH. (stat's "+4" = 3 content lines + the blank line.)
- knowledge-expected.txt delta is the single line `corpus/knowledge/github-global-security-advisories-rest-api.md`, present at line 38 of the landing file (sorted).

## 6. README F47 row (corpus/README.md line 1087)
`awk -F'|' 'NR==1087{...}'` → pipe fields = 8 → 6 columns. MATCH. Cells: `F47` | title (GET /advisories filters + GET /advisories/{ghsa_id}, reviewed-only/malware-excluded default) | `admitted` | `knowledge/github-global-security-advisories-rest-api.md` (exists under corpus/ — 8355 bytes) | `S103` | gate notes citing S103.txt:275-276/:293-294. Entry path and sources column MATCH.
- Entry Gate block independently spot-checked (entry lines 80-83): `## Gate` → `Admitted 2026-11-04 (round 69) on S103 … Located quote (≤25 words, S103.txt:275)` — the located ≤25-word quote for its own access date is present, satisfying the C2 kill rule's gate-block clause.

## Residuals / notes (no defeat)
1. Depth boundary: I verified the manifest carries exactly 13 `"quote"` records and the binding tool reports `records=83 bound=83 unbound=0`; I did not re-locate each of the 13 quotes inside S103.txt myself (the entry's recheck line asserts Q01-Q13 each at its anchor). Not required by the seat spec.
2. The census W04 duplicate-URL warnings are pre-existing lane-wide findings outside this seat's frozen predicate (exit code only).
3. No tool installs or upgrades were needed or performed (no RULES.md tooling record required). No mutating git/jj command was run anywhere; the only git operations were rev-parse, archive, ls-tree, diff, status, show-free.

Verdict: VERIFIED — every frozen C2 after-value reproduced from the landing export bytes, every before-value reproduced from the base export bytes, and the landing commit touches exactly the four C2 files with additions-only on SOURCES.md.
