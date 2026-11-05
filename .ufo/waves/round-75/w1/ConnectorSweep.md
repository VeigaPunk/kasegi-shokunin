# ConnectorSweep — kasegi round 75, attempt 1 (wave w1)

Cross-lane overlap and input sweep. All work read-only; every finding below was measured at the
freeze commit, before wave integration landed.

Revision discipline (commands and exit codes):

- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` →
  `748dfb666280adfb1e249fcf6a265c5d9951eefb`, rc=0. The working tree **is** the freeze commit;
  `w1.ready.dispatched` exists but integration has not landed, so every read below is at base.
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin cat-file -t 748dfb666280adfb1e249fcf6a265c5d9951eefb`
  → `commit`, rc=0.

Tooling note: harness policy routes all regex search through the grep tool (Rust regex), never shell
`grep`. Equivalent shell commands are stated beside each result for replay. The grep tool returns
match sets and page footers; it does not surface an exit code, so no exit code is claimed for the
searches — the counts are the tool's own page totals. No tools were installed (none needed); no
network was touched; no live target was contacted.

Claims read in full before starting: `.ufo/waves/round-75/claims.json` (all 45 lines, long lines
re-read raw). Predicates, kill rules and scope statements are quoted, never reworded.

---

## 1. Sibling overlap: Fuzzilli / JIT across `*/corpus/`

Command of record: `grep -rl 'Fuzzilli\|fuzzilli\|JIT' /home/vgpnk/*/Projects/... ` — concretely,
the seat-spec form `grep -rl 'Fuzzilli\|fuzzilli\|JIT' /home/vgpnk/Projects/shokunin/*/corpus/`.
Executed as three grep-tool searches over `/home/vgpnk/Projects/shokunin/*/corpus/**`:

| search | pattern (regex) | result |
|---|---|---|
| literal, case-sensitive | `Fuzzilli\|fuzzilli\|JIT` (as alternation) | **275 files** fleet-wide (tool page footer "files 1-20 of 275") |
| fuzzing subject | `fuzzilli`, case-insensitive | **one page, ≤20 files, all under `kasegi-shokunin/corpus/`** — no sibling lane matches at all |
| standalone JIT token | `\bJIT\b`, case-sensitive | one page, ≤20 files, in kaidoku, kasegi, kotoba, revenger, tabi, tameshi only |
| audio-lane literal total | same literal pattern, path scoped to `audio-shokunin/corpus/**` | **26 files** (tool footer "26 files total") |

Reading: the 275-file literal mass is dominated by the substring `JIT` inside `JITTER` /
`JITTER-LEAVES` — audio-lane timing-receipt vocabulary (`corpus/live/r74-baseline/semantic-compare.txt`,
`semantic_compare.py` `JITTER_KEYS`), with the same instrumentation pattern repeated in sibling
timing lanes. It is not fuzzing ground. Per R114 the sweep is by subject, organisation/programme
per hit:

| lane | organisation / programme per hit | verdict |
|---|---|---|
| **kasegi-shokunin** | **Google Project Zero — Fuzzilli** (S109, the project's own README, F52; S093, PZ's Fuzzilli-vs-BigSleep comparison, F41; S109.txt JIT-compiler content at :165, :250-320) | **the only lane holding Fuzzilli ground**; also the only lane with any `fuzzilli` mention |
| revenger-shokunin | fuzzer-tool documentation of other programmes: DecFuzzer ISSTA'20 artifact (S117, `corpus/SOURCES.md:132`) and trailofbits/mishegos differential x86-decoder fuzzer (S396, `:411`), plus S395 (Trail of Bits decoder-fuzzing post); Android ART JIT docs nav title inside `snapshots/dex-format.html` | holds fuzzer **tool** docs, none of them Fuzzilli; `grep -ril 'fuzzilli' ../revenger-shokunin/corpus` → **no matches** (B8 sibling grep) |
| kaidoku-shokunin | Ghidra (S007 local source) — JIT-accelerated p-code emulator release notes (`evidence/round-42/local-sources/S007/ChangeHistory.md:428,617`) and observation perturbation limits ("Timing and JIT behavior are affected") | RE-tool documentation, not fuzzer ground |
| tabi-shokunin | Chromium source pins — WebAssembly lazy-compilation JIT feature flags (`corpus/evidence/round-26/sources/content-features-154.0.8037.97.cc:1274`, round-29 release pins) | browser-source pins, not fuzzer ground |
| tameshi-shokunin | academic test-flakiness research — JIT compilation named as a flakiness mechanism (`corpus/knowledge/flaky-aware-verdict-evidence.md:36`) | measurement research, not fuzzer ground |
| kotoba-shokunin | agent-instruction census prose mentioning "JIT access" (`corpus/knowledge/scoped-rules-round60.md:30`) | incidental token, not fuzzer ground |
| audio-shokunin | none — 26 literal hits are all `JIT` ⊂ `JITTER` timing receipts | no fuzzing ground |

