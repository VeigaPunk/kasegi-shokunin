# ControlsRerun — source-recheck clean/corrupt controls, round-23 (F06–F08)

Seat: `L1Kasegi23.ControlsRerun-2` (leaf executor, falsify wave).
Wave: round-23 FALSIFY only. Lane: C2 coverage / Q7 executable-recheck controls.
Attacked bytes: HEAD `953c27880a97e8d3aaf8fac44c97e0252cddcddf`
(`round-23: mirror-fallback confinement with matrix receipts; admit F06-F08 with pinned-source rechecks`),
working tree clean for every path below (`git status --porcelain -- corpus/source-snapshots/round-23 corpus/instruments/source-recheck.py` → empty output, exit 0).

No production file was edited. No commit, push, admit, or score claim. All mutation happened in
`/tmp/kasegi-r23-falsify-ControlsRerun/`.

## Environment / identifiers (reproduce these first)

```
python3 --version                → Python 3.14.8
sha256sum corpus/instruments/source-recheck.py
  f743942d9643c930453c415414fd4468486140049541e3f7babc935581ae888d  corpus/instruments/source-recheck.py
sha256sum corpus/source-snapshots/round-23/*.txt corpus/source-snapshots/round-23/manifest.json
  d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4  S018.txt
  82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c  S029.txt
  673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019  S030.txt
  b8a20607e03743f6782093167b39d65edbf5c742a987488065a54eff79f4a2da  manifest.json
```

The three digests in `manifest.json` equal the bytes of `S018.txt`/`S029.txt`/`S030.txt` (same values
listed above), so the pinned baseline is self-consistent before any mutation.

Instrument paths used (unmodified, read from the repo — not a copy):

```
corpus/instruments/source-recheck.py:103   containment: os.path.commonpath(base, resolved) != base → exit 2
corpus/instruments/source-recheck.py:116-118 digest: actual != expected → "sha256 MISMATCH", exit 1
corpus/instruments/source-recheck.py:120-123 UTF-8 decode failure → "source UNAVAILABLE reason=not-utf8", exit 2
corpus/instruments/source-recheck.py:129   quote test: `if assertion["quote"] in source_text` (raw substring)
corpus/instruments/source-recheck.py:155-158 aggregate severity: 2 wins, else first 1 sticks
```

