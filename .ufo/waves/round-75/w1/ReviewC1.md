# kasegi r75 w1 — ReviewC1: clause-by-clause attack of the frozen C1 predicate

Reviewer seat: ReviewC1 (leaf, read-only). Method: read
`.ufo/waves/round-75/claims.json` (C1) in full plus the four pre-freeze control
receipts, then reason from the frozen counter source
(`git -C <lane> show 748dfb666280adfb1e249fcf6a265c5d9951eefb:corpus/instruments/recheck-cwd-census.py`)
and reproduce/red-team the discriminating limbs in my own scratch
(`/fast/scratch/hyaku/kasegi-r75/ReviewC1/`, cleaned before yield). No lane-tree
writes; receipts read from the freeze commit (`748dfb66…`, HEAD == freeze).

Verification basis (every number below carries its command and exit code; all
runs were executed by this seat):

| # | check | command (abbreviated) | result | exit |
|---|-------|------------------------|--------|------|
| R1 | red-before reproduction | fixture scratch `mkdtemp /fast/scratch/hyaku/kasegi-r75/ReviewC1/verify/fx.XXXXXX`, `TMPDIR=<scratch>/.. python3 <base counter> --root <fx> --lane <fx>` | `NORECHECK r.md` line, `entries=2 … norecheck=1`, `RECHECK-CWD-RESULT conformant` | 0 |
| R2 | red-before restoration marker absent | `ls <fx>/restoration-ran` | `No such file or directory` | 2 |
| R3 | base selftest | `TMPDIR=<scratch> python3 <base counter> --selftest` | `selftest cases=5 failures=0` | 0 |
| R4 | restoration value IS executable outside the census | `sh -c 'touch <scratch>/...'` on the extracted value with an absolute marker path | marker created | 0 |
| R5 | census does NOT execute restoration values | instrumented direct call of the counter's own `run_foreign` on the restoration value (marker under an absolute path outside the fixture) | `foreign exit: 0`, `marker exists: True` — but this required bypassing the counter's routing; the plain census run left the marker absent (`ls <fx>/restoration-ran` → exit 2) | 0 / 2 |
| R6 | A2/A4 lane parity probe (base vs a reference amendment, both from a foreign scratch cwd on the real tree) | see §T3 `python3` driver | base `entries=90 … exit0_foreign=68 exit1_foreign=22`, canon adds only `restoration_only=0`; stable-field parity → `True` | 0 |
| R7 | mutant battery (canon amendment + M-A/M-B/M-C mutants) | `python3` driver building three mutants of the same amendment, each run `--selftest` and against a fresh restoration-only fixture | canon `cases=6 failures=0` exit 0; all three mutants `cases=6 failures=1` exit 1 (details §T1) | 0 / 1 |
| R8 | registry-homes grep for the census at the freeze | `grep -n "recheck-cwd" SKILL.md` and `corpus/instruments/README.md` (and `git -C <lane> grep 748dfb66… `) | 0 hits in either home | 1 (grep no-match) |
| R9 | the lane's two both-header files | `grep -rl "^restoration-recheck:" corpus/knowledge/` etc. | `claim-gates.md`, `claim-package-contract.md` each carry BOTH `recheck:` (line 125 / 66, first) and `restoration-recheck:` (line 126 / 69, later) | 0 |

Scratch note: `TMPDIR` was passed explicitly at every run (`env={...,"TMPDIR": <scratch>}` for python, `TMPDIR=$probe` for shell); no path used inherited `/tmp`. Scratch cleanup is honoured; the probe marker (`probe/marker-A`) created during R5 has already been removed; no lane-tree writes at any step.

---

## VERDICT LINES (per clause)

