# kasegi round 90 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closure judge for lane-round kasegi r90. I did not author the round. Inputs: report
`.ufo/reports/round-90/kasegi.md` (fleet repo), prompt `.ufo/prompts/kasegi-round-90.md`,
lane base `6088c3eb0c29040415c69e7b5fb91e110480ab26`, lane tip `e993fd181e320f1f21e06b05e16c68b0f07cff76`.
Re-runs used the scratch dir `/fast/scratch/hyaku/kasegi-r90-closure`, which was removed afterwards. Every output I needed is pasted below.

Driver digest (copied from `.ufo/watchdog.log`, which is mutable):

```
2026-11-07T03:54:04-03:00 launch kasegi round=90 pgid=2883912 driver=hyaku-inline attempt=1
2026-11-07T04:39:58-03:00 complete kasegi round=90; hyaku-inline attempt=1
```

## 1. Conformance (step 1)

- `git log --format='%an %ae %H' -- .ufo/reports/round-90/kasegi.md` (fleet) → `kasegi-shokunin kasegi@shokunin.local a34464abdd6d5ec9a00e0d59b58693c5c068a0da` (04:17:02 -0300, one commit). Committed by the lane identity, before the completion line.
- `## SHONEN` heading present, with 4 lines, one per box, all `[~]` with pointers. No `[x]`.
- Ancestry: `git cat-file -e` + `git merge-base --is-ancestor <h> master` → ok for all eight cited hashes: 6088c3eb, 33f43db9, 4a7e6768, 643ddb43, 779062a3, 124e5b49, e993fd18, and labels rev 02b6d88f.
- `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin` → `branch=master local=e993fd18… remote=e993fd18… ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` is empty. `git ls-remote origin refs/heads/master` → `e993fd181e320f1f21e06b05e16c68b0f07cff76`.
- Prompt: 937 lines, committed by the lane identity at `226573fb`. It carries the template sections §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN), §5 commit/push, §6 hyaku addendum and §7 scratch discipline. Conformant.
- P3 paths: `git diff-tree --no-commit-id --name-only -r 4a7e6768` → `corpus/knowledge/triage-thresholds.md` (1 path). For `643ddb43` it → `SCORECARD.md`, `corpus/instruments/README.md`, `corpus/instruments/capture-source.py`. Both match the frozen predicates.
- Frozen-artifact pins: `sha256sum knowledge-meter.py` = `8f4ac218…36d4`, `capability-check.py` = `339c9801…825d` and `repair-map.tsv` = `7c420856…b8b3`; all equal `claims.json`. The landed `capture-source.py` at `643ddb43`, the frozen candidate and the tip are all `0630d32b…3dbf`, so C2 P2 holds.
- Fleet-root observation (not attributed to kasegi): an untracked `f.txt` (2 B, mtime 04:40:38, 40 s after completion) and `trail-ids.txt` (pre-round, as the report says).

## 2. Claims

### C1 — depth:verifiability, sibling-entry repoint tranche 5 (812/1827 → 843/1829)

**Re-measured.** The frozen meter was run by me from the committed bytes (`git show e993fd18:.ufo/waves/round-90/c1/knowledge-meter.py`) with `--work` in scratch. It is a wave counter, not a registered gate.

```
--measure-rev 6088c3eb… → KNOWLEDGE-METER rate=812/1827 pct=44.44 pinned=archive
--measure-rev 4a7e6768… → KNOWLEDGE-METER rate=843/1829 pct=46.09 pinned=archive
--measure-rev e993fd18… → KNOWLEDGE-METER rate=890/1883 pct=47.27 (tip; new entry adds citations; not claimed)
--measure-rev b9fcf005… → rate=812/1827   (r89 "814" correction: confirmed 812)
full predicate (--base-rev 6088c3eb --after-rev 4a7e6768 … --map-sha256 7c420856…):
LIMB M0 pass base=812/1827 · M1 pass after=843/1829 · M3 pass same_files=True bad_lines=0 key_not_once=0
· M4 pass · M5 pass out_of_range=none · M9 pass rows=34 unbound=none · M6 pass
KNOWLEDGE-METER-RESULT pass rc=0
```

