# ExecExemplarPackage — six-file claim-package exemplar (r43 C2 coverage)

Seat: ExecExemplarPackage (leaf executor). Lane `kasegi-shokunin`, round 43, wave 1.
Axes moved: `coverage` (the C2 capability row's worked exemplar) and, as a
consequence, `depth:verifiability` (every artifact digest and custody decision is
recomputable from the landed bytes).

## Supersession record (read this first)

The first build of this exemplar was bound to the **discarded** S067 draft —
`https://curl.se/docs/CVE-2023-38545.html`, capture sha256 `327bc909…`. While this
seat was working, `ExecSourceCapture` replaced `ExecSourceCapture.S067.txt`
byte-for-byte with a different advisory, and `ScribeKnowledgeGate` and
`ExecGateFixtures` both flagged that my package was bound to the superseded bytes.
I re-fetched, re-normalized and rebuilt from the landing capture; **every number
and digest below is from the rebuilt (CVE-2025-9086) package**. The earlier build
passed the same gate but was correctly rejected on provenance grounds: C2 requires
the exemplar to be built from the report captured *this round as the mined S067
row*, and that row is now CVE-2025-9086. The old artifacts are no longer in the
wave dir (all eleven files were overwritten by the rebuild).

## Result

The rebuilt exemplar passes the gate 8/8 on the landing capture:

```
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

Gate identity used: `.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py`
(the ExecGateCore deliverable, which lands at `corpus/instruments/claim-package-check.py`),
sha256 `bdb50a82623d93f10fe2cc0616d1d180c2a14f6e11fe8ff9004c84c35ba9ce8e`.
The three sourceable `*.rules.py` modules independently print 8/8 on the same
package (`package=… rules=8 pass=8 fail=0 … exit=0`).

## Source it is built from

The **landing** S067 capture, `curl - Out of bounds read for cookie path`,
`https://curl.se/docs/CVE-2025-9086.html`.

```
python3 corpus/instruments/capture-source.py --id S067 \
  --url https://curl.se/docs/CVE-2025-9086.html --out refetch.txt --kind html
S067 status=200 fetched_bytes=10455 snapshot_bytes=3822 \
  sha256=7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b utc=2026-10-28T16:49:10Z
cmp -s refetch.txt .ufo/waves/round-43/w1/ExecSourceCapture.S067.txt  -> IDENTICAL-TO-LANDED
```

Capture facts (first-party vendor advisory; public, no login, no customer data):
raw 10455 bytes, raw sha256
`58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd`; normalized
3822 bytes / 109 lines, sha256
`7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b` (the scout's
`fetched_utc` is `2026-10-28T16:46:34Z`; my re-fetch at `16:49:10Z` produced the
same bytes).

Advisory facts used, all from that capture: CWE-125 Out-of-bounds Read,
Severity Low, Bug bounty 505 USD, Area cookies, original report
`https://hackerone.com/reports/3294999`; affected `curl 8.13.0 to and including
8.15.0`; not affected `< 8.13.0 and >= 8.16.0`, and `>= 8.14.2` in the 8.14.X
branch; introduced-in `1aea05a6c2699e80c7593`; fixed-in
`c6ae07c6a541e0e96d0040afb6`; the advisory states the curl command-line tool is
not affected; reported 2025-08-11, distros@openwall 2025-09-05, 8.16.0 released
2025-09-10 ~06:00 UTC; credits Google Big Sleep (reporter) and Daniel Stenberg
(patcher); no active exploits known at publication.

## Deliverables and landing map

The six contract files alone are not a package: `evidence/manifest.json` declares
four artifacts that must land beside it. Landing map (all under
`corpus/instruments/fixtures/claim-package/exemplar/`):

| deliverable | lands at | lines | sha256 |
|---|---|---|---|
| `ExecExemplarPackage.report.md` | `exemplar/report.md` | 88 | `f99e2604eaafd0d2a9cac9ca04ff988d83a67ddf23d1b15340b689164a107144` |
| `ExecExemplarPackage.claim_checklist.md` | `exemplar/claim_checklist.md` | 41 | `855eb392d404b141dc25fa7efe7e25225dd54b34bb1a8ab452b3cff2304568cc` |
| `ExecExemplarPackage.manifest.json` | `exemplar/evidence/manifest.json` | 85 | `5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834` |
| `ExecExemplarPackage.custodian-receipts.json` | `exemplar/custodian-receipts.json` | 36 | `db85653db9019d4db5ee3e45930daf2bacc3a4b8270de3c9ee1aa5172ab3ab2b` |
| `ExecExemplarPackage.provenance.json` | `exemplar/provenance.json` | 95 | `c52b75f5390802da9f4e27e2fedc5d071becf4925becca6d788ad4760c221dbf` |
| `ExecExemplarPackage.status.json` | `exemplar/status.json` | 38 | `60f06dfebc04e4198999d203f0568dc8b7bde1b3caf96399e135132edf38a9c6` |
| `ExecExemplarPackage.source-capture.txt` | `exemplar/evidence/source-capture.txt` | 109 | `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b` |
| `ExecExemplarPackage.source-excerpt.txt` | `exemplar/evidence/source-excerpt.txt` | 13 | `9b81dd48db37b26303360334229c630f3e8ff32767b0ed68dd32a98e1d69e543` |
| `ExecExemplarPackage.solution-fixed-in.txt` | `exemplar/evidence/solution-fixed-in.txt` | 6 | `8e3d1b43a01a06397fe6141bfc9321cf695679e40d7260664ec23abaa1c3fc8b` |
| `ExecExemplarPackage.disclosure-timeline.txt` | `exemplar/evidence/disclosure-timeline.txt` | 7 | `8bececb6b37ba63f5c9fd32dd1b8b9f2cc08cb75ec443ffe81777ec6ed52bb8f` |
| `ExecExemplarPackage.transcript.txt` | evidence, not landed in the package | 57 | `e3cb646bd19e22f699cbd85cc29f198a761dbdc0b7c11911cf4b3cc29402ebef` |

`source-capture.txt` is a byte-identical copy of the landing S067 snapshot (so its
digest equals the committed snapshot's digest); the other three artifacts are
`sed -n` extracts with a three-line provenance header (ranges 82-91, 95-97,
102-105). The package contains no absolute path, no scratch path and no
`<pending` marker, and it passes 8/8 when the delivered bytes are re-assembled
under the landing names:

```
python3 ExecGateCore.claim-package-check.py "$D"   # $D assembled from the w1 files
package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
delivered_exit=0
grep -rn '/fast/scratch\|/home/vgpnk\|<pending' "$D"  -> no-absolute-or-pending
```

Note the rename: `cp ExecExemplarPackage.source-capture.txt <pkg>/evidence/` keeps
the seat-prefixed basename and reds R-MANIFEST (`missing=4`); the landing map
column is the target filename.

## Requirements, one at a time

- **Real artifact bytes with computed sha256** — four artifacts; the gate
  recomputes every digest (`digest-bad=0`). The report cites four digests and all
  four are `artifacts[].sha256` (`cited=4,unbound=0`).
- **One positive-polarity artifact** — three positive, one negative
  (`solution-fixed-in.txt` is the vendor fix statement bounding the claim to
  `< 8.16.0`).
- **Redaction receipts with distinct identities** — one receipt per artifact,
  `artifact_sha256 == scanned_artifact_sha256`, producer `exec-exemplar-package`,
  verifier `exemplar-redaction-pass`, `removed: []` (public advisory, no personal
  data).
- **Custodian chain, every scope_signal exactly `NO_SCOPE_OBJECTION`, head binds
  the manifest** — three actions (`scope-triage`, `evidence-freeze`,
  `manifest-attest`), grants `R43-EXEMPLAR-{SCOPE,EVIDENCE,ATTEST}-001`,
  `head_sha256 = 46b50b67491860280b6a5edbae59229d4e3609b9d262c6749aab8d50b6f9bf9f`
  `= chain[2].decision_sha256 = manifest.expected_head_sha256`; the documented
  formula recomputes independently:
  ```
  formula action=scope-triage decision=5de3f8187406 result=recomputed
  formula action=evidence-freeze decision=2f2153f9f569 result=recomputed
  formula action=manifest-attest decision=46b50b674918 result=recomputed
  attest input_sha256 matches blanked manifest: True
  head == last decision: True
  head == manifest.expected_head_sha256: True
  ```
- **Provenance with commands and exit codes** — two agents and two transitions
  (requested = resolved = `cursor/deepseek-v41-flash-1017`, the harness-declared
  session model), nine commands with the exit codes observed at build time, pin
  `https://github.com/VeigaPunk/kasegi-shokunin.git` @
  `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (lane HEAD at build, re-checked
  unchanged), `policy_sha256` = the landing capture digest,
  `external_effects_performed: []`, `secrets_attestation`
  `{"no_secrets": true, "findings": 0, …}`.
- **Status `claimable:false` naming its blockers with the `OPERATOR-GATED`
  marker** — `status.json` names, at top level, the operator submission gate, the
  prior-submission check and reviewer distinctness; `claim_checklist.md` repeats
  all three under `OPERATOR-GATED` and names them as residual gates.
  `finding_count: 1`, `state: BLOCKED`, `verdict:
  positive-blocked-operator-gated`, `no_submission_performed: true`.
- **report.md** — title, program and official URL, `Scope excerpt` with the
  verbatim capture lines 82-91, `observed_at`, the excerpt content sha256, CWE-125
  class, lab-only repro steps with no live target, impact quoted from the vendor's
  own `Severity: Low` / `Bug bounty: 505 USD` language, affected range including
  the 8.14.X exception, the vendor fix, the vendor timeline, and the literal
  `No submission performed`. No credential material (`R-NOSECRET hits=0`).
- **Transcript** — the gate's full output on the exemplar plus the sha256 of each
  of the six contract files, the four artifacts, fidelity, formula, rebuild
  determinism and the mutant control.

## Independent checks beyond the gate

Excerpt fidelity (each quoted line is the capture line it claims; header stripped):

```
fidelity source-excerpt.txt lines=82-91 lines=10 result=identical
fidelity solution-fixed-in.txt lines=95-97 lines=3 result=identical
fidelity disclosure-timeline.txt lines=102-105 lines=4 result=identical
fidelity source-capture.txt vs landed ExecSourceCapture.S067.txt result=identical
```

Rebuild determinism and mutant control:

```
rebuild determinism result=identical files=10
RULE R-MANIFEST verdict=fail detail=artifacts=4,digest-bad=1
package=…/mutant rules=8 pass=4 fail=4 verdict=DEFECT exit=1
```

Build derivation commands and their observed exit codes (`cmds.tsv`):

```
cp landed ExecSourceCapture.S067.txt capture.txt	0
cmp capture.txt landed ExecSourceCapture.S067.txt	0
cp capture.txt evidence/source-capture.txt	0
sed -n '82,91p' capture.txt (+3 header lines) > evidence/source-excerpt.txt	0
sed -n '95,97p' capture.txt (+3 header lines) > evidence/solution-fixed-in.txt	0
sed -n '102,105p' capture.txt (+3 header lines) > evidence/disclosure-timeline.txt	0
sha256sum source-capture.txt source-excerpt.txt solution-fixed-in.txt disclosure-timeline.txt	0
python3 build.py (composes the six contract files)	0
```

`provenance.json` carries the two capture commands (fetch, normalize) plus the
seven derivation commands that existed when it was written; the eighth line,
`python3 build.py`, is the command performing the write and so cannot appear in
its own output. Hence `commands=9`, not 10.

## Coordination

- `ExecSourceCapture` — replaced S067 mid-wave. I verified the landing bytes by
  re-fetching and re-normalizing (identical), and rebuilt from them.
- `ScribeKnowledgeGate` — caught that my first package was bound to the discarded
  38545 draft and supplied the landing anchors; I rebuilt and reported the new
  digests so the entry can be bound to this package.
- `ExecGateFixtures` — derives its nine defect fixtures from my bytes; told it the
  first build (38545) was superseded and supplied the rebuilt digests.
- `ExecGateCore` — supplied the schema and a superset-safe addendum
  (`sequence`, `artifacts[].bytes`, `redactions[].artifact`, agent `transition`,
  `secrets_attestation.no_secrets`, `transitions[]`); the package satisfies the
  gate bytes, which I ran directly rather than trusting a description of them.
- `ScribeExemplarReport-2` — also authors `report.md`/`claim_checklist.md`; I
  supplied the four artifact digests and flagged the overlap.

## Risks and open items for the L1

1. **Two producers for the two prose files.** `ScribeExemplarReport` is also
   dispatched to write `report.md` and `claim_checklist.md`. My item names all six
   files and my pair passes the gate. Land exactly one pair, never a
   concatenation. If the scribe's prose lands instead, it must cite only the four
   artifact digests above; nothing in the manifest, custody chain or status binds
   `report.md` bytes.
2. **Source binding.** The package is bound to capture sha256 `7e35413a…`
   (CVE-2025-9086). If S067 is replaced again, the exemplar must be rebuilt, not
   patched: `evidence/source-capture.txt` and the three excerpts all derive from
   it.
3. **Identity honesty.** `exemplar-redaction-pass` and `exemplar-reviewer` are
   fixture role identities executed by this seat (`provenance.identity_note` says
   so); reviewer distinctness therefore stays an `OPERATOR-GATED` residual gate.
4. **The exemplar asserts no submission and no new finding** — it is a worked
   example over an already-public, already-fixed advisory; `CritExemplarReal` can
   re-fetch `https://curl.se/docs/CVE-2025-9086.html` and diff against
   `evidence/source-capture.txt`.

## Tooling

None installed or upgraded; one documented `curl` fetch plus the lane's own
`capture-source.py`. No pacman, no writes to any PATH directory, no lane file
outside this seat's deliverables.

## Scratch

`/fast/scratch/hyaku/kasegi-r43/ExecExemplarPackage/` (recreated for the rebuild)
held the landing capture, build scripts, verification logs and package copies; it
is removed after the deliverables and this receipt were copied into the wave dir.
