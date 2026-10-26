# RevHarnessSync — independent recomputation of the F20 harness delta (round 37, C2 / coverage)

Seat: `RevHarnessSync` (leaf reviewer, no subagent dispatch). Judged axis: coverage.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — the only lane write is this receipt; all work
copies lived under `/fast/scratch/hyaku/kasegi-r37/RevHarnessSync-2/` (removed before this receipt was
finalized). No mutating git command (only `rev-parse`, `log`, `status`, `show`, `diff`, `archive`).
Base `b56a41680cefd391868c1c370dc063c69d827e7d`; freeze `224df74db2a46d627ae1475a72ca48796bbd177c`;
lane head observed `b362068195d5489aa94b31e6ec8f880c367e0ba0` (freeze + wave evidence + claims-erratum-1).

**Verdict: SUPPORTS C2.** The harness delta is exactly as claimed: base `entries=22 pass=22 exit=0`
maps one-to-one onto F01–F19 (no hidden gaps); base + F20/S054/entry/capture/manifest in a scratch
mirror gives `entries=23 pass=23 exit=0` with `PASS F20 … ids=S054 exit=0`; `--selftest` `cases=6
failures=0`; the F20 row/entry/manifest/capture all bind source id S054; and the capture is genuine
(I re-fetched the live page and re-normalized it to byte-equality with the pinned capture). One
measured limit, stated in §4: the harness chain cannot by itself reject a *self-consistently
fabricated* capture — it enforces local consistency only. For S054 that limit is discharged
out-of-band by my live re-fetch (§4.3).

## 1. What `corpus/instruments/frontier-recheck-count.py` checks per admitted frontier row

Read in full (433 lines) from the lane working tree; identical file confirmed in the base export.
Per `corpus/README.md` table row whose first cell matches `F<digits>` and whose status cell is exactly
`admitted` (any other status drops the row from the denominator), one record per comma-separated entry
path in the entry cell:

1. **Entry exists** at `root/<path>` or `root/corpus/<path>`; else `missing-entry` (row id + path
   printed, no traceback).
2. **Declaration set** = header `source: S<digits>` lines ∪ per-source evidence bullets
   (`- S<digits> …`). Empty header → `no-source-line`.
3. **Recheck shape**: first `recheck:` line must contain `source-recheck.py`, must not contain
   `--selftest` (`not-a-recheck-invocation`), must carry ≥1 `--source S<digits>`
   (`no-source-selection`) and a `--manifest PATH` (`no-manifest`).
4. **Bidirectional id binding (rule A)**: declared set ⊆ recheck ids (`header-sources-not-rechecked`)
   and recheck ids ⊆ declared set (`selection-not-declared-by-entry`).
5. **Citation limb**: recheck ids ⊆ S-ids mentioned on non-declaration/non-recheck lines
   (`selection-not-cited-by-entry`) — the recheck line cannot vouch for itself.
6. **Manifest (rule B)**: readable JSON, `schema_version == 1`, `sources[]` list of dicts, must list
   every recheck id (`manifest-unreadable` / `manifest-missing-ids`). Only `schema_version` and
   `sources[].id` are read.
7. **Execution (rule D)**: only when 1–6 hold, the line runs via `bash -c` from the lane root;
   non-zero exit → `recheck-exit-N`.
8. **Run-level fail-closed**: duplicate entry realpath → `DUPLICATE-ENTRY` + exit 1 (even if
   `pass=entries`); zero records → exit 1; README read error → exit 2; exit 0 iff every record passes.

What it does **not** read (measured, §4 B2b/B4): `corpus/SOURCES.md` registry rows, the README
`sources` cell, manifest `url`/`fetched_utc`/capture bytes content beyond the recheck line's own
verdict. `--selftest` runs 6 fixture lanes (stub `source-recheck.py` exiting 0), measuring the
binding rules, never the lane.

## 2. Base: entries=22 pass=22 maps exactly to F01–F19

```
$ git archive b56a4168 | tar -x -C $S/base
$ python3 $S/base/corpus/instruments/frontier-recheck-count.py --root $S/base
PASS F01 knowledge/cvss-v4-severity-and-vector.md ids=S001 exit=0
... (F01–F19, every line PASS; ids S001…S053) ...
PASS F19 knowledge/epss-exploit-prediction-scoring.md ids=S053 exit=0
entries=22 pass=22 exit=0                                   [exit 0]
```

