VERDICT: BROKEN

# R45CritCalibration — self-assessment vs observed state (freeze 8cf62c8)

Scope: read-only critic. Freeze tree = `git archive 8cf62c879e6e6b031e67412f8fac1fba0bd378cf`; pure base = `git archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`; round-43 box tree = `git archive 4cb6d4a`. All runs were on scratch exports; no commit, index or git mutation. Nothing was built (F27 and C1 repairs belong to the executor/scribe seats).

## Table — assertion | observed | match? | command

| assertion path:line | observed | match? | command |
|---|---|---|---|
| `claims.json` sha256 vs `freeze.txt:2` `claims-sha256: bbe40503…` | `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206` both | MATCH | `git show 8cf62c8:.ufo/waves/round-45/claims.json \| sha256sum` |
| `claims.json` C1 `before` (0 of 5 routed items; items 1-5 of lesson §6) | lesson §6 has items 1-6; item 6 self-reported; base counter `total=5 fixed=0 unresolved=5 exit=1` | MATCH | `python3 freeze/corpus/instruments/r45-routed-defects.py --root base --baseline base` |
| `claims.json` C1 `expect_before` | base run printed `routed-defects total=5 fixed=0 unresolved=5 exit=1` | MATCH | same as above |
| `claims.json` C2 `before` 26 frontier / 63 knowledge / 70 SOURCES / no kernel grep hit | README table-aware `rows=26 admitted=26`; `ls corpus/knowledge/*.md \| wc -l` = 63; SOURCES 70; kernel grep → no output, rc=1 | MATCH | `grep -rliE 'security-bugs\|linux kernel\|kernel\.org' base/corpus/knowledge base/corpus/SOURCES.md base/corpus/README.md; echo rc=$?` |
| `claims.json` C2 `expect_before` `c2-gate fixed=1/7 exit=1` | base run `c2-gate fixed=1/7 exit=1` | MATCH | `python3 freeze/corpus/instruments/r45-c2-gate.py --root base` |
| C2 basis: freeze tree is a do-nothing control? (`freeze-controls.txt` do-nothing = base) | freeze tree grades `c2-gate fixed=2/7 exit=1` (G4 passes: `recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`) | NO (basis unstated) | `python3 freeze/corpus/instruments/r45-c2-gate.py --root freeze` |
| `SCORECARD.md:1705` depth:verifiability gate: red on do-nothing export AND marker-only mutants | do-nothing-base reproduced (C1 0/5 exit 1); `c1-marker-only` line in `freeze-controls.txt` has no committed tree and no path | PARTIAL (marker control unreproducible) | `cat .ufo/waves/round-45/controls/freeze-controls.txt` |
| `SCORECARD.md:1706` coverage gate: table-correct counter + committed-export basis + nonauthor admit/reject spot-check BEFORE claiming movement | G1 table-aware (`rows=26 admitted=26`); committed basis yes; `claims.json` has no pre-score spot-check gate (only post-landing kill clause "non-author closure re-opening S071 does not locate the cited quotes") | PARTIAL (spot-check gate absent from claims) | `git show 8cf62c8:.ufo/waves/round-45/claims.json \| grep -ioE '.{60}non-?author.{60}'` |
| `claims.json` C1 R1 remedy vs `round-44-verifier-spotcheck.md:79` item 1 ("Append (never rewrite) a correction to `corpus/SOURCES.md` S070") | counter R1 forbids any S070 change: `if old is None or old != new: return False, "S070-row-changed-or-baseline-absent"`; claims chose supersession by S072 (not the routed remedy) | PARTIAL (literal remedy rejected by counter; deviation not flagged) | `sed -n 99,140p freeze/corpus/instruments/r45-routed-defects.py` |
| `claims.json` C1 R4 artifact `corpus/instruments/freeze-check.py` vs lesson item 4 ("Freeze hygiene … hold the lane to it") | item 4 names no artifact; counter R4 requires a new instrument | PARTIAL (mapping expanded beyond routed text) | `awk '/^## *6/{p=1} /^## *7/{p=0} p' base/corpus/lessons/round-44-verifier-spotcheck.md` |
| `claims.json` C2 `after`: "five located manifest quotes … each located in snapshot lines" | counter G5 accepts a span of any width: whole-file span `S071.txt:1-372` → `(True, 'spans=4 located=4 failed=0 cores=4/4')`; exact spans → same True; span `1-1` → False | NO (cited line numbers not enforced; quote presence only) | scratch fixture, `m.g5(root)` on `r45-c2-gate.py` (T1-T4 below) |
| C1 controls (`freeze-controls.txt`): c1-marker-only `fixed=0` | adversarial 4-line `freeze-check.py` stub that prints `selftest cases=6 failures=0` and `freeze-check claims=2 base_ok=2` flips R4 to fixed → `routed-defects total=5 fixed=1 unresolved=4 exit=1` | NO (marker-only tree can grade a limb green; control not reproducible) | `python3 freeze/corpus/instruments/r45-routed-defects.py --root fx/c1 --baseline base` |
| `freeze-controls.txt` C2 controls: junk-row 4/7, fabricated-quote 5/7 | trees not committed; not reproducible from committed bytes | UNVERIFIED | `cat .ufo/waves/round-45/controls/freeze-controls.txt` |
| `SOURCES.md` registry rows vs `claims.json` "70 SOURCES rows" | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `70`; every row NF=13 (11 cells); status `56 mined` + `14 rejected` = 70; no duplicate ids | MATCH | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' freeze/corpus/SOURCES.md` |
| `SOURCES.md` prose registry counts vs rows | last explicit count `Registry 55 rows pre-append → 59 post-append (R8)` at `SOURCES.md:147`; round-44 68→70 stated in SCORECARD and `round-44.md`, not in SOURCES prose; no prose count of 70 | NO (prose count stale/absent; no contradiction in prose itself) | `grep -nE 'post-append\|→ 70\|Registry 6[0-9]\|Registry 7[0-9]' freeze/corpus/SOURCES.md` |
| `corpus/README.md` frontier rows vs `PROVINCE.md` frontier lines | README `F01…F26` (26 rows, table-aware admitted 26); PROVINCE names F01–F10 (`:38`, `:57` ranges), F11 (`:41`), F12–F15 (`:60–63`), F16–F26 amendment lines (`:74–167`) | MATCH (ID set) | `grep -oE '^\| F[0-9]{2} ' freeze/corpus/README.md; grep -oE '\bF[0-9]{2}\b' freeze/PROVINCE.md \| sort -u` |
| README prose count `26/26 admitted` vs rows | `corpus/README.md:630` `26/26 admitted` | MATCH | `grep -noE '[0-9]+/[0-9]+ admitted' freeze/corpus/README.md \| tail -2` |
| PROVINCE count prose (current) | last count prose is historical `20/20 admitted` at `PROVINCE.md:118/131/147` (round-37 labelled) | MATCH-as-history; STALE if read as current | `grep -noE '[0-9]+/[0-9]+ admitted' freeze/PROVINCE.md` |
| Frozen C2 grep string `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` | `0` (status is 3rd cell); r45 counter does not use it (uses table-aware G1) | known defect, not used by r45 | `grep -cE '^\| F[0-9]+ \| admitted \|' freeze/corpus/README.md` |
| SHONEN box count: 4 boxes x 10 evidence blocks = 40, all `[~]` | `40` `- [~]` lines, `0` `[x]` | MATCH | `grep -c '^- \[~\]' SHONEN.md; grep -c '\[x\]' SHONEN.md` |
| `SHONEN.md:3-5` "Current pointers: the round-35 paragraphs … are the boxes' current evidence" | evidence blocks continue to `SHONEN.md:225` (Round 41), `:232` (Round 42), round-43 block at `:285–291`; r36–r40 blocks at `:162–210` | NO (header stale) | `git show 8cf62c8:SHONEN.md \| sed -n '3,5p'; grep -nE '^## ' SHONEN.md` |
| `SHONEN.md:9-233` round-42 box: `SKILL.md 1129 lines, sha256 f8e7a5d3…` | `git show 0566bd66:SKILL.md` → 1129 lines, sha `f8e7a5d3be746993` | MATCH | `git show 0566bd66:SKILL.md \| wc -l; git show 0566bd66:SKILL.md \| sha256sum` |
| `SHONEN.md:285-291` round-43 box 1: `SKILL.md` byte-unchanged `ab98fac9→4cb6d4a`, 1134 lines, sha `9eef84d1…` | `git diff --numstat ab98fac9 4cb6d4a -- SKILL.md` empty; 1134 lines; sha `9eef84d163173c8e` | MATCH | `git diff --numstat ab98fac9 4cb6d4a -- SKILL.md; git show 4cb6d4a:SKILL.md \| wc -l` |
| round-43 box 1 density `234.2 over 30 blocks / 782 cites` | at `4cb6d4a`: `Total path-citation instances: 782 across 30 blocks.`, mean `234.2` | MATCH (at 4cb6d4a) | `python3 freeze/corpus/instruments/density.py SKILL.md` in full export of 4cb6d4a |
| round-43 box 1 anchorcheck `16 in-range, 0 bad, LOST-RECORDED=306` | at `4cb6d4a` and at freeze: `SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` | MATCH | `python3 corpus/instruments/anchorcheck.py SKILL.md` (full tree export) |
| SKILL.md at freeze vs round-43 box figures | freeze `SKILL.md`: 1144 lines, sha `bb742f7e…`, density `237.4` over `31` blocks / `793` cites (r44 appended, numstat `10 0`) | NO (box describes pre-r44 bytes; no round-44/45 box update) | `git diff --numstat 4cb6d4a 8cf62c8 -- SKILL.md; python3 corpus/instruments/density.py SKILL.md` on freeze |
| round-43 box 4: `PROVINCE.md` 165 lines, sha `8deea5ea…`, byte-unchanged base→freeze | at `4cb6d4a`: 165 lines, sha `8deea5ea1c584573`; at freeze: 167 lines, sha `a3c64764999405a4`; numstat `2 0 PROVINCE.md` (F26 amendment `PROVINCE.md:165–167`) | NO (stale) | `git show 4cb6d4a:PROVINCE.md \| wc -l; git show 8cf62c8:PROVINCE.md \| wc -l` |
| SHONEN: any round-44 evidence for boxes 1-4 (F26 admitted, r44 SKILL append, PROVINCE 167) | no `Round 44` evidence block; `grep -niE 'round 44\|F26' SHONEN.md` hits only `:222`, `:294–302` (corrections) | NO | `grep -niE 'round 44\|round-44\|F26' SHONEN.md` |
| LOG.md round headings | `## Round 44 (attempt 1/2/3)` at `LOG.md:1965/1977/1994`; no SHONEN box refers to them | informational | `grep -n '^## Round 4[0-5]' LOG.md` |
| SCORECARD round-44 disposition (`:1693-1700`, "C1 unverified") vs `Round-44 final measurement` ("measured") | both in freeze SCORECARD; the later correction paragraph supersedes the disposition | MATCH with correction only | `git show 8cf62c8:SCORECARD.md \| sed -n '1693,1700p;1723,1730p' \| cut -c1-200` |
| Lane working tree vs freeze | `git status --short` shows untracked `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` (R5 path); absent at freeze (R5 `refiled-absent`) | NOTE — counts must use committed export | `git status --short` |
| counter external dependency `CENSUS` | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet root, outside lane); G7 and r45 limb use it; `census-rc=0` | NOTE (external, unpinned) | `grep -n CENSUS freeze/corpus/instruments/r45-c2-gate.py` |

