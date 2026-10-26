# ConnSibling — round 37 wave 1 (connector seat: sibling-overlap ruling for F20/S054 + province fit)

Seat id: `ConnSibling` (leaf connector; no subagent dispatch; no `agent://all`). Assignment: combine
the scout sweeps' evidence (grep over 20 sibling lanes, kagi probe, shokuknow doctrine) and rule on
(1) F20/S054 contested scope — expected uncontested, nearest neighbour kagi's retained NVD/SSVC probe,
report not absorbed — and (2) the F20 entry's province fit against the core "program rules, claim
packages" domain plus the F13/F18/F19 severity/prioritization precedent. Receipt only.

Object state at this seat's run time (read-only, HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0`):
`corpus/SOURCES.md` = 53 rows (S001–S053, no S054 yet), `corpus/knowledge/*.md` = 48 (no SSVC entry),
no `corpus/source-snapshots/round-37/` — the S054 row, the F20 knowledge entry, and the round-37
capture are in flight in sibling seats (`ScribeRowS054`, `ScribeEntryF20`, `ExecC2Capture`,
`RevRowS053`, `RevEntryF20`). Absent-at-run-time is expected, not a defect; this ruling is about
scope, not about landed bytes. `git status --porcelain` shows only untracked `.ufo/waves/round-37/…`
artifacts. The scout receipt `ScoutF20Sibling.md` had not landed in this directory at write time;
every load-bearing claim below was therefore re-executed by this seat against the live trees, not
quoted from the scout.

## Sources consolidated

| source | verdict label | load-bearing content |
|---|---|---|
| `wave1/ExecSiblingSweep.md` | UNCONTESTED | 20/20 sibling lanes CLEAN on corpus/SKILL.md/PROVINCE.md; whole-repo superset: only kagi's 4 retained `SrcCve202010735` probe files carry genuine SSVC semantics; 8 false-positive files classified; shokuknow doctrine zero SSVC rows, zero `certcc.github.io`; kasegi round-7–16 evidence quotes SSVC (surfaced before, never registered) |
| `wave1/ScoutF20Open.md` | access + anchor record | S054 opened 2026-10-26; `certcc.github.io/SSVC/` home vs overview tutorial grounding split; `claims-erratum-1.md` moves the row/capture URL home → overview (same host, same docs site — does not touch contested scope) |
| this seat's independent re-runs | — | sibling sweep command re-run verbatim → 20/20 CLEAN; kagi probe JSON payload + 4 sha256 digests re-verified; kagi round-28 rejection note re-read (never names SSVC); shokuknow doctrine grep exit 1 (zero SSVC), `certcc.github.io` grep exit 1 (zero in whole campaign); in-lane S001/S003/S004/S008 adjacency re-verified |

## Q1 — Is F20/S054 contested? NO (measured absence; every axis re-run by this seat)

Lane set: `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` → 21 lanes; kasegi excluded → 20 siblings.

**Sibling surface sweep (re-run verbatim).** The sweep's exact command over all 20 siblings
(`grep -rliE 'SSVC|Stakeholder-specific|Stakeholder-Specific|CERT/CC'` over `corpus/`, `SKILL.md`,
`PROVINCE.md`) → **20/20 CLEAN**, matching the sweep receipt. The pattern also matches `JPCERT/CC`, so
the negative is strict: not even the Japanese namesake appears in a sibling corpus.

**Whole-repo superset (accepted from the sweep, spot-verified).** Only kagi carries genuine SSVC
semantics — 4 files under `.ufo/waves/round-28/retained-probes/SrcCve202010735/`. This seat
re-verified the payload of `nvd-api.json` in full:

```json
"ssvcV203": [{ "source": "134c704f-…", "ssvcData": {
  "timestamp": "2026-10-07T18:38:50.558859Z", "id": "CVE-2020-10735",
  "options": [{"exploitation":"none"},{"automatable":"no"},{"technicalImpact":"partial"}],
  "role": "CISA Coordinator", "version": "2.0.3" }}]
```

