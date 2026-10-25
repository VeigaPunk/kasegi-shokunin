# Q2TierSupport — Q2 tier/kind support for the round-23 F06/F07/F08 entries

Seat: `L1Kasegi23.Q2TierSupport-2` (critic). Read-only. This file is the only write.
No admission, integration, or score movement is claimed. No install/update was performed, so
the tooling directive has no install to record.

## Question and method

Re-derive QUALITY Q2 — *"Every load-bearing claim rests on ≥1 tier-A or tier-B row for that
claim's scope, opened in the admitting round; a tier-C row is never sole support"*
(`corpus/QUALITY.md:12`) — for F06, F07 and F08, without taking the L1's Q1–Q6 assessment.

Admitting round = round 23; its dated artifacts are 2026-10-20 (`corpus/SOURCES.md:33-36`,
the three entries' `verified-at`). Round 22's entries were read 2026-10-19
(`corpus/README.md:5`).

Commands run (all read-only):

```
grep -n "^| S0" corpus/SOURCES.md
grep -n "S0[0-9][0-9]\|patch date\|24 hours\|72 hours" corpus/knowledge/*.md
for s in S018 S029 S030; do python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source $s; echo "exit=$?"; done
```

The three declared rechecks all exit 0 with every pinned quote `OK` (output in §5). Capture
integrity is therefore *not* the defect axis here: the findings below are scope/currency
mismatches between a claim and the row it rests on.

## 1. Registry cells actually in play

| row | kind | tier | `opened` cell | status | scope cell (abridged) | cited by |
|---|---|---|---|---|---|---|
| S018 (`SOURCES.md:24`) | docs | A | 2026-10-19 | mined | FIRST's recommended practices for multi-party vulnerability coordination | F06 |
| S030 (`SOURCES.md:36`) | spec | A | 2026-10-20 | mined | "CVE Program CNA scope, vulnerability determination and assignment requirements **in version 4.2.0**"; teaches: "use **current** 4.2.0 requirements" | F07 |
| S029 (`SOURCES.md:35`) | spec | A | 2026-10-20 | mined | "Original official CRA Article 14 manufacturer reporting duties and Article 71 application dates"; anchor "Articles 14(1)-(4), 15, 16 and 71" | F08 |
| S022 (`SOURCES.md:28`) | spec | A | 2026-10-19 | **queued** | CNA v4.1.0 sections 3.1 and 4.1; superseded by S030 | F07 (`:17`) |
| S024 (`SOURCES.md:30`) | spec | A | 2026-10-19 | queued, Article 14 "not yet verified" | superseded by S029 | not cited |

No F06/F07/F08 claim cites a tier-C row (S026/S027). No claim is supported *solely* by a
tier-C row, so Q2's tier clause fails nowhere for that reason.

## 2. F06 — `corpus/knowledge/multiparty-vulnerability-coordination.md`

| # | load-bearing claim (line) | row · tier/kind | verdict |
|---|---|---|---|
| 1 | record finder, upstream vendor, downstream vendors, affected-product boundaries, optional coordinator (`:8-10`) | S018 · docs/A | supported — FINDER / UPSTREAM / DOWNSTREAM / COORDINATOR definitions are in the captured excerpt |
| 2 | distinguish unconfirmed downstream relationship from confirmed affected product (`:10-11`) | S018 · docs/A | supported — "Vendors should pre-establish upstream and downstream vendor relationships to understand potential impacts" |
| 3 | record contact ownership, negotiated expectations, per-party timeline (`:11-12`) | S018 · docs/A | supported — "All parties should clearly and securely communicate and negotiate expectations and timelines." |
| 4 | "one vendor's patch date is not evidence that every downstream product has received a fix" (`:12-13`) | S018 · docs/A | **support exists in captured bytes, but the entry pins the wrong line** — see F3 |
| 5 | not a universal legal deadline / no authorization to test (`:15-17`) | scope disclaimer, no positive claim | no source needed |
| 6 | six evidence-table consequences (`:25-30`) | S018 · docs/A | supported; the "minimize exposure" row's consequence is correctly scoped to exposure |

**Verdict: Q2 PASS on tier and scope** (S018 is tier A, kind docs, and its scope cell covers
every claim above). One provenance defect (F2) and one quote-binding defect (F3, Q3 not Q2).

## 3. F07 — `corpus/knowledge/cna-assignment-and-vulnerability-rules.md`

| # | load-bearing claim (line) | row · tier/kind | verdict |
|---|---|---|---|
| 1 | review separates determination, assignment scope, identifier counting (`:8-9`) | S030 · spec/A | supported (3.1, 4.1, 4.2 in snapshot) |
| 2 | demonstrated security impact ≠ assignment authority (`:9-10`) | S030 · spec/A | supported (3.1.1, 3.1.4, 4.1.2) |
| 3 | identifier or vendor fix ≠ distinct independently fixable vulnerability (`:10-11`) | S030 · spec/A | supported (4.1.9, 4.2.7, 4.2.12) |
| 4 | "These are CVE Program rules for CNAs, not universal bounty eligibility criteria" (`:12`) | scope disclaimer | no source needed |
| 5 | **"The public document's current version opened this round is 4.2.0"** (`:14`) | S030 · spec/A, scoped to v4.2.0 | **Q2 FAIL — see F1** |
| 6 | S022 preserves 4.1.0 and must not silently become a 4.2.0 claim (`:14-16`) | S022 + S030 · spec/A | supported as a version-separation statement |
| 7 | independently fixable moved 4.1.10 (v4.1.0) → 4.1.9 (v4.2.0) (`:16-17`) | S022 · spec/A (queued, opened cell 2026-10-19) + S030 | claim is **true** (reproduced, F4); row-cell/status debt only |
| 8 | 3.1.1 / 3.1.4 / 4.1.2 / 4.1.9 / 4.2.1.1 / 4.2.12 table rows (`:26-29,31,33`) | S030 · spec/A | supported, and unchanged or unversioned in 4.2.6 |
| 9 | **"4.2.11 … CNAs SHOULD assign different CVE IDs to different, Independently Fixable Vulnerabilities"** (`:30`) | S030 · spec/A, scoped to v4.2.0 | **Q2 FAIL — see F1** |
| 10 | 3.2.4.2 coordination-method requirement / first-refusal waiver (`:35-38`) | S030 · spec/A | supported (snapshot line 110; same numbering in 4.2.6) |
| 11 | falsifiable check: 4.1.10 interdependent conditions = one vulnerability (`:43-46`) | S030 · spec/A | supported (snapshot line 166; same in 4.2.6) |
| 12 | rejected: 4.1.11 dependency update, 4.2.7 fixes, 4.2.13(1) shared code (`:52-56`) | S030 · spec/A | supported (snapshot lines 170, 204, 213-214) |

**Verdict: Q2 FAIL** on claims 5 and 9. Every other claim is tier-A supported, and the
section-number advice the README carries is correct.

## 4. F08 — `corpus/knowledge/cra-manufacturer-reporting-duties.md`

| # | load-bearing claim (line) | row · tier/kind | verdict |
|---|---|---|---|
| 1 | Article 14 covers actively exploited vulnerabilities and severe incidents (`:9-13`) | S029 · spec/A | supported (captured Art 14(1), 14(3)) |
| 2 | two tracks must not be collapsed (`:13`) | S029 · spec/A | supported (14(2) vs 14(4)) |
| 3 | Article 71: Art 14 from 2026-09-11; general application 2027-12-11 (`:15-16`) | S029 · spec/A | supported and pinned |
| 4 | six clock rows (`:29-34`) | S029 · spec/A | in scope; **14(4)(a)/(b) have no pinned quote** — see F5 (Q3) |
| 5 | Art 14(1)/(3) → CSIRT-coordinator + ENISA via Art 16 platform (`:36-39`) | S029 · spec/A | in scope (anchor names 14(1)-(4), 15, 16); unpinned — see F5 |
| 6 | Article 15 voluntary notifications by others; no testing grant (`:64-66`) | S029 · spec/A | in scope (anchor names Article 15); unpinned — see F5 |
| 7 | rejected "every researcher must publish in 24h" (`:64-66`) | S029 · spec/A | supported as a rejection of a generalized duty |

**Verdict: Q2 PASS.** S029 is tier A/spec, opened 2026-10-20 (the admitting round), and its
scope cell names Articles 14(1)-(4), 15, 16 and 71 — every claim above falls inside it.

## 5. Findings

### F1 — F07 Q2 FAIL: two current-rule claims rest on a row scoped to a version that was already superseded on the admitting date

Evidence (reproduced live, not taken from a sibling report):

```
$ # official v4.2.6 PDF, read 2026-10-25
https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf
#### Version: 4.2.6
#### Approved date: 2026-October-14
#### Effective date: 2026-October-20
4.2.11 CNAs MUST assign different CVE IDs to different, Independently Fixable Vulnerabilities.
```

Corpus side: `cna-assignment-and-vulnerability-rules.md:14` says "The public document's
current version opened this round is 4.2.0"; `:30` quotes §4.2.11 as **SHOULD**;
`SOURCES.md:36` scopes S030 to "in version 4.2.0" and says "use current 4.2.0
requirements"; no v4.2.6 row or snapshot exists (`ls corpus/source-snapshots/round-23/` →
`S018.txt S029.txt S030.txt manifest.json`).