Mapping check, no hidden gaps: the base README has exactly 19 `F<nn>` rows; all 19 carry status
`admitted` (a non-admitted row would have left the denominator and entries would be < 22); ids are
contiguous F01–F19, each appearing exactly once; F09, F10, F11 each name **two** entry paths in one
cell, so 19 − 3 + 6 = **22 entry records** — the count is fully accounted for. Corroborating run on
the live tree at head `b362068` (read-only): `entries=22 pass=22 exit=0`. Selftest:

```
$ python3 corpus/instruments/frontier-recheck-count.py --selftest
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0                                 [exit 0]
```

(Note: the C1 claim's `cases=14 failures=0` belongs to `r37-closure.sh`; this instrument's selftest
is 6 cases. No conflict — different suites.)

## 3. Simulation: base + F20/S054 delta → entries=23 pass=23

Scratch mirror = base export plus exactly five additions, built independently from the claims text +
erratum-1 URL + the sibling capture/quote receipts (my own files, my own bytes):

1. `corpus/README.md` row after F19: `| F20 | SSVC — Stakeholder-Specific Vulnerability
   Categorization | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |
   S054 | … |`
2. `corpus/SOURCES.md` row after S053: registry id **S054**, kind docs, tier **A**, status **mined**,
   opened **2026-10-26**, URL = erratum-corrected `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`.
3. `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`: `source: S054 — <URL>
   — capture corpus/source-snapshots/round-37/S054.txt (518 lines, sha256 ff3f3b2c…)`, `ground: F20`,
   `recheck: python3 corpus/instruments/source-recheck.py --manifest
   corpus/source-snapshots/round-37/manifest.json --source S054`, prose citing S054, four pinned
   claims.
