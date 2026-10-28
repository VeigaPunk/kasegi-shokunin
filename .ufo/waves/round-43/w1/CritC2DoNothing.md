# CritC2DoNothing — do-nothing controls for C2, scored with the frozen counters

Seat: CritC2DoNothing (leaf critic, receipt-only, no subagent dispatch).
Axes under attack: `coverage` (C2, score 8 held) and `depth:verifiability` (C2's counting commands).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Scratch: `/fast/scratch/hyaku/kasegi-r43/CritC2DoNothing` (removed before yield).
No network fetches; no tools installed; no mutating git command anywhere.

## Artifacts measured (read-only)

| artifact | sha256 | lines | bytes |
|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py` (lands as `corpus/instruments/claim-package-check.py`) | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` | 802 | 32520 |
| `.ufo/waves/round-43/w1/ExecGateSelftest.selftest.py` (the `--selftest` body; splice pending) | `04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17` | 616 | — |
| assembled landing layout `fixtures/claim-package/` (exemplar + defect-1..9, `expected-rule` stripped, 99 files) | tree aggregate `2722c7a141aabf6fa3085973865a6bb0e9400f0f5363cfb773cbec8692a580c7` | — | — |

Assembled from `ExecExemplarPackage.*` (bare names; manifest at `evidence/manifest.json`) and
`ExecGateFixtures.defect-1-missing-file … defect-9-secret`. At base `ab98fac9` both
`corpus/instruments/claim-package-check.py` and `corpus/instruments/fixtures/claim-package/` are absent
(`ls` → No such file or directory; the base export has 144-line SOURCES.md), so every C2 gate counter is
unrunnable there: the do-nothing/before state is control zero, already recorded in
`.ufo/waves/round-43/c2-controls/before.txt`.

## 1. Counter audit — what the frozen counters actually execute

C2 has eleven counting commands (`claims.json`). Four mention the gate; seven are tree counters:

```
 1 [GATE] python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar -> rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
 2 [GATE] python3 corpus/instruments/claim-package-check.py --selftest -> selftest cases=10 failures=0 exit=0
 3 [GATE] grep -c '^RULE ' <(python3 ... exemplar) -> 8
 4 [GATE] ls corpus/instruments/fixtures/claim-package/ | grep -c '^defect-' -> 9
 5..11 [tree] SOURCES rows, knowledge file count, capture-binding, recheck-audit, frontier, census
```

Measured facts:
- No counting command executes the gate over a defect fixture. Command 4 counts directory **names**:
  `mkdir` nine empty `defect-*` dirs → `ls | grep -c '^defect-'` = `9` with `find -type f | wc -l` = `0`.
- Command 2 is the artifact grading itself. It is a self-report; a stand-in can print the identical line
  (measured below).
- The discriminator ("any of the nine defect fixtures accepted (exit 0)") exists only in `kill_rule`
  prose, not in any counting command.

Baseline of the real artifacts (so the controls are scored against something honest):

```
$ python3 <gate> <fixtures>/exemplar
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
... (8 pass lines) ...
package=.../exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
$ python3 <gate> <fixtures>/defect-*/            # nine separate runs, one line each:
defect-1-missing-file  exit=1 | RULE R-FILES verdict=fail detail=missing=1,bad=0
defect-2-digest        exit=1 | RULE R-MANIFEST verdict=fail detail=artifacts=4,digest-bad=1
defect-3-negative      exit=1 | RULE R-MANIFEST verdict=fail detail=artifacts=4,positive=0
defect-4-escape        exit=1 | RULE R-MANIFEST verdict=fail detail=artifacts=4,escape=1
defect-5-redaction     exit=1 | RULE R-REDACT verdict=fail detail=redactions=empty
defect-6-custodian     exit=1 | RULE R-CUSTODIAN verdict=fail detail=chain=3,head=mismatch
defect-7-reviewer      exit=1 | RULE R-STATUS verdict=fail detail=reviewer=not-distinct
defect-8-marker        exit=1 | RULE R-REPORT verdict=fail detail=marker=absent
defect-9-secret        exit=1 | RULE R-NOSECRET verdict=fail detail=hits=1,first=provenance.json,shape=credential
```

Each fixture fails exactly its own rule (`pass=7 fail=1 verdict=DEFECT exit=1`); the exemplar is not a
blanket reject. The delivered `--selftest` returns `verdict=missing exit=2` because the splice is not in
the delivered bytes yet; run standalone against the same gate it grades 10/0:

```
$ python3 ExecGateSelftest.selftest.py --gate <gate> --fixtures <fixtures> --work <scratch>/selftest-work-real
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=R-FILES verdict=pass
... case=2..9 likewise, each observed == expected ...
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=0
exit=0
```

And the same selftest run with the always-pass stand-in as `--gate`:

```
$ python3 ExecGateSelftest.selftest.py --gate standins/always-pass/claim-package-check.py --fixtures <fixtures> --work <scratch>/selftest-work-degenerate
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=none verdict=fail detail=verdict=well-formed
... case=2..9 identical fail/verdict=well-formed ...
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=9
exit=1
```

So the *honest* selftest does reject an always-pass gate 9/9. The defect is not in the selftest; it is
that the frozen counters never invoke a selftest that the delivered artifact did not supply.

## 2. The four controls

### C-A — always-pass gate stand-in

`standins/always-pass/claim-package-check.py` (reads no package bytes; prints the eight literal `RULE
... verdict=pass` lines plus the summary; its own `--selftest` prints ten pass lines and
`selftest cases=10 failures=0`).

```
$ python3 <C-A> <real exemplar>          -> package=.../exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED   exit=0
$ python3 <C-A> --selftest               -> selftest cases=10 failures=0                                     exit=0
$ grep -c '^RULE ' <(python3 <C-A> ...)  -> 8
$ ls <real fixtures> | grep -c '^defect-' -> 9
$ for d in <real fixtures>/defect-*/; do python3 <C-A> "$d"; done
  defect-1..9  exit=0 WELL-FORMED failing=-        → defect-exits=0/9
```

### C-B — presence-only gate

`standins/presence-only/claim-package-check.py`: the entire gate is six `os.path.isfile` calls; no file
byte is read, no JSON parsed. `--selftest` prints `failures=0` regardless.

```
$ python3 <C-B> <junk-twin: six zero-byte files>
RULE R-FILES verdict=pass detail=present
... (8 pass lines, detail=present) ...
package=.../junk-twin rules=8 pass=8 fail=0 verdict=WELL-FORMED
exit=0

$ python3 <C-B> <real exemplar>  -> rules=8 pass=8 fail=0 exit=0
$ python3 <C-B> --selftest       -> selftest cases=10 failures=0 exit=0   (while it catches 1/9):
  defect-1-missing-file exit=1 DEFECT failing=R-FILES
  defect-2..9           exit=0 WELL-FORMED            → defect-exits=1/9
```

It catches only the one fixture class that is literally an absent file (`defect-1`), and its own
selftest still reports `failures=0`.

### C-C — exemplar that is a copy of a defect fixture, defect masked by blanket accept

Masked exemplar = byte copy of `defect-8-marker` (report.md lacks `No submission performed`), gate =
`standins/blanket-accept/claim-package-check.py` (every rule emits `verdict=pass detail=blanket`).

```
$ python3 <blanket-accept> <masked-real: defect-8 copy>
package=.../masked-real rules=8 pass=8 fail=0 verdict=WELL-FORMED
exit=0
$ python3 <blanket-accept> over the real nine  → defect-exits=0/9, selftest cases=10 failures=0 exit=0
```

Both branches of this control die, opposite ways:
- blanket-accept gate: exemplar counter passes, nine-DEFECT exits = 0/9;
- real gate on the same masked exemplar: the defect is not maskable —
  `RULE R-REPORT verdict=fail detail=marker=absent`, `rules=8 pass=7 fail=1 verdict=DEFECT exit=1`,
  so the exemplar counter itself fails.

### C-D — junk-twin (six empty files) through the real gate

`pkgs/junk-twin/` = `report.md`, `claim_checklist.md`, `custodian-receipts.json`, `provenance.json`,
`status.json`, `evidence/manifest.json`, each 0 bytes (verified by walk: six files, size 0).

```
$ python3 <real gate> pkgs/junk-twin
RULE R-FILES verdict=fail detail=missing=0,bad=6
RULE R-MANIFEST verdict=fail detail=parse:evidence_manifest.json
RULE R-REDACT verdict=fail detail=parse:evidence_manifest.json
RULE R-CUSTODIAN verdict=fail detail=parse:evidence_manifest.json
RULE R-PROVENANCE verdict=fail detail=parse:provenance.json
RULE R-STATUS verdict=fail detail=parse:evidence_manifest.json
RULE R-REPORT verdict=fail detail=parse:evidence_manifest.json
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=.../junk-twin rules=8 pass=1 fail=7 verdict=DEFECT exit=1
```

The real gate rejects it. The single pass is R-NOSECRET, which has nothing to scan; the verdict is
still DEFECT exit=1, and a blanket-accept gate would print `pass=8 exit=0` on the same bytes (measured
above with C-B/C-C), so the pass is a property of an empty package, not of a lenient rule. Note also
`<gate> <missing dir>` → `verdict=ERROR exit=2`, so the junk-twin red is not an error-path artefact.

## 3. Score against the three-part after-state

After-state as stated: `rules=8 pass=8`, `selftest cases=10 failures=0`, nine DEFECT exits.

| control | rules=8 pass=8 | selftest cases=10 failures=0 | nine DEFECT exits | reaches after-state? |
|---|---|---|---|---|
| C-A always-pass | yes, exit 0 | yes, exit 0 (forged) | **0/9** | no |
| C-B presence-only | yes, exit 0 (also on six empty files) | yes, exit 0 | **1/9** | no |
| C-C masked exemplar + blanket accept | yes, exit 0 | yes, exit 0 | **0/9** | no |
| C-D junk-twin, real gate | — (not the exemplar) | — | n/a: real gate returns `pass=1 fail=7 verdict=DEFECT exit=1` | no |

Where each dies, precisely:
- C-A dies only at the nine-DEFECT limb. It is byte-identical to the real artefact for counters 1-4.
- C-B dies at the nine-DEFECT limb (1/9) and is already disproved by the junk-twin: it prints
  `rules=8 pass=8` for six zero-byte files, which the real gate refuses (`pass=1 fail=7`).
- C-C dies twice: with a blanket gate it is 0/9; with the real gate its exemplar is rejected by
  R-REPORT. The defect cannot be masked by the accept side alone.
- C-D is the only control that is a *package*, not a gate; the real gate kills it outright (7 fail,
  exit 1). It does not touch the counters at all.

**No degenerate control reaches the after-state as stated.** The claim is reachable-by-work-only on
the three-part definition.

## 4. Where the frozen counters, as written, cannot see that

Scored against the **eleven frozen counting commands**, C-A passes every one of them: 1, 2, 3 come
straight from its own stdout (`exit=0`, `failures=0`, `8`), and 4 counts the real fixture directory
names, which the gate cannot influence. C-B and C-C likewise pass 1-4 (C-B passes 1 even on six empty
files, measured). Only `kill_rule` prose — "any of the nine defect fixtures accepted (exit 0)", "the
degenerate always-pass control accepted by the selftest" — carries the discrimination, and no frozen
counting command executes either check. In that operational sense the C2 gate limb is *not* reachable
by work only: a ~40-line always-pass script plus the round's tree work satisfies the entire measured
counter set.

Smallest safe correction — one added counting command, verifier-run, independent of the artifact's own
selftest:

```
for d in corpus/instruments/fixtures/claim-package/defect-*/; do
  python3 corpus/instruments/claim-package-check.py "$d" >/dev/null || continue; fail=1; done
  # require exit 1 AND the index-named rule failing, nine times
-> defect-exits=9/9 exit=0
```

Measured on the delivered bytes:

```
$ for d in <fixtures>/defect-*/; do rc=0; out=$(python3 <gate> "$d") || rc=$?; \
    [ "$rc" -eq 1 ] && printf '%s' "$out" | grep -q 'verdict=DEFECT' || bad=$((bad+1)); done
counter9 defects=9 rejecting=9 exit=0
```

With that command added, C-A dies (0/9), C-B dies (1/9) and C-C dies (0/9). Without it, the
`selftest cases=10 failures=0` counter remains a self-report: C-A/C-B/C-C print it while accepting
0/9, 1/9 and 0/9 respectively. The honest selftest is a genuine discriminator (always-pass stand-in
graded `failures=9 exit=1`), but nothing in the frozen counter set re-runs it outside the artifact.

## 5. Same shape in an adjacent C2 counter (secondary, measured)

The SOURCES row counter is `66 -> >=68`. Two junk table rows appended to a scratch copy of the base
SOURCES.md, with no capture, no URL fetch and no mined S067 row, produce:

```
rows after two junk rows: 68      (base: 66)
rows with S067:            0
```

The row counter is satisfied by row count alone; the binding that stops it is the neighbouring
`capture-binding-check records=56 -> 57` and `recheck-audit expected=61 -> 62`, which a junk row does
not move. Not a failure of C2 as written, but the row-count limb should not be read as proof of a
mined row.

## 6. Limits of this review

- The `--selftest` splice is not in the delivered bytes yet: `<gate> --selftest` prints
  `selftest module=.../claim-package-selftest.py verdict=missing exit=2`. I measured the selftest body
  standalone against the same gate and fixtures; the post-splice `--selftest` counter must be run at Y
  by the verifier, and the splice must not change rule verdicts (splice-immune names claimed by
  ExecGateCore are a claim I did not test).
- Self-report forgeries beyond the four controls (summary-only line, skipped case, sibling-dir read)
  belong to MutSelftestDegenerate; I did not duplicate that battery.
- Exemplar content/fabrication is CritExemplarReal's scope; I only tested that the real gate accepts it
  and that a defect copy is rejected.

## 7. Hygiene

- Writes: this receipt only. No deliverable file (receipt-only item). No lane source file touched.
- No mutating git/jj command; no fleet-root or shokuknow access; no PATH writes.
- Tools installed: none. Network: none.
- Scratch `/fast/scratch/hyaku/kasegi-r43/CritC2DoNothing` removed before yield.
