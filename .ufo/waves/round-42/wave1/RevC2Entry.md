# RevC2Entry — pre-review: acceptance checklist for ScribeC2Entry's F25 entry (round 42, wave 1)

Seat: reviewer, receipt-only. No lane file edited; no mutating git/jj; no network. Scratch
`/fast/scratch/hyaku/kasegi-r42/RevC2Entry/` created, used for one throwaway script, removed.
Reviewed bytes: `corpus/knowledge/cyclonedx-analysis-subtree.md` (322 lines, S060, F23),
`corpus/knowledge/rfc-9116-security-txt.md` (53 lines, S063, F24), `corpus/QUALITY.md` Q1-Q10/R*,
`corpus/instruments/{frontier-recheck-count,recheck-audit,capture-binding-check,source-recheck}.py`,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, `claims.json` C2 predicate + kill rule.
Nothing here is a verdict on the entry (not yet filed); it is the bar the L1 can grade it against.

## 0. Calibration evidence (the exemplars pass the bar this checklist sets)

Throwaway script (`chk.py`, scratch, deleted) joined each capture's whitespace-collapsed lines,
then checked every blockquote `> "..." — S0xx.txt:L<n>` span (split on `" / "`, `\"` unescaped) for
(i) ≤25 words, (ii) exactly one occurrence, (iii) declared line inside the occurrence's line range:

| entry | quote spans | pass | fail | max words | what the fail is |
|---|---|---|---|---|---|
| cyclonedx-analysis-subtree.md vs round-40/S060.txt | 13 | 12 | 1 | 21 | the `Type: enum (of string) Default: "affected"` code span (L105), not a prose quote |
| rfc-9116-security-txt.md vs round-41/S063.txt | 19 | 18 | 1 | 25 | the second half of a `L249, L250` pair: span sits at capture L250-251, citation says L250 (line-of-first-word convention; benign) |

Lesson for the bar: a quote can wrap across capture lines (RFC text is hard-wrapped), so the
check must join lines before matching; a per-line `grep` falsely rejects 17/19 RFC quotes (first
run of the script: 2 ok, 17 bad — the bug was the checker, not the entry). ScribeC2Entry's receipt
must therefore state which matcher it used (QUALITY R3).

Structural facts measured on the exemplars: H1 on line 1; header lines at L3-L6; both exemplars
put `source:` first, `verified-at:` second, and `ground:`/`recheck:` in either order (F23 `ground`
then `recheck`; F24 `recheck` then `ground`); exactly one line starting `source:`; zero list
items beginning with an S-id; 14 / 8 `##` sections; F23 has 7 numbered rejected
over-generalizations (`1. **"..."**`), F24 carries its two inside Claim 7 plus the falsifiable rule.

## 1. The checklist (A-L). Each item has a command or a deterministic read; ✗ on any item = reject

### A. Provenance trio — exact keys, exact positions (QUALITY Q1, Q10; claim kill rule "lacking the provenance trio")

- A1. Line 1 is `# <title>` (H1); lines 3-6 are four header lines directly under it, blank line 2,
  blank line after. Keys are exactly (lower-case, colon, no variants): `source:`, `verified-at:`,
  `recheck:`, plus lane convention `ground: F25`. No `Source:`/`verified:`/`checked-at:`.
- A2. `source: S064 — <canonical https URL> — capture corpus/source-snapshots/round-42/S064.txt
  (<N> lines, <B> bytes; sha256 <64 hex>): <anchor list of what the capture holds with its line
  ranges>`. It begins `source: S064` (harness regex `^source:\s*(S\d{3,})`). The URL byte-equals the
  single `https://` token in S064's registry source cell and the manifest record's `url` (capture-binding
  rule B5). Numbers (lines, bytes, sha256) equal the manifest record and `wc -l`/`wc -c`/`sha256sum`
  of the committed capture — copied, not retyped (Q3).
- A3. `verified-at: 2026-10-28 (fetched <same UTC instant as manifest fetched_utc>, HTTP <status>,
  <raw bytes>; …)`: an ISO date the author re-opened it, ≥ the capture's fetch date, ≤ today, and
  the fetch facts equal the manifest `http`/`fetched_utc`/`fetched_bytes`. If the raw digest is not
  stable across fetches say so (F23 precedent), if it is stable say the second-fetch cmp result.
