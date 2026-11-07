# Round 86 — lesson (kasegi, attempt 1)

Read first: the r85 closure (admitted), `corpus/lessons/round-85-verifier-spotcheck.md` (routed defects 1–4) and `corpus/lessons/round-85.md`. Base `d7296645c2cd9f631329fa8e2f38328a4c9c89a5`, freeze `252df0c90c066d83d229e3107811a6bc05e8feed`. The frozen claims, predicates, kill rules and executed controls are in `.ufo/waves/round-86/claims.json` and `.ufo/waves/round-86/controls/`. One v1 wave `w1` ran 12 seats; the reports are under `.ufo/waves/round-86/w1/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; the claim reads resolve.py's own classification over a new scope).** The frozen map `.ufo/waves/round-86/c1/repair-map.json` repoints 203 distinct bare snapshot citations in `corpus/knowledge/*.md` (each `S<digits>.txt` with an optional `:N`/`:N-M` anchor, GONE at base, whose bare name is the basename of exactly one tracked lane file under `corpus/source-snapshots/`, with every anchor inside that file) to their full lane paths. The resolve.py meter over the knowledge scope moves from 398/1721 (23.13 %) to 596/1716 (34.73 %); counter `.ufo/waves/round-86/c1/knowledge-meter.py`, limbs M1–M6.
  - These are 203 distinct tokens, not 203 occurrences (r85 routed defect 3); they span 292 changed lines in 14 knowledge files.
  - 89 GONE bare snapshot tokens are excluded because their basename is not unique among tracked files (S029, S040, S041, S069, S100, S102; `.ufo/waves/round-86/c1/excluded.json`).
  - Qualifier carried from r85 (CriticClaims A1): this is an internal-citation repoint, so external RESOLVES do not move and the integer score is held at 4.
- **C2 — coverage, held at 8; capability extension of `priced-claim-package`.** The six-file practice package `corpus/practice/curl-ibb-h1-1997312/` prices the payer side of CVE-2023-28319 from HackerOne IBB report 1997312 (S122) and the curl lead developer's end-of-bounty post (S123), with S120/S121 and the S052 KEV capture reused. It passes the frozen subject-bound counter `.ufo/waves/round-86/c2/e2e-check.py` (E0 subject binding answers r85 routed defect 1; the frozen B3-class wrong-subject controls fail). It is the round's sourced claim.

## Outcome

- **C1:** the frozen predicates P1–P4 hold at the landing `fdb5f4af` (`.ufo/waves/round-86/l1/c1-landing-r86.txt`: `base=398/1721 after=596/1716 target=596/1716 keys=203`, M1–M6 pass, rc 0; instrument sha256 10/10 OK; only `corpus/knowledge/` changed; SKILL density 273.2). ReviewC1Semantics Finding 1 then showed that 4 of the 203 keys (`S020.txt`, `S021.txt`, `S023.txt`, `S025.txt`) sit inside a quotation of the round-40 manifest record (`path` field), whose stored value is the bare basename; the repoint made those four sentences misquote the record. Commit `e73c1f94` restores the four lines to the base bytes; the lane tip reads 596/1720 (`.ufo/waves/round-86/l1/c1-correction-r86.txt`). The verdict is the operator's: frozen predicates met, with that disclosed semantic qualifier and CriticClaims' "nominal in class" qualifier.
- **C2:** killed as frozen. The captured S122 carried two presigned profile-picture URLs with AWS STS session-token material; the r43 gate's R-NOSECRET refuses those bytes (E1) while E2 requires exactly those bytes, so P1 and P2 cannot both hold (ExecC2Package, ReviewC2Package F-1, CriticClaims B1, MutC2Counter satisfiability probe). The package was still integrated after a post-freeze redaction and passes the gate and the counter (`.ufo/waves/round-86/l1/c2-postfreeze-r86.txt`), which is reported as post-freeze evidence, not admission.

## Gate

### S122 — HackerOne report 1997312, JSON record (admitted, used by the package)

- **URL:** https://hackerone.com/reports/1997312.json, HTTP 200, final URL unchanged.
- **Accessed:** 2026-11-07.
- **Capture:** `corpus/source-snapshots/round-86/S122.txt`; captured sha256 `ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1` (9131 bytes, freeze `252df0c9`), redacted after the freeze to sha256 `08cab370e7f153d051719bfe098cb140d0d68e9da99e27caacfa0b4228a72eb5` (5361 bytes; the manifest's `redaction` block records both).
- **Located quote, S122.txt:1:** `"handle":"ibb"`. Also on that line: `"has_bounty?":true` and "The original submission can be found here: https://hackerone.com/reports/1913733".
- **Row change (old → new):** status `queued` (freeze) → `mined`; used-by `—` → `corpus/practice/curl-ibb-h1-1997312/report.md`; scope cell "not the bounty amount, which the record leaves null" → "not a bounty amount: the record carries no bounty-amount field" (ReviewC2Package F-5).

### S123 — The end of the curl bug-bounty, 2026-01-26 (admitted)

- **URL:** https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/, HTTP 200.
- **Accessed:** 2026-11-07.
- **Capture:** `corpus/source-snapshots/round-86/S123.txt`, sha256 `22a7d5bed4d4081db7e94e4c788a5aaf12ed8dc8f7607536ef4ad36828de4ab5`, 143 lines.
- **Located quote, S123.txt:16:** "the awesome Internet Bug Bounty project, which has paid the bounties for us for many years". Also pinned: :13 "It officially stops on January 31, 2026." and :27 "We no longer offer any monetary rewards for security reports".
- **Row change (old → new):** status `queued` → `mined`; used-by `—` → `corpus/practice/curl-ibb-h1-1997312/report.md`.

Registry 121 → 123. Both rows flip the round-85 deferred leads. **Independent re-open:** ScoutSources re-fetched S122, S123 and S120 live (all HTTP 200) and found every manifest quote once; S122 is not byte-reproducible (per-request presigned URLs and a drifting disclosure field), S123 and S120 are (`.ufo/waves/round-86/w1/ScoutSources.md` §1–2).

### Deferred and rejected this round

- **Deferred (not rejected):** curl's `docs/BUG-BOUNTY.md` at commit `435acbd379` (https://raw.githubusercontent.com/curl/curl/435acbd379730eab3beb5dbb6c5027001ece6e1d/docs/BUG-BOUNTY.md, HTTP 200 via ScoutSources): "The actual monetary reward amount is decided and paid by the Internet Bug Bounty." It corroborates `payer` and `reward-at-disclosure` and changes no field. Reason: no landed claim rests on it (CORPUS rule 4). Flip condition: the round-87 re-freeze of the package cites it for the payer field.
- **Rejected as evidence for this 2023 award:** the IBB 80/20 finder/project split ("providing 80% to the finder and 20% to the open-source project", hackerone.com/internet-bug-bounty, archived 2024-08-13 via arquivo.pt, HTTP 200). Reason: ScoutSources found the sentence absent from the 2023-08-02, 2023-11-19 and 2024-01-25 captures and present from 2024-07-27, so it is not the rule in force at the 2023-05-17 disclosure; the package states that no capture shows the split. Flip condition: a capture dated on or before 2023-05-17 that states the split.
- **Still rejected:** third-party CVSS for this CVE (round-85 reason: S121 says the vendor sets none).

### considerthese and assimilation

- **considerthese:** no still-unimplemented proposal fits C1/C2 (`.ufo/waves/round-86/w1/ConnectorOverlap.md` §3).
- **Assimilation: none.** Lane 123 ids, staged 94, collisions 93 (none identical: the staged file predates the lane's S031–S123 expansion); the guard proof on an indented `  | S002 |` row gives a nonempty set (`.ufo/waves/round-86/w1/ConnectorOverlap.md` §2). The r77 L0 question is still open.

## Mistakes

**M86-1 — class `planned-tranche-wrong-repair-class`.**

- **What happened:** the round-85 SCORECARD "Planned round 86" row routed a "second repair-map tranche from ExecC1Hunt's 31 candidates". All 31 entries of `.ufo/waves/round-85/w1/ExecC1Hunt-r86-candidates.json` carry `rule` `B:split-first-resolving-word`: they are command-invocation strings (`bash corpus/instruments/r36-closure.sh --selftest`), not citations. Rewriting them changes a command, not a reference, so the planned tranche could not be landed as a repair. Round 86 rebuilt C1 on another scope instead. The same class reached the round-86 map in a narrower form: 4 keys were quoted manifest field values (ReviewC1Semantics Finding 1).
- **Evidence:** `.ufo/waves/round-85/w1/ExecC1Hunt-r86-candidates.json` (31/31 rule B); `SCORECARD.md` Round 85 "Planned round 86".
- **Captured-by:** none. No QUALITY row read what kind of rewrite a planned tranche proposes.
- **Fix:** QUALITY R137 with `.ufo/waves/round-86/l1/repair-class-check.py`.
- **Shown able to fail:** `.ufo/waves/round-86/l1/r137-check-r86.txt` prints `candidates=31 qualifying=0 verdict=FAIL exit=1` on the ExecC1Hunt list and `PASS` on the round-85 (18/18) and round-86 (203/203) maps. It does not catch the quoted-field class; that needs the semantic read, which stays required.

**M86-2 — class `credential-material-captured-and-pushed`.**

- **What happened:** the L1 captured https://hackerone.com/reports/1997312.json with `capture-source.py` and committed it in the freeze `252df0c9`, which `jj-lane.sh` pushed. The JSON held two presigned profile-picture URLs with a HackerOne-issued AWS STS session token (`X-Amz-Credential`, `X-Amz-Security-Token`; `X-Amz-Date` 2026-11-07T00:58:29Z, `X-Amz-Expires` 3600 s), so the token was live when pushed. The same shape was already in round-85 receipt `.ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json`. Three seat files copied it again.
- **Captured-by:** the r43 gate's R-NOSECRET pattern catches it, but it scans packages, and no rule ran it over a capture before the freeze commit.
- **Fix:** every capture file is scanned with the gate's `SECRET_PATTERNS` before its first commit; at the tip the capture, the r85 receipt and the seat copies are redacted (`.ufo/waves/round-86/l1/redact-presigned.py`, `.ufo/waves/round-86/l1/redact-presigned-r86.txt`). History is unchanged (no force-push); L0 question filed.
- **Shown able to fail:** the gate prints `R-NOSECRET verdict=fail ... first=evidence/S122.txt,shape=credential` on a package holding the captured bytes (`.ufo/waves/round-86/w1/ExecC2Package-receipts/gate-final.txt`) and `hits=0` after the redaction (`.ufo/waves/round-86/l1/redaction-scan-r86.txt`).

**M86-3 — class `no-full-positive-control-before-freeze`.**

- **What happened:** the C2 freeze ran the positive control in `--pricing-only` mode only. A full-package positive control over the frozen S122 bytes would have printed `E1 FAIL` and shown the frozen predicate unsatisfiable before the freeze. The pre-freeze `b3` control did print `gate_rc=1` in `.ufo/waves/round-86/controls/c2-controls-r86.txt`, but nobody read it as a positive-path failure.
- **Captured-by:** none; the round-85 freeze had the same shape and passed only because S119 carried no token.
- **Fix:** routed to round 87: a capability claim's freeze includes one full-path positive control built from the frozen inputs, and its rc 0 is in the freeze receipt.

## Routed-defect disposition (r85 spot-check §6)

| # | r85 routed defect | r86 disposition |
|---|---|---|
| 1 | e2e counter does not bind subject; wrong-subject control must fail | Partly answered: the r86 counter adds E0 (heading, report URL, stray report ids), duplicate keys, one Pricing section and a quote floor; the frozen `b3-wrong-subject` controls fail on E0. CriticClaims B2: a wrong body still passes once heading, URL and Pricing are swapped, so E0 binds labels, not the body. Carried. |
| 2 | Re-review after CHANGES-REQUESTED not recorded | Recorded honestly: `status.json` says the fixes were applied by the L1 and no re-pass ran. |
| 3 | "distinct" wording | Answered: the C1 claim counts distinct tokens and states the 292 changed lines separately. |
| 4 | Census of record stale | Carried: not regenerated (full census ~13 GB with ~9 lanes live). |

## Routed to round 87

- Re-freeze the C2 package claim with a full-package positive control (M86-3); cite the curl `BUG-BOUNTY.md` lead for the payer field.
- Knowledge tranche 2: the excluded tokens whose real snapshot is unique once `.ufo/` copies are discounted (ReviewC1Semantics routed candidate 1); exclude quoted manifest fields.
- Counter survivors: MutC1Counter (24/30 killed with its extra probes, 6/30 by the frozen controls alone) and MutC2Counter (15/39 killed).
