## Round 43 (attempt 1, fresh-start)

- Frozen claims (`.ufo/waves/round-43/claims.json`, sha256 `a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`,
  freeze commit `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`):
  C1 on axis depth:verifiability (4, held) and C2 on axis coverage (8, held; capability acquisition); both are
  asserted, not admitted, until a non-author verifier closes them. The before-controls
  `.ufo/waves/round-43/c1-controls/do-nothing.txt` (`measured-at=2026-10-28T16:32:23Z`) and
  `.ufo/waves/round-43/c2-controls/before.txt` (`measured-at=2026-10-28T16:34:15Z`) were committed before any
  round-43 data, and the freeze record `.ufo/waves/round-43/freeze.txt` (`frozen-at=2026-10-28T16:37:07Z`,
  `measured-at-max=2026-10-28T16:34:15Z`) orders the freeze after both; a do-nothing run reaches none of the
  declared after-states — the r43 suite is absent at base (`ls: cannot access 'corpus/instruments/r43-closure.sh'`)
  and the r42 suite, run as the do-nothing stand-in over the base export, prints `closed=12/13 exit=1` while the
  routed narrative defects (RD42-1, RD42-2, RD42-3, RD42-4, RD42-5, RD42-6, RD42-8) sit in committed bytes.

- C1 (depth:verifiability, 4 held): `corpus/instruments/r43-closure.sh` lands export-only — `--export-ref <hash>`
  extracts `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive <hash> | tar -x` into a work dir outside
  the lane (`--work`, `--scratch-root`), a plain run refuses exit 2, an unresolvable `--export-ref` prints its
  distinct `ref-not-found` red and exits 1 — printing one `K<n> payload=... closed=0|1` line per check K1-K19 in
  numeric order and exiting 0 only when all nineteen close; at Y the receipt
  `.ufo/waves/round-43/final-gates/all-gates.txt` records `closed=<pending: L1>` and
  `selftest cases=<pending: L1>`, the selftest printing nineteen graded
  `selftest case=K<n> ... positive=pass ... verdict=pass` lines.

- C1 . K1-K13 carried: the r42 J1-J13 bodies land as K1-K13 with their payload grammar and replay limbs
  unchanged, each replay limb re-executing its committed r41/r42 defeat artifact and requiring rejection
  (`.ufo/waves/round-43/w1/ExecCarryChecks.transcript.txt`, `.ufo/waves/round-43/w1/ExecCarryChecks.declared-blocks.txt`
  regenerating the K4 declaration block over the new paths).

- C1 . K14 (RD42-1): `ExecK14Corrections.sh` re-derives the correction ledger exactly as the r42 suite's J11 limb
  does and reds every correction-count literal in SCORECARD.md/LOG.md/SHENON.md that does not equal the
  same-export re-derivation, unless a `Correction (round 43)` line names it superseded
  (`.ufo/waves/round-43/w1/ExecK14Corrections.transcript.txt`).

- C1 . K15 (RD42-2/RD42-3): `ExecK15WaveNarrative.sh` parses each sentence in LOG.md and `corpus/lessons/*.md`
  that asserts a named `kasegi-r<NN>-<word>` wave was dispatched, requires its
  `.ufo/waves/round-<NN>/<wave>-results.json`, requires that file's seat count to equal the count the sentence
  states, and reds an unbacked sentence unless a `Correction (round 43)` line names the wave `never-true`
  (`.ufo/waves/round-43/w1/ExecK15WaveNarrative.transcript.txt`).

- C1 . K16 (RD42-4): `ExecK16Placeholder.sh` reds a `## ` section whose body promises content `when the ...
  reports` / `to be filled` / `TBD` / `pending the ... wave` and is not followed by a `Correction (round 43)`
  line naming that heading; at base it reds `corpus/lessons/round-42.md`'s `## Wave-2 falsification` paragraph
  (`.ufo/waves/round-43/w1/ExecK16Placeholder.transcript.txt`).

- C1 . K17 (RD42-8): `ExecK17ClaimsBefore.sh` extracts every `closed=<n>/<m>`, `failures=<k>` and `cases=<k>`
  token from each committed claims.json `before`/`after` cell as a whole token and requires it in the control
  receipt the cell cites, or a committed claims erratum naming it superseded
  (`.ufo/waves/round-43/w1/ExecK17ClaimsBefore.transcript.txt`); the round-43 claims erratum
  `.ufo/waves/round-43/claims-erratum-1.md` names round-42 C1's cell superseded.

