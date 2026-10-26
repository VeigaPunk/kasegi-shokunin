# ExecEntryF15 receipt — round 31, C2/F15 knowledge entry

- Seat: `ExecEntryF15` (leaf). Round 31, wave 1. Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`.
- Answering model: `devin/deepseek-v4-1-flash` (route-table default; no model passed).
- Write scope exercised: `corpus/knowledge/vendor-third-party-finding-coordination.md` (new file) + this receipt. Nothing else written. No git/jj command of any kind was run (not even read-only); no network fetch; no tool installed or upgraded (python3 stdlib + coreutils only); no pacman transaction.
- Deliverable: `corpus/knowledge/vendor-third-party-finding-coordination.md` — 160 lines, 11501 B, sha256 `1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb`.

## 1. Dependency receipts (waited for, then read)

```
cd .ufo/waves/round-31/wave1 && until [ -s ConnSibling.md ] && [ -s ExecCapManifest.md ]; do sleep 20; done
→ both present after one poll (20 s); ExecCapManifest.md 8057 B, ConnSibling.md 29411 B
```

| Peer receipt | What I took from it | Used for |
|---|---|---|
| `.ufo/waves/round-31/wave1/ExecCapManifest.md` §3 | `S048:sha256 OK` + `S048:Q1..Q8 OK occurrences=1` + `recheck_exit=0`; capture `3755 B`, `97` lines, sha256 `2001ad77…e55`, captured `2026-10-25T23:29:53Z` | the gate that the capture + manifest exist and recheck exits 0 before I wrote the entry |
| `.ufo/waves/round-31/wave1/ExecCapManifest.md` §6 | "page-level evidence only (no timelines/contacts)"; line 2 Trace Id is per-request | the `## Honest limit` section |
| `.ufo/waves/round-31/wave1/ScoutF15Sweep.md` head | verdict `residual-exists` (narrow) — **not** `restatement`, so no `BLOCKED: restatement` | decision to write the entry |
| `.ufo/waves/round-31/wave1/ScoutF15Sweep.md` §"exact residual" | r2 alone = restatement of Cisco S040; expansion credit requires foregrounding route 3 (internal research) + the self-declared coordinator role | structure of `## What this adds beyond F06 and F10` |
| `.ufo/waves/round-31/wave1/ScoutF15Sweep.md` §Cautions 1-2 | do not adopt staged `ground: F20` / S080 / prose recheck; do not assert an obligation on finders | header `ground: F15`; rejected over-generalization 4 |
| `.ufo/waves/round-31/wave1/ConnSibling.md` §1.5, §2.2 | zero sibling-lane overlap; F15 inside kasegi province; Q6 documentation-only | scope paragraph; no cross-lane claim made |

Also received: ExecCapManifest's IRC summary of the S048 final state (identical to its receipt §3 — no new fact used), and `CritC2Kill-4`'s review of this entry at the pre-fix digest (§9).

## 2. Entry header (lines 1-5, verbatim)

```
# A vendor's research programme as an intake route for other vendors' bugs
source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "Microsoft Security Vulnerability Research (MSVR)", capture corpus/source-snapshots/round-31/S048.txt:28-35 — the programme description L29, the three-route intake sentence L31, the three routes L32-L34, the three-role sentence L35
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048   # 8 assertions, every quote exactly-once in the pinned capture; a captured-source comparison, not a fresh network verification
ground: F15 — a vendor's research programme as an intake route for other vendors' bugs
```

Structure (final bytes): `## Attribution` L7, `## Claim 1` L17, `## Claim 2` L41, `## What this adds beyond F06 and F10` L61 (incl. the residual sweep at L91-L100), `## Honest limit` L102, `## Falsifiable checks` L114 (FC-1..FC-5 at L119-L123), `## Rejected over-generalizations` L125 (5 items), `## Scope and limits` L150.

## 3. Q1-Q10 self-check (line pointers are into the entry, 160 lines)

