# ConnClaims — round 35 wave 1 — D1–D7 defect→fix cross-index

Seat: `ConnClaims` (connector, leaf — no subagents, no dispatches). Lane: `kasegi-shokunin`
(only write scope). Lane base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze
`617496b9c6e92bc671e7e78b83df69a04470d0e9`; HEAD at my reads `da2d3c687f82a9814ee71c91c930cb733050d37c`
(wave-1 dispatch; the wave's landings are worktree-only, the L1 commits).

Assignment: cross-index the seven round-34 verifier-routed defects D1–D7
(`corpus/lessons/round-34-verifier-spotcheck.md:171-205`, §6) to their landed fixes — fix artifact
(file/line), closure check in `corpus/instruments/r35-defect-closure.sh`, proving receipt; coverage
table for all 7; flag any defect with no fix, no check, or no receipt; connect D5/D7 to the appended
erratum/supersession artifacts; confirm the fit-freeze satisfiability step is recorded.

Method: read-only greps/git-plumbing over the live worktree plus plain runs of the closure suite
(the plain run writes nothing; suite header `:70-72` — only `--selftest` builds scratch, and I ran no
`--selftest`). No git/jj mutation, no install, no network, no subagent, no `agent://all`.
Scratch: none created — `/fast/scratch/hyaku/kasegi-r35/` contains no `ConnClaims*` tree
(verified below, `ls | grep -i connclaims` exit 1), nothing to clean.

## Report

### 1. Coverage table — D1..D7 all 7 mapped

Defect source: `corpus/lessons/round-34-verifier-spotcheck.md` §6, lines 171-205 (D1 `:172-178`,
D2 `:179-183`, D3 `:184-188`, D4 `:189-193`, D5 `:194-199` [numbered 189-194 in the erratum's own
citation], D6 `:200-203`, D7 `:204-208` — the §6 heading "Routed defects" is at `:171`).

| defect | routed complaint (§6) | fix artifact (file:line, live tree) | closure check (suite) | receipts proving it | live state at my read |
|---|---|---|---|---|---|
| D1 | two unfilled lane-commit placeholders, `SCORECARD.md:1129` + `:1240`, R1 check spelling-brittle | `SCORECARD.md:1130` (preamble hash fill) + `:1241` (closing fill) + appended `Correction (round 35)` at `:1258-1261` | `check_d1` (`r35-defect-closure.sh:130-140`): `placeholders=0,lane-hash-markers=0,correction-c1c6a5f>=1` | `wave1/ExecD1Markers.md` (author; digest `a5c8020e…`); `wave1/RevC1BeforeAfter.md` §4 "D1 — MET"; before-row `wave1/ExecBeforeReceipts.md` §3 | **CLOSED** — payload `placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0` |
| D2 | stale round-34 depth:density row (`SCORECARD.md:1145`, mean 201.7 / 0 changed lines) | appended erratum `SCORECARD.md:1246` ("Erratum (round 35): the round-34 depth:density row … mean is 201.2") + measurement-state paragraph `:1248-1256`; stale row bytes verbatim at `:1146` | `check_d2` (`:143-157`): `erratum-row>=1,erratum-mean>=1,row-bytes>=1` | `wave1/ExecD2DensityRow.md` (author, both limbs re-derived from named blobs); `wave1/RevC1BeforeAfter.md` §4 "D2 — MET" (reproduced 201.7/201.2 with unchanged `density.py`) | **CLOSED** — `erratum-row=1,erratum-mean=2,row-bytes=1 open=0` |
| D3 | `r-defect-closure.sh` + `kill-rule-check.py` unregistered at the SKILL.md Gates & probes registry | `SKILL.md:1093-1104` — rows `:1097`/`:1098` (all eight fields), close-out + pinned digests `:1100-1104` | `check_d3` (`:160-171`): `registry-r-defect-closure>=1,registry-kill-rule>=1` | `wave1/ExecD3SkillRegistry.md` (author); `wave1/RevD3D4.md` §1 (eight fields field-by-field, pinned sha256s match, invocations executed, logs under `wave1/RevD3D4/`) | **CLOSED** — `registry-r-defect-closure=4,registry-kill-rule=4 open=0` |
| D4 | `wave1-results.json` written 3 min 48 s after the round-34 `complete` line, untracked | `.ufo/waves/round-34/wave1-results.json` (312874 B, sha256 `3afa3581…d4`, = the verifier's digest) + provenance note `.ufo/waves/round-34/wave1-results.json.provenance.md` (5639 B, sha256 `e1c44301…98`) | `check_d4` (`:174-186`): `tracked=1` (`git ls-files`) AND `provenance=1` | `wave1/ExecD4ResultsTrack.md` (author: identity pin, note text verbatim, quiescence proof); `wave1/RevD3D4.md` §2; `wave1/ScribeIntegrationNotes.md` Draft B | **HALF-OPEN by design** — `tracked=0,provenance=1 open=1`; the tracked limb flips exactly at the L1's integration commit (ExecD4ResultsTrack §4) |
| D5 | frozen C2 wording not executable / literally false (junk-twin phrase; "every assertion occurrences=1") | `.ufo/waves/round-35/claims-erratum-d5.md` — appended correction, frozen `claims.json` untouched; carries `discriminating invocation` ×5 and `per-id occurrences` ×5 | `check_d5` (`:191-200`): `erratum-file=present`, `discriminating-invocation>=1`, `per-id-occurrences>=1` | `wave1/ScribeErratumD5.md` (author; fixture runs quoted); `wave1/RevD5D6D7.md` §1 (independent re-verification: 10/10 reproductions incl. quote-not-found exit 1, per-id occurrences fixtures, `source-recheck.py --selftest` 10/10); `wave1/RevC1BeforeAfter.md` §4 "D5 — MET" | **CLOSED** — `erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0` |
| D6 | stale dead-seat sentence in `.ufo/waves/round-34/wave1/L1Integration.md:30` | **NO FIX LANDED** — file still the freeze bytes (digest `5472f60a…`, 37 lines); `grep -c 'did not file a receipt (dead seat'` = 1, `grep -c 'Correction (round 35)'` = 0 | `check_d6` (`:203-211`): `dead-seat-sentence=0` AND `correction-round-35>=1`; fixture `r35-fixtures/D6`; suite selftest proves the two clause mutants isolate on the all-fixed tree (`ExecClosureSuite.md` §7) | fix receipt: **NONE — flagged** (see §2). Gap itself documented: `wave1/ScribeIntegrationNotes.md` F7 ("D6 has no seat owner"); `wave1/RevD5D6D7.md` §2 "pending at receipt-draft time (L1 applies)"; `wave1/RevC1BeforeAfter.md` §4 "D6 — NOT MET at 06:39:25Z" | **OPEN** — `dead-seat-sentence=1,correction-round-35=0 open=1` |
| D7 | QUALITY R22 cites M34-2 (grounding is M34-3); R23 grounded-in cites `considerthese/2026-10-25.md:76` | **NO FIX LANDED** — `corpus/QUALITY.md` still the freeze bytes (digest `807cc714…`, 229 lines, `supersedes R22`/`R23` = 0/0). Draft append block ready: `wave1/ScribeQualityDraft.md` §1 (rows R26/R27, 21 lines / 2842 B, block sha `e3aa99a1…`, byte-prefix proof: first 30889 B unchanged) | `check_d7` (`:214-220`): `supersedes-R22>=1` AND `supersedes-R23>=1`; fixture `r35-fixtures/D7`; clause mutants isolate on the all-fixed tree (`ExecClosureSuite.md` §7) | draft receipt: `wave1/ScribeQualityDraft.md` (flips D7 `0,0 open=1` → `1,1 open=0` on a copy, and the row-filtered mutant back to `0,0 open=1`); draft ground-truth-verified by `wave1/RevD5D6D7.md` §3 (R22→M34-3 at `.ufo/waves/round-34/mistakes-erratum-1.md:9-29`; R23→round-34 lesson §considerthese `corpus/lessons/round-34.md:343-358`). Fix receipt: **PENDING — flagged** (see §2); `RevC1BeforeAfter.md` §4 "D7 — NOT MET at 06:39:25Z" | **OPEN** — `supersedes-R22=0,supersedes-R23=0 open=1` |

Suite-level evidence binding all seven rows: `wave1/ExecClosureSuite.md` (plain live `closed=4/7
exit=1`; base-tree export `closed=0/7 exit=1` §4; all-fixed fixture tree `closed=7/7 exit=0` §5;
live selftest `cases=7 failures=3` exactly at D4/D6/D7 §6; all-fixed selftest `cases=7 failures=0`
§7; fake-suite rejected by the suite's own judge §8), `wave1/ExecSelftestFixtures.md`,
`wave1/MutFixturesLimbs.md` (verdict: 21/21 detector runs, every fixture isolates its own defect),
`wave1/RevSelftestFixtures.md`, `wave1/RevClosureSuite.md` (verdict: "The instrument meets every
criterion in the seat item").

### 2. Flags — defects with no fix / no check / no receipt

- **No fix: D6, D7** (both files still byte-identical to the freeze blobs; re-verified at my final
  read). Neither is unowned-in-principle: D6 has *no seat owner* (`ScribeIntegrationNotes.md` F7 —
  no executor or scribe item appends the `Correction (round 35)` note; the L1 "must either land the
  correction itself or assign it before the final commit"), and D7's append is drafted but was not
  applied to `QUALITY.md` (`ScribeQualityDraft.md` §Verdict: "the §1 block is ready to append
  verbatim"). Both are therefore **L1-integration actions**, not lost work.
- **No check: none.** All seven checks exist as `check_d1`…`check_d7`, each with a committed
  per-defect fixture under `corpus/instruments/r35-fixtures/D1..D7` (plus `clean/` and
  `two-defect/D1D2` controls) and per-clause mutants; the suite selftest on the all-fixed tree
  prints `cases=7 failures=0` (`ExecClosureSuite.md` §7).
- **No receipt: D6 only.** D1/D2/D3/D4/D5 each carry an author receipt plus at least one independent
  review; D7 carries a draft receipt (`ScribeQualityDraft.md`) whose block is verified ground-true
  (`RevD5D6D7.md` §3) but awaits the append; D6 has no author receipt and `RevD5D6D7.md`'s §4/§Verdict
  are still "pending" for it. `RevD5D6D7.md` §5 F2 records the trap for whoever lands it: the
  correction must **paraphrase** the stale sentence — quoting `did not file a receipt (dead seat`
  back into the file re-opens `check_d6` (proved by the suite's own D6 mutant).
- **Half-landed by design: D4.** Fix artifacts and receipts are complete; `tracked=0` is a
  commit-order fact that flips at the L1's integration commit (`ExecD4ResultsTrack.md` §4, and the
  simulation in `RevC1BeforeAfter.md` §6).

### 3. D5/D7 → appended erratum / supersession artifacts

- **D5 → `.ufo/waves/round-35/claims-erratum-d5.md`.** Appended correction per the freeze rule:
  neither frozen `claims.json` is edited (erratum §8; `git status` shows no claims.json
  modification). §2 records the two non-discriminating routes with exit codes (twin's own
  `recheck:` line exits 0 on the real manifest; the instrument handed the twin `.md` exits 2 for any
  non-manifest); §3 restates clause 1 **with a discriminating invocation** (fabricated quote pinned
  in a manifest against the committed capture → `MISMATCH reason=quote-not-found`, exit 1, with the
  present-quote control at exit 0); §4 restates clause 2 as a **per-id occurrences** statement
  (16×`occurrences=1`; Q9/Q17 `occurrences=2` anchored 77/96; unanchored non-unique fails
  `occurrence-not-unique`; broken anchor fails `anchor-broken`); §5 discloses the verbatim
  recurrence of both phrasings in the round-35 frozen C2 and applies the restatements by reference;
  §6 states the forward rule (future twins carry only absent sentences — round-35 `junk-f18.md`
  conforms, both sentences absent); §7 self-verifies the two literals (`grep -c` → 5 / 5).
  Advisory findings on it: `RevD5D6D7.md` §5 F1 ("byte-identical" wording vs the real entry's
  recheck line — operative claim unaffected) and F4 (the file's own digest moved after its seat's
  receipt pinned it — correct design, bookkeeping only).
- **D7 → QUALITY supersession rows (drafted, append pending).** `ScribeQualityDraft.md` §1 block:
  `R26` … grounded-in cell "supersedes R22 — R22's Grounded-in column cites M34-2, but M34-2 is the
  SCORECARD unfilled-placeholder defect (R1 class); the correct mistake is **M34-3, the
  freeze-satisfiability row** minted at `.ufo/waves/round-34/mistakes-erratum-1.md`"; `R27` …
  grounded-in cell "supersedes R23 — … the landed grounding is the round-34 lesson's own
  §considerthese disposition (`corpus/lessons/round-34.md:343-358`) rather than
  `considerthese/2026-10-25.md:76` alone". Both keep the original criterion text byte-identical
  (append-only per R6; the suite greps `supersedes R22` / `supersedes R23`, which the rows carry
  verbatim). Note the C1 freeze phrases it "supersedes-R22/supersedes-R23" (hyphen) while the check
  and the rows use the space spelling — payload names vs literals, consistent in the landed bytes.

### 4. Fit-freeze satisfiability step — recorded?

Yes — at four layers, all in committed or wave-committed artifacts:

1. **At freeze:** the before-controls `.ufo/waves/round-35/c1-controls/before.txt` (sha256
   `352d3da2…`), `c2-controls/before.txt` (`28357003…`) and `census-before.txt` (`74fc6a26…`) were
   "measured at the freeze and committed with it" — freeze commit `617496b9` is "claims freeze +
   before controls" (`ScribeIntegrationNotes.md:36-38`, `:269`). This is the round's R22 artefact
   ("a frozen claim predicate is checked for satisfiability against base bytes before freeze",
   `corpus/QUALITY.md` R22 row).
2. **Post-landing replay at the freeze export:** `wave1/ExecBeforeReceipts.md` — `git archive
   617496b9` (tar sha256 `a008adf2…`, 6934 files, `git get-tar-commit-id` confirms the commit),
   all 18 stored C1/C2 values + census replay **MATCH, 0 mismatches**, and `claims.json` byte-identical
   at freeze / HEAD / worktree (`fe0dae89…`). Independently re-done by `wave1/ScoutDatawalk.md`
   (same 19-row table, all MATCH; vacuity sweep over every counter).
3. **Vacuity / satisfiability findings recorded, then encoded as clauses:** `ScoutDatawalk.md` F-1
   (the `<LANE_HASH>` kill-rule term is vacuous at freeze — count 0 before any work) and
   `ExecBeforeReceipts.md` finding 3 (D1's second placeholder spelling `the L1 fills this line` at
   `SCORECARD.md:1129` is invisible to the frozen count) and finding 2 (a global `grep -c '201\.7'
   == 0` is unsatisfiable while the round-33 row `:1003` stands — the check must be row-scoped).
   All three are encoded in the landed suite: `check_d1` gained the `lane-hash-markers` clause and
   counts both placeholder spellings; `check_d2`'s third clause is the row-scoped byte-survival
   pattern (`ExecClosureSuite.md` §2 notes). The do-nothing direction is closed by
   `wave1/MutCounterBase.md` (no C2 counter satisfiable on base bytes; all six probes print BEFORE)
   and `ExecClosureSuite.md` §4 (base-tree run `closed=0/7 exit=1`).
4. **Residual:** `ExecBeforeReceipts.md` finding 4 — the before-controls are output-only receipts
   with no committed runner ("fourth round running" of hand-reconstruction). This is the one
  bounded improvement this seat proposes (§5).

### 5. Bounded connector proposal (one move)

**Commit a before-control runner** — e.g. `corpus/instruments/before-replay.sh --controls
.ufo/waves/round-35/c1-controls/before.txt --root <git-archive export>` — so the freeze-replay step
of §4 layer 2 is runnable by a non-author instead of hand-reconstructed (the exact ask in
`ExecBeforeReceipts.md` finding 4, recurring since round 30). Shape: a dumb argv/expected-value
table stored *beside* the frozen controls (a v2 generated by `build-spec.py` at freeze; the
frozen `before.txt` itself stays byte-identical), replayed by one instrument across rounds.
- **Axes:** depth:verifiability up — the satisfiability step becomes replayable evidence and the
  hand-reconstruction class (and its transcription slips, cf. `RevC1BeforeAfter.md` §2's own
  corrected wrapper bug) disappears; coverage and depth:density untouched (a ~100-line read-only
  script; no corpus/ledger surface changes).
- **Risks:** (a) scope creep into a second claims engine — mitigate by keeping it a table runner,
  never a counter author; (b) the v2 table must be generated at freeze time, so it cannot close
  round 35's already-frozen controls — it would first serve round 36; (c) new instrument needs its
  own do-nothing control and registration per D3's bar.
- **Verification if adopted:** run it against `git archive 617496b9` and require the same 19 MATCH
  rows `ExecBeforeReceipts.md` produced by hand, plus one forged-value row rejected.

### 6. Commands, outputs, exit codes (this seat)

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1          # suite_exit=1; identical on a second run at my final read
```

```
$ grep -c -F -- 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md ; echo $?
1 / 0                       # D6 stale sentence present
$ grep -c -F -- 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md ; echo $?
0 / 1                       # D6 correction absent
$ grep -c -F -- 'supersedes R22' corpus/QUALITY.md ; grep -c -F -- 'supersedes R23' corpus/QUALITY.md
0 / 0                       # D7 rows absent
$ git ls-files -- .ufo/waves/round-34/wave1-results.json | wc -l
0                           # D4 tracked limb open until the L1 commits
$ ls /fast/scratch/hyaku/kasegi-r35/ | grep -i connclaims ; echo $?
(exit 1, no match)          # no ConnClaims scratch tree on disk
$ ls .ufo/waves/round-35/c1-controls/ .ufo/waves/round-35/c2-controls/
before.txt  fake-suite.sh / before.txt  junk-f18.md   # freeze controls present
```

### 7. File digests (my final read; the suite and erratum are live bytes still being revised by their seats)

| path | sha256 |
|---|---|
| `corpus/instruments/r35-defect-closure.sh` | `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` (moving — `ExecClosureSuite.md` pins `d7ad8438…`/773 lines; `RevC1BeforeAfter.md` saw `cba8c95b…`/760 → `d7ad8438…`/773 during its own passes; the L1 should pin the final bytes at commit time) |
| `.ufo/waves/round-35/claims-erratum-d5.md` | `eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6` (stable across my last two reads; `RevD5D6D7.md` F4 notes the receipt-pinned `becc64c9…` went stale by design) |
| `SCORECARD.md` (D1+D2 fixes) | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` (1261 lines; = ExecD1Markers/ExecD2DensityRow final checkpoint) |
| `SKILL.md` (D3 rows) | `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc` |
| `corpus/QUALITY.md` (D7 pending) | `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` (= freeze digest) |
| `.ufo/waves/round-34/wave1/L1Integration.md` (D6 pending) | `5472f60ab33a2241e7051c071e1469ca89b2c874e571d93420499cd0998a0fd5` (= freeze digest) |
| `.ufo/waves/round-34/wave1-results.json` (D4) | `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4` (= round-34 verifier's digest) |
| `.ufo/waves/round-34/wave1-results.json.provenance.md` (D4) | `e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98` |

### 8. Summary verdict (advisory — the L1 integrates and decides)

Cross-index complete: **7/7 defects mapped** to fix artifact, suite check, and receipt. Landed and
closed: D1, D2, D3, D5 (fix + check + author receipt + independent review). D4: fix + note +
receipts landed; the `tracked` limb is the L1's integration commit by construction. **Open at my
final read: D6 (no fix, no fix receipt — L1 must append a paraphrasing `Correction (round 35)`
note; never quote the stale literal) and D7 (fix drafted and ground-truth-verified but not appended
— L1 appends `ScribeQualityDraft.md` §1 verbatim).** Until those two appends and the D4 commit
land, the frozen counter honestly reads `closed=4/7 exit=1` — the suite is green exactly where the
tree is fixed and red exactly where it is not, which is the C1 predicate's own shape. The
fit-freeze satisfiability step is recorded (freeze-committed before-controls + two independent
freeze-export replays + vacuity findings now encoded as suite clauses), with the one residual that
the replay still has no committed runner (§5).

Report: .ufo/waves/round-35/wave1/ConnClaims.md
