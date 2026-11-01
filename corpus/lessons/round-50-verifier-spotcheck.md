author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# Round 50 verifier spot-check — kasegi (non-author closure)

Lane repo: `fleet/kasegi-shokunin`, branch `master`. Range under review:
`28c65eb9093c..021989bf4f5699fa55c6d90abd37ce6ad1caa50a`. Report:
`.ufo/reports/round-50/kasegi.md` (fleet commit `2ae5cdc469d6ea72105a9b62e2de0d682acbcef3`).
This file is written by the closure judge, not by the lane; it is not committed by the lane.

## 1. Step-1 conformance

| Check | Result | Command / evidence |
|---|---|---|
| Report committed in fleet repo by lane identity | PASS | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-50/kasegi.md` → `kasegi-shokunin <kasegi@shokunin.local> 2ae5cdc469d6ea72105a9b62e2de0d682acbcef3` |
| `SHONEN` heading present, one mark line per box | PASS | report §SHONEN carries `## SHONEN` with 4 lines: `[~]`, `[ ]`, `[~]`, `[~]`, each with a pointer; no `[x]` written by the lane |
| Cited lane commits exist and are ancestors of `refs/heads/master` | PASS | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `e1c3ef5`, `33946a3`, `7918178`, `e27d080`, `021989b` (all PASS); base refs `c5e3636`, `a2de23b`, `28c65eb` also resolve |
| Lane branch tip pushed | PASS | `git ls-remote origin refs/heads/master` → `021989bf4f56…` = local `refs/heads/master` |
| Round's cited work reachable in `28c65eb..021989b` | PASS | `git log --format='%h %s 28c65eb..021989b'` lists exactly the five cited commits; `diff-tree --name-status` over the range matches the report's landed-changes table (all A/M paths as claimed) |
| Marker-vs-report | real report | The report names checkable work, evidence pointers and five resolvable commit hashes; not a marker |
| Dispatch window consistency | PASS | watchdog digest launch `2026-10-31T18:04:37-07:00`, complete `18:57:19-07:00`; lane commits dated 01:46–01:51 UTC fall inside |

Conformance defects found (status-neutral, named in §5): two — see D1 and D2.

## 2. Claim re-checks

Freeze integrity first: all 13 sha256 pins in `.ufo/waves/round-50/freeze-v2.txt` were recomputed
over committed bytes at the tip (`git show <tip>:<path> | sha256sum`) — **13/13 match**, including
`claims.v2.json`, the instrument, the S080 capture, the manifest and all nine control receipts.
The freeze of record is the bytes it pins.

### C1 — capability acquisition, depth:verifiability (4 → 4 held)

Gate/selftest limbs are the lane's own instruments: per the closure contract they are
**evidence-verified** (committed receipts), never executed, by this reviewer.

- Instrument committed at tip: `corpus/instruments/census-freshness-check.py` (A in range; sha256
  matches freeze pin). RE-MEASURED (ls-tree/sha).
- Self-test receipt `.ufo/waves/round-50/controls/c1-gate-selftest.txt`:
  `case=fresh want=0 got=0 … case=stale want=1 got=1 … case=tampered want=1 got=1 …
  selftest cases=3 failures=0` — matches the claim. EVIDENCE-VERIFIED.
- Mutant battery receipt `controls/c1-mutbat.txt`: `battery verdict=complete mutants=6 closed=5
  survivors=1 (error-exit-0 …)`, survivor named, builder `c1-mutbat.py` committed beside it —
  matches the claim including the disclosed survivor. EVIDENCE-VERIFIED.
- Final gate receipt `controls/c1-gate-final.txt`: `CENSUS-FRESH=ok files=2`, re-measured per
  `freeze-v2.txt` rev 3 after the last census regeneration, which is the tip commit `021989b`
  (touches only the two census files + freeze-v2.txt). EVIDENCE-VERIFIED.
- Do-nothing control substance: RE-MEASURED — `git ls-tree 28c65eb -- corpus/instruments/` and
  `… c5e3636 …` show no `census-freshness-check.py` at either base, so the counter cannot print
  `CENSUS-FRESH=ok` at a base export.
