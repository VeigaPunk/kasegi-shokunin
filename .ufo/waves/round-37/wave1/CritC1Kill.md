# CritC1Kill — adversarial attack on the C1 kill rule (round 37)

seat: `CritC1Kill` (critic, leaf). Lane `kasegi-shokunin`, base `b56a41680cefd391868c1c370dc063c69d827e7d`,
claims freeze `224df74db2a46d627ae1475a72ca48796bbd177c`, frozen claims
`.ufo/waves/round-37/claims.json` (read only). Judged on **depth:verifiability**. Milestone round-37.

Question attacked: can `corpus/instruments/r37-closure.sh` print `closed=14/14 exit=0` on the round-37 final
lane head while one of D1–D6 is still open? Method: read the frozen predicate + kill rule, the r36 spot-check
§5, the committed bytes of the defect sites, the r36 suite's own code, and the wave's landed C1 receipts
(`ExecC1BaseFail`, `ExecC1JudgedHeadFail`, `ExecC1Fixtures`, `ExecC1ExportMode`, `RevC1Selftest`,
`ScribeScorecard`, `ScribeLOG`, `ScribeMistakes`); then build the counterexamples in scratch. The r37 suite
does not exist at this read (`ls corpus/instruments/r37-closure.sh` exit 2), so every attack is against the
**frozen measurable wording**, the **committed defect bytes**, and the **wave's own planned implementation**
(the stand-in and the Scribe drafts), not against r37 suite bytes.

All scratch lived under `/fast/scratch/hyaku/kasegi-r37/CritC1Kill` and was removed before yield. The only git
mutation was `git init/add/commit` inside a `mktemp`-class scratch repo whose `rev-parse --show-toplevel`
was compared to its `pwd -P` before commit. No lane, fleet, sibling-lane or source-tree file was modified.
Tooling: no installs, no upgrades (none needed).

## 1. Verdict

**As frozen, C1 is not judge-safe.** The kill rule is written as shape/count/section-scoped greps, and it has
holes through which a *compliant* 14/14 run can leave an open routed defect:

| defect | frozen instrument | can 14/14 coexist with the defect? | why |
|---|---|---|---|
| D1 positive receipt | E10 | **yes** | receipt genuineness is measured only by counts + a self-referential digest; payload content, ids, export-ref and case↔detail binding are unmeasured |
| D2 false `r36-fixtures` | E11 | **mostly no** (weakly yes) | a non-retraction sentence that names the path + correction word passes; the recomputed-absence limb is only in the fixture designer's stand-in |
| D4 final-commit label | E12 | **yes, and the wave plans it** | E12 requires a *new* `c20300df … anchor ancestor` label and scopes the stale `Final lane commit: e666d902` to the round-37 section; `SCORECARD.md:1492` and `corpus/lessons/round-36.md:3` are left uncorrected (Scribe draft F5 says exactly this) |
| D5 registry row | E13 | **yes** | the committed row is `gate\|probe` (escaped): a raw-token absence grep reads 0, and a naive `|` split misaligns column 4 onto the entry-command cell, which already contains `exit 2` |
| D6 fail-open status | E14 | **yes** | shape-only: spaced (`2> /dev/null`) and merged-stream (`>/dev/null 2>&1`) swallows, plus the suite's own `count_lines` (empty→0), all evade; the behavioral corrupt-index fixture exists but is not in the frozen E14 |
| D3 closure order | — | n/a | the frozen predicate says E1–E14 close **six** defects; the wave's own SCORECARD after-cell says D3 is **not** an E-check. The claim overstates its own coverage. |

Required before any gate/verdict data is collected: a **claims-erratum-2** (append-only) with the P0 limbs in
§4, or the judge will reject C1 on D4/D1/D5/D6 (the four where the frozen text can go green with the defect
present). With the P0 amendments the claim becomes judge-safe and buildable; the alternative (leaving the
predicate and trusting the wave to also do the unmeasured repairs) is not judge-safe, because a claim's truth
may not rest on an action its instrument neither requires nor measures.

## 2. Attack table

`D?` = routed defect the attack leaves open; `frozen?` = does the frozen predicate + kill rule defeat it?

