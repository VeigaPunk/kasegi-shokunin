# ScribeSearchLog — round 34

Seat: `ScribeSearchLog` (scribe). Scope: draft the round-34 `## Search log` bullet for the C2 Immunefi VSCS
sweep, PRISMA-shaped, for `ScribeSOURCESRow` / `ExecRegistryAppend`. I did not edit `corpus/SOURCES.md`,
`corpus/QUALITY.md`, any capture, manifest, or entry; no git/jj mutation was run.

## Draft (copy-ready bullet)

One line, appended after the current last Search-log bullet (`corpus/SOURCES.md:75`) and before the blank
line at `:76`:

```
- Immunefi severity-classification sweep (round 34); question: does the lane hold a Web3/smart-contract bounty severity-classification source, and does Immunefi's own Vulnerability Severity Classification System v2.2 add ground the lane's 45 knowledge entries do not; where: Immunefi's own site — the severity-classification index https://immunefi.com/severity-classification-systems/ plus every version page it links, with https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ opened in full (HTTP 200, 219384 bytes) alongside v2.3 (HTTP 200, 230877 bytes); and a six-term negative sweep over the lane's own corpus/knowledge/*.md (45 files at measurement time, before this round's entry landed — PRE-STATE; 46 after), corpus/README.md, corpus/SOURCES.md and SKILL.md for 'Immunefi', 'VSCS', 'severity classification', 'smart contract', 'Web3', 'blockchain'; date: 2026-10-26; identified 8, screened 3, included 1, excluded 7. Excluded: five version pages the index files under "Being Phased Out" (v2.1, v2, v1.2, "- Updated", and the unsuffixed system), screened at title only from the index status labels; the index itself, which locates versions but states no level table; and v2.3, which is in use concurrently but states a simplified 4-level scale where v2.2 states the 5-level scale, so it is a different version of the same instrument and not this row's subject (opened and preserved for a later round, not absorbed). Inclusion reason: the v2.2 page states Immunefi's own 5-level scale and its Smart Contracts table carries the Critical cell "Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield"; the negative sweep returned 0 hits for 'VSCS', 'severity classification', 'smart contract' and 'blockchain', and only program-operations ground for 'Immunefi' (15 hits in 6 files, e.g. corpus/knowledge/policy-access-playbook.md:11) and dataset/enum ground for 'Web3' (15 hits in 6 files, e.g. corpus/knowledge/triage-thresholds.md:359), so no held severity-classification source was displaced. Stop: one opened authority answered the bounded question and the version set was enumerated exhaustively from Immunefi's own index page, so no secondary scoring explainer or third-party summary was screened.
```

Measured properties of the drafted line: 2273 bytes, one line, `|` count 0, backtick count 0, no trailing
whitespace — it is a bullet, not a registry cell, so the NF=13 rule does not apply.

## Report

### 1. Question and surface

Bounded question (from the round-34 assignment and `claims.json` C2): does the lane already hold a
Web3/smart-contract bounty severity-classification source, and does Immunefi's own VSCS v2.2 add ground the
lane does not hold. Surfaces searched: Immunefi's own site (index + linked version pages) and the lane's own
corpus, read-only.

### 2. Commands, outputs, exit codes

Live fetches (read-only HTTP; scratch under `/fast/scratch/hyaku/kasegi-r34/ScribeSearchLog/`):

```
$ curl -sS -A "shokunin-capture/1.0 (+corpus provenance; contact: lane operator)" -L -o v22.html \
    -w "http=%{http_code} bytes=%{size_download} url=%{url_effective}\n" \
    https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/
http=200 bytes=219384 url=https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ ct=text/html; charset=utf-8
exit=0
$ curl ... -o v23.html  https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-3/
http=200 bytes=230877 url=https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-3/
exit=0
$ curl ... -o index.html https://immunefi.com/severity-classification-systems/
http=200 bytes=149273 url=https://immunefi.com/severity-classification-systems/
exit=0
```

My own HTML digests (independent of, and not interchangeable with, the instrument capture):

```
25e538041b8561cb0e2dd245ead1fb179fbd103218e3efb7ab2971027ad5997d  v22.html   219384 B
da104fbcc3414628bd689b1f5cfc8bf6d579dc0306adcbbd0eabe37d39c1c41a  v23.html   230877 B
2eafb84b4b4b2d5f23a0294c403fa5f1c8e2b07f59e9d57c955ad905c24df3f8  index.html 149273 B
```

Version enumeration from the index (`grep -c "Immunefi Vulnerability Severity Classification System"
index.txt` → `7`; anchor-text/href pairs extracted from `index.html`):

```
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-3   ... System v2.3   (Currently in Use)
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2   ... System v2.2   (Currently in Use)
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-1   ... System v2.1   (Being Phased Out)
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2     ... System v2     (Being Phased Out)
https://immunefi.com/severity-system-comprehensive                               ... System v1.2   (Being Phased Out)
https://immunefi.com/severity-updated                                            ... System - Updated (Being Phased Out)
https://immunefi.com/severity-system                                              ... System        (Being Phased Out)
```

Level-scale statements, verbatim, each `grep -cF` = 1:

