# RevSpotCheckReadiness — round-36 non-author spot-check sample plan + Gate draft readiness

Seat: `RevSpotCheckReadiness` (reviewer, leaf — no subagents). Round: kasegi-shokunin round 36 (hyaku run 9),
lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Head at all measurements: `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`
(claims freeze); the wave is in flight, so landing state below is a snapshot of 2026-10-26 ~16:05Z
(G1's correction landed 15:43:27Z and is re-verified below).
Axes served: calibration (which decisions a fresh reviewer re-opens), depth:verifiability (exact commands,
expected outputs, verified digests). This seat formulates the plan and checks the draft Gate's block
readiness; it verifies no claim and issues no verdict — verdicts belong to the fresh non-author reviewer
at the final lane head. Writes: this receipt only; scratch `/fast/scratch/hyaku/kasegi-r36/RevSpotCheckReadiness/`
removed before yield. No tools installed (none needed; 2026-10-19 tooling authorization unused). Read-only
git only; no mutating git/jj; no lane/fleet/source-tree write.

Standing rule for every re-open below: measure on a `git archive` export of the final lane head — the head
the closure prompt and the report's Final-lane-commit line pin (E1 binds it) — never on the worktree and
never on receipts alone (M36-1 / M35-1 class). Exports go in the reviewer's own scratch dir.

## 1. Sample plan

Minimum sample per the item: one admit (F19 entry + S053 row), one reject (junk-f19; quarantine verdicts),
plus census and suite reruns. Three rejects are listed because the round's reject surface has two
independent kinds (control fixture; register verdicts) and the quarantine slice is the standing
non-claim item the Gate must carry.

### A1 — Admit re-open: F19 entry + S053 row (the round's single admission)

| # | step | command | expected |
|---|---|---|---|
| 1 | capture+manifest are in the export, not just the worktree | `git archive <final-lane-hash> corpus/source-snapshots/round-36/S053.txt corpus/source-snapshots/round-36/manifest.json \| tar -t` | both paths listed (r35's C2 died exactly here: capture uncommitted at the judged head) |
| 2 | re-hash the exported capture | `sha256sum` on the exported `S053.txt`; `wc -l -c` | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`, 8448 B / 244 lines; must equal the manifest `sha256` field **and** the entry header's digest (the entry draft's `b0a9` header-pin defect was caught by ExecC2QuoteOnce pre-yield and fixed — final entry bytes `36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641`, 17,374 B; see G1 for the residual grep trap) |
| 3 | pinned comparison | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` (from the export root) | `S053:sha256 OK` + `S053:Q1..Q4 OK occurrences=1 anchor=216/217/217/235-ok`, exit 0 |
| 4 | one live re-fetch + access date | `curl -sSL -A 'kasegi-shokunin/1.0' https://www.first.org/epss/` | HTTP 200, `text/html; charset=UTF-8`, 26,804 served bytes, no redirect, raw sha256 `66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868`, `last-modified: Thu, 30 Jul 2026 13:48:13 GMT`; access date = manifest `fetched_utc` `2026-10-26T15:35:10Z` (strict UTC); three independent fetches already byte-identical: 15:35:10Z (capture), 15:36:36Z (ScoutF19Open), 15:42:09Z (this seat, re-derived through the lane's own normalizer) |
| 5 | row shape | read the S053 row in the exported `corpus/SOURCES.md` | 11 cells, no `\|` inside a cell; `docs`, tier `A`, `mined`, `opened 2026-10-26`, `recheck 90d`, `used-by corpus/knowledge/epss-exploit-prediction-scoring.md`; anchor cites Q1 at L216 with the full sha; source cell carries exactly one `https://` token == manifest `url` |
| 6 | entry shape | read the exported entry | header `source: S053`, `ground: F19`, `verified-at: 2026-10-26`; `recheck:` is one `cd`-prefixed command naming `--source S053` with a `#` note; 11 blockquotes each ≤25 words with `— L<n>`; the four manifest pins byte-equal; `0–1` is U+2013 (a hyphen fails `grep -cF`) |
| 7 | distinctness limbs | token counts on the exported capture | `severity` 0 occurrences; `KEV` only as combine-with pointer (L224) and the VulnCheck partner name (L234) — never the CISA catalog S052; no calibration/threshold/accuracy figure (L220 is a pointer to another page) |
| 8 | harness | `python3 corpus/instruments/frontier-recheck-count.py` | `PASS F19 knowledge/epss-exploit-prediction-scoring.md ids=S053 exit=0` in the list; tail `entries=22 pass=22 exit=0`. This seat ran the before-state first-hand: `entries=21 pass=21 exit=0` (offline, 1.5 s) — the delta is exactly one PASS line |
| 9 | counters | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 19; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 53; `grep -rlE '^source: S053 ' corpus/knowledge \| wc -l` → 1; `ls corpus/knowledge/*.md \| wc -l` → 48 | all four hold on the export |

### A2 — Reject re-open: junk twin `c2-controls/junk-f19.md`

Resolved path: `.ufo/waves/round-36/c2-controls/junk-f19.md` (wave dir). No lane-root `c1-controls/` or
`c2-controls/` exists at HEAD; the committed precedent fixtures live at
`.ufo/waves/round-34/c2-controls/junk-f17.md`, `.ufo/waves/round-35/c2-controls/junk-f18.md`,
`.ufo/waves/round-34/c1-controls/fake-suite.sh` (verified via `git ls-tree -r HEAD`). The claim text's
bare `c2-controls/junk-f19.md` resolves to the wave dir; the spot-check should state this resolution.

| # | step | command | expected |
|---|---|---|---|
| 1 | fixture identity | `sha256sum` the landed fixture; `wc -c` | `ea078f05b0574f5584af1acfa7e8dd27636acee014339da9872591acf53cfc8b`, 1,889 B (ExecC2JunkControl §2 verbatim block) |
| 2 | discriminating grep | `grep -cF -- 'EPSS guarantees exploitation within 30 days for every scored CVE.'` over the exported `S053.txt` | `0`, grep exit 1 (this seat verified occ=0 on its own re-derived capture; the sentence is 10 words) |
| 3 | executable rejection (pinned comparison) | rebuild the twin's own assertion manifest from ExecC2JunkControl §3 (`junk-assertion.json`, sha `f947f9edc655844cc13bf51d1317dd29bc0a800d6a409a5b5a2fafe64fb265b4`) beside the exported capture; `python3 corpus/instruments/source-recheck.py --manifest <junk-assertion.json> --source S053` | `S053:J1 MISMATCH reason=quote-not-found`, exit 1 |
| 4 | discriminating pair | identical invocation with the real manifest (`f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3`) | 4 OK lines, exit 0 — the pair (step 3 fail / step 4 pass) is what makes the reject discriminating, not the fixture's own `recheck:` line |
| 5 | harness non-admission | `grep -c 'junk-f19' corpus/README.md` → 0; harness on the committed tree | no Frontier row names the fixture; `entries=22 pass=22 exit=0` (H1: the fixture is never evaluated). **Trap (H2, measured by ExecC2JunkControl): the harness is quote-blind** — a forged `F19` row + the real manifest admits the twin (`PASS F19 knowledge/junk-f19.md ids=S053`, `entries=22 pass=22`). Never present `entries=22 pass=22` as quote truth; the committed rejection = (i) no row naming the fixture + (ii) the pinned comparison |
| 6 | alternate twin (real quote, wrong source) | if the L1 landed it: `source-recheck --manifest <real> --source S052` → `S052:source UNAVAILABLE reason=not-listed` exit 2; the same quote pinned to S052's own capture → `quote-not-found` exit 1; forged `F20` row → `FAIL … problems=manifest-missing-ids`, harness exit 1 | all three readings fail. Fixture sha `ce41b8dd034bf92c77c8bc7965d2fea91fdbdec0fdcd32b14d0140fc74d33559` (scratch-only per the receipt — landing optional; the reviewer records what actually landed) |

### A3 — Reject re-open: quarantine slice verdicts (7 rows, adopted 0)

| # | step | command | expected |
|---|---|---|---|
| 1 | re-derive the slice | frozen awk over the read-only register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (sha `5afe1810a6c3…bad833`): `awk -F'\|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"` | 7 lines, 417 B, sha256 `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`; `cmp` equal to `.ufo/waves/round-35/assimilation/quarantine-slice`; 7/7 lines carry an S-id |
| 2 | one verified fetch per row | `curl -sS -L --max-time 30` with UA `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` (= `capture-source.py:32`), TLS verified, no `-k` | compare to ScoutQuarantine §2: S037 200/24,189 B `9cba2e96…` → **absent**; S054 200/513,648 B `0150c9d1…` → **absent**; S048 **404**/748 B `95cd25d8…` → **unreachable**; S065 curl 28 timeout, 677,543/7,465,472 B partial `23c73742…` → **unreachable (this probe)**; S068 301→301→200/94,027 B `098f99a8…` → **present-and-located**, already lane row S040; S069/S070 curl 60 (TLS verify), 0 B → **unreachable** |
| 3 | what the Gate must carry | read the Gate block | r36 labels verbatim; the S037/S054 label conflict kept visible (r36 scout `absent` vs r35 exec `prose-class-unverifiable`, bytes identical — one label, chosen by the L1, no silent switch from r35's); S065 movement is transport-only ("not a source defect and not a fabrication"); S069/S070 TLS-policy caveat (verified client fails; `-k` bytes exist but were not re-measured); **adopted 0**; the id screen (lane S037/S048 are different documents from the register's same-numbered ids) |
| 4 | judging the S065 label | — | a re-fetch with a larger cap may legitimately return present-and-located (rounds 33–35 did); the verdict is probe-contract-bound, so a flip confirms the caveat rather than refuting the round |

### A4 — Census rerun

- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
  → exit 0, exactly two `W04` lines (S028, S029), `kasegi ok …/kasegi-shokunin/corpus/SOURCES.md`.
  This seat ran it first-hand at the before-state: exit 0, W04 ×2, 52 rows — matching
  `.ufo/waves/round-36/census-before.txt` (3 lines) and ExecCensusReplay's two byte-identical runs.
- After-state expectation (S053 is the only row landing; quarantine adopted 0): same two W04 + ok;
  rows 53; tier `A=50 B=1 C=2`; status `mined=41 queued=9 rejected=3`; malformed 0; duplicate ids none;
  enum/tier-inflation none; dangling used-by none (the row and its entry must land in the same commit —
  ScribeRowS053 §6 — or census flags `dangling-usedby`).
- The seven frozen `CORPUS.md` census commands are the specification; before-state measured by
  ExecCensusReplay §3–§4 (52 / 0 / A=49 B=1 C=2 / mined=40 queued=9 rejected=3 / none / none / none,
  with cross-checks so none is vacuous).

### A5 — Suite rerun (C1; frozen `counting_commands`, runnable once the L1 lands the suite)

Status at check time: `corpus/instruments/r36-closure.sh` is **not yet in the tree** (ExecC1SuiteBuild in
flight) — the following are the frozen expectations, not this seat's measurements:

```
bash corpus/instruments/r36-closure.sh --export-ref <final-lane-hash>                        -> closed=9/9  exit=0
bash corpus/instruments/r36-closure.sh --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c -> closed=0/9  exit=1   # r35 base
bash corpus/instruments/r36-closure.sh --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988 -> closed<9/9 exit=1   # r35 judged head
bash corpus/instruments/r36-closure.sh --selftest                                            -> cases=9 failures=0 exit=0
grep -c 'filled by the L1' SCORECARD.md                                                      -> 0
```

The suite performs its own `git archive` export internally (`--export-ref`); run it from the lane root on
the committed instrument. The two negative controls are what make `closed=9/9` mean anything: the suite
must fail on the r35 base (nothing closed) and on the r35 judged head (partially closed), or it is not
discriminating.

### A6 — Harness + source-recheck + binding rerun (C2 counting commands)

```
python3 corpus/instruments/frontier-recheck-count.py                                                          -> entries=22 pass=22 exit=0, PASS F19 ids=S053
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053 -> exit 0
python3 corpus/instruments/capture-binding-check.py                                                           -> exit 0
ls corpus/knowledge/*.md | wc -l                                                                              -> 48
```

Before-state of the harness verified by this seat (`entries=21 pass=21 exit=0`); the S053 source-recheck
exit 0 was measured by ExecC2Capture §4 on the scratch manifest and must be re-run on the export.

## 2. Gate required-blocks checklist (draft readiness)

Contract sources: `templates/round-prompt.md` §2b — "the lesson's `## Gate` records the URL, access date,
and a ≤25-word located quote for every new row. Rejections stay as rows with reason and flip. Every
`status` / `recheck` / `used-by` change is logged old→new in the lesson"; the round-35 Gate structure
(`corpus/lessons/round-35.md:60-196`: Admitted / Admission history / Rejected / Quarantine slice /
Id-collision / Standing refusals / Assimilation / Contested scope); the ScribeGateLesson item text.
The draft lesson (`corpus/lessons/round-36.md`) does not exist yet; the Gate scribe confirmed the block
list and three dispositions by IRC (see §4).

| # | required block | feeding receipt (landed in `.ufo/waves/round-36/wave1/`) | status at check time |
|---|---|---|---|
| 1 | Admitted F19/S053 — **URL** (requested==effective, status, content-type, served→normalized bytes, sha256) | ExecC2Capture §1–§3: 200, `text/html; charset=UTF-8`, 26,804 → 8,448 B, sha `4ec61c59b0e9…`, no redirect | ready |
| 2 | Admitted — **access date** | manifest `fetched_utc` `2026-10-26T15:35:10Z`; independent re-fetches 15:36:36Z (ScoutF19Open) and 15:42:09Z (this seat) identical | ready |
| 3 | Admitted — **≤25-word located, exactly-once quote** | manifest Q1–Q4: 25/8/23/23 words, occ=1 each, L216/L217/L217/L235 (all four re-verified by this seat on an independent re-derivation, and re-run by ExecC2QuoteOnce on the corrected entry bytes); Q1 is the 25-word span starting `(EPSS)`; the 30-word full L216 sentence is recorded as the source sentence, **not** as a pin (scribe confirmed via IRC) | ready; entry draft carries 11 spans ≤25 words (ScribeEntryF19 V3: `spans 11 occ_all_1 True words_max 25 anchors_ok 11 of 11`); header-pin defect fixed pre-landing (G1) |
| 4 | Admitted — row cells + anchor | ScribeRowS053 §1.1 (11 cells, tier A, mined, opened 2026-10-26, 90d, used-by, Q1 L216 + full sha) | drafted, not yet applied |
| 5 | Admission history (refuse→repair→admit) | RevEntryF19 | **not landed** (in flight) |
| 6 | Rejected — junk-f19 with reason + flip + discriminating invocation | ExecC2JunkControl §2–§7 (quote-not-found exit 1 vs real-Q1 exit 0; no-row non-admission; H2 quote-blindness bound) | drafted (fixture content), not yet applied |
| 7 | Rejected — staged entries failing flip conditions + standing refusals | ScoutStandingRefusals (7/7 stand, 0 flips cleared, package byte-identical to r35) + ScribeAssimilationGate §3 | ready |
| 8 | Quarantine slice verdicts | ScoutQuarantine §2 + ScribeAssimilationGate §2 (r36 labels, label conflict, S065 transport note, TLS caveat, adopted 0) | ready |
| 9 | Id-collision numbers | ScoutIdCollisions + ScribeAssimilationGate §1: reg 52 / staged 94 / **22 collisions S031..S052**; predicted **53/94/23** after S053 lands (staged S053 is a different document — METI 告示第19号 — so the new collision is the standing renumber class, not a defect); guard load-bearing (indented row caught only by the 0–3-space pattern) and fail-closed (exit 2) | ready |
| 10 | Assimilation: none adopted | ScribeAssimilationGate (adopted 0; the ≥1-admit leg is met by C2's F19, the ≥1-reject leg twice over) | ready |
| 11 | considerthese dispositions | ScribeConsiderthese: proposals 3 and 5 adopted; 1 computed (`gap: 24 of 47 rechecks still gated on a lost base`, criteria-in-§Saturation plank unlanded); 2/4/6/7 reasons recorded | ready |
| 12 | Spot-check result placeholder | this receipt's §1 plan | to be filled by the L1 after the fresh reviewer runs |
| 13 | `## Mistakes` anchor M36-1..M36-4 | ScribeMistakes (four rows with captured-by criteria R4/R16/R17+R11, fix contracts, fail-able fixtures) | ready |
| 14 | Census before → after with exit codes | before = `.ufo/waves/round-36/census-before.txt` (3 lines, exit 0; byte-matches ExecCensusReplay run-1 and this seat's run); after must **name the command and the measuring seat**, not an invented value (scribe confirmed via IRC) | before ready; after owed at integration |
| 15 | status/recheck/used-by old→new log | S053 is a new row (no old→new); any other cell changes must be logged | obligation on the L1 |
| 16 | No false evidence lines (E8 / M36-2 class) | every "exit 0 on committed bytes" claim in the Gate must be measured on the export head, never the worktree | obligation on the L1 at integration |

## 3. Gaps found (all verified by this seat)

- **G1 — one-hex-char sha256 discrepancy in the entry draft: found and fixed pre-landing (re-verified); residual is a grep trap.** ScribeEntryF19's first revision carried `4ec61c59b0a9aedf…` (b0**a**9) in the entry header and §2 where the capture is `4ec61c59b0e9aedf…` (b0**e**9). This seat settled the correct value independently at 15:42:09Z (re-fetch through the lane's own normalizer → b0e9) and flagged it to the Gate scribe; ExecC2QuoteOnce had caught the same defect pre-yield and ScribeEntryF19 fixed it (receipt revisions `c4f7d5b4e16f…78e0` → final `36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641`, 17,374 B, mtime 15:43:27Z). Re-verified by this seat on the corrected receipt: the §6 entry header (`:143`) and the V11 re-derivation (`:73`, `:124`) carry b0e9 and `match_capture: [True]`. **Residual:** the historical b0a9 string survives in record sections only — ExecC2QuoteOnce ×2 (defect-found-and-fixed), ScribeRowS053 ×3 (§8 conflict record), ScribeEntryF19 ×1 (the correction note quoting the error), MutJunkTwin ×1 (observation), this receipt ×1. A naive `grep -r b0a9 .ufo/waves/round-36/wave1/` reports five files red on a fixed defect; any future check must exempt record sections or anchor on the live pins (`ScribeEntryF19.md:46,59,85,123,143,373`). The live check stays A1 step 2: re-hash the landed capture and diff the entry header digest against the manifest — no instrument polices the entry header (source-recheck reads the manifest), which is why the defect was invisible to the harness.
- **G2 — before-control key unbacked.** `.ufo/waves/round-36/c2-controls/before.txt` records
  `junk_present: 1`, but `git ls-tree -r b47f2cd` contains no junk-f19 path anywhere and no lane-root
  `c2-controls/` exists (verified). The key has no recorded command and its value does not match the
  frozen tree; the junk-twin rejection is provable only from ExecC2JunkControl's receipt (the A2/A3 pair
  plus the no-row check), not from the frozen control. ScribeGateLesson flagged this independently; the
  Gate/report should state it rather than let the before-control imply the fixture existed at freeze.
- **G3 — S037/S054 label conflict unresolved.** Round-36 scout files both rows `absent` (register's own
  definition: fetched cleanly, span in none of the folds); round-35's executor filed the same facts
  `prose-class-unverifiable`; bytes are identical across rounds. Two receipts (ScoutQuarantine note A,
  ScribeAssimilationGate conflict 1) leave one label to the L1. The Gate must carry the conflict note —
  a silent switch from r35's label would be an unlogged verdict change.
- **G4 — S065 verdict is probe-bound.** `unreachable (this probe)` rests on the 30 s cap (677,543 of
  7,465,472 B delivered, no PDF trailer); rounds 33–35 fetched the full body. The Gate must carry the
  transport-only caveat verbatim; a reviewer re-fetching with a larger cap may flip the label, and that
  flip confirms the caveat instead of refuting the round.
- **G5 — after-state bytes not landed at check time.** The entry, the S053 row, the capture+manifest, the
  junk fixture, `r36-closure.sh`, RevEntryF19 and the ScribeGateLesson draft receipt are all absent from
  the tree at ~16:05Z; every after-number in the frozen claims is a prediction until the L1 lands and the
  suite/harness run on the export. The spot-check must therefore execute A5/A6 on the final-head export —
  receipts alone prove nothing about the judged revision (the exact r35 failure mode).
- **G6 — harness quote-blindness must be stated in the Gate.** H2 (measured): a forged F19 row plus the
  real manifest admits the twin (`entries=22 pass=22`). `entries=22 pass=22` is admission-shape evidence;
  quote truth rides on the pinned comparison and the no-row check. A Gate that cites the harness count as
  the rejection would repeat the round-35 erratum's mistake in new clothes.

## 4. This seat's verification log

- Re-derived the capture through the lane's own instrument: `capture-source.py --id S053 --url
  https://www.first.org/epss/ --out <scratch>/S053-recheck.txt --kind html` → status 200, fetched 26,804,
  snapshot 8,448 B / 244 lines, sha256 `4ec61c59b0e9aedf…83e9`, utc `2026-10-26T15:42:09Z` (third
  independent identical fetch of the round).
- Quote pins on that copy: Q1 25 words occ=1; Q2 8 occ=1; Q3 23 occ=1; Q4 23 occ=1; junk sentence
  `EPSS guarantees exploitation within 30 days for every scored CVE.` occ=0 (10 words).
- Harness before-state: `python3 corpus/instruments/frontier-recheck-count.py` → `entries=21 pass=21
  exit=0` (offline, ~1.5 s), confirming the invocation and the before-control's `harness` cell.
- Census validate (fleet script, read-only, no `--out`): exit 0, `W04 S028` + `W04 S029` + `ok`; registry
  rows 52 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`).
- Before-controls read: `.ufo/waves/round-36/c1-controls/before.txt` (suite_missing=1, placeholder_filled=0,
  placeholder_angle=0, r36_registry=0, r35_registry=0, scratch_leftovers=0, worktree_clean=0),
  `c2-controls/before.txt` (frontier 18, registry 52, s053_rows 0, entries_citing 0, knowledge 47,
  harness entries=21 pass=21 exit=0, junk_present=1 — see G2), `census-before.txt` (3 lines).
- `git ls-tree -r HEAD`: no junk-f19; committed control fixtures at `.ufo/waves/round-34/c2-controls/junk-f17.md`,
  `.ufo/waves/round-35/c2-controls/junk-f18.md`, `.ufo/waves/round-34/c1-controls/fake-suite.sh`.
- Suite control refs verified: `git cat-file -t` + `git merge-base --is-ancestor refs/heads/master` for
  `3266c993…` (commit, ancestor), `0aee0ef1…` (commit, ancestor), `b47f2cdf…` (commit, ancestor),
  `cc692008…` (commit, ancestor) — the A5 negative controls are runnable refs, not dangling names.
- Peer coordination: two messages to `ScribeGateLesson` (required-block list; G1/G2 findings + verified
  pin counts); two replies received — the first confirming the block list, the Q1 25-word handling, the
  census-after discipline, and independently flagging G2; the second reporting the G1 fix. Re-verified
  the fix myself rather than taking the peer's word: `ScribeEntryF19.md` mtime `15:43:27Z`; live header
  and pins carry b0e9 (`:46,59,85,123,143,373`); ExecC2QuoteOnce verdict line records **PASS on the
  final entry bytes `36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641`** (17,374 B) with
  `sha256 literals in entry: ['4ec61c59b0e9…']`, `match_capture: [True]`, pins re-run 25/8/23/23 words at
  216/217/217/235, junk both 0, 11/11 blockquotes anchored, `recheck:` `bash -n` rc=0; b0a9 full-string
  census over wave1 receipts: ExecC2QuoteOnce ×2, ScribeRowS053 ×3, ScribeEntryF19 ×1 (correction note),
  MutJunkTwin ×1, this receipt ×1 — all record sections (G1 residual).
- No tools installed or upgraded (2026-10-19 authorization unused); no lane, fleet, sibling-lane or
  source-tree write; read-only git only (`rev-parse`, `ls-tree`, `status`, `log`, `show`).

## 5. Limits

- This receipt is a plan plus draft-readiness check: it verifies no claim and issues no admit/reject
  verdict; the fresh non-author reviewer owns those at the final lane head.
- Landing state is a snapshot at ~15:45Z; receipts landing after it (ScribeGateLesson, RevEntryF19, the
  suite, the applied row/entry/fixture) may resolve G5's items — re-check before judging.
- The A5/A6 after-state expectations are the frozen `counting_commands` from `claims.json`, not this
  seat's measurements (the suite is not yet in the tree; F19 is not yet landed).
- Scratch `/fast/scratch/hyaku/kasegi-r36/RevSpotCheckReadiness/` (re-derived capture + tmp) removed
  before yield; nothing was copied into the wave dir except this receipt.

Report: .ufo/waves/round-36/wave1/RevSpotCheckReadiness.md
