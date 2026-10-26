# ConnPatterns — round-36 defect/class correlation and R28/R29 proposal

| field | value |
|---|---|
| seat | `ConnPatterns` (connector, leaf — no dispatch) |
| item | correlate this round's defects with the kaika fleet mistake taxonomy and prior rounds; name repeating classes and the criteria that would have caught each; propose R28/R29 wording (fed to `ScribeQualityRows`); verify no duplication against `corpus/QUALITY.md` |
| axes owned by the round | `depth:verifiability`, `coverage`, `calibration`; this seat judged on `depth:verifiability`, `calibration` |
| milestone | round-36 |
| lane head at work | `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze); base `cc692008b0cfd58d18275aa6c4aed79620120799` |
| worked at (UTC) | 2026-10-26T15:40–15:56Z (local shell clock 12:40–12:56 -03:00) |
| lane writes | none — receipt only. `corpus/QUALITY.md` sha256 unchanged across this seat: `d4f83bb1206f5084…d6e2b69` (250 lines / 33,731 B, re-measured) |

This is a correlation and proposal seat: it produces analysis and draft wording, and it lands no
lane artefact. Every measurement below is a read-only command over the freeze head
`b47f2cd` unless a command names another revision. Class names use the kaika §5 Gate vocabulary
(`landing`, `closure-order`, `stale-premise`, `counter-discrimination`, `number-drift`,
`reference-drift`, `scope`, `attribution`, `provider`) as extended by this lane's lessons
(`freeze-satisfiability`, `gate registration`, `line-number drift`, `limb-oracle gap` are
lane-internal specialisations in use since round 31).

---

## 1. The defect set being correlated

Round 36 closes the round-35 verifier spot-check's routed defects
(`corpus/lessons/round-35-verifier-spotcheck.md:127-141`) plus the round-35 lesson's standing
mistakes (`corpus/lessons/round-35.md:209-337`). Mapped to the frozen E-checks
(`.ufo/waves/round-36/claims.json` C1) and the M36 rows
(`.ufo/waves/round-36/wave1/ScribeMistakes.md:25-28`):

| spot-check item | E-check / M36 row | class (kaika §5) |
|---|---|---|
| §5.1 commits after `complete`; §5.6 dirty tree | E9 / M36-1, M36-4 | landing / closure-order |
| §5.2 re-claim with frozen evidence (run over the cited head) | E1 export mode / — | closure-order (measurement binding) |
| §5.3 D1 guard file-wide; repudiation fixture scores `open=0` | E1 slot-binding / M35-2 | counter-discrimination |
| §5.4 D6 in-place rewrite (−3/+6) though frozen after said appended | E6 / — | line-number drift / append-only violation |
| §5.5 false evidence lines at the judged head | E8 / M36-2 | stale-premise |
| D3 registry rows never landed; near-name sibling satisfied the literal | E3 / M36-3 (M35-4) | counter-discrimination (gate registration) |
| D5/M35-5 junk-twin rejection limb not executable | C2 junk control / M35-5 | counter-discrimination (frozen predicate form) |
| M35-3 15-line deletion shifted density row 1145→1146 | (append-only discipline; no dedicated E-check) | line-number drift |
| M35-11 stale density guard row (base mean as after-reading) | E2 (D2 class recurs) / — | stale-premise |
| M35-9 future-dated freeze instant; M35-8 false build-spec premise | (disclosed open items) | stale-premise |

## 2. Which classes repeat — the four-class correlation

### 2.1 closure-order — the lane's most persistent class at closure

Fleet mapping: kaika C09 *evidence landing* (7 ledger rows; kasegi is one of the named lanes).

Lineage (re-verified this seat, commands in §5):

- **r30** — spot-check defect 1: 8 untracked leftovers at closure
  (`corpus/lessons/round-30-verifier-spotcheck.md:15`); lesson M30-3 transient non-comparative
  outputs during concurrent writes (`corpus/lessons/round-30.md:76`).
- **r31** — lesson M31-2 in-flight digest churn: peers gated on an entry still being rewritten
  (`corpus/lessons/round-31.md:106`). The r31 spotcheck quiescence check itself **passed**
  (`round-31-verifier-spotcheck.md:17`).
- **r32, r33** — quiescence checks **passed** (`round-32-verifier-spotcheck.md:32`;
  `round-33-verifier-spotcheck.md:31`).
- **r34** — spot-check D4: `wave1-results.json` written 3 min 48 s after `complete`
  (`round-34-verifier-spotcheck.md:30`); minted as **M35-1**
  (`corpus/lessons/round-35.md:209-221`).
- **r35** — spot-check routed 1 (commits `8ce6fb4`…`48e6053` after `complete`, 04:01–04:04) and
  routed 6 (dirty tree) (`round-35-verifier-spotcheck.md:127-129,140-141`); in-wave M35-7:
  a receipt asserted `scratch-absent` while later writes re-created the tree
  (`corpus/lessons/round-35.md:282-292`).
- **r36 target** — M36-1 (commits after `complete`), M36-4 (report re-filed after `complete`).

Calibration: the class is **non-monotonic** — it landed at r30, r34, r35 (3 of the last 6 closure
checks) and passed at r31–r33. It also appears between closures as in-flight measurement (M30-3,
M31-2). The recurrence tracks wave pressure, not reviewer attention: exactly the argument for a
standing gate (E9 + proposed R28) instead of per-round vigilance. Criteria that existed and their
limbs: **R4** requires a resolvable work commit and says "a rendered wave is not execution" but has
no quiescence-before-`complete` limb and no export-bound-run limb; **R16** binds failure paragraphs,
not lane state. ScribeMistakes records M36-1 captured-by `none (new)`, criterion missed R4 — the
gap is real and R28 fills it.

### 2.2 stale-premise — the second repeating class

Fleet mapping: kaika C06 *stale premise* (8 ledger rows, 121 lesson mentions — second only to C04).

Lineage: **M31-1** (r30 paragraph outlived its fix; `corpus/lessons/round-31.md:104`) → **r31 O3**
(the stale premise recurred *inside its own fix*: CHECK A kept the historical `43/43` literal
load-bearing; `corpus/lessons/round-31.md:119`) → **M35-8** (uncommitted build-spec edit states a
false capture premise; `corpus/lessons/round-35.md:294-305`) → **M35-9** (freeze instant 62 min in
the future; `corpus/lessons/round-35.md:307-313`) → **M35-11** (guard row prints the base density
mean as the after-reading; `corpus/lessons/round-35.md:325-337`) → **M36-2** (lesson Gate line
"source-recheck exit 0 on committed bytes" false at the judged head; ScribeMistakes row, captured-by
R16).

Criteria limbs: R1 (live-assertion as-of dating), R2 (self-description cites its census), R16
(paragraph closure checks), R18 (byte-bound closure), R19 (specimen figure bound to its producing
command). M36-2's specific form — an evidence line asserted against a head that is not the judged
head — is the stale-premise and closure-order overlap; R16 is ScribeMistakes' recorded capture, and
R28's export-binding limb is the closer root fix. No new criterion is proposed for this class:
R28 + R16 together close it.

### 2.3 counter-discrimination — the most-instrumented fleet class, still recurring

Fleet mapping: kaika C04 *vacuous or inert verification* (9 rows, **208 mentions** — the fleet's
most-instrumented failure class) plus C07 *unbounded closure* (7 rows).

Lineage: **r24 wave-1 mutants** (forged S001 record, `location:` no code reads — Q9/R10 grounding;
`ResolverAttack` always-GONE 1/8, R11 grounding) → **r25** (bound-64→8 scored 4/8 while "8/8
dispatch" was reported — R13's grounding overstatement) → **M34-1** (kill rule caught 3 of 4,
report said "all mutants killed"; `corpus/lessons/round-34.md:238-252`) → **M34-4** (own-instrument
false green: selftest reused a fixture root; `corpus/lessons/round-34.md:288-297`) → **M35-2** (D1
clause cannot see the placeholder spelling that actually occurred; a repudiation of the hash
satisfies its correction clause, `open=0`; `corpus/lessons/round-35.md:222-233`) → **M35-5** (C2
junk-twin rejection limb has no discriminating invocation — "exactly the round-34 D5 finding";
`corpus/lessons/round-35.md:258-267`) → **M36-3** (the round's own closure gate unregistered: the
near-name `r-defect-closure` satisfied the old literal while `r35-defect-closure.sh` counted 0;
ScribeMistakes row, captured-by R17 limb / R11).

Criteria limbs: R11 (publish discrimination against degenerate/mutated instruments), R13 (one frozen
instrument, isolating fixture per limb), R17 (one-limb mutants), R24 (`selftest case=` verdict line
per case), R22/R25 (freeze satisfiability — M35-2's recorded miss). The registry-identity form
(M35-4/M36-3) has **no** row: SKILL.md Gates & probes registration had no exact-basename rule →
proposed R29.

### 2.4 line-number drift — fully covered, still recurring on process

Fleet mapping: adjacent to kaika C01 *reference drift* (11 rows) and C02 *number drift* (10 rows);
the lane's R6 is the specialised rule.

Lineage: **M17** (r22 provenance headers inserted at line 2 shifted ~160 anchors by +3;
`corpus/lessons/round-22.md` M17 row, R6 minted) → **M31-3** (SOURCES.md row insertion left
round-29 citations +2, then +4, then +7 stale; `corpus/lessons/round-31.md:147`) → **M35-3** (the
D1 landing deleted 15 lines from append-only SCORECARD.md, shifting the round-34 density row
1145→1146 and orphaning `round-34-verifier-spotcheck.md:173`'s citation;
`corpus/lessons/round-35.md:235-245`).

Criteria limbs: **R6** (edits keep every existing line at its number; append at the end;
anchorcheck before/after prints the same cited lines) and **R9** (numerical errata name their base;
line pointers re-opened against the cited revision; corrections appended, filed assertions left
byte-identical). Both defects were *disclosed by seats* (ExecD1Markers for M35-3) — the rule held,
the process pressure to substitute in place came from the frozen kill rule's own placeholder
clause. Verdict: **no new criterion**; the class is caught by existing rows and the round-36
instrument inherits the append-only discipline (R28/R29 are appended; E7's supersedes strings are
not re-worded).

## 3. Criteria coverage matrix — which QUALITY row would have caught each defect

| defect | class | existing criterion that would have caught it | capture recorded | gap filled this round |
|---|---|---|---|---|
| r35 §5.1/§5.6 quiescence | closure-order | R4 (partial: work-commit limb only) | M36-1 `none (new)`, missed R4 | **R28 + E9** |
| r35 §5.2 run over cited head | closure-order | R13/R19 (binding spirit) | M34-4 (r34 instance) | E1 export mode (+R28 limb) |
| r35 §5.3 D1 file-wide literal; repudiation | counter-discrimination | R11/R17/R24; R22 recorded miss | M35-2 missed R22 | E1 slot-binding |
| r35 §5.4 in-place rewrite | line-number drift | R6 + R9 | disclosed (ExecD1Markers class) | E6 (append form) |
| r35 §5.5 false evidence line | stale-premise | R16 (recorded); R18/R19 partial | M36-2 captured-by R16 | E8 (+R28 root limb) |
| D3/M36-3 registry identity | counter-discrimination | R17/R11 (instrument side only) | M36-3 R17 limb / R11 | **R29 + E3** |
| M35-5 junk-twin limb | counter-discrimination | R22/R25 (freeze satisfiability) | M35-5 "criterion missed: D5 erratum rule" | C2 junk control |
| M35-3 line shift | line-number drift | R6 + R9 | disclosed | none needed |
| M35-11 stale guard row | stale-premise | R9/R16; D2's own fix | recorded | E2 |
| M35-9/M35-8 stale premises | stale-premise | R22/R25 (M35-9); none (M35-8) | recorded | disclosed open items |

## 4. R28/R29 proposal (fed to ScribeQualityRows)

`ScribeQualityRows` drafted both rows (`.ufo/waves/round-36/wave1/ScribeQualityRows.md` §1); this
seat independently re-derived the grounding and ran the duplication sweep, then proposed one
grounding addition. Messages to `agent://ScribeQualityRows` carry: (a) add M35-7 as R28's second
grounding instance (cleanup-ordering limb: "a durability assertion made before the last write is a
prediction" — same class, distinct mechanism from §5.1/§5.6); (b) duplication verification results
below; (c) a correction to my own first-pass recurrence claim — r31/r32/r33 quiescence checks
**passed**; the closure-order lineage is r30 → r34 → r35 (3 of the last 6) plus in-flight M30-3 /
M31-2, not six consecutive. **Adoption record (15:55Z):** ScribeQualityRows adopted both items — M35-7 now in R28's grounded-in cell with criterion text byte-identical, and my corrected lineage is their receipt's F6 ("3 of the last 6 closure checks", never "six consecutive"). The feed loop is closed; their receipt re-ran the greps independently (its G15/F5).

Proposed final wording (connector synthesis of the ScribeQualityRows draft; changes from that draft
marked):

| id | criterion | grounded in |
|---|---|---|
| R28 | A round's claims rest on committed paths at the quoted head, and the run that carries them is made against that head, not the worktree: the counter/harness runs a claim cites are recorded over a `git archive <final lane commit>` export (an `--export-ref <hash>` run), and the lane is quiescent before filing — `git status --porcelain` empty and no leftover scratch seat dirs under `/fast/scratch/hyaku/kasegi-rNN/`. A run made while wave seats still write, or over a worktree that differs from the quoted head, is not a closure run and cannot carry a claim. | `corpus/lessons/round-35-verifier-spotcheck.md:127-129` (§5.1) and `:140-141` (§5.6); M35-7 (`corpus/lessons/round-35.md:282-292` — the cleanup-ordering recurrence); `considerthese/2026-10-26.md:31` proposal 3. [addition: M35-7 citation] |
| R29 | An instrument is registered at the `SKILL.md` § Gates & probes registry under its exact basename — one row whose name cell is exactly the file name (`r36-closure.sh`) — not under a name of which it is a substring. A near-name sibling row (the `r-defect-closure.sh` row for `r35-defect-closure.sh`) does not satisfy the registry requirement, and a registry count reached by a substring literal is a false green even when it prints non-zero. | M36-3 (`.ufo/waves/round-36/wave1/ScribeMistakes.md` row 3; class counter-discrimination, captured-by R17 limb / R11); re-derived at freeze: `git show b47f2cdf…:SKILL.md \| grep -cF 'r35-defect-closure.sh'` → 0 while `grep -cF 'r-defect-closure' SKILL.md` → 4 |

No wording change is proposed for R29's criterion cell; the ScribeQualityRows draft text stands.

## 5. Duplication verification (independent grep at the freeze head)

Commands and observed values (lane root, `b47f2cd` worktree, 2026-10-26T15:47Z):

| probe | command | observed |
|---|---|---|
| no quiescence row | `grep -ci quiesc corpus/QUALITY.md` | 0 |
| no porcelain clause | `grep -ci porcelain corpus/QUALITY.md` | 0 |
| `git archive` usage | `grep -ci 'git archive' corpus/QUALITY.md` | 1 — R14 only: tarball regeneration for evidence economy (semantics: bloat control, not measurement binding) |
| `scratch` usage | `grep -ci scratch corpus/QUALITY.md` | 2 — both inside R18's closure-check commentary (mutant-control scratch copies, not seat scratch dirs) |
| no export-ref | `grep -ci export-ref corpus/QUALITY.md` | 0 |
| no basename rule | `grep -ci basename corpus/QUALITY.md`; `grep -ci near-name corpus/QUALITY.md` | 0; 0 |
| highest row id | `grep -cE '^\| R[0-9]+ \|' corpus/QUALITY.md`; `grep -cE '^\| R2[89] \|' corpus/QUALITY.md` | 27; 0 |
| file anchors | `wc -l -c corpus/QUALITY.md`; `sha256sum corpus/QUALITY.md` | 250 lines / 33,731 B; `d4f83bb1206f5084…d6e2b69` (matches ScribeQualityRows G12) |

Adjacent-row discrimination (the semantic-overlap check a future re-reader would run):

- **R28 vs R4**: R4 credits a round's existence (resolvable work commit; rendered wave ≠ execution);
  it has no quiescence-before-filing limb and no export-bound-run limb. R28 adds both. Distinct.
- **R28 vs R14**: R14's `git archive` regenerates fixture trees to cap repo growth. R28's binds the
  measurement to the quoted head. Same command, different purpose; both cells say which.
- **R28 vs R16/R19**: R16 binds failure paragraphs; R19 binds specimen figures to a producing
  command. R28 widens the binding family from figures/paragraphs to whole counter/harness runs — a
  widening, not a duplicate; no supersession clause is carried (consistent with ScribeQualityRows F4).
- **R29 vs R11/R17**: R11/R17 govern an instrument's *discrimination* (mutants, degenerate
  controls); R29 governs the *registry identity* of the instrument at its home. The M35-4 failure
  passed R17's letter (the mutants were instrument-side) while the registry side stayed unregistered.
  Distinct object; both needed (ScribeQualityRows F1's point, confirmed).

Verdict: **no duplication; no supersession; append-only block after line 250 consistent with R6.**

## 6. Findings for the L1

- **F1 (calibration)**. The four repeating classes rank by persistence at closure: closure-order
  (3 of the last 6 spotchecks: r30, r34, r35) > stale-premise (every round since r31: M31-1, O3,
  M35-8/9/11, M36-2) > counter-discrimination (r24, r25, M34-1, M34-4, M35-2, M35-5, M36-3) >
  line-number drift (M17, M31-3, M35-3). Coverage today: line-number drift fully held by R6/R9;
  counter-discrimination held on the instrument side (R11/R13/R17/R24) with the registry side the
  remaining gap (R29); stale-premise held for paragraphs/figures (R16/R18/R19) with the
  wrong-head-evidence-line form closed by R28+E8; closure-order had no standing gate (R28+E9). The
  two proposed rows close the two open gaps — each is grounded in a mistake that recurred *after*
  its adjacent criterion existed, which is the QUALITY.md design rule ("every criterion exists
  because the lane already failed it once").
- **F2 (depth:verifiability)**. R28 and E9 are the same gate stated on two surfaces (bar and
  counter); C1's suite is R29's counter (E3). Landing either without the other halves the closure —
  the round-35 lesson's open item 1 pattern (kill rule met, certification unbound) in reverse.
- **F3 (correction to the record)**. My initial correlation message to ScribeQualityRows overstated
  the closure-order recurrence as "six consecutive spotchecks"; the re-verified lineage is r30 →
  r34 → r35 with r31–r33 passing. The corrected table (§2.1) is the citable one; the calibration
  argument for a standing gate is *stronger* under the corrected facts (recurrence tracks wave
  pressure, not reviewer attention).
- **F4 (line-number drift needs no R30)**. Both M31-3 and M35-3 were *disclosed by seats*, not
  missed by the bar; the pressure came from frozen clauses mandating in-place substitution. The
  fix is process (append + erratum, per R9), already exercised by E6/E7's form this round.

## 7. Hygiene

- Receipt: `.ufo/waves/round-36/wave1/ConnPatterns.md` (this file).
- Scratch: `/fast/scratch/hyaku/kasegi-r36/ConnPatterns/` (draft only), removed before yield.
- Lane writes: none. `git status --porcelain` over the lane shows only pre-existing round-36 wave
  artifacts; no lane file was created or modified by this seat.
- Coordination: two messages to `agent://ScribeQualityRows` (proposal + correction); no broadcast.
- Tooling: none installed or upgraded; system `git 2.56.0`, `grep`, `python3`, `bash` — all
  pre-existing. `/home/vgpnk/.omp/agent/RULES.md` was not required beyond the operator
  authorization quoted in the assignment (no install performed).
- Read-only git only: `log/show/grep/diff/status/ls-tree` over the lane and fleet root; the kaika
  fleet taxonomy was read at `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/mistakes.md`
  (fleet root is read-only to this seat; nothing written there).

Report: .ufo/waves/round-36/wave1/ConnPatterns.md
