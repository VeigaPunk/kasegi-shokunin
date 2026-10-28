# CritExemplarReal — fabrication audit of the r43 claim-package exemplar and its source

Seat `CritExemplarReal` (leaf critic), kasegi-shokunin round 43, wave 1. Axes:
`depth:verifiability`, `coverage`. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`,
freeze `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. Frozen claims read first
(`.ufo/waves/round-43/claims.json`), never edited. Receipt-only item: no deliverable,
no lane file outside this receipt and my scratch.

## Verdict

**Not a refusal of the C2 admit.** The captured document is genuine, and it is
reproducible on demand: two independent fetches of the claimed URL, 94 s apart,
returned raw-identical bytes whose normalized digest equals both the delivered
snapshot and the digest the manifest declares. Every quoted line in the exemplar is
an exact capture line at the line number the exemplar states. The publication date
is real and independently corroborated. The exemplar invents no program, no URL, no
amount, no date and no event, and it asserts no submission.

Two defects must be fixed **before landing** (F1, F5), and two framing constraints
apply to whatever text the round writes about this package (F3, F4). None of them is
a fabricated capture.

## Audited bytes (final state of the wave, 2026-10-28T16:53Z)

Paths below: `W=.ufo/waves/round-43/w1` (lane-relative); `$S` is my scratch
(`/fast/scratch/hyaku/kasegi-r43/CritExemplarReal`).

| file (in `.ufo/waves/round-43/w1/`) | lines | bytes | sha256 |
|---|---|---|---|
| `ExecExemplarPackage.report.md` | 88 | 3981 | `f99e2604eaafd0d2a9cac9ca04ff988d83a67ddf23d1b15340b689164a107144` |
| `ExecExemplarPackage.claim_checklist.md` | 41 | 2089 | `855eb392d404b141dc25fa7efe7e25225dd54b34bb1a8ab452b3cff2304568cc` |
| `ExecExemplarPackage.manifest.json` (lands at `evidence/manifest.json`) | 85 | 3327 | `5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834` |
| `ExecExemplarPackage.custodian-receipts.json` | 36 | 1577 | `db85653db9019d4db5ee3e45930daf2bacc3a4b8270de3c9ee1aa5172ab3ab2b` |
| `ExecExemplarPackage.provenance.json` | 95 | 3176 | `c52b75f5390802da9f4e27e2fedc5d071becf4925becca6d788ad4760c221dbf` |
| `ExecExemplarPackage.status.json` | 38 | 1007 | `60f06dfebc04e4198999d203f0568dc8b7bde1b3caf96399e135132edf38a9c6` |
| `ExecExemplarPackage.source-capture.txt` | 109 | 3822 | `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b` |
| `ExecExemplarPackage.source-excerpt.txt` | 13 | 549 | `9b81dd48db37b26303360334229c630f3e8ff32767b0ed68dd32a98e1d69e543` |
| `ExecExemplarPackage.solution-fixed-in.txt` | 6 | 308 | `8e3d1b43a01a06397fe6141bfc9321cf695679e40d7260664ec23abaa1c3fc8b` |
| `ExecExemplarPackage.disclosure-timeline.txt` | 7 | 489 | `8bececb6b37ba63f5c9fd32dd1b8b9f2cc08cb75ec443ffe81777ec6ed52bb8f` |

The four evidence digests above are the ones that matter for R-MANIFEST/R-REPORT.

The exemplar receipt `ExecExemplarPackage.md` (14 164 B, sha256
`55c28dbb65c6a1513e5b2082a6f452b4ecf27e72c65cbc11c805dcebbaf51f7d`) now carries these same digests: of the 14 distinct 64-hex tokens
it asserts, 11 equal a current `ExecExemplarPackage.*` file's digest and the other
three are the raw-HTML digest (`58ca9900…`), the custody head (`46b50b67…`) and the
gate's digest (`bdb50a82…`) — none of them claimed to be a wave-dir file. **No digest
drift remains between the receipt and the delivered bytes** (a first version of the
receipt, written before the 16:50:36Z rebuild, did drift; see the supersede record in F2).