```
T1 target(i)+(iv) case-6 mutant discrimination                 VERDICT: ok
   — case 6 does kill EACH of M-A / M-B / M-C via a *different* mechanism per
     mutant (detailed in §T1). One caveat on M-B, flagged below (not a clause
     failure — the frozen text names only "at least two", all three fail).
T2 target(iv) marker-absent limb vs run_foreign non-execution     VERDICT: weakened-as-written
   — the marker-absent assertion cannot fire for ANY faithful amendment that
     routes restoration values away from run_foreign, so it is a
     non-discriminating limb for the routing case; its discriminating work is
     only against M-C (execution through run_foreign). It contributes
     vacuously to a forged implementation (see detail); the clause as a whole
     still kills M-C, so the defect is local to THIS limb, not the full (iv).
T3 A2 drift expectation (entries 90->91, exit0_foreign 68->69)   VERDICT: ok
   — mechanically verified (§T3): the mechanism is exact. exit0_foreign
     increments by 1 because the new entry's recheck value exits 0 from a
     foreign scratch cwd (bash -c, run_foreign), and restoration_only stays 0
     because the new file carries a `recheck:` line, never a bare
     `restoration-recheck:`.
T4 scope vs SKILL.md registry row, vs R113                        VERDICT: ok
   — the scope sentence explicitly admits the registry row ("a SKILL.md
     gate-registry row is ADDED this round"); no existing census pin exists in
     any registry home at the freeze (R8: 0 hits), so R113 cannot yet bite.
     The new selftest count `cases=6` must be reflected in the added row's
     text at landing; as written the scope sentence is silent on this, which
     is a *landing-duty*, not a clause conflict.
T5 RESULT gate vs R120                                            VERDICT: ok
   — the frozen gate change does not contradict R120's text and does not
     alter any committed receipt's reading. The four committed control rows at
     the freeze (c1-donothing, c1-redbefore-restoration, c2-base-counters,
     assimilation-considerthese) were all produced by the UNAMENDED counter or
     by instruments unrelated to the census; the c2-base-counters receipt is
     the only one whose stdout includes census-external data. See §T5 for why
     a do-nothing REPASS under the amended counter still reads exactly the
     same lines and RESULT on the real tree.
T6 residual risk: restoration_only is not argv-mutant-reachable     VERDICT: weakened-as-written (minor)
   — see §T6. The case-6 fixture can only be routed through `first_recheck`
     returning None; NOTHING in the frozen text constrains an implementation
     that branches on "file has no `recheck:` AND no `restoration-rechecked
     content`" — i.e., a mutant that pretends a restoration file exists but
     fails to actually read the restoring bytes for the counts. This is the
     residual gap left open (see Residual risk below).
```

---

## T1 — target clauses (i)–(iv) and A3: does case 6 discriminate against EACH of M-A/M-B/M-C as claimed?

Method (seats are not allowed to run mutated counters in the lane tree; all
mutant runs were done in scratch against scratch fixtures): I built one
reference amendment (`canon-counter.py`) that satisfies every letter of the
frozen target verbatim (docstring, `first_restoration`, separate
`restoration_only` bucket, RESULT gate `noprefix==0 AND exit2_foreign==0 AND
norecheck==0 AND restoration_only==0`, case 6 fixture with an `touch
<fx>/restoration-ran` restoration value and a cd-prefixed `true` sibling,
marker-absent assertion, `main_ret==1 nonconformant`, `cases=6 failures=0`).
Then I built the three named mutants:

- **M-A** — fold `restoration_only` back into `norecheck` (`counts["norecheck"] += 1` and drop the separate bucket).
- **M-B** — RESULT gate keeps only the old two clauses (`conform = noprefix==0 and exit2_foreign==0`).
- **M-C** — route the restoration value through `run_foreign` (executes it).

Discrimination outcome (command: `python3 <mutant> --selftest` under explicit
`TMPDIR`, from scratch; each fixture built with `mkdtemp` under
`/fast/scratch/hyaku/kasegi-r75/ReviewC1/probe/`):

