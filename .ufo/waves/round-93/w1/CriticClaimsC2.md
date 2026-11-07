# CriticClaimsC2 — round 93, C2 (capture-secret-scan: `gitlab-pat` + escape-terminator left boundary)

Seat: leaf critic, no dispatch. Lane: kasegi. Landing under attack: `9225954a6e3f177af46bdb9d811c062a4353a552`
(parent `ae53b3c6…` = C1 landing, parent `5bad9e55…` = freeze, base `e15996bf…`).
Every command ran in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` or in a fresh `git clone --shared`
of the lane at `/fast/scratch/hyaku/kasegi-r93/CriticClaimsC2/clone` (scratch removed at exit).

## Verdict

**C2 STANDS on the frozen predicate P1–P3.** P1 passes at a printed run-time seed and at seeds 1 and 9191,
in a fresh shared clone of the landing; P2 matches the frozen candidate sha256; P3 names exactly the two
frozen paths and the landed SCORECARD row is byte-identical to the frozen candidate row.

The claim is **not** clean, though, and the qualifier is material: the frozen statement's own sentence about
the counter — "a path-keyed forgery cannot know the paths" — is **false as implemented**. The nonce reroot is
a deterministic syntactic transform (`r<8 hex>/`, `n<8 hex>/`, `p<8 hex>/`) that leaves the basename and the
`round-1/` segment intact, and K7's generated plants keep fixed relative paths. A round-92 scanner (no
`gitlab-pat` shape, no escape left boundary) that keys only on the *shape* of the rerooted paths passes all
eight limbs at rc=0 (forgery H). That is a routed counter defect, not a re-score: P1–P3 are about the
counter's verdict and the pinned bytes, and both hold.

## P1 — counter at the landing, three seeds (re-derived)

Fresh `git clone --shared` of the lane, checked out at the landing; `git rev-parse --show-toplevel` asserted
equal to the clone dir. Counter run with the frozen pins
`--instrument-sha256 7d9d7309…f683c5 --gate-sha256 8b6f8493…1cc8e6`:

| run | seed | rc | limbs |
|---|---|---|---|
| `run-runtime-seed.txt` (no `--seed`) | 1466534565 (printed) | 0 | K1–K8 pass |
| `run-seed-1.txt` | 1 | 0 | K1–K8 pass |
| `run-seed-9191.txt` | 9191 | 0 | K1–K8 pass |

Stable limb detail across all three: K1 `selftest_rc=0`, instrument sha `7d9d73…`, gate sha `8b6f84…`;
K2 `rc=1 sts_files=2 oracle=2`; K3 `scanned=1957,hits=0,allowed=24,unused_allow=0`; K4 `missing=none
extra=none` with a different nonce each run (`17f2d315`, `adc4b2d3`, `c8309894`), `sts_allow_rc=2`,
`files_hits=2`; K6 `base_rc=1 base_hits=22 new_caught_by_base=none outside_plants=none`; K7 `missing=none
extra=none` at the same seed; K8 `clauses=50 failing=none`; K5 `rows=1`.

## P2 — pins (re-derived from the clone's rev, not the working tree)

| byte string | observed | frozen |
|---|---|---|
| `git show 9225954a…:corpus/instruments/capture-secret-scan.py \| sha256sum` | `7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5` | same |
| `…:.ufo/waves/round-93/c2/capability-check.py \| sha256sum` | `8a4ad5081cb21d9afb80e83f490b51df2e3a7fb6211a4e9e91a69c456d751bb6` | same |
| `…:.ufo/waves/round-93/c2/candidate-row.txt \| sha256sum` | `6d18d57978f3ae8e45da85fcf9ef6cdf2a523f1ec50955c7d496e85741e3fb40` | same |

The landed file and the wave's frozen candidate file are the same bytes.

## P3 — path set and row

`git diff-tree --no-commit-id --name-only -r 9225954a…` prints exactly

```
SCORECARD.md
corpus/instruments/capture-secret-scan.py
```

(two paths; path count 2). The freeze→landing range also touches `corpus/knowledge/triage-thresholds.md`,
but that file enters through the C1 commit `ae53b3c6`, which is this commit's parent and not this commit.

Row: exactly one `## Capabilities` row starts `| capture-secret-scan |` (line 307); its text is 2730 bytes
and is byte-identical to `candidate-row.txt` after stripping that file's single trailing newline — 2730
bytes on both sides, `==` True in Python bytes comparison, row-text sha256
`d354640353c2815cb152b653986e474721ed8bf94a4106f0909358dfc83c1d78` (the frozen `6d18d5…` is the sha256 of
the row file *including* its newline, which a row inside `SCORECARD.md` cannot carry).

