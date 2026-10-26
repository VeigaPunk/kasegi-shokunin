# ScribeRowS053 — round-36 SOURCES row, Search-log bullet and Paths snippet for F19 / S053

Seat: `ScribeRowS053` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane head at draft time: `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze; the only porcelain
lines were untracked `.ufo/waves/round-36/*`). Axes touched: `coverage` (C2's registry row, search-log
`where/date/counts/stop` and negative-sweep ground, and the Paths study line). Assigns no verdict; the
L1 applies the lines.

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/ScribeRowS053/`
(removed after the receipt was written). No lane, fleet, sibling-lane or source-tree file was edited; no
capture was made by this seat; no git/jj mutation was run; no tool was installed.

## 1. Exact lines to land

Registry target: append after the S052 row at `corpus/SOURCES.md:58` (registry held 52 rows `S001`–`S052`;
`grep -n S053 corpus/SOURCES.md corpus/README.md SKILL.md` → no output, exit 1). `## Paths` starts at
`:60`, `## Search log` at `:67` in the frozen file. **This seat did not insert them.**

### 1.1 Row (11 cells, no `|` inside any cell) — for `corpus/SOURCES.md` Registry

```markdown
| S053 | FIRST EPSS documentation page — https://www.first.org/epss/ | docs | A | FIRST's own EPSS statements on the fixed EPSS page: the model definition and its 30-day horizon, the daily 0–1 score with ranking percentiles, the open CSV/API/GitHub distribution and the FIRST EPSS SIG as maintainer | capture corpus/source-snapshots/round-36/S053.txt: Q1 L216 the model sentence (sha256 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9); Q2 L217 the daily 0–1 probability with ranking percentiles; Q3 L217 the CSV/API/github distribution; Q4 L235 the EPSS Special Interest Group at FIRST as maintainer | EPSS estimates the probability that a published CVE will be exploited in the wild in the next 30 days; treat it as a likelihood signal distinct from CVSS severity and KEV catalog status | mined | 2026-10-26 | 90d | corpus/knowledge/epss-exploit-prediction-scoring.md |
```

### 1.2 Search-log bullet (append inside `## Search log`)

```markdown
- FIRST EPSS exploitation-likelihood sweep (round 36); question: does the lane hold a first-party source for exploitation-likelihood scoring that is distinct from CVSS severity and from KEV catalog membership, and does FIRST's own EPSS page add that ground; where: the fixed FIRST EPSS page at https://www.first.org/epss/ captured under the instrument UA into corpus/source-snapshots/round-36/S053.txt (HTTP status 200, content-type text/html, content-length 26804, snapshot 8448 bytes and 244 lines, sha256 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9), plus a negative sweep `grep -rn "EPSS\|exploitation-likelihood" corpus/knowledge/` over corpus/knowledge/*.md (47 files, the pre-F19 state) that printed no lines and exited 1 (0 hits; the pattern is scoped to that directory, and the unhyphenated phrase "exploitation likelihood" does occur once at corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:26 as a generic severity-factor sentence, not an EPSS or exploit-prediction source; the lane's CVSS v4 captures carry only an EPSS navigation link at corpus/source-snapshots/round-24/S001.txt:153-159 and S002.txt:153-159 and 208); date: 2026-10-26; identified 1, screened 1, included 1, excluded 0. The fixed page states EPSS's own model definition, 30-day horizon and daily 0–1 probability, which answers the bounded question; stop: the page is authoritative for F19 and no linked sub-page or secondary explainer was needed.
```

### 1.3 Paths line (append inside `## Paths`)

```markdown
- Exploitation likelihood — S053 → S052 → S001 → S002: start from FIRST's own EPSS definition of a 30-day exploitation probability, contrast it with CISA's KEV catalog membership (S052), then read the CVSS v4 severity documents (S001, S002) that score severity without assigning exploitation likelihood.
```

## 2. Contract v1 checks (measured on the drafted row, not on the applied file)

```
cells 11 inner_pipes False
https_tokens_source_cell 1
id,kind,tier,status,opened,recheck,usedby= S053 docs A mined 2026-10-26 90d corpus/knowledge/epss-exploit-prediction-scoring.md
anchor starts: capture corpus/source-snapshots/round-36/S053.txt: Q1 L216 the model sentence (sha256 4ec6
```

- 11 cells in registry column order `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`; no cell carries `|`; `starts/ends: True True`.
- Source cell carries exactly one `https://` token, byte-equal to the capture manifest's `url`
  `https://www.first.org/epss/` (rule B4/B5 of `corpus/instruments/capture-binding-check.py`).
- `tier` cell `A`; scope cell narrows to FIRST's own statements on the fixed EPSS page, matching the frozen
  claim's "tier A scoped to FIRST's own EPSS statements".
- `teaches` is one learner benefit (30-day exploitation probability as a likelihood signal separate from
  CVSS severity and KEV membership).
- `status mined`, `opened 2026-10-26`, `recheck 90d`, `used-by corpus/knowledge/epss-exploit-prediction-scoring.md`
  exactly as the C2 predicate names them.

## 3. Anchor provenance (capture owned by ExecC2Capture, not this seat)

`corpus/source-snapshots/round-36/S053.txt` is the normalized capture of `https://www.first.org/epss/`
(ExecC2Capture receipt `.ufo/waves/round-36/wave1/ExecC2Capture.md`): HTTP 200, `text/html; charset=UTF-8`,
`content-length` 26804, snapshot 8448 bytes / 244 lines, sha256
`4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`.

Measured on the byte-identical copy left under
`/fast/scratch/hyaku/kasegi-r36/ScribeEntryF19/S053.txt` (same sha256) and the then-present
`/fast/scratch/hyaku/kasegi-r36/ExecC2Capture/S053.txt`:

```
216:The Exploit Prediction Scoring System (EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.
1   # grep -cF count of the manifest Q1 span "(EPSS) is a data-driven … next 30 days."
244 # wc -l → 244 lines
```

IRC confirmation from ExecC2Capture (2026-10-26): the committed bytes must be byte-identical to that file,
Q1 anchor is `216`; manifest Q1 is the 25-word span starting at `(EPSS)` because the full L216 sentence is
30 words; Q2 L217, Q3 L217, Q4 L235. This matches the manifest embedded in
`.ufo/waves/round-36/wave1/ExecC2Capture.md`. The row's `anchor` cites Q1 at L216 with the full sha256 and
the three supporting lines; it makes no quotation claim longer than the page text.

Independent freshness check (ScoutF19Open receipt, same wave): the live raw body sha256
`66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868` equals the capture's served body,
`last-modified 2026-07-30`, no redirect. Nothing here relies on that receipt for the row; it only shows the
capture is current as of the round.

## 4. Negative sweep — exact command and verbatim scope

Executed at the frozen head, cwd = lane:

```
$ grep -rn "EPSS\|exploitation-likelihood" corpus/knowledge/ ; echo "exit=$?"
exit=1          # no output lines
$ ls corpus/knowledge/*.md | wc -l
47
```

Adjacent hits, recorded so the bullet cannot be read as a whole-corpus zero-hit claim:

```
$ grep -rni "exploitation likelihood" corpus/knowledge/
corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:26:A likelihood argument alone therefore does not set a level: exploitation likelihood and other factors are weighed, then the level is decided largely on impact.
$ grep -rni "exploit prediction" corpus/knowledge/ ; echo "exit=$?"
exit=1
$ grep -rn "EPSS" corpus/knowledge/ ; echo "exit=$?"
exit=1
$ grep -n "EPSS" corpus/source-snapshots/round-24/S001.txt corpus/source-snapshots/round-24/S002.txt | head
corpus/source-snapshots/round-24/S001.txt:153:Exploit Prediction Scoring System (EPSS)Why EPSS?
corpus/source-snapshots/round-24/S002.txt:153:Exploit Prediction Scoring System (EPSS)Why EPSS?
```

ScoutF19Open independently reports the broad case-insensitive sweep
`grep -rilE 'EPSS|exploit prediction|exploitation likelihood' corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md`
as **1 hit** (the Immunefi line), with `EPSS` 0 and `exploit prediction` 0. The drafted bullet therefore
states the executed pattern and its directory, names the unhyphenated hit, and does not claim
"0 hits lane-wide".

## 5. Search counts and stop rationale

- `identified 1`: the fixed FIRST EPSS page was the single fixed surface for F19; no search engine was used
  (the item fixes `where`).
- `screened 1`: that page was captured and read; the page's linked sub-pages (How It Works, Why EPSS?,
  Using EPSS, FAQ, Research, Get the Data) were not opened, so they are not counted.
- `included 1`: S053. `excluded 0`.
- Stop: the fixed page states EPSS's own model definition, 30-day horizon, daily 0–1 probability with
  percentiles, distribution channels and maintainer, which answers the bounded F19 question; no secondary
  or linked sub-page was needed for the row.

## 6. Dependency the L1 must land with this row

`corpus/knowledge/epss-exploit-prediction-scoring.md` did **not** exist at draft time
(`test -e` → absent). The row's `used-by` names it as the C2 predicate requires, so the row and that entry
(ScribeEntryF19 / ExecC2's entry work) must land in the same commit or census `dangling-usedby` will flag
the row. This seat did not author the entry.

## 7. Findings and limits

- The lane's pre-existing CVSS captures (`corpus/source-snapshots/round-24/S001.txt:153-159`,
  `S002.txt:153-159` and `208`) contain only an EPSS *navigation link*, not EPSS statements. The row's
  ground therefore rests on S053 alone, and the search bullet says "navigation link", not "source".
- The full L216 definition sentence is 30 words, over the manifest's 25-word pin budget; the row cites the
  line, not a truncated quotation, and the manifest's `location` field records the full sentence.
- Out of scope and unverified here: the knowledge entry body, `knowledge-expected.txt` (47→48), the
  frontier harness (`entries=22 pass=22`, `PASS F19 ids=S053`), `source-recheck.py` exit 0, census exit 0,
  README frontier sentence 18→19, and the junk twin `c2-controls/junk-f19.md`. No claim is made on them.
- No tools installed; scratch `/fast/scratch/hyaku/kasegi-r36/ScribeRowS053/` removed after this receipt.

## 8. Conflict observed after draft — ScribeEntryF19 signs a wrong capture digest (reported verbatim)

At 12:51 on 2026-10-26 the sibling entry receipt `.ufo/waves/round-36/wave1/ScribeEntryF19.md` was
re-read. Its entry header (`:123`) and its pins at `:46`, `:85` and `:372-373` give the capture sha256 as
`4ec61c59b0a9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`; the digest measured on the
byte-identical capture is `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`. The strings
differ only at index 10: `a` versus `e` (`b0a9aedf` versus `b0e9aedf`).

Measured distribution across the round-36 receipts:

```
$ grep -rho "4ec61c59[0-9a-f]*" . | sort | uniq -c
      7 4ec61c59
      4 4ec61c59b0a9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9
     17 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9
$ grep -rln "4ec61c59b0a9aedf" .
./ScribeEntryF19.md
$ grep -rln "4ec61c59b0e9aedf" .
./ScoutCaptureAvailability.md ./ExecC2Capture.md ./ScribeRowS053.md ./ExecManifestChecks.md ./ExecC2QuoteOnce.md ./ExecC2JunkControl.md
```

The `0e9aedf` value is the one in ExecC2Capture's embedded manifest, in six other receipts, and in the
scratch copy `ScribeEntryF19/S053.txt` hashed by this seat at 12:37 (`sha256sum` → `4ec61c59b0e9aedf…83e9`).
This seat's row cites `4ec61c59b0e9aedf…83e9` and is not changed. The conflict was sent verbatim to
`agent://ScribeEntryF19`; the L1 and the canonical judge decide it. It does not affect the row's line
anchors (L216/L217/L235), the manifest URL, or any cell shape.

Resolution (verified read-only at 12:56 on 2026-10-26): ScribeEntryF19 re-derived the digest and fixed the
entry; `grep -c "4ec61c59b0a9aedf" ScribeEntryF19.md` → 1 (the §5 correction paragraph that records the
error) and `grep -c "4ec61c59b0e9aedf" ScribeEntryF19.md` → 6 (the entry `source:` line, the Scope pin,
the §2 table and the findings). The sibling also scoped its H1 and rule (b) so L234's KEV is named as
VulnCheck's feed, not the CISA catalog. No change to this seat's row.

Artifact: `.ufo/waves/round-36/wave1/ScribeRowS053.md`.
