# RevEntryF17 — non-author review of the F17 entry (kasegi round 34, wave 1)

Seat: RevEntryF17 (reviewer, non-author — I did not author the entry; author seat ScribeEntryF17).
Scope per item: Q1–Q10 verdict table on the final entry bytes at the tip path, plus re-open of
`corpus/source-snapshots/round-34/S051.txt` and exactly-once-at-cited-line verification of every
quoted string; verdict ADMIT / REFUSE.

**Bytes reviewed:** `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`
sha256 `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`, 113 lines, 11143 B,
mtime 2026-10-26 02:37:10 -0300.
Process note: the author first announced `e71fbcd9…` (11206 B) and corrected mid-review to
`948b202e…` after ExecSnapshotR34 restored the two printed bullets into the manifest; my review
target is `948b202e…` only. The earlier `e71fbcd9…` bytes were superseded before verdict; the L1
should commit exactly `948b202e…`.

**Capture pin re-opened:** `corpus/source-snapshots/round-34/S051.txt`
sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` (8502 B, 175 lines) —
equals the digest pinned in `corpus/source-snapshots/round-34/manifest.json` (manifest sha256
`d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe`) and in the entry's Scope
section.

## Report

All commands run in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless noted. Exit codes shown
as measured.

### 1. Digests

```
sha256sum corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
  -> 948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a
wc -l  -> 113          stat size=11143  mtime=2026-10-26 02:37:10 -0300
sha256sum corpus/source-snapshots/round-34/S051.txt
  -> 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5   (manifest pin: equal)
sha256sum corpus/source-snapshots/round-34/manifest.json
  -> d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe
```

### 2. Exactly-once verification (item requirement)

Method: every double-quoted span in the entry (25 found) checked with fixed-string `grep` counts
and line numbers against `S051.txt`; multi-line spans checked under whitespace-joined
normalization (declared by the manifest as `markup-whitespace`; Q8). Results:

- **16 of 18 source quotes: EXACTLY-ONCE at the exact cited line.** Verified singles:
  L46 ("At Immunefi, we classify bugs on a simplified 5-level scale:"), L52 ×2 (both Claim 2
  quotes; L52 holds the full sentence), L74, L79 ("Miner-extractable value (MEV)"), L83
  ("Protocol insolvency"), L88 ("Temporary freezing of funds"), L99 ("Execute arbitrary system
  commands"), L90, L92, L94, L95. Word counts 2–20, all ≤25 (Q3).
- **2 span quotes** cite two-line ranges and verify across exactly those lines:
  "The table below is mostly concerned with the consequence of a successful exploit." = L53-54;
  "the level of the bug may be downgraded to reflect that or rejected." = L55-56. Entry cites
  `S051.txt:53-54` and `:55-56` — correct.
- **1 whitespace-joined quote** "Critical High Medium Low None" cited L47-51: verified per line
  (L47 Critical, L48 High, L49 Medium, L50 Low, L51 None), matching manifest Q2
  (`normalized=markup-whitespace occurrences=1`).
- **2 quotes occur twice and are anchor-pinned, not exactly-once:**
  "Permanent freezing of funds" at L62 (Blockchain/DLT) **and** L77 (Smart Contracts), entry cites
  L77; "1. None- Best practices" at L71 and L96, entry cites L96. The entry discloses both in
  "Scope and limits"; the manifest binds them as Q9 `anchor: 77` and Q17 `anchor: 96`, and the
  instrument prints `occurrences=2 anchor=77-ok` / `occurrences=2 anchor=96-ok`. This satisfies
  QUALITY Q9's disjunction (exactly-once **or** an anchor line the instrument verifies); both
  anchors hold at the cited lines.
- **9 remaining quoted spans are the entry's own rhetoric** (the six rejected-overgeneralization
  headings, "funds are at risk" as a hypothetical report statement, "or" as a word citation, and
  partial literals like `5. Critical-`): none is presented as a source quote; none cited to the
  capture as one. Not load-bearing source claims.

Conclusion: every load-bearing quoted string is verified exactly-once at its cited line, or
anchor-verified at its cited line with the multiplicity disclosed in the entry itself.

### 3. Q1–Q10 verdict table (QUALITY.md entry bar)

| id | verdict | evidence (measured this review) |
|---|---|---|
| Q1 | PASS | H1 at L1; header trio directly under it: `source: S051 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ — …(S051.txt:45; L1), (L46-51), (L52-56), (L72-96)…` (row id + URL + exact anchors); `verified-at: 2026-10-26` (ISO); `recheck:` runnable command failing closed (exit 2 measured, §5). |
| Q2 | PASS | Every load-bearing claim cites the tier-A S051 row opened this round: `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` → `1` (row reads `docs`, tier `A`, scope "Immunefi's own Web3 seve…"). No tier-C support anywhere. Cross-refs F13/F15 verified: `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (`ground: F13`; carries Bugcrowd/VRT/HackerOne) and `vendor-third-party-finding-coordination.md` (`ground: F15 — a vendor's research programme as an intake route`) exist and match the entry's characterization. |
| Q3 | PASS | 18 verbatim quotes, 2–20 words each (≤25), exact locations verified against the pin (§2): 16 exact-once singles, 2 two-line spans cited as ranges, 1 joined five-line sequence. All counts/numbers traceable to capture lines. |
| Q4 | PASS | Attribution section: "Immunefi's own classification system, read as Immunefi's position and nothing wider (Q4)". Claims are phrased as Immunefi's table semantics; six rejected over-generalizations explicitly block universalizing (incl. "the VSCS is CVSS under another name" — rejected). |
| Q5 | PASS | Seven falsifiable checks FC-1…FC-7, each a runnable command with a stated count — all re-measured by me and all matching (§4). Six rejected over-generalizations each with a reason grounded in counts or lines. |
| Q6 | PASS | Documentation-only. FC commands operate on the local capture; no probing/login/submit instruction. Entry contains exactly one URL (`grep -oE 'https?://[^ )]+'` → 1 hit: the public source URL). No credential/session/private-URL material; the capture itself carries none. |
| Q7 | PASS | Recheck is one command; its output names what was checked (`S051:sha256 OK` + 18 per-assertion `OK` lines with occurrences/anchor). Missing-base control measured: `--manifest <nonexistent>` → `manifest UNAVAILABLE reason=missing`, exit=2. Note discloses "captured-source comparison, not a fresh network verification". |
| Q8 | PASS | Normalization declared and printed by the instrument on the three span/joined assertions (`S051:Q2/Q5/Q6 OK normalized=markup-whitespace`); the entry never quotes converter markup; 15 raw quotes also bind unnormalized. |
| Q9 | PASS | Manifest record `path` stem `S051.txt` = id `S051`; 16/18 assertions exactly-once; the 2 occ=2 assertions carry anchors the instrument verifies (`anchor=77-ok`, `anchor=96-ok`); the check prints the occurrence count observed for every assertion. Entry discloses the anchor-pinned pair. All 18 manifest quotes occur verbatim in the entry (checked programmatically: 0 missing). |
| Q10 | PASS | One executable command with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix; `bash -n` → OK; executed verbatim from foreign cwd `/tmp` → exit=0 (§5); human note kept after `#`. |

### 4. FC-1…FC-7 re-measurement on the pinned capture (all stated counts reproduced)

```
grep -cE '^[1-5]\. (Critical|High|Medium|Low|None)' S051.txt -> 15   (FC-1 says 15)
grep -cE 'Severe|Moderate'                          S051.txt -> 0    (FC-1: 0)
grep -c 'v2\.2'                                     S051.txt -> 2    (FC-2: 2; lines L1, L45 — grep -n confirmed)
grep -c 'v2\.3'                                     S051.txt -> 0    (FC-2: 0)
grep -c 'CVSS'                                      S051.txt -> 0    (FC-3: 0)
grep -c 'reward'                                    S051.txt -> 0    (FC-4: 0)
grep -c '\$'                                        S051.txt -> 0    (FC-4: 0)
grep -c 'Permanent freezing of funds'               S051.txt -> 2    (FC-5: 2 at L62, L77)
grep -c 'Temporary freezing of funds'               S051.txt -> 1    (FC-5: 1 at L88)
grep -c 'Execute arbitrary system commands'         S051.txt -> 1    (FC-6: 1 at L99)
grep -c '1. None- Best practices'                   S051.txt -> 2    (FC-7: 2 at L71, L96)
```