and re-computed all four sha256 digests — exact match with the sweep's table
(`d043111e…841a5`, `f897c85c…bf0e6`, `42bc257c…004bf9`, `b206e962…139bd`). The other 8 whole-repo
hits (kaidoku/kake base64 blobs, mori seat-name `…Svc` substring, kotoba codepoint blob, tameshi PNG
`data:` base64, tsukuroi probe line) carry no SSVC semantics — accepted as classified non-ground.
The sweep's coverage hardening is accepted: generic-token counts prove the big corpora were read
(game-dev-3d 332 `vulnerab|prioriti` files, 538 text files inventoried), 50 symlinks all resolve
in-lane, synonym sweep (`CERT Coordination Center` 0, `Vultron` 0, `VINCE` 0 strict, `vulnerability
categoriz` 0), lane HEADs pinned.

**kagi deep read (nearest neighbour — re-verified).** Exactly one provenance chain: kagi round-28
`SrcCve202010735`, probing the NVD API for CVE-2020-10735. The seat's own build note
(`kagi-shokunin/.ufo/waves/round-28/build/SrcCve202010735.md`) records NVD as tier B and the lesson
row (`kagi-shokunin/corpus/lessons/round-28.md:43`) closes **NOT REGISTERED** — and a grep for
`ssvc` over both the build note and the round-28 lesson exits **1**: kagi never names SSVC anywhere.
kagi's registry today: 51 `| S0xx |` rows, none SSVC/scoring-related; `certcc.github.io` absent from
the whole kagi repo (grep exit 1). So the payload is live CISA SSVC v2.0.3 coordinator data for one
CVE, captured incidentally inside NVD's `ssvcV203` ADP container — **retained probe, never a row,
never knowledge, explicitly rejected for registration by its own lane.**

**shokuknow doctrine (re-verified).** `grep -rinE 'ssvc|certcc\.github\.io|stakeholder.?specific'
doctrine/` → exit 1 (zero rows in all of doctrine/); `grep -rl 'certcc\.github\.io'` over the whole
campaign → exit 1. CERT/CC name collisions only, both different bodies: CNCERT/CC (China,
`doctrine/channel-index-chinese.md`) and JPCERT/CC (Japan, `doctrine/channel-index-japanese.md`,
`doctrine/verified-numbers.md`) — recorded so they are never read as ground. Campaign-side
adjacency (report-only, from the sweep, spot-verified): kasegi's own earlier-round mirrors quote
SSVC — `shokuknow/lanes/kasegi/round7/evidence/zxd_wd.txt:2733` ("CISA Stakeholder-Specific
Vulnerability Categorization Guide 2022"), repeated in rounds 8/15/16 — the topic surfaced as
evidence before round 37 and was never registered: consistent with "frontier opening", not "new
discovery".

**Registry/id adjacency.** kagi holds S001–S051; kasegi holds S001–S053 at this head. No S054 exists
anywhere in the fleet; no sibling knowledge entry covers SSVC. `F20` in other lanes (game-dev-2d/3d
tween/actor findings, etc.) is lane-local id usage and raises no fleet collision for kasegi's F20
admission. The round-37 assimilation quarantine (id-collision rerun, registry 53 × staged 94) is a
separate seat's scope; nothing in it touches SSVC ground.

**Q1 ruling: uncontested.** Zero sibling-lane claims on SSVC / CERT/CC / `certcc.github.io`; no
doctrine row contests or assigns the ground; no id collision; no competing knowledge entry. The only
genuine SSVC payload in the fleet is kagi's unabsorbed, self-rejected retained probe.

## Q1b — Nearest-neighbour disposition: kagi NVD/SSVC probe — REPORT, NOT ABSORBED

The assignment's expectation is confirmed and sharpened by the payload read. kagi's
`ssvcV203` captures are the **SSVC decision-point evaluation applied by one coordinator (CISA) to one
CVE** (Exploitation=none, Automatable=no, Technical Impact=partial, v2.0.3) — decision-point *data*,
not the SSVC methodology documentation, and not a source row by kagi's own rejection. F20/S054 (even
after `claims-erratum-1.md` moves the pinned URL home → `tutorials/ssvc_overview/`, same host and
docs site) is the SSVC framework itself: stakeholder-defined decision model, decision points →
outcomes, prioritization contrasted with technical severity and exploitability (`ScoutF20Open.md`
§3). Same acronym family, different object class: per-CVE coordinator output vs published
methodology. Disposition per `PROVINCE.md` Adjacent ("Sibling lanes are reported, not absorbed"):
**reported in this ruling and available to the L1 as a round-37 lesson note ("not absorbed" lead);
not absorbed into kasegi's corpus, not cited by the F20 entry, not a registry row.** No
`PROVINCE.md` refinement is required: the adjacency is evidence-shaped, not scope-shaped.

