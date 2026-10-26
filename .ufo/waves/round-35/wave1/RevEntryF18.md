# RevEntryF18 — non-author review of the final F18 entry bytes

- Seat: RevEntryF18 (reviewer, leaf). Reviewed for: depth:verifiability, coverage. Milestone: round-35.
- Review target: `corpus/knowledge/cisa-kev-catalog.md` at the lane working-copy tip, final digest `sha256 e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730` (118 lines, 17,643 B).
- I did not author the entry. Author seat: ScribeEntryF18. The bytes changed twice while my battery ran (I inspected `da81204b…` 88-line, `09888666…` 117-line, then re-ran everything quoted below on the final `e3f233c0…`); every command/output in this receipt was run against the final digest unless marked "(unchanged since da81204b — source-side)".
- Verification inputs re-opened by me: `corpus/source-snapshots/round-35/S052.txt` (27,870 lines, 1,479,694 B, `sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` — recomputed independently, matches manifest and entry L3/L84), `corpus/source-snapshots/round-35/manifest.json`, `corpus/SOURCES.md` (S052 row at L58), `corpus/README.md`, `corpus/QUALITY.md` (Q1–Q10), `corpus/instruments/source-recheck.py` (L85–150 read for anchor semantics).

## Report

### 1. Verdict

**REFUSE — one criterion: Q2, for Claim 4b only.** Every other criterion passes on measured evidence (table §3). If the L1 lands either repair in §2, the entry is ADMIT on my re-check without further findings.

### 2. The Q2 failure — exact criterion and lines

Q2 (`corpus/QUALITY.md` entry bar): *"Every load-bearing claim rests on ≥1 tier-A or tier-B row for that claim's scope, opened in the admitting round; a tier-C row is never sole support."*

Claim 4b is a claim (heading `## Claim 4b — the current directive is BOD 26-04, and BOD 22-01 is revoked (live-page read, not a captured source)`, entry L42) whose scope is CISA's BOD 26-04 directive page. That page has **no source row at all** — the entry says so itself:

- L47–48: "This page is **not** in the S052 capture and is **not** a registered source row, so these quotes are a dated live-page claim, not a pinned-source claim (see Scope)."
- L116 (Scope bullet): "CISA's BOD 26-04 page is tier A but has no registry row and no `corpus/source-snapshots/` capture this round."

The claim is load-bearing: Claim 4's conclusion depends on it — L40 tail: "legacy field text, because BOD 22-01 is revoked and BOD 26-04 is the current directive (Claim 4b) — … the capture's bytes alone do not establish either directive's force, so that part rests on the live page in Claim 4b" — and L66–67: "BOD 22-01 is listed as revoked (L208), so the 340 capture rows that still name it are legacy field text". Remove Claim 4b and those statements lose their only support. S052 (tier A, opened 2026-10-26, `SOURCES.md:58`) does not cover the page's scope — its registered scope is "CISA's own Known Exploited Vulnerabilities catalog statements as the captured feed states them".

The disclosure is honest and prominent (L47–48, L116–117: "Claim 4b's provenance is weaker than Claims 1–6 and is labelled as such; the S052 claims are unaffected") — this is not a hidden defect, and the author asked me to rule explicitly on exactly this point. But QUALITY has no disclosed-live-read exemption: disclosure is not a registry row. The corollary defect: the four 4b blockquotes (L50, L52, L54, L56) and the inline extraction-line citations (L92, L208, L179, L181, L169, L98–L101, L171) point at an extraction that exists nowhere in the repo. My presence check: the quote text "compulsory direction to federal" occurs in exactly one file under `corpus/` — the entry itself; no `corpus/source-snapshots/` capture, no checked-in extraction. Once CISA edits the page, these quotes are permanently unverifiable — the exact failure mode captures exist to prevent.