```
v22.txt:130  At Immunefi, we classify bugs on a simplified 5-level scale:
v23.txt:130  At Immunefi, we classify bugs on a simplified 4-level scale:
             (grep -cF "simplified 5-level scale" v22.txt -> 1; grep -cF "simplified 4-level scale" v23.txt -> 1;
              note the extract is my own HTML-to-text render, so v22.txt:130 is not S051.txt:46)
```

Cross-check against the committed round-34 capture (read-only; **the capture is authoritative**, line numbers
below belong to it, not to my extract):

```
$ sha256sum corpus/source-snapshots/round-34/S051.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
$ wc -l -c corpus/source-snapshots/round-34/S051.txt
175 8502
$ grep -cF "simplified 5-level scale" S051.txt                                        -> 1   (:46)
$ grep -cF "Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield" S051.txt -> 1   (:75)
$ grep -cF "table below is mostly concerned with the consequence of a successful" S051.txt -> 1   (:53)
$ grep -cF "Direct theft of any user NFTs, whether at-rest or in-motion, other than unclaimed royalties" S051.txt -> 1 (:76)
$ grep -n "Smart Contracts" S051.txt                                                  -> :72
$ grep -n "v2.2" S051.txt                                                             -> :1, :45
```

All exit codes 0; every quoted string occurs exactly once in the capture at the line cited above. At the time
of my read, `corpus/source-snapshots/round-34/manifest.json` did not exist (`cat` → "No such file or
directory"), so the manifest-anchored `source-recheck` run is not mine to report — `ExecSnapshotR34` owns it.

### 3. Negative sweep over the lane corpus (PRE-STATE)

Commands (`corpus/knowledge/*.md` = 45 files at the time of measurement; the F17 entry was not yet on disk):

```
for t in Immunefi VSCS "severity classification" "smart contract" Web3 blockchain; do
  files_k=$(grep -ril -- "$t" corpus/knowledge/*.md | wc -l)
  hits_k=$(grep -ric -- "$t" corpus/knowledge/*.md | awk -F: '{s+=$2} END{print s+0}')
  hits_r=$(grep -ic -- "$t" corpus/README.md); hits_s=$(grep -ic -- "$t" corpus/SOURCES.md)
  hits_sk=$(grep -ic -- "$t" SKILL.md)
  echo "$t | knowledge_files=$files_k knowledge_hits=$hits_k README=$hits_r SOURCES=$hits_s SKILL=$hits_sk"
done
```

Output (verbatim):

```
Immunefi | knowledge_files=6 knowledge_hits=15 README=2 SOURCES=0 SKILL=2
VSCS | knowledge_files=0 knowledge_hits=0 README=0 SOURCES=0 SKILL=0
severity classification | knowledge_files=0 knowledge_hits=0 README=0 SOURCES=0 SKILL=0
smart contract | knowledge_files=0 knowledge_hits=0 README=0 SOURCES=0 SKILL=0
Web3 | knowledge_files=6 knowledge_hits=15 README=0 SOURCES=0 SKILL=1
blockchain | knowledge_files=0 knowledge_hits=0 README=0 SOURCES=0 SKILL=0
```

`grep -ric "Immunefi" corpus/knowledge/*.md | grep -v ":0"` → `claim-anatomy-sample.md:6`,
`intake-surface.md:1`, `mission-ledger.md:1`, `operator-queue.md:1`, `policy-access-playbook.md:1`,
`ufo-workspaces.md:5`. `grep -ric "Web3" corpus/knowledge/*.md | grep -v ":0"` →
`intake-and-finalize.md:3`, `intake-surface.md:3`, `source-tree-loss-2026-09-28.md:1`,
`target-checkouts.md:1`, `triage-thresholds.md:2`, `ufo-archive-2026.md:5`. Variant spellings of the
hyphen/space term: `grep -rio "smart-contract"` → 2, `"SmartContracts"` → 1, `"smart contract"` → 0.

Character of the hits (why no held classification source was displaced): `Immunefi` appears only as
program-operations ground — ingestion/provenance hashing (`corpus/knowledge/policy-access-playbook.md:11`,
`SKILL.md:130`), claim paths (`corpus/knowledge/claim-anatomy-sample.md:51-56`), telemetry
(`corpus/README.md:175-177`); `Web3` appears only as dataset/enum ground (`corpus/knowledge/triage-thresholds.md:359`
`source_kind` enum, `:376` `board_ref.dataset`, `corpus/knowledge/intake-and-finalize.md:19` `web3_programs.json`).
Neither term appears with a severity level table or classification system.

### 4. PRISMA accounting (why 8 / 3 / 1 / 7)

- **identified 8** = the index page + the seven version pages it links (enumerated above from the index's own
  anchor text).
- **screened 3** = opened and read in full: the index, v2.2, v2.3 (all HTTP 200, text bodies extracted).
- **included 1** = v2.2 (`https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/`).
- **excluded 7** = 5 phased-out version pages (title-level screen: the index files them under "Being Phased
  Out") + the index itself (locator only, no level table) + v2.3 (full-text screen: 4-level scale, a
  concurrent version of the same instrument).
- One further surface is named but **not counted**: the index's "Help Desk article, which explains every
  impact from the Severity Classification System 2.3" — a secondary explainer for v2.3, deliberately left
  unscreened rather than miscounted as a VSCS version record.

Stop rule as applied: the version set is closed by Immunefi's own index (no wider Web3-scoring sweep needed),
and one opened authority answers the bounded question, so the sweep stops without screening third-party
severity explainers.

### 5. Consumer constraints (for `ScribeSOURCESRow` / `ExecRegistryAppend`)

1. The bullet is PRE-STATE-labelled on purpose: after the F17 entry lands, the same six-term sweep gains one
   file (and its `Immunefi`/`VSCS`/`smart contract`/`Web3` hits). Do not silently rewrite `45 … 46` to a
   post-state number without re-running the sweep; if you prefer post-state only, re-run the loop above and
   drop the PRE-STATE clause.
2. Quote anchors in the S051 row must cite the **capture** line numbers (46, 53, 72, 75, 76 in
   `corpus/source-snapshots/round-34/S051.txt`), not my extract's numbering. Both agree on content; the
   capture is the pinned bytes (`sha256 4fd8ed98…b325a5`).
3. Version discipline: v2.2 = 5 levels (Critical/High/Medium/Low/None); v2.3 = 4 levels. The index states
   both are "Currently in Use". Any sentence that treats v2.2's scale as current-for-all-programs is
   over-generalized; the entry should attribute the 5-level scale to v2.2 specifically.
4. Anchor drift (M33-3 class): current anchors measured in `corpus/SOURCES.md` — `## Registry` :3,
   `## Paths` :58, `## Search log` :65, first bullet :67, last bullet :75, `## Leads (unopened)` :77,
   `## Registry changes` :83, R8 lines :85–:90, S043 change-cell :90. This round adds two lines above those
   (one registry row before :58, one Search-log bullet after :75), so `## Leads (unopened)` is expected at
   :79 and `## Registry changes` at :85, and the R8 block now cited at :85–:90 lands at :87–:92. Re-measure
   after your own writes; these are predictions from the current bytes, not observations of the landed file.
5. The bullet carries no `|`; if any later edit introduces one, the census row parser is unaffected (search
   log is outside the registry table) but the lane's own no-pipe-in-cells convention is worth keeping.

### 6. Scratch, tooling, digests

Scratch `/fast/scratch/hyaku/kasegi-r34/ScribeSearchLog/` (`v22.html`, `v22.txt`, `v23.html`, `v23.txt`,
`index.html`, `index.txt`) was deleted with `rm -rf` after the numbers above were transcribed; the directory
is gone (`ls` → "No such file or directory"). No tools installed, nothing upgraded; `curl` and `grep` from the
host as-is (no `pacman`, no `uv`).

Input digests at measurement time:

```
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
```

The lane tree was mid-landing while I measured (`git status --porcelain` showed ` M SCORECARD.md`,
` M corpus/QUALITY.md`, ` M corpus/instruments/frontier-recheck-count.py`,
` M corpus/source-snapshots/round-32/manifest.json`, `?? corpus/source-snapshots/round-34/`); every count above
is bound to the digests listed, not to the eventual tip.

### 7. Findings and limits

- **Scope defect (self-inflicted, repaired).** My first write of this receipt resolved its relative path
  against the fleet root, so a copy landed at
  `/home/vgpnk/Projects/shokunin/.ufo/waves/round-34/wave1/ScribeSearchLog.md` (14938 B) — outside my lane
  write scope. Repair: copied the file into the lane at the assigned path, deleted the stray copy
  (`test -e` on the fleet path → `ABSENT`), then removed the two directories that write had created
  (`…/.ufo/waves/round-34/wave1` and `…/.ufo/waves/round-34`; both carried the same 02:33 mtime as the stray
  file and were empty after its deletion, so `rmdir` succeeded). No pre-existing fleet file was removed.
  `SentScopeFinal`/`CritBoundary` should still sweep the fleet root independently; this note is my own
  disclosure, not a clearance.
- **Finding (supports C2):** the lane held **no** Web3/smart-contract severity-classification source before
  this round — `VSCS`, `severity classification`, `smart contract`, `blockchain` all 0 in
  `corpus/knowledge/*.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`.
- **Finding (verifier bait):** v2.3 exists, is concurrently in use, and states a **4-level** scale. Any round-34
  text claiming the 5-level scale is "Immunefi's current system" without the v2.2 qualifier is a defect; the
  draft bullet and constraint 3 are written to prevent it.
- **Limit:** the index's Help Desk impacts article was not opened (secondary explainer for v2.3); the manifest
  for the round-34 capture did not yet exist, so no `source-recheck` run appears here; and my HTML digests are
  not comparable to the capture's text digest (different UA, HTML→text extraction).
- **Unobserved, therefore not claimed:** live re-open stability of the page beyond the single fetch recorded
  (`ScoutImmunefiLive` owns the second fetch and the differing-line comparison), and any sibling-lane overlap
  (`ScoutSiblingSweep`/`ConnSibling` own that ruling).
