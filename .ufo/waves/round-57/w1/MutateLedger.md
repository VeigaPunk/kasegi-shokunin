# MutateLedger — verdict: the figure-audit comparison limbs ARE load-bearing for C1 (3/3 required mutants killed), but two of six probe limbs SURVIVE every detector the instrument owns (m4 selftest case-drop, m6 read-only-gate removal); the green audit over the unmodified ledger is a near-dead limb for comparison defects (only m2 moves it).

seat: MutateLedger (mutation-tester) · wave: kasegi r57 w1 · axis: depth:verifiability
scratch: `/fast/scratch/hyaku/kasegi-r57/MutateLedger` (created, then deleted; see §9)
lane root L = `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only; instrument and ledger never edited)
claims read first: `L/.ufo/waves/round-57/claims.json` (C1, frozen; predicates/kill rules unchanged by this seat)

## 0. Tooling

No tool was installed or upgraded this seat (pacman paused host-wide; nothing needed). Versions used, from
`python3 --version; git --version; bash --version | head -1; sed --version | head -1` (cwd=L, exit 0):

```
Python 3.14.8
git version 2.56.0
GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
sed 0.1.1
```

## 1. The instrument's interface (read before mutating)

`L/corpus/instruments/figure-audit.py:186-197` — `main()`: `--selftest` short-circuits to `selftest()`
(`:187-188`); otherwise defaults `ledger = corpus/instruments/figure-audit-ledger.json` (`:189`) and `root = "."`
(`:190`), then `--ledger PATH` / `--root DIR` override (`:191-197`). So a mutant copy is exercised as
`python3 <S>/mut/<m>.py --ledger <S>/mut/<ledger>.json` run with **cwd=L**, which is what every run below does.

Behaviour-bearing sites (`grep -n`, cwd=L):

```
75: def check_read_only(cmd):
81:     return head.startswith(READ_ONLY_HEADS)
108:             stale += 1
111:         if derived == str(ent["want"]):
115:             stale += 1
171:     run_case("ok-ledger", 0, SELFTEST_LEDGER_OK)
172:     run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)
173:     run_case("derive-fails-fail-closed", 1, SELFTEST_LEDGER_FAILS)
174:     run_case("token-boundary-34-vs-340", 1, SELFTEST_LEDGER_TOKEN)
175:     run_case("unreadable-ledger-exit-2", 2, None, broken=True)
```

## 2. Pristine baseline (byte-identical copy) — the detector's own numbers

```
cp L/corpus/instruments/figure-audit.py          <S>/mut/fig-audit-pristine.py
cp L/corpus/instruments/figure-audit-ledger.json <S>/mut/figure-audit-ledger.json
```
```
sha256sum <S>/mut/fig-audit-pristine.py L/corpus/instruments/figure-audit.py
6f63581ec36f216267f803b26d4941e1882185d3db32b3ca77b3cee10696740b  /fast/scratch/.../mut/fig-audit-pristine.py
6f63581ec36f216267f803b26d4941e1882185d3db32b3ca77b3cee10696740b  .../kasegi-shokunin/corpus/instruments/figure-audit.py
sha256sum <S>/mut/figure-audit-ledger.json L/corpus/instruments/figure-audit-ledger.json
94d8ac9b48e1d96d6579f622feed53a4a53cb3e92319e6d7521716bcee5602cd  /fast/scratch/.../mut/figure-audit-ledger.json
94d8ac9b48e1d96d6579f622feed53a4a53cb3e92319e6d7521716bcee5602cd  .../kasegi-shokunin/corpus/instruments/figure-audit-ledger.json
```
Baseline detectors (cwd=L, `TMPDIR=<S>`) — **both green, so a mutant's red is attributable to the edit**:
(in the two `sha256sum` blocks above, long absolute paths are elided to `/fast/scratch/.../` and `.../kasegi-shokunin/`;
the 64-hex hashes are printed in full and unedited)

```
$ python3 <S>/mut/fig-audit-pristine.py --selftest | tail -1        # exit 0
selftest cases=5 failures=0
$ python3 <S>/mut/fig-audit-pristine.py --ledger <S>/mut/figure-audit-ledger.json | tail -1   # exit 0
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
```

## 3. The six one-limb mutants — exact before/after text

Each edit is exact-once. For m1/m2/m4/m6 the site string occurs once in the pristine copy; m3's single
`stale += 1` line is one of two occurrences of that shorter string in the file (`:108` and `:115`), so m3 is
anchored on the unique three-line block shown below rather than on the bare line. Verification, cwd=`<S>/mut`:

```
$ python3 - <<'PY'   # count anchors in fig-audit-pristine.py
...
m1/m2/m5 site count= 1
m3 site count= 2                      # bare '            stale += 1\n'
m4 site count= 1
m6 site count= 1
$ python3 -c '...'  # m3 three-line anchor
m3 multiline-anchor count = 1
m3b == m3 byte-identical (multiline anchor reproduces the line-115 deletion)
```

| id | limb | before (exact) | after (exact) |
|---|---|---|---|
| m1 | whole-value equality → substring test (`:111`) | `        if derived == str(ent["want"]):` | `        if str(ent["want"]) in derived:` |
| m2 | compares **recorded** instead of **derived** (`:111`) | `        if derived == str(ent["want"]):` | `        if str(ent["recorded"]) == str(ent["want"]):` |
| m3 | a stale figure no longer increments the stale count (`:115`, block anchor) | `        else:`<br>`            stale += 1`<br>`            print("FIG %s recorded=%s derived=%s want=%s stale" % (ent["id"], ent["recorded"], derived, ent["want"]))` | same block with the `stale += 1` line deleted |
| m4 | selftest case covering a stale figure disabled (`:172`) | `    run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)` | (line deleted) |
| m5 | comparison always true (extra) | `        if derived == str(ent["want"]):` | `        if True:` |
| m6 | read-only derive gate disabled (`:81`, extra) | `    return head.startswith(READ_ONLY_HEADS)` | `    return True` |

Reproduction commands (cwd=`<S>/mut`), each confirmed byte-identical to the graded mutant file:

```
sed -E 's/if derived == str\(ent\["want"\]\):/if str(ent["want"]) in derived:/'            "$P" > m1.sed.py
sed -E 's/if derived == str\(ent\["want"\]\):/if str(ent["recorded"]) == str(ent["want"]):/' "$P" > m2.sed.py
sed '115d' "$P" > m3.sed.py
sed '/run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)/d' "$P" > m4.sed.py
sed -E 's/if derived == str\(ent\["want"\]\):/if True:/'                                    "$P" > m5.sed.py
sed 's/return head.startswith(READ_ONLY_HEADS)/return True/'                                "$P" > m6.sed.py
# -> "m1 sed-reproduction byte-identical OK" ... "m6 sed-reproduction byte-identical OK" (all six)

