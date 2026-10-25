# ControlsRerun — source-recheck clean/corrupt controls, round-23 (F06–F08)

Seat: `L1Kasegi23.ControlsRerun-2` (leaf executor, falsify wave).
Wave: round-23 FALSIFY only. Lane: C2 coverage / Q7 executable-recheck controls.
Attacked bytes — **two baselines, because the tree moved under this seat mid-wave**:

- **Baseline A** (sections up to and including "As-landed, verbatim entry commands"): HEAD
  `953c27880a97e8d3aaf8fac44c97e0252cddcddf`
  (`round-23: mirror-fallback confinement with matrix receipts; admit F06-F08 with pinned-source rechecks`),
  `source-recheck.py` `f743942d…888d`, `manifest.json` `b8a20607…a2da`, three captures
  S018/S029/S030. Working tree clean for those paths at measurement time.
- **Baseline B** ("## Baseline B" below): the repaired pair, committed by `12edac4`/`8acb255` and still
  current at HEAD `bf9ce024` when measured — `source-recheck.py` `5f72b4c0…e12a`, `manifest.json`
  `e06aa3c…eeba`, four captures S018/S029/S030/S031, F07 re-pointed from S030 to S031; `git status`
  clean for those paths.
- **Intermediate B0** (HEAD `4d9231e`, superseded): the first repaired pair, instrument still
  `f743942d…888d` with manifest `eb6044c3…`, four sources, S030 quote still carrying `<u>` markup. Measured
  only to separate "the repair" from "the normalization edit" — it is not the landed state.

Both A and B were measured in full; B0 only on the specific questions F5/F7 raise. Neither baseline is
reported as the other, and A's commit is retained in history, so all three evidence sets stay re-derivable.

No production file was edited. No commit, push, admit, or score claim. All mutation happened in
`/tmp/kasegi-r23-falsify-ControlsRerun/`.

## Environment / identifiers (reproduce these first)

