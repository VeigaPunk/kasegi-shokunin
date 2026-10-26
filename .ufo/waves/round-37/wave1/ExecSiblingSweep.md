# ExecSiblingSweep — negative sibling sweep for SSVC ground (round 37)

Seat: ExecSiblingSweep (leaf executor, round-37 wave 1). Read-only over the 20 sibling lanes,
kagi, and shokuknow; no lane/fleet/shokuknow write. Findings only — no absorption.

## Verdict

**F20 / S054 is UNCONTESTED as a claim, and its adjacency is dense rather than empty.**

- No sibling lane anywhere under `/home/vgpnk/Projects/shokunin/*-shokunin/` (kasegi excluded)
  mentions SSVC, Stakeholder-Specific Vulnerability Categorization, CERT/CC (Carnegie Mellon),
  `certcc.github.io`, CERT Coordination Center, Vultron, VINCE, or `vulnerability categoriz`
  in `corpus/`, `SKILL.md`, or `PROVINCE.md` — or anywhere else in those repos.
- The only semantic SSVC payload in the fleet lives in **kagi** and was never absorbed:
  `kagi-shokunin/.ufo/waves/round-28/retained-probes/SrcCve202010735/*.json` (4 captures) each
  carry `vulnerabilities[0].cve.metrics.ssvcV203[0].ssvcData` — CISA Coordinator, **version
  2.0.3**, `timestamp 2026-10-07T18:38:50.558859Z`, `exploitation=none`, `automatable=no`,
  `technicalImpact=partial`, `id=CVE-2020-10735`. kagi's round-28 build note explicitly
  **REJECTED registering** that CVE row and never names SSVC, and no kagi source row or
  knowledge entry cites it (see §4).
- The nearest *host-level* precedent is inside kasegi itself (not a sibling): round-24 snapshot
  **S004 = `https://certcc.github.io/certcc_disclosure_policy/`** (manifest-bound), and SSVC is
  already named verbatim in four committed kasegi captures (S001/S003/S004/S008, §5). So S054's
  novelty is **page-level** (`https://certcc.github.io/SSVC/`), never host-level or concept-level.
- Nothing to route for absorption: no sibling claims S054, no duplicate row id, no competing
  knowledge entry. Risk is **under-credit, not collision**: F20 should be scored as a frontier
  opening over already-present adjacent ground, and the kagi `ssvcV203` payload is an unabsorbed
  lead the L1 may cite in the lesson without adding it to the registry.

## 1. Sweep command (as specified)

```bash
cd /home/vgpnk/Projects/shokunin
for lane in */; do lane=${lane%/}
  [ "$lane" = kasegi-shokunin ] && continue
  hits=$(grep -rliE 'SSVC|Stakeholder-specific|Stakeholder-Specific|CERT/CC' \
           "$lane/corpus" "$lane/SKILL.md" "$lane/PROVINCE.md" 2>/dev/null | grep -v '/\.git/')
  [ -n "$hits" ] && { echo "HIT $lane"; printf '%s\n' "$hits" | sed 's|^|  FILE |'; } || echo "CLEAN $lane"
done
```

Output (20 lanes, verbatim):

```
CLEAN audio-shokunin
CLEAN chousa-shokunin
CLEAN game-dev-2d-shokunin
CLEAN game-dev-3d-shokunin
CLEAN kagi-shokunin
CLEAN kaidoku-shokunin
CLEAN kake-shokunin
CLEAN kama-shokunin
CLEAN kengaku-shokunin
CLEAN kotoba-shokunin
CLEAN kotodama-shokunin
CLEAN kumitate-shokunin
CLEAN lore-shokunin
CLEAN mado-shokunin
CLEAN mori-shokunin
CLEAN revenger-shokunin
CLEAN souji-shokunin
CLEAN tabi-shokunin
CLEAN tameshi-shokunin
CLEAN tsukuroi-shokunin
```

Surface note: `audio-shokunin` and `game-dev-2d-shokunin` have **no `SKILL.md`** (checked:
`test -f` false for both); their surface is `corpus/` + `PROVINCE.md`. All 20 have `corpus/`
and `PROVINCE.md`. The literal pattern also matches `JPCERT/CC`, so the negative is strict:
not even the Japanese namesake appears in a sibling corpus.

