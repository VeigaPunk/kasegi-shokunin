# ExecInstrSelftest — round 28 wave 1

Item: selftest instrumentation run (no production edits) — C1 counter (c), `anchorcheck.py --selftest`.
Verdict: **PRE-STATE**. The impl has not landed; the limb under test does not exist in the live bytes.
Receipt: `.ufo/waves/round-28/receipts/ExecInstrSelftest.txt`.

## 1. Why PRE-STATE (byte facts, all read-only)

| Check | Command (cwd = lane root) | Observed |
|---|---|---|
| live digest | `sha256sum corpus/instruments/anchorcheck.py` | `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748` |
| frozen-base blob | `git cat-file -p c9f8b11…:corpus/instruments/anchorcheck.py \| sha256sum` | same `c2a9e6c6…` |
| tree vs HEAD | `git diff --stat HEAD -- corpus/instruments/anchorcheck.py` | empty (clean), 283 lines |
| limb tokens | `grep -nE 'selftest\|BOUNTIES-ABSENT\|FAIL_CLASSES' corpus/instruments/anchorcheck.py` | zero matches |
| peer scratch | `ls .ufo/waves/round-28/wave1/ExecImplC1/` | absent |

The live digest equals `claims.json` C1.`before.instrument_sha256` and the frozen-base blob, so the
three limbs (a) FAIL_CLASSES, (b) bounties CITE arm, (c) `--selftest` are not present. This seat's
branch condition ("if the impl has not landed … record the FileNotFoundError as PRE-STATE") is met.

## 2. What was run, twice

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/anchorcheck.py --selftest    # run 1
python3 corpus/instruments/anchorcheck.py --selftest    # run 2
```

Both runs: **exit 1**, stdout **0 bytes**, stderr **442 bytes**, identical:

```
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/anchorcheck.py", line 283, in <module>
    sys.exit(main(sys.argv[1:]))
             ~~~~^^^^^^^^^^^^^^
  File "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/anchorcheck.py", line 135, in main
    for line in open(src):
                ~~~~^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '--selftest'
```

`selftest cases=` lines: 0 in both runs.
Determinism: `diff` clean on stdout and stderr; `md5(selftest-pre.err) = md5(selftest-pre-2.err) = 73be6ae7745c1a875a0e1b11fe9d8661`.
Instrument sha256 recorded immediately before and after each run: `c2a9e6c6…f748` (unchanged across both).

This reproduces the frozen `before`/do-nothing value exactly:
`selftest_receipt_lines: 0 (--selftest crashes FileNotFoundError exit 1)`. It **confirms the
before side and does not reach the after side** (`selftest cases=N failures=0`, exit 0, at the landed
digest). C1(c) stays UNVERIFIED at this seat.

Note on determinism's scope (R13): identical PRE-STATE crash output is not evidence that the landed
`--selftest` is deterministic. That limb must be re-measured on the landed bytes.

## 3. Exact re-run the L1 must execute post-change

Full paste-ready command is in §"RE-RUN COMMAND" of the receipt. It: hashes the instrument before run 1
and before run 2 and after run 2, captures FULL stdout+stderr per run, records both exit codes, diffs
the two runs, counts `^selftest cases=[0-9]+ failures=0$`, and tees to
`.ufo/waves/round-28/receipts/ExecInstrSelftest.at-landing.txt`.

Pass requires, on one digest `!= c2a9e6c6…`: `exit1=0 exit2=0`, `determinism=IDENTICAL`,
`selftest_cases_lines=1`, `s1 == s2 == s3`. Then, for the claims counter,
`grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt` must be `1` and the index's
`instrument_sha256=` must equal `sha256sum corpus/instruments/anchorcheck.py`.
`assemble-receipts.py` runs `--selftest` **once** and does not test determinism — the determinism limb
is carried only by the re-run command above.

## 4. Files touched

- `.ufo/waves/round-28/receipts/ExecInstrSelftest.txt` (this seat's receipt)
- `.ufo/waves/round-28/wave1/ExecInstrSelftest/` — `selftest-pre.out` (0 B), `selftest-pre.err` (442 B),
  `selftest-pre-2.out` (0 B), `selftest-pre-2.err` (442 B), `sha-pre.txt`
- this report

No production file written, no VCS write, no background job, no subagent, no tool install.

## 5. Blockers / risks

- **Blocker (expected, by design of the branch):** C1(c) cannot pass until ExecImplC1 lands. The re-run
  above is the only remaining step and it is unrun — therefore unpassed.
- **Risk:** if the landed instrument prints `selftest cases=N failures>0` or a cases line that is not at
  line start, the claims regex `selftest cases=` still matches (unanchored) but the strict re-run regex
  `^selftest cases=[0-9]+ failures=0$` will not — the L1 should treat a mismatch as a fail and quote the
  actual line, not loosen the regex.
- **Risk:** if ExecImplC1 lands *after* `assemble-receipts.py` runs, the canonical index would pin the
  pre-change digest. Assemble last, after the instrument digest is final.
