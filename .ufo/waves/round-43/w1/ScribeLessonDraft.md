# ScribeLessonDraft — round 43 receipt

Lane `kasegi-shokunin`, round 43, base `ab98fac9dce87130bc4f66de89e30650d63943dc`, claims freeze
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. Leaf seat: no subagent dispatch, no second judge, no git
mutation. Deliverable: `ScribeLessonDraft.round-43-lesson.md` (lands at `corpus/lessons/round-43.md`).

## Deliverable

| path | bytes | lines | sha256 |
|---|---:|---:|---|
| `.ufo/waves/round-43/w1/ScribeLessonDraft.round-43-lesson.md` | 22222 | 164 | `85d222ebf92d58107925f3c2780993448cd5ea0b11328d4ba94265ed75a85d26` |

Sections, in order: H1 header with the revisions/J-and-Y rule, `## Frozen claims`, `## Mistakes`,
`## Census`, `## Gate` (admitted S067 = curl CVE-2025-9086; rejected S068 = GHSA-v676-f8gm-92r9),
`## considerthese 2026-10-26 dispositions`, `## Assimilation`.

## Commands run and their real output

All commands ran in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless a scratch path is named.

1. Freeze identity:

```
$ git log -1 --format='%H %s' -- .ufo/waves/round-43/claims.json
4cb6d4ae768481e1a14afbedc2d865a060ebacfd round-43: frozen claims C1 (r43-closure.sh K1-K19 narrative-evidence) + C2 (claim-package gate capability), controls, freeze record, v2 wave spec and dispatch (73 seats)
$ sha256sum .ufo/waves/round-43/claims.json
a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630  .ufo/waves/round-43/claims.json
$ cat .ufo/waves/round-43/freeze.txt
frozen-at=2026-10-28T16:37:07Z / measured-at-max=2026-10-28T16:34:15Z / claims-sha256=a4c03e1e…a6630 / base=ab98fac9…
```

2. Wave size and attack share (counted, never estimated):

```
$ python3 -c "... json.load('.ufo/waves/round-43/w1-dispatch.json')['counts'] ..."
spawn 73, resume 0, total 73
$ python3 -c "... collections.Counter(role) over w1-spec.json items ..."
items 73; executor 23, reviewer 11, scribe 10, scout 9, critic 7, mutation-tester 5, connector 2,
sentinel 2, revenger 2, simplifier 2
```

Reviewer 11 + critic 7 + mutation-tester 5 = 23 → `23/73 = 31.5%`, the figure the milestone names.