**Repair paths (L1's decision, either yields ADMIT on my re-check):**
1. Register a tier-A source row + checked-in capture for `https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk` this round (the same move that admitted S052 itself: "a source first registered this round"), bind a manifest with the 4b assertions, and point the 4b quotes at the capture. Note: claims.json C2 is frozen; a second registered source is a wave-scope question for the L1, not mine.
2. Demote the directive-force content out of claim status: strip "## Claim 4b" to a Scope note and reword Claim 4's "legacy field text, because BOD 22-01 is revoked…" to what S052 alone supports (e.g. "340 rows still name BOD 22-01; the capture does not state whether it is current"). Claims 1–3, 5, 6 and all falsifiable checks FC-1..FC-11/FC-13 stand on S052 alone today.

### 3. Q1–Q10 verdict table

| id | verdict | evidence (commands run on final bytes e3f233c0) |
|---|---|---|
| Q1 | PASS | L1 H1; L3 `source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt (…sha256 d69349e8…): title L2, catalogVersion L3, …` — S### id + URL + capture path + line anchors; L4 `verified-at: 2026-10-26` (ISO); L6 `recheck:` runnable, fails closed (§4 controls). Anchor spot-checks all held except the minor span in §5.1. No cadence token on the line — matches corpus convention: `grep -c '^recheck:' corpus/knowledge/*.md` sums 47 lines, `grep -l '^recheck:.*[0-9]d\b' …` = 0 files; cadence (`90d`) lives in the S052 row. |
| Q2 | **FAIL (Claim 4b)** | §2. All S052-grounded claims rest on tier-A S052 opened this round. |
| Q3 | PASS | Six blockquotes, word counts ≤25 (7/4/8/19/16/23, counted by me): locations L2, L4-L5, L15472-L15475 (+cveID L15465), L19165-L19168 (+cveID L19161), L5423-L5424, L2246 — all verified against capture bytes (§4). Numbers (1,756 / 2026.10.23 / 340/139/1,277 / 361/1,395 / 91/1,665 / 893 / 46 / 327 / 11954) verified via FC-1..FC-11 runs (§4) — copied from source, not retyped. 4b quotes carry heading+line locations but unpinned bytes (§2). |
| Q4 | PASS | L10 attributes to "CISA's catalog … CISA's own machine-readable feed"; declines to attribute a definition S052 lacks; L66-67 "this entry does not present BOD 22-01 as the current authority"; six rejected over-generalizations keep attribution. |
| Q5 | PASS | L59 falsifiable rule with five checkable conditions (a)–(e); L75–80 six rejected over-generalizations each with a reason. |
| Q6 | PASS | Sweep `grep -in 'password\|secret\|token\|vault:\|session'` on the entry: only L71/L118 which use the words in negation. URLs are public (cisa.gov feed + directives page, nvd.nist.gov inside quoted feed text). FC-12 is a read-only GET of a public page — the same class as the registry's own `capture-source.py` fetches; no probing/scanning/login/submission instruction. |
| Q7 | PASS | Recheck output names what was checked: `S052:sha256 OK`, `S052:Q1..Q5 OK occurrences=1 anchor=N-ok`. Missing/corrupted controls both fail (§4 controls). The entry's own note states "a pinned-capture comparison, not a fresh network check"; FC-12 is a separate falsifiable check, not presented as the recheck. |
| Q8 | PASS | Declared normalization: L16 "(whitespace-joined across the line break)", L86/Scope: "Q3, Q4 and Q5 each span consecutive source lines; the instrument prints `normalized=markup-whitespace …`". Instrument output confirmed: Q3/Q4/Q5 `normalized=markup-whitespace occurrences=1`; Q1/Q2 raw. No converter markup quoted anywhere (the `--kind text` capture avoided entity rewriting, manifest purpose field). |
| Q9 | PASS | Five manifest assertions each exactly-once — my independent count (normalized whole-file, markup-stripped): Q1=1, Q2=1, Q3=1, Q4=1, Q5=1; anchors 2/3/4/15472/19165 all hold (instrument `anchor=N-ok` + my own window check). The two non-manifest quotes are non-unique **by declared design** (2 and 327), carry anchors that hold (L5423/L5439 verified; L2246 verified), and are counted by FC-9/FC-10 which I ran: `2` and `327`. This contradicts no frozen claim — claims.json requires "every **assertion** occurrences=1" i.e. manifest assertions only, and the frozen counting command (`source-recheck … every assertion occurrences=1`) passes as stated. Occurrence counts are printed by every check. FC-13 ran: `anchors_ok 5 of 5` — and its stated instrument gap (a retargeted anchor on an exactly-once quote still passes source-recheck) is accurate per `source-recheck.py` L85–107 (B2 fatal only when `occurrences>1`). |
| Q10 | PASS | L6 is one executable command: `bash -n` exit 0; carries `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`; runs green from a foreign cwd (`/fast/scratch/hyaku/kasegi-r35/RevEntryF18`): exit 0 with the five `OK occurrences=1` lines; human note kept after `#`. |

### 4. Command log (all run by me, cwd = lane root unless stated)

```
$ sha256sum corpus/knowledge/cisa-kev-catalog.md corpus/source-snapshots/round-35/S052.txt
e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730  corpus/knowledge/cisa-kev-catalog.md
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
$ wc -lc corpus/knowledge/cisa-kev-catalog.md            -> 118 17643 (matches author's claim)
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
exit=0

# exactly-once battery (assignment core) — every quoted string vs S052.txt:
$ grep -cF '"title": "CISA Catalog of Known Exploited Vulnerabilities",' S052.txt        -> 1   (at L2,  grep -nF)  PASS
$ grep -cF '"catalogVersion": "2026.10.23",' S052.txt                                    -> 1   (at L3)                 PASS
$ grep -cF '"dateReleased": "2026-10-23T19:30:18.9209Z",' / '"count": 1756,'             -> 1 / 1 (L4 / L5)                PASS (span Q3 normalized count = 1, Python)
$ Q4 span L15472-L15475: fragments file-wide 12/361/1665 (declared open vocabularies); discriminating
  notes URL CVE-2022-29499: raw hits = 2 (cveID L15465 + notes L15475); normalized 4-line span count = 1; anchor 15472 holds  PASS
$ Q5 span L19165-L19168: Citrix shortDescription fragment = 1; normalized 4-line span count = 1; anchor 19165 holds          PASS
$ FC-9  grep -cF 'The KEV due date refers to the deadline by which FCEB agencies are expected to review'  -> 2  (L5423, L5439) — declared "occurs twice", anchored, not a manifest assertion
$ FC-10 grep -cF 'follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable\.' -> 327; anchor L2246 holds the sentence (grep on sed -n '2246p' = 1)
$ inline numeric claims: severity occurrences=2 (L5135, L11629); score=1 (L23592); cvss=0; 'risk rating'=0; reward=0; bounty=0; UserResource\$UriData=1 (L11954)
$ python3 (verbatim FC-13) -> anchors_ok 5 of 5, exit=0
$ python3 (verbatim FC-1)  -> keys 5 count 1756 records 1756, exit=0

# Q7 fail-closed controls (copies under my scratch, originals untouched):
$ corrupted capture (one byte changed) -> S052:sha256 MISMATCH expected=d69349e8… actual=0955bca3…  exit=1
$ --manifest <absent>                  -> manifest UNAVAILABLE reason=missing                        exit=2

# Q10 cold-start form (foreign cwd):
$ bash -n <L6 command>   -> exit 0
$ bash -c '<L6 command>' from /fast/scratch/hyaku/kasegi-r35/RevEntryF18 -> exit 0, prints the five S052:Q* OK lines

# 4b traceability probe:
$ grep -rln 'compulsory direction to federal' corpus/ -> only corpus/knowledge/cisa-kev-catalog.md (no capture, no extraction anywhere in the lane)
```

FC-12 (live curl) I did not execute: it re-verifies the live page, and the Q2 defect is row-absence, which no live fetch cures.

### 5. Minor findings (non-blocking, for the L1)

1. **Entry L3 anchor span off by one.** Entry: "first record L8-L21". Capture bytes: L6 `"vulnerabilities": [`, L7 `{`, L8 cveID, …, L19 `"cwes": [`, L21 `]`, L22 `},` — the record object spans **L7–L22**, exactly as the SOURCES row (`SOURCES.md:58`: "first record L7-L22 with cveID L8") states. L8–L21 are the fields between the braces. Recommend entry L3 → "first record L7-L22" so entry and row agree byte-for-byte. Not refusal-grade: the anchor unambiguously identifies the same record, and every other anchor I checked is exact.
2. **L116 phrasing** "is tier A but has no registry row" is self-contradictory on its face (tier is a row property). Presumably means tier-A-class material. Suggest "would be tier A material once registered".
3. **Coverage observation (outside my seat scope):** `grep -c '^| F[0-9]* |' corpus/README.md` = **17** — the F18 frontier row has not landed yet (entry L5 `ground: F18` resolves once it does; claims after-state expects 18). SOURCES registry = 52 rows including tier-A S052, landed mid-review. Flagging for the L1's integration checklist only.

### 6. Digests and cleanup

- Entry (reviewed bytes): `e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730` (118 lines, 17,643 B). Intermediate digests seen and superseded during review: `da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf` (88 lines), `0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74` (117 lines).
- Snapshot: `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` (27,870 lines, 1,479,694 B) — matches manifest record and SOURCES row.
- Scratch `/fast/scratch/hyaku/kasegi-r35/RevEntryF18/` (controls fixtures, recheck.sh copy) deleted before yielding; no lane files modified by this seat; no tool installs (none needed).

### 7. Post-repair re-check (appended after the author applied repair option 2)

The author deleted Claim 4b outright (their reason for not taking option 1 is sound: a new tier-A row would take SOURCES.md 52→53 and fail the frozen C2 literal `registry rows != 52`; the row block belongs to ExecRegistryAppend-3 and a row addition needs an L1 claim erratum). New digest reviewed: `sha256 e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761` (91 lines, 15,831 B).

Re-verified on the new bytes, not trusted from the author's message:

- `grep -n '4b'` on the entry → no output, exit 1 — Claim 4b fully gone.
- Claim 4 (L40) now ends: "these bytes establish neither directive's status nor its force, and no claim in this entry depends on one. The live page that states the directives' status is noted, not claimed, in Scope." — the load-bearing dependency is severed; every claim now rests on tier-A S052 alone → **Q2 PASS**.
- Scope bullet L89: "**Directive status: a live-page note, not an admitted claim (Q2).**" with page URL, read date 2026-10-26, the three quoted fragments inline, "The page has no registry row and no capture in this lane, so these are a dated live read: **no claim above rests on them**, and FC-12 re-fetches the page. Registering a row plus capture is the repair that would let a later round admit the statement under Q2." — context with inline provenance, not claim support; Q3 does not bind a non-claim note.
- Entry L3 fixed to "first record L7-L22" — now byte-exact and agreeing with `SOURCES.md:58` (my minor finding 1 resolved); the self-contradictory "is tier A but has no registry row" phrasing is gone (finding 2 resolved).
- All six remaining blockquotes re-counted against `S052.txt` on the final bytes: 7w raw=1 norm=1 (L2); 4w raw=0 norm=1 (L4-L5 span); 8w raw=0 norm=1 (L15472-L15475 span); 19w raw=0 norm=1 (L19165-L19168 span); 16w raw=2 norm=2 (L5423/L5439, declared twice, anchored); 23w raw=327 norm=327 (L2246 anchor holds). Same results as the pre-repair battery — quotes unchanged.
- `source-recheck --source S052` re-run: exit 0, `sha256 OK`, Q1–Q5 `occurrences=1` with anchors 2/3/4/15472/19165-ok; recheck line re-run from a foreign cwd: exit 0.
- Q6 sweep re-run on the new bytes: only negation-context hits (L44, L91).

**Final verdict: ADMIT** (digest `e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761`). Q1–Q10 all PASS. Residual notes for the L1: (a) the live-page directive-status statement remains unregistered by design — a later round can admit it under Q2 via a row+capture, as the note itself proposes; (b) README frontier rows still 17 at my last check — the F18 row must land for the C2 after-state (outside my seat scope).

Scratch `/fast/scratch/hyaku/kasegi-r35/RevEntryF18/` and the re-check temp dir were deleted; no lane files modified by this seat except this receipt.
