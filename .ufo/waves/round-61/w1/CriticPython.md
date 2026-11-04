RESIDUAL CONFIRMED — universal Python-path confinement fails; no counterexample to frozen C1 P1–P3 predicate established by this seat.

## Axes and scope
- depth:verifiability: 24 isolated cases × base/pin = 48 instrument invocations, with harmless execution markers and exact base comparison.
- coverage: quoted/escaped arguments, variable/brace/glob expansion, target/directory symlinks, normalized paths. C2 source admission was not assigned or tested.
- No judging/admission decision, production edits, commits, broad suite, or real-target execution. Only this report is written in the lane. No tools installed.

## Identity and commands
Read operator RULES first and claims before implementation inspection. Frozen claims were also read using:
`TMPDIR=/fast/scratch/hyaku/kasegi-r61/CriticPython git -C /fast/scratch/hyaku/kasegi-r61/CriticPython/clone show 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766:.ufo/waves/round-61/claims.json` (exit 0; C1 explicitly excludes universal security and names quoting/expansion residual).

Scratch creation and pinning (all exits 0):
```sh
mkdir -p /fast/scratch/hyaku/kasegi-r61/CriticPython
TMPDIR=/fast/scratch/hyaku/kasegi-r61/CriticPython git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kasegi-shokunin /fast/scratch/hyaku/kasegi-r61/CriticPython/clone
TMPDIR=/fast/scratch/hyaku/kasegi-r61/CriticPython git -C /fast/scratch/hyaku/kasegi-r61/CriticPython/clone rev-parse --show-toplevel
TMPDIR=/fast/scratch/hyaku/kasegi-r61/CriticPython git -C /fast/scratch/hyaku/kasegi-r61/CriticPython/clone checkout --detach 13c8060b343e002339ffd72da37ff74514f82765
```
Top-level output was `/fast/scratch/hyaku/kasegi-r61/CriticPython/clone` before checkout. Checkout output: `HEAD is now at 13c8060 round-61: confine python probe paths and admit sourced F42 SQLite account`.

Driver below was created only in scratch. Executed from `/fast/scratch/hyaku/kasegi-r61/CriticPython`:
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/CriticPython PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/kasegi-r61/CriticPython/probe.py
```
Driver exit 0; Python 3.14.8. Each subprocess uses `/usr/bin/python3`, `--ledger` and `--root` absolute paths, fixture cwd, TMPDIR set, and ESC=../.. Base bytes were obtained by `git -C /fast/scratch/hyaku/kasegi-r61/CriticPython/clone show c33d24ddd11abf1ebdea0dccf7327e9069dd9104:corpus/instruments/figure-audit.py` (exit 0).
- base SHA256: 35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2
- pin SHA256: 051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9 (matches frozen C1 digest).

## Decisive counterexample
Minimal derive: `python3 corpus/instruments/"../../outside.py"`.
Outside script (only MARK creation plus count; all files in seat scratch):
```python
from pathlib import Path
Path('MARK').write_text('harmless\n')
print(35)
```
Both base and pin: exit=0, markers=1. Pin exact stdout:
```text
FIG quote-traversal recorded=35 derived=35 ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
```
No stderr. The executed script is fixture-root `outside.py`, not under its corpus/instruments directory. This is stronger evidence than a gate-only boolean: execution occurred and the audit reported OK.

## Complete observed matrix
Each row is base exit/markers → pin exit/markers. Paths below are shell derive arguments; each command begins `python3 `. `{root}` is expanded by the fixture driver to its absolute fixture path. All 0 exits output derived=35 and `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0`; all 2 exits have empty stdout and stderr `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=<case>`. All markers counted at the fixture root.

| Case | Script argument(s) | Base → pin |
|---|---|---|
| P1 | `corpus/instruments/../../outside.py` | 0/1 → 2/0 |
| P2 | `corpus/instruments/../../../outside-parent.py` | 0/1 → 2/0 |
| P3 | `corpus/instruments/link.py` | 0/1 → 2/0 |
| absolute | `{root}/outside.py` | 2/0 → 2/0 |
| inside | `corpus/instruments/ok.py` | 0/0 → 0/0 |
| normalized | `corpus/instruments/../instruments/ok.py` | 0/0 → 0/0 |
| quote-whole-inside | `"corpus/instruments/ok.py"` | 2/0 → 2/0 |
| quote-leaf-inside | `corpus/instruments/"ok.py"` | 0/0 → 0/0 |
| quote-traversal | `corpus/instruments/"../../outside.py"` | 0/1 → 0/1 |
| single-quote-traversal | `corpus/instruments/'../../outside.py'` | 0/1 → 0/1 |
| escaped-traversal | `corpus/instruments/\..\/\..\/outside.py` | 0/1 → 0/1 |
| variable-traversal | `corpus/instruments/$ESC/outside.py` | 0/1 → 0/1 |
| quoted-variable-traversal | `corpus/instruments/"$ESC"/outside.py` | 0/1 → 0/1 |
| brace-traversal | `corpus/instruments/{../../outside.py,ok.py}` | 0/1 → 0/1 |
| glob-symlink-target | `corpus/instruments/link*.py` | 0/1 → 0/1 |
| symlink-dir | `corpus/instruments/linkdir/outside.py` | 0/1 → 2/0 |
| quoted-symlink-dir | `corpus/instruments/"linkdir"/outside.py` | 0/1 → 0/1 |
| glob-symlink-dir | `corpus/instruments/linkdi?/outside.py` | 0/1 → 0/1 |
| quoted-symlink-target | `corpus/instruments/"link.py"` | 0/1 → 0/1 |
| escaped-symlink-target | `corpus/instruments/lin\k.py` | 0/1 → 0/1 |
| symlink-inside | `corpus/instruments/inlink.py` | 0/0 → 0/0 |
| normal-dot-out | `corpus/instruments/./../../outside.py` | 0/1 → 2/0 |
| double-slash-out | `corpus/instruments//../../outside.py` | 0/1 → 2/0 |
| backslash-out | `corpus/instruments/..\../outside.py` | 1/0 → 1/0 |

