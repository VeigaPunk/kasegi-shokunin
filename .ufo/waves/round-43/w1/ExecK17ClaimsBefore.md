# ExecK17ClaimsBefore — round 43 K17 limb (RD42-8: claims.json before literal vs its control)

Seat: ExecK17ClaimsBefore (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base: `ab98fac9dce87130bc4f66de89e30650d63943dc`. Round-41 judged head: `1f7464612ac4c44e39886b82e812610d3c039b13`.
Round-43 freeze: `4cb6d4a` (claims frozen at 2026-10-28T16:37:07Z, read first, never edited).
Axes: depth:verifiability (primary), coverage.

## Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.sh` | 591 | `37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348` |
| `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.transcript.txt` | 92 | `ab40a06031441a5d609d25350e27479dd10c212d167f11fd49f04d48e1207f1b` |
| `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.md` (this receipt) | — | — |

Sourceable contract (verified in transcript block 9): sourcing defines functions and globals only, sets no shell options, runs nothing.
`check_k17 <export>` prints exactly one `K17 payload=... closed=0|1` line on stdout and returns 0 only when closed; evidence details
(`K17 detail ...`) go to stderr. `k17_payload <export>` prints the payload cell alone. `k17_selftest WORK TREE` drives the graded fixtures.
Standalone driver: `--export-ref <hash>` (git archive into `--work`, outside the lane) or `--tree <dir>`; a plain run refuses with exit 2.

## The rule the limb enforces

Population: every `.ufo/waves/round-<NN>/claims.json` at depth two under `.ufo/waves/` (the six fixture copies nested in
`round-25/wave1/**` are not round freezes and are not read; `claims` proves it: 20 at base, 21 at the round-43 freeze, not 26).

Whole token: `closed=<n>/<m>`, `failures=<k>`, `cases=<k>`, value = maximal digit run with at most one `/`; the character before the
key and after the value must be absent or not in `[A-Za-z0-9_/-]`. `closed=10/100` extracts as `10/100` (never `10/12`);
`closed=13/13x`, `closed=13/13/7`, `xclosed=13/13`, `closed =13/13` are not tokens.

- **`before` tokens are measurements.** A token is backed when it appears as a whole token in a cited receipt:
  `controls.c1`/`controls.c2` or a non-record path named in the cell. Not printed by any cited receipt, it must be named by a
  `claims-erratum*.md` paragraph in the SAME round dir that also carries `superseded` (verified: block 3, block 6). Otherwise
  `unbacked` -> red. A claim that cites no receipt (rounds 23-39 freezes carry no `controls` and no path) has nothing to be
  compared against and contributes no token: inventing a receipt would grade a claim against a document it never named.
- **`after` tokens are targets, not measurements.** They are extracted and near-token-checked but never counted as backed or
  unbacked. This is load-bearing, not a convenience: round-42's `after` cell carries `closed=13/13`, `failures=0`, `cases=13` and
  only `closed=13/13` is in a control receipt; round 27's `failures=0`, round 35's `closed=0/7`, round 36's `closed=9/9` are printed by
  no committed receipt at all; and the round-43 `after` cell carries `closed=13/19` (a base measurement) that no Y transcript prints.
  Grading after-cells against controls makes the frozen C1 unsatisfiable (independently reproduced by reviewer RevK17). The fixpoint
  rule is the r42 J8 canonical-mode precedent: a round's own claim cannot be evidence for the run that grades it.
- **Quotations are skipped.** A `before` token introduced by a quote verb (`quote`, `says`, `states`, `carries`, `reads`) from a
  RECORD (another `claims.json`, a `claims-erratum*`, `corpus/lessons/`, `corpus/knowledge/`) is that record's statement, counted in
  `quoted=` and not graded here. A receipt verb (`prints`, `outputs`, `tees`, `reports`) between the attribution and the literal
  cancels the exemption. The round-43 freeze's own before cell quotes `closed=10/13` from
  `corpus/lessons/round-42-verifier-spotcheck.md`/`claims-erratum-4.md` and `closed=10/12` from `round-42 claims.json`; those two
  are quotations (transcript block 5, `quoted=2`), while the round-42 claims.json that states `closed=10/12` as its own before
  literal is graded at its own turn and is the base red.
- **Near-tokens are rejected.** Two same-key whole tokens in one cell related by digit deletion (`10/12` vs `10/120`,
  `13/13` vs `1/13` — the committed r41 I3 defeat shape) make the non-printed, longer-digit twin `rejected`: excluded from
  `tokens=` and red, named in the payload (`rejected=closed=10/120`, block 4).

Payload: `claims=<n>,tokens=<t>,verified=<v>,superseded=<s>,unbacked=<u>` with `t = v + s + u`, plus `,quoted=<q>` when a
quotation was skipped, `,rejected=<tok>[+<tok>]` when a near-token was rejected and `,parse=<k>` on a malformed claims.json.
On the canonical base and green trees it is exactly the five frozen cells. Closed iff `claims>0`, `tokens>0`, `unbacked=0`, no
rejected near-token, no parse error.

## Measured evidence (all in `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.transcript.txt`)

| # | command | observed |
|---|---|---|
| 1 | `bash -n ExecK17ClaimsBefore.sh` | exit=0 |
| 1 | plain run (no `--export-ref`/`--tree`) | refuses, exit=2 |
| 2 | `--export-ref ab98fac9...` | `K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0`, exit=1 |
| 3 | `--tree <base + round-42/claims-erratum-1.md>` | `...,verified=2,superseded=1,unbacked=0 closed=1`, exit=0 |
| 4 | `--tree <base + r42 `closed=10/120` beside `closed=10/12`>` | `...,unbacked=0,rejected=closed=10/120 closed=0`, exit=1 |
| 5 | `--export-ref 4cb6d4a` (round-43 freeze) | `claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0`, exit=1 |
| 6 | `--export-ref 4cb6d4a` + round-42 erratum | `claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1`, exit=0 |
| 7 | `--export-ref 1f746461...` (round-41 head) | `claims=19,tokens=1,verified=1,superseded=0,unbacked=0 closed=1` |
| 8 | `--selftest --work <scratch>` on the base export | 6 graded fixtures, `K17 selftest cases=6 failures=0` |
| 9 | source the limb, call `check_k17`/`k17_payload` | no output at source time; `rc=1` on base; payload printed |

Base red, verbatim (block 2 — the mismatched token and both values):

```
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
```

The three graded base tokens are round-41 C1 before `closed=12/12` (printed by `round-41/c1-controls/do-nothing.txt`: "cannot print
closed=12/12"), round-42 C1 before `closed=13/13` (printed by `round-42/c1-controls/do-nothing.txt`) and round-42 C1 before
`closed=10/12` (printed by nothing; the control prints `closed=8/12`). At the round-43 freeze the population is five tokens — the
four above plus round-43 C1 before `closed=12/13` and `closed=8/12` (both printed by `round-43/c1-controls/do-nothing.txt`) — and the
two quoted defect literals are skipped.

Graded fixtures (block 8), each built under the seat's scratch from the base export:

```
K17 replay committed-defect            expected=reject observed=reject verdict=pass
K17 replay repaired                    expected=accept observed=accept verdict=pass
K17 replay erratum-without-superseded  expected=reject observed=reject verdict=pass
K17 replay near-token                  expected=reject observed=reject payload=...,rejected=closed=10/120 verdict=pass
K17 replay fabricated-value            expected=reject observed=reject payload=tokens=4,...,unbacked=1 verdict=pass
K17 replay citation-missing            expected=reject observed=reject payload=verified=1,...,unbacked=1 verdict=pass
K17 selftest cases=6 failures=0
```

(`--selftest` returns the tree's own verdict, so the block-8 command exits 1 because the tree under test is the base export; the
fixture tally is `failures=0`.)

## Findings the L1 needs

1. **One landing closes K17 at Y**: a committed `.ufo/waves/round-42/claims-erratum-5.md` (any `claims-erratum*.md` name in that dir)
   with one paragraph that names `closed=10/12` as a whole token and carries the word `superseded`. Round 43 cannot both keep
   append-only r42 bytes and close K17 without it; the r42 `before` literal is the committed defect. With that file the round-43
   freeze export measures `closed=1` (block 6). No round-43 erratum is needed.
2. **The round-43 freeze's own before cell is not a K17 defect.** It quotes `closed=10/13` (from
   `corpus/lessons/round-42-verifier-spotcheck.md:65` + `round-42/claims-erratum-4.md:9`, "with no committed transcript printing
   it") and `closed=10/12` (from `round-42 claims.json`) as defect evidence attributed to those records; both are `quoted=` and the
   quoted `10/12` is graded where it actually lives (round-42's claims.json). Grading them as round-43 measurements is what would
   make the frozen C1 unsatisfiable, so treat `quoted=2` at Y as the expected cell, not a leak.
3. **`after` cells are outside K17 by design.** `closed=19/19`, `cases=19`, `failures=0` at Y are targets measured by K1-K13 and
   the receipt; `closed=13/19` in the same cell is a base measurement with no Y backer. K18 owns quoted-value-vs-transcript; if the
   L1 wants after-cell numbers bound, K18 is the check that must carry them (it already owns `.ufo/waves/round-43/final-gates/`).
4. The round-41 judged head has no round-42/43 claims.json, so K17 is green there (`claims=19,tokens=1,verified=1`). That is data-driven,
   not a weakened rule: the 10/12 literal does not exist at that ref. The base export is the discriminating negative control.

## Bounds and risks (stated, not hidden)

- **After-cells are not graded.** A false after claim is invisible to K17 (K1-K13 grade the after state at Y). This is deliberate and
  the only satisfiable reading; it is the same class of exemption r42 J8 needed.
- **Uncited claims are outside the population.** Rounds 23-39 freezes carry no `controls` object and name no receipt path; their
  before cells (round 34: `cases=11`, `cases=0`/`failures=0`, no citation) have no cited control to compare against and are neither
  graded nor counted. The frozen wording is "the control receipt the claim cites"; K17 refuses to invent a citation.
- **Quotation exemption is contextual.** It requires a record path/`claims.json` mention before the token, a quote verb after it, and
  no receipt verb in between. A fabricated value with no attribution is graded (fixture `fabricated-value`); a value the cell says the
  control prints is graded even when the same sentence earlier quoted a record (`... says X while its own control prints Y` grades Y,
  and Y is the token the round-43 cell backs). A rewrite that adds a record attribution to a fabricated control value is not in the
  committed-defeat class and would evade — record that as the known escape and keep K18 on quoted values.
- **Near-token detection is sibling-scoped within one cell.** `closed=10/120` alone (no sibling, no printed near value) is an ordinary
  unbacked token, red but not named in `rejected=`.
- **Erratum supersession is paragraph-scoped** (blank-line-delimited block holding both the token and `superseded`; a single line
  works). An erratum that splits token and word across paragraphs does not supersede.

## Discipline

- Lane writes: only the two deliverables above plus this receipt, all under `.ufo/waves/round-43/w1/`. No tracked lane file touched
  (`git status --porcelain` shows the wave dir untracked only). No fleet-root, shokuknow, sibling-lane or source-tree write, no PATH
  write, no `~/.local/bin` write.
- Git: read-only only (`archive`, `show`, `rev-parse`, `log`, `status`). No add/commit/checkout/reset/stash/branch/tag/worktree anywhere.
- Tooling: none installed, none needed (bash + python3 already present); pacman untouched. No network fetch.
- Scratch: `/fast/scratch/hyaku/kasegi-r43/ExecK17ClaimsBefore` (export, head export, fixture trees, driver). Disk guard checked before the
  heavy pass (25% used on `/fast/scratch/hyaku`, 606.9G free). One incident, disclosed: the first transcript run used `cp -al` hardlink
  fixture trees and wrote a fixture erratum over an existing filename, which wrote through the hardlink into the scratch base export's
  `round-42/claims-erratum-1.md`. The lane was never involved; the scratch export was re-extracted and the driver now unlinks the target
  before every write; transcript block 3 proves the base export's erratum sha equals the `ab98fac` git blob
  (`d3e5e1e2a58834afcb543efdaa6f8a176dd3ce866003f2960e1aa6c4a5b37403`). Scratch removed and verified absent after this receipt was written.
- Subagents: none (leaf seat, no swarm, no second judge).
