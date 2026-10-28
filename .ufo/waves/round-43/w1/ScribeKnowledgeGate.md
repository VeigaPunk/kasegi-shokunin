# ScribeKnowledgeGate — round 43 receipt

Seat: ScribeKnowledgeGate (leaf scribe, no dispatch). Lane `kasegi-shokunin`, round 43,
base `ab98fac9dce87130bc4f66de89e30650d63943dc`; lane HEAD during work
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (the freeze commit; nothing round-43 landed while I ran).
Frozen claims read first (`.ufo/waves/round-43/claims.json`), not edited.

## Deliverable

| file | lands at | lines | bytes | sha256 |
|---|---|---|---|---|
| `ScribeKnowledgeGate.entry.md` | `corpus/knowledge/claim-package-gate.md` | 38 | 9830 | `f53109d842b185ed49ca599fda221351caf03df9d3443c5d50c8bb19a0cb5940` |

The wave-dir copy is byte-identical to the scratch file that was validated
(`sha256sum` printed the same digest for both).

## Where each assertion came from

- Gate behaviour and per-rule predicates: `w1/ExecGateCore.rules.txt` (the rule table, including its
  `[convention]` labels) and the deliverable's own module docstring — `w1/ExecGateCore.claim-package-check.py`,
  sha256 `bdb50a82623d93f10fe2cc0616d1d180c2a14f6e11fe8ff9004c84c35ba9ce8e`.
- Contract quotes: `corpus/knowledge/claim-package-contract.md` lines 7, 11, 13, 14, 15, 16, 18-26, 22-23 and
  `corpus/knowledge/claim-gates.md` lines 15 and 45-47. Every quote was printed back by anchorcheck (below).
- S067 advisory facts: `w1/ExecSourceCapture.S067.txt` (= `corpus/source-snapshots/round-43/S067.txt`,
  sha256 `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`, 109 lines) at L69, L83, L88.
- Exemplar facts: rebuilt deliverables (`ExecExemplarPackage.report.md` sha256 `f99e2604…`,
  `manifest.json` `5e296a37…`); operator gates confirmed in `claim_checklist.md` (three `OPERATOR-GATED`
  lines) and `status.json` (`claimable: false`, the same three blockers).