For backslash-out, both stdout values were exactly:
```text
FIG backslash-out recorded=35 derived=UNAVAILABLE reason=derive-exit-2 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
```
No stderr; this is admitted-but-failed execution, not gate refusal. A Linux backslash is not a directory separator. Whole-path quoting over-refusal already existed in base, so it is not a new regression. Eleven expansion/encoding variants still execute out-of-directory on both revisions.

## Evidence, boundary, and smallest safe correction
All source references below refer to implementation pin 13c8060b343e002339ffd72da37ff74514f82765 (the pinned clone was inspected).
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:172-187`: `head.split()` plus realpath on undecoded source. The filesystem sees literal quote/escape/expansion bytes, while bash subsequently removes/expands them. Nonexistent literal paths can still pass the startswith test.
- Same file `:72-79`: approved source is later passed to `bash -c`, allowing that disagreement to become execution.
- Same file `:173-178` and `:29-31`: universal-sounding confinement prose overstates behavior demonstrated by this review.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/claims.json:13-16,28-31`: frozen predicate is expressly the named probes, and undecoded quoting/expansion is an explicit residual. These attacks instantiate that residual; they are not grounds to silently replace the frozen predicate.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:29-32,41-51`: named probe payloads differ from this seat's harmless payload: the committed outside scripts create a marker but print no count. Therefore this seat's base P1–P3 exit 0 is intentional, not evidence contradicting the frozen base exit 1. The custom fixtures corroborate refusal/admission shape only; they do not replace the named runner or full C1 verification.

Smallest safe current-round correction: keep the frozen named-predicate limitation visible wherever confinement is described; do not label this a sandbox or universal symlink/quote defense. No production correction applied. If universal path confinement is proposed separately, a fix must align the validated script token with the executed argv (decode supported literal quoting/escapes, reject unsupported expansions, and execute that same validated argv); merely applying shlex then passing original text to bash does not address variable/brace/glob expansion. This is fixable but outside frozen acceptance. No new regression among tested cases; no C2 conclusion.

## Self-evaluation
Accuracy 4/5: exact exits/markers and pin digest, but custom payload intentionally differs from named runner. Completeness 4/5: all assigned attack classes covered, not exhaustive shell semantics. Clarity 4/5: boundary and full matrix included; reproduction appendix is necessarily long. Actionability 4/5: minimal retained reproducer and correction boundary, no implementation by read-only contract. Conciseness 4/5: receipt source retained to survive mandatory scratch cleanup. Overall 4.0; improvements: preserve boundary in public prose, use structured execution only if a broader contract is separately adopted. User agreement expected because residual and named predicate are kept distinct.

## Reproduction appendix: exact scratch driver
```python
import os, sys, json, subprocess, pathlib, hashlib, concurrent.futures
S = pathlib.Path('/fast/scratch/hyaku/kasegi-r61/CriticPython')
C = S / 'clone'
os.environ['TMPDIR'] = str(S)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
base = subprocess.run(['git','-C',str(C),'show','c33d24ddd11abf1ebdea0dccf7327e9069dd9104:corpus/instruments/figure-audit.py'],capture_output=True,check=True).stdout
(S/'base.py').write_bytes(base)
instruments = {'base': S/'base.py', 'pin': C/'corpus/instruments/figure-audit.py'}
cases = {
 'P1': 'python3 corpus/instruments/../../outside.py',
 'P2': 'python3 corpus/instruments/../../../outside-parent.py',
 'P3': 'python3 corpus/instruments/link.py',
 'absolute': 'python3 {root}/outside.py',
 'inside': 'python3 corpus/instruments/ok.py',
 'normalized': 'python3 corpus/instruments/../instruments/ok.py',
 'quote-whole-inside': 'python3 "corpus/instruments/ok.py"',
 'quote-leaf-inside': 'python3 corpus/instruments/"ok.py"',
 'quote-traversal': 'python3 corpus/instruments/"../../outside.py"',
 'single-quote-traversal': "python3 corpus/instruments/'../../outside.py'",
 'escaped-traversal': r'python3 corpus/instruments/\..\/\..\/outside.py',
 'variable-traversal': 'python3 corpus/instruments/$ESC/outside.py',
 'quoted-variable-traversal': 'python3 corpus/instruments/"$ESC"/outside.py',
 'brace-traversal': 'python3 corpus/instruments/{../../outside.py,ok.py}',
 'glob-symlink-target': 'python3 corpus/instruments/link*.py',
 'symlink-dir': 'python3 corpus/instruments/linkdir/outside.py',
 'quoted-symlink-dir': 'python3 corpus/instruments/"linkdir"/outside.py',
 'glob-symlink-dir': 'python3 corpus/instruments/linkdi?/outside.py',
 'quoted-symlink-target': 'python3 corpus/instruments/"link.py"',
 'escaped-symlink-target': r'python3 corpus/instruments/lin\k.py',
 'symlink-inside': 'python3 corpus/instruments/inlink.py',
 'normal-dot-out': 'python3 corpus/instruments/./../../outside.py',
 'double-slash-out': 'python3 corpus/instruments//../../outside.py',
 'backslash-out': r'python3 corpus/instruments/..\../outside.py',
}
marker_source = "from pathlib import Path\nPath('MARK').write_text('harmless\\n')\nprint(35)\n"
(S/'outside-parent.py').write_text(marker_source)

