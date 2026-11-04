# SentinelGate — R68 W1 security review of C1 (`82b3b7d` corpus/instruments/figure-audit.py vs base `d0f48405`)

**Verdict: FINDINGS.** The change is strictly narrowing: no widening, no new write/exec path, no credentials/network/lane-state write, and no regression on the real ledger. But the new denial is **incomplete**. GNU `sort` accepts unique-prefix abbreviations of `--compress-program` (`--co=`, `--comp=`, `--compress=`, `--compress-prog=`, `--co PROG`). The candidate admits those spellings and runs PROG: 9144 runs per derive, and the audit verdict is green `exit=0` (F1, HIGH, a residual of the claimed class). The frozen counter only probes the exact spelling, so it cannot see this. Three other classes are pre-existing (they behave the same at base) and are listed separately (F2, F3).

Gates under test (sha256 measured in this seat):
- base `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247` (= `git show d0f48405:corpus/instruments/figure-audit.py` = controls/base-gate-d0f48405.py)
- candidate `10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8` (= `git show 82b3b7d:…` = working tree)
- Host binaries that Popen resolves: `/usr/bin/sort` (GNU coreutils 9.12), git 2.56.0, Python 3.14.8.

## (1) Admission parity matrix — does the change widen what executes?

Driver: `w1/SentinelGate/parity-matrix.py` (receipt `parity-matrix.txt`, per-row JSON `matrix.json`). It builds one git fixture under `$SCR/fx.XXXX` and asserts that `rev-parse --show-toplevel` equals the fixture before committing. It plants marker programs: sort compressor `cp.sh`, `diff.tc.textconv`, `diff.external`, `filter.f.smudge`, with `*.bin diff=tc filter=f`. Then it runs every derive through each gate's own CLI (`python3 -B GATE --ledger L --root FX`). For each run it records admission, exit, marker deltas (real exec) and new fixture files (real writes).

```
$ cd $SCR && TMPDIR=$SCR python3 -B parity-matrix.py --base $SCR/base-gate.py --cand $SCR/cand-gate.py --scratch $SCR
MATRIX derives=85 diffs=18 widened=0 narrowed=18 cand_admitted_with_exec_or_write=13
```

The 85 derives cover: every allow-listed head with 0, 1 or 2 operands; `--`; `<`; pipelines; `&&`; sort `-o/--output/--compress-program` in `=`, space, single-quoted, double-quoted, escaped (`-\o`, `--compress-progra\m=`, `\-\-compress-program=`), after-operand and after-`--` spellings; `git show --output/--ext-diff/--textconv` (plus the same abbreviated); `git cat-file`; `git ls-tree`; python heads inside and outside `corpus/instruments/`; wrapper heads `sh/sed/awk/env/xargs/tee/cp/mv`; `git -c`; `/usr/bin/sort`.

**All 18 diffs are base ADMITTED → candidate REFUSED (0 widenings):**
```
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort --compress-program=$SCR/cp.sh -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort --compress-program $SCR/cp.sh -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort '--compress-program=$SCR/cp.sh' -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort "--compress-program=$SCR/cp.sh" -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort '--compress-program' $SCR/cp.sh -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort --compress-progra\m=$SCR/cp.sh -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort \-\-compress-program=$SCR/cp.sh -S 1K big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort -S 1K big.txt --compress-program=$SCR/cp.sh | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | cat big.txt | sort -S 1K --compress-program=$SCR/cp.sh | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | sort -S 1K --compress-program=$SCR/cp.sh < big.txt | head -n 1
DIFF base=ADM/1 exec={'cp': 9144} cand=REF/2 | cat g.txt && sort --compress-program=$SCR/cp.sh -S 1K big.txt | head -n 1
DIFF base=ADM/1 cand=REF/2 | sort -- --compress-program=$SCR/cp.sh
DIFF base=ADM/1 exec={'tc': 1, 'sm': 1} cand=REF/2 | git show --textconv HEAD:a.bin
DIFF base=ADM/1 exec={'tc': 1, 'sm': 1} cand=REF/2 | git show '--textconv' HEAD:a.bin
DIFF base=ADM/1 exec={'tc': 1, 'sm': 1} cand=REF/2 | git show "--textconv" HEAD:a.bin
DIFF base=ADM/1 exec={'tc': 1, 'sm': 1} cand=REF/2 | git show --text\conv HEAD:a.bin
DIFF base=ADM/1 exec={'tc': 1, 'sm': 1} cand=REF/2 | git show HEAD:a.bin --textconv
DIFF base=ADM/1 cand=REF/2 | git show -- --textconv
```
16 of the diffs close real execution. 2 are over-refusals (`sort -- --compress-program=…`, `git show -- --textconv`): after `--` the token is a file operand, which base ran as `derive-exit-2` / `derive-empty`. They are safe and narrowing only (F4). The other 67 rows are identical across gates. All read-only controls and every python-inside head stay admitted at both, so there is no false refusal of legitimate derives (`git show --output-indicator-new=+ HEAD` is still admitted).

