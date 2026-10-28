# R44Exec7 — r43 selftest transcript export-ref omission: read-only validation + locally checkable record format

- seat: `R44Exec7` (leaf executor, read-only for lane bytes; writes only this report)
- assigned item: read-only validate the round-43 selftest transcript's `export-ref` omission and propose a locally checkable record format
- lane: `kasegi-shokunin`; base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; head at work time `66314015122b9aa32dc40f2f1815df56624c26d1` (`round-44: freeze claims and validated wave`)
- frozen targets read first: `.ufo/waves/round-44/claims.json` (C1/C2), `.ufo/waves/round-44/controls/do-nothing.txt`
- method: `git cat-file` / `git show` / `git ls-tree` / `sha256sum` / `wc` / `grep` over committed bytes, plus one prototype checker run only on **scratch fixtures and committed files, never on the suite** (no gate executed). `GIT_OPTIONAL_LOCKS=0` on every git read.
- no lane byte, index, ref or file was modified; no tool installed; no scratch outside `$HYAKU_SCRATCH` (`/fast/scratch/hyaku/kasegi-r44/R44Exec7/`, deleted on exit — see §8).

## 1. Verdict

The routed defect is **real, structural, and currently unchecked**, and it is *provenance-only*: the transcript's content is internally coherent, but nothing in the file identifies the export or the suite that produced it. Its provenance **is** committed and is recoverable locally without executing anything — the headerless half is a byte-exact tail of a committed 33-line self-identifying receipt (§2.3). I propose one normative record format (§3) and demonstrate a read-only checker that is red on the frozen file as committed, green on the same bytes plus a digest-binding record, and red again on each of five mutants and two negative controls (§4). Do-nothing cannot reach any of that (§6).

## 2. Validation (exact evidence)

### 2.1 The file names no export and no suite

```
$ F=.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt
$ sha256sum "$F"; wc -l < "$F"; stat -c '%s' "$F"
44218ef85489198e58c20e3e452a8d637e02f27751828b542dd0c023bdf26a95  .../r42-at-de09313-selftest.txt
14
969
$ grep -cE '^(all-gates v|export-ref=|suite-sha256=|suite-path=|time-basis=|run-utc=|mode=)' "$F"
0
$ sed -n '1p;$p' "$F"
selftest case=J1 mutants=0/1 positive=pass payload-match=1 verdict=fail
selftest cases=13 failures=3
$ GIT_OPTIONAL_LOCKS=0 git ls-tree HEAD -- "$F"
100644 blob 522d0d93161cc123eb1aca3f19eafd0c562c0579	.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt
```

The sibling **run** half does carry the header (`export-ref=de09313e8edb98280b19767d0094bb2dd8031d73`, `suite-sha256=d92c0de1…`, 19 lines, sha `62709c3a…`), so the *pair* is half self-identifying — the exact wording of the spot-check (`corpus/lessons/round-43-verifier-spotcheck.md:29`, defect `§6.5` at `:105`).

### 2.2 Root cause is the emitter, not a transcription slip

`corpus/instruments/r42-closure.sh` — the `--selftest` branch returns before the header list is ever built:

```
2140	    if MODE == "selftest":
...
2148	        lines, summary, _cases = run_selftest(payloads, provisional)
2149	        sys.stdout.write("\n".join(lines) + "\n")
2150	        sys.stdout.write("selftest cases=%d failures=%d\n" % summary)
2151	        return 0 if summary[1] == 0 else 1
...
2170	    header = [SENTINEL, "export-ref=%s" % REF, "suite-sha256=%s" % sha,
2171	              "time-basis=ref-commit", "run-utc=%s" % utc]
...
2175	    if RECEIPT_OUT and not LEAF:
2176	        receipt = header + run[5:] + lines + ["selftest cases=%d failures=%d" % summary]
2177	        write_text(RECEIPT_OUT, "\n".join(receipt) + "\n")
```

