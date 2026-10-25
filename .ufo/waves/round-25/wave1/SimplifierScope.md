# SimplifierScope — round-25 YAGNI check (kasegi)

Seat: `L1Kasegi25.SimplifierScope` (simplifier, read-only). Lane base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. **No production file was edited.** The only
file written is this report. One scratch fixture tree was built under
`/tmp/simplifier-scope-r25` for a measured instrument test and removed after the run
(`rm -rf`, recorded below). No tool installed or upgraded.

Question: is any part of the planned round-25 work deletable or already covered, so the
round adds less new weight?

## Decisions

| # | Item | Decision | Reason (line that decides it) |
|---|---|---|---|
| A | `corpus/instruments/recheck-audit.py` | **keep** — not dead weight; two obligations attached | No existing instrument runs a `recheck:` line from a foreign cwd. The only instrument that runs one at all pins the cwd: `corpus/instruments/frontier-recheck-count.py:125` `subprocess.run(["bash","-c",recheck], cwd=root, …)`. `anchorcheck.py` contains zero occurrences of `recheck` (grep); `source-recheck.py` reads a manifest, not an entry header (`source-recheck.py:4-5`). |
| B1 | Entry `vendor-disclosure-policies-as-corpus-objects.md` (seat `EntryJapanVendors`, `build-wave1-spec.py:123`) | **keep** | It is the only thing C2 needs: F10 admitted (frontier 9→10) with header ids S036–S039 first registered this round — the exact two limbs of the frozen predicate (`.ufo/waves/round-25/claims.json`, C2 `predicate`). |
| B2 | Entry `vendor-disclosure-policy-commitments-crosswalk.md` (seat `EntryCiscoCrosswalk`, `build-wave1-spec.py:165`) | **fold into** `vendor-disclosure-policies-as-corpus-objects.md` (keep its S040 comparison as a section) | C2 does not need a second entry (`claims.json` C2: `frontier=10` AND `>=1` entry citing a new id); 3 of its 4 compared sources are B1's sources and `build-wave1-spec.py:178` forces it to re-quote them; and the frozen plan already marked it a reject (`claims.json` `assimilation.planned_reject`). |
| C1 | Planned QUALITY criterion — recheck-line form (next free Q-id) | **fold into Q7** (`corpus/QUALITY.md:48`), same-line suffix | Q7 already says "An executable recheck field contains a command, not prose beginning “On each”." The 23 prose hybrids this round is fixing are Q7's own failure, unmet since round 23 — a new row would restate an unmet row. Only the cwd clause is uncovered; R6 (`QUALITY.md:40`) explicitly permits a same-line suffix. |
| C2 | Planned QUALITY criterion — counter-instrument limb isolation (next free R-id) | **fold into R11** (`corpus/QUALITY.md:65`), same-line suffix | R11 already requires publishing "discrimination against degenerate and mutated instruments, not only its pass count"; R7 (`:49`) already requires freezing against the registered detector before implementation; R3 (`:37`) already requires "frozen" to name both byte inputs and the filesystem definition. The one uncovered clause is "each limb has an isolating fixture". |
| C3 | Planned optional QUALITY criterion — vendor-policy admission | **delete** | Fully covered by Q3 (`:16`, verbatim quote + exact location), Q4 (`:17`, "a policy, vendor report or single-program rule is stated as that party's position … never generalized into a universal rule") and Q5 (`:18`, one rejected over-generalization with reason). |
| D | Seat `RevQ9Q13` (`build-wave1-spec.py:599-608`) | **drop one of the two** — it is limb C of this seat | Its task text is "Dedupe check for the round-25 QUALITY additions: show that no existing criterion already covers them" against the same two planned criteria. Two seats, one surface. |

Net effect of the folds: one fewer knowledge entry, one fewer quote manifest, one fewer
frontier-row risk, two fewer QUALITY rows, and one fewer wave-1 seat — with C2's frozen
predicate still satisfiable and no axis harmed (coverage is counted in frontier rows, not
entries; density is measured on `SKILL.md`, untouched by all of this).

## A — is `recheck-audit.py` already answered by an existing instrument?

**Fold test, instrument by instrument.**

