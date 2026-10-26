# ConnSibling — contested-scope ruling draft (round 35, wave 1)

*Draft for absorption into `corpus/lessons/round-35.md` (Gate / contested-scope record).
Source scan: `ScoutSiblingSweep` (`.ufo/waves/round-35/wave1/ScoutSiblingSweep.md`), every load-bearing
claim of which was independently re-run by this seat (commands and outputs in
`.ufo/waves/round-35/wave1/ConnSibling.md`). Doctrine: `PROTOCOL.md:457-461` contested-scope
invariant (report in the lane report; integrator arbitrates; an unruled report is re-flagged — so
this ruling is recorded, not left silent); kasegi `PROVINCE.md` Adjacent: "Sibling lanes are
reported, not absorbed." Object under protection: C2 / Frontier F18 / registry row S052
(CISA Known Exploited Vulnerabilities catalog, `corpus/SOURCES.md:58`, opened 2026-10-26).*

## Ruling table — every CISA/KEV-ground hit found in sibling corpora

| # | Hit (named location, quoted) | Ruling | Discriminating test |
|---|---|---|---|
| 1 | `kake-shokunin/corpus/lessons/round-35.md:58-60` — the sentence spans two lines; read directly at file digest `cffb84a5…` (sha256 below): "It proposed rejecting the CISA BOD 20-01 template: “Your policy must be published as / a public web page in plain text or HTML at the “/vulnerability-disclosure-policy” path”. That / template names neither security.txt nor `.well-known` (`w1/ScoutSecurityTxtCandidates.md`)." (doubled smart quotes as in the source; `ScoutSiblingSweep.md:17` renders the same line with an elision — this draft's rendering is the byte-faithful one) | **No contested scope** | Directive discrimination: BOD 20-01 (publish a VDP) ≠ BOD 22-01 / KEV (exploitation-status prioritization with remediation deadlines). Topic test: kake's round-35 ground is VDP *publication path* (security.txt / RFC 9116), not exploitation-status prioritization. Occupancy test: kake's own scout *rejected* the candidate and kake created **no** SOURCES row for it (its S078–S087 rows are RFC 9116 / GitHub Pages rows). Prior-occupancy test: the BOD 20-01 template is already kasegi-held ground — `corpus/SOURCES.md:14` S008 "CISA Vulnerability Disclosure Policy Template … BOD 20-01 template" and `:27` S021 "CISA, BOD 20-01: Develop and Publish a Vulnerability Disclosure Policy". |
| 2 | `kake-shokunin/corpus/SOURCES.md:255` — round-35 bounded-question paragraph; `grep -n "BOD 20-01"` over the file returns **only** this line ("wave-1 `ScoutSecurityTxtCandidates` screened six more candidates (OWASP cheat sheet, RFC 9116 errata, securitytxt/…") | **No contested scope** | Same three tests as #1 — the paragraph *records the screening-out* of the same BOD 20-01 candidate; a rejection record in a sibling's search log is not held ground. Two files, two lines, one rejected candidate, zero rows. |
| 3 | `kagi-shokunin/corpus/lessons/round-28.md:43,151,154`, `kagi-shokunin/corpus/SOURCES.md:89` — NVD REST/API used to quote CVE-2020-10735 (Python int-conversion limit) | **No contested scope** (adjacent-theme, semantic sweep) | Topic test: kagi's round-28 ground is version-token typing; the NVD page is a *quote source*, marked "NOT REGISTERED" as a source. No CVSS-vs-exploitation distinction, EPSS, SSVC, or KEV teaching anywhere in kagi. |
| 4 | `mori-shokunin/corpus/evidence/recheck-r32/S012.src` — "CVSS overall score" ×1 | **No contested scope** (adjacent-theme) | Container test: the hit is inside a raw fetched GitHub-advisory HTML evidence blob (`grep -c` → 1), not a taught claim, lesson row, or registry row. |
| 5 | "in the wild" incidental hits — `kotoba-shokunin/corpus/SOURCES.md:354`, `kotodama-shokunin/corpus/lessons/round-8.md:133` and `append-only-record-verification.md:40`, `tabi-shokunin` fixtures, `mori-shokunin/corpus/SOURCES.md` S175 blob | **No contested scope** (adjacent-theme) | Sense test: mutation-testing / record-state / curl-docs senses of "in the wild"; none concerns exploitation status. |
| 6 | `shokuknow/doctrine/channel-recurrence.md:62` — "`\| cisa.gov \| kasegi \|`" | **No contested scope — affirmative ratification** | Ownership test: the doctrine table *assigns the cisa.gov host to kasegi*; adjacent rows are cert.org.cn / cnnvd.org.cn / cnvd.org.cn / butian.net → kasegi. This favors, not contests, F18/S052. |
| 7 | All other sibling surfaces — 19 zero-hit sibling corpora (20 siblings scanned; `audio-shokunin` and `game-dev-2d-shokunin` have no SKILL.md, corpus-only), zero hits outside sibling corpora (PROVINCE.md/README/considerthese/plans/SCORECARD/LOG), zero hits at fleet root (`merge/` and `considerthese/` do not exist there), zero hits in `shokuknow/merge/*` (21 lane dirs) | **No contested scope** | Absence test: `rg -i -n -e '\bCISA\b|\bKEV\b|known exploited\|BOD 22-01\|exploited vulnerabilit\|remediation deadline'` returns nothing outside the rows above (exit 1 = no matches), with the word-boundary pattern discarding the `exercisable` false-positive class (kaidoku ×4 confirmed). |

## Verdict

**F18 / S052 is uncontested by any sibling corpus; no report-to-lane item arises this round; no
`PROVINCE.md` refinement is required.** The only CISA tokens anywhere in the 20 sibling lanes are
kake's *rejection record* of the BOD 20-01 VDP template — a directive kasegi already holds as S008/S021
and a topic (VDP publication path) that is not exploitation-status prioritization. Recorded here so the
item is ruled, not re-flagged under the "silence is not a ruling" clause.

## Re-runnable evidence (embed in the lesson)

```
cd /home/vgpnk/Projects/shokunin
P='\bCISA\b|\bKEV\b|known exploited|BOD 22-01|exploited vulnerabilit|remediation deadline'
for d in *-shokunin; do [ "$d" = kasegi-shokunin ] && continue; rg -i -n --no-heading -e "$P" "$d/corpus" "$d/SKILL.md"; done   # only kake :58 and :255
rg -i -n -e "$P" -g '!kasegi-shokunin/**' -g '!*/corpus/**' *-shokunin                        # exit 1 (zero)
rg -i -n -e "$P" -g '!*-shokunin/**' .                                                        # exit 1 (zero, fleet root)
rg -i -n -e "$P" /home/vgpnk/Projects/shokuknow/{merge,doctrine,lanes,README.md}              # kasegi-owned rows + channel-recurrence :62 only
```

## One bounded proposal (connector move; for the L1, not executed this round)

**Mint a registered sibling-overlap probe next round.** This round's scan is sound but lives only as
prose + receipt; depth:verifiability would be served by a `corpus/instruments/sibling-overlap.sh`
(five-token pattern above, word-boundary false-positive rule, verdict map `0 uncontested | 1 contested
hit found`, `--selftest` on an indented-row/exercisable fixture) registered in SKILL.md Gates & probes
in a future round's claim. Not done now: C1's frozen after-state names exactly two registry rows and
the wave is mid-land. Affected axes: depth:verifiability (runnable, non-author-checkable), coverage
(guards F18-class novelty claims each round). Risks: none to frozen claims (no corpus write this
round); the probe's first run would itself need the same sibling read-only discipline recorded here.

Precision note for the lesson: the scout's kasegi-baseline "`rg -i -c '\bCISA\b|\bKEV\b'
corpus/SOURCES.md` → 10" is stale by one landed edit — the same command at this receipt's run time
prints **11** (`:9 :14 :27 :29 :32 :58 :70 :71 :79 :108 :112`; the added line is the round-35
search-log scope-correction note at `corpus/SOURCES.md:112`). **A count must travel with its
pattern** (binding agreed with `ScribeGateAssimilation`, which measured the same 11 at 06:46Z):
the scout's wider five-token sweep pattern reads **12** lines here (adds `:111`, the round-35
search-log superseded-bullet note) — measured twice independently. A count printed without its
pattern is the defect class C1 is closing. No claim counts either baseline; noted so the lesson
prints pattern + count together.

Cross-seat agreement: `ScribeGateAssimilation` verified zero intersection between the staged
assimilation package (67 knowledge files, `grep -rliE 'cisa|known.exploited|kev'` → 0) and the
CISA/KEV ground this ruling protects — the contested-scope record and the assimilation Gate are
disjoint records.