## Assigned forgeries — each rejected, limb named

All mutants were committed as single-path commits on the clone (toplevel asserted before each commit) and run
through the frozen counter **unpinned** (no `--instrument-sha256`), so K1 could not reject on the pin and the
rejection had to come from behaviour.

| forgery | what it is | counter rc | limb(s) that reject |
|---|---|---|---|
| **A — hardcoded round-92 plant paths** | round-92 scanner (`58c0c115` blob) + literal-path table for the ten round-93 plant paths | 1 | **K4** (`missing=` ten entries at `r<nonce>/round-1/S035.txt` … `w/n<nonce>/t-receipts/live-m.json`), **K7** (`live-g10/g11/g12` missing), **K8** (9 clauses) |
| **B — `glpat-` + any 3+ characters** | `glpat-[A-Za-z0-9_-]{3,}` with the three affected selftest cases relaxed so its own `--selftest` passes (90 ok, 0 FAIL) | 1 | **K4** (`extra=` S040, S041), **K7** (`extra=` live-n12, live-n13), **K8** (19-char and 21-char clauses) |
| **C — JWT-segment floor 1** | `_JWT_SEG = [A-Za-z0-9_-]{1,}`, selftest case relaxed so `--selftest` passes | 1 | **K3** (`hits=1` at the landing, path `.ufo/waves/round-92/w1/MutC2Counter-receipts/forgery-diffs.txt:159`), **K4** (`extra=` S034, S048), **K8** (U3 and the "three 10+ segments" clause) |

Forgery A also proves the nonce defeats *literal-path* keying directly: on a two-file fixture holding the same
42-byte `glpat-` line at `corpus/source-snapshots/round-1/S035.txt` and at
`corpus/source-snapshots/rNONCE1/round-1/S035.txt`, A reports `hits=1 files=1` (literal path only) and the
landed instrument reports `hits=2 files=2`.

## Additional forgeries — the ones the counter does not stop

Not required by the ticket, but they are the strongest counterexamples in local evidence and they decide the
qualifier.

| forgery | what it is | counter rc | limbs |
|---|---|---|---|
| **D — no GitLab left boundary** | `_GL_LB` dropped from `GITLAB_PATTERNS`, selftest `gl-pat-letter-before` relaxed; reports `gitlab-pat` for `xglpat-<20>`, which the statement says is not a hit | **0 PASS** | none — K4/K7/K8 all pass |
| **E — no GitLab escape terminators** | `(?<=\\[ntr])` dropped from `_GL_LB` only; misses `\t`, `\r`, `\n` forms in `glpat-` position that the statement says are hits (`hits=0` on all three probes) | **0 PASS** | none — no K4 plant and no gitlab selftest case covers them |
| **G — basename-keyed** | round-92 scanner + a table keyed on `S035.txt`, `live-k.json`, `live-g10.txt`, … | 1 | **K3 only**, and only by accident: real files `corpus/source-snapshots/round-24/S035.txt`, `round-25/S036.txt`, `round-32/S050.txt` share basenames. K4, K7, K8 pass. |
| **H — rerooted-shape-keyed** | round-92 scanner + 13 anchored regexes `^corpus/source-snapshots/r[0-9a-f]{8}/round-1/S035\.txt$`, … `^g/x-receipts/live-g12\.txt$`; **zero content detection of either new shape** | **0 PASS** | none — K1–K8 all pass |