- **D1 (defect, status-neutral): do-nothing-c1.txt provenance.** The receipt is labeled "produced
  on this host" (report; `claims.v2.json` do_nothing_control; erratum §"What survives unchanged";
  lesson M3 calls its error string "Windows CPython"). Its bytes are
  `python3: can't open file '/fast/scratch/hyaku/kasegi-r50/base-export/…': [Errno 2] …` +
  `C1_EXIT=2` — a Unix CPython errno string for an unconverted `/fast/...` path with a *functioning*
  `python3`. Probed live on this host: `python3` is the Microsoft Store stub ("Python was not
  found; …"), and `python /fast/...` prints
  `C:\…\python.exe: can't open file 'C:\\Program Files\\Git\\fast\\…': [Errno 2] …` — a different
  format. No run on this host produces those bytes; the erratum's host-distinguishing claim for
  this file is factually wrong, and the file is an old-host import. The control's *substance*
  still holds (independently re-derived above), so C1 is not defeated; the mislabeling is exactly
  the M3 class the round itself mined.
- Census of record figures: the report/LOG/SCORECARD/lesson state 204 files / 4807 distinct —
  **see D2 below**; the certified tip census reads 204 files / **4809** distinct. The C1 predicate
  (byte-identity, receipt ok) is unaffected.

Verdict C1: **verifies** (capability acquired; gate evidence complete; substance of every
predicate re-measured or evidence-verified). Axis depth:verifiability: **improved** (capability
row enters the table on a demonstrated run; numeric score honestly held at 4 by the lane's own bar).

### C2' — frontier admission F31 (OSV affected-range events), coverage (8 → 8 held)

Plain re-measurements over committed bytes (this reviewer's own commands):

- `git show <base>:corpus/SOURCES.md | grep -cE '^\|\s*S[0-9]{3,}\s*\|'` → **79**;
  same at tip → **80**. The range diff for SOURCES.md is exactly one added line (S080) —
  append-only respected; S065 byte-identical (`rejected`, R8 claim holds).
- S080 row complete: kind `spec`, tier A, status `mined`, opened `2026-11-01`, recheck `90d`,
  used-by the new entry, anchors into the capture, capture sha256 `97b850a4…` written in-row.
- Capture: `git show <tip>:corpus/source-snapshots/round-50/S080.txt | wc -l -c` → **1462 lines,
  70913 bytes**; sha256 matches the freeze pin, the manifest, and the in-row value.
  RE-MEASURED.
- Manifest: 16 assertion ids `Q1…Q16` (counted). Receipt `controls/s080-recheck.txt`: 16/16
  `OK`, `anchor=N-ok` throughout, `S080:sha256 OK`. EVIDENCE-VERIFIED (source-recheck.py is the
  lane's instrument; not executed by this reviewer).
- Gate quote (≤25 words) located in committed bytes at `S080.txt:9-10`: "This document defines a
  standard interchange format for describing vulnerabilities in open source packages." —
  14 words. VERBATIM-VERIFIED in the committed capture.
- Frontier census receipts: before `controls/do-nothing-c2-winhost.txt` = `FRONTIER-CENSUS rows=30
  admitted=30 closed=0 problem-rows=30 registry=79`, `entries=33 pass=0`, **zero `F31` lines**
  (grep -c F31 = 0); after `controls/c2-counter-final.txt` = `rows=31 admitted=31 closed=1
  problem-rows=30 registry=80`, `entries=34 pass=1` with `FRONTIER-PASS F31 ids=S080`; FAIL lines
  counted: **33**, all carrying exactly `problems=recheck-exit-1` (0 exceptions) — the honest
  inherited-debt taxonomy as claimed. Receipts pinned by freeze-v2. EVIDENCE-VERIFIED.
- Independent cross-checks: README frontier rows `| F[0-9] |` 30 → 31; F31 row present (line 743)
  with the round-50 admission block (lines 739/745); PROVINCE r50 amendment appended at EOF
  (line 178, R6-style append); knowledge entry `corpus/knowledge/osv-affected-range-events.md`
  carries the provenance trio (source S080 + URL + capture, verified-at 2026-11-01,
  interpreter-portable `python3 || python` recheck), `ground: F31`, and stated distinctness
  against F25/F21/F23. corpus/*.md file count 232 → 234 = exactly the two claimed new files.
- The re-open fires the S065 flip condition as recorded (OSV-specific range semantics the CVE
  format cannot express), stated in both the SOURCES row and the entry.

Verdict C2': **verifies** (new, non-duplicate, first-party-sourced frontier admission; every
plain number re-derived). Axis coverage: **improved** (frontier measure 30 → 31; score honestly
held at 8 under the declared operator-owned denominator).

### Axis-harm check

`git diff-tree -r -p 28c65eb 021989b -- SCORECARD.md` is purely additive (zero removed lines):
Round-50 result section appended; depth:verifiability 4→4 held, coverage 8→8 held,
depth:density 9 held (SKILL.md untouched — not in the range diff). No owned axis harmed.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| Admit S080 (OpenSSF OSV format spec page) → F31 | admit (Gate) | Live fetch `https://ossf.github.io/osv-schema/` + committed capture | **agree** | Live page today: version line "Version 1.9.2 (October 13, 2026)" (= S080.txt:4); purpose sentence matches the Gate quote verbatim (= S080.txt:9-10); events introduced/fixed/last_affected/limit confirmed; three range types SEMVER/ECOSYSTEM/GIT confirmed. The surface is what the row says it is; tier A (primary spec) is right; genuinely new vs F25/F21/F23/F19. |
| Refuse the inherited freeze C2 (F31 = EPSS) as duplicate of F19 | reject (Gate) | `PROVINCE.md:78` (r36 amendment), `corpus/knowledge/epss-exploit-prediction-scoring.md`, S053 | **agree** | F19 is an admitted EPSS surface with its own entry since round 36; the frozen C2 named distinctions only against F01/F05/F13/F18, never F19. Landing it would have been a fabricated admission; the refusal is the correct call and the flip-condition re-open of S065 is the legitimate path to an F31. |
| New SOURCES row S080 quote | row check | Committed bytes `S080.txt:9-10` + live page | **agree** | Quote ≤25 words (14), located, verbatim in both the committed capture and the live page. |

Census (this reviewer's own run):
`bash <fleet>/scripts/sources-census.sh validate --root <fleet> kasegi` → exit **0**,
`kasegi ok`, five W04 warnings: the four inherited (S028/S029/S072/S076 duplicate-url) plus the
expected `W04 S080 duplicate url ossf.github.io/osv-schema across scopes` (the disclosed S065/S080
re-open pair) — exactly the round-end state the report pastes.

## 4. Trend verdicts (with evidence)

- **expansion: improved.** Frontier 30 → 31 admitted (README rows re-counted; counter receipts),
  on a genuinely new, first-party captured, non-duplicate surface reached by firing the recorded
  S065 flip rather than re-admitting held ground. The coverage score is held by declared
  denominator; the improvement is the frontier measure, stated as such by the lane.
- **quality: improved.** A new re-runnable instrument (selftest 3/3, battery 6/5-closed/1-named)
  converts the round-49 stale-census mistake class into an exit-1, with the fresh census of record
  certified at the tip. Residue named, not gamed (67 host-bound recheck lines filed as L0 kasegi
  round-50, verified present at fleet `.ufo/l0-questions.md` line 225). One blemish routed as D2:
  the final regeneration left 4807 in the prose records vs 4809 in the certified bytes — a fresh,
  small instance of the very number-drift class the round mined; it does not un-improve the
  instrument or the corpus.
- **discernment: improved.** The round refused its own inherited freeze on three mined defects
  (duplicate surface; host-unportable predicates; unproducible control), re-froze only at the bar
  the host supports, and reported the unflattering taxonomy (`entries=34 pass=1`, 33 ×
  `recheck-exit-1`). Both sampled gate decisions (admit S080, refuse EPSS C2) agree on re-open.
  Scores asserted: none; held: all.

## 5. Routed defects for the lane (fix next round; append-only corrections)

- **D1 — do-nothing-c1.txt provenance mislabel (attribution class, M3's own class).** The report,
  `claims.v2.json`, the erratum §"What survives unchanged", and lesson M3 all attribute the
  receipt to this host; its bytes are an old-host (Linux, `/fast/...`, working `python3`) run, and
  the erratum's "Windows CPython error string" distinguishing claim is factually wrong (probed:
  Store stub; Windows python formats the error differently). Fix: a named erratum/lesson row
  relabeling the file as an imported old-host receipt; the control's substance is unaffected and
  independently re-derived (instrument absent at both base commits).
- **D2 — census-figure number-drift (number-drift class).** The report, LOG round-50 entry,
  SCORECARD round-50 row and the lesson erratum state the census of record as "204 files / 4807
  distinct", while the certified tip census (`021989b`, the last commit, receipt `CENSUS-FRESH=ok
  files=2`) reads **204 files / 4809 distinct** (final regen: GONE 3736→3738, total 10295→10298),
  and no committed in-scope byte change between `e27d080` and `021989b` explains the delta — one
  of the two census runs was not taken over the bytes it shipped with. Fix: an append-only
  correction naming 4809 as the census of record at `021989b`, and a sentence in the lesson on
  the regenerated-after-record pattern the gate exists to catch.

Both defects are status-neutral conformance/evidence defects; neither defeats a claim, and no
axis is harmed.

## 6. Verdict summary

| Axis | Verdict |
|---|---|
| depth:verifiability | improved |
| coverage | improved |
| depth:density | unchanged |

Claims: C1 verifies (capability acquisition), C2' verifies (frontier admission). Exploratory
claims: none declared. **Round admitted** — every claim verifies and no owned axis is harmed;
defects D1/D2 ride the notes and the routed queue.
