# Round 85 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r85. Base `bc722e540c93b48ff159454b65a0f9f4630db1ed`, freeze `4a2d34f203519a87078f21a896dc8679137ff675`, C1 landing `c0507adf685058cefc749c0e07e9b72e100b17a4`, C2 landing `a48fe8b9ee34cf4b38106ce0b2357bbff489cb1d`, lane HEAD `6013dc983867a90cf6f2cc486ac872315d8f4aba`. Report `.ufo/reports/round-85/kasegi.md` (fleet repo, commit `df3e8467549d94b164b1d8b2ffbeec37d2d3b455`). Every measurement below reads committed bytes at `6013dc98` (`git show 6013dc98:<path>`), not the worktree.

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T21:17:17-03:00 launch kasegi round=85 pgid=4060595 driver=hyaku-inline attempt=1
2026-11-06T21:51:08-03:00 complete kasegi round=85; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-85/kasegi.md` | `kasegi-shokunin kasegi@shokunin.local df3e8467…` (21:50:30-03:00, before the 21:51:08 completion line) | pass |
| `## SHONEN` heading, one line per box | read report §SHONEN | 4 lines `[~]`, matching SHONEN.md's 4 boxes; no `[x]` | pass |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for bc722e54, 4a2d34f2, c0507adf, a48fe8b9, 170cadf4, 6013dc98, c91c944f | all `anc` | pass |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain` | `branch=master local=remote=6013dc98… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Remote tip | `git ls-remote origin refs/heads/master` | `6013dc983867a90cf6f2cc486ac872315d8f4aba` | pass |
| Prompt carries template contract | `.ufo/prompts/kasegi-round-85.md` (931 lines; committed `46beb18d` 21:17:15) | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract incl. SHONEN, §5 commit scope, §6 hyaku addendum, §7 scratch | pass |
| Round commits by lane identity | `git log --format='%an <%ae>' bc722e54..6013dc98` | 5 commits, all `kasegi-shokunin <kasegi@shokunin.local>` | pass |

Observation (not a defect): the freeze `4a2d34f2` carries author date 21:16:16-03:00, one minute before the launch line; its committer date is 21:30:31. This is the jj working-copy change's creation time, not evidence produced before dispatch: the captures inside it say `observed_at 2026-11-07T00:26:30Z` (21:26 local).

## 2. Claims — re-check

### C1 — depth:verifiability (resolve.py SKILL meter 158/741 → 167/732)