Forgery H is the sharp one. It is derived from the round-92 scanner, which has no `gitlab-pat` pattern and no
escape left boundary at all, so it cannot detect either round-93 addition from content; on a fixture where the
same `glpat-` line sits at `corpus/source-snapshots/round-7/S035.txt` and `…/round-1/S035.txt` it prints
`scanned=2 hits=0 rc=0` while the landed instrument prints `hits=2`. Yet the counter accepts it at rc=0,
including K4 `missing=none extra=none` on the nonce'd plants and K7 `missing=none extra=none`.

Mechanism: `reroot()` (counter, line 440) only inserts `r<nonce>/`, `p<nonce>/`, `n<nonce>/` into fixed
positions; the basename and the `round-1` segment survive, and K7's generated plants keep fixed relative
paths (`g/x-receipts/live-g10.txt` …). So the reroot defeats a *literal-path* table (forgery A) but not a
*shape* table (forgery H).

## Clauses of the frozen statement the counter does not bind

The statement's detection clauses are **true of the landed instrument** — I probed 13 clause forms directly
with `--files` on the landed scanner: `\t`, `\r`, `\n`, `&#38;`, `&#x26;` before `glpat-` all hit; `\r`,
`&#38;`, `&#x26;` before `ghp_` all hit; `xglpat-`, `glpat-<20>_`, `glpat-<20>-`, `glpat%2D<20>`,
`gh%5Fp_<36>` all do not hit. So there is no behavioural falsification. What the counter does not bind:

1. **GitLab left boundary** ("not preceded by `A-Za-z0-9_-`"): no K4 plant, no CLAUSES row. Forgery D passes.
2. **GitLab escape terminators `\t`, `\r`, `\n`**: the only gitlab escape plants are `%20` (S036) and
   `\u0026` (live-l); no selftest case covers `\t`/`\r`/`\n` for `gitlab-pat` either. Forgery E passes.
3. **GitLab right boundary `_` / `-`**: only the alphanumeric form is planted (S041); `glpat-<20>_` and
   `glpat-<20>-` are unplanted (the landed instrument is correct on both, per the probes, so silent only).
4. **GitHub `\r` escape**: no K4 plant; only the instrument's own selftest (`gh-escape-cr`) binds it, so the
   binding is K1, not K4/K7/K8 — a forger that also relaxes that case would pass.
5. **HTML-entity forms (`&#NN;`, `&#xXX;`)**: no plant for either shape; they hold transitively because the
   escape's last byte is `;` and the generic negative lookbehind already admits it (round-92 P1 control e03
   measured exactly this). For `gitlab-pat` they ride on the unbound generic boundary (item 1).
6. **Named limit "encoded prefix separators"**: no plant; the landed instrument is correct (`glpat%2D…`,
   `gh%5Fp_…` both silent) but nothing in K4/K7/K8 says so.
7. **"Other GitLab token prefixes"**: only `glrt-` is planted (S044); other prefixes are representative-only.

Two doc/claim defects on top of the bindings:

8. The counter's K8 docstring (line 69) still says "every clause of the frozen **round-92** C2 statement";
   the `CLAUSES` dict it now guards contains round-93 rows. Stale text, not behaviour.
9. The statement's counter sentence: "plants every value under a run-time nonce directory (a path-keyed
   forgery cannot know the paths)". K4 does; K7's generated plants keep fixed relative paths (their *values*
   are run-time random), and the reroot is invertible enough that a shape-keyed table passes (forgery H).
   The parenthetical is false as written.

## Impacted axes

