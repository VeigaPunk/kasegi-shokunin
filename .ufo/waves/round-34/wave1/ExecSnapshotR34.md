# ExecSnapshotR34 — round-34 S051 capture and manifest

Seat: ExecSnapshotR34 (leaf, L2 wave 1). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.
Assignment: create the C2 capture for F17 — capture the Immunefi Vulnerability Severity Classification
System v2.2 page, verify the SSR text body carries the Smart Contracts level table, and build the round-34
`manifest.json` with the F17 entry's quotes, line anchors and a passing `source-recheck`.

## Report

### Files landed (write scope: this lane only)

| path | bytes | lines | sha256 |
|---|---|---|---|
| `corpus/source-snapshots/round-34/S051.txt` | 8502 | 175 | `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` |
| `corpus/source-snapshots/round-34/manifest.json` | 7654 | 122 | `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe` |

No other lane file was modified. `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/` and
`SCORECARD.md` are untouched by this seat (the S051 row, the F17 row and the entry belong to
ScribeSOURCESRow / ScribeEntryF17 / ExecRegistryAppend).

### 1. Capture

Assigned command form is not supported by the instrument — it takes flag arguments only:

```
$ python3 corpus/instruments/capture-source.py "https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/" --out /fast/scratch/hyaku/kasegi-r34/ExecSnapshotR34/probe.txt
usage: capture-source.py [-h] [--id ID] [--url URL] [--out OUT]
                         [--kind {html,pdf,text}] [--selftest]
capture-source.py: error: unrecognized arguments: https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/
exit=2
```

So the run used the instrument's `--id/--url/--out` form (`capture-source.py:main()` requires all three):

```
$ python3 corpus/instruments/capture-source.py --id S051 \
    --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ \
    --out corpus/source-snapshots/round-34/S051.txt
S051 status=200 fetched_bytes=219383 snapshot_bytes=8502 sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5 utc=2026-10-26T05:31:10Z out=corpus/source-snapshots/round-34/S051.txt
exit=0
```

- Instrument UA (`capture-source.py:UA`): `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`.
- HTTP `status=200`; fetched body 219383 bytes; post-conversion snapshot 8502 bytes / 175 lines.
- `fetched_utc` recorded in the manifest as `2026-10-26T05:31:10Z` — strict UTC (`…Z`), no local offset
  (round-33 R8 / round-34 C1 rule for round-32+ records; `capture-binding-check.py` prints `fetched=1`
  for this record).
- Independent reproducibility: ScribeSOURCESRow refetched the same URL with its own instrument run and
  reported the identical snapshot sha256 `4fd8ed98…b325a5` (peer-measured, `.ufo/waves/round-34/wave1/ScribeSOURCESRow.md`).

### 2. Body verification — the page is SSR and the tables are present

`capture-source.py` strips `<script>`/`<style>` before extracting text (`SCRIPT_RE`), so text surviving in
the snapshot is in the served HTML, not injected at runtime: the severity body is server-rendered, as the
assignment says. Measured on the landed capture:

```
$ python3 - <<'PY'   (re.match(r'^[1-5]\. (Critical|High|Medium|Low|None)') over the snapshot)
level markers 15
 59 5. Critical- Network not being able to confirm new transactions (Total network shutdown)
 64 4. High- Unintended chain split (Network partition)
 66 3. Medium- High compute consumption by validator/mining nodes
 69 2. Low- DoS of greater than 10% but less than 30% of validator or miner nodes and does not shut down the network
 71 1. None- Best practices
 74 5. Critical- Any governance voting result manipulation
 84 4. High- Theft of unclaimed yield
 90 3. Medium- Smart contract unable to operate due to lack of token funds
 95 2. Low- Contract fails to deliver promised returns, but doesn't lose value
 96 1. None- Best practices
 99 5. Critical- Execute arbitrary system commands
122 4. High- Injecting/modifying the static content on the target application without Javascript (Persistent) such as:
133 3. Medium- Changing non-sensitive details of other users (including modifying browser local storage) without already-connected wallet interaction and with up to one click of user interaction, such as:
140 2. Low- Changing details of other users (including modifying browser local storage) without already-connected wallet interaction and with significant user interaction such as:
147 1. None- SPF/DMARC misconfigured records
headers [(57, 'Blockchain/DLT'), (72, 'Smart Contracts'), (97, 'Websites and Apps')]
bullets in the Smart Contracts Critical cell (L74-L83): 9
```