## 1. Does the captured document at the claimed URL say what the manifest claims?

Claimed URL: `https://curl.se/docs/CVE-2025-9086.html` (manifest `sources[0].url`,
exemplar report line 4, checklist line 9).

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-28T16:51:53Z
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o raw9086.html \
    -w 'http=%{http_code} bytes=%{size_download} redirects=%{num_redirects}\n' \
    https://curl.se/docs/CVE-2025-9086.html
http=200 bytes=10455 redirects=0
$ sha256sum raw9086.html
58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd  raw9086.html
```

Normalization with the lane's own instrument functions
(`corpus/instruments/capture-source.py`, `html_to_text`, the `--kind html` path):

```
norm bytes 3822 lines 109 sha 7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b
```

Diff against the delivered capture:

```
$ diff -u .ufo/waves/round-43/w1/ExecExemplarPackage.source-capture.txt S9086.mine.txt
(no output)
BYTE-IDENTICAL
```

Second independent fetch twelve minutes apart:

```
2026-10-28T16:53:27Z  http=200 bytes=10455 redirects=0
58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd  raw9086b.html
58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd  raw9086.html
RAW-IDENTICAL-ACROSS-FETCHES
LANDED-EQUALS-MY-NORMALIZATION
```

The manifest's identity fields all match measured bytes: `sha256`
`7e35413a…` = sha256 of the delivered capture, `lines 109` = `wc -l`, and the raw
size 10455 B is the size I fetched twice. `ExecSourceCapture.manifest.json` declares
the same snapshot digest and its six quote anchors verify (below).

## 2. Do the quoted lines exist at the recorded line numbers?

Capture manifest, every quote checked for exact line equality and for uniqueness:

```
Q1 69  exact: True occ=1
Q2 82  exact: True occ=1
Q3 84  exact: True occ=1
Q4 88  exact: True occ=1
Q5 97  exact: True occ=1
Q6 103 exact: True occ=1
```

Exemplar report, every `> `-quoted line matched against the capture by exact string
equality:

```
exact=[82] :: CWE-125: Out-of-bounds Read
exact=[83] :: Severity: Low
exact=[84] :: Bug bounty: 505 USD
exact=[85] :: Area: cookies
exact=[86] :: Original report: https://hackerone.com/reports/3294999
exact=[87] :: AFFECTED VERSIONS
exact=[88] :: Affected versions: curl 8.13.0 to and including 8.15.0
exact=[89] :: Not affected versions: curl < 8.13.0 and >= 8.16.0
exact=[90] :: Not affected versions: curl >= 8.14.2 in the 8.14.X branch
exact=[91] :: Introduced-in: https://github.com/curl/curl/commit/1aea05a6c2699e80c7593
```

The report's caption says "from capture lines 82-91"; all ten lines are exactly those
lines, in order, with no line from outside the range. The three evidence artifacts are
verbatim slices (header stripped before comparison):

```
source-excerpt.txt      body==capture[82-91]:  True
solution-fixed-in.txt   body==capture[95-97]:  True
disclosure-timeline.txt body==capture[102-105]:True
```

Each artifact header also carries `# source: S067 (capture of https://curl.se/docs/CVE-2025-9086.html)`
and a `# capture_lines:` range that matches its body.

Other load-bearing statements in the report were checked against the capture line by
line: "does not affect the curl command line tool" (L94), "8.14.X branch fixed from
8.14.2" (L90), the crash/wrong-comparison impact and heap fragility (L74-L77, L80),
the attacker prerequisite "control of the http:// site … or … MITM capability" (L79),
the fix text and commit `c6ae07c6a541e0e96d0040afb6` (L96-L97), recommendation A
(L99) and C (L101), and the three timeline entries 2025-08-11 / 2025-09-05 /
2025-09-10 ~06:00 UTC plus "not aware of any active exploits" (L103-L105). No
statement required a source outside the capture.

## 3. Is the publication date real?