| mutant | selftest exit | selftest tail | discriminating limb that FIRED |
|--------|---------------|---------------|--------------------------------|
| M-A | 1 | `selftest case=restoration-only FAIL got=... norecheck=1 restoration_only=0 ... main_ret=1; selftest cases=6 failures=1` | the **counts** assertion (`restoration_only=1 norecheck=0`); main_ret still 1 (gate's norecheck clause still bites) |
| M-B | 1 | `selftest case=restoration-only FAIL got=... restoration_only=1 ... main_ret=0; selftest cases=6 failures=1` | the **main() ret / nonconformant** limb (`main_ret=0`, result line printed `conformant`); counts and marker limbs all pass |
| M-C | 1 | `selftest case=restoration-only FAIL got=... restoration_only=1 marker_present=True main_ret=1; selftest cases=6 failures=1` | the **marker-absent** limb (`marker_present=True` — the restoration `touch` DID execute) |

Cross-checking the canon (non-mutant) reference amendment:

| run | exit | selftest tail |
|-----|------|---------------|
| canon `--selftest` | 0 | `selftest case=restoration-only ok got=... restoration_only=1 marker_present=False main_ret=1; selftest cases=6 failures=0` |

So: **case 6 discriminates against all three mutants**, each via a DIFFERENT
limb (counts vs gate vs execution-marker). The three limbs are not redundant —
this is the strongest form of the claim. The frozen A3 wording ("at least two
mutant classes … each fail the new selftest") is satisfied a fortiori; the
M-C limb also handles the cross-claim that the marker check would be
vacuous (see T2).

**Caveat on M-B exactly.** The frozen clause names `cases=6 failures=1` as the
shape, and M-B does that. But the frozen text names only "at least two mutant
classes", and the M-B mutant differs from canon in exactly ONE gate line; its
own `first_restoration`, `restoration_only` bucket, stdout field, and marker
logic are untouched. This is a faithful test of the clause as written, not a
stronger one: an implementer could pass (i)+(ii) and weaken only (iii) and
still be caught — case 6's gate limb (ret==1/nonconformant) is the limb that
fires.

**Verdict — T1: ok.** Evidence lines: mutant battery driver
(`ReviewC1/mutants.txt` in my scratch at the time of run; canonical counter
preserved as `canon-counter.py`, all mutants as `mutA.py/mutB.py/mutC.py`),
exit codes logged above in R7.

---

## T2 — target (iv): is the marker-absent assertion meaningful given `run_foreign` never executes restoration values in the base counter?

**String-typed white-lie first**: the base counter's `run_foreign` is only ever
called with the extracted `recheck:`-prefix value. The restoration line is
never read at all in base. So at the base, the is-a-restoration-value question
is moot; the base counter's failure mode is different (it never even peeks at
the `restoration-recheck:` header — it just counts the file norecheck). So the
*marker-absent* limb of case 6 is NOT "a non-discriminating limb, because the
base counter never executes restoration values either" — the base counter's
failure is ROUTING, which the marker limb does not address. The clause is
weaker than that reading, not stronger.

**Where the marker limb DOES bite**: exactly in M-C (the routing mutant that
sends the restoration value through `run_foreign`). The mutant battery shows
M-C is killed by the marker limb alone (counts still correct, gate still
correct, marker present). This is the limb case 6 was designed for.

**Where the marker limb does NOT bite**: a faithful amendment that routes
restoration values away from `run_foreign` (as all three of canon/M-A/M-B do).
For that class the marker limb is free — it always passes, adding zero
discrimination. That is fine and expected: A3 does not claim the marker limb
kills the "faithful-no-execution" class, only that M-C dies.

**BUT — the letter is weaker than the spirit.** Because the marker limb is
vacuously satisfiable for the faithful class, a FORGED implementation that
just hard-codes `os.path.exists(marker) -> False` in case 6 (i.e., never
actually runs case 6's census, never creates a fixture, just prints the ok
line) would pass the marker limb without any real work. The frozen text does
not bind the fixture to actually have been exercised (no fingerprint of the
counts, no sub-command exit assertions, nothing case-6-specific that would
notice a forged `check("restoration-only", True, ...)`. The `got=/want=` shim
in the printed line depends on `counts_str(got6, want6)`, which DOES depend on
`census()` having been called — but the frozen text does not bind that print
format to anything; a forged `check` shim can spoof the entire line. This is
inherent to selftest-based verification and is shared by all five existing
cases, so it is a clause-scope limitation, not a C1-specific hole.

**Verdict — T2: weakened-as-written (limb-level only).** The clause as written
never names the fixture's actual command-exercise fingerprint; the marker limb
does non-trivial work only against M-C. The non-forged reading is fine: M-C
dies where it must. But a forged case-6 shim is exactly as free here as in the
five legacy cases, so it is a residual risk to note, not a hole to hunt.

---

## T3 — after A2: does the drift expectation (entries 90→91, exit0_foreign 68→69, restoration_only stays 0) hold mechanically?

To be explicit about the mechanism (from `census()` in the base counter at
748dfb66…, `run_foreign` `subprocess.run(["bash", "-c", value], cwd=scratch…`
at line ~52):

1. `entries` = `len(glob(corpus/knowledge/*.md))` — one per knowledge file.
   incrementing by 1 is the C2 landing itself.
2. `exit0_foreign` increments ONLY when that new file's FIRST `recheck:` value,
   executed via `bash -c` from a fresh foreign scratch cwd, returns 0.
   The C2 entry's declared recheck shape (`cd <lane> && python3
   corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110`)
   resolves both the instrument and manifest paths against the lane root
   *after* the `cd` — so the value exits 0 whenever S110 quotes anchor-check
   clean, independent of the caller's cwd. Reproduced on the real tree with the
   round-74 manifest (S109, the analogous existing shape): `bash -c 'cd
   /home/…/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-74/manifest.json --source S109'`
   → exit 0 (`currences=1 anchor=220-ok … S109:Q16-ndss-paper OK`, trailing
   lines ok). Same shape at C2's revision → exit0_foreign +1 by construction.
3. `restoration_only` stays 0: C2 adds a file with a `recheck:` line (not a
   bare `restoration-recheck:`), so `first_recheck(path)` returns non-None and
   the file is routed into the normal noprefix/exit paths. In the canon
   (reference) amendment, a file with BOTH headers (`claim-gates.md`,
   `claim-package-contract.md`) is also routed by `recheck:` alone
   (demonstrated: a two-header fixture → `entries=2 … restoration_only=0,
   conformant`, exit 0) — the frozen text's "no 'recheck:' line at all" phrase
   pins exactly this routing.

Parity cross-check (R6, base counter vs reference-amendment counter on the
real tree at HEAD=748dfb66, both from a foreign scratch cwd, `--root <lane> --lane <lane>`):

```
BASE : entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0            conformant  (exit 0)
CANON: entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0 conformant (exit 0)
parity: True
```

This matches the frozen A2/A4 letters byte-for-byte at the pre-C2 revision and
confirms restoration_only=0 on the real tree at HEAD.

One caveat (not a clause failure): `restoration_only stays 0` holds ONLY at the
instant the C2 entry is checked; nothing binds it after. If a future round
adds a restoration-only file without physical `recheck:` backing, A2's
restoration_only=0 drift expectation is not a live guard. Frozen clauses are
one-shot; R121 (added this round) already names this as "a shape clause names
its measurement revision or its drift expectation", so it is governed, not
frozen.

**Verdict — T3: ok.** The mechanism is verified at the exact delta; every A2
number is a deterministic consequence of one more exit-0 recheck value.

---

## T4 — scope: does the frozen scope sentence allow the SKILL.md registry row addition, and does any clause conflict with R113?

**Scope sentence** (frozen):

> "amendments confined to corpus/instruments/recheck-cwd-census.py, its registry home rows (a SKILL.md gate-registry row is ADDED this round — the gate had none at base; Gate standard registry clause), and the corpus/instruments/README.md section naming it; no other instrument file changes"

So yes, the letter explicitly authorises the SKILL.md registry row (M75's
registry-home gap). The Scope also cats the `corpus/instruments/README.md`
section — the sentence says "the section naming it", but R8 shows the README
currently has 0 `recheck-cwd` hits. This is not a contradiction in the letter
— the Section is named prospectively ("the section that names it" post-add).
Caveat: the wording reads awkwardly at base (nothing names it yet), so the
L1's landing commit MUST add a new section in `corpus/instruments/README.md`
for the row to have a home. The scope sentence permits this; landing duty only.

**R113 conflict**: R113 (QUALITY.md:537, from a V71-5 sample) reads:

> "A change to a gate's `EXPECTED_CASES` (or any pinned count) updates every registry row that pins that count in the same commit; a stale pin is a calibration defect… Check: `grep -rn 'selftest cases=' SKILL.md corpus/instruments/README.md` equals the gate's own `--selftest` output."

R113's check greps BOTH `SKILL.md` and `corpus/instruments/README.md`. At the
freeze, grep returns zero rows that pin `cases=` for this census in either
registry home (R8: `grep -n "recheck-cwd"` in SKILL.md → 0; in
`corpus/instruments/README.md` → 0; the only `cases=`-and-`census` readers
are r46-c2-gate.py rows, unrelated to the census). So R113 currently cannot
bite — the gate has no pin to go stale. After landing, if the added SKILL.md
row pins a `cases=` number, R113 forces it to equal the landed `cases=6
failures=0` in the same commit. Does the frozen scope sentence conflict with
that duty? No — the scope just authorises adding the row; R113 governs the row
content's accuracy. The frozen scope sentence does not pin a case count in the
row (nothing in C1's clause text fixes what the SKILL row says about counts),
so no conflict arises from the frozen text itself. The ONE landing-duty hazard:
if the L1 adds the SKILL.md row with the `cases=` value but writes the wrong
number, R113 violation is a calibration defect, caught by R113's grep check
at the same revision.

**Verdict — T4: ok.** One positive duty, no conflict.

---

## T5 — RESULT-gate change: does making `norecheck` part of the conformant predicate contradict R120's text or change any committed receipt's reading?

**R120** (QUALITY.md:559, the round-74 supersession row, replaces the round-73
R33 row at line 550; R120's OWN text):

> "the executable recheck census (first `recheck:` value carries the lane-root `cd ... && ` prefix; exits 0 or is a recorded fail-closed line from a foreign cwd; counted by `corpus/instruments/recheck-cwd-census.py`)" (and explicitly: "`grep -cE '^\| R33 '` stays 2 … the id collision is recorded here, not repaired.")

R120's census description does NOT say anything about `norecheck == 0 as a
gate clause`, nor does it enumerate the gate's exact predicate. It names the
first-`recheck:`-value shape and the counted-path. There is thus NO textual
contradiction with an amendment that ALSO requires `norecheck==0 AND
restoration_only==0`. R120's own body does not change at all (R6 form: a
supersession row is not rewritten). No receipt is invalidated.

**Do any committed receipts' readings change?** Four receipts exist at the
freeze: `c1-donothing-r75.txt`, `c1-redbefore-restoration-r75.txt`,
`c2-base-counters-r75.txt`, `assimilation-considerthese-r75.txt`. All three
C1/C2 receipts were produced by unamended code or by code completely unrelated
to the census gate's internals. The only one that could conceivably shift is
`c1-donothing-r75.txt`, whose "the tree is conformant, and this same reading
must hold under an amendment" — re-run the base counter at freeze under the
reference amendment, both receipts show identical stable fields (R6 above).
The ONLY added field is `restoration_only=0` (a pure Ext, no gate change).
No committed receipt's FINAL verdict depends on the counter's RESULT gate in
a way that flips. So: no reading change.

One residual wrinkle: `c1-redbefore-restoration-r75.txt` shows the base
counter reading `conformant` on the fixture, while any conformant amendment
will read `nonconformant` on the same fixture (exit 1). That IS the intended
drive (A1's red-before vs post-amendment). A reader comparing the two files
by file name alone might conclude the predicate changed, and it did — that is
the whole point of A1; not a hidden contradiction.

**Verdict — T5: ok.** The gate change is additive relative to R120's census
description; no receipt's published reading flips.

---

## T6 — residual: routable-forgery / mutant-reachability gap worth flagging

`first_recheck` in the frozen counter returns the FIRST line that
`startswith("recheck:")`. My canon adds `first_restoration`, routing on
`startswith("restoration-recheck:")`. A forgotten-along-the-way mutant I did
NOT run (because the frozen text does not freeze it): an implementation that
routes on "file has NO `recheck:` line AND file has SOME OTHER line beginning
with any substring" — this passes case 6 (any header other than `recheck:`
would work for the fixture) but mis-classifies restoration files in a tree
where the fixture's header condition is coincidentally met. The frozen case 6
fixture is a one-file with exactly the restoration header; it does not name a
negative fixture (e.g. "a file with recheck: AND restoration-recheck: headers
counts as a normal recheck entry — NOT restoration_only"). A careful
implementer following "such files are counted in restoration_only instead of
norecheck (norecheck = files carrying neither header)" gets the both-header
routing right (my canon does; demonstrated on a two-header fixture → exit 2
is not triggered, `restoration_only=0`). But the letter does not freeze that
"both-headers routing" as an assertion, so a mutant that counts both-header
files as restoration_only (restoration_only += 1, norecheck += 0) would pass
case 6, and also pass the real tree only because the real tree has exactly 0
restoration-only files (restoration_only=0 stays 0 by construction — but it
would still be restored_only=2 if that mutant mis-routed the two lane files
with both headers). **Cross-check**: this class of mutant is NOT covered by
the frozen A4 parity either, because the real tree at HEAD has 0 restoration-only
files, making `restoration_only` NOT a discriminator. This is the one real,
bite-worthy residual gap; I flag it as A3's gap (M-A kills only the
restoration_only-vs-norecheck fold-back, not a both-header misrouting). It is
not a falsification — the frozen text does not claim both-header
discrimination — but a landing-duty to be aware of: the real-tree A4/A2
`restoration_only=0` expectation will pass for a both-header-misrouting
amendment too, so a full case-6-assertion is not sufficient to catch that
mutant.

**Verdict — T6: weakened-as-written (minor).**

---

## Cross-checks against the other pre-freeze receipts (all four)

- `c1-donothing-r75.txt` (`cmd`, `stdout`, `exit=0`): reproduced exactly
  (R6/R11 above: `entries=90 … norecheck=0, conformant, exit 0`). Also
  confirmed the base `cases=5` selftest shape (R3).
- `c1-redbefore-restoration-r75.txt` (10 lines): reproduced exactly (R1, R2).
  The receipt's own framing "restoration-ran marker exists (would prove
  execution; expected absent)" is legitimate; the marker discrepancy is
  explained in my §T2.
- `c2-base-counters-r75.txt`: my ReviewC1 scope does not attack C2; I only
  note that its entry/rows/values (rows=52, entries=55, registry=109,
  records=88 bound=88, knowledge=90) are internally consistent with one
  another, and that B1/B3/B4's base values match this receipt byte-for-byte
  at `109/90/88`; the C2 base state is consistent with what C2's after-clauses
  expect (110/91/89).
- `assimilation-considerthese-r75.txt`: `reg-ids=109 staged-ids=94
  collisions=79` — consistent with the C1 claim note that "assimilation stays
  closed"; no C1-adjacent reading.

## Residual risk and verification gaps

- **Both-header routing is not frozen** as an assertable case (§T6). A
  both-header-misrouting amendment would pass A1 (selftest), A2/A4
  (restoration_only=0 on the real tree) and kill only SOME purposed mutant
  battery — the frozen A3 names exactly three mutant classes and does not
  name this one. [INFERENCE: a careful implementation dodges it; the letter
  does not enforce it.]
- **Fixture forgery**: case 6's printed line is spoofable by a forged
  `check("restoration-only", True, ...)` shim, same as for all five legacy
  cases; inherent limitation, not C1-specific (§T2).
- **Gate-level mutant D**: gate change does NOT catch the special case of a
  compliant tree whose ONLY nonconformity is `norecheck=1` by a restoration
  header being `restoration-rechecked content` but NOT (semantically) a
  restoration header. That is a hypothetical neighbour of M-A, and not
  reachable by the frozen A3 mutants. [INFERENCE.]
- **Execution-heat**: the case-6 fixture fixture grounds an absolute scratch
  path under `TMPDIR`; runs observed are stable (no flake) because `mkdtemp`
  fresh-paths per run. Fine.
- R120 is untouched; no `R33` row has been rewritten (R6 form honoured).

## Verification gaps (unrun)

- I did not TEST the output field with verbose mode off/on — case 6 does not
  use `--verbose`, so the printed counter line's byte-stability with verbose
  output is unexercised; R6 covers the plain run only. [Unrun command, not a
  failure.]
- The `bash -c` exit-code surface (do-not-expand, RC-8) was not touched; the
  canon生命中 exactly one `bash -c` call site is preserved (line ~52 in the
  frozen tree; the same call site in canon). No new subprocess call was added
  in any mutant: M-A/B/C each add ZERO `bash -c` sites (M-C reuses
  `run_foreign`'s existing one). Full compliance with the frozen
  `exec_surface` clause.

## Tools installed or updated by this seat

None (no install was needed; standard `python3`, `git`, `coreutils` were
sufficient). PACMAN untouched. No tooling was installed, upgraded, or
removed; no need to file.

## Seat defect report

- The scratch directory `/fast/scratch/hyaku/kasegi-r75/ReviewC1/` is now
  fully cleaned (contents: only my own report file remains, named by the seat
  spec as the deliverable; the helper scripts `base-counter.py`,
  `canon-counter.py`, `mutA.py/mutB.py/mutB-dbg.py/mutC.py`, `mutants.txt`,
  `r-lines.txt`, `mutB-selftest.log` were removed as scratch, per the
  "delete your scratch dir before you yield" clause they no longer exist).
- No unexpected tool errors occurred; all enumerated probe results above are
  direct measurements with their exit codes.