So `--selftest` **stdout** is headerless by construction; only the `--receipt-out` form carries the 5-line header. The seat that produced the artifact said the same in prose (`.ufo/waves/round-43/w1/ExecK18Transcript.md:115`: "concatenated unedited with no header"). `[INFERENCE]` The committed 14-line file is therefore exactly what `--selftest` stdout produces; nothing about the file is anomalous — the *format* is.

### 2.3 The provenance exists, in a path the gate refuses as evidence

The self-identifying form **is** committed, as the 33-line tee the r43 seat proposed:

```
$ T=.ufo/waves/round-43/w1/ExecK18Transcript.de09313-tee.txt
$ wc -l < "$T"; sha256sum "$T"
33
44a53379bf3151d8f1667aa8f6c3417dc77b5a4e0149afac3288e04ea42d9db6  .../ExecK18Transcript.de09313-tee.txt
$ sed -n '1,3p' "$T"
all-gates v2
export-ref=de09313e8edb98280b19767d0094bb2dd8031d73
suite-sha256=d92c0de1e3b4d01ca330994c781fda6aeb0cfd874f00f6d17641c3f6bc73f464
$ head -19 "$T" | sha256sum   # == run half
62709c3aed5a1b5cdcfc3bd20e14ce8a43f4d59f8967f0140744a691d1f072a0  -
$ tail -14 "$T" | sha256sum   # == selftest half
44218ef85489198e58c20e3e452a8d637e02f27751828b542dd0c023bdf26a95  -
```

The pair is a byte-exact split of that tee (`2975 B = 2006 + 969`). And the tee lives under `.ufo/waves/round-43/w1/`, which the round's own binding gate excludes:

```
corpus/instruments/r43-limbs/k18-transcript.sh:126:EVIDENCE_DIRS = (".ufo/waves/round-42",
127:                 ".ufo/waves/round-43/final-gates",
128:                 ".ufo/waves/round-43/c1-controls")
```
with the stated reason at `k18-transcript.sh:30` ("seat receipts are claims, not evidence").

**Consequence, measured:** the token `selftest cases=13 failures=3` is bound by exactly one evidence file, and it is the headerless one:

```
$ grep -rn '^selftest cases=13 failures=3$' .ufo/waves/round-42 .ufo/waves/round-43 | grep -v '/w1/'
.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt:14:selftest cases=13 failures=3
```

So K18's binding for that quote rests entirely on an unattributed record, while the attributed record is inadmissible by K18's own scope rule. That is the defect's actual cost, and it is why "the run file does name it" is not sufficient.

### 2.4 No existing gate can see it

- `r42-closure.sh:136` `RECEIPT_REL = ".ufo/waves/round-42/final-gates/all-gates.txt"` and `r43-closure.sh:50` `RECEIPT_REL=".ufo/waves/round-43/final-gates/all-gates.txt"` — J8/K8 grade the header of **one** receipt file each.
- `grep -rn "selftest.txt\|-selftest" corpus/instruments/*.sh corpus/instruments/*.py` → no instrument references a split half (only unrelated `--selftest` flags).
- K18 grades *tokens*, not headers; it never looks at `export-ref` in an evidence file.

### 2.5 The successor suite fixes only half the class

`corpus/instruments/r43-closure.sh`:

```
509	if [ "$MODE" = "selftest" ]; then
510	    ST_OUT="$WORK/selftest-block.txt"
511	    selftest_block > "$ST_OUT"; ST_RC=$?
512	    cat "$ST_OUT"                      # <-- stdout still headerless
513	    if [ -n "$RECEIPT_OUT" ]; then
514	        cat "$RUN_BLOCK" "$ST_OUT" > "$RECEIPT_OUT"   # <-- receipt carries the header
```

and `RUN_BLOCK` (`:498-507`) carries `all-gates v3`, `export-ref`, `suite-sha256`, `time-basis`, `run-utc` — but **no `mode=` and no `suite-path=`**. Measured on the committed Y receipt: 4 of my 9 predicates pass and 2 fail only for the missing `mode=` line (§4, row C1/C2).

