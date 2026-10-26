# RevRowS054 — planned S054 registry row: SOURCES-contract audit + census simulation (round 37, C2 coverage)

Seat: `RevRowS054` (reviewer), leaf, no subagent dispatch used.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Lane head during verification: `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(round-37 claims-erratum-1). Claims freeze `224df74db2a46d627ae1475a72ca48796bbd177c`; erratum applied:
`.ufo/waves/round-37/claims-erratum-1.md` (capture URL literal → `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`).
`corpus/SOURCES.md` at verification: sha256 `2ff7818ad2179c1f8ecf89262e3f8a84a585dfb4f64bbc1fa0e7dbc3be2465fe`,
worktree byte-equal to HEAD, **0** `S054` rows, 48 knowledge entries — the row and entry are not landed yet, so
this audit is of the **planned** row, per the item.

## 1. The audited row (verbatim, byte-reproduced)

Source of truth: `.ufo/waves/round-37/wave1/ScribeRowS054.md` §1 (the drafting seat's delivered row). I
re-staged the line into scratch and hashed it:

```
| S054 | SSVC: Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ | docs | A | CERT/CC's own SSVC documentation: decision-point-based prioritization for vulnerability management | the overview definition sentence at line 247 of capture corpus/source-snapshots/round-37/S054.txt (SSVC rates vulnerabilities on risk to the concerned stakeholder), the categorization opener at line 259, and the outcome/decision-point sections at lines 261-265 and 277-281 | SSVC is a modular decision-point system for prioritizing vulnerability-management actions for a stakeholder — distinct from CVSS severity, KEV catalog status and EPSS likelihood; read each stakeholder model's chosen decision points and outcomes | mined | 2026-10-26 | 90d | corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |
```

- 866 bytes with trailing newline, sha256 `83020b30ca32fd49c2a1cd85864792d01004a594b59ad2f13fb83e1e6f734f03`
  — byte-identical to the sha the ScribeRowS054 receipt states for its delivered row.
- Planned insertion point: directly after the `| S053 |` row (`corpus/SOURCES.md:59`), i.e. as line 60, inside
  the `## Registry` table (Registry spans to line 60 today; `## Paths` starts at line 61).

## 2. Contract audit (CORPUS.md §"SOURCES.md — where a shokunin learns", contract v1 frozen; census E/W codes from `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:24-33`)

| check | result | evidence |
|---|---|---|
| 11 columns, NF=13 under `awk -F'|'` | **pass** | `awk -F'|' '{print "NF="NF" cells="NF-2}' row.txt` → `NF=13 cells=11` |
| no `|` inside cells (literal or escaped) | **pass** | structural pipes `12` (1 leading + 11 separators; trailing pipe is the 12th... measured `tr -cd '|' < row.txt \| wc -c` → `12`), escaped `\|` count `0`. No cell content contains a pipe |
| id enum: `S[0-9]{3,}`, next unused (E02/E03) | **pass** | `S054` matches; pristine registry has **0** `S054` rows (`grep -cE '^\|[[:space:]]*S054[[:space:]]*\|'` → 0), max existing id `S053` |
| kind enum `docs` (E05) | **pass** | cell 3 = `docs` |
| tier enum `A` (E06) | **pass** | cell 4 = `A` |
| status enum `mined` (E07) | **pass** | cell 8 = `mined` |
| tier-A-not-community (E10) | **pass** | tier `A` with kind `docs`; contract bars `community` at A. Tier A is justified by the contract's own definition ("official docs" = primary for the scope), and the scope cell bounds it to CERT/CC's own SSVC documentation |
| scope/anchor/teaches coherence | **pass** | see §3 — every anchor line exists in the pinned capture bytes and the teaches distinctions map onto them |
| opened ISO date, past/present (E08) | **pass** | `2026-10-26` = today (UTC); not future |
| recheck cadence in vocabulary (E09) | **pass** | `90d` matches `^[0-9]+d$` |
| used-by path exists (E11) | **pass in simulation; open in lane** | cell 11 = `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` — the planned entry path; **not on disk in the lane yet** (48 entries). See §5 finding F1 |
| row inside `## Registry` (E12) | **pass** | inserted after `S053`, before `## Paths`; validate emits no E12 |
| exactly one `https://` token = corrected URL (capture-binding B4/B5 row side) | **pass** | `grep -o 'https://[^[:space:]\|]*' row.txt` → single token `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`; byte-equal to the capture seat's byte-exact manifest record `url` (`.ufo/waves/round-37/wave1/ExecC2Capture.md:650`), trailing slash included |
| no duplicate URL+scope / cross-scope URL (E04/W04) | **pass** | pristine registry's only `certcc` mention is S004 `https://certcc.github.io/certcc_disclosure_policy/` (`SOURCES.md:10`) — different path; validate emits no new W04/E04 for S054 (§4) |

