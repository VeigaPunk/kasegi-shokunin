# kasegi round 39 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure of lane-round kasegi 39. The judge did not author the round, dispatched no lane work, ran no
lane-owned gate or instrument, and edited no lane-authored file. Inputs: report
`.ufo/reports/round-39/kasegi.md` (fleet repo), prompt `.ufo/prompts/kasegi-round-39.md`, lane base
B = `480b1a505a2dfc14a4f718d16d63808247214d0a`, judged head J = `ee5ae5e1739527f4cdb50babe2d694005607b44e`
(the receipt's `export-ref`), lane tip Y = `8371e7ac9f32cae5ed72f8c28205634603f836fa`
(`git diff --name-only J Y` → `.ufo/waves/round-39/final-gates/all-gates.txt` only). Frozen claims:
`.ufo/waves/round-39/claims.json` at Y, sha256 `e427ab6a6ecec4b1f49ed5eed95860c468e0982af331a3a1ba135649d27e051c`,
last touched by the freeze commit `dcd31701`; erratum `claims-erratum-1.md` (E1/E2/E4/E5).

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 1549/1562/1563/1566 at read time):

```
2026-10-26T16:23:01-03:00 launch kasegi round=39 pgid=3965921 driver=hyaku-inline attempt=1
2026-10-26T17:41:35-03:00 lane-dead-no-report kasegi round=39; retry same round (hyaku-inline attempt=1: L1 force-stopped at soft request budget (305/200) before report; lane tip 5006097 receipt Y; wave2 falsify settled (results json present, 37 seats); resume: integrate wave2 findings, final gates, report)
2026-10-26T17:41:38-03:00 launch kasegi round=39 pgid=452103 driver=hyaku-inline attempt=2
2026-10-26T17:58:04-03:00 complete kasegi round=39; hyaku-inline attempt=2
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane, last | `git log --format='%an %H a=%aI c=%cI' -- .ufo/reports/round-39/kasegi.md` | one commit, `kasegi-shokunin 3af1bd1cfdcaa8e092cfc51a7bbecb1a3cde8248`, committed 17:57:30-03:00: after lane tip Y (17:55:17) and before `complete` (17:58:04); prompt commits `edaa4fd1` (16:22:12, attempt 1) and `880117bf` (17:36:34, attempt 2) by the same identity, each before its `launch` | conformant |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` on the report; `- [` lines under it | `1`; four `[~]` lines for the four boxes; no `[x]` | conformant |
| Cited lane commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` for every hash in the report: `480b1a50`, `dcd31701`, `06632fa8`, `57ea9ea5`, `1a139e0f`, `46c66c26`, `5006097a`, `3fa81ef5`, `752e476d`, `ee5ae5e1`, `8371e7ac` | all resolve; all ancestors (exit 0); `B..Y` = 12 commits, all `kasegi-shokunin` | conformant |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state kasegi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=8371e7ac… remote=8371e7ac… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `8371e7ac…` | conformant |
| Prompt carries the template contract | read `.ufo/prompts/kasegi-round-39.md` (624 lines) | §1 MISSION/AXES binding (L3-L7), 1–3 claims incl. lowest axis (L9-L27), §2b frontier step (L42-L74), §3 L2 floor one batched call (L80-L82), §4 report path + SHONEN + hash rule + marker rule (L99-L129), §5 commit/push scope/L0 (L131-L140), §6 hyaku addendum (L141) | conformant |
| L2 route map vs `MISSION.md` | same rendering as round 38 | the prompt quotes the operator's model routing, not a MISSION bucket table | no defect |
| Report is not a marker | report names claims, commits, commands | real committed work: 12 round commits B..Y, 339 files, 42,542 insertions, 0 deletions | status `ok` |
| Wave records | `jq '.taskCall.tasks\|length' wave{1,2}-dispatch.json`; result-entry counts | 49 = 49 (build), 37 = 37 (falsify); 86 total; results committed at `3fa81ef5` (17:48:26), before `complete` | conformant |
| Receipt timestamp ≤ containing commit | `run-utc` of `final-gates/all-gates.txt` at Y vs `git log -1 --format=%cI 8371e7a` | `2026-10-26T20:54:44Z` ≤ `2026-10-26T20:55:17Z` | conformant (at Y) |

Defects recorded (status-neutral; routed in §5): the superseded attempt-1 receipt at `5006097a` was
future-dated and claimed a run no transcript shows (R1); round-39 records still state C1 8/8 at Y (R2);
the report's base/r38 control values disagree with the committed `reds.txt` (R3); an attempt-1 scratch
directory survives at filing (R4); no `## Mistakes` row or criterion for the round's own evidence miss
(R1) and M39-2 has `captured-by: none` with no criterion (R5).

## 2. Claims — re-checked at J/Y

