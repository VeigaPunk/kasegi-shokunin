author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# kasegi round 51 — non-author verifier spot-check (closure)

Closed at 2026-11-01T03:56Z UTC against lane tip `acbdd202b7490a0c4892e78d140952b99db45ee5` (branch `master`,
pushed), base `bcd5d89a65ab612ef88e3d49cea0ef3cb3ccca09`. All commands below were run by the closure judge
(fresh session, non-author); every count was re-measured over committed bytes (`git show` / `ls-tree` /
`diff-tree` / `git grep <rev>`, index-free per the host note). Lane-owned instruments were NOT executed; their
committed receipts were verified instead.

## 1. Step-1 conformance

| Check | Result | Command / evidence |
|---|---|---|
| Report committed in fleet repo by lane identity | PASS | `git log --format='%an %ae %H' -1 -- .ufo/reports/round-51/kasegi.md` → `kasegi-shokunin kasegi@shokunin.local c881934099c41200ef076d58670567a62229c9e5` |
| `SHONEN` heading in report | PASS | `## SHONEN` present; one line per box: `[~]`, `[ ]`, `[~]`, `[~]` — no `[x]` written by the lane (correct: non-author required) |
| Cited lane commits exist and are ancestors of master | PASS | `git cat-file -t` + `merge-base --is-ancestor` for `73555db`, `aca3c29`, `85e1ea5`, `c5743f8`, `acbdd202` (all commit + ancestor); referenced `021989b`, `c5e3636`, `bcd5d89` also resolve |
| Lane tip pushed | PASS | `git ls-remote origin refs/heads/master` = `acbdd202b749…` = local `refs/heads/master` = `HEAD` |
| Round work inside bcd5d89..acbdd202 | PASS | `git log --oneline bcd5d89..acbdd20` → exactly the round's 5 commits (73555db freeze → acbdd20 final regen); `git diff-tree -r --stat` = 24 files, 1206+/146−, matching the report |
| Dispatch/complete digest consistency | PASS | launch 2026-10-31T19:21:40-07:00 (02:21:40Z) → commits 02:59:16Z–03:27:40Z → complete 20:34:19-07:00 (03:34:19Z); S081 fetch stamp 2026-11-01T02:48:34Z is inside the window and before the freeze commit 73555db (02:59:16Z) — no future-dated evidence |
| LOG.md entry covers the landed changes | PASS | `LOG.md:2205` `## Round 51 — …` covers C1/C2/C3, registry, mistakes, non-targets, wave disposition |

Conformance defects: none blocking. Two figure-level defects found in re-derivation (§5, routed next round).

## 2. Per-claim re-derivation

### C1 — depth:verifiability (the r50-closure D1 fix) — RE-MEASURED: verifies, `improved` (score honestly held 4)

- Controls census (index-free): `git ls-tree -r --name-only <rev> | grep do-nothing-c1` → base `bcd5d89`: 1 file
  (`.ufo/waves/round-50/controls/do-nothing-c1.txt`); tip `acbdd20`: 2 files (+ `.ufo/waves/round-51/controls/do-nothing-c1-winhost.txt`). Matches reported before→after 1 → 2.
- The imported receipt is genuinely old-host-shaped: `git show bcd5d89:.ufo/waves/round-50/controls/do-nothing-c1.txt | grep -c '[/]fast'` → 2; `grep -c 'python3: can'` → 1 (Unix CPython form, `/fast/...` target). This host has no working `python3` and no `/fast` (probe receipt `controls/probe-host-r51.txt`: Store stub exit 49; `ls /fast` exit 2; `python /fast/...` prints the Git-mount backslash form) — so the round-50 "produced on this host" label and the "Windows CPython error string" claim were both wrong, exactly as erratum-1 states.
- The new control of record is host-shaped: `do-nothing-c1-winhost.txt` ends `C1_EXIT=2`, names this host's `C:\Users\jpvei\AppData\Local\Programs\Python\Python313\python.exe`, carries a backslash-quoted target, and embeds reproduce commands; `grep -c "python3: can"` on it → 0. First landed at freeze `73555db`, byte-identical through tip (`git diff 73555db..acbdd20 -- <file>` empty).
- Semantics re-checked: `git ls-tree c5e3636 -- corpus/instruments/census-freshness-check.py` → 0 entries — the instrument is genuinely absent at that base, so the do-nothing exit-2 control is sound.
- The old file is retained byte-identical (`git diff bcd5d89..acbdd20 -- .ufo/waves/round-50/controls/do-nothing-c1.txt` empty); erratum-1 names all four mislabeling locations (round-50 report, `claims.v2.json` do_nothing_control, claims-erratum-1 §"What survives unchanged", lesson round-50 M3) and stays append-only.

