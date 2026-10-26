# ScoutSiblingFinal — round-40 falsify wave 2, final sibling-overlap sweep

Seat: ScoutSiblingFinal. Attacks: the claim that the eight round-40 landed knowledge entries (and the S060 row / F23) do not
bleed into, or duplicate, any other lane's domain. Method: lexical sweep of the 20 sibling lane repos plus fleet-root files,
read-only. Lane HEAD at sweep: `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (= J; the receipt `final-gates/all-gates.txt` is
still untracked, so the lane tip Y did not yet exist as a commit; the eight entries were read from the working tree == J, tree
clean except `.ufo/waves/round-40/final-gates/` and the two `kasegi-r40-falsify.ready*` markers).
Sweep ran 2026-10-26 ~22:05-22:15Z. Scratch `/fast/scratch/hyaku/kasegi-r40/ScoutSiblingFinal/` removed before yield.

## Landed entries swept for (J, `git diff --name-status a7af2ce..HEAD -- corpus`)
S016 anthropic-cvd-provenance-and-pacing · S017 pz-reporting-transparency-trial · S019 nist-sp800-216-vdp-framework ·
S020 doj-vdp-framework-scope-and-authorization · S021 cisa-bod-20-01-vdp-minimums · S023 cisa-cvd-program-stages ·
S025 cve-bench-agent-exploitation-benchmark · S060 cyclonedx-analysis-subtree. (S061 VEX Status Justifications and S062 CSAF v2.1
are registry rows only; no entry or snapshot landed for them, so no entry text exists to overlap — the sweep still covers the topic.)

## Scope searched
`/home/vgpnk/Projects/shokunin/{audio,chousa,game-dev-2d,game-dev-3d,kagi,kaidoku,kake,kama,kengaku,kotoba,kotodama,kumitate,lore,mado,mori,revenger,souji,tabi,tameshi,tsukuroi}-shokunin`
(all 20; whole lane trees incl. `corpus/`, `.ufo/`, tools, reports; excluding `.git`, `node_modules`, venvs; files <=20 MB; ripgrep,
case-insensitive, `--no-ignore --hidden`), plus fleet-root `*.md`, `MANIFEST.json`, `research/`, `scripts/`, `templates/`, `ok/`,
`shokunin.conf`, `m-rev-vs-rev.py`. Read-only extra: `/home/vgpnk/Projects/shokuknow` (grep only, no tools run).
Note on method: my in-command `-g '!kasegi-shokunin/**'` exclusion did NOT take (kasegi self-hits appeared: 446/420/947/165/735/149/287 lines),
so kasegi paths were removed by post-filter (`grep -v /kasegi-shokunin/`). Counts below are post-filter.

Patterns (rg -i -n -e), run in parallel per topic (`run.sh`, 4.8 s wall):
- T1 CycloneDX: `cyclonedx|cyclone dx|vulnerabilities\[\]\.analysis|bom-link`
- T2 CVE-Bench / AI-agent exploitation: `cve-bench|cvebench|2503\.17332|agent..exploit..(vulnerab|cve)|(exploit|exploitation)..(by|with) (ai|llm) agents?|zero-day..one-day|one-day..zero-day`
- T3 federal VDP guidance: `bod[ -]?20-01|sp[ -]?800-216|800-216|ccips|framework for a vulnerability disclosure program|cna[ -]of[ -]last[ -]resort|vince-nt|cisa..(cvd program|coordinated vulnerability disclosure program)|federal..(vdp|vulnerability disclosure (policy|program|guideline))`
- T4 Anthropic CVD: `anthropic..(coordinated|cvd|vulnerability disclosure|responsible disclosure)|anthropic\.com/coordinated`
- T5 Project Zero transparency: `reporting transparency|upstream patch gap|projectzero\.google/2025|project zero..(transparen|trial|90\+30|90-day|disclosure polic)`
- T6 CSAF v2.1 / os/: `csaf[ -]?(v|version )?2\.1|csaf-v2\.1|csaf/v2\.1|csaf/os|os/ directory|product_status..(nine|9)`
- T7 VEX Status Justifications: `vex_status_justification|vex status justification|status justification|vulnerable_code_not_in_execute_path|vulnerable_code_not_present|component_not_present|inline_mitigations_already_exist|vulnerable_code_cannot_be_controlled_by_adversary`
- Second, deliberately broad pass (`run2.sh`, per-file counts): `\bsbom\b|\bvex\b|\bcsaf\b|purl|spdx`; `cybench|cybergym|bountybench|xbow|agent..(exploit|cve)`; `\bvdp\b|\bcvd\b|coordinated disclosure|vulnerability disclosure|responsible disclosure|safe harbor|\bcisa\b|\bnist\b|\bdoj\b|\bcfaa\b`; `project zero|projectzero|tim willis|anthropic\.com|claude..(vulnerab|disclos)`.

## Sweep result — hits outside kasegi, per sibling lane (corpus c / .ufo u / other o), topics T1..T7
Lanes with ALL zeros across T1-T7 (corpus, .ufo and other): audio, chousa, game-dev-2d, game-dev-3d, kagi, kama, kotoba, kotodama,
kumitate, lore, mado, mori, revenger, tameshi. Fleet root: only `MANIFEST.json:26204,26209` (T6, kasegi's own round-38 record).
`T4` (Anthropic CVD) and `T5` (Project Zero transparency): 0 hits in every sibling lane, the fleet root and shokuknow.
`T2` core-term hits: only the kengaku item below.

| lane | T1 | T2 | T3 | T6 | T7 | classification |
|---|---|---|---|---|---|---|
| kaidoku | 19c/1u | – | 0c/1u | – | – | FALSE POSITIVE: T1 = `cyclonedx-bom` crate name inside round-30 binary-evidence JSON envelopes (`corpus/evidence/round-30/{c1,c2}/envelopes/*.json`) and a Ghidra ChangeHistory SBOM line; T3 = binary patch noise (`CCIPS` in a base64-like patch string) |
| kake | – | – | 2c/22u | – | – | REAL-ADJACENT (topic T3, see O1) |
| kengaku | – | 2u | – | – | – | REAL-ADJACENT in `.ufo` only (O2); no corpus hit |
| souji | – | – | – | – | 1u | FALSE POSITIVE ("status justification" in a source-register sentence) ; plus broad-pass `lanes/souji/round9/...gitlab-deprecations.md` CycloneDX SBOM mentions in shokuknow (O4) |
| tabi | – | – | – | – | 7u | REAL but historic, `.ufo` only (O3) |
| tsukuroi | 3u | – | – | – | – | FALSE POSITIVE: `cargo-cyclonedx 0.5.9-1` in round-24 pacman package lists |

Broad pass B1-B4 (corpus/ + root only, kasegi excluded): the large corpus counts are all non-security noise — `game-dev-3d/corpus/live` (216) and
`audio/corpus/live` (65) are scraped pages; `kaidoku`/`mori`/`tabi`/`kengaku/corpus/evidence` are byte captures (`purl`/`vex`/`nist`/`doj`
substrings, FTX news URL, HHS vuln-disclosure link in a captured page); `kagi`/`revenger`/`mori`/`kotodama` corpus hits are NIST SP 800-57 / FIPS 180-4 /
SP 800-122 / SP 800-92 / CFTT citations (different NIST documents; none is SP 800-216); `kumitate`/`kotoba` corpus hits are anthropic.com agent-design
pages (`engineering/multi-agent-research-system`, `research/building-effective-agents`, agent-skills) — none is `anthropic.com/coordinated-vulnerability-disclosure`;
`kotoba` `VDP disclosure` strings are kotoba's routing table citing kasegi's own `vdp-disclosure-packages.md`. No `cybench|cybergym|bountybench|xbow` hit in
any sibling corpus knowledge entry about exploit-agent benchmarks (kotodama/souji hits are unrelated text).

## Overlapping claims recorded (owning lane + path)
- **O1 — kake, CISA BOD 20-01 (T3), topic-adjacent, not duplicate, not a contradiction.**
  `kake-shokunin/corpus/lessons/round-35.md:58` and `kake-shokunin/corpus/SOURCES.md:255` record a *rejected candidate*: "the CISA BOD 20-01
  template" (`.ufo/waves/round-35/w1/ScoutSecurityTxtCandidates.md:12,38`, row C3, HTTP 200, reject), rejected because it "names neither security.txt nor
  `.well-known`" and quoting "Your policy must be published as a public web page in plain text or HTML at the “/vulnerability-disclosure-policy” path".
  That is kake's security.txt-publishing scope (RFC 9116, S078/S079); kake holds no BOD 20-01 row, no entry, no capture.
  Kasegi's `knowledge/cisa-bod-20-01-vdp-minimums.md` (S021) is the BOD page itself (different URL from kake's template page) and carries the same
  path text at `corpus/source-snapshots/round-40/S021.txt:118` ("Publish a vulnerability disclosure policy as a public web page in plain text or HTML at the
  “/vulnerability-disclosure-policy” path of the agency’s primary .gov website."; entry FC-4 counts the path 6x). Same fact, consistent, different lane purpose.
  Also `kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` mentions securitytxt.org's `CSAF` field extension (S079) — a security.txt field, not CSAF v2.1 `os/`, no overlap with kasegi's CSAF material.
  Ruling: no bleed; kake's rejection reason does not apply to kasegi's use. Neither entry cross-references the other (not required).
- **O2 — kengaku, CVE-Bench via ABC (T2), `.ufo` only, benchmark-method axis.**
  `kengaku-shokunin/.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md:498,500` quote ABC (kengaku S091, arXiv 2507.02825): "When applied to
  CVE-Bench … ABC reduces the performance overestimation by 33%". Live re-open (2026-10-26T22:10:03Z, HTTP 200, 45,559 bytes, sha256
  `98f75e67134f5a642f8d29006e9217dcf371d5df9b58fdd5a15398f3c43bb53a`) confirms the abstract sentence verbatim. Kengaku's *corpus* (`corpus/SOURCES.md:104`,
  `corpus/knowledge/benchmark-task-validity-checklist.md:103-111`) names ABC but never CVE-Bench. Kasegi's `cve-bench-agent-exploitation-benchmark.md` is the security-capability
  arm (40 CVEs, 8 attack goals, success rates) and declares `Self-reported, first-party … no independent replication is in the capture` (L130) — true of its capture;
  it does not mention that a third-party instrument (ABC) reports CVE-Bench overestimation. This is a cross-reference gap, NOT bleed and NOT a false claim (ABC is a checklist
  application, not a replication of the 13% figure). Kasegi's PROVINCE lists kengaku as the adjacent lane for "LLM evaluation and benchmarks"; the entry stays on the exploitation-measurement side
  (grounded in F04) and does no benchmark-validity analysis. Ruling: no bleed; optional follow-up = one pointer sentence in the entry's Honest limit to kengaku S091.
- **O3 — tabi `.ufo` snapshot of kasegi's prior VEX entries (T7), historic.**
  `tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/kasegi.diff:18,22,70,72,107,125,140` is tabi's round-34 *copy of kasegi's own round-34 diff* (S055/S057 VEX
  profile + not-affected label enumeration). It is the owning lane's own text, mirrored in a sibling workdir; not a tabi claim. It predates and does not concern the round-40
  rows (S061 VEX Status Justifications is registry-only this round).
- **O4 — shokuknow (read-only upstream), stale NIST SP 800-216 status.**
  `shokuknow/lanes/kasegi/CHANNELS.md:15`, `lanes/kasegi/round16/DOMAIN.md:18`, `lanes/kasegi/round16/KNOWLEDGE-PROPOSED.md:203`,
  `merge/kasegi/knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md:45`, `.ufo/scopes/corpus-expansion-16/ScoutKasegi.md:96` all describe SP 800-216 as "queued"/unmined.
  Kasegi mined it this round (`knowledge/nist-sp800-216-vdp-framework.md`, S019). Not a sibling lane, not an error in either lane (the shokuknow text is a round-16 snapshot); recorded only so a later
  merge screen does not re-adopt an old "queued" claim. `shokuknow/lanes/souji/round9/evidence/gitlab-deprecations.md` mentions GitLab's CycloneDX *SBOM report* properties (component inventory),
  unrelated to the `vulnerabilities[].analysis` subtree.
- No other overlap: no sibling carries CycloneDX `analysis`, CVE-Bench as an entry, Anthropic CVD, Project Zero Reporting Transparency, CISA CVD program, DOJ CCIPS framework, SP 800-216, CSAF v2.1 `os/`, or the VEX Status Justifications document.
- Outward direction: `git show 3074c76:corpus/knowledge/<each of the 8>.md | rg` for any sibling-lane name, `../<lane>/`, `shokuknow`, `sibling` → 0 matches in all eight. No landed entry cites or
  absorbs another lane's corpus.

## Ruling
**No cross-domain bleed in the landed entries; no duplicate or conflicting claim in any sibling lane or fleet-root file.** Real adjacent items: O1 (kake, rejected BOD template candidate, consistent
wording), O2 (kengaku `.ufo` ABC↔CVE-Bench, benchmark-method axis; optional pointer), O3 (tabi mirror of kasegi's own text), O4 (shokuknow stale "queued"). Everything else was false-positive
noise (cyclonedx crate names in binary envelopes, pacman package lists, GitLab SBOM properties). Defects found: **0 blocking**; 1 optional improvement (O2). Frozen-claim impact: none (C1/C2 predicates do not depend on sibling absence).

Attack ledger (item / command / result):
1. Claim "no sibling-lane bleed in landed entries" / T1-T7 ripgrep over 20 lanes + fleet root (`run.sh`) / **reproduced as clean** after classification (4 real-adjacent items, 0 conflicts).
2. Broad second pass B1-B4 / `run2.sh` per-file counts / **no further real hits** beyond false positives.
3. Outward cross-references from 8 entries / `git show 3074c76:… | rg` lane names / **0**.
4. kake quote vs kasegi S021 / `rg 'public web page' S021.txt` / **consistent (L118)**.
5. kengaku ABC quote / live fetch arXiv 2507.02825 / **quote reproduced** (HTTP 200, 45,559 B, sha256 above).
6. Method defect in my own run: rg glob exclusion of kasegi failed; handled by post-filter (disclosed above).