11/11 stated counts match. The v2.3 finding (0 occurrences) means the entry correctly claims NO
version-selector rule and records the round brief's v2.2-vs-v2.3 selector as an open item instead
of a finding — verified against the capture.

### 5. Recheck execution (entry's own line, verbatim)

```
bash -n <recheck command>            -> OK (parses)
cd /tmp && bash <recheck command>    -> exit=0, output:
  S051:sha256 OK
  S051:Q1 OK occurrences=1 anchor=46-ok      S051:Q2 OK normalized=markup-whitespace occurrences=1
  S051:Q3 OK occurrences=1 anchor=52-ok      S051:Q4 OK occurrences=1 anchor=52-ok
  S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
  S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
  S051:Q7 OK occurrences=1 anchor=74-ok      S051:Q8 OK occurrences=1 anchor=75-ok
  S051:Q9 OK occurrences=2 anchor=77-ok      S051:Q10 OK occurrences=1 anchor=79-ok
  S051:Q11 OK occurrences=1 anchor=83-ok     S051:Q12 OK occurrences=1 anchor=88-ok
  S051:Q13 OK occurrences=1 anchor=92-ok     S051:Q14 OK occurrences=1 anchor=94-ok
  S051:Q15 OK occurrences=1 anchor=90-ok     S051:Q16 OK occurrences=1 anchor=95-ok
  S051:Q17 OK occurrences=2 anchor=96-ok     S051:Q18 OK occurrences=1 anchor=99-ok
missing-manifest control             -> "manifest UNAVAILABLE reason=missing", exit=2
```

18/18 assertions OK; 16 at occurrences=1, 2 at occurrences=2 with verified anchors — exactly the
shape the entry's Scope section states. The recheck ran from a foreign cwd, proving the Q10
`cd` prefix limb.

### 6. Manifest cross-check

`corpus/source-snapshots/round-34/manifest.json` (sha256 `d5077f81…`): S051 record `fetched_utc
2026-10-26T05:31:10Z` (strict UTC), sha256 equal to the on-disk capture, 18 assertions; program
check: every assertion quote occurs verbatim in the reviewed entry bytes (`entry_missing=[]` —
0 of 18 absent).

### 7. Notes (non-blocking)

1. **Byte churn during review** — author's first announced digest `e71fbcd9…` was superseded by
   `948b202e…` while seats were still running. This review binds to `948b202e…` only; the L1
   should verify the committed bytes hash to it.
2. **Two occ=2 quotes ride the Q9 anchor limb, not exact-once.** Conformant (anchor verified,
   multiplicity disclosed in the entry), but any future re-capture that shifts L77 or L96 fails
   the assertions closed — which is the intended behavior.
3. Entry length 113 lines (author brief said ≤120) — informational, not a Q criterion.

## Verdict

**ADMIT.** The final bytes (`948b202e…`) satisfy Q1–Q10 on measured evidence; every quoted string
is exactly-once at its cited line or anchor-verified at its cited line with the double occurrence
disclosed; all seven falsifiable checks reproduce; the recheck line parses, runs from any cwd,
exits 0 on the pin, and fails closed on a missing base. No criterion fails; no REFUSE grounds.

Scratch `/fast/scratch/hyaku/kasegi-r34/RevEntryF17/` removed before yielding (checker + recheck
copies were the only contents; no fixture trees).

Report: .ufo/waves/round-34/wave1/RevEntryF17.md