### C2 — calibration (the r50-closure D2 fix; verdict row, not a number) — RE-MEASURED: verifies, `improved`

- `git show <rev>:<f> | grep -c 4809` → base `bcd5d89`: round-50.md 0 / LOG.md 0 / SCORECARD.md 0; tip: **2 / 3 / 5** — matches the report exactly.
- Append-only held: the two filed 4807 lines (SCORECARD:1948, round-50.md:92) are byte-identical base→tip; every other 4807 match at tip is new correction text quoting the superseded figure. SCORECARD/PROVINCE/LOG have 0 removed lines in the range; SKILL.md diff is empty.
- 4809 figure provenance re-derived from committed bytes: `git show 021989b:corpus/instruments/citation-survival.md` reads **204 files / 4809 distinct** (GONE 3738, INTERNAL 1063, RESOLVES 8, total 10298; 8+1063+3738=4809 ✓); the erratum's own counter `git show 021989b:corpus/instruments/citation-survival.md | grep -c 4809` → 4, reproducing the lesson's claim.
- This round's final census of record re-derived at tip: `citation-survival.md` reads **206 files / 4868 distinct** (RESOLVES 11, INTERNAL 1075, GONE 3782, total occurrences 10388; lane 1086/4868 = 22.31%). Internal consistency re-checked: 11+1075+3782=4868 ✓; 11+1075=1086 ✓. File-scope delta re-measured: exactly 2 new corpus `.md` files in the range (`cisa-vulnrichment-adp-enrichment.md`, `lessons/round-51.md`) → 204+2=206 ✓. The distinct-citation totals themselves rest on the lane's `resolve.py` regeneration — verified via committed evidence only.
- Gate receipts (evidence-verified, gate not executed): `controls/c1-gate-final-r51.txt` = `CENSUS-FRESH=ok files=2`, `C1_GATE_EXIT=0`, marked REV 3 over the truly final tree (SCORECARD 2044 lines / LOG 2260 lines at measurement); `controls/c1-gate-selftest-r51.txt` = 3 cases, `want==got` on all, `selftest cases=3 failures=0`, `C1_SELFTEST_EXIT=0`. The two self-catches (receipts-cited-before-they-existed → stale; SCORECARD line-count change → stale) are recorded in the SCORECARD census paragraph, not smoothed over.
- DEFECT (minor, status-neutral, next round): the SCORECARD round-51 move-log row records the 4809-row counts as "**2/3/2**" while the same commit measures **2/3/5** under the report's own counting command (`grep -c 4809 SCORECARD.md`); the calibration verdict row in the same file records 2/3/5 correctly. Self-count drift — the D2 class, on the round that fixed D2. Append-only correction owed.

### C3 — coverage (frontier F32 on S081) — RE-MEASURED: verifies, `improved` (score honestly held 8)

