# MutC1Counter — mutation test of the round-90 C1 counter

| field | value |
|---|---|
| seat | MutC1Counter (leaf, w1, round 90 attempt 1) |
| target claim | C1 only, depth:verifiability (internal-citation repoint, tranche 5); this seat re-scores nothing |
| instrument | `.ufo/waves/round-90/c1/knowledge-meter.py` sha256 `8f4ac21823979adb4096977ede78140eeade19baaa9072f546a5d6dd703836d4` — **unchanged before and after** this probe (never edited; all mutants are scratch copies) |
| revs | base `6088c3eb0c29040415c69e7b5fb91e110480ab26`, freeze `33f43db99c06e89bb9fb78c538313e9450da649f`, C1 landing `4a7e676895d3fc74e18c853457c9b465ade2ddf5` |
| fixture | one scratch git repo whose base commit `293e9347f77a60006e71d4e25a1749d89304e435` has exactly the tree of `git archive 6088c3eb…`; 27 commits (base + 26 candidate/forgery/plant/label commits) on 28 branches, worktree left at base |
| detector | the frozen pre-freeze control set (`.ufo/waves/round-90/controls/c1-controls-r90.sh`, 6 invocations + env receipt) rebuilt case by case, **plus 20 added falsification shapes** so that every limb has a case that fails on it alone |
| mutants | 26, each an exact single-point replacement of the frozen text (one hunk per mutant; every replacement string asserted to occur exactly once; every mutant compiles) |
| verdicts | **24 killed**, 2 case-equivalent survivors with proofs (§5) |
| baseline | pristine counter = 812/1827 → 843/1829, all limbs pass on the candidate; the rebuilt control images are **byte-identical** to `c1-controls-r90.txt`; the frozen counter also passes at the real landing (§2) |

## 1. Method

The frozen counter was copied to scratch as the source text; each mutant is
`orig.replace(old, new)` with `orig.count(old) == 1` asserted (receipt
`MutC1Counter-receipts/mutants.tsv` carries the exact `old`/`new` lines, the hunk and the sha256).
No mutant re-implements a limb; each removes or weakens one conjunct.

Detector cases are the frozen script's own fixtures, rebuilt exactly as it builds them
(`git archive 6088c3eb | tar -x` into a scratch repo, `git init`, one base commit, the frozen
`apply-map.py` for every repoint) plus plants. Each case is run with `--lane <fixture>` and an
explicit `--work`; a case's expected verdict is the pristine counter's verdict on that case.
Judging rule: a mutant is **killed** when its verdict on a case differs from the pristine verdict
(a limb that must FAIL starts passing = detection lost; the honest candidate case starts failing =
the mutant cannot verify the honest bytes). A mutant that matches pristine on every case is
**SURVIVED**, and is then swept over all 25 cases.

