# ExecGateFixtures — round-43 C2 defect fixtures

- Lane: kasegi-shokunin, round 43, base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
- Seat: ExecGateFixtures (leaf executor). Item: nine claim-package defect fixtures + index + this receipt.
- Frozen claims read first and not edited: `.ufo/waves/round-43/claims.json` (C2).

## Authoritative gate

- Path: `.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py` (lands at `corpus/instruments/claim-package-check.py`).
- sha256: `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`.
- Rule table: `.ufo/waves/round-43/w1/ExecGateCore.rules.txt`.
- The three `*.rules.py` modules are development fragments, not the committed gate; this receipt verifies against the committed gate file above.

## Base package (the exemplar)

The base is the landed exemplar, built from `S067` = CVE-2025-9086 (`ExecSourceCapture.S067.txt`, sha256 `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`, 109 lines), reconstructed byte-for-byte from the w1 deliverables. Mapping and per-file sha256:

| exemplar path | w1 deliverable | sha256 |
|---|---|---|
| `report.md` | `ExecExemplarPackage.report.md` | `f99e2604eaafd0d2a9cac9ca04ff988d83a67ddf23d1b15340b689164a107144` |
| `claim_checklist.md` | `ExecExemplarPackage.claim_checklist.md` | `855eb392d404b141dc25fa7efe7e25225dd54b34bb1a8ab452b3cff2304568cc` |
| `evidence/manifest.json` | `ExecExemplarPackage.manifest.json` | `5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834` |
| `custodian-receipts.json` | `ExecExemplarPackage.custodian-receipts.json` | `db85653db9019d4db5ee3e45930daf2bacc3a4b8270de3c9ee1aa5172ab3ab2b` |
| `provenance.json` | `ExecExemplarPackage.provenance.json` | `c52b75f5390802da9f4e27e2fedc5d071becf4925becca6d788ad4760c221dbf` |
| `status.json` | `ExecExemplarPackage.status.json` | `60f06dfebc04e4198999d203f0568dc8b7bde1b3caf96399e135132edf38a9c6` |
| `evidence/disclosure-timeline.txt` | `ExecExemplarPackage.disclosure-timeline.txt` | `8bececb6b37ba63f5c9fd32dd1b8b9f2cc08cb75ec443ffe81777ec6ed52bb8f` |
| `evidence/solution-fixed-in.txt` | `ExecExemplarPackage.solution-fixed-in.txt` | `8e3d1b43a01a06397fe6141bfc9321cf695679e40d7260664ec23abaa1c3fc8b` |
| `evidence/source-capture.txt` | `ExecExemplarPackage.source-capture.txt` | `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b` |
| `evidence/source-excerpt.txt` | `ExecExemplarPackage.source-excerpt.txt` | `9b81dd48db37b26303360334229c630f3e8ff32767b0ed68dd32a98e1d69e543` |

Reconstruction (run in a scratch dir):

```sh
W=.ufo/waves/round-43/w1; E=<scratch>/exemplar; mkdir -p "$E/evidence"
cp "$W/ExecExemplarPackage.report.md" "$E/report.md"
cp "$W/ExecExemplarPackage.claim_checklist.md" "$E/claim_checklist.md"
cp "$W/ExecExemplarPackage.manifest.json" "$E/evidence/manifest.json"
cp "$W/ExecExemplarPackage.custodian-receipts.json" "$E/custodian-receipts.json"
cp "$W/ExecExemplarPackage.provenance.json" "$E/provenance.json"
cp "$W/ExecExemplarPackage.status.json" "$E/status.json"
for f in disclosure-timeline solution-fixed-in source-capture source-excerpt; do
  cp "$W/ExecExemplarPackage.$f.txt" "$E/evidence/$f.txt"
done
```

Base gate run: `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` (full output in the transcript below).

Superseded build note: the first derivation used the earlier exemplar built from the discarded CVE-2023-38545 capture (`report.md` sha256 `764028e0…`). ExecExemplarPackage rebuilt the exemplar from the landing `S067` = CVE-2025-9086; the nine fixtures, index and this receipt were re-derived and re-run from the rebuilt bytes. No 38545-derived fixture remains in the delivery.

## Method

Each fixture is the base with exactly one documented delta, listed in `ExecGateFixtures.index.txt` (also reproduced in the table below). Every fixture dir additionally carries a one-line `expected-rule` file so the selftest can resolve the expected rule without parsing the index. Manifest edits are followed by recomputing `status.manifest_sha256` (the mechanical seal); the digest fixture mutates artifact bytes, not the declared manifest digest, because the gate's own rule table records that editing a declared digest alone also reds R-REDACT and R-REPORT.

## Deliverables

Each dir lands as `corpus/instruments/fixtures/claim-package/defect-<n>-<class>` (drop the `ExecGateFixtures.` prefix).