### C1 — depth:verifiability (held 4): NOT VERIFIED (frozen kill rule fires; evidence-verified)

Frozen predicate (claims.json at Y): `r39-closure.sh --export-ref J` prints `closed=8/8 exit=0` and
`--selftest --export-ref J` prints `selftest cases=8 failures=0`. Kill rule: "the judged-head export prints
closed != 8/8 or exit != 0; --selftest prints … any failure". Erratum E4 moves the verification ref to
Y = J + receipt. I did not run `r39-closure.sh` (a lane gate; PROTOCOL §Gate standard, Closure
consequence). Committed evidence read at Y:

- `.ufo/waves/round-39/final-gates/all-gates.txt` (`all-gates v5`, sha256 `8d46d7b2…`): `export-ref=ee5ae5e1…`
  (= J), `suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`, equal to
  `git show Y:corpus/instruments/r39-closure.sh | sha256sum` and to the SKILL.md registry row (`SKILL.md:1115`).
  Run: `G2 payload=…diff-clean=0… closed=0`, the other seven `closed=1`, `closed=7/8 exit=1`, `run-exit=1`.
  Selftest: `selftest case=G2 positive=fail mutants=8/8 verdict=fail`, the other seven `verdict=pass`,
  `selftest cases=8 failures=1`, `selftest-exit=1`. The kill rule fires at J.
- The report's Y run (`closed=7/8`, selftest `failures=1`) is labelled report-only and has no committed
  transcript; it does not change the verdict.
- `final-gates/reds.txt` (committed at `3fa81ef5`): base `closed=1/8 exit=1`, r38 judged head
  `closed=1/8 exit=1`; the "base/r38 head prints 8/8" kill clause does not fire.
- Wave-2 attack receipts `wave2/CritG2Exploit.md` (G2 accepts forged payload values) and
  `wave2/CritC1Kill.md` (G6 depends on a quiet scratch root) are cited by the lane; I read them as the lane's
  own disclosure and did not re-run them.
- Plain re-derivation of the round-38 routed defects the suite targets (committed bytes at Y, no lane gate):
  `grep -c '^Correction (round 39)'` → round-38 lesson 1, `LOG.md` 2, `SCORECARD.md` 3, `SHONEN.md` 2 (R2
  swept); `QUALITY.md` R34/R35/R36 present, citing M39-1 (2 hits), M39-3 (2), M39-4 (1); `grep -cE
  'M38-5|M38-7' corpus/QUALITY.md` → 1 (R4); `grep -c '⟨pending' corpus/lessons/round-39.md` → 0. The
  corrections are real and append-only, but the claim is the frozen predicate, and it fails at J.

The report grades C1 "harmed/unprovable". The claim is a failed measurable claim, not an exploratory one,
so it is simply not verified; it does not move the axis down (see §2 harm check).

### C2 — coverage (held 7): VERIFIED (re-measured + evidence-verified)

Re-measured over committed bytes with `git show <rev>:<path>` / `git ls-tree` / `git grep`:

| Measure | B | freeze `dcd31701` | J | Y | Reported |
|---|---|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 21 | 21 | 22 | 22 | 21 → 22 |
| admitted frontier rows (`awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/'`) | 21 | 21 | 22 | 22 | 22/22 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 55 | 55 | 59 | 59 | 55 → 59 |
| `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'` | 50 | 50 | 51 | 51 | 50 → 51 |
| `git grep -lE '^source: S057' <rev> -- corpus/knowledge \| wc -l` | 0 | 0 | 1 | 1 | 0 → 1 |
| `corpus/instruments/knowledge-expected.txt` lines | 52 | 52 | 53 | 53 | expected 50 → 51 (audit) |

New rows S057/S056/S058/S059 at `corpus/SOURCES.md:62-65`, each `NF=13`; S057 `mined`, tier A; S056, S058,
S059 `rejected` with reason and flip. Capture: `git show Y:corpus/source-snapshots/round-39/S057.txt |
sha256sum` → `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`, `wc -lc` → 275 lines,
17,971 bytes (matches manifest `sha256`, `lines`, `snapshot_bytes`). Entry
`corpus/knowledge/cisa-when-to-issue-vex.md` carries `source: S057`; every curly-quoted span in it occurs
in the live PDF text (the zero-count spans are its "Rejected over-generalizations", which are meant to be
absent); its line anchors L2-L3, L79-L81, L117-L122, L183-L186 hold the cited text in the capture.

