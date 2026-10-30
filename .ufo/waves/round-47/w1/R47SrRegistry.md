# R47SrRegistry — verbatim landing blocks

Axes: depth:verifiability; coverage. Draft only; L1 owns integration. Apply only fenced `markdown` contents below, never this report's instructions, receipts or fences.

## Insertion positions (base fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8)

Read-only `git show fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8:corpus/SOURCES.md` and `git show fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8:corpus/README.md` supplied the base bytes (tool artifacts `artifact://30050`, `artifact://30020`).

1. SOURCES registry: insert block A after S074 at base `corpus/SOURCES.md:80`, before blank :81 and `## Paths` :82. S076 belongs immediately after S075 when the D7 owner integrates it.
2. Search log: insert block C after the F29 bullet at base :121 and its closing fence :122, before `## Leads (unopened)` :124. The closing fence is D5 scaffold, not part of a legitimate search log; after D5 removes scaffolding, append C immediately after the retained F29 bullet, outside every fence.
3. Registry changes: append block B after the retained S074 and capture-directory bullets, base :183-184, discarding their surrounding D5 scaffolding and closing fence :185. Do not append inside that fence.
4. README: append block D after base EOF `corpus/README.md:694` (last nonblank line :693, r46 attempt-2 amendment). D contains the sole F30 row; do not also insert it into the original Frontier table.

SOURCES line numbers shift when D5 removes scaffolding and D7 adds S076. The named section and retained bullet/row text, not post-edit absolute line numbers, identify each insertion. README's old admission text is historical; this seat does not rewrite it.

## A — S075 row (11 cells)

```markdown
| S075 | TrendAI Zero Day Initiative (ZDI), Disclosure Policy — https://www.zerodayinitiative.com/advisories/disclosure_policy/ | docs | A | ZDI's own stated disclosure policy for acquired vulnerabilities and product-vendor coordination; not individual advisory records, reward terms or researcher submission rules | lines 20-27 of corpus/source-snapshots/round-47/S075.txt (sha256 9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1, 60 lines, 4701 bytes): policy heading and body; no-response contact sequence L23, conditional 120-day window and rare extensions L24, faulty-patch tiers L25, acquired-vulnerability publication rule L26 | ZDI states that an acquired vulnerability will not be kept quiet merely because the product vendor declines to address it. | mined | 2026-10-30 | 90d | corpus/knowledge/zdi-disclosure-policy.md |
```

## B — Registry changes bullet

```markdown
- S075 row added: new row (id `S075`, kind `docs`, tier A scoped to ZDI's own stated disclosure policy for acquired vulnerabilities and product-vendor coordination only, status mined, opened 2026-10-30, recheck `90d`, used-by `corpus/knowledge/zdi-disclosure-policy.md`), anchor pinned to the round-47 capture `corpus/source-snapshots/round-47/S075.txt` (sha256 `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`, 60 lines, 4701 bytes: policy heading L20, scope L21, contact routes L22, no-response sequence L23, conditional 120-day window and rare extensions L24, faulty-patch tiers L25, acquired-vulnerability publication rule L26, official-advisory location L27). Rule-1 Gate quote grounding `teaches` (20 words): 'In no cases will an acquired vulnerability be "kept quiet" because a product vendor does not wish to address it.' (`S075.txt:26`; recorded in `corpus/lessons/round-47.md` Gate). Access 2026-10-30 (manifest `fetched_utc` 2026-10-30T10:35:37Z, HTTP 200, final URL equals the row URL). This addition alone takes registry rows 74 → 75; C1's separately attributed S076 addition takes the round-end total to 76. No pre-existing row status, recheck or used-by cell is changed by S075; the S074 changes belong to C1's D7 correction, not this addition (R8).
```

## C — Search-log bullet

