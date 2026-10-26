# CritC1Kill — round 38: attack on the C1 predicate and kill rule

Seat `CritC1Kill` (leaf critic; no subagent dispatch). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
read-only for this seat. Writes: this receipt and `/fast/scratch/hyaku/kasegi-r38/CritC1Kill/` only.
Assignment: `depth:verifiability`, round 38. Receipt-only item — no landable bytes, no deliverable file.

## 0. State read and method

| object | value |
|---|---|
| lane HEAD at work | `700153593eb586c70a6499c8ca225ee4d673bc9b` (`a173b0c2..HEAD` = 2 commits: `9a10b02` claims freeze, `7001535` wave1 spec + dispatch; no content change to the files below) |
| base / claims freeze | `a173b0c2b98c5ae39599fa9be76027fbbead0b9e` / `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` |
| r37 judged head / lane tip | `2387dcf6ccfefcfb703783387b9aade8fc82abfa` / `83975acc83df4bd8d5eaf463182ae615f2b64546` |
| frozen C1 predicate | `.ufo/waves/round-38/claims.json` line 24 (read `:24:raw`) |
| before-controls | `.ufo/waves/round-38/c1-controls/before.txt` |
| `corpus/instruments/r38-closure.sh` | absent at base and at HEAD (`git ls-tree -r --name-only a173b0c2 -- corpus/instruments \| grep -c r38-closure` → `0`); this review is against the frozen words, not an implementation |
| sibling deliverables used as instruments of the attack | `wave1/ExecDeclaredBlocks.gen.sh` (`49925cd4…`), `wave1/ExecFenceWalk.sh` (`f5018c46…`) |
| r38 time of measurement | runs below at 2026-10-26T18:2x–18:37Z |

I attacked the predicate and the kill rule, not the suite. The suite does not exist yet, so every claim
below is a property of the frozen bytes: given an honest implementation of the predicate as written, does
the routed defect stay open while the check is green, or does the check go red for a reason unrelated to
its defect. Two of the twelve findings are proven by executing the round's own helper scripts on
purpose-built trees; the rest are exact readings of the frozen text plus measured facts about the lane.

## 1. Scenario matrix for the five shapes the item names

| # | attack shape (item) | defeated by the frozen predicate? | finding |
|---|---|---|---|
| A | `Correction (round 38)` line names the right range, but the scaffolding is re-pasted in round 38 | **no** — limb (i) is satisfied by the line alone; limb (ii) is satisfied when the paste is fence-balanced; limb (iii) is satisfied by declaring the paste | K2 |
| B | `declared-blocks.txt` covers only a 1-line tail | **no** — the limb is `tail -n <lines> \| sha256`, and an undefended 1-line suffix is green over an arbitrary body | K2 |
| C | all-gates receipt copied from another round | **yes** for a cross-round copy (`all-gates v2` header + `suite-sha256` = executing digest; the r37 receipt is `all-gates v1`, `0da98e37…`) and for a stale same-round copy (`diff(export-ref, run-ref) ⊆ {receipt}`) | — (sound; see §6) |
| D | `*-results.json` with the right count but other seats | **no** — the limb counts seats and never compares names | K5 |
| E | ledger rows numbered 1–7 but empty | **no** — the limb counts 7 rows; cell content is unconstrained, and `7` is hardcoded rather than derived from the source | K6 |

Two further shapes the item invites, both **not** defeated: G8 accepts any file named
`corpus/instruments/r37-closure.sh` that prints `closed=14/14 exit=0` because no digest is bound (K8);
G6 is the one limb that is not a function of the commit, so `closed=8/8` is not reproducible from the
archive (K7). And one shape that kills the claim before any of these matter: **the frozen green ref is
unsatisfiable** (K1).

## 2. K1 — S1, kills the claim as frozen: `--export-ref <J>` cannot print `closed=8/8`

### The three frozen sentences, side by side

