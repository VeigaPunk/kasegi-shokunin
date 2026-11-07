# CriticClaims — kasegi round 85 (attempt 1, wave 1)

Seat: critic (attack only). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze `4a2d34f203519a87078f21a896dc8679137ff675`, base `bc722e540c93b48ff159454b65a0f9f4630db1ed`.
Receipts: `.ufo/waves/round-85/w1/CriticClaims-receipts/`. No lane, instrument, frozen control or claim was edited.

## 0. State I measured (not the report's prose)

| Fact | Command | Observed |
|---|---|---|
| C1 landed | `git log --oneline -2 -- SKILL.md` | `c0507ad round-85: land C1 …`; `git diff --numstat bc722e5 HEAD -- SKILL.md` = `17 17` |
| C1 P1 | frozen counting command from `claims.json` (see receipts `c1-counter-at-head.txt`) | `base=158/741 after=167/732 target=167/732`, M1–M5 pass, `rc=0` |
| C1 P2 | `sha256sum` of the six frozen instruments | all six equal `claims.json` `instruments` |
| C1 P4 | `density.py` on `bc722e5:SKILL.md` and on the map-applied file | mean dens `273.2 → 273.2`; path-cite instances `932 → 932` |
| C1 harm | `anchorcheck.py SKILL.md`, `r-defect-closure.sh`, `figure-audit.py` | rc 0, `closed=9/9 exit=0`, `figures=35 ok=35 stale=0 exit=0` |
| C2 not landed | `ls corpus/practice` | absent at review time; C2 is judged as a counter + predicate set, not as an artifact |
| C2 sources | `source-recheck.py --manifest … --source S119|S120|S121` | each rc 0, every quote `occurrences=1`, `sha256 OK`; `SOURCES.md` S119–S121 rows `queued`; registry `121` rows |
| Host | `resolve.MIRROR_ABSENT` | `True` (both mirror roots absent); CI marker `mirror_absent=True` on every run |

## 1. C1 — `depth:verifiability`, 18-entry repair map

### A1 — Is "depth:verifiability" the honest label, or citation surgery that inflates the meter?

Composition of the scored meter at base (`receipts/c1-composition.txt`):

```
BASE verdicts {'GONE': 583, 'INTERNAL': 154, 'RESOLVES': 4} total 741      nonGONE 158
```

**The numerator is 154 INTERNAL + 4 RESOLVES.** 97.5 % of the "resolved citations" are the lane's own files; external (`RESOLVES`) citations are `4/741 = 0.54 %`. The repair removes 18 GONE tokens and adds 9 already/now-resolving **INTERNAL** tokens (denominator 741→732, numerator 158→167).

Verdict on the *number*: **SURVIVES** — it is the lane's own meter, measured by the lane's own instrument, and the claim says explicitly that "the integer score is not claimed to move".
Verdict on the *axis reading*: **BREAKS** if any SCORECARD/report line presents `22.81 %` as verifiability of the skill's claims. It is a self-citation rate; the claim's own wording ("the scored meter itself") is honest, the axis name is not. The lane has already recorded the rule twice for this axis: `SCORECARD.md:172` "Do not replace primary sources with circular corpus citations to raise the resolution fraction", and `:177`/`:181` "No internal-citation credit". C1 is 100 % internal-citation credit by construction.
Smallest safe correction: the r85 `depth:verifiability` row must carry the qualifier `internal-citation repoint; external RESOLVES unchanged 4/741` (and the existing 4 must not be graded "improved" as verifiability).

### A2 — Is 18 an arbitrary slice (free meter inflation), or the whole class?

Probe (`receipts/c1-composition.txt`):

```
GONE tokens 583  repairable-unique-basename 18  ambiguous-basename 5
ambiguous sample ['claim_checklist.md','custodian-receipts.json','provenance.json','report.md','status.json']
map keys 18   map keys that are also in repairable 18
bulk-sweep simulated rate = 167/732 = 22.81%
```