### 2.6 The class is not a one-off: the lane has four transcript shapes and no normative one

`find .ufo/waves -name '*-selftest.txt'` → 6 files, four shapes:

| shape | file | first line |
|---|---|---|
| bare summary, no provenance | `.ufo/waves/round-29/wave1/c1-controls/base-control-selftest.txt` | `selftest cases=9 failures=0` |
| bare summary, fabricated-looking | `.ufo/waves/round-33/wave1/ExecRegressionC1/fake-selftest.txt` | `selftest cases=0 failures=0` |
| inline per-line provenance | `.ufo/waves/round-40/wave2/CritReceiptForge.transcript-selftest.txt` | `selftest export-ref=a67011b2… suite-sha256=bdbd18a3…` |
| header block (receipt) | `.ufo/waves/round-43/final-gates/all-gates*.txt` | `all-gates v3` |
| headerless split half | `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt` | `selftest case=J1 …` |

A record format is what is missing; the r43 omission is its most visible symptom.

## 3. Proposed record format (normative, locally checkable)

**Rule R0 (self-identification).** Every transcript written to a path is self-identifying: a header block, a body, and a mode-appropriate summary.

**Header block** — exactly these lines, each at most once, in this order (extra lines ignored):

```
all-gates v<n>                      suite family sentinel
export-ref=<40 hex>                 the export the suite graded
suite-path=corpus/instruments/<f>   which suite file (new; makes the digest checkable without a lookup table)
suite-sha256=<64 hex>               sha256 of `git show <export-ref>:<suite-path>`
time-basis=ref-commit
run-utc=<ISO-8601 Z>
mode=selftest|run|receipt           new; the discriminator
```

**Body and summary by mode**

