# ScribeEntryF19 — round 36: F19 knowledge entry (FIRST EPSS) drafted, ready to land

Seat: `ScribeEntryF19` (leaf, scribe). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`).
Axis: coverage (C1 depth:verifiability untouched by this seat). Milestone: round-36.
All measurements on 2026-10-26. Report path: `.ufo/waves/round-36/wave1/ScribeEntryF19.md`.

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/ScribeEntryF19/`.
No lane file, registry row, manifest, capture, entry, instrument or scorecard was edited; no git/jj
mutation was run; no subagent was spawned; `agent://all` was not messaged. The scratch directory is
removed after this receipt is written; the entry text below is the deliverable byte-for-byte.

---

## 1. Deliverable

`corpus/knowledge/epss-exploit-prediction-scoring.md` — full text in §6 between the
`---BEGIN ENTRY---` and `---END ENTRY---` markers. L1 lands it (this seat has no lane write scope).
It measures 263 lines / 17,374 bytes; `##` sections: Attribution, Claim 1-6, What the
capture does not contain, Honest limit, Falsifiable rule and checks, Rejected over-generalizations,
Scope and limits of the pin.

Requirement coverage, each point checked against the drafted bytes:

| requirement | how the draft meets it |
|---|---|
| QUALITY Q1 (three header lines under H1) | `source:` names row `S053`, URL `https://www.first.org/epss/`, capture path, 244 lines, 8,448 bytes, full sha256 and the line anchors the claims cite; `verified-at: 2026-10-26`; `recheck:` one command. A fourth line `ground: F19` mirrors `cisa-kev-catalog.md`'s `ground: F18`. |
| Q2 (tier-A support) | every load-bearing claim quotes the S053 capture; no other source is cited as support. |
| Q3 (≤25-word verbatim quote + exact location) | 11 blockquoted spans, max 25 words (measured), each carrying `— L<n>`; four of them are the manifest pins verbatim. |
| Q4 (attribution kept) | Attribution section states the page is FIRST's self-description and names Empirical Security as score generator (L235); the partner list is quoted with its "includes but is not limited to" bound (L234); "freely and openly accessible" is scoped to the data, not the model. |
| Q5 (falsifiable rule + rejected over-generalization) | Falsifiable rule with four limbs (a)-(d) plus FC-1..FC-5 runnable checks; 8 rejected over-generalizations with reasons. |
| Q6 (documentation only) | no credential, session or private URL; no probing/scanning/login/submission instruction; the only commands read local capture bytes. |
| Q7 (recheck is a command, names what it checked, has a failing control) | `source-recheck.py --manifest … --source S053` prints `S053:sha256 OK` plus one `S053:Q<n> OK … occurrences=1` line per pin; observed failing control: missing manifest → `manifest UNAVAILABLE reason=missing`, rc=2. |
| Q10 (one command, `bash -n`, `cd` prefix, `#` note) | measured `bash -n` rc=0; line carries `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` and a `#` note; backticks and `$(` avoided inside the note. |
| R12 (recheck's `--source` matches the entry's header ids and the manifest lists it) | header `source: S053`; recheck `--source S053`; the landed manifest's record id is `S053`. |
| item content brief (model definition, 0-1 output + percentiles, cadence/free access via CSV/API/github, distinct axes vs CVSS severity and KEV) | Claims 1-4; each element traces to a quoted line, and "no severity" is a measured token fact rather than an assertion about CVSS itself. |
| item constraint (no claim outside the capture) | the capture-only boundary is stated twice: "Honest limit" and "Scope and limits of the pin"; the CISA/S052 disambiguation is marked as a disambiguation, not a claim about EPSS. |

---

## 2. Provenance of the capture I anchored against

