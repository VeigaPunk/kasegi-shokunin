# Seat RevengerReceipt (kasegi round 43, w1) — the r42 receipt generator, reconstructed from bytes

Object: `.ufo/waves/round-42/final-gates/all-gates.txt` (33 lines, sha256
`8e42256eb249b9fe69de1bb7b5a7e63d8e8bf0a64385c00a0a145c5f1f36aa8c`), the artifact its
generator is `corpus/instruments/r42-closure.sh` (2185 lines, sha256
`fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b` at the receipt's own
`export-ref`). Method: read the instrument's bytes (not the round-42 prose), derive every
header field by direct git/file computation, then re-execute the instrument at the receipt's
ref and `cmp` the result against the committed artifact.

## 1. Reconstructed generator limb

### 1.1 Driver (shell, lines 35-105)

- Arg loop accepts `--export-ref --lane --work --scratch-root --receipt-out --selftest --leaf`;
  no `--export-ref` → prints `a plain run is refused (export mode only)` and exits 2 (lines 56-60).
- Ref resolution: `git -C "$LANE" rev-parse --verify --quiet "${EXPORT_REF}^{commit}"`; unresolvable
  → `ERROR ref-not-found ref=<r> closed=0 exit=1` exit 1 (lines 68-72) — distinct from the
  lane-missing red at line 62-65.
- Scratch: `SCRATCH_ROOT` defaults to `TMPDIR`, `mkdir -p`, then the suite owns
  `SUITE_SCRATCH="$SCRATCH_ROOT/r42-${RESOLVED:0:12}"` (line 78) and `WORK` (default
  `$SUITE_SCRATCH/work`). The ref-prefixed scratch name is what check_j13's `named=` fact later
  reads back.
- Export: `EXPORT="$WORK/export"`; `rm -rf` then
  `git -C "$LANE" archive "$RESOLVED" | tar -x -C "$EXPORT"`; failure →
  `ERROR export-failed ref=<r> closed=0 exit=1` exit 1 (lines 85-92).
- Hand-off: nine `export R42_*` variables (`LANE, EXPORT, WORK, SCRATCH_ROOT, REF, MODE, LEAF,
  RECEIPT_OUT, SELF`) then `exec python3 - <<'R42_ENGINE_PY'` (line 106). All grading happens in
  the embedded Python engine (lines 107-2184); the shell does no grading.

### 1.2 Engine constants

`CHECK_IDS = ["J1".."J13"]`, `NCHECKS = 13` (lines 127-128);
`DETERMINISTIC = ["J1","J2","J3","J4","J5","J6","J7","J9","J10","J11","J12","J13"]` —
**J8 is the only check excluded** (lines 130-132);
`RECEIPT_REL = ".ufo/waves/round-42/final-gates/all-gates.txt"`, `SUITE_REL =
"corpus/instruments/r42-closure.sh"`, `BASE_REF`, `R41_HEAD`, `DENSITY_SHA`,
`SENTINEL = "all-gates v2"` (lines 136-146).

### 1.3 Production order (main, lines 2134-2180)

1. `utc = ref_utc(REF)`; `sha = suite_sha()`.
2. `payloads[cid] = run_one(cid)` for `CHEAP = [J1..J7, J11, J12, J13]` (lines 2119-2131);
   `run_one` appends the replay limb (`payload = "%s,replay=%s"`) and ANDs its verdict.
3. `payloads["J9"] = check_j9(EXPORT)` — it re-invokes the suite recursively on `BASE_REF` and
   `R41_HEAD` with `--leaf` (nested_run, lines 1660-1678) and requires a tree-red control
   (`neg_accept`, lines 1650-1658).
4. `lines, summary, cases = run_selftest(payloads, run_lines_from(payloads, REF, utc, sha))`.
5. `payloads["J10"] = check_j10(cases)` — counts the *live* case records, not the receipt.
6. `provisional = run_lines_from(...)`; `payloads["J8"] = check_j8(EXPORT, payloads, lines,
   summary, provisional)`.
7. `run = run_lines_from(payloads, REF, utc, sha)` → written to stdout (line 2173).
8. `receipt = header + run[5:] + lines + ["selftest cases=%d failures=%d" % summary]` written by
   `write_text(RECEIPT_OUT, ...)` (lines 2170-2177). `header` is the five-line header; `run[5:]`
   is the thirteen payload lines plus the `closed=` line.
9. Exit `0` iff all thirteen closed, else `1` (lines 2179-2180).

### 1.4 Header fields

