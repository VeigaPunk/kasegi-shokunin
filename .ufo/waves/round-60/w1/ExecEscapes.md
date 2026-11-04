VERDICT: 43 derives measured against the round-60 gate (scratch copy, sha256 35f7bcd3… = the C1 counting-command want) — 14 **admitted-and-executing** (marker created in the gate's own root), 10 admitted-safe (no marker), 19 refused (exit 2 `reason=derive-not-read-only`); 15 of the 19 refusals are the only thing between the derive and execution. Two of the 14 admitted-and-executing derives leave the audit **green** (exit 0, `FIG … ok`) while running arbitrary commands. Three classes remain open beyond Q1-Q7 and beyond the recorded python-traversal residual: (A) `#` comment state is unmodelled, so a quote inside a comment becomes a phantom quote that spans a real newline; (B) the denied-flag screen matches raw whitespace tokens before quote removal, so quoting, ANSI-C spelling, combined short options and long-option abbreviations walk `-o`/`--output`/`--ext-diff` past it; (C) `sort --compress-program=PROG` is exec-capable, absent from `DENIED_FLAGS`, admitted, and executes on spill. Claim C1's kill rule (Q1-Q7 only) is **not** triggered by any of this; no claim value is contradicted.

# ExecEscapes — round 60 / w1 — residual escape, quote and comment classes

Seat: ExecEscapes (Kasegi lane). Item: bounded probe of escape/quote/comment classes the round-60 gate does not claim.
Claims read first: `L/.ufo/waves/round-60/claims.json` (frozen `66e6241`) and `.ufo/waves/round-60/claims-erratum-1.md` (C2 command 8 want 1→2). Nothing under `L` was modified except this file.
`L` = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; `S` = `/fast/scratch/hyaku/kasegi-r60/ExecEscapes`.

## 1. Instrument identity (the exact bytes tested)

```
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  …/corpus/instruments/figure-audit.py
$ sha256sum $S/instrument/figure-audit.py          # scratch copy actually exercised
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/ExecEscapes/instrument/figure-audit.py
```
exit 0. The lane digest equals the C1 counting-command want (`claims.json`, C1 `counting_commands[6]`), so the copy tested is the landed gate. Host: `Python 3.14.8`, `GNU bash, version 5.3.20(1)-release` (`/usr/bin/bash`), `git version 2.56.0`, `sort (GNU coreutils) 9.12` (`/usr/bin/sort`).
Note: the harness shell has a builtin `sort` (0.8.0); every measurement below was taken through Python `subprocess` → `/usr/bin/bash`, i.e. the same resolution the gate itself uses at `L/corpus/instruments/figure-audit.py:75` (`subprocess.run([bash, "-c", cmd], cwd=root…)`). `bash -c 'type -a sort'` → `sort is /usr/bin/sort`.

## 2. Harness — what "run it through the gate" means here

For every derive: a fresh root containing `g.txt` (`35`), a one-figure ledger, the gate run **inside** that root, and then the **same byte string** run by `/usr/bin/bash -c` in a second identical fresh root.

```
printf '35\n' > "$ROOT/g.txt"
python3 -c 'import json,sys; json.dump({"figures":[{"id":PID,"record":"g.txt:1","recorded":"35","derive":DERIVE,"want":"35"}]}, open(LEDGER,"w"))'
( cd "$ROOT" && python3 "$S/instrument/figure-audit.py" --ledger "$LEDGER" --root "$ROOT" )   # gate
( cd "$ROOT2" && /usr/bin/bash -c "$DERIVE" )                                                  # bash truth
find "$ROOT" -name 'MARK*'                                                                    # marker count
```
Verdict convention (as fixed by the seat item): **admitted** = gate exit 0 or 1 with a `FIG ` line; **refused** = exit 2 with `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only`. Ledger/root work is under `$S`; `TMPDIR=$S` was passed on every driver invocation; no `/tmp` use. The drivers built `$ROOT` as `$S/roots/gate-<id>` (second root `$S/roots/bash-<id>`) and `$LEDGER` as `$S/ledgers/<id>.json` — every path absolute, under `$S`.

For the two `git` heads the root additionally holds `repo/`: `git init -q`, user config, one **non-empty** commit (`f1.txt`), and `git config diff.external <repo>/ext.sh` where `ext.sh` is `#!/bin/sh` + `touch MARK-EXTDIFF`. `git show` on an empty commit produces no diff, so the external program is never invoked; the fixture is what makes the `--ext-diff` execution observable. Each fixture asserts `git -C <repo> rev-parse --show-toplevel` equals the fixture path before committing. For `P37` the root also holds `payload.txt` = 200 000 lines of `touch MARK-Z` (2 600 000 bytes) so GNU sort spills and invokes the compress program.

Batches (what actually ran; all drivers in `$S`, `2>&1 | tee`):

| # | command (cwd `$S`) | exit |
|---|---|---|
| 3.1 | `TMPDIR=$S python3 drive.py "$S/instrument/figure-audit.py" "$S" 2>&1 \| tee run1.txt` | 0 (`PIPE_RC=0`) |
| 3.2 | `TMPDIR=$S python3 drive2.py "$S/instrument/figure-audit.py" "$S" 2>&1 \| tee run2.txt` | 0 |
| 3.3 | `TMPDIR=$S python3 drive3.py "$S/instrument/figure-audit.py" "$S" 2>&1 \| tee run3.txt` | 0 |
| 3.4 | `python3 summarize.py run1.txt run2.txt run3.txt` | 0 |

`3.4` printed (decisive lines, verbatim):

```
probes=43
admitted_and_executing=14 P15-comment-phantom-squote,P16-comment-phantom-dquote,P30-phantom-squote-chain,P21-sort-quoted-short,P22-sort-quoted-long,P23-sort-combined-short,P24-sort-ansi-flag,P27-git-ext-diff-quoted,P29-git-output-quoted,P35-sort-abbrev-o,P36-sort-abbrev-out,P37-compress-spill,P42-sort-abbrev-space,P43-git-output-quoted-sep
admitted_safe=10 P03-line-continuation,P04-dquote-semicolon-real,P04b-dquote-escaped-close,P07-ansic-hex-semicolon,P19-continuation-hash,P26-sort-compress-program,P33-phantom-same-line,P34-phantom-line2-semicolon,P38-git-abbrev-out,P40-real-quote-newline
refused_bash_would_execute=15 P01-ansic-escape,P05-escaped-dquotes-subst,P06-empty-quote,P08-pipe-empty,P10-pipe-and,P11-herestring,P12-clobber,P13-tab-semicolon,P17-comment-phantom-unbalanced,P18-comment-phantom-third-line,P20-continuation-andand,P25-sort-bare-control,P28-git-ext-diff-bare,P32-newline-in-dquote-continuation,P41-sort-long-control
refused_bash_no_execute=4 P02-comment-semicolon,P09-trailing-andand,P14-semicolon-hash,P31-lone-backslash
refused_total=19
```
14 + 10 + 19 = 43; the four lists are disjoint.

## 4. The full result table (43 derives)

`⏎` = one real LF byte inside the derive string; `⇥` = one TAB. "marker" is the marker file left in the **gate's** root (bash's root agrees in every row).

