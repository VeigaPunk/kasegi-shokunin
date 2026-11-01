# Round 52 — the routed figure corrections (C2), the R56 quote-count gate (C1), and the NVD API 2.0 surface (C3)

Three declared claims, frozen in `.ufo/waves/round-52/claims.json` at base `6c0a08e2b99344ff3e82f8a52771af34fccc0155`
(freeze commit `29c4bd9dd0aa05a9276be6e3d6b35da7d9ecaa31`) before implementation: C1 on depth:verifiability (the lane's
lowest non-retired axis, score 4 — capability acquisition: `corpus/instruments/gate-quote-audit.py`, the fail-closed
auditor for the QUALITY.md R56 word-count class), C2 on calibration (verdict row, not a number — the round-51 closure's
two figure corrections, append-only, plus the S013/F05 scope note in PROVINCE), C3 on coverage (frontier F33 = the NVD
Vulnerability Data API 2.0 retrieval interface on S083, with S066's round-42 flip spent and S084 recorded as the rejected
JS-wall). Host unchanged from rounds 50-51 (Windows workspace, `python` 3.13.15, `python3` = Store stub, no /home, no
/fast). The carry-in items were addressed first: the S081 quote re-measured 17 (by `wc -w`; the filed figure was 24) before anything
was written, and the 4809 counts re-measured 2/3/5 by `grep -c 4809` over lesson-50/LOG/SCORECARD.

## Mistakes

