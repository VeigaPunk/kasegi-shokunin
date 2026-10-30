# R47ScoutF02 — F02/F15 contrast evidence

Axes: depth:verifiability; coverage. Read F02 (44 lines) and F15 (172 lines) fully; checked their quoted source sections and S075:21-27. No production edits, commands/counters, installations, clones or scratch artifacts.

## Findings — observed

1. **F02 requires all five fields, with an important qualification (high confidence).** `corpus/knowledge/coordinated-disclosure-timelines.md:7`: “A disclosure timeline in a report or case record must name the policy or coordinator, the event that starts its clock, the stated interval, the patch/publication relationship, and any documented extension or exception.” It requires **policy OR coordinator**, not necessarily both; extensions are conditional on documentation. Lines 9 and 16 require unknown dates when policy/trigger is unidentified; lines 11-15 enumerate the checklist, and line 17 says “Do not transplant CERT/CC or Project Zero intervals into another policy record.” Lines 29-30 require retaining the actual policy and its exceptions/patch trigger.

   Its quoted ground supports a policy-specific synthesis, not a source verbatim five-field mandate: `corpus/source-snapshots/round-24/S003.txt:202-205` allows “a fixed period, a minimum or maximum, or a negotiated default starting point” and collaborative embargo adjustment; `S004.txt:24-29` specifies CERT/CC's 45 days after initial report regardless of patches, subject to circumstances; `S005.txt:17-23` specifies initial reporting, conditional 30-days-after-fix publication and the developer-commitment grace condition. F02's rule is the entry's recording discipline, not a universal legal deadline (entry:37-38).

2. **F15 declines clock inference from S048 specifically, not every vendor programme categorically (high confidence).** Exact contrast citations:
   - `corpus/knowledge/vendor-third-party-finding-coordination.md:116-120`: “The page states intake routes and roles. It does not state the coordination agreements, a timeline, a reporting address or a per-vendor process” and “nothing establishes that the affected vendor was told, or when.”
   - Same file:133: “Any \"MSVR's N-day embargo\" or \"report it to MSVR at ⟨address⟩\" line cannot be supported from S048.”
   - Same file:150-154 rejects a finder coordinated-disclosure obligation: “it states no obligation, no deadline and no address”.
   - Same file:164-169 bounds this to one pinned page and disclaims upstream freshness.

   Direct body check: `corpus/source-snapshots/round-31/S048.txt:31-35` enumerates three arrival routes and Microsoft's affected-vendor/finder/coordinator roles. L34 says “under accepted Coordinated Vulnerability Disclosure practices”; L35 says “under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.” Neither states a numeric disclosure clock. Thus a contrast saying F15 prohibits reading clocks from *all* vendor programmes would over-generalize its explicit one-page scope (entry:9-11).

3. **S075 contains distinct acquired-vulnerability handling, despite acknowledged coordination/timeline overlap (observed evidence; distinct-frontier judgment is inference, medium-high confidence).** Exact new ground:
   - `corpus/source-snapshots/round-47/S075.txt:22`: “Simultaneous to the vendor notification, protection filters may be distributed to TrendAI™ customers through approved channels.”
   - Same file:23: non-acknowledgment after five business days triggers second contact, then an additional five business days permits an intermediary; exhausted reasonable contact permits public advisory “fifteen business days after the initial contact.”
   - Same file:24: “If a vendor response is received within the timeframe outlined above” then four months (120 days) to address with patch/corrective measure; limited advisory under the stated end-of-deadline condition; extensions at ZDI's sole discretion “only in rare circumstances.”
   - Same file:25: faulty/incomplete-patch disclosures get conditional 30/60/90-day tiers, not a universal original-report clock.
   - Same file:26: “In no cases will an acquired vulnerability be \"kept quiet\" because a product vendor does not wish to address it.” Also offers public disclosure with effective workarounds if the vendor cannot/will not patch, and plans publication of a communication summary.

## Contrast text F30 can cite

“F02 already requires the policy/coordinator, trigger, interval, patch/publication relationship and documented exceptions (`corpus/knowledge/coordinated-disclosure-timelines.md:7-17`); F30 applies that existing discipline rather than adding a generic timeline rule. F15 records a vendor's own third-party-finding intake routes and coordinator seat (`corpus/knowledge/vendor-third-party-finding-coordination.md:19-39,48-59`) but expressly cannot derive an MSVR clock from its page (`:116-120,133`). S075 instead records ZDI's acquired-vulnerability policy: contemporaneous customer protection distribution (`corpus/source-snapshots/round-47/S075.txt:22`), contact-escalation and conditional disclosure branches (`:23-25`), and refusal to keep an acquired vulnerability quiet merely because its vendor will not address it (`:26`).”

## Do-nothing discrimination and limits

**Control: leave F02/F15 unchanged and add no F30/S075 policy account.** That control retains the five-field checklist, CERT/CC/Project Zero examples and MSVR intake/roles, but neither fully read entry supplies ZDI's acquired-vulnerability non-suppression, customer-filter timing or escalation/tier branches. Merely renaming their generic coordination/timeline material as F30 would double-count; explicitly documenting those S075-specific commitments provides the distinguishing ground. This is a textual control comparison, not an executed counter result.

Do not call 120 days “after acquisition”: S075:24 conditions the allowance on timely vendor response but gives no explicit acquisition-date epoch. The word “acquired” at :26 supports acquired-vulnerability handling, **not** purchase mechanics, payment, acquisition date, or a measured real case. No live-policy fetch, hash/manifest recheck, corpus-wide uniqueness proof, gate, or mutation battery was run; known survivor gaps remain unassessed by this seat. F02/F15 overlap is assessed only for the assigned two entries. `xd://lsp` discovery returned “No such tool”; this Markdown source assessment uses literal located text, not semantic-reference proof.

Self-evaluation: accuracy 4/5 (pinned text only, no freshness/hash recheck); completeness 4/5 (all three assigned questions covered; no corpus-wide uniqueness claim); clarity 4/5 (explicit observed/inference split; citations require opening files); actionability 4/5 (ready contrast paragraph, not an integrated F30 draft); conciseness 4/5 (some quotations repeated for integration). Overall 4.0/5. Highest-value improvement is integration-time source-pin verification, without broadening this seat's two-entry contrast into a uniqueness audit. Would the user agree? Expected yes: scope, control and unrun checks are explicit.

Report: .ufo/waves/round-47/w1/R47ScoutF02.md
