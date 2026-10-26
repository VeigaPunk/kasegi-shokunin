# RevEntryF19 — round-36 review: drafted F19 entry vs QUALITY Q1–Q10

Seat: `RevEntryF19` (leaf, reviewer). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`).
Axis judged: coverage (C2's F19 entry). All measurements 2026-10-26. Report path: `.ufo/waves/round-36/wave1/RevEntryF19.md`.

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/RevEntryF19/`
(removed before yield). No lane, fleet, sibling-lane or source-tree file was edited; no git/jj
mutation was run; no subagent was spawned; `agent://all` was not messaged; no tool was installed.

**Object reviewed:** the entry text between `---BEGIN ENTRY---` / `---END ENTRY---` in
`.ufo/waves/round-36/wave1/ScribeEntryF19.md` **at its current revision** — receipt sha256
`11b7168f31a9555f3ba749bb96a16c3ce22e2a323e0fcfb843646e94735b62f0` (31,278 B), entry block at receipt
L140–L404: **263 lines, 17,374 bytes with final newline, sha256
`36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641`**. An earlier revision I first
extracted (262 lines / 17,266 B entry) still carried the digest typo of Finding F1 below; the scribe
fixed it mid-review after three peers reported it, and every check below was re-run on the fixed text.

## 0. Capture status — not missing, recovered and digest-verified

`ExecC2Capture` removed its scratch at yield, so `S053.txt` was gone from `/fast/scratch/hyaku/kasegi-r36/ExecC2Capture/`
when I started. It is **not missing in substance**: I reconstructed the normalized capture from the
verbatim block in `ExecC2Capture.md` §6 and `sha256sum` over the reconstruction gives
`4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` (8,448 bytes, 244 lines) — equal to
the manifest `sha256` field, to `ScribeRowS053.md` §1.1/§3, and to the instrument's own `expected=` print
(see §2 below). The manifest reconstructs byte-identically too once its final newline is included:
`f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` (3,566 B). Every grep below ran
against those recovered bytes. Independent confirmation: the scribe's own re-fetch that day produced the
same served-body digest (`66fece52…`) as ExecC2Capture's `raw.html` (`ScribeEntryF19.md` §2).

## 1. Verdict

**ADMIT** — no Q1–Q10 criterion fails on the current text. One repair should land with the entry (F2,
one line + a re-measured count), two are one-word/one-clause touch-ups (F3, F4), one is an L1 note (F5).
None of them touches a pinned byte, an anchor, or a quote.

## 2. What I verified (all commands read-only; fixture lane roots under my scratch)

