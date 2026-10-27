# RevFreshStart — round-41 wave-1 fresh-start discipline review (receipt-only item)

Seat: RevFreshStart (leaf, reviewer). Scope: verify the round-41 frozen claims avoid the exact failure
modes of the three rejected closures (r38 self-referential predicate; r39 records overstate receipts;
r40 kill rule fires on committed fixtures), and that the do-nothing controls were scored BEFORE data and
are committed. Verdict per item; no deliverable files (receipt-only item).

Inputs read: `.ufo/waves/round-41/claims.json` (live; freeze errata applied), `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md`
(committed 96dbd5f, declared authoritative), `corpus/lessons/round-38-verifier-spotcheck.md`,
`corpus/lessons/round-39-verifier-spotcheck.md`, `corpus/lessons/round-40-verifier-spotcheck.md`,
`.ufo/waves/round-41/c1-controls/do-nothing.txt`, `.ufo/waves/round-41/c2-controls/before.txt`,
`.ufo/waves/round-41/census-before.txt`, `.ufo/waves/round-40/wave2/CritKillRule.md`.

Freeze errata in force (L1, CORRECTIONS-L1.md committed at 96dbd5f; confirmed by me):
- Base is the 40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (prefix 5b29ea14). The freeze files wrote
  a 38-char literal missing `f0`. Verified: `git rev-parse 5b29ea1` →
  `5b29ea1439450b712581edf5f0f0bf98dfb262ab`; `git rev-parse --verify 5b29ea1439450b712581edf5f0bf98dfb262ab`
  → `fatal: Needed a single revision` (unresolvable). The 38-char also appears in my dispatched seat spec;
  I used the 40-char everywhere.
- I11 target is the EIGHT committed CritKillRule states F1–F8 (`grep -c '^### F'` → 8), payload
  `escapes=8 red=8`.

---

## Item 1 — r38 mode: frozen self-referential predicate. Is the r41 `judged_head_rule` satisfiable by a commit that cannot name itself?

r38 failure (spotcheck §C1, and lesson R1 at line 155): G2 required the receipt *inside* the export at
judged head J, while the judged-head rule made J the receipt's own `export-ref`; J cannot contain the
receipt that names it, so the frozen counting command could never print `closed=8/8` over J.

r41 rule (claims.json line 19): "J is the lane commit that carries every round-41 change except the
receipt; the lane tip Y adds only the receipt (.ufo/waves/round-41/final-gates/all-gates.txt). Lane files
never name J by hash (a commit cannot contain its own hash); the report names J and Y. Counting commands
over the suite run at Y; negative controls run at base … and round-40 judged head
c7aea5ef97902f38289cbdc1cf267068876a62dd."

VERDICT: AVOIDED — the rule is satisfiable. Evidence and reasoning:

1. The counting command is `bash corpus/instruments/r41-closure.sh --export-ref <Y>`; Y's hash is supplied
   externally by the verifier. No lane file needs to contain Y's (or J's) hash — the explicit sentence
   "Lane files never name J by hash" is the fix for r38's impossibility, and it is enforced by the C1
   kill rule, which contains no "lane file names J/Y" clause to trip over.
2. The receipt at Y does not name the ref by hash. I2 (claims.json line 26) requires the receipt to be
   "the teed transcript of BOTH the suite run and the graded selftest at Y, with `time-basis=ref-commit`
   and run-utc equal to the ref's committer instant" — a timestamp the committer controls
   (GIT_COMMITTER_DATE; the freeze commit itself uses a controlled `-03:00` instant), not a self-naming
   hash. Precedent verified: the r40 receipt names `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd`
   (J7, a commit that predates the receipt commit d0fe34d — `git show d0fe34d:.ufo/waves/round-40/final-gates/all-gates.txt`
   header confirmed).
3. J is defined structurally ("carries every round-41 change except the receipt"), checkable by
   `git diff --name-only J Y` without naming J inside any file — same construction the r38/r39/r40
   spotcheck paragraphs used to state J and Y externally.