| line | value | derivation (bytes) |
|---|---|---|
| 1 | `all-gates v2` | `SENTINEL` constant, line 146 |
| 2 | `export-ref=<40 hex>` | the **resolved** commit of `--export-ref` (`R42_REF`), not the argument text |
| 3 | `suite-sha256=<64 hex>` | `sha256_file($EXPORT/corpus/instruments/r42-closure.sh)` (line 1431-1432) — the digest of the suite bytes *inside the exported tree at that ref*, i.e. a self-digest taken from committed content |
| 4 | `time-basis=ref-commit` | literal (line 2170) |
| 5 | `run-utc=<ISO Z>` | `ref_utc(REF)`: `git log -1 --format=%ct <REF>` → `datetime.fromtimestamp(int, tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")` (lines 240-248). **Wall clock is never read.** |

Verified: `git log -1 --format=%ct 4c40ef21…` → `1793200366` → `2026-10-28T15:12:46Z`, the exact
line 5 in the committed artifact; `git cat-file blob 4c40ef21…:corpus/instruments/r42-closure.sh |
sha256sum` → `fca5ae62…f6d6b`, the exact line 3.

### 1.5 Selftest block (how it is appended)

- `selftest_pass` (lines 2077-2096) walks `SELFTEST_SPECS` in J1..J13 order, runs
  `selftest_case(cid, payloads, provisional, ctx)`, and emits
  `selftest case=J<n> mutants=<good>/<total> positive=<pass|fail> payload-match=<0|1> verdict=<pass|fail>`
  where `pm = 1` iff the case's own freshly-computed payload equals `payloads[cid]` (with
  `,replay=…` stripped) and `verdict=pass` gates `positive AND pm==1 AND good==total`.
- `run_selftest` (lines 2099-2116) iterates to a fixed point (≤4 passes): J10 from `cases`, J8
  from a provisional transcript, then re-grades until the `(lines, summary)` pair stops moving.
  The fixed point exists because J10 and J8 each read the other's payload.
- The receipt's last 14 lines are exactly `lines` (13 graded case lines) + one summary line.
- **In run mode stdout carries only `run` (5 + 13 + 1 = 19 lines). In selftest mode stdout carries
  only the 13 case lines + summary. No single invocation prints the 33-line receipt**, so the
  receipt cannot be produced by `tee`-ing either mode; only `--receipt-out` (run mode) assembles it,
  and `--receipt-out` is ignored in selftest mode (main returns at line 2151).

### 1.6 What binds each line to the run

`check_j8` (lines 1584-1643) is the receipt grader. Its facts, in receipt order:
`sentinel`, `lines == 5+13+1+13+1 == 33`, `ref` nonempty, `digest` (`info["suite"] ==
suite_sha()` at the graded ref), `time-basis == "ref-commit"`, `utc == ref_utc(info["ref"])`,
`ancestor` (`git merge-base --is-ancestor <receipt-ref> <graded-ref>`), `diff`
(`git diff --name-only <receipt-ref> <graded-ref>` has ≤1 path and every path is the receipt),
`run-lines == 13`, `selftest-lines == 13`, `verdicts` (all 13 `verdict=pass`), `summary ==
(13,0)`, `closed-line == (13,13,0)`, `no-stray` (every other line matches a known regex),
`payload-match` (12 deterministic payloads re-derived at the graded ref), `forged` (six
structural forgeries rejected by the reader). Consequence: the payload body is bound to the
tree; the header is bound to a commit object; the selftest block is bound only to *shape*.

## 2. Byte-level reproduction (evidence)

Command (scratch outside the lane, `TMPDIR` bound):

```
S=/fast/scratch/hyaku/kasegi-r43/RevengerReceipt; mkdir -p "$S/repro"; cd "$S/repro"
export TMPDIR="$S/repro"
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r42-closure.sh \
  --export-ref 4c40ef21cced6ebed592e5622996ab41996e2da9 \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --work "$S/repro/w" --scratch-root "$S/repro" \
  --receipt-out "$S/repro/all-gates.txt" > "$S/repro/stdout.txt" 2>"$S/repro/stderr.txt"
```

Output: `exit=0`, `real 3m55.314s`, stderr 0 bytes, `wc -l all-gates.txt` = 33,
`wc -l stdout.txt` = 19.

