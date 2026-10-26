# ScribeSourcesLog — receipt (round 38, wave 1)

Seat: ScribeSourcesLog (scribe, leaf). Axis owned by the round: coverage (C2). Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Read-only inputs honoured: fleet root, `shokuknow` (greps only, no campaign tools).

Lane state where the draft was measured: `git -C . rev-parse HEAD` = `700153593eb586c70a6499c8ca225ee4d673bc9b` (`round-38: wave1 spec + validated dispatch (73 seats, v2)`), base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, claims-freeze `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`. `git status --porcelain` showed only untracked round-38 wave paths (`.ufo/waves/round-38/wave1.ready`, `wave1.ready.partial`, `wave1/`); `corpus/SOURCES.md` clean.

## Deliverable

Path: `.ufo/waves/round-38/wave1/ScribeSourcesLog.blocks.md`
Bytes: 4007. Lines: 6. sha256: `14c632b2a9f7534b7aff19d5b20aeefc02ef8ddca45f67a974cbf2c96b33795a`.

Structure (comment lines are markers, not landable bytes):

| # | content | lines | bytes-ish | sha256 |
|---|---|---|---|---|
| 1 | `<!-- target: corpus/SOURCES.md ## Registry changes ... -->` | 1 | — | — |
| 2-3 | two `- ...` registry-change bullets (landable) | 2 | — | `d5636fa4813f01c09894690b5061ee079241314fa5ef0de6bfe94a45d0cdaca5` |
| 4 | blank | 1 | — | — |
| 5 | `<!-- target: corpus/SOURCES.md ## Search log ... -->` | 1 | — | — |
| 6 | search-log bullet (landable) | 1 | 2456 bytes incl. newline | `59fcb58ed1172a54f0a029137e68cb882299a3ed0c4aaca311b86e2a45177701` |

