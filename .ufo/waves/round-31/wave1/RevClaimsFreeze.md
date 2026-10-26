# RevClaimsFreeze — Round-31 Frozen Claims Falsification Receipt

- **Seat:** `RevClaimsFreeze` (role: `reviewer`, leaf)
- **Answering model:** `google-antigravity/gemini-4-argon` (config route table; no model passed)
- **Lane base:** `b374febbb33ccadade78a787279707fd5d2e6e1d`
- **Claims freeze commit:** `738a77999a00efbca129cfccb28a481037f6241f`
- **Reviewed files (read-only):**
  - `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/claims.json`
  - `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/c1-controls/{before.txt,base-instrument-digests.txt,fake-counter.py,fake-counter-receipt.txt}`
  - `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/c2-controls/before.txt`
  - `/home/vgpnk/Projects/shokunin/.ufo/prompts/kasegi-round-31.md` (§2 lines 9–40, §9 lines 417–439)
  - `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` (Q1–Q10, R1–R15)
  - `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` (lines 20–79, 784–835)

---

## Summary Verdicts per Attack

| Attack | Question | Verdict | Summary |
|---|---|---|---|
| **(1)** | Is C1's target reachable by a do-nothing control? Run `fake-counter.py` and build a second cheap control. | **PASS (Unreachable; 1 tightening note on `kill_rule` line 25)** | Base bytes exit `2` (`No such file or directory`). `fake-counter.py` prints the 2 summary lines and exits `0`, but emits `0` `LIMB ` lines and is rejected by the **13-LIMB-line clause** and **closure hand re-derivation clause** (`claims.json:25`). Our second cheap control (`count-by-exit-no-compile` + `live-only-skip-mutant`) is rejected by **`CTL-nocompile` / `CTL-noop`** (`controls=3 rejected=1`, `exit=1`) and by the **`controls=3 rejected=3` / exit-0 kill-rule clause** (`claims.json:18,25,27`). |
| **(2)** | Universal clauses (`all`, `every`, `no harm`) in the predicate sentences without an enumerating command? | **PASS (0 unenumerated universals in `predicate_sentence`)** | `C1.predicate_sentence` (`claims.json:18`) and `C2.predicate_sentence` (`claims.json:37`) contain **0** occurrences of `all`, `every`, or `no harm`. In `C1.predicate_sentence`, `completeness` is a limb name (`RA-completeness`) and `each of which` binds the closed 3-control tuple enumerated by `limb-mutation-check.py`. Note: `C2.kill_rule` (`claims.json:47`) contains `"every programme claim (Q4)"`, which is human-reviewed over the single file `corpus/knowledge/vendor-third-party-finding-coordination.md`. |
| **(3)** | C2: can a junk-row + empty-entry commit meet any counter? | **YES for individual counters 1–5 (4/7 on 0-byte entry; 5/7 on 1-line stub); NO for the conjunctive C2 target** | A junk `S048` row (`kind=docs`) + `F15` README row + `0`-byte `vendor-third-party-finding-coordination.md` meets **Counters 1, 3, 4, and 5 (`sources-census.sh validate` exits `0` because `E11` only checks `[ -e ]`)**, and a 1-line `source: S048 ...` stub also meets **Counter 2** (`5/7`). However, **Counter 6 (`frontier-recheck-count.py`, `exit=1`)** and **Counter 7 (`source-recheck.py`, `exit=2`)** plus `C2.kill_rule` (Q1–Q10) deterministically reject it. |
| **(4)** | Does C1's `depth:verifiability` axis name the surface the round changes (§9)? | **Qualified YES (as `held 4` detector-soundness under `QUALITY.md` R7/R11/R13); NO as primary corpus citation-resolution** | **Yes** within the lane's 3-axis `SCORECARD.md` ontology (`depth:density`, `depth:verifiability`, `coverage`) because C1 does not merely re-score already-passing checks: on base `b374febbb`, `recheck-audit.py:350` (`RA-completeness`) is a **survivor** under `--selftest` (`exit=0`), `frontier-recheck-count.py` has no committed limb fixtures, and round 30's B2 fixture (`M30-1`) tripped B1 first. **No** if judged as a primary `SCORECARD.md:33-38` citation-resolvability move, which is why `score_after` must stay `"held 4"` with unchanged source-availability scores disclosed per `QUALITY.md` R7. |

