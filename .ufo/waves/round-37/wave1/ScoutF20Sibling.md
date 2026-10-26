# ScoutF20Sibling — F20 (SSVC) sibling-overlap reconnaissance, round 37

Seat: ScoutF20Sibling (leaf scout, read-only; no lane/fleet/shokuknow/sibling write; no tool installs).
Lane head observed: b362068 (claims-erratum-1; S054 primary URL = https://certcc.github.io/SSVC/tutorials/ssvc_overview/).

## Ruling

**F20 / S054 is UNCONTESTED.** None of the 20 sibling lanes (kasegi excluded) holds SSVC ground: no sibling corpus,
SKILL.md, PROVINCE.md, or any other tracked file names SSVC / Stakeholder-Specific Vulnerability Categorization, and
`certcc.github.io` appears in no sibling. shokuknow doctrine has no SSVC/CERT-CC (CMU) row for any lane. Every
non-empty hit is either **unrelated** (substring/base64 noise, or "Carnegie Mellon" as a place/institution) or
**adjacent, unabsorbed** (one kagi NVD payload). Nothing to route, no row-id or knowledge collision.

Host-level note (kasegi itself, not a sibling): CERT/CC ground already exists in kasegi at host/page level — S004
`https://certcc.github.io/certcc_disclosure_policy/` (round 24, tier A, CVD disclosure schedule) and SSVC named
verbatim in kasegi's round-24 captures S003 (L239 "Stakeholder-Specific Vulnerability Categorization (SSVC)", L252
"CISA uses SSVC") and S004/S008. So S054 novelty is page/concept-level (decision-point model, distinct from CVSS/KEV/EPSS),
not host-level. Kasegi's existing knowledge has `cvss-v4-severity-and-vector.md` (adjacent severity entry) but no SSVC entry
at HEAD (`ls corpus/knowledge | grep -i ssvc` -> empty).

## Sweep commands (run verbatim)

20 sibling lanes = `ls -d *-shokunin | grep -v '^kasegi-shokunin$'` under /home/vgpnk/Projects/shokunin
(audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kengaku kotoba kotodama kumitate lore mado mori revenger
souji tabi tameshi tsukuroi). Heads at sweep time saved in scratch (e.g. kagi 69b61db, kengaku 3077adb, kotodama f556d10).

A. Assigned surface (corpus + SKILL.md + PROVINCE), with the spec terms:
```
cd /home/vgpnk/Projects/shokunin
for d in $(ls -d *-shokunin | grep -v '^kasegi-shokunin$'); do ( cd $d
  grep -rIniE "SSVC|Stakeholder-specific|CERT/CC|Carnegie Mellon" corpus SKILL.md PROVINCE.md PROVINCE 2>/dev/null | sed "s|^|$d: |" ); done
```
-> 721 lines. SSVC=0, Stakeholder-specific=0, CERT/CC=0, Carnegie Mellon=721 (720 kengaku, 1 kotodama).

B. Whole-repo, word-bound, incl. dot-dirs (superset), `-w`:
```
grep -rIlwiE "SSVC|Stakeholder[- ]Specific Vulnerab|certcc\.github\.io|CERT/CC|CERT Coordination" . --exclude-dir=.git
```
-> 1 file: kaidoku-shokunin/.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch (base64 blob).

C. Whole-repo, no `-w` (catches `ssvcV203`), non-boundary `CERT/CC`:
```
grep -rIlE -i 'ssvc|stakeholder.?specific|certcc\.github\.io|(^|[^A-Za-z])CERT/CC' . --exclude-dir=.git --exclude-dir=node_modules
```
-> 19 files in 7 repos (below). Also zh/ja: `grep -rIl "利益相关者特定漏洞分类\|ステークホルダー特定"` over all 21 lanes -> only kasegi.

## Hit list and classification

