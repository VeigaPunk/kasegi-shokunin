# ReviewC1 — round-77 w1 — C1 frozen-bytes attack (recheck-cwd census RESULT-limb gate)

Seat: ReviewC1 (leaf reviewer; no subagents). Scope: claim C1 as frozen at
539a43877809bd90b6f506e8fd24a6d871598cd5 (base 2e53fc74776824898b5c5eb914aeddc19a091157) —
`.ufo/waves/round-77/claims.json` (C1), `.ufo/waves/round-77/c1-amended-reference.py`,
`.ufo/waves/round-77/c1-mutant-transforms.md`, `.ufo/waves/round-77/controls/`. I never edited
any lane file; every run was on scratch copies under
`/fast/scratch/hyaku/kasegi-r77/ReviewC1/` (removed before this report was yielded; receipts
copied into this directory first). Tooling installs: none (stdlib python3 + git only; pacman
untouched). All lane git access read-only (`archive`/`show`/`ls-tree`/`rev-parse`).

Provenance (sha256, all equal the frozen pins): reference `18bfc439238310af…a33`;
base counter `e666ae11fd9d50ec…21a`; m1 `c2746492…`, m2 `b7772949…`, m3 `1fd8d29a…`,
m4 `7f5bb936…`, m5 `b7af7722…` — all five match `c1-mutant-transforms.md:21-23`.

Evidence files (this directory): `ReviewC1-ev-selftests.txt`,
`ReviewC1-ev-kills-m1-m5.txt`, `ReviewC1-ev-xmutants.txt`,
`ReviewC1-ev-census-c2-shape.txt`, `ReviewC1-ev-a5-a6-structure.txt`.

## Findings

### MAJOR-1 — A2 binds an exact baseline and a population drift but never names the landing order; a single-commit landing makes A2 self-falsifying at "the landing commit" (QUALITY R124)

- `claims.json:17` (A2) binds `entries=91 … byte-identical to the base receipt
  …/c1-base-realtree-census-r77.txt` "at the C1-landing tree" **and** a drift expectation
  `entries=92, exit0_foreign=70` "once C2 lands at the final tree".
- `claims.json:23` (kill_rule) evaluates "Any of A1-A6 false **at the landing commit** =
  claim fails" — singular commit.
- `claims.json:25` (registry_pins) moves the SKILL/README pins "in **the same landing
  commit**" — the C1 pin move and (by the wave framing) C2's landing share one integrator
  pass with no declared order.
- QUALITY.md:576 (R124): "A census-parity freeze names the landing order and separate input
  revisions when another claim changes its population; an exact baseline value and a
  population drift cannot both bind one tree."

Failure mode: if the amended counter and C2's 92nd knowledge entry land in one commit, the
census at that landing commit reads `entries=92`, A2's primary clause (entries=91,
byte-identical) is false **at the landing commit**, and C1 fails by its own kill rule although
every artifact is correct. The freeze names the two tree states but not the order between
them, and not which claims.json revision measures the "C1-landing tree".

The arithmetic itself is sound and I verified it empirically (see Verified positives): a new
cd-prefixed entry whose recheck exits 0 from a foreign cwd moves `entries` 91→92 and
`exit0_foreign` 69→70 with every other bucket unchanged, exactly as the drift limb states.

Resolution path that rewrites no predicate: land C1 (amended counter + pin moves) in a commit
that does not contain the S112 knowledge entry — A2's primary clause binds there
(byte-identical to the base receipt) — and let the S112 entry land afterward; the drift limb
then binds at the final tree. Routing recommendation only; I changed nothing.

### NOTE-2 — The routed known-limit class measured: gate-negpolarity boolean neuter survives (rc=0), and the composite with K-M2 silently disables THE required m2b-class kill

`c1-mutant-transforms.md:25-27` routes "a mutant that neuters the gate-negpolarity check's
own boolean (`neg_ok is False` → `True`) while leaving the closures intact, or composite
mutants combining two named transforms" to the next round. Measured:

- X1 (single transform: `neg_ok is False` → `True` at reference `:329`, closures intact):
  exit **0**, `selftest cases=12 failures=0` — survivor, exactly as the routing implies.
- X1+K-M2 composite (closure body additionally `→ True`): exit **0**, and the receipt prints
  `gate-negpolarity ok neg_ok=True` — the closure is neutered and nothing fails.

Verdict on the routing question I was asked: **honest, not hiding anything undeclared** — the
paragraph names the exact transform and concedes non-coverage, and no named-kill promise is
broken. But the load-bearing consequence deserves the next round's attention: with that one
boolean neutered, K-M2 (the required m2b-class kill, `claims.json:18`, transform row
`c1-mutant-transforms.md:12`) becomes undetectable. A future design could make the
negpolarity expectation consumed data (like the RESULT limb) instead of an inline literal.
Evidence: `ReviewC1-ev-xmutants.txt`.

