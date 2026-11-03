C1 mutant probe — verdict: 13 one-limb mutants of `corpus/instruments/figure-audit.py` at lane HEAD 472737847, killed=6 (m1, m3, m5, m10, m11, m12), survived=7 (m2, m2b, m4, m6, m7, m8, m9), inconclusive=0 (pristine baseline green at cases=14 failures=0 exit 0); on the ten named mutants alone killed=4 / survived=6, so the R17 pin (selftest cases=14) does not cover the backtick limbs, the double-quoted `$(`, the python-head confinement, the `head ` allow-list member, the lone-`&` separator limb, or the unterminated-quote refusal.

# Seat MutationC1 — one-limb mutant battery against the figure-audit selftest

Target: Claim C1 (depth:verifiability), instrument `corpus/instruments/figure-audit.py` at lane HEAD.
Frozen claims read first: `.ufo/waves/round-59/claims.json` (never edited, never copied into any result path).

## 1. Pins measured on the lane (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
472737847ff31d1255bf1a0745822a5e878e9622
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
$ python3 --version
Python 3.14.8
$ wc -l .../corpus/instruments/figure-audit.py
286
```
The sha256 equals the candidate sha256 frozen in C1's counting_commands; lane HEAD equals the round's implementation commit. All mutants were cut from this exact byte string.

Scratch: `S=/fast/scratch/hyaku/kasegi-r59/MutationC1` (on `/fast`, 405G free at start). Every path below is absolute.

## 2. Method (exact commands, run in `$S`)

Mutant applier `$S/mutate.py` (sha256 `8b1f23d7bd9b160371d65043cd548cb0cf36f3f70f8e79728e2c5ca88a25348c`): takes a table of (name, label, OLD, NEW), counts OLD in the target bytes, refuses unless `occurrences==1`, then applies one `str.replace(old, new, 1)` and prints the before/after sha256 and Python reprs of OLD and NEW. No mutant table entry touches more than one limb.

Per mutant, exactly:

```
d="$S/mut/<m>"; mkdir -p "$d"; cp "$L/corpus/instruments/figure-audit.py" "$d/figure-audit.py"
python3 "$S/mutate.py" "$d/figure-audit.py" <m>                 # exit 0, prints occurrences=1
python3 -m py_compile "$d/figure-audit.py"                      # exit 0, no output
TMPDIR="$S" python3 "$d/figure-audit.py" --selftest             # exit code + last line
```

Baseline `m0` is the same pipeline with the `mutate.py` step replaced by a pristine `cp` (`occurrences=0`), so a red selftest is attributable to the edit and not to the copy. `TMPDIR=$S` forces the selftest's `tempfile.mkdtemp` trees under scratch; nothing was written under `/tmp`. Each mutant runs from its own copy because `selftest()` re-invokes `os.path.abspath(sys.argv[0])`.

The driver loop actually run:

```
for m in m0 m1 m2 m2b m3 m4 m5 m6 m7 m8 m9 m10 m11 m12; do
  d="$S/mut/$m"; mkdir -p "$d"; cp "$SRC" "$d/figure-audit.py"
  [ "$m" != m0 ] && python3 "$S/mutate.py" "$d/figure-audit.py" "$m" > "$d/apply.log" 2>&1
  python3 -m py_compile "$d/figure-audit.py" > "$d/compile.log" 2>&1; c=$?
  TMPDIR="$S" python3 "$d/figure-audit.py" --selftest > "$d/selftest.log" 2>&1; e=$?
