# Immunefi Vulnerability Severity Classification System v2.2 — the Smart Contracts severity ladder

source: S051 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ — page heading “Immunefi Vulnerability Severity Classification System - v2.2” (S051.txt:45; document title tag L1), the five-level statement and its list (L46-51), the criterion sentences (L52-56), and the Smart Contracts table (L72-96) in capture corpus/source-snapshots/round-34/S051.txt
verified-at: 2026-10-26
ground: F17
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051   # 18 assertions (Q1-Q18) on the pinned capture, each `occurrences=1` or anchored (Q9/Q17); exits 2 with no capture or manifest and 1 on a quote that moved, so a missing or corrupted source fails closed; a captured-source comparison, not a fresh network verification

## Attribution

Immunefi's own classification system, read as Immunefi's position and nothing wider (Q4). It is not a CVSS mapping (the string `CVSS` does not occur in the capture), not a payout scale (no `reward` or currency token occurs), and not a rule any other programme or reader is bound by.

## Claim 1 — five levels, numbered 5 for Critical down to 1 for None, and the numbering is per asset class

> "At Immunefi, we classify bugs on a simplified 5-level scale:" — S051.txt:46

> "Critical High Medium Low None" — S051.txt:47-51 (one name per line in the capture)

Three tables carry it — `Blockchain/DLT` (L57-71), `Smart Contracts` (L72-96), `Websites and Apps` (L97-148) — each opening with the merged header row `LevelImpact` (L58, L73, L98) and the same five numbered headings: 15 headings in all (FC-1). So `5. Critical-` ranks an impact five-of-five *within its own asset class*; the page prints no ranking across tables, and an impact listed under one class is not thereby present in another (Claim 6).

## Claim 2 — the level is fixed largely by impact; likelihood is taken as an input

> "The development of this scale took into consideration multiple factors that may affect a vulnerability and its likelihood of exploitation" — S051.txt:52

> "finalizes them largely by the impact that they cause" — S051.txt:52

A likelihood argument alone therefore does not set a level: exploitation likelihood and other factors are weighed, then the level is decided largely on impact.

## Claim 3 — the tables classify exploit consequences, under a downgrade-or-reject carve-out

> "The table below is mostly concerned with the consequence of a successful exploit." — S051.txt:53-54

> "the level of the bug may be downgraded to reflect that or rejected." — S051.txt:55-56

The trigger printed between those sentences is a property of the exploit — elevated privileges or uncommon user interaction (L54-55) — not of report quality or researcher reputation. The page names two outcomes, downgrade and rejection, and prints no rule for choosing between them.

## Claim 4 — the Smart Contracts Critical row is an enumerated impact list

> "5. Critical- Any governance voting result manipulation" — S051.txt:74 (heading and first bullet share one line in the extracted text)

A smart-contract finding reaches 5 by producing one of: governance voting manipulation (L74); direct theft of user funds or NFTs at-rest or in-motion, other than unclaimed yield or royalties (L75-76); permanent freezing of funds or NFTs (L77-78); Miner-extractable value (MEV) (L79); unauthorized minting, predictable or manipulable RNG, unintended NFT alteration (L80-82); or protocol insolvency (L83). Three bullets carry the level's economic meaning:

> "Permanent freezing of funds" — S051.txt:77

> "Miner-extractable value (MEV)" — S051.txt:79

> "Protocol insolvency" — S051.txt:83

## Claim 5 — inside the Smart Contracts table the funds boundary is *whose* funds and *how long* they stay frozen

Theft of *any* user funds is Critical (L75) while unclaimed yield and royalties are stolen at High (L84-85); permanent freezing is Critical (L77) while temporary freezing is High:

> "Temporary freezing of funds" — S051.txt:88

A report that says only "funds are at risk" fixes no level from this table: the page asks which funds, and for how long they stay frozen.

## Claim 6 — an impact belongs to one asset class

> "Execute arbitrary system commands" — S051.txt:99 (first `Websites and Apps` Critical bullet)

That phrase occurs once in the capture and only inside the Websites and Apps block (FC-6); the Smart Contracts Critical list (L74-83) does not carry it. The same outcome can appear in both blocks with different wording — `Direct theft of user funds` at L115 (Websites, Critical) against `Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield` at L75 (Smart Contracts, Critical) — so a level is portable only together with its table.

## Claim 7 — Medium and Low are operational and value-preserved outcomes, not smaller thefts

> "Smart contract unable to operate due to lack of token funds" — S051.txt:90 (Medium)

> "Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)" — S051.txt:92 (Medium)

> "Unbounded gas consumption" — S051.txt:94 (Medium)

> "Contract fails to deliver promised returns, but doesn't lose value" — S051.txt:95 (Low; the value-preservation clause is the Low criterion)

> "1. None- Best practices" — S051.txt:96 (None; the identical row closes the Blockchain/DLT table at L71)

Medium absorbs the availability and gas costs the table lists — block stuffing for profit (L91), theft of gas (L93) — and Low is defined by value retained: promised returns fail, value is not lost.

## Honest limit

