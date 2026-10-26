# LabDeterminismY — round-40 falsify wave 2 receipt (H7 determinism probe)

Attacked: the C1 closure suite `corpus/instruments/r40-closure.sh` (suite-sha256 `bdbd18a3…897f1e`, verified equal to `git show 3074c76:corpus/instruments/r40-closure.sh | sha256sum` and to the working-tree file) and the committed receipt `.ufo/waves/round-40/final-gates/all-gates.txt` (1062 bytes, sha256 `7b8cda36c793c5855fa6ffcb78d241fca47f0d3679b2d7c38f7a959042463484`). Claim attacked: "the transcript is a function of the tree and the ref-scoped facts only, so two plain runs over the same ref are byte-identical and the receipt equals a re-run with nothing normalised" (H7).

Result: **byte-identity REPRODUCED; no nondeterminism found. One documented-limit contradiction (D1) and one procedural observation (O1) below.**

## 0. What "Y" is at the time of this probe

Lane tip is `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (= J, the ref the receipt names; committer instant 2026-10-26T21:56:22Z = receipt `run-utc`). `all-gates.txt` is still UNTRACKED in the lane working tree (`git status --short`: `?? .ufo/waves/round-40/final-gates/`), so no commit Y = J + receipt exists in the lane yet (re-checked at the end of the seat: same). The contract's `--export-ref <Y>` therefore cannot be run against the real lane. I measured two things instead:

1. `--export-ref J --lane <real lane>` (the actual lane, receipt absent from the export).
2. `--export-ref Y' --lane <scratch clone>` where Y' = `1031d7cb2e9758ffe2b83833b5a1fee5ef1a95de` is a commit I made in a throwaway `git clone --no-hardlinks` of the lane (toplevel asserted equal to the clone dir before commit), adding only the byte-exact committed receipt; `git diff --name-only J Y'` lists exactly `.ufo/waves/round-40/final-gates/all-gates.txt`. This is exactly the lane shape Y will have. Y' differs from the real Y hash, but the transcript names only J, so the output is hash-independent of Y.

## 1. Required probe (as specified)

Commands (cwd and TMPDIR in my scratch; absolute paths):

```
bash <lane>/corpus/instruments/r40-closure.sh --export-ref Y' --work $S/ya --lane <clone>   -> exit 0
bash <lane>/corpus/instruments/r40-closure.sh --export-ref Y' --work $S/yb --lane <clone>   -> exit 0
diff ya-out yb-out                 -> empty, cmp identical
diff ya-out all-gates.txt          -> empty, cmp identical (nothing normalised)
```

Result: **closed=10/10 exit=0; run A == run B == committed receipt, byte for byte** (three identical sha256 `7b8cda36…63484`). Transcripts: `LabDeterminismY.Y-run-a.txt`, `LabDeterminismY.Y-run-b.txt` (wall ≈4 s each).

At J on the real lane (receipt absent from the export — the documented "9/10 by construction" state), two runs `--work $S/a` / `--work $S/b`: exit 1, both **byte-identical to each other** (`LabDeterminismY.J-run-a.txt`, `…-b.txt`), `closed=9/10 exit=1`, header lines 1-5 and H1-H6, H8-H10 lines identical to the receipt; the only differing line is H7 (`receipt=0,sentinel=0,ref=,…,h7-line=0 closed=0`, receipt missing) plus the tally line. This is exactly the documented green-window behaviour, reproduced.

## 2. Extra attacks on determinism (all vs. the committed receipt, `cmp`, nothing normalised)