| # | derive (exact) | gate | bash | marker |
|---|---|---|---|---|
| **admitted-and-executing** | | | | |
| P15 | `cat g.txt #'⏎touch MARK-M #'` | **admitted, exit 0, `FIG … derived=35 ok`** | rc 0, `35` | MARK-M |
| P16 | `cat g.txt #"⏎touch MARK-N #"` | **admitted, exit 0, `FIG … derived=35 ok`** | rc 0, `35` | MARK-N |
| P30 | `cat g.txt #'⏎touch MARK-T && echo hi #'` | admitted, exit 1, stale (`derived=35` + `hi`) | rc 0 | MARK-T |
| P21 | `sort "-o"MARK1 g.txt` | admitted, exit 1, `derive-empty` | rc 0, no stdout | MARK1 |
| P22 | `sort '--output=MARK2' g.txt` | admitted, exit 1, `derive-empty` | rc 0 | MARK2 |
| P23 | `sort -noMARK3 g.txt` | admitted, exit 1, `derive-empty` | rc 0 | MARK3 |
| P24 | `sort -$'\x6f'MARK4 g.txt` | admitted, exit 1, `derive-empty` | rc 0 | MARK4 |
| P27 | `git show "--ext-diff" HEAD` | admitted, exit 1 (derived = commit line) | rc 0, ran `diff.external` | repo/MARK-EXTDIFF |
| P29 | `git show '--output=MARK8' HEAD` | admitted, exit 1, `derive-empty` | rc 0 | repo/MARK8 |
| P35 | `sort --o=MARK9 g.txt` | admitted, exit 1, `derive-empty` | rc 0 | MARK9 |
| P36 | `sort --out=MARK10 g.txt` | admitted, exit 1, `derive-empty` | rc 0 | MARK10 |
| P37 | `sort -S 1K --compress-program=/bin/sh payload.txt` | admitted, exit 1, `derive-exit-2` | rc 2, `/bin/sh` executed the data file | MARK-Z |
| P42 | `sort --o MARK13 g.txt` | admitted, exit 1, `derive-empty` | rc 0 | MARK13 |
| P43 | `git show "--output" MARK14 HEAD` | admitted, exit 1, `derive-empty` | rc 0 | repo/MARK14 |
| **admitted-safe (no marker)** | | | | |
| P03 | `cat g.txt \⏎touch MARK-C` | admitted, exit 1, `derive-exit-1` | rc 1: lines joined to `cat g.txt touch MARK-C` | — |
| P04 | `cat g.txt "x; touch MARK-D"` | admitted, exit 1, `derive-exit-1` | rc 1, `;` literal in the argument | — |
| P04b | `cat g.txt "x\"; touch MARK-D2"` | admitted, exit 1, `derive-exit-1` | rc 1, `\"` literal | — |
| P07 | `cat g.txt $'\x3b' touch MARK-G` | admitted, exit 1, `derive-exit-1` | rc 1, `;` a word, not a separator | — |
| P19 | `cat g.txt \⏎# touch MARK-R` | admitted, exit 0, `FIG … ok` | rc 0, whole rest is a comment | — |
| P26 | `cat g.txt \| sort --compress-program=/bin/true` | admitted, exit 0, `FIG … ok` | rc 0, flag present but never invoked | — |
| P33 | `cat g.txt #'; touch MARK-V; echo '` | admitted, exit 0, `FIG … ok` | rc 0, comment swallowed the `;` | — |
| P34 | `cat g.txt #'⏎; touch MARK-W #'` | admitted, exit 1, `derive-exit-2` | rc 2, parse error at line 2 | — |
| P38 | `git show --outp=MARK11 HEAD` | admitted, exit 1, `derive-exit-128` | rc 128, `unrecognized argument` | — |
| P40 | `cat g.txt '#⏎touch MARK-40'` | admitted, exit 1, `derive-exit-1` | rc 1, quote really spans the newline | — |
| **refused (exit 2 `reason=derive-not-read-only`)** — bash would have executed | | | | |
| P01 | `cat g.txt $'a\\'; touch MARK-A; \\'b'` | refused | rc 127, `touch` ran | MARK-A |
| P05 | `cat g.txt \"$(touch MARK-E)\"` | refused | rc 1, substitution ran | MARK-E |
| P06 | `cat g.txt ''; touch MARK-F` | refused | rc 0 | MARK-F |
| P08 | `cat g.txt \| "" ; touch MARK-H` | refused | rc 0 | MARK-H |
| P10 | `cat g.txt \|& touch MARK-I` | refused | rc 0 | MARK-I |
| P11 | `cat g.txt <<< "x"; touch MARK-J` | refused | rc 0 | MARK-J |
| P12 | `cat g.txt >\|MARK-K` | refused | rc 0, created MARK-K | MARK-K |
| P13 | `cat g.txt⇥; touch MARK-L` | refused | rc 0 | MARK-L |
| P17 | `cat g.txt #'⏎touch MARK-O` | refused (unterminated phantom quote) | rc 0 | MARK-O |
| P18 | `cat g.txt #'⏎touch P #'⏎touch MARK-Q` | refused (third line re-exposes the LF) | rc 0 | MARK-Q |
| P20 | `cat g.txt \⏎&& touch MARK-S` | refused (`&&` still visible) | rc 0 | MARK-S |
| P25 | `sort -oMARK5 g.txt` | refused (the spelling the screen catches) | rc 0 | MARK5 |
| P28 | `git show --ext-diff HEAD` | refused (the Q7 spelling) | rc 0 | repo/MARK-EXTDIFF |
| P32 | `cat g.txt "a\⏎"; touch MARK-U` | refused | rc 0 | MARK-U |
| P41 | `sort --output=MARK12 g.txt` | refused (full long token) | rc 0 | MARK12 |
| **refused, bash would not have executed** | | | | |
| P02 | `cat g.txt #; touch MARK-B` | refused | rc 0, `;` commented out | — |
| P09 | `cat g.txt &&` | refused | rc 2, syntax error | — |
| P14 | `cat g.txt ;# comment` | refused | rc 0, nothing after `;` | — |
| P31 | `cat g.txt \` | refused (trailing lone backslash) | rc 1 | — |

Decisive raw lines for the load-bearing rows (`run1.txt`/`run2.txt`/`run3.txt`):

```
probe=P15-comment-phantom-squote kind=plain note=OPEN: ' in a # comment opens a scanner single-quote that spans the real newline
derive_repr="cat g.txt #'\ntouch MARK-M #'"
gate_rc=0 gate_1st=FIG P15-comment-phantom-squote recorded=35 derived=35 ok gate_last=FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0 gate_markers=['MARK-M']
bash_rc=0 bash_out='35' bash_markers=['MARK-M']