| id | verdict | pointer / measurement |
|---|---|---|
| Q1 | pass | L2 `source: S048 — URL — section + capture path + line numbers`; L3 `verified-at: 2026-10-25`; L4 one executable `recheck:` with its own `cd` prefix; L5 `ground: F15`. The three header lines sit directly under the H1 (L1), no blank line between. |
| Q2 | pass | Every load-bearing claim rests on S048, a tier-A row opened this round (capture `2026-10-25T23:29:53Z`, manifest pin). No tier-C source; the only other citations are the lane's own entries/captures (S018, S039, S040) used for the contrast in L63-L100, never as support for an MSVR claim. |
| Q3 | pass | 13 located quotes, each ≤25 words, each exactly-once in the capture, each carrying its capture line (§6). No number is retyped: file size, line count, sha256 and every grep count were measured this seat (§4, §6, §7). |
| Q4 | pass | Every programme claim is attributed to the stating party: L17 and L41 read "Microsoft's MSVR states…"; L9-L12 `## Attribution` states it is a first-party self-description and "not a rule about vendors in general". No sentence says "vendors do…". |
| Q5 | pass | `## Falsifiable checks` L114-L123: 5 runnable greps with their measured counts. `## Rejected over-generalizations` L125-L149: 5 rejections, each with its reason. |
| Q6 | pass | Documentation only: published programme text plus greps over a local capture. No probing/scanning/login/submission instruction. The words `vault`/`token`/`session`/`credential` occur only inside the standard Q6 disclaimer at L158-L160 ("carries no credential material, session or private URL"), which names no value. |
| Q7 | pass | L4 is a command, not prose; its note names what it checks ("8 assertions, every quote exactly-once in the pinned capture") and discloses the captured-source limit (L155-L157). Fail-closed controls measured by ExecCapManifest §4: wrong pin → exit 1, absent/foreign stem → exit 1, dropped quote word → exit 1. |
| Q8 | pass | Normalization declared in the manifest `purpose` and at L155-L156 ("capture markup stripped, whitespace collapsed"). No quote repeats converter markup; the quoted text is the page's own prose. |
| Q9 | pass | Stem `S048.txt` == id `S048`; all 8 manifest quotes exactly-once (`occurrences=1` printed per quote, no `anchor` needed); the entry's own extra quotes were measured the same way (§6). `location` in the manifest is documentation the instrument does not read, so every quote in the entry also carries its raw capture line. |
| Q10 | pass | L4 is one command: `bash -n -c "<line>"` → exit 0; run from `/tmp` → exit 0 with all 8 `OK` lines (§4). Human note kept after `#`. |

R6/R12/R13 are records, not entry criteria; R12 is checked mechanically in §5.

## 4. Recheck (target command) — lane root and foreign cwd

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "recheck_exit=$?"
```
```
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
recheck_exit=0
```
```
RL=$(grep -m1 '^recheck:' corpus/knowledge/vendor-third-party-finding-coordination.md | sed 's/^recheck: //')
bash -n -c "$RL"; echo "bashn_exit=$?"            → bashn_exit=0
cd /tmp && bash -c "$RL"; echo "foreign_exit=$?"  → same eight OK lines, foreign_exit=0
```

## 5. Harness contract (frontier-recheck-count.py, imported read-only — the F15 README row is another seat's path)

```
declared: ['S048']
recheck_ids: ['S048']
manifest: corpus/source-snapshots/round-31/manifest.json
cited has S048: True   cited count: 4
manifest ids: {'S048'}
subset checks: True True
```
Checks A-C hold on this entry; D (the run) is the exit-0 command in §4. I did not run the harness itself: F15 is not yet an admitted row, so its output would be PRE-STATE for C2 and is cited nowhere.

## 6. Quote inventory — occurrence count, word count, raw capture line

Measured under `source-recheck.py`'s normalization (`<…>` stripped, whitespace collapsed) on the pinned capture:

| entry line | words | occ | raw line | quote (truncated) |
|---|---|---|---|---|
| L14 | 23 | 1 | 29 | MSVR is a program specifically designed to help improve the security ecosystem… |
| L19 | 10 | 1 | 31 | MSVR learns about vulnerabilities in third-party products in three ways: |
| L26 | 3 | 1 | 32 | Internal Microsoft engineers |
| L26 | 19 | 1 | 32 | These vulnerabilities are reported to the MSVR team, which then works with the affected vendor… |
| L27 | 9 | 1 | 33 | External reports to the Microsoft Security Response Center (MSRC) |
| L27 | 6 | 1 | 33 | These issues are coordinated by MSVR. |
| L28 | 3 | 1 | 34 | Internal research projects |
| L28 | 14 | 1 | 34 | Any issues are reported to the affected vendor under accepted CVD practices. |
| L32 | 14 | 1 | 34 | products that run on Microsoft operating systems, but that are not developed by Microsoft |
| L43 | 11 | 1 | 35 | This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach. |
| L48 | 11 | 1 | 35 | as a vendor affected by vulnerabilities in its products and services |
| L51 | 11 | 1 | 35 | as a finder of new vulnerabilities in third-party products and services |
| L54 | 9 | 1 | 35 | as a coordinator of vulnerabilities that affect multiple vendors |
| L122 | 4 | 1 | 15 | Microsoft Bug Bounty Programs (navigation link, quoted as chrome, not as programme text) |

Non-S048 citations, both re-measured before use: `S039.txt:506` contains `他社製品に影響することがわかった` (Hitachi's spill-to-other-vendors sentence); `S040.txt:185-193` is the "Incidents that may impact other vendors" paragraph and the 4-word quote `may impact multiple vendors` is on L191, inside the cited range. Neither supports an MSVR claim — both are contrast rows.

Capture anatomy measured: L1 `msvr`, L2 per-request Trace Id, L3-L27 navigation, L28 section title, L29-L35 programme body, L36-L97 footer; `Microsoft Bug Bounty Programs` is L15 (nav), `Certified Refurbished` is L48 (footer).

## 7. Falsifiable checks — run, not asserted

```
S=corpus/source-snapshots/round-31/S048.txt
grep -cE '^(Internal Microsoft engineers|External reports to the Microsoft Security Response Center \(MSRC\)|Internal research projects):' $S → 3
grep -c 'in three ways' $S → 1 ; grep -ci 'only' $S → 0
grep -c 'as a coordinator of vulnerabilities that affect multiple vendors' $S → 1
grep -ciE '90[ -]day|deadline|embargo|timeline' $S → 0 ; grep -ci '@microsoft' $S → 0
sed -n '28,35p' $S | grep -ci bounty → 0 ; grep -ci bounty $S → 1 (nav L15)
grep -c 'affected vendor' $S → 2
grep -c 'CERT/CC' $S → 0 ; grep -c 'JPCERT' $S → 0 ; grep -c 'IPA' $S → 0 ; grep -n -i cert $S → 48:Certified Refurbished
grep -ci 'http' $S → 0
for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
  → corpus/knowledge/vendor-third-party-finding-coordination.md (each of the four terms)