| variant | result |
|---|---|
| `TZ=Asia/Tokyo LC_ALL=C` | IDENT, 10/10 |
| `TZ=America/Los_Angeles LANG/LC_ALL=de_DE.UTF-8` (locale absent on host; bash warns on stderr only) | IDENT, 10/10 |
| `TZ=UTC LC_ALL=POSIX` | IDENT |
| reused `--work` dir (stale export/mut/neg-*/h5) | IDENT |
| no `--work` (auto) | IDENT |
| invoked by relative path from `corpus/instruments`, absolute `--work` | IDENT |
| abbreviated `--export-ref` (12 hex) | IDENT (header prints the resolved 40-hex) |
| 8 concurrent plain runs, distinct `--work` | 8/8 IDENT |
| 5 sequential runs on one reused `--work` | 5/5 IDENT |
| `--receipt-out` at Y' | written file IDENT to committed receipt |
| `--receipt-out` at J (real lane) | exit 0, file == stdout == committed receipt (H7 is satisfied against the output file in this mode by design; this is how the receipt was producible at J) |
| strace (`-f`, openat/mkdir/rename/unlink/creat) of a full run at J on the real lane | zero writes under the lane path; all writes under scratch (tar extraction is relative to the export dirfd) |

## 3. Findings

**D1 (contradiction with a documented claim; host-state dependence, severity low-medium).** The suite header says of H6: "moving --work inside or outside the scratch root does not change the transcript." Measured: with the default `--scratch-root /fast/scratch/hyaku` and `--work` OUTSIDE the `kasegi-r40` family dir (I used `/tmp/<dir>/w` and `/var/tmp/<dir>`), the run reads the live family dir `/fast/scratch/hyaku/kasegi-r40` as a stray: H6 `strays=1 closed=0`, and the damage cascades into H5 (`control=6/8`), H7 (`payload-match=6`, `h7-line=0`) and H8 (`base=2/10 r39=1/10`) → **closed=7/10 exit=1** (`LabDeterminismY.work-outside-scratch.txt`, diff vs receipt = 7 lines: H5, H6, H7, H8, tally). With `--scratch-root` pointed at an empty root, or `--work` under the family dir, it is 10/10 IDENT. A scratch root with two family strays (`kasegi-r40b`, `kasegi-r39-old` beside the work family) → `strays=2`, 7/10 (`LabDeterminismY.two-strays.txt`). Consequences: (a) the receipt is reproducible only when `--work` lies under the single live `kasegi-r40*` directory or `--scratch-root` is clean — the header's wording is wrong, and a verifier that picks any other `--work` (including the H6 verifier's own checkout) while `/fast/scratch/hyaku/kasegi-r40` exists will read RED from a correct tree; (b) H5 and H8 inherit H6's liveness through their nested runs, so "H8 base=3/10" in the receipt is itself a function of live scratch state, not just of the tree. Recommendation: verify with `--work` under `/fast/scratch/hyaku/kasegi-r40/<seat>/` (as I did) or `--scratch-root` a clean dir, and fix the header sentence (it is the H6 liveness limit the same header lists above, not "does not change the transcript").

**O1 (procedural, not a suite defect).** At the time of this probe Y is not a lane commit: the receipt is untracked in the working tree and the lane tip is J. The contract's "green window" (10/10) therefore exists only after the L1 commits J+receipt; H7/H9/H10 on the real Y should be re-run once that commit exists (the transcript will be unchanged because it names J, as my Y' fixture shows).

**No defects found for:** nondeterminism across runs, TZ, locale, cwd, work-dir reuse, concurrency, ref abbreviation, or `--receipt-out`; suite-sha256 header; run-utc (`time-basis=ref-commit`, equals J committer instant 2026-10-26T21:56:22Z); lane write-freedom.

## 4. Tooling

No tools installed or upgraded (strace pre-existing at /usr/bin/strace). Read-only git only against the lane; the one commit (Y') was made in my scratch clone with the host's existing global git identity. Scratch `/fast/scratch/hyaku/kasegi-r40/LabDeterminismY` removed before yield.

## 5. Deliverables

`LabDeterminismY.md` (this), `LabDeterminismY.J-run-a.txt`, `LabDeterminismY.J-run-b.txt`, `LabDeterminismY.Y-run-a.txt`, `LabDeterminismY.Y-run-b.txt`, `LabDeterminismY.work-outside-scratch.txt`, `LabDeterminismY.two-strays.txt` (all byte-exact stdout of the named runs).