### NOTE-3 — An unnamed single-transform survivor class: deleting the case-8 globals() restore

Transform: reference `:301-302` `finally: globals()["has_restoration_recheck"] = real_hrr` →
`finally: pass` (one statement). Measured: exit **0**, `selftest cases=12 failures=0`
(`ReviewC1-ev-xmutants.txt`). This class is in neither the transform table nor the
known-limits paragraph. It is observationally inert inside the selftest (case 8 is the last
census-consuming fixture; the gate never touches the module global), so claim validity is
unaffected — but "known limits" is not exhaustive. Cheap future closure: a gate limb asserting
the global is restored after case 8, or any later census-consuming fixture.

### NOTE-4 — The gate is a two-point consumption: polarity is pinned, content is not

The closure is probed only at `(out6, ret6)` (reference `:253`, consumed at `:323` requiring
`clean_ok is True`) and `(out2c, ret2c)` (`:199`, consumed at `:329` requiring `neg_ok is
False`). Any closure agreeing at those two points passes all four gates — e.g. `ret >= 1`
[INFERENCE: ret6=1 and ret2c=0 are measured, so `ret >= 1` yields True/False at the two
probes; not executed, third-mutant budget spent on X1-X3]. R127's letter ("consumed in both
polarities") is satisfied; content-weakenings short of neutering are an unnamed residual in
the same family as NOTE-3.

### NOTE-5 — R113 pin sweep: exactly two lines must move 6→12; two other `cases=6` lines must NOT move

- Move in the landing commit: `SKILL.md:982` (recheck-cwd-census.py gates-registry row,
  self-test column `selftest cases=6 failures=0`) and
  `corpus/instruments/README.md:354` (Q10 census row, run column, same pin). Both verified as
  this instrument's rows by reading the rows in full.
- Do not touch: `corpus/instruments/README.md:851` and `README.md:887` — both pin
  `frontier-recheck-count.py` (round-34 amendment section, README.md:844-895), a different
  instrument whose selftest stays at six.
- Side note: `SKILL.md:982`'s pinned-value path still cites
  `.ufo/waves/round-75/controls/c1-after-r75.txt`. R113's letter (QUALITY.md:537) requires
  the count pin to move; refreshing the receipt path to the round-77 landing receipt is L1's
  discretion. Flagging so the stale-path question is decided, not discovered later.

### NOTE-6 — Do-nothing sufficiency confirmed (attack item 5)

Base bytes (`e666ae11…`) have six checks, no gate, no `regs`, no `REQUIRED_CHECKS` (grep over
base: the only `cases=` symbols are the docstring/base:31-32, selftest docstring base:130,
print base:248). My rerun of base `--selftest`: `selftest cases=6 failures=0`, rc=0 — equal
to the frozen receipt `controls/c1-donothing-selftest-r77.txt`. The amended counter's printed
count is `len(done)` (reference `:338`) over names appended in `check()` (`:171`) and
audited against `REQUIRED_CHECKS` (`:139-142`, `:334-336`): printing `cases=12 failures=0`
requires twelve distinct checks to actually run and pass, and the gate exists only in the
amended bytes. A no-work tree cannot reach A1.

## Verified positives (re-derived, not taken from receipts)

- **A1** ✓ reference `--selftest` rc=0, `selftest cases=12 failures=0`
  (`ReviewC1-ev-selftests.txt`).
- **A3** ✓ all five named kills re-derived from the frozen control bytes; every verdict line
  equals the committed `.py.out` receipts, no tracebacks: m1 rc=1 `gate-regs FAIL
  registered=[]` + `gate-consume/gate-negpolarity FAIL no-registration`; m2 rc=1
  `gate-consume ok clean_ok=True` + `gate-negpolarity FAIL neg_ok=True` (assertion kill — the
  required m2b-class, closure neutered, satisfying the kill_rule's R127 demand at
  `claims.json:23`); m3 rc=1 `gate-consume FAIL exception=NameError("name 'out6' is not
  defined")` + `not-evaluated-after-exception` (exception class logged distinctly — counted
  only for K-M3, exactly as the kill_rule scopes it); m4 rc=1 `gate-negpolarity FAIL
  neg_ok=False`; m5 rc=1 `gate-checkids FAIL missing=['both-headers'] extra=[]`,
  `cases=11 failures=1` (`ReviewC1-ev-kills-m1-m5.txt`).
- **A4** ✓ red-before stands: r76 `m2b-conjunct-removed.py --selftest` rc=0,
  `selftest cases=8 failures=0` — the RESULT limb is probed (`result_ok=True`) but consumed by
  nothing on the prior design; the gate is the delta that kills it
  (`ReviewC1-ev-selftests.txt`).
- **A5** ✓ reference contains exactly one `subprocess.run` and one `["bash", "-c"]` pair
  (grep counts = 1/1); file creation only via `write_entry` under the selftest mkdtemp
  (reference `:143,:146`) and `run_foreign`'s mkdtemp with `dir=env_tmp` honoring TMPDIR
  (`:66`; `env_tmp` sourced from `os.environ["TMPDIR"]` in `census()`).