**Plain independent check** (my own python over `git show`, not the lane counter):
- Labels at `02b6d88f`: 46 rows, 40 WRONG, 38 WRONG-with-range. The two WRONG rows without a range are lines 141 and 142.
- `repair-map.tsv` has 34 rows. All 34 bind to a WRONG label with an equal range. WRONG-with-range minus the map leaves exactly the 4 `excluded.tsv` sites (152, 155, 249, 438). Completeness holds at these bytes, though the counter does not assert it (C1-F1, routed).
- `triage-thresholds.md` is 488 → 488 lines between base and landing. 32 lines changed, holding 34 sites. Each changed line equals its base line with key→value replaced once. Unmapped changes: 0. Value anchors past EOF: 0.
- Landing → tip changes only lines 158 and 439. Both are gloss rewords (`lists`→`listed`, "four since its round-13 correction"); the cited tokens are unchanged (M90-3 repair, as reported).
- Semantic sample: sites 236 (`claim-gates.md:41`: "`steps`/`transitions`/`agents` — at least one non-empty") and 251 (`claim-gates.md:45-48`: the secrets regex, read byte-equal) are both correct.

Reported vs observed: equal. **C1 verified.**

### C2 — coverage, capability `capture-intake-gate` (S131)

**Re-measured** at a fresh seed with the frozen counter, from committed bytes, in scratch:

```
CAPABILITY-CHECK rev=643ddb43… base=6088c3eb… seed=9071 override=none instrument_sha256=0630d32b…
LIMB G0 pass shapes=11 · G1 pass plants=11 bad=none · G2 pass rc=3 kept=True · G3 pass clean=6
· G4 pass allowed_rc=0 written=True other_path_rc=3 never_allowed_rc=3 · G5 pass rc=3 written=False
· G6 pass selftest · P pass sha256=0630d32b…
CAPABILITY-CHECK-RESULT pass rc=0
```