**Does any lane hold the NDSS 2023 Fuzzilli paper? No.** Only kasegi mentions Fuzzilli at all; its
sole NDSS presence is the round-74 lead bullet — `corpus/SOURCES.md:175`: "NDSS Symposium 2023 paper
on Fuzzilli (named at kasegi capture S109.txt:243; the capture carries no URL for it) — unopened
lead; existence and name only" — and the S109 entry's Resources note
(`corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md:71-73`), which asserts existence and name
and nothing more. F53 (C2) therefore advances ground no sibling holds.

B8 named-grep receipts (executed this sweep, at the freeze commit):

- `grep -n 'ndss\|Fuzzilli' corpus/SOURCES.md` (kasegi) → per-hit verdicts: :100 S093 row (held,
  PZ comparison, F41); :121 S109 row (held, Fuzzilli README, F52); :134 Search-log Fuzzilli
  screening sentence (r61 history); :173 Fuzzilli-primary-docs lead kept byte-identical as history
  (retired as opened by S109/F52, round-74 note at :270); :175 the NDSS 2023 lead (F53's input);
  :245/:247/:250/:253/:255/:267/:270 Registry-changes notes (r60/r61/r62/r65/r70/r73/r74). No `S110`
  row exists at the freeze commit — the L1 lands it during integration.
- `grep -ril 'fuzzilli' ../revenger-shokunin/corpus` → no matches. Consistent with M74-7: revenger's
  fuzzer ground is DecFuzzer/mishegos documentation; the Fuzzilli-specific distinctness holds.

## 2. considerthese verdict

`considerthese/` holds exactly 8 files, 2026-10-19.md … 2026-10-26.md (headings sweep
`grep -n '^## \|^[0-9]+\. \*\*' considerthese/*.md`; same 8 filenames the r75 receipt records). The
lane's disposition home is `corpus/knowledge/considerthese-proposals-ledger.md` (itself the landing
of proposal 7, see below) plus QUALITY rows R31 (:278, disposition per touched proposal) and the
grounded-in cells of R14/R15/R23/R26/R28/R110.

### 2026-10-26.md (this round's named input) — proposals and dispositions

| # | proposal (short) | verdict | landing evidence |
|---|---|---|---|
| 1 | Make "distance to next score" explicit | **mined, r39** | `SCORECARD.md:1532` — "## Distance-to-next-score (round 39, mined from considerthese 2026-10-26 proposal 1)"; re-verified by r74's ConnectorSweep (round-74 lesson, Gate) |
| 2 | Run one end-to-end domain task round | **mined: partially r40, completed r74** | r40 Immunefi Sky/MakerDAO six-file exemplar (ledger round-40 section); remainder (claim checker) landed r74: `claim-package-check.py` `rules=8 pass=8 fail=0 verdict=WELL-FORMED`, CVE-2023-38545 trial (`corpus/lessons/round-74.md` § Non-claim work, item 1; r74 Gate last bullet names proposal 2 mined) |
| 3 | Add a quiescence gate before `complete` | **mined, r36 (hardened r37-r43)** | `corpus/instruments/r46-landing-gate.py:4` "Adopts `considerthese/2026-10-26.md` proposal 3"; QUALITY R28 (:263), R33 (:292), R110 (:534, grounded in this proposal); closure-suite E9 lineage r36→r43 |
| 4 | Cap or externalise wave evidence | **in-lane cap half mined r28 (R14); externalise plank still open, operator-owned** | QUALITY R14 (:83, "Wave evidence is receipts and digests in git…", grounded in the 10-25 sibling of this proposal); ledger rows r37-r46 all read "open (unchanged; operator-owned)" for externalisation (release/LFS/prune) — no `.gitattributes`, no LFS filter, measured each round |
| 5 | Land the owed F18 `PROVINCE.md` amendment | **mined/landed, r36** | `PROVINCE.md:77` — "[r36 Frontier amendment …] F18 — CISA Known Exploited Vulnerabilities catalog … admitted round 35"; resolved-landed per ledger round-39 section |
| 6 | Re-tune my own cadence and depth | **sibling mined r34 (R23); this restatement's planks operator/bot-owned, open** | QUALITY R23 (:227, event-driven reflection cadence, grounded in `considerthese/2026-10-25.md` proposal 6, "mined → landed" per round-34 lesson); no second daily run, per-round digest section or weekly cloud pass tracked (ledger round-46 section) |
| 7 | Keep a proposal-status ledger | **mined, r30** | `corpus/knowledge/considerthese-proposals-ledger.md` exists with per-round disposition sections (r37-r42, r46 fills read this sweep); QUALITY R31 (:278) grounded in `considerthese/2026-10-26.md:35` proposal 7 |