- C1 . K18 (RD42-5): `ExecK18Transcript.sh` requires every `closed=<n>/<m>` and `selftest cases=<n> failures=<k>`
  value quoted in the round-42/43 lane records to appear as a whole token in a committed transcript under a
  `final-gates/` or `c1-controls/` root, or to carry `report-only`, or to be named superseded; the missing
  backing is supplied by `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`, the unedited tee of
  `bash corpus/instruments/r42-closure.sh --export-ref de09313e8edb98280b19767d0094bb2dd8031d73`
  (`.ufo/waves/round-43/w1/ExecTranscriptDe0931.md`).

- C1 . K19 (RD42-6): `ExecK19Freeze.sh` requires one `measured-at=<ISO Z>` line per control receipt,
  `frozen_at_utc` not earlier than the latest of them, a committed `freeze.txt` `frozen-at=` line equal to it, and
  the `claims-sha256` to bind the claims bytes; its transcript records base
  `K19 payload=freeze=absent,order=bad,sha=mismatch closed=0` and the round-43 freeze commit
  `K19 payload=freeze=present,order=ok,sha=match closed=1`
  (`.ufo/waves/round-43/w1/ExecK19Freeze.transcript.txt`, format `.ufo/waves/round-43/w1/ExecK19Freeze.freeze-format.txt`).

- C1 . negative controls and receipt: `ExecNegCtlReceipt.sh` re-invokes the suite over exports of base
  `ab98fac9dce87130bc4f66de89e30650d63943dc` and round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13`
  (each `closed<19/19 exit=1`), over a plain run (exit 2) and over an unresolvable ref (`ref-not-found`, exit 1),
  and rejects a receipt that is payload-contradicting, foreign-ref, future-dated, summary-only, tampered or
  composed of two runs (`.ufo/waves/round-43/w1/ExecNegCtlReceipt.md`).

- C2 (coverage, 8 held; capability acquisition): `corpus/instruments/claim-package-check.py` gates the six-file
  claim-package contract with eight rules — R-FILES, R-MANIFEST, R-REDACT, R-CUSTODIAN, R-PROVENANCE, R-STATUS,
  R-REPORT, R-NOSECRET — printing one `RULE <id> verdict=pass|fail detail=...` line each and
  `package=<path> rules=8 pass=<k> fail=<m> verdict=WELL-FORMED|DEFECT`, exit 0 only when all eight pass; it
  reads only files beneath the package root it is given, recomputes every digest and rejects an escape or a
  symlinked contract file (`.ufo/waves/round-43/w1/ExecGateManifest.transcript.txt` shows
  `R-MANIFEST verdict=fail detail=... digest-bad=1 escape=0 missing=0 shape=0 fail=digest-mismatch` on an artifact
  whose digest does not match and `R-FILES verdict=fail detail=... notregular=1 fail=not-regular-file` on a
  symlinked file).

- C2 . exemplar: `corpus/instruments/fixtures/claim-package/exemplar/` is built from S067, the curl project's own
  security advisory for CVE-2023-38545 captured this round — HTTP 200, 0 redirects,
  `fetched_utc=2026-10-28T16:39:59Z`, raw 13940 B sha256
  `e9038f569b4dfe6b9fc0e2b8e984bba908f093254de4f928c636d98ae3372a30`, normalized 6446 B / 131 lines with sha256
  `327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b`, landed at
  `corpus/source-snapshots/round-43/S067.txt` with its `manifest.json`
  (`.ufo/waves/round-43/w1/ExecSourceCapture.provenance.txt`); `claimable` stays false and the operator gates are
  named in `claim_checklist.md`.

- C2 . nine defect fixtures and graded selftest: `corpus/instruments/fixtures/claim-package/defect-*/` each fail
  exactly their own rule (missing sixth file, wrong artifact digest, negative-only polarity, path escaping the
  package, empty redactions, custodian head mismatch, reviewer equal to producer, report without
  `No submission performed`, secret-shaped token), and the gate's `--selftest` grades the nine classes plus a
  degenerate always-pass control it rejects (`.ufo/waves/round-43/w1/ExecGateSelftest.transcript.txt`,
  `.ufo/waves/round-43/w1/ExecGateFixtures.index.txt`).

- C2 . registry, capture and counters: `corpus/SOURCES.md` 66 → 68 rows — S067 `mined` from that capture
  (used-by `corpus/knowledge/claim-package-gate.md`) and S068 `rejected` with reason plus flip
  (`.ufo/waves/round-43/w1/ExecRegistryRows.rows.txt`); `capture-binding-check.py` prints
  `records=57 bound=57 unbound=0`; `recheck-audit.py --quiet` prints `expected=62 missing=0 unexpected=0`;
  `frontier-recheck-count.py` prints `entries=28 pass=28 exit=0` (no F-row moves this round); the census exits 0
  with only the standing `W04 S028`/`W04 S029` and `ok`.

- C2 . knowledge and capability: `corpus/knowledge/claim-package-gate.md` enters with its provenance trio
  (registry row citation, capture manifest, source-recheck pass) and knowledge moves 61 → 62; the capability row
  `claim-package-gate` enters `SCORECARD.md` with the exemplar command as its evidence pointer
  (`python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar`).

- Repairs (round-42 verifier spot-check §7): RD42-1 the stale correction-count cell at `SCORECARD.md:1634`;
  RD42-2/RD42-3 the unbacked round-42 wave-2 narrative in LOG.md and `corpus/lessons/round-42.md`; RD42-4 the
  round-42 lesson's `## Wave-2 falsification` paragraph — each closed by an end-of-file
  `Correction (round 43)` block (`ScribeCorrections.scorecard.txt`, `ScribeCorrections.log.txt`,
  `ScribeCorrections.lesson42.txt`), RD42-5 by the `r42-at-de09313` transcript and RD42-8 by the claims erratum;
  no existing line is rewritten (R9).

