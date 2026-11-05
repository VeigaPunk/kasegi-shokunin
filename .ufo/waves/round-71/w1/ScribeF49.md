# ScribeF49 — F49 knowledge entry for S106 (ZDI disclosure process and vendor coordination)

Seat: ScribeF49 (scribe). Round 71, wave w1, claim C2 (coverage). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Only production file written by this seat: `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`.
No git/jj mutation of any kind was run by this seat (no add/commit/checkout/reset/push; no mutating `jj`).

## 1. Deliverable

- path: `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`
- line count: **256** (`wc -l`), 20076 bytes
- sha256 of the file as written: `6f304a052190d988b189ed82d547b0ba53562fc6837fa3dd52a8dbfb87986684`
  (`sha256sum` on the file after the last edit)
- section headings (`^## `): 11
- quote count: **15 pinned manifest quotes (Q01–Q15)** + **8 further sub-spans** of the same anchored
  lines = 23 verbatim source quotes, every one with an `(S106.txt:<anchor>)` citation.

### Anchors used (all 12 manifest anchors, no invented line numbers)

| anchor | manifest quote ids | lines quoted from it in the entry |
|---|---|---|
| `S106.txt:28` | Q01-scope | 1 (self-description) |
| `S106.txt:31` | Q02-acquisition | 1 (acquisition model) |
| `S106.txt:47` | Q03-guarantee | 2 (process guarantee; acquired-finding scope) |
| `S106.txt:49` | Q04-validation | 2 (validation; reward + private share) |
| `S106.txt:51` | Q09-full | 2 (full advisory; what it carries) |
| `S106.txt:52` | Q08-limited | 2 (limited advisory; sanitized sharing) |
| `S106.txt:60` | Q10-offer, Q15-nolimit | 4 (offer; no-limit; payment→coordination; bonus multipliers) |
| `S106.txt:61` | Q12-credit | 2 (credit/anonymity/pseudonym; vendor communication) |
| `S106.txt:62` | Q11-nobacklog | 2 (no-backlog guarantee; every case tracked) |
| `S106.txt:69` | Q13-dossier | 1 (vendor technical dossier) |
| `S106.txt:70` | Q05-window, Q06-shortened, Q07-escalation | 6 (120-day window; 30/60/90; the shortening's condition; escalation; "depending on multiple factors") |
| `S106.txt:72` | Q14-refusal | 1 (refusal/unresponsive branch) |

Manifest anchor set = {28, 31, 47, 49, 51, 52, 60, 61, 62, 69, 70, 72} — the entry cites **only** these.

## 2. Q1 — header trio

Measured on the written file (`grep -n` on the first lines):

```
3:source: S106 — https://www.zerodayinitiative.com/about/ — TrendAI™ Zero Day Initiative™ (ZDI), "About Us" page; capture corpus/source-snapshots/round-71/S106.txt (sha256 291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db, 148 lines, 15004 snapshot bytes, fetched 2026-11-05T01:27:03Z): …
4:verified-at: 2026-11-05
5:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-71/manifest.json --source S106   # 15 pinned quotes (Q01-Q15), each located at its anchor; …
```

- `source:` names S106, the canonical URL, the capture path + sha256 + line/byte counts + fetch instant,
  and every anchor the entry uses.
- `verified-at: 2026-11-05` (the capture's fetch date, `2026-11-05T01:27:03Z`; host-local was
  2026-11-04T22:xx-03:00, so the date is stamped UTC — the round-70 critic's O21 finding).
- `recheck:` is ONE executable command with the required `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`
  prefix and a `#` note after it (Q10).

Measured run of that exact command from the lane root:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-71/manifest.json --source S106
S106:sha256 OK
S106:Q01-scope OK occurrences=2 anchor=28-ok
S106:Q02-acquisition OK occurrences=1 anchor=31-ok
S106:Q03-guarantee OK occurrences=1 anchor=47-ok
S106:Q04-validation OK occurrences=1 anchor=49-ok
S106:Q05-window OK occurrences=1 anchor=70-ok
S106:Q06-shortened OK occurrences=1 anchor=70-ok
S106:Q07-escalation OK occurrences=1 anchor=70-ok
S106:Q08-limited OK occurrences=1 anchor=52-ok
S106:Q09-full OK occurrences=1 anchor=51-ok
S106:Q10-offer OK occurrences=1 anchor=60-ok
S106:Q11-nobacklog OK occurrences=1 anchor=62-ok
S106:Q12-credit OK occurrences=1 anchor=61-ok
S106:Q13-dossier OK occurrences=1 anchor=69-ok
S106:Q14-refusal OK occurrences=1 anchor=72-ok
S106:Q15-nolimit OK occurrences=1 anchor=60-ok
EXIT=0
```

Fail-closed controls for the same instrument (Q7 "at least one missing/corrupted-source control must fail"):

```
$ python3 corpus/instruments/source-recheck.py --selftest
SELFTEST clean PASS expected-exit=0 observed-exit=0 …
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 …
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 …
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 …
SELFTEST stem-mismatch PASS expected-exit=1 observed-exit=1 …
SELFTEST quote-absent PASS expected-exit=1 observed-exit=1 …
selftest cases=10 failures=0
EXIT=0
```

## 3. Q3 — every load-bearing claim carries a ≤25-word verbatim quote at its anchor

Measured by a script that (a) takes each double-quoted span in the entry, (b) normalizes whitespace,
(c) checks the span is present in `corpus/source-snapshots/round-71/S106.txt` **at the line the entry
cites**, (d) counts its words, and (e) checks the cited line is in the manifest anchor set.

```
spans checked (source-quoted spans, excluding the Rejected-over-generalizations section): 32
source-spans verified at anchor: 32
bad: 0
```

26 distinct anchored spans, all at their anchor, all ≤25 words (largest = 25 words:
`Every case is tracked, managed under a defined timeline, and disclosed according to our disclosure
policy even if a vendor declines to issue a patch.` at `S106.txt:62`, and the pinned
`Q07-escalation` at `S106.txt:70`). No span exceeds the ≤25-word bound.

Full-file sweep of every quoted span (50 quoted strings in the file):

```
total quoted spans: 50
spans NOT in the capture: 12
    ZDI disclosure timeline                <- entry's own phrase in a scare-quoted question
    what does this page establish?          <- entry's own phrase in a scare-quoted question
    (`S106.txt:47`), and that               <- regex artifacts of the sweep (quote boundaries)
    (`S106.txt:51`); that
    (`S106.txt:61`). ZDI also states a guarantee about its own case handling:
    (`S106.txt:62`), and that
    120 days is the disclosure deadline for vulnerabilities.      <- rejected proposition (entry-authored)
    ZDI publishes 30, 60 or 90 days after a submission, by severity.
    A vendor that goes silent for 15 business days is automatically published.
    ZDI's no-backlog guarantee is a property of coordinated disclosure generally.
    ZDI's reward structure is a platform severity ladder.
    ZDI's window is the same as Project Zero's 90-day policy or CERT/CC's policy.
```

The six quoted propositions are the entry's own rejected over-generalizations; each is verified
**not** to be a sentence of the capture (`in_capture = False` for all six, checked individually), and
the section says so in its own lead sentence: "Each proposition below is this entry's own phrasing of
a claim a reader might make; none of them is a sentence from the capture…".

### Word counts in the entry's Gate tables

The Gate table's per-pin word counts were computed from `corpus/source-snapshots/round-71/manifest.json`
and cross-checked against the entry's table rows:

```
pinned rows in Gate table: 15
mismatches vs manifest: []
```

The eight further-span counts were measured with `wc -w` on the quoted text (not hand-typed):
15, 17, 22, 19, 16, 21, 25, 10 — matching the entry's table exactly. The 15 pinned counts were also
re-measured with `wc -w` (7, 13, 19, 5, 15, 15, 25, 19, 12, 19, 19, 16, 19, 18, 13) and agree with the
manifest.

## 4. Q4 / R108 — attribution, and no sentence claiming more than its anchor

Every statement is attributed to ZDI as the stating party ("ZDI states", "ZDI prints", "TrendAI ZDI's
own"). The four R108-mandated readings are carried explicitly in the entry:

- **120-day window** — "a standard coordination window of 120 days **under TrendAI™ ZDI's disclosure
  policy**" (`S106.txt:70`); the entry states it is ZDI's policy statement about its own programme.
- **30/60/90 shortening** — the entry's condition column carries ZDI's own words "For flaws that
  result from incomplete or problematic security patches" (`S106.txt:70`) and the Limits section says
  the page "names no factor, threshold or severity band that selects between 30, 60 and 90 days".
- **15-business-day escalation** — quoted as the permission "may escalate to a limited public
  advisory to protect users" (`S106.txt:70`); the entry states it is "written as a permission … not as
  an automatic publication".
- **"no backlog"** — presented as "ZDI's own guarantee about ZDI's own tracked cases, not a property
  of coordinated disclosure in general and not an observation of any individual case" (`S106.txt:62`).

Two defects were found by my own sweep and **fixed before filing**:

1. **Misquote** — the first draft rendered the limited-advisory row as ZDI "may publish / to protect
   the broader public…", dropping "a limited advisory" from the source sentence. Corrected to the
   verbatim "TrendAI™ ZDI may publish a limited advisory to protect the broader public while
   withholding information that could enable exploitation." (`S106.txt:52`).
2. **Unsupported attribution** — the first draft said ZDI prints "the acquisition model it
   introduced". The capture's "introduced" wording is at `S106.txt:30`, which is **not** a manifest
   anchor, so the claim could not be anchored. Rewritten to "ZDI also prints an acquisition model:"
   with the quote at `S106.txt:31`.

### Scope-limit paragraph (as required)

The `## Scope limits` section states that this is one acquisition programme's own process statement
and that it is **not** F13's platform severity ladder and reward scale, **not** S005's Project Zero
90-day policy, **not** S004's CERT/CC own disclosure policy, **not** F11/F38's ISO 29147/30111
division of labour, and **not** any single published advisory instance. The three cross-referenced
knowledge paths it names exist on disk (`corpus/knowledge/program-severity-ladders-and-reward-scales.md`,
`corpus/knowledge/zdi-disclosure-policy.md`).

## 5. Q5 — falsifiable rule and a rejected over-generalization

**Falsifiable rule** (`## Falsifiable rule`): three checks a reader can run against the capture —
(1) the package must name TrendAI™ ZDI as the party whose policy states the window; (2) a package
stating 30/60/90 days must carry ZDI's condition "For flaws that result from incomplete or
problematic security patches"; (3) a package stating the 15-business-day branch must say ZDI "may
escalate to a limited public advisory to protect users", not "publishes". Each failure is tied to a
located quote, so the falsification is the quote, not the entry's judgement.

**Rejected over-generalizations** (`## Rejected over-generalizations`), six of them, each with its
reason and a falsifying located quote. The rejected over-generalization recorded as the headline one:

> **"120 days is the disclosure deadline for vulnerabilities."** Rejected: the figure is ZDI's own
> statement of a standard *coordination* window under ZDI's disclosure policy (`S106.txt:70`), the
> same line states a shorter window for a named class of flaws, and the capture states no
> clock-start event for the 120 days.

The other five rejected: (2) "ZDI publishes 30, 60 or 90 days after a submission, by severity";
(3) "A vendor that goes silent for 15 business days is automatically published";
(4) "ZDI's no-backlog guarantee is a property of coordinated disclosure generally";
(5) "ZDI's reward structure is a platform severity ladder"; (6) "ZDI's window is the same as
Project Zero's 90-day policy or CERT/CC's policy".

## 6. Q6 — documentation only

No probing, scanning, logging-in or submission instruction; no credential material; no private URL
or vault reference. The dossier sentence is stated as what ZDI says it hands a vendor, with the
explicit note that it "is not an instruction to probe, scan or test any target, and no target, host
or credential appears here".

## 7. Lane-harness measurements (read-only, on a scratch export)

All harness runs below were executed against a scratch export
`/fast/scratch/hyaku/kasegi-r71/ScribeF49/mirror` built with
`git -C <lane> archive HEAD | tar -x -C <scratch>` (no clone, no checkout, no commit anywhere), plus
the new entry copied in. The S106 registry row / F49 README row / knowledge-expected line were
**scratch-only fixture rows** (ScribeRegistry owns the real ones) so the F49 path could be exercised.

```
$ python3 corpus/instruments/frontier-recheck-count.py        # in the scratch mirror
FRONTIER-PASS F49 ids=S106
PASS     F49  knowledge/zdi-disclosure-process-and-vendor-coordination.md ids=S106  exit=0
entries=52 pass=52 exit=0
EXIT=0
```

```
$ python3 corpus/instruments/recheck-audit.py --quiet          # in the scratch mirror
strict pass=1/87 cdroot_fail=77 instrument_fail=0 own_fail=0
executes=65 gated=22 broken=0
lines=87 total=87 pass=78 fail-closed=22 parse_fail=0 cwd_fail=9 paths_fail=0 exit=1
expect=present expected=87 missing=0 unexpected=0 exit=1
```

The mirror's `cdroot_fail=77` is an artifact of the export (every entry's `recheck:` line `cd`s to the
real lane root, not the mirror); the same audit run **in the lane root** gives my entry
`frozen=111 strict=111111 lane=0 foreign=0 executes PASS`, identical to the F48 shape model and to
`zdi-disclosure-policy.md`:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py | grep -E "zdi-disclosure-process|github-advisory-database-curation|zdi-disclosure-policy"
github-advisory-database-curation-semantics.md             frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
zdi-disclosure-policy.md                                   frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
zdi-disclosure-process-and-vendor-coordination.md          frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
unexpected=corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md
```

The `unexpected=` line is expected until ScribeRegistry lands the `knowledge-expected.txt` line (its
file); the audit's set-equality limb is doing its job. Pre-existing baseline for comparison, same
audit on a clean export of HEAD: `lines=86 total=86 pass=77 fail-closed=22 parse_fail=0 cwd_fail=9
paths_fail=0 exit=1` — my entry adds one line and one PASS, and changes no failing count.

```
$ python3 corpus/instruments/capture-binding-check.py         # in the scratch mirror
MANIFEST round-71 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=85 with_url=85 with_fetched_utc=47 with_archival=38 snapshot_dirs=44 manifest_dirs=44 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=85 bound=85 unbound=0
EXIT=0
```

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url …            (six inherited W04 warnings)
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

## 7b. Citation-class measurement (one run that completed, one that did not)

`corpus/instruments/resolve.py` was run in the scratch mirror **with** this entry present. It
completed and reported:

```
resolve exit 0
distinct=5966 resolves=66 mirror=0 internal=1340 other=0 gone=4560 skill=153/736 corpus=1371/5563 all=1406/5966
```

The 12 distinct capture-stem cites this entry introduces are classified the same way as every other
capture-stem cite in the corpus — `GONE` in the `rel` domain, sub-kind unresolved:

```
S106.txt:28	GONE		1		rel	3	+CORPUS
S106.txt:31	GONE		1		rel	3	+CORPUS
S106.txt:47	GONE		1		rel	6	+CORPUS
… (12 distinct S106.txt tokens, all GONE / rel)
```

Committed-lane comparison of the same class: `grep -E "^S07[0-9]\.txt" corpus/instruments/citation-survival.tsv`
→ **101 rows, all `GONE`**; `S075.txt` alone contributes 8 rows, all `GONE` (S075.txt:26, :20-27, :22, :23,
:23-25, :24, :25, :27). The in-mirror `S105.txt` rows (37) and `S103.txt` rows (40) are likewise all
`GONE`. So the bare capture-stem form is a lane-wide convention for captured snapshots, and this
entry adds 12 more cites of that established class — it does not introduce a new class.

**A second run did not complete and no figure is claimed from it.** I launched the same census on a
clean export of HEAD (no entry, for a base-vs-mirror delta) as a background job; it was still running
when I removed the scratch tree, and it died with:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '/fast/scratch/hyaku/kasegi-r71/ScribeF49/base/corpus/instruments/citation-survival.tsv'
```

That run produced no output, so **no base-vs-mirror citation-rate delta is claimed anywhere** in this
report. The lane's committed census files were not written by this seat
(`git status --porcelain corpus/instruments/citation-survival.tsv corpus/instruments/citation-survival.md`
→ empty; the lane file's mtime is unchanged at 2026-11-03 18:22).

## 8. Known limits of this entry (stated in the entry's own `## Limits` section)

- First-party statements only; no evidence that any advisory was published or any window honoured.
- The capture states **no** start event for the 120-day window. Measured: `grep -c "120 days"` on the
  capture → `1` (line 70); `grep -niE "window (starts|begins)|from the (date|day) (of )?(submission|acquisition|report)|clock"` → `0` hits.
- The factors behind 30/60/90 are not enumerated ("depending on multiple factors", `S106.txt:70`).
- No severity tiers, no payout amounts (the page names "bonus multipliers, higher payout tiers" at
  `S106.txt:60` but no amount or tier value).
- General programme claims on the page (founding year, researcher counts, disclosure counts,
  protection-filter deployment) are **not** asserted: none is pinned by the manifest's fifteen quotes.
- The `recheck:` line verifies pinned bytes and located quotes, not live-page freshness.
- `anchorcheck.py` on this file reports `BASE-ABSENT` for every `S106.txt:<n>` cite, because the bare
  capture stem is not a lane-root file — identical to the F48 shape model (`S105.txt`) and to the
  existing `zdi-disclosure-policy.md` (`S075.txt`). It is the lane's established citation form for
  captured snapshots, not a defect introduced here.

## 9. Dependencies on other seats (measured, not asserted)

- ScribeRegistry's four files must reference this exact path; the census E11 limb checks the
  `used-by` path exists on disk, and it now does (`test -e
  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` → ok).
- `frontier-recheck-count.py` needs the F49 README row's sources cell to be `S106` and the S106
  registry row to exist; on the scratch fixture with exactly those cells, F49 scored
  `FRONTIER-PASS F49 ids=S106 … exit=0` and the whole run printed `entries=52 pass=52 exit=0`.
- `recheck-audit.py` needs the `knowledge-expected.txt` line; until it lands, the audit prints
  `unexpected=corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` and exits 1.
- I did NOT touch `corpus/SOURCES.md`, `corpus/README.md`, `corpus/instruments/knowledge-expected.txt`
  or `PROVINCE.md` — those are ScribeRegistry's.

## 10. Tooling

No tool was installed or upgraded by this seat; no pacman/uv/npm transaction was run, so no
tool/version/channel record is owed. Everything used was already present: `git`, `python3` (3.14.8),
`grep`, `wc`, `sha256sum`, `tar`, and the lane's own instruments.

## 11. Scratch hygiene

Scratch tree `/fast/scratch/hyaku/kasegi-r71/ScribeF49/` held `mirror/`, `base/`, `quotes.txt`,
`extra.txt`. The two exported trees were read-only measurements; nothing outside the lane's
`corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` and this report was written in
the lane. The scratch tree is removed before this seat yields.
