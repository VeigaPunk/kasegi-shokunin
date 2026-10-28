# Round 43 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `ab98fac9dce87130bc4f66de89e30650d63943dc`; claims-freeze commit
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (`.ufo/waves/round-43/claims.json`, `frozen_at_utc`
`2026-10-28T16:37:07Z` by KasegiR43, digest
`a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630` recorded in
`.ufo/waves/round-43/freeze.txt`). Judged head J = the lane commit carrying every round-43 change except the
receipt (the lane never names it); verification ref Y = J + the receipt
`.ufo/waves/round-43/final-gates/all-gates.txt` only. Lane files never name J by hash (a commit cannot contain
its own hash); the report names J and Y. Counting commands run over the suite at Y; negative controls run at
base `ab98fac9dce87130bc4f66de89e30650d63943dc` and round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`. Shape: one v2 wave; wave 1 `kasegi-r43-hyaku` dispatched 73
seats (`w1-dispatch.json` `counts.spawn` 73: executor 23, reviewer 11, scribe 10, scout 9, critic 7,
mutation-tester 5, connector 2, sentinel 2, revenger 2, simplifier 2), so the round total is 73 unless a
further wave lands, which is counted from its own dispatch and never estimated.

Attack share: wave 1 `kasegi-r43-hyaku` 23/73 = 31.5% (reviewer 11 + critic 7 + mutation-tester 5, counted
from the `w1-spec.json` seat roles; `counts.spawn` 73).

## Frozen claims

Before → after, as frozen in `.ufo/waves/round-43/claims.json` (2026-10-28T16:37:07Z, KasegiR43).

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | `corpus/instruments/r43-closure.sh` absent — the base export cannot print `closed=19/19` (`c1-controls/do-nothing.txt` §A); the r42 suite, the do-nothing stand-in, run over the base export prints `closed=12/13 exit=1` (§B, J8 red only because the base carries commits after the r42 receipt), while all six routed defects sit in committed bytes and no check in the thirteen grades any of them: `SCORECARD.md:1634` `corrections=33` against the suite's own live `corrections=34`; `LOG.md:1804` `wave 2 kasegi-r42-falsify 36 seats dispatched` with no `.ufo/waves/round-42/wave2-results.json`; `corpus/lessons/round-42.md:11-16` repeating that dispatch and a round total of 100; its `## Wave-2 falsification` section at line 52 promising verdicts "when the round-42 falsify wave reports"; `corpus/lessons/round-42-verifier-spotcheck.md:65` and `.ufo/waves/round-42/claims-erratum-4.md:9` quoting `closed=10/13` with no committed transcript printing it; round-42 claims C1 `before` saying `closed=10/12` where its own control prints `closed=8/12` (§C) | `closed=19/19 exit=0` at Y; graded `selftest cases=19 failures=0` with nineteen `verdict=pass` lines; the base export `closed=13/19 exit=1` with exactly K14-K19 open; the round-41 head red; a plain run exit 2; `ref-not-found` distinct and exit 1; every K1-K13 replay limb still rejects its committed defeat; each K14-K19 mutant rejects; the receipt is one unedited tee of the run and the selftest at Y |
| C2 | coverage (8, held; capability row enters) | `corpus/instruments/claim-package-check.py` and `corpus/instruments/fixtures/claim-package/` absent at base; no instrument basename matches `claim`; registry 66 rows with S067 onward absent; knowledge 61 files, none citing S067; `capture-binding-check.py` `records=56 bound=56 unbound=0`; `recheck-audit.py --quiet` `expected=61`; `frontier-recheck-count.py` `entries=28 pass=28`; census exit 0 (`c2-controls/before.txt`) | `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` on the committed exemplar; nine defect fixtures each `verdict=DEFECT exit=1` with their own rule failing; `selftest cases=10 failures=0`, the degenerate always-pass control rejected; registry 66 → ≥68 with S067 `mined` and one screened reject S068; capture binding `records=57 bound=57 unbound=0`; knowledge 62 with the entry citing S067; `recheck-audit` `expected=62`; census exit 0; the capability row `claim-package-gate` enters `SCORECARD.md` with the gate command as its evidence pointer, `claimable` stays false and the operator gates are named in `claim_checklist.md` |

## Mistakes