Landing instructions (measured against `corpus/SOURCES.md` at HEAD `7001535`, 118 lines):
- Registry bullets: append after line 118, which is the last bullet of `## Registry changes` (the section is the file's last section). `tail -c 1` of SOURCES.md is `\n`, so a plain append needs no separator.
- Search-log bullet: insert after line 84 (last bullet of `## Search log`), before line 85 `## Leads (unopened)`. It is **not** an EOF append.
- Drop lines 1, 4, 5 of the deliverable when landing; keep the two registry bullets and the one search-log bullet byte-intact.

Simulated landing into scratch (not the lane file): `cp corpus/SOURCES.md sim-SOURCES.md`, append block 2-3, blank, block 6 → 122 lines, registry table rows 54, no other section changed. (The S055 table row itself is C2's landing, not this block's: the bullets are records.)

## Evidence — commands and actual output

### 1. Registry pre-state and id availability

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
54
$ tail -3 .ufo/waves/round-38/wave1/ExecIdCollision.reg-ids
S052
S053
S054
$ wc -l .ufo/waves/round-38/wave1/ExecIdCollision.{reg-ids,collisions,staged-ids}
 54 reg-ids   24 collisions   94 staged-ids
$ grep -c 'S055' ExecIdCollision.collisions ExecIdCollision.reg-ids
ExecIdCollision.collisions:0
ExecIdCollision.reg-ids:0
```

→ 54 registry rows (S001–S054), S055 unused, no collision touching S055. This grounds the bullet's `S001–S054` / `54 rows pre-append → 55 post-append` and "S055 unused".

### 2. In-lane negative sweep (PRE-STATE for S055)

```
$ ls corpus/knowledge/*.md | wc -l
49
$ for t in csaf 'common security advisory framework' vex product_status not_affected justification; do
    n=$(grep -rniF -- "$t" corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md | wc -l); echo "$t -> $n"; done
csaf -> 0
common security advisory framework -> 0
vex -> 0
product_status -> 0
not_affected -> 0
justification -> 0
```

Six terms, six zeros, over `corpus/knowledge/*.md` (49 files, pre-F21), `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`.

### 3. Sibling sweep (fleet root, read-only)

```
$ find . -maxdepth 1 -mindepth 1 -type d -name '*shokunin' | wc -l
21
$ for d in $(... '*shokunin' ...); do n=$(grep -rilE 'csaf|\bvex\b|vulnerability exploitability exchange' "$d/corpus" --include='*.md' | wc -l); ...; done
kake-shokunin md_hits=1 :: kake-shokunin/corpus/knowledge/security-txt-publishing.md
$ grep -liE 'csaf|\bvex\b' */corpus/SOURCES.md
(no output, exit 2)
$ grep -niE 'csaf|common security advisory framework|\bvex\b' kake-shokunin/corpus/knowledge/security-txt-publishing.md
63:  be ignored (S078); securitytxt.org already lists one extension, `CSAF` (S079).
```

21 `*-shokunin` lane roots = kasegi + 20 siblings; the only sibling markdown hit is kake line 63 (a security.txt extension name, not the standard); no sibling `corpus/SOURCES.md` carries a CSAF/VEX row. An unscoped sweep also matched `audio-shokunin/.../peak-31129.wav`, `peak-31130.wav` and `mori-shokunin/corpus/evidence/sources-r42/S235.pdf` — raw-byte coincidences in binary artefacts, carrying no text claim; screened out and not reported as hits.

Lane's own incidental mentions (not new ground, no row): `corpus/source-snapshots/round-24/S003.txt:287,293` (CISA CVD page: "Publish advisories using the Common Security Advisory Framework (CSAF)"), `round-24/S001.txt:1123` (a VEX mention inside the CVSS capture), `round-25/S040.txt` and `round-26/S040-live.txt:240,269,355,356` (Cisco policy naming CSAF as an output format).

### 4. Staged package (shokuknow, read-only)

```
$ grep -cE '^\| S[0-9]{3} ' merge/kasegi/SOURCES.append.md
94
$ grep -ciE 'csaf|vex' merge/kasegi/SOURCES.append.md
0   (exit 1)
$ grep -rliE 'csaf' merge/kasegi
(no output)
```

94 staged rows, 0 CSAF/VEX → S055 is a live-capture admission, not a staged row (statement in the registry bullet is grounded).

### 5. Live fetches (instrument UA `-A kasegi-shokunin/1.0`, `--max-time 90/60`)

| # | URL | status | bytes | ctype | effective URL | UTC |
|---|---|---|---|---|---|---|
| 1 | `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` | 200 | 414858 | text/html | same (no redirect) | 2026-10-26T18:30:10Z |
| 2 | `https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html` | 200 | 1231332 | text/html | same | 2026-10-26T18:30:55Z |
| 3 | `https://docs.oasis-open.org/csaf/csaf/v2.1/os/csaf-v2.1-os.html` | 404 | 41334 | text/html | same | 2026-10-26T18:30:55Z |
| 4 | `https://www.cisa.gov/resources-tools/resources/vex-minimum-requirements` | 404 | 46961 | text/html | same | 2026-10-26T18:30:56Z |
| 5 | `https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex` | 200 | 49253 | text/html | same | 2026-10-26T18:31:15Z |
| 6 | `https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf` | 200 | 313386 | application/pdf | same | 2026-10-26T18:31:17Z |

Fetch 1 sha256 (scratch HTML body only, **not** the lane capture): `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b`. Fetch 6 was made only to confirm the `[VEX-Justification]` reference printed in CSAF §3.2.3.5 resolves; it was not screened as a candidate. No lane capture was created by this seat (`corpus/source-snapshots/round-38/` does not exist yet; capture and manifest are C2's).

### 6. Section grounding for the anchor cell (fetch 1, converted to text for reading only)

```
1 Common Security Advisory Framework Version 2.0
3 OASIS Standard
4 18 November 2022
196 3.2.3 Vulnerabilities Property
201 3.2.3.5 Vulnerabilities Property - Flags
205 3.2.3.9 Vulnerabilities Property - Product Status
265 6.1.27.7 VEX Product Status
3964 4.5 Profile 5: VEX
```

- §3.2.3.5: "Valid enum values are: component_not_present, inline_mitigations_already_exist, vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path, vulnerable_code_not_present" followed by "The given values reflect the VEX not affected justifications."
- §3.2.3.9: eight `product_status` lists — first_affected, first_fixed, fixed, known_affected, known_not_affected, last_affected, recommended, under_investigation.
- §4.5: "For each item in `/vulnerabilities[]/product_status/known_not_affected` an impact statement SHALL exist as machine readable flag in `/vulnerabilities[]/flags` or as human readable justification in `/vulnerabilities[]/threats`"; "The value of `/document/category` SHALL be `csaf_vex`."
- CSAF v2.1 front matter (fetch 2): "Committee Specification Draft 04", "21 October 2026" — a draft, hence excluded; `/csaf/v2.1/os/` 404 (fetch 3) confirms no approved-standard stage.
- CISA page (fetch 5): "Publish Date April 21, 2023"; body sentence "These elements are derived from, but may not fully conform to, existing VEX documentation" — the quoted exclusion reason.

### 7. Deliverable checks

```
$ wc -l -c .ufo/waves/round-38/wave1/ScribeSourcesLog.blocks.md
6 4007
$ sha256sum .ufo/waves/round-38/wave1/ScribeSourcesLog.blocks.md
14c632b2a9f7534b7aff19d5b20aeefc02ef8ddca45f67a974cbf2c96b33795a
$ grep -nE '<sha256>|sha256 [0-9a-f]{64}|\bTODO\b|⟨pending|PLACEHOLDER' <deliverable>
(no output; grep exit 1)
$ cp corpus/SOURCES.md sim-SOURCES.md; append blocks; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' sim-SOURCES.md
54
$ wc -l sim-SOURCES.md
122
```

No hex digest, no `sha256` placeholder, no `TODO`/`⟨pending` token in the deliverable; the digest is referenced only as "capture digest and quote line pins in `corpus/source-snapshots/round-38/manifest.json`" as the item directs.

## Findings

1. **Item premise correction (routed as a finding, not fixed):** the `## Registry changes` section has **no S053 and no S054 bullet** at base `a173b0c2` / HEAD `7001535`. Its last bullet (line 118) is the round-35 S052 Search-log digest correction; `grep -n 'S053\|S054' corpus/SOURCES.md` returns 4 lines, all elsewhere (registry rows at 59-60, `## Paths` at 69, `## Search log` at 84). So the round-36/round-37 append bullets were never landed, while their rows were. My draft therefore follows the S051/S052 registry-bullet shape (the most recent `- S0NN row added:` bullets present) rather than an S054 precedent. Adding the missing S053/S054 bullets is out of my write scope (it would edit a pre-existing section outside the S055 append) and stays with the L1.
2. The block does **not** create the S055 table row; C2's landing owns the row (claim cell set: kind `spec`, tier A, status `mined`, opened `2026-10-26`, used-by `corpus/knowledge/csaf-vex-product-status-and-justifications.md`). The bullets are the R8 record of that append.
3. `recheck` cell chosen as `on-release` — precedent: the spec rows S002, S022, S030, S031 all carry `on-release`; a published OASIS Standard's text does not drift, and a successor arrives as a new version (v2.1 CSD04 observed). If the L1 prefers a clock cadence (`180d` as on S041/S046/S048), that is a single-token change in line 2 and does not affect the digest-free anchor.
4. The anchor pins **section numbers** on the round-38 capture (plus the §-level quote set) instead of capture line numbers: the C2 capture did not exist at drafting time, and inventing line numbers would not survive a different HTML→text conversion. Per the item, the digest and quote line pins live in `corpus/source-snapshots/round-38/manifest.json`; if the C2 seat's manifest pins concrete `L` values for the same sections, the anchor can be tightened to `capture ... : <section> L<n>` without touching the rest of the bullet.
5. Search-log counts are honest about what was screened: `identified 3, screened 3, included 1, excluded 2` covers CSAF v2.0 OS, CSAF v2.1 CSD04 and CISA's VEX minimum requirements. The CISA `VEX_Status_Justification_Jun22.pdf` (fetch 6) was reached as a resolved citation, not screened as a candidate, so it is not counted.
6. The `## Search log` insertion point is line 84/85 (before `## Leads (unopened)`), not EOF; landing it at EOF would put a search-log bullet inside `## Registry changes` (the same class of misplacement as round-37 D-A).

## Out of scope / untouched

- No edit to `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/*`, `corpus/source-snapshots/*`, instruments, SCORECARD, SHONEN, PROVINCE, ledger, or any `.ufo` file other than this receipt and the `.blocks.md` deliverable.
- No lane capture and no `corpus/source-snapshots/round-38/` directory created (C2 owns capture + manifest); no entry authored.
- No `## Paths` line drafted (not in the item).
- No tool installed or upgraded (no pacman, no `uv tool install`, no `npx`): the work needed `curl`, `python3`, `grep`, `awk`, `sha256sum`, all already present.
- No subagent dispatched; no `agent://all` message.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r38/ScribeSourcesLog` created with `mkdir -p`; contents used: `S055.raw`, `S055.txt`, `cisa-minimum-requirements.out`, `cisa-VEX_Status_Justifica.out`, `88e58dee.out` (v2.1), `sim-SOURCES.md`, `siblings.txt`, md5-named 404 bodies. All work copies lived under `$S`; nothing written to `/tmp`. `rm -rf -- "$S"` run after the deliverable and this receipt were in place; scratch directory does not survive this seat.