- **No version-selection statement.** The capture names v2.2 twice (L1, L45) and `v2.3` zero times (FC-2). It prints no rule that a programme chooses which VSCS version applies, so this entry claims none: the round brief's v2.2-versus-v2.3 selector is unstated in these bytes and is recorded as an open item, not as a finding.
- **The extraction flattens the tables.** A level heading shares its line with its first bullet (`5. Critical- …`, L74), continuation bullets are `- ` lines, and the header row reads `LevelImpact` (L58, L73, L98); bullet membership is read from printed order, and a bullet's table from the nearest section line above it.
- **Classification only.** No amount, currency or reward vocabulary occurs (FC-4); nothing here supports a payment figure for any level.
- **A pin, not a live page.** The recheck compares this entry's quotes with the captured bytes; it says nothing about the page after the capture instant.

## Falsifiable checks

Run from the lane root; each prints the count stated here, so any claim above is refutable.

- **FC-1 — three tables, five numbered levels each, no sixth level.** `grep -cE '^[1-5]\. (Critical|High|Medium|Low|None)' corpus/source-snapshots/round-34/S051.txt` → `15`; `grep -cE 'Severe|Moderate' …S051.txt` → `0`.
- **FC-2 — the capture is the v2.2 page and names no other version.** `grep -c 'v2\.2' …S051.txt` → `2` (L1, L45); `grep -c 'v2\.3' …S051.txt` → `0`. An entry asserting a version selector fails FC-2.
- **FC-3 — not CVSS.** `grep -c 'CVSS' …S051.txt` → `0`. Reading this ladder as a CVSS mapping fails FC-3.
- **FC-4 — not a payout scale.** `grep -c 'reward' …S051.txt` → `0`; `grep -c '\$' …S051.txt` → `0`.
- **FC-5 — permanent freezing is level 5, temporary freezing level 4.** `grep -c 'Permanent freezing of funds' …S051.txt` → `2` (L62 Blockchain, L77 Smart Contracts); `grep -c 'Temporary freezing of funds' …S051.txt` → `1` (L88). Scoring temporary freezing Critical, or permanent freezing High, contradicts both counts.
- **FC-6 — an impact belongs to one asset class.** `grep -c 'Execute arbitrary system commands' …S051.txt` → `1`, at L99 inside the Websites block (L97-148), never inside L72-96.
- **FC-7 — the None row is the same string in both blocks that print it.** `grep -c '1. None- Best practices' …S051.txt` → `2` (L71 Blockchain/DLT, L96 Smart Contracts); the manifest's Q17 adds `anchor: 96`, so the count and the intended row are both checked.

## Rejected over-generalizations

1. **"A VSCS level converts to a bounty figure."** Rejected: no amount or currency occurs (FC-4); the page classifies impact, and reward rules are a different document's business.
2. **"The five levels mean the same thing in every asset class."** Rejected: the headings repeat per table and the impact lists differ — arbitrary command execution is Websites-Critical only (FC-6).
3. **"A downgrade is a rejection."** Rejected: the sentence names both outcomes, separated by "or" (L55-56), and the trigger is an exploit property rather than a scope decision.
4. **"Any loss of funds is Critical."** Rejected: unclaimed yield and royalties are stolen at High (L84-85) and temporary freezing is High (FC-5); Critical needs any user funds, or permanence.
5. **"The VSCS is CVSS under another name."** Rejected: the capture contains no `CVSS` string (FC-3) and states its own five-level construction (Claim 1).
6. **"Level None means out of scope."** Rejected: the row reads `Best practices` (L96), and the page prints no scope, acceptance or eligibility consequence for any level.

## What this adds beyond F13 and F15

F13 holds platform severity ladders (a HackerOne policy record, Bugcrowd's VRT) and F15 holds a vendor research programme as an intake route. Neither carries a Web3 asset-class ladder whose levels are enumerated by economic consequence: governance manipulation, MEV, NFT integrity and protocol insolvency are impacts this lane had not recorded, and each is a bullet a smart-contract report can be checked against without leaving the capture.

## Scope and limits

- Pin: `corpus/source-snapshots/round-34/S051.txt` (8502 B, 175 lines, sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`), bound by `corpus/source-snapshots/round-34/manifest.json`, whose record S051 carries that digest, the URL, a strict-UTC `fetched_utc`, and the eighteen Q1-Q18 assertions this entry quotes — sixteen at `occurrences=1`, two at `occurrences=2` with a verified anchor (next bullet).
- **Two quoted bullets occur twice in the capture and are anchor-pinned.** `Permanent freezing of funds` occurs at L62 (Blockchain/DLT) and L77 (Smart Contracts); `1. None- Best practices` at L71 and L96. The manifest pins them with `anchor: 77` and `anchor: 96`, so `source-recheck.py` prints `occurrences=2 anchor=N-ok` — the count and the intended line are both checked, and a capture that drops either line fails the assertion rather than passing on the other.
- `verified-at: 2026-10-26` is when this entry was written and its quotes checked against the pin, not the capture instant (the manifest's `fetched_utc` is the fetch time).
- Documentation only: the capture carries no credential, session or private URL, and this entry quotes no such line (Q6).