| fact | value | where observed |
|---|---|---|
| capture | `S053.txt`, 244 lines, 8,448 bytes | `wc -l`, `wc -c` |
| capture sha256 | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` | `sha256sum` |
| source of those bytes | `/fast/scratch/hyaku/kasegi-r36/ExecC2Capture/S053.txt`, read before that seat removed its scratch; copied to my scratch and re-hashed (same digest) | `ls`, `cp`, `sha256sum` |
| upstream fetch (that seat, per `.ufo/waves/round-36/wave1/ExecC2Capture.md` §1) | `https://www.first.org/epss/`, HTTP 200, `text/html; charset=UTF-8`, 26,804 served bytes, no redirect, `fetched_utc` 2026-10-26T15:35:10Z, `last-modified: Thu, 30 Jul 2026 13:48:13 GMT` | that receipt §1 (read, not re-run) |
| manifest pins (that seat) | Q1 L216 (25 words), Q2 L217 (8), Q3 L217 (23), Q4 L235 (23); manifest sha256 `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` | that receipt §3-§4 (read, not re-run) |
| independent cross-check by this seat | one read-only GET `curl -sSL -A kasegi-shokunin/1.0 https://www.first.org/epss/` → HTTP 200, `text/html; charset=UTF-8`, `size_download=26804`, final URL == requested URL; served-body sha256 `66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868` | my own `curl -w` + `sha256sum` of the saved body |

The cross-check matters for one reason only: the body digest I measured on my own fetch equals the
`raw.html` digest ExecC2Capture recorded, so the normalized capture I anchored against is the page as
served on 2026-10-26 and not a variant. It is not a re-verification of that seat's work and no claim
in the entry rests on it.

---

## 3. Verification actually run (all on the byte-identical copy, sha256 `4ec61c59…83e9`)

| # | check | observed output |
|---|---|---|
| V1 | `bash -n` on the extracted `recheck:` command line | `rc=0` |
| V2 | run the `recheck:` line from the lane root before the manifest lands | `manifest UNAVAILABLE reason=missing`, `run_rc=2` (fail-closed; not a pass) |
| V3 | 11 cited spans: uniqueness, word budget, anchor binding (`str.count`, `split()`, anchor window `L[n-1:n+3]`) | `spans 11 occ_all_1 True words_max 25 anchors_ok 11 of 11` |
| V4 | four manifest pins `grep -cF` | `1 1 1 1` |
| V5 | absent vocabulary | `severity=0 reward=0 http=0 bounty=1 threshold=1` |
| V6 | present vocabulary | `CVSS=33 KEV=2 calibration=1 percentile=2 probability=2 score=4` |
| V7 | 30-day horizon line | `216` |
| V8 | `CVSS` distribution | 33 occurrences on 28 lines: 31 in navigation (L70-L198, 26 lines; five lines carry two), 1 at L222, 1 at L224 |
| V9 | marker lines on the entry's own lines | `KEV` only on L224 and L234; `threshold` only on L224; `calibration` only on L220; `percentile` only on L217 and L226; `probability` only on L216 and L217; `score` only on L224, L226, L230, L235 |
| V10 | entry's quoted spans vs capture, re-extracted from the final markdown | 11 blockquotes, each `occ=1`, each ≤25 words; the four pinned spans are byte-equal to the manifest pins |
| V11 | digest the entry's `source:` line and Scope bullet print, re-derived after the peer reports: extract the normalized capture embedded in `ExecC2Capture.md` §6, write to scratch, `sha256sum` | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`, 8,448 bytes, 244 lines — equals the manifest `sha256` field; no pin in this receipt carries the former `b0a9aedf` form, which survives only inside the §5 correction that quotes it as the error |
| V12 | FC-2 re-run against the re-derived capture copy | `spans 11 occ_all_1 True words_max 25 anchors_ok 11 of 11` (the recovered bytes are the same bytes the entry was anchored on) |

Not run by this seat, deliberately: `source-recheck.py` against a real manifest (the manifest is not
landed), the F19 harness, source-recheck S053 exit-code measurement, census, and any F19 junk-twin
rejection. Those are C2 executor seats' evidence, not mine, and this receipt does not restate them as
measured here.

---

## 4. Findings for L1 (things that will bite if they are missed)

1. **Land the capture byte-identically or the entry re-anchors.** The entry's ten line anchors
   (L216, L217, L220, L222, L224, L226, L230, L232, L234, L235) are valid only for the 244-line
   normalization with sha256 `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`. A
   re-normalization that keeps or drops a line shifts them all; re-run FC-2 (it prints
   `anchors_ok 11 of 11`) after landing.
