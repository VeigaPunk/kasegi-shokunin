VERDICT: DRAFT-READY

Seat: R46bScoutPureRecipe (round 46 attempt 2, kasegi lane). Item: what the two counter
selftests need from `--pure`, whether the corpus-only export of 914ca0b at
`/fast/scratch/hyaku/kasegi-r46/L1/pure2` satisfies them, and the minimal fix for the dead
default. All runs below were performed by this seat on 2026-10-29. No tool installs were
needed (nothing added/updated; no pacman use). No git/jj mutation anywhere; no repo file
edited by this seat; this Report file is the only bytes written outside scratch.

## 1. The defect is real (both defaults are dead)

Both selftests default `--pure` to the attempt-1 scratch export, which no longer exists:

- `corpus/instruments/r46-counters-selftest-c1.py:47` — `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"`
- `corpus/instruments/r46-counters-selftest-c1.py:568` — `ap.add_argument("--pure", default=PURE)`
- `corpus/instruments/r46-counters-selftest-c2.py:47` — same constant
- `corpus/instruments/r46-counters-selftest-c2.py:275` — same default

Observed (control, do-nothing — bare invocation, no `--pure`):

    $ ls /fast/scratch/hyaku/kasegi-r46/L1/
    S074-candidate.txt  base-a2  f29r50  mutbat-before  mutbat-before.txt  pure2  raw.html
    selftest-c2-baseline.txt  work-sb  work-selftest
    $ test -e /fast/scratch/hyaku/kasegi-r46/L1/pure || echo "PURE DEAD (missing)"
    PURE DEAD (missing)

    $ python3 corpus/instruments/r46-counters-selftest-c1.py --work $S/c1-control
      File "/usr/lib/python3.14/shutil.py", line 652, in copytree
        with os.scandir(src) as itr:
    FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r46/L1/pure'
    (selftest copytree at r46-counters-selftest-c1.py:589)

    $ python3 corpus/instruments/r46-counters-selftest-c2.py
      File ".../r46-counters-selftest-c2.py", line 308, in main
        sources_txt = open(os.path.join(a.pure, SOURCES), encoding="utf-8").read()
    FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r46/L1/pure/corpus/SOURCES.md'

This control discriminates the verification below: without `--pure` the selftests die at
startup, so the passing runs in section 4 are caused by routing `--pure` to pure2, not by a
vacuously green harness.

## 2. What the synthetic trees need from `--pure` (resolved by reading the builders)

### C1 (`r46-counters-selftest-c1.py`)

- Whole tree: `shutil.copytree(pure, ...)` at :589 (BASE tree) and :165 (TIP build) — pure
  must be a complete corpus the counter can grade.
- `corpus/knowledge/claim-package-contract.md` and `corpus/knowledge/claim-gates.md`: read
  at :591 (`BASE_LINE[name] = next(ln ... if ln.startswith("recheck:"))`) — each must carry
  at least one `recheck:` line; it seeds every re-ground/restoration mutant.
- Anchor files located at build time by `loc(pure, rel, token)` (:73-80, raises
  `SystemExit("selftest setup: token ... not found ...")` if a token is absent):
  - `corpus/instruments/claim-package-check.py` — 14 tokens across the ROWS dict (:85-102),
    e.g. `MAX_SCAN_BYTES = 5 * 1024 * 1024`, `(?i)\b(?:api[_-]?key`,
    `SUBCHECK_KEYS = ('no_secrets', 'operator_attribution')`, `expected_head_sha256`;
  - `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json`
    (`"polarity": "positive"`, `"expected_head_sha256"`);
  - `corpus/instruments/fixtures/claim-package/exemplar/custodian-receipts.json`
    (`"scope_signal": "NO_SCOPE_OBJECTION"`).
- Semantic: pure must be the PRE-round-46 base — no `## Re-ground (round 46)` section in the
  two entries — so the internal do-nothing control (BASE tree, :622-623) reads exactly
  `fixed=1/7 exit=1` with L7 pass=1.

### C2 (`r46-counters-selftest-c2.py`)

- Whole tree: `copytree(pure, ...)` at :196 (build) and :558 (null control).
- `corpus/README.md` must contain an `| F27 |` row — `add_f28` (:203-206) anchors on
  `max` index of `^\| F27 \|`.
- `corpus/SOURCES.md` read at :308 and must contain an `| S0dd |` row — `add_s073`
  (:208-211) anchors on the last `^\| S0\d\d \|` row.
- `corpus/knowledge/` must contain at least two spare `.md` entries not named in SOURCES and
  outside the exclusion set (:309-312, delete/rename mutants), and must contain
  `claim-gates.md` / `claim-package-contract.md` byte-different from the lane's (:358-359
  assert) — i.e. pure predates the C1 re-ground.
- The S073 snapshot and manifest come from `--lane`, not `--pure` (Snap at :66-70; build
  copies `os.path.join(lane, rel)` at :262-263), so pure need not carry round-46 captures.

## 3. pure2 satisfies every requirement (corpus-only export of 914ca0b)