- **A6** ✓ `first_recheck`, `has_restoration_recheck`, `run_foreign`, `census`, `main` are
  ast-identical base→reference; the unified diff is confined to the module docstring's
  --selftest sentence (base `:31-33` → ref `:31-36`) and `selftest()` docstring+body (base
  `:122-248` → ref `:123-338`) (`ReviewC1-ev-a5-a6-structure.txt`).
- **Gate soundness (attack item 3)** ✓ the RESULT limb is consumed in both polarities.
  `gate-consume` (`:323`) requires `clean_ok is True` where `clean_ok = limb(out6, ret6)`;
  `out6, ret6` are case-6 main outputs (`:253`; measured ret6=1, stdout contains
  `RECHECK-CWD-RESULT nonconformant`). `gate-negpolarity` (`:329`) requires `neg_ok is
  False` where `neg_ok = limb(out2c, ret2c)`; `out2c, ret2c` are the case-2 conformant main
  outputs (`:199`; measured ret2c=0, `RECHECK-CWD-RESULT conformant`). Because `ret2c == 0`
  dominates the closure's first conjunct, the negpolarity arm can pass only if the closure
  returns False on conformant outputs; both comparisons are strict identity (`is True`/`is
  False`), no truthiness slack. `gate-checkids` (`:334-336`) audits executed names (`done`,
  `:171`) against `REQUIRED_CHECKS - {"gate-checkids"}` and detects both missing (m5) and
  extra (my X3: dropping `"both-headers"` from `REQUIRED_CHECKS` while the check still runs →
  `FAIL extra=['both-headers']`, rc=1) — REQUIRED_CHECKS tampering is discriminated.
- **A2 arithmetic + cd-prefix lane-relativity (attack item 1)** ✓ measured: census on a
  one-entry fixture whose recheck is exactly the C2 landing shape
  (`cd <lane> && python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-77/manifest.json --source S112`) from a foreign cwd →
  `entries=1 … exit0_foreign=1`, conformant; adding a base-mass cd-prefixed entry →
  `entries=2 … exit0_foreign=2`. Direct `bash -c` of that value from a foreign cwd → rc=0,
  all 13 quotes `OK occurrences=1 anchor=<n>-ok` (`ReviewC1-ev-census-c2-shape.txt`). So the
  cd prefix makes the value lane-relative from any cwd and it lands solely in
  `entries`+1/`exit0_foreign`+1 — base 91 = 69+22 checks out, and the drift limb
  (92/70, all other fields unchanged, `exit1_foreign` still 22) is arithmetically consistent
  with the counting rule.
- **R123 sweep**: no upper-bound clause exists in C1 (twelve and 13 are exact values, not
  caps) — R123 (QUALITY.md:569) is vacuously satisfied this round; no finding.
- **R121 sweep**: A1 (`claims.json:16`), A3 (`:18`), A4 (`:19`), A6 (`:21`), kill_rule
  (`:23`) all name their measured revision (landing commit, named receipts, sha-pinned
  reference and base). A2 names both its revision (base receipt) and its drift trigger — but
  see MAJOR-1 for the R124 landing-order gap.

## Residual risk and verification gaps

- I did not re-run the full 91-entry real-tree census: it executes 91 repo-controlled recheck
  commands; the frozen receipt `controls/c1-base-realtree-census-r77.txt` is the controlling
  evidence and L1 re-derives it at landing per A2. My counting-rule evidence is fixture-scale
  (2-entry/1-entry fixtures plus one direct execution of the real S112 value).
- X1/X2/X3/X1+M2 are my own mutants, built by exact single string replacements on a scratch
  copy of the reference (each replacement's occurrence count asserted == 1); no
  byte-identity-to-controls applies to them.
- NOTE-4's `ret >= 1` weakening is inferred from the two measured probe points, not executed.
- No LSP device was used in this review: the artifacts are frozen bytes; evidence is
  execution- and diff-based (lsp status not consulted because no server-backed semantic query
  was needed; text reads cite exact lines).
- My m2b red-before rerun was compared to the committed receipt by verdict lines and counts,
  not byte-for-byte.

## Verdict

No BLOCKER. One MAJOR (MAJOR-1: R124 landing-order gap in A2 — actionable at landing time by
commit ordering, no predicate rewrite needed) and five NOTEs. The C1 claim's A1/A3/A4/A5/A6
re-derive cleanly from the frozen bytes on this host; the gate consumes the case-6 RESULT limb
in both polarities as claimed; the five named mutants die as specified; the do-nothing control
is sufficient; the transform table's known-limits routing of the gate-boolean-neutering class
is honest but not exhaustive (NOTE-3/NOTE-4 are unnamed survivor classes of the same kind).