## 3. Anchor grounding against the pinned capture bytes

Capture reference: `corpus/source-snapshots/round-37/S054.txt` as staged by the capture/entry seats —
518 lines, 32,623 bytes, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`
(byte-identical across four surviving peer-scratch copies: `CritC2Claim/S054.txt`,
`ExecDatawalk/S054-overview.txt`, `RevSourceRecheck/S054.txt`, `RevHarnessSync-2/S054.real.txt`; I copied one
into my scratch and hashed it there). Verified against those bytes:

- **L247** exists and contains the quoted definition sentence — `SSVC rates vulnerabilities on risk to the
  concerned stakeholder` occurs **1×** in the capture. The same line carries `technical severity (how bad it
  could be if the vulnerability were exploited)` and `exploitability (how likely it is that there will be an
  exploit)`.
- **L259** exists: `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.`
  — occurs **1×**.
- **L261–L265** exist: the outcome-category section (`Defer` / `Scheduled` / `Out-of-cycle` / `Immediate`).
- **L277–L281** exist: the decision-point section opener (`All decision points and decision outcomes … must be
  explainable to the non-expert`) through the first decision point (`Exploitation refers to how much evidence
  currently exists that the vulnerability is being exploited`).

Coherence reading: scope names CERT/CC's own documentation and decision-point-based prioritization; the anchor
cites the definition sentence (L247), the categorization opener (L259), the outcome categories (L261-265) and
the decision-point section (L277-281); teaches' three-way distinction is grounded in those same lines —
"distinct from CVSS severity" ← L247 `technical severity`; "EPSS likelihood" ← L247 `exploitability (how likely
it is that there will be an exploit)`; "KEV catalog status" ← L280-281 exploitation-evidence decision point.
No cell claims anything outside the captured page. (The KEV/EPSS names are the frontier-row framing shared
with the F20 README row; the capture grounds the underlying distinctions, not the product names.)

## 4. Simulation — `validate --file` over a scratch copy with the row appended

Fixture (all under my scratch, lane untouched): `fixture/` = lane `corpus/SOURCES.md` (sha `2ff7818a…`,
53 rows) + copies of lane `corpus/knowledge/` (48 files) and `corpus/lessons/` + the row inserted after the
`| S053 |` row + a clearly-labelled stub file at
`fixture/corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` standing in for the
planned entry (the E11 check resolves used-by paths against the parent of `corpus/`, per
`sources-census.sh` `resolve_targets`: `dir = realpath(dirname(file)/..)`).

Insertion command: `awk '{print} /^\| S053 \|/{while ((getline l < "row.txt") > 0) print l; close("row.txt")}' fixture/corpus/SOURCES.md`

Integrity: `diff pristine.md fixture/corpus/SOURCES.md` → exactly one added line, `59a60`, the S054 row; no
other line changes.

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file .../RevRowS054/fixture/corpus/SOURCES.md --today 2026-10-26
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r37/RevRowS054/fixture/corpus/SOURCES.md
VALIDATE_EXIT=0
```

**exit 0, zero E-codes**; the only findings are the two pre-existing W04 duplicate-URL warnings (S028, S029)
that the frozen C2 claim already discloses as the expected census state. The S054 row adds no E-code and no
new warning.

```
$ .../sources-census.sh census --file .../fixture/corpus/SOURCES.md
file	rows	54
file	tier.A	51
file	tier.B	1
file	tier.C	2
file	status.mined	42
file	status.queued	9
file	status.rejected	3
CENSUS_EXIT=0
```

`rows 54` reproduces the C2 counting command's expected post-insertion value
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 54`). Pristine baseline measured on
the same bytes: rows 53, tier.A 50 / B 1 / C 2, status mined 41 / queued 9 / rejected 3, kind docs 40 /
dataset 3 / spec 8 / paper 1 / community 1, recheck on-release 15 / 180d 17 / 90d 18 / 730d 3.

## 5. Discriminating controls (the simulation is not vacuous)

| control | mutation | result |
|---|---|---|
| E11 load-bearing | stub file removed, validate rerun | `file	E11	S054 missing used-by corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`, exit **1** — the used-by existence check fires on exactly this row when its target is absent; the stub is what makes it pass |
| E06 mutant | S054 tier `A`→`Z` | `file	E06	S054 tier=Z`, exit **1** (the same sed also hit S004's `| docs | A | CERT` prefix — mutant artifact, disclosed) |
| E01 mutant | S054 used-by cell dropped | mutant row `NF=12`, `file	E01	S054 fields=10`, exit **1** |

Artifact note: the two mutants were validated from files at the scratch root, so their `dir` resolves one level
higher and unrelated E11 lines appear; the E06/E01 signals quoted above are the intended ones. The main
simulation ran from `fixture/corpus/SOURCES.md`, where `dir` = the fixture root and the knowledge copies make
E11 exact.

## 6. Findings for the L1

1. **F1 — sequencing dependency (blocking for the real-lane census).** The used-by target
   `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` does not exist in the lane at
   head `b362068` (48 entries). If the row lands before the entry, the real-lane `validate` emits
   `E11 S054 missing used-by …` and exits 1, breaking C2's "census exit 0" leg. Land the entry before or with
   the row.
2. **F2 — stale L1 prep copy.** `/fast/scratch/hyaku/kasegi-r37/l1prep/S054-row.txt` (sha256
   `79038d630a970ccac4252ce5591f6f8c87b0cb6bfc484c47618c60abd0fee318`) is an earlier draft: its scope cell
   reads `CERT/CC's own SSVC overview: stakeholder-tailored decision-point prioritization…` and its anchor
   cites only `"SSVC rates vulnerabilities on risk to the concerned stakeholder." (S054.txt L247)`. It is also
   census-clean (NF=13, same corrected URL), but the audited row is the ScribeRowS054 receipt's delivered row
   (sha `83020b30…`, anchor citing L247 + L259 + L261-265 + L277-281). Apply the receipt row verbatim, not the
   l1prep copy.
