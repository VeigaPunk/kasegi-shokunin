# ScoutConsiderthese — mining `considerthese/2026-10-24.md` (round 25, wave 1)

Read-only seat. Every command below was run by me on 2026-10-25 against lane base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`, from the lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. No file outside
`.ufo/waves/round-25/wave1/ScoutConsiderthese.md` was written. No tool was installed or
upgraded (nothing was needed). `observed` = command output pasted verbatim;
`[INFERENCE]` = my reading, not measured.

---

## 1. Proposal ledger (acceptance a)

Source: `considerthese/2026-10-24.md` § "Self-improvement suggestions for João (proposals only,
not acted on)", dated **2026-10-24** (window 2026-10-21 08:12 → 2026-10-24 08:12 BRT; HEAD read
`8d2ce5a`).

| # | Proposal as filed (2026-10-24) | Landing evidence | Verdict |
|---|---|---|---|
| 1 | "Make the rechecker normalize and pin, not just substring-match" — strip a fixed inline-tag allowlist, **and** require exactly-once **or** a verified `SNNN.txt:LINE` anchor | `corpus/QUALITY.md:57` (**Q8**, commit `12edac4`, 2026-10-25 03:48:41 -0300) — declared normalization, receipt must print `normalized=markup-whitespace`; `corpus/QUALITY.md:64` (**Q9**, commit `d3614a2`) — path-stem = id, exactly-once-or-anchor, prints `occurrences=N`; code: `corpus/instruments/source-recheck.py:24` (`MARKUP_RE = re.compile(r"</?u>")`), `:28-30` (`normalize()`), `:166-176` (the `elif occurrences:` branch whose own comment reads *"Declared normalization (considerthese/2026-10-24 proposal 1)"*) | **LANDED** (all three conjuncts: normalize, exactly-once, anchor) |
| 2 | "Fix snapshot capture to store clean text … **record a canonical 'text' rendering beside the raw one**, so quotes don't have to anticipate `<u>` boundaries" | Only the *producer* half exists: `corpus/instruments/capture-source.py:35` (`TAG_RE = re.compile(r"<[^>]+>")`) + `:48-49` (`html_to_text`, added by `d3614a2`) strip tags at fetch time for `--kind html`. No manifest record names a rendering or a raw digest (§2.1: `records_with_render_field=0` of 23); the one dirty committed capture was never re-rendered (§2.1); `Q8`'s grounding cites this proposal but codifies only the compare-time half | **NOT LANDED** — chosen |
| 3 | "Close-r23 dossier": (a) F08 Art. 71 wording, (b) de-tag `S030.txt` **or** fix the F07 quote, (c) `manifest.json` with SHA-256 pins, (d) flip `corpus/README.md` rows | (c) `corpus/source-snapshots/round-23/manifest.json` pins S018/S029/S030/S031 (`sha256` per source; commit `2712c99`/`d3614a2`); (d) `corpus/README.md:205-207` — F06/F07/F08 all `admitted` with entry paths; (b) landed through the *or*-branch: F07 re-pointed to `S031` (`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:3`, `corpus/SOURCES.md:37`, commit `2712c99`), so no entry quotes `S030` markup any more | **LANDED** (residue: `S030.txt` bytes still carry 148 `<u>`/`</u>` tags — folded into proposal 2, not re-opened here) |
| 4 | "Downshift cadence while idle; reflect on events, not a timer" | Operator directive ("the directive says daily"). No lane artifact exists or should | **OPERATOR-OWNED** — out of lane scope |
| 5 | "Decide the fate of draft PR #1 and the 8 README branches" | No lane artifact; branch/PR pruning is operator-owned | **OPERATOR-OWNED** — out of lane scope |

Two proposals are landed (1, 3), two are operator-owned (4, 5), one is not (2). Proposal 2 is the
only still-unimplemented lane action, so it is the chosen one.

---

## 2. Chosen proposal 2, grounded (acceptance b)

### 2.1 Current state — commands and verbatim output

**Counter (the proposed instrument's shape, run inline over committed bytes):**

```
$ python3 - <<'PY'   # counts snapshots, manifest records, render fields, dirty captures
...
PY
snapshots=28
manifest_records=23
records_with_render_field=0
snapshots_with_capture_markup=1 ['corpus/source-snapshots/round-23/S030.txt']
snapshots_with_extraction_annotations=1 ['corpus/source-snapshots/round-24/S010.txt']
corpus/source-snapshots/round-23 txt=4 manifest=yes
corpus/source-snapshots/round-24 txt=19 manifest=yes
corpus/source-snapshots/round-25 txt=5 manifest=NO
S030 <u> occurrences=74 </u>=74 page_comments=12
```

The manifest record schema is exactly four keys — no rendering, no raw digest:

```
$ python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));...;print(sorted(ks))"
['id', 'path', 'quotes', 'sha256']
```

(round-23 manifest: same four keys.)

**The markup still binds a live assertion** — the quote is absent from the committed bytes and
present only after `normalize()`:

```
$ python3 - <<'PY'   # F07's historical S030 quote, raw vs normalized
src=open('corpus/source-snapshots/round-23/S030.txt').read()
q="CNAs SHOULD consider whether the Vulnerabilities are Independently Fixable."
raw count: 0
normalized count: 1
raw line containing: [165, 211, 212, 213]
PY

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json
...
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace occurrences=1
...
S029:art14-2a-early-warning OK occurrences=2 anchor=10-ok
exit=0
```

**Capture-time stripping is lossy and unrecorded.** `S010.txt` is a Project Zero HTML post
(`corpus/SOURCES.md:16`) whose committed bytes contain a genuine C++ listing. Re-rendering the
*committed bytes* through the instrument's own default `html_to_text`:

```
$ python3 - <<'PY'   # import capture-source.py, re-render S010's committed bytes as html
committed bytes: 36452 html_to_text(bytes): 26571
committed sha256: f22f8c63e55e3047
re-rendered as html sha256: d6c3d6b39d38f6a3
<cassert>                  committed=1 html-render=0
<iostream>                 committed=1 html-render=0
<optional>                 committed=1 html-render=0
<no newline at the end>    committed=3 html-render=0
<skipped 3033 bytes>       committed=1 html-render=0
PY
```

And the committed bytes carry extraction annotations that **no instrument in this lane emits**
(`grep -rn "skipped" corpus/instruments/` returns only an unrelated `density.py` docstring line):

```
$ grep -n -B1 -A1 'skipped 3033 bytes' corpus/source-snapshots/round-24/S010.txt
582:==1410137==ERROR: AddressSanitizer: heap-buffer-overflow on ad<skipped 3033 bytes>ect redzone: bb
```

while the manifest's own purpose sentence attributes the whole family to the instrument:

> "S001-S015 … captured 2026-10-25 by `corpus/instruments/capture-source.py`"
> — `corpus/source-snapshots/round-24/manifest.json`, `purpose`

`observed`: the sentence is contradicted by committed bytes. `[INFERENCE]` on cause (an earlier
ad-hoc extraction path, not the instrument) — but the *undetectability* is observed, and that is
the defect.

### 2.2 The gap, in three limbs

1. **No rendering is recorded.** 23 of 23 manifest records carry `{id,path,quotes,sha256}` and
   nothing else. A reader cannot tell whether a snapshot is tag-stripped text, `pdftotext`
   output, or as-served text — the three branches at `capture-source.py:84-88` are
   indistinguishable from the committed artifact. Proposal 2's "record a canonical text
   rendering beside the raw one" is exactly this missing record, and it is missing.
2. **The raw is not recorded either.** `capture()` (`capture-source.py:82-97`) prints
   `fetched_bytes` and the text `sha256` to stdout and returns only the text digest. Nothing
   persists the raw fetch digest, so a snapshot is not re-derivable from committed bytes and the
   `<skipped 3033 bytes>` truncation in S010 is invisible to every check the lane owns.
3. **The capture-time stripper destroys legitimate content.** `TAG_RE = re.compile(r"<[^>]+>")`
   (`capture-source.py:35`) is a *deny-nothing* pattern: it deletes `<cassert>`, `<iostream>`,
   `<optional>` — real document text — as readily as `<u>`. Measured: a re-render of S010 loses
   9,881 bytes (36,452 → 26,571) and changes the digest (`f22f8c63…` → `d6c3d6b3…`). Today the
   only reason nothing breaks is that S010's quotes (`Q1`, `Q2`, …) do not span the code listing
   — `observed`: no manifest quote contains `<` or `>` (`0` rows). One quoted diff line would
   turn this into a silent MISMATCH-or-worse.

Note the asymmetry that makes this the right proposal to land now: **Q8 already promises the
outcome** ("an entry never has to quote converter markup to pass", `QUALITY.md:57`) but delivers
it by compare-time regex, so the promise holds for exactly one consumer — `source-recheck.py`.
Every other reader of `corpus/source-snapshots/` (a critic grepping a quote, a future instrument,
the round-25 entries being written now) sees the markup.

### 2.3 Minimal landing

Three edits, no new dependency, no quote edits:

**(a) Code — make the stripper name-aware** (`corpus/instruments/capture-source.py:35`):

```python
TAG_RE = re.compile(
    r"</?(?:a|b|i|u|em|strong|p|div|li|tr|td|th|h[1-6]|br|span|code|pre|ul|ol"
    r"|table|thead|tbody|section|article|header|footer|nav|sup|sub|blockquote"
    r"|figure|figcaption)\b[^>]*>", re.I)