---

## Attack (1): C1 Do-Nothing Control, `fake-counter.py`, and Second Cheap Control

### 1.1 Base Do-Nothing Control (`b374febbb33ccadade78a787279707fd5d2e6e1d`)
- At base bytes `b374febbb33ccadade78a787279707fd5d2e6e1d` (`.ufo/waves/round-31/c1-controls/before.txt:2-8`), neither `corpus/instruments/limb-mutation-check.py` nor `corpus/instruments/limb-ledger.json` exists; `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` exits `2`.
- **Rejecting kill-rule clause (`claims.json:25`):** `"Fails if any of: the counter is absent or exits non-zero; its output lacks the exact lines limbs=13 killed=13 survivors=0 and controls=3 rejected=3"`.

### 1.2 First Cheap Control: `c1-controls/fake-counter.py` (Executed)
Command and output:
```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/c1-controls/fake-counter.py; echo "fake_exit=$?"; python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/c1-controls/fake-counter.py | grep -c '^LIMB ' || true
controls=3 rejected=3
limbs=13 killed=13 survivors=0
fake_exit=0
0
```
- **Rejecting kill-rule clauses (`claims.json:25`):**
  1. **13-LIMB-line clause:** `"it prints fewer than 13 lines beginning LIMB  or any LIMB line shows live-result == mutant-result"` — `fake-counter.py` prints `0` lines matching `^LIMB ` (`0 < 13`).
  2. **Closure re-derivation clause:** `"OR the closure re-derives any one ledger patch by hand (apply the find/replace to a copy, run the row's kill command) and the result differs from the counter's LIMB line"` — `fake-counter.py` emits no `LIMB <id> live=... mutant=...` line for any ledger row.

### 1.3 Second Cheap Control: Built and Executed in Ephemeral `/tmp`
We constructed two variants of a second cheap control in `/tmp` (no lane writes) against base `corpus/instruments/source-recheck.py` (`33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`):
- **Cheap Control 2A (`count-by-exit-no-compile`):** Runs the live baseline (`live=0/y`), applies `find`/`replace` **without** `py_compile` or byte-equality (`invalid:noop`) checks, runs the kill command on the mutated file, and reports `verdict=killed` whenever `mutant_exit != 0` or the signal is absent — even when the mutant file fails to compile (`SyntaxError`).
- **Cheap Control 2B (`live-only-skip-mutant`):** Runs only the live baseline (`live=0/y`), skips the mutant run completely, and reports `mutant=1/n verdict=killed` for every row.

