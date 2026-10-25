# RevQ9Q13 — dedupe check of the round-25 QUALITY additions

Seat `L1Kasegi25.RevQ9Q13` (reviewer, READ-ONLY). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. No production edit; no VCS write; no subagent or
background job started. Working tree was **dirty and moving** while I measured (sibling seats editing
`corpus/knowledge/*.md`, the untracked instrument, and `corpus/QUALITY.md` itself), so every dedupe claim
below rests on committed or pinned bytes, named by sha.

The two planned rows were **already landed** by the time I read the file: `corpus/QUALITY.md:76` (Q10)
and `:77` (R13), section heading at `:68`. So this report checks the landed text as well as the plan.

## 0. Verdicts

| planned row | landed as | closest existing row(s) | verdict |
|---|---|---|---|
| recheck-line form | Q10, `corpus/QUALITY.md:76` | **Q7** (co-closest Q1; R12 is the binding row, not the form row) | **new criterion justified** |
| counter-instrument limb isolation | R13, `corpus/QUALITY.md:77` | **R11** (R10 next; R7/R3 already own 2 of R13's clauses) | **new criterion justified** — for the limb-isolation conjunct only |
| optional vendor-policy row | not minted (correct) | **Q4** (+Q3, R12) | **fold into Q4** — agrees with the landed decision |

No existing row covers either addition. But both landed rows carry conjuncts that *are* already in the
file, and one landed row cites an instrument that no longer exists in the form it cites (finding F-1).

---

## 1. Planned addition A — recheck-line form → Q10

### 1.1 Closest existing rows, quoted verbatim

**Q7** (`corpus/QUALITY.md:48`) — the nearest, and the one the plan asked about:

> An executable recheck field contains a command, not prose beginning “On each”. Its successful output
> names what was checked: a pinned captured-source comparison is not a fresh network verification. At
> least one missing/corrupted-source control must fail.

**Q1** (`:14`) — the row that *defines* the field's content, and the row whose wording the defect used:

> … `recheck:` (date or cadence plus the runnable command or URL anchor that re-verifies it, failing
> closed when the base is absent).

**R12** (`:66`) — nearest on what a recheck must *point at*, silent on form:

> A recheck line is measured against the entry that owns it: its `--source` ids must cover the entry's
> header `source:` ids and be cited by the entry, and the named manifest must list them. A line pointing
> at another entry's capture, at `true`, or at `--selftest` is not a recheck.

**Q9** (`:64`) — checked and excluded: Q9 binds *captured-source assertions* (path stem = id, quote
exactly-once or `anchor`, occurrence count printed). It never reads a `recheck:` line as a program.

### 1.2 What those rows leave out — measured, not argued

All numbers from the frozen receipt `.ufo/waves/round-25/c1-before.json` (sha
`3e3eeb4e39f0d6200ad521fc02fd1c970c872c9e73b5c2ec8868e66c8b2d877e`; `lines=35 pass=6
fail-closed=23 failing_limbs={parse:23, cwd:6, paths:0}`):

| gap | measurement | why no existing row sees it |
|---|---|---|
| Q7 has no **parse** limb | 23/35 lines fail `bash -n`; those 23 are exactly the `class=fail-closed` set | Q7 forbids one prose *shape* (“On each”) and asks that a command be **present**. Each of the 23 contains a command; the syntax error comes from the trailing parenthetical. Measured: `bash -n -c 'on-restoration — true'` → **exit 0**; with `(fails closed today: base absent)` appended → **exit 2**. |
| Q7's **control** clause rewards the defect | the same 23 lines fail closed, so “at least one missing/corrupted-source control must fail” is satisfied *by* the 23 lines that do not parse | a corpus of 35 prose hybrids that never parse satisfies Q7 |
| Q7 has no **cwd** limb | 6/35 lines: `lane_exit=0`, `foreign_exit=2` | these 6 are Q7-clean: they are commands, their successful output names the `--source` ids checked, and a failing control exists elsewhere in the corpus. R12 is also satisfied for 5 of the 6 (header `source:` id ⊂ `--source` ids, manifest lists them — measured: S001/S003/S006/S009/S013; `citation-bases.md` has no header `source:` so R12 is vacuous there). |
| Q1 **licenses** the failing form | 23/35 lines begin `on-restoration — …` and end in a parenthetical | Q1's own words are “date or cadence **plus** the runnable command … failing closed when the base is absent” — the prefix and the parenthetical are Q1-conforming |
| no row requires the named `corpus/` path to **exist** | `paths_fail=0` at base, so no live counterexample | the frozen predicate's limb (c) is unrepresented in the bar; a line naming a deleted instrument would satisfy Q7/R12 |

Also measured at base: **5/35** lines carried the `cd … &&` prefix (D24-5's figure, confirmed), and
**2/35** name only a `~/Projects/` base test with no `corpus/` token (`repo-git-state.md`,
`root-loss-2026-10-12.md`) — so the criterion must keep the base-test alternative open.

### 1.3 The landed Q10 vs the frozen predicate it claims to state

Landed text (`:76`) covers parse, the `cd <lane-root> &&` mechanism and the trailing `#`. It does **not**
state frozen limb (c): *names a lane-relative `corpus/` path or a `~/Projects/` base test, and every
named `corpus/` path exists*. No live counterexample exists at base (`paths_fail=0`), so this is a spec
gap, not an observed failure — but the row's grounding says it measures the C1 surface, and one of the
three limbs is missing from the bar.

### 1.4 Proposed row (verbatim, 44 words) + grounding pointer

```
| Q10 | A `recheck:` line is one shell command that parses under `bash -n`, runs cwd-independently (same
exit status and combined-output digest from `/`, usually via `cd <lane> &&`), keeps notes after `#`, and
names a lane-relative `corpus/` path that exists or a `~/Projects/` base test. |
```

`grounded in`: `` `.ufo/waves/round-25/c1-before.json` (sha `3e3eeb4e…`, `lines=35 pass=6 fail-closed=23`,
`parse_fail=23 cwd_fail=6 paths_fail=0`; 5/35 prefixed, and the 6 cwd lines are `lane=0/foreign=2`);
D24-5 in `corpus/lessons/round-24-verifier-spotcheck.md` §6. Extends Q7, which forbids one prose shape and
asks only that a command be present; moves Q1's “date or cadence plus” prefix into the trailing `#`; the
`~/Projects/` alternative is load-bearing for 2/35 lines. ``

Word count measured programmatically: **44**. Delta from the landed row: adds the existence/base-test
conjunct (frozen limb (c)); states cwd-independence as the property with the `cd` prefix as its usual
spelling (an absolute-path command that is cwd-independent is not rejected); keeps the `#` note rule.

### 1.5 Verdict

**new criterion justified.** Folding into Q7 would mean rewriting a round-23 row whose grounding is a
different mistake (five prose rechecks exiting 2), and the round's own instruction is append-only (R6);
folding into Q1 would mean rewriting the row that licenses the defect. Q10's novelty is the parse limb,
cwd-invariance, and path existence — none present in any of Q1–Q9 or R1–R12. The overlap that *does*
exist (“a prose sentence with a command appended … is not a recheck” restates Q7's prohibition) should be
named in the grounding column so a later reader does not read Q7 and Q10 as two independent discoveries.

---

## 2. Planned addition B — counter-instrument limb isolation → R13

### 2.1 Closest existing rows, quoted verbatim

**R11** (`:65`, as corrected this round) — nearest:

> A counter's instrument is part of the claim: the round publishes its discrimination against degenerate
> and mutated instruments, not only its pass count. A matrix that a bound-8 brace mutant passes
> identically to the real fix proves the matrix does not exercise that bound — say so in the receipt.

**R10** (`:58`) — nearest on fixture coverage:

> A fixture matrix is evidence only for the bytes it actually exercises: an escape class reached by a code
> path the matrix never enters (an absolute spelling, an expansion branch, a bare-root citation) is
> unpinned, and the matrix note must say which spellings it does and does not cover.

**R7** (`:49`) and **R3** (`:37`) — already own two of R13's clauses:

> R7: Freeze an axis claim against its registered detector before implementation. … instrument-correctness
> claims must change and exercise the actual detector …
>
> R3: An instrument verdict names its matcher and definition; “frozen” names both byte inputs and the
> filesystem definition, and replays publish every divergent definition.

### 2.2 The gap

R11's and R10's remedy is **disclosure** — “say so in the receipt”, “must say which spellings it does and
does not cover”. Neither requires a fixture that fails **exactly one** limb, so a suite whose fixtures each
fail two limbs is R11/R10-clean while proving nothing about either limb. R7 already binds “one frozen
instrument” and “an unchanged instrument is not the fix”; R3 already binds naming the frozen bytes.
So R13's genuinely new conjunct is **per-limb isolation**, and the rest of the landed row is a restatement
of R7/R3/R11 that must be marked as such, not counted as new coverage.

### 2.3 What the specimen actually isolates — measured

The landed R13 cites `corpus/instruments/recheck-audit.py --selftest` as the specimen. That file is
**untracked and was rewritten at least four times during this wave**:

| revision | sha256 | state I measured |
|---|---|---|
| frozen pin (`.ufo/waves/round-25/c1-instrument-digest.txt`) | `d07af435…b564d6` | 4-case selftest, `cases=4 failures=0 exit=0`; the revision `c1-before.json` was produced by |
| mid-wave | `efbd18ee…676d` | 6-case selftest, `cases=6 failures=0 exit=0` |
| at 05:34:28 (13,037 B) | `4475d2e6…cccc` | 11-case selftest, **`cases=11 failures=4 exit=1`** — fails on its own bytes |
| at 05:39:56 (13,783 B), current at write | `1ccee066…1c82` | 12-case selftest, `cases=12 failures=0 exit=0`, and it declares its own gap: `completeness lines=11 total=13 complete=False ok` |

Mutant matrix I ran against the `efbd18ee` fixture set (in-memory replicas of its six fixture lines; the
replica's baseline verdicts matched all six expectations, so the replica is faithful):

| mutant | fixture suite | base corpus (`c1-before.json`) |
|---|---|---|
| `parse_ok → True` | **survives** (`prose.md` still fails `paths`) | flips 23 entries (`pass 6→29`) — load-bearing |
| cwd limb → `True` | caught (`cwd.md`) | flips 6 entries — load-bearing |
| `paths` limb → `True` | caught (`ghost.md`) | `paths_fail=0` → **nothing flips** |
| digest half dropped (`rc` only) | **survives** | 0 entries where rc-equality differs from digest-equality → **nothing flips** |
| always-PASS (all limbs `True`) | caught (`prose`, `cwd`, `ghost`) | — |

Corroborated independently by `.ufo/waves/round-25/wave1/MutAuditLimbs.md` (mutants a–e at the frozen pin
`d07af435`): parse flips 23, digest half flips 0, paths flips 0, the summary-counter mutant inflates the
headline to 29, and the composite parse+cwd mutant prints exactly the claim target `pass=35 exit=0` on
**unchanged** base bytes. Its finding 5 is the same one I measured: mutant (a) “sails through the
selftest”.

Against the **current** revision `1ccee066` (seven strict limbs, suite green), forcing each limb `True`
inside its own `--selftest`:

| limb forced `True` | selftest | reading |
|---|---|---|
| `cdroot`, `cwd`, `own`, `paths` | `rc=1` **CAUGHT** | isolated by a fixture |
| `parse` (`parse_ok → True`) | `rc=0` **SURVIVES** | not isolated — `prose.md` fails `parse` *and* `paths` |
| `instrument` | `rc=0` **SURVIVES** | not isolated |
| `artifact` | `rc=0` **SURVIVES** | not isolated |
| digest half of `cwd` (`run` returns a constant digest) | `rc=0` **SURVIVES** | not isolated — no fixture has equal exit status with divergent output |

Consequence for the landed row: **the specimen named in R13 does not satisfy R13.** At `efbd18ee` the
suite isolated `cwd` and `paths` only; at `1ccee066` it isolates four of seven strict limbs and neither
the `parse` limb (the one that owns 23 of 35 verdicts) nor the digest half of limb (b). At `4475d2e6` it
did not even pass. And the instrument no longer matches its frozen pin, which is the exact condition R13's
first clause forbids. The suite's own `completeness complete=False` line is the honest form of this, and
it is the shape R13 should be grounded on — a declared gap, not implied coverage.

Two fixtures close both gaps (measured against `efbd18ee` bytes; each fails exactly one limb and nothing
else — `strict` vectors `{'parse': False, 'cwd': True, 'paths': True}` and
`{'parse': True, 'cwd': False, 'paths': True}` with `lane/foreign = 0/0` and divergent digests):

```
parse-only.md : recheck: on-restoration — python3 corpus/instruments/tool.py corpus/knowledge/parse-only.md (fails closed today: base absent)
digest-only.md: recheck: python3 corpus/instruments/tool.py corpus/knowledge/digest-only.md; test -e corpus/knowledge/digest-only.md || echo MISSING
```

With those two added, `parse_ok → True` and digest-half-off are both caught (measured). Neither is in the
landed instrument, and the file is not this seat's write scope.

### 2.4 Proposed row (verbatim, 37 words) + grounding pointer

```
| R13 | A counter's before and after come from one frozen instrument whose limbs are each shown
load-bearing by an isolating fixture (one that fails that limb and no other); a discrimination figure is a
measurement, not a construction. |
```

`grounded in`: `` `.ufo/waves/round-25/wave1/MutAuditLimbs.md` (mutants a–e at pin `d07af435…`,
`.ufo/waves/round-25/c1-instrument-digest.txt`): parse flips 23 verdicts, the cwd digest half and the paths
limb flip none, and the composite mutant prints the claim's own target on unchanged bytes;
`.ufo/waves/round-25/c1-before.json`; this report §2.3 (suite isolates `cwd`/`paths`, not `parse`, not the
digest half). R11/R10 permit disclosing such a blind spot; R7/R3 already bind the frozen-instrument clause. ``

Word count measured: **37**. Delta from the landed row: drops “An unchanged or vacuous instrument is never
cited as the fix” (already R7's “must change and exercise the actual detector”) and keeps the isolating-
fixture definition and the measurement-not-construction clause.

### 2.5 Verdict

**new criterion justified** — but only for the limb-isolation conjunct. R13 must (a) name the instrument
by sha256 at the measured revision, not by path, because the path's bytes changed twice under this wave
and the file currently fails its own selftest; (b) not imply the cited specimen isolates every limb until
the two fixtures above land; (c) mark the frozen-instrument and unchanged-instrument clauses as restating
R7/R3.

---

## 3. Optional third row — vendor-policy admission

**fold into Q4.** Q4 (`:17`) already says a policy “is stated as that party's position … never generalized
into a universal rule”; Q3 already requires each claim's ≤25-word verbatim quote at an exact location
(the “quote each vendor's own words” conjunct); R12 already binds a recheck to the entry's own header
sources (the “do not merge four vendors behind one `--source`” conjunct, mechanically). The landed
decision not to mint a third row is correct, and its section lead (`:70-72`) records where the vendor
surface is actually measured instead of asserting a negative.

---

## 4. Residual risk (outside the bar, inside this round's counter)

1. **A cadence-prefixed no-op satisfies all three frozen C1 limbs.** Measured on `efbd18ee` bytes:
   `recheck: 2026-10-25 — python3 corpus/instruments/tool.py corpus/knowledge/target.md` scores
   `limbs={'parse': True, 'cwd': True, 'paths': True} pass=True class=fail-closed lane=127 foreign=127`.
   The prefix makes the line a 127 no-op at both cwds; `bash -n` accepts it; the named path exists; the
   instrument files it as “fail-closed”, which its docstring treats as benign. The landed Q10 does forbid
   it (no `cd <lane-root> &&` prefix), so the exposure is confined to the frozen predicate, not the bar.
   No landed line has this shape — all 35 base lines begin with a command or `on-restoration`, and 35/36
   working-tree lines now begin `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` (the 36th is
   `root-loss-2026-10-12.md`, which needs none).
2. **The instrument drifted from its frozen pin** (`d07af435` → `4475d2e6`) after `c1-before.json` was
   produced, so the round's after-receipt will not be scored by the instrument the before-receipt was
   scored by unless the pin is re-frozen and the drift disclosed. MutAuditLimbs' finding — “the only thing
   that makes [the composite] attack detectable is the frozen instrument digest” — is the same point.
3. **The suite's limb count grew mid-wave** (3 → 5 → 7 strict limbs: `parse, cwd, paths, cdroot,
   instrument, artifact, own`). A criterion citing “the selftest” without a sha cannot be falsified later.

## 5. Verification gaps (what I did not establish)

- I did not run the base-tree mutant matrix end-to-end; `MutAuditLimbs.md` did (at `d07af435`), and my
  base-corpus claims are **derived** from `c1-before.json`'s exit pairs and limb flags (0 entries where
  rc-equality differs from digest-equality; the 23 parse failures have `cwd=1, paths=1`).
- The `cdroot`/`instrument` limb isolation I could not pin: the revision that introduced `artifact`/`own`
  makes `elsewhere.md` and `degenerate.md` fail `own` as well, so forcing `cdroot` or `instrument` alone
  did not flip them (measured, but against bytes I can no longer name by sha). I therefore make no claim
  about those two limbs.
- The working tree moved under me throughout: `corpus/knowledge` 35 → 37 recheck lines, `QUALITY.md`
  modified by the scribe, the instrument rewritten at least four times. Every figure above names its sha or its
  committed receipt.
- `/tmp` is full on this host (284 K free); no scratch copies were made. All fixtures used
  `tempfile` under `/var/tmp` and in-memory module loads.

## 6. Commands run (all read-only; lane root)

```sh
python3 corpus/instruments/recheck-audit.py --selftest            # 4-case (d07af435): cases=4 failures=0 exit=0
                                                                  # 6-case (efbd18ee): cases=6 failures=0 exit=0
                                                                  # 11-case (4475d2e6): cases=11 failures=4 exit=1
                                                                  # 12-case (1ccee066): cases=12 failures=0 exit=0, completeness lines=11 total=13 complete=False
python3 corpus/instruments/recheck-audit.py --quiet               # live tree, moved 35→37 lines during the wave
sha256sum corpus/instruments/recheck-audit.py                     # 4475d2e6…cccc at 05:34:28, 13,037 B
cat .ufo/waves/round-25/c1-instrument-digest.txt                  # pin d07af435…b564d6 ; c1-before.json 3e3eeb4e…877e
git show b49948f:corpus/knowledge/<f>.md | grep -m1 '^recheck: ' # 5/35 prefixed, 23/35 prose hybrids
bash -n -c 'on-restoration — true'                                # exit 0
bash -n -c 'on-restoration — true (fails closed today: base absent)'   # exit 2
grep -nE '^\| (Q10|R13) |^## Round-25' corpus/QUALITY.md          # 68, 76, 77
grep -cE '^\| [QR][0-9]+ ' corpus/QUALITY.md                      # 23 after the scribe's append (21 at base)
```

Mutant matrix (in-memory `exec` of the pinned bytes, `tempfile` under `/var/tmp`, no lane write):
`parse_ok→True`, cwd→True, paths→True, digest-half-off, always-PASS, scored against the instrument's own
six fixtures with its own scoring convention (`pass` for the four originals, `pass_strict` for the two
strict fixtures) — results in §2.3.