4. `corpus/source-snapshots/round-37/S054.txt` — the real capture bytes (extracted from the
   ExecC2Capture receipt's byte-exact block; **verified** `sha256 = ff3f3b2cc82819eb52b4292f1fee3efa
   ef40e7102962494cceabc1d7e5fdce21`, 518 lines, 32623 bytes).
5. `corpus/source-snapshots/round-37/manifest.json` — schema 1, one record `id: S054`, `path:
   S054.txt` (stem = id), that sha256, the four landed quotes Q1–Q4 (anchors 247/259/277/367), url +
   `fetched_utc 2026-10-26T17:02:19Z`.

```
$ cd $S/mirror
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=247-ok
S054:Q2 OK occurrences=1 anchor=259-ok
S054:Q3 OK occurrences=1 anchor=277-ok
S054:Q4 OK occurrences=1 anchor=367-ok                      [exit 0]
$ python3 corpus/instruments/frontier-recheck-count.py --root $S/mirror --json $S/mirror.json
... F01–F19 all PASS, then:
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054 exit=0
entries=23 pass=23 exit=0                                   [exit 0]
```

F20 JSON record: `declared_ids=[S054] cited_ids=[S054] recheck_ids=[S054] manifest=corpus/
source-snapshots/round-37/manifest.json exit=0 problems=[] status=PASS`; run-level
`entries=23 pass=23 duplicate=None`. All four quotes occur exactly once in the capture.

## 4. Can a fabricated capture satisfy the harness? Measured limit — yes, if fabricated *with* its manifest record

Isolation probes, each a one-mutation copy of the §3 mirror (same harness invocation):

| probe | mutation | result | exit |
|---|---|---|---|
| B1 | one byte changed inside a pinned quote, manifest untouched | `FAIL F20 … problems=recheck-exit-1`; `S054:sha256 MISMATCH expected=ff3f… actual=e7bf…`; `entries=23 pass=22 exit=1` | 1 |
| B2 | capture replaced by fabricated text (false claims: "numeric priority score from 0 to 10", "arithmetic mean of CVSS base and EPSS") **and** manifest sha256 + quotes regenerated from it, real url kept | `PASS F20 … ids=S054 exit=0`; `entries=23 pass=23 exit=0` | **0** |
| B2b | B2 with `url` → `https://example.invalid/fabricated` | still `PASS … entries=23 pass=23 exit=0` — `url`/`fetched_utc` unread by this chain | 0 |
| B3 | quotes shorter than 12 normalized chars | `S054:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence` → `recheck-exit-2`, FAIL | 1 |
| B4 | README `sources` cell `S054`→`S999` **and** S054 registry row deleted from `SOURCES.md` | still `PASS F20 … ids=S054`, `entries=23 pass=23 exit=0` — neither file is read | 0 |

**The limit, precisely.** `source-recheck.py` never touches the network; it verifies capture ↔
manifest self-consistency (sha256, quotes present, stem = id, path inside manifest dir, B2 anchor
rule for non-unique quotes, 12-char minimum). `frontier-recheck-count.py` binds entry ↔ recheck line
↔ ids ↔ manifest shape, then runs the line. The composed chain enforces *internal* consistency only:
a capture fabricated together with its manifest record (matching digest, quotes ≥12 chars present in
the fabricated bytes) passes as `PASS F20 ids=S054` and flips the run to `entries=23 pass=23 exit=0`,
even when its content contradicts the real upstream page (B2). A fabricator who mutates capture bytes
without regenerating the manifest is caught (B1); degenerate quotes are caught (B3). The instrument's
own docstring concedes the same: "a passing entry proves its pinned captures still hold its own
assertions, not that the entry's claims are current upstream or that the quotes assert what the entry
says they assert." Fabrication resistance therefore lives **outside** this chain: capture-provenance
bookkeeping (`url`/`fetched_utc`, read by `capture-binding-check.py`, itself still self-consistency)
and out-of-band re-verification.

### 4.3 Discharge for S054 (live re-fetch, this seat, 2026-10-26)

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o live-overview.html \
      https://certcc.github.io/SSVC/tutorials/ssvc_overview/
HTTP=200 bytes=143053   raw sha256 = 9dba9f7500a6a1cece1a7acc77f1d768454b75fd04fa5bfdf382dfe598faec3f
$ html_to_text(raw)  # lane's own corpus/instruments/capture-source.py, imported read-only
normalized bytes = 32623  lines = 518
normalized sha256 = ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21
byte-equal to pinned S054.txt = True
```

The pinned capture is byte-identical to the live upstream page as of this run (raw digest also equals
ExecC2Capture's §1 record). The F20 capture is genuine; the B2 limit does not bite for S054 as
delivered. Anyone can repeat this check deterministically (fetch → `html_to_text` → sha256).

## 5. F20 row source ids match S054

All four binding points agree on S054: README row `sources` cell `S054` (drafted row and mirror);
entry `source: S054` header (sole declared id, `declared_ids=[S054]`); manifest record `id: S054`
with `path: S054.txt` (stem = id, B1 rule); harness prints `PASS F20 … ids=S054`. Frozen claims'
registry attributes (tier A, mined, opened 2026-10-26) are in the drafted row and my mirror row.
Caveat from B4: the row-cell↔S054 match is **not** harness-enforced (the printed `ids=` comes from
the entry, and `SOURCES.md` is unread by this counter) — it is verified here by direct inspection of
the drafted row and claims text, and will be enforceable at final head only by the C1 closure suite /
census, not by this instrument.

## 6. Residual risk and scope notes

- **F20 is not yet committed at lane head `b362068`**: `git diff --stat b56a4168 b362068` touches
  only `.ufo/waves/round-37/*` metadata, and the live-tree harness still prints 22/22. The claims'
  23/23 is verified here *by simulation* on base + the planned delta (§3); final-head verification
  belongs to integration (C1 closure suite, census, final gates). Nothing in this seat's evidence
  contradicts the claim; the delta is fully specified and simulated.
- Erratum-1 applied throughout: the corrected URL
  `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` is used in row, entry, manifest, and in
  the live re-fetch; the frozen claims JSON still carries the pre-erratum home-page literal
  (expected — errata are appended, never edited in).
- The harness measures recheck coverage, not upstream currency (§4 limit). C2's other legs
  (census, knowledge count, knowledge-expected sync, junk-twin rejection) are separate instruments
  outside this item.
- Independent agreement: my base 22/22, mirror 23/23, selftest 6/0, capture digest ff3f3b2c…,
  raw digest 9dba9f75…, and the four quotes/anchors match the sibling receipts (ExecC2Harness,
  ExecC2Capture, ExecC2QuoteOnce) — recomputed, not copied.

Tooling: nothing installed or upgraded (python3, curl, git already present); no `pacman` run.