Why this is Q2 and not merely Q3/Q7: the claim's scope is *the current CNA counting rule on
2026-10-20*. The only tier-A row cited (S030) is scoped to v4.2.0, and v4.2.6 states
`Effective date: 2026-October-20` with §4.2.11 changed from SHOULD to **MUST**. A tier-A row
for the *historical* version cannot support a claim about the current version; the currency
sentence additionally rests on a search-log line (`SOURCES.md:53`), not on any registry row.
Consequence: the entry understates a mandatory current requirement as recommended — the
A5 failure mode Q2 exists to prevent.

Falsifier: produce a registry row whose scope cell names v4.2.6 with §4.2.11 as SHOULD, or a
v4.2.6 text stating SHOULD. Neither exists.

Smallest safe correction (no re-admission needed): add a new tier-A row S031 for
CNA Rules v4.2.6 (new row per R8, "supersedes S030 —"), pin its §4.2.11 MUST text in the
round-23/24 manifest, change `:14` to "4.2.0 (superseded 2026-10-20 by 4.2.6)" and replace
the `:30` row with the MUST quote. Leave the rest of F07 untouched; §3.1, §4.1.9, §4.1.10,
§4.1.11, §4.2.7, §4.2.12, §4.2.13 and §3.2.4.2 keep their numbering and wording in 4.2.6.

