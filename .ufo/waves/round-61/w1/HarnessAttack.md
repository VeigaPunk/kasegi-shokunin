FINDINGS — required refusal cases pass; runner can delete its instrument and return success, and dependency failures can be masked. Named C1 probes match the frozen predicate on this host.

# Axes and scope
Axes: depth:verifiability (C1); coverage (C2 not exercised by this assigned harness review). Read-only production review; no claim amendments, suite, commits, clones, installation, or sibling writes. These are harness defects, not a sandbox claim and not a canonical admission judgment.

Implementation pin: `13c8060b343e002339ffd72da37ff74514f82765`. Frozen claims pin: `6f88f3a7f6b9689b49241e3f4a8e551c57a3f766`. Pinned blobs were extracted with `git -C` into this seat's scratch, not run from a moving checkout. Claims blob equals the lane copy. Receipts below give full digests.

# Counterexamples and smallest safe corrections
1. **Instrument destroyed by its own scratch argument (observed).** With an existing instrument at `/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py` and scratch `/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete`, the runner accepts the file, removes it, prints an empty digest, reports eight Python open failures, then exits **0**. Evidence: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:14-21` checks existence before `rm -rf`; `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:34-38` stores rather than propagates failures. Smallest correction: reject an instrument equal to or beneath canonical scratch before deletion, check digest command success, and make mismatched probe outcomes fail the runner. No production path was placed at risk: only our disposable fixture was removed.
2. **Exit 0 is not the named-predicate verdict (observed).** A Python instrument containing `raise SystemExit(99)` yields all eight `exit=99 markers=0` records and runner exit **0**. `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:24-39` never asserts expected exit, reason, marker count, or derived output; its final echo succeeds. This does not refute the observed normal named probes, and a consumer explicitly comparing records can still reject this output. Smallest correction: explicit expectations for each named case, or unambiguous collector-only labeling plus a mandatory independent predicate checker. Do not treat runner status alone as pass.
3. **Dependency failures can become false evidence (observed).** Exported `find() { return 71; }` simulates dependency failure without touching PATH directories. Runner still reports `markers=0` for every case and exits **0**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:37` uses a pipeline without `pipefail`. Digest pipeline at line 21 also masks `sha256sum` failure (observed in counterexample 1). Conversely a simulated unavailable fixture `python3` exits **127** before any probe records, so that setup failure is correctly fail-closed. Smallest correction: fail on pipeline/command errors and preflight dependencies. Declared baseline at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:10` omits **find (findutils)** and **grep** used at lines 37 and 53, beyond Bash/Python3/coreutils. All dependencies are present on this host (receipt below).
4. **Deletion boundary (review).** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:15-18` canonicalizes scratch then requires `/fast/scratch/hyaku/kasegi-r61/*/*`, before deletion. Missing args, missing/empty instrument, lane root, empty scratch, and seat root all refuse with exit **2** in harmless probes. A pre-existing sentinel under the permitted scratch child survives both missing-instrument cases. The guard does not enforce caller seat ownership: any qualifying seat/child can be selected [static inference], so it is not a general ownership boundary. No sibling path was tested. Smallest safe correction if ownership isolation is intended: require an explicit owned root and fresh child, rather than trusting the round-wide prefix. This is distinct from C1, which is not a sandbox.
5. **Symlink selftest is not vacuous on the examined failure mode.** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:291-295` swallows symlink creation errors, but the missing link then resolves inside the instrument directory (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:183-187`), so it is admitted to execution and audit exits **1**, not the selftest's expected **2** (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:335`, compared at line 308). Focused present/absent-link probes below observe exactly 2/refusal versus 1/stale. Runner itself has checked `ln -sf` under `set -e` at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:12,32`. Smallest clarity correction: report symlink setup failure explicitly rather than hide it; no observed false pass from missing-link setup.
6. **Selftest host dependency is explicit residual, not new coverage.** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:304-306` locates Bash then launches bare `python` (not `sys.executable`/`python3`); only return code is graded at line 308. Host has `/usr/bin/python` and `/usr/bin/python3`. Missing `python` would cause child exit 127 and failure tallies [static inference]; missing Bash can raise before summary [static inference]. This matches the frozen residual `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/claims.json:32`. Smallest correction: use `sys.executable` plus explicit Bash-unavailable reporting; do not reinterpret current host-conditional tally as portable success. No full selftest or unrelated suite was run.

# Exact execution and decisive receipts
Every subprocess below used cwd `/fast/scratch/hyaku/kasegi-r61/HarnessAttack` and environment `os.environ` overridden with `TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack`. The scratch was created with `mkdir -p /fast/scratch/hyaku/kasegi-r61/HarnessAttack` (exit 0). The runner and instrument were written byte-for-byte from the successful pinned `git show` stdout using `pathlib.Path.write_bytes`.

Additional fixtures were constructed in Python exactly as follows (paths below all absolute via S):
```python
S = '/fast/scratch/hyaku/kasegi-r61/HarnessAttack'
pathlib.Path(S+'/keep').mkdir()
pathlib.Path(S+'/keep/sentinel').write_text('retain')
pathlib.Path(S+'/broken.py').write_text('raise SystemExit(99)\n')
pathlib.Path(S+'/self-delete').mkdir()
pathlib.Path(S+'/self-delete/instrument.py').write_bytes(pathlib.Path(S+'/figure-audit.py').read_bytes())
froot = pathlib.Path(S+'/link-witness')
(froot/'corpus/instruments').mkdir(parents=True)
(froot/'out.py').write_text('print(35)\n')
(froot/'one.json').write_text(json.dumps({'figures':[{'id':'link-witness','record':'probe','recorded':'35','derive':'python3 corpus/instruments/link.py','want':'35'}]}))
(froot/'corpus/instruments/link.py').symlink_to(froot/'out.py')
# After the symlink-present probe, before symlink-absent:
(froot/'corpus/instruments/link.py').unlink()
```
Sentinel observed afterward: `sentinel-retained retain`. No production deletion was attempted. Normal eight-case output below matches C1's named runner predicate; other C1 counting commands and C2 are outside this seat's checks.

```json
{
  "command": "git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 13c8060b343e002339ffd72da37ff74514f82765:.ufo/waves/round-61/controls/c1-probe-run-r61.sh",
  "exit": 0,
  "sha256": "bd5ac6054479aba578db855122afd2f9627a464bbc8b56d6d50f1ae9e71932f4",
  "file": ".ufo/waves/round-61/controls/c1-probe-run-r61.sh"
}
```
```json
{
  "command": "git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 13c8060b343e002339ffd72da37ff74514f82765:corpus/instruments/figure-audit.py",
  "exit": 0,
  "sha256": "051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9",
  "file": "corpus/instruments/figure-audit.py"
}
```
```json
{
  "command": "git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766:.ufo/waves/round-61/claims.json",
  "exit": 0,
  "matches_lane_claims": true
}
```
## missing-args
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh
```
Exit: 2
```text
stdout:
HARNESS-USAGE want-instrument-and-scratch
stderr:
```
## one-arg
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py
```
Exit: 2
```text
stdout:
HARNESS-USAGE want-instrument-and-scratch
stderr:
```
## missing-instrument
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/not-found.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack/keep
```
Exit: 2
```text
stdout:
HARNESS-USAGE not-a-file /fast/scratch/hyaku/kasegi-r61/HarnessAttack/not-found.py
stderr:
```
## empty-instrument
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh '' /fast/scratch/hyaku/kasegi-r61/HarnessAttack/keep
```
Exit: 2
```text
stdout:
HARNESS-USAGE missing-instrument
stderr:
```
## lane-root
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py /home/vgpnk/Projects/shokunin/kasegi-shokunin
```
Exit: 2
```text
stdout:
HARNESS-USAGE unsafe-scratch /home/vgpnk/Projects/shokunin/kasegi-shokunin
stderr:
```
## empty-scratch
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py ''
```
Exit: 2
```text
stdout:
HARNESS-USAGE missing-scratch
stderr:
```
## seat-root
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack
```
Exit: 2
```text
stdout:
HARNESS-USAGE unsafe-scratch /fast/scratch/hyaku/kasegi-r61/HarnessAttack
stderr:
```
## normal-runner
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack/normal
```
Exit: 0
```text
stdout:
instrument=/fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:26:20Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/HarnessAttack/normal/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
stderr:
```
## broken-instrument
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/broken.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack/broken-run
```
Exit: 0
```text
stdout:
instrument=/fast/scratch/hyaku/kasegi-r61/HarnessAttack/broken.py sha256=237f6b53709bf513
run-utc=2026-11-04T14:26:20Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=99 markers=0 :: 
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=99 markers=0 :: 
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=99 markers=0 :: 
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/HarnessAttack/broken-run/outside-P4-absolute-out.py exit=99 markers=0 :: 
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=99 markers=0 :: 
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=99 markers=0 :: 
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=99 markers=0 :: 
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=99 markers=0 :: 
stderr:
```
## missing-find
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash -c 'find() { return 71; }; export -f find; exec bash "$@"' dependency-probe /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack/missing-find
```
Exit: 0
```text
stdout:
instrument=/fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:26:20Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/HarnessAttack/missing-find/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
stderr:
```
## instrument-inside-scratch
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete
```
Exit: 0
```text
stdout:
instrument=/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py sha256=
run-utc=2026-11-04T14:26:34Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/outside-P4-absolute-out.py exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py': [Errno 2] No such file or directory
stderr:
sha256sum: /fast/scratch/hyaku/kasegi-r61/HarnessAttack/self-delete/instrument.py: No such file or directory
```
## fixture-python-missing
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash -c 'python3() { return 127; }; export -f python3; exec bash "$@"' dependency-probe /fast/scratch/hyaku/kasegi-r61/HarnessAttack/runner.sh /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py /fast/scratch/hyaku/kasegi-r61/HarnessAttack/no-python3
```
Exit: 127
```text
stdout:
instrument=/fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:26:34Z
stderr:
```
## symlink-present
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack python3 /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py --ledger /fast/scratch/hyaku/kasegi-r61/HarnessAttack/link-witness/one.json --root /fast/scratch/hyaku/kasegi-r61/HarnessAttack/link-witness
```
Exit: 2
```text
stdout:
stderr:
FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=link-witness
```
## symlink-absent
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack python3 /fast/scratch/hyaku/kasegi-r61/HarnessAttack/figure-audit.py --ledger /fast/scratch/hyaku/kasegi-r61/HarnessAttack/link-witness/one.json --root /fast/scratch/hyaku/kasegi-r61/HarnessAttack/link-witness
```
Exit: 1
```text
stdout:
FIG link-witness recorded=35 derived=UNAVAILABLE reason=derive-exit-2 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
stderr:
```
## host-dependencies
```sh
TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack bash -c 'for x in bash python python3 realpath rm mkdir sha256sum cut date cp ln find wc cat head tr grep; do command -v "$x" || exit; done'
```
Exit: 0
```text
stdout:
/usr/bin/bash
/usr/bin/python
/usr/bin/python3
/usr/bin/realpath
/usr/bin/rm
/usr/bin/mkdir
/usr/bin/sha256sum
/usr/bin/cut
/usr/bin/date
/usr/bin/cp
/usr/bin/ln
/usr/bin/find
/usr/bin/wc
/usr/bin/cat
/usr/bin/head
/usr/bin/tr
/usr/bin/grep
stderr:
```

# Cleanup and handoff
Exact cleanup command: `env TMPDIR=/fast/scratch/hyaku/kasegi-r61/HarnessAttack rm -rf -- /fast/scratch/hyaku/kasegi-r61/HarnessAttack`; exit 0, no output. Receipts preserved in this report; scratch removed. No tools installed or updated. Production code intentionally unchanged.

No canonical judgment issued. Harness defects are fixable without changing frozen predicates; any claim of broader confinement or portable selftest success would exceed the explicitly scoped evidence.