## (2) Any new write or exec path reachable?

No. The full file diff (`git diff d0f48405 82b3b7d -- corpus/instruments/figure-audit.py`, +18/−4) only does four things: it adds two strings to the `DENIED_FLAGS` tuples, updates the docstring and comment, bumps `EXPECTED_CASES` from 73 to 77, and adds four `run_case(...)` selftest calls that use the existing `_one` fixture path. `denied_flag`, `tokenize`, `parse_derive`, `run_derive`, `segment_ok` and the imports are unchanged. In the matrix, `widened=0`. Every candidate exec or write in an admitted row also happens at base (F1–F3).

## (3) Is the denial complete for the two flags in tokenizer spellings?

Yes, for every spelling the tokenizer can produce. These are refused at the candidate, and their markers record no runs: `=`, space-separated value, single-quoted, double-quoted, escaped inside the flag, escaped dashes, after an operand, in a pipeline stage after `cat`, with `<` input, in the second `&&` group, and after `--` (over-refused).

**No, at the getopt level (F1).** Abbreviated long options are a separate case. `denied_flag` matches only `tok == flag` or `tok.startswith(flag + "=")`, and GNU getopt_long expands unique prefixes:
```
same base=ADM/1 exec={'cp': 9144} cand=ADM/1 exec={'cp': 9144} | sort --compress-prog=$SCR/cp.sh -S 1K big.txt | head -n 1
same base=ADM/1 exec={'cp': 9144} cand=ADM/1 exec={'cp': 9144} | sort --compress=$SCR/cp.sh -S 1K big.txt | head -n 1
same base=ADM/1 exec={'cp': 9144} cand=ADM/1 exec={'cp': 9144} | sort --co=$SCR/cp.sh -S 1K big.txt | head -n 1
same base=ADM/1 exec={'cp': 9144} cand=ADM/1 exec={'cp': 9144} | sort --co $SCR/cp.sh -S 1K big.txt | head -n 1
same base=ADM/1 exec={'cp': 9144} cand=ADM/1 exec={'cp': 9144} | sort -S 1K big.txt --comp=$SCR/cp.sh | head -n 1
$ /usr/bin/sort --c=x g.txt
/usr/bin/sort: option '--c=x' is ambiguous; possibilities: '--check' '--compress-program'
```
Green verdict with execution (`green-exec-demo.txt`):
```
$ TMPDIR=$SCR python3 -B cand-gate.py --ledger demo2.json --root $FX   # derive: sort --co=$SCR/cp.sh -S1K big.txt | wc -l
FIG abbrev-co-wc recorded=30000 derived=30000 ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
marker cp.log lines=9144
```
(Base gives the same output, with the same 9144 runs.) In the `| head -n 1` shapes the audit verdict is stale (`derive-upstream-signal-13`), but PROG has already run by then: 18288 marker lines across two such derives, at both gates.

`git show` abbreviations are not a bypass on this git. Git's diff-option parser rejects them and nothing runs:
```
git show --textcon -> exit=128 fatal: unrecognized argument: --textcon
git show --outp=x -> exit=128 fatal: unrecognized argument: --outp=x
git show --ext-dif -> exit=128 fatal: unrecognized argument: --ext-dif
```
(matrix: `--textcon`, `--textc`, `--outp=`, `--ext-dif` → `derive-exit-128`, no markers.)

## (4) Credential material, network call, lane-state write introduced?

None. The only line added by the diff that matches `socket|urllib|http|requests|token|secret|passw|key|environ|open(|write|unlink|remove|subprocess|import` is the comment `+# read-only derives, so they are refused at parse time like the round-60 write flags.` The new selftest cases write only under `$HYAKU_SCRATCH` temp dirs, which is the existing `run_case` path.

## (5) Real-ledger regression