| # | attack (scenario that prints 14/14 with the defect open) | evidence (committed bytes / observed) | frozen? | smallest safe correction |
|---|---|---|---|---|
| K1 | **D4 relocation.** Append the drafted round-37 section (`anchor ancestor: c20300df…`, no stale literal) and change neither `SCORECARD.md:1492` nor `corpus/lessons/round-36.md:3`. E12 green; both false "final lane commit e666d902" statements stand. | `SCORECARD.md:1492` = `Final lane commit: e666d902337a49dcbfc…` (round-36 section, `## Round 36` at `:1406`, next `## ` after it: none, file is 1494 lines); `corpus/lessons/round-36.md:3` = `…final lane commit \`e666d902…\` (filled at closure)`; wave draft `wave1/ScribeScorecard.md` F5: *"The round-36 stale label remains at SCORECARD.md:1492 … leaves the round-36 bytes alone"*; `wave1/ScribeMistakes.md` M37-3 records the mislabel but does not relabel it; the wave's own red control measures D4 with a **file-wide** `grep -c 'Final lane commit: e666d902' SCORECARD.md` (>=1) — that value is still 1 at a compliant final head | **no** — predicate and kill rule both scope to the round-37 section; the check's required hash is `c20300df`, but the mislabeled hash is `e666d902`, so E12 never touches the defect | P0-1: E12 binds the correction to the mislabeled site (same line or immediate successor carries `anchor ancestor`) in both files; kill-rule stale limb becomes file-wide and markdown-normalized; add the mutant "round-37 section clean, `:1492` bare" → must be **red** |
| K2 | **E10 forged receipt.** Hand-write `all-gates.txt`: `suite-sha256=<sha256 of the suite>`, 14 `E<n> payload=` lines, `closed=14/14 exit=0`, 14 `selftest case=` lines, `cases=14 failures=0`. | demo (scratch): `header_sha_match=1 E_lines=14 closed_line=1 case_lines=14 selftest_total=1`; a **lying** variant (14 unique ids, every payload `closed=0`, bare case lines) also passes every limb the wave's stand-in checks: `payload-lines=14 payload-ids=14 closed-line=1 selftest-cases=14 selftest-ids=14 summary=1`, while `closed=1 payload lines=0`. The builder spec's E10 is literally *"contains ≥14 `E<n> payload=` lines; contains `closed=14/14 exit=0`; contains ≥14 `selftest case=` lines and `cases=14 failures=0`"* (`wave1-spec.json` ExecC1SuiteBuild) | **no** — "(genuine suite output)" is a parenthetical, not a limb; no payload-value, id-uniqueness, `closed=1`, case↔detail, or export-ref binding; the fixture matrix breaks only the digest and deletes lines | P0-2: E10 must bind content (see §4). Add the mutant "digest correct, one payload edited / one case line forged" → red naming the limb |
| K3 | **E13 escaped pipe + column shift.** Keep the committed row. A raw-token check for `gate\|probe` (unescaped) reads 0; a naive `|` split reads type cell `gate\`→`gate` (single choice) and column 4 = the entry-command cell, which contains `exit 2`. Both E13 limbs go green on today's bytes. | `SKILL.md:1111` raw = `| r36-closure.sh | gate\|probe | \`bash … --export-ref <hash>\` (export-mode only; a plain run refuses with exit 2) | one \`E<n> payload=… closed=0\|1\` … exit 0 only for K=9 | …`; the line's bytes hold the **escaped** form (a backslash between `gate` and the pipe): an unescaped-literal count on that line is 0 and an escaped-literal count is 1 (§3.3 shows both); a naive split's 4th cell = the entry command (`exit 2` present); the rendered 4th cell (cell-aware split) has **no** `exit 2`, **no** `could-not-evaluate`; the same bytes hold at `a23dc478` (so a raw-absence E13 is green at the r36 judged head where D5 is open) | **no** — "not the literal `gate\|probe`" is satisfiable by the escape; the fixture designer found the split bug (§4.2) but that fix is in the stand-in, not in the frozen limb | P0-3: parse cells with the markdown escape rule, require exactly one row, inspect the rendered type cell and the rendered verdict-map cell; mutants: escaped pipe, duplicate row in a non-registry/other section, tokens only in the entry-command cell |
| K4 | **E14 shape-only fail-closed.** Write the status read as `git … status --porcelain 2> /dev/null` (space) or `… status --porcelain >/dev/null 2>&1` (merged stream); or keep `count_lines`, which maps an empty stream to "0". E14's shape greps stay clean and the limb reads clean on a failing status read. | scratch fixture repo with a corrupt `.git/index`: `git status --porcelain` → rc 128; my r36-shape function → `status-dirty=0`; spaced redirect → `0`; merged stream → `0`; fail-closed shape → `status-read=failed`. `corpus/instruments/r36-closure.sh:294` `count_lines(){ grep -c . 2>/dev/null || true; }` (empty→"0"); D6 site `:465-466`. The fixtures seat's E14 mutants are (a) the literal `${porcelain:-0}` and (b) the literal `2>/dev/null` (ExecC1Fixtures §2) — neither covers the variants | **no** — the limb is a spelling grep; the behavioral fixture (corrupt index) exists for E9(b) but is not part of the frozen E14 | P0-4: make E14 behavioral — execute the suite's own quiescence status limb on the corrupt-index fixture and require red/`status-read=failed`; keep a **scoped** regex (`git[^|]*status[^|]*2>/dev/null`, spaces allowed) as belt-and-braces; add spaced/merged mutants |
| K5 | **E9 scratch-root absence.** Run the closure with `/fast/scratch/hyaku/kasegi-r37` absent (cleaned, typo'd, or `/fast` not mounted) or with a non-default `--scratch-root`: `find` yields 0 dirs, limb (c) green, "no leftover seat dirs" asserted over a path that was never read. | `r36-closure.sh:469` sets `sroot_state=present` only if `[ -d "$sroot" ]`; the closed condition at `:481-483` tests `porcelain`, `left`, `head_ok`, `root_ok` — **not** `sroot_state`; the payload prints `scratch-root=present|absent`, so the signal exists but is not a verdict | **no** — the predicate says "no leftover … seat dirs", silent on root presence/readability; the kill rule is the same | P0-4 (same erratum): E9's closed condition requires `scratch-root=present` on the default literal path (or records `deviation=non-default --scratch-root`), absent/unreadable root = red |
| K6 | **Red attribution vacuity.** `closed<14/14 exit=1` at the two r36 exports is satisfied by *any* failing subset (or a crash). An E13 implemented as raw-token absence is **green at a23dc478** where D5 is open, yet the red still holds through E10/E11/E12/E14 — so the required red cannot detect E13 vacuity. | at `a23dc478`: `corpus/instruments/r36-closure.sh` present; `SKILL.md:1111` escaped (`gate\|probe`, raw unescaped count 0); `.ufo/waves/round-37/final-gates/all-gates.txt` absent; no `## Round 37` in `LOG.md`; no r37 lesson → E10/E11/E12/E14 red | **no** — the counting command pins only the total, and the parenthetical "(E10–E14 open there)" is not measured | P0-5: the red run must print an `open=` list; at `a23dc478` require E10, E11, E12, E13, E14 each reported `closed=0` by id; the E13 mutant must be the committed escaped-pipe row |
| K7 | **E10 foreign-head receipt.** A receipt produced on a different head (suite bytes unchanged; all checks green there), committed at the final head, satisfies every frozen E10 limb; D1 says "for the head it names" but the frozen limb has no `export-ref` at all. | the r36 receipt has no header (`cat .ufo/waves/round-36/final-gates/all-gates.txt` → starts `== selftest ==`); the r36 suite's own run header prints `export-ref=… suite-sha256=…` (`r36-closure.sh` run header), so the field exists; the frozen E10 lists only the digest header and the four counts | **no** — no ref binding, no id-uniqueness, no `closed=1` count | P0-2(e): receipt names `export-ref=<P>`, P an ancestor of the checked ref, `git diff --name-only P <checked>` == the receipt path. **Do not** require P == checked head: that is unsatisfiable (a commit cannot carry its own minted receipt; the M36-1 self-reference class) |
| K8 | **E11 non-retraction / wrong-site correction.** An entry that names `corpus/instruments/r36-fixtures/` and the word "correction" without retracting, or that asserts presence, passes a keyword shape. | `LOG.md:1665` (round-36 C1 bullet) `Landed \`corpus/instruments/r36-closure.sh\` + \`corpus/instruments/r36-fixtures/\`.`; `git ls-tree -r --name-only <ref> \| grep -c r36-fixtures` = 0 at `cc692008`, `a23dc478`, `c20300df`, and HEAD. The planned correction (`ScribeLOG.md:28`) is truthful; nothing in the frozen limb forces the absence recomputation | **partly** — if the check recomputes absence, a false presence claim dies; a non-retraction sentence that does not assert presence survives | P1: require (a) recomputed absence at the export ref and at a23dc478, (b) a retraction verb from a closed set bound to the path, (c) reject a line that asserts presence; mutant already designed (`named-correction=0`) |
| K9 | **D3 overclaim.** The frozen predicate and `after` assert six defects closed by E1–E14; the wave's own after-cell says D3 is carried as mistake rows, not an E-check. A judge reading the claim sees an instrument that cannot close one of the six it names. | `claims.json` C1 predicate: *"Its fourteen checks E1-E14 close the six routed defects D1-D6"*; `claims.json` C1 after: *"E9 fail-closed shape proven (D1-D6 closed)"*; `ScribeScorecard.md` after-cell: *"E10-E14 close D1, D2, D4, D5 and D6; D3 … not as an E-check"* | **no** — identity/scope mismatch inside the claim | P0-1: erratum restates "E10–E14 close D1, D2, D4, D5, D6 by instrument; D3 by lesson mistake row + dispatch order, explicitly not instrumented" and fixes the `after` line |
| K10 | **E12 wrapped / heading-split stale label.** `Final lane commit:` + newline + `e666d902…`, or `Final lane commit: **e666d902**`, or the stale literal moved under a second `## ` heading inside the round-37 block. Literal in-section grep misses all three. | scratch: wrapped form `literal=0 joined=1`; markdown normalisation needed (backticks/emphasis/line wrap); the round-37 block's closing pair `Anchor ancestor: …` then `Final lane commit: …` must stay under one `## ` heading | **no** (the in-section literal is the only measured form) | P0-1: normalise before matching (strip backticks/emphasis, join wrapped lines, ignore fenced code), define the section by the committed `## Round 37 result …` heading closed by the next `## `, and require the anchor line and the final-commit line in that window |

Additional false-negative of the same class as K3/K4 (already covered, listed for the builder):

| # | hazard | evidence | correction |
|---|---|---|---|
| H1 | **Self-poisoning selftest literals.** If the suite's mutant-construction code contains the literal `porcelain:-0` or `git … status … 2>/dev/null`, E14's own scan of the exported suite goes red (13/14) **and** the kill-rule grep `grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh != 0` kills the claim — even though the deployable limb is fail-closed. | the fixtures seat's wiring puts the literal into the suite's `printf` (§2 E14(a)/(b), §5); r36 already assembles its hunted tokens: `ph=$(grep -cF -- "filled by the $(printf 'L1')" …)` (`r36-closure.sh:309-310`) | build both mutant strings by concatenation (`p='porcelain=${porcelain:-'; sfx='0}'`), so the suite bytes never contain the literal; state it in the builder item |
| H2 | **Whole-file redirect grep.** `grep -cF '2>/dev/null'` on the suite is not a status-read test: r36 legitimately has 41 occurrences (`sha256sum`, `realpath`, `grep -c`, `rev-parse`, …) and exactly **1** status-line swallow (`grep -cE 'status[^|]*2>/dev/null'` → 1). A whole-file limb would be a permanent false red. | measured on `corpus/instruments/r36-closure.sh` | scope the limb to the status command (regex above) and rely on the behavioral corrupt-index test |
| H3 | **E1 four-line window sweep.** E1 binds 40-hex on a `Final lane commit:` line **or the four lines after it**; the round-37 block is appended at `SCORECARD.md:1495+`, so depending on blank lines the frozen-claim paragraph (`b56a416…`, `224df74d…`) can fall in `:1492`'s window. Those are ancestors (bound), but any non-ancestor hash in that window turns E1 red for a reason unrelated to closure. | `ScribeScorecard.md:1492` boundary; fixtures seat §4.1 measured the same class (`round36-final-lane-commits=2,bound=1`) | keep ≥5 lines (or a non-hash line) between `:1492` and the first 40-hex of the appended block; do not put the final-head hash within four lines of a historical `Final lane commit:` |

## 3. Strongest counterexamples, in full

### 3.1 D4: the claim's own instrument cannot see the defect it says it closes (K1, K9)

The routed defect (spot-check §5 D4): *"`corpus/lessons/round-36.md:3` and `SCORECARD.md`'s `Final lane commit:
e666d902…` name an intermediate ancestor, not the round's final head (`a23dc478`, then `c20300df`). Label it as
the anchor ancestor."* The correct hash to relabel is **e666d902**.

The frozen E12 instead requires a *new* label — `c20300df … anchor ancestor` — and forbids the stale literal
only **inside the round-37 section**. The wave's own draft makes the consequence explicit:

```
$ grep -nF 'Final lane commit: e666d902' SCORECARD.md
1492:Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b
$ awk 'NR>1406 && /^## /{print NR": "$0}' SCORECARD.md   # no heading after Round 36
$ wc -l SCORECARD.md
1494 SCORECARD.md
```

`ScribeScorecard.md` §3.2: *"The round-36 section's stale line at `SCORECARD.md:1492` is outside this section's
scope; relabel it only if you also keep E12's round-37-section grep clean."* F5: *"the draft therefore relabels
only through the anchor-ancestor convention and leaves the round-36 bytes alone."*

So after a fully compliant closure: E12 green (`c20300df` labelled, no stale literal in the round-37 section),
suite `closed=14/14`, and both false statements intact. The wave's own red measurement for D4
(`grep -c 'Final lane commit: e666d902' SCORECARD.md` >= 1 at the r36 heads) **never moves to 0** — the
instrument's final-head criterion and its own defect-state criterion disagree. The claim's `after` says
"D1-D6 closed"; D4 is not. This is a kill of the claim as frozen, not a defect of the wave's intent (the wave
records the mislabel as M37-3; it just does not correct it, and the instrument does not require the correction).

### 3.2 E10: the positive-limb receipt is forgeable without touching the digest (K2, K7)

Frozen E10, in full: digest header equal to the suite's digest, fourteen `E<n> payload=` lines,
`closed=14/14 exit=0`, fourteen `selftest case=` lines, `cases=14 failures=0` ("genuine suite output committed
in-tree"). The builder item drops even the parenthetical and asks for `≥14` lines.

Observed (scratch, stand-in suite = committed `r36-closure.sh`, sha `4db1ae70…`):

```
$ # hand-written receipt: header = sha256sum of the suite, 14 fabricated payloads, 14 bare cases
header_sha_match=1
E_lines=14
closed_line=1
case_lines=14
selftest_total=1

$ # lying receipt: every payload says closed=0, summary says 14/14, case lines carry no verdict/detail
payload-lines=14 payload-ids=14 closed-line=1 selftest-cases=14 selftest-ids=14 summary=1
closed=1 payload lines=0
```

Nothing in the frozen E10 can distinguish these from a real run. The fixture matrix breaks only (a) the digest
and (b) a deleted line — the two attacks the shape check does catch. Missing limbs, all implementable without
circularity:

1. each id E1..E14 exactly once, every payload line ending `closed=1`, zero `closed=0`;
2. the **13 non-E10 payload values byte-equal the values the suite computes in this run** (E10's own line is the
   one self-asserted line — comparing it would be circular);
3. the selftest section passes the r36 judge (`r36-closure.sh:763+`: case line + detail line + `verdict=pass` +
   `mutants=n/n`; the three forged reports rejected — the r36 receipt already records
   `judge=forged-caselines|forged-failed-cases|forged-detail-free rejected=1`);
4. the receipt names `export-ref=<P>`, P an ancestor of the checked ref, with
   `git diff --name-only P <checked>` == the receipt path. Equality P == checked head is **unsatisfiable** (the
   receipt must be committed after it is minted); the ancestor+diff-scope form is the satisfiable binding and it
   forces the closure-order discipline D3 asks for (mint from the parent, commit only the receipt).

With limb 2 in place the forged receipts above are red, and the check remains satisfiable: the real
two-commit closure (P = final content, H = P + receipt) has identical 13 payloads at H.

### 3.3 E13: the committed row already demonstrates both escapes (K3)

```
$ python3 - <<'PY'   # cell-aware render of SKILL.md:1111
type cell      = 'gate|probe'          # non-choice
verdict cell 4 = '… closed=K/9 exit=0|1; exit 0 only for K=9'   # no exit 2, no could-not-evaluate
entry cell 3   = '… a plain run refuses with exit 2'            # contains the token
PY
$ printf '%s' "$ROW" | grep -cF 'gate|probe'      # raw unescaped
0
$ printf '%s' "$ROW" | grep -cF 'gate\|probe'     # escaped
1
$ awk -F'|' '{print $5}' <<< "$ROW"               # naive split, 4th cell
 `bash corpus/instruments/r36-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit 2)
```

So (i) the literal-absence limb is already satisfied by the defect's spelling, and (ii) a `|`-splitter reads
column 4 as the entry command and finds `exit 2` there. The fixture seat found (ii) independently
(`ExecC1Fixtures.md` §4.2: *"Any counter that parses registry rows by raw `|` will read `gate\|probe` as the
single choice `gate`"*) and fixed it **in the stand-in** — the frozen E13 text still only says "not the literal
`gate|probe`". A whole-row search for both tokens is also satisfiable from the wrong cell: appending
`could-not-evaluate` to the write-scope cell makes `exit2=True cne=True => pass=True` while the cell-aware
check stays red. And a second conforming row under any other heading makes an exists-check pass while the
registry row is unchanged (`rows=2`).

### 3.4 E14 / E9: fail-closed cannot be established by spelling (K4, K5)

```
$ python3 -c "open('.git/index','w').write('CORRUPT-INDEX')"   # fixture repo, toplevel verified
$ git -C . status --porcelain; echo rc=$?
fatal: .git/index: index file smaller than expected
rc=128
$ bash quiesce-demo.sh .
r36-shape: status-dirty=0        # 2>/dev/null | count_lines, porcelain:-0
spaced-redirect: status-dirty=0  # 2> /dev/null   (token not contiguous)
merged-stream: status-dirty=0    # >/dev/null 2>&1 (no token at all)
fail-closed: status-read=failed
```

`count_lines` (`r36-closure.sh:294`) maps an empty stream to `"0"`, so `${porcelain:-0}` is only decoration; a
spaced or merged redirect reaches the same `0` without either hunted token. The predicate's intended semantics
("a git-status read that fails is red") is only observable by running the limb on a fixture whose status read
fails — which the fixtures seat already built (§3 of its receipt) and which E14 should *be*. Separately, the
scratch-root limb is computed but not part of the verdict (`r36-closure.sh:469` vs `:481-483`), so a missing
root reads "0 leftovers".

## 4. Required amendments (P0 before data; P1 recommended)

All are append-only: file as `.ufo/waves/round-37/claims-erratum-2.md` (and keep `claims.json` untouched), or
land as the instrument's documented limbs where the erratum points at them.

**P0-1 — D4/D3 identity and binding (K1, K9, K10).**
- Claim text: replace "close the six routed defects D1-D6" and "D1-D6 closed" with "E10–E14 close D1, D2, D4,
  D5, D6 by instrument; D3 is carried by the round-37 lesson mistake row and the round's dispatch order and is
  not instrumented".
- E12 limbs: (i) a line in the round-37 SCORECARD section labels `c20300df…` `anchor ancestor`; (ii) the stale
  literal appears nowhere in that section **after normalization** (strip backticks/emphasis, join wrapped
  lines, ignore fenced code; section = `## Round 37 result …` closed by the next `## `); (iii) **for every**
  `Final lane commit:` label naming `e666d902` in `SCORECARD.md` and in `corpus/lessons/round-36.md`, the same
  line or its immediate successor carries `anchor ancestor`; (iv) mutant: round-37 section clean +
  `SCORECARD.md:1492` bare → **red** (this is the currently planned final state, so it must be red, not green).
- Kill rule: drop the section scoping from the stale-label limb (file-wide, normalized).
- Note: E12's required hash (`c20300df`) is not the mislabeled hash (`e666d902`); both statements are needed and
  they are compatible (label the r36 head for round-37's ancestry, relabel the intermediate ancestor at its
  site). In-place relabel of `:1492`/lesson:3 (or an adjacent appended correction line under the same section)
  is the smallest change; do not rely on M37-3 alone — a mistake row records, it does not relabel.

**P0-2 — E10 receipt genuineness (K2, K7).**
Limbs (a) header == sha256 of the **export's** `corpus/instruments/r37-closure.sh`; (b) ids E1..E14 exactly
once, each payload `closed=1`, no `closed=0`; (c) the 13 non-E10 payload strings byte-equal this run's payloads
for those ids; (d) the selftest section passes the r36-style judge (case + detail + `verdict=pass` +
`mutants=n/n`, forged summary/caselines/detail-free rejected); (e) `export-ref=<P>` with P an ancestor of the
checked ref and `git diff --name-only P <checked>` == the receipt path; (f) mutants: digest-correct receipt with
one payload edited, and one case line forged → red, naming the limb. Print `export-ref=` and the recomputed
payload block in the run header (the r36 suite already prints the ref and digest).

**P0-3 — E13 row semantics (K3).**
Exactly one row whose rendered first cell is `r36-closure.sh` across all `## …Gates & probes registry…`
sections (duplicate = red, naming both line numbers); rendered type cell ∈ {`gate`,`probe`} after escaping;
rendered verdict-map cell (column 4) contains an explicit `exit 2 … could-not-evaluate` mapping; mutants:
escaped pipe, duplicate row in another section, tokens placed only in the entry-command/write-scope cell.

**P0-4 — E14 behavioral, E9 root fail-closed (K4, K5).**
E14 = the suite's own quiescence status limb executed on the corrupt-index fixture must be red
(`status-read=failed`), plus the scoped regex `git[^|]*status[^|]*2>/dev/null` (space variants rejected; no
contiguous-token-only test); mutants: spaced redirect, merged stream, corrupt index. E9's closed condition adds
`scratch-root=present` on the default path, and a failed status read is red (never 0). Build both mutant
strings by concatenation so the suite bytes never contain the hunted literals (H1).

**P0-5 — red attribution (K6).**
The red run prints `open=<ids>`; at `a23dc478` the set must contain E10, E11, E12, E13, E14 (each
`closed=0`); at `cc692008` require `closed<14/14` with the still-open carried ids named. The E13 mutant must
be the committed escaped-pipe row.

**P1 — E11 wording (K8).** Recompute the absence at the export ref and at `a23dc478` in the same check; accept
only a retraction verb bound to the exact path; reject a line asserting presence. P1 — normalise E1's window
risk (H3) by keeping ≥5 lines between `:1492` and the appended block's first 40-hex.

## 5. Attacks the frozen predicate/kill rule does defeat (so the judge does not over-correct)

- **Dirty-worktree forgery** (edit the suite uncommitted, print a fake 14/14): killed by `git status --porcelain`
  non-empty and by E9 limb (d) head-match, provided E10 hashes the export's suite bytes (P0-2(a)); state the
  export-bytes requirement.
- **Stale-suite digest** (receipt header matches an older suite): defeated when the header is compared to the
  export's suite bytes — a different suite file has a different digest. It only survives if E10 hashes the live
  suite; P0-2(a) closes that.
- **Constant-green stub checks**: a stub returning closed=1 unconditionally makes the old exports 14/14 and
  kills the required reds; the two reds are load-bearing here (subject to K6).
- **In-section stale label**: the E12 absence limb does catch `Final lane commit: e666d902` placed inside the
  round-37 section (the fixtures seat's `e12-stale` proves it). The hole is only the *outside* placement.
- **E11 false presence claim**: *if* the absence is recomputed, an entry asserting the path exists is red; only
  a non-asserting, non-retracting sentence survives (P1).
- **D2's append-only mechanism**: a correction bullet in the round-37 entry is the right form; no rewrite of
  `LOG.md:1665` is needed or desirable.

## 6. Impacted axes and limits

Impacted: **depth:verifiability** (primary — C1's instrument and its kill rule; D1, D4, D5, D6, and the D3
overclaim), with a knock-on for the round's own claim identity (`after` says D1–D6 closed). No coverage or
density claim is touched. The `depth:verifiability` obligation stays active after this round regardless.

Limits of this review: the r37 suite does not exist at this read, so no r37 bytes were executed; the attacks
target the frozen measurable wording, the committed defect sites, and the wave's own planned stand-in/drafts.
The two "shape" claims about a future implementation (E10 forging, E14 evasion) are demonstrated against a
stand-in and against r36's own code, not against r37 bytes; a builder who implements the P0 limbs closes them.
No lane file was edited; this receipt is the only lane write.