probe=P21-sort-quoted-short kind=plain note=OPEN: -o spliced by quotes escapes DENIED_FLAGS[tok.startswith]
derive_repr='sort "-o"MARK1 g.txt'
gate_rc=1 gate_1st=FIG P21-sort-quoted-short recorded=35 derived=UNAVAILABLE reason=derive-empty stale gate_last=FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1 gate_markers=['MARK1']

probe=P27-git-ext-diff-quoted kind=repo note=OPEN: quoted --ext-diff admitted; runs diff.external
derive_repr='git show "--ext-diff" HEAD'
gate_rc=1 gate_1st=FIG P27-git-ext-diff-quoted recorded=35 derived=commit ed2cb32c… gate_markers=['repo/MARK-EXTDIFF']

probe=P35-sort-abbrev-o kind=plain note=OPEN?: long-option abbreviation of --output
derive_repr='sort --o=MARK9 g.txt'
gate_rc=1 gate_1st=FIG P35-sort-abbrev-o recorded=35 derived=UNAVAILABLE reason=derive-empty stale gate_markers=['MARK9']

probe=P37-compress-spill kind=payload note=OPEN?: unscreened exec flag actually executes on spill
derive_repr='sort -S 1K --compress-program=/bin/sh payload.txt'
gate_rc=1 gate_1st=FIG P37-compress-spill recorded=35 derived=UNAVAILABLE reason=derive-exit-2 stale gate_markers=['MARK-Z']
```
(`P27`'s commit id is per-fixture; the fixture is re-created per run, so only the shape — `derived=commit …` — is stable.)

## 5. Class A — `#` comment state is unmodelled: a comment quote becomes a phantom quote over a real newline

