# EntryRoE — F09 draft: the rules-of-engagement document (S032, NIST SP 800-115)

Seat: scribe (writer, private clone). Item target: `corpus/knowledge/authorised-testing-rules-of-engagement.md`.
Clone: `/tmp/kasegi-r24-EntryRoE`, made with
`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kasegi-shokunin /tmp/kasegi-r24-EntryRoE`,
then `git reset --hard d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` (`git rev-parse HEAD` printed that id).
No commit, no push, no jj, no other file in the clone touched (`git status --porcelain` →
`?? corpus/knowledge/authorised-testing-rules-of-engagement.md`, one line).

## Findings first

1. **The draft exists and is structurally complete.** `/tmp/kasegi-r24-EntryRoE/corpus/knowledge/authorised-testing-rules-of-engagement.md`
   — 11 985 B, 146 lines, sha256 `afec2ef97cb999fb107c1ee11be7ee4852100e790e377da2bb66561c78e74653`.
   H1, then `source:` / `verified-at: 2026-10-25` / `recheck:` on lines 2–4, then
   `## Rule`, `## Falsifiable checks against a claim package`, `## Evidence`,
   `## What this entry adds beyond F03`, `## Rejected`, `## Limits`. Exactly one `recheck:` line.
2. **The primary is re-grounded from bytes fetched this round, not from the package entry.**
   `curl -sS -o sp800-115.pdf -w 'http=%{http_code} bytes=%{size_download} type=%{content_type}\n'
   https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` →
   `http=200 bytes=544047 type=application/pdf`;
   `sha256sum` → `58e5ed41e5c8ca34ce14fd80b70f118f2c6d613d1647bc307edca30bcc45f063`;
   `pdfinfo` → `Pages: 80`, `CreationDate: Mon Sep 29 14:09:24 2008`, `ModDate: Fri Nov 21 17:31:06 2025`,
   `File size: 544047 bytes`. Bytes live in `/tmp/roe-capture/`.
3. **Every source quote in the draft is exactly-once under the rechecker's `normalize()` against a
   flowed `pdftotext -enc UTF-8` extraction** — the rendering the round-24 capture will use. Audit
   over all 24 quoted spans of ≥5 words: `problems: none`, `max words: 17`. The four sub-5-word
   spans (`defined activities`, `a starting point`, `illustrative`, `specific permission to
   deviate`) are also present in the source. Method and output in §Verification.
4. **The `recheck:` line is executable and was exercised end-to-end on a fixture manifest**, with
   both a positive and a missing-source control: clean → exit 0 with `S032:sha256 OK` plus 11
   assertion lines; corrupt capture → exit 1; one wrong quote → exit 1; absent manifest → exit 2;
   `--source S999` → exit 2 `not-listed`. Receipts in §Verification §(c).
5. **CONFLICT — the source id.** The integration owner instructed S032; the executor's registry
   append carries S124; the frozen claim's counter B greps `S1xx`. All three verbatim:
   - parent (`L1Kasegi24`, IRC, 2026-10-25): "Lane id for NIST SP 800-115 is **S032**, not S124:
     the staged S031 collides with the lane's own S031 (CNA 4.2.6) and nothing keeps the package
     numbering; ids follow the document, append-only from the lane's S031."
   - `/tmp/kasegi-r24-SOURCESRows/corpus/SOURCES.md:41` (executor clone, uncommitted):
     `| S124 | NIST Special Publication 800-115, … |`
   - `.ufo/waves/round-24/claims.json` C2 `counter.command_B`:
     `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l`, `after_target_B: 2`.
   Arithmetic: package staged `S123` + one-column shift = lane `S124`; the parent's "append-only
   from the lane's S031" rule applied to the same row also yields `S124` (94 adopted rows,
   `S031`→`S032` … `S123`→`S124`). `S032` yields `124 − 32 = 92` for the same row and collides
   with the statute rows the executor numbered `S040`/`S041`/`S042`. With `source: S032`, C2
   counter B greps **0** entries, so the frozen `after_target_B: 2` cannot be met by either F09
   entry as filed. I followed the integration owner's ruling in the draft (S032) because the
   committed manifest is confirmed to carry that id; this conflict is recorded, not resolved, by
   this seat.
6. **What the draft deliberately does not claim** (parent's IRC constraint, independently confirmed
   in the extraction): Appendix B contains no authorisation letter, no escalation ladder and no
   evidence-handling/chain-of-custody content. `grep -ci` over PDF sheets 67–69 of
   `/tmp/roe-capture/sp800-115.txt`: `letter` 0, `permission` 0, `escalat` 0, `evidence` 0.
   §7 is a Signature Page recording that signatories understand scope and boundaries; §6.5 places
   acknowledgement on the assessment plan; §3.2 is incident handling; §5.3 is test-data handling.
   The draft says exactly that and rejects the over-reading.