Command and output:
```text
$ python3 - <<'PY'
import py_compile, subprocess, tempfile, pathlib

inst_src = pathlib.Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py").read_text()

controls = [
    {"id": "CTL-noop", "find": "SCHEMA_VERSION = 1", "replace": "SCHEMA_VERSION = 1", "expect": "invalid:noop"},
    {"id": "CTL-nocompile", "find": "SCHEMA_VERSION = 1", "replace": "SCHEMA_VERSION = (", "expect": "invalid:nocompile"},
    {"id": "CTL-equivalent", "find": "SCHEMA_VERSION = 1", "replace": "SCHEMA_VERSION = int(1)", "expect": "survivor"},
]

with tempfile.TemporaryDirectory() as tmp:
    p = pathlib.Path(tmp) / "source-recheck.py"
    p.write_text(inst_src)
    live = subprocess.run(["python3", str(p), "--selftest"], capture_output=True, text=True)
    live_sig = "selftest cases=9 failures=0" in (live.stdout + live.stderr)
    print(f"# Cheap control 2A: runs live baseline ({live.returncode}/{'y' if live_sig else 'n'}), applies patch WITHOUT noop/py_compile check, counts any mutant exit != 0 as killed")
    rejected = 0
    for c in controls:
        p.write_text(inst_src.replace(c["find"], c["replace"], 1))
        mut = subprocess.run(["python3", str(p), "--selftest"], capture_output=True, text=True)
        mut_sig = "selftest cases=9 failures=0" in (mut.stdout + mut.stderr)
        verdict = "killed" if (mut.returncode != 0 or not mut_sig) else "survivor"
        ok = (verdict == c["expect"])
        if ok:
            rejected += 1
        print(f"CONTROL {c['id']} live={live.returncode}/{'y' if live_sig else 'n'} mutant={mut.returncode}/{'y' if mut_sig else 'n'} verdict={verdict} expected={c['expect']} ok={'y' if ok else 'n'}")
    print(f"controls={len(controls)} rejected={rejected}")
    print(f"cheap_2a_exit={0 if rejected == len(controls) else 1}")

    print("\n# Cheap control 2B: runs ONLY live baseline, skips mutant run, reports mutant=1/n verdict=killed for every row")
    rejected_2b = 0
    for c in controls:
        verdict = "killed"
        ok = (verdict == c["expect"])
        if ok:
            rejected_2b += 1
        print(f"CONTROL {c['id']} live={live.returncode}/{'y' if live_sig else 'n'} mutant=1/n verdict={verdict} expected={c['expect']} ok={'y' if ok else 'n'}")
    print(f"controls={len(controls)} rejected={rejected_2b}")
    print(f"cheap_2b_exit={0 if rejected_2b == len(controls) else 1}")
PY
# Cheap control 2A: runs live baseline (0/y), applies patch WITHOUT noop/py_compile check, counts any mutant exit != 0 as killed
CONTROL CTL-noop live=0/y mutant=0/y verdict=survivor expected=invalid:noop ok=n
CONTROL CTL-nocompile live=0/y mutant=1/n verdict=killed expected=invalid:nocompile ok=n
CONTROL CTL-equivalent live=0/y mutant=0/y verdict=survivor expected=survivor ok=y
controls=3 rejected=1
cheap_2a_exit=1

# Cheap control 2B: runs ONLY live baseline, skips mutant run, reports mutant=1/n verdict=killed for every row
CONTROL CTL-noop live=0/y mutant=1/n verdict=killed expected=invalid:noop ok=n
CONTROL CTL-nocompile live=0/y mutant=1/n verdict=killed expected=invalid:nocompile ok=n
CONTROL CTL-equivalent live=0/y mutant=1/n verdict=killed expected=survivor ok=n
controls=3 rejected=0
cheap_2b_exit=1
```

- **Which control and kill-rule clauses catch Cheap Control 2A and 2B:**
  1. **`CTL-nocompile` (`expect: "invalid:nocompile"`) and `CTL-noop` (`expect: "invalid:noop"`):** Under Cheap Control 2A, the syntax-broken patch `SCHEMA_VERSION = (` causes `python3 source-recheck.py --selftest` to exit `1` (`SyntaxError`), so a counter that omits `py_compile` misclassifies `CTL-nocompile` as `verdict=killed` (`ok=n`), and without the byte-equality check misclassifies `CTL-noop` as `verdict=survivor` (`ok=n`), printing `controls=3 rejected=1` (`cheap_2a_exit=1`). Under Cheap Control 2B, all three controls fail (`controls=3 rejected=0`, `cheap_2b_exit=1`).
  2. **Kill-rule summary & exit clauses (`claims.json:25`):** Rejects both because the counter exits `1` (non-zero) and lacks `controls=3 rejected=3`.
  3. **Kill-rule closure hand re-derivation clause (`claims.json:25`) + `predicate_sentence` compile requirement (`claims.json:18`):** Even if a malicious counter special-cased `controls` to print `controls=3 rejected=3`, `C1.predicate_sentence` (`claims.json:18`) requires `"an exact-once find/replace patch of the instrument bytes that still compiles"`, and `C1.kill_rule` (`claims.json:25`) re-derives ledger patches by hand (`"the closure re-derives any one ledger patch by hand ... and the result differs from the counter's LIMB line"`), which catches Cheap Control 2B on any limb whose real mutant exits `0/y` (such as `RA-completeness` on unmutated base `recheck-audit.py`, proven in §4 below).
  4. **Tightening recommendation for L1 (appended correction only if desired; never edit `claims.json`):** In `C1.kill_rule` (`claims.json:25`), the `LIMB ` line clause currently reads `"it prints fewer than 13 lines beginning LIMB  or any LIMB line shows live-result == mutant-result"`. Because `LIMB <id> live=0/y mutant=1/n verdict=invalid:nocompile` has `live-result != mutant-result`, closure hand re-derivation should also explicitly check `verdict=killed` on all 13 `LIMB ` lines and `python3 -m py_compile` on the patched copy, matching `C1.predicate_sentence` (`claims.json:18`).