The scanner at `L/corpus/instruments/figure-audit.py:88-153` has quote states `'` and `"` and nothing else; `#` is an ordinary character (`#` does not appear in the refusal set at `:146`). bash ends a comment at the newline but the scanner does not know a comment began, so:

* `#'` after a word-start `#` **opens** a single-quote in the scanner (`:127-131`);
* the LF is inside that quote, and both quote branches append every character including a newline (`:101-106` single quote, `:107-119` double quote) — only the *unquoted* path refuses it (`:146`);
* the balancing `'` in a **second** comment on the next line closes it (`:101-105`), so `check_read_only` sees one segment headed `cat ` (`:180-186`) and admits.

bash, meanwhile, executes line 1 (`cat g.txt`, then `#'` is a comment) and line 2 up to its own `#` comment. Measured: `P15` and `P16` are admitted with **exit 0 and `FIG … ok`** while `MARK-M`/`MARK-N` appear in the audit root — the audit goes green *because* the escape was appended after a derive whose stdout still reads `35`.

Boundaries measured (why the class is exactly this):
* `P33` same-line phantom (`#…'…'`) — admitted, **no** execution: bash comments the whole tail.
* `P17` phantom never closed — refused (unterminated quote, `:150-151`).
* `P18` third line — refused: closing the quote on line 2 puts the line-3 LF back in the unquoted path.
* `P34` phantom spanning the newline with `;` starting line 2 — admitted by the scanner but bash raises a parse error (`rc 2`), so no execution: the phantom needs line 2 to be syntactically valid for bash.
* `P40` a *real* quote spanning a newline — admitted and inert (bash agrees the text is quoted): the defect is the comment, not the newline.
* `P30` amplification: arbitrary `&&`/`;` chaining is available on the closing line while the phantom stays open (exit 1, marker created).