Sweep that found them (paste, per contract): the round's own receipt runs — every defect below was caught by a
counter's output disagreeing with its expectation BEFORE any implementation commit existed: (a) the C1 rev-1 AFTER
receipt printed `corpus/lessons/round-51.md:97 claimed=24 measured=5 MISMATCH` where a clean erratum-on-record was
expected; (b) the C1 BEFORE-state re-derivation printed `erratum-on-record=1 ... exit=0` where exit 1 was expected
(the pre-erratum lesson was wrongly acknowledged); (c) the C3 counter's first run printed
`FAIL F33 ... problems=selection-not-cited-by-entry` and `entries=36 pass=2` where pass=3 was expected; (d) the first
`source-recheck.py` run printed `S083:Q8 UNAVAILABLE reason=quote-too-short-to-be-evidence`; (e) the first freeze.txt
build printed a leading `*` on every pinned line (Git Bash sha256sum binary-mode marker), caught by reading the file
back before committing.; and (f) AFTER the implementation commit, the round's own auditor run over the
final tree flagged three annotation-shaped references in THIS lesson's own prose (figures 17/24/24 stated in
the audited "N words by wc -w" shape, resolving to a placeholder or to nothing) — the instrument policing the
figure class caught the round documenting the figure class. The prose was rephrased to state figures outside
the annotation shape, the audit re-run green, and the census regenerated (gate receipt rev 4).

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| an acknowledgment check that accepts a figure anywhere in a file that merely discusses the topic | the C1 rev-2 erratum-acknowledgment check (`"rratum" in raw and str(measured) in raw`) passed the PRE-erratum round-51 lesson — which mentions errata generally (its own M3/Erratum prose) and contains stray digit substrings — so `quote-audit-before-recheck-r52.txt`'s first run read exit 0 where the uncorrected 24-vs-17 had to stay red (`.ufo/waves/round-52/controls/quote-audit-before-recheck-r52.txt` now shows the tightened run: MISMATCH + LEDGER-ORPHAN, exit 1) | the BEFORE-state re-derivation disagreeing with its expected exit, on its first run, before the implementation commit | the check now requires a SEPARATE occurrence of `<measured> words` within ±1000 chars of an erratum mention (not the audited annotation itself); pinned as selftest case-i (`erratum-mention-without-correction` → want fail); `corpus/instruments/gate-quote-audit.py` sha superseded in `freeze.txt` rev 1b and `.ufo/waves/round-52/claims-erratum-1.md` |
| an instrument matching its own subject's quotations | the C1 rev-1 AFTER receipt flagged the round-51 Erratum's own quoted reference to the 24-figure as an annotation and measured the annotation against itself (claimed=24 measured=5) — a quoted span that CONTAINS the annotation is a reference to an annotation, not a Gate locating a quote | the AFTER receipt printing a MISMATCH row the tree should not have had, on its first run | `find_span` now skips self-referential spans and resolves the nearest real quote (the Erratum's reference re-measures the same 17-word quote); pinned as selftest case-h; recorded in `claims-erratum-1.md` |
| a claim quote cited only on its declaration lines | the F33 entry first named S083 only on its `source:`/`recheck:` header lines, so the frontier counter's citation limb read the entry as never citing its source: `FAIL F33 ... problems=selection-not-cited-by-entry`, `entries=36 pass=2` (first `frontier-recheck-count.py` run) | the frozen counter failing on the round's own entry, before any commit | the entry's claim attributions now carry capture-line citations (`— Q<n>, S083.txt:1`, the F32 house style); the re-run reads `PASS F33 ids=S083 exit=0`, `entries=36 pass=3` (`controls/c2-counter-final-r52.txt`) |
| (inherited, fixed this round) a Gate word count written from memory instead of re-measured | round-51 closure §5 item 2: the round-51 lesson annotates the S081 quote as 24 (attributed to `wc -w`); `printf '%s\n' "<quote>" \| wc -w` returns 17 (re-measured first-hand this round before anything was written). Same class as round-48 M48-3 (16 claimed, 14 measured) — the R56 prose rule did not hold twice | the round-51 non-author closure; re-measured first-hand this round | C2: `corpus/lessons/round-51.md` gains Erratum 1 naming 17 with the command, the filed 24-words line retained byte-identical; and the class is now instrument-checked: C1's `gate-quote-audit.py` BEFORE receipt (exit 1 on the then-uncorrected figure) → AFTER receipt (exit 0, erratum-on-record) |
| (inherited, fixed this round) a move-log self-count figure disagreeing with its own counting command | round-51 closure §5 item 1: the SCORECARD round-51 move-log row records the 4809-row counts as "2/3/2"; `grep -c 4809 corpus/lessons/round-50.md LOG.md SCORECARD.md` measures 2/3/5 (re-measured first-hand this round) — the D2 class, on the round that fixed D2 | the round-51 non-author closure; re-measured first-hand this round | C2: the SCORECARD round-52 section carries the correction-of-record paragraph naming 2/3/5 with the command; the filed "2/3/2" line stays byte-identical (append-only, R9) |

## Gate

**S083 admitted** — NVD Vulnerability Data API 2.0, live CVE response for CVE-2024-3094,
`https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-3094` (NIST's own services host, first-party
machine output), kind `code`, tier A, status `mined`, opened 2026-11-01, recheck `90d`, used-by
`corpus/knowledge/nvd-api-2.0-retrieval-interface.md`. Capture `corpus/source-snapshots/round-52/S083.txt`
(sha256 `5c35a51b103934778b94b385a060a26da53a7319e7339f85efcf646899a0e716`, 13077 bytes, 1 line; fetched
2026-11-01T04:18:04Z, HTTP 200, 13076 raw bytes), manifest `corpus/source-snapshots/round-52/manifest.json`
(12 assertions Q1-Q12, each exactly-once at its pinned anchor — the capture is single-line, so every anchor is
line 1; `python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-52/manifest.json
--source S083` exits 0 — receipt `controls/s083-recheck-r52.txt`).

Located quote grounding `teaches` (1 "word" by `wc -w` — the quote is contiguous single-line JSON with no
interior whitespace: `printf '%s' '"resultsPerPage":1,"startIndex":0,"totalResults":1,"format":"NVD_CVE","version":"2.0"' | wc -w`
→ `1`, `wc -c` → 85; the ≤25-word bound is read against that measurement, not skipped): "resultsPerPage":1,
"startIndex":0,"totalResults":1,"format":"NVD_CVE","version":"2.0" (S083.txt:1, Q1). The further anchors the entry
cites: S083.txt:1 Q2 (record id + CNA source identifier), Q3 (published/lastModified/vulnStatus), Q4 (CNA-secondary
CVSS), Q5 (NVD-primary CVSS), Q6 (ingested ssvcV203 + source UUID), Q7 (SSVC decision points + role), Q8 (Spanish
description), Q9 (tagged reference), Q10 (CPE criteria), Q11 (CWE-506 weaknesses block), Q12 (match operators).

**Admitted:** the NVD API 2.0 surface as frontier row F33 — NIST's read-side retrieval interface over the
NVD-enriched CVE record (the 2.0 paging envelope, NVD's own Primary CVSS served beside the CNA's Secondary with
per-item provenance, CPE applicability configurations, CWE weaknesses, tagged references, multilingual descriptions,
change tracking, and the ingested CISA ADP SSVC block) — admitted with the pre-freeze neighbor screen named against
F05/F18/F19/F25/F30/F32 (entry §Distinctness) and EXTENDED per the round-51 closure's observation: the screen's
downstream-consumer sweep also covered `corpus/source-snapshots/` (receipt `controls/neighbor-screen-r52.txt`,
run before the freeze commit). S066's round-42 flip is spent by this admission; the row stays byte-identical.
Counter before→after ON THIS HOST: `FRONTIER-CENSUS rows=32 admitted=32 closed=2 problem-rows=30 registry=82`,
`entries=35 pass=2`, zero F33 lines (`controls/do-nothing-c3-r52.txt`, base export 6c0a08e built per-file, 506/506)
→ `FRONTIER-CENSUS rows=33 admitted=33 closed=3 problem-rows=30 registry=84`, `entries=36 pass=3`,
`PASS F33 ids=S083 exit=0`, all 33 inherited fails exactly `recheck-exit-1` and 30 row fails exactly
`missing-pass-line` (`controls/c2-counter-final-r52.txt`).

**Rejected / refused, with reason and flip:** S084 — the NVD API 2.0 developer-hub documentation page
(`https://nvd.nist.gov/developers/vulnerabilities`), refused because the page serves a JS application shell to the
lane's capture instrument (HTTP 200, 2629 raw bytes → an 11-byte text snapshot, receipt
`controls/s084-hub-shell.txt`) — the same wall round-42's S066 anchor already recorded — so the API's own live
response is the first-party source of record (S083) and rate-limit/authentication/parameter claims are NOT asserted
anywhere this round. Flip: a static or text-renderable copy of the developer-hub documentation capturable by the
lane instrument. Also refused this round: any portability rewrite of the 67 host-bound recheck lines (L0 kasegi
round-50 unanswered, routed around), and considerthese 2026-10-26 proposal 2 (end-to-end domain task round — noted,
not adopted; proposal 1 was already implemented as the round-39 distance-to-next-score section).

