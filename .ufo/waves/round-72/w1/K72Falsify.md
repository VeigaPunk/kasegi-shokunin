# K72Falsify — round 72 attempt 1: falsification of C1 (derive-gate write-root/realpath) and C2 (F50 Bugzilla REST on S107)

Seat: K72Falsify (leaf, read-only). Scratch: /fast/scratch/hyaku/kasegi-r72/K72Falsify (removed at yield). No lane or fleet file written; no git mutation in the fleet repo.

## Identities measured

| item | measured | source of comparison |
|---|---|---|
| base gate `a34ce4c:corpus/instruments/figure-audit.py` | `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603` | matches claims C1 `before_values.measured_against` |
| counter `derive-head-census.py` at a34ce4c and dd9f55e | `255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52` | matches claims C1 counter and control receipt header |
| committed candidate `dd9f55e` (figure-audit.py last changed in `123796a`) | `4f59bda47eab2f93d54ccc7abe6256a878db5cbee98684d9d110043d91f9d221` | matches `.ufo/waves/round-72/candidate-sha256.txt` in 123796a |
| frozen candidate named in the round brief | `b146c81a…` | **not reproducible**: no `figure-audit.py` at a34ce4c, 123796a or dd9f55e has that sha (`git show <c>:corpus/instruments/figure-audit.py \| sha256sum`); the lane and fleet trees were clean (`git status --short` empty) and no copy with that sha was found in scratch |

Finding 0 (identity): the candidate the brief freezes (`b146c81a`) is not a committed or present byte string. The bytes I measured are the committed `4f59bda4`, which the round's own `candidate-sha256.txt` records. The brief says the difference is one comment line; I could not verify that and do not rely on it. `claims.json` itself pins no gate sha (only the counter's sha is recorded, and only as "recorded in controls/…"), so the C1 phrase "the measured candidate gate" does not name bytes. Verdict on this item: **WEAKENED**.

## C1 — derive-gate write-root / realpath repair

### Finding 1 — C1 do-nothing control reproduces (item 2)

Commands (cwd = scratch lane clone at a34ce4c; gate and counter copied into scratch, `TMPDIR` in scratch):

    TMPDIR=$S/census-base python3 $S/base-run/instruments/derive-head-census.py --gate $S/base-run/instruments/figure-audit.py --instruments $S/base-run/instruments