The repairable class is **exactly** 18 and the map takes all 18; the 5 ambiguous basenames are correctly excluded. Re-running the same repair rule over every GONE token reproduces `167/732` exactly — so there is no withheld cheap move and no unclaimed inflation left in this class.
Verdict: **SURVIVES** (no under-delivery, no hidden headroom).

### A3 — Can a reader open what SKILL.md cites, at the cited meaning?

All 17 changed lines are in `receipts/c1-repaired-lines.txt`. Sample: `Authoritative detail: corpus/knowledge/ufo-workspaces.md, repo-git-state.md, target-checkouts.md` → each item becomes independently openable (the list previously required inferring the first item's directory). Every other repair is a prose/table mention of an instrument (`score-gap.py`, `capture-binding-check.py` row, `r-defect-closure.sh`, `shonen-form.py`, `entry29-fixed-bytes.md`, `source-recheck.py`); commands that were already full paths (`python3 corpus/instruments/frontier-recheck-count.py …`) are untouched. No line's meaning changes; line count and table shape are preserved (`bad_lines=0`).
Verdict: **SURVIVES** — real, small, meaning-preserving gain. It is bookkeeping, not new evidence.

### A4 — Can a cheap forgery reach 167/732 with all limbs passing?

| Forgery | Command | rc | Verdict |
|---|---|---|---|
| F1 pad base with 3 resolving lane paths | frozen counter (commands as recorded in `receipts/c1-forgeries.txt`) | **1** (`after=158/742`, M1/M2/M3 FAIL) | counter SURVIVES |
| F4 map with two values pointing at tracked `.ufo/` copies of the same basenames (the 14 `S040-live.txt` / 41 `resolve.py` copies exist) | frozen counter, `--map map-ufo.json` | **1** (`M4 bad=resolve.py,score-gap.py`, M1 `167/733`) | counter SURVIVES |
| do-nothing / pad-18 / de-cite-18 / wrong-target / partial-9 (`controls/c1-controls-r85.txt`) | frozen counter | all **1** | counter SURVIVES |

Structurally the counter cannot be gamed: M3 forces the after file to be byte-for-byte the base with the map substituted, M4 forces unique git-tracked non-`.ufo` paths ending in the key, M5 pins the map bytes. No forgery I can build reaches the target without the map.

### A5 — Duplicate authority: the metric has two numbers in the same tree after landing

`python3 corpus/instruments/score-gap.py` at HEAD (`receipts/c1-coauthority.txt`) — the lane's own reporter for "the four committed-byte measurements that decide whether depth:verifiability 5 is reachable":

```
census-lane: 1227/5152 = 23.82%
census-skill: 132/701 = 18.83%
```

C1's counter at the same HEAD prints `after=167/732` (22.81 %). `citation-survival.md:31` still says `132/701 = 18.83 %`, and `SCORECARD.md:66` names that file "the committed census file is authoritative". Regenerating it is not free: `figure-audit.py` pins its figures (`census-internal-r56-receipt recorded=1130 derived=1130`, `census-gone-r56 … 3915`), so a regeneration must move the ledger in the same round.
Verdict: **BREAKS** the claim's "the scored meter itself" as a single authority — the score-5 decision instrument does not read the claim's number, and the tree now carries two SKILL rates 4 pp apart with no disclosure in `claims.json`. Routed as D1.

## 2. C2 — `coverage / capability acquisition`, priced package for H1 1913733

### B1 — Is it an "end-to-end domain task" in the sense of SHONEN box 2 and proposal 2?

`SHONEN.md:7` — "At least one end-to-end domain task executed and logged in LOG.md". `considerthese/2026-10-26.md:30` (proposal 2) proposes exactly this artefact: "take one public disclosed report …, build the six-file claim package …, and price it through F13/F17/F18". The *type* is therefore endorsed by the lane's own proposal, retrospective and submission-free included.
Verdict: **SURVIVES** as a task type. Caveat: proposal 2's "price it through F13/F17/F18" is not what the frozen counter prices — `e2e-check.py:derive()` prices 5 vendor/platform fields in S119/S120/S121 plus a KEV substring test; S121's four-level ladder quote (`Q03-medium-def`, manifest `anchor=103`) is captured and never used. The demonstrated capability is "transcribe a vendor advisory into a pricing block", which the r43 exemplar already did for CVE-2025-9086 (Low / 505 USD). The frontier pricing knowledge is not exercised.

### B2 — Is "coverage" the right axis label?

`AXES.md` coverage = "Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes)". A capability is not an axis: `AXES.md:59–64` says the six axes "do not measure what the shokunin can now *do*", and `SCORECARD.md:300–310` carries a separate `capabilities:` table with exactly one row (`sources-registry`, r22) whose columns are name / what it can now do / evidence pointer / first-working round. `claims.json` labels C2 `coverage (capability acquisition: …)` and no predicate (`P1`–`P6`) requires that row.
Verdict: **BREAKS** as a category — the claim type is bundled into an axis name, and the capability table entry that `AXES.md:63–64` requires ("a capability without a passing demonstration … does not enter the table" — the inverse also holds: a capability claim without a table row is pre-claiming) is absent. Routed as D2. Coverage score 8 held stays honest; the *label* does not.

### B3 — Does the counter evidence an end-to-end task on report 1913733? (substantive forgery)

Forgery: the r43 exemplar package (body = CVE-2025-9086, H1 report 3294999) with (i) S119/S120 byte copies added as evidence, (ii) an appended `## Pricing` block carrying the correct 1913733 lines, (iii) `status.json` `manifest_sha256` rebound. Re-runnable: `receipts/REBUILD-wrong-subject.sh` (scratch-only). Output `receipts/c2-wrong-subject.txt`:

```
package=…/c2-forged-pkg rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
LIMB E1 pass gate_rc=0
LIMB E2 pass bound=S119,S120
LIMB E3 pass section=True bad=none
LIMB E4 pass quotes=3 missing=0
LIMB E5 pass rel=corpus/practice/curl-h1-1913733 log=True shonen=True
E2E-RESULT pass limbs=5 rc=0
body: 1:# CVE-2025-9086 … 4:https://curl.se/docs/CVE-2025-9086.html 23:reports/3294999 102:price-cve: CVE-2023-28319
```

**rc=0 on a package whose report is about a different vulnerability and a different report id.** Nothing in E1–E5 binds the package's subject, title, affected asset, vulnerability class or narrative to `price-cve`; E5 is a substring test on two committed docs (`e2e-check.py` `full()`: `rel in log and rel in shonen`).
Verdict: **BREAKS** — the counter measures package *shape plus five transcribed fields*, not "one end-to-end domain task for 1913733". The claim's statement ("build the six-file claim package … for disclosed HackerOne report 1913733") is not what P1 proves.

### B4 — E4 "≥ 3 located quotes"

| Forgery | Output | rc |
|---|---|---|
| `> a` / `> b` / `> curl` | `E4 pass quotes=3 missing=0` | **0** |
| three empty quote lines `> ` | `E4 pass quotes=3 missing=0` | **0** |
| quotes from S052 (KEV, outside the pool) | `E4 FAIL quotes=3 missing=2` | 1 (control holds) |

A one-letter quote is "located" because the match is `norm(q) in norm(snapshot)` and the empty string is in every snapshot. Verdict: **BREAKS** E4 as "≥3 located quotes" (`receipts/c2-pricing-forgeries.txt`).

### B5 — Can the pricing be wrong and E3 still pass?

| Forgery | Output | rc |
|---|---|---|
| body says "Critical severity, CVSS 6.3, HackerOne awarded 2500 USD, listed in KEV"; price lines correct | `E3 pass bad=none`, `E4 pass` | **0** |
| duplicate `price-severity: critical` line after the correct one (`got.setdefault` keeps the first) | `E3 pass` | **0** |
| a second `## Pricing` section with all seven values wrong (`re.search` reads only the first section) | `E3 pass` | **0** |
| `price-kev: not-listed-or-listed-unknown` (startswith test) | `E3 pass` | **0** |
| no `## Pricing` section | `E3 FAIL`, `E4 FAIL` | 1 (control holds) |

Verdict: **BREAKS** — E3 checks the first occurrence of seven keys in the first `## Pricing` section only; contradictory machine-readable price lines and a wrong price section in the same document both pass (`receipts/c2-pricing-forgeries.txt`).

### B6 — The price triple is not a price

The forced values are `platform-bounty-flag: false` (S119 `has_bounty?` false), `reward-at-disclosure: 2400 USD` (S120 `Bug bounty: 2400 USD`), `reward-current-policy: none` (S121 "There is no bug bounty …"). E3 requires a package to assert all three and never asks it to reconcile them, so a reader cannot tell what the finding was paid; the counter rewards transcription of a source conflict. Verdict: **BREAKS** the claim's "priced" as an established price — routed as D3 (the package's prose must state the conflict; no new pricing field this round).