## Gates — QUALITY Q1–Q8 against the draft

| id | verdict | evidence in the draft |
|---|---|---|
| Q1 | PASS | Line 2 `source: S032 — <URL> — NIST SP 800-115, September 2008: Appendix B …, printed pages B-1 to B-3, and the glossary entry …, printed page F-2` (row id + URL + exact anchor); line 3 `verified-at: 2026-10-25`; line 4 a runnable command with a fail-closed negative control (absent manifest → exit 2 → line fails; measured). |
| Q2 | PASS | Every load-bearing claim rests on S032, a tier-A `spec` row opened 2026-10-25 (`corpus/SOURCES.md` schema; row currently `| S124 | … | spec | A |` in the executor clone, or `S032` per the parent's ruling — same document, same opening). No tier-C row is used at all. |
| Q3 | PASS | 15-row Evidence table, each row `location + ≤25-word verbatim quote` with NIST's printed folio and PDF sheet (`F-2 [sheet 77]`, `1-2 [sheet 11]`, `B-1 [sheet 67]`, `B-2 [sheet 68]`, `B-3 [sheet 69]`, `6-11`, `7-2 [sheet 56]`, `6-12 [sheet 53]`). Numbers are copied from `pdfinfo`, not recalled. |
| Q4 | PASS | "NIST's name for it", "It is NIST's assessment methodology, not a statute", footnote 42 quoted as the attribution limit, and three separate Rejected entries keep the template, the legal question and Appendix B's contents attributed. |
| Q5 | PASS | Four falsifiable checks a reader can run on a claim package (prior-instrument, defined-activity, exclude-list, acknowledgment) and four rejected over-generalisations, each with its reason and quote. |
| Q6 | PASS | "It authorises nothing, and it does not instruct anyone to probe, scan, log in to, or submit against any target." No credential, session, private URL or op-scheme URI. All four checks are reads of the package and its cited documents. |
| Q7 | PASS (conditional on the committed capture) | The recheck is a command, not prose; its output names what was checked (`S032:sha256 OK` + per-quote lines) and the Limits section states containment ≠ currency. A missing/corrupt-source control is in the line itself (`--source S999` must exit 2) and both failure modes were measured (exit 1 digest, exit 1 quote, exit 2 absent manifest). **Condition:** the round-24 manifest must list `S032`; until L1's capture lands the line exits 2 `not-listed`, exactly the F01–F05 defect. |
| Q8 | PASS | Line-spanning assertions are disclosed in Limits as printing `normalized=markup-whitespace`; single-line assertions print `OK`. The audit accepts both (it uses the same `normalize()`). |

F03 cross-reference (as the item requires): the draft does not restate F03. It names F03's holdings
(safe-harbor statements, asset scope, grant, prohibited methods, badge ≠ added assets), states that
F03 holds no engagement document — no ROE definition, no prior-in-time rule, no exclude list, no
deviation rule, no signature element — and assigns the split: F03 answers *which assets a programme
authorised*, this entry answers *whether a defining document exists and whether the activity falls
inside it*.

## Verification — commands and outputs

### (a) Quote audit (flowed rendering, the capture's rendering)

```
pdftotext -enc UTF-8 /tmp/roe-capture/sp800-115.pdf /tmp/roe-capture/sp800-115-flow.txt   # 250 971 B, sha256 4bd09f788d00ed5eec8ac4bfefa2e8f4088e296da6ae1808ceeae0220237fcd6
python3 - <<'EOF'  # extract every “…” span from the draft; count under normalize()
…
EOF
quoted spans >=5 words: 24
problems: none
max words: 17
all short spans: ['Rules of Engagement Template', 'Rules of Engagement (ROE)', 'defined activities',
 'a starting\npoint', 'illustrative', 'defined activities', 'specific permission to deviate', 'the 2008 file']
```

Also checked against the `-layout` rendering: all 15 Evidence quotes are exactly once under
`normalize()`, and 5 of them are line-spanning there and so depend on that branch —
the glossary definition, `Areas to which the test team will not be given access…`,
`By signing the assessment plan…`, the signature clause, and
`it is recommended that they always be involved…` — matching the disclosure in Limits.

### (b) Folio derivation (one example each)

`pdftotext -layout` page split on `\f`; folio = last non-empty line of the segment.
Glossary ROE entry → segment 77, folio `F-2`; Appendix B → segments 67–69, folios `B-1`…`B-3`;
`§1.4` → segment 11, folio `1-2`; `§7.2` → segment 56, folio `7-2`; `§6.5` → segment 52, folio
`6-11`; `§6.6` → segment 53, folio `6-12`.

### (c) Recheck line, exercised on a fixture manifest

Fixture: `/tmp/roe-fixture/S032.txt` = 5-line provenance header + the flowed extraction;
`sha256` `410162f5d83b5f040623b13e1e47c9674508bc9a063c629afd0a30cbb2d49754`;
`manifest.json` lists S032 with the 11 assertions below. Instrument is the committed one at lane HEAD.

```
python3 corpus/instruments/source-recheck.py --manifest /tmp/roe-fixture/manifest.json --source S032
S032:sha256 OK
S032:appendix-b-template OK
S032:deviation-permission OK
S032:exclude-list-crucial OK
S032:roe-authority OK
S032:roe-definition OK normalized=markup-whitespace
S032:roe-prior OK
S032:scope-actions-outcomes OK
S032:signature-page-scope OK normalized=markup-whitespace
S032:template-illustrative OK
S032:template-starting-point OK
S032:test-site-authorised OK
positive_exit=0      control_clause_exit=0   (S999 → not-listed, exit 2)
```

Compound-line controls (same line shape as the entry, fixture path substituted):

| fixture state | line exit |
|---|---|
| clean | 0 |
| `corruption\n` appended to capture (digest) | 1 |
| one quote replaced with absent text | 1 |
| manifest absent | 2 |

The entry's 11 assertions, in manifest form, are the eight sent to L1 earlier plus
`signature-page-scope` (13 words, `normalized`), `scope-actions-outcomes` and
`exclude-list-crucial`; `deviation-permission`, `template-starting-point` and
`template-illustrative` are single-line in both renderings. L1 verifies each against the committed
capture and drops any that is not exactly-once.

## Touched surfaces

- Wrote `/tmp/kasegi-r24-EntryRoE/corpus/knowledge/authorised-testing-rules-of-engagement.md`
  (the only change in the clone; `git status --porcelain` shows one untracked file).
- Wrote this report: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/EntryRoE.md`.
- Scratch only, outside any repo: `/tmp/roe-capture/` (fetched PDF, two extractions, fixtures),
  `/tmp/roe-fixture*`.
- Not touched: the lane tree, `corpus/SOURCES.md`, `corpus/README.md`, the round-24 manifest,
  git/jj state, the fleet repo, sibling lanes, `/home/vgpnk/Projects/shokuknow` (read only:
  the package entry and `SOURCES.append.md`).

## Integration left to L1 (not done by this seat)

1. **Manifest record.** Round-24 `corpus/source-snapshots/round-24/manifest.json` needs the
   `S032` record + its capture beside the manifest (round-23 convention: own copy, `path`
   relative, digest over raw bytes including any provenance header). Without it the draft's
   recheck exits 2.
2. **SOURCES row.** The row must carry the id the entry cites. If integration keeps `S124`,
   lines 2 and 4 of the entry need `S124` in both places (one edit, no prose change).
3. **README F09 row** (owner: L1; not written here). Proposed:

   `| F09 | Authorisation outside a platform's safe-harbor text — engagement document (ROE) and statute | admitted | knowledge/authorised-testing-rules-of-engagement.md, knowledge/statutory-authorization-and-unauthorized-access.md | <S-ids> | Keep the engagement document's defined activities and the statute's consent carve-out attributed; neither is a platform's safe-harbor grant. |`

4. **C2 counter B.** As filed (`^source: S1[0-9][0-9]`), the counter cannot reach 2 under the
   parent's S032 ruling; the frozen claim's kill rule applies unless the registration or the
   counter is changed before the round closes. Recorded, not decided, here.

## Known limits of this draft

- The draft cites one source (S032). It does not adjudicate the package's Chinese case-law framing,
  third-party asset ownership, jurisdiction, or what any platform's safe-harbor text grants — F03
  and the statute entry hold those.
- `ModDate 2025-11-21` means the served bytes are a 2025 re-save of the 2008 edition; the draft
  pins the capture, not "the 2008 file", and says so.
- The recheck is containment-only: quote-to-folio binding is human-verified (I derived each folio
  from the page split, but the instrument does not re-derive it).
- Tool installs/upgrades this seat: **none**. `pdftotext`/`pdfinfo` were already present
  (`/usr/bin/pdftotext`); pacman was not invoked.