Baseline A identifiers (Baseline B's are listed in its own section):

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

## Required evidence: every stdout line and exit code (Baseline A)

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

### As-landed at Baseline A: verbatim entry commands (repo, unmutated)

Run as written, from `/tmp` (to prove the `cd` prefix makes them cwd-independent):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018  → EXIT 0 (7 × OK)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S030  → EXIT 0 (8 × OK)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S029  → EXIT 0 (7 × OK)
```
(Full stdout for these three is identical, line for line, to the three V1 `--source` blocks above. The
pre-`cd` form was also run from the repo root with the same three exit-0 results.)

## Baseline B — the repaired pair (`12edac4`/`8acb255`, current at measurement)

Identifiers at measurement (`python3 --version` → 3.14.8, same host; `git status --porcelain` clean for
these paths, `git show 8acb255:<path>` reproduces both hashes):

```
sha256sum corpus/instruments/source-recheck.py
  5f72b4c076670bb6a06e786d761495ef016ad3c29511f155a4961c9a71bbe12a   (committed, 12edac4 onward)
sha256sum corpus/source-snapshots/round-23/*
  d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4  S018.txt   (unchanged vs A)
  82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c  S029.txt   (unchanged vs A)
  673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019  S030.txt   (unchanged vs A)
  3c7ae8ba56df4e0c1d619956b894b5c3e3a7c9e35c8e1112576f521322460678  S031.txt   (new in B)
  e06aa3cdf65f316e6718342ed5dc03e289fd0132149f22c632225f3fbed0eeba  manifest.json (4 sources, 32 quotes)
```

The earlier intermediate pair (HEAD `4d9231e`) had the same four captures but instrument `f743942d` and
manifest `eb6044c3`; that pair is quoted only where F5/F7 need it.

Manifest delta vs A: `S029` quotes 7 → 9 (`art14-2a-track-context`, `art14-4a-early-warning`,
`art14-4b-incident-notification`), new `S031` source with 10 quotes, `S030` retained at 7 quotes,
`purpose` extended with an explicit ceiling sentence ("the instrument asserts substring containment only;
quote-to-location binding is human-verified and is not machine-checked"). Instrument delta vs A: a
`normalize()` fallback (`MARKUP_RE = re.compile(r"</?u>")`, whitespace collapse) reached only after the
exact-substring test fails, emitting `OK normalized=markup-whitespace`. `location` is still not read from
records — in fact **no** of the 32 quote records in manifest B carries a `location` key at all.

Variants re-derived from a fresh `copytree` of the current directory, one mutation each (mutation targets
follow the F07 re-point: the missing-source variant deletes `S031.txt`, the fabricated-quote variant
rewrites `S031/rule-4-2-11-separate-ids`):

### B1 `B_clean` → EXIT 0 (aggregate), stderr empty
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
S029:art14-2a-track-context OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4a-early-warning OK
S029:art14-4b-incident-notification OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
S031:sha256 OK
S031:effective-date OK
S031:rule-3-1-1-scope-definition OK
S031:rule-3-1-4-covered-products OK
S031:rule-3-2-4-2-request-method OK
S031:rule-4-1-2-security-impact OK
S031:rule-4-1-9-independently-fixable OK
S031:rule-4-2-1-1-first-opportunity OK
S031:rule-4-2-11-separate-ids OK
S031:rule-4-2-12-uncertainty OK
S031:version-4-2-6 OK
```
Note: the clean run is not uniformly exact. `S030:rule-4-1-9-independently-fixable` passes **only** through
the normalization fallback — direct check, `q["quote"] in S030_text` → `False`, and the tag-free sentence
`are Independently Fixable.` occurs **0** times in `S030.txt` (`S030.txt:165` holds
`…the Vulnerabilities are <u>Independently Fixable</u>.`). Cross-revision check, run from
`/tmp/kasegi-r23-falsify-ControlsRerun`:

```
$ git show 4d9231e:corpus/instruments/source-recheck.py > old_4d9231e.py   # sha256 f743942d…888d
$ python3 old_4d9231e.py --manifest <current manifest e06aa3c>             # strict, no normalize
S030:rule-4-1-9-independently-fixable MISMATCH reason=quote-not-found
EXIT=1
$ python3 old_4d9231e.py --manifest B0/manifest.json                       # 4d9231e manifest eb6044c3
EXIT=0     (that manifest quotes the sentence *with* the <u> tags, so it is an exact substring)
$ python3 <current instrument 5f72b4c0> --manifest B0/manifest.json        # new instrument, old manifest
EXIT=0
```

So the committed pair is internally consistent (before and after the edit), but the pair is **coupled**: the
current instrument is the only one under which the current manifest's S030 quote verifies, and that one line
is the fallback's, not an exact match.

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
S029:art14-2a-track-context OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4a-early-warning OK
S029:art14-4b-incident-notification OK
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
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
```
`--source S031` → **EXIT 0**
```
S031:sha256 OK
S031:effective-date OK
S031:rule-3-1-1-scope-definition OK
S031:rule-3-1-4-covered-products OK
S031:rule-3-2-4-2-request-method OK
S031:rule-4-1-2-security-impact OK
S031:rule-4-1-9-independently-fixable OK
S031:rule-4-2-1-1-first-opportunity OK
S031:rule-4-2-11-separate-ids OK
S031:rule-4-2-12-uncertainty OK
S031:version-4-2-6 OK
```

### B2 `B_digest` (S029 pin flipped) → EXIT 1 (aggregate), stderr empty
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
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
S031:sha256 OK
S031:effective-date OK
S031:rule-3-1-1-scope-definition OK
S031:rule-3-1-4-covered-products OK
S031:rule-3-2-4-2-request-method OK
S031:rule-4-1-2-security-impact OK
S031:rule-4-1-9-independently-fixable OK
S031:rule-4-2-1-1-first-opportunity OK
S031:rule-4-2-11-separate-ids OK
S031:rule-4-2-12-uncertainty OK
S031:version-4-2-6 OK
```
`--source S029` → **EXIT 1**
```
S029:sha256 MISMATCH expected=82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8d actual=82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c
```

### B3 `B_missing` (`S031.txt` deleted, manifest untouched) → EXIT 2 (aggregate), stderr empty
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
S029:art14-2a-track-context OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4a-early-warning OK
S029:art14-4b-incident-notification OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
S031:source UNAVAILABLE reason=missing
```
`--source S031` → **EXIT 2**
```
S031:source UNAVAILABLE reason=missing
```

### B4 `B_quote` (fabricated S031 quote, digest intact) → EXIT 1 (aggregate), stderr empty
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
S029:art14-2a-track-context OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4a-early-warning OK
S029:art14-4b-incident-notification OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
S031:sha256 OK
S031:effective-date OK
S031:rule-3-1-1-scope-definition OK
S031:rule-3-1-4-covered-products OK
S031:rule-3-2-4-2-request-method OK
S031:rule-4-1-2-security-impact OK
S031:rule-4-1-9-independently-fixable OK
S031:rule-4-2-1-1-first-opportunity OK
S031:rule-4-2-11-separate-ids MISMATCH reason=quote-not-found
S031:rule-4-2-12-uncertainty OK
S031:version-4-2-6 OK
```
`--source S031` → **EXIT 1** (11 lines; only `rule-4-2-11-separate-ids` is `MISMATCH`)

### B probes

| probe | mutation on B | exit | decisive line |
|---|---|---|---|
| B-P1 | `S031/version-4-2-6` quote = `" "` | **0** | `S031:version-4-2-6 OK` |
| B-P2 | `S031/effective-date` quote = `the` | **0** | `S031:effective-date OK` |
| B-P3 | wrong `location` keys added to `S018` + `S031` quotes | **0** | `S018:coordinator-lead OK`, `S031:rule-4-2-11-separate-ids OK` (full 41-line stdout in `outB/B-P3-location.txt`) |
| B-P16 | `S031/rule-3-1-1` quote rewritten to `CNAs  MUST   develop, document, and operate within a <u>Scope Definition</u>` (double spaces + injected markup) | **0** | `S031:rule-3-1-1-scope-definition OK normalized=markup-whitespace` |
| B-P12 | `S030` repointed at `S018.txt` with S018 digest + one S018 quote | **0** | `S030:sha256 OK` / `S030:rule-3-1-1-scope-definition OK` |
| B-P5 | `S018.path = "../outside-copy-S018.txt"` (digest-matching copy outside the manifest dir) | **2** | `S018:source UNAVAILABLE reason=outside-manifest-directory` |
| B-P6 | `S018.txt` replaced by symlink to that same outside file | **2** | `S018:source UNAVAILABLE reason=outside-manifest-directory` |

All Baseline B captures: `/tmp/kasegi-r23-falsify-ControlsRerun/outB/*.txt`; variant trees
`/tmp/kasegi-r23-falsify-ControlsRerun/{B_clean,B_digest,B_missing,B_quote,B_ws,B_token,B_loc,B_norm,B_shared,B_escape,B_symlink}`.

### B5 published entry commands, executed against the repo as it stands (not a copy)

Run from `cwd=/tmp`, i.e. the `cd … &&` form the entries now carry:

```
S018 → EXIT 0, 7 stdout lines   (identical to the B1 `--source S018` block)
S029 → EXIT 0, 10 stdout lines  (identical to the B1 `--source S029` block)
S031 → EXIT 0, 11 stdout lines  (identical to the B1 `--source S031` block)
```

`python3 corpus/instruments/source-recheck.py --selftest` on `5f72b4c0` → **EXIT 0**, 4/4 `PASS`
(`clean` 0, `corrupt` 1, `missing-source` 2, `missing-manifest` 2). The instrument's own controls survived
the `normalize()` edit.

## Q7 verdict on exit codes

Q7 (`corpus/QUALITY.md:48`): *"At least one missing/corrupted-source control must fail"*, and the
successful output must *"name what was checked"*.

**Baseline A** (HEAD `953c278`, instrument `f743942d`, manifest `b8a20607`, 3 sources):

| control | required | observed | match |
|---|---|---|---|
| clean manifest, all 3 sources | 0 | 0 | yes |
| one flipped digest (manifest pin) | nonzero | 1 | yes |
| one missing source path | nonzero | 2 | yes |
| one fabricated quote (digest intact) | nonzero | 1 | yes |
| corrupted snapshot bytes, pin untouched (append 1 byte to `S030.txt`) | nonzero | 1 (`S030:sha256 MISMATCH expected=673526…019 actual=8cc91b4…f46`) | yes |
| corrupted snapshot word (`Optional participant` → `Compulsory participant` in `S018.txt`) | nonzero | 1 (`S018:sha256 MISMATCH expected=d366bf4…ab4 actual=17894ba…efc2`) | yes |

**Baseline B** (committed `12edac4`/`8acb255`, instrument `5f72b4c0`, manifest `e06aa3c`, 4 sources):

| control | required | observed | match |
|---|---|---|---|
| clean manifest, all 4 sources (32 quotes) | 0 | 0 | yes |
| one flipped digest (`S029` pin) | nonzero | 1 | yes |
| one missing source path (`S031.txt`, the F07 pin) | nonzero | 2 | yes |
| one fabricated quote (`S031/rule-4-2-11`, digest intact) | nonzero | 1 | yes |
| `../` path escape with digest-matching outside file | nonzero | 2 (`outside-manifest-directory`) | yes |
| symlink to that outside file (identical bytes) | nonzero | 2 (`outside-manifest-directory`) | yes |

Exit 0 output names each checked object as `<source-id>:<sha256|quote-id> OK` (plus
`normalized=markup-whitespace` when the fallback matched); it makes no freshness or upstream claim. Exit
codes are deterministic across repeated runs and stderr stays empty in every run above. **Both baselines
match Q7 as literally written**, and the repair did not regress any control.

Severity is aggregate, not per-assertion (`source-recheck.py:155-158`; line numbers as of `f743942d`): a
mixed manifest with one digest mismatch and one missing file returns 2 and still prints both diagnostic
lines —
```
S029:sha256 MISMATCH expected=…32b80 actual=…32b8c
S030:source UNAVAILABLE reason=missing
→ EXIT 2
```

## Findings

**F1 (Q7 control verdict, falsifiable).** Both landed baselines fail closed on every corruption class
tested — digest pin, missing file, absent quote, relative-path escape, symlink escape — and pass
bit-identical bytes; no tested corruption returned 0 on either. The repair between A and B added a source
(S031) and a normalization fallback without regressing any control. Refutation: any row in either verdict
table returning 0, or a clean manifest returning nonzero. Artifacts:
`/tmp/kasegi-r23-falsify-ControlsRerun/{clean,digest,missing,quote}/` (A) and
`/tmp/kasegi-r23-falsify-ControlsRerun/{B_clean,B_digest,B_missing,B_quote}/` (B), captured stdout in
`out/*.txt` and `outB/*.txt`.

**F2 (verifiability — quote assertion is containment, not correspondence; falsifiable).**
The exact test is plain `assertion["quote"] in source_text` (`source-recheck.py:129` in `f743942d`;
`:134` in `5f72b4c0`), and `location` is never read from a record — it appears only inside the self-test
fixture (`:180`). Manifest B does not even carry the key: 0 of its 32 quote records have `location`.
Consequences, each observed on both baselines:

| probe | mutation | exit A | exit B | line |
|---|---|---|---|---|
| P1 / B-P1 | quote = `" "` (single space) | **0** | **0** | `<id> OK` |
| P2 / B-P2 | quote = `the` | **0** | **0** | `<id> OK` |
| P3 / B-P3 | deliberately wrong `location` labels | **0** | **0** | every line `OK` |
| P12 / B-P12 | an existing source id repointed at a *different* capture file with that file's digest | **0** | **0** | `<id>:sha256 OK` + `OK` |

So an exit 0 proves *"these pinned bytes contain this character sequence"*; it does **not** prove the quote
is the claimed sentence, that the sentence sits at the cited rule/article, or that a given source id labels
the capture it names. A manifest carrying `"quote": " "` is indistinguishable by exit code from a correctly
quoted one. This is now *disclosed* rather than hidden — manifest B's `purpose` says verbatim: "the
instrument asserts substring containment only; quote-to-location binding is human-verified and is not
machine-checked, so exit 0 does not prove a sentence sits at the article or rule the entry names." The
finding therefore is not that the ceiling is undeclared; it is that the ceiling is real, reproducible on
demand, and that two orderings of it (degenerate quote; relabeled capture) still exit 0 with no diagnostic.
The only content guard is truthiness: the empty string is rejected (`"quote": ""` → **EXIT 2**,
`reason=empty-quote`) while a single space passes.
Refutation: run the P1/P2/P3/P12 manifests; any nonzero exit, an `invalid-location`/shared-path diagnostic,
or a warning on a degenerate quote falsifies this finding. (Distinct from P4: lifting S029's sentence into
S030 fails, exit 1 — byte identity across sources is enforced by content.)

**F3 (ordering, falsifiable).** The pin is compared before the UTF-8 decode (`:116-118` precede `:120-123`
in `f743942d`), so a corrupted-but-undecodable snapshot reports `sha256 MISMATCH` (1), never `not-utf8`.
`not-utf8`/exit 2 is reachable only when the manifest pins the non-UTF-8 bytes themselves:
self-pinned `b"\xff\xfe\x00bad"` for `S029.txt` → **EXIT 2**, `S029:source UNAVAILABLE reason=not-utf8`.
Both codes are nonzero, so Q7 is unaffected; the distinction matters only to anyone reading exit 2 as
"missing".

**F4 (containment holds for the C2 surface; falsifiable).** With bytes *identical* to the pinned capture,
both escape shapes are refused at `:103`, on both baselines:
`path = "../outside-copy-S018.txt"` (digest-matching file outside the manifest dir) → **EXIT 2**,
`S018:source UNAVAILABLE reason=outside-manifest-directory`; replacing `S018.txt` with a symlink to that
same outside file → **EXIT 2**, same line. An uppercase `sha256` → **EXIT 2**,
`S018:manifest UNAVAILABLE reason=invalid-sha256`. No escape that still exits 0 was found.

**F5 (normalization fallback widens exit-0; falsifiable, and it is load-bearing on the clean run).**
`5f72b4c0` adds `normalize()` — `MARKUP_RE = re.compile(r"</?u>")` plus whitespace collapse — consulted
only after the exact test fails, emitting `OK normalized=markup-whitespace`. Two consequences measured:

1. The *clean* Baseline B run is not uniformly exact: `S030:rule-4-1-9-independently-fixable` passes **only**
   via the fallback. Measured, not inferred: the quote string is not a substring of `S030.txt`
   (`in` → `False`; the tag-free sentence occurs 0 times), and the previously committed strict instrument
   (`git show 4d9231e:…`, `f743942d`) run against the current manifest returns **EXIT 1** with
   `S030:rule-4-1-9-independently-fixable MISMATCH reason=quote-not-found`. The superseded `4d9231e`
   manifest (`eb6044c3`) quoted the sentence *with* `<u>…</u>` and is an exact substring, so it passes under
   both instruments — i.e. the normalization was introduced when the quote was de-marked, and the two edits
   are coupled.
2. A quote may be non-verbatim in both whitespace and markup and still pass: rewriting
   `S031/rule-3-1-1-scope-definition` to
   `CNAs  MUST   develop, document, and operate within a <u>Scope Definition</u>` (double spaces, injected
   tags) → **EXIT 0**, `S031:rule-3-1-1-scope-definition OK normalized=markup-whitespace` (B-P16).

The transformation is named on the passing line, so Q7's "names what was checked" is preserved and this is
not a silent normalization. It is still a semantic widening of "verbatim": an exit-0 line without the
annotation is exact, one with it is normalized, and a reader who treats `OK` as uniform will overstate the
match. Refutation: run B-P16; a `MISMATCH` or an unannotated `OK` falsifies it.

**F6 (landed C2 receipt is mislabeled/duplicated; falsifiable).** `.ufo/waves/round-23/c2-recheck-S030.txt`
and `c2-recheck-S031.txt` are byte-identical (`sha256 6042dad3f9e0cf13…`, 634 B each) and *both* contain
`--source S031` output — the file whose name says S030 measures S031, and S030's published recheck output
exists nowhere as a c2 receipt. The shared header also cites
`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:4`, but that entry's `recheck:` line is now at
`:5` after the S031 re-point. Both files were committed that way at `2712c99` (verified with
`git show HEAD:.ufo/waves/round-23/c2-recheck-S030.txt`), i.e. this is not a scratch artifact.
Refutation: `sha256sum` the two files (differing hashes), or find a receipt containing `S030:sha256 OK` for
the S030 capture. Reporting only — I did not rename, delete, or rewrite either receipt.

**F7 (committed baselines are real; the B pair is coupled; falsifiable).** At Baseline A, `git ls-files`
listed `manifest.json`, the three `.txt` snapshots and `source-recheck.py`, `git status --porcelain` was
empty for those paths at HEAD `953c278`, and the three F06–F08 recheck commands resolved from a clean
checkout (exit 0). At Baseline B the same holds — `git show 8acb255:corpus/instruments/source-recheck.py`
and `…/manifest.json` reproduce `5f72b4c0…` and `e06aa3c…` exactly, `git status` clean for those paths, and
the published `--source S018/S029/S031` commands exit 0 — but the two B artifacts are a package: only the
normalizing instrument verifies the de-marked S030 quote (F5), while the superseded pair at `4d9231e`
(`f743942d` + `eb6044c3`) also verifies as a package. A future revert of either half alone turns the
aggregate run red (measured: strict instrument + current manifest → exit 1). Refutation: any of those files
untracked at the stated commit, or a `git show <commit>:<path>` hash differing from the one printed here.

## Scope limits (what this report does not establish)

- No network access was used, and none is implied: an exit 0 says captured bytes match the manifest, not
  that the capture still matches the upstream PDF/page (Q7 says exactly this). Freshness is untested — in
  particular I did not confirm that `S031.txt` reproduces the CNA 4.2.6 PDF, only that the manifest pins the
  bytes that are on disk.
- I did not verify the quotes against page numbers or section anchors of the original documents; F2 shows
  the instrument cannot do so either, and manifest B now says so itself.
- The tree moved twice while this seat ran (`953c278` → `4d9231e` → `12edac4`/`8acb255` → `bf9ce024`), and
  sibling seats were still committing at measurement time. Every hash here was re-read after the fact; a
  new commit can make any of them historical. Re-run the commands before quoting a hash as current.
- I did not test a revert of *both* halves of the B pair, only of the instrument half (→ exit 1, F5/F7).
- I did not evaluate Q1–Q5 for the F06/F07/F08 entries, the C1 `resolve.py` detectors or its fixtures, or
  any admission/score outcome. Those are other seats' bytes and claims. F6 is reported as a defect in a
  landed C2 receipt, not repaired: fixing it is the integration owner's call.
- Mutations were JSON/text-level only; no attempt was made to defeat the digest with a length-extension or
  hash-collision construction. A manifest that repins the corrupted bytes it ships is self-consistent by
  construction and out of scope for a local recheck.
- Single host, Linux, CPython 3.14.8; `os.path.commonpath` behaviour cited is the POSIX one.
- Codes 1 and 2 are both treated as "nonzero" per Q7; this report does not argue that a consumer must
  distinguish them.
- Two exit codes I did **not** produce on Baseline B: no `not-utf8` (F3's branch is pin-gated, and the B
  capture is UTF-8), and no `invalid-sha256`/`invalid-source-id` re-check (those paths are unchanged between
  A and B by inspection of the diff, which touched only `normalize()` and the quote branch).

## Tooling / side effects

No packages installed or upgraded (pacman paused host-wide; nothing needed). Scratch confined to
`/tmp/kasegi-r23-falsify-ControlsRerun/` (Baseline A trees + `out/`, Baseline B trees + `outB/`, plus
`B0/` holding the `4d9231e` manifest and `old_4d9231e.py` holding that commit's instrument, both produced
with `git show <commit>:<path> > …`); `/tmp` only, no `.ufo/waves/*/scratch*` dependency, so the round-35
relocation notices from peers do not affect this report. No production file, lane tree, git index, or
sibling lane was modified — the two receipts named in F6 were read with `git show`/`sha256sum` only. Report
written: `.ufo/waves/round-23/falsify/ControlsRerun.md`.