- A4. `recheck:` is ONE line that parses under `bash -n`, begins `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`
  (Q10; recheck-audit limb (d)), runs `python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-42/manifest.json --source S064` (limbs (e),(f)), and keeps its prose after
  a `#`. Fail-closed text names exit 2 (absent) / exit 1 (digest or moved quote), and states it is a
  pinned-capture comparison, not a fresh network check (Q7).
  **Trap — harness rule A reads the whole line, comment included:** `RECHECK_SOURCE = --source\s+(S\d{3,})`
  runs over the `#` note too, so a note that contains `--source S0xx` for any other id adds an undeclared
  selection (`selection-not-declared-by-entry`); a note containing the literal `--selftest` flips the
  line to `not-a-recheck-invocation`. The note must contain neither.
- A5. The recheck selects exactly `{S064}` and nothing else. The declared set is `source:` lines ∪
  list items that START with an S-id. **Trap — evidence-list regex:** `^(?:[-*]|\d+[.)])\s+(S\d{3,})\b`
  turns any list line like `- S055.txt:L12 …` or `1. S060 says …` into a declaration of S055/S060, and
  rule A (`header-sources-not-rechecked`) then fails the entry. Cross-references to other sources
  go inside a sentence or blockquote attribution (`— S060.txt:L7`), never at the start of a list item,
  and no second `source:` line.
- A6. `S064` is mentioned in the body outside the `source:`/`recheck:` lines (rule `selection-not-cited-by-entry`
  — the quote attributions satisfy this).
- Verify: `python3 corpus/instruments/frontier-recheck-count.py` → `PASS F25 ... ids=S064 exit=0`
  and `entries=28 pass=28 exit=0`; `recheck-audit.py --quiet` → `pass=61/61 … expected=61 missing=0
  unexpected=0 exit=0`.

### B. Anchored limbs (QUALITY Q2, Q3, Q9; frozen spec "3+ anchored limbs")

- B1. At least 5 `## Claim N —` limbs (exemplars: 7 and 7); floor from the seat spec is 3. Each limb has ≥1
  blockquote `> "<verbatim span>" — S064.txt:L<n>` (anchor in `S064.txt:L<n>` or `L<a>-L<b>` form — the
  form that does not trip anchorcheck's backtick `path:NN` matcher; if a backticked
  `corpus/source-snapshots/round-42/S064.txt:NN` form is used it must resolve IN-RANGE).