## 2. Whole-repo superset re-run (strict boundaries)

Same 20 lanes, whole repo (superset of the required surface), `.git`/`__pycache__` excluded,
with a strict boundary so `JPCERT/CC` is not a match:

```bash
PAT='ssvc|certcc\.github\.io|(^|[^A-Za-z])CERT/CC|stakeholder.?specific'
grep -rliE "$PAT" <lane> --exclude-dir=.git --exclude-dir=__pycache__
```

Per-lane counts: audio 0, chousa 0, game-dev-2d 0, game-dev-3d 0, **kagi 4**, **kaidoku 2**,
**kake 2**, kama 0, kengaku 0, **kotoba 1**, kotodama 0, kumitate 0, lore 0, mado 0, **mori 8**,
revenger 0, souji 0, tabi 0, **tameshi 2**, **tsukuroi 1**.

### Hits — genuine (kagi only)

| lane | path | context (line 1, all four files) |
|---|---|---|
| kagi | `.ufo/waves/round-28/retained-probes/SrcCve202010735/nvd-api.json` | `..."exploitabilityScore":2.5,"impactScore":3.6}],"ssvcV203":[{"source":"134c704f-9b21-4f2e-91b3-4a467353bcc0","ssvcData":{"timestamp":"2026-10-07T18:38:50.558859Z","id":"CVE-2020-10735","options":[{"exploitation":"none"},{"automatable":"no"},{"technicalImpact":"partial"}],"role":"CISA Coordinator","version":"2.0.3"}}]...` |
| kagi | `.../nvd-api-1.json` | same `ssvcV203` block; `timestamp` 2026-10-21T17:07:14.744 |
| kagi | `.../nvd-api-2.json` | same `ssvcV203` block; `timestamp` 2026-10-21T17:07:18.730 |
| kagi | `.../cap-nvd-api.json` | same `ssvcV203` block; `timestamp` 2026-10-21T17:09:21.654 |

### Hits — false positives (recorded, not ground)

| lane | path | why it matched |
|---|---|---|
| kaidoku | `.ufo/waves/round-20/w1/patches/WasmRefusalLeg-2.patch` | base64 blob substring `...KmcYSsVCS\`r^eAXT9...` |
| kaidoku | `.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch` | same base64 family |
| kake | `.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` | base64 `...lWZbhj1vlSSVcqCuC5C4...` |
| kake | `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` | same file, assimilated copy |
| kotoba | `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt` | codepoint blob `...qtrarlrmrqrsscshsmsostt3...` |
| mori | `.ufo/waves/round-49/w1/swarm-registry.json`, `Mo49ExecQuotesSvc.md`, `build-w1-spec.py`, `w1-spec.json`, `w1-dispatch.json`, `.ufo/waves/round-50/a2w1/Mo50bExecScratchInventory.md`, `.jj/working_copy/tree_state` | seat name `Mo49ExecQuotesSvc` → substring `ssvc` |
| tameshi | `.ufo/evidence/round-48/freshness/sources/S026.html`, `.ufo/waves/round-48/w1/sources/S026.html` | PNG `data:` base64 |
| tsukuroi | `.ufo/waves/round-36/w2/W2MutTool5/m5-pristine-probe.jsonl` | `/tmp`-path bearing base64/hash line |

No false positive carries SSVC semantics: none names CERT/CC, `certcc.github.io`, SSVC decision
points, or stakeholder categorization.

## 3. Coverage hardening (negative is a true negative)

- **Proof the big corpora were really read.** Generic-token counts in the largest corpora
  (`grep -rliE 'vulnerab|prioriti'`): audio 40 files, game-dev-2d 77, game-dev-3d 332,
  tabi 14. Text-file inventories: audio 16 813, game-dev-2d 2 662, game-dev-3d 538, tabi 2 329.
  The engine reached the text layers; zero SSVC hits is absence, not a scan artifact.