### Per-file verdicts, 2026-10-19 … 2026-10-25

Every lane-actionable proposal in the older files is mined; the unmined remainders are bot-routine
or operator-owned carry-overs, repeatedly tracked as such in the later files themselves.

- **2026-10-19.md — mined.** P1 anchorcheck regression test: superseded r28 (`anchorcheck.py`
  fail-closed; named in 10-26 P7's own text). P3 severity-language grounding: mined via S006/S007
  and F13 (r29) / F17 (r34). P4 saturation line: landed — `SCORECARD.md:309` `## Saturation`
  (verified this sweep). P5 draft-PR-#1 decision: no lane record of a decision — João-side
  carry-over, restated in 10-20..10-25; not lane-mineable. P2/P6/P7 (rubric calibration,
  craft-vs-meta ratio, GitHub listener): bot-routine, no lane surface.
- **2026-10-20.md — mined.** P1 live-source rechecker → `source-recheck.py` (r24 family, R12/R20/R21
  binding lineage). P3 owed-corrections ledger → R15 open-defects ledger (r29, grounded in 10-25 P5)
  and R26 distance reporting (r35). P4 pre-screening queued sources → the standard pre-freeze screen
  (R85). P2/P5 rubric lenses and metric-redefinition flag: bot-side; P6 carry-overs restated.
- **2026-10-21.md — mined.** P1 run every recheck daily → `recheck-audit.py` (running by r26/r31);
  P2 quotes-vs-snapshots before admission → the source-recheck gate itself (Q8/Q9 family);
  P4 second-reviewer red-before fixtures → the fail-before/red-before discipline (R84, R22/R25
  satisfiability). P3/P5 bot-side; P6 carry-overs.
- **2026-10-22.md — mined.** P1 close-r23 dossier → executed (r23 close, then F06–F08 admitted in
  the r25 window per 10-25's own record). P3 idleness counter → covered on the lane side by R26
  distance-to-next-score reporting; the wall-clock counter itself is bot-side. P2/P4/P5 bot-side.
- **2026-10-23.md — mined.** P1 quote uniqueness + anchor → QUALITY Q9 (:64; the 10-24 sharpening is
  the grounded-in row; 10-23 P1 is its predecessor) and R41 whole-token reads. P2/P3 dossier
  variants → executed as above. P4/P5 bot-side carry-overs (cadence, PR #1).
- **2026-10-24.md — mined.** P1 normalize + pin → QUALITY Q8 (:57, grounded in "10-24 proposals 1
  and 2") with R41; P2 clean-text capture → the capture/normalization conventions (R20/R21, R73);
  P3 dossier → executed. P4/P5 bot-side carry-overs.
- **2026-10-25.md — mined.** P1 wave-evidence cap → QUALITY R14 (r28). P2 distance-to-next-score →
  QUALITY R26 (r35, grounded in this file's proposal 2) plus the r39 SCORECARD section. P3 bounty
  craft / SHONEN box 2 → partially r40 (exemplar), completed r74 (trial + `claim-package-check.py`).
  P4 status ledger → r30 (the ledger file). P5 open-defects ledger with runnable closure checks →
  QUALITY R15 (r29). P6 event-driven reflections → QUALITY R23 (r34).

### The one still-unimplemented item

Zero lane-actionable proposals remain unimplemented. Exactly one plank remains open anywhere in the
file set: **2026-10-26.md proposal 4's externalise remainder** ("Cap or externalise wave evidence" —
keep digests in-tree and move raw seat transcripts to releases or LFS, or prune by round age). The
ledger has carried it `open (unchanged; operator-owned)` every measured round since r37; the
keep-or-externalise decision is the operator's, not the lane's.

**Fits this round's claims? No.** r75's claims are C1 (a census counter amendment confined to
`recheck-cwd-census.py`, its registry rows and its README section) and C2 (the F53/S110 admission);
RC-8's kill rule pins the census's exec surface. Evidence externalisation touches neither claim and
is not adoptable read-only by a lane round under the operator-ownership record. **Verdict only —
not adopted this round.** (2026-10-26 P6's cadence planks are likewise open but bot/operator-owned,
not lane proposals.)

## 3. L0 sweep

`grep -n 'kasegi' /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` → 20 kasegi rows (pattern
`kasegi \| round-`: lines 1, 10, 16, 39, 175, 189, 209, 217, 218, 222, 225, 246, 269, 273, 279, 293,
307, 308, 313, 315). Tail 10: :225 (r50 Windows portability), :246 (r54 prompt fidelity), :269 (r57
counter amendment authorization), :273 (r58 re-ask), :279 (r59 derive-gate sandbox), :293 (r60
derive-gate scope), :307 (r70), :308 (r71), :313 (r72), :315 (r73).

The three items this round's spec names — **all three open, none answered in place**:

- **r15 re-scope (:10)** — the vanished `~/Projects/bounties` PROVINCE root; three operator
  questions ((1) reorg vs unintended deletion, (2) recoverability, (3) PROVINCE re-point and
  the-bounty-hunter ownership). No answer marker in the row; corroborated as open by claims.json
  itself — C2 `score_delta_basis`: "the coverage denominator (the lost-domain surface set) is
  operator-owned (L0 kasegi round-15 row)" — and by `PROVINCE.md` r51 annotation (the round-19
  ABSENT record stands; no local checkout has returned).
- **r70 (:307) / r71 (:308) assimilation adoption** — re-stage `merge/kasegi` vs authorize a bounded
  lane-side renumber by document. :308 states in its own bytes: "round-70 row above still open, no
  answer … Decision still needed". Open.
- **RC-8 bash -c exec surface (:315, kasegi round-73)** — "may the first recheck value of each
  knowledge entry run in a counter (bash -c, operator privileges, repo-controlled text)? … Route
  around until ruled." Open; claims.json notes repeat it: "RC-8 (operator, open) … routed around,
  not decided (kill rule keeps the exec-surface count fixed)."

Also open in the tail (recorded, unchanged, not re-litigated here): :246, :269, :273, :279, :293
(r54/r57/r58/r59/r60 operator authorizations), :313 (r72 — the narrowed-C2 amendment
`.ufo/waves/round-72/claims-amendment-c2.json` still "awaits accept/reject"), :225 (r50 Windows
portability), :222 (r49 non-author-lesson citation repair), :217/:218 (r48 attempt authority).

## 4. Assimilation

Committed receipt `.ufo/waves/round-75/controls/assimilation-considerthese-r75.txt` (23 lines, read
in full): header line `reg-ids=109 staged-ids=94 collisions=79`, dated 2026-11-05T09:43:17Z, with
the recorded commands and their outputs.

Cross-checked against the committed collision files (`wc -l`, rc=0):

```
 79 .ufo/waves/round-75/assimilation/collisions
109 .ufo/waves/round-75/assimilation/reg-ids
 94 .ufo/waves/round-75/assimilation/staged-ids
```

The collisions file enumerates staged ids S031 … S109 — 79 of the package's 94 ids collide with this
lane's 109-row registry. **Current collision count: 79.** Trend on committed evidence: 73 collisions
at a 103-row registry (r70), 75 at 105 (r71), 78 at 108 (r74, round-74 lesson Routed defects), 79 at
109 (this receipt) — the collision grows with every admitted row.

**Adoption stays closed**, reason: mass id drift / reshuffled register in
`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`; per the contract's drift rule no
staged row may be adopted and no renumber map can be derived by a read-only check; the decision is
the operator's via the still-open r70/r71 L0 rows. Note the drift also explains the registry-id
headroom C2 uses: staged `S109` is a different document (GB/T 30279-2020 征求意见稿, per the r74
sweep), so lane `S110` for the NDSS paper is uncollided (claims B1 pre-condition).

## 5. Round-73/74 routed-defect carryover

Source: `corpus/lessons/round-74.md` § Routed defects (read in full) cross-read against
claims.json C1/C2.

**Round 75 closes (by claim, as frozen):**

- **M74-6 → C1.** C1's scope sentence was falsified at file level (a file carrying only
  `restoration-recheck:` counted as `norecheck=1`, RESULT conformant). C1 makes the exclusion
  explicit: docstring sentence, a `restoration_only=N` output field moving such files out of
  `norecheck`, a norecheck- and restoration_only-aware RESULT gate (conformant requires all four
  zero), and selftest case 6 — before-values A1–A4 and the kill rule frozen in claims.json.
- **M74-7 → C2's B8.** The overbroad "none holds fuzzer tool documentation" sibling clause is
  replaced by a narrowed screen asserting only S109/S093/revenger-S117/mishegos-S396 distinctness,
  with named commands. Both named commands were executed by this sweep (§1): the SOURCES per-hit
  verdicts and the revenger corpus grep (no `fuzzilli` matches; S117 at `:132`, S396 at `:411`
  verified on the sibling registry itself).
- **M74-3 → R122-by-document.** The R33 id collision (2 rows, `corpus/QUALITY.md:292` and `:550`)
  is not repaired in place (QUALITY supersession rule); r75 adds R122 (criterion-id uniqueness;
  collisions are superseded by document, never repaired in place). The class closes; the two
  historical rows stay byte-identical.
- **V74-1 → the erratum + R121.** The census-evidence timing defect is closed by re-running the
  census receipt at the final tip, appending an erratum after the filed bytes of
  `.ufo/reports/round-74/kasegi.md`, and grounding R121 (a shape clause names its measurement
  revision or its drift expectation) — already reflected in claims.json's own notes, which name the
  drift expectation (entries 90→91, exit0_foreign 68→69, restoration_only stays 0).
- **C2-clause weaknesses → named commands B2/B5.** The r74 critic's §(b)/(c) finding (no measuring
  command for the registry-unchanged clause and the quote≤25-words/anchor clause) is closed by B2
  (`git diff <base> -- corpus/SOURCES.md` shows 0 removed lines) and B5
  (`source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110`,
  every quote anchor-ok and ≤25 words) being frozen predicates this time.

**Stays open:**

- **RC-8** (operator): the census still runs recheck values through `bash -c` with operator
  privileges. r75 neither expands nor reroutes the surface — the kill rule pins exactly one `bash -c`
  call site (`run_foreign`) before and after. Routed around, not decided.
- **RC-4 (claim text falsified), RC-5 (weakened), RC-6 (tree scope), RC-7 (dead seat)** — carried
  from round 73, unchanged by r74 and untouched by the r75 claims; RC-7 still has no successor (the
  r73 attack seat was not re-run).
- **M74-3's physical rows** remain present (recorded-not-repaired is the rule; R122 governs the
  class going forward).
