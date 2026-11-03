H HOLDS (M=0) for the specified seed-59 400-derive 1–4-token sample (N=68, M=0); as a universal claim H is FALSIFIED outside that bounded space — 28/28 targeted B1/B2-family derives are ADMITTED, create MARK-F, and 14/28 make the gate print `FIG … ok` / `figures=1 ok=1 stale=0 exit=0` (mechanism = the already-recorded B1/B2 residual; the ≥9-token shape it needs is unreachable with 1–4 tokens).

Seat FuzzDerive, kasegi round 59 w1. Instrument under test: `corpus/instruments/figure-audit.py` at lane HEAD (sha256 in E1). No lane file modified, nothing committed, nothing installed.

# 0. Method

- ADMITTED = `figure_audit.check_read_only(derive)` is true (the seat's rule), module loaded with importlib from `L/corpus/instruments/figure-audit.py`.
- Every derive is run once with `bash -c` in a fresh root holding `g.txt` = `3\n2\n1\n`, `timeout 10 s`, stdin `/dev/null`, under `strace -f -e trace=execve`; the whole per-derive sandbox is then searched for a file named exactly `MARK-F`, and the exec set is compared with the head allow-list (`cat grep wc head tail sort awk sed python python3`, plus the `bash` interpreter).
- For every ADMITTED derive the real gate is also run end-to-end (`fa.audit()` on a one-figure ledger, `want` = observed stdout, second fresh root), so each row carries the gate's own `ok`/`stale` verdict and a MARK-F search of the gate's own root.
- Alphabet (25 tokens, in this order): `cat g.txt`, `grep -c 1 g.txt`, `wc -l g.txt`, `head -1 g.txt`, `tail -1 g.txt`, `sort g.txt`, `echo x`, `touch MARK-F`, `tee MARK-F`, `sh`, `awk 1`, `|`, `&&`, `;`, `&`, `||`, newline, `$(cat g.txt)`, `` `cat g.txt` ``, `>`, `<`, space, single quote, double quote, backslash. A derive is the concatenation of 1–4 tokens (`""` join — the space is itself a token). A space-join variant is run as a joiner-sensitivity control.
- Every inline `python3 - <<'EOF'` block below was run from `cd /fast/scratch/hyaku/kasegi-r59/FuzzDerive` with `TMPDIR=$PWD` and `2>&1 | tee <log>` (the log name is the first line of each block); its printed lines are quoted verbatim beneath it.

# E1. Lane state and instrument identity (read-only git)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
472737847ff31d1255bf1a0745822a5e878e9622
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  …/corpus/instruments/figure-audit.py
$ git -C … diff --stat HEAD -- corpus/instruments/figure-audit.py
(no output)
$ git -C … diff --stat 00b535758d2cfa4511cda7167b67cdc045b85fb4 -- .ufo/waves/round-59/claims.json
(no output)
$ git -C … status --porcelain -- corpus/instruments/figure-audit.py corpus/SOURCES.md corpus/README.md
(no output)
```
Each command exited 0. HEAD is the lane HEAD named in the seat assignment; the instrument blob at HEAD equals the worktree copy and equals the frozen C1 candidate sha256 `32e1cddb…` (`claims.json` counting_commands, sha256sum line). The worktree was already dirty at seat start in `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md` (not touched by this seat).

# E2. Primary run: 400 derives, 1–4 tokens, seed 59 (the specified sample)

```
$ cd /fast/scratch/hyaku/kasegi-r59/FuzzDerive && TMPDIR=$PWD python3 fuzz_derive.py < /dev/null > run.log 2>&1; echo "exit=$?"
exit=0
$ sha256sum fuzz_derive.py
f6fb16e1c8bc6e9ad1e783abcce6abe885d5f3b2d814880d4cdf507610783e55  fuzz_derive.py
```
`run.log:1–3` (the fuzzer prints the sha256 of the file it imported, so the line self-certifies the loaded bytes):

```
INSTRUMENT=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py sha256=32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0
ALPHABET=25 SEED=59
PHASE primary_1_4_concat derives=400 N=68 M=0 M_outside_root=0 gate_ok=29 gate_ok_and_M=0 nonallow_exec=0
```

N=68 admitted of 400; M=0 admitted-and-MARK-F; 0 files outside the root; 29 of the 68 also pass the gate's `ok` path; 0 admitted derive executed a program outside the allow-list. Fuzzer sha256 `f6fb16e1c8bc6e9ad1e783abcce6abe885d5f3b2d814880d4cdf507610783e55`.

Admitted-set composition (re-derived from the same deterministic generator):

```
$ python3 - <<'EOF' 2>&1 | tee compose.log
import importlib.util, collections
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
rows = [fz.probe(d, i) for i, d in enumerate(fz.gen(59, 1, 4, ""))]
adm = [r for r in rows if r["admitted"]]
print("COMPOSE distinct=%d total=%d top=%r" % (len({r["derive"] for r in adm}), len(adm),
      collections.Counter(r["derive"] for r in adm).most_common(5)))
EOF
COMPOSE distinct=40 total=68 top=[('cat g.txt', 9), ('head -1 g.txt', 7), ('tail -1 g.txt', 6), ('sort g.txt', 5), ('awk 1', 4)]
```
All 40 admitted texts are an allow-listed head with writer/token noise glued into argument position (e.g. `cat g.txttouch MARK-F`, `sort g.txtsh`, `head -1 g.txttee MARK-Ftouch MARK-F`).

# E3. Joiner/length controls (same run.log)

`run.log:34`, `run.log:45`, `run.log:76`:

```
PHASE variant_concat_5_9 derives=400 N=10 M=0 M_outside_root=0 gate_ok=0 gate_ok_and_M=0 nonallow_exec=0
PHASE variant_space_1_4 derives=400 N=68 M=0 M_outside_root=0 gate_ok=29 gate_ok_and_M=0 nonallow_exec=0
PHASE variant_space_5_9 derives=400 N=10 M=0 M_outside_root=0 gate_ok=0 gate_ok_and_M=0 nonallow_exec=0
```
The `" "`-join 1–4-token variant reproduces N=68/M=0 (same admitted multiset), so the joiner choice does not drive the result. The 5–9-token samples admit fewer derives (10) and still no MARK-F.

# E4. Exhaustive whole 1–4-token space (not a sample)

```
$ TMPDIR=$PWD python3 fuzz_derive.py --exhaustive < /dev/null; echo "exhaustive_exit=$?"
EXHAUSTIVE_1_4 admitted_by_len={1: 7, 2: 105, 3: 1589, 4: 24402} admitted_total=26103 writer_candidates=11718 hits=0
exhaustive_exit=0
```
All 25+25²+25³+25⁴ = 406,900 sequences of 1–4 tokens were tested against `check_read_only`; **26,103** are admitted; the **11,718** admitted ones containing a writer token (`touch MARK-F`, `tee MARK-F`, `sh`) were executed in fresh roots: **0** create MARK-F. The 400-derive M=0 is therefore not sampling luck — the entire bounded space is M=0.

# E5. Targeted B1/B2-family extension: 7 heads × 2 quote kinds × 2 closers = 28

Shape per row: `HEAD '\; touch MARK-F; CLOSER\'` (and the `"` form) — the recorded backslash-escaped-quote divergence, written with spaces (spaced form; 12 alphabet tokens per row, confirmed by the tokenizer block in E6).

`run.log:87`:

```
PHASE targeted_b1b2_family_7heads_x2quotes_x2closers derives=28 N=28 M=28 M_outside_root=0 gate_ok=14 gate_ok_and_M=14 nonallow_exec=28
```
`run.log:116–125` (first ten HITs; paths trimmed):

```
  HIT i=5000 derive="cat g.txt \\'; touch MARK-F; echo x\\'" marks=[…/sand/p5000/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
  HIT i=5001 derive="cat g.txt \\'; touch MARK-F; cat g.txt\\'" marks=[…/sand/p5001/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
  HIT i=5002 derive='cat g.txt \\"; touch MARK-F; echo x\\"' marks=[…/sand/p5002/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
  HIT i=5003 derive='cat g.txt \\"; touch MARK-F; cat g.txt\\"' marks=[…/sand/p5003/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
  HIT i=5004 derive="grep -c 1 g.txt \\'; touch MARK-F; echo x\\'" marks=[…/sand/p5004/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
  HIT i=5005 derive="grep -c 1 g.txt \\'; touch MARK-F; cat g.txt\\'" marks=[…/sand/p5005/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
  HIT i=5006 derive='grep -c 1 g.txt \\"; touch MARK-F; echo x\\"' marks=[…/sand/p5006/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
  HIT i=5007 derive='grep -c 1 g.txt \\"; touch MARK-F; cat g.txt\\"' marks=[…/sand/p5007/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
  HIT i=5008 derive="wc -l g.txt \\'; touch MARK-F; echo x\\'" marks=[…/sand/p5008/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
  HIT i=5009 derive="wc -l g.txt \\'; touch MARK-F; cat g.txt\\'" marks=[…/sand/p5009/root/MARK-F] outside=[] gate=FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
```
All 28 admitted, all 28 create MARK-F, every row executes `touch` (non-allow-listed), none writes outside its root. **14/28 additionally make the gate print `figures=1 ok=1 stale=0 exit=0` while MARK-F exists in the gate's own root** — the `gate_marks` field is non-empty for those rows, e.g. row i=5000: `gate_marks=['…/sand/g5000/root/MARK-F']`.

# E6. Minimal falsifier (9 alphabet tokens) and its ladder

```
$ python3 - <<'EOF' 2>&1 | tee minimal.log
import importlib.util, json
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
d = "cat g.txt\\';touch MARK-F;echo x\\'"
r = fz.probe(d, 6100)
print("MINIMAL derive=%r len=%d admitted=%s rc=%s stdout=%r" % (d, len(d), r["admitted"], r["rc"], r["stdout"]))
print("MINIMAL execs=%r nonallow=%r marks=%r" % (r["execs"], r["nonallow"], r["marks"]))
print("MINIMAL gate_code=%s gate_line=%r gate_marks=%r" % (r["gate_code"], r["gate_line"], r["gate_marks"]))
toks = ["cat g.txt", "\\", "'", ";", "touch MARK-F", ";", "echo x", "\\", "'"]
print("MINIMAL tokens=%d concat_equal=%s %r" % (len(toks), "".join(toks) == d, toks))
print("MINIMAL check_read_only(final advice)==%s" % fz.fa.check_read_only(d))
EOF
MINIMAL derive="cat g.txt\\';touch MARK-F;echo x\\'" len=33 admitted=True rc=0 stdout="x'"
MINIMAL execs=['bash', 'cat', 'touch'] nonallow=['touch'] marks=['/fast/scratch/hyaku/kasegi-r59/FuzzDerive/sand/p6100/root/MARK-F']
MINIMAL gate_code=0 gate_line='FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0' gate_marks=['/fast/scratch/hyaku/kasegi-r59/FuzzDerive/sand/g6100/root/MARK-F']
MINIMAL tokens=9 concat_equal=True ['cat g.txt', '\\', "'", ';', 'touch MARK-F', ';', 'echo x', '\\', "'"]
MINIMAL check_read_only(final advice)==True
```
`cat g.txt\';touch MARK-F;echo x\'` — 9 tokens, admitted, exit 0, stdout `x'`, creates MARK-F in the probe root **and** in the gate's own audit root, gate `figures=1 ok=1 stale=0 exit=0`.

Same shape through the instrument's real CLI (production path `main` → `audit`), separate fresh roots:

```
$ L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 $L/corpus/instruments/figure-audit.py --ledger cliA/ledger.json --root cliA ; echo exitA=$?
FIG CLI1 recorded=x' derived=x' ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
exitA=0
$ find cliA -maxdepth 1 -type f -printf '%f\n' | sort
g.txt
ledger.json
MARK-F
$ python3 $L/corpus/instruments/figure-audit.py --ledger cliB/ledger.json --root cliB ; echo exitB=$?
FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=CLI2
exitB=2
$ find cliB -maxdepth 1 -type f -printf '%f\n' | sort
g.txt
ledger.json
```
cliA ledger derive = the 9-token text above; cliB ledger derive = `cat g.txt;touch MARK-F`. The admitted ledger both prints `ok` and writes MARK-F into the audited root; the refused ledger exits 2 and writes nothing — refusal is checked before execution (`figure-audit.py:166-167` returns 2 before `run_derive` at `:169`). The selftest passes `--root` = a temp dir (`:236`), so it never writes into the lane.

Ladder of the same mechanism below and around 9 tokens (all measured with the same `probe`, `tee minimal2.log` / `tee edge7.log`):

```
$ python3 - <<'EOF' 2>&1 | tee minimal2.log
import importlib.util
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
for tag, d in [
  ("plain-quote-glue", "cat g.txt\\';touch MARK-F'"),
  ("plain-quote-syntax", "cat g.txt\\';touch MARK-F;x'"),
  ("pipe-inside-quote", "cat g.txt\\'|touch MARK-F|echo x\\'"),
  ("semicolon-8-token-with-spaces", "cat g.txt \\'; touch MARK-F; \\'")]:
    r = fz.probe(d, 6200 + len(d))
    print("%-28s admitted=%-5s rc=%-4s marks=%d gate=%s derive=%r"
          % (tag, r["admitted"], r["rc"], len(r["marks"]),
             (r.get("gate_line") or "-")[-28:], d))
EOF
plain-quote-glue             admitted=True  rc=2    marks=0 gate=igures=1 ok=0 stale=1 exit=1 derive="cat g.txt\\';touch MARK-F'"
plain-quote-syntax           admitted=True  rc=2    marks=0 gate=igures=1 ok=0 stale=1 exit=1 derive="cat g.txt\\';touch MARK-F;x'"
pipe-inside-quote            admitted=True  rc=0    marks=1 gate=igures=1 ok=1 stale=0 exit=0 derive="cat g.txt\\'|touch MARK-F|echo x\\'"
semicolon-8-token-with-spaces admitted=True  rc=127  marks=1 gate=igures=1 ok=0 stale=1 exit=1 derive="cat g.txt \\'; touch MARK-F; \\'"
```
Plus the 7-token attached-close edge and the 5-token unterminated edge from the first ladder run:

```
$ python3 - <<'EOF' 2>&1 | tee edge7.log
import importlib.util, os
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
d = "cat g.txt\\';touch MARK-F\\'"
r = fz.probe(d, 6300)
print("EDGE7 admitted=%s rc=%s marks=%r derive=%r tokens=%r"
      % (r["admitted"], r["rc"], r["marks"], d,
         ["cat g.txt","\\","'",";","touch MARK-F","\\","'"]))
print("EDGE7 root_files=%r" % sorted(os.listdir(os.path.join(fz.S,"sand","p6300","root"))))
EOF
EDGE7 admitted=True rc=0 marks=[] derive="cat g.txt\\';touch MARK-F\\'" tokens=['cat g.txt', '\\', "'", ';', 'touch MARK-F', '\\', "'"]
EDGE7 root_files=["MARK-F'", 'g.txt']
```
and:

```
$ python3 - <<'EOF' 2>&1 | tee ladder5.log
import importlib.util
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
d = "cat g.txt\\';touch MARK-F"
r = fz.probe(d, 6400)
print("L5 admitted=%s rc=%s marks=%r derive=%r" % (r["admitted"], r["rc"], r["marks"], d))
EOF
L5 admitted=False rc=0 marks=['/fast/scratch/hyaku/kasegi-r59/FuzzDerive/sand/p6400/root/MARK-F'] derive="cat g.txt\\';touch MARK-F"
```
The 5-token text is REFUSED (unterminated quote); my harness still ran it (hence the marker), which the gate never does because refusal precedes execution (E7 `REFUSAL` line).

Token counts of every ladder text and of a spaced targeted row, by greedy longest-match over the same 25-token alphabet:

```
$ python3 - <<'EOF' 2>&1 | tee tokens.log
import importlib.util
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
ALPHA = sorted(fz.ALPHABET, key=len, reverse=True)
def tok(s):
    out, i = [], 0
    while i < len(s):
        for t in ALPHA:
            if s.startswith(t, i):
                out.append(t); i += len(t); break
        else:
            raise SystemExit("no token at %d in %r" % (i, s))
    return out
texts = [
 "cat g.txt\\';touch MARK-F",
 "cat g.txt\\';touch MARK-F'",
 "cat g.txt\\';touch MARK-F\\'",
 "cat g.txt\\';touch MARK-F;echo x\\'",
 "cat g.txt\\'|touch MARK-F|echo x\\'",
 "cat g.txt \\'; touch MARK-F; \\'",
 "cat g.txt \\'; touch MARK-F; echo x\\'",
]
for t in texts:
    print("TOKENS=%d %r" % (len(tok(t)), t))
EOF
TOKENS=5 "cat g.txt\\';touch MARK-F"
TOKENS=6 "cat g.txt\\';touch MARK-F'"
TOKENS=7 "cat g.txt\\';touch MARK-F\\'"
TOKENS=9 "cat g.txt\\';touch MARK-F;echo x\\'"
TOKENS=9 "cat g.txt\\'|touch MARK-F|echo x\\'"
TOKENS=11 "cat g.txt \\'; touch MARK-F; \\'"
TOKENS=12 "cat g.txt \\'; touch MARK-F; echo x\\'"
```
The 12-token row is the spaced form of the targeted family (E5); the smallest exactly-MARK-F shapes here are 9 tokens.

Summary of the ladder (counts from the tokenizer block above): 5 tokens refused; 6 tokens (`…touch MARK-F'`) admitted but bash rejects the whole string as a syntax error (`rc=2`, nothing runs); 7 tokens (`…touch MARK-F\'`) admitted, `rc=0`, creates the decoy `MARK-F'` not MARK-F; **9 tokens (`…touch MARK-F;echo x\'` and `…\'|touch MARK-F|echo x\'`) admitted, `rc=0`, creates MARK-F and the gate prints `ok`**; the 11-token spaced form (`cat g.txt \'; touch MARK-F; \'`) is admitted, creates MARK-F, gate `stale` at `rc=127`. Minimum found = 9 tokens. `[INFERENCE]` 9 is the minimum for exactly-MARK-F: the scanner's quote can only be opened by a backslash+quote pair (2 tokens) and closed by a second escaped quote (2) that must follow a separator or it glues onto the writer's argument; head + open pair + hidden separator + writer + close pair ≥ 9.

# E7. Other candidate classes: all refused (and refusal is pre-execution)

```
$ python3 - <<'EOF' 2>&1 | tee classes.log
import importlib.util, os, json, contextlib, io
spec = importlib.util.spec_from_file_location("fz", "fuzz_derive.py")
fz = importlib.util.module_from_spec(spec); spec.loader.exec_module(fz)
cases = [
 ("A-subshell",   "cat g.txt <(touch MARK-F)"),
 ("B-semicolon",  "cat g.txt;touch MARK-F"),
 ("C-andand",     "cat g.txt&&touch MARK-F"),
 ("D-pipe-tee",   "cat g.txt|tee MARK-F"),
 ("E-newline",    "cat g.txt\ntouch MARK-F"),
 ("F-sq-glue",    "cat g.txt'touch MARK-F'"),
 ("G-dq-arg",     'cat g.txt "touch MARK-F"'),
 ("H-dq-cmdsub",  'cat "$(touch MARK-F)"'),
 ("I-dq-backtick",'cat "`touch MARK-F`"'),
 ("J-sq-backtick","cat g.txt '`touch MARK-F`'"),
 ("K-redirect",   "cat g.txt > MARK-F"),
 ("L-in-redirect","cat g.txt < MARK-F"),
 ("M-backslash-close","cat g.txt \\';touch MARK-F;echo x\\'"),
]
for name, d in cases:
    r = fz.probe(d, 8000 + len(d) + len(name))
    print("CLASS %-15s admitted=%-5s rc=%-4s marks=%-6d gate=%s derive=%r"
          % (name, r["admitted"], r["rc"], len(r["marks"]),
             (r.get("gate_line") or "-")[-30:], d))
d = "cat g.txt;touch MARK-F"
dd, root = fz.fresh_root("refuse")
led = os.path.join(fz.S, "ledgers", "refuse.json")
os.makedirs(os.path.dirname(led), exist_ok=True)
json.dump({"figures":[{"id":"R","record":"g.txt:1","recorded":"x","derive":d,"want":"x"}]}, open(led,"w"))
err = io.StringIO()
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
    code = fz.fa.audit(led, root)
print("REFUSAL audit(derive=%r) exit=%d stderr=%r marks=%d" % (d, code, err.getvalue().strip(), len(fz.marks(dd))))
EOF
CLASS A-subshell      admitted=False rc=0    marks=1      gate=- derive='cat g.txt <(touch MARK-F)'
CLASS B-semicolon     admitted=False rc=0    marks=1      gate=- derive='cat g.txt;touch MARK-F'
CLASS C-andand        admitted=False rc=0    marks=1      gate=- derive='cat g.txt&&touch MARK-F'
CLASS D-pipe-tee      admitted=False rc=0    marks=1      gate=- derive='cat g.txt|tee MARK-F'
CLASS E-newline       admitted=False rc=0    marks=1      gate=- derive='cat g.txt\ntouch MARK-F'
CLASS F-sq-glue       admitted=True  rc=1    marks=0      gate= figures=1 ok=0 stale=1 exit=1 derive="cat g.txt'touch MARK-F'"
CLASS G-dq-arg        admitted=True  rc=1    marks=0      gate= figures=1 ok=0 stale=1 exit=1 derive='cat g.txt "touch MARK-F"'
CLASS H-dq-cmdsub     admitted=False rc=1    marks=1      gate=- derive='cat "$(touch MARK-F)"'
CLASS I-dq-backtick   admitted=False rc=1    marks=1      gate=- derive='cat "`touch MARK-F`"'
CLASS J-sq-backtick   admitted=True  rc=1    marks=0      gate= figures=1 ok=0 stale=1 exit=1 derive="cat g.txt '`touch MARK-F`'"
CLASS K-redirect      admitted=False rc=0    marks=1      gate=- derive='cat g.txt > MARK-F'
CLASS L-in-redirect   admitted=True  rc=1    marks=0      gate= figures=1 ok=0 stale=1 exit=1 derive='cat g.txt < MARK-F'
CLASS M-backslash-close admitted=True rc=0   marks=1      gate= figures=1 ok=1 stale=0 exit=0 derive="cat g.txt \\';touch MARK-F;echo x\\'"
REFUSAL audit(derive='cat g.txt;touch MARK-F') exit=2 stderr='FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=R' marks=0
```
The `marks=1` on refused rows are **my harness** running the derive deliberately; the gate never runs a refused derive — the `REFUSAL` line shows `audit` exiting 2 with the refusal reason and `marks=0`. Admitted rows F/G/J/L are argument-noise (the writer token is a filename argument to `cat`, nothing execs). Only the B1/B2 backslash-quote mechanism (row M) executes.

# E8. Known-residual controls (harness sensitivity; already recorded by the lead, not new)

`run.log:126–130`:

```
  CTL admitted=True rc=127 marks=['…/sand/p9000/root/MARK-F'] gate_code=1 gate='FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1' derive="cat g.txt \\'; touch MARK-F; \\'"
  CTL admitted=True rc=0 marks=['…/sand/p9001/root/MARK-F'] gate_code=1 gate='FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1' derive='awk \'BEGIN{system("touch MARK-F")}\''
  CTL admitted=True rc=0 marks=['…/sand/p9002/root/MARK-F'] gate_code=1 gate='FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1' derive="sed -n '1e touch MARK-F' g.txt"
  CTL admitted=True rc=0 marks=['…/sand/p9003/root/MARK-F'] gate_code=1 gate='FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1' derive='sort -o MARK-F g.txt'
```
B1, B4, B3, B6 reproduce (admitted, MARK-F created) and all four end `ok=0 stale=1 exit=1`; the harness detects creation in every case, so the M=0 results above are not a detector failure. None of the four controls writes outside its root:

```
$ python3 -c "import json; r=json.load(open('results.json')); print({k: v['outside'] for k, v in r.items() if k.startswith('ctl_')})"
{'ctl_0': [], 'ctl_1': [], 'ctl_2': [], 'ctl_3': []}
```

# Findings

1. **No other class found.** Within the 25-token alphabet every non-B1/B2 execution shape is refused (`;`, `<(` via `(`, `&&`, `|`, newline, `>`, `$(`/backtick inside double quotes), and refusal happens before `run_derive` (`figure-audit.py:166-169`), so a refused derive cannot write. The only admitted writers are argument-noise (F/G/J/L) and the recorded B1/B2 divergence.
2. **The specified 1–4-token probe has structural zero power against the recorded class.** The scanner's quote must be opened by a backslash-escaped quote and closed by a second escaped quote after a separator: 9 alphabet tokens by construction (E6 ladder), and the 6-token close is a bash syntax error that runs nothing. Hence M=0 at 1–4 tokens, confirmed exhaustively over all 26,103 admitted 1–4-token derivations (E4), not merely over 400 samples.
3. **New receipt on the recorded B1/B2 residual: it can make the gate green.** 14/28 targeted variants print `FIG … ok` / `figures=1 ok=1 stale=0 exit=0` while MARK-F exists in the gate's own audit root (E5), and the real CLI reproduces it (`exitA=0`, E6). The lead's B1 example ends `rc 127`/stale (E8 row 1); the residual is therefore not confined to derives the gate later marks stale — an `ok` verdict from this gate does not imply the derive had no side effects.
4. **The default audit root is `.`** (`figure-audit.py:275`), so the documented lane invocation `python3 corpus/instruments/figure-audit.py` executes ledger derives with cwd = the lane root. A committed ledger entry of this shape would write into the lane, not into a temp dir. Not exercised against the lane (read-only seat); the CLI receipts above use `--root` inside scratch.
5. **Limb (b) of H held everywhere**: `M_outside_root=0` in every primary/variant/targeted row and `outside=[]` for all four controls; every MARK-F was created inside the root the derive was given. The falsification is the in-root marker creation that the seat's rule names.

# Limits

- The alphabet contains no `{`, `$`, `-o`, `sed -n`, or `--output`, so B3/B4/B6 are out of reach by construction; they are reproduced only as controls (E8), not re-derived as new classes.
- `[INFERENCE]` "only allow-listed programs" over the whole 1–4-token space rests on measurement of the 68 admitted primary derivations (`nonallow_exec=0`) plus the structural argument that an admitted 1–4-token derive has no unquoted separator, so only the first word can be a program; it was not straced over all 26,103.
- Single host, single bash (5.3.20), single python (3.14.8); marker detection is exact-name `MARK-F` only (a `MARK-F'` decoy is not counted, E6).
- The 400-derive primary is deterministic (`random.Random(59)`, fixed alphabet, `""` join, lengths via `randint(1,4)`), so its numbers reproduce on re-run.

# Fuzzer source (the file that produced run.log, exhaustive.log and the two inline probes; sha256 f6fb16e1c8bc6e9ad1e783abcce6abe885d5f3b2d814880d4cdf507610783e55)

```python
#!/usr/bin/env python3
"""FuzzDerive r59 w1 — bounded probe of the figure-audit derive gate.

H: every derive the gate ADMITS runs only allow-listed programs and creates
no file outside its scratch root; one admitted derive that creates MARK-F
falsifies H. ADMITS := figure-audit.check_read_only(derive) is true (seat
rule). Each admitted derive is run once with `bash -c` in a fresh root
holding g.txt, timeout 10 s, under `strace -f -e trace=execve`, then handed
to the real gate fa.audit() in a second fresh root (one-figure ledger, want =
observed stdout) so the gate's own ok/stale line is seen.
"""
import contextlib, importlib.util, io, json, os, random, re, shutil, subprocess, sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
INSTR = L + "/corpus/instruments/figure-audit.py"
S = "/fast/scratch/hyaku/kasegi-r59/FuzzDerive"
SEED = 59
ALPHABET = ["cat g.txt", "grep -c 1 g.txt", "wc -l g.txt", "head -1 g.txt",
            "tail -1 g.txt", "sort g.txt", "echo x", "touch MARK-F", "tee MARK-F",
            "sh", "awk 1", "|", "&&", ";", "&", "||", "\n", "$(cat g.txt)",
            "`cat g.txt`", ">", "<", " ", "'", '"', "\\"]
ALLOWED_EXEC = {"bash", "cat", "grep", "wc", "head", "tail", "sort", "awk", "sed", "python", "python3"}
EXEC_RE = re.compile(r'execve\("([^"]+)"')

spec = importlib.util.spec_from_file_location("figure_audit", INSTR)
fa = importlib.util.module_from_spec(spec); spec.loader.exec_module(fa)


def fresh_root(tag):
    d = os.path.join(S, "sand", tag); root = os.path.join(d, "root")
    shutil.rmtree(d, ignore_errors=True); os.makedirs(root)
    with open(os.path.join(root, "g.txt"), "w") as f:
        f.write("3\n2\n1\n")
    return d, root


def bash_run(derive, root, trace):
    try:
        p = subprocess.run(["strace", "-f", "-qq", "-e", "trace=execve", "-o", trace,
                            "bash", "-c", derive], cwd=root, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return None, "", "timeout"


def marks(sand):
    return [os.path.join(dp, fn) for dp, _, fns in os.walk(sand) for fn in fns if fn == "MARK-F"]


def outside(sand, root):
    return [os.path.join(dp, fn) for dp, _, fns in os.walk(sand) for fn in fns
            if not os.path.join(dp, fn).startswith(root + os.sep)]


def execs(trace):
    seen = set()
    if os.path.exists(trace):
        for line in open(trace, errors="replace"):
            m = EXEC_RE.search(line)
            if m:
                seen.add(os.path.basename(m.group(1)))
    return sorted(seen)


def gate_verdict(derive, want, tag):
    d, root = fresh_root(tag)
    os.makedirs(os.path.join(S, "ledgers"), exist_ok=True)
    led = os.path.join(S, "ledgers", tag + ".json")
    json.dump({"figures": [{"id": "FZ", "record": "g.txt:1", "recorded": want,
                            "derive": derive, "want": want}]}, open(led, "w"))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        code = fa.audit(led, root)
    return code, buf.getvalue().strip().splitlines()[-1], marks(d)


def probe(derive, i):
    d, root = fresh_root("p%04d" % i)
    trace = os.path.join(S, "traces", "p%04d.trace" % i)
    os.makedirs(os.path.join(S, "traces"), exist_ok=True)
    rc, out, err = bash_run(derive, root, trace)
    ms, ex, ok = marks(d), execs(trace), fa.check_read_only(derive)
    rec = {"i": i, "derive": derive, "admitted": ok, "rc": rc, "stdout": out.strip()[:120],
           "stderr": err.strip()[:120], "marks": ms, "outside": outside(d, root), "execs": ex,
           "nonallow": [e for e in ex if e not in ALLOWED_EXEC]}
    if ok:
        want = out.strip() if out.strip() else "x"
        rec["gate_code"], rec["gate_line"], rec["gate_marks"] = gate_verdict(derive, want, "g%04d" % i)
    return rec


def bash_plain(derive, root):
    try:
        p = subprocess.run(["bash", "-c", derive], cwd=root, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return None, ""


def exhaustive():
    from itertools import product
    cnt, cand = {n: 0 for n in (1, 2, 3, 4)}, []
    for n in (1, 2, 3, 4):
        for seq in product(ALPHABET, repeat=n):
            d = "".join(seq)
            if fa.check_read_only(d):
                cnt[n] += 1
                if any(w in d for w in ("touch MARK-F", "tee MARK-F", "sh")):
                    cand.append(d)
    hits = []
    for j, d in enumerate(cand):
        dd, root = fresh_root("x%05d" % j)
        bash_plain(d, root)
        if marks(dd):
            hits.append((d, marks(dd)))
    print("EXHAUSTIVE_1_4 admitted_by_len=%s admitted_total=%d writer_candidates=%d hits=%d"
          % (cnt, sum(cnt.values()), len(cand), len(hits)))
    for d, m in hits[:10]:
        print("  XHIT derive=%r marks=%r" % (d, m))


def gen(seed, lo, hi, join):
    rng = random.Random(seed)
    return [join.join(rng.choice(ALPHABET) for _ in range(rng.randint(lo, hi))) for _ in range(400)]


def summarize(name, derives, pbase):
    rows = [probe(d, pbase + i) for i, d in enumerate(derives)]
    adm = [r for r in rows if r["admitted"]]
    hit = [r for r in adm if r["marks"]]
    gok = [r for r in adm if r.get("gate_code") == 0]
    gh = [r for r in gok if r["marks"]]
    print("PHASE %s derives=%d N=%d M=%d M_outside_root=%d gate_ok=%d gate_ok_and_M=%d nonallow_exec=%d"
          % (name, len(rows), len(adm), len(hit), sum(1 for r in adm if r["outside"]),
             len(gok), len(gh), sum(1 for r in adm if r["nonallow"])))
    for r in adm[:30]:
        print("  ADMIT i=%d rc=%s derive=%r execs=%s nonallow=%s gate=%s"
              % (r["i"], r["rc"], r["derive"], ",".join(r["execs"]), r["nonallow"],
                 r.get("gate_line", "")[-18:]))
    for r in hit[:10]:
        print("  HIT i=%d derive=%r marks=%s outside=%s gate=%s"
              % (r["i"], r["derive"], r["marks"], r["outside"], r.get("gate_line", "")))
    return rows


def targeted():
    ds = []
    for h in ["cat g.txt", "grep -c 1 g.txt", "wc -l g.txt", "head -1 g.txt",
              "tail -1 g.txt", "sort g.txt", "awk 1"]:
        for q in ["'", '"']:
            for c in ["echo x", "cat g.txt"]:
                ds.append(h + " \\" + q + "; touch MARK-F; " + c + "\\" + q)
    return summarize("targeted_b1b2_family_7heads_x2quotes_x2closers", ds, 5000)


if __name__ == "__main__":
    if "--exhaustive" in sys.argv:
        exhaustive(); sys.exit(0)
    print("INSTRUMENT=%s sha256=%s" % (INSTR, subprocess.check_output(
        ["sha256sum", INSTR]).decode().split()[0]))
    print("ALPHABET=%d SEED=%d" % (len(ALPHABET), SEED))
    res = {"primary": summarize("primary_1_4_concat", gen(SEED, 1, 4, ""), 0),
           "v_concat_5_9": summarize("variant_concat_5_9", gen(SEED, 5, 9, ""), 1000),
           "v_space_1_4": summarize("variant_space_1_4", gen(SEED, 1, 4, " "), 2000),
           "v_space_5_9": summarize("variant_space_5_9", gen(SEED, 5, 9, " "), 3000),
           "targeted": targeted()}
    ctl = ["cat g.txt \\'; touch MARK-F; \\'",
           "awk 'BEGIN{system(\"touch MARK-F\")}'",
           "sed -n '1e touch MARK-F' g.txt",
           "sort -o MARK-F g.txt"]
    print("CONTROLS (known residuals B1/B4/B3/B6, harness sensitivity)")
    for j, dv in enumerate(ctl):
        r = probe(dv, 9000 + j)
        print("  CTL admitted=%s rc=%s marks=%s gate_code=%s gate=%r derive=%r"
              % (r["admitted"], r["rc"], r["marks"], r.get("gate_code"),
                 r.get("gate_line"), r["derive"]))
        res["ctl_%d" % j] = r
    json.dump(res, open(os.path.join(S, "results.json"), "w"), indent=1)
    print("RESULTS=%s" % os.path.join(S, "results.json"))
```

# Tooling, scratch, footprint

- No tool was installed or upgraded; no pacman transaction was run.
- Versions: `Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1 20260810]`, `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)`, `strace -- version 7.2`, `git` (read-only lane commands only).
- Scratch root `/fast/scratch/hyaku/kasegi-r59/FuzzDerive` (fuzzer, logs, per-derive sandboxes, result JSON) is removed before this seat yields; no temp file was ever written under `/tmp` (`TMPDIR` always pointed at the scratch dir) and no leftover is named because none remains.
- Files written under `L`: this evidence file only. No lane file, ledger, claims file, instrument, SOURCES row, README, PROVINCE or knowledge file was modified; no git mutation, no commit.
- No credential material appears in this file; none was read.