## Findings

### F1 — C2 quote check does not bound the cited span (G5)
Attacked: `corpus/instruments/r45-c2-gate.py` G5 (`window = norm(" ".join(snap[max(a-1,0):b]))`, no width bound). Fixture: freeze copy + README F27 row + knowledge file with four frozen-core quotes; quotes located by exact search at spans 309-311, 94-96, 38-40, 40-42.
- T1 exact spans → `(True, 'spans=4 located=4 failed=0 cores=4/4')`
- T2 whole-file span `1-372` for all four → `(True, 'spans=4 located=4 failed=0 cores=4/4')`
- T3 span `1-1` → `(False, 'spans=4 located=0 failed=4 cores=0/4')`
- T4 one fabricated quote "The Linux kernel pays a bounty of one million dollars" with span `1-372` → `(False, 'spans=4 located=3 failed=1 cores=3/4')`
Discrimination: the counter rejects fabricated text and out-of-range spans (T3/T4) but accepts any true substring at any line citation (T2). The claim "located in snapshot lines" is therefore grading presence in the file, not the cited location. Counter-side fix, not a lane-data fix.

### F2 — C1 limb R4 grades printed tokens, not behaviour
Attacked: `r45-routed-defects.py` `limb_r4` (requires `selftest cases>=6 failures=0` and the string `freeze-check claims=2 base_ok=2`). Fixture: base copy + stub `corpus/instruments/freeze-check.py` that prints those two strings.
Output: `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2`; `routed-defects total=5 fixed=1 unresolved=4 exit=1`.
So the frozen control "c1-marker-only → fixed=0" is only as strong as its unpublished content; a marker that prints the tokens grades a limb green. Predicate sentence unchanged, so this is a counter-hardening item (replay outputs must be behaviour-checked, e.g. run freeze-check on a mutated claims file), not a kill-rule breach by itself.