1. Predicate, line 24: "The committed instrument `corpus/instruments/r38-closure.sh` runs over a `git
   archive` export of a named lane head … and prints `closed=8/8 exit=0` on the round-38 judged head J".
2. `after`: "closed=8/8 exit=0 at J; … all-gates.txt receipt committed at Y (= J + receipt only)".
3. Counting command 1: `bash corpus/instruments/r38-closure.sh --export-ref <J> -> closed=8/8 exit=0`.

against

4. `judged_head_rule`: "J is the lane commit that carries every round-38 change **except that receipt**;
   the lane tip Y adds only the receipt file (`git diff --name-only J Y` = `.ufo/waves/round-38/final-gates/all-gates.txt`)".

and

5. G2: "`.ufo/waves/round-38/final-gates/all-gates.txt` **in the export** has header `all-gates v2`, an
   `export-ref=<40-hex>` that is REF or an ancestor of REF with `git diff --name-only <export-ref> REF` a
   subset of {that receipt path}, `suite-sha256=` equal to the executing suite's digest, eight
   `G<n> payload=... closed=1` lines, `closed=8/8 exit=0`, eight `selftest case=G<n>` lines …".

### The proof

An export of J does not contain the receipt (4: J carries everything **except** it; the receipt is the
one file Y adds). G2's first clause requires that file **in the export** to have the v2 header, so the
G2 check cannot be green on an export of J; it is red on presence alone, before any digest is computed.
Hence `--export-ref J` prints at most `closed=7/8 exit=1`. The only export ref on which G2 is satisfiable
is the receipt-bearing commit: `export-ref=J` is then an ancestor of the exported ref, and
`git diff --name-only J <exported>` is exactly the receipt.

The escape hatch a resident of this lane would reach for — grade yourself, `export-ref` = the exported
ref — is closed by hash circularity: a commit cannot contain its own hash, so the receipt committed at
`<exported>` cannot name `<exported>`, and `diff(Y,Y) = ∅ ⊆ {receipt}` is unreachable. The clause is
well designed *because* it forces the split; the split is what makes the headline wrong.

The r37 pattern is not available as a workaround. Measured on the r37 chain, whose receipt *was* inside
the judged-head export:

```text
$ git -C <lane> ls-tree -r --name-only 2387dcf6 -- .ufo/waves/round-37/final-gates/
.ufo/waves/round-37/final-gates/all-gates.txt
$ git -C <lane> diff --name-only 9492c776 2387dcf6
.ufo/waves/round-37/final-gates/all-gates.txt
SCORECARD.md
SHONEN.md
```

r37 could print `14/14` at its judged head because its receipt graded an ancestor with a three-file diff.
r38's `⊆ {that receipt path}` forbids exactly that diff, so r38 must split J and Y — and then its green
is at Y, not at J.

### Consequence under the kill rule

Kill limb 2 is "the judged-head export prints closed != 8/8 or exit != 0". An honest round-38 prints
`closed=7/8 exit=1` at J (G2 open, correctly: there is no receipt yet) and `closed=8/8 exit=0` at Y. A
canonical judge that runs counting command 1 literally must kill a correct claim. The claim is therefore
true only under a reading its own counting command contradicts.

### Smallest safe correction (no re-freeze needed)

* The report and SCORECARD state the pair: `export-ref=J` (the value inside the receipt) and `run-ref=Y`
  (the tip that carries the receipt), with `git diff --name-only J Y` = the receipt path — the same
  sentence `judged_head_rule` already uses, quoted at the point of the green.
* `r38-closure.sh` prints one identity line per run so the transcript is self-describing, e.g.
  `run=export ref=<rev-parse --short of the exported tree> export-ref=<receipt field> receipt=present|absent`,
  and `all-gates.txt` records that line. Then the green transcript names both refs and no reader has to
  guess which one `closed=8/8` belongs to.
* Do **not** "fix" this by exempting G2 when the receipt is absent or self-named: that makes the receipt
  non-required and re-opens D-B (the round's own routed defect), and it is the one hole this limb closes.

## 3. K2 — S2: G1's declared-blocks limb is green over a re-pasted D-A scaffold (item shapes A and B)

### The frozen limb, verbatim

"every round-38 end-of-file block appended to either file is byte-equal to its declaration in
`.ufo/waves/round-38/declared-blocks.txt` (one line `<path> <lines> <sha256>` per block; the file's last
`<lines>` lines hash to `<sha256>`)".

That is a **suffix** assertion with no lower bound on coverage and no statement that the declaration must
cover the whole append. The round's own helper documents the gap and offers an optional guard
(`wave1/ExecDeclaredBlocks.md` §8.5: "Base guard is optional"; §7 T7: `tail-only: rc=0` with "junk
inserted before the block").

### Constructed counterexample — executed

Tree: base `PROVINCE.md` (152 lines) + a 30-line D-A scaffold paste + a 2-line correction of record. The
scaffold is a verbatim-shape copy of the r37 paste (receipt section headings, property table, "Validation
on a scratch mirror", padding rows); the correction line names `PROVINCE.md L79-L152` as misplaced
receipt scaffolding, i.e. it satisfies G1 limb (i) on its face.

```text
$ git -C <lane> archive a173b0c2 PROVINCE.md | tar -x -C $S/t && wc -l PROVINCE.md
152 PROVINCE.md
$ cat scaffold30.txt corr2.txt >> PROVINCE.md && wc -l PROVINCE.md
184 PROVINCE.md
$ sha256sum scaffold30.txt corr2.txt
8e5e858f38c7ff19a764c6e0f7a239d16de8fc54675f2a8102da980df06ede5b  scaffold30.txt   (30 lines, 1415 B)
0c538afe3891363a5f60aab20528c4b3ee9aa357df1bf85564392fb5594be525  corr2.txt           (2 lines, 205 B)
```

Declaration produced by the round's helper over the 2-line correction (the honest declaration — nothing
forged):

```text
$ bash <wave1>/ExecDeclaredBlocks.gen.sh gen PROVINCE.md corr2.txt > declared-blocks.txt 2>gen.err; echo rc=$?
rc=0
$ cat declared-blocks.txt
PROVINCE.md 2 0c538afe3891363a5f60aab20528c4b3ee9aa357df1bf85564392fb5594be525
$ bash <wave1>/ExecDeclaredBlocks.gen.sh check declared-blocks.txt --root .
OK   PROVINCE.md lines=2 file_lines=184 sha256=0c538afe3891363a5f60aab20528c4b3ee9aa357df1bf85564392fb5594be525
declared=1 ok=1 fail=0 base=0 exit=0
$ want=$(awk '{print $3}' declared-blocks.txt); got=$(tail -n 2 PROVINCE.md | sha256sum | awk '{print $1}')
$ [ "$got" = "$want" ] && echo frozen-limb=GREEN
frozen-limb=GREEN
```

G1 limb (ii) on the same tree, with the round's own walker:

```text
$ bash <wave1>/ExecFenceWalk.sh PROVINCE.md
closed
```

G1 limb (i) is satisfied by the correction line itself. G1 limb (iii) is green as shown. **All three G1
limbs are green while 30 lines of receipt scaffolding sit in the front door.** The defect D-A exists in
the file exactly in the shape the round is closing, and the instrument reports `closed=1`.

The same tree with the optional guard the helper offers:

```text
$ { echo '# base PROVINCE.md 152'; cat declared-blocks.txt; } > declared-base.txt
$ bash <wave1>/ExecDeclaredBlocks.gen.sh check declared-base.txt --root .
OK   PROVINCE.md lines=2 file_lines=184 sha256=0c538afe3891363a5f60aab20528c4b3ee9aa357df1bf85564392fb5594be525
FAIL base PROVINCE.md file_lines=184 != pre_lines=152 + declared_lines=2 (lines were added before the declared block)
declared=1 ok=1 fail=1 base=1 exit=1
```

The guard is the fix; the frozen predicate does not require it.

### Why the 1-line tail is the cheapest exploit of the same hole

`PROVINCE.md 1 <sha of last line>` is green by construction on any file whose last line does not move, so
the declaration can cover one line of a 32-line round-38 append. Nothing in the limb rejects a
declaration smaller than the append. An **empty** `declared-blocks.txt` also satisfies the frozen wording
vacuously ("every block is byte-equal to its declaration" over zero declarations); the helper refuses it
(`FAIL empty.txt carries no declaration`, `exit=1`) — so the helper is stricter than the predicate, and a
suite that inlines the predicate's sentence instead of the helper's contract is green on an empty list.

### Smallest safe correction

Add to G1, per front-door file whose added-line count is > 0 (both numbers already available from
`git diff <base> REF -- <path>`):

1. exactly one declaration line for the path, `<lines>` = the **whole** added tail (measured today: the
   r37 appends were 74 lines to `PROVINCE.md` and 56 to `corpus/README.md`, so a round-38 append must be
   declared whole, not trimmed to its correction);
2. the `# base <path> <pre_lines>` guard when the round append is the file's last append (i.e. always,
   for these two files), or equivalently `wc -l <path>` == `pre_lines + <lines>`;
