# CritC2Kill — attacking C2 (coverage) at round-36 claim shape

Seat: attack critic, C2 (coverage). Leaf seat, no subagent, no lane edit, no mutating git, no peer
broadcast. All fixtures under `/fast/scratch/hyaku/kasegi-r36/CritC2Kill/` (removed before yield).
The only lane file written is this receipt.

Measurement instant: `2026-10-26T15:42:19Z`; lane head `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`
(claims freeze). The C2 artifacts are **not landed at that instant** — `corpus/SOURCES.md` carries
**0** S053 rows, `corpus/source-snapshots/round-36/` does not exist, `corpus/knowledge/epss-*` does not
exist, `.ufo/waves/round-36/c2-controls/` holds only `before.txt` (no `junk-f19.md`). So every attack
below is built as a fixture lane (a copy of `corpus/` at that commit) and run against the **committed
instruments** at that commit, which is the right direction: the matrix states what the landed C2 must
survive, and the five attacks your item names are the tests.

Instrument code measured (sha256, unmodified copies of the lane files):

```
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  scripts/sources-census.sh (fleet, read-only)
```

Their own selftests pass at that commit (`cases=6 failures=0`, `cases=10 failures=0`,
`cases=23 failures=0`), so everything below is a **scope gap in the counter battery**, not an
instrument bug.