The advisory's own heading, capture L69, is
`Project curl Security Advisory, September 10 2025 Permalink`; the exemplar's
"Source URL: … (Project curl Security Advisory, September 10 2025)" restates it, and
its timeline's release entry is 2025-09-10.

Two independent first-party registries corroborate the date:

```
2026-10-28T16:52:10Z GET https://curl.se/docs/CVE-2025-9086.json -> http=200 bytes=2468
  {'id': 'CURL-CVE-2025-9086', 'published': '2025-09-10T08:00:00.00Z',
   'modified': '2026-10-24T23:17:46.00Z'}
  award {'amount': '505', 'currency': 'USD'}  severity Low  issue
  https://hackerone.com/reports/3294999

2026-10-28T16:53:34Z GET https://cveawg.mitre.org/api/cve/CVE-2025-9086 -> http=200 bytes=9234
  {'cveId': 'CVE-2025-9086', 'state': 'PUBLISHED', 'assignerShortName': 'curl',
   'datePublished': '2025-09-12T05:10:03.815Z', 'dateReserved': '2025-08-16T05:40:23.800Z'}
```

The vendor advisory date (2025-09-10) and the CVE record publication date
(2025-09-12) differ by two days, as expected for an embargo lift followed by record
publication; the exemplar claims only the vendor date, and that date is real. The
`Bug bounty: 505 USD` and `Severity: Low` figures asserted in the report's Impact
section are the vendor's own fields (L84, L83), corroborated by the JSON `award` and
`severity`.

## 4. Is the program/scope text actually in the document?

**No policy or scope text exists in the captured document.** Full term scan over the
delivered capture:

```
$ grep -n -i -e scope -e policy -e program -e bounty -e submit -e reward S9086.mine.txt
42:Vulnerability Disclosure Policy
84:Bug bounty: 505 USD
```

Line 42 is navigation link text with no URL in the normalized text; line 84 is the
award field. The only URLs in the capture are the HackerOne report (L86) and two
commit links (L91, L97). There is no program name, no program URL, no submission
form and no scope-policy sentence.

The exemplar does not pretend otherwise: its section is captioned
"Verbatim scope, severity and affected-version lines from capture lines 82-91", and
`claim_checklist.md` step 1 says the advisory "does not state the program's
submission-form URL, so the operator confirms the form address on the program page
before any other step". The word "scope" in the section therefore means the vendor's
affected-version/severity/award determination, not program scope. That is honest,
but it is a limit the round's prose must respect (F3).

## 5. Does the exemplar assert a submission that never happened?

No. Four independent guards, all present in the delivered bytes:

```
report.md line 88:            No submission performed.
claim_checklist.md line 4:    submitted nowhere, and no external effect has been performed.
status.json:                  "claimable": false, "state": "BLOCKED",
                              "no_submission_performed": true, "do_not_submit": true,
                              "verdict": "positive-blocked-operator-gated",
                              hard_gate no_duplicate_or_prior_submission = PENDING
provenance.json:              "external_effects_performed": []
```

`grep -n -i -e submitted -e 'submission"' -e 'claimable.*true'` over the six contract
files returns only those two honest lines and the PENDING gate; there is no
`submission_url`, no `SUBMITTED` state, no reward-claimed event. The award figure is
attributed to the vendor's record "for the original report" (report line 45), which
is the 2025 disclosure by Google Big Sleep (credits L107-L108); no authorship or
submission is claimed for this lane.

The reviewer identity `exemplar-reviewer` is a fixture role, and the package says so
in `provenance.identity_note` and in `claim_checklist.md`'s residual-gates section;
`claimable` is false. That is a disclosed fixture convention, not a claim that a
review happened.

## 6. Is the package internally verifiable, or only well-formed?

```
$ sha256sum ExecExemplarPackage.manifest.json
5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834
status.manifest_sha256==sha(manifest): True 5e296a37ad0bbc16 5e296a37ad0bbc16

manifest.expected_head: 46b50b6749186028  cust head: 46b50b6749186028
last decision:          46b50b6749186028
 seq 1 scope-triage       decision match: True
 seq 2 evidence-freeze    decision match: True
 seq 3 manifest-attest    decision match: True
```

