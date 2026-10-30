
## Round-47 admission — coverage map row and Frontier F30 (appended 2026-10-30)

The coverage map and frontier table above are not edited in place (R6). The round-47 entry
`corpus/knowledge/zdi-disclosure-policy.md` (F30, source S075) records the Zero Day Initiative
(ZDI) disclosure policy — the third-party broker's acquisition-disclosure timeline. Its
responsive-vendor branch allows four months (120 days) without stating the clock's start
event; its exhausted-contact branch permits a public advisory fifteen business days after
initial contact; extensions to the 120-day timeline are rare and at ZDI's sole discretion.
At deadline, the limited advisory with mitigation is conditional on vendor nonresponse or
inability to provide a reasonable explanation for the missing fix. Incomplete or faulty
patches have separate conditional 30/60/90-day windows. The acquired-vulnerability rule
states that a finding will not be kept quiet because the product vendor declines to address
it. This is the captured policy's statement, not an observation of actual broker conduct.

F02 (`corpus/knowledge/coordinated-disclosure-timelines.md`) supplies the existing discipline
for comparing attributed coordinator timelines, including leaving a date unknown when its
trigger is unstated. F15 (`corpus/knowledge/vendor-third-party-finding-coordination.md`)
holds Microsoft's vendor research programme's third-party intake routes and coordinator
role; its pinned page supplies no timeline. F30 applies F02's timeline discipline rather
than inventing a new general clock rule. Its narrower acquired-finding ground is ZDI's
stated refusal to suppress an acquired vulnerability merely because the vendor will not
address it (`S075.txt:26`), not merely another coordinator's interval values.

Evidence is limited to the policy page text captured at `S075.txt:20-27`. Individual
advisories, reward rules, the researcher submission page and the linked blog's additional
details are outside this admission. This policy grants no testing or disclosure
authorization, establishes no universal vendor deadline, and does not make the capture a
statement of present network freshness.

| Area | Entry | Source basis |
|---|---|---|
| Zero Day Initiative disclosure policy: broker-controlled acquired-vulnerability timeline and non-suppression commitment (round 47) | `corpus/knowledge/zdi-disclosure-policy.md` | S075 — ZDI's own Disclosure Policy, https://www.zerodayinitiative.com/advisories/disclosure_policy/, opened 2026-10-30 (capture UTC 2026-10-30T10:35:37Z); `corpus/source-snapshots/round-47/S075.txt`, policy body lines 20-27, sha256 `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`; access record and ten located quotes in `corpus/source-snapshots/round-47/manifest.json` |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F30 | Zero Day Initiative disclosure policy — the third-party broker's acquisition-disclosure timeline and acquired-vulnerability non-suppression commitment | admitted | corpus/knowledge/zdi-disclosure-policy.md | S075 | Keep this broker's conditional policy separate from a universal vendor clock: the responsive branch allows "four months (120 days) to address the vulnerability" (`S075.txt:24`) without a stated start event; the exhausted-contact fallback is "fifteen business days after the initial contact" (`S075.txt:23`). Preserve publication conditions, rare sole-discretion extensions and faulty-patch tiers. F02 supplies timeline comparison, F15 vendor intake; the acquired-finding non-suppression rule is at `S075.txt:26`. Re-open the policy before relying on it; advisories, reward rules and researcher submission rules stay out. |

[r47 amendment, appended 2026-10-30] The round-46 attempt-2 amendment above records its own
29/29 state and is retained as history (R9): at round 47 the frontier stands at **30/30 admitted**
— F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26, F12 at round 28,
F13 at round 29, F14 at round 30, F15 at round 31, F16 at round 33, F17 at round 34, F18 at
round 35, F19 at round 36, F20 at round 37, F21 at round 38, F22 at round 39, F23 at round 40,
F24 at round 41, F25 at round 42, F26 at round 44, F27 at round 45, F28 at round 46, F29 at
round 46 (attempt 2), F30 at round 47; rounds 27, 32 and 43 admitted no frontier row. This is
one additional admitted frontier and the 67th knowledge entry, not a coverage-ratio move:
(20+30)/(20+30) remains 1.000. The lost-domain denominator remains 0/18; the frontier count
is separate.