```markdown
- Zero Day Initiative disclosure-policy sweep (round 47, frontier F30); question: does ZDI's own policy add the third-party broker's acquired-vulnerability disclosure rules beyond F02's attributed coordinator-timeline comparison and F15's vendor third-party intake programme; where: the lane's `corpus/knowledge/`, `corpus/SOURCES.md` and `corpus/README.md` before integration, screened for `zero day initiative|zerodayinitiative`, `zerodayinitiative\.com/advisories/disclosure_policy|TrendAI|five business days|fifteen business days`, and the separate acronym `ZDI`, plus the fixed first-party policy https://www.zerodayinitiative.com/advisories/disclosure_policy/ captured as `corpus/source-snapshots/round-47/S075.txt`; date 2026-10-30; identified 1 policy document, screened 1, included 1 (S075), excluded 0. The read-only regex-search tool returned no matches for each of the first two patterns over that bounded lane scope; the separate `ZDI` sweep returned one line, the round-43 advisory-pair search record in SOURCES, not disclosure-policy text. Reproducible shell spellings are `grep -rniE 'zero day initiative|zerodayinitiative' corpus/knowledge corpus/SOURCES.md corpus/README.md`, `grep -rniE 'zerodayinitiative\.com/advisories/disclosure_policy|TrendAI|five business days|fifteen business days' corpus/knowledge corpus/SOURCES.md corpus/README.md`, and `grep -rniE 'ZDI' corpus/knowledge corpus/SOURCES.md corpus/README.md` (these shell equivalents are not separately executed receipts). The policy's conditional 120-day vendor window has no stated start event; the fifteen-business-day fallback has an initial-contact anchor; faulty-patch disclosures have their own 30/60/90-day tiers. Stop: the fixed first-party policy and its ten located manifest quotes answer this bounded question. Individual advisories, reward terms, researcher submission rules and linked blog details are not included; this is not an exhaustive web search or proof that every existing entry is semantically disjoint.
```

## D — README EOF admission block (contains F30 exactly once)

```markdown

## Round-47 admission — coverage map row and Frontier F30 (appended 2026-10-30)

The coverage map and frontier table above are not edited in place (R6). The round-47 entry
`corpus/knowledge/zdi-disclosure-policy.md` (F30, source S075) records ZDI's own disclosure
policy for acquired vulnerabilities and product-vendor coordination. The policy gives a
conditional four-month (120-day) window without stating its start event, a no-response
contact sequence ending in a possible public advisory fifteen business days after initial
contact, rare extensions at ZDI's sole discretion, limited-advisory publication at the
conditional deadline, and separate 30/60/90-day windows for incomplete or faulty patches.
Its acquired-vulnerability publication rule does not let a vendor's unwillingness to fix
silence the finding. Evidence is limited to the captured policy body, not individual
advisories, reward terms, researcher submission rules or the linked blog's details.

| Area | Entry | Source basis |
|---|---|---|
| ZDI disclosure policy for acquired vulnerabilities: broker-controlled vendor windows, no-response fallback and faulty-patch tiers (round 47) | `corpus/knowledge/zdi-disclosure-policy.md` | S075 — ZDI's own Disclosure Policy, opened 2026-10-30; capture `corpus/source-snapshots/round-47/S075.txt`, policy body lines 20-27, sha256 `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`; ten located quotes and access record in `corpus/source-snapshots/round-47/manifest.json` |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F30 | Zero Day Initiative disclosure policy — the third-party broker's acquired-vulnerability disclosure timeline | admitted | corpus/knowledge/zdi-disclosure-policy.md | S075 | Treat a broker's policy as its own conditional commitment, not a universal vendor clock: ZDI allows "four months (120 days) to address the vulnerability" (`S075.txt:24`) without a stated start event, while its no-response fallback is "fifteen business days after the initial contact" (`S075.txt:23`); extensions are "granted only in rare circumstances" (`S075.txt:24`). Keep F02's coordinator comparison and F15's vendor intake distinct; re-open this policy before relying on it. |

F02 (`corpus/knowledge/coordinated-disclosure-timelines.md`) compares attributed coordinator
timelines; F15 (`corpus/knowledge/vendor-third-party-finding-coordination.md`) records Microsoft's
vendor research programme and third-party intake routes, not a disclosure clock. F30 adds
ZDI's policy for the broker that acquires vulnerabilities; it does not replace those entries
or claim their general timeline distinctions were absent. F02 overlap remains subject to the
independent semantic review required by the frozen C2 kill rule.

[r47 amendment, appended 2026-10-30] The 29/29 count in the round-46 attempt-2 amendment above
records that historical state and is retained (R9). With F30 admitted this round, the
public-practice frontier has **30/30 admitted** rows: F01-F29 as previously recorded and F30
added here. This is one new frontier admission and the 67th knowledge entry, not a coverage-ratio
promotion: (20+30)/(20+30) remains 1.000. The lost-domain denominator remains 0/18; the frontier
count is separate.
```