2. **Seven cited spans sit outside the manifest.** Only L216, L217 (×2) and L235 are pinned; L220,
   L222, L224, L226, L230, L232 and L234 are exactly-once but unpinned, so `source-recheck.py` will
   not police them and FC-2 is the only guard. If a later round wants them pinned, that is a new
   manifest revision, not an entry edit.
3. **Q2 and Q3 are two clauses of one L217 sentence**, both anchored at 217 — the instrument prints
   `anchor=217-ok` twice, which is correct and not a duplicate-quote defect (the spans do not overlap:
   `EPSS publishes a 0–1 probability (with ranking percentiles)` ends before `every day for every CVE`).
4. **U+2013.** `0–1` is the page's en dash; a hyphen there fails `grep -cF` and the manifest pin.
5. **"KEV" in this capture is not the CISA catalog.** L224 says combine with KEV; L234 names
   "VulnCheck KEV (VulnCheck Known Exploited Vulnerabilities)" as one data partner. The entry says so
   explicitly so the S053 row's `teaches` cell and the C2 claim do not read `KEV` as S052.
6. **The entry makes no calibration, threshold or accuracy claim.** L220 is a pointer to the How It
   Works page, and the capture has no figure behind it. A C2 claim sentence that asserts measured
   performance would not be supported by S053.

---

## 5. Conflicts and disagreements recorded verbatim

- `ExecC2QuoteOnce` (peer, independent quote verifier), message of 2026-10-26, verbatim:
  "Note your mine.txt spaces differ from the normative S053.txt (e.g. S053.txt has \"github repo, so\"
  with no space before the comma); quote from S053.txt bytes, not mine.txt." — Recorded as observed:
  the difference is real. `mine.txt` was this seat's own ad-hoc normalization of the served HTML for
  drafting; every quote in the deliverable was taken from the normative `S053.txt` bytes and re-checked
  against them (V3/V10), and `mine.txt` is discarded with the scratch directory.
