# ExecControls — round-41 C2 junk control + C1 do-nothing re-verification

Seat `ExecControls` (leaf executor). Item: build the C2 junk control on a scratch registry copy —
append a junk S063 row (status `mined`, no capture, no manifest, no entry) and show every frozen C2
counter rejects it — and re-verify the C1 do-nothing receipt
`.ufo/waves/round-41/c1-controls/do-nothing.txt` still holds (suite absent at the claims freeze).

Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read-only throughout; no mutating git/jj
command was run anywhere. Lane head at run time `96dbd5f` (round-41 freeze errata); the freeze
commit every arm is archived from is `fbba3d96cdf8d37c1ea41304a1ba35691329684b`. Base
`5b29ea1439450b712581edf5f0f0bf98dfb262ab` (40-char, per `wave1/CORRECTIONS-L1.md` item 1). Driver
pass completed `2026-10-27T09:12:46Z`.

## 1. Deliverable

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-41/wave1/ExecControls.junk-s063.txt` | 974 | 61647 | `63a522608a1f0de9884d1a2dce32465fdceb79fb757a7d1ec7b6c67e68360656` |

The deliverable is the transcript (header + every command with its real output and exit status +
the one-line control verdict per claim). It is not text the L1 lands in the corpus: it is the
retained counter-evidence for the C2 `junk twin accepted` kill clause and for the C1 do-nothing
control.

## 2. What was built — a monotone junk ladder

Six scratch copies of the freeze export, each adding one more piece of the forgery a do-nothing
family would need to reach the C2 after-state. Every copy's 58 landed `recheck:` lines were
retargeted to that copy's own root so each tree is self-contained (the audit's `cdroot` limb then
measures the tree under test; the live lane's own reading is untouched — the `base` arm reproduces
`c2-controls/before.txt` exactly).

| arm | what it adds | registry rows | frontier rows | knowledge files |
|---|---|---|---|---|
| `base` | nothing — pristine freeze export (positive control) | 62 | 23 | 59 |
| `A1` | the bare junk S063 row: status `mined`, no capture file, no manifest record, no knowledge entry | 63 | 23 | 59 |
| `A2` | A1 + the F24 frontier row (`admitted`) naming the entry that was never written | 63 | 24 | 59 |
| `A3` | A2 + a round-41 manifest record for S063 that cannot bind (no `url`, no fetch provenance, no capture bytes) | 63 | 24 | 59 |
| `A4` | A3 + the expected-entry list bumped to name the entry that still does not exist | 63 | 24 | 59 |
| `A5` | A4 + the junk knowledge entry written but NOT registered in the expected list | 63 | 24 | 60 |

Fixture digests (re-derivable from the artifact texts in §7):

```
cfe25e07616fad912b219d81816f944dcbe470a0025789afe4a88c4d549cfb4f  base/corpus/SOURCES.md
26ca70404a0d9a66913f8637ac56730932948f6d670f5a3c6311653ef760cc4e  A1..A5/corpus/SOURCES.md  (one appended row, identical in every arm)
7e59a0d85b34c193b243f65d1ed3c6ced91c656af165fd40b08d111ab61bcbd1  base/corpus/README.md
0ce4edfedc0ed84f1025f9b3bb7ab1f09b66a7814839fdf3fc8deb390dcef8a0  A2..A5/corpus/README.md   (one appended F24 row)
84acfc1a4dd6ac0df1ad5268fb60da866fc3ea4514ae1b0ea5d40242ab3a8b0d  A3..A5/corpus/source-snapshots/round-41/manifest.json
eb93a5a20439a441032b234ea47114f630065f200f6c880369b765a208f3c809  A4/corpus/instruments/knowledge-expected.txt
328041466810f72e7900669e811d36d0434991503e57bec4f1817921b31714a2  base and A5 expected lists (A5 = base, entry deliberately unregistered)
21cfe3425f54e87197433fb4a5ce28d5cedc5d4607325cd05cb961d5a4072425  A5/corpus/knowledge/rfc-9116-security-txt.md
```

## 3. Measured matrix — the frozen C2 counting commands per arm

Every cell is a real output from the transcript; `e<N>` is the command's exit status.

| probe (frozen C2 counting command) | base | A1 | A2 | A3 | A4 | A5 |
|---|---|---|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 23 | 23 | **24** | 24 | 24 | 24 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 62 | **63** | 63 | 63 | 63 | 63 |
| `awk … S063 … s=="mined"` | 0 | **1** | 1 | 1 | 1 | 1 |
| `grep -rlE '^source: S063' corpus/knowledge \| wc -l` | 0 | 0 | 0 | 0 | 0 | **1** |
| `ls corpus/knowledge/*.md \| wc -l` | 59 | 59 | 59 | 59 | 59 | **60** |
| `frontier-recheck-count.py` — `PASS F24` lines | 0 | 0 | **0** | 0 | 0 | 0 |
| `frontier-recheck-count.py` — summary | 26/26 e0 | 26/26 e0 | **27/26 e1** `F24 … problems=missing-entry` | 27/26 e1 | 27/26 e1 | **27/26 e1** `F24 ids=S063 exit=2 problems=recheck-exit-2` |
| `capture-binding-check.py` | 54/54/**0** e0 | 54/54/0 e0 | 54/54/0 e0 | **55/54/1 e1** | 55/54/1 e1 | 55/54/1 e1 |
| `capture-binding-check.py` failing lines | — | — | — | `FAIL rule=url-mismatch record=S063 detail=absent`, `FAIL rule=provenance-missing record=S063 dir=round-41` | same | same |
| `recheck-audit.py --quiet` expected / missing / unexpected | 59 / 0 / 0 e0 | 59/0/0 e0 | 59/0/0 e0 | 59/0/0 e0 | **60 / 1 / 0 e1** | **59 / 0 / 1 e1** |
| `source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063` | `manifest UNAVAILABLE reason=missing` e2 | same e2 | same e2 | **`S063:source UNAVAILABLE reason=missing` e2** | same e2 | same e2 |
| `source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S063` | `S063:source UNAVAILABLE reason=not-listed` e2 | same | same | same | same | same |
| `sources-census.sh validate` | `ok` e0 | **`E11 … S063 missing used-by` e1** | E11 e1 | E11 e1 | E11 e1 | **`ok` e0** |
| r22 measure `(20+F_admitted)/(20+F_total)` (SCORECARD.md:1551) | 43/43 met=yes | 43/43 met=yes | **44/44 met=no** | 44/44 met=no | 44/44 met=no | 44/44 met=no |
| `corpus/source-snapshots/round-41/S063.txt` (capture bytes) | absent | absent | absent | **absent** | absent | absent |
| round-41 snapshot dir contents | absent | absent | absent | `manifest.json` only | same | same |

## 4. The four named rejections, and the arm that fires each

| named rejection | observed | arm |
|---|---|---|
| source-recheck fails (no manifest record) | `manifest UNAVAILABLE reason=missing` (no round-41 manifest) and, against the existing round-40 manifest, `S063:source UNAVAILABLE reason=not-listed` — the row has no manifest record anywhere. From A3 the record exists but no capture does: `S063:source UNAVAILABLE reason=missing`. All exits 2. | base–A5 |
| binding `unbound != 0` | needs a manifest record: A1/A2 print `records=54 bound=54 unbound=0 exit=0` (the junk row alone is invisible to this counter); A3+ print `records=55 bound=54 unbound=1 exit=1` with `url-mismatch detail=absent` and `provenance-missing`. Note the record count reaches the after-state's 55 while the binding still fails. | A3–A5 |
| harness has no PASS F24 | zero `PASS F24` lines in every arm; A2–A4 print `FAIL F24 problems=missing-entry`, A5 prints `FAIL F24 ids=S063 exit=2 problems=recheck-exit-2`, and every arm's summary is `entries=27 pass=26 exit=1` from A2 onward. | base–A5 |
| audit unexpected/missing mismatch | needs the expected list and the tree to disagree: A4 prints `expected=60 missing=1 exit=1`, A5 prints `expected=59 missing=0 unexpected=1 exit=1`. A1–A3 leave the audit green (`expected=59 missing=0 unexpected=0 exit=0`) because it is entry/expected-list-driven, not registry-row-driven. | A4 (missing), A5 (unexpected) |

## 5. Findings

1. **The bare junk row is caught by the census, not by binding or the audit.** A1 (a well-formed
   `mined` row whose `used-by` names a file that does not exist) reds `sources-census.sh validate`
   with `E11 … S063 missing used-by` exit 1 on the first pass, while `capture-binding-check.py`
   stays at `records=54 bound=54 unbound=0 exit=0` and `recheck-audit.py` stays at
   `expected=59 missing=0 unexpected=0 exit=0`. Both of those counters are record/entry-driven:
   a registry row with no manifest record produces no `unbound` record and no knowledge entry, so
   they cannot see it. The precise statement is that the *junk family* is rejected by the counter
   set as a whole; the row alone is rejected by three of the four named limbs (source-recheck,
   harness, census) and needs A3/A4 to red binding and the audit.
2. **`unbound != 0` fires exactly when a manifest record exists and cannot bind** (A3:
   `rule=url-mismatch record=S063 detail=absent` + `rule=provenance-missing record=S063 dir=round-41`
   → `records=55 bound=54 unbound=1 exit=1`). The record count alone reaches the after-state value
   (55) — the count is not the certificate; the binding is.
3. **Writing the entry does not help.** A5 carries the full provenance trio (`source:`,
   `verified-at:`, `recheck:`) and an F24 frontier row that resolves to it, yet its own recheck line
   exits 2, so the harness record moves from `missing-entry` to `recheck-exit-2` and the audit moves
   from `missing=1` to `unexpected=1`. All four named limbs stay red.
4. **The r22 measure does not discriminate the junk.** From A2 onward the ratio reads exactly
   `44/44 = 1.000` — the claim's after-state number — while the criterion is *not* met, because its
   conjunct "every admitted row's entry passing `frontier-recheck-count.py`" is false. In A1 the
   measure reads `43/43 met=yes` with the junk row sitting in the registry (a `mined`, non-`queued`
   row is not counted by `F_total`). **Note for the L1:** the C2 predicate's discrimination rests on
   the `PASS F24 ids=S063` line and the harness exit, not on the ratio.
5. **The census returns to green once the `used-by` path exists** (A5 → `ok` exit 0), so `E11` is
   necessary but not sufficient: it catches the dangling row (A1–A4), not the registered forgery.

## 6. Positive controls — the counters are not constant-red printers

- The `base` arm reproduces `c2-controls/before.txt` exactly: frontier 23, registry 62, S063 mined 0,
  entries citing S063 0, knowledge 59, `entries=26 pass=26 exit=0`, `records=54 bound=54 unbound=0`,
  audit `lines=59 total=59 pass=59 … exit=0` / `expect=present expected=59 missing=0 unexpected=0
  exit=0`, census `ok` exit 0 with only the standing `W04 S028` / `W04 S029`.
- Every arm prints 26 `PASS` lines from the harness and re-verifies a real landed capture:
  `source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S060` →
  `S060:sha256 OK`, `S060:Q1..Q3 OK occurrences=1 anchor=7/15/50-ok`, exit 0.
- The frozen census command verbatim on the live lane — `sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kasegi` — exits 0 with only `W04 S028` / `W04 S029`, matching
  `c2-controls/census-before.txt`.

## 7. Fixture artifact texts (so the control survives scratch removal)

The appended registry row, identical in A1–A5:

```
| S063 | RFC 9116, Security.txt — https://www.rfc-editor.org/rfc/rfc9116.txt | spec | A | Machine-readable vulnerability-disclosure channel discovery: the location of the contact set, the field semantics, and the expiry of the published contacts | RFC 9116 sections 2-3 and 4: the /.well-known/security.txt location, the Contact, Expires, Encryption and Acknowledgments fields, and the requirement that the file be served over HTTPS | Treat a published security.txt as a dated, expiring artifact rather than as a standing guarantee that a disclosure channel is staffed, and read the encryption field as a routing instruction | mined | 2026-10-27 | 180d | corpus/knowledge/rfc-9116-security-txt.md |
```

The appended frontier row (A2–A5):

```
| F24 | RFC 9116 security.txt — machine-readable disclosure-channel discovery | admitted | knowledge/rfc-9116-security-txt.md | S063 | Read the published contact set as a dated, expiring artifact rather than as a standing guarantee that a channel is staffed. |
```

The forged manifest (`A3..A5/corpus/source-snapshots/round-41/manifest.json`, no `S063.txt` written
beside it) — a record with no `url`, no `fetched_utc`, a `0`×64 sha256 and one invented quote:

```json
{
  "purpose": "round-41 C2 junk control (ExecControls) — a fabricated S063 record with no capture bytes behind it and no fetch provenance; NOT evidence of any RFC 9116 text",
  "schema_version": 1,
  "sources": [
    {
      "id": "S063",
      "path": "S063.txt",
      "quotes": [
        {
          "id": "Q1",
          "location": "junk control — fabricated assertion, not a capture locator",
          "quote": "RFC 9116 defines the security.txt contact format for machine-readable vulnerability disclosure channels."
        }
      ],
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ]
}
```

The junk knowledge entry (`A5/corpus/knowledge/rfc-9116-security-txt.md`) — the full provenance trio
is present and is still not evidence:

```
# RFC 9116 `security.txt` — machine-readable disclosure-channel discovery (JUNK CONTROL)

source: S063 — https://www.rfc-editor.org/rfc/rfc9116.txt — capture corpus/source-snapshots/round-41/S063.txt (no such capture exists: this entry is a round-41 junk control, not evidence)
verified-at: 2026-10-27 (junk control — nothing was verified)
ground: F24
recheck: cd <arm root> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063

## Purpose

This file exists so that a do-nothing family can see how far a forged row
carries: the S063 row is mined, the F24 frontier row admits it, and this entry
cites S063 — but no capture bytes were ever fetched, so the recheck line above
cannot succeed.
```

**Nothing in this fixture is evidence about RFC 9116.** The capture bytes were never fetched; the
quote is invented; every artifact is labelled a control in its own text.

## 8. C1 do-nothing re-verification

The frozen receipt is unchanged in substance and its verdict still holds:

```
$ git -C <lane> cat-file -e fbba3d9…:corpus/instruments/r41-closure.sh
fatal: path 'corpus/instruments/r41-closure.sh' does not exist in 'fbba3d96cdf8d37c1ea41304a1ba35691329684b'   exit=128
$ git -C <lane> ls-tree -r --name-only fbba3d9… -- corpus/instruments/r41-closure.sh
(no output)   exit=0
$ (cd <freeze export> && bash corpus/instruments/r41-closure.sh --export-ref 5b29ea1439450b712581edf5f0f0bf98dfb262ab)
bash: corpus/instruments/r41-closure.sh: No such file or directory   exit=127
$ (cd <freeze export> && bash corpus/instruments/r41-closure.sh)
bash: corpus/instruments/r41-closure.sh: No such file or directory   exit=127
```

- The receipt as committed at the freeze commit is the five-line text shown verbatim in the
  transcript (`git show fbba3d9…:.ufo/waves/round-41/c1-controls/do-nothing.txt`): base line,
  the counter invocation, `bash: … No such file or directory`, `exit=127`, and the verdict "suite
  absent — the do-nothing control cannot print closed=12/12 exit=0". So the control's verdict is
  reproduced, not merely quoted.
- The erratum paragraph (40-char base, 38-char literal unresolvable) landed later at `96dbd5f`; the
  receipt's HEAD/working-tree blob digests to
  `955c605b3309eb50fc5557a0b5b20b1775d16ba348d9be4eb5b3ada4e082edff` and
  `git status --porcelain` on it is empty.
- Corroboration of the erratum: `git rev-parse --verify 5b29ea1439450b712581edf5f0f0bf98dfb262ab`
  resolves; the 38-char literal `5b29ea1439450b712581edf5f0bf98dfb262ab` fails with
  `fatal: Needed a single revision`; the live `claims.json` `base` field is the 40-char value.
- Either way the counter exits 127 because the suite file itself is absent, so the 38-vs-40 literal
  never changes this control's verdict — as the erratum says.

## 9. Write scope, scratch, tooling

- Writes: this receipt and `ExecControls.junk-s063.txt` in `.ufo/waves/round-41/wave1/`, plus
  `/fast/scratch/hyaku/kasegi-r41/ExecControls/` (six arm copies, `build.py`, `measure.py`,
  `run_counters.sh`, `transcript.txt`, header/verdict fragments). No lane, fleet, sibling-lane or
  source-tree file was modified; no mutating git/jj command ran; `MANIFEST.json`, `templates/`,
  `scripts/`, `.ufo/state/`, `corpus/` were never written.
- Scratch removed after both wave-1 files were copied and verified (`rm -rf`).
- No tool was installed or upgraded (pacman is paused host-wide; nothing was needed). Disk guard read
  before the run: `/tmp` 3%, `/var/tmp` 35%, `/fast/scratch/hyaku` 24% — green.
- Scratch incident: a sibling seat (`ExecI8Forge`) deleted the shared scratch parent
  `/fast/scratch/hyaku/kasegi-r41` at ~05:46. This seat re-created its directory and rebuilt every
  fixture from the freeze commit; the transcript's `run-utc` is a single complete pass afterwards, and
  the arm digests in §2 were re-verified after that pass.

## 10. Risks / notes

1. **Two arms exceed the item's literal shape.** The item specifies the junk row with "no capture, no
   manifest, no entry" — that is exactly `A1`. `A2`–`A5` add the artifacts needed to drive the other
   two named limbs (binding, audit), because those counters cannot see a registry row. The ladder is
   reported so no arm's evidence is attributed to another. If the L1 prefers the strict reading, the
   `A1` row is the defensible "junk twin" and it is rejected by source-recheck, the harness (no
   `PASS F24`) and the census (`E11`, exit 1).
2. **The arms are scratch trees, not the lane.** The census is therefore invoked as
   `validate --root <arm> <arm>` (lane label = the arm directory name) rather than the frozen
   `--root /home/vgpnk/Projects/shokunin kasegi`; the frozen form is run once verbatim on the live
   lane as a positive control (exit 0, `W04 S028`/`S029` only).
3. **The 58 `cd` rewrites are a fixture necessity**, not a claim about the corpus: they keep each arm
   self-contained so the audit's `cdroot` limb measures the arm. The live lane's lines are untouched
   (`git status` clean on `corpus/`), and the `base` arm with the rewrite reproduces
   `c2-controls/before.txt` exactly, which is the check that the rewrite is inert.
4. **Threat to validity:** all six arms share one harness (`frontier-recheck-count.py`) reading
   `corpus/README.md`; an arm whose F24 row were malformed would fail with a different problem name.
   A2–A4 show `missing-entry` and A5 shows `recheck-exit-2`, i.e. the row parsed and the harness
   reached the entry — the intended failures, not a parse artifact.