3. **F3 — ScribeRowS054 §2 histogram drift (cross-seat observation, row unaffected).** Her audit-table
   histograms do not reproduce against the pristine 53-row registry: she wrote tier `A 51 / B 1 / C 2`
   (sums 54 ≠ 53; truth A 50 / B 1 / C 2), kind `docs 41 / dataset 2` (truth docs 40 / dataset 3), recheck
   `90d 15 / 180d 16 / on-release 17 / 730d 4` (truth 90d 18 / 180d 17 / on-release 15 / 730d 3). Her
   post-insertion values for docs/tier.A/mined match mine (41 / 51 / 42); the pristine-side numbers are the
   drifted ones. The row's own cells are unaffected.
4. **F4 — B5 context.** The row side of capture-binding B4/B5 is satisfied (single token, byte-equal to the
   capture seat's byte-exact manifest `url`, `ExecC2Capture.md:650`). A divergent manifest copy exists in peer
   scratch (`RevSourceRecheck/manifest.json`, sha `5ba8abe0…`: no `url` field, anchors 244/256/274/364 — a
   3-line-offset capture variant). Not my seat's defect to resolve; recording it so the L1 lands the capture
   seat's manifest (sha `fabc3163dbd31d33bff6e0bccf8b86b94e081b06b3ab1f00538dd9c0a57df642`, 3,989 B), which is
   the one that binds.
5. **F5 — erratum followed.** The frozen C2 predicate still prints the home-page literal; the row uses the
   erratum-1 corrected URL, as the erratum directs and as rule B5 requires. Same resolution ScribeRowS054 §5
   recorded; no new conflict.
6. **F6 — id-collision context is label-only.** `corpus/lessons/round-35.md:120` uses the token `S054` as a
   quarantine label for a different payload (513,648 B IPA PDF); no registry row ever carried the id (0 hits
   in the pristine registry). No E03 risk.

## 7. Verdict

The planned S054 row **complies with the SOURCES contract**: 11 columns (NF=13), enums `docs`/`A`/`mined`,
no pipes inside cells, tier A justified and not community, scope/anchor/teaches coherent and grounded in the
pinned capture bytes, opened `2026-10-26` (ISO, present), recheck `90d` (permitted cadence), used-by naming
exactly the planned entry path. The `validate --file` simulation over a scratch copy with the row inserted
after `S053` prints **exit 0 with zero E-codes** (only the two pre-existing W04 warnings), and controls show
the E11/E06/E01 checks fire when the row or its environment is mutated. One open dependency (F1: entry must
land with/before the row) and one stale-copy caution (F2) go to the L1.

## 8. Touched surfaces

- Writes: `/fast/scratch/hyaku/kasegi-r37/RevRowS054/` (fixture, `row.txt`, `pristine.md`, `mut-E06.md`,
  `mut-E01.md`, `pinned/{S054.txt,manifest.json}`) and this receipt only. Scratch removed after filing.
- Reads only: lane repo (`corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`,
  `corpus/instruments/capture-binding-check.py`, `.ufo/waves/round-37/*`), fleet root
  (`/home/vgpnk/Projects/shokunin/CORPUS.md`, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` —
  executed read-only in `validate`/`census` modes against my fixture), peer scratch dirs (hash + copy of the
  pinned capture bytes). No mutating git/jj command; no lane/fleet/sibling/source-tree write; no tool install
  or upgrade (pre-existing `bash`, `gawk`, `git`, `jq`, `grep`, `sed` on scratch copies only); no swarm; no
  `agent://all` message.

Report: `.ufo/waves/round-37/wave1/RevRowS054.md`