sha256sum m?-figure-audit.py
44282f6d7a456d8eec4a4a00e3e729e9cb867cc78926a084093f08386cc67ad4  m1-figure-audit.py
3a000ebf2210c23958958885078b470eec04d6d6e67abbb5ad925bab638544a4  m2-figure-audit.py
7b3baa9cca3124e4aac9befdeaa338315ea57daa49cf46a78407f3da40229ed3  m3-figure-audit.py
8dfea40da17ef7e087cacacef8a0b323504acbd50aac4910b9f77247197ecff0  m4-figure-audit.py
5c1358ebee9556214120af67b04a191bec8826f8887d34e8971b9ba28f9ce5a2  m5-figure-audit.py
9888ad7ec891681f405876f5dca798df4d7a0650affed6bcf720ac751b9dbad8  m6-figure-audit.py
```

## 4. Mutant results — compile, `--selftest`, green audit (unmodified ledger)

Commands (cwd=L, `TMPDIR=<S>`, exit code is the left-hand command's):

```
for m in m1 m2 m3 m4 m5 m6; do python3 -m py_compile <S>/mut/$m-figure-audit.py; echo "$m py_compile exit=$?"; done
for m in pristine m1 m2 m3 m4 m5 m6; do python3 <S>/mut/$m-figure-audit.py --selftest | tail -1; echo "exit=${PIPESTATUS[0]}"; done
for m in pristine m1 m2 m3 m4 m5 m6; do python3 <S>/mut/$m-figure-audit.py --ledger <S>/mut/figure-audit-ledger.json | tail -1; echo "exit=${PIPESTATUS[0]}"; done
```

Printed output, verbatim (pristine row is the baseline from §2):

```
m1 py_compile exit=0   m2 exit=0   m3 exit=0   m4 exit=0   m5 exit=0   m6 exit=0