Census (fleet script, not a lane gate): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029` (the standing duplicate-URL warnings),
`ok`, exit 0, the same as the report's before and after.

Evidence-verified only (lane-owned instruments, not executed): harness `entries=25 pass=25 exit=0`, source
recheck S057 exit 0, binding `records=46 bound=46 unbound=0`, audit `expected=51 missing=0 unexpected=0
exit=0` — `corpus/lessons/round-39.md:94` and the wave-2 seats `RevC2Recheck.md` / `CritC2Kill.md`. Junk
control `.ufo/waves/round-39/c2-controls/junk-f22-recheck.txt`: 4× `MISMATCH reason=quote-not-found`,
`exit=1`. No C2 kill clause fires.

### Owned-axis harm check

`git diff 480b1a50 8371e7ac -- SCORECARD.md` → 54 added lines, 0 removed (the distance-to-next-score
section, a `Correction (round 39)` line, the `## Round 39 result` table and claims table; scores 4→4, 7→7,
9→9). `git diff --numstat B Y -- . ':!.ufo'` → every file `N/0` (SKILL.md 1/0, PROVINCE.md 2/0, README
28/0, SOURCES 10/0, QUALITY 17/0, ledger 28/0, round-38 lesson 2/0, LOG 17/0, SHONEN 16/0 + new files).
No deletion, no score drop. The round's new records overstate C1 (R2) but each carries an appended
correction in the same round, so they are marked, not left false and unmarked. No owned axis harmed.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | unchanged | C1 fails its frozen command at J (`closed=7/8 exit=1`, selftest `failures=1`, both committed); score held 4; the round-38 R1–R4 corrections re-derive closed by plain reads, but the claim as frozen does not verify |
| coverage | improved | frontier 21→22, registry 55→59 (S057 tier A mined; three rejects with flip), knowledge 50→51 on VEX-issuance ground absent at B; re-measured; S057 PDF re-opened live, byte-identical; score held 7 |
| depth:density | unchanged | `SKILL.md` append-only (1 registry row); no claim |

## 3. Discernment spot-check (`corpus/lessons/round-39.md` `## Gate`, at Y)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| F22 / S057 CISA, When to Issue VEX Information | admit | `curl -sS -L -A kasegi-shokunin/1.0 https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf` (2026-10-26T21:00:25Z) → `code=200 type=application/pdf bytes=235270`, sha256 `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99` | agree | the live PDF is byte-identical to the manifest's `raw_sha256`; `pdftotext -enc UTF-8` plus the manifest's collapse rule reproduces the committed `S057.txt` exactly (sha256 `11c8d6d6…`); manifest Q1–Q4 each occur once live and once in the capture; the document says it is guidance ("not determined by a strict protocol", capture L79-L81), and the entry scopes it as guidance; landing page `200`, 54,453 bytes (same size; its sha256 differs from the recorded one, as a dynamic HTML page can; the row's capture is the PDF) |
| S056 CISA, Minimum Requirements for VEX | reject | `curl -sS -L https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex` (21:00:49Z) → `200`, 49,253 bytes, sha256 `67bafe172cb7ba5cee8938235abce59ca2a0069d96c65fa1078dc42f05a8eab8` | agree | byte-identical to the fetch recorded in the row; its status/justification vocabulary is what S055 (CSAF VEX profile) already holds, so admitting it adds no uncovered ground this round; the flip (consumer-side minimum-elements phrasing) is the right trigger |
| S058 OpenVEX v0.2.0 | reject | `curl -sS -L https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md` → `200`, 30,580 bytes, sha256 `9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884` | agree | identical to the row's recorded digest; H1 L1 `# OpenVEX Specification v0.2.0`; the five not-affected labels at L373-L377 are the same as CISA/CSAF; the revisions table (L639-L647) ends 2023-07-18 with no v0.2.0 entry, and the URL is the mutable `main` ref — tier B and reject-with-pin-flip fit |
| `c2-controls/junk-f22.md` (four fabricated When-to-Issue claims) | reject | live PDF text above | agree | "mandates a strict protocol" 0, "must never be changed" 0, "exploitation-likelihood" 0 in the live text; `action_statement` appears only as an optional place for exploitation info (L146-L148: "such information could be included in the "action_statement" field"), and `vulnerable_code_not_in_execute_path` is absent, so claims 3–4 are false as the junk file says |