- Registry rows re-measured: `git show <rev>:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,} \|'` → base 80, tip **82** ✓. S081/S082 rows absent at base, present at tip; the range diff removes no table row → no pre-existing row's status/recheck/used-by cell changed (R8 held).
- Capture re-measured from committed bytes: `corpus/source-snapshots/round-51/S081.txt` = 8290 bytes (`git cat-file -s`), 120 lines (`wc -l`), sha256 `2da0941448d88f48bfc7275c6444abf3aaf57244719e64b3b3ab6591f4458b65` — all three match the row/manifest/entry. Manifest re-measured: `"Q1"…"Q12"` each exactly once.
- Recheck receipt (evidence-verified): `controls/s081-recheck.txt` = `S081:sha256 OK` + 12 `Q<n> OK occurrences=1 anchor=<n>-ok` lines, `S081_RECHECK_EXIT=0`.
- Counter receipts (evidence-verified, instrument not executed): before (`do-nothing-c2-r51-winhost.txt`, base export of bcd5d89 built per-file) `FRONTIER-CENSUS rows=31 admitted=31 closed=1 problem-rows=30 registry=80`, `entries=34 pass=1`, zero F32 lines, `C3_DONOTHING_EXIT=1`; after (`c2-counter-final-r51.txt`) `rows=32 admitted=32 closed=2 problem-rows=30 registry=82`, `entries=35 pass=2`, `PASS F32 ids=S081 exit=0`, and 33 FAIL entry lines each ending `problems=recheck-exit-1` (counted). Matches the frozen `expect_after` exactly; the do-nothing control cannot reach the after-state without the round's work.
- F32 entry `corpus/knowledge/cisa-vulnrichment-adp-enrichment.md` exists with the provenance trio (`source: S081 …`, `verified-at: 2026-11-01`, `recheck:` re-runnable), `ground: F32`, and §Distinctness naming F18/F20/F22/F25/F30 with the screen's commands and zero-hit results quoted.
- Neighbor screen re-run by me at base over the quoted scope: `git grep -ric vulnrichment bcd5d89 -- corpus/knowledge corpus/README.md PROVINCE.md corpus/SOURCES.md SKILL.md` → zero hits (exit 1). The screen-before-freeze ordering is supported by the freeze's own claims.json naming the screen's results and by commit timestamps.
- Observation (non-blocking): one byte OUTSIDE the screen's quoted scope also names the surface at base — `corpus/source-snapshots/round-24/S013.txt:65` ("CISA Vulnrichment" listed as a data source in the MITRE CWE Top 25 2025 methodology capture; S013 is mined by F05 `cwe-top25-2025-methodology.md`). F05 consumes the surface's output for exploitability evidence; it does not hold the enrichment-program ground F32 admits. A fuller screen would have named F05 as a downstream-consumer neighbor in §Distinctness. Recorded for next round; the admission's distinctness from F18/F20/F22/F25/F30 is real and verified.

## 3. Axis-harm check

`git diff-tree -r bcd5d89 acbdd20 -- SCORECARD.md` (61 insertions, 0 deletions): the round-51 section holds depth:verifiability **4→4**, coverage **8→8**, depth:density **9→9** (SKILL.md diff empty — guard verified on bytes), calibration as a verdict-only row. PROVINCE (+12/0) and LOG (+57/0) append-only. No owned axis harmed; no score asserted beyond holds.