One row per defect mined this round, all seven routed by the round-42 verifier spot-check
(`corpus/lessons/round-42-verifier-spotcheck.md` §9.6) and re-measured at base in
`.ufo/waves/round-43/c1-controls/do-nothing.txt` §C.

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| RD42-1 | stale counter (an append-only correction line quotes a superseded tally) | `SCORECARD.md:1634`, a `Correction (round 42)` line, states that "the r42 suite at Y prints `J11 payload=corrections=33,...`", while the suite at that same export and its own Y receipt print `corrections=34` — the correction line itself raised the count | `sed -n '1634p' SCORECARD.md`; `c1-controls/do-nothing.txt` `J11 payload=corrections=34,...`; route at `round-42-verifier-spotcheck.md:173`, which names `final-gates/all-gates.txt:16` as printing 34 | round-42 spot-check §9.6, re-measured in `c1-controls/do-nothing.txt` §C (`RD42-1`) | K14: every `corrections=<n>` literal in `SCORECARD.md`, `LOG.md` or `SHONEN.md` must equal the value the suite re-derives at the same export, or be named superseded by a committed `Correction (round 43)` line; the round appends that line (`wave1/ScribeCorrections.scorecard.txt`) rather than rewriting 1634 | K14 must print `closed=0` at base; a K14 that closes at base fails the frozen kill rule ("a check that cannot see its own defect is not repaired"); the base line is `<pending: integration>` |
| RD42-2 | never-true narrative (a log line reports a dispatch that never happened) | `LOG.md:1804` says "wave 2 `kasegi-r42-falsify` 36 seats dispatched against the repaired head; dead seats counted from `wave2-results.json` in the round report" — no dispatch marker, no results file, zero seats | `sed -n '1804p' LOG.md`; `c1-controls/do-nothing.txt` §C `RD42-2` prints `ls: cannot access '.ufo/waves/round-42/wave2-results.json': No such file or directory`; `.ufo/waves/round-42/` holds only `kasegi-r42-build-results.json`; route at `round-42-verifier-spotcheck.md:174` | round-42 spot-check §9.6, re-measured in `c1-controls/do-nothing.txt` §C (`RD42-2`) | K15: a sentence asserting a named `kasegi-rNN-*` wave was dispatched needs `.ufo/waves/round-NN/<wave>-results.json`, or must be named never-true by a `Correction (round 43)` line; the round appends that LOG correction (`wave1/ScribeCorrections.log.txt`) and states the executed round-42 wave as wave 1, 64 seats, round total 64 | K15 must print `closed=0` at base; base line `<pending: integration>` |
| RD42-3 | never-true narrative (the lesson repeats the unbacked dispatch and derives a round total from it) | `corpus/lessons/round-42.md:11-16` says "wave 2 dispatched 36 seats; the round total is 100" and "36 seats, 32 attack roles" for a wave that was handed off, not taken | `sed -n '9,17p' corpus/lessons/round-42.md`; `c1-controls/do-nothing.txt` §C `RD42-3` prints `wave 2 dispatched 36 seats; the round total is 100`; route at `round-42-verifier-spotcheck.md:175` | round-42 spot-check §9.6, re-measured in `c1-controls/do-nothing.txt` §C (`RD42-3`) | K15, the same check that grades the LOG sentence; the round appends a `Correction (round 43)` naming both lesson lines superseded as never-true, with the round-42 total 64 (`wave1/ScribeCorrections.lesson42.txt`) | K15 must print `closed=0` at base; base line `<pending: integration>` |
| RD42-4 | placeholder promise (a committed record promises a section's content for a wave that never reported) | `corpus/lessons/round-42.md:52` opens `## Wave-2 falsification` and states that per-claim verdicts, attack tallies and per-family replay status are "Appended when the round-42 falsify wave reports"; no round-42 falsify report exists, so the section carries a promise and no verdict | `sed -n '50,57p' corpus/lessons/round-42.md`; `c1-controls/do-nothing.txt` §C `RD42-4` prints `## Wave-2 falsification`; route at `round-42-verifier-spotcheck.md:176` | round-42 spot-check §9.6, re-measured in `c1-controls/do-nothing.txt` §C (`RD42-4`) | K16: the promise must be named unfulfilled by a committed `Correction (round 43)` line (the round-42 lesson is append-only; the placeholder itself is not rewritten), which the same lesson-42 correction supplies | K16 must print `closed=0` at base; base line `<pending: integration>` |
| RD42-5 | receipt granularity (a quoted counter appears in no committed transcript) | `corpus/lessons/round-42-verifier-spotcheck.md:65` and `.ufo/waves/round-42/claims-erratum-4.md:9` quote `closed=10/13 exit=1` and `failures=3` at `de09313`; the committed red transcript is `final-gates/all-gates.pre-repair.txt` at `d238e36` and prints `closed=9/13 exit=1`, `failures=4` | `grep -rn 'closed=10/13' .ufo/waves/round-42/final-gates/` prints nothing, while `all-gates.pre-repair.txt:19` prints `closed=9/13 exit=1` and `all-gates.txt:19` prints `closed=13/13 exit=0`; `c1-controls/do-nothing.txt` §C `RD42-5` lists the three final-gates files; route at `round-42-verifier-spotcheck.md:64` and `:177` | round-42 spot-check §9.6, re-measured in `c1-controls/do-nothing.txt` §C (`RD42-5`) | K18: every `closed=` or `selftest cases=` value quoted in a round-42/43 lane record must appear in a committed transcript under the round's `final-gates/` or `c1-controls/`, or its line must carry `report-only`, or it must be named superseded by a `Correction (round 43)` or claims-erratum line | K18 must print `closed=0` at base; base line `<pending: integration>` |
| RD42-6 | timestamp hygiene (the freeze label postdates the file that carries it) | round-42 `claims.json` records `frozen_at_utc=2026-10-28T12:05:00Z`; the containing commit `0566bd6` is dated 11:00:01Z and the file's own mtime is 10:51:52Z, so the label is 65 minutes future-dated | `.ufo/waves/round-42/claims-erratum-3.md:3` records the mtime `2026-10-28 07:51:52.149991752 -0300` (10:51:52Z); `c1-controls/do-nothing.txt` §C `RD42-6` prints `2026-10-28T12:05:00Z` and `2026-10-28T08:00:01-03:00`; route at `round-42-verifier-spotcheck.md:178` and `:38` | round-42 spot-check §9.6, re-measured in `c1-controls/do-nothing.txt` §C (`RD42-6`) | K19: the round-43 freeze record's `frozen-at` must be an `<iso-z>` instant not earlier than the latest `measured-at=` over the two committed control receipts, and both receipts must carry that line; the record is `.ufo/waves/round-43/freeze.txt` in the four-line format fixed by `wave1/ExecK19Freeze.freeze-format.txt` | K19 must print `closed=0` at base, where no round-43 freeze record exists; base line `<pending: integration>` |
| RD42-8 | before/control mismatch (a frozen before-cell quotes a number its own cited control contradicts) | round-42 `claims.json` C1 `before` says "the r41 suite at base prints `closed=10/12 exit=1`", but the pointer it cites, `.ufo/waves/round-42/c1-controls/do-nothing.txt`, prints `closed=8/12 exit=1`; 10/12 is the r41 suite's count at its own head, not at base | `sed -n '16p' .ufo/waves/round-42/c1-controls/do-nothing.txt` prints `closed=8/12 exit=1`; the round-42 claims C1 `before` string; `c1-controls/do-nothing.txt` §C `RD42-8` prints both the sentence and `closed=8/12 exit=1`; route at `round-42-verifier-spotcheck.md:297-303` | round-42 spot-check §9.6 (`:297`), re-measured in `c1-controls/do-nothing.txt` §C (`RD42-8`) | K17: every `closed=` or `failures=` literal in a claims `before`/`after` cell must appear in the control receipt that cell cites, or be named superseded by a committed claims erratum; `wave1/ScribeClaimsErratum.claims-erratum-1.md` names `closed=10/12` superseded by `closed=8/12` without re-freezing the claim | K17 must print `closed=0` at base; base line `<pending: integration>` |

## Census

Before (`.ufo/waves/round-43/census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0.
After (`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi`): `<pending: integration at Y>`. The same command run at the freeze
commit `4cb6d4a`, before the C2 rows append, prints the before value again — `W04 S028`, `W04 S029`, `ok`,
exit 0 — so that run is not the after measurement; the after is re-read at Y after S067 and S068 land.

## Gate

### Admitted — S067 / curl security advisory CVE-2025-9086

- **Lead screen (2026-10-28, six candidates).** Six public documents were identified and screened, one
  included and five excluded (`wave1/ScoutSourceHunt.md`, "Other screened candidates" and its scope note):
  ZDI-26-811 (no fix commit and no scope or reward sentence), OSV-2025-17 (no scope or reward sentence, and
  adjacent to the rejected S065), GHSA-v676-f8gm-92r9 (the designated S068 reject), HackerOne 3294999 (the
  page does not contain the report), and an Intigriti page that is a program policy naming live hosts.
  Supporting fetches that are not candidates: the curl JSON sibling (2468 B — it, not the HTML, carries the
  full 40-character fix hash), the project's `dev/vuln-disclosure.html` policy (26500 B), the guessed
  `/docs/vuln-disclosure.html` (HTTP 404, 8017 B) and the ZDI index (2551868 B) used only to confirm the
  advisory URL. Sibling ground: no lane owns a claim-package gate or a six-file contract checker — the hit
  lanes (kotoba `claim-gates` citations, kagi and kotodama `custodian`, kaidoku `redactions`) cite or use
  the vocabulary without owning the gate (`wave1/ScoutSiblingOverlap.md`), so this is adjacency, not
  overlap.
- **Row.** S067, kind `docs`, tier A, status `mined`, opened 2026-10-28, recheck `annual`,
  `used-by corpus/knowledge/claim-package-gate.md`; row deliverable `wave1/ExecRegistryRows.rows.txt`, whose
  anchor cell names the advisory heading L69, the CVE assignment L81, the CWE-125 class L82,
  `Severity: Low` L83, the award figure L84, the area L85, the affected range L88 with two not-affected rows
  L89-L90, the fixed-in solution L97, the upgrade recommendation L99, the timeline L103, the release line
  L104 and the credit L107-L108. The frozen counter requires the registry at ≥68 rows from 66 (`grep -cE`
  over `corpus/SOURCES.md`; 66 measured at the freeze commit).
- **Source / capture.** `https://curl.se/docs/CVE-2025-9086.html`; access 2026-10-28 (capture fetch
  2026-10-28T16:46:34Z, scout fetch 2026-10-28T16:40:33Z: HTTP 200, zero redirects, 10455 raw bytes, raw
  sha256 `58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd`). Capture
  `corpus/source-snapshots/round-43/S067.txt` is the complete document, no slice — navigation chrome
  L1-L66, advisory body L67-L109 — 109 lines, 3822 B, sha256
  `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`, normalized by
  `corpus/instruments/capture-source.py --kind html` (deliverable `wave1/ExecSourceCapture.S067.txt`);
  `source-recheck.py --source S067` prints `S067:sha256 OK` and `Q1..Q6 OK occurrences=1 anchor=<n>-ok`.
- **Quotes (≤25 words, located in the capture).** L69 (8 words): "Project curl Security Advisory, September
  10 2025 Permalink" — the advisory is the project's own, dated. L82 (3 words): "CWE-125: Out-of-bounds
  Read", with L83 (2 words): "Severity: Low" — class and severity as the project states them. L88 (8 words):
  "Affected versions: curl 8.13.0 to and including 8.15.0", with L89 (9 words): "Not affected versions:
  curl < 8.13.0 and >= 8.16.0". L97 (2 words): "Fixed-in:
  https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6" — the fix pointer, a 29-character prefix
  in the HTML. L103 (19 words): "This issue was reported to the curl project on August 11, 2025. We
  contacted distros@openwall on September 5, 2025." — the disclosure timeline.
- **Entry.** `corpus/knowledge/claim-package-gate.md` (source S067, `verified-at: 2026-10-28`, one executable
  `recheck:` that re-runs the gate selftest and fails closed); it separates what the gate decides — the
  eight rules, one located contract quote each — from what it does not: the lost `ops/claim-check.mjs`
  parity and the operator gates (submission, prior-submission, reviewer distinctness). Deliverable
  `<pending: ScribeKnowledgeGate>`.
- **Limit.** The capture is the advisory page, not a program policy: the word scope does not occur on it and
  it carries no reward ladder — the `Bug bounty: 505 USD` line (L84) is one award on this advisory, and the
  project's own disclosure page states it never offers rewards, so a package may cite the award but must not
  present it as policy. The fix pointer is a 29-character prefix; the full 40-character hash exists only in
  the JSON sibling, which was not spliced into the capture. The page states the attacker needs the `http://`
  host or MITM capability (L79), that the out-of-bounds read depends on heap contents (L80), and that the
  curl tool is not affected (L94), so an exemplar can reproduce the reasoning and the version bound, never a
  demonstration. The HTML can be re-rendered and the sibling's `modified` timestamp moves independently, so
  the pin is the captured byte digest, not fetch success.

### Rejected — S068

- **S068 (GitHub Advisory Database GHSA-v676-f8gm-92r9 for CVE-2025-9086)** —
  `https://github.com/advisories/GHSA-v676-f8gm-92r9`; access 2026-10-28 (fetched 2026-10-28T16:46:43Z by
  the registry seat and 2026-10-28T16:41:46Z by the source hunt; this seat's own check at
  2026-10-28T16:48:33Z: HTTP 200, zero redirects, 141794 raw bytes — the raw body is not byte-stable,
  141794-141796 bytes across three fetches, so the pin is the normalized text: 191 lines, sha256
  `530cbcf9925b082f9effea7bbc5e96650949794d80893d7ac8ec5e289b4c97e6`, byte-identical on every
  normalization). Located quotes in that text: L64 and L68 "Unreviewed" (1 word); L67 "High severity" (2
  words) against the vendor's `Low`; L75 "No package listed" (3 words, the line continues with an em dash);
  L78 and L80 "Unknown" (1 word each) for affected and patched versions; L105 "Published by the National
  Vulnerability Database"; L170 "No known source code". REJECTED: screened out on primary-of-record and
  record completeness — the entry republishes NVD's record of the CVE that S067 captures from the project,
  self-labelled Unreviewed, with no package, both version cells Unknown and no known source code, so it
  carries neither the affected range nor the fix a package's report and manifest must bind; it also grades
  the issue High (7.5) where the vendor grades it Low. Flip: re-open only if the entry becomes Reviewed and
  names the curl package with per-version affected and patched ranges or the fixing commit
  `c6ae07c6a541e0e96d0040afb62b45dd37711300`, at which point it stops being a derived mirror.
- Screened and dropped without a row (grounded in `wave1/ScoutSourceHunt.md`): ZDI-26-811 (no fix commit, no
  scope or reward sentence), OSV-2025-17 (no scope or reward sentence, adjacent to the rejected S065),
  HackerOne 3294999 (the page does not contain the report) and an Intigriti program policy that names live
  hosts.

## considerthese 2026-10-26 dispositions

R31 (`corpus/QUALITY.md:278`) wants each touched proposal disposed old → new in the round lesson and in
`corpus/knowledge/considerthese-proposals-ledger.md`. The ONE proposal this round mines is proposal 2's
claim-checker remainder: "Rebuild a minimal claim checker under `corpus/instruments/`, since the `ops/*`
executables are gone." (`considerthese/2026-10-26.md:30`, 15 words). Before: the ledger's Round-41
dispositions row 2 reads "partially landed r40 — remainder open (unchanged)", and no instrument basename
matches `claim` (`ls corpus/instruments/` filtered for `claim` at the freeze commit: 0 matches). After:
`<pending: integration>` — the round's frozen C2 deliverable is `corpus/instruments/claim-package-check.py`,
the eight-rule gate with the exemplar and nine defect fixtures, and when the C2 receipt prints
`rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` and `selftest cases=10 failures=0` at Y the row's status
is `landed (r43)` with the remainder named open: the lost `ops/claim-check.mjs` parity and the three
operator gates (submission, prior-submission, reviewer distinctness) that keep `claimable: false`. Landed
pointer: `corpus/instruments/claim-package-check.py` plus `corpus/knowledge/claim-package-gate.md`; the
ledger section the round appends is `## Round-42 dispositions` — 7 of 7 proposals rowed at the round-43 base
(deliverable `wave1/ScoutConsiderthese.txt`, an end-of-file append with every section above unedited), and
the round-43 disposition of proposal 2 is the lesson half recorded here, its ledger row
`<pending: ScoutConsiderthese>`. No other proposal is touched: 3, 5 and 7 stay landed; 4 and 6 stay
operator-owned.

## Assimilation

§10 id-collision rerun, read-only against `/home/vgpnk/Projects/shokuknow` with the 0–3-leading-space
extractor (`wave1/ScoutAssimilation.md`): lane ids 66 (`S001`–`S066`), staged ids 94 (`S031`–`S124`),
`comm -12` = 36 collisions (`S031`–`S066`); of those, 35 source cells name different documents and `S042`
names the same one. Guard proof on a scratch registry with an indented `  | S002 |` row: the column-zero
extractor reports 0 collisions while the 0–3-space extractor reports `S002` with `GUARD_NONEMPTY=yes`, and
the census over that fixture prints `rows=2`, exit 0, so the indented form is parsed and the guard can fail.
The staged package (`MERGE-REPORT.md` sha256 `0e6759b47595f1bce5fbf49bf0422838ff89a394b2f424d17fb17d96a09106df`,
`SOURCES.append.md` sha256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`) is not
adopted: **Assimilation: none** — no renumber map, no registry append, no knowledge copy, because no staged
theme serves a frozen claim and the staged `S067` (Microsoft MSRC pentest rules of engagement) is a
different document from the lane `S067` this round mints. The collision list stands as a refusal input, not
a map; the round's C2 source is a §2b row minted this round, never a staged-package adoption. Verdict:
**none adopted, 0 adoptable, no renumber map filed.**