The entry keeps the rules attributed to the lane contract and the advisory facts to S067; it says so in
the intro sentence ("S067 is this entry's only external source, and it grounds the worked exemplar, not
the rules") rather than implying the advisory is the rules' authority.

## Commands and real output

Scratch `S=/fast/scratch/hyaku/kasegi-r43/ScribeKnowledgeGate`; disk guard before the pass
(`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`) printed
`/fast/scratch/hyaku 26% 598.9G free`. Nothing was written to `/tmp`.

Staging tree = the lane at its freeze commit plus the wave deliverables, all under scratch:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive HEAD | tar -x -C "$S/stage"
$ git rev-parse HEAD   ->  4cb6d4ae768481e1a14afbedc2d865a060ebacfd
```

Overlay: `corpus/instruments/claim-package-check.py` <- `ExecGateCore.claim-package-check.py`;
`corpus/instruments/claim-package-selftest.py` <- `ExecGateSelftest.selftest.py`;
`corpus/instruments/fixtures/claim-package/exemplar/{report.md,claim_checklist.md,custodian-receipts.json,
provenance.json,status.json,evidence/{manifest.json,source-capture.txt,source-excerpt.txt,
solution-fixed-in.txt,disclosure-timeline.txt}}` <- the rebuilt `ExecExemplarPackage.*`;
fixtures `ExecGateFixtures.defect-*` copied and renamed to their landing names `defect-<k>-<class>`;
`corpus/source-snapshots/round-43/{S067.txt,manifest.json}` <- `ExecSourceCapture.*`.

1. Exemplar through the gate:

```
$ cd "$S/stage" && python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exemplar_exit=0
```

2. The nine defect fixtures (re-run on the bytes re-derived after the exemplar rebuild, mtime 13:51):

```
defect-1-missing-file          exit=1 fail=R-FILES    expected=R-FILES     match=True
defect-2-digest                exit=1 fail=R-MANIFEST expected=R-MANIFEST  match=True
defect-3-negative              exit=1 fail=R-MANIFEST expected=R-MANIFEST  match=True
defect-4-escape                exit=1 fail=R-MANIFEST expected=R-MANIFEST  match=True
defect-5-redaction             exit=1 fail=R-REDACT   expected=R-REDACT    match=True
defect-6-custodian             exit=1 fail=R-CUSTODIAN expected=R-CUSTODIAN match=True
defect-7-reviewer              exit=1 fail=R-STATUS   expected=R-STATUS    match=True
defect-8-marker                exit=1 fail=R-REPORT   expected=R-REPORT    match=True
defect-9-secret                exit=1 fail=R-NOSECRET expected=R-NOSECRET  match=True
```

3. Selftest (companion landing, fixtures named `defect-*`):

```
$ python3 corpus/instruments/claim-package-check.py --selftest | tail -1
selftest cases=10 failures=0
selftest_exit=0
```
The ten graded lines each printed `expected=<rule> observed=<rule> verdict=pass`, including
`case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass`.

4. The entry's falsifiable rule, measured on the rebuilt fixture:

```
$ cp -a corpus/instruments/fixtures/claim-package/defect-8-marker "$S/flip"
$ python3 corpus/instruments/claim-package-check.py "$S/flip" | tail -1
package=/fast/scratch/.../flip rules=8 pass=7 fail=1 verdict=DEFECT exit=1
$ printf 'No submission performed.\n' >> "$S/flip/report.md"
$ python3 corpus/instruments/claim-package-check.py "$S/flip" | tail -1
package=/fast/scratch/.../flip rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```
(Only the marker line changed; pass 7 -> 8.)

5. Exit-code limbs claimed in the entry's intro:

```
$ python3 corpus/instruments/claim-package-check.py        ->  no_arg_exit=2
$ python3 corpus/instruments/claim-package-check.py <absent dir>
package=<absent> verdict=ERROR exit=2                       ->  missing_dir_exit=2
```

6. The entry's `recheck:` line. Parse, then execution from two cwds with the lane path substituted by
the staged tree (the lane has nothing landed yet, so the literal lane path cannot resolve today):

```
$ line=$(grep '^recheck: ' entry.md | sed 's/^recheck: //'); bash -n -c "$line"
bash_n_exit=0

$ staged=$(printf '%s' "$line" | sed "s#cd /home/vgpnk/Projects/shokunin/kasegi-shokunin#cd $S/stage#")
$ cd "$S/stage" && bash -c "$staged" > o1 2>&1   ->  lane_exit=0
$ cd /          && bash -c "$staged" > o2 2>&1   ->  foreign_exit=0
$ sha256sum o1 o2
30ca9575c2811abaa0f77abedeb22fdccf475dc37596961979efef4e458f33ed  o1
30ca9575c2811abaa0f77abedeb22fdccf475dc37596961979efef4e458f33ed  o2
IDENTICAL
$ cat o1
selftest cases=10 failures=0
package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

7. anchorcheck over the staged entry:

```
== corpus/knowledge/claim-package-gate.md: 17 in-range cite instances, 0 bad; 14 distinct anchors;
   LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```
Each cited line printed its own text, including
`corpus/source-snapshots/round-43/S067.txt:69 [Project curl Security Advisory, September 10 2025 Permalink]`,
`:83 [Severity: Low]`, `:88 [Affected versions: curl 8.13.0 to and including 8.15.0]`, and every contract
line for the eight rules.

8. recheck-audit's own limbs (`python3 corpus/instruments/recheck-audit.py` over the staged root, with the
line's `cd` rewritten to that root so its cdroot limb is testable):

```
claim-package-gate.md   frozen=111 strict=111111 lane=0 foreign=0 executes PASS
strict pass=2/62 cdroot_fail=60 instrument_fail=0 own_fail=0
lines=62 total=62 pass=62 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0
```
The 60 cdroot failures are the other entries, which `cd` to the real lane while the audited root was the
staged tree; in the real lane the cd path IS the audited root. With the unmodified line and the staged
root, the audit printed `strict=111011 cdroot_fail=1` for my entry — the only failing limb is the root
identity that landing supplies.

## Conflict found and reported (S067 was swapped under the exemplar)

At 16:46:34Z the capture seat replaced the S067 snapshot (CVE-2023-38545 -> CVE-2025-9086, sha256
`7e35413a…`, 109 lines) after the scout designated the latter, and rewrote the registry row; the exemplar
and all nine fixtures were still built from the discarded 38545 bytes (`report.md` `764028e0…`, evidence
`327bc909…`). `w1/ScoutSourceHunt.md:156,158` had already filed the mismatch. I sent the evidence to
`ExecExemplarPackage` and `ExecGateFixtures`; both rebuilt against the landing capture and confirmed by
message. The entry is written against the rebuilt bytes (`report.md` `f99e2604…`); at landing, the
exemplar paragraph is true only if that rebuild is what lands. Reported to `KasegiR43` with the exact
digests.

## Landing couplings the L1 must honour (told to KasegiR43)

- The selftest is delivered as 592 lines meant to be pasted into `claim-package-check.py`; pasting changes
  the gate's sha256 and orphans the `bdb50a82…` identity cited by the exemplar and fixture receipts. Landing
  it as the gate's documented companion `corpus/instruments/claim-package-selftest.py` preserves those bytes
  (measured: `selftest cases=10 failures=0`, exit 0). Either way the fixtures must land as
  `defect-<k>-<class>`; under the `ExecGateFixtures.defect-…` names the selftest sees `fixtures=0` and my
  recheck fails closed.
- `corpus/instruments/knowledge-expected.txt` needs `corpus/knowledge/claim-package-gate.md` appended
  (61 -> 62) or the audit reports `unexpected=corpus/knowledge/claim-package-gate.md`.

## Independent verification of the recheck line (peer-reported, not my run)

`ExecEntryGateRecheck-2` (the seat that authored the line) messaged after the landing and re-measured it
end-to-end on the landed bytes, 570 bytes, sha256
`fbee7c32f17a1566e6e25653c0ccafeb0d494688a5189b6e99c5534b78adc26d`: `bash -n` exit 0; replica run exit 0
from three cwds with identical stdout sha256 `30ca9575…` (the digest I measured independently); a mutant
with R-REPORT forced to pass exits 1; and `recheck-audit` on a 62-entry replica prints `frozen=111
strict=111111`, `expected=62`. That supplies the cdroot limb my staged run could not (root identity), and
confirms the expected-list count the L1 must land. Their measurement report also states both selftest
integrations (pasted body and companion) print identical output; I measured the companion only, so that
half is their observation, not mine. Their seat's final `entry-fix.txt` carries these exact landed bytes
rather than its earlier 447-byte form.

## QUALITY Q1-Q6 on the deliverable

| id | evidence |
|---|---|
| Q1 | H1 at line 1, then `source:` (S067, URL, `corpus/source-snapshots/round-43/S067.txt:69-109`), `verified-at: 2026-10-28`, `recheck:` one command, lines 2-4. |
| Q2 | S067 is a tier-A mined row opened this round; the exemplar claims quote L69/L83/L88. The rule claims rest on the lane contract at the cited lines — stated openly rather than presented as a registry-row claim. |
| Q3 | Every rule carries a verbatim quote, each <=25 words, each printed back by anchorcheck from the cited line. |
| Q4 | Advisory facts are the curl project's own ("stated as the project's position rather than as a general rule"); the rules are the lane contract's, not a vendor's. |
| Q5 | One falsifiable rule (the marker rule) with the command and the measured 7 -> 8 flip; one rejected over-generalization (`WELL-FORMED` = claim-ready) with its reason. |
| Q6 | Documentation only: no probing/scanning instruction, no credential material, no session/private URL, no vault-reference URI. `grep -n '/fast/scratch\|/home/vgpnk\|<pending\|op://' entry.md` returns only the `cd /home/...` the recheck form requires. |

## Limits

- I did not execute the literal recheck line against the lane path, because the lane is still at
  `4cb6d4ae` with nothing landed; I executed it against a staged tree with identical bytes and the
  `cd` target substituted, from two cwds, with identical output digests and exit 0. The peer seat's
  replica run (above) is the end-to-end form; the `source:` anchors were verified against the capture
  deliverable, not against a landed snapshot.
- My gate runs are over `bdb50a82…` (pre-selftest-paste) plus the companion module; if the L1 pastes
  instead, the gate bytes change while the rule behaviour measured here does not.
- `unexpected=` noise in the audit runs is the missing expected-list row, not a failing limb.

## Tooling and scratch

Nothing installed or upgraded (no pacman — host pause respected; no `uv`/`npx`/release binary needed).
Scratch `/fast/scratch/hyaku/kasegi-r43/ScribeKnowledgeGate` removed after copying the deliverable and
this receipt; verified absent.

## Write scope

Wrote only `.ufo/waves/round-43/w1/ScribeKnowledgeGate.entry.md` (deliverable) and this receipt in the
lane; everything else lived under the scratch dir. No write to the fleet root, `shokuknow`, `corpus/`,
or any PATH directory; no mutating git anywhere (archive only, read-only).