| check | method | observed |
|---|---|---|
| capture digest | `sha256sum` over reconstruction from `ExecC2Capture.md` §6 | `4ec61c59b0e9aedf…83e9`, 8,448 B, 244 lines — matches manifest, row receipt, instrument |
| manifest digest | `sha256sum` over §3 JSON + final newline | `f9590c2bbc26244a…` — matches the pinned value |
| Q1 header trio | read | `source: S053 — https://www.first.org/epss/ — capture …S053.txt (244 lines, 8448 bytes; sha256 …):` + ten line anchors (L1, L208, L216, L217, L220-L230, L224, L232, L234, L235); `verified-at: 2026-10-26`; `recheck:` one command. Extra `ground: F19` line is precedented (`ground: F13` at `corpus/knowledge/program-severity-ladders-and-reward-scales.md`, `ground: F15`, `ground: F18` at `corpus/knowledge/cisa-kev-catalog.md:5`) |
| Q3 quotes ≤25 words, exactly-once, on-anchor | `grep -cF` + `str.count` + anchor-line membership over **11 blockquotes and 9 inline spans** | all 20 pass: max 25 words (Q1 pin), every `occ=1`, every span on its cited line. Spot-verified anchors: L216 definition, L217 both clauses, L224 combine sentence, L226 FAQ clause, L230 Get-the-Data, L232 SIG sentences, L234 partners, L235 maintainer |
| numbers copied, not retyped | compare vs capture/receipt | `0–1` carries the page's U+2013 (hyphen probe fails, as the entry itself warns); `30 days` only on L216; 244/8,448/26,804; `fetched_utc` 2026-10-26T15:35:10Z; `last-modified: Thu, 30 Jul 2026 13:48:13 GMT` — all equal the capture/receipt values |
| Q4 attribution | read + token counts | FIRST's statements kept first-party; Empirical Security named as generator (L235); partner list bounded by "which includes but is not limited to" (L234, occ=1); "freely and openly accessible" scoped to the data; KEV disambiguated from CISA/S052 (S052 row verified present at `corpus/SOURCES.md`, CISA KEV catalog). One hygiene nit → F4 |
| Q5 falsifiable rule + rejected over-generalization | read | four limbs (a)–(d), each tied to a claim and line; 8 rejected over-generalizations each with a reason grounded in a measured token count or quoted line. Cross-refs check out: F13 = "program severity ladders and reward scales" (`SKILL.md:1047`), F17 = Immunefi severity/impact classification (`corpus/SOURCES.md:78`), S052 = CISA KEV |
| Q6 no credential/probe content | regex sweep | only benign meta-mentions: "Counting the token alone…" and "the capture holds no credential, session or private URL…". No credential material, no probing/scanning/login/submission instruction, no private URL; the only URI is the registry-row source URL |
| Q7 executable recheck | `bash -n` + execution in a lane-shaped fixture | `bash -n` rc=0; successful run prints `S053:sha256 OK` + `S053:Q1..Q4 OK occurrences=1 anchor=216/217/217/235-ok`, rc=0 — output names what was checked. **Fail-closed controls measured**: manifest absent → `manifest UNAVAILABLE reason=missing`, rc=2; one corrupted capture byte → `S053:sha256 MISMATCH expected=4ec61c59b0e9aedf… actual=530edc41…`, rc=1 |
| Q8 normalization | manifest `normalized` field + quote matching | normalization declared (`capture-source.py html_to_text()…`); the entry never quotes converter markup; all quotes match the normalized bytes; the transformation is named in ExecC2Capture's receipt |
| Q9 three-way binding | instrument rules B1/B2 + output | manifest `path` stem `S053` == `id` `S053` (instrument B1 passes); each pinned quote exactly-once (`occurrences=1` printed by the recheck — third leg observed). Gap for one unpinned span → F2 |
| Q10 recheck line form | `bash -n` + read | one command, `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix, `--manifest corpus/source-snapshots/round-36/manifest.json --source S053`, human note after `#`, no `$(`/backticks in the note |
| R12 recheck↔entry binding | read | `--source S053` covers the header's `source: S053`; the named manifest lists S053; the command is cited by the entry |
| FC-1..FC-5 | executed in fixture | outputs equal the entry's stated observations exactly: `1 1 1 1`; `spans 11 occ_all_1 True words_max 25 anchors_ok 11 of 11`; `severity=0 reward=0 http=0 bounty=1 threshold=1`; `CVSS=33 KEV=2 calibration=1 percentile=2 probability=2 score=4`; `216` |
| CVSS/KEV distribution | recount | 33 `CVSS` occurrences: 31 on 26 lines inside L70–L198 (nav) + L222 + L224 — matches the entry's Claim 4 bullet; `KEV` only on L224, L234 — matches |

## 3. Findings

**F1 — digest typo in the entry's sha256 literals: FOUND, already FIXED during this review.**
The revision I first extracted wrote the capture digest as `4ec61c59b0a9aedf…` (`b0a9` for `b0e9`, one
hex digit) in the `source:` header and the Scope bullet. The recheck is immune (it reads the manifest
digest), so only a reader comparing the header hash to the landed bytes would catch it — a false
evidence line of the E8 class. `ExecC2QuoteOnce`, `MutJunkTwin` and `ScribeRowS053` reported it
independently; the scribe re-derived the digest and fixed all four occurrences (entry ×2, receipt §2,
receipt §4) in the current revision. Current state: true digest ×2, typo ×0 in the entry text; the wrong
form survives only inside the receipt's correction paragraph, quoted as the error. **No action left;
the standing discriminator is: the header's sha256 literal must equal `sha256sum` of the landed
`corpus/source-snapshots/round-36/S053.txt`.**