```
$ TMPDIR=$SCR python3 -B corpus/instruments/figure-audit.py                       # candidate
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
$ TMPDIR=$SCR python3 -B .ufo/waves/round-68/controls/base-gate-d0f48405.py --ledger corpus/instruments/figure-audit-ledger.json --root .
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
$ HYAKU_SCRATCH=$SCR python3 -B corpus/instruments/figure-audit.py --selftest
selftest case=sort-compress-program-refused exit=2 want=2 verdict=pass
selftest case=sort-compress-program-space-refused exit=2 want=2 verdict=pass
selftest case=sort-compress-program-quoted-refused exit=2 want=2 verdict=pass
selftest case=git-show-textconv-refused exit=2 want=2 verdict=pass
selftest cases=77 failures=0          (exit=0)
```
No regression. Receipt: `real-ledger-and-selftest.txt`.

## Findings

**F1 — HIGH — residual of the C1 class (incomplete denial; not introduced, not a regression).**
- **Exploit path:** a ledger entry `sort --co=PROG -S1K big.txt | wc -l` passes `parse_derive`, and `run_derive` execs PROG once per temp-file compression. The audit then reports `ok`/`exit=0`.
- **Evidence:** the 5 matrix rows above and `green-exec-demo.txt`.
- **Impact:** the round's stated repair ("program-execution classes … refused at parse time") is bypassable with getopt spellings, through the same head and flag.
- **Predicate coverage:** the frozen counter `c1-probe-run-r68.py` probes only `--compress-program=<prog>` (line 166), so `VERIFY failures=0` cannot detect this. That is a coverage limit of the frozen predicate, reported for L1 adjudication. The predicate itself was not changed.
- **Smallest remediation:** in `denied_flag`, refuse a `--`-led token whose stem `tok.split("=",1)[0]` is a prefix of a denied long flag and has at least 3 characters. For sort, `--co…`/`--compress-program` and `--o…`/`--output` are then refused. `--c` is already ambiguous to sort (shown above). Add selftest cases for `--co=` and `--co PROG`.

**F2 — MEDIUM — PRE-EXISTING (identical at base): config-driven program execution through allow-listed git heads.**
Denying `--textconv` does not close textconv/filter execution. Measured at both gates:
- `git show HEAD`: tc 2 runs, sm 2 runs. Textconv is on by default for `git show` patches.
- `git show --output-indicator-new=+ HEAD`: tc 2, sm 2.
- `git cat-file --textconv HEAD:a.bin`: tc 1, sm 1.
- `git cat-file --filters HEAD:a.bin`: sm 1.
- Green: `preexisting-show-default-textconv`, `preexisting-catfile-textconv` and `preexisting-catfile-filters` are all `ok` at both gates (`green-exec-demo.txt`).

The docstring already discloses "Git configuration … can still … execute other programs". The class is documented but not closed. Smallest remediation: add `git cat-file` `--textconv`/`--filters` to `DENIED_FLAGS`. Default patch textconv needs a design decision; L1 should rule.

**F3 — MEDIUM — PRE-EXISTING (round-60 write class, identical at base): sort `-o/--output` denial bypassed by bundling and abbreviation.**
`sort -uo out.txt g.txt`, `sort -uoout.txt g.txt`, `sort --outp=out.txt g.txt` and `sort --o=out.txt g.txt` are admitted at both gates, and each wrote `out.txt` in the fixture (`writes=['out.txt']`). Remediation: the same prefix rule as F1, plus refusing any short-option cluster `-[^-]*o` for sort.

**F4 — INFO — candidate narrowing:** `sort -- --compress-program=X` and `git show -- --textconv` are refused even though the token is an operand there. This is safe over-refusal, and it accounts for 2 of the 18 diffs.

## Notes / residuals
- Unexercised (not claimed either way): `sort -T DIR` temp-file placement, `sort --files0-from`, `tail -f` timeouts, `core.fsmonitor`/hooks on git heads.
- Lane observation, not attributable to this seat: during the wave, `git status` showed new modifications to `.ufo/waves/round-67/controls/driver-pins.json` and `corpus/knowledge/first-psirt-maturity-document.md` (mtime 18:52:51) and a new `controls/seat-c2-counters-r68.txt` (18:53:49). My only lane-rooted command was the real-ledger/selftest run at about 18:55. Every matrix run used `--root $SCR/fx.*`. Another seat or the integrator made these changes.
- Tools installed: none. Scratch `/fast/scratch/hyaku/kasegi-r68/SentinelGate/` was removed before yield. Receipts use `$SCR` for that path.
- Receipts: `w1/SentinelGate/{parity-matrix.py,parity-matrix.txt,matrix.json,green-exec-demo.txt,real-ledger-and-selftest.txt}`.