Live-lane baseline (the "before" side of C2), measured read-only at the instant above:

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                              -> 18
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md    -> 52   (S053 rows: 0)
ls corpus/knowledge/*.md | wc -l                                        -> 47
python3 corpus/instruments/frontier-recheck-count.py                    -> entries=21 pass=21 exit=0
python3 corpus/instruments/capture-binding-check.py --root .            -> records=42 bound=42 unbound=0 exit=0
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
   -> W04 S028, W04 S029, kasegi ok                                     -> exit 0
```

## Verdict

**C2 is not falsified as a literal artifact claim, and one limb of it is falsified as a
verifiability claim.**

- Attacks 1, 3 (URL half) and 4-as-declared are **caught** by the battery, with the exact instruments
  and exact failure strings recorded below.
- **Attack 3 has a second half that is not caught and that defeats the whole battery**: a manifest
  whose `url` is byte-correct, whose `sha256` matches, whose assertion occurs in the capture — where
  the capture bytes are **a different document**. All seven counting commands go green
  (`frontier=19, registry=53, knowledge=48, citing S053=1, harness 22/22 exit 0, source-recheck 0,
  capture-binding 0, census 0`). This is round-35 gap G2, still open. For **this round** the gap is
  neutralized out of band: the planned capture is reproduced byte-identically by two independent
  live fetches (Addendum A), which is K1's Gate line — but no instrument performs that comparison, so
  the claim's own counters cannot distinguish the planned capture from the A3f construction.
- **The planned artifacts pass the battery as written** (Addendum A), so C2 as filed is achievable
  on the current bytes; the corrections below are about what the battery can *prove*, not about
  whether the round-36 landing will go green.
- **Attack 4's control is falsifiable only if the landed `junk-f19.md` carries its own fabricated
  assertion.** A twin that reuses the real entry's `recheck:` line is admitted with
  `entries=23 pass=23 exit=0`; a twin rejected only by `selection-not-cited-by-entry` is rejected on
  form, not on fabrication, and must not be credited.
- **Attack 5 is closed as a conjunction but open per counter**: `entries=22` never reads the README
  row's `sources` cell, so the row↔entry↔source binding is enforced by the claim's own
  `PASS F19 ids=S053` substring — i.e. by a human reading — not by a command. Measured: a battery
  with every counter green except the knowledge delta (`49` instead of `48`) admits a KEV entry under
  the F19 row while the EPSS entry sits unadmitted.

Impacted axes: `coverage` (C2's evidence base). No other axis is touched by this seat's findings.

## Attack matrix (commands and outcomes)

Rig: `build.py` builds one root per construction from a pristine `cp -a corpus`; each root runs

```
( cd <root> && python3 corpus/instruments/frontier-recheck-count.py --root . )
python3 <root>/corpus/instruments/source-recheck.py \
    --manifest <root>/corpus/source-snapshots/round-36/manifest.json --source S053
python3 <root>/corpus/instruments/capture-binding-check.py --root <root>
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file <root>/corpus/SOURCES.md --today 2026-10-26
```

The real F19 page was fetched live for the quote (`curl -sS https://www.first.org/epss/` → `http=200
bytes=26804`), normalized with the lane's own `capture-source.py::html_to_text` → 8,448 bytes, sha256
`4ec61c59b0e9aedf…` (`4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`), 244 lines.
The quote used is an **exact** live-page substring (occurrences=1 at line 216).

| # | construction (fixture) | harness | source-recheck S053 | capture-binding | census | verdict |
|---|---|---|---|---|---|---|
| A1 | S053 row + F19 row + entry, **no manifest** | `entries=22 pass=21 exit=1` `FAIL F19 … problems=manifest-unreadable` | `manifest UNAVAILABLE reason=missing` exit 2 | `records=42 bound=42 unbound=0` **exit 0** | **exit 0** | caught by harness + recheck; binding and census **blind** |
| A1b | row + entry + manifest record (url, sha, quote) with **capture file absent** | `FAIL F19 … recheck-exit-2` exit 1 | `S053:source UNAVAILABLE reason=missing` exit 2 | `records=43 bound=43 unbound=0` **exit 0** | exit 0 | caught by recheck/harness; **binding counts the record as bound** |
| A2 | entry quoting the live page, **no capture bytes** | `FAIL F19 … recheck-exit-2` exit 1 | `S053:source UNAVAILABLE reason=missing` exit 2 | exit 0 | exit 0 | **caught (fail-closed)** |
| A2c | capture present; manifest asserts a *different* sentence; entry body quote fabricated (`"EPSS guarantees exploitation within 30 days"`) | `PASS F19 ids=S053 exit=0`, `entries=22 pass=22 exit=0` | `Q1 OK anchor=235-ok` exit 0 | exit 0 | exit 0 | **not caught** (entry bodies unverified; r35 G1) |
| A3a | manifest `url` = `https://www.first.org/epss/data_stats` (row token = `/epss/`) | `PASS F19 exit=0` 22/22 | exit 0 | `FAIL rule=url-mismatch record=S053 row=S053 dir=round-36` **exit 1** | exit 0 | **caught by capture-binding only** |
| A3b | manifest `url` = another row's real URL (S001 CVSS guide) | `PASS F19 exit=0` 22/22 | exit 0 | `FAIL rule=url-mismatch` exit 1 | exit 0 | caught (cross-row credit blocked) |
| A3c | manifest record id `S054` (no registry row) | `FAIL F19 problems=manifest-missing-ids` | `S053:source UNAVAILABLE reason=not-listed` exit 2 | `FAIL rule=no-row record=S054` exit 1 | exit 0 | caught |
| A3d | manifest record with **no `url` field** | `PASS F19 exit=0` | exit 0 | `FAIL rule=url-mismatch record=S053 detail=absent` exit 1 | exit 0 | caught |
| A3e | **positive control**: url byte-equal, real capture bytes | `PASS F19 ids=S053 exit=0` 22/22 | `Q1 OK anchor=216-ok` exit 0 | `records=43 bound=43 unbound=0` exit 0 | exit 0 | control passes (limb not vacuous) |
| **A3f** | **content substitution**: url byte-correct, sha over the **KEV feed** (`cmp -s` identical to `round-35/S052.txt`), assertion = the KEV title `CISA Catalog of Known Exploited Vulnerabilities`; entry body still quotes EPSS text **absent from the capture** (`grep -c` → 0) | `PASS F19 ids=S053 exit=0` 22/22 | `Q1 OK anchor=2-ok` exit 0 | `records=43 bound=43 unbound=0` exit 0 | exit 0 | **NOT CAUGHT — full battery green** |
| A4 | twin with **its own** manifest assertion = fabricated sentence | `FAIL F19 … recheck-exit-1` exit 1 | `S053:Q1 MISMATCH reason=quote-not-found` **exit 1** | exit 0 | exit 0 | **caught, as the claim requires** |
| A4b | twin reusing the real selection, **no prose citation**; seeded as F20 | `FAIL F20 problems=selection-not-cited-by-entry` exit 1 | **exit 0** | exit 0 | exit 0 | rejected on **form**, not fabrication — not credit-worthy |
| A4c | same twin **with** the prose citation, admitted as F20 | `PASS F20 ids=S053 exit=0`, `entries=23 pass=23 exit=0` | **exit 0** | exit 0 | exit 0 | **NOT CAUGHT — twin admitted** |
| A5a | passing entry, **no README row** | `entries=21 pass=21 exit=0` | exit 0 | exit 0 | exit 0 | invisible (silent orphan) |
| A5b | two rows → same entry realpath | `DUPLICATE-ENTRY F19,F20 …` `entries=23 pass=23 exit=1` | exit 0 | exit 0 | exit 0 | caught |
| A5c | entry + manifested capture declare **S999** (no registry row) | `PASS F19 ids=S999 exit=0` 22/22 | `S053:… not-listed` exit 2 | `FAIL rule=no-row record=S999` exit 1 | exit 0 | harness blind; binding catches |
| A5d | cross-credit: entry declares/rechecks S053, body quotes the **KEV title** | `PASS F19 ids=S053 exit=0` 22/22 | exit 0 | exit 0 | exit 0 | **not caught** (`ids=` is binding, not provenance) |
| A5e | entry body quote fabricated outright | `PASS F19 ids=S053 exit=0` 22/22 | exit 0 | exit 0 | exit 0 | **not caught** |
| A5f | F19 row `sources` cell `S053`, entry = KEV entry (copy) | `PASS F19 ids=S052 exit=0`; `census E11 S053 missing used-by` exit 1 | exit 0 | exit 0 | exit 1 | caught only incidentally (census used-by / duplicate guard) |
| A5f2 | same, used-by repointed at the KEV copy, EPSS entry present but **unadmitted** | `PASS F19 ids=S052 exit=0`, `entries=22 pass=22 exit=0`; `frontier=19 registry=53 citing=1` | exit 0 | exit 0 | exit 0 | **every C2 command green except knowledge delta (`49` vs `48`)** |
| A5g | F19 status cell `admitted (provisional)` + compensating admitted row | F19 **absent from output**, `entries=22 pass=22 exit=0`, **no diagnostic**; `grep -c '^\| F[0-9]+ \|'` → 20 | exit 0 | exit 0 | exit 0 | unknown status **silently skipped** |
| A6 | unique quote, declared anchor `999` (out of range) | `PASS F19 exit=0` | **`Q1 OK occurrences=1 anchor=OUT-OF-RANGE`, exit 0** | exit 0 | exit 0 | not caught (anchor decorative on unique quotes) |
| A6b | unique quote, declared anchor `5` (points elsewhere) | `PASS F19 exit=0` | **`Q1 OK occurrences=1 anchor=5-BROKEN`, exit 0** | exit 0 | exit 0 | not caught, same class |
| A7 | round-36 record with `"archival": true`, no `fetched_utc` | — | — | `FAIL rule=provenance-missing record=S053` exit 1 | exit 0 | caught (archival exemption correctly closed) |

Also measured, for the claim's fourth limb: the harness **never reads** a file that is not named by a
README row. A `junk-f19.md` placed under `.ufo/waves/round-36/c2-controls/` leaves the run at
`entries=22 pass=22 exit=0`. "Harness non-admission" of a control file is therefore **trivially true
and non-discriminating** unless the twin is deliberately seeded as an admitted row (A4c), which is the
condition that makes it pass.

## The one full-battery counterexample (A3f), in the claim's own units

```
frontier rows     19          <- F19 row present
registry rows     53          <- S053 row present
knowledge files   48          <- 47 -> 48, one new entry
entries citing S053  1        <- grep -rlE '^source: S053 ' corpus/knowledge | wc -l
harness           PASS F19 knowledge/epss-exploit-prediction-scoring.md ids=S053 exit=0
                  entries=22 pass=22 exit=0
source-recheck    S053:sha256 OK / S053:Q1 OK occurrences=1 anchor=2-ok   exit 0
capture-binding   records=43 bound=43 unbound=0                          exit 0
census            W04 S028, W04 S029, ok                                  exit 0
capture bytes     cmp -s round-36/S053.txt round-35/S052.txt  -> identical (the KEV feed)
entry body quote  grep -c 'data-driven machine-learning model...' round-36/S053.txt -> 0
```

Every C2 counting command passes. Nothing in the battery reads the capture against the row's document,
and nothing reads the entry's own quote. A lane that landed this shape would be certified as having
read FIRST's EPSS page when it read the KEV feed.

## Smallest safe corrections

- **K1 (closes A3f, A2c, A5e — the real one).** Add a verify mode to the existing
  `capture-source.py` (it already fetches and normalizes): `--verify --id S053 --url <row url>
  --manifest corpus/source-snapshots/round-36/manifest.json` re-fetches, applies the same
  `html_to_text`/`collapse`, and prints `IDENTICAL|DIFFERS pinned=<sha> live=<sha> utc=<Z>`. Because
  live pages drift (the KEV feed changes daily), the honest reading is a **recorded Gate step**, not a
  fail-closed rule: the round-36 lesson records `live_fetch sha256 == manifest sha256` for S053 with the
  fetch instant. Without this line the C2 evidence base stays self-referential.
- **K2 (makes the kill rule's capture limb discriminate; closes A1b).** `capture-binding-check` counts
  a record as `bound` when its capture file is absent (`records=43 bound=43 unbound=0`, exit 0). Add
  rule **A3**: a manifest `path` that names no file in its directory is
  `FAIL rule=capture-missing record=<id>`. If that scope change is refused (it was scoped out in
  round 34), the Gate must say so explicitly and name `source-recheck` as the *only* instrument that
  fails closed on a missing capture — otherwise the kill-rule phrase "capture/manifest absent or
  unbound (capture-binding-check)" is not reproducible.
- **K3 (closes A5f2, A5c, A5g).** In `frontier-recheck-count.py`: (a) parse the README row's `sources`
  cell (column 5, today discarded by `FRONTIER_ROW`) and require the entry's declared set to be a
  subset of it, `problems=row-sources-not-matching-entry`; (b) treat any `status` value outside a
  fixed enum as fail-closed, `problems=unknown-status`, instead of skipping the row silently. With (a)
  the row↔entry↔source triple is machine-bound; the claim's `ids=S053` substring becomes redundant
  rather than load-bearing.
- **K4 (junk-twin credit rule).** Credit the twin only when **its own** `recheck:` line exits non-zero
  **and** the reason is `quote-not-found` (or `not-listed`), run from the lane root:

  ```
  line=$(grep -m1 '^recheck:' .ufo/waves/round-36/c2-controls/junk-f19.md | sed 's/^recheck:[[:space:]]*//')
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && bash -c "$line"; echo "twin_exit=$?"
  ```

  A twin rejected by `selection-not-cited-by-entry` (A4b) or whose line exits 0 (A4c) does **not**
  satisfy the C2 limb. The reproducible construction is A4's: the twin carries a twin-local manifest
  whose single assertion is the fabricated sentence over the real capture bytes →
  `S053:sha256 OK / S053:Q1 MISMATCH reason=quote-not-found`, exit 1.

Fragility note for the L1 (not a defect): the conjunction currently closes A5f2 only because
`knowledge 47 -> 48` allows exactly one new file, so the citing-count and the entry-count are forced
onto the same file. That is a coincidence of the number, not a binding; if a later round permits two
new files, A5f2 becomes a full-battery pass.

## Addendum A — replay against the planned artifacts (pre-landing, 2026-10-26T15:44–15:50Z)

The C2 seats' artifacts are in sibling receipts but not yet in the lane. I reconstructed the planned
landing in a scratch root and re-ran the battery, so the numbers below are about the bytes the L1
intends to land, not about a generic fixture:

| input | source | digest |
|---|---|---|
| `corpus/source-snapshots/round-36/S053.txt` | **my own** `curl -sS https://www.first.org/epss/` at `15:37:19Z` (26,804 B) → lane `capture-source.py::html_to_text` | `4ec61c59b0e9aedf…83e9` — **identical to ExecC2Capture's** `15:35:10Z` capture |
| `round-36/manifest.json` | `ExecC2Capture.md` §3 JSON block | `f9590c2b…` (4 quotes, anchors 216/217/217/235) |
| `SOURCES.md` S053 row | `ScribeRowS053.md` line 22 | as drafted |
| `corpus/knowledge/epss-exploit-prediction-scoring.md` | `ScribeEntryF19.md` §6, `cd` retargeted to the scratch root | as drafted |
| F19 README row | synthesized structurally (row, `sources=S053`, entry path); final wording is the row seat's | — |
| `.ufo/waves/round-36/c2-controls/junk-f19.md` | `ExecC2JunkControl.md` §2 block, `cd` retargeted | text as drafted |