- **Symlink gap audited.** `find */corpus -type l` = **50** links. Zero resolve outside their
  own lane (`os.path.realpath` containment check, 0 outside-lane). Broken ones are intentional
  kaidoku RE fixtures (`link-to-hello`, `.../etc/shadow`, `.../etc/passwd`, `outside`).
  Follow-symlink passes over the two symlinked subtree roots
  (`audio-shokunin/corpus/live/r80-simplifier/artifacts`,
  `game-dev-2d-shokunin/corpus/live/r67-simplifier/del-measure/fixtures`) and file-level `grep`
  through all 50 links → **0 hits**.
- **Synonym sweep** (20 lanes, required surface): `CERT Coordination Center` 0 files,
  `Vultron` 0, `\bVINCE\b` 0 (the loose `VINCE` pattern's 1 107 files are all `PROVINCE.md` /
  `province` substrings — discarded), `vulnerability categoriz` 0, `decision point` 7 files
  (generic prose: kengaku design doc, kotodama glossary/verification notes — no SSVC content).
  `Carnegie Mellon` 7 files, all `kengaku-shokunin/corpus/evidence/round28-calibration/*/audit-*.stdout`
  geocoding benchmark intents ("…airports within 50 km of Carnegie Mellon University") — unrelated.
- **Lane HEADs pinned** (read-only `git rev-parse HEAD`): audio 7a2fcd4f, chousa 00f8c7f5,
  game-dev-2d 7753d49b, game-dev-3d 89dd182b, kagi 69b61db4, kaidoku a2f64e1d, kake 044048597,
  kama 0163fea2, kengaku 3077adbc, kotoba 65a5c7a6, kotodama f556d104, kumitate 8d557f85,
  lore 380ef3ab, mado ae996fcf, mori aa3af1ec, revenger 6da884c6, souji fef88f21,
  tabi b234a589, tameshi c6295cb0, tsukuroi 8b7c4132.

## 4. kagi (NVD/SSVC probe) — deep read

```bash
grep -rinE 'ssvc|certcc|stakeholder.?specific|CERT/CC' kagi-shokunin \
  --exclude-dir=.git --exclude-dir=__pycache__      # 4 files, all the retained probe
grep -rn 'certcc\.github\.io' kagi-shokunin --exclude-dir=.git   # exit 1, absent
```

- Exactly one provenance chain: kagi round-28 `SrcCve202010735` ("kagi round28 BUILD wave"),
  which probed `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2020-10735`
  (`corpus/lessons/round-28.md:151`). The seat's own note
  (`.ufo/waves/round-28/build/SrcCve202010735.md`) records NVD as tier **B**, the HTML detail
  page as a Cloudflare/Angular shell, and closes with the row **REJECTED** for registration
  (`corpus/lessons/round-28.md:43`, "NOT REGISTERED"). It never mentions SSVC.
- Probe digests (sha256): `d043111e…841a5` (nvd-api.json), `f897c85c…bf0e6` (nvd-api-1.json),
  `42bc257c…004bf9` (nvd-api-2.json), `b206e962…139bd` (cap-nvd-api.json).
- kagi registry today: 51 `| S0xx |` rows, 25 knowledge entries, none SSVC/scoring-related;
  `certcc.github.io` absent from the whole repo.

## 5. Adjacency inside kasegi (reported, not absorbed)

- `corpus/source-snapshots/round-24/manifest.json` → **S004 = `https://certcc.github.io/certcc_disclosure_policy/`**
  (the only `certcc.github.io` URL in the lane). Its captured page
  `S004.txt:9,21` names `SSVC` in the site nav ("CERT Guide to CVD / VINCE / SSVC / Vultron").
- `S001.txt:954,994` (FIRST CVSS v4.0 user guide) — "the decision point by the same name in the
  stakeholder specific vulnerability categorization (version 2)".
- `S003.txt:239,252` (CISA CVD program) — "support systems such as Stakeholder-Specific
  Vulnerability Categorization (SSVC) to help prioritize"; "CISA uses SSVC…".