**Spot-check:** none of this round's gate decisions has an independent non-author spot-check yet; the most recent
outside check is `corpus/lessons/round-51-verifier-spotcheck.md` (commit `6c0a08e`), which routed the defects this
round fixes. The claims verify on their frozen predicates by re-derivable commands only.

**Wave disposition — no AgentSwarm surface on this host; no seats ran.** As in rounds 49-51, no AgentSwarm/Kimi
host surface exists in this environment and no L2 wave was dispatched; the round's craft, commits and verdicts are
the L1's own. The MISSION.md L2 floor stays unsatisfiable on this host and is recorded as such, not simulated.

## Limits

- The C1 instrument audits figure HYGIENE of Gate word counts only: it does not judge whether a quote supports
  the claim it grounds (occurrence/anchor truth stays with `source-recheck.py`, location truth with the capture),
  and its erratum-acknowledgment path trusts the ledger only as far as the lesson's own erratum text (verified
  positionally, not semantically).
- The round-51 Erratum's word-count correction is grounded on `wc -w` re-measurement (17), the same command R56
  names; the quote itself and its S081.txt:2 location were verified verbatim by the round-51 closure and stand.
- The F33 capture pins one live response for one record at one instant; `vulnStatus: Modified` and the record's own
  2026-06-17 `lastModified` are the interface's statement that this data changes — the 90d row recheck re-opens the
  query, it does not trust the instant. Rate limits, authentication and the wider parameter surface are unasserted
  (S084's JS wall).
- The F33 admission inherits the host split unchanged: the counter reads `entries=36 pass=3` with 33 inherited
  `recheck-exit-1` rows (L0 kasegi round-50, operator-owned). No coverage score is asserted from the frontier row;
  the score's denominator stays the lost domain root's 18-surface set.
- The gate certifies census freshness, not citation truth (unchanged from rounds 50-51); `resolve.py` and
  `anchorcheck.py` keep those jobs.

## Census of record at this round's tip (quoted only from the final regeneration)

Measured AFTER the last corpus edit of the round: the figures below live in the SCORECARD round-52 section and are
quoted only from the final regeneration at the final tip, certified by the gate receipt
`controls/c1-gate-final-r52.txt` (`CENSUS-FRESH=ok`). This lesson intentionally quotes them only by pointer, so the
lesson bytes cannot drift from the gate-certified census they describe.
