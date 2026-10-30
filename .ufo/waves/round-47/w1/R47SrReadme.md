# R47SrReadme — README-only append draft

Axes: **depth:verifiability**, **coverage**. Draft only; L1 integrates and judges admission. No shared production file changed.

## Landing behavior and artifact

Append the complete bytes of `.ufo/waves/round-47/w1/R47SrReadme.draft/README.append.md` at EOF of `corpus/README.md`; do not rewrite or insert among existing lines. The existing final amendment is `corpus/README.md:693`. Preserve any trailing blank line as well. The artifact starts with a newline, contains the requested round-47 heading, a coverage-map table, exactly one F30 frontier row, source digest/access details, F02/F15 contrast, scope limits, and the complete historical attribution chain. Use this README-only artifact **instead of**, not in addition to, block D of `R47SrRegistry.md`; appending both would duplicate F30.

## Proposed EOF addition

```markdown

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
```

## Evidence and provenance

All following paths are lane-relative.

- Append shape: `corpus/README.md:401-424` (round 37) and `:671-693` (round 46 attempt 2) provide the R6 append convention, both table shapes, historical amendment and separate lost-domain denominator. Every prior round attribution in the draft comes from the complete existing amendment at `:693`, corroborated through F20 by `:418-424`; no prior attribution is invented.
- Entry destination: `.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md:1-7,24-34` supplies the matching entry identity, dated provenance, decision rule and limits. Destination also appears in the registry draft `R47SrRegistry.md:25,41,53,57`.
- Capture provenance: `corpus/source-snapshots/round-47/manifest.json:6-23` pins S075, URL, access UTC, complete sha256, 60 lines and body range. Its ten quote records are `:25-74`. This report reads those records; it does not claim to have executed source-recheck or recaptured the page.
- Policy support: `corpus/source-snapshots/round-47/S075.txt:23` supplies the contact thresholds and conditional fifteen-business-day fallback; `:24` supplies responsive-vendor interval, conditional limited advisory and extension authority without specifying a start event; `:25` supplies the faulty-patch tiers; `:26` supplies acquired-vulnerability non-suppression.
- Existing comparison ground: `corpus/knowledge/coordinated-disclosure-timelines.md:7-17` already requires policy attribution, trigger, interval, publication conditions and documented exceptions. `corpus/knowledge/vendor-third-party-finding-coordination.md:114-120` expressly says its pinned page states intake routes/roles but no timeline. Therefore the draft does not present the missing-trigger discipline itself as novel.

## Gates and do-nothing discrimination

Observed read-only count command, executed from the lane:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && printf 'frontier_rows=' && grep -cE '^\| F[0-9]+ \|' corpus/README.md && printf 'knowledge_entries=' && find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l && printf 'sources_rows=' && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
```

Printed:

```text
frontier_rows=29
knowledge_entries=66
sources_rows=74
```

These are current unintegrated counts, not observed target counts. The unchanged README is the do-nothing control: it retains 29 rows, unlike the draft's additional single F30 row. Frozen inherited counter receipt `.ufo/waves/round-47/controls/c2-base.txt:1-9` records rows=29, entry absent, S075 absent, `f30-gate fixed=1/7 exit=1`; no counter was rerun by this seat. Freeze-tree 2/7 and final target 7/7 are contract data from `claims.json`, not passes earned by this draft. The proposed 30/30 and 67-entry amendment becomes factual only after corresponding integration and acceptance.

L1's remaining checks: pure-prefix preservation of existing README bytes, exactly one F30 row across integrated additions, matching entry/S075 registry destination, frozen C2 counter, census, and independent semantic/source review. No integrated checks, live-page opening, full battery or 43-case selftest were run here. Known disclosed battery gaps remain C1 16 uncaught of 35 mutants and C2 18 uncaught of 21; baseline_failures=0 is inherited receipt information, not this seat's observation.

## Findings and limits

- F02 overlap remains disputed. Peer `R47RevNovelty.md:15` states: **“Strongest reduction attack: keep the ZDI conditional timeline as another F02 policy comparison.”** This report preserves that challenge for canonical judgment; the draft's narrower non-suppression ground is a proposed distinction, not an independently established admission result.
- The README-only artifact supersedes the overlapping registry-seat README block for integration; it adds the user-required full historical chain instead of only “F01-F29 as previously recorded.” Do not append both artifacts.
- Touched surfaces: only this findings file and the owned `R47SrReadme.draft/README.append.md`. Production README, sources, entry, instruments, judge, git/jj/index, fleet root and siblings remain untouched by this seat.
- No scratch directory, clone, fixture, tool installation, service change, or heavy pass was needed. No scratch remains. Two finite Bash calls were automatically backgrounded by the harness while delivering IRC; neither requested background execution; both completion receipts arrived before this report. The mkdir command exited successfully with no output.
- Out of scope: C1 D5-D8 repairs, source registry/Search-log integration, entry integration, score changes, adoption, commits, publishing and wave-2 attacks.

Self-evaluation: accuracy 4 (capture grounded; admission unexercised), completeness 4 (requested draft supplied; integration belongs to L1), clarity 4 (full historical chain is necessarily long), actionability 4 (append-ready artifact; overlap judgment remains), conciseness 4 (report duplicates artifact intentionally to put requested draft at the named Report path). Overall 4.0. Highest-impact next step is L1 integrated verification followed by independent F02 novelty adjudication. Would the user agree: this is a complete scoped draft, not a claimed passing admission.

Report: .ufo/waves/round-47/w1/R47SrReadme.md