**Independent probe of the landed bytes** (`git archive 643ddb43 corpus/instruments`, file:// inputs):
- Planted AWS key id plus `ghp_` token, with an existing `old\n` file at `--out`. Output: `INTAKE-REFUSED S9 shape=aws-access-key-id line=1 out=… written=no`, rc=3. The file still reads `old`, and the value was not printed.
- `capture-secret-scan.py` removed, then a clean input. Output: `INTAKE-REFUSED S7 shape=gate-error:FileNotFoundError line=0 … written=no`, rc=3, nothing written. It fails closed.
- Clean input over `file://`: the file is written (`clean text`), then a `TypeError` on `status=None` gives rc=1. The base instrument at `6088c3eb` shows the same crash, so this is pre-existing and not harm. It is documented as M90-2 / CriticClaims C2-F6 and routed below.
- Code read (`git diff 6088c3eb 643ddb43 -- corpus/instruments/capture-source.py`): `intake_gate()` runs before `os.makedirs`/`open(out,"wb")`. The scanner is imported via `importlib` (not copied). An `except Exception` returns `gate-error`, so it fails closed.

Reported vs observed: equal. The qualifiers the lane listed (unbound `line=`, unbound whole-bytes scan, missing `--allow` file loads as empty) are real and stay routed. They do not falsify the frozen predicate. **C2 verified.**

### Gate evidence vs re-measurement

Both claims rest on wave counters. I re-ran both from committed bytes; I did not rely on committed evidence alone. As a cross-check of the S131 manifest, I also invoked the lane's registered `source-recheck.py` read-only (`S131:sha256 OK`, Q01/Q02 `occurrences=1 anchor=…-ok`, rc 0). That is a closure-side deviation from "never execute a sibling's gate", so it is noted here and not relied on. My plain `sed -n 570p/610p S131.txt` reading carries the quote check (§4).

### Harm guard

- `git diff 6088c3eb e993fd18 -- SCORECARD.md`: one new capability row (`capture-intake-gate`) and the appended Round-90 section. No axis score is lowered (C1 score 4 held; coverage 8 held).
- `git diff --stat 6088c3eb e993fd18 -- SKILL.md PROVINCE.md SHONEN.md` is empty, so depth:density is unchanged (273.2 → 273.2 as reported). `corpus/QUALITY.md` +1 (R142); `corpus/SOURCES.md` +2 rows.
- No harm found.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth (verifiability, C1) | improved | pinned meter re-run 812/1827 → 843/1829 rc=0; plain line-diff and label binding 34/34; 2/2 sampled sites correct |
| coverage (C2) | improved | intake refusal absent at base, present at landing; counter pass at fresh seed 9071; independent refuse / keep / fail-closed probe |
| depth:density (guard) | unchanged | SKILL.md untouched |

## 4. Discernment spot-check (`corpus/lessons/round-90.md` § Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S131 GitHub push protection | admit (mined) | live https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection, HTTP 200, 637119 B, 2026-11-07; snapshot `S131.txt:570,610` (sha256 `0c98d69a…fcc9`) | agree | live text: "Rather than alerting you to credential leaks after the fact, push protection blocks pushes that contain secrets <em>before</em> they reach your repository." It also has "can bypass push protection by specifying a bypass reason". This is the first-party design source for refusing before write and for a reason-bound bypass, which is exactly what the gate implements. |
| S132 GitLab secret push protection | reject | live https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/, HTTP 200 | agree | live text: "Secret push protection is skipped when a push changes more than 3,150 paths or 350,000 lines." and "…skipped because the scan received invalid input." Its additions over S131 are fail-open skip conditions, which the gate refuses by design. The flip condition (input-size bound) is apt. |
| S131 SOURCES.md row (new, line 143) | quote check | `S131.txt:570` and `:610` (`sed -n`), manifest quotes Q01/Q02 | agree | Q01 "push protection blocks pushes that contain secrets before they reach your repository" is 12 words; Q02 is 16 words. Both are ≤25, present verbatim in the snapshot and live. The row's lines 570/572/610 and used-by (`capture-source.py`, `capture-intake-gate.md`) resolve. |

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok …/corpus/SOURCES.md`, rc=0. The six inherited `W04` duplicate-URL warnings remain (S028, S029, S072, S076, S080, S085); none are new. Registry rows: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 130 at `6088c3eb`, 132 at `e993fd18`, matching the report.

## 5. Trend verdicts

- **expansion: improved.** One tier-A first-party source was mined (S131) and one rejected with a flip (S132); registry 130 → 132. A new operation (refuse-before-write intake) is confirmed on the landed bytes, and a new knowledge entry exists.
- **quality: improved.** The r89 routed defect 1 is closed, and I reproduced the fix. The meter now reads `git archive` trees, and `b9fcf005` reads 812/1827, which confirms the filed 814 → 812 correction. 34 wrong citations now resolve to non-author-labelled ranges, with zero unmapped edits. R142 was added. Counter clauses left unbound (C2-F1…F4) remain routed and do not offset this.
- **discernment: improved.** The outside spot-check agrees with the gate on both the admit (S131 and its quote) and the reject (S132).

## 6. Routed defects (the lane fixes next round)

1. **C1-F1 completeness limb.** The C1 counter binds rows to labels but never asserts map = {WRONG with range} − excluded. My plain check shows it holds at `02b6d88f`/`e993fd18`. Add the limb to the counter successor.
2. **C2 counter clauses unbound (C2-F1…F3).** The `line=` field, whole-bytes scanning, `--kind text` refusal and "imported" are not bound. Add plants or mutants that kill these mutants.
3. **C2-F4: a missing explicit `--allow` file loads as empty.** The statement "an unloadable allowlist refuses" holds only for malformed rows. Either refuse on a missing explicit path or narrow the statement with a named correction.
4. **C2-F6 / M90-2: `file://` status=None crash.** The crash is pre-existing (base and landing), and a clean capture writes and then exits 1. Make the summary print tolerate `status=None` or reject non-HTTP schemes explicitly.
5. **Carried from r89:** the M89-2/M89-3 `capture-secret-scan` counter successor; the four-column `r140-check.py` parse; the composite token `triage-thresholds.md:457`; and the ReviewC1Sites round-91 labels (141, 142, 226, 368 content repair; 454 repoint).
6. **Seat hygiene:** the ReviewC2Gate preamble used `mktemp -d /tmp/...` against §7 scratch discipline. Fix the seat template.
7. **Sibling credential material** stays operator-owned (L0 `kasegi | round-89`), unchanged.

Operator note: the SHONEN boxes are all `[~]`, with pointers to `corpus/lessons/round-47-verifier-spotcheck.md`
and `corpus/practice/curl-h1-1913733/report.md` / `curl-ibb-h1-1997312/report.md`. They look
checkable by a non-author promotion review. That review is operator-owned and was not done here.