## 4. Discernment spot-check (non-author, this closure)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S081 / F32 CISA Vulnrichment README (admit, tier A, mined) | admit | live `https://raw.githubusercontent.com/cisagov/vulnrichment/develop/README.md` | **agree** | The located quote is verbatim at the top of the live README; all seven asserted program facts confirmed live: SSVC decision points on every assessed CVE; CWE and/or CVSS only for some higher-risk CVEs; CNA precedence with ADP dropping its own assessments; KEV block for KEV-listed CVEs; SSVC `major.minor.patch` version field (2.0.3); CPE enrichment stopped December 10, 2024. Scope limit honest (not the CVE format / SSVC framework / KEV catalog / CVE Services). |
| S082 VeigaPunk/open-bug-bounties (reject, tier C, on-release) | reject | live `https://github.com/VeigaPunk/open-bug-bounties` + committed `controls/mirror-probe.txt` | **agree** | Live repo is a same-named but different object: default branch `main`, GitHub Pages board description, root inventory 15 entries (`.github`, `.omp`, `app`, `data`, `public`, `scripts`, `tests` + 8 files) with no `submission-review/` and no `.ufo-missions/`; committed receipt shows `gh api …/commits/1307b8b` → 422 "No commit found for SHA" and `git ls-remote` HEAD `4c895519…`. The negative identity answer is probed, not wished; the rejection keeps RECEIPT-STORE-LOST corpus-attested-only. Taste done right. |
| New SOURCES row located quote (S081) | quote check | `corpus/source-snapshots/round-51/S081.txt:2` | agree (location exact; count annotation wrong) | Quote is verbatim at S081.txt:2. Measured `wc -w` on the quoted string = **17 words** ≤ 25 — conformant — but the lesson annotates it "24 words by wc -w". Minor figure defect (§5). |
| Census validate | gate run | `sources-census.sh validate --root <fleet root> kasegi` | pass | Exit 0; exactly the 5 known W04 duplicate-url warnings (S028, S029, S072, S076, S080), no new warning from S081/S082 — matches the report. The validator resolves `kasegi-shokunin` under the fleet root through a symlink to this lane repo, so it read the lane's real corpus (82 rows). |

Spot-check sample: 1 admit + 1 reject, both re-opened, both agree. Discernment stands: `improved`.

## 5. Routed defects for round 52 (all status-neutral; none bars admission)

1. **SCORECARD r51 move-log self-count drift.** The move-log row records 4809-row counts "2/3/2"; the same commit measures 2/3/5 under the report's own command (`grep -c 4809 SCORECARD.md` → 5). The calibration row in the same file says 2/3/5 correctly. Append-only correction next round (the D2 class, self-inflicted).
2. **Lesson Gate quote word-count annotation.** "24 words by wc -w" for the S081 quote; measured 17. The ≤25-word bound holds either way; correct the figure append-only.
3. **Neighbor-screen scope observation.** The quoted screen scope (knowledge/README/PROVINCE/SOURCES/SKILL) was truthful, but `corpus/source-snapshots/round-24/S013.txt:65` (mined by F05) names CISA Vulnrichment as a data source. If a fuller screen is wanted, name F05 as a downstream-consumer neighbor in §Distinctness.
4. **Carried operator-owned debt (unchanged, disclosed).** 67 host-bound recheck lines + 22 gated lines; L0 kasegi round-50 unanswered and routed around. Not lane-fixable.

## 6. Trend verdicts (with evidence)

- **expansion: improved.** Frontier 31 → 32 admitted, re-derived from committed receipts plus my own byte re-measures (rows 80 → 82; F32 entry + S081 mined row landed; PROVINCE F32 amendment + honest negative S082 annotation). New surface, first-party-captured, screen-before-freeze.
- **quality: improved.** Both closure-routed defects repaired and re-derived (C1: host-produced control of record + provenance erratum; C2: append-only 4809 correction with filed lines byte-identical), and the fresh-regeneration rule was then enforced on the round's own bytes — the gate caught the round twice and the catches are recorded where the figures live (rev-3 receipt of record). No admitted entry failed a re-check.
- **discernment: improved.** The mirror was refused on a two-probe negative and kept as a rejected row with a concrete flip; both gate decisions survive my outside re-opening (agree/agree); scores honestly held (4 / 8 / 9) with the calibration verdict a row, not a number.

## 7. SHONEN note for the operator

No `[x]` written by the lane (correct). Box 1 (`[~]` SKILL.md decision tables/error patterns/checklists/cited sources) looks checkable by a non-author reviewer on the stable, instrument-verified SKILL.md bytes; box 2 (end-to-end domain task) remains genuinely open (the considerthese proposal is noted, not adopted). No promotion action from this closure.

## Verdict

All three declared claims verify (C1, C2, C3 re-measured from committed bytes; lane-owned gate/instrument outputs verified via committed receipts). No axis harmed. Round admitted.

`CLOSURE kasegi r51 status=ok admitted=true`