- `S008.txt:174` (CISA VDP template) — "Stakeholder-Specific Vulnerability Categorization (SSVC)".
- CERT/CC itself is already knowledge-grounded as a coordinator (e.g.
  `corpus/knowledge/coordinated-disclosure-timelines.md:17,22,23,34,38` citing S004's 45-day policy).
- Observed state at sweep time (read-only, no judgement): `corpus/knowledge/*.md` = **48**,
  `SOURCES.md` rows = **53**, no `ssvc-stakeholder-specific-vulnerability-categorization.md`,
  no `S054` row; lane HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0`, `git status --porcelain`
  shows only untracked `.ufo/waves/round-37/…` artifacts.

## 6. shokuknow doctrine rows

```bash
cd /home/vgpnk/Projects/shokuknow
grep -rinE 'ssvc|certcc\.github\.io|(^|[^A-Za-z])CERT/CC|stakeholder.?specific' doctrine lanes *.md
grep -rn 'certcc\.github\.io' . --exclude-dir=.git            # exit 1, absent everywhere
```

- **`certcc.github.io`: zero occurrences in all of shokuknow** (including `.deepresearch`,
  `.ufo` caches).
- **`SSVC` in `doctrine/`: zero.** `doctrine/*.md` has no SSVC row at all.
- CERT/CC name collisions only, both distinct bodies — do not let these read as ground:
  - `doctrine/channel-index-chinese.md:664` — "CERT/CC 漏洞公告 (section 9)",
    `https://www.cert.org.cn/publish/main/9/…` → **China's CNCERT/CC**, not Carnegie Mellon.
  - `doctrine/verified-numbers.md:1261`, `doctrine/channel-index-japanese.md:22,114-115,153,168,189,452,505-506`
    → **JPCERT/CC** (Japan), plus `github.com/JPCERTCC/rust-binary-analysis-research-ja`.
- Extra adjacency layer found while sweeping `lanes/` (not doctrine, report-only): kasegi's own
  earlier-round mirrors already quote SSVC — `lanes/kasegi/round7/evidence/zxd_wd.txt:2733`
  ("CISA Stakeholder-Specific Vulnerability Categorization Guide 2022"),
  `lanes/kasegi/round7/evidence/zxd_di.txt:216,231` ("《利益相关者特定漏洞分类 (SSVC)》"),
  repeated in round8 (`zxd_wd.txt`, `zxd_di.txt`, `zxd_di8.txt`), round15 and round16
  (`di2026.txt:216,231`). The topic surfaced before round 37 as evidence and was never
  registered — consistent with "frontier opening", not "new discovery".
- shokuknow false positives discarding: `lanes/tabi/round10/.work/chromium-strings.txt`
  (`UseDnsHttpsSvcb…`, `Net.DNS.HTTPSSVC` = DNS SVCB/HTTPS records), `lanes/kake/round1x`
  `auraConfig` base64, `lanes/revenger`, `lanes/tameshi`, `lanes/audio` binary/PDF bytes.

## 7. Ruling

1. **Uncontested.** Zero sibling-lane claims on SSVC / CERT/CC / `certcc.github.io`; no id
   collision (no S054 anywhere, kagi holds S001-S051), no duplicate knowledge entry.
2. **Nearest-neighbour ground, in order:** kagi `SrcCve202010735` `ssvcV203` payload (CISA SSVC
   v2.0.3 data actually captured, unabsorbed) → kasegi round-24 S004 (`certcc.github.io` host
   already bound) → kasegi S001/S003/S008 (SSVC named verbatim) → shokuknow
   `lanes/kasegi/round7-16` evidence (SSVC quoted in Chinese-language captures).
3. **Consequence for C2 scoring (stated, not enacted):** S054's url is same-host-different-page;
   the knowledge entry is genuinely new ground in the registry but its host and concept are
   already present. F20 should be described as opening on adjacent ground, and the kagi
   `ssvcV203` capture is the natural "not absorbed" note for the round-37 lesson. No absorption
   performed here.

## Tooling

No installs, no upgrades (nothing needed; `grep`, `find`, `sha256sum`, `python3` only).
Scratch `/fast/scratch/hyaku/kasegi-r37/ExecSiblingSweep/` removed after this receipt was written.