done
```

Kill rule: `--selftest` exit nonzero (the instrument's own R17 detector). Exit 0 = survivor.

## 3. Baseline (pristine bytes)

```
$ TMPDIR="$S" python3 "$S/mut/m0/figure-audit.py" --selftest | tail -1
selftest cases=14 failures=0        # exit 0
```
Green, so every red below is mutant-caused. The baseline copy's sha256 is the pristine `32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0`.

## 4. Results — every mutant, one line each

`compile` column is `py_compile` exit; `exit`/`last` are the selftest exit and its final line. All 14 `compile.log` files together are 0 bytes.

| # | one-limb change (file:line of the limb) | compile | selftest exit | last line | verdict |
|---|---|---|---|---|---|
| m0 | none (pristine copy) | 0 | 0 | `selftest cases=14 failures=0` | control pass |
| m1 | `;` dropped from unquoted reject set — `:121` ``";`()\n\r>"`` → ``"`()\n\r>"`` | 0 | 1 | `selftest cases=14 failures=1` | KILLED |
| m2 | backtick dropped from unquoted reject set — `:121` ``";`()…`` → ``";()…`` | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m2b | backtick dropped from double-quote live-char refusal — `:97` ``elif c == "`" or (c == "$" and …)`` → ``elif c == "$" and …`` | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m3 | `>` dropped from unquoted reject set — `:121` `…\r>"` → `…\r"` | 0 | 1 | `selftest cases=14 failures=1` | KILLED |
| m4 | lone `&` accepted as separator — `:115-116` `return None` → `segs.append(...); cur=[]; i+=1; continue` | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m5 | `\|\|` refusal dropped, double pipe treated as one separator — `:108-109` `return None` → `i += 1` | 0 | 1 | `selftest cases=14 failures=1` | KILLED |
| m6 | `$(` no longer live inside double quotes — `:97` ``elif c == "`" or (c == "$" and …)`` → ``elif c == "`":`` | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m7 | python heads always admissible — `:135` `return len(parts) >= 2 and parts[1].replace(...)...` → `return True` | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m8 | `"head "` removed from `READ_ONLY_HEADS` — `:49` | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m9 | unterminated-quote refusal removed — `:125-126` `if quote is not None: return None` deleted | 0 | 0 | `selftest cases=14 failures=0` | SURVIVED |
| m10 | only the first segment checked — `:144` `all(...)` → `segment_ok(segs[0].strip())` | 0 | 1 | `selftest cases=14 failures=1` | KILLED |
| m11 | `(` and `)` dropped from unquoted reject set — `:121` ``";`()\n\r>"`` → ``";`\n\r>"`` | 0 | 1 | `selftest cases=14 failures=1` | KILLED |
| m12 | `"awk "` removed from `READ_ONLY_HEADS` — `:49` | 0 | 1 | `selftest cases=14 failures=1` | KILLED |

Extras beyond the ten named in the item: m2b (the other backtick limb, split out because `:97` and `:121` are two separate refusals), m11 (the paren limb isolated from m1's semicolon), m12 (allow-list membership contrast to m8). Counts: 13 mutants, killed 6, survived 7; named ten only: killed 4, survived 6.

Exactly-once application was enforced by the driver and each edit is a single hunk. Confirming diffs (pristine → mutant, `diff -u` hunk bodies, one per mutant):

```
m1   -        if c in ";`()\n\r>":      +        if c in "`()\n\r>":
m2   -        if c in ";`()\n\r>":      +        if c in ";()\n\r>":
m2b  -            elif c == "`" or (c == "$" and cmd[i + 1:i + 2] == "("):
     +            elif c == "$" and cmd[i + 1:i + 2] == "(":
m3   -        if c in ";`()\n\r>":      +        if c in ";`()\n\r":
m4   -                return None       +                segs.append("".join(cur))
                                        +                cur = []
                                        +                i += 1
                                        +                continue
m5   -                return None       +                i += 1
m6   -            elif c == "`" or (c == "$" and cmd[i + 1:i + 2] == "("):
     +            elif c == "`":
m7   -        return len(parts) >= 2 and parts[1].replace("\\", "/").startswith("corpus/instruments/")
     +        return True
m8   -    "sha256sum", "cat ", "cut ", "sort ", "awk ", "sed -n ", "head ", "tail ", "python ", "python3 ",
     +    "sha256sum", "cat ", "cut ", "sort ", "awk ", "sed -n ", "tail ", "python ", "python3 ",
m9   -    if quote is not None:          (two lines deleted)
     -        return None
m10  -    return all(segment_ok(seg.strip()) for seg in segs)
     +    return segment_ok(segs[0].strip())
m11  -        if c in ";`()\n\r>":      +        if c in ";`\n\r>":
m12  -    "sha256sum", "cat ", "cut ", "sort ", "awk ", "sed -n ", "head ", "tail ", ...
     +    "sha256sum", "cat ", "cut ", "sort ", "sed -n ", "head ", "tail ", ...
```

Process note (disclosed, not hidden): my first m2 replacement string also swallowed the `;` (it became an m1 duplicate). The `diff -u` caught it, the copy was rebuilt from pristine and m2 re-run with the corrected pair (``";`()…`` → ``";()…``, after_sha256 `723b4e07221d2376a5fe7dd30fffe91e102ec9ce92e16d288eff31a8e409548e`). The first m2 result (exit 1) is discarded and is *not* the reported result; the reported m2 is the corrected one, exit 0. Corrected after_sha256 values for every mutant (full digests of the mutated bytes; each is fully determined by the pristine `32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0` plus the single replacement listed for that mutant):

```
m1  304ad405dc6e59df1a379b17632d11faf828c1d7ab649cb5f330c7c2b91f9464
m2  723b4e07221d2376a5fe7dd30fffe91e102ec9ce92e16d288eff31a8e409548e
m2b 490034fd5c9c7b539079cb602fb49bee8dfe279219b5269e14f2659a6bd8bb1c
m3  8524535e7e185b13024811ec3c7b34a6f25753ef86df2d6119f9a14938e983d4
m4  5257ed09b4cc2b9ef0d56f1c53b0f3eaaa0789cc54704917bcdad903438dedb9
m5  2e5dc1e6d680a3687a2792d1ee75708da309e4cc745735d6397b3f11318a7029
m6  08dc06dde11556394bdf8b5ce8d5d48b01f475a926382424297057689ebf1494
m7  0c415c4f66c4df56bbc3be2423d1517e6855b509b60a118da56bf7e7d1e31eb9
m8  62a30e2e2a6c9aebf404d45ca03be90de3d27770fad201a838676ec2f096de69
m9  63f4e48224cfc915988ff626e014098f929200d41b3979ee87e181fb92762993
m10 251bc1929fc8375aac34d4f01ae58fd9ac19f15ba40481684e7e6caf75d50db4
m11 a178ba9a8ee4336ec2d6e0d88241dda52fe47957f0d27132249e60bacf377622
m12 eba9bd816e453d3d6953e3ea5dc513d50a99ad262ed50f8d6cc1c3d14f0e1e5b
```

## 5. The six kills — which case did the killing

Decisive line from each `$S/mut/<m>/selftest.log`, verbatim:

```
m1   selftest case=chain-semicolon-refused exit=1 want=2 verdict=fail
m3   selftest case=redirect-refused exit=1 want=2 verdict=fail
m5   selftest case=or-chain-refused exit=0 want=2 verdict=fail
m10  selftest case=pipe-to-shell-refused exit=1 want=2 verdict=fail
m11  selftest case=chain-cmdsubst-refused exit=1 want=2 verdict=fail
m12  selftest case=quoted-separator-admitted exit=2 want=0 verdict=fail
```

m1/m3/m11 are not killed by a refusal-vs-admission change but by the downstream exit code: with the metacharacter accepted the derive runs and lands on exit 1 (`cat g.txt; cat g.txt` prints two lines; `cat g.txt > out.txt` prints nothing; `cat g.txt $(cat g.txt)` errors), so the case's `want=2` still fails. The case is therefore sensitive to the limb even though the mechanism is indirect. m5 and m10 are killed on the intended axis (admission flips exit 0). m12 is killed in the strictness direction; see m8 below.

## 6. The seven survivors — equivalence judgment

Judgments are static traces over the quoted source (each cites file:line of the pristine instrument); this seat's command set is the selftest, so **none of the witness derives below was executed** — they are the differential inputs a follow-up case could pin, not measured runs.

- **m2 — NOT behaviour-equivalent.** ``cat g.txt `touch MARK` ``: the unquoted backtick is no longer refused at `:121`, the string stays one segment, `segment_ok` sees head `cat ` and returns True (`:136`), and `run_derive` hands it to `bash -c`, which performs the substitution and creates MARK. This is a limb the frozen C1 sentence explicitly claims ("a backtick"), and it is not one of B1/B2/B3/B4/B6 — so it is an unpinned *claimed* refusal, not a re-report of a recorded residual.
- **m2b — NOT behaviour-equivalent.** ``cat g.txt "`touch MARK`"``: with the `:97` backtick disjunct gone, the double-quote branch appends the backticks literally, the closing `"` ends the quote, one segment with head `cat ` is admitted, and bash substitutes. Same escape class as m2, reached through the double-quote path.
- **m4 — NOT behaviour-equivalent as a grammar; no new write primitive found.** With `:115-116` relaxed, `cat g.txt & cat g.txt` is admitted (pristine refuses at the lone `&`). Every resulting segment must still pass `segment_ok`, so a writer such as `touch MARK` remains refused as a segment; a writer that *is* admissible (`sort -o MARK g.txt`, residual B6) is already reachable in pristine through `&&`, so this limb widens composition (backgrounding) without adding a file-creation primitive beyond the allow-list residuals. This one is the sharpest coverage gap: the `chain-background-refused` case (`:251`) still passes under m4 for the *wrong* reason — its second segment ` true` fails the head allow-list, not the `&` refusal, which is exactly why the mutant scores 14/0.
- **m6 — NOT behaviour-equivalent.** `cat g.txt "$(touch MARK)"`: with the `$( ` disjunct removed at `:97`, the `(` sits inside double quotes where the unquoted reject set cannot see it, the segment is admitted on head `cat `, and bash runs the substitution before `cat` fails. The frozen C1 sentence claims `'(' or ')' (so '$(' too)` and the docstring claims a `$(` inside double quotes is refused — unpinned claimed limb, not in B1–B6.
- **m7 — NOT behaviour-equivalent, and this is a code-execution limb.** `python3 -c "import os; os.system('touch MARK')"`: pristine `segment_ok` rejects it because `parts[1] == "-c"` does not start with `corpus/instruments/` (`:135`); the mutant's blanket `return True` admits it. The selftest contains no case with a `python`/`python3` head at all, so the confinement of counters to committed instruments is entirely unpinned.
- **m8 — NOT behaviour-equivalent in the strictness direction.** Removing `"head "` (`:49`) makes an otherwise-legitimate derive such as `head -1 g.txt` exit 2 (harness refusal) instead of auditing, i.e. a false refusal rather than an escape. The allow-list is partially pinned: m12 proves `awk ` is load-bearing for `quoted-separator-admitted` (`:257`), whereas `head ` has no case, so the tuple is pinned only by the one member a control happens to use.
- **m9 — NOT behaviour-equivalent; enables a B1/B2-family variant.** `cat g.txt \" ; touch MARK`: the scanner treats `\` as an ordinary char and the `"` as an opener (`:102-106`), so on pristine the string ends with an open quote and is refused at `:125-126`. With that refusal deleted the string is one segment admitted on head `cat `, and bash — for which `\"` is a literal quote — executes `touch MARK` as a following command. The escape is the already-named backslash-escaped-quote family (B1/B2) in its *unclosed* variant, so removing this refusal is not a new class, but the refusal is load-bearing for that family and the selftest does not pin it.

Summary of the survivor set: two limbs (m2, m2b) and one (m6) are refusals the frozen claim names explicitly, one (m7) is arbitrary-code admission, one (m9) is the B1/B2 family's last line, one (m4) is a grammar widening, one (m8) is over-strictness. The R17 count is 14/0 in all seven cases: `EXPECTED_CASES` pins the *number* of cases, not the limbs they touch.

## 7. Coverage accounting against the eight chain cases

The chain cases at `:250-257` exercise: `;`, lone `&`, newline, `$(`, `| sh`, `>`, `||`, and the quoted-separator control. Measured sensitivities: `;` (m1 kill), `>` (m3 kill), `||` (m5 kill), pipe+head allow-list (m10 kill), `$(` unquoted (m11 kill), `awk ` membership (m12 kill). Measured insensitivities: backtick unquoted (m2), backtick in double quotes (m2b), lone `&` (m4 — masked by the head check), `$(` in double quotes (m6), python-head confinement (m7), `head ` membership (m8), unterminated-quote refusal (m9). So six of the thirteen limbs are pinned and seven are not, with the background case passing for an unintended reason.

No contract change is proposed here: a survivor is a pin gap, and the gate's own behaviour on the lane bytes is unchanged. Adding cases for the seven gaps would change `EXPECTED_CASES` (14) and the C1 selftest pin, i.e. it is an instrument/claim decision for the lead, not this seat's.

## 8. Restoration and cleanliness

The lane instrument was never opened for writing. After the battery:

```
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  .../figure-audit.py
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
472737847ff31d1255bf1a0745822a5e878e9622
```

Both equal the values in §1, so the pristine detector ran on the same bytes before and after (before: the m0 copy, after: the lane re-hash). No `git add/commit/checkout/reset/stash/switch` and no `jj` command was run against L or any clone; this seat built no git fixture at all, so no repository identity was created or used.

Only two scratch artifacts existed: `$S/mut/` (13 mutant copies plus baseline, each with `apply.log`, `compile.log`, `selftest.log`) and `$S/mutate.py`. `$S` was removed with `rm -rf -- "$S"` before yielding; verification of the removal is reported in the yield message. No file under `/tmp`, the fleet root, a sibling lane, or `/home/vgpnk/Projects/shokuknow` was created or modified. Leftovers: none.

## 9. Tooling

No tool was installed or upgraded (no uv tool, npx, official binary, or pacman invocation). `python3 3.14.8` was already on the host; `bash`, `cp`, `diff`, `sha256sum`, `wc`, `grep`, `sed`, `tail` came from the base system. All pacman transactions remain paused and none was attempted.