Measured output (EXIT=1), identical line-for-line to `controls/c1-census-donothing-r72.txt` from `READMITTED-ROW head=capture-binding-check.py flag=--scratch` through `EXIT=1` (19 `READMITTED-ROW` lines, `CENSUS heads=45 write_class_pairs=5 READMITTED=19`, `ALIAS-PROBE verdict=admitted rc=1 `, `POSITIVE admitted=2/2`, `CENSUS-RESULT defect`). `diff` of the two line sets (filtered on the receipt's line prefixes) is empty.

Base selftest (`cd lane; TMPDIR=… python3 corpus/instruments/figure-audit.py --selftest`): EXIT=0, `selftest cases=106 failures=0`, 106 `selftest case=` lines. Receipt value `cases=106 failures=0` reproduces. HOLDS.

### Finding 2 — C1 after_predicate fails on the do-nothing control (item 3)

Measured on the base gate (above) every clause of the C1 after_predicate that is required fails:

- census exit: 1 (predicate requires 0);
- `READMITTED=19` (predicate requires `READMITTED=0`), with 19 `READMITTED-ROW` lines (predicate forbids any);
- `ALIAS-PROBE verdict=admitted rc=1` (predicate requires `refused`);
- `CENSUS-RESULT defect` (predicate requires `ok`);
- selftest `cases=106` (predicate requires `cases >= 107`).

A base-identical gate fails the predicate. HOLDS.

Blanket refusal control (extra, mutant m2 = candidate with `python_head_ok` returning `False` as its first statement, scratch copy): census `READMITTED=0`, `ALIAS-PROBE verdict=refused`, `POSITIVE admitted=0/2`, `CENSUS-RESULT defect`, EXIT=1; selftest `cases=110 failures=13` (e.g. `selftest case=python-inside-admitted exit=2 want=0 verdict=fail`). The predicate fails on POSITIVE and on selftest failures, as the kill rule's "blanket-refusal gate is not a repair" intends. HOLDS.

### Finding 3 — C1 after_predicate holds on the committed candidate (4f59bda4, measured at dd9f55e)

    TMPDIR=$S/census-cand python3 corpus/instruments/derive-head-census.py   (cwd = lane at dd9f55e)
    CENSUS heads=45 write_class_pairs=5 READMITTED=0
    ALIAS-PROBE verdict=refused rc=2 FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
    POSITIVE admitted=2/2
    CENSUS-RESULT ok
    EXIT=0

    python3 corpus/instruments/figure-audit.py --selftest  ->  EXIT=0, 110 `selftest case=` lines,
    selftest cases=110 failures=0, and python-work-global-refused / python-scratch-global-refused /
    python-work-equals-refused / python-work-abbrev-refused all `verdict=pass`.

No `READMITTED-ROW` line. `cases=110 >= 107`. HOLDS on 4f59bda4 (see Finding 0 for the unreproduced frozen sha).

### Finding 4 — the C1 predicate's literal "exactly" is not satisfied by the census output as printed (item 1)

Quoted predicate: "prints exactly `READMITTED=0`, `ALIAS-PROBE verdict=refused`, `POSITIVE admitted=2/2`, `CENSUS-RESULT ok`". The measured lines are `CENSUS heads=45 write_class_pairs=5 READMITTED=0` and `ALIAS-PROBE verdict=refused rc=2 FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe`. `READMITTED=0` and `ALIAS-PROBE verdict=refused` occur as substrings, not as whole lines. A counter cannot re-derive "exactly" from these lines without a stated match rule. Verdict: **WEAKENED** (the values are present and correct; the match rule is missing).

### Finding 5 — C1 kill-rule clause "any named literal differs at the measured commit" (item 1)

"the measured commit" is not named in claims.json; the candidate was measured at `dd9f55e` (and the frozen claim says `87d84a2` as lane tip, which is the base). Verdict: **WEAKENED** (unnamed commit; "any named literal" is enumerated only by the predicate text).

### Finding 6 — C1 kill-rule clause "(including any pre-existing admission case newly refused)" (item 1)

Universal, not enumerated. What the selftest actually pins: 14 `run_case(..., 0, …)` admission cases in figure-audit.py (fixture heads `ok.py`, plus per-script `--root`/`--json` cases). Mutant m1 (candidate with `--root` added to `PY_DENIED_ANY`, scratch): census `POSITIVE admitted=1/2`, `CENSUS-RESULT defect`; selftest `cases=110 failures=1`, `selftest case=python-per-script-root-admitted exit=2 want=0 verdict=fail`. So the selftest does catch one newly refused pre-existing admission. Whether it catches every one is not stated or measured. Verdict: **WEAKENED** (holds for the cases pinned, universal not enumerated).

### Finding 7 — C1 target "denies every write-class option a head declares" is weakened by the census's read surface (item 1 universal)

`derive-head-census.py` reads declarations only through `add_argument(...)` literals (`declared_options`). 39 python heads contain `add_argument`; 28 heads contain `sys.argv` or `getopt` text (`grep -l 'sys\.argv\|getopt'`), so argv-parsed declarations are outside the census's read surface. Concrete instance on shipped bytes: `claim-package-selftest.py:591  elif arg == "--work" and i + 1 < len(args):` (not an add_argument). It is harmless today because `--work` is in the global `PY_DENIED_ANY`.

Fixture (mutant m3 = candidate + head `corpus/instruments/zz-url.py` that hand-parses `--url` and writes `zz-fetched.txt`, plus `"zz-url.py": (),` added to `PY_SCRIPT_CENSUS`, scratch copy):

    census: CENSUS heads=46 write_class_pairs=5 READMITTED=0   CENSUS-RESULT ok   EXIT=0
    selftest: selftest cases=110 failures=0   EXIT=0
    derive `python3 corpus/instruments/zz-url.py --url http://example.invalid/x`: derive ran,
      zz-fetched.txt written with the URL; figure-audit exit 1 only from a stale figure value
      (`FIG probe recorded=0 derived=fetched http://example.invalid/x want=0 stale`), not from a refusal.

So the gate admits a write-class `--url` for a head the census calls clean. On the shipped bytes this does not occur: `grep` finds `--url` declared only in `capture-source.py:123` (add_argument) and the gate itself. The claim's universal "every write-class option a head declares" is therefore HOLDS on the shipped tree and **WEAKENED** as a predicate, because the predicate (`READMITTED=0`) cannot see hand-parsed declarations. Recommendation for the lane (not repaired here): census should also AST-read string-literal `--flag` comparisons, or the claim should scope "declares" to add_argument.

### Finding 8 — C1 alias probe is one shape

The ALIAS probe checks one fixture shape (in-directory symlink `ok.py` → `gate-quote-audit.py`, argv `--json out/alias.json`). The candidate's `os.path.realpath` keying refuses it (`rc=2`). I did not test further shapes (hardlink, symlink outside `corpus/instruments`); the source reads as refusing both (realpath basename not in census; `startswith(base + os.sep)` check). Not measured: **untested beyond the probe**.

## C2 — F50 Bugzilla REST on S107

### Finding 9 — C2 before values reproduce (item 2 analogue)

On the base lane (a34ce4c), measured:

    FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106
    entries=52 pass=52 exit=0
    records=85 bound=85 unbound=0   (EXIT=0; orphan S040-live.txt declared)
    knowledge-expected: 89 lines / 87 rows;  knowledge files 87

Matches `controls/c2-base-counters-r72.txt` and the claim's `before_values`. HOLDS.

### Finding 10 — C2 after values hold on the committed tree (dd9f55e)

    FRONTIER-CENSUS rows=50 admitted=50 closed=50 problem-rows=0 registry=107
    FRONTIER-PASS F50 ids=S107
    PASS     F50  knowledge/bugzilla-rest-api-bug-endpoints.md ids=S107 exit=0
    entries=53 pass=53 exit=0                                   (EXIT=0)
    records=86 bound=86 unbound=0                              (EXIT=0; orphan S040-live.txt declared)
    knowledge-expected: 90 lines / 88 rows;  knowledge files 88;  set(knowledge-expected) == set(files): equal
    scripts/sources-census.sh validate kasegi --root /home/vgpnk/Projects/shokunin  -> EXIT=0 (6 W04 warnings, `kasegi ok …`)

HOLDS for the numeric predicate values. Two caveats in Findings 12 and 13.

### Finding 11 — C2 do-nothing control: copy S107 into the capture directory only (item 4)

Fixture: a34ce4c plus `corpus/source-snapshots/round-72/S107.txt` (bytes from dd9f55e), nothing else (no manifest record, no README row, no SOURCES row, no knowledge entry). Measured:

    frontier-recheck-count:  FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106;  entries=52 pass=52 exit=0
    capture-binding-check:   FAIL rule=missing-manifest dir=round-72
                             records=85 bound=85 unbound=0           (EXIT=1)
    knowledge-expected:      89 / 87;  knowledge files 87

Why: `frontier-recheck-count.py` enumerates rows from `corpus/README.md` and registry ids from `corpus/SOURCES.md`, and neither changed, so every frontier value stays at the base value. `capture-binding-check.py` counts only manifest `sources[]` records, so the orphan capture is not counted in `records=`; it fails rule A (`missing-manifest`) and exits 1 while its summary still says `unbound=0`.

Answer to item 4: the copy-only control meets **none** of the eight C2 after values (rows 49≠50, registry 106≠107, entries 52≠53, capture bound 85≠86, knowledge 89/87≠90/88, files 87≠88). Its only deviation that a predicate can see is the capture-binding exit code (1≠0). Verdict on that clause: HOLDS (predicate fails on the control) — but see Finding 13 for why the kill rule does not name it.

### Finding 12 — C2 kill-rule vs after-predicate contradiction (item 5)

Quoted kill rule: "C2 FAILS if … capture-binding reports an unbound record".
Quoted after predicate: "capture `bound=86 unbound=0` with exit 0".

The copy-only control (Finding 11) gives `unbound=0` and exit 1. The predicate fails (exit and `bound=85`), while no kill condition fires (no unbound record is reported). So a C2 verdict can be "predicate failed, kill rule not fired", and the claim's two clauses are not complements. Verdict: **FALSIFIED as a consistency statement** (the kill rule is narrower than its predicate). The same gap applies to the `sort -c` clause in Finding 14.

### Finding 13 — C2 "knowledge-expected … `sort -c` clean" is locale-dependent and not in the counter command (item 1)

Counter command (claims.json `counter.command`) lists `wc -l`, `grep -vc '^#'`, `ls corpus/knowledge/*.md | wc -l` and sources-census. It contains no `sort`. Measured `sort -c` on `corpus/instruments/knowledge-expected.txt`:

    LANG=en_US.UTF-8 (host default), full file:  sort: …knowledge-expected.txt:3: disorder: corpus/knowledge/ai-assisted-finding-validation.md   EXIT=1
    LANG=en_US.UTF-8, body (grep -v '^#'):       sort: …:34: disorder: corpus/knowledge/evidence-dir.md                                   EXIT=1
    LC_ALL=C, full file:                          EXIT=0
    LC_ALL=C, body:                               EXIT=0

The clause holds only under `LC_ALL=C`. Verdict: **WEAKENED** (not re-derivable from the listed command; fails under the host default locale).

### Finding 14 — C2 "knowledge-expected drifts from the file set" is not in the counter command (item 1)

The counter command checks counts only (90, 88, 88). A same-count rename would not change any counted value. My own set comparison (`grep -v '^#' | awk '{print $2}'` vs `ls corpus/knowledge/*.md`) is equal (`SET-EQUAL`) on dd9f55e, so the shipped bytes hold, but the kill clause is not re-derivable from the listed command. Verdict: **WEAKENED**.

### Finding 15 — C2 kill-rule "any F50 row, entry or registry row … duplicated" (item 1)

A duplicate `| S107 |` line appended to SOURCES.md (scratch copy, still 2 rows) gives `FRONTIER-CENSUS rows=50 admitted=50 closed=50 problem-rows=0 registry=107` and `entries=53 pass=53 exit=0` (EXIT=0), because `frontier-recheck-count.py` builds the registry as `set(REGISTRY_ROW.findall(...))`. The counter therefore does not see a duplicated registry row. In my placement (row appended after the Registry section), `sources-census.sh validate --file <copy>` returns exit 1 with `E12 S107 row outside Registry section`; the E03 duplicate-id code is not exercised by that placement. So the duplicate-registry limb is caught only by the out-of-repo sources-census script (fleet repo `scripts/sources-census.sh`, tracked at the fleet root). Verdict: **WEAKENED**.

Duplicated F50 README row: not measured; the `rows=50` exact predicate would catch it (rows=51).

### Finding 16 — C2 kill-rule "any quote in the entry is not located in the capture" (item 1, universal)

Not in the listed counter command, but enforced through the entry's `recheck:` line (`source-recheck.py --manifest … --source S107`), which `frontier-recheck-count.py` executes (PASS F50 exit=0). Independent measurement: all 29 double-quoted spans of length ≥3 in `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` occur in `corpus/source-snapshots/round-72/S107.txt` after whitespace and curly-quote normalization (`MISSING: 0`). Verdict: **HOLDS** on the shipped bytes; the clause is re-derivable only through the recheck line, which the claim should name.

### Finding 17 — C2 frozen target overclaims content the entry itself disclaims (item 1; target)

Quoted claim target: "the api_key and mandatory-field contract, the security-group restriction that keeps a report private".

The entry (committed in 123796a) says:
- line 18: "so this entry does not list which create parameters are required" (mandatory-field contract not delivered);
- line 48: "The api_key clause of this round's frozen C2 target is therefore not grounded in S107";
- line 49: "a security-group rule that keeps a report private. The capture has no sentence naming security".

Measured: `grep -ci secur …S107.txt` → 0; `grep -i 'api_key\|api key' …S107.txt` → no matches. The predicate does not test these, so the counters still pass, but the frozen target text is false for three of its four named components. Verdict: **FALSIFIED** (target text), HOLDS (predicate values).

### Finding 18 — C2 sources-census clause depends on the fleet working tree (item 1)

`sources-census.sh validate kasegi --root /home/vgpnk/Projects/shokunin` reads `kasegi-shokunin/corpus/SOURCES.md` from the fleet root's working tree, not from a committed revision. It returned EXIT=0 (`kasegi ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`). That working tree was clean at HEAD dd9f55e when measured. Verdict: **WEAKENED** against "re-derive from committed bytes" (the script is tracked in the fleet repo, so the command is reproducible, but its input is not pinned to a commit).

## Selftest count (item 6)

Candidate (4f59bda4): `selftest cases=110 failures=0`, EXIT=0, 110 case lines. Base: `cases=106 failures=0`. The claim's `cases >= 107` holds for the candidate and fails for the base. HOLDS.

## Network

`source-recheck.py` contains no `urllib|requests|curl|http.client|socket` calls (grep, empty). No URL was fetched by this seat.

## Summary table

| # | claim/clause | verdict |
|---|---|---|
| 0 | candidate identity (b146c81a unreproducible; measured 4f59bda4) | WEAKENED |
| 1 | C1 do-nothing reproduces receipt (READMITTED=19, alias admitted, POSITIVE 2/2, defect, selftest 106) | HOLDS |
| 2 | C1 predicate fails on do-nothing | HOLDS |
| 3 | C1 candidate: READMITTED=0, alias refused, POSITIVE 2/2, ok, selftest 110/0 | HOLDS (on 4f59bda4) |
| 4 | C1 "prints exactly" match rule | WEAKENED |
| 5 | C1 kill "at the measured commit" unnamed | WEAKENED |
| 6 | C1 kill "any pre-existing admission case" | WEAKENED (one case shown caught) |
| 7 | C1 target "every write-class option a head declares" (add_argument-only census) | WEAKENED (HOLDS on shipped bytes) |
| 8 | C1 alias probe shape coverage | not measured beyond one shape |
| 9 | C2 before values | HOLDS |
| 10 | C2 after values | HOLDS |
| 11 | C2 copy-only control meets none of the after values | HOLDS (predicate fails, via exit 1 only) |
| 12 | C2 kill rule vs predicate ("unbound record" vs "unbound=0 with exit 0") | FALSIFIED (not complementary) |
| 13 | C2 "sort -c clean" | WEAKENED (locale; not in command) |
| 14 | C2 "knowledge-expected drifts from the file set" | WEAKENED |
| 15 | C2 duplicated registry row | WEAKENED (only sources-census catches it) |
| 16 | C2 "every quote located in the capture" | HOLDS (29/29, via recheck line) |
| 17 | C2 target: api_key / mandatory-field / security-group | FALSIFIED (target text) |
| 18 | C2 sources-census reads fleet working tree | WEAKENED |
| 19 | selftest count >= 107 | HOLDS |

## Commands run (exact)

    git -C <lane> clone --shared ... ; git checkout a34ce4c | dd9f55e | (scratch only)
    git show a34ce4c:corpus/instruments/figure-audit.py | sha256sum        -> 182f4ef7…
    git show 123796a|dd9f55e:corpus/instruments/figure-audit.py | sha256sum -> 4f59bda4…
    TMPDIR=… python3 <base-copy>/derive-head-census.py --gate … --instruments …   (base, EXIT=1)
    TMPDIR=… python3 corpus/instruments/derive-head-census.py                       (cand, EXIT=0)
    python3 corpus/instruments/figure-audit.py --selftest                           (base 106/0; cand 110/0; m1 110/1; m2 110/13; m3 110/0)
    python3 corpus/instruments/frontier-recheck-count.py ; capture-binding-check.py ; wc/grep/ls  (a34ce4c, dd9f55e, copy-only)
    bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate kasegi --root /home/vgpnk/Projects/shokunin
    bash …/sources-census.sh validate --file <copy>/corpus/SOURCES.md --today 2026-11-05   (duplicate row fixture)
    python3 (scratch-only) quote-location check of 29 spans
    derive via figure-audit.py --ledger <json> --root <mutant>   (m3)

Scratch edits were confined to clones and mutant copies under the seat's scratch tree; no lane file, fleet file, or receipt outside this report was written. Scratch removed at yield.

## Routed to the lane (not repaired here)

1. Census declaration reader: add string-literal `--flag` scanning (or scope the claim to add_argument) before C1 "every write-class option" is cited as complete (Finding 7).
2. C1 predicate: give a match rule for "exactly" and pin the gate by sha in claims.json (Findings 0, 4).
3. C2 counter command: add the `sort` locale (`LC_ALL=C sort -c` on the body) and a set comparison for knowledge-expected; name the recheck line for quotes; make the registry count fail on duplicate rows (Findings 13–16).
4. C2 kill rule: add "capture-binding exits nonzero" and "sort -c fails" so the kill rule covers the predicate (Finding 12).
5. C2 target: remove or narrow "api_key", "mandatory-field contract", "security-group restriction" to what S107 supports (Finding 17).

Round verdict under falsification: C1 holds on the committed gate 4f59bda4 (the do-nothing base control fails its predicate and the blanket-refusal mutant fails it too), but its universal "every write-class option a head declares" is weakened by an add_argument-only census, its frozen b146c81a gate is unreproducible, and its "exactly" and "at the measured commit" clauses are unenumerated; C2's numeric after values hold, but its kill rule is not the complement of its predicate, its sort -c clause is locale-dependent, and its target names api_key, mandatory-field and security-group content that the entry itself disclaims.