```
Every count printed in the entry is a count measured above.

## 8. Three defects I caught in my own draft (disclosed, fixed before final)

1. I wrote the bounty navigation item as `L12`; `grep -n -i bounty` shows it at **L15**. Fixed (now L122 in the entry).
2. I wrote "`grep -ci 'cert'` over the capture is `0`"; measured it is **1** (footer `Certified Refurbished`, L48). Replaced with the three centre names actually measured (`CERT/CC`, `JPCERT`, `IPA`, all 0) and the real `cert` hit disclosed.
3. The first draft claimed each route ends at the affected vendor; measured `affected vendor` = 2 for 3 routes. Fixed in §9 item 1 below (this one was also caught by the critic).

Pre-fix digests (`bf40fd9e…` and the earlier drafts) are cited nowhere.

## 9. Critic fixes applied (CritC2Kill-4, review at sha256 `bf40fd9e…`)

| # | critic finding | change |
|---|---|---|
| 1 | FC-5 falsified by its own command: `affected vendor` = 2 for 3 routes, L33 names no recipient | Claim 1 heading lost "as a closed list"; the L35-L39 summary now says Microsoft names a recipient for **two** routes and that route 2 "says only that MSVR coordinates the issue"; FC-5 (L123) restated as "two of the three routes name the affected vendor; route 2 names no recipient" |
| 2 | "closed list" / "closed at three" overreach: the page says "in three ways" and never says "only" | FC-1 (L119) restated as "the page enumerates three labelled routes", now carrying `grep -c 'in three ways'` → `1` and `grep -ci 'only'` → `0`, and stating that a fourth route is unsupported by the capture, not excluded by the page |
| 3 | route-2 gloss dropped L33's third-party-only alternative | L36-L37 now reads "an external report filed against a Microsoft product that the reporter believes also affects a third-party product (or affects both)" |
| 4 | kill rule needs a sweep command and F11 named | L89-L100: F11 named (no finder/coordinator seat) and the four-term `grep -rli` sweep added with its measured output |

Critic's live re-open (2026-10-25T23:31Z, code 200, 81802 B, L31-L35 verbatim, diff vs capture = line 2 only) is recorded here as the critic's observation, not re-run by me. Their two out-of-scope flags (registry row placement inside `## Registry`; manifest carrying no `url` field) are routed to the L1/ExecCapManifest by them; I took no action on another seat's path.