3. a non-empty list, one declaration per path, positive integer, 64 lowercase hex — the helper's
   `check` guarantees all of these, so naming the helper as the instrument is enough.

Do not add "no headings / no table rows" as the D-A test: the *intended* r37 README block legitimately
carries one `## Round-37 admission` heading and two tables. The scaffold-specific vocabulary is exact and
already measured in the base appends (added lines matching `^## [0-9]+\.`, `^\| property \| value \|`,
`Validation on a scratch mirror`): over the r37 append, `PROVINCE.md` 3 headings / 29 table rows / 1
scratch-mirror line and `corpus/README.md` 1/23/1; the 184-line counterexample holds 7 lines matching the
three-token vocabulary in total (4 already in base `PROVINCE.md`, 3 added by the 30-line fixture).
Requiring zero of those three patterns in the round-38 added lines is a small addition that cannot
mis-fire on the legitimate amendment.

## 4. K3 — S2: G2's selftest limb is weaker than the check r37 already had

The r38 predicate requires eight `selftest case=G<n>` lines and the summary. The r37 receipt carried the
stronger shape, and r37's own E10 check enforced it:

```text
$ git -C <lane> show 2387dcf6:.ufo/waves/round-37/final-gates/all-gates.txt | grep -E '^selftest case=' | head -3
selftest case=E1 positive=pass mutants=4/4 verdict=pass
selftest case=E2 positive=pass mutants=3/3 verdict=pass
selftest case=E3 positive=pass mutants=5/5 verdict=pass
```