---

## Attack (2): Universal Clauses in `predicate_sentence` Without an Enumerating Command

Command and output:
```text
$ python3 - <<'PY'
import json, re
d = json.load(open("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/claims.json"))
pat = re.compile(r"\b(all|every|complete|completeness|no harm|no-harm|each|any|none|zero|never)\b", re.I)
for c in d["claims"]:
    print(f"=== {c['id']} ===")
    for field in ("surface", "predicate_sentence", "kill_rule", "do_nothing_control"):
        val = c.get(field, "")
        matches = [(m.group(0), m.start()) for m in pat.finditer(val)]
        print(f"  {field}: matches={matches}")
PY
=== C1 ===
  surface: matches=[('each', 269)]
  predicate_sentence: matches=[('completeness', 233), ('each', 705)]
  kill_rule: matches=[('any', 9), ('zero', 52), ('any', 204), ('any', 254), ('any', 589)]
  do_nothing_control: matches=[('any', 343)]
=== C2 ===
  surface: matches=[]
  predicate_sentence: matches=[]
  kill_rule: matches=[('any', 9), ('any', 288), ('any', 348), ('every', 460)]
  do_nothing_control: matches=[]
```

- **Verdict:** **PASS.**
  - Neither `C1.predicate_sentence` (`claims.json:18`) nor `C2.predicate_sentence` (`claims.json:37`) contains `"all"`, `"every"`, or `"no harm"`.
  - In `C1.predicate_sentence` (`claims.json:18`), `completeness` is the proper name of one of the 13 enumerated limbs (`RA-completeness`), and `each of which` refers to the finite 3-element control set (`a no-op patch, a patch that does not compile, and a semantically equivalent patch`), enumerated by `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` (`controls=3 rejected=3`).
  - In `C2.predicate_sentence` (`claims.json:37`), every clause is an exact finite equality/delta paired with its counting command in `C2.counter_commands` (`claims.json:39-45`).
  - **Residual note on `C2.kill_rule` (`claims.json:47`):** Contains `"the entry does not name Microsoft as the stating party for every programme claim (Q4)"` and `"any assertion not exactly-once-or-anchored"`. The assertion clause is machine-enumerated by Counter 7 (`source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048`); the Q4 clause is in `kill_rule` (not `predicate_sentence`) and is verified by the non-author reviewer over the single bounded file `corpus/knowledge/vendor-third-party-finding-coordination.md`.

---

## Attack (3): C2 Junk-Row + Empty-Entry Control Against the 7 Counter Commands

We exported base commit `b374febbb33ccadade78a787279707fd5d2e6e1d` into an ephemeral `/tmp` directory (cleaned on exit) and tested two junk commits against all 7 `C2.counter_commands` (`claims.json:39-45`):
- **Case 3a:** Append `| F15 | Junk topic | admitted | ... |` to `corpus/README.md`, append a syntactically valid 11-column `S048` row (`kind=docs`, `tier=A`, `status=mined`, `used-by=corpus/knowledge/vendor-third-party-finding-coordination.md`) to `corpus/SOURCES.md`, and create a **0-byte empty file** `corpus/knowledge/vendor-third-party-finding-coordination.md`.
- **Case 3b:** Same, except `corpus/knowledge/vendor-third-party-finding-coordination.md` contains a **1-line header stub** `source: S048 https://example.invalid/junk` with no body, no `recheck:` line, and no round-31 capture/manifest.

