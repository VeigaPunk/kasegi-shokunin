# ScoutSiblingSweep — round 35 wave 1 (negative sweep for C2 / F18 / S052)

Question: does any sibling lane (all `/home/vgpnk/Projects/shokunin/*-shokunin/` except kasegi) already hold CISA KEV / known-exploited-vulnerabilities / BOD 22-01 / remediation-deadline material in its corpus or SKILL.md? Same tokens at the fleet root and in the merge/considerthese themes.

## Report

Method: `rg -i -n` over `<lane>/corpus` (recursive, includes SOURCES.md, knowledge/, lessons/, evidence/) and `<lane>/SKILL.md` for each of 20 siblings. Patterns: `\bCISA\b|\bKEV\b|known exploited|BOD 22-01|exploited vulnerabilit|remediation deadline`. Word boundaries are needed: an unbounded `CISA` case-insensitive match false-hits "exer**cisa**ble" (kaidoku x3 files, chousa, kotoba, kake lesson-47 — all false positives, discarded). Missing SKILL.md: `audio-shokunin`, `game-dev-2d-shokunin` (only corpus searched there; zero hits).

### Per-sibling result (corpus + SKILL.md)

| sibling | hits |
|---|---|
| audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi | ZERO (19 lanes) |
| kake | 2 files, 3 lines, all about the CISA **BOD 20-01 VDP template**, not KEV / BOD 22-01 / deadlines (below) |

kake hits:
- `kake-shokunin/corpus/lessons/round-35.md:58` — "It proposed rejecting the CISA BOD 20-01 template: “Your policy must be published as a public web page …/vulnerability-disclosure-policy”. That template names neither security.txt nor `.well-known`." Wave-1 scout candidate for a security.txt question; rejected, no row. Topic = VDP publication path, not exploitation-status prioritization.
- `kake-shokunin/corpus/SOURCES.md:255` — round-35 bounded-question paragraph repeating the same screened-and-rejected BOD 20-01 candidate (identified 11, 6 more screened, none given a row).
- (Third line counted in an earlier pass was lesson-47 `exercisable`, a false positive.)

No sibling holds: "Known Exploited Vulnerabilities", `KEV`, `BOD 22-01`, "remediation deadline", "exploited vulnerabilities". **Zero overlap with F18/S052 in any of the 19+1 sibling lanes.**

### Other lane files (PROVINCE.md, README, AGENTS, considerthese/, plans/, SCORECARD, LOG, etc., excluding corpus)
`rg -i -n` with the same pattern over all sibling lane trees outside `corpus/` → zero hits (all 20 siblings; kasegi excluded). Sibling `considerthese/` dirs (13 siblings have one): zero hits.

### Adjacent-theme semantic sweep (CVSS|EPSS|SSVC|actively exploited|in the wild|NVD|exploitation status|vulnerability prioriti*) over sibling corpus/SKILL.md/considerthese/PROVINCE.md
Only incidental hits; none concern exploitation-status prioritization:
- `kagi-shokunin/corpus/lessons/round-28.md:43,151,154` and `kagi-shokunin/corpus/SOURCES.md:89` — NVD REST API used to quote CVE-2020-10735 (Python int-conversion limit), "NOT REGISTERED" as a source; kagi's topic is version-token typing.
- `mori-shokunin/corpus/evidence/recheck-r32/S012.src:1230,1242,1255` — a fetched GitHub advisory HTML page containing the string "CVSS overall score" (raw evidence blob, not a taught claim).
- `kotoba SOURCES.md:354`, `kotodama append-only-record-verification.md:40`, `kotodama lessons/round-8.md:133`, `tabi external-class-fixture-v2.md:547`, `tabi w6-aud-b6-scratch/*`, `mori S175.src:2014` — "in the wild" in unrelated senses (mutation testing, record state, curl docs).
No sibling teaches CVSS-vs-exploitation distinction, EPSS, SSVC, or KEV.

### Fleet root (`/home/vgpnk/Projects/shokunin`, read-only)
- All files outside `*-shokunin/**` (AGENTS, AXES, CORPUS, LEARNING, LOG, MANIFEST.json, MISSION, PROTOCOL*, README, ROADMAP, SCORECARD, research/, scripts/, templates/, ok, m-rev-vs-rev.py): `rg -i -n` same pattern → ZERO hits. No fleet-root `merge/` or `considerthese/` dir exists in `/home/vgpnk/Projects/shokunin` (the merge tree is in shokuknow, below). `research/` holds deep-research-2026-09-28 + round-18-kimi-model-routing, zero hits.