- B2. Every quoted span: verbatim, ≤25 words (Q3; the L1's own Gate rule), whitespace-collapsed
  exactly-once in the capture, and the declared line lies inside its occurrence (use the joining
  matcher in §0 — a per-line grep wrongly rejects wrapped quotes). Spans from the entry
  itself must be mechanically re-run in the receipt: print `quotes=N ok=N bad=0 maxwords=<≤25>`.
- B3. At least 3 limbs' quotes are the same spans pinned as manifest `Q1`-`Q4` (so
  `source-recheck.py` exercises them), each pinned quote ≥12 normalized chars, `anchor` present when the
  quote occurs >1 time. The entry's Q-ids are named in a count line so the recheck's `Q<n> OK` rows are
  explained (F23's header states the shape).
- B4. Numbers (enum sizes, counts, field names, versions) are counted, not remembered: each has a
  command (the F23 FC-3 pattern — a count script over named line ranges returning the printed number).
- B5. Normative verbs are measured, not asserted: the entry reports the capture's `MUST`/`SHALL`/`SHOULD`/`MAY`
  /`should` occurrence counts (`grep -oF`), and every conformance claim names its verb. A claim saying
  "requires" with a `should`-only source fails (the F23 Claim 3 / rejected #2 pattern).
- B6. Lane readings are labelled as such ("Lane reading, not a quote:") and never placed in a blockquote (Q4).
- B7. Every attributed rule is stated as the document's (Q4): "the OSV schema says" / "the CVE
  Record Format defines", never "vulnerability data must…". Self-reported/first-party labelled.

### C. Topic fit and no-overlap (claim kill rule: "chosen topic's document already covered")

- C1. States, with a command, that no lane row/entry covers the chosen document. Lane check I ran
  (read-only, 2026-10-28): `grep -rniE 'osv\.dev|OSV schema|CVE Record Format|cve-schema|CVE JSON 5|cveMetadata'
  corpus/knowledge corpus/SOURCES.md corpus/README.md PROVINCE.md corpus/source-snapshots/*/manifest.json`
  → **0 hits in all of them**; the only occurrences are in capture text `round-23/S031.txt` L102-L114 (CNA Rules
  4.5.5 "CVE Record Formatting", 5.2.3-5.2.5 "elements of the CVE Record Format") and passing CVE-Record
  phrases in `cwe-top25-2025-methodology.md:22` and `cisa-cvd-program-stages.md` (stage 4 "CVE Record
  Determination"). Sibling check: `grep -liE 'osv|CVE Record Format' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/*.md`
  → empty. So OSV or the CVE Record Format are both lane-new today.
- C2. **If the pick is the CVE Record Format**, the entry must draw its line against F07 (S031 CNA rules:
  they REQUIRE CNAs to submit in the format; they do not DEFINE it) with an explicit rejected
  over-generalization ("CNA rules define the record's fields"). **If OSV**, draw it against CVE/CVSS (F01/F07):
  OSV is an ecosystem/range-oriented record, not a CVE record and not a severity. Either way draw the
  line against F21 (CSAF) / F23 (CycloneDX) whose VEX vocabulary the lane already holds, instead of
  duplicating it. Cross-refs to existing entries are fine in prose.
- C3. F24 / RFC 9116 is PARKED: never cited as a candidate, never re-mined, never named as "the next
  topic". A passing mention of S063 in a comparison is legal for the harness but not needed and a
  needless risk: recommended zero mentions of F24 or S063 in the entry.
- C4. The entry's own frontier slot is exactly ONE entry path (the README row's `entry` cell has no comma): the
  harness counts entries, not rows (F09-F12 carry two each → 27 entries over 24 rows). A second entry file for F25 makes
  `entries=29`, breaking the frozen `entries=28 pass=28`.

### D. Rejected over-generalizations (Q5)

- D1. ≥3 numbered items (exemplar F23: 7), each in the form `N. **"<the tempting claim>"** Rejected: <reason with
  line cites and a measured count>`; the tempting claim is a plausible mis-reading of THIS document, not a strawman.
- D2. Each rejection is falsifiable against the capture (a line cite, a zero-count or a default value) — "Rejected: it is
  complicated" fails. At least one rejection must be of the scope-creep type ("the standard
  requires/defines X" when only `should`/absent, or "equals the CSAF/CVE/CVSS equivalent").
- D3. A `**Falsifiable rule.**` paragraph with lettered limbs (a)-(f) in the F23/F24 shape, each limb a
  claim that the capture refutes (Q5's first half), plus an `FC-n` check block with an executable test
  per limb (F23: FC-1..FC-7), each producing a number the reader can compare.

### E. Limits section (Q4, Q6; exemplars' `## Honest limit`)

- E1. A `## Honest limit` (or `## Falsifiable rule and honest limit`, the F24 merged form) section that states: (1) what the
  capture is — full document vs declared slice, its line count, whether the full page is committed;
  (2) edition/ratification/status is a different source unless the capture carries it (F23's "no
  edition line" disclosure); (3) the raw-vs-normalized digest relationship (stable or not);
  (4) no producer/vendor/tool practice is asserted — the page defines a format, not who emits it;
  (5) conformance level of the document type (Informational/specification/schema docs; whether verbs bind
  the format or a vendor); (6) normalizer artifacts (BOM/markup/line wraps) that shift anchors, if any.
- E2. The final bullet/sentence: "Documentation only: the capture is public reference text, no credential, session or private
  URL, and this entry quotes none." (Q6 wording used by both exemplars.)
- E3. The entry instructs NO probing, scanning, login or submission against any target (Q6); any
  "how a researcher uses it" step is reading/triage guidance on documents, not testing instructions.
  No `op://`-form vault reference, no token, no private URL.

### F. What-it-teaches section (the topic's researcher use)

- F1. A `## How a bounty or security researcher uses it` numbered list (exemplar F23: 7 items), each item
  tied to a limb by line cite, each phrased as read-this-field-and-do-not-conclude-that, not as an
  action against a live service. One item must say what the document does NOT let a reader conclude.
- F2. At least one comparison table or paragraph vs an existing lane source (F23 vs S055, S057; format
  differences as counted vocabularies), citing the other source as `S055.txt:L<n>` only after the
  citing line number is opened (never copied unverified — F23 re-opens L2151-L2152 etc.).

### G. Registry/README/PROVINCE/manifest consistency (all must be byte-consistent with the entry)

- G1. `corpus/README.md` F25 row grammar `| F25 | <topic> | admitted | knowledge/<slug>.md | S064 | <next> |`
  (6 cells; no literal `|` in any cell; entry path corpus-relative as F23/F24 use). Count: `grep -cE '^\| F[0-9]+ \|'
  corpus/README.md` 24 → 25.
- G2. The slug is lower-case kebab, descriptive of the document and the sub-aspect (F23 `cyclonedx-analysis-subtree`,
  F24 `rfc-9116-security-txt`); the file is `corpus/knowledge/<slug>.md`; the SOURCES row's `used-by` cell is
  exactly `corpus/knowledge/<slug>.md` (census E11 path-exists, W03 mined-unused).
- G3. S064 row: 11 cells (NF=13 in the census awk — a literal `|` inside a cell is E01); kind in
  `spec|docs|paper|code|tool|dataset|talk|book|community|own-work` (a JSON-schema/spec page: `spec` or
  `dataset`; never `community` at tier A, E10); tier A/B/C; status `mined`; opened `2026-10-28`
  (E08 not future); recheck a date, `NNd` or a symbolic cadence (E09; use `on-release` or `180d`, cadence-only
  cells — a human-note suffix is exactly what E09 rejected for S040/S041 in earlier rounds); source cell carries exactly
  ONE `https://` token (capture-binding rule B4) and it byte-equals manifest `url` (B5).
- G4. S065+ rejected rows: status `rejected`, `used-by` `—`, reason in `teaches` starting `REJECTED:` and containing `flip:`
  (S026/S027 grammar; census W02 needs ≥8 chars), a screened-doc URL that is DISTINCT from every other registry row's URL after
  census normalisation (scheme dropped, host lower-cased, fragment/trailing slash stripped) — a duplicate across scopes is a
  new `W04`, which the kill rule counts as a "new W/E code"; and it must NOT have a manifest record (capture-binding B3
  `rejected-row-anchor` fails the 56/56 count). A rejected row's `anchor` cell holds the located quote + access date.
- G5. `corpus/instruments/knowledge-expected.txt`: new `corpus/knowledge/<slug>.md` line inserted in sorted position
  (the file is sorted; round-41 `rfc-9116-security-txt.md` is at line 47 of 62, header 2 comment lines; 60 entries now → 61).
  Without it `recheck-audit.py` prints `unexpected=<slug>` and exits non-zero.
- G6. PROVINCE.md: one appended `[r42 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F25 — <topic> — admitted round 42;
  entry corpus/knowledge/<slug>.md (source S064)` line; pure addition (`diff … | grep -c '^<'` = 0; R6).
- G7. `corpus/source-snapshots/round-42/manifest.json`: `schema_version` 1; a `sources` record with `id` S064, `path` S064.txt,
  `url`, strict-UTC `fetched_utc` (`…Z` — round ≥32 has no archival exemption), `sha256` of the capture, `quotes[]` Q1..Qn
  (≥1; ≥3 recommended); `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-42/manifest.json
  --source S064` prints `S064:sha256 OK` then one `S064:Q<n> OK … occurrences=1 anchor=N-ok` per quote; binding
  `records=56 bound=56 unbound=0`; capture file path = `S064.txt` (stem = id, B1).

### H. Gate-block/lesson requirements that the entry text must not contradict

- H1. The lesson Gate block (written elsewhere) records the admitted source with URL, access date UTC, ≤25-word located quote,
  AND ≥1 screened reject with reason + flip + URL + date + ≤25-word located quote (closes D-r41-2); the entry's `verified-at`
  matches the Gate's access date.
- H2. The entry states nothing the Gate marks as a limit.

### I. Cross-checks the L1 will run (commands; every one must print the frozen value)

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                                   -> 25
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md           -> 64+R, R>=1
awk -F'|' '/^\|[[:space:]]*S064[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="mined") n++} END{print n+0}' corpus/SOURCES.md -> 1
grep -rlE '^source: S064' corpus/knowledge | wc -l                             -> 1
ls corpus/knowledge/*.md | wc -l                                               -> 61
python3 corpus/instruments/frontier-recheck-count.py                           -> entries=28 pass=28 exit=0, incl PASS F25
python3 corpus/instruments/capture-binding-check.py                            -> records=56 bound=56 unbound=0
python3 corpus/instruments/recheck-audit.py --quiet                            -> expected=61 missing=0 unexpected=0 exit=0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi -> exit 0, no W/E other than the two pre-existing W04 (S028, S029)
```

Baseline from `c2-controls/before.txt` and a live re-run of the first four pre-existing instruments in this seat
(2026-10-28): `frontier-recheck-count` → `PASS F24 … entries=27 pass=27 exit=0`; `recheck-audit --quiet` →
`lines=60 total=60 pass=60 … expect=present expected=60 missing=0 unexpected=0 exit=0`; knowledge 60; census exit 0.

### J. The "O4 junk-twin" class (claim kill rule: mined row without capture+entry+harness pass)

- J1. The entry must exist AND the row S064 must be `mined` AND the capture bound; a README F25 row marked `admitted`
  with an entry that fails any of A-G is an O4 junk twin. The entry's `recheck:` must actually execute (A4) — an entry whose
  recheck line passes the harness but whose manifest quotes are decorative (a 12-char quote of boilerplate) is a weaker twin;
  at least two pinned quotes must be topic-specific sentences, not headings.

### K. What the exemplars do that the bar should keep (quality bar, concrete)

- K1. Attribution paragraph opening: names whose document it is, whether the capture is the whole document or a slice,
  and what the capture's text type is (field documentation vs prose) so a reader does not read a field
  definition as a conformance rule (F23 `## Attribution`).
- K2. A table of counted vocabulary or fields when the document is enumerative, with a line cite per row.
- K3. A "No X is in the slice" paragraph for each tempting absent thing (edition, severity, VEX, issuance), each backed by a
  zero-count (`grep -oF | wc -l`) in the FC block.
- K4. Length: exemplars are 322 and 53 lines; there is no minimum but a thin entry (<40 lines of body, <3 claims) is the
  rejected-entry type QUALITY records.

### L. Reject triggers (any one = send back to ScribeC2Entry)

1. A header key misspelled/missing, `recheck:` not on one line, or its `cd` prefix absent (A1/A4).
2. `--source S0xx` (other than S064) or `--selftest` anywhere on the recheck line including its note (A4).
3. A list item beginning with an S-id other than via an in-sentence cite (A5) — makes harness rule A fail.
4. Any quote >25 words, not verbatim, non-unique without anchor, or on the wrong line (B2).
5. Only `MUST`-sounding claims from a source whose capture counts `should`/zero `MUST` (B5).
6. Fewer than 3 anchored limbs; fewer than 3 numbered rejected over-generalizations; no `Falsifiable rule`; no `Honest limit` (B1/D/E).
7. Two entry paths for F25, no `ground: F25`, or an entry slug not in `knowledge-expected.txt` (C4/G5).
8. F24/S063/RFC 9116 named as a candidate or re-mined (C3); any claim that the lane's S064 equals a CNA-rules (S031) statement
   without the F07 line drawn (C2).
9. Any probing/credential/private-URL content (E3).
10. Numbers retyped rather than copied from the manifest/`wc`/`sha256sum` (A2/B4) — the receipt must show the command and output.

## 2. Verification gaps (stated, not hidden)

- The entry is not yet on disk (`ls .ufo/waves/round-42/wave1` held only `swarm-registry.json` when I read it), and neither is the S064
  capture/manifest (`corpus/source-snapshots/round-42` absent), so no item could be checked against it; this is a pre-review.
- The census `symbolic()` set for recheck cells and the exact W02 length were read from `sources-census.sh` lines 600-690 only;
  the symbolic words list (`on-release` is used by S001) was not enumerated — use a cadence the registry already uses.
- The §0 matcher treats `"` / `\"` unescaping and `" / "` splitting; entries with other quoting styles (curly quotes inside
  quotes) need the matcher extended.
- I did not run `anchorcheck.py` over a candidate; B1's anchor form claim comes from reading the exemplars (neither uses
  backticked `corpus/...:NN` for capture lines) and the anchorcheck docstring.

## 3. Residual risk for C2

- The strongest kill-rule exposure is not the prose but the interplay: harness rule A (A4/A5 traps), capture-binding
  B3/B4/B5 (rejected row must not be in the manifest; one https token per mined row) and census W04 (distinct URL for S065).
  All three are cheap to test on a scratch mirror of the lane once ExecC2Rows/ScribeC2Entry land: copy `corpus` into scratch, apply
  deliverables, run the §1.I block. Recommended as the L1's single integration step.

Tools installed/updated: none.
Scratch: `/fast/scratch/hyaku/kasegi-r42/RevC2Entry/` removed (shutil/rm) before yield.