4. The Y-level fixpoint (receipt = transcript of the run over the tree containing that receipt) is
   consistent because suite output is required to be deterministic (no wall-clock basis — time comes from
   the ref's committer instant) and byte-identity is checked by an external re-run tee at verification
   (kill rule: "the receipt at Y not byte-identical to the teed transcript of the run that produced it"),
   not by self-inclusion of a hash. Nothing in the predicate or kill rule requires a lane file at Y to
   contain Y's own hash; r38's impossibility is therefore not reintroduced.

## Item 2 — r39 mode: records overstate receipts. Does any r41 claim quote values without a committed transcript at freeze time?

r39 failure (spotcheck §C1 + §5 R2 line 168, R3 line 174): SCORECARD/LOG/SHONEN/the lesson stated C1
`closed=8/8 exit=0` / `selftest cases=8 failures=0` at Y while the committed receipt at Y read
`closed=7/8 exit=1` / `failures=1`; the report quoted control values (`closed=2/8 exit=1`) that no
committed transcript contained (actual `1/8`).

VERDICT: NONE FOUND — no r41 claim quotes an observed run value lacking a committed transcript.

1. Every before-value traces to a committed control file cited by name: C1 `before[]` cites
   `c1-controls/do-nothing.txt`; C2 `before[]` cites `c2-controls/before.txt`. I read both at HEAD and in
   the working tree; their contents match the claims (suite absent / exit=127; frontier 23 / no F24 /
   registry 62 / no S063 / entries citing S063 0 / knowledge 59 / harness `entries=26 pass=26` /
   binding `records=54 bound=54` / audit `expected=59` / census exit 0 W04 S028,S029 only).
2. All after-values (`closed=12/12 exit=0`, `selftest cases=12 failures=0`, `entries=27 pass=27`,
   `records=55 bound=55`, `expected=60`, etc.) are declared as future-facing predicate targets verified
   by the listed counting commands — none is asserted as an observed past run. At freeze time no such run
   exists or is claimed to exist.
3. The structural gap that produced r39-D2/r40-D2 (a Y-level selftest tally with no transcript) is closed
   in the claim itself: I2 requires the receipt at Y to be the teed transcript of BOTH runs, and the kill
   rule fires if it is not byte-identical to that tee. Quoting the tally without the committed tee would
   now itself trip the kill rule.
4. The named evidence in I1 and the kill rule is file-named, already committed, and exists on disk:
   `.ufo/waves/round-40/wave2/{RevC1Counters.defeats.txt,MutH1H5.md,MutH6H10.md,CritKillRule.md}` (ls
   confirmed) and `corpus/lessons/round-40-verifier-spotcheck.md` §5 — no hash-of-J naming anywhere.

Freeze-quality caveat (not the r39 mode, recorded for honesty): the freeze-committed claims.json and
do-nothing.txt carried the 38-char base literal that resolves to no object; the L1 erratum (CORRECTIONS-L1.md,
committed 96dbd5f; appended line in the working-tree do-nothing.txt) corrects it and states the control
verdict (suite absent, exit=127) is unchanged. This is a transcription defect, not an overstated receipt.

## Item 3 — r40 mode: kill rule fires on committed fixtures. Does the r41 predicate bind the wave-2 defeat fixtures as MUST-RED?

r40 failure (spotcheck §C1 + lesson D1 line 176): the lane's own committed wave-2 artifacts showed
checks passing while their defects were present (T2 substring values, T4 fenced pseudo-row, T7 symlink
out-of-export declaration, T13 mention-only row, T14 + CritKillRule script escapes, MutH6H10 leaf-capped
green base); the frozen clause "a committed fixture shows a check passing while its defect is present"
fired; the lesson then narrowed the clause after landing.

VERDICT: BOUND — the r41 predicate freezes the fixture set as MUST-RED before the suite exists, each
fixture class bound to a named check limb, in BOTH directions (predicate limbs and kill rule).

1. Predicate limbs (claims.json line 26): I3 rejects the r40 substring defeat fixtures `closed=7/80` /
   `failures=10` by the value limb (T2); I4 fence-aware line anchoring (T4); I5 readlink-canonicalized
   declared-block paths under the export root (T7); I6 case/separator-insensitive recursive dot-inclusive
   fail-closed scratch scan (T14 + CritKillRule); I7 well-formed SKILL.md registry row, mention-only
   rejected (T13); I8 per-variant forgery flags, not count-relative (MutH1H5); I10 leaf-capped green base
   rejected by a real numeric comparison, M-H8a-class mutation killed by the graded selftest (MutH6H10
   D2); I11 every committed CritKillRule escape state reds its limb.
2. Kill rule (line 27) repeats the binding verbatim: "a committed fixture shows a check passing while the
   defect it names is present — including the round-40 defeat fixtures T2 … T4 … T7 … T13 … T14 (H6
   case/separator escape), the CritKillRule escape states, the MutH6H10 leaf-capped green base, and the
   MutH1H5 count-relative forgery" — symmetric binding; a pass-with-defect on any of them kills C1. There
   is no room for the r40 post-hoc narrowing: the fixtures are named in the frozen text.
3. Fixture bytes verified present: `grep -c '^### F' .ufo/waves/round-40/wave2/CritKillRule.md` → 8
   (F1–F8, headings read); `RevC1Counters.defeats.txt`, `MutH1H5.md`, `MutH6H10.md` exist; the r40
   spotcheck §C1 independently lists the same T2/T4/T7/T13/T14 and MutH6H10-D2 fixture evidence.
4. Count correction: the freeze text said "seven" escape states; the committed file carries EIGHT. The L1
   correction (claims.json lines 77–78, committed CORRECTIONS-L1.md) strengthens I11 to
   "escapes=8 red=8 naming F1–F8 — predicate semantics strengthened to the committed evidence, not
   narrowed". Residual cosmetic defect: the predicate sentence ("each of the seven committed …") and the
   kill-rule sentence ("the CritKillRule seven escape states") still contain the stale "seven" literal;
   both are governed by the appended authoritative correction, but the L1 should rewrite the two literals
   when landing to remove the internal inconsistency.

## Item 4 — do-nothing controls scored BEFORE data and committed

VERDICT: CONFIRMED.

- Commit order (read-only git): `fbba3d96 2026-10-27T05:07:54-03:00 round-41: claims freeze … + do-nothing
  controls + census baseline` → `b3b08b2 05:17:06 wave-1 build spec (60 seats) + dispatch` → `96dbd5f
  05:26:15 freeze errata`. `git show --stat fbba3d96` touches only the four freeze files (claims.json,
  c1-controls/do-nothing.txt, c2-controls/before.txt, census-before.txt).
- No round-41 data is committed: `git diff --name-only 5b29ea1439450b712581edf5f0f0bf98dfb262ab HEAD -- corpus/`
  → empty; all seat data lives in the untracked `.ufo/waves/round-41/wave1/` and working-tree
  modifications. The controls therefore predate every produced datum.
- Control contents match the claims' `before[]` values (quoted in item 2); the census baseline is exit 0
  with only the standing W04 S028/S029 warnings, matching the C2 kill rule's allowance.
- Post-freeze edits to the control files are erratum-only (base-hash correction), committed durably in
  CORRECTIONS-L1.md at 96dbd5f; the appended working-tree line in do-nothing.txt repeats it.

## Residual risk and verification gaps

1. Byte-identity fixpoint (item 1) is the fragile construction point: it requires the L1 to commit the
   receipt as the unedited tee (r39 R1 lesson) with a controlled committer instant, and the suite output to
   be receipt-payload-insensitive and deterministic. Satisfiable in principle (no self-naming hash is
   required anywhere); execution is the L1's to land. If the suite's I2 line echoes receipt bytes into its
   output, the fixpoint could fail to converge — recommend the L1 dry-run the receipt convergence before
   filing Y.
2. Stale "seven" literals in the I11 predicate/kill-rule sentences vs the authoritative "eight" correction
   (item 3.4): low severity while CORRECTIONS-L1.md governs; should be rewritten to avoid a future reader
   binding only seven states.
3. My item is receipt-level review; I did not run `corpus/instruments/r41-closure.sh` (it does not exist
   yet — wave-1 is building it) and did not re-execute the C2 instruments; closure-time verification
   remains with the round-41 verifier per protocol.
4. Claims freeze time field (`frozen_at_utc 2026-10-27T09:05:00Z`) postdates the freeze commit instant
   (08:07:54Z); immaterial to the before-data ordering, noted only for exactness.

Tooling: no installs/upgrades needed (read-only review with git/grep/cat). Network: none.