F06/F07/F08 recheck fields under test (verbatim, as they read during this wave):
`corpus/knowledge/multiparty-vulnerability-coordination.md:4` → `--source S018`,
`cna-assignment-and-vulnerability-rules.md:4` → `--source S030`,
`cra-manufacturer-reporting-duties.md:4` → `--source S029`, each as
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S0NN`.

Concurrent-change note: these three lines were bare
`python3 corpus/instruments/source-recheck.py --manifest … --source S0NN` when I read them at the start of
this seat and gained the `cd … &&` prefix during the wave (another seat's edit; `git status` shows the three
knowledge files modified). Both forms were executed and both exit 0. The artifacts under test —
`source-recheck.py` (`f743942d…888d`) and all four files under `corpus/source-snapshots/round-23/`
(including `manifest.json` `b8a20607…a2da`) — are byte-identical to the start of this seat, re-hashed after
the variant runs, and `git diff --stat` for those paths is empty.

## Setup

```
mkdir -p /tmp/kasegi-r23-falsify-ControlsRerun
cp -a corpus/source-snapshots/round-23/. /tmp/kasegi-r23-falsify-ControlsRerun/base/
```

`base/` is byte-identical to the committed capture (digests above). Every variant is a `copytree` of
`base/`, then exactly one mutation, then:

```
python3 corpus/instruments/source-recheck.py --manifest /tmp/kasegi-r23-falsify-ControlsRerun/<variant>/manifest.json [--source S018|S029|S030]
```

run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Manifest `path` values are relative to the
manifest's own directory, so the instrument reads the scratch copies, never the repo.

Variant mutations (exactly one per variant):

| variant | mutation |
|---|---|
| `clean` | none (byte-identical copy) |
| `digest` | `S029.sha256` last hex char `…32b8c` → `…32b8d` |
| `missing` | `S030.txt` deleted; manifest untouched |
| `quote` | `S018` / `coordinator-def` quote replaced with `Coordinators MUST publish a public vulnerability register within 24 hours.` |

## Required evidence: every stdout line and exit code

### V1 `clean` — expected exit 0

`... --manifest .../clean/manifest.json` → **EXIT 0**, stderr empty

```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
S029:sha256 OK
S029:art14-2a-early-warning OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
```

`--source S018` → **EXIT 0**
```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
```
`--source S029` → **EXIT 0**
```
S029:sha256 OK
S029:art14-2a-early-warning OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
```
`--source S030` → **EXIT 0**
```
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
```

### V2 `digest` (one flipped SHA-256) — expected nonzero

`... --manifest .../digest/manifest.json` → **EXIT 1**, stderr empty
```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
S029:sha256 MISMATCH expected=82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8d actual=82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
```
`--source S018` → **EXIT 0** (7 × `S018:… OK`, identical to V1/S018).
`--source S029` → **EXIT 1**
```
S029:sha256 MISMATCH expected=82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8d actual=82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c
```
`--source S030` → **EXIT 0** (8 × `S030:… OK`, identical to V1/S030).

### V3 `missing` (source path has no file) — expected nonzero

`... --manifest .../missing/manifest.json` → **EXIT 2**, stderr empty
```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
S029:sha256 OK
S029:art14-2a-early-warning OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
S030:source UNAVAILABLE reason=missing
```
`--source S018` → **EXIT 0**; `--source S029` → **EXIT 0** (both identical to V1);
`--source S030` → **EXIT 2**
```
S030:source UNAVAILABLE reason=missing
```

### V4 `quote` (fabricated quote, digest intact) — expected nonzero

`... --manifest .../quote/manifest.json` → **EXIT 1**, stderr empty
```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def MISMATCH reason=quote-not-found
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
S029:sha256 OK
S029:art14-2a-early-warning OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
```
`--source S018` → **EXIT 1** (7 lines, `coordinator-def MISMATCH reason=quote-not-found`);
`--source S029` → **EXIT 0**; `--source S030` → **EXIT 0** (identical to V1).

### Instrument self-controls

`python3 corpus/instruments/source-recheck.py --selftest` → **EXIT 0**
```
SELFTEST clean PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
```

### As-landed, verbatim entry commands (repo, unmutated)

Run as written, from `/tmp` (to prove the `cd` prefix makes them cwd-independent):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018  → EXIT 0 (7 × OK)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S030  → EXIT 0 (8 × OK)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S029  → EXIT 0 (7 × OK)
```
(Full stdout for these three is identical, line for line, to the three V1 `--source` blocks above. The
pre-`cd` form was also run from the repo root with the same three exit-0 results.)

## Q7 verdict on exit codes

Q7 (`corpus/QUALITY.md:48`): *"At least one missing/corrupted-source control must fail"*, and the
successful output must *"name what was checked"*.

| control | required | observed | match |
|---|---|---|---|
| clean manifest, all 3 sources | 0 | 0 | yes |
| one flipped digest (manifest pin) | nonzero | 1 | yes |
| one missing source path | nonzero | 2 | yes |
| one fabricated quote (digest intact) | nonzero | 1 | yes |
| corrupted snapshot bytes, pin untouched (append 1 byte to `S030.txt`) | nonzero | 1 (`S030:sha256 MISMATCH expected=673526…019 actual=8cc91b4…f46`) | yes |
| corrupted snapshot word (`Optional participant` → `Compulsory participant` in `S018.txt`) | nonzero | 1 (`S018:sha256 MISMATCH expected=d366bf4…ab4 actual=17894ba…efc2`) | yes |

Exit 0 output names each checked object as `<source-id>:<sha256|quote-id> OK`; it makes no freshness or
upstream claim. Exit codes are deterministic across repeated runs and stderr stays empty in all cases.
**The four required variants match Q7 as literally written.** Severity is aggregate, not per-assertion
(`source-recheck.py:155-158`): a mixed manifest with one digest mismatch and one missing file returns 2
and still prints both diagnostic lines —
```
S029:sha256 MISMATCH expected=…32b80 actual=…32b8c
S030:source UNAVAILABLE reason=missing
→ EXIT 2
```

## Findings

**F1 (Q7 control verdict, falsifiable).** The landed instrument fails closed on all three corruption
classes tested (digest pin, missing file, absent quote) and passes bit-identical bytes; no tested
corruption returned 0. Refutation: any of the six rows above returning 0, or the clean manifest returning
nonzero. Scratch artifacts: `/tmp/kasegi-r23-falsify-ControlsRerun/{clean,digest,missing,quote}/`,
captured stdout in `/tmp/kasegi-r23-falsify-ControlsRerun/out/*.txt`.

**F2 (verifiability — quote assertion is raw substring, nothing more; falsifiable).**
`source-recheck.py:129` is plain `assertion["quote"] in source_text`, and `location` is never read from a
record (it appears only in the self-test fixture, `source-recheck.py:180`). Consequences, each observed:

| probe | mutation | exit | line |
|---|---|---|---|
| P1 | `S018/coordinator-def` quote = `" "` (single space) | **0** | `S018:coordinator-def OK` |
| P2 | `S029/art14-2a-early-warning` quote = `the` | **0** | `S029:art14-2a-early-warning OK` |
| P3 | `S030` quotes given deliberately wrong `location` labels (`"Section 9.9, page 999"`, `"page 1"`) | **0** | all 8 `S030:… OK` |
| P12 | `S030` repointed at `S018.txt` with S018's digest and one S018 quote | **0** | `S030:sha256 OK`, `S030:rule-3-1-1-scope-definition OK` |

So an exit 0 proves *"these pinned bytes contain this character sequence"*; it does **not** prove the quote
is the claimed sentence, at the claimed location, or that source id `S030` labels the CNA capture. A
manifest carrying `"quote": " "` is indistinguishable, by exit code, from a correctly quoted one — the
exit-code contract of Q7 is satisfied while the Q3-style "exact located quote" property is unverified.
The only content guard is truthiness (`source-recheck.py`, `not assertion["quote"]`): the empty string is
rejected — `"quote": ""` → **EXIT 2**, `S018:coordinator-def UNAVAILABLE reason=empty-quote` — while a single
space passes P1 with exit 0.
Refutation: run the P1/P2/P3/P12 manifests; any nonzero exit, an `empty-quote`/`invalid-location`
diagnostic, or a warning on a shared `path`, falsifies this finding. (Distinct from P4: lifting S029's
sentence into S030 does fail, exit 1 — byte identity across sources *is* enforced by accident of content.)

**F3 (ordering, falsifiable).** The pin is compared before the UTF-8 decode (`:116-118` precede `:120-123`),
so a corrupted-but-undecodable snapshot reports `sha256 MISMATCH` (1), never `not-utf8`.
`not-utf8`/exit 2 is reachable only when the manifest pins the non-UTF-8 bytes themselves:
self-pinned `b"\xff\xfe\x00bad"` for `S029.txt` → **EXIT 2**, `S029:source UNAVAILABLE reason=not-utf8`.
Both codes are nonzero, so Q7 is unaffected; the distinction matters only to anyone reading exit 2 as
"missing".

**F4 (containment holds for the C2 surface; falsifiable).** With bytes *identical* to the pinned capture,
both escape shapes are refused at `:103`:
`path = "../outside-copy-S018.txt"` (digest-matching file outside the manifest dir) → **EXIT 2**,
`S018:source UNAVAILABLE reason=outside-manifest-directory`; replacing `S018.txt` with a symlink to that
same outside file → **EXIT 2**, same line. An uppercase `sha256` → **EXIT 2**,
`S018:manifest UNAVAILABLE reason=invalid-sha256`. No escape that still exits 0 was found.

**F5 (committed baseline is real, falsifiable).** `git ls-files` lists `manifest.json`, all three `.txt`
snapshots and `source-recheck.py`; `git status --porcelain` for those paths is empty at HEAD `953c278`.
The F06–F08 recheck commands therefore resolve from a clean checkout, and all three exit 0 as written.
Refutation: any of those files untracked/modified at HEAD.

## Scope limits (what this report does not establish)

- No network access was used, and none is implied: an exit 0 says captured bytes match the manifest, not
  that the capture still matches the upstream PDF/page (Q7 says exactly this). Freshness is untested.
- I did not verify the quotes against page numbers or section anchors of the original documents; F2 shows
  the instrument cannot do so either.
- I did not evaluate Q1–Q5 for the F06/F07/F08 entries, the C1 `resolve.py` detectors or its fixtures, or
  any admission/score outcome. Those are other seats' bytes and claims.
- Mutations were JSON/text-level only; no attempt was made to defeat the digest with a length-extension or
  hash-collision construction. A manifest that repins the corrupted bytes it ships is self-consistent by
  construction and out of scope for a local recheck.
- Single host, Linux, CPython 3.14.8; `os.path.commonpath` behaviour cited is the POSIX one.
- Codes 1 and 2 are both treated as "nonzero" per Q7; this report does not argue that a consumer must
  distinguish them.

## Tooling / side effects

No packages installed or upgraded (pacman paused host-wide; nothing needed). Scratch confined to
`/tmp/kasegi-r23-falsify-ControlsRerun/`; `/tmp` only. No production file, lane tree, git index, or sibling
lane was modified. Report written: `.ufo/waves/round-23/falsify/ControlsRerun.md`.