3. Base counters re-measured at the freeze tree (they match `c2-controls/before.txt`):

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
66
$ ls corpus/knowledge/*.md | wc -l
61
$ ls corpus/instruments | wc -l
33
$ ls corpus/instruments/ | grep -ci claim
0
```

4. Census at the freeze tree (before the C2 rows append — used in the lesson only as evidence that the
   before value repeats, never as the after value):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census-exit=0
```

5. Defect evidence re-read in committed bytes (each cited in the Mistakes table):

```
$ sed -n '1634p' SCORECARD.md
Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33,groups=4,…
$ sed -n '1804p' LOG.md
  (`.ufo/waves/round-42/wave1-dispatch.json`); wave 2 `kasegi-r42-falsify` 36 seats dispatched against the repaired head; dead seats counted from `wave2-results.json` in the round report.
$ sed -n '9,17p' corpus/lessons/round-42.md
… "wave 2 dispatched 36 seats; the round total is 100" …
$ sed -n '52p' corpus/lessons/round-42.md
## Wave-2 falsification
$ sed -n '60,70p' corpus/lessons/round-42-verifier-spotcheck.md
… "the pre-repair instrument at `de09313` prints `closed=10/13 exit=1`" …
$ grep -rn 'closed=10/13' .ufo/waves/round-42/final-gates/
(no output)
$ sed -n '19p' .ufo/waves/round-42/final-gates/all-gates.pre-repair.txt
closed=9/13 exit=1
$ sed -n '19p' .ufo/waves/round-42/final-gates/all-gates.txt
closed=13/13 exit=0
$ sed -n '16p' .ufo/waves/round-42/c1-controls/do-nothing.txt
closed=8/12 exit=1
$ ls .ufo/waves/round-42/wave2-results.json
ls: cannot access '.ufo/waves/round-42/wave2-results.json': No such file or directory
```

The `corrections=34` side is the base control's own line:
`J11 payload=corrections=34,groups=4,dups=4,excused=4,unexcused=0,…` in
`.ufo/waves/round-43/c1-controls/do-nothing.txt` §B. The freeze-label mtime is
`.ufo/waves/round-42/claims-erratum-3.md:3` (`2026-10-28 07:51:52.149991752 -0300`, i.e. 10:51:52Z).

6. Wave-table shape check (no cell may carry a raw pipe):

```
$ awk -F'|' '/^\|/ {print NR": NF="NF}' .ufo/waves/round-43/w1/ScribeLessonDraft.round-43-lesson.md
24-27: NF=6 (4-column Frozen claims table) ; 35-43: NF=9 (7-column Mistakes table)
```

Uniform field counts: no stray pipes inside cells.

7. S067 capture, re-read after the capture seat overwrote its first draft:

```
$ wc -l -c .ufo/waves/round-43/w1/ExecSourceCapture.S067.txt
109 3822
$ sha256sum .ufo/waves/round-43/w1/ExecSourceCapture.S067.txt
7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b
$ python3 - <<'EOF'  # exact-match check of each quoted line against the capture
69 "Project curl Security Advisory, September 10 2025 Permalink"            exact 8 words
82 "CWE-125: Out-of-bounds Read"                                             exact 3 words
83 "Severity: Low"                                                           exact 2 words
84 "Bug bounty: 505 USD"                                                     exact 4 words
88 "Affected versions: curl 8.13.0 to and including 8.15.0"                  exact 8 words
89 "Not affected versions: curl < 8.13.0 and >= 8.16.0"                      exact 9 words
97 "Fixed-in: https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6" exact 2 words
103 "This issue was reported to the curl project on August 11, 2025. We contacted distros@openwall on September 5, 2025." exact 19 words
```

Manifest record read back: `url https://curl.se/docs/CVE-2025-9086.html`, `fetched_utc 2026-10-28T16:46:34Z`,
`bytes 10455` raw, `raw_sha256 58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd`,
`snapshot_bytes 3822`, `lines 109`, `sha256 7e35413a…f975c8b`; the capture receipt's
`source-recheck.py --source S067` prints `S067:sha256 OK` and `Q1..Q6 OK occurrences=1 anchor=<n>-ok`, and its
fetch line prints `code=200 bytes=10455 redirects=0`.

8. S068 screen — the row's normalized pin verified by this seat's own fetch and normalization:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ ; curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o ghsa.html \
    -w 'code=%{http_code} bytes=%{size_download} redirects=%{num_redirects}\n' \
    https://github.com/advisories/GHSA-v676-f8gm-92r9 ; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-28T16:48:33Z
code=200 bytes=141794 redirects=0
2026-10-28T16:48:33Z
```

Normalized with the committed instrument's own `html_to_text` (the `capture-source.py --kind html` code
path): 191 lines, 5936 bytes, sha256
`530cbcf9925b082f9effea7bbc5e96650949794d80893d7ac8ec5e289b4c97e6` — byte-identical to the registry row's
screen-record pin. Lines read verbatim at the anchors the row and the lesson cite: L64 `Unreviewed`,
L66 the per-CVE title, L67 `High severity`, L68 `Unreviewed`, L75 `No package listed—` (the lesson quotes
the first three words and says the line continues with an em dash), L78 `Unknown`, L80 `Unknown`,
L105 `Published by the National Vulnerability Database`, L161 `CWE-125`, L170 `No known source code`.

## Inputs read (committed, never edited)

`claims.json` (frozen), `freeze.txt`, `census-before.txt`, `c1-controls/do-nothing.txt`,
`c2-controls/before.txt`, `corpus/lessons/round-42.md`, `corpus/lessons/round-42-verifier-spotcheck.md`
(§9.6, `:34`, `:38`, `:64`, `:173-179`, `:297-303`), `.ufo/waves/round-42/claims.json`,
`.ufo/waves/round-42/c1-controls/do-nothing.txt`, `.ufo/waves/round-42/claims-erratum-3.md`,
`.ufo/waves/round-42/claims-erratum-4.md`, `.ufo/waves/round-42/final-gates/*`, `SCORECARD.md:1634`,
`LOG.md:1804`, `corpus/knowledge/considerthese-proposals-ledger.md`, `considerthese/2026-10-26.md:30`,
`corpus/QUALITY.md:278` (R31), and this wave's landed deliverables (`ExecSourceCapture.*` after the
overwrite, `ExecRegistryRows.rows.txt` after the rewrite, `ScoutSourceHunt.md`, `ScoutAssimilation.md`,
`ScoutSiblingOverlap.md`, `ScoutConsiderthese.txt`, `ExecK19Freeze.freeze-format.txt`, `ScribeCorrections.*`,
`ScribeClaimsErratum.*`).

## `<pending: …>` markers left in the deliverable (deliberate; never invented)

| where | marker | why |
|---|---|---|
| Mistakes, `able to fail` column, all seven rows | `<pending: integration>` | the base suite line for each of K14-K19 is measured at integration; the frozen C1 rule is quoted in the column and the number is not pre-declared |
| `## Census` | `<pending: integration at Y>` | the after value must be read at Y after S067/S068 append; the freeze-tree run is the before value and is labelled as such |
| Gate, Entry bullet | `<pending: ScribeKnowledgeGate>` | `ScribeKnowledgeGate.entry.md` had not landed when this seat last read the wave directory |
| considerthese, after-state | `<pending: integration>` | the C2 receipt (`rules=8 pass=8 fail=0 …`, `selftest cases=10 failures=0`) is the evidence; this seat did not run a sibling's deliverable to stand in for it |
| considerthese, ledger row | `<pending: ScoutConsiderthese>` | `ScoutConsiderthese.txt` supplies the `## Round-42 dispositions` section; no round-43 ledger row was in it |

Nothing else is marked pending. No number in the deliverable is estimated: `73`, `23/73`, `66`, `61`, `0`,
the digests, the line anchors and the quotes each come from a command printed above or from a committed
deliverable named beside them.

## Findings for the L1 (not fixed here — outside this seat's write scope)

1. **Capture and row moved mid-round, and the lesson was rewritten to follow them.** `ExecSourceCapture`
   first landed the curl CVE-2023-38545 advisory (13940 B raw, sha256 `e9038f56…`, 131 lines / 6446 B /
   sha256 `327bc909…`); after the source hunt designated `https://curl.se/docs/CVE-2025-9086.html` it was
   overwritten byte-for-byte (10455 B raw, sha256 `58ca9900…`, 109 lines / 3822 B / sha256 `7e35413a…`),
   and `ExecRegistryRows.rows.txt` was rewritten at the same time (S067 = CVE-2025-9086; S068 = the GHSA
   mirror). The lesson now quotes only the landed 2025-9086 capture and the rewritten rows; no 2023 digest,
   line anchor or quote survives in it. The capture receipt discloses the superseded draft itself.
2. **S068 changed from Mozilla MFSA 2026-99 to GHSA-v676-f8gm-92r9.** The first row version named Mozilla;
   `ExecRegistryRows` messaged this seat at ~13:47Z and the row on disk then named the GHSA entry. The
   lesson follows the landed row (GHSA); the Mozilla page is on no row now and is not in the lesson. The
   Mozilla fetch this seat made at 2026-10-28T16:44:44Z (HTTP 200, 57551 B, 0 redirects) supports nothing
   that lands and is recorded here only so the network record is complete.
3. **The GHSA raw page is not byte-stable.** Three fetches gave 141794, 141795 and 141796 raw bytes with
   different raw digests; every normalization is byte-identical at 191 lines / `530cbcf9…`. The row's pin is
   correctly the normalized text; a raw-digest recheck of that URL would false-red. This deserves a note in
   whatever recheck cadence the row carries (`on-release`).
4. `wave1/ScoutCorpusCensus.md` was a one-line placeholder (`# ScoutCorpusCensus placeholder`) with no
   command and no output when this seat read it; the lesson's census after value stays pending.
5. The frozen C1 predicate writes `SHENON.md`; the lane file is `SHONEN.md` (the r43 correction line and the
   round-42 spot-check both use `SHONEN.md`). The lesson uses the real path; an errata note would put K14's
   scope sentence and the file it grades in agreement.
6. The lesson states the round total as 73 "unless a further wave lands" — the conditional is there so a
   later dispatch cannot falsify the sentence (the RD42-2/RD42-3 class this round grades).

## Write scope, cleanliness, scratch

Written: the deliverable above and this receipt, both under `.ufo/waves/round-43/w1/`; two scratch
directories under `/fast/scratch/hyaku/kasegi-r43/` (`ScribeLessonDraft` for the S067-era check,
`ScribeLessonDraft2` for the GHSA check). No write to `corpus/`, the fleet root, `shokuknow`, any
`*-shokunin` sibling, or any PATH directory. No mutating git ran; git use was `log -1 --format` and
`status --porcelain` only. No subagents spawned, no swarm, no judge.

Both scratch directories were removed after the deliverable and receipt were in the wave directory
(`test ! -e` → `scratch-absent` for `ScribeLessonDraft`; `ScribeLessonDraft2` removed in the same cleanup).
Disk guard was checked before the first fetch (`/fast/scratch/hyaku` 25% used, 606.3G free).

Network: two curl fetches with UA `kasegi-shokunin/1.0`, both HTTP 200 and zero redirects —
`mozilla.org/en-US/security/advisories/mfsa2026-99/` at 2026-10-28T16:44:44Z (57551 B; superseded, see
finding 2) and `github.com/advisories/GHSA-v676-f8gm-92r9` at 2026-10-28T16:48:33Z (141794 B; supports the
S068 block). The S067 quote check used the committed capture, not a new fetch.

Tooling: nothing installed, upgraded or configured; `bash`, `awk`, `sed`, `grep`, `sha256sum`, `curl`,
`python3` as present on the host. TMPDIR was never inherited: every scratch path was explicit.

## Limits

- The lesson is a draft of landable text with the frozen claims table, the seven control-grounded mistake
  rows and the Gate block; the L1 supplies any further rows from the wave receipts and the final
  after-values.
- Quotes were checked against the committed S067 capture and a fresh normalization of the S068 page; both
  pages can be re-rendered upstream, so each pin is the recorded byte digest, not fetch success.
- No claim, kill rule, target or score was evaluated or altered here; the claims table reproduces the frozen
  before/after statements and grades nothing.
