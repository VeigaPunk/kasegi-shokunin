# ExecCountersC2 — round-70 C2 counters re-measured from committed bytes

Seat: ExecCountersC2 (executor, leaf). Lane: kasegi. Frozen claims: `e74ba6b5` (claims.json, pins-r70.txt). C2 landing: `b4afd8a0`. Base: `e7c02bdd`.

Method: `git archive` of `b4afd8a0` (after) and `e7c02bdd` (base) into the seat scratch; every counter run from inside the exported tree with `python3 -B` (host python3 3.14.8, GNU sort 9.12 via `/usr/bin/sort`, `LC_ALL=C`). Frozen inputs (claims commit) exported read-only for the assimilation files and the pinned receipt. No lane file was written; the only lane write is this report. No tools installed or upgraded.

## 1. Counter battery (item 1)

| counter | base `e7c02bdd` | after `b4afd8a0` | frozen before / after (claims.json) | reproduces |
|---|---|---|---|---|
| `frontier-recheck-count.py` (census line) | `rows=47 admitted=47 closed=47 problem-rows=0 registry=103`, exit 0 | `rows=48 admitted=48 closed=48 problem-rows=0 registry=105`, exit 0 | 47/103 → 48/105 | yes |
| `frontier-recheck-count.py` (entries) | `entries=50 pass=50 exit=0` | `entries=51 pass=51 exit=0` | 50 → 51 | yes |
| `capture-binding-check.py` | `records=83 bound=83 unbound=0`, exit 0 | `records=84 bound=84 unbound=0`, exit 0 | 83 → 84 | yes |
| `wc -l < knowledge-expected.txt` | 87 | 88 | 87 → 88 | yes |
| `grep -vc '^#' knowledge-expected.txt` | 85 | 86 | 85 → 86 | yes |
| `LC_ALL=C sort -c knowledge-expected.txt; echo $?` | 0 | 0 | sort-clean | yes |
| `ls corpus/knowledge/*.md \| wc -l` | 85 | 86 | 85 → 86 | yes |
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 47 | 48 | 47 → 48 | yes |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 103 | 105 | — | n/a (new S104, S105 rows) |
| awk 13-column check on SOURCES.md rows | 0 | 0 | — | rows well-formed |

Additional after-tree facts:
- `FRONTIER-PASS F48 ids=S105` and `PASS F48 knowledge/github-advisory-database-curation-semantics.md ids=S105 exit=0` (after only).
- `records=84 with_url=84 with_fetched_utc=46 with_archival=38 ... missing_manifest=0 digest_unpinned=0 orphans=1 orphan=S040-live.txt` (after). Base is `records=83 ... with_fetched_utc=45 ... with_archival=38 ... orphans=1` — the orphan line is inherited, not new.
- `corpus/README.md:1097` names S105 and the knowledge path for F48.
- Frozen receipt `.ufo/waves/round-70/controls/c2-after-counters-r70.txt` at the claims commit: sha256 `f20fd6e72e1fb5f96a16e81fe66a2176897d155075d6e2c533eb959123d166ab` (matches pins-r70.txt); its summary lines (`FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105`, `entries=51 pass=51 exit=0`, `records=84 bound=84 unbound=0`) match my re-measurement.

Verdict for the counter predicate: every frozen after-value reproduces from the committed C2 bytes; every before-value reproduces from base.

## 2. Census (item 2)

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
Exit code: **0**. stderr: empty. stdout: 7 lines.

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
kasegi	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
kasegi	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

- Six warnings, all W04, all inherited (S028, S029, S072, S076, S080, S085): matches the claim's "six inherited W04 warnings".
- **No warning names S104 or S105** (`grep -nE 'S104|S105'` on the output: none).
- Caveat: this validator reads the live `kasegi-shokunin` working tree at the root, not the committed `b4afd8a0` tree. The committed after-tree census inputs were checked in section 1 instead.

## 3. Assimilation id-collision re-derivation (item 3)

Inputs (claims commit `e74ba6b5`, `.ufo/waves/round-70/assimilation/`):
- `reg-ids`: 103 lines, 103 unique, `sort -c` exit 0; head S001–S005, tail S099–S103.
- `staged-ids`: 94 lines, S031–S124.
- `collisions`: 73 lines.
- Read-only register `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`: 100 lines; 94 unique `S`-ids in table rows, the same set as `staged-ids` (`comm -12` against staged = 94).

Derivation: `LC_ALL=C comm -12 reg.sorted staged.sorted`:
```
73
```
`diff` of `sort(collisions)` against the derived set: **no difference** (the committed file is exactly the derived intersection, S031–S103).
Staged ids not in the registry: 21 (S104–S124).

**The 73-collision conclusion holds**: 73 of the lane's 103 registry ids collide with the staged id set, so the contract's no-adopt decision stands.

Additional finding (strengthens the drift rule; not in the frozen text): the read-only register's **S104 and S105 are the same source under two ids**, a Chinese-law article (袁炜案 ... `iolaw.cssn.cn/fxyjdt/201709/t20170928_4653108.shtml`, kind docs, tier B, status `mined`). The lane's S104 is ENISA EUVD (`rejected`) and the lane's S105 is GitHub Docs (`mined`). So the staged ids S104/S105 do not denote the lane's sources, and the staged set double-counts one source. Any future adoption of that register must re-key these rows.