## 6. Class B — the denied-flag screen is raw-token textual, before quote removal

`denied_flag` (`:156-168`) splits the segment head on whitespace and prefix-matches the raw token against `("-o" | "--output" | "--ext-diff")` (`:57-60`). bash removes quotes, splits combined short options and expands ANSI-C before it builds argv; GNU `getopt_long` also accepts unambiguous long-option prefixes. All four divergences were measured to produce a file write under an **admitted** derive:

| sub-form | derive | gate | vs. the spelling the screen does catch |
|---|---|---|---|
| quoting splice | `sort "-o"MARK1 g.txt` | admitted | `sort -oMARK5 g.txt` → refused (P25) |
| quoting splice | `sort '--output=MARK2' g.txt` | admitted | `sort --output=MARK12 g.txt` → refused (P41) |
| separate token | `git show "--output" MARK14 HEAD` | admitted | — |
| ANSI-C | `sort -$'\x6f'MARK4 g.txt` | admitted | — |
| combined short | `sort -noMARK3 g.txt` | admitted | — |
| abbreviation | `sort --o=MARK9 g.txt`, `sort --out=MARK10 g.txt`, `sort --o MARK13 g.txt` | admitted | — |
| git exec flag | `git show "--ext-diff" HEAD` | admitted → ran `diff.external` | `git show --ext-diff HEAD` → refused (P28, the Q7 spelling) |
| git write flag | `git show '--output=MARK8' HEAD` | admitted | — |

git does **not** accept abbreviated long options (`P38`: `git show --outp=MARK11 HEAD` → `fatal: unrecognized argument`, rc 128), so the abbreviation sub-form is `sort`-only; quoting and ANSI-C apply to both heads. `P27`/`P28` are the exact pair that matters for C1's frozen Q7 sentence: the *unquoted* `--ext-diff` is refused as claimed, the quoted one is admitted and executes the repo-configured external diff. This is a residual **class**, not a contradiction of the Q7 probe.

## 7. Class C — an exec-capable flag that is not in `DENIED_FLAGS` at all

The comment above the tuple states its own criterion: "Heads whose flags can write a file or **execute a configured command**" (`:56`). `sort --compress-program=PROG` meets that criterion (GNU coreutils: `--compress-program=PROG compress temporary files with PROG; decompress with PROG -d`) and is not listed. Measured twice:

* `P26` `cat g.txt | sort --compress-program=/bin/true` — admitted, exit 0, `FIG … ok`, flag never invoked on a 1-line input.
* `P37` `sort -S 1K --compress-program=/bin/sh payload.txt` (root also holds `payload.txt` = 200 000 lines of `touch MARK-Z`, measured 2 600 000 bytes) — admitted, sort spills, `/bin/sh` is handed the temporary file and **executes the sorted data as a script**. Driver transcript: `gate_rc=1 … gate_markers=['MARK-Z']`, `bash_rc=2 … bash_markers=['MARK-Z']`. The standalone reproduction (same text plus `> out.txt` to keep the 200 000-line stdout off the transcript):

```
$ R=/fast/scratch/hyaku/kasegi-r60/ExecEscapes/manual/cp
$ cd "$R" && TMPDIR="$R" /usr/bin/bash -c 'sort -S 1K --compress-program=/bin/sh payload.txt > out.txt'
/bin/sh: -d: invalid option  …  sort: '/bin/sh' [-d] terminated abnormally      (repeated per spill)
$ echo "bash_rc=$?"
bash_rc=2
$ ls "$R" | grep -c '^MARK'
1
$ ls "$R"
MARK-Z  g.txt  out.txt  payload.txt
```
The execution is limited to data the derive itself can point at, but the derive controls its own arguments and the root it runs in, so the precondition is satisfiable by the ledger entry alone.

## 8. Class D — backslash-newline outside quotes is kept as an opaque pair (model gap, measured non-executing)

