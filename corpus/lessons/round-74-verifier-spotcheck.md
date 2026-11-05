# Round 74 — verifier spot-check (non-author integrator)

author: hyaku closure (non-author integrator, @m_zfl)

Subject: kasegi r74 (attempt 1). Lane HEAD measured: `dca80cf52c5d640ec8be3465fc4aa8e7c5648cc1`. Base and controls: `ccd6a54bf392922495c4860332665499582e3213`. Freeze: `847b53792d2d29d161cad7d21a33c89df9e52e8d`. Pre-freeze controls: `654d877f0bd4005fd139c46e5b889f4c1833ddda`. Replay receipt: `a5e814a1`. Report: `.ufo/reports/round-74/kasegi.md` (fleet commit `1ebb85bfd70ad79a7bb4700f05a7182b2c662f76`, author `kasegi-shokunin <kasegi@shokunin.local>`). Lane lesson under review: `corpus/lessons/round-74.md`.

Dispatch digest (copied from `.ufo/watchdog.log`, mutable):
- `2026-11-05T05:13:46-03:00 launch kasegi round=74 pgid=923825 driver=hyaku-inline attempt=1`
- `2026-11-05T06:14:07-03:00 complete kasegi round=74; hyaku-inline attempt=1`

Method. Plain measurements over committed bytes (`git show`, `git ls-tree`, `git diff`, `grep`, `wc`, `sha256sum`, `python3` stdlib). The lane-owned gates and selftests (`recheck-cwd-census.py`, `frontier-recheck-count.py`, `capture-binding-check.py`, `source-recheck.py`, `claim-package-check.py`) were **not executed**; their committed receipts were read instead (PROTOCOL §Gate standard, Closure consequence). Re-executed by this verifier: `sources-census.sh validate` (operator-side), the manifest quote/anchor check over committed bytes, and live re-opens of two sources. Claims re-measured vs evidence-verified: **C2 re-measured** (every frozen after-value re-derived over committed bytes); **C1 evidence-verified** (gate rests on the lane's selftest; receipts read, plus byte-level diff of the counter and the parity sha over committed bytes). No sibling gate was executed.

## 1. Step-1 conformance

| check | command / evidence | observed | result |
|---|---|---|---|
| report by lane identity | `git log --format='%an %H' -- .ufo/reports/round-74/kasegi.md` (fleet repo) | `kasegi-shokunin <kasegi@shokunin.local> 1ebb85bf…` | ok |
| SHONEN heading, one line per box | `grep -c '^## SHONEN'` = 1; `grep -cE '^- \[(x\| \|~)\]'` = 4 | four `[~]` lines with pointers (boxes 1–4) | ok |
| cited lane hashes resolve | `git cat-file -t` | `ccd6a54…`, `654d877f`, `847b5379`, `a5e814a1`, `dca80cf5…` all `commit` | ok |
| ancestry against branch ref (not `@{u}`) | `git merge-base --is-ancestor <h> master` | all five exit 0 | ok |
| report hash = lane tip | `git rev-parse HEAD` (lane repo, detached) | `dca80cf52c5d640ec8be3465fc4aa8e7c5648cc1` | ok |
| lane clean and pushed | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `branch=master local=remote=dca80cf5… ahead=0 behind=0`; porcelain empty | ok |
| remote confirms tip | `git ls-remote origin refs/heads/master` | `dca80cf52c5d640ec8be3465fc4aa8e7c5648cc1` | ok |
| census (operator script, my run) | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok`, exit 0; six inherited W04 warnings (S028 S029 S072 S076 S080 S085), unchanged | ok |
| prompt carries template contract | `.ufo/prompts/kasegi-round-74.md` vs `templates/round-prompt.md` | §1 mission/axes binding, §2 claim cap 1–3 + exploratory rule, §2b frontier step + census command, §3 L2 floor 8 + role split, §4 report sections + SHONEN + marker rule, §5 commit-then-push + push scope + L0 — verbatim modulo substitution; hyaku addendum §6 present; committed at fleet `0106fdcb` by lane identity | ok |
| dispatch digest | watchdog lines 2771, 2790 | identical to the lines given at closure | ok |
| report is real, not a marker | work items, evidence pointers, LOG-tied landed-changes table (`LOG.md` § Round 74 at lane line 2787) | real report; status `ok` | ok |

Status `ok`. Conformance defect (status-neutral): the report's "Landed-state checks (L1, after integration)" census line — see §5, V74-1.

## 2. Claim re-checks

### C1 — depth:verifiability (counter amendment; score held 4, nominal per QUALITY R58) — VERIFIED with defect V74-1

Evidence-verified (no gate executed):

- **Red-before receipt** `.ufo/waves/round-74/controls/c1-redbefore-mutant-survival-r74.txt`: header names revision `ccd6a54…` and `2026-11-05T08:31:27Z` (pre-freeze); M4-forced-conformant, M5-hardcoded-tmp, M6-scratch-leak, M7-last-line each `cases=1 failures=0` exit 0 `VERDICT=SURVIVED`; orig r73 counter same. Matches the frozen do-nothing control.
- **Amended counter at tip**: `git diff ccd6a54 dca80cf5 -- corpus/instruments/recheck-cwd-census.py` = 87 added lines, confined to the selftest; tip file registers exactly the five frozen cases (`check("prefix-census"…`, `check("result-main"…`, `check("tmpdir-parent"…`, `check("scratch-cleanup"…`, `check("first-line"…`) and prints `selftest cases=5 failures=%d`.
- **Kill receipts**: `.ufo/waves/round-74/w1/MutAuditC1-evidence.txt` (independent battery) shows mutant counters `failures=1` (e.g. `fixtures counter=M9p-foreign-cwd-is-lane.py failures=1`) and `fixtures counter=orig-base.py failures=0`; `.ufo/waves/round-74/w1/ExecC1Amend-kills.txt` present. Kill rule (a) holds: no survivor.
- **Parity limb (b)**: `.ufo/waves/round-74/w1/ExecC1Amend-parity.txt`: `sha256 orig-stdout = sha256 amended-stdout = e1906b886e856fa688f01f08b28a5034e5979adc311d3a040e7642776770f241`, equal to the base receipt value; byte difference 0.
- **Kill rule (c), (d)**: conformant positive control in `MutAuditC1` fixtures (`F-result` `last_good=RECHECK-CWD-RESULT conformant, rc_good=0`); `SentinelCounter.md` §1 recorded one `bash -c` call site before and after (no exec-surface expansion).
- **Scope sentence (M74-6)**: the lane's own WEAKENED verdict is confirmed by the committed critic/reviewer findings; routed, not re-worded (freeze discipline respected).

Verdict: the claim's target (the selftest kills the four routed survivor classes, parity preserved, no exec expansion) verifies on committed evidence; kill rule (a)–(d) all pass; axis `improved` (instrument verifiability move; score nominal 4 → 4 by design).

**V74-1 (new defect, this verifier — census-evidence timing).** The counter's entry population is `glob(corpus/knowledge/*.md)` (tip file lines 63–70), so at the implementation revision `dca80cf5` (90 knowledge files, measured: `git ls-tree -r --name-only dca80cf5 corpus/knowledge | grep -c '\.md$'` = 90) a census run would print `entries=90` (and `exit0_foreign=68`, the new entry's recheck exiting 0 from a foreign cwd per the entry-recheck receipt). Every committed census line carrying values — the report's C1 section, `corpus/lessons/round-74.md` § Counters ("entries 89 = `ls corpus/knowledge/*.md` 89"), and the report's "Landed-state checks (L1, after integration): `entries=89` = `ls corpus/knowledge/*.md` = 89" — describes the mid-round working tree (89 files, before the C2 entry landed), not the implementation revision. The frozen census clause binds `printed entries == ls corpus/knowledge/*.md | wc -l` **at the implementation revision**: it is satisfiable there (90 == 90) but no committed receipt demonstrates a census run at that revision, and the "after integration" line misstates the tree (tip `ls` = 90). The `claims.json` note "C2's landing cannot falsify it (RC-6 class)" is likewise falsified as a statement about receipts. Class: M74-2 (measured value attributed to the wrong tree). Status-neutral: the shape zeros (`noprefix=0 exit2_foreign=0 norecheck=0`, conformant) are receipt-backed and unaffected; no kill-rule limb depends on the absolute counts. Routed: round 75 re-runs the census at the actual tip revision, commits that receipt (expect `entries=90`, `exit0_foreign=68`), and appends an erratum correcting the landed-state line and the claims-note lesson.

### C2 — coverage (frontier admission F52 on S109; score held 8) — VERIFIED (re-measured)

Every frozen after-value re-derived by this verifier over committed bytes:

| frozen clause | my command | observed |
|---|---|---|
| registry = 109 (base 108), one new row S109 | `git show {ccd6a54,dca80cf5}:corpus/SOURCES.md \| grep -cE '^\|\s*S[0-9]{3,}\s*\|'` | 108 → 109 |
| every pre-existing row unchanged | `git diff ccd6a54 dca80cf5 -- corpus/SOURCES.md` removed/added lines | 0 removed, 4 added (S109 row, two leads, registry note) |
| knowledge = 90 (base 89) | `git ls-tree -r --name-only {ccd6a54,dca80cf5} corpus/knowledge \| grep -c '\.md$'` | 89 → 90 |
| knowledge-expected 92 lines / 90 rows, sort-clean | `git show dca80cf5:…knowledge-expected.txt \| wc -l`; non-comment rows; `LC_ALL=C sort -c` | 92 / 90 / clean |
| capture sha256 `c9a7adfb…d486`, 375 lines | `git show dca80cf5:corpus/source-snapshots/round-74/S109.txt \| sha256sum` / `wc -l` | `c9a7adfb…d486` / 375 |
| manifest pins ≥10 quotes for S109, each ≤25 words, each located at its anchor | python over the committed manifest + capture | 16 quotes; max 22 words; 0 unanchored; **0 anchor mismatches** (each quote's 40-char prefix found at its pinned capture line) |
| entry exists, provenance trio, cd-prefixed recheck citing S109 | `git show dca80cf5:corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md \| head -8` | `source: S109 …`, `verified-at: 2026-11-05`, `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py …` |
| F52 admitted (51 → 52) | `git show dca80cf5:corpus/README.md \| grep -n F52`; `git show dca80cf5:PROVINCE.md \| grep -n F52` | `## Round-74 admission` block with F52 row (R6 end-append, map not edited in place); PROVINCE r74 line with the full scope limit |
| census exit 0 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (my run) | `kasegi ok`, exit 0, six inherited W04 warnings |

Lane-frontier instruments (`frontier-recheck-count.py`, `capture-binding-check.py`, `source-recheck.py`) not executed; their committed receipts (`c2-base-counters-r74.txt` base values; after-values in the report and lesson) are consistent with every value I re-measured. The two clauses the lane itself flagged as lacking frozen commands (registry-unchanged, quote word-count/anchor) were measured by me above and hold. Axis `improved` (net new admitted ground; score nominal 8 → 8, denominator operator-owned).

### Axis harm

`git diff ccd6a54 dca80cf5 -- SCORECARD.md` → 0 deleted lines; additions only (Round 74 section, move log, planned). `depth:density` untouched ("not re-measured", 9 held); `calibration` move-log row records R119/R120 without a score change; saturation line unchanged. No owned axis harmed.

## 3. Spot-check (LEARNING.md — non-author, ≥1 admit and ≥1 reject)

| item | decision under review | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S109 = Fuzzilli README, `https://github.com/googleprojectzero/fuzzilli` | ADMIT (F52, one knowledge entry) | live fetch `https://raw.githubusercontent.com/googleprojectzero/fuzzilli/master/README.md` → HTTP 200 | **agree** | the 22-word Gate quote is present verbatim at README line 3 — "A (coverage-)guided fuzzer for dynamic language interpreters based on a custom intermediate language (\"FuzzIL\") which can be mutated and translated to JavaScript." — including the printed `(coverage-)guided` parenthetical the lane was careful to preserve; tier A (maintainer's own statement) scoped to the README is correct; distinctness from S093/S092/S094 holds; the recorded lead-URL correction reproduces (`https://github.com/google/fuzzilli` → 404, probed live) |
| OSV.dev overview page, `https://google.github.io/osv.dev/api/` | REJECT as a row (kept lead-only) | live fetch → HTTP 200 | **agree** | the page is real and carries both lead statements ("Currently there are no limits on the API"; response-size limit 32 MiB on HTTP/1.1), but the reject reason is CORPUS rule 1: a row requires the source captured in the round that writes it, and this round opened it lead-only with no capture/manifest. Lead + flip condition is the contract-conformant disposition; the facts are not lost |
| S109 registry row quote (≤25 words, located) | row discipline check | capture line 151 vs live README line 3; `wc -w` = 22 | **agree** | quote is 22 words, located (capture `S109.txt:151`, pinned in the manifest and re-verified against the live source), and matches the row's `teaches` wording including the printed parenthetical |

## 4. Trend verdicts (this verifier, with evidence)

- **expansion: improved** — one net new admitted knowledge entry on ground the coverage map did not hold (`corpus/README.md` `## Round-74 admission`; `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`, source S109, re-measured above: knowledge 89 → 90, registry 108 → 109, F52 row appended per R6).
- **quality: unchanged** — no admitted entry superseded or re-verified against a changed source; none found false. R33 id collision open (2 rows at base and tip, measured) and recorded, not repaired (M74-3, R120) — recorded-not-repaired is the QUALITY-supersession rule applied, not a decay.
- **discernment: improved** — the r73 spot-check disagreement became lesson M74-1 and grounded criterion R119; this round's Gate carries located reject lines with reasons; this verifier independently agrees with the sampled admit (S109/F52) and reject (OSV overview lead-only) — the first non-author agreement on r74's own gate decisions, recorded here.

## 5. Routed defects (for round 75)

- **V74-1 (this verifier): census-evidence timing.** Re-run and commit the census receipt at the actual tip revision (expect `entries=90`, `exit0_foreign=68` with the new entry counted); append an erratum to the report's landed-state line and the lesson's § Counters line; add a freeze-note lesson: a shape clause binding `entries == file count` is falsifiable by any later admission — freeze it against the measurement revision only, or name the drift expectation. (Class: M74-2.)
- **M74-6 (lane-routed, confirmed)**: C1 scope sentence falsified at file level for `restoration-recheck:`-only files; counter amendment with its own freeze.
- **M74-7 (lane-routed, confirmed)**: sibling-distinctness sentence overbroad (revenger holds DecFuzzer S117 and mishegos S396 README documentation); narrow before the next freeze.
- **M74-3 (lane-routed, confirmed by measurement)**: R33 held twice (`corpus/QUALITY.md` at base and tip); renumber by document.
- **C2 clause weaknesses (lane-routed, confirmed)**: the registry-unchanged and quote word-count/anchor clauses had no frozen measuring commands; this verifier measured both and they hold — name them as commands before the next C2-type freeze.
- **RC-8 (operator, open)**: `bash -c` recheck surface unchanged this round (kill rule (d) receipt + sentinel count); still awaiting the operator decision.

Operator note (promotion is operator-owned; no `[x]` written here): the four SHONEN boxes look fully checkable by a non-author — box 1 on `SKILL.md`'s standing tables plus the new sourced entry, box 2 on the LOG'd end-to-end trial package (documentation-only, `claimable: false`, operator-gated), box 3 on the receipt-backed executable counters, box 4 on the PROVINCE r74 scope line plus `ConnectorSweep` §2.

Closure entry values this file supports: lanes.kasegi = `ok`, admitted = true, verdicts {depth:verifiability: improved, coverage: improved, depth:density: unchanged, calibration: unchanged}, trends {expansion: improved, quality: unchanged, discernment: improved}.