New `SOURCES.md` row re-opened: S057 (`corpus/SOURCES.md:62`, NF=13). The row's `anchor` cell gives
locations, not a quote; the `## Gate` quotes are ≤25 words (Q1 "Whether, and when, to issue VEX
information is a business decision…" 25 words, located `S057.txt:12-14`; Q2 "The decisions and timing
around providing VEX information are primarily business decisions and are not determined by a strict
protocol." 20 words, `:79-81`), and both occur live. Q3/Q4 in the Gate are described, not quoted; the
manifest's Q3 (42 words) and Q4 (34 words) are recheck assertions, not Gate quotes, so they do not breach
the ≤25-word rule. Gap: the three rejected rows S056/S058/S059 are new rows too, and the Gate records only
a reason and flip for each — no URL, access date, or ≤25-word quote (CORPUS.md item 1) (R6).

Census: as in §2 C2 — exit 0, `W04 S028`/`W04 S029` only.

## 4. Trend verdicts

- **expansion: improved** — one admitted entry (`cisa-when-to-issue-vex.md`) on VEX-issuance ground B did
  not hold (`grep` for `source: S057` 0 → 1), citing mined tier-A S057; F21→F22; re-measured above.
- **quality: unchanged** — the round-38 verifier's R1–R4 re-derive closed by plain reads and S057 re-opens
  byte-identical, but no admitted knowledge entry was re-verified or superseded, and the round's own records
  repeat the R2 defect class (C1 8/8 at Y in SCORECARD/LOG/SHONEN, §5 R2). Agrees with the lane's grade.
- **discernment: unchanged** — the spot-check agrees with the gate on the admit and on all three rejects
  sampled; but the round's main calibration miss — the attempt-1 receipt that recorded 8/8 with a
  future-dated `run-utc` while the L1's own check over the same tip printed 6/8 — is disclosed in
  `§Instrument attack findings` and not mined into `## Mistakes` with a criterion (§5 R1, R5). Agreement on
  gate decisions is offset by an unlearned evidence-calibration miss. Agrees with the lane's grade.

## 5. Routed defects (kasegi owes these next round)

- **R1 — attempt-1 receipt not mined.** `5006097a:.ufo/waves/round-39/final-gates/all-gates.txt` (`all-gates
  v3`) records `run-utc=2026-10-26T21:35:00Z`, after its containing commit (`2026-10-26T20:12:12Z`), and
  `G2 … diff-clean=1 … closed=1` / an 8/8 tally. The attempt-1 L1 scratch transcript
  `/fast/scratch/hyaku/kasegi-r39-l1/verify-Y.txt` (sha256 `98290ee6…`, mtime 17:12:25-03:00, uncommitted
  and not durable) shows the L1's own run over `5006097a` printing `closed=6/8 exit=1` and `selftest
  cases=8 failures=2`, and `make-receipt.sh` there prints no `run-utc` line, so the committed v3 header was
  not produced by that script's run. The report and lesson `:86` disclose the false timestamp and discard
  the receipt; add a `## Mistakes` row (class evidence-provenance, captured-by wave 2) with a grounded
  `QUALITY.md` criterion (e.g. a receipt is only ever the unedited tee of one observed run, and its
  `run-utc` is printed by the run itself).
- **R2 — round-39 records still state C1 8/8 at Y.** `SCORECARD.md:1567` ("`closed=8/8 exit=0` at Y,
  graded `selftest cases=8 failures=0`"), the `LOG.md` round-39 C1 bullet, `SHONEN.md` round-39 box 1
  ("graded cases=8 failures=0 at the verification ref") and `corpus/lessons/round-39.md:15` contradict the
  committed receipt at Y (`closed=7/8 exit=1`, `failures=1`). The appended corrections call the 8/8 "not
  independent proof" but do not name the final 7/8 / `failures=1` in SCORECARD and SHONEN. Append
  `Correction (round 40)` lines naming the final receipt values in each record.
- **R3 — report control values not in a transcript.** The report (`Before → after`, C1) says base and r38
  judged-head controls "each printed `closed=2/8 exit=1`"; the committed `final-gates/reds.txt` shows
  `closed=1/8 exit=1` for both. Correct the report value in the next report, or commit the 2/8 transcript.
- **R4 — scratch left at filing.** `/fast/scratch/hyaku/kasegi-r39-l1/` (17 files, 76K, newest mtime
  17:12:45-03:00) survives at closure (2026-10-26T21:0xZ); the frozen kill rule names "any leftover
  kasegi-r37/r38/r39 scratch entry at filing", and G6 looks only under `kasegi-r39/`, so it cannot see this
  sibling name. Remove it and widen G6 to the `kasegi-r39*` prefix.
- **R5 — M39-2 has `captured-by: none` and no criterion.** `grep -c M39-2 corpus/QUALITY.md` → 0, against the
  lane's own new R36. Add the criterion or state in the lesson why not.
- **R6 — Gate rows for the three rejects lack URL/date/quote.** `corpus/lessons/round-39.md:36-42` gives
  reason and flip for S056/S058/S059 but not the URL, access date and ≤25-word located quote CORPUS.md
  requires for every new row (the fetch data sit only in the row cells, from round-38 scout seats). Append
  them.
- **R7 — instrument findings (lane self-routed, carried).** G2 does not bind recorded payload values to a
  captured run (`wave2/CritG2Exploit.md` F2); G6 depends on scratch-root quiet (`wave2/CritC1Kill.md`);
  planned for round 40 (`SCORECARD.md` "Planned for round 40").

Promotion note for the operator: all four SHONEN boxes are `[~]`; box 2 (end-to-end domain task) is "no
end-to-end domain hunt ran", so the checklist is not fully checkable by a non-author from this round.