Decision digests recompute from the file's own documented formula
`sha256(action|input_sha256|matched_grant_id|NO_SCOPE_OBJECTION)`; the head equals the
last decision and the manifest's `expected_head_sha256`. Manifest artifact digests
equal the delivered evidence bytes (gate detail `digest-bad=0`, and the checks in §1
and §2). `provenance.pin` is real:

```
$ git -C kasegi-shokunin remote -v      -> https://github.com/VeigaPunk/kasegi-shokunin.git
$ git -C kasegi-shokunin rev-parse HEAD -> 4cb6d4ae768481e1a14afbedc2d865a060ebacfd
```

Gate on the delivered bytes (assembled at the receipt's landing map, run with the
delivered gate `ExecGateCore.claim-package-check.py`, sha256 `bdb50a82…`):

```
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=pkg3/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

The gate proves form, not truth: its R-REPORT accepts any `Scope excerpt` heading,
any `https://` URL and any cited digest present in the manifest. The truth of the
excerpt and of the URL is what §1-§5 establish, and what a later reader must recheck
with the capture.

## Findings

**F1 — BLOCKING (integration): the second prose authority is stale and its record now
contradicts the tree.**
`ScribeExemplarReport.report.md` (4663 B, mtime 16:49:37Z) and
`ScribeExemplarReport.claim-checklist.md` were authored against the *superseded*
S067 capture (CVE-2023-38545): report line 1 is
`# libcurl SOCKS5 heap buffer overflow (CVE-2023-38545) — claim-package exemplar`, and
its "content sha256" is `9103704c…`. `ScribeExemplarReport.md` asserts
`327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b` for
`ExecSourceCapture.S067.txt`, but the delivered file is
`7e35413a…` / 109 lines / 3822 B. Mixing that prose with the current evidence is
caught by the gate, not by luck:

```
$ python3 "$W/ExecGateCore.claim-package-check.py" pkg4/exemplar > pkg4.out; echo rc=$?
rc=1
$ tail -2 pkg4.out
RULE R-REPORT verdict=fail detail=cited=2,unbound=2
package=pkg4/exemplar rules=8 pass=7 fail=1 verdict=DEFECT exit=1
```

Smallest safe correction: land **one** pair — the `ExecExemplarPackage.report.md` +
`ExecExemplarPackage.claim_checklist.md` pair that passes 8/8 — or have the scribe
regenerate both files against S067 = CVE-2025-9086. Never land
`ScribeExemplarReport.md` (its `sha256sum` output no longer describes the tree) and
never mix one prose file from each pair.

**F2 — INFO (supersede record): S067 changed identity mid-round.**
The seat `ExecSourceCapture` first captured `https://curl.se/docs/CVE-2023-38545.html`
at 16:39:59Z (delivered bytes then: 6446 B / 131 lines, sha256 `327bc909…`) and
re-captured S067 as `https://curl.se/docs/CVE-2025-9086.html` at 16:46:56Z. Both
captures were genuine — I re-fetched both URLs twice and each was byte-identical to
its delivered file, and the 2023 advisory's date was independently corroborated
(curl JSON `published 2023-10-11T08:00:00Z`; MITRE `datePublished 2023-10-18`). The
final wave is internally consistent on CVE-2025-9086: `ExecSourceCapture.S067.txt`,
its manifest/provenance, the R43 registry row, the exemplar, and the nine defect
fixtures all name CVE-2025-9086, and the capture receipt documents the supersede
(`ExecSourceCapture.md` L26-L36). Consequence: the round report, lesson, knowledge
entry and LOG must cite only the CVE-2025-9086 capture; any `327bc909…` or
`CVE-2023-38545` citation left in landed text is stale.