Every plant that must isolate a limb was built so that the *measured rates stay at the frozen
targets*: the value substituted at site `triage-thresholds.md:236` is a token with zero base
citations and exactly one map use, so replacing it leaves 843/1829 intact (verified: the pristine
runs of `v9999`, `vhi`, `vlo` fail **only** the intended M5 limb, and `cross` fails M4 plus the M5
line that folds M4's verdict into itself — Q1). This is what makes the kill attributable: no mutant
below dies on M0/M1.

## 2. Detector baseline (pristine counter) — 25 cases

| case | expect | pristine limb image | what it isolates |
|---|---|---|---|
| `cand` (frozen positive control) | pass | all pass; 812/1827 → 843/1829 | honest bytes |
| `nowork` (frozen no-work case) | fail | M1 FAIL 812/1827; M3 FAIL bad_lines=32 | the repoint must exist in the after rev |
| `shift` (frozen shift-forgery) | fail | M9 FAIL (34 rows unbound) | M9 value binding |
| `superset` (frozen superset-forgery) | fail | M1 FAIL 846/1829 | M1 rate + M9 exclusion |
| `unlabelled` (frozen CORRECT-site forgery) | fail | M1 FAIL 844/1829; M9 FAIL row 458 | M9 WRONG filter |
| `base811` | fail | M0 FAIL base=812/1827 | M0 numerator |
| `basedenom` (`--base-target 812/1826`) | fail | M0 FAIL base=812/1827 | M0 denominator |
| `tgt844` | fail | M1 FAIL after=843/1829 | M1 numerator |
| `tgtdenom` (`--target 843/1828`) | fail | M1 FAIL after=843/1829 | M1 denominator |
| `wrongsha` (map digest `0…0`) | fail | M6 FAIL | M6 |
| `dupmap` (row #1 repeated; own digest) | fail | M3 FAIL dup_rows=1 | M3 duplicate-row guard |
| `blank` (cand + trailing blank line in `claim-gates.md`) | fail | M3 FAIL bad_lines=1 | M3 line count |
| `tamper` (cand + ` PROBE-TAMPER` on `claim-gates.md:1`) | fail | M3 FAIL bad_lines=1 | M3 line equality |
| `extra` (cand + empty `corpus/knowledge/zzprobe.md`) | fail | M3 FAIL same_files=False | M3 file set |
| `noop` (map row at `triage-thresholds.md:457` whose key is absent from that line; labels row added) | fail | M3 FAIL key_not_once=1 | M3 key-once (a no-op row is otherwise invisible) |
| `dupbase` (empty `corpus/other/mission-control.md` in both revs) | fail | M4 FAIL 9 rows; M5 FAIL out_of_range=none | M4 unique basename |
| `ufocopy` (empty `.ufo/copy/claim-gates.md` in both revs) | **pass** | all pass | M4's `.ufo/` exclusion (pristine must ignore it) |
| `gone` (map row citing off-scope `corpus/other/probe.md:1`, key `zz.md`, value `corpus/knowledge/zz.md:1`) | fail | M4 FAIL bad=probe.md:1; M5 FAIL out_of_range=none | M4 key-GONE-in-base |
| `v9999` (row #1 value `…claim-gates.md:9999`) | fail | M5 FAIL out_of_range=…:236 | M5 |
| `vhi` (`…:41-9999`) | fail | M5 FAIL out_of_range=…:236 | M5 upper bound |
| `vlo` (`…:0-41`) | fail | M5 FAIL out_of_range=…:236 | M5 lower bound |
| `cross` (row #1 value `corpus/knowledge/ev-model.md:2`) | fail | M4 FAIL 236; **M5 FAIL out_of_range=none** | M4 key-name = value-name |
| `lwrong` (labels row 236 verdict WRONG→CORRECT) | fail | M9 FAIL unbound=236 | M9 WRONG filter |
| `lrange` (labels row 236 range → `…:42`) | fail | M9 FAIL unbound=236 | M9 value equality |
| `lfile` (labels row 236 citing file → `probe-other.md:236`) | fail | M9 FAIL unbound=236 | M9 citing file |

Fidelity of the rebuild: re-running the frozen script in scratch produced LIMB / KNOWLEDGE-METER /
`control_rc` lines **byte-identical** to `.ufo/waves/round-90/controls/c1-controls-r90.txt`
(receipt `control-rerun.txt`), including the environment receipt (r89 meter 815 live / 814 clone vs
r90 meter 812 / 812, `pinned=archive`). The frozen counter at the real landing `4a7e6768`, with the
frozen targets/map digest/labels rev, prints `KNOWLEDGE-METER-RESULT pass rc=0` (receipt
`landing-run.txt`).

Plant construction, one line each (all in scratch, rebuilt from `repair-map.tsv`):

- CLI-only: `base811`, `basedenom`, `tgt844`, `tgtdenom`, `wrongsha` change no tree.
- `shift`, `superset`, `unlabelled`: the frozen script's forgeries, run with the **forged map's own
  digest** so M6 passes and only the intended limb fails (the frozen script itself passes the
  frozen map's digest, which is why its shift/superset/unlabelled images also show M6 FAIL).
- `blank`, `tamper`, `extra`, `dupmap`: candidate tree plus one edit; `dupmap` keeps the candidate
  tree (the extra row is a repeat, so applying is a no-op).
- `noop`: candidate tree + a map row at line 457 whose key is not on that line + a labels rev that
  appends that row.
- `dupbase`, `ufocopy`, `gone`: base commit carries one added tracked file (`corpus/other/…`,
  `.ufo/copy/…`, `corpus/knowledge/zz.md`) in *both* revs, so M0/M1 are untouched; `gone` also adds
  one map row citing a non-scope file.
- `v9999`, `vhi`, `vlo`, `cross`: map row #1's value replaced, the candidate tree rebuilt with that
  map, and a labels rev whose row 236 carries the same replaced range.
- `lwrong`, `lrange`, `lfile`: labels rev only.
- the pin mutant's kill is the honest `cand` case with the fixture worktree checked out at base.

## 3. Mutants — 26

| # | mutant | area | diff summary (one hunk) | kill case | pristine → mutant |
|---|---|---|---|---|---|
| 1 | `m0_always` | M0 | `("M0", (bn,bm)==(bn0,bm0), …)` → `("M0", True, …)` | `base811` | M0 FAIL → pass (verdict pass) |
| 2 | `m0_numonly` | M0 | `(bn,bm)==(bn0,bm0)` → `bn==bn0` | `basedenom` | M0 FAIL → pass |
| 3 | `m1_always` | M1 | `("M1", (an,am)==(tn,tm), …)` → `("M1", True, …)` | `tgt844` | M1 FAIL → pass |
| 4 | `m1_numonly` | M1 | `(an,am)==(tn,tm)` → `an==tn` | `tgtdenom` | M1 FAIL → pass |
| 5 | `m3_linecount` | M3 | `if len(bl) != len(al):` → `if False:` | `blank` | M3 FAIL bad_lines=1 → pass |
| 6 | `m3_keyonce` | M3 | `count(...) != 1` → `count(...) < 0` | `noop` | M3 FAIL key_not_once=1 → pass |
| 7 | `m3_dup` | M3 | `if (f,n,k) in sites: dup += 1` → `if False:` | `dupmap` | M3 FAIL dup_rows=1 → pass |
| 8 | `m3_samefiles` | M3 | `same_files = set(bfiles)==set(afiles)` → `True` | `extra` | M3 FAIL same_files=False → pass |
| 9 | `m3_eq` | M3 | `if fwd != x:` → `if False:` | `tamper` | M3 FAIL bad_lines=1 → pass |
| 10 | `m4_gone` | M4 | drop `and bcls.get(k) == "GONE"` | `gone` | M4 FAIL bad=probe.md:1 → pass |
| 11 | `m4_unique` | M4 | `bybase.get(name)==[path]` → `True` | `dupbase` | M4 FAIL (9 rows) → pass |
| 12 | `m4_internal` | M4 | drop `and A["classify"](v) == "INTERNAL"` | — | **SURVIVED** (25/25 identical to pristine, §5) |
| 13 | `m4_nameeq` | M4 | `vm.group(1) == name` → `True` | `cross` | M4 FAIL 236 → pass |
| 14 | `m4_ufo` | M4 | `if not p.startswith(".ufo/")` → `if True:` | `cand` **and** `ufocopy` | honest candidate M4 FAIL → killed (over-strict: 43 tracked `.ufo/` copies of `claim-gates.md` exist at base) |
| 15 | `m5_always` | M5 | `("M5", not m5bad and not m4bad, …)` → `("M5", True, …)` | `v9999` | M5 FAIL → pass |
| 16 | `m5_hi` | M5 | `1 <= lo <= hi <= len` → `1 <= lo <= len` | `vhi` | M5 FAIL → pass |
| 17 | `m5_lo` | M5 | `1 <= lo <= hi <= len` → `lo <= hi <= len` | `vlo` | M5 FAIL → pass |
| 18 | `m5_basefiles` | M5 | `text = afiles.get(path)` → `bfiles.get(path)` | — | **SURVIVED** (25/25 identical to pristine, §5) |
| 19 | `m6_drop` | M6 | `if a.map_sha256:` → `if False:` | `wrongsha` | M6 FAIL → limb absent, pass |
| 20 | `m6_self` | M6 | `got == a.map_sha256.lower()` → `got == got.lower()` | `wrongsha` | M6 FAIL → pass |
| 21 | `m9_always` | M9 | `("M9", not m9bad and bool(rows), …)` → `("M9", True, …)` | `shift` (frozen shape) | M9 FAIL → pass |
| 22 | `m9_wrong` | M9 | `c[2] == "WRONG"` → drop | `lwrong` | M9 FAIL unbound=236 → pass |
| 23 | `m9_value` | M9 | bind `(site,k)` instead of `(site,k,v)` | `lrange` | M9 FAIL unbound=236 → pass |
| 24 | `m9_line` | M9 | bind `(line,k,v)` instead of `(file:line,k,v)` | `lfile` | M9 FAIL unbound=236 → pass |
| 25 | `mpin_worktree` | provenance | `tree = extract(lane, rev, work)` → `copytree(lane, …)` | `cand` | honest candidate M1 FAIL + M3 FAIL (812/812) → killed |
| 26 | `mlabels_pin` | provenance | labels via `git show labels_rev:path` → read the lane worktree file | `lwrong` | M9 FAIL unbound=236 → pass (passes all six frozen controls) |

Every kill above was produced by a case whose pristine verdict is the opposite of the mutant's
verdict; each row's two verdicts are in `MutC1Counter-receipts/killmatrix.tsv` and the full limb
images in `MutC1Counter-receipts/baseline.tsv` / `frozen-suite.tsv`.

Notable non-kill observations from the runs: `m6_drop`'s candidate output simply has no M6 line
(the limb is only appended when the flag is passed, §6-Q6), and `mpin_worktree` keeps printing
`pinned=archive` while reading the working tree (§6-Q5).

## 4. Kill ratio against the frozen control set alone

All 26 mutants were swept over the five frozen control shapes with the frozen command lines (frozen
map digest on every case, exactly as `c1-controls-r90.sh` runs them; the script's sixth invocation,
working-tree-only, needs a dirty worktree and targets a worktree-reading counter — covered here by
`mpin_worktree` on the honest candidate). The pristine counter reproduces the frozen receipt's limb
images for these five shapes exactly (receipts `frozen-suite-baseline.tsv` / `control-rerun.txt`).
Result: **0/26 killed by detection; 2/26 killed only because the positive control stops passing.**

| frozen case | pristine image | limbs that must fail | mutants that flip the case |
|---|---|---|---|
| `cand` | all pass | — | `m4_ufo`, `mpin_worktree` (over-strict: their honest-candidate verdict flips — dead mutants, not detections) |
| `nowork` | M1 **and** M3 | two at once | none |
| `shift` | M6 **and** M9 | two at once | none |
| `superset` | M1 **and** M6 | two at once | none |
| `unlabelled` | M1 **and** M6 **and** M9 | three at once | none |

The 24 remaining mutants reproduce every frozen verdict — including all six forgery detections —
with a limb silently disabled. The reason is structural: **the frozen repertoire contains no
single-limb case**, so a single-conjunct regression is always masked by a sibling conjunct.

- The frozen forgeries pass the *frozen map's* digest on a *forged* map, so M6 fails on top of M1 or
  M9 (`shift` M6+M9, `superset` M1+M6, `unlabelled` M1+M6+M9). Passing the forged map's own digest
  (as my `shift`/`superset`/`unlabelled`-derived cases do) is what isolates M9 or M1.
- The no-work case trips M1 and M3 together (`bad_lines=32`), so neither M1 nor M3 can be isolated.
- No frozen case ever puts a bad M4 value, a non-GONE key, a second basename, an out-of-range
  anchor, a wrong map digest, or a labels file different from the worktree in front of the counter.

The 24 kills in §3 therefore come entirely from the added cases, one per limb conjunct:
M0 ← `base811`/`basedenom`; M1 ← `tgt844`/`tgtdenom`; M3 ← `blank` (line count), `tamper`
(equality), `extra` (file set), `noop` (key-once), `dupmap` (dup rows); M4 ← `gone` (GONE), `dupbase`
(unique basename), `cross` (name equality), `cand` (`.ufo` filter); M5 ← `v9999`, `vhi`, `vlo`;
M6 ← `wrongsha`; M9 ← `lwrong`, `lrange`, `lfile`, `shift`-own-digest; provenance ← `cand` (pin),
`lwrong` with a labels rev whose bytes differ from the worktree (labels pin).

## 5. The two survivors — case-equivalent, no plant can kill them

Both survivors were swept over **all 25 cases** (50 runs) and are byte-identical to pristine on
every limb of every case (`receipts/survivors.tsv`). That is not a missing plant; it follows from the
counter's own invariants:

1. **`m4_internal`** (M4 stops requiring `A["classify"](v) == "INTERNAL"`). M4 still requires
   `bybase.get(name) == [path]` where `path = "corpus/knowledge/" + km.group(1)`, i.e. the after rev
   tracks exactly one non-`.ufo` file with that basename, at exactly that path; M3/M5 then require
   `afiles.get(path)` — read from the **same pinned extract** — to be a regular file with
   `1 <= lo <= hi <= len`. If `classify(v)` were anything but INTERNAL, the file would not exist as
   a regular file in that extract, so `afiles.get(path)` would be `None` and M5 would fail (the
   `classify` failure modes are a broken symlink or a gitlink, and the scope reader lists only
   regular files). So `INTERNAL` is entailed by (unique basename ∧ M5), and dropping the conjunct can
   never flip a verdict. `classify(v)` is also guaranteed non-GONE/non-mirror: a `corpus/…` path is in
   the rel domain, lane-first.
2. **`m5_basefiles`** (M5 measures the value's anchor against the base tree instead of the after
   tree). M5's `path` is `corpus/knowledge/<key name>.md`, always one of the M3-compared scope files.
   To make `bfiles` and `afiles` disagree on the *line count* an after scope file must change length,
   which M3 already fails (`same_files=False` or `bad_lines≥1`); if the file disappears, M3 fails as
   well. Content changes that keep the count are invisible to M5 either way. So any case where the
   two trees differ on this test already fails M3 and the mutant's delta cannot be observed.

The plant that *would* be needed is stated for completeness: for `m4_internal` a tracked path that
`git archive` does not materialize as a regular file, and for `m5_basefiles` an after scope file whose
line count changes — and both of those also fail M5/M3, which is exactly why the mutants survive.
These are redundant-guard findings, not permission to change the contract: the frozen limbs still
hold on the frozen inputs, and the C1 landing passes all of them.

## 6. Qualifiers routed to round 91 (not re-scoring; the frozen predicates decide C1)

**Q1 — the M5 limb is not independent.** `("M5", not m5bad and not m4bad, …)` folds M4's verdict into
M5: every M4 failure also prints `LIMB M5 FAIL` with `out_of_range=none` (observed in `dupbase`,
`gone`, `cross`). A reader must look at the detail column to know whether M5's own range check ran.
Not a C1 defect (both pass at the landing), but "M5 pass" alone is not evidence about ranges.

**Q2 — M5 range-checks the value's anchor against the *key's* file.** `path` is derived from
`km.group(1)`, not from `vm.group(1)`; in the `cross` plant the value names
`corpus/knowledge/ev-model.md:2` and M5 still passes (`out_of_range=none`) because it measured against
`claim-gates.md` (160 lines). M4's `bybase.get(name) == [path]` does not tie them either — it is a
statement about the *key's* basename only, and the cross plant satisfies it (that is why `m4_nameeq`
is the one mutant the plant kills). `vm.group(1) == name` is therefore the sole conjunct tying the
value's file to the key's file, and it belongs to M4, not M5. All 34 frozen values name their key's
file, so C1 is unaffected; a future map with a cross-file value would have its anchor range-checked
against the wrong entry (the value's own file could be short or missing and M5 would not see it).
Worth hardening: derive `path` from `vm.group(1)`.

**Q3 — the labels-rev pin is not exercised by the frozen control set.** Every frozen control passes
`--labels-rev <fixture base>`, whose labels bytes equal the worktree's, so a counter that read
`.ufo/waves/round-89/…/tranche5-labels.tsv` from the *worktree* instead of `git show labels_rev:path`
passes all six invocations. `mlabels_pin` demonstrates it (killed only by the added `lwrong` case);
`lfile`/`lrange`/`lwrong` are the shapes that pin the rev. The counter itself does pin correctly; the
control repertoire has a hole.

**Q4 — the `.ufo/` basename exclusion is load-bearing, and the lane leans on it heavily.** At base
there are 44 tracked paths named `claim-gates.md` (43 named `intake-surface.md`), and **43 of the 44**
live under `.ufo/`; the only non-`.ufo` one is `corpus/knowledge/claim-gates.md`. Dropping the
exclusion (`m4_ufo`) fails the **honest** candidate immediately, so the filter is what keeps M4's
uniqueness argument true. Consequence for future landings: any copy of a
knowledge file outside `.ufo/` (`docs/claim-gates.md`, another checkout committed into the tree)
makes C1's M4 fail on honest bytes — correct behaviour (uniqueness is the point), but a maintenance
hazard to know before adding files.

**Q5 — `pinned=archive` in the headline is a literal, not evidence.** `mpin_worktree` prints
`pinned=archive` while reading a copy of the working tree; the measure-mode probe shows the same
`rev=` line with `rate=812/1827` instead of `843/1829`. The pin is only visible in the numbers, so a
reader should treat the marker as a label, not a guarantee.

**Q6 — M6 is optional.** The digest limb is appended only `if a.map_sha256`; without the flag nothing
fails closed (`m6_drop` passes every case, including the positive control, with no M6 line). The
frozen predicate passes the flag with the frozen digest, so C1 is unaffected, but a future invocation
that omits it would silently drop the map pin.

**Q7 — `key_not_once` is the only guard against a map row that silently did not apply.** For a site
whose base line lacks the key, the line-equality check sees "nothing replaced" as equal; only the
key-once guard fails (`noop`: `key_not_once=1` with every other limb passing). Keep it: it is the
map's only proof that each repoint happened at its own citing line.

## 7. Restoration and hygiene

- The frozen counter was never written: sha256 `8f4ac21823979adb4096977ede78140eeade19baaa9072f546a5d6dd703836d4`
  before and after the whole battery. Mutants are scratch copies; the frozen c1/, c2/, controls/, l1/
  bytes and every instrument were read-only for this seat.
- No lane file was written outside `.ufo/waves/round-90/w1/` (this report and
  `MutC1Counter-receipts/`). No git/jj mutation touched the lane: the only commits are inside the
  scratch fixture repo, made with `git -C <fixture>` after asserting `rev-parse --show-toplevel`
  equals that fixture; the lane was read with `git -C <lane> archive/show/ls-tree` only.
- Scratch `/fast/scratch/hyaku/kasegi-r90/MutC1Counter` (fixture repo, 26 mutants, maps, label
  variants, work dirs, results) was **deleted before yield**; `TMPDIR` was passed explicitly for
  every run, nothing was written to `/tmp`, `~/.local/bin`, the fleet repo or any sibling lane.
- Credential hygiene: the receipts contain limb images, code lines and sha256 digests only — no
  fixture bytes, no copy of the counter/scanner, no `S<digits>.txt` snapshot, no planted value. The
  report plus its nine receipts (10 files) were self-scanned before yield with
  `python3 -B corpus/instruments/capture-secret-scan.py --files …`: `scanned=10 hits=0 files=0 allowed=0 rc=0`.
- No tool was installed or upgraded; `python3 -B` was used for every lane script.

Re-run: `bash .ufo/waves/round-90/controls/c1-controls-r90.sh <lane> 6088c3eb0c29040415c69e7b5fb91e110480ab26 <scratch>`
reproduces §2 byte-for-byte. Each mutant is one `old ==> new` replacement of the frozen counter; the
mutant table plus `MutC1Counter-receipts/mutants.tsv` (exact lines, hunk, sha256) and
`MutC1Counter-receipts/baseline.tsv` (case → expected pristine limb image) are enough to rebuild any
case: build the fixture (`git archive 6088c3eb | tar -x` into a scratch repo, commit), apply
`repair-map.tsv` with `apply-map.py` for the candidate, then
`python3 -B <mutant>.py --lane <fixture> --base-rev <base commit> --after-rev <cand commit> --map <map>
--labels-rev <labels commit> --base-target 812/1827 --target 843/1829 --map-sha256 <map sha> --work <scratch>/w`.