`split_segments` handles `\` before it looks at the metacharacter set (`:120-126` vs `:146`), so `\`+LF is accepted as two literal characters. bash deletes the pair and joins the lines. Measured consequences: `P03` admitted (bash turns `touch MARK-C` into extra `cat` arguments; exit 1, **no** marker) and `P19` admitted green with the rest of the line commented out. There is no execution vector here on its own: a `&&`/`|` after the continuation is still reached by the scanner (`P20` refused; `P32` refused). Reported because it is a real divergence in the newline model, not because it writes.

## 9. Classes that remain open (the deliverable)

1. **A — comment-phantom quote over a real newline** (`P15`, `P16`, `P30`). Highest severity measured: admitted **and** audit-green with a marker in the root. Both quote characters. Needs a balancing quote on a later line; line 2 must be valid bash.
2. **B1 — quote-spliced denied flags** (`P21`, `P22`, `P29`, `P43`): quotes inside the flag token defeat the raw `tok == f` / `tok.startswith(f+"=")` / `tok.startswith("-o")` tests.
3. **B2 — combined short options** (`P23`): `-noMARK` reaches `-o` without a token that starts with `-o`.
4. **B3 — ANSI-C spelling of a flag** (`P24`): `-$'\x6f'MARK` is `-oMARK` to bash.
5. **B4 — long-option abbreviation** (`P35`, `P36`, `P42`): `--o=`, `--out=`, `--o X` are `--output` to GNU getopt, and none starts with `--output`. `sort`-only (git rejects abbreviation, `P38`).
6. **C — exec-capable flag absent from `DENIED_FLAGS`** (`P26`, `P37`): `sort --compress-program` executes on spill.
7. **D — backslash-newline accepted as an opaque pair** (`P03`, `P19`): newline model gap, measured non-executing.

Not defects / explicitly out of scope: `P04`, `P04b`, `P07`, `P33`, `P40` are correct admissions (bash agrees the metacharacter is quoted); `P02`, `P09`, `P14`, `P31` are refused and inert; `P34` is admitted but bash refuses to parse it (fail-closed in effect). ANSI-C and comment handling were declared "refused-or-admitted conservatively and not claimed" by the lead; `P15`/`P16`/`P24` are **admitted-and-executing**, so if that note is read as covering them it understates the outcome. The python-head traversal residual (`RESIDUAL-python-traversal`) was not re-probed and is not re-reported; the gate-is-not-a-sandbox residual is unchanged.

## 10. Claim interaction and scope discipline

* C1 `kill_rule` and `counting_commands[0]` cover Q1-Q7 and the two controls only. None of the 43 derives here is Q1-Q7 or a control, so the frozen claim's values are untouched — this file reports residual **classes**, not claim failure.
* No lane file was edited: `claims.json`, the erratum, `corpus/`, `.ufo/waves/round-60/controls/` are read-only inputs. The correction above is text only, as required.
* Corroborating anchors in the lane: `L/corpus/instruments/figure-audit.py:27` (docstring allow-list), `:57-60` (`DENIED_FLAGS`), `:75` (`bash -c` invocation), `:88-153` (`split_segments`, R72 quote model at `:91`, metachar set at `:146`, unterminated-quote refusal at `:150-151`), `:156-167` (`denied_flag`), `:170-177` (`segment_ok`), `:180-185` (`check_read_only`). Claim anchors: `L/.ufo/waves/round-60/claims.json:15` (C1 frozen sentence naming Q5/Q6/Q7).

## 11. Hygiene

* Tooling: no installs or upgrades were needed; nothing was installed, so there is no tool/version/channel row to record. `pacman` was not invoked.
* Scratch: all clones/roots/ledgers/payloads/transcripts lived under `S`; the directory was removed before yielding (`rm -rf -- /fast/scratch/hyaku/kasegi-r60/ExecEscapes`). No leftover is named because none remains.
* No credential, token, cookie, session value or `op://` reference was read or written; nothing in this file is secret-bearing.
* No `git add/commit/stash/checkout/switch/reset/pull/push` and no `jj` ran against `L`; the only git mutations were `init`/`add`/`commit`/`config` inside throwaway fixture repos under `S`, each asserted with `git -C <repo> rev-parse --show-toplevel` = the fixture path before committing (`drive.py` `make_repo`).

Report: .ufo/waves/round-60/w1/ExecEscapes.md