- Adjacent operator rows still unanswered in the tail (status unchanged, listed for completeness):
  :313 (r72 amendment acceptance), :293/:279/:273/:269 (derive-gate/counter authorizations), :246
  (prompt fidelity), :225 (Windows portability), :222 (non-author-lesson citations).

## Verification summary

Commands run and their results (exit codes where the shell surfaced them):

- `git -C <lane> rev-parse HEAD` → 748dfb666280adfb1e249fcf6a265c5d9951eefb, rc=0.
- `git -C <lane> cat-file -t 748dfb66…` → commit, rc=0.
- `wc -l` on the four assimilation/controls files → 79 / 109 / 94 / 23 lines, rc=0.
- grep-tool searches (patterns, paths and totals stated inline in §1–§5): the 275-file and 26-file
  totals are the tool's own page footers; the sibling `fuzzilli` search returned no matches for
  revenger and no non-kasegi lane; `## Distance-to-next-score` at `SCORECARD.md:1532`, `## Saturation`
  at `:309`, `### coverage, 7 → 8` at `:1547`; `r46-landing-gate.py:4` adopts proposal 3; QUALITY
  R14 `:83`, R15, R23 `:227`, R26, R28 `:263`, R31 `:278`, R33 `:292`, R110 `:534`; ledger
  disposition sections r37–r46; `PROVINCE.md:77` F18 line; round-74 lesson Gate/Non-claim/Routed
  defects.
- No build, no test run, no instrument executed: this seat is read-only by contract; C1/C2
  after-values are the L1's integration duty and are not re-measured here.

Bounds compliance: writes limited to this file and the seat scratch dir
`/fast/scratch/hyaku/kasegi-r75/ConnectorSweep-2/` (created explicitly; deleted before yield); no
lane-tree writes beyond this report; git usage limited to `rev-parse`/`cat-file` (both on the
allowed read-only list); no subagents spawned (leaf seat); no peer messages needed.