`git -C <lane> log --oneline -1 914ca0b` → `914ca0b round-45 verifier spot-check (integrator, hyaku): non-author admit/reject`.

    $ for f in corpus/knowledge/claim-package-contract.md corpus/knowledge/claim-gates.md \
        corpus/instruments/claim-package-check.py \
        corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json \
        corpus/instruments/fixtures/claim-package/exemplar/custodian-receipts.json \
        corpus/README.md corpus/SOURCES.md; do test -f $P/$f && echo "OK  $f"; done
    OK  (all seven)
    $ grep -c "^recheck:" .../pure2/corpus/knowledge/claim-package-contract.md .../claim-gates.md
    .../claim-package-contract.md:1
    .../claim-gates.md:1
    $ grep -c "^| F27 |" .../pure2/corpus/README.md          -> 1
    $ grep -cE "^\| S0[0-9][0-9] \|" .../pure2/corpus/SOURCES.md -> 72
    $ ls .../pure2/corpus/knowledge/*.md | wc -l             -> 64
    $ grep -c "## Re-ground (round 46)" .../claim-package-contract.md .../claim-gates.md -> 0, 0
    $ grep -c "^| F28 |" .../pure2/corpus/README.md          -> 0

Pre-round-46 base confirmed (no re-ground section, no F28 row): both the C1 do-nothing
control and the C2 null case are semantically valid against it.

## 4. The runs (both expected values reproduced)

Environment per seat rules: `S=/fast/scratch/hyaku/kasegi-r46/R46bScoutPureRecipe`,
`TMPDIR=$S/tmp` and `HYAKU_SCRATCH=$S` exported explicitly; scratch removed at exit.

    $ python3 corpus/instruments/r46-counters-selftest-c1.py \
        --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/c1-work
    C1 exit=0
    case X-stubbed-gate-copy-alone  L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
    residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
    selftest cases=76 failures=0
    (959 s, default --jobs 4)

    $ python3 corpus/instruments/r46-counters-selftest-c2.py \
        --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
    C2 exit=0
    probe       probe-four-tick-fence-with-inner-three-tick-line fixed=7/7 failing=[] (ACCEPTED)
    probe       probe-entry-pad-is-garbage-bytes fixed=7/7 failing=[] (ACCEPTED)
    selftest cases=137 failures=0
    (126 s)

Both match the frozen expectation and the documented contract
(`corpus/instruments/README.md:1001` `prints selftest cases=76 failures=0`,
`:1002` `prints selftest cases=137 failures=0`).

Read-only proof on the shared export — sha256 over the sorted file list before and after
both runs, unchanged:

    a9e845a18871618f2a26b333544314bb9c2ba5049ce4234e9d06a8d1fd15aa61  -  (448 files, before)
    a9e845a18871618f2a26b333544314bb9c2ba5049ce4234e9d06a8d1fd15aa61  -  (448 files, after)

## 5. Minimal fix for the dead default (spec for L1 integration errata; NOT applied here)

The committed counters and selftests are read-only for seats, so the amendment below is
drafted for L1 integration. Recommend `required=True`, not env-derivation:

- The only programmatic caller, `corpus/instruments/r46-mutbat.py`, already requires
  `--pure` on its own CLI (`:128 ap.add_argument("--pure", required=True, ...)`) and always
  forwards it to the selftests (`:103` c1: `cmd += ["--pure", pure, "--work", work, ...]`;
  `:105` c2: `cmd += ["--pure", pure]`), invoking them under `python3 -I` (`:99`). No caller
  breaks.
- The documented contract (`corpus/instruments/README.md:1001-1002`) is "run ... with
  --lane DIR --pure DIR" — `required=True` enforces exactly that.
- Env-derivation (`os.environ.get("HYAKU_SCRATCH", ...)/kasegi-r46/L1/pure2`) would bake an
  attempt-local scratch name into a committed instrument — the same rot that killed the
  attempt-1 `L1/pure` constant. The export is environment state; the caller names it.

Exact edits:

1. `corpus/instruments/r46-counters-selftest-c1.py`
   - :568 `ap.add_argument("--pure", default=PURE)` → `ap.add_argument("--pure", required=True)`
   - :47 delete `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"` (its only remaining
     reference is :568; verified by grep over the file)
   - :30 USAGE docstring: `[--pure DIR]` → `--pure DIR` (mark required)
2. `corpus/instruments/r46-counters-selftest-c2.py`
   - :275 `ap.add_argument("--pure", default=PURE)` → `ap.add_argument("--pure", required=True)`
   - :47 delete the same constant (only other reference is :275)
   - :30 Usage docstring: same bracket removal

Errata note for integration: `r46-mutbat.py:98` runs the graded TREE's own copy of the
selftests (`st = os.path.join(tree, "corpus/instruments", ...)`), so the amendment takes
effect per graded tree only once it is in those trees' committed bytes — i.e. it lands with
the counters at integration, not by editing the lane working copy alone.

## Limitations

- The fix is specified, not applied: seat bounds forbid editing the committed selftests;
  verified behavior is the unfixed files' with explicit `--pure` pass-through.
- The C1 selftest's 76th case list includes 1 disclosed residual false-green
  (`R-claim-text-unrelated-to-anchor`), printed and not counted by the harness itself.
- Runtime asymmetry (c1 959 s vs c2 126 s at default jobs) is observed, not tuned; mutbat
  passes its own `--jobs`.
- Evidence for "what pure must contain" is source reading of the two selftests plus the
  passing runs; the C2 gate's own tree expectations were not re-derived (out of item scope).
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScoutPureRecipe` removed before yield; all
  commit-worthy output is quoted verbatim above.
