# R47W2SafetyBoundary — integrated-tree safety review (round 47, wave 2)

Seat: safety boundary over the integrated revision `65e19bdb142c90a08103eb4b2af60c71218a920e`
(base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`).
Bounded item: live-target testing, secrets/private URLs, authorization/reward overclaims,
and honesty of the disclosed claim failures in the corpus changes (19 corpus-level files,
all under `corpus/`, `LOG.md`, `SKILL.md`; working tree verified byte-identical to the
integrated revision outside `.ufo/`). Axes (godspeed): depth:verifiability, coverage —
every finding below carries a path:line and an EXECUTED or STATIC tag. This is a
read-only review: no production edits, no git/jj mutation, no delegation, no installs
(RULES.md read; pacman pause respected), no domain fetches by this seat, no reroll of
either target, no mutant battery or selftest. Scratch `/fast/scratch/hyaku/kasegi-r47/R47W2SafetyBoundary/`
exported as receipts into this draft directory and deleted on exit.

## Headline counterexamples

- **H-A (new, undisclosed): the frozen C1 counter is RED at the integrated tree — 10/11, limb L3.**
  Executed: `python3 corpus/instruments/r47-routed-defects.py --root <lane>` →
  `limb L3 (D5) fixed=0 read=corrections-section-present content=0`,
  `routed-defects total=11 fixed=10 unresolved=1 exit=1`
  (receipt: `.ufo/waves/round-47/w2/R47W2SafetyBoundary.draft/gate-routed-defects-integrated.txt`).
  Cause (static + executed): L3 (r47-routed-defects.py:176-183) demands the literals
  "Search log"/"Registry changes" inside the `## Corrections (round 47)` tail of
  `corpus/lessons/round-46.md`; the landed D5 correction writes the hyphenated
  "Search-log"/"Registry-changes" (executed grep counts 0 vs 1;
  `.../draft/l3-token-check.txt`). Every committed L3 mention is a base/mid reading
  (w1 R47ConnCross.md:19, R47CritSever.md:20, R47ExecGateReplay.md:16,48); no committed
  receipt records the final 10/11 state, and LOG.md:2037/lesson disclose only the
  intentional S074-transition refusal as C1's unmet part. The freeze-time kill rule
  ("C1 fails if the counter prints fixed<11/11") therefore fails for a second,
  undisclosed reason. Smallest safe correction: one-line prose addition to the D5
  correction bullet naming the sections unhyphenated, or a counter-errata note;
  C1 stays unmet either way, so this is a disclosure/landing defect, not a reroll trigger.
- **H-B (mechanically corroborated honest failure): frozen C2 gate 6/7 exit 1, H1 red.**
  Executed: `python3 corpus/instruments/r47-f30-gate.py --root <lane>` →
  `gate H1 pass=0 read=rows=29 admitted=29 dup=0`, H2-H7 green
  (`.../draft/gate-f30-gate-integrated.txt`). The only red limb is the frontier count:
  the ZDI enrichment entry exists and passes every quality limb (recheck 10 quotes,
  spans 10/10, census ok) while no F30 row was added — exactly the disclosed C2-unmet
  state ("The proposed independent frontier target is missed", LOG.md:2038). No reroll
  performed; the reading is recorded as evidence only.

## Group A — live-target testing (10 attacks)

1. Capture instrument is GET-only urllib with a declared UA, 32 MiB cap, no POST/auth/cookie code (STATIC: `corpus/instruments/capture-source.py:32,73-79`); it accepts any `--url`, so the documentation-only rule is procedural, not enforced. Verdict: neutral tool; committed round-47 network evidence is exactly the two documentation GETs (attack 2), so no live-target testing occurred.
2. Committed round-47 HTTP evidence = S075 + S076 only (lesson §Gate; `corpus/source-snapshots/round-47/manifest.json` http blocks; `.ufo/waves/round-47/controls/capture-determinism.txt` binds both digests, first==second). EXECUTED: my sha256sum over both committed captures matches the manifest pins (`9dee8161…04e1`, `9bd8ab57…b38`). No third fetch receipt exists in `.ufo/waves/round-47/controls/` (listing inspected).
3. The frozen gates and rechecks are offline: no `urllib`/`socket`/`http` fetch code in `r47-routed-defects.py`, `r47-f30-gate.py`, `r47-mutbat.py`, `r47-counters-selftest.py`, `source-recheck.py` (STATIC grep; subprocess only to local interpreters/bash). EXECUTED: my four instrument runs performed zero HTTP.
4. `live` naming in r47-f30-gate.py could suggest a live-page check; it is `live_lines(raw)` = uncommented entry bytes (STATIC: r47-f30-gate.py:339-343). Verdict: documentation nit, no network; H5 executed on entry+snapshot bytes only.
5. Capture UA contact URL uses the reserved `.invalid` TLD (`shokunin.invalid`, capture-source.py:32) — no real identity/contact domain is embedded (STATIC). Good practice.
6. Corpus boundaries intact: `PROVINCE.md:52` "Live-target testing is refused; this corpus is documentation only." and `corpus/QUALITY.md:19` Q6 (no probing/scanning/login/submission instructions, no credential/session/private-URL/vault material) are unchanged by the base→integrated diff (STATIC diff scope: both files untouched by round 47).
7. LOG.md:2040 wording is carefully scoped: "No domain-facing submission, scanning or probing performed." — it does not make the absolute "no live host contacted" claim that Q6's grounded-in cell (QUALITY.md:19, A3) records as previously falsified, and it is consistent with the two documented GET captures. Verdict: honest wording, no overclaim.
8. S076 capture chrome carries imperative security-product text ("Enable secret scanning" S076.txt:135, "Scan for secrets with MCP" :293) but stays outside the prose window 558-600; EXECUTED: recheck Q1-Q12 OK with anchors 568-600 and counter L9 `spans=47 located=47 failed=0` — no navigation imperative is cited as corpus guidance on the integrated tree.
9. ZDI submission/reward surfaces (`/portal/register/`, `/about/benefits/`) appear only in w1 historical scout files (R47ScoutLeads.md:24-28, grep repo-wide); the integrated `## Leads (unopened)` section (corpus/SOURCES.md:119-124) contains only the REST-API lead — the do-not-open boundary held.
10. Execution hygiene: all seat executions ran in scratch with read-only instrument invocations; scratch deleted after receipts were saved; only `.ufo/waves/round-47/w2/R47W2SafetyBoundary*` files written.

## Group B — secrets / private URLs (9 attacks)

11. EXECUTED credential-signature sweep over all 19 corpus-level changed files (AKIA/ghp_/github_pat_/xox/JWT/Bearer/password=/api_key=/private-key): 0 hits everywhere; the single SKILL.md:677 hit ("one-char `Bearer x`") is pre-round-47 historical probe description, not new content (receipt `.../draft/secrets-sweep.txt`).
12. S075 chrome commits real-party contact addresses `zdi@trendmicro.com` / `media_relations@trendmicro.com` (S075.txt:42,44) — already-public page footer data, not credentials; flagged because they sit inside a capture branded "TrendAI™" (attack 27). STATIC.
13. The only loopback/private URL in the round-47 diff, `https://127.0.0.1/private-synthetic`, lives in the historical w1 sweep control (`.ufo/waves/round-47/w1/R47SentSecrets.draft/sweep-receipt.md`) as a synthetic positive control; grep confirms it is absent from production `corpus/instruments/` (STATIC). No private-URL fixture shipped.
14. EXECUTED scan of S076.txt for token/secret/key/bearer/JWT shapes: only GitHub product prose ("Secret scanning", "GitHub token missing" as a docs status string); no credential-shaped strings.
15. STATIC: `r47-*.py` instruments embed no tokens; constants are sha pins, URLs, and paths only.
16. STATIC: `.ufo/waves/round-47/w2/swarm-registry.json` — its one '@|token|secret' match is this seat's own assignment text; no secrets in wave-2 dispatch metadata.
17. STATIC: `corpus/source-snapshots/round-47/manifest.json` carries only sha pins, URLs and quote records; no secrets.
18. STATIC: `corpus/instruments/entry29-fixed-bytes.md` fixture is an entry copy; 0 credential-signature hits (executed sweep, item 11).
19. Coverage continuity: w1 R47SentSecrets explicitly limited its sweep to an unsealed producer snapshot and required a post-settlement repeat; this seat's Group B sweep over the integrated diff is that repeat for the corpus-level changes (non-corpus `.ufo` wave files remain historical evidence, not production bytes).

## Group C — authorization / reward overclaims (9 attacks)

20. The ZDI entry disclaims authorization in its Limits: "It makes no live-page claim, observation of actual broker conduct, legal conclusion, or authorization to contact or disclose against any target" (STATIC: `corpus/knowledge/zdi-disclosure-policy.md:32`). Present and unweakened at the integrated tree.
21. The S075 scope cell excludes "individual advisory records, reward terms or researcher submission rules" (STATIC: `corpus/SOURCES.md:81`) and the capture agrees: reward/submission vocabulary exists only as chrome ("Submit a vulnerability" :32, "Researcher Rewards" :53, "Sign Up"/"Log In" :10-11,:17-18) outside the pinned body 20-27 (EXECUTED line map; quote-location receipt shows all 10 manifest quotes in-body).
22. EXECUTED grep: no bounty/cash/payment/dollar figures in `corpus/knowledge/zdi-disclosure-policy.md` or `corpus/lessons/round-47.md` — no reward overclaim is possible from the admitted enrichment.
23. The F29 entry's documentation-only limit survived the S076 re-ground: "The entry instructs no advisory creation, no CVE request, no contact with GitHub or any maintainer, and no probing of any repository" (STATIC: `corpus/knowledge/github-repository-security-advisories.md` Limits final bullet; mirrored in fixture `corpus/instruments/entry29-fixed-bytes.md`).
24. "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers" appears only as attributed capture quotes (entry G12 at S076.txt:582; SOURCES scope cell) — attribution, not a corpus authorization claim (STATIC; anchor verified by executed recheck Q4).
25. The D6 anti-overclaim repair holds: the entry now states only S076.txt:599-600 permit publish-without-fix-version and that the :598 imminent-fix case forbids it (STATIC entry Limits bullet; EXECUTED sed of S076.txt:598 matches the quoted sentence; counter L6 `fix-version-cases-corrected` executed green). The base's "permission to publish without a fix" misreading is gone (L4 false-phrase sweep executed green).
26. `corpus/QUALITY.md` R54 (new) codifies "do not weaken B3 or rewrite the frozen predicate to manufacture success" (STATIC) — the anti-overclaim guard for exactly this round's temptation landed intact.
27. **TrendAI™ provenance ambiguity (unresolvable statically):** the committed S075 snapshot brands the stating party "TrendAI™ Zero Day Initiative™" (S075.txt:1,21-27,39,49-50) while its chrome keeps the real vendor's email domain (attack 12); the capture pipeline performs no text substitution (STATIC: capture-source.py:39-53 strips tags/scripts only), so the brand text is as-fetched; this seat performed no live fetch (no domain-target actions), so whether the environment serves this text verbatim is unverifiable here. No older corpus capture of the ZDI policy exists to diff (the S042/S047/S052 "Trend Micro" hits are unrelated Japanese vendor pages — EXECUTED grep: 0 ZDI mentions in those). The entry/SOURCES/README consistently attribute to "TrendAI ZDI", and the entry disclaims live-page claims (attack 20). Smallest safe correction: a manifest/row provenance note that the brand text is as-captured and not verified against the public web.
28. "Admitted" wording drift: LOG.md:2038 says the policy is "admitted as a sourced F02 coordinator case", SOURCES.md:175 says "not an admitted F30 row", lesson §Final Gate says lane decisions are not the independent closure's admit/reject sampling (STATIC). Read together the meaning is consistent (lane acceptance ≠ frontier admission), but a scorer reading LOG alone could over-read admission. Verdict: wording note, no safety defect; registry cells say `mined` (SOURCES.md:80-82 tails, counter L8 demands `mined` — STATIC r47-routed-defects.py:249), which caps the claim.
29. No live-target reward vocabulary was imported from the capture into any entry: the entry's decision rule is a package-check rule ("mark the 120-day start event unknown unless separately evidenced", zdi entry §Falsifiable package rule) — documentation-only, no submission instruction (STATIC; entry :32 closes the same door).

## Group D — honest claim failures and the safe repairs (11 attacks)

30. C1's frozen prose is unmet and disclosed: claims.json C1.after requires "S074 status mined->rejected and used-by -> corpus/lessons/round-46.md"; the integrated tree keeps S074 `mined` with used-by re-pointed (STATIC: `.ufo/waves/round-47/claims.json` C1.after; SOURCES.md:80 tail, :176), and LOG.md:2037 discloses the refusal with the B3 rationale ("rejecting it breaks B3"; R47RevD7 receipts). Honest.
31. C2's frozen target is missed and disclosed: LOG.md:2038, corpus/README.md round-47 block ("No F30 row is admitted"), and counter-errata ("the thirty-row target remains missed") all state it without narrowing the target post-score (STATIC). EXECUTED H1=rows=29 corroborates mechanically (H-B).
32. Freeze integrity: `claims.json` is byte-identical freeze→HEAD (EXECUTED: `git diff 308a2cb..HEAD -- .ufo/waves/round-47/claims.json` empty); the freeze tree carries no round-47 lesson (EXECUTED: `git ls-tree 308a2cb corpus/lessons/` — no round-47.md; sorted listing jumps round-46.md → round-5*). No post-freeze predicate rewriting (anti-overclaim).
33. **New defect (fixable): the integrated disclosure understates the mechanical state — two unmet reasons, one undisclosed.** The lesson/errata discuss only the S074-transition refusal and say C1 "is not fully verified even if all eleven mechanical limbs become true" (counter-errata.md §Claim outcomes); the actual final reading is 10/11 with L3 red (H-A). Impacted axis: depth:verifiability (the disclosure duty of a red frozen counter at the final revision). Smallest safe correction: record the 10/11 reading (receipt already committed under this wave) and land the one-line L3 token fix or its errata note before final measurement.
34. `verified-at` staleness after the re-ground: `corpus/knowledge/github-repository-security-advisories.md:3` says `verified-at: 2026-10-29` while its source line now cites S076 (fetched 2026-10-30T10:35:47Z, manifest) and its row says opened 2026-10-30 (SOURCES.md:82); the fixture `corpus/instruments/entry29-fixed-bytes.md:3` mirrors the stale date. The verification claim predates its evidence by a day. Smallest safe correction: bump `verified-at` on both (current-claim cell, not one of the lesson's immutable source/scope/anchor/teaches cells).
35. REST-API lead identity drift (defect, fixable): lesson:39 uses `…/rest/security-advisories/repository-security-advisories`, SOURCES.md:124 uses `…/rest/security-advisories/repository-advisories`, selftest fixture uses the lesson variant (r47-counters-selftest.py:155); no frozen counter discriminates them (both share the plain-grep prefix). An unopened lead with two spellings weakens the boundary (receipt `.../draft/lead-url-variants.txt`). Smallest safe correction: one URL in lead+lesson, other named as alias or dropped.
36. The safe S074 repair itself checks out: used-by old→new logged (SOURCES.md:176), immutable cells unchanged (base→integrated row diff is the permitted used-by cell only), original capture byte-retained (EXECUTED: `round-46-a2/S074.txt` untouched by the diff), and the frozen counter never demanded rejection (no S074-status limb; STATIC limb list r47-routed-defects.py:11-40) — the freeze-time tension between claims prose ("mined->rejected") and counter (silent) was resolved toward B3 and disclosed, not silently narrowed.
37. Quote honesty: EXECUTED all 22 manifest quotes (10 S075 + 12 S076) locate exactly in their committed captures at their anchors, all inside declared body windows (`.../draft/quote-location.txt`); snapshot shas match manifest pins; snapshot/raw byte fields self-consistent (4701/25321; 19804/582877).
38. Instrument honesty: the pre-freeze H4 docstring-vs-code anchor-count mismatch is already disclosed in `counter-errata.md` with the surviving-witness rule ("A mechanically green integrated tree does not erase these witnesses") — the corpus does not retro-harden or re-present counters as validators (STATIC).
39. Registry discipline: S075/S076 registered `mined` with 90d rechecks and used-by pointing at the two new entries; `corpus/instruments/knowledge-expected.txt` gains exactly the new entry; registry rows 74→76 claimed and consistent with the executed census limb (H7 ok; H6 knowledge=67) — no row-number inflation is presented as admission (EXECUTED H1/H6/H7).
40. The historical boundary is respected: S074 capture, w1 receipts, and prior source captures are untouched by the integrated diff (EXECUTED: `git diff fc8e0af..65e19bd -- corpus/source-snapshots/round-46-a2/` empty; `.ufo` w1 files added once at 82a8bd7/65e19bd and not modified since), matching the seat instruction that prior captures remain historical.

## Executed-verification index (all offline; zero HTTP)

- `python3 corpus/instruments/r47-routed-defects.py --root <lane>` → `total=11 fixed=10 unresolved=1 exit=1` (L3 red; receipt `.../draft/gate-routed-defects-integrated.txt`)
- `python3 corpus/instruments/r47-f30-gate.py --root <lane>` → `fixed=6/7 exit=1` (H1 red by design; receipt `.../draft/gate-f30-gate-integrated.txt`)
- `python3 corpus/instruments/source-recheck.py --manifest … --source S075|S076` → both rc=0, all pinned quotes OK (receipts `recheck-s075.txt`, `recheck-s076.txt`)
- sha256sum of both captures matches manifest; 22-quote location check (receipt `quote-location.txt`); credential sweep over 19 changed files (receipt `secrets-sweep.txt`); L3 token counts (receipt `l3-token-check.txt`); lead URL variants (receipt `lead-url-variants.txt`)
- Read-only git: rev-parse/log/diff/show/ls-tree only; no mutation, no push, no jj op.

## Boundaries and limitations

Static-only items: TrendAI™ verbatim-ness vs the live page (no domain fetch performed, per no-domain-target rule), non-text/encoded secrets (regex sweep bounded, same limitation the w1 secrets seat disclosed), and the historical `.ufo` wave bytes (reviewed as data, not re-validated). The w1 secrets seat's own limits (snapshot not atomic; matcher not an oracle) are inherited where they overlap. Neither frozen target was rerolled; the two gate readings above are evidence records, not attempts to flip outcomes.

Tooling: none installed or updated (operator directive read at /home/vgpnk/.omp/agent/RULES.md; pacman transactions untouched).

Report: .ufo/waves/round-47/w2/R47W2SafetyBoundary.md