Re-measured myself (Python over `git show bc722e54:SKILL.md` and `git show 6013dc98:SKILL.md`; the lane's skill-meter/resolve.py were not executed):

- Repair map `git show 6013dc98:.ufo/waves/round-85/c1/repair-map.json | sha256sum` → `b575f147…1944`, equal to `claims.json` instruments. 18 keys; every target path is tracked at `6013dc98` (18/18); no key is tracked as a root-level file (`[]`); each key has exactly one tracked non-`.ufo/` basename match (18 × 1).
- SKILL.md line count 1252 → 1252; 17 lines changed (claim P3: 17 lines).
- Byte delta of the whole file = 478, equal to the sum of the inserted path prefixes (23 occurrence repoints × (len(target) − len(key))). The diff is pure prefix insertion; nothing else changed.
- Distinct backtick-quoted tokens base → after: 18 removed, exactly the 18 map keys; 9 added, all full paths that exist in the tree (`capture-source.py`, `claim-package-check.py`, `entry29-fixed-bytes.md`, `score-gap.py`, `shonen-form.py`, `target-checkouts.md`, `S040-live.txt`, `S073.txt`, `S074.txt` under their corpus dirs); the other 9 targets were already cited.
- Arithmetic: 741 − 18 + 9 = 732 citations; 158 + 9 = 167 resolving. This reproduces the claimed 167/732 independently of resolve.py.

Evidence-verified (lane gate, not executed): `l1/L1-landing-r85.txt` at the landing commit `a48fe8b9` prints `SKILL-METER base=158/741 after=167/732 target=167/732`, LIMB M1–M5 pass, `SKILL-METER-RESULT pass rc=0`; P2 all six instrument sha256 OK; P4 density `273.2` → `273.2`. `controls/c1-controls-r85.txt` shows do-nothing 158/741, pad 168/751, de-cite 158/723, wrong-target 168/733 and partial 164/738 all rc 1, and the positive control 167/732 rc 0. `l1/census-of-record-c1-r85.txt`: SKILL 167/732, lane 1755/6941.

Qualifier carried (CriticClaims A1, also in SCORECARD): all gain is internal citations; external RESOLVES stay 4/741; the score holds at 4. Wording note: the report says "18 bare citations". These are 18 distinct citation tokens, spread over 23 occurrences. 16 bare non-backtick occurrences of the keys remain in SKILL.md, mostly in registry-table name cells, which the meter does not count.

**Verdict C1: verified; depth:verifiability `improved`** (measured meter move, reproduced).

### C2 — coverage (capability acquisition: end-to-end priced claim package)

Re-measured myself over committed bytes:

- Package `corpus/practice/curl-h1-1913733/` has 6 top-level entries (claim_checklist.md, custodian-receipts.json, provenance.json, report.md, status.json, evidence/), and `evidence/` holds S119–S121 plus manifest.json.
- Snapshot digests `sha256sum` of `corpus/source-snapshots/round-85/S119|S120|S121.txt` → `9e4fb52e…6105`, `65d6b230…3690`, `9e346a4e…f102`, equal to claims.json and report.md.
- Subject binding (the counter's known gap, CriticClaims B3, checked by hand): S119 contains `"id":1913733` and `"title":"CVE-2023-28319: UAF in SSH sha256 fingerprint check"`; S120 contains `Original report: https://hackerone.com/reports/1913733` once. The package is about the right report.
- Pricing fields, each `grep -c -F` = 1 in its snapshot: S119 `"has_bounty?":false`, `"severity_rating":"medium"`, `"asset_identifier":"https://github.com/curl/curl"`, `"disclosed_at":"2023-05-24T08:25:54.715Z"` (CVE id ×2); S120 `Bug bounty: 2400 USD`, `Severity: Medium`, `CWE-416: Use After Free`, `Affected versions: curl 7.81.0 to and including 8.0.1`; S121 `There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.`, `We do not support CVSS`. S120 also carries `186` bytes (:77), the introduced/fixed commits (:87, :90) and the credits (:99–100) that report.md states.
- KEV: `git show 6013dc98:corpus/source-snapshots/round-35/S052.txt | grep -c CVE-2023-28319` → 0; catalogVersion `2026.10.23`; that file is unchanged in this round's diff. `price-kev: not-listed catalogVersion 2026.10.23` holds.
- Registry rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`: bc722e54 118, 4a2d34f2 121, a48fe8b9 121, 6013dc98 121. `git diff bc722e54 6013dc98 -- corpus/SOURCES.md`: +3 rows S119–S121 (`mined`, used-by the package report) plus 3 registry-changes lines; no deletion.
- LOG.md `## Round 85` (line 2927) logs the task with trigger, action, outcome and pointer. SHONEN box 2 `[ ]` → `[~]` with evidence `corpus/practice/curl-h1-1913733/report.md — …`.
- Reviewer CHANGES-REQUESTED (`w1/ReviewC2Package.md` F-1..F-7), with "re-review not recorded" (status.json). I re-read every fix at `6013dc98`:
  - F-1: a real scan exists, `l1/redaction-scan-r85.txt` `artifacts=3 bad=0`.
  - F-2: "paid" appears only in "No captured record shows who paid it".
  - F-3: the grant `kasegi-PROVINCE.md:52-documentation-only` is labelled a producer attestation, and PROVINCE.md:52 reads "this corpus is documentation only".
  - F-4: resolved models are recorded in provenance.json.
  - F-5: the KEV capture date 2026-10-26 / r35 is in the report.
  - F-6: the scope is quoted as raw JSON.
  - F-7: the label is now "severity agreement check".

  All seven are fixed, and this closure stands as the missing re-review.

Evidence-verified (lane gates, not executed): `L1-landing-r85.txt` C2 P1 `LIMB E1–E5 pass`, `E2E-RESULT pass limbs=5 rc=0`; P2 `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`; P3 S119/S120/S121 `sha256 OK` rc 0; P4 registry=121; P5 census rc 0; R136 `shonen-form canonical=1 finding=SF-CLEAN exit=0`. `controls/c2-controls-r85.txt`: absent package, the r43 exemplar and the eight pricing forgeries each rc 1; positive rc 0. Known counter limits stay routed by the lane (M85-2: wrong-subject pass B3, E4 empty quotes / E3 duplicate keys R-01/R-02, MutC2Counter 13 survivors, MutC1Counter 16 survivors).

**Verdict C2: verified; coverage `improved`** (capability `priced-claim-package` enters with a checked package; the coverage score holds at 8).

### Harm check

- `git diff bc722e54 6013dc98 -- SCORECARD.md`: additions only (one capability row and `## Round 85`); no earlier score edited.
- The SKILL.md diff is pure prefix insertion (above).
- density 273.2 → 273.2 (receipt, evidence-verified).
- SHONEN.md: box 1's pointer was reformatted to canonical form (`:94` moved into the explanation). The box state is unchanged at `[~]`; box 2 went `[ ]` → `[~]`. No `[x]`.
- QUALITY.md: +R136 only.

No owned axis harmed.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | re-measured: 18 GONE tokens out, 9 new resolving paths in → 158/741 → 167/732 |
| coverage | improved | re-measured: package facts all located in committed captures, subject bound by hand, S119–S121 mined, capability row |
| depth:density | unchanged | evidence-verified receipt 273.2 → 273.2 |

## 4. Discernment spot-check (`corpus/lessons/round-85.md` § Gate)

Re-opened live on 2026-11-07 (UTC) with curl:

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S120 curl advisory CVE-2023-28319 | admit | https://curl.se/docs/CVE-2023-28319.html, HTTP 200 | agree | the live page carries `Severity: Medium` and `Bug bounty: 2400 USD`, as captured at S120.txt:80–81; it is vendor-authored, so tier A holds |
| S119 HackerOne JSON record 1913733 | admit | https://hackerone.com/reports/1913733.json, HTTP 200 | agree | the live record returns `"severity_rating":"medium"`, `"has_bounty?":false` and `"cve_ids":["CVE-2023-28319"]`, matching the capture; it is the platform's own record |
| Third-party CVSS (NVD/MITRE) as package evidence | reject | https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2023-28319, HTTP 200 | agree | NVD publishes `baseScore 7.5 / HIGH`, which contradicts the vendor's Medium; S121 (live) says "We do not support CVSS … we do not set them for CVE records"; pricing on that score would use a ladder the program refuses |
| daniel.haxx.se end-of-bounty post | defer | https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/, HTTP 200 | agree | it is reachable, but no claim this round rests on it (CORPUS rule 4); the flip condition is stated |

SOURCES.md row re-opened: **S121** (`corpus/SOURCES.md:133`). Anchor "policy page, snapshot lines 43, 95 and 99-110". `S121.txt:43` = "There is no bug bounty and the curl project never offers rewards for reported vulnerabilities." (15 words, ≤25). It is found verbatim on the live page (`grep -oF` hit). `:95` is the CVSS refusal and `:103` the Medium rung, as the lesson cites.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok …/corpus/SOURCES.md`, rc 0, with six inherited W04 duplicate-url warnings (S028, S029, S072, S076, S080, S085), the same set as `l1/census-end-r85.txt`.

## 5. Trend verdicts

- **expansion: improved.** Three new tier-A sources were mined (registry 118 → 121), and the first end-to-end task opened a new kind of lane output (`corpus/practice/`). A capability was admitted to SCORECARD (`priced-claim-package`), and its every priced fact is located in a committed capture (§2 C2).
- **quality: improved.** 9 more SKILL.md citations resolve (reproduced), the broken SHONEN gate form was fixed with R136, and its frozen receipt shows `SF-POINTER` at c91c944f/bc722e54 and `SF-CLEAN` at landing. No admitted entry failed its re-check here.
- **discernment: improved.** The spot-check agrees on 2 admits, 1 reject and 1 defer. The reviewer's CHANGES-REQUESTED was integrated (all 7 fixes confirmed above), not overridden. R136 adds a grounded QUALITY criterion citing lesson M85-1.

## 6. Routed defects (lane fixes next round)

1. **e2e counter does not bind subject** (CriticClaims B3) and accepts empty quotes / first-of-duplicate keys (R-01, R-02); MutC2Counter 13 survivors, MutC1Counter 16 survivors. The lane already routes these as M85-2. The r86 counter amendment must ship a wrong-subject control that fails.
2. **Re-review after CHANGES-REQUESTED not recorded.** `status.json` says "re-review not recorded". This closure re-read F-1..F-7. Next package: record a reviewer re-pass, or have the status say the closure is the re-review.
3. **Citation-count wording.** "18 bare citations" means 18 distinct tokens over 23 occurrences. 16 bare non-backtick occurrences of the same basenames remain in SKILL.md. Say "distinct" in future meter claims. The ExecC1Hunt tranche should decide whether the table-name cells stay bare.
4. **Census of record stale.** `corpus/instruments/citation-survival.md` still reads 132/701 (r57-era); the lane routed its regeneration to r86.

## 7. Operator notes

- SHONEN box 2 is now `[~]` on a retrospective practice package: public records only, no submission, not claimable. Whether a documentation-only retrospective package satisfies "end-to-end domain task" under PROTOCOL §Evidence standard ("executed against the domain's actual surfaces … prepared + verified + handed off") is the operator's promotion call. The package itself checks out from outside (§2 C2).
- Boxes 1, 3 and 4 remain checkable from outside as recorded at round 47. Promotion is operator-owned; nothing is promoted here.