```
frontier rows 19 | registry rows 53 | knowledge files 48 | entries citing S053 1
python3 corpus/instruments/frontier-recheck-count.py --root .
  PASS F19 knowledge/epss-exploit-prediction-scoring.md ids=S053 exit=0
  entries=22 pass=22 exit=0                                        harness_exit=0
source-recheck --manifest …/round-36/manifest.json --source S053
  S053:sha256 OK / Q1 OK 216-ok / Q2 OK 217-ok / Q3 OK 217-ok / Q4 OK 235-ok   exit 0
capture-binding-check --root .
  MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
  records=43 bound=43 unbound=0                                    binding_exit=0
sources-census.sh validate --file …/corpus/SOURCES.md --today 2026-10-26
  W04 S028, W04 S029, ok                                           census_exit=0
```

So the **planned** artifact set passes the C2 battery as written. Two findings attach to that:

1. **The twin's own line still exits 0** (the claim's literal rejection command, run from the lane
   root):

   ```
   LINE=$(grep -m1 '^recheck:' .ufo/waves/round-36/c2-controls/junk-f19.md | sed 's/^recheck:[[:space:]]*//')
   bash -c "$LINE"
     S053:sha256 OK / Q1..Q4 OK …                                  twin_own_line_exit=0
   ```

   The rejection is real but lives elsewhere — the twin-local pin control on the **real** capture:

   ```
   python3 corpus/instruments/source-recheck.py --manifest …/round-36/junk-assertion.json --source S053
     S053:sha256 OK
     S053:J1 MISMATCH reason=quote-not-found      ("EPSS guarantees exploitation within 30 days for every scored CVE.")
     S053:J2 MISMATCH reason=quote-not-found      ("EPSS scores CVSS severity rather than exploitation likelihood")
                                                                   pin_control_exit=1
   ```

   `ExecC2JunkControl` §7 and `MutJunkTwin` boundary-observation 1 concede the same point. K4 is
   therefore a **scoring rule** ("credit the pin control, not the twin's line"), not a request to
   change the fixture.
