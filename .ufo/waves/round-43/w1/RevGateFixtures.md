# RevGateFixtures — round-43 C2 defect-fixture attribution review (receipt only)

- Lane: `kasegi-shokunin`, round 43. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
- Seat: `RevGateFixtures` (leaf reviewer; no subagent, no swarm, no second judge). Receipt-only item.
- Frozen claims read first and never edited: `.ufo/waves/round-43/claims.json` (C2: `claim-package-check.py`,
  eight rules, exemplar, nine defect fixtures, `--selftest` cases=10, degenerate always-pass control rejected).
- Review clock: 2026-10-28T16:41Z–16:56Z. The gate was revised at 16:50:46Z and the exemplar/fixtures at
  16:50:36Z–16:51:53Z; the whole battery was re-run against those bytes (hashes above are the re-run's).

## Subject under review (all hashes re-measured, not quoted)

| artifact | path | sha256 |
|---|---|---|
| gate CLI | `.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py` | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` |
| fixtures index | `.ufo/waves/round-43/w1/ExecGateFixtures.index.txt` | `abe4460a142550e4f2b09579357037a28bfeddd8e22f4c326177a02b938ab7b4` |
| selftest (consumer) | `.ufo/waves/round-43/w1/ExecGateSelftest.selftest.py` | `04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17` |

Exemplar base: reconstructed in scratch from the w1 `ExecExemplarPackage.*` deliverables with the mapping the
fixtures receipt states (`report.md`, `claim_checklist.md`, `custodian-receipts.json`, `provenance.json`,
`status.json` at the package root; `manifest.json` plus the four artifacts under `evidence/`). Gate on that
reconstruction: 8/8 pass, exit 0 (block B).

Nine fixture dirs under `.ufo/waves/round-43/w1/ExecGateFixtures.defect-*`; tree sha256 (formula `(cd <dir> && find .
-type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)`):

| fixture | files | bytes | tree sha256 |
|---|---|---|---|
| defect-1-missing-file | 10 | 18244 | `967fb599c2a9cc92395f7086f19bb1afd0f43639bb4f9ff40cfa13f306857c63` |
| defect-2-digest | 11 | 20337 | `a92290b0a34d4723fc189a5130eb8c9e98bda02c9a6704cab903653d0db27029` |
| defect-3-negative | 11 | 20336 | `e27317df1fef1c043ad15df8e09d76b1a1e92344f372e20b17b93dfc876ad97d` |
| defect-4-escape | 11 | 20331 | `a1a2b74f6c4b76716801c066784b99c0299be307fe7906175a368dec15c8f39a` |
| defect-5-redaction | 11 | 18473 | `f81ea3a6e872c481e58fed41f92d6885b9aae5f8b798f83555b71cd5fd4d434b` |
| defect-6-custodian | 11 | 20337 | `e831d65ec990dca189209539b17440aaafcacf3858481b483c726d28c15fcbcf` |
| defect-7-reviewer | 11 | 20338 | `16d729aec4edbff9a40c949930376501b44138f52a50a7f0959470cf5256792f` |
| defect-8-marker | 11 | 20335 | `0b932b7b6ea320b0c84f1f7f582aeec995a68c6aa32f2f9a5644d36150eda216` |
| defect-9-secret | 11 | 20392 | `563043c8504bdd4239263072fc21a15e8d125bda46a2f61649574935db423459` |

These match the fixtures receipt's own table exactly (block I).

## Answers to the three questions

**1. Does each fixture fail for its OWN rule and not another?** Yes, all nine. Each prints exactly eight
`RULE` lines, one `verdict=fail`, and the failing id equals the fixture's `expected-rule` file, the index line,
and the selftest's `expected=` column. `package=… rules=8 pass=7 fail=1 verdict=DEFECT exit=1` in every case.
The failing `detail` token is the rule's own limb and matches the documented delta (no incidental limb fired):

| fixture | expected | observed failing rule | fail detail | assessed cause |
|---|---|---|---|---|
| defect-1-missing-file | R-FILES | R-FILES | `missing=1,bad=0` | `claim_checklist.md` absent |
| defect-2-digest | R-MANIFEST | R-MANIFEST | `artifacts=4,digest-bad=1` | one byte appended to `evidence/source-capture.txt` (`0x78`) |
| defect-3-negative | R-MANIFEST | R-MANIFEST | `artifacts=4,positive=0` | all `polarity` set to `negative` |
| defect-4-escape | R-MANIFEST | R-MANIFEST | `artifacts=4,escape=1` | artifact path gains a `..` component |
| defect-5-redaction | R-REDACT | R-REDACT | `redactions=empty` | `manifest.redactions := []` |
| defect-6-custodian | R-CUSTODIAN | R-CUSTODIAN | `chain=3,head=mismatch` | `head_sha256` := `f`×64 |
| defect-7-reviewer | R-STATUS | R-STATUS | `reviewer=not-distinct` | reviewer identity := `redactions[0].producer` (`exec-exemplar-package`) |
| defect-8-marker | R-REPORT | R-REPORT | `marker=absent` | the literal `No submission performed` removed |
| defect-9-secret | R-NOSECRET | R-NOSECRET | `hits=1,first=provenance.json,shape=credential` | top-level `api_key` := 40 lowercase hex |

No fixture fails for the wrong reason. Two coupling traps were probed and do not fire: the manifest edits in
defect-3/4/5 are resealed into `status.manifest_sha256` (each fixture's recorded digest equals the sha256 of its
own manifest bytes, and R-STATUS passes), and the `expected-rule` marker file is inert metadata — deleting it
from a copy leaves the same single failing rule and `fail=1 exit=1` in all nine (block L).

**2. Is each a full six-file package, so the failure is caused by the one delta?** Eight of nine are six-of-six
regular files (`report.md`, `claim_checklist.md`, `evidence/manifest.json`, `custodian-receipts.json`,
`provenance.json`, `status.json`). defect-1 is five-of-six by design: the absent sixth file *is* its delta. That
choice is minimal-coupling: dropping each contract file from the exemplar in turn shows `claim_checklist.md` is
the only one whose absence reds R-FILES alone (block J: `report.md` also reds R-REPORT; `custodian-receipts.json`
also reds R-CUSTODIAN; `provenance.json` also reds R-PROVENANCE; `status.json` also reds R-STATUS;
`evidence/manifest.json` reds six rules).

**3. Is the delta documented and reproducible from the exemplar?** Documented in `ExecGateFixtures.index.txt`
(one line per fixture) and in the fixtures receipt's delta table; reproducible: an independent rebuild from the
exemplar of the exemplar + the documented delta is **byte-identical to every landed fixture, every file**
(9/9 fixtures, 10/10 or 11/11 files each, block F). Exact per-fixture recipe that reproduces the bytes:

| fixture | exact mutation applied to a copy of the exemplar |
|---|---|
| defect-1 | `rm claim_checklist.md` |
| defect-2 | append `0x78` (`x`) to `evidence/source-capture.txt`; manifest untouched |
| defect-3 | every `evidence/manifest.json.artifacts[].polarity` → `negative`; reseal `status.manifest_sha256` |
| defect-4 | `artifacts[0].path` → `../escape.txt`; reseal |
| defect-5 | `manifest.redactions` → `[]`; reseal |
| defect-6 | `custodian-receipts.json.head_sha256` → `f`×64 |
| defect-7 | `status.claim_review.reviewer.identity` → `exec-exemplar-package` |
| defect-8 | `report.md`: `No submission performed` → `No filing has been made.` |
| defect-9 | `provenance.json.api_key` → `0123456789abcdef0123456789abcdef01234567` |

(`reseal` = recompute sha256 over the new manifest bytes and substitute it for the old value in
`status.json.manifest_sha256`; after reseal the status↔manifest binding re-verifies as `ok` for all nine.)

**Junk-twin control.** A byte-identical copy of the exemplar (`diff -r` exit 0, empty output) prints 8/8
`verdict=pass`, `verdict=WELL-FORMED exit=0`, exit 0 (block D). The nine failures therefore cannot come from a
blanket reject. The gate's containment also holds: with a canary file placed at the escaped parent path outside
the package, `strace -f -e trace=openat,newfstatat` records **zero** references to it, and the escaped-byte
canary never appears in gate output (block K).

## Evidence (commands and their actual output)

Scratch root `S=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures`; `W=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1`; `GATE` is `$W/ExecGateCore.claim-package-check.py` unless stated. The
landing-layout runs use `<S>/land2/corpus/instruments/claim-package-check.py` assembled from the w1 deliverables
with fixtures under `corpus/instruments/fixtures/claim-package/` (names de-prefixed, `index.txt` from
`ExecGateFixtures.index.txt`) — a prospective landing tree, not the landed corpus path. The gate and selftest
copies in that tree are byte-identical to the w1 files whose sha256 are listed above; blocks D, E, F and K were
run through that copy.

### A. gate and index identity

```
$ sha256sum "$W/ExecGateCore.claim-package-check.py" "$W/ExecGateFixtures.index.txt"
8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py
abe4460a142550e4f2b09579357037a28bfeddd8e22f4c326177a02b938ab7b4  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.index.txt
```

### B. exemplar (reconstructed from w1 `ExecExemplarPackage.*`)

```
$ python3 "$GATE" /fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/exemplar
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0
```

### C. all nine fixtures, full gate output

```
$ for d in "$S"/live2/defect-*; do echo "--- $(basename "$d") expected-rule=$(cat "$d/expected-rule")"; python3 "$G" "$d"; echo "exit=$?"; done
--- defect-1-missing-file expected-rule=R-FILES
RULE R-FILES verdict=fail detail=missing=1,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-1-missing-file rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-2-digest expected-rule=R-MANIFEST
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=fail detail=artifacts=4,digest-bad=1
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-2-digest rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-3-negative expected-rule=R-MANIFEST
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=fail detail=artifacts=4,positive=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-3-negative rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-4-escape expected-rule=R-MANIFEST
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=fail detail=artifacts=4,escape=1
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-4-escape rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-5-redaction expected-rule=R-REDACT
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=fail detail=redactions=empty
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-5-redaction rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-6-custodian expected-rule=R-CUSTODIAN
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=fail detail=chain=3,head=mismatch
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-6-custodian rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-7-reviewer expected-rule=R-STATUS
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=fail detail=reviewer=not-distinct
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-7-reviewer rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-8-marker expected-rule=R-REPORT
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=fail detail=marker=absent
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-8-marker rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
--- defect-9-secret expected-rule=R-NOSECRET
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=fail detail=hits=1,first=provenance.json,shape=credential
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/live2/defect-9-secret rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1
```

### D. junk-twin control

```
$ cp -a <exemplar> <S>/jt3; diff -r <exemplar> <S>/jt3; echo diff-exit=$?
diff-exit=0
$ python3 $GATE <S>/jt3
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r43/RevGateFixtures/jt3 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0
```

### E. selftest as fixture consumer, prospective landing layout

```
$ cd <S>/land2 && python3 corpus/instruments/claim-package-check.py --selftest
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=R-FILES verdict=pass
selftest case=2 class=defect fixture=defect-2-digest expected=R-MANIFEST observed=R-MANIFEST verdict=pass
selftest case=3 class=defect fixture=defect-3-negative expected=R-MANIFEST observed=R-MANIFEST verdict=pass
selftest case=4 class=defect fixture=defect-4-escape expected=R-MANIFEST observed=R-MANIFEST verdict=pass
selftest case=5 class=defect fixture=defect-5-redaction expected=R-REDACT observed=R-REDACT verdict=pass
selftest case=6 class=defect fixture=defect-6-custodian expected=R-CUSTODIAN observed=R-CUSTODIAN verdict=pass
selftest case=7 class=defect fixture=defect-7-reviewer expected=R-STATUS observed=R-STATUS verdict=pass
selftest case=8 class=defect fixture=defect-8-marker expected=R-REPORT observed=R-REPORT verdict=pass
selftest case=9 class=defect fixture=defect-9-secret expected=R-NOSECRET observed=R-NOSECRET verdict=pass
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=0
exit=0
```

Two consecutive runs are byte-identical (`cmp` clean). In the flat w1 layout (fixtures not beside the gate) the
same command prints `observed=fixtures-absent verdict=fail` on all ten cases and `selftest cases=10 failures=10`,
exit 1 — i.e. the fixture subtree must land where the gate looks (`<gate dir>/fixtures/claim-package`) for the
C2 counter to reach zero.

### F. independent reproduction from the exemplar

```
$ python3 "$S/reproduce.py" "$G" "$S/live2/exemplar" "$S/live2" "$S/rebuilt3"
defect-1-missing-file      rebuilt-vs-landed=identical gate-exit=1 fails=R-FILES PASS
defect-2-digest            rebuilt-vs-landed=identical gate-exit=1 fails=R-MANIFEST PASS
defect-3-negative          rebuilt-vs-landed=identical gate-exit=1 fails=R-MANIFEST PASS
defect-4-escape            rebuilt-vs-landed=identical gate-exit=1 fails=R-MANIFEST PASS
defect-5-redaction         rebuilt-vs-landed=identical gate-exit=1 fails=R-REDACT PASS
defect-6-custodian         rebuilt-vs-landed=identical gate-exit=1 fails=R-CUSTODIAN PASS
defect-7-reviewer          rebuilt-vs-landed=identical gate-exit=1 fails=R-STATUS PASS
defect-8-marker            rebuilt-vs-landed=identical gate-exit=1 fails=R-REPORT PASS
defect-9-secret            rebuilt-vs-landed=identical gate-exit=1 fails=R-NOSECRET PASS
reproducible=all-nine
exit=0
```

Per-file sha256 comparison of rebuild vs landed: 10/10 files for defect-1 and 11/11 for each of the other eight —
`differing=none` in every fixture.

### G. fail distribution across the nine

```
      1 R-CUSTODIAN
      1 R-FILES
      3 R-MANIFEST
      1 R-NOSECRET
      1 R-REDACT
      1 R-REPORT
      1 R-STATUS
```

(R-PROVENANCE: 0 — see finding F2.)

### H. structure: six contract files, changed files, seal

```
defect-1-missing-file      six=5/6 changed=[]                            added=['expected-rule'] removed=['claim_checklist.md'] seal=ok
defect-2-digest            six=6/6 changed=['evidence/source-capture.txt'] added=['expected-rule'] removed=[] seal=ok
defect-3-negative          six=6/6 changed=['evidence/manifest.json','status.json'] added=['expected-rule'] removed=[] seal=ok
defect-4-escape            six=6/6 changed=['evidence/manifest.json','status.json'] added=['expected-rule'] removed=[] seal=ok
defect-5-redaction         six=6/6 changed=['evidence/manifest.json','status.json'] added=['expected-rule'] removed=[] seal=ok
defect-6-custodian         six=6/6 changed=['custodian-receipts.json']    added=['expected-rule'] removed=[] seal=ok
defect-7-reviewer          six=6/6 changed=['status.json']               added=['expected-rule'] removed=[] seal=ok
defect-8-marker            six=6/6 changed=['report.md']                  added=['expected-rule'] removed=[] seal=ok
defect-9-secret            six=6/6 changed=['provenance.json']           added=['expected-rule'] removed=[] seal=ok
```

No file other than the delta target (and, for manifest edits, the resealed `status.json`) differs from the
exemplar; nothing is added except the `expected-rule` marker; nothing is removed except defect-1's file. No
symlinks anywhere in the fixture tree (`find -type l` count 0); no host absolute paths in fixture text.

### I. receipt claims re-measured

File counts, byte counts and tree sha256 for all nine match the fixtures receipt's table exactly (see the subject
table at the top; measured 16:55Z against the revised bytes).

### J. minimal-coupling probe (drop each contract file from the exemplar)

```
drop report.md                -> fails=R-FILES,R-REPORT,
drop claim_checklist.md       -> fails=R-FILES,
drop evidence/manifest.json   -> fails=R-FILES,R-MANIFEST,R-REDACT,R-CUSTODIAN,R-STATUS,R-REPORT,
drop custodian-receipts.json  -> fails=R-FILES,R-CUSTODIAN,
drop provenance.json          -> fails=R-FILES,R-PROVENANCE,
drop status.json              -> fails=R-FILES,R-STATUS,
```

### K. escape semantics and containment

```
$ (cd <defect-4-escape> && python3 $GATE .)
RULE R-MANIFEST verdict=fail detail=artifacts=4,escape=1
...
package=. rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

$ printf 'CANARY-OUTSIDE-77\n' > <S>/live2/escape.txt   # OUTSIDE the package, at the escaped parent path
$ strace -f -e trace=openat,newfstatat -o trace2.txt python3 $GATE <defect-4-escape>
$ grep -c "<S>/live2/escape.txt" trace2.txt
0
```

Variant probe (not a committed fixture): a true parent escape `../../outside.txt`, resealed, also fails R-MANIFEST
alone — `rules=8 pass=7 fail=1 verdict=DEFECT exit=1` — so the rule covers both `..` and realpath confinement
while never touching the outside file.

### L. the `expected-rule` marker is not load-bearing

```
$ for each fixture: cp -a, rm expected-rule, run gate
ExecGateFixtures.defect-1-missing-file     removed-marker: rule=R-FILES fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-2-digest           removed-marker: rule=R-MANIFEST fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-3-negative         removed-marker: rule=R-MANIFEST fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-4-escape           removed-marker: rule=R-MANIFEST fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-5-redaction        removed-marker: rule=R-REDACT fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-6-custodian        removed-marker: rule=R-CUSTODIAN fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-7-reviewer         removed-marker: rule=R-STATUS fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-8-marker           removed-marker: rule=R-REPORT fail=1 verdict=DEFECT exit=1
ExecGateFixtures.defect-9-secret           removed-marker: rule=R-NOSECRET fail=1 verdict=DEFECT exit=1
```

### M. rule count and print order

Every fixture prints eight `RULE` lines in the canonical order
`R-FILES R-MANIFEST R-REDACT R-CUSTODIAN R-PROVENANCE R-STATUS R-REPORT R-NOSECRET`; `rules=8` in the summary.

## Findings

**F1 (low — documentation precision).** Two deltas are documented at class level only: `ExecGateFixtures.index.txt`
says "append one byte" (actual byte `0x78`) and "40 lowercase hex" (actual
`0123456789abcdef0123456789abcdef01234567`). The exact parameters are recoverable only by reading the fixture bytes,
so "reproducible from the exemplar" holds from the fixture plus description, not from the description alone. The
same line calls `../escape.txt` "a `..` path escaping evidence/ and the package"; under the gate's `evidence/` join
it resolves to the package root, so it escapes `evidence/` but not the package. The rule rejects it on the `..`
component regardless, and a genuine `../../outside.txt` escape also fails R-MANIFEST alone once resealed (block K's
variant probe). No functional impact; two one-line index amendments would close it.

**F2 (low — coverage observation, not a rule-attribution defect).** The nine fixtures exercise seven of the eight
rules: R-MANIFEST×3, and one each for R-FILES, R-REDACT, R-CUSTODIAN, R-STATUS, R-REPORT, R-NOSECRET. No committed
fixture has R-PROVENANCE as its expected rule, so the gate's provenance rule is exercised only positively by the
exemplar in the committed set (`--selftest` never sees a provenance-negative package). The frozen C2 wording ("nine
committed defect fixtures each … with their own rule failing") is satisfied as written; this is a coverage gap
worth a tenth class in a later round (its negative limbs exist only in the gate module's uncommitted transcript).

**F3 (integration note, not a fixture defect).** `claim-package-check.py --selftest` resolves the fixtures at
`<gate dir>/fixtures/claim-package` and the selftest implementation as a sibling `claim-package-selftest.py` (or
`$CLAIM_PACKAGE_SELFTEST`). In the flat w1 layout the command prints `fixtures-absent` ×10 and
`selftest cases=10 failures=10` exit 1. The L1 landing must put the nine de-prefixed dirs **and** `exemplar/` under
`corpus/instruments/fixtures/claim-package/`, carry the index (any of `index.txt`, `INDEX.txt`,
`ExecGateFixtures.index.txt`), and land the selftest beside the gate under its sibling name. Verified green only in
that assembled layout (block E).

**F4 (low — forward risk).** `expected-rule` sits inside each package directory, so every fixture is a seven-entry
package root. Today's gate ignores unknown root entries, and all nine fail/pass as intended; a future stricter
R-FILES ("only the six") would red all nine for the wrong reason. Keeping the marker outside the package (e.g.
`fixtures/claim-package/expected/*.rule`) would remove the hazard.

**F5 (cosmetic, no rule impact).** defect-8 leaves `No filing has been made..` (double period) because the
replacement string supplies its own period. The marker is genuinely absent, which is the point; no rule reads the
sentence.

No fixture fails for the wrong reason; no fixture fails for more than one rule.

## Residual risk and verification gaps

- I reviewed the fixtures as consumers of the gate; rule-internal semantics (whether each rule's predicate matches
  the contract) belong to `RevGateRules`, and exemplar content provenance to `ExecExemplarPackage`/scouts.
- The selftest was run against a prospective landing tree assembled in scratch from the w1 deliverables, not
  against the landed `corpus/instruments/` path (nothing was landed at review time). Its isolation/audit
  behaviour is the selftest seat's subject; I only used its `expected=`/`observed=` columns.
- The C2 counters that depend on these files (census, recheck-audit expected count, capture binding, registry) were
  out of scope.
- Fixture hashes were re-measured at 16:55Z; if the fixtures seat rebuilds again, the digests above are the ones
  reviewed.

## Hygiene

- Writes: this receipt only (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/RevGateFixtures.md`).
  Scratch under `/fast/scratch/hyaku/kasegi-r43/RevGateFixtures`, removed before yield. No lane file, no fleet-root
  file, no PATH directory touched; no git/jj mutation anywhere (read-only `git log/status/rev-parse` only).
- Tooling: nothing installed or upgraded (preinstalled `python3`, `strace`, coreutils sufficed); no network fetch.
- Peer note received during the run (souji-lane `SOURCES.md` S242 field-width defect) is outside this seat's
  files and was not acted on.