- Mistakes: minted in `corpus/lessons/round-43.md` §Mistakes, with the criteria the round mints appended to
  `corpus/QUALITY.md` — narrative-vs-evidence binding, freeze-record ordering, a capability row needs its run,
  and an exemplar's `claimable` state is operator-owned.

- Assimilation: audited this round (`.ufo/waves/round-43/w1/ScoutAssimilation.md`); nothing adopted
  (`Assimilation: none`). The sibling screen finds the claim-package gate disjoint — no sibling lane owns a
  claim-package gate, a six-file contract checker or a disclosed-report-to-package workflow
  (`.ufo/waves/round-43/w1/ScoutSiblingOverlap.md`).

- considerthese: the round's `considerthese/2026-10-26.md` proposals and their dispositions in
  `corpus/knowledge/considerthese-proposals-ledger.md` — ledger row appended.

- Wave shape: one v2 wave `kasegi-r43-hyaku`, 73 seats dispatched — executor 23, reviewer 11, scribe 10,
  scout 9, critic 7, mutation-tester 5, connector 2, sentinel 2, revenger 2, simplifier 2
  (`.ufo/waves/round-43/w1-dispatch.json`, `counts.spawn` 73); attack share 23/73 = 31.5% (reviewer 11 plus
  critic 7 plus mutation-tester 5); dead seats: `<pending: L1 reads kasegi-r43-hyaku-results.json>`
  (`.ufo/waves/round-43/kasegi-r43-hyaku-results.json`, `seats` 73).

- Trend — expansion: improved. Registry 66 → 68 (one mined, one rejected with its flip), knowledge 61 → 62, and
  one executable capability enters (`claim-package-gate`); the frontier is held at 28 rows rather than widened,
  and the census stays at the two standing W04 warnings plus `ok`.

- Trend — quality: improved. The routed narrative defects that sat in committed bytes while the r42 suite was
  green (RD42-1 through RD42-8) are now machine-graded by K14-K19, each red at base and each built to reject a
  mutant made from the committed defeat bytes; the transcript at `de09313e8edb98280b19767d0094bb2dd8031d73`
  closes the one quote that had no backing.

- Trend — discernment: improved. The gate is exercised against its own exemplar and nine deliberate defects, its
  selftest rejects a degenerate always-pass gate, and `claimable` is left false with the operator gates named —
  the round reports what its instrument can show, not a verification it did not run.

- Tooling: no pacman transactions (host-wide pause); package/install moves: none this round.

- Planned for round 44 (not a claim): (1) depth:verifiability — put the K1-K19 predicate to a non-author
  verifier's spot-check, carry any new routed attack finding into round-44 fixtures, and keep every replay limb
  live; the 4 → 5 gap stays gated. (2) coverage — decide the remaining candidates from the S067/S068 screen,
  keep F24 parked until the L0 ruling, and hold the measure at 1.000.