**F3 — FRAMING (must reach the knowledge entry/SCORECARD): S067 carries no policy or
scope text.** The exemplar's "Scope excerpt" is the vendor's severity/CWE/reward/
affected-range block, and both prose files say the program's submission form must be
confirmed by the operator. The round must not describe S067 as the program's scope
authority or as policy text; it is an advisory for one fixed finding.

**F4 — FRAMING: the vendor's live policy contradicts the captured reward line.**
I fetched the first-party policy page the advisory's navigation links
(`https://curl.se/dev/vuln-disclosure.html`, 2026-10-28T16:48:39Z, HTTP 200, 26 500 B,
normalized 221 lines, sha256 `9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102`,
`last-modified: Sun, 25 Oct 2026 10:45:03 GMT`). Its normalized line 43 reads:

```
There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.
```

That contradicts the advisory's own field `Bug bounty: 505 USD` (capture L84) if the
field is read as evidence of a bounty program. The exemplar only says the vendor
"records a Bug bounty: 505 USD for the original report", which is exactly what the
capture says and is therefore not a fabrication — but no round text may promote the
package into "a curl bug-bounty submission" or claim scope inclusion under a bounty
program. Note the limit: my policy read is my own live fetch, not a lane capture;
its bytes and date are recorded above so it can be rechecked.

**F5 — BLOCKING AT LANDING (layout): the manifest must land at
`exemplar/evidence/manifest.json`, not at the exemplar root.**
The wave-dir filename `ExecExemplarPackage.manifest.json` does not encode the target
basename. Landing the six contract files flat reds six rules:

```
$ python3 "$W/ExecGateCore.claim-package-check.py" pkgflat/exemplar > flat.out; echo rc=$?
rc=1
$ cat flat.out
RULE R-FILES verdict=fail detail=missing=1,bad=0
RULE R-MANIFEST verdict=fail detail=missing
RULE R-REDACT verdict=fail detail=missing
RULE R-CUSTODIAN verdict=fail detail=missing
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=fail detail=missing
RULE R-REPORT verdict=fail detail=missing
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=pkgflat/exemplar rules=8 pass=2 fail=6 verdict=DEFECT exit=1
```

With the receipt's landing map (manifest at `evidence/manifest.json`, the four
artifacts at `evidence/<manifest path>`) the same bytes pass 8/8 (§6). `status.json`
binds the manifest bytes, so the file must be byte-unchanged.

**F6 — MINOR (record fidelity, no fabrication).**
(a) The report's `## Disclosure timeline (vendor)` list includes the lane's own
`2026-10-28 advisory captured as S067 for this exemplar`; that is not a vendor event
and a reader can misread it as one. Smallest correction: move it after the list or
relabel the list "(vendor, then capture)".
(b) `provenance.commands` entries contain `(+3 header lines)` inside the command
text, so the recorded command is not executable as written; the artifact bytes are
correct, the record is a paraphrase.
(c) The reviewer identity is a fixture role (disclosed); the gate's
`reviewer=distinct` therefore proves distinctness of strings, not an independent
review. It is already named as a residual `OPERATOR-GATED` gate.

## Boundaries of this audit

- `corpus/knowledge/claim-package-gate.md` had not landed at 16:53Z, so its `source:
  S067` line and any quote it makes from the capture are **unaudited here**. The same
  applies to the round report, lesson and SCORECARD rows. When they land they must
  quote CVE-2025-9086 line numbers from the delivered capture, not the superseded one.
- `corpus/source-snapshots/round-43/S067.txt` and the `corpus/SOURCES.md` S067 row are
  not in the lane tree yet (verified: `ls corpus/source-snapshots/round-43/` →
  `No such file or directory`; `grep -c S067 corpus/SOURCES.md` → 0). The exemplar's
  evidence headers and the manifest note "byte-identical to the committed snapshot"
  therefore assert a path that does not exist until the L1 lands the capture. Against
  the wave-dir deliverable the identity is verified (§1). The registry row was
  audited from `ExecRegistryRows.rows.txt` after the reseat: 11 columns (NF=13),
  `S067`, status `mined`, `used-by corpus/knowledge/claim-package-gate.md`, capture
  digest `7e35413a…` / 109 lines / 3822 B, and anchors L69, L81, L82, L83, L84, L85,
  L88, L89-L90, L97, L99, L103, L104, L107-L108 — each verified as the capture line
  it names.