## Q2 — Province fit of the F20 entry: FITS, no re-scope

- **Domain line.** `PROVINCE.md:3` — "bounty & security research — scopes ~/Projects/bounties,
  program rules, claim packages". Core (`PROVINCE.md:28-30`): "the line-3 domain comprises program
  rules, scopes, and claim packages; the core also covers triage and claim gates, and
  submission/disclosure packaging." SSVC is a vulnerability-management prioritization methodology —
  which findings demand action first, decided per stakeholder (finder/vendor/coordinator/deployer).
  That is triage craft applied to incoming claims, the exact core the province owns; a coordinator
  side (CERT/CC) is already knowledge-grounded in the lane
  (`corpus/knowledge/coordinated-disclosure-timelines.md`, citing the round-24 CERT/CC capture).
- **The F13/F18/F19 precedent ladder.** The lane's frontier already indexes severity and
  prioritization as its own axis: F13 (program severity ladders and reward scales, S043–S045,
  round 29), F14 (Japanese severity vocabulary and the handling-priority model, round 30), F17
  (Immunefi Vulnerability Severity Classification, round 34), F18 (CISA KEV — prioritize by
  known in-the-wild exploitation, S052, round 35), F19 (FIRST EPSS — prioritize by exploitation
  likelihood, 0–1 probability, S053, round 36; the F19 entry's own header states the axis split from
  CVSS severity and KEV membership). F20 is the next rung: given severity (F13/F17 vocabulary), KEV
  membership (F18) and exploitation likelihood (F19), SSVC asks the stakeholder-prioritization
  question those axes do not — *whose risk, and what action priority*. The registry's own
  decision-order line (`corpus/SOURCES.md:68`, "Exploitation likelihood — S053 → S052 → S001 →
  S002") shows the lane already teaches combined triage input ordering; a stakeholder-prioritization
  methodology is a native complement, not a foreign body.
- **Prior occupancy of the same publisher.** `certcc.github.io` is already manifest-bound in-lane:
  S004 = `https://certcc.github.io/certcc_disclosure_policy/` (round-24 capture, bound in
  `corpus/source-snapshots/round-24/manifest.json`, re-verified this seat) and SSVC is already named
  verbatim in four committed kasegi captures — S004.txt (site nav, 2 hits), S001.txt:954,994 (FIRST
  CVSS v4.0 user guide: "the decision point by the same name in the stakeholder specific
  vulnerability categorization (version 2)" — line-wrapped, hence the phrase grep needs the loose
  form), S003.txt (CISA CVD program: "CISA uses SSVC…"), S008.txt (CISA VDP template). Novelty of
  S054 is **page-level** (`/SSVC/` home, `/tutorials/ssvc_overview/` per erratum-1), never
  host-level or concept-level.
- **Consequence for C2 scoring (stated, not enacted).** The coverage claim should be phrased as a
  frontier opening over already-present adjacent ground: first SSVC-methodology ground in the
  registry (genuinely new row + entry), on a host and concept the lane already holds. Risk is
  **under-credit, not collision**. No province re-scope is implied or needed; the entry grounds
  solely on kasegi's own S054 capture.

## Caveats consolidated

- **A (URL).** `claims-erratum-1.md` (filed pre-score) moves the S054 row/manifest/capture URL from
  the frozen home page to the overview tutorial page; both are `certcc.github.io`, so contested
  scope and province fit are unaffected. The frozen claim C2 literal remains the home URL; the
  erratum is the operative steering for builders (`ScoutF20Open.md` independently confirms the
  erratum is necessary: HOME alone grounds (a),(b) and only partial (d), not (c)).
- **B (phrasing).** Never claim "SSVC was absent from the lane": S001/S003/S004/S008 name it since
  rounds 22–24. Correct phrase: "first SSVC methodology ground" / "first SSVC registry row".
- **C (kagi discipline).** The kagi `ssvcV203` payload must not be cited as a source and must not be
  read as kagi claiming SSVC ground — kagi's own note rejected the row and never names SSVC. It is a
  lesson note only ("retained, not absorbed").
- **D (name collisions).** CNCERT/CC (China) and JPCERT/CC (Japan) appear in shokuknow doctrine;
  neither is Carnegie Mellon's CERT/CC and neither contests or supports F20.

## Final ruling text for the lesson (splice-ready)

> ### Contested scope — none, ruled rather than left silent (F20/S054)
>
> `wave1/ConnSibling.md` consolidates the round-37 scout sweep evidence and rules on F20/S054 under
> `PROTOCOL.md:457-461` and kasegi's `PROVINCE.md` Adjacent ("Sibling lanes are reported, not
> absorbed"):
>
> - **Uncontested.** All 20 sibling lanes hold zero SSVC ground on the required surface
>   (`grep -rliE 'SSVC|Stakeholder-specific|Stakeholder-Specific|CERT/CC'` over `corpus/`,
>   `SKILL.md`, `PROVINCE.md` → 20/20 CLEAN, re-run by this seat); the whole-repo superset finds
>   genuine SSVC semantics only in kagi's four retained `SrcCve202010735` NVD probe files (CISA
>   SSVC v2.0.3 coordinator evaluation of CVE-2020-10735: exploitation=none, automatable=no,
>   technicalImpact=partial; digests re-verified), and every other whole-repo hit is a classified
>   false positive (base64/blob substrings, a seat-name `…Svc` substring, DNS-SVCB noise). No
>   sibling `SKILL.md` or registry row claims SSVC; kasegi is the fleet's only
>   vulnerability-domain lane. shokuknow doctrine carries zero SSVC rows and zero
>   `certcc.github.io` occurrences; its CERT/CC name collisions are CNCERT/CC (China) and JPCERT/CC
>   (Japan), different bodies. No S054 id exists anywhere in the fleet; no doctrine row contests or
>   assigns the ground.
> - **Nearest neighbour — report, not absorbed.** kagi's retained NVD/SSVC probe is the SSVC
>   decision-point *data* (one coordinator's evaluation of one CVE, inside NVD's `ssvcV203` ADP
>   container), not the SSVC methodology; kagi's own round-28 note rejected the row for registration
>   and never names SSVC. Recorded as an unabsorbed lead in this lesson; not cited by the F20 entry,
>   not absorbed into the corpus.
> - **Province fit.** F20 fits the core province without re-scope: SSVC is triage/prioritization
>   craft over incoming claims ("program rules, claim packages" + `PROVINCE.md`'s triage-and-claim-
>   gates core), it extends the lane's own severity/prioritization ladder (F13 severity ladders →
>   F14 handling-priority vocabulary → F17 Web3 severity classification → F18 KEV exploitation
>   status → F19 EPSS exploitation likelihood → F20 stakeholder-specific prioritization), and its
>   publisher's host is already manifest-bound in-lane (S004, round 24) with SSVC named verbatim in
>   captures S001/S003/S004/S008. Novelty is page-level, never host- or concept-level: phrase the
>   admission as "first SSVC methodology ground", never "SSVC absent from the lane".
> - **Ruling.** F20/S054 is uncontested; no report-to-lane absorption arises; no `PROVINCE.md`
>   refinement is required. C2 coverage scoring should treat the opening as adjacent-ground
>   (under-credit risk, not collision risk).

## Housekeeping

- Writes: this receipt only (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-37/wave1/ConnSibling.md`).
  No lane/fleet/shokuknow file edited; no doctrine row written; no git/jj mutation (read-only
  `rev-parse`/`status`/`grep`/`ls` only); no tool installed (none needed — pacman pause respected);
  no subagents dispatched; no `agent://all`.
- Coordination: `ScoutF20Sibling.md` had not landed at write time; this seat re-ran the underlying
  sweep, kagi, and shokuknow evidence independently rather than blocking on it. If the scout's
  receipt later disagrees on any load-bearing point, the disagreement is a review item, not a
  contradiction of scope.
- Scratch `/fast/scratch/hyaku/kasegi-r37/ConnSibling/` (created at seat start, held no fixtures —
  all work was read-only greps/parses) removed before yield; verified empty at exit.

Report: .ufo/waves/round-37/wave1/ConnSibling.md