r37's regex was `^selftest case=E[0-9]+ positive=pass mutants=([0-9]+)/\1 verdict=pass` (quoted in
`corpus/lessons/round-37-verifier-spotcheck.md` §2 C1). Round 38 dropped `positive=`, `mutants=n/n` and
`verdict=` from the receipt requirement, so a selftest that prints eight bare case lines and runs zero
mutants satisfies G2, while the kill rule's "summary-only forgery" clause covers only a receipt with the
summary and no case lines. This is a regression against the round that is supposed to close D-A..D-F.

Correction: restore r37's per-case regex with a non-zero back-reference, `mutants=([1-9][0-9]*)/\1`.

## 5. K4 — S2: G2's `payload=` may be empty of measurements

The r37 receipt's payloads were recomputable `k=v` measurements
(`E1 payload=placeholders=0,lane-hash-markers=0,round37-section=1,round37-final-lane-commits=1,bound=1`).
The r38 limb is `G<n> payload=... closed=1` with no content requirement, so `G1 payload=x closed=1`
satisfies it and the receipt records nothing a judge can recompute. Since D-B's wound was "the positive
run exists only as an assertion", a receipt whose payloads assert nothing reproduces the wound in a new
file. Correction: require named keys with numbers, one set per check, e.g. G1
`added-lines=<n>,declared-lines=<n>,fence=closed`, G3 `rows=8,tokens=0`, G4 `dispatches=<n>,seats=<n>,results=<n>`,
G7 `proposals=7,rows=7`, G8 `r37-closed=14,r37-sha=<12 hex>`.

## 6. K5 — S2: G4 compares seat counts, never seat identities

G4: "every `.ufo/waves/round-38/*-dispatch.json` in the export has a tracked sibling `*-results.json`
that parses as JSON and lists exactly as many seats as the dispatch's `taskCall.tasks`". Measured attack
against the real r37 harness shape (same schema the r38 wave uses):

```text
$ python3 -c "... r37 wave1-dispatch.json ..."
count-only green: True n= 64
name-set equal: False
```

A `*-results.json` with 64 entries named `seat-00`…`seat-63` is green. The real harness is already
name-complete, so identity equality costs nothing and is reproducible:

```text
r37 dispatch tasks: 64
r37 results seats field: 64 type int results len: 64
names equal: True missing from results: 0 extra in results: 0
empty outputs: 0
```

Two further ambiguities in the same limb: "sibling" is undefined (the harness writes
`.ufo/waves/round-37/kasegi-r37-build-results.json`, *not* `wave1-results.json`, so a stem-matched check
looks for a file the lane does not have, while a glob `*-results.json` would accept the wrong file if two
exist); and `seats` is an integer field in the r37 file, so "lists exactly as many seats" can be read
against `seats` (an int) instead of `len(results)`.