## Evidence, gates and limits

- Capture/anchor facts: `corpus/source-snapshots/round-47/manifest.json:6-23` pins S075's URL, access, digest, bytes, 60 lines and body range. Q10 is :71-73, located at `S075.txt:26`; other timeline text is `S075.txt:23-25`. The ten quote records do not imply ten distinct source lines.
- Do-nothing control: `.ufo/waves/round-47/controls/c2-base.txt:1-9` records H1 rows=29, H3 S075 absent and `f30-gate fixed=1/7 exit=1`. This is inherited execution evidence, not a counter rerun by this seat. Freeze-tree 2/7 is reported in `claims.json`, C2 `freeze_tree_reading`; no 7/7 claim is made for these unapplied blocks.
- Explicitly requested bounded row-shape check (Python Eval; no counter or product execution): S075_rows=1, S075_cells=11, scope_words=23, teaches_words=20, escaped_pipe_anywhere_in_rows=false, F30_rows=1, F30_cells=6, locator=true, quote_word_count=20. Companion receipt: `R47SrRegistry.draft/row-shape.json`. README tables deliberately have three or six cells, not eleven: only the source registry uses eleven. No cell contains a literal or escaped pipe.
- Lesson dependency: the exact 20-word Q10 grounding quote was sent to `R47SrLesson` for the round-47 Gate. Block B's statement that it is recorded becomes true only when the lesson owner lands it; L1 must integrate that quote alongside B.
- Existing contrasts: `corpus/README.md:203` F02 and :309 F15; previous admission shape :671-694. Registry's 11-column header is `corpus/SOURCES.md:5`; S073 change-bullet shape is :174 (base and current before D5).
- No product file, index, commit, judge, deployment, fleet-root file or sibling repo was modified. No tool installed. No heavy pass, clone, fixture or scratch directory was needed. The only mkdir was the assigned `R47SrRegistry.draft/`; the harness briefly auto-backgrounded that finite mkdir to deliver IRC, then reported successful completion. No background work was intentionally requested.
- Full mutation battery not rerun. Frozen disclosed survivors remain C1 16/35 and C2 18/21, baseline_failures=0; the 43-case tree-probe selftest is inherited evidence only. Full integrated counters, census, semantic overlap review and live-page closure remain L1/wave-2 gates, not exercised passes here.
- Peer finding, not executed by this seat: `R47ScoutRegistry` reported `FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2` after the contract-required S074 rejection, with `records=63 bound=62 unbound=1 exit1`; its report is `.ufo/waves/round-47/w1/R47ScoutRegistry.md`. This D7 capture-binding conflict is preserved verbatim for canonical judgment; this seat neither changes the contract nor edits the instrument to suppress it.

Self-evaluation (1-5): accuracy 4 (pins and quote count grounded; integration not exercised); completeness 4 (all four landing blocks and base positions supplied, lesson landing dependent on owner); clarity 4 (fences separate deliverables from receipts, D5 shifts explicitly noted); actionability 4 (verbatim blocks supplied, L1 integrated gates remain); conciseness 4 (search-log provenance intentionally detailed). Overall 4.0. Improvement priority: integrate the lesson quote, then have L1 exercise integrated gates and semantic overlap review. Would the user agree: the deliverable is a draft, not a claimed pass.

Report: .ufo/waves/round-47/w1/R47SrRegistry.md