**F2 — FC-2's span list omits the entry's 11th blockquote (recommended pre-landing).** The entry
blockquotes twelve distinct spans' worth of citations but FC-2's tuple list carries 11: it includes the
inline-quoted L220 sentence and **omits the L217 blockquote "It offsets subjective judgments with
empirical signals from observed exploitation and ongoing activity"** (13 words, occ=1, on-anchor — I
verified the span itself). That span is neither manifest-pinned nor FC-2-guarded nor listed in the Scope
bullet's "remaining cited spans (L220, L222, L224, L226, L230, L232, L234)", so its exactly-once
property has no landed check — the only Q9-coverage gap in the entry. Repair (entry-local, no manifest
revision needed): add `(217,"It offsets subjective judgments with empirical signals from observed
exploitation and ongoing activity")` to FC-2's list, re-run FC-2, and update its `Observed` line to the
re-measured output (expected shape `spans 12 occ_all_1 True words_max 25 anchors_ok 12 of 12`); amend
the Scope bullet to "L217 (third span)". Heavier alternative per the scribe's own receipt §4.2: pin it
in a new manifest revision — not required.

**F3 — "seven topic pointers (L220-L230)" is a miscount (minor).** Entry Honest-limit line: the capture
holds **six** pointer pairs spanning **L219–L230** (titles at L219 "How It Works", L221 "Why EPSS?",
L223 "Using EPSS", L225 "Frequently Asked Questions", L227 "Research", L229 "Get the Data";
descriptions at L220/222/224/226/228/230). Repair: "six topic pointers (L219-L230)". The `source:` line's
"topic pointers L220-L230" is defensible as the description lines, but the same L219-L230 range is
cleaner there too.

**F4 — one clause rides inside a page-attribution sentence (minor, Q4 hygiene).** Claim 4 closes with
"the page's own instruction is to combine them, not to rank one against the other" — the page instructs
combining (L224); "not to rank one against the other" is the entry's inference, not page text, and as
written it reads as part of the page's instruction. Repair: "…the page's own instruction is to combine
them; ranking one against the other is this entry's contrast, not the page's." — or drop the clause.

**F5 — receipt §1 metadata is stale (L1 note, not an entry defect).** `ScribeEntryF19.md` §1 still says
the entry "measures 262 lines / 17,251 bytes as drafted"; the current §6 text measures 263 lines /
17,374 bytes (final newline included), sha256 `36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641`.
The L1 should measure the landed file after any F2–F4 edit rather than trust §1's figure.

## 4. Cross-checks and non-blocking observations

- Agreement with `ExecC2QuoteOnce.md` (independent quote verifier): same digest catch (now fixed), same
  pin/anchor results, same `bash -n` verdict. Their §7.1 note (annotation parenthetical inside the Q1
  blockquote line) — I counted words inside the quotation marks only, so the 25-word cap holds; their
  optional hardening (move the parenthetical to prose) stands as optional.
- The entry's FC commands reference `corpus/source-snapshots/round-36/S053.txt`, which does not exist in
  the lane yet; my runs used a lane-shaped fixture with the recovered bytes. The landed-path run belongs
  to ExecC2Harness/ExecManifestChecks after integration.
- Q2's tier-A support is evidenced by `ScribeRowS053.md` §2 (tier `A`, `mined`, opened 2026-10-26,
  `used-by` this entry, source-cell URL byte-equal to the manifest `url`); the row itself lands with
  integration, as does the F19 frontier row — both outside this seat's scope.
- The H1 title's parenthetical "(L234's KEV is VulnCheck's feed, not the CISA catalog)" is accurate
  against the capture (L234 names VulnCheck KEV; `CISA` occurs 0 times) and was added on ScribeRowS053's
  flag — an improvement, kept.

## 5. Method / artifacts

- Review performed against the receipt-embedded entry text (the scratch copies were removed at the
  producers' yields); capture and manifest recovered from `ExecC2Capture.md` §3/§6 and digest-verified
  before any quote check.
- Fixture lane roots (`fx-pass`, `fx-nomanifest`, `fx-corrupt`) under `/fast/scratch/hyaku/kasegi-r36/RevEntryF19/`
  with the lane's own `corpus/instruments/source-recheck.py` copied in read-only; no lane write at any point.
- Tooling: none installed or upgraded (no pacman, no uv/npx).
- Scratch directory removed before this receipt was finalized; every number above is reproducible from
  the two producer receipts plus this file.

Report: .ufo/waves/round-36/wave1/RevEntryF19.md