Scope limit on F1: readings are dated documents, not a live target. The v4.2.6 PDF is served
today (2026-10-25) and declares itself effective 2026-10-20; I cannot prove the byte was not
published hours *after* the F07 seat ran, but the declared effective date makes "4.2.0 is the
current version" false for any review performed on 2026-10-20.

### F2 — F06 provenance-cell defect (tier support unaffected)

`SOURCES.md:24` records S018 `opened` = **2026-10-19** (round 22), while round 23 admits F06
on 2026-10-20. The round-23 re-open is asserted only by the entry (`:21` "opened 2026-10-20")
and by the round-23 capture digest (`manifest.json`, S018 sha256
`d366bf40…27ab4`) — no registry cell records it. Under a registry-only reading of Q2's
"opened in the admitting round" clause, F06 fails that clause; under the reading that the
round-23 pinned capture is the open evidence, F06 passes. Falsifiable: `grep` the registry
for a 2026-10-20 open of S018 — it is absent. Smallest correction: record the r23 re-open
(a `reopened:`/`recheck` note on the row, or one sentence in QUALITY's Q2 interpretation
naming the manifest as the open evidence). This is a documentation fix; it does not change
tier support.

### F3 — F06 quote/claim mismatch (Q3, not Q2)

`:12-13` ("one vendor's patch date is not evidence that every downstream product has received
a fix") is pinned to the *Minimize exposure* line (`S018.txt`: "Vendors should be aware that
publication of fixes can disclose the presence of the same vulnerability in other vendors'
components."). That line entails downstream *exposure*, not downstream *patch receipt*. The
captured excerpt does contain a closer support — "Downstream vendors should consider updating
their components as soon as upstream vendors recommend a new release." — but the entry does
not pin or quote it, and `minimize-exposure` is the only manifest assertion for that idea.
Smallest correction: pin that sentence and cite it for the patch-date claim, or narrow the
claim to what the pinned quote says. Q2 scope is unaffected (S018's scope covers both).

### F4 — F07 cross-version claim is TRUE; its row bookkeeping is stale (R8/R2, not Q2)

`:17` "independently fixable guidance moved from 4.1.10 in 4.1.0 to 4.1.9 in 4.2.0" is
correct, reproduced from the official v4.1.0 PDF: `Version 4.1.0 / Effective May 14, 2025`,
`4.1.10 To help determine whether separate Vulnerabilities exist, CNAs SHOULD consider
whether the Vulnerabilities are <u>Independently Fixable</u>.` The 4.2.0 snapshot has the same
sentence at 4.1.9 (`S030.txt:165`) and 4.2.6 keeps it at 4.1.9. The pre-removal row is
S022, whose cell still reads `queued` with `used-by: —` (`SOURCES.md:28`) even though it is
now the support for a live claim; R8 asks that status/used-by changes be logged. Fix:
record S022's used-by/`superseded` state, or cite the round-23 v4.1.0 open in the entry.
No Q2 tier defect: S022 is spec/A and the claim was re-opened in round 23 (`SOURCES.md:53`
"Opened CNA 4.1.0 and 4.2.0").

### F5 — F08 unquoted load-bearing claims (Q3, not Q2)

The manifest pins six S029 quotes; the entry's quote table (`:43-50`) repeats those six. Three
load-bearing statements have no verbatim located quote at all: `:36-39` (Art 14(1)/(3) +
Art 16 platform), the `:32-33` incident-track clocks 14(4)(a) and 14(4)(b), and the Article 15
sentence at `:64-66`. The 14(4)(b) wording differs from the pinned vulnerability-track quote
("within 72 hours of the manufacturer becoming aware of the incident"), so the pinned
`art14-2b` assertion does not cover it. All of this is inside S029's scope cell, so Q2 still
passes; Q3 does not. Smallest correction: add `art14-1-3-platform`, `art14-4a`, `art14-4b`,
`art15-1` assertions to the manifest and rows to the entry table.

### Recheck replay (evidence that capture integrity is not the issue)

```
S018:sha256 OK … S018:minimize-exposure OK        exit=0
S029:sha256 OK … S029:art71-general-application OK exit=0
S030:sha256 OK … S030:rule-4-2-12-uncertainty OK   exit=0
```

### Durable external-evidence anchors (F1 and F4)

The two official PDFs F1/F4 rely on were downloaded again on 2026-10-25 to
`/tmp/kasegi-r23-q2tier/` (scratch; not cited as an evidence locus) and hashed. The digests,
not the scratch copies or any session artifact, are the reproducible anchor:

| document | bytes | sha256 | text check (`pdftotext` + grep) |
|---|---|---|---|
| CNA Rules v4.2.6 PDF | 271367 | `e296c9376cabcd09879f03920d99bb17e545a0e9c270d94478e45eda99677a22` | `Version: 4.2.6`, `Approved date: 2026-October-14`, `Effective date: 2026-October-20`, `4.2.11 CNAs MUST assign different CVE IDs…` |
| CNA Rules v4.1.0 PDF | 250107 | `9c55618efcc632b2b498e87ecf8eb9dcc2c724754b6bfacf5270f6b606b29cf0` | `Version 4.1.0`, `Effective May 14, 2025`, `4.1.10 … Independently Fixable`, `4.1.11 Interdependent conditions…` |

Reproduce F1: `curl -sSL -o /tmp/v426.pdf https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf && sha256sum /tmp/v426.pdf && pdftotext /tmp/v426.pdf - | grep -n "Effective date\|^4.2.11 "`.
A future reader comparing these numbers observes the same bytes I measured; no rebuilt file
stands in for them. This report deliberately does not quote its own sha256: the value changes
with every edit, so pin it at hand-off instead of trusting a number inside the file it hashes.

## 6. Verdict summary

| entry | Q2 verdict | basis |
|---|---|---|
| F06 | **PASS** (tier/scope), subject to F2 | S018 · docs/A; every claim inside its scope |
| F07 | **FAIL** | claims at `:14` and `:30` lack a tier-A row scoped to the current v4.2.6 text (F1) |
| F08 | **PASS** | S029 · spec/A, opened 2026-10-20; all claims inside Articles 14(1)-(4), 15, 16, 71 |

## 7. Scope limits

- I did not judge Q1, Q3–Q7 as criteria; F3/F5 are reported as residual observations for the
  owning seats, not as Q2 findings.
- C1 (`resolve.py` mirror containment, fixtures, receipts) was not exercised by this seat; the
  round-wide milestone mention does not move my target, and no C1 claim is adopted.
- Live reads were limited to the two public CVE Program PDFs (v4.2.6, v4.1.0) and the corpus
  capture; no auth, scanning, submission, or account operation.
- The v4.2.6/v4.1.0 reads are live as of 2026-10-25; the corpus pins no v4.2.6 bytes, so F1's
  correction requires a snapshot before it can be rechecked offline.
- No install or update was performed.