Correction: `len(results) == len(tasks)` **and** multiset equality of `results[].name` with
`taskCall.tasks[].name`; every `output` non-empty; pick the results file by the dispatch's `wave` field
rather than by filename shape.

## 7. K6 — S2: G7 counts rows, not dispositions; `7` is not derived from the source

Source measured: `considerthese/2026-10-26.md` has exactly seven numbered proposals under
"Self-improvement suggestions" (1–7), so `7` is right *today* and wrong the moment the file gains or
loses an item. The empty-row attack:

```text
$ printf '%s\n' '| # | proposal | disposition | evidence |' '|---|---|---|---|' '| 1 | | | |' … '| 7 | | | |' > ledger7.md
$ grep -cE '^\| *[1-7] *\|' ledger7.md
7
(row-count-only check green with 7 empty rows)
```

G7 as frozen is satisfied by seven rows with empty disposition and empty evidence. This is the exact
defect D-F reports one round earlier (r37 "claimed an 18-row table" that did not exist), so a count-only
limb re-admits it in table form. The anchor is real and empty as described:

```text
$ git -C <lane> show a173b0c2:corpus/knowledge/considerthese-proposals-ledger.md | sed -n '37,40p' | cat -A
## Round-37 dispositions (appended 2026-10-26, R31 home)$
$
$
$
```

Correction: derive N from the source (`grep -cE '^[0-9]+\. \*\*' considerthese/2026-10-26.md` → 7) and
require N rows; each row's disposition cell ∈ a closed vocabulary (`adopted|declined|deferred|superseded|open`)
and each evidence cell to resolve as `<path>:<line>` in the export.

## 8. K7 — S2: G6 is the only non-export limb, so `closed=8/8` is not a function of the commit

G6 reads live host state: "`/fast/scratch/hyaku/kasegi-r36` and …`-r37` hold zero entries (or are absent)
and …`-r38` holds nothing except the suite's own `--work` dir". Measured at 2026-10-26T18:3xZ:

```text
$ find /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38 -mindepth 1 | wc -l
45288
$ find /fast/scratch/hyaku/kasegi-r3[678] -mindepth 1 -maxdepth 1 -type d | wc -l
27
```

Three consequences:

1. **Non-reproducible verdict.** Re-running the same `--export-ref Y` minutes later, or on another host,
   can flip one of the eight checks with no tracked byte changed. The claim's frame is "export mode
   only"; that sentence is false for one limb, and a judge who expects determinism will read the
   difference as a forgery rather than as host state.
2. **Red for a reason unrelated to its defect, at every intermediate state.** Mid-wave the limb is red
   because 26 seat dirs and the L1's own `L1/` dir exist. The receipt-producing run must therefore be
   sequenced after *every* seat has removed its scratch, including the L1's — an ordering fact that no
   clause states, and the same closure-order class as D3.
3. **The exception is name-shaped, not provenance-shaped.** "the suite's own `--work` dir" is matched by
   name; and the scratch discipline permits `/tmp` for files under 50 MB, which the three enumerated
   paths never see.

Correction (keep the check, bound the damage): record the measurement in the receipt — absolute paths
found, `run-utc`, count — so the limb is auditable rather than silent; widen the globs to
`/fast/scratch/hyaku/kasegi-r3[678]*` and `"${TMPDIR:-/tmp}"/kasegi-r3[678]*`; and state in the suite
header that this limb measures the host, so `closed=8/8` is reproducible only on a quiescent host.

## 9. K8 — S3: G8 carries the r37 suite forward without binding its bytes

"G8 (carry-over) `corpus/instruments/r37-closure.sh --export-ref REF` prints `closed=14/14 exit=0`." No
digest appears. Today the file is unchanged, measured:

```text
$ git -C <lane> rev-parse 2387dcf6:corpus/instruments/r37-closure.sh
68ac41e8fdab46ba508800a377f396e663f2a436
$ git -C <lane> rev-parse HEAD:corpus/instruments/r37-closure.sh
68ac41e8fdab46ba508800a377f396e663f2a436
```

so the limb is sound *by luck*. Any file with that name satisfies it:

```text
$ printf 'echo "closed=14/14 exit=0"\nexit 0\n' > r37-stub.sh && bash r37-stub.sh --export-ref a173b0c2…
closed=14/14 exit=0
stub rc=0
```

