# R48Probe12 — duplicate box 1

## Scope and axes
Axes: canonical-form defect detection, reproducibility, isolation/restoration. Author-side grammar only; no promotion or semantic-truth judgment. Read `/home/vgpnk/.omp/agent/RULES.md`, Godspeed skill, frozen protocol source, and round-47 R1/R2 routes. R1's four-box canonical-form repair is relevant; R2's plain-target counter is not changed or exercised.

## Mutant and expected detector
Copied `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` to `/fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md`. Inserted an exact duplicate of original lines 5–6 immediately after line 6: box 1 plus its evidence line. Boxes 2–4 remained byte-for-byte unchanged. Removed only those two inserted lines to restore.

Duplicating a required box is not permitted by the exact four-box grammar. Expected pristine/restored: exit 0, `SF-CLEAN`. Expected mutant: exit 1, `SF-BOX`, because the parser encounters the repeated first label where it requires the second label. No predicate or checker changes.

Frozen checker SHA256 before and after: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`.

## Full detector commands and observed output
All detector runs used this exact command; the following `echo` captures the detector status, not the wrapper's status:

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md; echo "exit=$?"
```

Pristine positive:
```text
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

Mutant, first run:
```text
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

Mutant, repeated without changing bytes:
```text
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

Restored:
```text
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

## Hash and restoration receipts
Initial command:
```sh
mkdir -p /fast/scratch/hyaku/kasegi-r48/R48Probe12 && cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md && sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py; echo "exit=$?"
```
Output:
```text
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
exit=0
```

Mutant hash command:
```sh
sha256sum /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md
```
Output:
```text
051952e0948ad2def1ddab609a84b64570f151c242729e89008e3382e5f456ca  /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md
```

Restoration command (followed by the restored detector command above):
```sh
sha256sum /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py; cmp /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md; echo "cmp_exit=$?"
```
Output:
```text
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /fast/scratch/hyaku/kasegi-r48/R48Probe12/SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
cmp_exit=0
```

## Verdict
**Killed.** Positive and restored controls pass; the duplicate-box mutant fails twice with stable `SF-BOX` and exit 1. Expected and observed agree. No frozen-claim defeat found by this probe. Exact original scratch bytes restored before cleanup; canonical and checker hashes unchanged. No production edits, tool installs, target tests, builds, commits, delegation, or background jobs.

Operational note: the first setup attempt requested the not-yet-created scratch as process cwd and therefore failed before executing any command (`Working directory does not exist`). Retried from `/fast/scratch` using absolute write paths; setup succeeded. Receipts saved here before removing the named scratch directory.
