# ExecProofSuiteSelftest — independent reproducibility proof of the r39 suite predicates

Round 39 · leaf seat · axis depth:verifiability · lane kasegi-shokunin
Base 480b1a505a2dfc14a4f718d16d63808247214d0a · claims freeze dcd31701720a6a4929a32471a62011ed87103421
Lane HEAD observed while proving: 06632fa8f569398d705a0651058191eafe602fa9 (read-only)

## Files changed

- `.ufo/waves/round-39/wave1/ExecProofSuiteSelftest.proof.txt` — deliverable.
  284 lines, sha256 `eb715dc4b3063d9d1d3a85cc09b34a2f2b2ab2396d354b68353a951f748fd3f9`.
- `.ufo/waves/round-39/wave1/ExecProofSuiteSelftest.md` — this receipt.

No lane, fleet, sibling or source-tree file was edited; no git/jj mutation was run. Read-only
`git status --porcelain` shows only the untracked `.ufo/waves/round-39/` wave artifacts.

## Behavior

A minimal throwaway reference of the two frozen C1 predicates was written in scratch
(`ref.py`, 286 lines, sha256 `b495487236a7edef5736976c2f2fd41a51154c511d81d6cdddc4426b0bf24407`,
python 3.14.8, stdlib only) and run over both wave-1 fixture packs, which were read as data:

- G1 whole-tail (`ExecWholeTailFixture.fixtures`): 5/5 fixture verdicts as documented —
  01 GREEN, 02 RED (`declared2 != added3`), 03 RED (correction only inside a fence),
  04 GREEN under the r39 backtick+tilde walk and RED under the r38 backtick-only walk,
  05 RED (declared path not in export). Plus 7/7 fence-walk probes U1–U7 and 4/4
  clause-isolation mutants M1–M4 all agree with the pack's reference model.
- G2 graded receipt (`ExecGradedSelftestFixture.fixtures`): 24/24 receipts reproduce
  `expected.tsv` payload line and exit status byte for byte (0 mismatches), including the
  five named variants (a)–(e) and 19 mutants; the pack's own runner is 24/24.
- Added-line semantics verified: `git diff --numstat` over the fixture base→head repos
  equals the reference's clause-3 count on all five G1 fixtures.

The reference was run in two G2 profiles. The pack contract rejects all 24 receipts as
specified. A profile implementing only the frozen claim's literal grading sentence
(`positive=pass` and `verdict=pass` present) still prints `closed=1` on six pack mutants
(m02, m03, m04, m05, m07, m08) — recorded as finding F2.

## Exact retained evidence (embedded in the deliverable)

- Transcript A: git-numstat vs reference added-line counts, 5/5 MATCH.
- Transcript B: G1 fixture verdicts (reference) with per-block clause detail, the r38-walk
  contrast on 04, and the pack's own `g1-check.sh` golden lines for all five fixtures
  (`export-sync=1` on each).
- Transcript C: U1–U7 walk probes, reference vs pack, plus U3 under the r38 walk.
- Transcript D: M1–M4 clause mutants, reference vs pack (both RED, one limb each).
- Transcript E: 24/24 G2 receipts, reference payload/exit vs `expected.tsv`.
- Transcripts F/G: claim-literal profile on the five named variants and the six
  false-greens it produces.
- Contract-file bindings: `expected.tsv` sha256
  `60d3b200c48ae07eb9943cd2423ebd61515e18252750cbc94c7805a12b57ec41`, `judge-g2-cases.sh`
  sha256 `73aa11f2e2e5554ed58d2ad8d4a2d201a02511aa690c6d26da592e09e6d245a9`, `g1-check.sh`
  sha256 `f56e2d02591df9cdc246b056dc4757ca759f1e123ff3ead89dddc744bb1b7e86`,
  `claims.json` sha256 `e427ab6a6ecec4b1f49ed5eed95860c468e0982af331a3a1ba135649d27e051c`.

All commands were run from `/fast/scratch/hyaku/kasegi-r39/ExecProofSuiteSelftest` with
absolute paths; the five throwaway fixture repos used for the numstat comparison were built
under that scratch dir after asserting `git rev-parse --show-toplevel` equalled the fixture
dir.

## Findings (evidence above, text in the deliverable)

- **F1** — the fence-closer length is stated two ways. The suite-build item says "exactly
  three backticks or three tildes … same type as opener"; the G1 fixture model (and
  CommonMark) says a run **at least as long as the opener**, blanks only, backtick info
  strings may not contain a backtick. Probe U1 (4-backtick opener, 3-backtick mid,
  4-backtick closer) is `closed` under the fixture model and `open` under a literal
  exactly-three closer. The landed suite must implement the fixture/CommonMark rule or it
  will misgrade U1-class documents RED.
- **F2** — the claim's literal G2 grading sentence cannot reject m02/m03/m04/m05 (detail
  corroboration), m07 (verdict field must terminate the line) or m08 (`mutants=` mandatory).
  Rejecting all of them requires the fixture pack's whole-line case regex plus the
  `mutants=<a>/<b>`/detail rule; otherwise those limbs are false-green.
- **F3** — the G2 receipts bind no header (export-ref/ancestry/digest are zeros by the
  pack's design), so fixture agreement is no evidence for the header half of G2; the real
  export run at J remains its only evidence.
- **F4** — the G1 fixtures grade clause 3 against the fixture's own `base/` (by design).
  On the real export the base must be 480b1a5… and the head J.

## Risks

- The reference is deleted with the scratch dir; only its digest and the transcripts bind it.
  The deliverable's transcripts and predicate descriptions are the durable record.
- F1/F2 are spec-text gaps the L1 must resolve when landing `r39-closure.sh`; the proof
  shows which fixtures expose each.

## Blockers

None.

## Scratch / tooling / guard

- Scratch `/fast/scratch/hyaku/kasegi-r39/ExecProofSuiteSelftest/` was created with
  `mkdir -p`, held all reference/probe/mutant/work copies, and was removed before yield;
  absence re-checked afterwards.
- Disk guard was green before the run (`/fast/scratch/hyaku` use 25%, free 609.7G).
- No tool was installed or upgraded (nothing needed).