```
cmp "$S/repro/all-gates.txt" <lane>/.ufo/waves/round-42/final-gates/all-gates.txt
→ byte-identical
sha256sum both  → 8e42256eb249b9fe69de1bb7b5a7e63d8e8bf0a64385c00a0a145c5f1f36aa8c (both)
diff <(sed -n '1,19p' all-gates.txt) stdout.txt → no output (stdout == receipt lines 1-19)
git diff --name-only 4c40ef21… b2c49ea5…  → .ufo/waves/round-42/final-gates/all-gates.txt (exactly one)
git log -1 --format=%ct 4c40ef21…          → 1793200366  (== 2026-10-28T15:12:46Z)
```

So the committed receipt is a **deterministic pure function of the ref**: same ref, same 33 bytes,
at any later wall-clock time. J = `4c40ef21…` (receipt dropped), Y = `b2c49ea5…` (adds only the
receipt); the receipt names J, not Y.

## 3. The one place the r42 receipt could have been forged

**The post-`closed=` selftest block — receipt lines 20-33 — is the unbound section; and its
sibling, the J8 payload line, is the only payload line that is never re-derived.** Every other
line is pinned: 12 payloads are re-derived at the graded ref (`DETERMINISTIC`), the five header
fields are recomputed from the commit object and the exported suite bytes, and the `closed=` line
and summary are checked against `(13,13,0)` / `(13,0)`. The 13 `selftest case=` lines are checked
only for matching `SELFTEST_RX` and ending in `verdict=pass` (`verdicts` fact, line 1625); their
`mutants=<a>/<b>`, `positive=`, and inner `payload-match=` values are never recomputed, and
`check_j10` grades the *live* run's case records, not the committed block. `J8` is excluded from
`DETERMINISTIC` outright (line 130).

Executed proof (`$S/harness/forge_probe.py`: imports the extracted engine, grades the export at
`b2c49ea5…`, passes the live payload lines from the reproduction above):

```
genuine                            ok=True  payload-match=12/12,forged=6/6
selftest-lines-rewritten=13
selftest-block-forged              ok=True  payload-match=12/12,forged=6/6
selftest-forged+J3-edited          ok=False payload-match=11/12,forged=6/6
J8-payload-edited                  ok=True  payload-match=12/12,forged=6/6
```

The forged block is `selftest case=J1 mutants=999/999 positive=pass payload-match=1
verdict=pass` for all thirteen cases — an impossible tally — and `check_j8` returns `ok=True`.
Editing one deterministic payload line (J3) is caught immediately (11/12). Editing the J8 line's
own `payload-match=0/12,forged=0/6` is accepted. So: **the receipt's own evidence that its checks
can fail is the one thing a forger can rewrite without any check noticing.**

Why the J8 line is excluded — directly observable, not inferred: at mint time (receipt absent) the
engine grades a synthetic canonical transcript and prints
`J8 payload=receipt=(canonical),source=canonical,…`; grading the same receipt at Y prints
`receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,…` (executed above). The
payload is not ref-stable, so it cannot join `payload-match` as-is.

Secondary, same class: the receipt's `run-utc` is the *commit* timestamp, not the run instant, so
the artifact attests no execution time at all; the reproduction above re-minted the identical bytes
hours later. And at J — where the receipt does not exist — `check_j8` takes its canonical branch — no receipt found, so
`locate_receipt` (lines 1494-1506) returns nothing and check_j8 sets `rel=(canonical)`,
`source=canonical` — and still reports `closed=1`, which
is how the r42 judged head is 13/13 with no committed receipt in its tree.

## 4. Production recipe the r43 receipt must follow