| Lane | Path | What matched | Class |
|---|---|---|---|
| kengaku | corpus/evidence/round28-calibration/{build,complete,final}-acceptance/audit-{current,without-c2}.stdout (6 files, 720 lines) | "Carnegie Mellon University" as a place name in WebArena map-task intents (Pittsburgh) | unrelated |
| kotodama | corpus/SOURCES.md:737 (S783) | Hunt Institute for Botanical Documentation (Carnegie Mellon University) — rosemary perfume source | unrelated |
| kagi | .ufo/waves/round-28/retained-probes/SrcCve202010735/{nvd-api,nvd-api-1,nvd-api-2,cap-nvd-api}.json | NVD 2.0 API capture for CVE-2020-10735: `vulnerabilities[0].cve.metrics.ssvcV203[0].ssvcData` = CISA Coordinator, version 2.0.3, timestamp 2026-10-07T18:38:50.558859Z, options exploitation=none / automatable=no / technicalImpact=partial (verified by parsing all 4 files) | **adjacent** (unabsorbed): SSVC data as an NVD metric field in a CVE probe, never a registry row or knowledge entry; kagi's round-28 note rejected registering the CVE (kagi corpus/lessons/round-28.md:43,151 name only NVD). Not held ground. |
| kaidoku | .ufo/waves/round-20/w1/patches/Wasm{Compare,Refusal}Leg-2.patch | `ssVc`/`SSvC` inside base64 | unrelated (noise) |
| kake | .ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py (+ round-48 validate copy) | `lSSVc` in base64 | unrelated (noise) |
| kotoba | .ufo/round-44/evidence/omp-live-18.12.2-strings.txt | `...ussvcsvd...` in a strings dump | unrelated (noise) |
| mori | .ufo/waves/round-49/w1/{Mo49ExecQuotesSvc.md,swarm-registry.json,w1-spec.json,w1-dispatch.json,build-w1-spec.py,Mo49ExecScratchHygiene.md}, round-50/a2w1/Mo50bExecScratchInventory.md | seat name `...QuotesSvc` | unrelated (substring) |
| tameshi | .ufo/evidence/round-48/freshness/sources/S026.html, .ufo/waves/round-48/w1/sources/S026.html | `ssvC` in base64 | unrelated (noise) |
| tsukuroi | .ufo/waves/round-36/w2/W2MutTool5/m5-pristine-probe.jsonl | `xcubisssvc` fuzzed env value | unrelated (noise) |

No sibling hit is **held ground** (no sibling registry row, knowledge entry, SKILL gate, or PROVINCE line owns SSVC / CERT/CC CMU).
The wider adjacent-vocabulary scan (`CVSS|EPSS|KEV|exploit prediction|vulnerability prioriti|NVD|known exploited|CVD|vulnerability disclosure` over corpus/SKILL/PROVINCE/CORPUS.md) returned: kagi (NVD fetch note, round-28 lesson), kake S078 (RFC 9116 security.txt), mori (CVSS in a GitHub advisory page capture), mado/tabi/tameshi (incidental strings), game-dev-2d (479 hits = `epss` substring inside Godot fixtures, noise). Those are
CVD/disclosure-format adjacency only — none are prioritization-framework ground. Severity-vocabulary ground is kasegi's own
(`cvss-v4-severity-and-vector.md`, `japanese-severity-vocabulary-and-impact-model.md`).

## shokuknow doctrine (read-only, host = kasegi)

- `grep -rIlw SSVC` over the whole /home/vgpnk/Projects/shokuknow (excl. .git) -> 7 files, **all** in kasegi's own lane material:
  lanes/kasegi/round{7,8,15,16}/evidence/{zxd_wd,zxd_di,zxd_di8,di2026}.txt and 2 `.ufo/waves/corpus-expansion-1/.qcache/*.txt`
  (verified the same text). Context (di2026.txt:213-232): a Chinese national standard draft's compilation note says it was drafted
  with reference to CWE, CAPEC, CVSS 4.0 and 《利益相关者特定漏洞分类 (SSVC) 指南》 — a passing mention of the standard, no CERT/CC
  or certcc.github.io source, no row. The same text is already in kasegi as `.ufo/waves/round-29/wave1/assimilation/fetch/S070.txt`
  (L205, L218). So SSVC's only shokuknow footprint is host-owned and incidental.
- doctrine/*.md (12 files): zero SSVC/EPSS/`certcc.github.io`/`Stakeholder-Specific Vulnerability`; no KEV hit.
  "CERT/CC" appears only as **CNCERT/CC** (channel-index-chinese.md:406,664; cert.org.cn, CNVD) and **JPCERT/CC** (channel-index-japanese.md:115,
  JVN) — different organisations from CERT/CC at CMU. Doctrine rows naming kasegi (anchor-craft, anti-patterns, channel-index-chinese)
  cover Chinese/Japanese security sources and AP-19 re-typesetting, not CVD prioritization.
- (Two shokuknow whole-tree sweeps timed out at 300s on huge lane trees; the SSVC/certcc scans were completed on a narrowed `-l` pass and returned the counts above. EPSS/KEV were re-checked: 0 whole-word EPSS hits, 0 KEV hits.)

## Relation to sibling seat ExecSiblingSweep

ExecSiblingSweep's receipt agrees on the verdict (uncontested; kagi `ssvcV203` payload unabsorbed; kasegi S004/S003 host precedent).
Differences from this seat: this seat also swept `Carnegie Mellon` (surfaces kengaku/kotodama place-name noise that `CERT/CC` alone cannot),
classified every residual substring hit of the non-`-w` sweep, and traced the shokuknow SSVC hits to a Chinese-standard compilation note (host-owned, already S070 in kasegi).

## Caveats

- Sweep C's non-word-bound `ssvc` pattern is intentionally noisy; `-w` would have missed kagi's `ssvcV203` key, the only real payload. Use C, then classify.
- Heads are the live working trees at sweep time (not pinned export refs); the sweep is a point-in-time read.
- Unresolved: whether the L1 wants to cite kagi's `ssvcV203` capture in the round-37 lesson (information only; no sibling write required).