Three scope tables, five level markers each (15), the `Smart Contracts` header at L72 with its Critical cell
L74-L83 (level marker L74, nine bullets L75-L83), and 175 lines total. Five-level scale statement at L46;
version string at L45 (`Immunefi Vulnerability Severity Classification System - v2.2`), also in the HTML
title (L1): `text.count('v2.2') = 2`, `text.count('v2.3') = 0`.

### 3. Manifest — `corpus/source-snapshots/round-34/manifest.json`

One record, `S051`: `path=S051.txt`, `sha256=4fd8ed98…b325a5`,
`url=https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/`,
`fetched_utc=2026-10-26T05:31:10Z`, 18 quote assertions Q1-Q18. Quotes are the ones the F17 entry uses
(agreed with ScribeEntryF17; final list below). Each carries a `location` naming the line and what it binds;
17 carry an `anchor` line number, Q2 does not (reason below).

| id | anchor | source lines | quote (verbatim from the capture) |
|---|---|---|---|
| Q1 | 46 | L46 | `At Immunefi, we classify bugs on a simplified 5-level scale:` |
| Q2 | — | L47-L51 | `Critical High Medium Low None` |
| Q3 | 52 | L52 | `The development of this scale took into consideration multiple factors that may affect a vulnerability and its likelihood of exploitation` |
| Q4 | 52 | L52 | `finalizes them largely by the impact that they cause` |
| Q5 | 53 | L53-L54 (wrapped) | `The table below is mostly concerned with the consequence of a successful exploit.` |
| Q6 | 55 | L55-L56 (wrapped) | `the level of the bug may be downgraded to reflect that or rejected.` |
| Q7 | 74 | L74 | `5. Critical- Any governance voting result manipulation` |
| Q8 | 75 | L75 | `Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield` |
| Q9 | 77 | L77 | `Permanent freezing of funds` |
| Q10 | 79 | L79 | `Miner-extractable value (MEV)` |
| Q11 | 83 | L83 | `Protocol insolvency` |
| Q12 | 88 | L88 | `Temporary freezing of funds` |
| Q13 | 92 | L92 | `Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)` |
| Q14 | 94 | L94 | `Unbounded gas consumption` |
| Q15 | 90 | L90 | `Smart contract unable to operate due to lack of token funds` |
| Q16 | 95 | L95 | `Contract fails to deliver promised returns, but doesn't lose value` |
| Q17 | 96 | L96 | `1. None- Best practices` |
| Q18 | 99 | L99 | `Execute arbitrary system commands` |

Every quote is <=20 words. Q5/Q6 are wrapped by the converter across two source lines and are asserted
under the declared `normalized=markup-whitespace` path; Q2 joins five one-name-per-line entries L47-L51 and
is asserted the same way. All other 15 are present raw in the snapshot.

### 4. Self-check — `source-recheck.py`

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok
S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok
S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
exit=0
```

18/18 assertions `OK`, `sha256 OK`, `exit=0`. 16 print `occurrences=1`; Q9 and Q17 print `occurrences=2`
because they are the printed bullets and the same words occur in the Blockchain/DLT table (L62, L71) —
both carry verified anchors under the instrument's QUALITY Q9 / B2 rule. This deviation from the
assignment's literal "every assertion occurrences=1" is deliberate and is the one open decision recorded
below.

### 5. Binding state (cross-seat dependency, not a defect in this capture)

```
$ python3 corpus/instruments/capture-binding-check.py
...
MANIFEST round-34 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S051 dir=round-34
records=41 bound=40 unbound=1
exit=1
```

Rule B needs a registry row for the record id, and `corpus/SOURCES.md` currently holds 0 `| S051 |` rows and
50 `| S### |` rows. The required input is exact-token equality on the URL; I gave ScribeSOURCESRow the string
`https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/` (trailing slash intact, no
path/query), and it replied that its applied tokenizer yields exactly that single token from the drafted row
(row draft sha256 `94deb84a4507ced156d2e3e78c1dc1e1f8f5b4907b4ffba6e8f6cb3b3d8d5b1d`, to be appended by
ExecRegistryAppend). After that append, `bound` should move 40 -> 41 and `unbound` 1 -> 0. The
`orphans=1 orphan=S040-live.txt` line is pre-existing and belongs to the R6 seat, not here.

### 6. Decisions and deviations (for the L1)

1. **Instrument invocation.** The assigned `<url> --out` form is rejected by the instrument (exit 2, above);
   the manifest record was produced with `--id S051 --url … --out …`.