- **coverage (8 held)** — the landed instrument implements both additions and the boundary for the forms
  probed; nothing in the evidence re-scores coverage. The capability row is consistent with the instrument.
- **depth:verifiability** — the successor counter did land the round-92 routed fixes it claims (run-time
  nonce on K4 plants, `\u0026`-free plant paths, U1–U6 as S046–S051, base-instrument K6 over round-93 plants)
  and it is stronger than round 92's. But its plant-based limbs are **saturable by path-keying on the rerooted
  shape**, and two statement clauses have no plant at all. C2's verifiability therefore grows by less than the
  statement's last sentence asserts — the same defect class as round-89's M89-2, not a new class.

## Routed defects (not verdict changes) and the smallest safe correction

- **D-C2-1 (high, counter)**: K4/K7/K8 are satisfiable without any content detection (forgery H, rc=0). Smallest
  safe correction, next round's counter only: plant each new shape in **two** fixtures with unrelated relative
  paths, at least one with a random basename and directory chain drawn from the same run-time seed, so no
  fixed regex on the path can satisfy both; or randomize the K7 plant paths per run as K4 already does.
- **D-C2-2 (medium, counter)**: no plant binds the GitLab left boundary or the `\t`/`\r`/`\n` GitLab escapes
  (forgeries D and E pass). Smallest correction: two K4 plants, `xglpat-<20>` (negative) and
  `x\tglpat-<20>|\r|\n` (positive), plus the CLAUSES rows — the landed instrument already behaves correctly,
  so no instrument change is implied.
- **D-C2-3 (low, text)**: K8 docstring still names round 92; the statement's "a path-keyed forgery cannot know
  the paths" should say "a literal-path forgery cannot know the paths" or be dropped.

## Receipts

Commands and observed rc/lines are in `.ufo/waves/round-93/w1/CriticClaimsC2-receipts/`:

- `run-runtime-seed.txt` — counter, no `--seed`, pins; seed 1466534565, K1–K8 pass, `CAPABILITY-CHECK-RESULT pass rc=0`.
- `run-seed-1.txt`, `run-seed-9191.txt` — same at seeds 1 and 9191, rc=0.
- `p2-p3-checks.txt` — `git diff-tree --no-commit-id --name-only -r 9225954a…` (2 paths); `git show …:corpus/instruments/capture-secret-scan.py | sha256sum`, `…:capability-check.py | sha256sum`, `…:candidate-row.txt | sha256sum`; row vs candidate-row byte comparison.
- `forgery-A-pathkeyed.txt` (rc=1, K4/K7/K8 FAIL), `forgery-B-glpat3.txt` (rc=1, K4/K7/K8), `forgery-C-jwt1.txt` (rc=1, K3/K4/K8), `forgery-D-no-gitlab-lb.txt` (rc=0 pass), `forgery-E-no-gitlab-escapes.txt` (rc=0 pass), `forgery-G-basename-keyed.txt` (rc=1, K3 only), `forgery-H-nonce-shape-keyed.txt` (rc=0, K1–K8 pass).
- `forgery-diffs.txt` — `diff -u` of every mutant against the round-92 blob (`58c0c115`) or the landed file, including the relaxed selftest cases that let each forgery pass its own `--selftest`.
- `keyed-path-demo.txt` — literal path vs `rNONCE1` path, forgery A `hits=1`, landed `hits=2` (fixture `git rev-parse --show-toplevel` asserted).
- `forgery-H-content-probe.txt` — forgery H `scanned=2 hits=0 rc=0` where the landed instrument `hits=2 rc=1` on the same two files.
- `clause-probes-landed.txt` — the 13 clause forms through the landed scanner (`hits=8`), plus forgery E `hits=0` on `c01..c03` and forgery D `hits=1` on `c09`.

No credential values appear in these files: every token-like string is the counter's own fabricated fixture
(`PLANTED…`, `0123456789abcdefghij`) or a mutant of it.