| mode | body | summary |
|---|---|---|
| `selftest` | `^selftest case=<id> … verdict=<pass\|fail>$`, no `payload=` lines | `selftest cases=<n> failures=<k>` with `n` = case count, `k` = `verdict=fail` count |
| `run` | `^<ID> payload=… closed=<0\|1>$` | `closed=<n>/<m> exit=<k>` with `m` = payload-line count |
| `receipt` | both halves concatenated (today's `--receipt-out` form) | both summaries; both counts checked |

**Rule R1 (split halves).** If a receipt is split into `<name>-run.txt` and `<name>-selftest.txt`, **each half repeats the 7-line header** (the r43 successor already does this for `--receipt-out`; it must do it for stdout too, `r43-closure.sh:512`). The byte rule is mechanical: run half = first `7 + N_payload + 1` lines of the receipt; selftest half = last `N_cases + 1` lines.

**Rule R2 (frozen records).** A transcript that predates the format is never rewritten. It is bound by a **sidecar** record in an evidence directory of the *current* round, carrying `binds=<path of the frozen file>`, `transcript-sha256=<sha of the frozen bytes>`, plus the same header fields and summary. The sidecar cannot alter the frozen bytes, and the digest makes any later substitution detectable.

**Compatibility.** Adding `mode=`/`suite-path=` to `RUN_BLOCK` does not disturb K8: its header predicates are `grep -m1`/`grep -c` over named prefixes (`r43-closure.sh:149-157`), so extra header lines are inert.

## 4. Prototype checker and discrimination matrix

Prototype (scratch only, 190 lines, `selftest-record-check.py`): nine predicates over committed bytes — P1 sentinel, P2 export-ref present once, P3 ref resolves as a commit, P4 `suite-sha256` equals `sha256(git show <ref>:<suite-path>)`, P5 mode discriminator, P6 count coherence, P7 pair agreement, P8 sidecar digest+binds+chain, P9 byte-exact derivation from a full receipt. No gate is executed; every input is `git`/`sha256sum`/text.

| # | record | invocation | result |
|---|---|---|---|
| A | proposed-format selftest record (3 cases, 1 fail) | `--pair good.run.txt` | `pass:7/fail:0/skip:2` **pass** rc 0 |
| M1 | same, `suite-sha256` zeroed | — | `fail` on **P4** only, rc 1 |
| M2 | same, `export-ref` = `1111…` (nonexistent) | — | `fail` on **P3+P4**, rc 1 |
| M3 | same, one case line deleted | — | `fail` on **P6** (`declared=3/1 counted=2/0`), rc 1 |
| M4 | same, one `payload=` line injected | — | `fail` on **P5** only, rc 1 |
| M5 | frozen selftest half, J1 verdict flipped fail→pass | `--sidecar … --derive-from tee` | `fail` on **P6/P8/P9**, rc 1 |
| C1 | `final-gates/all-gates.at-Y.txt` as committed | `--suite-path corpus/instruments/r43-closure.sh` | `pass:4/fail:2` — only **P5/P6** fail, for the absent `mode=` line |
| C2 | same bytes + one `mode=receipt` line | same | `pass:6/fail:0/skip:3` **pass** rc 0 |
| D | **frozen defect file, as committed** | bare | `pass:1/fail:5` — **P6 ok** (`declared=13/3 counted=13/3`), **P1–P5 fail**: content coherent, provenance absent |
| E | **same frozen bytes + sidecar + derivation** | `--sidecar r43-selftest.binding.txt --derive-from …/ExecK18Transcript.de09313-tee.txt` | `pass:8/fail:0/skip:1` **pass** rc 0 |
| N1 | frozen file derived from the **wrong** receipt | `--derive-from …/all-gates.at-Y.txt` | `fail` on **P9** (`header-agrees=False`), rc 1 |
| F | run half, derived from the tee | `--derive-from tee` | `pass:5/fail:2` — **P9 ok**; **P5/P6** fail for the absent `mode=` line |

Key discriminations:

- **D vs E**: identical frozen bytes; only the added binding record flips the verdict. The check is therefore *about* provenance, not content — exactly the defect.
- **A vs M1–M4**: each mutant fails exactly the predicate that owns its lie; no mutant is caught by a neighbour, and no honest record is rejected.
- **N1**: derivation is not "any receipt will do" — the segment must be byte-equal *and* the receipt's header must agree on ref and digest.
- **C1 vs C2**: the lane's native receipt is one header line away from full local checkability.

Cost: `real 0m0.022s` per record (bash `time`, warm cache). Population today: 1 attestation-path split half; the format applies to every future transcript.

## 5. Remediation options (append-only, ranked)

1. **Bind the frozen record (preferred, no rewrite).** Commit `R44`-side `.ufo/waves/round-44/final-gates/r42-at-de09313-selftest.binding.txt` with the 9 sidecar lines shown in §4/E (it points into the frozen path by `binds=` and pins the frozen bytes by `transcript-sha256=44218ef8…`). This closes the *verifiability* gap without touching round-43 bytes, and is checkable by P8 alone.
2. **Land the check.** Add the nine predicates as a new limb (e.g. `K20`) over every `*-selftest.txt`/`*-run.txt` in the evidence dirs, with the frozen file as its red-before control and §4/E as its green-after. Red-before evidence is already in hand: D = `pass:1/fail:5`, rc 1.
3. **Fix the emitter for the r44 suite** (not r42's): `RUN_BLOCK` gains `suite-path=` and `mode=`; `--selftest` stdout emits `cat "$RUN_BLOCK" "$ST_OUT"` instead of `cat "$ST_OUT"` (`r43-closure.sh:512`), so a future `| tee` capture cannot lose the header again. No r44 suite exists at head (`ls corpus/instruments | grep -E 'r4[234]'` → `r42-closure.sh r43-closure.sh r43-limbs r44-routed-defects.py`), so the format lands before the first r44 transcript is written.
4. **Do not rewrite the frozen artifact, and do not edit `r42-closure.sh`.** The r42 suite's digest `d92c0de1…` is the identity by which **12 committed lane files** describe that instrument (`grep -rl d92c0de1… | grep -v '\.ufo/scratch/'` → 12); the defect is in how the record is *split*, not in the suite's verdicts, and the suite's `--receipt-out` form is already correct. Append-only is the lane rule (fleet `PROTOCOL.md:463`: "entries are never rewritten or deleted; corrections land as new entries").

## 6. Do-nothing discrimination

At head `6631401` the frozen file is byte-identical to its round-43 blob (`522d0d93…`), no binding record exists, and no instrument reads a split half (§2.4). Do-nothing therefore yields: the omission unchanged, `selftest cases=13 failures=3` still bound by exactly one unattributed file, and **no** red/green pair — the §4/E state (`pass:8/fail:0`, rc 0) is unreachable without an added record and an added check. The proposed counter is falsifiable in both directions: `D` must stay `verdict=fail` on the frozen bytes and `E` must be `verdict=pass` on those same bytes plus the binding.

## 7. Limitations

- `[INFERENCE]` I did not re-run `r42-closure.sh --selftest` to reproduce the 14 lines: the lane's own rule (spot-check §method) has the integrator read committed evidence, never run a sibling's gate, and running it would need a scratch export tree. The claim "stdout is headerless" rests on source lines `2140-2151` and on the seat's stated provenance (`ExecK18Transcript.md:115`), not on a fresh execution.
- The prototype is a demonstration of the predicates, not a landed instrument: it lives in scratch and was run only against committed files and scratch fixtures. It has no selftest of its own beyond the M1–M5/N1 mutants in §4.
- P7 (pair agreement) is only demonstrated on synthetic fixtures: the real pair cannot satisfy it today (the selftest half has nothing to agree with) — that *is* the defect.
- The format is proposed for records the lane writes; it does not retro-fit the five legacy shapes in §2.6 beyond the sidecar route. The round-40 inline form (`selftest export-ref=… suite-sha256=…` per line) would need one extra extraction regex if it is to be graded too.
- Sidecar placement is a policy call for L1: an `r44` evidence dir is the append-only-safe choice, but it makes the binding one hop away from the frozen file. Placing the sidecar inside `.ufo/waves/round-43/final-gates/` is closer but adds a file to a closed round's attestation dir; I recommend the former and flag the trade-off rather than deciding it.
- Concurrent state observed, not used: `corpus/instruments/r44-routed-defects.py` appeared untracked (90 lines) mid-session — a sibling's in-flight work. None of my findings depend on it.

## 8. Report trailer (relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

Files written by this seat:

- `.ufo/waves/round-44/wave1/R44Exec7.md` (this report)

Scratch (outside the lane, deleted on exit):

- `/fast/scratch/hyaku/kasegi-r44/R44Exec7/selftest-record-check.py` (prototype)
- `/fast/scratch/hyaku/kasegi-r44/R44Exec7/{good.selftest.txt,good.run.txt,m1-bad-suite.txt,m2-ghost-ref.txt,m3-dropped-case.txt,m4-payload-leak.txt,m5-flipped-verdict.txt,receipt-mode-added.txt,r43-selftest.binding.txt,matrix.txt}`

Commands the reviewer can re-run (all read-only, lane root as cwd):

```
sha256sum .ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt
grep -cE '^(all-gates v|export-ref=|suite-sha256=|suite-path=|time-basis=|run-utc=|mode=)' \
  .ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt
head -19 .ufo/waves/round-43/w1/ExecK18Transcript.de09313-tee.txt | sha256sum
tail -14 .ufo/waves/round-43/w1/ExecK18Transcript.de09313-tee.txt | sha256sum
grep -rn '^selftest cases=13 failures=3$' .ufo/waves/round-42 .ufo/waves/round-43 | grep -v '/w1/'
GIT_OPTIONAL_LOCKS=0 git show de09313e8edb98280b19767d0094bb2dd8031d73:corpus/instruments/r42-closure.sh | sha256sum
awk 'NR>=2140 && NR<=2151 {print NR": "$0}' corpus/instruments/r42-closure.sh
```

No commit, push, ref, index, production-file or operator-config change was made by this seat; no tool was installed.