Command and output:
```text
$ bash -c '
D=$(mktemp -d)
trap "rm -rf \"$D\"" EXIT
mkdir -p "$D/kasegi-shokunin"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive b374febbb33ccadade78a787279707fd5d2e6e1d | tar -x -C "$D/kasegi-shokunin"
cp /home/vgpnk/Projects/shokunin/shokunin.conf "$D/shokunin.conf"
cd "$D/kasegi-shokunin"
printf "| F15 | Junk topic | admitted | \`knowledge/vendor-third-party-finding-coordination.md\` | S048 |\n" >> corpus/README.md
python3 - <<PY
p = "corpus/SOURCES.md"
t = open(p).read()
row = "| S048 | https://example.invalid/junk | docs | A | junk | sec 1 | junk teaches | mined | 2026-10-25 | 90d | corpus/knowledge/vendor-third-party-finding-coordination.md |\n"
idx = t.index("| S047 |")
line_end = t.index("\n", idx) + 1
open(p, "w").write(t[:line_end] + row + t[line_end:])
PY
: > corpus/knowledge/vendor-third-party-finding-coordination.md
echo "=== Case 3a (0-byte empty entry, valid kind=docs) ==="
echo -n "c1_frontier_admitted="; awk -F"|" "\$2 ~ /^ *F[0-9]+ / && \$4 ~ /^ *admitted *\$/ {n++} END{print n+0}" corpus/README.md
echo -n "c2_entries_citing_S048="; grep -lE "^source: S048 " corpus/knowledge/*.md | wc -l
echo -n "c3_s048_rows="; grep -cE "^\|[[:space:]]*S048[[:space:]]*\|" corpus/SOURCES.md
echo -n "c4_registry_rows="; grep -cE "^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|" corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$D" kasegi --today 2026-10-25; echo "c5_census_exit=$?"
python3 corpus/instruments/frontier-recheck-count.py --root "$D/kasegi-shokunin" | tail -n 2; echo "c6_harness_exit=${PIPESTATUS[0]}"
python3 corpus/instruments/source-recheck.py --manifest "$D/kasegi-shokunin/corpus/source-snapshots/round-31/manifest.json" --source S048; echo "c7_recheck_exit=$?"
'
=== Case 3a (0-byte empty entry, valid kind=docs) ===
c1_frontier_admitted=15
c2_entries_citing_S048=0
c3_s048_rows=1
c4_registry_rows=48
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/tmp/tmp.TWIfIbenz0/kasegi-shokunin/corpus/SOURCES.md
c5_census_exit=0
FAIL     F15  knowledge/vendor-third-party-finding-coordination.md ids=-              exit=-    problems=no-source-line,no-recheck-line,no-source-selection,no-manifest
entries=18 pass=17 exit=1
c6_harness_exit=1
manifest UNAVAILABLE reason=missing
c7_recheck_exit=2
```
And for **Case 3b** (1-line stub `source: S048 https://example.invalid/junk`):
```text
=== Case 3b: Junk S048 row + F15 README row + 1-line stub entry ===
c2_entries_citing_S048=1
FAIL     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=-    problems=no-recheck-line,no-source-selection,no-manifest
entries=18 pass=17 exit=1
c6_harness_exit=1
```

- **Verdict on Attack (3):**
  1. **Can a junk-row + empty-entry commit meet *any* individual C2 counter? YES:**
     - With a `0`-byte empty entry file (`Case 3a`), it meets **4 of the 7 counters**: Counter 1 (`frontier_admitted=15`), Counter 3 (`s048_rows=1`), Counter 4 (`registry_rows=48`), and **Counter 5 (`sources-census.sh validate` exits `0` with `kasegi ok`)** because `sources-census.sh` `E11` only checks whether the `used-by` file path exists on disk (`[ -e ]`), not whether the file is non-empty or cites `S048`.
     - With a 1-line `source: S048 ...` stub (`Case 3b`), it meets **5 of the 7 counters** (adding Counter 2: `entries_citing_S048=1`).
     - Note that `C2.do_nothing_control` (`claims.json:48`) only describes a bare `S048` row *without* touching the entry path, which fails Counter 5 (`E11`/`W03`); touching an empty file bypasses Counter 5.
  2. **Can it meet the conjunctive C2 target? NO:**
     - **Counter 6 (`frontier-recheck-count.py:137-162`)** rejects both `Case 3a` (`problems=no-source-line,no-recheck-line,no-source-selection,no-manifest`, `entries=18 pass=17 exit=1`) and `Case 3b` (`problems=no-recheck-line,no-source-selection,no-manifest`, `exit=1`).
     - **Counter 7 (`source-recheck.py`)** rejects both (`manifest UNAVAILABLE reason=missing`, `recheck_exit=2`).
     - C1's no-harm corpus audit (`recheck-audit.py --quiet`) also fails (`complete=False` on a file with no `recheck:` line), and `C2.kill_rule` (`claims.json:47`) rejects any stub entry failing `QUALITY.md` Q1–Q10 under non-author review.

---

## Attack (4): Does C1's `depth:verifiability` Axis Name the Surface the Round Changes (§9)?