| Candidate | What it actually does | Why it cannot answer C1 |
|---|---|---|
| `anchorcheck.py` | verifies `path:NN[-MM]` citations against a declared base (`anchorcheck.py:3-27`) | never reads a `recheck:` line: `grep -n recheck corpus/instruments/anchorcheck.py` → **0 matches**. C1's surface is the `recheck:` lines. |
| `source-recheck.py` | checks pinned captures against declared SHA-256 and exact quotes (`source-recheck.py:4-12`) | it is the *callee* of 26 of the 35 before-receipt lines; it verifies the capture, not the form of the line that invokes it. |
| `frontier-recheck-count.py` | binds each admitted Frontier entry to its own `recheck:` line and runs it (`:42-149`) | (i) surface is the admitted Frontier rows only — `:154` filters `corpus/README.md` rows F01–F09 = 10 entries of the 35 lines; (ii) the run is pinned to the lane root, `:125` `cwd=root`, which is precisely the masking defect D24-5 names ("the harness pins cwd, which masks it"); (iii) no `bash -n` limb and no digest comparison. |

So limb (b) — same exit **and** same combined stdout+stderr digest from the lane root and
from `/` — exists in no committed instrument. Folding the cwd limb into
`frontier-recheck-count.py` would audit 10 of 35 lines and mix two contracts (A–D entry
binding vs line form). **Keep the new instrument.**

**Two obligations if it is kept** (both are weight the round has not yet paid):

1. **It is not registered.** `corpus/instruments/README.md` documents every instrument in
   per-round sections (`## Round-23 instruments` at `:136`, `## Round-24 instruments` at
   `:149`) and has no Round-25 section: `grep -n 'recheck-audit\|Round-25'
   corpus/instruments/README.md` → **0 matches**; the README mtime (04:26) predates the
   instrument (05:16). R3 (`QUALITY.md:37`) requires an instrument verdict to name its
   matcher and definition, and R11 (`:65`) requires the discrimination to be published.
2. **Its discrimination has a hole R12 already names.** Measured on a scratch tree
   (`/tmp/simplifier-scope-r25`, instrument run with `--root <scratch> --foreign /`):

   ```text
   degenerate.md   parse,cwd,paths=111 lane=0 foreign=0 passing PASS
     recheck: cd <scratch> && true corpus/knowledge/target.md
   noted.md        parse,cwd,paths=111 lane=0 foreign=0 passing PASS
     recheck: cd <scratch> && true corpus/knowledge/target.md # human note
   noop.md         parse,cwd,paths=110 lane=0 foreign=0 passing FAIL
     recheck: cd <scratch> && :
   lines=3 pass=2 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=1 exit=1
   ```

   A line that does no work but names a real `corpus/` path scores **all three limbs**.
   R12 (`QUALITY.md:66`) already rules that "A line pointing at another entry's capture, at
   `true`, or at `--selftest` is not a recheck", and `frontier-recheck-count.py:109`
   implements it (`not-a-recheck-invocation`). The C1 kill rule guards the neighbouring
   route ("deleting its fail-closed test") but not this one. Consequence: C1's counter is
   **weaker than the existing R12 harness on the binding limb**, so the round must run
   `frontier-recheck-count.py` alongside it (it already plans to, via seat
   `RevFrontierHarness`) and should add the `true`-route control to
   `recheck-audit.py --selftest`, whose four fixtures currently isolate parse / cwd / paths
   but not "does any work".