Quarantine slice (`.ufo/waves/round-70/assimilation/quarantine-slice`), 7 lines:
```
 S037   `payload-absent` 
 S054   `payload-absent` 
 S048`   the cited source could not be fetched, so no quote was checked 
 S065`   the cited source could not be fetched, so no quote was checked 
 S068`   the cited source could not be fetched, so no quote was checked 
 S069`   the cited source could not be fetched, so no quote was checked 
 S070`   the cited source could not be fetched, so no quote was checked 
```
- **Every line carries an S-id**: 7 of 7 match `S[0-9]{3}`; 0 lines without one.
- All 7 ids are members of `staged-ids` and of the 73-collision set.
- Re-derivation from the register is only partial: the register has no fetch-state, payload or fetch-failure column, and neither literal string (`payload-absent`, `could not be fetched`) occurs in it. The seven register rows carry status `mined` with opened dates 2026-10-23 and recheck intervals of 180d / 90d / on-release. The quarantine reason labels therefore come from fetch state that the register does not carry; I could not reproduce them from the read-only register and did not verify them against the lane's own fetch records. The contract states no slice-membership rule, so I cannot confirm the slice is complete.

## 4. F48 / S105 anchors (item 4)

Capture: `corpus/source-snapshots/round-70/S105.txt`, sha256 `9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350` (matches pins), `wc -l` = 656, `wc -c` = 22791 (matches the knowledge file's "22791 snapshot bytes"). Knowledge entry sha256 `d479c4954675b52c1ae49901efb1c780f686d686c96f6f24e4ab31d660fea72f` (matches pins).

Anchor inventory: 43 `S105.txt:N` / `S105.txt:N-M` occurrences in `corpus/knowledge/github-advisory-database-curation-semantics.md`.
- **Range: all 43 in 1..656. Zero out-of-range anchors.**
- Distinct cited lines/ranges: 558; 567; 568–608; 570; 571; 573; 574–582; 584; 585; 586–597; 597; 599; 601; 602; 604; 605; 606; 607; 611–616; 621; 621–634 (incl. 623–627, 628); 636–640; 639; 640; 642; 643.

Semantic check (each cited line printed in full and compared with the sentence it supports):
- Exact quote matches: 584, 585 (two quotes); 601, 602, 604 (malware), 606; 567 (OSV format); 570 ("the earliest version where the problem was fixed"); 571 ("the only safe course of action is not to use the package at all", "no safe versions", "Malware alerts do not contain a fix version"); 607 (both quoted spans, incl. "doesn't look at project configurations to determine if the packages are coming from a private registry" and "Users who have their dependencies appropriately scoped should not be affected by malware."); 611–616 (GHSA shape, charset, lowercase); 621 and 628 (CVSS 3.1/4.0 provenance, "imported CVE supports 4.0, 3.1 and 3.0"); 623–627 (four severity levels); 639 ("when significantly different", "always fully synchronized", daily sync); 640 ("we do not author this data, but rather source it from FIRST"); 642 (PR to github/advisory-database, published on acceptance); 643 ("Analyst" credit); 586–597 (twelve ecosystems, matching the knowledge list); 574–582 (nine feeds, matching "the nine imported feeds" in the README row); 599 (Dependabot alert for reviewed advisories); 605 (malware alerts when enabled); 558 (page purpose).

**One semantically wrong anchor-claim pairing** (knowledge lines 69–70):
> "each named after its package registry except GitHub Actions and Swift, whose registry cell reads "Swift (registry: N/A)" (`S105.txt:597`)"

Line 597 is `Swift (registry: N/A)` — correct for Swift only. The GitHub Actions line (589) reads `GitHub Actions (https://github.com/marketplace?type=actions)`: it has no registry cell and no "N/A". The sentence attributes the N/A registry cell to GitHub Actions as well, which the page does not say. Fix would be to name only Swift as the N/A case and cite 589 for GitHub Actions. No anchor is out of range; this is a claim-precision defect, not a range defect.

Other anchors checked for precision and found correct: 642 is cited for "published only if accepted" (642 says "publish them ... if accepted"; the Analyst credit is at 643, which the entry cites separately).

## 5. Limits and disclosures
- Ran the counters on the committed after and base trees only; did not run `source-recheck.py` or the 19 pinned S105 quotes (not in this seat's assignment).
- The census run reads the live lane working tree, per the command given (see section 2).
- Quarantine reason labels not reproducible from the register (section 3).
- The S104/S105 duplicate-source finding in the staged register is an observation about the read-only input; it did not change any frozen value.
- `find -mmin` on the lane shows many round-70 files with recent mtimes (the claims-commit files and this wave's landed files). I did not write them; I did not attribute the mtimes.
- No labrat dispatched (no falsifiable hypothesis required beyond the checks above). No subagent spawned.
- No tools installed or upgraded. No git mutating command. Scratch tree `/fast/scratch/hyaku/kasegi-r70/ExecCountersC2/` removed at yield; no receipt points at it (all outputs are pasted above).