Derived from §1-§2; r43 names substituted (`all-gates v3`, 19 checks, receipt at
`.ufo/waves/round-43/final-gates/all-gates.txt`). The r43 suite does not exist yet at this
writing, so the engine-level numbers below are the contract it must meet [INFERENCE from the
frozen claims' 19/19 + 19 selftest cases + the r42 engine shape]: header 5 lines + 19 payload
lines + `closed=` 1 line + 19 selftest case lines + summary 1 line = **45 lines**.

1. **Mint at the judged head J, once, with `--receipt-out` in run mode.** All round-43 changes are
   committed at J; the receipt is the only thing Y adds.

   ```
   S=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r43 r43receipt.XXXXXX)
   cd "$S"; export TMPDIR="$S"
   bash <lane>/corpus/instruments/r43-closure.sh \
     --export-ref <J> --lane <lane> \
     --work "$S/w" --scratch-root "$S" \
     --receipt-out <lane>/.ufo/waves/round-43/final-gates/all-gates.txt \
     | tee "$S/run.stdout"
   echo "exit=${PIPESTATUS[0]}"
   ```

   Expected: `exit=0`, `closed=19/19 exit=0` on the last transcript line, stderr empty, and
   `<receipt>` exactly 45 lines. Do not use `--selftest` for the minting invocation (it ignores
   `--receipt-out` and prints 20 lines, not 45).

2. **Prove the artifact is the engine's own write, not a captured transcript.** The receipt's first
   25 lines (5 header + 19 payload + `closed=`) must equal the 25-line run transcript:

   ```
   sed -n '1,25p' <receipt> | cmp - "$S/run.stdout"
   ```

   Lines 26-45 (the selftest block) never cross stdout in any mode; if they were pasted in by
   hand, step 5 is the only thing that can expose it (see §5).

3. **Commit Y = J + this one file.** `git diff --name-only <J>..<Y>` must print exactly
   `.ufo/waves/round-43/final-gates/all-gates.txt`. The header must read `export-ref=<J>` (not Y:
   Y contains the receipt and cannot name itself), `time-basis=ref-commit`, and
   `run-utc=<J's %ct as ISO Z>` — recompute both with
   `git log -1 --format=%ct <J>` and
   `git cat-file blob <J>:corpus/instruments/r43-closure.sh | sha256sum` and compare to the
   receipt's `run-utc=` and `suite-sha256=` lines.

4. **Verify at Y.** `bash <lane>/corpus/instruments/r43-closure.sh --export-ref <Y> --work "$S/w2"
   --scratch-root "$S"` must print `closed=19/19 exit=0`, and the K8 payload must read
   `source=committed` (receipt actually graded, not synthesized). Then `--selftest --export-ref <Y>`
   must print nineteen `selftest case=K<n> … verdict=pass` lines and `selftest cases=19 failures=0`.

5. **Independently reproduce it.** Re-run step 1 into a throwaway path and `cmp` against the
   committed receipt; it must be byte-identical (proven property, §2). This is the *only* check
   that currently covers the selftest block, and it must be in the report as a command, not a
   claim.

6. **Never**: hand-edit the receipt, append a note, paste a selftest block, produce two headers or
   two `run-utc=` lines, mint with an `--export-ref` other than J, write the receipt from a working
   tree instead of an export, or reuse a receipt minted at another ref.

## 5. Where the r43 suite must differ

The r43 receipt inherits the r42 hole verbatim unless the r43 engine closes it. Two changes are
required, and both are visible against the r42 byte anchors:

1. **Re-derive the committed selftest block.** K8 must run its own nineteen cases against the
   receipt's ref and compare each committed `selftest case=K<n>` line token-for-token (`mutants=`,
   `positive=`, `payload-match=`, `verdict=`), not just count them and require `verdict=pass`
   (r42: line 1625 `verdicts`). Without this, `mutants=999/999` is accepted — executed, §3.
2. **Bind K8's own line.** Either make the K8 payload ref-stable (drop or normalize the
   `receipt=`/`source=` cells that flip `(canonical)`/`canonical` → path/`committed` between J and
   Y, quoted in §3) and include K8 in the re-derived set, or compare the committed K8 payload
   against the value the grader computes from that same receipt. Otherwise the line that grades
   the receipt is the one line a forger may write freely.

Both must stay outside K1-K7/K9-K13, whose payloads and replay limbs are frozen unchanged; the
natural vehicles are K8 itself (facts, not cells, if the grammar must not move) and the r43-only
K14-K19 surface. [INFERENCE] Whether the frozen "payload grammar unchanged" wording permits a new
K8 cell is an integration decision for the L1; the requirement is that some green/red limb in the
r43 suite changes when a committed selftest line is fabricated, and today none does.

Until that lands, the r43 receipt's claim "one unedited tee of one run" rests on step 5
(reproduce and `cmp`), not on the suite.

## 6. Confidence, environment, scratch

- Generator/recipe: **high** — read line-by-line and reproduced byte-identically (sha256 match).
- Forgery finding: **high** — executed probe with live payloads; behaviour observed, not inferred.
- r43 45-line shape: **inference** from frozen claims + r42 engine; recompute against the landed
  r43 instrument before quoting it in the report.
- Tooling: none installed, none upgraded (no pacman, no network).
- Network: none used.
- Scratch: `/fast/scratch/hyaku/kasegi-r43/RevengerReceipt/` (repro, reproY export, harness),
  removed before yield.

Deliverable: `.ufo/waves/round-43/w1/RevengerReceipt.md`. Body (lines 1-265) sha256 =
`81db3ca7499793ec4a1f6509f6975be3657ed45170ea4e64457b5f455d9347cb`; the file adds this trailer
line (reproduce: `sed -n '1,265p' RevengerReceipt.md | sha256sum`).
