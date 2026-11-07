author: hyaku closure (non-author integrator, @m_zfl)

# Round 99 — verifier spot-check (non-author closure judge)

Lane: kasegi. Report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-99/kasegi.md`.
Lane HEAD before the round: `b9411a6b530e486180cf14c72fccc46668dcf5ee`; after:
`6f4858a89764ef29263c3abe4387873ed583f806` (branch `refs/heads/master`, remote equal).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-07T19:04:18-03:00 launch kasegi round=99 pgid=2566269 driver=hyaku-inline attempt=1`;
`2026-11-07T19:48:31-03:00 complete kasegi round=99; hyaku-inline attempt=1`.

Method: the lane's `census-at-rev.py`, `tamper.py`, `session-cookie-probe.py` and
`capture-secret-scan.py --selftest` are lane-owned instruments/counters. Per PROTOCOL §Gate
standard (Closure consequence) I verified their **committed evidence** — receipts, limb tallies,
frozen pins, the revision printed — and did **not** execute them. Every claim's substance was
additionally re-derived over committed bytes with plain commands I ran myself (`git show`,
`git cat-file`, `git merge-base`, `sha256sum`, `grep`/`awk`/`wc`, `curl`, and static Python
parsing of the instrument's selftest tables; the independent regex application in §2 is my own
measurement, not the lane's gate). No seat was dispatched; this file is the non-author record.

## 1. Conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-99/kasegi.md` (fleet repo) | `kasegi-shokunin <kasegi@shokunin.local> 4b117bd3c64de3b284da215f0bc0a6c73f658249 round-99: kasegi report` | PASS |
| Report lands after the lane work | committer times | lane tip `6f4858a8` committer `19:47:31`; report `4b117bd3` committer `19:48:02`; driver complete `19:48:31` | PASS (report author date `19:44:28` precedes the tip — the recurring jj change-creation-time artifact, status-neutral) |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` = 1; `grep -c '^- \['` in `SHONEN.md` = 4; report `^- \`\[` = 4 | four `[~]` lines with resolvable pointers (`corpus/lessons/round-47-verifier-spotcheck.md:94`, `corpus/practice/curl-h1-1913733/report.md`, `corpus/practice/curl-ibb-h1-1997312/report.md`, `PROVINCE.md`); all four paths exist | PASS |
| Cited commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `b9411a6b`, `6195db30`, `7f890046`, `a3db47e7`, `35e3ab60`, `29cd3058`, `bedb6c47`, `2c2124f2`, `e7d70757`, `01f4f59f`, `44897114`, `c264526a`, `3746f64e`, `5015113f`, `6f4858a8`, `e2d3de7b`, `e2caf4a1` | all 17 exist; all 17 `ancestor`; `jj-lane.sh state` = `branch=master local=6f4858a8 remote=6f4858a8 ahead=0 behind=0 head=detached tracked=0 untracked=0` | PASS |
| No uncommitted round work; pushed | `jj-lane.sh state`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | porcelain empty; remote `6f4858a8` | PASS |
| Prompt carries the template contract | `.ufo/prompts/kasegi-round-99.md` vs `templates/round-prompt.md` | the prompt prefix (140 lines) is byte-identical to the rendered template (LANE=kasegi, ROUND=99, AXES="depth + coverage (bounty and security research)", FLEET_ROOT=/home/vgpnk/Projects/shokunin) except line 1, where the prompt carries the real cwd `kasegi-shokunin` and the template's `{{LANE}}-repo` placeholder renders `<kasegi-repo>`; five child-lane items present (report path/filename, commit-then-report ordering, `SHONEN` heading, commit-hash citation, lane write scope); L2 floor "at least 8"; the hyaku §6 addendum follows | PASS (template defect below: the working-dir placeholder is malformed; the prompt corrects it) |
| Real report vs marker | report sections in order | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Round shape, Wave findings, Stale-lane, Tool installs, Open L0 questions; hashes and measurements present | PASS (not a marker) |
| Wave shape | `.ufo/waves/round-99/w1-dispatch.json`, `w1-results.json`, `w1.ready` | 13 seats / 13 results, all with non-empty outputs; roles 3 critic, 2 reviewer, 2 mutation-tester, 1 sentinel, 2 executor, 1 scout, 1 connector, 1 scribe; `counts.spawn=13`; band 8–16; no `model` key in spec or dispatch | PASS (no planner seat: the L1 holds it per the fleet-wide 2026-10-19 ruling and the round-97/98 precedent, disclosed in the report) |
| Source census | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok` rc 0; 151 rows; the seven inherited W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085, S143) | PASS |
| Registry delta | `git show b9411a6b:corpus/SOURCES.md \| grep -cE '^ {0,3}\| S[0-9]{3} \|'`; same at the tip | 149 → 151; frozen manual census: malformed rows 0, duplicate ids 0, enum violations 0, mined used-by missing paths 0 | PASS |
| LOG ties | `grep -c <hash> LOG.md`; report Landed-changes "LOG entry" column vs the LOG's Round 99 bullets | the LOG entry has 8 bullets (Base/freeze, Freeze, C2 landing, C2 addendum, C1 landing, Sources, Integration, Mistakes); the report's bullet 2/3/4/5/6–7 pointers resolve; the `5015113f` row cites "bullet 8 (Wave evidence)" while bullet 8 is "Mistakes" and no wave-evidence bullet exists | **DEFECT** (low; routed) |
| Count consistency | `grep -n '53 synthetic\|7+11+17+18 = 53\|six mistakes\|nine mistakes' SCORECARD.md LOG.md corpus/QUALITY.md .ufo/reports/round-99/kasegi.md` | the redaction count is 57 (8+12+18+19 markers; 57 per-line digest rows), but SCORECARD's C2 row, LOG's C2-addendum bullet and M99-5, and QUALITY R160 still say 53 (R160 says `7+11+17+18 = 53`); the lesson carries ten mistakes (M99-1…M99-10) while LOG says "six mistakes M99-1…M99-6" and the report's trend verdict says "nine mistakes mined (M99-1…M99-9)" | **DEFECT** (medium; correction sweep incomplete; routed) |
| Report measurement precision | report Before→after vs the cited receipts | C1 "after" cites `35e3ab60` / `6d68d955` (the pre-R161 landing) while the final landing is `3746f64e` / `c06d95cd` (the re-run is in the Landed-changes receipt and `claims.json` `erratum_landing`); the report's 2.23 s / 512,980 kB is not in `c1-layout-memory-controls-r99.txt` (2.29 s / 512,064 kB); the layout control is at `b9411a6b` (162/732, 2569/7620, 2607/8022) while the report quotes the `a3db47e7` census's 2569/7624, 2607/8026; "confined 1" is not in `citation-survival.md:5-12` | **DEFECT** (medium; routed) |

The report is a real report. Conformance defects above are status-neutral; none prescribes `failed`.

## 2. Per-claim re-check

### C1 — `depth:verifiability` (lowest non-retired axis; score 4 held) → **VERIFIED on P1–P4; axis improved**

Re-measured by me (plain, over committed bytes):

- **P1 evidence-verified.** `c1-tamper-base-r99.txt` prints `TAMPER-RESULT killed=5 total=12
  evaluated=12 instrument_sha256=66383371… rc=0` with exactly seven survivors (T05 body-edited,
  T06 host-line-removed, T07 host-line-edited, T08 body-from-other-rev, T09 poisoned-cache, T11
  host-owned-edited, T12 body-truncated); `c1-tamper-candidate-r99.txt` prints `killed=12 total=12
  … instrument_sha256=6d68d955…`; `c1-landing-r99.txt` re-runs the landing instrument
  `c06d95cd…` at 12/12 and the round-98 instrument at 5/12. `git show <rev>:corpus/instruments/census-at-rev.py | sha256sum`
  reproduces every pin: `e2d3de7b` → `66383371…`, `35e3ab60` → `6d68d955…`, `3746f64e`/HEAD → `c06d95cd…`.
- **P2 evidence-verified.** `c1-layout-memory-controls-r99.txt` prints `CENSUS-CHECK pass
  rev=b9411a6b… skill=162/732 corpus=2569/7620 lane=2607/8022 host_owned=76 confined=1` twice
  (clean and dirty parent), rc 0 both. The triple is identical; the report quotes the `a3db47e7`
  census's 2569/7624, 2607/8026 instead (defect above).
- **P3 re-measured.** `grep -c '^measured-at: a3db47e7…$'` = 1; `git merge-base --is-ancestor
  a3db47e7 refs/heads/master` holds; `grep -c 'fast/scratch'` = 0; `grep -c 'tree-a3db47e71fe2'` = 0;
  one `Lane root:` line.
- **P4 evidence-verified.** The control receipt's `/usr/bin/time -v` prints `0:02.29` and
  `512064` kB (the report's 2.23 s / 512,980 kB is a seat's earlier run, not the receipt); under
  the frozen 60 s / 1 GiB bound.
- **Digest binding re-measured.** Over the committed `corpus/instruments/citation-survival.md`:
  `sha256("\n".join(lines[5-10]))` = `ddad8766…` = the file's `header-sha256`;
  `sha256(body after "\n---\n\n")` = `680a3534…` = the file's `body-sha256`. The class table sums
  76 + 0 + 2608 + 5342 = 8026; the pinned numerator 2607 = 2608 INTERNAL − 1 confined.
- **Record defect (new).** The header's `host-inclusive rate (resolve.py's definition, confined
  HOME)` line reads corpus 2645/7624, lane 2683/8026, while the body's `## Resolvability rate`
  (resolve.py's own section) reads 2646/7624, 2684/8026 — off by exactly the one reclassified
  HOST-OWNED row, which the instrument's `host_incl` excludes. The label names resolve.py's
  definition but computes the instrument's. `confined 1` appears only in the `CENSUS-CHECK`
  output, not in the file, so a reader cannot reconcile the body's INTERNAL 2608 with the header's
  2607 from the record alone. The pinned rate itself is unaffected.

**Axis verdict: `improved`.** The tamper-evidence (5/12 → 12/12), layout-stability (identical
triple in clean and dirty work dirs) and runnability (2.29 s / 512 MB instead of an earlyoom kill)
are real and evidence-verified; the record's reconciliation defect is routed, not a re-score.

### C2 — `coverage` (score 8 held), capability extension `capture-secret-scan` → **claim VERIFIED on K1–K6; axis HARMED**

Re-measured by me:

- **K1 re-measured statically.** `ast` parse of `selftest()`: `cases` 181 + `paths` 8 + `checks` 3
  = 192 at the landing; `git show e2caf4a1:` gives 159 + 8 + 3 = 170. `sha256sum` of the landing
  blob = `8b338726…` = the pin.
- **K2 re-measured independently.** My own regex application (the committed `_GL_LB` + the landed
  `gitlab-session-cookie` body) to the probe's 12 MUST-FIX payloads and 10 negatives prints
  `mustfix=12/12 negatives_extra=0`; the round-98 body (`[\s"'=:;]+`) prints `mustfix=0/12
  negatives_extra=2` (`n-gap-9`, `n-gap-newline`). The committed probe receipts agree exactly.
- **K3 evidence-verified.** `c2-probe-base-r99.txt`: `mustfix_hit=0/12 negatives_extra=2
  instrument_sha256=45f8d226…`; `git show e2caf4a1:corpus/instruments/capture-secret-scan.py |
  sha256sum` = `45f8d226…`.
- **K4 evidence-verified.** `c2-landing-r99.txt`: pre-redaction `hits=4 files=4` at `7f890046`
  (kept), post-redaction `hits=0 files=0 allowed=27 unused_allow=0 rc=0` at `a3db47e7`.
- **K5 re-measured.** One `| capture-secret-scan |` row; it names `gitlab-session-cookie` and the
  separator window; cell 5 = `87`.
- **K6 re-measured.** The knowledge entry states the window (`:21-22`, `:78-79`) and cites S140
  (`:3`), S148 (`:38`, `:52`), S150 (`:3`, `:38`).

**Axis harm.** The landing replaced round-98's `[\s"'=:;]+` with `[^\n]{0,8}[:=][^\n]{0,8}`
instead of their union. The wave's own matrix (`w1/SentinelCookie-receipts/delta.txt`) records
`NEW-HIT-VS-R98=39` and `LOST-HIT-VS-R98=23`; the 23 lost cells include the tab- and
space-separated Netscape cookie jar (`ctx-cookie-jar-tab`, `ctx-cookie-jar-space`), which the
round-98 instrument hit and the landing does not — the one high-realism loss in the sentinel's
table (a normal curl/browser capture artifact under `corpus/practice/*/evidence/`). The wave also
measured a bounded union (candidate B: `mustfix=12/12`, `negatives=0/10`, jar recovered) and
routed it to round 100; the landing chose the strict S140 window and deferred the fix. The
round-98 remediation text had already named both options and the loss the second one causes.
`CriticClaimsC2` §6 adds over-detection the frozen negatives cannot see (65- and 72-hex runs now
match; a following cookie is over-attributed). The report discloses all of this as a "measured
qualifier"; it is a coverage regression, and PROTOCOL's admission rule is "a trade anywhere is
not an improvement".

**Axis verdict: `harmed`.** The 12/12 gain is real and independently reproduced; the 23-class
loss (jar among them) with a measured union available is a regression in what the capability
governs. The round is not admitted on this axis.

### Guard — `depth:density` → **unchanged**

`git diff --stat b9411a6b 6f4858a8 -- SKILL.md` is empty; `python3 corpus/instruments/density.py
SKILL.md --label r99` prints **273.2** and the base blob prints **273.2** (932 path-citation
instances, 38 blocks, both).

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S151 — GitLab secret-detection-rules, `pkg/rules/assignment_regex.go` at 59ada1f4 | **ADMIT** (`code`, tier A, `mined`) | live `https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/pkg%2Frules%2Fassignment_regex.go/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39` (HTTP **200**, 9,776 bytes, sha256 `91519731800ab8d96a00a03fff44e72c1c16a3bad12c9e017d7d679a8fad756d`) | **agree** | the file is byte-identical to the row's anchor (size and sha256 exact); lines 27-29 carry the three quotes the lesson records (`assignmentOperand specifies …`, `assignmentOperand = [="' :>\],\t.()\\?|]{1,10}`, `terminalRegex = …`), each under 25 words; tier A for the pinned commit's own delimiter class is correct, and the row's `supersedes S150 — form` framing is accurate. |
| S150 — GitLab secret-detection-rules merge request !151 | **ADMIT** (`code`, tier B, `mined`) | live `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/merge_requests/151` (HTTP **200**, 128,124 bytes, sha256 `e857d062…`) | **agree, with the row's own caveat** | the page carries the exact "Generated Regex:" block (`(?:API_SECRET_KEY\|…).{0,8}[:=].{0,8}([a-z]{32})\b`) and the `keywordGroupType` sentence the lesson quotes; the recorded 128,120 bytes / `aa60d7af…` did not reproduce (128,124 / `e857d062…`), which is the round's own F2 finding (the MR HTML is nonce-bound) and the reason S151 is the byte-stable authority. The admit is sound; the anchor should eventually name a stable section rather than a digest. |
| A new row for the round-98 sentinel's MR quote | **REJECT** (duplicate of S150; no row) | `.ufo/waves/round-98/w1/SentinelShapes-receipts/assignment-context.txt` | **agree** | the receipt records the same MR !151 and the same "Generated Regex:" block, with no URL; a second row for the same page would duplicate S150, and the receipt is correctly cited as the discovery pointer instead. |

## 4. Trend verdicts

- **expansion: improved** — registry 149 → 151 (S150 tier B `mined`, S151 tier A `mined`; the
  frozen census checks print 0 malformed / 0 duplicate / 0 enum violations / 0 missing used-by);
  the knowledge entry gains the assignment-context window and the two-form statement on ground
  the coverage map did not hold; the `capture-secret-scan` capability row is extended. Evidence:
  the row-count command, the census `kasegi ok` rc 0, the S150/S151 re-opens.
- **quality: improved, with the C2 regression counted under coverage** — the census check's
  discrimination rises 5/12 → 12/12, the census is layout-stable and runnable (2.29 s / 512 MB),
  the scanner's selftest grows 170 → 192, and the knowledge entry's false "S140's class" clause is
  corrected by a named erratum rather than smoothed over. Defects routed: the record's
  header/body reconciliation, the redaction accounting (53 vs 57; single-line after-digests), and
  the stale counts below.
- **discernment: improved** — ten mistakes mined (M99-1…M99-10; the report's "nine" is stale),
  the wave falsified the C2 statement's clause and the round reported it, and the round-98
  spot-check's routed defects 1–5, 7–9 are closed or answered (defect 6 is not — see below). My
  spot-check agrees on both admits and the reject.

## 5. Routed defects for round 100

1. **C2 coverage regression (high).** The strict S140 window loses 23 detection classes the
   round-98 instrument hit, including the Netscape cookie jar (tab and space). Land the measured
   bounded union (candidate B: 12/12, 0/10, jar recovered) or record the loss in the capability
   row and `QUALITY.md`; the current row overstates what the scanner governs.
2. **Census header/body reconciliation (medium).** `citation-survival.md`'s header says
   `host-inclusive rate (resolve.py's definition …)` corpus 2645/7624, lane 2683/8026, while the
   body's `## Resolvability rate` says 2646/7624, 2684/8026; the one reclassified HOST-OWNED row
   is excluded from the instrument's `host_incl` but counted by resolve.py. Name the instrument's
   definition in the label or include the row, and state `confined 1` in the file so the pinned
   numerator reconciles with the body's INTERNAL 2608.
3. **Correction sweep (medium).** 53 → 57 is corrected in the lesson and the report but stale in
   `SCORECARD.md` (C2 row), `LOG.md` (C2-addendum bullet and M99-5) and `corpus/QUALITY.md` R160
   (`7+11+17+18 = 53`); the mistake count is stale in `LOG.md` ("six mistakes M99-1…M99-6") and
   the report's discernment verdict ("nine mistakes"). PROTOCOL §Evidence standard: corrections
   sweep every mention.
4. **Redaction control provenance (medium).** `controls/redaction-r99.txt`'s four `after=`
   digests are the single-line-redacted states, not the landed files (CriticClaimsC2 §7), and the
   redaction mutated the `%20` separator on four lines; record the landed file digests or say
   what the `after=` value describes, and restore the separator bytes.
5. **End-to-end regression receipt (medium).** The report's "round-98 hits=1" end-to-end claim
   cites `SentinelCookie-receipts/cli-checks.txt`, where both r98 CLI runs print
   `CAPTURE-SECRET-SCAN error reason=FileNotFoundError rc=2`; the matrix (`matrix-run.txt`,
   `delta.txt`) is the real regression evidence. Fix the citation or re-run the r98 CLI with
   `claim-package-check.py` staged.
6. **Probe provenance (low).** `session-cookie-probe.py`'s docstring says the payloads are
   "verbatim from final-checks.txt lines 15-26"; at the landing those lines carry
   `[session-cookie-fixture-redacted-r99]`. Cite `a3db47e7^:…final-checks.txt:15-26` (the
   payloads are byte-identical there) or note the redaction.
7. **LOG bullet pointer (low).** The report's `5015113f` row cites "Round 99 bullet 8 (Wave
   evidence)"; the LOG's bullet 8 is "Mistakes" and the entry has no wave-evidence bullet.
8. **Routed defect 6 from round 98 (low).** The lesson says it is "closed by the appended LOG
   correction"; no such correction exists — the round-98 report's bullet pointers are unchanged.
   Append the correction or reopen the row.
9. **Report measurement precision (low).** The C1 "after" cites `35e3ab60` / `6d68d955` (pre-R161)
   while the final landing is `3746f64e` / `c06d95cd`; the 2.23 s / 512,980 kB is not in the
   layout receipt (2.29 s / 512,064 kB); the layout control is at `b9411a6b` (2569/7620,
   2607/8022), not the `a3db47e7` census's 2569/7624, 2607/8026; "confined 1" is not in
   `citation-survival.md:5-12`.
10. **Template defect (operator-side, low).** `templates/round-prompt.md` line 1 renders
    `{{FLEET_ROOT}}/<{{LANE}}-repo>` → `<kasegi-repo>`; the dispatched prompt corrected it to
    `kasegi-shokunin`. The placeholder should be `{{LANE}}-shokunin`.

None of these re-scores C1: P1–P4 verify and the record's reconciliation defect is routed. C2
verifies on K1–K6, but the landing harms the coverage axis (23 lost detection classes, the jar
among them, with a measured union deferred), so the round is a **rejected harm**, not an
admission.