2. **Q9/Q17 quote shape (open decision).** The entry author (ScribeEntryF17) first asked for the printed
   bullets `Permanent freezing of funds` (L77) and `1. None- Best practices` (L96); those are `occurrences=2`
   in this capture. I briefly replaced them with unique merged spans (`… royalties - Permanent freezing of
   funds`; `1. None- Best practices Websites and Apps`) to make all 18 occurrences 1, and the entry author
   objected that those quote converter-joined text and cross a section boundary (QUALITY Q8/Q3), which is
   correct. The landed manifest therefore binds the printed bullets with anchors 77 and 96: entry quotes and
   manifest quotes are byte-identical, and the two non-unique assertions pass under B2. Precedent for this
   exact shape is committed in the lane: `corpus/source-snapshots/round-30/manifest.json` prints
   `S047:Q1 OK occurrences=3 anchor=123-ok` and `S047:Q3 OK occurrences=2 anchor=130-ok`, exit 0. Consequence
   to record: the frozen C2 predicate sentence "source-recheck S051 prints every assertion occurrences=1" is
   not literally true for 2 of 18 assertions; the C2 kill rule ("source-recheck S051 exit != 0") is satisfied.
   The alternative bytes (all-18-unique, manifest sha256 `3e726d84842158d45e12324c3f551246c12c92c9abcf670a5c1380862c1656d9`)
   are reproducible by restoring the two merged-span quotes; I did not ship them because they make the
   manifest assert extractor text the entry does not quote.
3. **Q2 has no anchor.** The five level names occupy L47-L51; `source-recheck.py`'s anchor window is
   `raw_lines[anchor-1:anchor+3]` (four lines), so no anchor can verify a five-line span. Q2 is unique under
   normalization (`occurrences=1`), so B2 does not require an anchor; the `location` field names L47-L51.
4. **Candidate quote fidelity.** The assignment's candidate `severity5. Critical — Direct theft of any user
   funds, …` does not occur in the capture (the em-dash/space form is a rendering artifact). The captured
   text puts the level marker on its own line with the first bullet merged: `5. Critical- Any governance
   voting result manipulation` (L74), with `Direct theft of any user funds, …` as its own bullet on L75.
   Q7/Q8 quote the captured forms; the entry follows them (ScribeEntryF17 confirmed).
5. **No version-selection claim.** The capture contains v2.2 at L1/L45 and no `v2.3` string; it carries no
   statement about which version a program uses. ScribeEntryF17 reported the same gap and will record it as
   a limit rather than a claim. ScribeSOURCESRow separately captured v2.3 (peer-measured, 4 levels, both
   versions marked "Currently in Use"), which is why the row scopes to v2.2 and makes no recency claim.

### 7. Limits

- One instant, one host response: this is evidence of what the page served at 2026-10-26T05:31:10Z, not a
  claim that it serves the same bytes today, and not a statement about any other Immunefi page.
- `source-recheck.py` verifies local bytes against pins and quotes; it does not authenticate the upstream
  document, its version status, or that a quote supports the entry's reading.
- The snapshot is post-conversion text (script/style stripped, tags removed, whitespace collapsed): table
  structure survives only as the header/level/bullet sequence, which is what the anchors name. HTML-level
  evidence (e.g. `<table>` boundaries) is not in the capture and is not asserted.
- `capture-binding-check.py` at this timestamp accepts any non-empty `fetched_utc`; the value here is strict
  UTC by form, and the strict-UTC rejection case belongs to the hardened instrument (ExecCaptureBindingHarden).

### 8. Scratch

Scratch root `/fast/scratch/hyaku/kasegi-r34/ExecSnapshotR34` was created for the instrument probe; the probe
exited before writing (`probe.txt` never created). Directory removed before yield, and its absence measured
(sibling seats' directories under the shared parent were left alone):

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/ExecSnapshotR34
rm_exit=0
$ test -d /fast/scratch/hyaku/kasegi-r34/ExecSnapshotR34
test_d=1            # 1 = absent
$ ls -1 /fast/scratch/hyaku/kasegi-r34/ | grep -c ExecSnapshotR34
0
```

### 9. Tooling

Nothing installed or upgraded. `python3` (stdlib only) and the lane's own committed instruments were used;
no `pacman`, `uv`, `npx` or network tooling beyond the instrument's own fetch.

### 10. Reproduction

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/capture-source.py --id S051 \
  --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ \
  --out corpus/source-snapshots/round-34/S051.txt          # expect sha256 4fd8ed98…b325a5
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-34/manifest.json --source S051   # expect 18 OK lines, exit 0
python3 corpus/instruments/capture-binding-check.py        # expect S051 bound once the row is appended
```