### F3 — Self-assessment pointers are stale
SHONEN header (`:3-5`) points at round-35 paragraphs; boxes carry round-41/42/43 evidence and no round-44/45 evidence. Box 1 figures (1134 lines, `9eef84d1…`, 234.2/30/782) reproduce exactly at `4cb6d4a` but the freeze SKILL.md is 1144 lines / `bb742f7e…` / 237.4 / 31 / 793. Box 4 (165 lines / `8deea5ea…`) is stale against 167 lines / `a3c64764…` after the F26 amendment. The round-43 box itself discloses "pre-append bytes" for box 1, so the miss is the absence of any later box update, not concealment.

### F4 — Gate text vs frozen claims
SCORECARD `:1706` requires a nonauthor admit/reject spot-check before any coverage movement; `claims.json` C2 has no such pre-score gate. SCORECARD `:1705` requires a marker-only red control; the marker tree is not committed. Both are gate-text vs claim-text mismatches to be resolved by the L1 before scoring.

### F5 — Routed-defect remedy vs counter predicate (R1, R4)
Lesson §6 item 1 asks for an appended correction to the S070 row; counter R1 forbids any S070 change and requires S072 supersession. Lesson item 4 ("freeze hygiene", no artifact named) is mapped to a new instrument `freeze-check.py`. Both mappings are reasonable but undisclosed as deviations in `claims.json`.

### F6 — Confirmed matches
Base counts reproduce (C1 0/5 exit 1; C2 1/7 exit 1; README 26/26; SOURCES 70 = 56 mined + 14 rejected; knowledge 63; kernel grep empty; claims sha; round-42 and round-43 SKILL/PROVINCE figures at their own commits; anchorcheck 16/0/306 at 4cb6d4a and freeze).

## Limitations
- Did not build F27, C1 repairs, S072, or any draft; critic seat is read-only. Counters were run only on exports and scratch fixtures.
- Fixtures T1–T4 and the R4 stub are adversarial constructions, not seat output; they show predicate gaps, not seat behaviour.
- Control trees `c1-marker-only`, `c2-junk-row`, `c2-fabricated-quote` are not committed; their freeze-controls numbers are recorded as UNVERIFIED.
- `density.py` / `anchorcheck.py` were run from the committed exports with the freeze-tree script versions; the 4cb6d4a density figure used the freeze `density.py`, not the r43-era copy (none committed separately).
- Counters depend on a fleet-root census script outside the lane; not audited.
- No non-author check, no network access, no LOG.md semantic audit beyond heading counts.
- Installed nothing; no tool or version changes.