--- pristine  selftest cases=5 failures=0        exit=0
--- m1        selftest cases=5 failures=1        exit=1
--- m2        selftest cases=5 failures=2        exit=1
--- m3        selftest cases=5 failures=2        exit=1
--- m4        selftest cases=4 failures=0        exit=0
--- m5        selftest cases=5 failures=2        exit=1
--- m6        selftest cases=5 failures=0        exit=0

--- pristine  FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   exit=0
--- m1        FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   exit=0
--- m2        FIGURE-AUDIT figures=35 ok=31 stale=4 exit=1   exit=1
--- m3        FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   exit=0
--- m4        FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   exit=0
--- m5        FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   exit=0
--- m6        FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   exit=0
```

Which selftest case found each kill (from the per-case lines of the same `--selftest` runs):

```
m1 fails: case=token-boundary-34-vs-340
m2 fails: case=stale-literal, case=token-boundary-34-vs-340
m3 fails: case=stale-literal, case=token-boundary-34-vs-340
m5 fails: case=stale-literal, case=token-boundary-34-vs-340
m4: all pass — but cases dropped 5 -> 4
m6: all pass — cases=5, no case covers the read-only gate
```

### Mutant table

| id | exact edit | compile | `--selftest` | green audit (unmodified ledger) | verdict |
|---|---|---|---|---|---|
| m1 | `derived == str(ent["want"])` → `str(ent["want"]) in derived` | ok | `cases=5 failures=1`, exit 1 | `figures=35 ok=35 stale=0 exit=0`, exit 0 | **KILLED** (token-boundary case) |
| m2 | `derived == str(ent["want"])` → `str(ent["recorded"]) == str(ent["want"])` | ok | `cases=5 failures=2`, exit 1 | `figures=35 ok=31 stale=4 exit=1`, exit 1 | **KILLED** (stale-literal + token-boundary) |
| m3 | delete `stale += 1` at `:115` | ok | `cases=5 failures=2`, exit 1 | `figures=35 ok=35 stale=0 exit=0`, exit 0 | **KILLED** (stale-literal + token-boundary) |
| m4 | delete `run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)` at `:172` | ok | `cases=4 failures=0`, exit 0 | `figures=35 ok=35 stale=0 exit=0`, exit 0 | **SURVIVED** |
| m5 | `derived == str(ent["want"])` → `True` | ok | `cases=5 failures=2`, exit 1 | `figures=35 ok=35 stale=0 exit=0`, exit 0 | **KILLED** (stale-literal + token-boundary) |
| m6 | `return head.startswith(READ_ONLY_HEADS)` → `return True` | ok | `cases=5 failures=0`, exit 0 | `figures=35 ok=35 stale=0 exit=0`, exit 0 | **SURVIVED** |

Reading of the table, limb by limb:

- **m2 is the only mutant that moves the green audit.** Over the unmodified 35-figure ledger, `derived == want`
  is true for 31 entries; the 4 that turn stale under m2 are exactly the 4 entries whose `recorded` is prose
  rather than the bare literal (`capture-lines-s085`, `figure-audit-mentions-base-scorecard`,
  `census-fresh-literal-r55`, `fail-entry-records`; count verified: "entries with recorded != want: 4"). So the
  green run alone cannot separate a correct comparator from m1/m3/m5 — those are caught only by the selftest.
- **m3 is killed by the selftest, and would *additionally* be killed by C1's red-control clause**, because under
  m3 the red control still prints the stale line but exits 0: `red1` under m3 →
  `FIGURE-AUDIT figures=35 ok=34 stale=0 exit=0` with `FIG registry-rows-r56 ... stale` on stdout (see §5).
  That clause of C1's kill rule ("red control 1 ... exits 0" ⇒ C1 FAILS) is load-bearing precisely for m3.
- **m4 survives because the selftest grades its own case list.** The stale-figure semantics lose their only
  regression test, and the instrument still prints `failures=0` and exits 0. C1's kill rule pins
  "the selftest prints failures != 0 or exits != 0" only; it does not pin `cases=5`, although C1's `after`
  line does say "the selftest prints cases=5 failures=0 exit 0". Coverage finding, not a claim defect: the
  case *count* is stated in `after` but absent from `kill_rule`.
- **m6 survives every detector the instrument owns.** Disabling the read-only allow-list changes no green output
  and no selftest case. It is observable only by feeding a non-allow-listed derive (§6, `echo 34` → exit 2
  becomes exit 1 + a stale line). The property "the audit never runs a mutating command"
  (`figure-audit.py:25-30`, docstring: "the audit never runs a mutating command: entries are rejected whose
  derive lacks a read-only head") therefore has no regression test in the instrument.

## 5. Red controls per mutant — where m3 and m6 actually show

`red1` = ledger copy with `registry-rows-r56.want` `88 → 87`; `red2` = `fail-entry-records.derive` replaced by the
allow-listed constant `sed -n '1s/.*/34/p' corpus/README.md` (prints 34, want 33); `red2echo` = the literal
`echo 34` form. Commands: `python3 <S>/mut/<m>.py --ledger <S>/mut/red1-wrong-want-r57.json` etc., cwd=L.
`stale` column = number of stdout lines ending in `stale`.

```
pristine   red1      exit=1 stale=1 ids=['registry-rows-r56'] | FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
pristine   red2      exit=1 stale=1 ids=['fail-entry-records'] | FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
pristine   red2echo  exit=2 stale=0 ids=[]                     | (no summary; stderr only)
m1         red1      exit=1 stale=1 ids=['registry-rows-r56'] | figures=35 ok=34 stale=1 exit=1
m1         red2      exit=1 stale=1 ids=['fail-entry-records'] | figures=35 ok=34 stale=1 exit=1
m2         red1      exit=1 stale=5 ids=['capture-lines-s085','figure-audit-mentions-base-scorecard','census-fresh-literal-r55','fail-entry-records','registry-rows-r56'] | figures=35 ok=30 stale=5 exit=1
m2         red2      exit=1 stale=4 ids=['capture-lines-s085','figure-audit-mentions-base-scorecard','census-fresh-literal-r55','fail-entry-records'] | figures=35 ok=31 stale=4 exit=1
m2         red2echo  exit=2 stale=3 ids=['capture-lines-s085','figure-audit-mentions-base-scorecard','census-fresh-literal-r55']
m3         red1      exit=0 stale=1 ids=['registry-rows-r56'] | FIGURE-AUDIT figures=35 ok=34 stale=0 exit=0
m3         red2      exit=0 stale=1 ids=['fail-entry-records'] | FIGURE-AUDIT figures=35 ok=34 stale=0 exit=0
m3         red2echo  exit=2 stale=0
m4         red1      exit=1 stale=1 ids=['registry-rows-r56'] | figures=35 ok=34 stale=1 exit=1
m4         red2      exit=1 stale=1 ids=['fail-entry-records'] | figures=35 ok=34 stale=1 exit=1
m5         red1      exit=0 stale=0 ids=[]                     | FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
m5         red2      exit=0 stale=0 ids=[]                     | FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
m6         red1      exit=1 stale=1 ids=['registry-rows-r56'] | figures=35 ok=34 stale=1 exit=1
m6         red2      exit=1 stale=1 ids=['fail-entry-records'] | figures=35 ok=34 stale=1 exit=1
m6         red2echo  exit=1 stale=1 ids=['fail-entry-records'] | figures=35 ok=34 stale=1 exit=1   <-- m6's only visible trace
```

m2's five-stale `red1` run is a **false positive generator**: cwd=L over the unmodified ledger, m2 already
reports four stale entries, so a red control that prints ">=1 stale line on the right id" would be satisfied
for the wrong reason. This is the strongest argument that `figures=35 ok=35 stale=0` on the green run is part
of C1's detector and not decoration — m2 is the one mutant the green summary catches and the red lines alone
would not.

m1 escape probe (`<S>/mut/ledger-sub-probe.json`, one figure, `derive=cat <S>/mut/probe-340.txt` printing
`340`, `want=34`) — declared because m1 leaves the green ledger green: the substring limb really does break
the token boundary when a want is a proper substring of the derive.

```
pristine  FIG sub-probe recorded=34 derived=340 want=34 stale | FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1  exit=1
m1        FIG sub-probe recorded=34 derived=340 ok             | FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0  exit=0
```

## 6. Ledger mutants (C1's own red controls, reproduced on this host)

Script = the **unmodified** copy `<S>/mut/fig-audit-pristine.py`, cwd=L, `TMPDIR=<S>`. Ledger copies were built
with a `python3 -c` JSON edit of `<S>/mut/figure-audit-ledger.json` (never L's file).

**(a) `registry-rows-r56` want 88 → 87** — `--ledger <S>/mut/red1-wrong-want-r57.json`:

```
FIG registry-rows-r56 recorded=88 derived=88 want=87 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
exit=1
```
**Exit 1 as expected.** One stale line, on the named id only, `ok` drops 35→34: exactly C1's red-control-1
predicate, and it matches the committed `.ufo/waves/round-57/controls/c1-red-r57.txt:9-10` (RED 1 block,
opened at `:7`).

**(b) `fail-entry-records` derive → `echo 34`** (the seat spec's literal wording) —
`--ledger <S>/mut/red2-literal-echo34.json`:

```
exit=2
FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=fail-entry-records
```
**Exit 2, not 1.** Deviation from the seat spec's expectation, recorded as measured: `check_read_only()`
(`figure-audit.py:75-81`) rejects the non-allow-listed head `echo` before the comparison runs, so the instrument
fails *closed at the shape gate* (exit 2 UNAVAILABLE, no `FIGURE-AUDIT` summary line) rather than reaching the
stale comparison. A constant-echo derive can therefore only be expressed in an allow-listed form.

**(c) `fail-entry-records` derive → allow-listed constant 34**, `sed -n '1s/.*/34/p' corpus/README.md`
(`check_read_only(...) -> True` verified by importing the pristine module) —
`--ledger <S>/mut/red2-deriverepair-r57.json`:

```
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=34 want=33 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
exit=1
```
**Exit 1 as expected** — the derive-repair comparison limb does catch a constant-34 derive when the derive can
be expressed, and it prints the stale line on the named id only.

**(d) The committed instrument's own removal path**, i.e. the method `.ufo/waves/round-57/controls/c1-red-r57.txt`
used: mutate the *receipt* the derive reads. `sed -E 's/FAIL_entry_records=33/FAIL_entry_records=34/'` over
`L/.ufo/waves/round-53/controls/c2-counter-final-r53.txt` into `<S>/mut/receipts/c2-counter-final-r53.mut.txt`
(diff `1c1 < FAIL_entry_records=33 --- > FAIL_entry_records=34`), ledger derive re-pointed at the mutated copy:

```
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=34 want=33 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
exit=1
```
This is the host-portable form that actually reproduces C1's red-control-2 on this host (the committed derive
reads a committed receipt line, `L/.ufo/waves/round-53/controls/c2-counter-final-r53.txt:8`, and still prints 33
at rest: `grep -oE 'FAIL_entry_records=[0-9]+' … | head -1` → `FAIL_entry_records=33`). Under the mutants the same
control reads: m1 exit 1, m2 exit 1 (`ok=31 stale=4`), **m3 exit 0 (`stale=0`)**, m4 exit 1, m5 exit 0, m6 exit 1
— again m3/m5 are the limbs that would silently discharge a red control.

**(e) Both red controls combined** (`want=87` **and** constant-34 derive) — `red1red2-both.json`:

```
FIG fail-entry-records ... derived=34 want=33 stale
FIG registry-rows-r56 recorded=88 derived=88 want=87 stale
FIGURE-AUDIT figures=35 ok=33 stale=2 exit=1
exit=1
```
`stale` is a true count (2), not a boolean: m3's defect (no `stale += 1`) is the only mutant that would mask it.

## 7. Survivors

| id | survivor | why nothing in the instrument notices |
|---|---|---|
| m4 | selftest case `stale-literal` deleted | the selftest reports `cases=4 failures=0`, exit 0 — it grades the cases that remain. Only a case-count or case-name assertion would catch it; C1's `kill_rule` pins `failures`/exit, C1's `after` pins `cases=5` (so the *claim text* covers it, the *kill rule* does not). |
| m6 | `read_only` allow-list disabled | no selftest case feeds a non-allow-listed derive, and both green and red controls use allow-listed derives; caught only by the `echo 34` probe (exit 2 → exit 1). |

No other survivor: m1, m2, m3, m5 are killed by the selftest, and m2/m5 additionally flip the green summary
(m2 red, m5 green-but-blind on red controls).

## 8. Integrity / restoration

- The lane copies were never edited: `figure-audit.py` sha256 `6f63581e…96740b` and `figure-audit-ledger.json`
  sha256 `94d8ac9b…5602cd` re-read **after** all runs, both unchanged from their pre-run values (§2).
- `git -C L status --porcelain -- corpus/instruments/figure-audit.py corpus/instruments/figure-audit-ledger.json`
  → empty (the `M LOG.md`, `M SCORECARD.md`, `?? .ufo/waves/round-57/` entries in the full status are other
  seats' writes, not this seat's).
- Restoration evidence for the mutated scratch copy: the pristine copy is byte-identical to L
  (`restored/pristine check: pristine bytes identical to L -> True`), and every mutant was produced *from* that
  copy, so no mutant ever occupied a graded path. `<S>` is deleted at exit (§9); nothing persistent under L
  depends on it.
- No credential material read, written or echoed: every derive touched is a count/grep over corpus records.

## 9. Scratch disposition

`mkdir -p /fast/scratch/hyaku/kasegi-r57/MutateLedger` at start; all runs used `TMPDIR` inside it. After every
measured run above completed, `cd /tmp && rm -rf -- /fast/scratch/hyaku/kasegi-r57/MutateLedger` was executed;
`ls -d` on the path then printed `ls: cannot access '/fast/scratch/hyaku/kasegi-r57/MutateLedger': No such file or
directory` (exit 2). Sibling seat directories under `/fast/scratch/hyaku/kasegi-r57/` were left untouched.
No leftovers of this seat anywhere; no file created in `~/.local/bin` or in the fleet root.

## 10. Verdict line

**The figure-audit limbs under test are load-bearing for C1:** each of the three mandated comparison-limbs — whole-value equality (m1), derive-vs-want rather than recorded-vs-want (m2), and stale-count increment driving the exit (m3) — is killed by the committed selftest, and m2/m5 are additionally caught by C1's green summary, while m3/m5 are additionally caught by C1's "red control exits 0 ⇒ FAILS" clause; the two ledger mutants C1 names both turn the unmodified instrument red (exit 1) on this host, with the single deviation that the literal `echo 34` derive is rejected earlier at exit 2 by the read-only gate and needs an allow-listed form (or the receipt mutation C1's own control uses) to reach the comparison. Two probes SURVIVE every detector the instrument owns — m4 (deleting the stale-literal selftest case leaves `cases=4 failures=0 exit=0`) and m6 (disabling the read-only allow-list leaves green and selftest untouched) — so the selftest's case inventory and the read-only gate are *not* themselves load-bearing; C1's `after` line pins `cases=5` but its `kill_rule` does not, which is the one coverage gap this battery found. Reported as text only; the instrument, the ledger and the frozen claims were not modified.