| w1 dir | expected rule | delta | files | bytes | tree sha256 |
|---|---|---|---|---|---|
| `ExecGateFixtures.defect-1-missing-file` | R-FILES | rm claim_checklist.md (one of the six contract files absent) | 10 | 18244 | `967fb599c2a9cc92395f7086f19bb1afd0f43639bb4f9ff40cfa13f306857c63` |
| `ExecGateFixtures.defect-2-digest` | R-MANIFEST | append one byte to the first evidence artifact (manifest.artifacts[0].path); the declared sha256 is unchanged | 11 | 20337 | `a92290b0a34d4723fc189a5130eb8c9e98bda02c9a6704cab903653d0db27029` |
| `ExecGateFixtures.defect-3-negative` | R-MANIFEST | every artifacts[].polarity "positive" -> "negative" (zero positive artifacts); manifest resealed into status.manifest_sha256 | 11 | 20336 | `e27317df1fef1c043ad15df8e09d76b1a1e92344f372e20b17b93dfc876ad97d` |
| `ExecGateFixtures.defect-4-escape` | R-MANIFEST | manifest.artifacts[0].path := "../escape.txt" (a .. path escaping evidence/ and the package); resealed | 11 | 20331 | `a1a2b74f6c4b76716801c066784b99c0299be307fe7906175a368dec15c8f39a` |
| `ExecGateFixtures.defect-5-redaction` | R-REDACT | manifest.redactions := [] (no redaction receipt for any artifact); resealed | 11 | 18473 | `f81ea3a6e872c481e58fed41f92d6885b9aae5f8b798f83555b71cd5fd4d434b` |
| `ExecGateFixtures.defect-6-custodian` | R-CUSTODIAN | custodian-receipts.json head_sha256 := 64x'f' (breaks head == final decision == manifest.expected_head_sha256) | 11 | 20337 | `e831d65ec990dca189209539b17440aaafcacf3858481b483c726d28c15fcbcf` |
| `ExecGateFixtures.defect-7-reviewer` | R-STATUS | status.claim_review.reviewer.identity := manifest.redactions[0].producer (reviewer == producer) | 11 | 20338 | `16d729aec4edbff9a40c949930376501b44138f52a50a7f0959470cf5256792f` |
| `ExecGateFixtures.defect-8-marker` | R-REPORT | report.md literal "No submission performed" replaced with "No filing has been made." | 11 | 20335 | `0b932b7b6ea320b0c84f1f7f582aeec995a68c6aa32f2f9a5644d36150eda216` |
| `ExecGateFixtures.defect-9-secret` | R-NOSECRET | provenance.json gains top-level "api_key": 40 lowercase hex (labelled-credential secret shape) | 11 | 20392 | `563043c8504bdd4239263072fc21a15e8d125bda46a2f61649574935db423459` |

- `ExecGateFixtures.index.txt`: 9 lines, sha256 `abe4460a142550e4f2b09579357037a28bfeddd8e22f4c326177a02b938ab7b4`.
- tree sha256 = `(cd <dir> && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)` over the dir's relative paths.
- The receipt itself cannot embed its own sha256; reproduce it with `sha256sum .ufo/waves/round-43/w1/ExecGateFixtures.md`.

## Verification transcript (exact command output)

Every fixture prints `rules=8 pass=7 fail=1 verdict=DEFECT exit=1` with exactly its named rule failing. Command:

```sh
GATE=.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py
for d in .ufo/waves/round-43/w1/ExecGateFixtures.defect-*; do
  python3 "$GATE" "$d"
done
```

```
### gate: /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py
8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py

### base exemplar (S067 = CVE-2025-9086, reconstructed from w1 ExecExemplarPackage.* files)
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=work/exemplar-v2 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0

### ExecGateFixtures.defect-1-missing-file expected=R-FILES
RULE R-FILES verdict=fail detail=missing=1,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-1-missing-file rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-2-digest expected=R-MANIFEST
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=fail detail=artifacts=4,digest-bad=1
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-2-digest rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-3-negative expected=R-MANIFEST
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=fail detail=artifacts=4,positive=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-3-negative rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-4-escape expected=R-MANIFEST
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=fail detail=artifacts=4,escape=1
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-4-escape rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-5-redaction expected=R-REDACT
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=fail detail=redactions=empty
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-5-redaction rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-6-custodian expected=R-CUSTODIAN
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=fail detail=chain=3,head=mismatch
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-6-custodian rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-7-reviewer expected=R-STATUS
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=fail detail=reviewer=not-distinct
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-7-reviewer rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-8-marker expected=R-REPORT
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=fail detail=marker=absent
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-8-marker rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### ExecGateFixtures.defect-9-secret expected=R-NOSECRET
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=fail detail=hits=1,first=provenance.json,shape=credential
package=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateFixtures.defect-9-secret rules=8 pass=7 fail=1 verdict=DEFECT exit=1
exit=1

### junk twin (byte-identical copy of the rebuilt exemplar)
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=work/junk-v2 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0
```

## Junk-twin control

A tenth directory that is a byte-identical copy of the rebuilt exemplar passes, so the nine failures cannot come from a blanket reject:

```sh
cp -a <scratch>/exemplar <scratch>/junk-v2
diff -r <scratch>/exemplar <scratch>/junk-v2   # no output == byte-identical
python3 .ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py <scratch>/junk-v2
```

```
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=<scratch>/junk-v2 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0
```

## Handoff notes

- Land the nine dirs as `defect-1-missing-file` … `defect-9-secret`; keep `expected-rule` in each (ExecGateSelftest reads it). The index uses the landed names.
- These fixtures are bound to the rebuilt exemplar bytes hashed in the table above (S067 = CVE-2025-9086). If ExecExemplarPackage changes those bytes again, re-derive with `build_fixtures.py` and re-run the transcript.
- `defect-1` removes `claim_checklist.md` deliberately: it is the only contract file no rule but R-FILES reads, so the fixture fails exactly one rule. (Dropping `provenance.json`, as ExecGateCore's scratch delta did, reds R-FILES and R-PROVENANCE; the expected rule there is still R-FILES, the first failing in canonical order.)
- Keys the gate enforces by convention rather than contract (e.g. `sequence`, `redactions[].artifact`, `secrets_attestation.no_secrets`) are documented in `ExecGateCore.rules.txt`; the exemplar satisfies them and the fixtures inherit them.
- Tooling: none installed or upgraded. Scratch removed before yield; no PATH directory touched.
- `ExecGateFixtures.md` (this receipt): 252 lines; its sha256 is not self-embeddable — `sha256sum .ufo/waves/round-43/w1/ExecGateFixtures.md` reproduces it.