- I fetched `https://hackerone.com/reports/3294999` once (2026-10-28T16:55:39Z, HTTP
  200, 3829 B): the response is a JavaScript app shell with no report text, like
  `https://hackerone.com/curl` (200, 3614 B). Neither the capture nor the exemplar
  depends on second-party bytes; the HackerOne URL is quoted only as the vendor's own
  pointer (capture L86), and nothing in the package claims to have read that report.

## Network log (user agent `kasegi-shokunin/1.0`, `--max-time 90`, UTC)

| # | time | URL | status | bytes | note |
|---|---|---|---|---|---|
| 1 | 16:40:32Z | curl.se/docs/CVE-2023-38545.html | 200 | 13940 | superseded capture, sha `e9038f56…` |
| 2 | 16:40:55Z | curl.se/docs/CVE-2023-38545.json | 200 | 2473 | `published 2023-10-11T08:00:00Z` |
| 3 | 16:40:56Z | curl.se/changes.html | 200 | 1507175 | release page |
| 4 | 16:42:10Z | hackerone.com/curl | 200 | 3614 | JS shell only; no policy text |
| 5 | 16:42:11Z | curl.se/dev/vuln-disclosure.html | 200 | 26500 | live VDP (F4) |
| 6 | 16:43:00Z | cveawg.mitre.org/api/cve/CVE-2023-38545 | 200 | 6561 | `datePublished 2023-10-18` |
| 7 | 16:43:06Z | api.github.com/repos/curl/curl/commits/fb4415d8aee6c1 | 200 | 9226 | fix commit exists |
| 8 | 16:43:07Z | api.github.com/repos/curl/curl/commits/4a4b63daaa | 200 | 75930 | introduced commit exists |
| 9 | 16:48:39Z | curl.se/dev/vuln-disclosure.html (`-D`) | 200 | 26500 | `last-modified 2026-10-25 10:45:03` |
| 10 | 16:49:35Z | curl.se/docs/CVE-2023-38545.html | 200 | 13940 | raw-identical to #1 |
| 11 | 16:51:53Z | curl.se/docs/CVE-2025-9086.html | 200 | 10455 | final source, raw sha `58ca9900…` |
| 12 | 16:52:10Z | curl.se/docs/CVE-2025-9086.json | 200 | 2468 | `published 2025-09-10`, award 505 USD, Low |
| 13 | 16:53:27Z | curl.se/docs/CVE-2025-9086.html | 200 | 10455 | raw-identical to #11 |
| 14 | 16:53:34Z | cveawg.mitre.org/api/cve/CVE-2025-9086 | 200 | 9234 | `datePublished 2025-09-12` |
| 15 | 16:55:39Z | hackerone.com/reports/3294999 | 200 | 3829 | JS app shell, no report text |

## Tooling, writes, scratch

- Observed, not mine and not touched: `.ufo/waves/round-43/w1/__pycache__/` holds four
  `.pyc` files (13:44–13:50) created when sibling seats imported the rule modules from
  the wave dir. It must not land with the wave (`git status --porcelain` sees the whole
  `w1/` as one untracked entry, so the L1 must exclude it explicitly).
- Tooling: nothing installed or upgraded; no pacman, no `uv`, no `npx`; `~/.omp/agent/*`
  untouched.
- Writes: this receipt only, plus scratch. No lane file, no fleet-root file, no
  sibling lane, no PATH directory. No mutating git/jj command ran (read-only
  `remote -v`, `rev-parse`, `cat-file -t`).
- Scratch: `S=/fast/scratch/hyaku/kasegi-r43/CritExemplarReal` (mkdir -p), all fetches,
  normalizations, package assemblies and gate runs under `$S`; disk guard read before
  the pass (`/fast/scratch/hyaku` 25% used, ~605G free). `$S` removed after this
  receipt was written.
