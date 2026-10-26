# ExecC2JunkControl — round 36: junk-twin control for F19 (FIRST EPSS, S053)

Seat: `ExecC2JunkControl` (leaf, executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`).
Axis touched: `coverage` (C2's junk-twin rejection control). All measurements 2026-10-26.
Report path: `.ufo/waves/round-36/wave1/ExecC2JunkControl.md`.

This seat wrote only this receipt and files under
`/fast/scratch/hyaku/kasegi-r36/ExecC2JunkControl/` (removed before yield, §9). No lane, fleet, sibling-lane
or source-tree file was edited; no git/jj mutation was run; no tool was installed (bash + python3 already
present, so nothing is recorded under the 2026-10-19 tooling rule). The fixture is delivered as content and
is **not** landed by this seat.

---

## 1. Inputs and digests

| input | bytes / lines | sha256 |
|---|---|---|
| `S053.txt` capture (ExecC2Capture receipt, §6) | 8,448 / 244 | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` |
| round-36 `manifest.json` (ExecC2Capture receipt, §3) | 3,566 | `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` |
| round-35 `S052.txt` (committed, wrong-source capture) | — / 27,870 | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` |
| fixture `junk-f19.md` (§2) | 1,889 | `ea078f05b0574f5584af1acfa7e8dd27636acee014339da9872591acf53cfc8b` |
| alternate `junk-f19-wrongsource.md` (§4) | 1,883 | `ce41b8dd034bf92c77c8bc7965d2fea91fdbdec0fdcd32b14d0140fc74d33559` |
| control manifest `junk-assertion.json` (§3) | 1,265 | `f947f9edc655844cc13bf51d1317dd29bc0a800d6a409a5b5a2fafe64fb265b4` |
| control manifest `wrongsource-s052.json` (§4) | 598 | `7cb28aebfe2c4937da6bf9ba7699461bf108de2a8a9d93ed64d97c89d241bccc` |

The capture and manifest are the bytes ExecC2Capture's receipt publishes (the manifest was extracted from
that receipt's `json` block and re-hashes to the receipt's `f9590c2b…`); this seat did not fetch or
re-normalize anything. `grep -cF` counts and `source-recheck` runs read that copy under
`/fast/scratch/.../capture/S053.txt`, byte-identical to the published capture.

---

## 2. Fixture to land — `.ufo/waves/round-36/c2-controls/junk-f19.md`

Land the block below **verbatim** (UTF-8, single trailing newline); sha256 must be
`ea078f05b0574f5584af1acfa7e8dd27636acee014339da9872591acf53cfc8b`. It mirrors the committed round-35
fixture location (`.ufo/waves/round-35/c2-controls/junk-f18.md`) and the real F19 entry's header shape:
H1, `source:` citing S053 with the capture path/sha256/anchors, `verified-at:`, `ground: F19`, and a
`recheck:` line that names the real S053 recheck.

````markdown
# Exploit Prediction Scoring System (EPSS) — junk twin (do-nothing control for C2)

This file is a **fabricated fixture**, not a knowledge entry. It carries the
same *shape* as the claimed F19 admission (H1 header, `source:` line citing
S053, a `recheck:` line) but quotes a sentence that does **not** exist in the
pinned capture, and it declares no manifest record. It exists to prove the F19
admission gate rejects a construction the shape counters cannot see.

source: S053 — https://www.first.org/epss/ — capture corpus/source-snapshots/round-36/S053.txt (244 lines; sha256 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9): model definition L216, probability/percentiles L217, maintenance L235
verified-at: 2026-10-26
ground: F19
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053   # fixture line: it names the real recheck of S053, so it cannot itself be the gate; the gate is the pinned comparison in the control receipt, which prints MISMATCH reason=quote-not-found on the sentence below

## What this adds

> "EPSS guarantees exploitation within 30 days for every scored CVE." — L216 (fabricated anchor)

The fabricated sentence replaces FIRST's probabilistic statement (L216:
"estimates the probability that a published CVE will be exploited in the wild
in the next 30 days") with a guarantee. The twin also claims that S053 "scores
CVSS severity rather than exploitation likelihood", which the capture does not
say anywhere.

[FABRICATED — the quoted strings above are fabrications, and the admission gate
must reject this entry. Per-string occurrence counts in the pinned capture are
measured and recorded in the control seat receipt
`.ufo/waves/round-36/wave1/ExecC2JunkControl.md`; this file asserts nothing
about them.]
````

The twin lives under `.ufo/waves/round-36/c2-controls/`, **not** `corpus/knowledge/`: it is outside the
entry glob (`corpus/knowledge/*.md`), so it cannot move the 47→48 knowledge count, `knowledge-expected.txt`,
or the Frontier row count. If it were copied into `corpus/knowledge/`, the 48-entry census would see a
49th file — do not do that.

---

## 3. Control A — the fabricated sentence is absent, and the pinned comparison rejects it

### A1. The discriminating `grep` (the item's named invocation)

```
$ cd /fast/scratch/hyaku/kasegi-r36/ExecC2JunkControl
$ grep -cF -- 'EPSS guarantees exploitation within 30 days' capture/S053.txt
0
grep_exit=1
```

Normalized count (the instrument's own comparison) is also 0: `normalized_occurrences=0`. The full fixture
sentence `EPSS guarantees exploitation within 30 days for every scored CVE.` has raw count 0 and normalized
count 0; the twin's second fabricated claim (`scores CVSS severity rather than exploitation likelihood`) also
has count 0.

### A2. `source-recheck` with the twin's sentence pinned to the committed capture → **fails**

Control manifest `junk-assertion.json` (the twin's own assertion; `S053.txt` beside it, sha256 pinned to the
published capture):

```json
{
  "schema_version": 1,
  "purpose": "Junk-twin control for F19: pins the twin's fabricated sentence against the committed S053 capture.",
  "sources": [
    {
      "id": "S053",
      "path": "S053.txt",
      "url": "https://www.first.org/epss/",
      "fetched_utc": "2026-10-26T15:35:10Z",
      "fetched_bytes": 26804,
      "snapshot_bytes": 8448,
      "lines": 244,
      "sha256": "4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9",
      "normalized": "capture-source.py html_to_text(): <script>/<style> removed, block tags (p div li tr h1-h6 section article br) to newlines, remaining tags stripped, html.unescape() applied, runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8; final newline",
      "http": {"status": 200, "content_type": "text/html; charset=UTF-8", "final_url": "https://www.first.org/epss/", "redirects": 0, "user_agent": "kasegi-shokunin/1.0", "fetched_utc": "2026-10-26T15:35:10Z"},
      "quotes": [
        {"id": "J1", "quote": "EPSS guarantees exploitation within 30 days for every scored CVE.", "anchor": 216, "location": "L216 (fabricated; not present in the capture)"}
      ]
    }
  ]
}
```

Measured (from the lane root's instrument):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py \
    --manifest /fast/scratch/hyaku/kasegi-r36/ExecC2JunkControl/manifests/junk-assertion.json --source S053
S053:sha256 OK
S053:J1 MISMATCH reason=quote-not-found
exit=1
```

### A3. The control that makes A2 discriminating — the same invocation shape on the real Q1 → **passes**

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py \
    --manifest /fast/scratch/hyaku/kasegi-r36/ExecC2JunkControl/manifests/round-36-real.json --source S053
S053:sha256 OK
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok
exit=0
```

`round-36-real.json` is ExecC2Capture's published manifest (`f9590c2b…`), unmodified. The pair
(A2 `quote-not-found` exit 1 vs A3 exit 0) is the discriminating control: the fabricated sentence is rejected
by the comparator while a sentence the capture holds, under the identical manifest/capture binding, is
accepted.

---

## 4. Control B — alternate twin: real quote, wrong `source:` (S052) → **fails**

Fixture content (scratch-only; sha256 `ce41b8dd034bf92c77c8bc7965d2fea91fdbdec0fdcd32b14d0140fc74d33559`):

````markdown
# Exploit Prediction Scoring System (EPSS) — wrong-source twin (do-nothing control for C2)

This file is a **fabricated fixture**, not a knowledge entry. It carries the
same *shape* as the claimed F19 admission but attributes a **real** EPSS
sentence to the wrong source: the header names S052 (the CISA KEV capture),
while the quoted sentence exists only in S053. It exists to prove that a
correct quote under a wrong `source:` is rejected by the source binding rather
than by the quote comparator.

source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt (27,870 lines; sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826): fabricated attribution — the sentence below is from the FIRST EPSS page, not from this feed
verified-at: 2026-10-26
ground: F19
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S052   # fixture line: the round-36 manifest lists S053, not S052, so this selection is not-listed (exit 2)

## What this adds

> "(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days." — L216 of S053.txt, attributed here to S052

The quoted sentence is real and occurs exactly once, but in the EPSS capture;
the CISA KEV feed S052 does not contain it. This twin therefore fails the
source binding even though the quote comparator would pass it against S053.

[FABRICATED ATTRIBUTION — the quote is verbatim from S053, and the `source:`
line is wrong. The admission gate must reject this entry. Occurrence counts and
the failing invocations are recorded in the control seat receipt
`.ufo/waves/round-36/wave1/ExecC2JunkControl.md`.]
````

Measured:

```
$ grep -cF -- '(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.' S053.txt
1                     # the quote is real and unique — in S053
$ grep -cF -- '<same sentence>' corpus/source-snapshots/round-35/S052.txt
0 ; grep_exit=1       # and absent from the source the twin names

# B1: the real quote pinned to the named source's committed capture
$ python3 .../source-recheck.py --manifest .../wrongsource-s052.json --source S052
S052:sha256 OK
S052:Q1 MISMATCH reason=quote-not-found
exit=1

# B2: the twin's own recheck selection against the round-36 manifest (lists S053 only)
$ python3 .../source-recheck.py --manifest .../round-36-real.json --source S052
S052:source UNAVAILABLE reason=not-listed
exit=2
```

`wrongsource-s052.json` is `{"schema_version":1,"sources":[{"id":"S052","path":"S052.txt","sha256":"d69349e8…","quotes":[{"id":"Q1","quote":"(EPSS) is a data-driven … next 30 days.","location":"L216 of S053.txt (wrong source by construction)"}]}]}`.

The alternate twin therefore fails in all three readings: the quote comparator fails it against the source it
names (`quote-not-found`), the round-36 manifest does not list S052 (`not-listed`, exit 2), and the harness
fails its row on `manifest-missing-ids` (§5, H5).

---

## 5. Harness limb — non-admission in the committed shape, and what a forged row exposes

Root: a scratch copy of `corpus/` plus the twin at `corpus/knowledge/junk-f19.md`, with the twin's own
`cd … &&` retargeted to the scratch root so the harness's `--root` governs the run. The real lane's
`grep -c 'junk-f19' corpus/README.md` is **0 / exit 1** — no Frontier row names the fixture.

| run | tree | harness output |
|---|---|---|
| H1 | twin file present, **no** Frontier row | `entries=21 pass=21 exit=0` — the file is never evaluated |
| H2 | forged `F19` row naming `knowledge/junk-f19.md`; round-36 manifest = real Q1–Q4 | `PASS F19 knowledge/junk-f19.md ids=S053 exit=0`; `entries=22 pass=22 exit=0` |
| H3 | same forged row; round-36 manifest = the twin's own `J1` sentence | `FAIL F19 knowledge/junk-f19.md ids=S053 exit=1 problems=recheck-exit-1`; `entries=22 pass=21 exit=1` |
| H5 | forged `F20` row naming the wrong-source twin (`source: S052`, recheck `--source S052`, round-36 manifest lists S053) | `FAIL F20 knowledge/junk-f19-wrongsource.md ids=S052 exit=- problems=manifest-missing-ids`; harness exit 1 |

Verbatim tail of each run:

```
entries=21 pass=21 exit=0
entries=22 pass=22 exit=0
entries=22 pass=21 exit=1
entries=23 pass=22 exit=1
```

**Attributability (measured, not a contract change).** H2 is the round-35 finding re-measured on S053: the
harness is quote-blind. It executes each entry's `recheck:` line against the pinned manifest; a twin whose
`sentence` is fabricated but whose line selects the real S053 record passes. Only H3 — where the manifest pins
the twin's own sentence — propagates rejection. So the claim's two rejection routes are distinct and both are
real: (i) **harness non-admission** = the committed tree gives the fixture no Frontier row, so the harness
never sees it (H1; `grep -c junk-f19 corpus/README.md` = 0); (ii) **`source-recheck` quote-not-found** = the
comparison that pins the twin's sentence against the committed capture (§3 A2). The twin's *own* recheck line
cannot be the gate — exactly the erratum D5 §3 statement, carried forward to S053.

---

## 6. The fixture's `recheck:` line — parse and pre-landing behaviour

```
$ LINE=$(grep '^recheck:' junk-f19.md | sed 's/^recheck: //')
$ bash -n -c "$LINE" ; echo $?
0
$ bash -c "$LINE"          # current lane, before corpus/source-snapshots/round-36/manifest.json lands
manifest UNAVAILABLE reason=missing
exit=2
```

The line is `bash -n`-parseable (Q10 shape: one command, `cd`-prefixed, note after `#`) and fails closed while
the manifest is absent (`reason=missing`, exit 2). Once the round-36 manifest lands, that same line exits 0 on
the real manifest — which is why §7 says the pinned comparison, not the fixture's line, is the discriminator.

---

## 7. What the control proves, and what it does not

- Proves: a twin that mirrors the F19 header (`source: S053`, capture path/sha256, anchors, `ground: F19`,
  real-looking `recheck:`) but quotes `EPSS guarantees exploitation within 30 days for every scored CVE.`
  is rejected — `grep -cF` = 0, and a sha256-pinned manifest carrying that sentence prints
  `S053:J1 MISMATCH reason=quote-not-found` exit 1, while the identical invocation shape on the real Q1
  exits 0. A real quote under a wrong source (S052) likewise fails (`quote-not-found` / `not-listed` /
  harness `manifest-missing-ids`).
- Proves (coverage bound): the harness's contribution is admission, not quote truth. A forged Frontier row
  plus the real manifest admits the twin (H2). The committed rejection rides on “no row naming the fixture”
  plus the pinned comparison — do not read the harness's `entries=` count as a quote check.
- Does not prove: that the real entry `corpus/knowledge/epss-exploit-prediction-scoring.md` is correct
  (ExecC2QuoteOnce / ExecC2Harness / RevEntryF19). This control only exercises the rejection of the twin.
- Does not prove: current upstream availability of `https://www.first.org/epss/`; all runs are against the
  committed bytes (`4ec61c59…`), a pinned-capture comparison, not a re-fetch.

---

## 8. No-harm / restoration evidence

- Lane writes by this seat: this receipt only. `git status --porcelain` before and after the probe shows only
  the pre-existing untracked `.ufo/waves/round-36/*` wave files (L1/sibling landings), no file of mine.
- Read-only git only (`rev-parse`, `status`, `ls-tree`); no mutating git/jj command.
- No tool installed or upgraded (bash + python3 already present).
- Input bytes unchanged by this seat: capture `4ec61c59…` (8,448 B / 244 lines), manifest `f9590c2b…`,
  S052 `d69349e8…` — all measured from read-only copies.
- The fixture is delivered as content above and was **not** written into the lane.

## 9. Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r36/ExecC2JunkControl/` (capture copy, twins, four manifests, harness
root, transcripts) is removed before yield; the removal is verified with `test -d` → exit 1. No seat tree is
left on disk by this seat.