2. **Capture authenticity is satisfied this round, out of band.** Two independent fetches two minutes
   apart — `ExecC2Capture` at `15:35:10Z` and this seat at `15:37:19Z` — produced the same served-body
   sha256 `66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868` and the same normalized
   capture `4ec61c59b0e9aedf…83e9`. That is K1's Gate line, and it is the only thing that separates the
   planned capture from the A3f construction. **No instrument performs this comparison**; if the Gate
   does not record it, the S053 capture is bound only to its own manifest.
3. **The planned manifest's anchors all verify** (`216-ok/217-ok/217-ok/235-ok`), so the A6/A6b class
   is not present in the planned manifest. It remains latent: the comparator accepts a declared
   anchor that is out of range or holds other text whenever the quote occurs once (measured above).

## What I did not do

- No lane file touched except this receipt; no scratch file outside
  `/fast/scratch/hyaku/kasegi-r36/CritC2Kill/` (removed before yield); fleet root, sibling lanes,
  `shokuknow`, `~/Projects/*` untouched; no mutating git/jj; no subagent; no `agent://all`.
- No tooling installed or upgraded (python3 stdlib, `curl`, `sha256sum`, `cmp`, read-only `git`); no
  pacman. `curl` was used once, read-only, to fetch the live FIRST EPSS page for the A2/A3 fixtures.
- C1 (`depth:verifiability`) is out of this seat's scope and is not judged here.