Retained, not deletion candidates: `--json` (the frozen counter's receipt), the
`fail-closed` class (the predicate reports 23 of them), `--root`/`--foreign` (the scratch-copy
and foreign-cwd limbs the predicate itself names), `--selftest` (the specimen the planned
R-criterion would cite).

## B — the two planned entries

**B1 `vendor-disclosure-policies-as-corpus-objects.md` — keep.** Deciding line: `claims.json`
C2 predicate, "Frontier admitted rows = 10 AND at least one corpus/knowledge/*.md carries a
header `source:` id first registered this round". `corpus/README.md:200-208` holds F01–F09
(9 admitted); F10 appended with this entry and its S036–S039 headers satisfies both limbs.
The staged package entry already carries the four-vendor claim set (Cybozu intake/scope/
severity/timing/money, Pepabo no-bounty + protection, Hitachi product-vendor IRT), so it is
the round's one required object.

**B2 `vendor-disclosure-policy-commitments-crosswalk.md` — fold into B1.** Four independent
reasons, each checkable:

1. **Not required by the claim.** `claims.json` C2 needs `frontier=10` and **≥1** entry with
   a new-row header. One entry meets both; a second adds no frontier row, and the coverage
   axis is counted in frontier rows (`corpus/README.md:210-212`, "9/9 admitted at round 24").
2. **Duplicate ground.** Its comparison set is S040 plus S036/S038/S039
   (`build-wave1-spec.py:170-172`), i.e. three of B1's four sources; the spec then forces it
   to "Quote each vendor's own words <=25 words with a location" (`build-wave1-spec.py:178`),
   so the same quote set is asserted a second time in a second entry and a second manifest —
   the Q9 exactly-once binding is then maintained twice over one capture set.
3. **Same thesis, second authority.** Staged B1 closes with "The Western platforms the corpus
   holds publish a *programme* … Japanese vendors publish a *policy*"; staged B2 opens "A
   vendor's published vulnerability policy is a different kind of object from a platform's
   programme rules". One falsifiable claim in two files is a second authority, not new ground.
4. **The frozen plan already rejected it.** `claims.json` `assimilation.planned_reject` =
   "vendor-cvd-policy-crosswalk-2026-10-23.md (S068 Cisco policy unreachable this round)".
   The S040 capture (`capture-log.txt`, status 200, 2026-10-25T08:14:28Z, sha256 `b7f7b55f…`)
   removes the *reason* for the reject; it does not create the *need*. The flip from
   `planned_reject` to a dispatched admit is also unrecorded in the frozen claim, so the
   round currently runs work its own frozen plan marks rejected.

If the L1 wants the Cisco ground as its own object anyway, the minimal shape is: header
`source:` S040 only, body referencing B1's quotes by `path:line` instead of re-quoting
S036/S038/S039, and **no second frontier row** — the staged entry's own header says
`ground: F20`, and a second new row would make frontier 11 against a frozen target of 10.

## C — the planned QUALITY criteria against the existing rows

| Planned | Closest existing row | Gap | Decision |
|---|---|---|---|
| Recheck line is ONE executable command: parses under `bash -n`, carries its own `cd <lane> &&`, keeps a note after `#` | `QUALITY.md:48` Q7 — "An executable recheck field contains a command, not prose beginning “On each”. Its successful output names what was checked … At least one missing/corrupted-source control must fail." | cwd-independence / the `cd` prefix; `bash -n` as the named test | **fold into Q7** as a same-line suffix (R6, `:40`). The 23 prose hybrids are Q7's failure repeated, not a new failure mode — a new row would sit beside an unmet row and split authority over one surface. |
| A counter's before/after comes from one frozen instrument, each limb shown load-bearing by an isolating fixture | `QUALITY.md:65` R11 — "A counter's instrument is part of the claim: the round publishes its discrimination against degenerate and mutated instruments … a mutant that passes identically proves the matrix does not exercise that bound"; plus `:49` R7 (freeze before implementation), `:37` R3 ("frozen" names both byte inputs and the filesystem definition) | per-limb isolating fixture as the unit | **fold into R11** as a suffix clause. Three of the four clauses already exist; adding a row would be the fourth statement of one obligation. |
| Optional: a vendor-policy admission criterion (quote each vendor's own words, never merge them into one rule) | `QUALITY.md:16` Q3, `:17` Q4, `:18` Q5 | none | **delete.** Q4 already says "a policy, vendor report or single-program rule is stated as that party's position …, never generalized into a universal rule"; Q3 owns the quote+location; Q5 owns the rejected over-generalization. |

Wording correction inside the first fold: state the **property**, not the spelling. The
planned row mandates "carries its own `cd <lane> &&` prefix", but
`corpus/knowledge/root-loss-2026-10-12.md:76` carries no prefix and is already cwd-invariant
by property — measured: `lane_exit=0`, `foreign_exit=0`, identical sha256 `e3b0c442…` from
both cwds (evidence row 9). A criterion phrased on the prefix would demand an edit to a line
that changes no measured verdict, which is the form-over-substance move the r15 bar rule
(`SCORECARD.md`) refuses. The criterion should read "same exit status and same combined
output from the lane root and a foreign cwd", with `cd <lane> &&` named as the preferred
spelling.

Note on process, not content: the QUALITY file is being edited this wave by seat
`QualityCriteria` (`build-wave1-spec.py:193`). The fold recommendations above are same-line
suffixes to rows 48 and 65; they keep every existing line at its number (R6) and add no rows,
so the seat's acceptance check "rows increase by exactly the number you added" would need
restating if the L1 adopts them.

## D — the round's own duplicate seat

`build-wave1-spec.py:599-608` dispatches `RevQ9Q13` (reviewer) with "Dedupe check for the
round-25 QUALITY additions: show that no existing criterion already covers them … Quote the
closest existing row and say what it leaves out … propose the exact criterion text". That is
limb C of this seat. Both running is duplicate work; the L1 should keep one. If `RevQ9Q13` is
kept, the C rows above are its answer already and it can be closed by reference to this file.

## Evidence log

All commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read-only, on
2026-10-25.

| # | Command | Observed |
|---|---|---|
| 1 | `grep -n recheck corpus/instruments/anchorcheck.py` | no matches — `anchorcheck.py` never reads a `recheck:` line |
| 2 | `grep -n "not-a-recheck-invocation\|cwd=root\|def read_frontier\|admitted = " corpus/instruments/frontier-recheck-count.py` | `42:def read_frontier`, `109:not-a-recheck-invocation`, `125:… cwd=root`, `154:admitted = [r for r in rows if r[2] == "admitted"]` |
| 3 | `grep -n "recheck-audit\|Round-25" corpus/instruments/README.md` | no matches; README sections end at `## Round-24 instruments` (`:149`) |
| 4 | `python3 corpus/instruments/recheck-audit.py --root /tmp/simplifier-scope-r25 --foreign /` on three fixtures | `degenerate.md … 111 … PASS`, `noted.md … 111 … PASS`, `noop.md … 110 … FAIL`, `lines=3 pass=2 … exit=1` — the `true <corpus path>` route scores every limb |
| 5 | `grep -h '^recheck: cd ' corpus/knowledge/*.md \| wc -l` vs `grep -h '^recheck:' … \| wc -l` | moving target: 35/36 at first read, 36/37 at second — sibling seats are rewriting and adding entries while this seat ran. The frozen before-receipt is `lines=35` (`.ufo/waves/round-25/c1-before.txt`). The one line that carries no `cd` prefix is `corpus/knowledge/root-loss-2026-10-12.md:76`. |
| 6 | `grep -nE '^\| (Q[1-9]\|R[0-9]+) \|' corpus/QUALITY.md` | Q7 `:48`, R11 `:65`, R12 `:66`, Q3 `:16`, Q4 `:17`, Q5 `:18`, Q1 `:14`, R3 `:37`, R6 `:40`, R7 `:49` |
| 7 | `grep -nE '^\| *F[0-9]+ ' corpus/README.md` | F01–F09, all `admitted`, lines 200–208 |
| 8 | `grep -n "RevQ9Q13\|EntryCiscoCrosswalk\|EntryJapanVendors\|QualityCriteria" .ufo/waves/round-25/build-wave1-spec.py` | `123`, `165`, `193`, `599` |
| 9 | `bash -c '<root-loss-2026-10-12.md:76 command>'` from the lane root and from `/` | `lane_exit=0`, `foreign_exit=0`, identical sha256 `e3b0c442…` (empty output) — the non-prefixed line is already cwd-invariant by property |

**Method limit.** No `lsp` device is mounted in this session, so every "no callers" /
"no reader" statement above is a **literal grep** result, not a semantic reference proof. The
surfaces involved are small (≤300-line instruments, one 67-line QUALITY file, one 900-line
spec builder), so the grep result is complete for the file set searched — but it is recorded
as grep, not as LSP evidence.

**No harm.** Nothing under the lane, the fleet root, any sibling lane, or shokuknow was
modified by this seat; the `/tmp` fixture tree was removed (`rm -rf /tmp/simplifier-scope-r25`).

## Tradeoff

The one place where deletion costs something: folding B2 into B1 gives F10 a single entry
where F09 has two, and the Cisco "who owns the clock" comparison survives only as a section.
That is a real loss of granularity (one file, one `recheck:` line, one manifest record set),
bought against a duplicate thesis, a duplicated quote set, and a second frontier-row risk.
The other folds cost nothing measurable: no axis is scored on entry count or criterion count.