## 3. Impacted axes

| Axis | Impact |
|---|---|
| `depth:verifiability` | C1 moves the number, all of it internal (`154 INTERNAL + 4 RESOLVES`). Grading it "improved" without the internal-only qualifier overstates the axis (see D1). |
| `coverage` | C2 does not add a governed surface; the score stays 8. The axis *label* carries a capability claim that `AXES.md` puts in another table (D2). |
| `calibration` | C2's P1 passes a wrong-subject package (B3) and E3/E4 pass contradictory or empty pricing text (B4, B5). The round's most self-asserting artefact is the least bound to its own statement. |

## 4. Routed defects (nothing frozen is changed this round)

1. **D1 (C1, landing text — integrator decision).** Do not let the r85 `depth:verifiability` row assert external verifiability, and do not leave the tree with two un-reconciled SKILL rates. Re-run: `python3 corpus/instruments/score-gap.py` → `census-skill: 132/701 = 18.83 %` at HEAD while C1's counter prints `167/732`. Smallest safe correction this round: qualify the row `internal-citation repoint; external RESOLVES unchanged 4/741; census of record still 132/701`; next round regenerate `citation-survival.md` together with `figure-audit-ledger.json` pins (`census-internal-r56`, `census-gone-r56`).
2. **D2 (C2, label).** Record C2's claim type as `capability-acquisition` and add the `SCORECARD.md` `capabilities:` row (name / what it can now do / evidence pointer / first-working round), or drop "capability acquisition" from the `coverage` axis string. `AXES.md:59–64`, `SCORECARD.md:300–310`.
3. **D3 (C2, package text).** The package's `report.md` must state the source conflict in prose: S119 `has_bounty?` false and S121 "no bug bounty" versus S120 "Bug bounty: 2400 USD". No counter field can check it; a package that omits it passes E3.
4. **D4 (C2 counter, next round — frozen now, do not change).** E4 accepts sub-word and empty quotes; E3 ignores duplicate/contradictory `price-*` lines and any second `## Pricing` section; no limb binds the package subject to `price-cve`/the report URL. Add: a minimum quote length (≥5 words, non-generic), duplicate-key rejection, single-section rule, and a subject binding (body must contain the report URL or CVE that `price-cve` names).

## 5. Limits of this review

- C2's package did not exist, so C2 was attacked at the counter, not at the landed artefact. If the landed package's prose contradicts its price lines, D3 fires; if its body is the right CVE, B3's hole is latent rather than realised.
- E2's byte-equality was exercised only with scratch fixtures (lane bytes copied in); no lane file was modified.
- `MIRROR_ABSENT=True`; the 18 base verdicts are for bare basenames that carry no bounty prefix, so the target should be host-robust — but that is `[INFERENCE]`, not measured on a mirror-present host.
- No network use, no live target, no git/jj writes. Tooling: nothing installed. Scratch `/fast/scratch/hyaku/kasegi-r85/CriticClaims` removed at exit.