- **Verdict:** **Qualified YES (as a `"held 4"` detector-soundness claim under `QUALITY.md` R7/R11/R13); NO if framed as a primary corpus citation-resolvability move under `SCORECARD.md:33-38`.**
- **Reasoning & Evidence:**
  1. **Why `No` as a primary `depth:verifiability` score-moving surface (`SCORECARD.md:33-38`, `considerthese/2026-10-25.md:53-57`, `kasegi-round-31.md:435-437`):**
     - `SCORECARD.md:33-38` defines `depth:verifiability` by the live citation-resolution fraction (`resolve.py` + `anchorcheck.py`), and `considerthese/2026-10-25.md:53-57` (proposal 2) notes that the gap from score `4` to `5` is the `23/37` (now `24/43`) rechecks gated on absent domain bases.
     - Under `kasegi-round-31.md` §9 (`"Name the axis by the surface the round changes, not by the number it produces (kaidoku r29). Re-scoring a rule the lane already holds on new inputs, or counting rows a sourceless fixture also counts, is quality work, never coverage or depth"`), if C1 only re-scored already-passing instrument checks on synthetic scratch fixtures without strengthening any detector or selftest limb, it would be pure `quality` work rather than `depth:verifiability`.
  2. **Why `Yes` (with `score_after: "held 4"` and mandatory `QUALITY.md` R7 disclosure) on the actual base bytes `b374febbb33ccadade78a787279707fd5d2e6e1d`:**
     - The lane's `SCORECARD.md:63-67` owns only three scored axes (`depth:density`, `depth:verifiability`, `coverage`); `quality` is a §4 trend verdict, not a scored axis, and `kasegi-round-31.md` §2 rule 2 requires working the lowest non-retired axis (`depth:verifiability (4)`).
     - `C1.surface` (`claims.json:17`) explicitly names the changed surface (`"Discrimination of the lane's three recheck-family instruments (recheck-audit.py, source-recheck.py, frontier-recheck-count.py): a new committed one-limb mutation ledger ... and counter ...; routed defect M30-1 ... is closed by a stem-correct B2 row"`), not a bare number.
     - Crucially, we verified on base `b374febbb33ccadade78a787279707fd5d2e6e1d` that C1 is **not** merely re-scoring rules the three detectors already enforce in their selftests: mutating `RA-completeness` at `recheck-audit.py:350` (`complete = len(entries) == total and total > 0` → `complete = True`) **survives** `recheck-audit.py --selftest` on base bytes (`exit=0`), because `selftest()` (`recheck-audit.py:245-254`) never invokes `main()` on a missing-recheck-line fixture:
       ```text
       $ python3 - <<'PY'
       import subprocess, tempfile, pathlib
       raw = subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/kasegi-shokunin", "show", "b374febbb33ccadade78a787279707fd5d2e6e1d:corpus/instruments/recheck-audit.py"]).decode()
       mut = raw.replace("complete = len(entries) == total and total > 0", "complete = True", 1)
       assert raw != mut
       with tempfile.TemporaryDirectory() as d:
           p = pathlib.Path(d) / "recheck-audit.py"
           p.write_text(mut)
           r = subprocess.run(["python3", str(p), "--selftest"], capture_output=True, text=True)
           print("base_ra_completeness_mutant_selftest_exit=", r.returncode)
       PY
       base_ra_completeness_mutant_selftest_exit= 0
       ```
     - Likewise, at base `b374febbb`, `frontier-recheck-count.py` lacks committed isolating limb fixtures (`corpus/instruments/limb-fixtures/fr/**`), and round 30's B2 fixture (`M30-1`) tripped B1 (`stem-mismatch`) first instead of isolating `SR-occurrence-not-unique`.
     - Therefore, under `QUALITY.md` **R7** (`corpus/QUALITY.md:49`: `"instrument-correctness claims must change and exercise the actual detector, report semantic before→after cases, and disclose unchanged source-availability scores"`), **R11**, and **R13**, C1 is properly placed on `depth:verifiability` at `held 4` **provided** the round lands the strengthened detector/selftest/fixture bytes (`recheck-audit.py` + `sr`/`fr` limb fixtures) and discloses in `SCORECARD.md` and the round report that corpus source-availability / citation-resolution scores are unchanged.