A round-38 seat that finds an E-check inconvenient (e.g. E14, the D6 status-read check) can neuter it and
G8 stays green, silently retiring the r37 defect closure. Correction: G8 first asserts
`git rev-parse REF:corpus/instruments/r37-closure.sh` == `68ac41e8fdab46ba508800a377f396e663f2a436`
(equivalently `git diff --quiet 2387dcf6 REF -- corpus/instruments/r37-closure.sh`), then runs it.

## 10. K9 — S3: G5's section limb is vacuous when the section is absent; the drift vocabulary is three literals

"the round-38 SCORECARD.md section has zero `Final lane commit:` lines" is satisfied by an absent
section, and nothing in G1–G8 requires the section to exist or to carry the round-38 axis rows. The
drift vocabulary (G2) is `final head`, `final lane head`, `Final lane commit`; a line reading
`judged head: 700153593eb586c70a6499c8ca225ee4d673bc9b` or `lane tip: 83975acc…` is a new round of the
same D-D label drift and passes. Correction: require the round-38 section to exist with its axis rows;
require the exact reference sentence G2 already names; and require every 7+-hex token in the round-38
SCORECARD/SHONEN sections to carry a label from the allow-list {`anchor ancestor`, `base`,
`r37 judged head`} (the only three heads a lane file may name).

## 11. K10 — S3: the fence limb is described narrower than CommonMark and narrower than the delivered walker

Frozen words: "fence state at EOF is closed under a CommonMark fence walk (opening fence = ``` with
optional info string; closing fence = ``` with no info string)". That parenthetical is not CommonMark:
it ignores `~~~` fences, ignores openers of four or more backticks, and rejects a legal longer-or-equal
closer. A `~~~`-opened block at EOF reads "closed" to a literal implementation and "open" to the delivered
walker; a 3-tick opener closed by a 4-tick run reads "open" to the literal reader and "closed" to the
walker. `wave1/ExecFenceWalk.md` implements the correct rule and agrees with `cmark 0.31.2` on 9/9 files
including `~/` fixtures, so the deliverable is right and the sentence is wrong — a judge re-deriving from
the frozen text can contradict the suite in both directions. Correction: replace the parenthetical with
the walker's rule (`^ {0,3}(`{3,}|~{3,})` opener with optional info string; closer = same character,
length ≥ opener, info-free; 4+ spaces of indentation is never a fence) and cite the 9/9 agreement.

## 12. K11 — S3: `REF` is an undefined token in the frozen predicate

The predicate uses `<base> REF`, "REF or an ancestor of REF", "in the export". `J` and `Y` are defined
in `judged_head_rule`; `REF` is defined nowhere (`grep -n 'REF is\|define REF' claims.json` → no match).
Two readings exist, and one is fatal to G2:

* REF = the ref passed to `--export-ref` (the intended reading; makes K1 a theorem);
* REF = the receipt's own `export-ref` field (then `git diff --name-only <export-ref> REF` compares a
  value with itself: `∅ ⊆ {receipt}` always, the ancestry clause degenerates to "is itself", and a
  copied or stale receipt is accepted).

A suite author implementing the second reading produces a vacuous G2 that looks green. Correction: define
`REF` once in the predicate head ("REF is the ref passed to `--export-ref`"), and add a selftest mutant
that names a non-ancestor sibling commit as `export-ref` (must be red) — that mutant distinguishes the
two readings.

## 13. K12 — S3: the kill rule's `corpus/lessons/round-38.md` grep has undefined behaviour on an absent file

Kill limb: `` `grep -c '⟨pending' corpus/lessons/round-38.md` != 0 ``. Measured semantics and state:

```text
$ grep -c 'x' /nonexistent/file.md; echo rc=$?
grep: /nonexistent/file.md: No such file or directory (os error 2)
rc=2
$ git -C <lane> ls-tree -r --name-only a173b0c2 -- corpus/lessons/ | grep -c 'round-38'
0
```

The base tree has no round-38 lesson. On a tree that still lacks it, `grep -c` prints no count and exits
2, so `!= 0` is satisfied by the empty string and the kill fires on a missing file; conversely G3's token
limb scans only *added* lines, so a round that omits the lesson entirely is green on all eight checks. The
kill rule therefore adjudicates a state the predicate never measures. Correction: make it a limb — require
`corpus/lessons/round-38.md` to exist at REF and carry zero tokens of the widened vocabulary — and drop
the side-condition grep.