## 10. Scope, limits, blockers

- One page, one vendor, page-level evidence. The entry says so at L102-L112 and L150-L160; it does not claim the coordination agreements, a timeline, a contact or a per-vendor process, because the capture carries none (`@microsoft` 0, `http` 0, clock terms 0).
- Nothing here establishes that an affected vendor was told, or when. The staged package's "the finder also has a coordinated-disclosure obligation" is refused at L138-L142 as an inference the bytes do not carry.
- No blocker. `BLOCKED:` is not used: all three dependency receipts arrived and the capture recheck exits 0.
- Untouched by this seat: `corpus/SOURCES.md`, `corpus/README.md`, `corpus/instruments/knowledge-expected.txt`, `PROVINCE.md`, `SKILL.md`, `QUALITY.md`, `LOG.md`, `SCORECARD.md`, `corpus/instruments/README.md`, the report, `claims.json`. Messaged after final: ExecRegistryAppend, ScribeReadmeF15, ScribeProvince, ExecExpectedList, ScribeGateDraft.

## 11. Downstream confirmations (peer-observed, not re-run by this seat)

- `ExecRegistryAppend` (round-30 registry seat, no write): the S048 row is `corpus/SOURCES.md:54` inside `## Registry` (starts line 3) and before `## Paths` (line 56), so no census E12; `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 (base W04 S028/S029 lines only); used-by cell is exactly `corpus/knowledge/vendor-third-party-finding-coordination.md`; registry 48 rows, S048 once; landed S048 line digest `0f2d9cb6…3de7a`, which is **not** the census-dry mirror row's digest and is the one to cite.
- `CritC2Kill-4` re-checked the final bytes `1f16e371…` (160 lines) at 2026-10-25T23:43:45Z: all four requested fixes present, `grep -n 'closed list|in each case|every stated route'` → no output, and on these bytes the seven C2 counters read `c1=15 c2=1 c3=1 c4=48`, `census_exit=0`, `harness entries=18 pass=18 exit=0`, `source-recheck S048 exit=0`.
- Both peers' numbers are their measurements; this receipt does not restate them as mine. The only numbers I own are those in §4, §5, §6 and §7, all produced on the bytes named above.

## 12. Routing note — `ScribeGateDraft` is not a kasegi seat

The item named `ScribeGateDraft` as a seat to message when final. Its reply (2026-10-25) reports it reads `/home/vgpnk/Projects/shokunin/souji-shokunin` at HEAD `ba8b54b`, where neither `corpus/knowledge/vendor-third-party-finding-coordination.md` nor `.ufo/waves/round-31/wave1/` exists, and that its Gate draft is a frozen round-26 C2 case set (S128-S132). So the message was mis-addressed by the roster, not mis-delivered content: I told it to take no action and to keep its frozen case set, and I did not ask it to absorb my quote inventory as evidence. No kasegi round-31 gate draft was produced through this seat; if one is required, it is a different instance's path.

## 13. Final downstream state (peer-measured on the bytes `1f16e371…`, not re-run here)

- `ScribeReadmeF15`: frontier row landed with entry cell exactly `knowledge/vendor-third-party-finding-coordination.md` (no backticks), status `admitted`, sources `S048`; coverage-map row added; r31 amendment records 15/15; its measurements: admitted count 15, `frontier-recheck-count.py` → `PASS F15 … ids=S048 exit=0`, `entries=18 pass=18 exit=0`, `git diff --numstat corpus/README.md` 25/0 in one hunk, pre-append head identity preserved. Its `next` cell still matches the final entry (S039/S040 contrast L63-L73; honest-limit sentence L104-L105).
- `ExecExpectedList`: `ls corpus/knowledge/*.md | wc -l` = 44; `corpus/instruments/knowledge-expected.txt` is 46 lines / 44 entries with this entry at line 46, `comm` both ways empty, so no new line was needed; audit `lines=44 total=44 pass=44`, `strict pass=44/44`, `exit=0`. It flags that the expected-list modification is still uncommitted (`M` on top of `5703f9f`) and must be included in the landing commit, or the next audit reds with `unexpected=` this entry — an L1 commit-scope fact, not mine to commit.
- These two lines close every C2 clause that depends on my path: frontier 15, one entry citing S048, harness 18/18 exit 0, census exit 0, source-recheck S048 exit 0.