- **Correction (digest), caught by three peers before landing and fixed in this receipt.** The draft I
  composed at 12:41 wrote the capture sha256 as `4ec61c59b0a9aedf…83e9` in four places (the entry's
  `source:` line, the entry's Scope bullet, §2's table, §4's finding 1) — a one-nibble transcription
  error from my terminal output, not a different file. `ExecC2QuoteOnce` ("a one-hex-digit corruption
  … a reader who checks the header hash against the landed S053.txt gets a mismatch (false evidence
  line)"), `MutJunkTwin` ("one-hex-digit drift at position 10 … the entry's inline evidence line is
  currently false") and `ScribeRowS053` ("the `0a` variant appears only 4 times, all in your
  ScribeEntryF19.md") reported it independently. I re-derived the digest before changing anything: I
  extracted the normalized capture embedded in `ExecC2Capture.md` §6, wrote it to scratch and hashed it
  → `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`, 8,448 bytes, 244 lines,
  matching the manifest's `sha256` field and the seat's own reported digest. All four occurrences now
  carry the `b0e9` form; the wrong string survives only in this paragraph, where it is quoted as the
  error. `source-recheck.py` was
  immune throughout (it reads the manifest digest), which is exactly why the false line survived my own
  verification: my V-table checked quotes against the file bytes, never the transcribed hex.
- `ScribeRowS053` also flagged the entry title's bare "KEV membership": the H1 now reads "…a separate
  axis from CVSS severity and from KEV membership (L234's KEV is VulnCheck's feed, not the CISA
  catalog)" and rule limb (b) names VulnCheck KEV, so no heading or rule reads `KEV` as CISA's catalog.
- No disagreement with any other measured figure in `.ufo/waves/round-36/wave1/ExecC2Capture.md` was
  found: the digest (after the correction above), line count and the four pins match byte-for-byte.

---

## 6. Entry text — verbatim, to be landed at `corpus/knowledge/epss-exploit-prediction-scoring.md`

---BEGIN ENTRY---
# FIRST EPSS — exploitation likelihood as a 0–1 probability, a separate axis from CVSS severity and from KEV membership (L234's KEV is VulnCheck's feed, not the CISA catalog)

source: S053 — https://www.first.org/epss/ — capture corpus/source-snapshots/round-36/S053.txt (244 lines, 8448 bytes; sha256 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9): title L1 and L208, definition L216, probability/percentiles/cadence/access L217, topic pointers L220-L230, combining with CVSS and KEV L224, SIG L232, data partners L234, maintainer L235
verified-at: 2026-10-26
ground: F19
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053   # prints S053:sha256 OK then one S053:Q<n> OK line per pinned quote with occurrences=1 and anchor=N-ok; exits 2 when the manifest or capture is absent and 1 when the sha256 differs or a quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

FIRST's own page, read as FIRST's own statement and nothing wider (Q4). The
page names the parties on one line: the EPSS Special Interest Group at FIRST
maintains it, and Empirical Security generates the scores (L235). Exploitation
activity data comes "in part by a number of industry and government partners"
(L234). So a description of what EPSS is and what it publishes is FIRST's
self-description of its own system; what any downstream pipeline does with the
number is outside these bytes.

## Claim 1 — a model that estimates a probability, scoped to a published CVE and a 30-day horizon

> "(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days." — L216 (the page's full sentence is 30 words; the pin starts at the parenthetical, 25 words)

Four parts, all on that line: the estimator is "data-driven machine-learning";
the quantity is "the probability", and the verb is "estimates"; the unit is "a
published CVE"; the horizon is "the next 30 days". An EPSS score is therefore a
per-CVE exploitation-likelihood estimate over a fixed window — not a severity, not
an impact statement, and not a judgement about a host, a product, a program or a
report.

The page states the design intent in its own words on the next line:

> "It offsets subjective judgments with empirical signals from observed exploitation and ongoing activity" — L217

The purpose label the page uses elsewhere is "exploitation likelihood as a
prioritization signal" (L222, quoted in Claim 4): the number orders remediation
work. The capture attaches no impact dimension to it anywhere.

## Claim 2 — the output: a 0–1 probability together with ranking percentiles

> "EPSS publishes a 0–1 probability (with ranking percentiles)" — L217

Two outputs in one clause: the score's stated domain is 0–1, and a second number,
"ranking percentiles", ranks it. The FAQ pointer keeps the two separate:

> "about the score, the percentile, and how EPSS compares to other tools" — L226

A score and its percentile are distinct numbers, and the page treats "the score"
and "the percentile" as two named things a reader asks about. The capture
contains no worked example — no numeric score, no CVE record, no percentile
table — so 0–1 and the existence of a percentile are the measured statements;
what a particular value means in practice is not in these bytes.

## Claim 3 — cadence and access: daily, for every CVE, free and open, over CSV, API and a github repo

> "every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo" — L217

The cadence is daily and the population is "every CVE", stated in the same clause
as the three distribution channels. The Get the Data pointer repeats both:

> "API reference, daily CSV downloads, historical scores, and integration examples." — L230

So the page promises a daily cadence, historical scores, and CSV, API and github
repo access, and describes that access as free and open (L235, quoted in Claim 5:
"published freely to the community"). "Freely and openly accessible" is a
statement about the data (Q4), not about the model's source code; the capture says
nothing about a licence. It also carries no endpoint: `http` occurs 0 times, so
this entry records channels, not addresses.

## Claim 4 — distinct axes: CVSS and KEV are separate inputs combined with EPSS, and this page measures neither severity nor membership

> "How to set thresholds, combine EPSS with CVSS and KEV, interpret score changes, and avoid common misuses." — L224

That sentence is the "Using EPSS" pointer. Its own verb is "combine": CVSS and KEV
are inputs that sit beside EPSS, and threshold-setting, change interpretation and
misuse-avoidance are topics routed to another page. The capture states no
threshold value and no combination rule. The "Why EPSS?" pointer separates the
axes a second time:

> "The empirical case for exploitation likelihood as a prioritization signal. Performance data, CVSS comparison, and what the research shows." — L222

Three axes follow, each from its own text:

- **EPSS** measures exploitation likelihood over 30 days (L216, Claim 1).
- **CVSS** appears in this capture as the FIRST CVSS SIG's subject in the site
  navigation (31 of its 33 occurrences, on 26 lines from L70 to L198) and twice
  in the page's own prose (L222, L224) — a scoring system the reader is told to
  compare and combine with, and one this capture never defines.
- **KEV** appears twice: as a thing to combine with (L224) and as a named data
  partner, "VulnCheck KEV (VulnCheck Known Exploited Vulnerabilities)" (L234).
  That partner is VulnCheck's feed; the capture never mentions CISA, so "KEV"
  here must not be read as the CISA catalog this corpus holds as S052.

The severity vocabulary is absent outright: `severity` occurs 0 times and no
impact, score banding or rating field appears anywhere in the capture. A high
likelihood number and a high severity number are two different signals, and the
page's own instruction is to combine them, not to rank one against the other.

## Claim 5 — who maintains it, who generates the scores, and how it is published

> "EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community." — L235

Maintenance and generation are attributed to different parties in consecutive
sentences: the SIG at FIRST maintains the system, Empirical Security generates
the scores, and the scores are published freely. The SIG is described as a
practitioner community rather than an editorial board:

> "The EPSS Special Interest Group (SIG) is a practitioner community focused on putting EPSS to work." — L232

with a standing cadence ("Members meet every other Friday", L232) and an open
door ("the SIG is where the conversation happens", L232). A copy of the scores is
therefore not a FIRST policy statement; the page is.

## Claim 6 — the data partners are named in part, not in full

> "Exploitation activity data used in EPSS is provided in part by a number of industry and government partners" — L234

The sentence continues with three names — VulnCheck KEV, Shadow Server Foundation,
LevelBlue — and bounds itself with "which includes but is not limited to". The
partner list is open and incomplete (Q4): these three are not the only inputs, and
the capture does not describe the model's features or weights.

## What the capture does not contain

- **No numeric example.** No score, no CVE record, no percentile table, no dataset.
  `probability` occurs twice (L216, L217) and `percentile` twice (L217, L226), both
  descriptively.
- **No model detail.** "Model methodology, feature overview, calibration, and known
  limitations." (L220) is a pointer to the How It Works page; the capture makes no
  calibration claim of its own.
- **No threshold value.** `threshold` occurs once (L224), inside the pointer
  sentence that promises the guidance elsewhere.
- **No severity and no reward vocabulary.** `severity` 0, `reward` 0; `bounty`
  occurs once as FIRST's own navigation item "Bug Bounty Program" (L25), not an
  EPSS field. `score` occurs on four lines (L224, L226, L230, L235), each inside
  prose quoted above.
- **No URLs.** `http` occurs 0 times: the page names the channels (CSV, API,
  github repo), never an address.

## Honest limit

- **A hub page, not the documentation.** This capture is the EPSS landing page:
  one definition paragraph (L216-L217), seven topic pointers (L220-L230), a
  community paragraph (L232), data partners (L234) and a maintainer line (L235).
  The methodology, calibration, limitations, thresholds and CVSS/KEV comparison
  guidance all live on pages this capture only names.
- **Pinned, not live.** The recheck compares this entry's quotes with the captured
  bytes of 2026-10-26T15:35:10Z (the manifest's `http` block: status 200,
  `text/html; charset=UTF-8`, no redirect; `fetched_bytes` 26,804). It says nothing
  about the page after that instant; a re-fetch is a new capture with a new pin.
- **One en dash.** `0–1` in L217 is the page's own U+2013; a reader grepping the
  bytes must use that character, not a hyphen.
- **The capture names no CVE.** No example score, no identifier, no exploit
  reference appears in it, so any per-CVE illustration in a downstream report is
  that report's own evidence, not S053's.
- `verified-at: 2026-10-26` is when this entry was written and its quotes checked
  against the pin, not the capture instant.
- Documentation only: the capture holds no credential, session or private URL and
  this entry quotes none (Q6). Nothing here authorizes probing, scanning, logging
  in, or submitting against any target.

## Falsifiable rule and checks

**Falsifiable rule.** An EPSS-derived statement is checkable against S053 by four
tests, and any one failing falsifies the claims above:

- (a) a reported score outside `[0, 1]`, or a single number presented as both the
  score and the percentile, contradicts Claim 2 (L217);
- (b) a report that treats an EPSS value as a severity band, a reward or payout
  multiplier, or as membership in the KEV feed S053 names (VulnCheck KEV, L234)
  contradicts Claim 4 (L224, L222) — `severity` and `reward` occur 0 times in the
  capture;
- (c) an exploitation claim about a named host, product, program or report, rather
  than about "a published CVE" within "the next 30 days", contradicts Claim 1
  (L216);
- (d) the pinned quotes must each occur exactly once with the pinned sha256; the
  `recheck:` line prints `occurrences=1` per quote and exits non-zero otherwise, so
  a moved or corrupted capture re-opens every claim instead of passing silently.

**FC-1 — every pinned quote occurs exactly once.** Four `grep -cF` counts on the
capture, run from the lane root; observed `1 1 1 1`:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
for q in '(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.' \
         'EPSS publishes a 0–1 probability (with ranking percentiles)' \
         'every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo' \
         'EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.'; do
  printf '%s ' "$(grep -cF -- "$q" corpus/source-snapshots/round-36/S053.txt)"
done; printf '\n'
```

**FC-2 — eleven cited spans: unique, ≤25 words, on their anchor line.** Observed
`spans 11 occ_all_1 True words_max 25 anchors_ok 11 of 11`:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -c 't=open("corpus/source-snapshots/round-36/S053.txt",encoding="utf-8").read();L=t.splitlines();q=[(216,"(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days."),(217,"EPSS publishes a 0–1 probability (with ranking percentiles)"),(217,"every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo"),(235,"EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community."),(220,"Model methodology, feature overview, calibration, and known limitations."),(222,"The empirical case for exploitation likelihood as a prioritization signal. Performance data, CVSS comparison, and what the research shows."),(224,"How to set thresholds, combine EPSS with CVSS and KEV, interpret score changes, and avoid common misuses."),(226,"about the score, the percentile, and how EPSS compares to other tools"),(230,"API reference, daily CSV downloads, historical scores, and integration examples."),(232,"The EPSS Special Interest Group (SIG) is a practitioner community focused on putting EPSS to work."),(234,"Exploitation activity data used in EPSS is provided in part by a number of industry and government partners")];print("spans",len(q),"occ_all_1",all(t.count(x[1])==1 for x in q),"words_max",max(len(x[1].split()) for x in q),"anchors_ok",sum(x[1] in " ".join(L[x[0]-1:x[0]+3]) for x in q),"of",len(q))'
```

**FC-3 — absent vocabulary.** `severity=0 reward=0 http=0 bounty=1 threshold=1`:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
for t in severity reward http bounty threshold; do printf '%s=%s ' "$t" "$(grep -oiF -- "$t" corpus/source-snapshots/round-36/S053.txt | wc -l)"; done; printf '\n'
```

**FC-4 — present vocabulary.** `CVSS=33 KEV=2 calibration=1 percentile=2 probability=2 score=4`:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
for t in CVSS KEV calibration percentile probability score; do printf '%s=%s ' "$t" "$(grep -oiF -- "$t" corpus/source-snapshots/round-36/S053.txt | wc -l)"; done; printf '\n'
```

**FC-5 — the 30-day horizon is stated once, on the definition line.** Observed `216`:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
grep -nF '30 days' corpus/source-snapshots/round-36/S053.txt | cut -d: -f1
```

## Rejected over-generalizations

1. **"EPSS predicts exploitation."** Rejected: the source's verb is "estimates the
   probability" (L216), and the page routes "calibration, and known limitations"
   (L220) to a separate page. A probability is not a per-CVE forecast, and calling
   it one adds certainty the capture withholds.
2. **"EPSS is a severity score, or a substitute for CVSS."** Rejected: `severity`
   occurs 0 times and no impact field exists, and the page's instruction is
   "combine EPSS with CVSS and KEV" (L224) — combination is not replacement.
3. **"EPSS membership is KEV status."** Rejected: `KEV` occurs twice (L224, L234),
   once as a thing to combine and once as VulnCheck's product named as a data
   partner; the capture never mentions CISA and never equates the two. The two
   feeds answer different questions, and this page treats KEV as an input.
4. **"A high EPSS score means my system is exploitable."** Rejected: the estimate
   is about "a published CVE" being exploited "in the wild" within 30 days (L216);
   the capture carries no host, product, configuration or telemetry unit for a
   reader's own estate.
5. **"Every identifier gets a score."** Rejected: the text says "every CVE" (L217)
   and "a published CVE" (L216). Nothing extends the population to other
   identifier types, to unpublished reports, or to non-CVE findings.
6. **"EPSS is open source."** Rejected: "freely and openly accessible" (L217)
   modifies "the data", and "published freely to the community" (L235) describes
   the scores. The capture says nothing about code, licence or model publication.
7. **"EPSS sets your remediation policy."** Rejected: "How to set thresholds"
   (L224) is a pointer to guidance this capture does not contain; no threshold
   value, no policy and no decision rule appears in these bytes.
8. **"EPSS is a reward or payout scaler."** Rejected: `reward` occurs 0 times and
   `bounty` occurs once as FIRST's own "Bug Bounty Program" navigation item (L25);
   the capture contains no amount, currency or payout field. F13 and F17 hold
   reward and impact ladders; this page holds a likelihood and its rank.

## Scope and limits of the pin

- Pin: `corpus/source-snapshots/round-36/S053.txt` (244 lines, 8,448 bytes, sha256
  `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`), bound by
  `corpus/source-snapshots/round-36/manifest.json` (record S053: same digest, the
  page URL, `fetched_utc` 2026-10-26T15:35:10Z, and the four pinned quotes Q1-Q4,
  each `occurrences=1` with a verifying anchor).
- The four pinned assertions cover L216, L217 (two) and L235. The remaining cited
  spans (L220, L222, L224, L226, L230, L232, L234) occur exactly once but sit
  outside the manifest, so FC-2 is what keeps those line numbers honest.
- `CVSS` 33 occurrences are dominated by site navigation (L70-L198); only L222 and
  L224 are the page's own prose about it. Counting the token alone would overstate
  what the page says about CVSS.
---END ENTRY---

## 7. Out of scope for this seat, and what it did not touch

- **Not written:** `corpus/knowledge/epss-exploit-prediction-scoring.md` itself (L1 lands it from §6),
  `corpus/SOURCES.md` (row S053 is `ScribeRowS053`'s), `corpus/instruments/frontier-harness.*`,
  `corpus/registry*`, `SCORECARD.md`, `SKILL.md`, the round-36 lesson, `claims*.json`, and the
  round-36 manifest/capture (both `ExecC2Capture`'s findings for L1 to land).
- **Not measured here:** harness `entries=22 pass=22`/`PASS F19 ids=S053`, `source-recheck S053`
  exit 0 on the landed manifest, census exit 0, knowledge count 47→48, the junk twin
  `c2-controls/junk-f19.md` rejection. Each belongs to a C2 executor receipt; this receipt cites none
  of them as its own evidence.
- **Not run:** no git/jj mutation, no subagent spawn, no `agent://all` message, no lane/tree write
  outside the two allowed paths, no campaign tool from `/home/vgpnk/Projects/shokuknow`.
- **Tooling:** nothing installed and nothing upgraded — `pacman` was not invoked (host-wide pause
  respected), no `uv tool install`, no `npx`, no binary drop. Tools used as already present:
  `curl`, `sha256sum`, `grep`, `python3`, `bash`.
- **Scratch:** `/fast/scratch/hyaku/kasegi-r36/ScribeEntryF19/` removed after this receipt was copied
  into the wave dir, per the seat's scratch rule. Nothing in this receipt depends on a surviving
  scratch file: the capture is pinned by sha256 and its bytes are in the landed snapshot, and every
  command in FC-1..FC-5 reads `corpus/source-snapshots/round-36/S053.txt`.