## 14. Smallest safe corrections, ranked

| id | sev | one-line fix | cost |
|---|---|---|---|
| K1 | S1 | report + receipt name `export-ref=J` and `run-ref=Y`; suite prints a `run=export` identity line | 1 sentence + 1 echo |
| K2 | S2 | G1 requires the whole appended tail per front-door file and the `# base` guard (or the helper's `check`) | 2 conditions, helper already built |
| K3 | S2 | restore `selftest case=G<n> positive=pass mutants=([1-9][0-9]*)/\1 verdict=pass` | 1 regex |
| K5 | S2 | G4 requires `results[].name` multiset == `tasks[].name`, non-empty `output`, results picked by `wave` | 3 lines of jq/python |
| K6 | S2 | G7 derives N from the source and requires a closed-vocabulary disposition + resolvable evidence per row | 2 conditions |
| K7 | S2 | receipt records the G6 measurement; globs widen; header states the one host limb | 1 line + 1 comment |
| K4 | S2 | G2 requires named numeric keys per payload | 1 regex per check |
| K8 | S3 | G8 pins `r37-closure.sh` to blob `68ac41e8…` before running | 1 line |
| K9 | S3 | G5 requires the section to exist; allow-list the only three heads a lane file may name | 2 conditions |
| K10 | S3 | G1's fence parenthetical replaced by the walker's rule | 1 sentence |
| K11 | S3 | define `REF`; add the non-ancestor `export-ref` mutant | 1 clause + 1 mutant |
| K12 | S3 | round-38 lesson existence + zero tokens becomes a limb | 1 condition |

## 15. What the predicate does defeat (do not over-correct)

* **Cross-round receipt copy** — `all-gates v2` plus `suite-sha256` = the executing suite's digest; the
  r37 receipt is `all-gates v1` with `0da98e37…`. A copy from any other round or lane fails the header or
  the digest.
* **Stale same-round receipt** — `diff(export-ref, run-ref) ⊆ {receipt}` fails the moment the tree moves
  after the receipt.
* **Self-grading receipt** — impossible: a commit cannot contain its own hash, so `export-ref` always
  names a pre-receipt state.
* **A red base or red r37 head** — the two red limbs are the right two refs, and both are named by hash
  (commands 3 and 4), so the trap is well formed.
* **Summary-only selftest forgery** — the kill rule names it; K3's mutants field makes it stick.
* **Placeholder tokens** — the widened vocabulary on added lines is the right shape; only case/space
  variants (`TODO` vs `todo`, `<fill />`) escape it, which a case-insensitive match closes. Ordering the
  scan over *added* lines is correct and cheap.

## 16. Impacted axes and verdict

| axis | impact |
|---|---|
| depth:verifiability (C1, held 4) | K1 is a claim-truth hazard: the frozen counting command cannot print the frozen green, and the kill rule fires on an honest implementation. K2/K5/K6 are instrument-coverage gaps that let D-A, D3 and D-F stay open while green — i.e. the claim sentence "its eight checks close the routed defects" is overstated unless the corrections land. No other axis is touched; C2 has no exposure here. |
| depth:density | none (this seat writes one receipt, no lane file) |
| coverage | none |

This is a **fixable defect, not a tradeoff**: every correction above is one clause or one regex, and none
of them weakens a check. The one item the canonical judge must not accept is K1's wording — if the report
presents `--export-ref <J>` as the green command, a literal kill-rule application rejects a correct round.

## 17. Tooling, scratch, cleanup

* No tool installed, upgraded or removed; no `pacman` invocation; no network fetch; no host service
  touched. `python3 3.14.8`, `GNU bash 5.3.20(1)`, `coreutils 9.12` were already present.
* No mutating git/jj command was run. One fixture repo was created for the bind rule and verified:
  `D=$(mktemp -d -p "$S") && git -C "$D" init -q` with
  `[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]` → `fixture-ok`. All other git use was
  `rev-parse`, `ls-tree`, `show`, `diff`, `archive` (read-only).
* Scratch `/fast/scratch/hyaku/kasegi-r38/CritC1Kill/` (counterexample tree, helper runs, stub, ledger
  fixture) removed after this receipt was written.
* Deliverable: none (receipt-only item). No line count or sha256 to report.