def probe(item):
 label, instr, name, text = item
 r = S/(label+'-'+name)
 d = r/'corpus/instruments'; d.mkdir(parents=True)
 (r/'outside.py').write_text(marker_source)
 (d/'ok.py').write_text('print(35)\n')
 (d/'link.py').symlink_to(r/'outside.py')
 (d/'linkdir').symlink_to(r, target_is_directory=True)
 (d/'inlink.py').symlink_to(d/'ok.py')
 cmd = text.replace('{root}',str(r))
 ledger = r/'ledger.json'
 ledger.write_text(json.dumps({'figures':[{'id': name,'record':'scratch','recorded':'35','derive':cmd,'want':'35'}]}))
 argv = [sys.executable,str(instr),'--ledger',str(ledger),'--root',str(r)]
 p = subprocess.run(argv,cwd=r,env=dict(os.environ,ESC='../..'),text=True,capture_output=True,timeout=15)
 return {'revision': label, 'case': name,'derive':cmd,'argv':argv,'cwd':str(r),'exit':p.returncode,'markers':int((r/'MARK').exists()),'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
items = [(label,instr,name,text) for label,instr in instruments.items() for name,text in cases.items()]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 results = list(pool.map(probe,items))
print('python='+sys.version.split()[0])
for label,path in instruments.items(): print(label+' sha256='+hashlib.sha256(path.read_bytes()).hexdigest())
for result in results: print(json.dumps(result,sort_keys=True))

```

## Cleanup receipt
Executed from `/fast/scratch/hyaku/kasegi-r61`:
```sh
rm -rf -- /fast/scratch/hyaku/kasegi-r61/CriticPython && test ! -e /fast/scratch/hyaku/kasegi-r61/CriticPython && printf 'cleanup exit=0 scratch_absent=yes\n'
```
Exit 0; exact output: `cleanup exit=0 scratch_absent=yes`. Scratch driver, shared clone, fixtures and harmless MARK files removed; driver source, decisive output patterns and full observed matrix retained above.