### shokuknow (read-only; no campaign tools run, nothing written)
`rg` over `/home/vgpnk/Projects/shokuknow/{merge,doctrine,lanes,README.md}`:
- `merge/*` (21 lane dirs incl. kasegi: MERGE-REPORT.md/json, SOURCES.append.md, knowledge/): ZERO hits for the five tokens.
- `doctrine/channel-recurrence.md:62` — `| cisa.gov | kasegi |` : host `cisa.gov` is assigned to kasegi in the shokuknow channel-recurrence table (adjacent rows: cert.org.cn, cnnvd.org.cn, cnvd.org.cn, butian.net → kasegi). This is the only ownership statement; **it favors kasegi's claim on the CISA host.**
- `lanes/kasegi/DOMAIN.md:41` registry "30 rows, 20 hosts, all Western: CISA (5), FIRST (3), Project Zero (3)…"; `:59` F02 coordinator timelines (CISA, CERT/CC, P0); `:60` F03 CISA VDP safe harbor; `lanes/kasegi/CHANNELS.md:14` CISA VDP Template (held as S008); `lanes/kasegi/CANNOT-ANSWER.md:148`; `lanes/kasegi/round7/KNOWLEDGE-PROPOSED.md:4` and `round7|round8/evidence/zxd_wd.txt:2733` cite "[4] CISA Stakeholder-Specific Vulnerability Categorization Guide 2022" (an SSVC reference inside kasegi's own round7/8 evidence — kasegi-owned, not another lane).
- No other lane's shokuknow dir (`lanes/<other>/`) matched any of the tokens.

### Kasegi baseline for context
`rg -i -c` on `kasegi-shokunin/corpus/SOURCES.md`: CISA/KEV lines = 10 (S003, S008, S021, S023, S026 existing CISA rows; S052 KEV row at SOURCES.md:58, with sweep note :79 and S052 row-added note :108 — already present in the working tree).

### Verdict for the connector (contested scope)
- Siblings with KEV/BOD 22-01/known-exploited/remediation-deadline content: **none (20/20 zero)**.
- Nearest neighbor: kake's rejected BOD 20-01 VDP-template candidate (different directive, different topic, no row created, explicitly not taught).
- Fleet root and shokuknow merge themes: zero for the tokens; shokuknow doctrine assigns `cisa.gov` to kasegi.
- F18/S052 is uncontested by any sibling corpus; no scope conflict found. `[INFERENCE]` that overlap could only arise in kake (publisher-side security.txt/VDP) or kagi (CVE/NVD usage) and neither teaches exploitation-status prioritization.

### Commands (abridged)
```
cd /home/vgpnk/Projects/shokunin
P='\bCISA\b|\bKEV\b|known exploited|BOD 22-01|exploited vulnerabilit|remediation deadline'
for d in *-shokunin; do [ $d = kasegi-shokunin ] && continue; rg -i -n --no-heading -e "$P" $d/corpus $d/SKILL.md; done        # exit 0; only kake lines above
rg -i -n -e "$P" -g '!kasegi-shokunin/**' -g '!*/corpus/**' -g '!.git' *-shokunin                                              # zero
rg -i -n -e "$P" -g '!*-shokunin/**' .                                                                                         # zero (fleet root)
rg -i -n -e "$P" /home/vgpnk/Projects/shokuknow/{merge,doctrine,lanes,README.md}                                                # kasegi-owned + channel-recurrence.md:62 only
```
All exit 0 / no errors beyond `No such file` for the two absent SKILL.md files.

### File digests (sha256, evidence files read)
- kake-shokunin/corpus/lessons/round-35.md `cffb84a5e1e8627aebe51eddf36fe487b165f15fc652bf63e6174dc45282c413`
- kake-shokunin/corpus/SOURCES.md `57c83362dbc6ba81dc45351f1bcdc33aecbb2b448a6343a95a1a585feccbe4ea`
- shokuknow/doctrine/channel-recurrence.md `7ec813c70973b4d3c37210120b88889b558a1c7a30b395220d7b9df29c1400d1`
- shokuknow/lanes/kasegi/DOMAIN.md `08c28d44ec3a7a610e85e104217daff76c6b68b03623c300f5c554f57349f5e5`

### Housekeeping
No scratch dir created (read-only search only); nothing to clean. No tool installs. No writes outside this receipt. No jj/git mutations, no subagents, no shokuknow campaign tools.
