# ScribeSearchLog — round-33 Search-log seat (verification receipt)

Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, round 33, wave 1. Seat scope: the
`## Search log` section of `corpus/SOURCES.md` (one prose note per bounded search, CORPUS.md
rule 5). Date 2026-10-26. Answering model: config route table decides, not passed by hand; the
session context for this seat reports `opencode-go/deepseek-v4.1-flash`. No tools installed, no
fetch by this seat, no scratch dir created, no git/jj mutation, no delegation.

**Outcome: no second bullet was written.** The single round-33 Search-log bullet was landed by
`ExecRegistryAppend` (the file owner in the FILE OWNERSHIP table) at `corpus/SOURCES.md:75`; this
seat verified it claim by claim, had two measurable defects corrected, and re-verified the final
bytes. Writing a second note would have duplicated one bounded search in the same section.

## 1. Ownership contradiction and how it was resolved

- My item: "Own the Search log section … ONLY … After ExecRegistryAppend lands …, append one prose
  note". FILE OWNERSHIP assigns the whole file (`corpus/SOURCES.md` — "append rows S049/S050 +
  Search log + R8 lines") to `ExecRegistryAppend`.
- `ConnOwnership` (message received this seat: "Ownership contradiction found (pre-write) … your
  item tells you to append the round-33 note to ## Search log, but ExecRegistryAppend's item ALSO
  appends that note … HOLD your write until Main rules — interim default: ExecRegistryAppend lands
  the note; you verify the landed note … without editing the file").
- Resolution taken: I held my write, read the landed bullet, verified it, and sent
  `ExecRegistryAppend` (by id) the exact content and the two defects. It replied "Option (b): the
  bullet is already landed by me at corpus/SOURCES.md:75 — do not write a second one. Both defects
  you flagged are fixed in that same line". Its receipt records the same outcome as a ruling by
  `ConnOwnership` ("Ownership: `ConnOwnership` ruled the whole `corpus/SOURCES.md` (rows + Search
  log + R8) to this seat; `ScribeSearchLog` (second claimant) was told the bullet was already
  landed by me and applied no duplicate", `wave1/ExecRegistryAppend.md:7`). No Main message was
  sent and no `agent://all` broadcast was used; the interim action I took is the ruled outcome.

## 2. Commands and output (all read-only, run from the lane root unless stated)

Row and section state at verification:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
50
$ grep -n '^## ' corpus/SOURCES.md
3:## Registry
58:## Paths
65:## Search log
77:## Leads (unopened)
83:## Registry changes
$ wc -lc corpus/SOURCES.md && sha256sum corpus/SOURCES.md
  100 52996 corpus/SOURCES.md
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
$ grep -c 'round 33' corpus/SOURCES.md
1
```

One round-33 note only, at line 75, inside `## Search log` (lines 65–77); section order unchanged.
Registry rows 50 (48 pre-append → 50), so the appended URLs did not land in a second registry row:

```
$ grep -n 'zc.cnvd.org.cn' corpus/SOURCES.md      → 55 (row S049), 75 (Search-log bullet)
$ grep -n 'security.360.cn' corpus/SOURCES.md     → 56 (row S050), 75 (Search-log bullet)
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && /zc\.cnvd\.org\.cn/ {print NR": row"}' corpus/SOURCES.md
55: row
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && /security\.360\.cn/ {print NR": row"}' corpus/SOURCES.md
56: row
```

Each record URL therefore matches exactly one registry row (C1 rule B basis); the second
occurrence is prose in the Search-log bullet, not a row.

Lane sweep re-run on the post-append bytes (the negative sweep itself was PRE-STATE — see §4):

```
$ ls corpus/knowledge/*.md | wc -l          → 45 (44 before the F16 entry landed)
for t in CNVD 360SRC 360 众测 zc.cnvd.org.cn security.360.cn crowdsourced Chinese \
         crowd-testing 漏洞 收录 SRC; do grep -c -- "$t" <knowledge|README|SOURCES|SKILL>; done
CNVD             kn=20 README=2 SOURCES=3 SKILL=0
360SRC           kn=23 README=2 SOURCES=3 SKILL=0
360              kn=38 README=2 SOURCES=3 SKILL=0
众测             kn=19 README=2 SOURCES=3 SKILL=0
zc.cnvd.org.cn   kn=2  README=1 SOURCES=2 SKILL=0
security.360.cn  kn=4  README=1 SOURCES=2 SKILL=0
crowdsourced     kn=5  README=3 SOURCES=6 SKILL=0
Chinese          kn=3  README=2 SOURCES=1 SKILL=0
crowd-testing    kn=0  README=0 SOURCES=2 SKILL=0
漏洞             kn=33 README=1 SOURCES=4 SKILL=0
收录             kn=5  README=0 SOURCES=1 SKILL=0
SRC              kn=29 README=2 SOURCES=5 SKILL=0
```

(The `kn` column sums line hits across `corpus/knowledge/*.md`; it includes the new F16 entry and
boilerplate such as `3600`-second constants and `MSRC` substrings — counts are context, not the
verdict. The PRE-STATE sweep, whose verdict the note records, was `wave1/ScoutF16Sweep.md` §1.)

Capture and package facts the bullet cites, re-measured here:

```
$ sha256sum corpus/source-snapshots/round-32/S049.txt corpus/source-snapshots/round-32/S050.txt
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  S050.txt
$ wc -lc …/S049.txt …/S050.txt   → 426 20272 / 630 31016
$ grep -cE '^\| *S[0-9]+' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
94
$ ls /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/*.md | wc -l
67
$ python3 -c 'print(len("https://zc.cnvd.org.cn/news/helpList".encode()), len("https://security.360.cn/Reward/rules".encode()))'
36 36
$ grep -cE '^source: S0(49|50) ' corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
2
```

Whitespace-normalized exactly-once probes the bullet's exclusion reasons rest on:

```
S049: 您不得因为漏洞信息私自联系厂商 = 0 ; 众测需求方 = 0 ; 授权测试方 = 0 ; 43741 = 0 ; 国家标准 = 0
S050: 您不得因为漏洞信息私自联系厂商 = 0 ; 众测需求方 = 0 ; 授权测试方 = 0 ; 43741 = 0 ; 国家标准 = 0
      仅从理论层面说明漏洞的存在而无利用和复现过程将不予收录 = 1
```

## 3. Claim-by-claim verification of the landed bullet (`corpus/SOURCES.md:75`)

| rule-5 element | bullet says | verified against | verdict |
|---|---|---|---|
| question | does the lane already hold CNVD 众测 help-page scope/scoring ground or the 360SRC V2.0 handling rules, and do the two staged rows add ground F13–F15 do not | the round's frozen C2 / F16 surface; `wave1/ScoutF16Sweep.md` verdict `residual-exists` | **agree** — the question is the bounded F16 question, not a general Chinese sweep |
| where | package `merge/kasegi/` (`SOURCES.append.md`, 94 staged rows, staged entries, `MERGE-REPORT.json`); twelve-term sweep over 44 knowledge files (PRE-STATE; 45 after), README, SOURCES, SKILL; two URLs re-fetched 2026-10-26T04:16Z under the instrument UA (S049 200/56,674 B; S050 200/427,391 B; text byte-identical, 0 differing lines — `wave1/ScoutLiveDrift.md`), committed captures named | measured above; `ScoutLiveDrift.md`; `ScoutF16Sweep.md` §1 | **agree** — three surfaces named, live re-fetch now stated (defect 1 fixed, §5), PRE-STATE label present (defect 2 fixed) |
| date | 2026-10-26 | today; captures hashed above | **agree** |
| counts | identified 9 (the 9 rows of `ScoutPackageThemes.md`'s verdict table = 2 staged source rows that join by URL, S034/S035 of 94, plus the 7 staged entries re-gated), screened 9, included 2, excluded 7 | `ScoutPackageThemes.md` verdict table: 2 ADMIT-by-document + 7 REJECT = 9; 2+7 = 9 | **agree, arithmetic closes**, and the denominator is stated so it can be re-derived |
| exclusion reasons | program-scope-rules-and-asset-boundaries + claim-packaging-and-report-quality (unregistered rows, no located quotes, no per-platform attribution, no executable recheck, no lane F-id); cn-crowdsourced-testing-roles-and-conduct (S081/S082 unregistered, different page, conduct sentences 0 in both captures); chinese-crowd-testing-national-standard (no `43741`/`国家标准` in either capture); chinese-criminal-thresholds (staged S044–S046 unregistered, cross-instrument conclusion); chinese-program-severity-instrument (`newsType_6` locator not checkable, second source unregistered); program-severity-ladders-and-reward-scales (same-name lane file, copy would overwrite F13) | `ScoutPackageThemes.md` §2 tables; `ScoutF16Sweep.md` §2/§3; probe counts in §2 above | **agree** — every named reason is in a committed receipt, and the zero-count reasons reproduce on the captures |
| stop rationale | the bounded package set plus the two committed captures answered F16 and supplied the located quotes; no wider target-facing research, no other staged entry carried | the seat set this round: `ScoutF16Sweep` (residual), `ScoutLiveDrift` (no drift), `ConnSibling` (no sibling holds it) | **agree** — the stop is justified by the question being answered by two mutually distinct first-party documents, not by exhaustion of a search engine |
| included | staged S034 → lane S049, staged S035 → lane S050, by DOCUMENT, URL byte-equal at 36 bytes each | row 55/56 source cells; `len(url)=36,36` measured; `ScoutPackageThemes.md` §1 | **agree** |

## 4. Count framing — two different, non-conflicting measurements (disclosed)

`ExecEntryF16` proposed to this seat "identified 2 staged rows, screened 2, refused 0, adopted 2".
That is **not** what the file holds and not what the receipts support: the landed note's basis is
`ScoutPackageThemes.md`'s 9-row verdict table (7 re-refusals + 2 admits). My own independent
census measures a third, narrower set, which I am recording so no later reader mistakes one for
another:

```
$ grep -l -E 'zc\.cnvd\.org\.cn|security\.360\.cn|360SRC|众测' <package>/knowledge/corpus/knowledge/*.md | wc -l
9                       # of 67 staged entries whose BYTES mention the theme
$ grep -l -E '^source:.*\bS0?3[45]\b' <package>/knowledge/corpus/knowledge/*.md | wc -l
4                       # of 67 staged entries that cite staged S034 or S035 by id
```

The 9 theme-byte hits are `chinese-criminal-thresholds-and-authorisation`,
`chinese-crowd-testing-national-standard-2026-10-23`, `chinese-program-severity-instrument`,
`chinese-vulnerability-taxonomy-and-grading`, `claim-packaging-and-report-quality`,
`cn-crowdsourced-testing-roles-and-conduct`, `japanese-severity-vocabulary-and-impact-model`,
`program-scope-rules-and-asset-boundaries`, `program-severity-ladders-and-reward-scales`. Two of
them are **not** in the landed note's exclusion list — `japanese-severity-vocabulary-and-impact-model`
(same-name staged twin of the landed F14 entry; its staged `S049/S050` are the IPA PDFs, not the
lane documents) and `chinese-vulnerability-taxonomy-and-grading` (national taxonomy on staged
`S037/S038`; its only theme sentence is a mention of "BILISRC, 360SRC, CNVD 众测" ladders, line 42).
Both were screened and carry no new ground for F16 (the first is already resident, the second is
outside the platform scope/reward question), so their omission from the bullet's 7-name exclusion
list is a **scope-of-list choice, not a missing exclusion**; the list plus its stated denominator
(9 = 2 rows + 7 entries) is internally consistent and re-derivable. Recorded here rather than
rewritten into the file, because a second edit would churn a verified line for no factual gain.

## 5. Defects found in the first landing, and their fix

| # | defect (measured) | evidence | fix |
|---|---|---|---|
| 1 | "the already-committed round-32 captures … (no target was re-fetched this round)" — false: both pages were fetched live on 2026-10-26T04:16:06Z / 04:16:16Z under the instrument UA, HTTP 200, 56,674 B / 427,391 B, text byte-identical (`wave1/ScoutLiveDrift.md`) | receipt command + status line quoted at the top of that file | replaced by `ExecRegistryAppend` with the live re-fetch clause (without re-printing the URL strings, so rule B still sees one URL per registry row); wording confirmed in the final line 75 |
| 2 | "over the lane's own `corpus/knowledge/*.md` (44 files)" — a PRE-STATE number (rule 6) printed unlabelled; the tree holds 45 after the F16 entry | `ls corpus/knowledge/*.md \| wc -l` → 45 | replaced with "(44 files before the F16 entry landed — PRE-STATE for S049/S050, labelled in `wave1/ScoutF16Sweep.md`; 45 after)"; confirmed in the final line 75 |

Both fixes are inside the single bullet; no Registry, Paths or Registry-changes line was touched by
either correction. Line accounting against the base blob (`git show 690b69da…:corpus/SOURCES.md`,
94 lines): the file is now 100 lines = 94 + 6, and the 6 are the S049 row (line 55), the S050 row
(56), this Search-log bullet (75) and the three Registry-changes lines (98–100, the two row-added
notes and the closing "Registry 48 rows pre-append → 50 post-append (R8)" line); the other 94 lines
are the base bytes, shifted.

Residual nit, recorded not fixed: the bullet's sweep sentence ("returned no lane hit for `360SRC`,
`zc.cnvd.org.cn` or `security.360.cn`") describes the PRE-STATE run; on today's bytes those terms
hit the two new rows and the F16 entry. The same bullet labels the sweep PRE-STATE in its `where`
clause, so the sentence is dated rather than false; a future reader re-running the grep without the
label would see a discrepancy.

## 6. Bounds and limits

- I did not fetch any URL: the live-read facts are `ScoutLiveDrift`'s receipt; I verified locally
  its pinned digests/sizes against the committed captures (`sha256sum`, `wc -lc`).
- The Search-log note describes **one** bounded search. The registry-row content, the F16 entry and
  the C1/C2 counters are other seats' deliverables; this receipt verifies only the section it owns.
- Pre/post sweep comparison is deliberate: the negative sweep is PRE-STATE by nature (it asks what
  the lane held before admission), and the post-append numbers are given as the named re-run, never
  as an "after" column to be compared with a pre column.
- Model recorded per rule 10 as the session context states it; no model was passed. Nothing
  installed; no scratch dir used or left behind; no writes outside this receipt.

## 7. Files touched

- Written: `.ufo/waves/round-33/wave1/ScribeSearchLog.md` (this receipt).
- Not written: `corpus/SOURCES.md` — landed and corrected by its owner `ExecRegistryAppend`; verified
  at `sha256 b22c7f01…d13b`, 100 lines, 52,996 B.