```

Verified against the lane's own two fixtures:

```
$ python3 - <<'PY'   # allowlist TAG_RE vs the current <[^>]+>
S030 allowlist: <u> left=148, current-RE left=160     # 148 = all <u>/</u>; 160 = 148 tags + 12 page comments
<cassert>                  allowlist_keeps=True
<iostream>                 allowlist_keeps=True
<optional>                 allowlist_keeps=True
<skipped 3033 bytes>       allowlist_keeps=True
<no newline at the end>    allowlist_keeps=True
S010 allowlist deletions=0 current-RE deletions=22
PY
```

i.e. the allowlist strips every `<u>` in S030 and deletes **nothing** from S010's code listing.
`--selftest` (`capture-source.py:100-117`) gains one case: `"<u>gamma</u> <cassert>"` →
`"gamma <cassert>"`.

**(b) Record — the manifest carries the rendering and the raw digest.** `capture()` gains
`--record <manifest>` (or a sidecar `<round>/capture-log.json`), writing per source:
`{id, url, kind, render, fetched_bytes, raw_sha256, text_sha256, utc}` where `render ∈
{html-strip-tags, pdf-pdftotext, text-collapse}`. The 23 existing records are backfilled with
`render` only where it is provable from bytes; the two that are not provable are declared
(`S010: render=unrecorded, lossy=true`; `S030: render=unrecorded, markup=u-148`) rather than
guessed — R9/R8 discipline (append the declaration, do not rewrite the historical record).

**(c) Criterion — `corpus/QUALITY.md`, new **R13** beside R3** (R3 already governs "an
instrument verdict names its matcher and definition"; a snapshot's rendering is the same class of
obligation, and Q-series is entry-scoped while this is instrument/record-scoped):

> **R13** — A committed capture names its rendering and its raw digest: each manifest source
> record carries `render:` (the transformation applied), `raw_sha256:` (the fetched bytes) and the
> instrument that produced it. A capture that carries converter markup or extraction annotations
> must be declared (`markup:`, `lossy:`) together with the compare-time normalization it depends
> on; an undeclared dirty capture is a rejection. A re-render that changes a pinned `sha256` is a
> new capture under R8, never an in-place edit.
> Grounded in `considerthese/2026-10-24.md` proposal 2 (2026-10-24); `QUALITY.md:57` Q8 delivered
> only the compare-time half; measured today: 0/23 records name a rendering, S030 holds 148
> `<u>` tags, S010 holds a `<skipped 3033 bytes>` truncation.

**Counter** (makes R13 measurable; ~25 lines, same shape as `frontier-recheck-count.py`):
`python3 corpus/instruments/snapshot-hygiene.py --root corpus/source-snapshots` printing
`snapshots=N recorded=R render_ok=K markup=M lossy=L undeclared=U exit=0|1`, failing closed when
any `.txt` has no manifest record or any dirty capture lacks its declaration.

**Today's value of that counter** (measured inline above): `snapshots=28 recorded=23 render_ok=0
markup=1 lossy=1 undeclared=5 exit=1` — the 5 undeclared are the round-25 captures, which have
no `manifest.json` yet (see §4).

**Do-nothing control / kill rule.** Unchanged bytes score `render_ok=0 markup=1 lossy=1 exit=1`;
the claim is void if the counter passes by deleting S030 or by relaxing `TAG_RE` back to
`<[^>]+>`, and void if a "fix" changes S010's pinned `sha256` in place instead of filing a new
capture.

---

## 3. One line for the L1 report (acceptance c)

```
considerthese: proposal 2 mined — snapshots record neither rendering nor raw digest (0/23 records), and the capture-time stripper silently deletes literal <cassert> from S010 (36,452→26,571 B); land R13 + a render/raw_sha256 record field.
```

---

## 4. Residual unknowns and notes for the L1

- **`corpus/source-snapshots/round-25/` has 5 captures and no `manifest.json`** (`observed`:
  `round-25 txt=5 manifest=NO`). Every C2 recheck line that names a round-25 capture exits 2
  until a manifest with `sha256` pins + quote assertions exists. That is a C2 dependency, not
  mine to land — flagging it because the hygiene counter above fails on exactly those five.
- **`QUALITY.md:57` Q8's grounding cites proposals "1 and 2"** but its text codifies only
  proposal 1's compare-time normalization. If proposal 2 lands as R13, Q8's citation should be
  narrowed to proposal 1 (R6: same-line suffix, no anchor shift).
- **Candidate routed defect (D25-x)**: `corpus/source-snapshots/round-24/manifest.json` `purpose`
  claims S001-S015 were "captured 2026-10-25 by corpus/instruments/capture-source.py", but
  S010's committed bytes contain `<skipped 3033 bytes>` and `<no newline at the end>`, which no
  instrument in `corpus/instruments/` emits (`observed` via `grep -rn "skipped" corpus/instruments/`).
  R2 applies: the self-description is a claim and its cited producer does not produce those bytes.
- **Not re-opened**: proposal 3's residue (S030 still 148 tags) is subsumed by proposal 2's
  declaration path; re-rendering S030 would change a pinned `sha256` and 12 page-comment line
  anchors, which R8/R9 make a new capture, not an edit — out of scope for a read-only seat.
- **Confidence**: §1 verdicts and every number in §2 are `observed` from commands run today on
  committed bytes. The S010 cause ("an ad-hoc extraction path produced it") is `[INFERENCE]`;
  the fact that the committed bytes cannot be reproduced by the instrument is `observed`.
