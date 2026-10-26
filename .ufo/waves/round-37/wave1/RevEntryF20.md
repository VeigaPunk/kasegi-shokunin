# RevEntryF20 — F20 entry plan review against Q1–Q6 (round 37, C2 / coverage)

Seat: `RevEntryF20` (leaf reviewer, no subagent dispatch; receipt only — no lane file edited except this receipt).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Commits read: base `b56a4168`, freeze `224df74d`, erratum `b3620681` (HEAD while working).
Claim served: C2 coverage — the F20 (SSVC) knowledge-entry plan, reviewed before the entry lands.

## 0. What I reviewed

- The entry plan = the `ScribeEntryF20` item text in `.ufo/waves/round-37/wave1-spec.json` (draft `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`; header `source: S054` + URL + anchor, `verified-at: 2026-10-26`, executable `recheck:`; ≤25-word located quotes; CERT/CC first-party attribution; ≥1 falsifiable rule; ≥1 rejected over-generalization; sources-overlap paragraph vs F18 KEV / F19 EPSS; ~60–100 lines).
- The S054 row plan (`ScribeRowS054` item), frozen C2 predicate/kill rule (`.ufo/waves/round-37/claims.json`), and claims-erratum-1 (URL corrected to the overview tutorial page).
- Sibling pins: `wave1/ExecC2QuoteOnce.md` (four quotes Q1–Q4) and `wave1/ExecC2Capture.md` (manifest quote set). The entry itself is **not yet in the worktree** (`ls corpus/knowledge | grep -i ssvc` → empty; `grep -n S054 corpus/SOURCES.md` → empty at review time) — this review is of the plan, as assigned.

## 1. Independent fetch (scratch, my own bytes)

Copied the lane instruments byte-for-byte into scratch and re-fetched both candidate URLs with `capture-source.py` (UA `kasegi-shokunin/1.0`):

| url | status | fetched | snapshot | sha256 |
|---|---|---|---|---|
| `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` (erratum-1 pin) | 200 | 143053 | 32623 B, 518 lines | `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21` |
| `https://certcc.github.io/SSVC/` (home control) | 200 | 105807 | 7730 B, 286 lines | `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56` |

My overview sha256 equals the pin in `ExecC2Capture.md`/`ExecC2QuoteOnce.md` exactly, so their line anchors carry over to my capture. I then rebuilt a scratch manifest from my own capture and ran the lane's `source-recheck.py`:

```
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=247-ok
S054:Q2 OK occurrences=1 anchor=259-ok
S054:Q3 OK occurrences=1 anchor=277-ok
S054:Q4 OK occurrences=1 anchor=367-ok        exit=0
```

Negative controls (same shape): fabricated quotes → `MISMATCH reason=quote-not-found`, exit 1; unlisted `--source S999` → `UNAVAILABLE reason=not-listed`, exit 2. Fail-closed confirmed independently.

## 2. Q1–Q6 against the planned entry

| id | how the plan meets it | evidence / residual condition |
|---|---|---|
| Q1 header | Plan opens with `source: S054` + URL + anchor, `verified-at: 2026-10-26`, executable `recheck:`. Convention matches admitted entries (`cvss-v4-severity-and-vector.md:2-4`). | **Must use the erratum-1 URL** `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` — the item text still carries the stale home URL `https://certcc.github.io/SSVC/` (pre-erratum wording; the L1 steering message supersedes it). Header line must start `source: S054 ` (space before the URL) so `grep -rlE '^source: S054 '` hits exactly 1 file. `recheck:` must be one `bash -n`-parseable, `cd <lane> &&`-prefixed command over `corpus/source-snapshots/round-37/manifest.json --source S054` (Q10/R12 shape; the KEV entry `cisa-kev-catalog.md:7` is the model). |
| Q2 tier support | Single tier-A row S054 (kind docs, status mined, opened 2026-10-26) opened in the admitting round; no tier-C sole support. | Row must land in the same round (kill rule: "S054 row absent or malformed"). Scope cell "CERT/CC's own SSVC documentation" matches what the capture is. |
| Q3 quotes | All planned quotes verified ≤25 words, exactly-once, anchor-verified (§3). Numbers the entry may cite are once-only in the capture: `ssvc:E:1.1.0` (L282), `ssvc:EXP:1.0.1` (L373), "perhaps within 90 days" (L266), "4-level Service Level Expectation" (L261) — copy byte-exact, never from memory. | Q3's quote is exactly 25 words and contains the page typo `decisions point values` — quote verbatim, note the typo outside the quote marks; one added word breaks the bar. |
| Q4 attribution | Plan says attribute to CERT/CC/Carnegie Mellon first-party, never a universal rule. Capture supports: `CERT/CC` in prose 14× (e.g. L268, L457, L462, L466-468); `Carnegie` only in the footer copyright (L505-507); `FIRST` 0×. | Keep methodology sentences attributed ("CERT/CC's SSVC documentation states/suggests…"). "Carnegie Mellon University" is footer-only support — use it for the ©/host framing, not as the voice of methodology sentences. The page hedges itself ("we suggest", L277; "We provide these categories as examples", L261; "roles are not exhaustive", L257; "it is not a one-size-fits-all system", L249) — the entry must preserve that advisory voice, not harden suggestions into mandates. |
| Q5 falsifiable rule + rejected over-generalization | Plan requires ≥1 of each. The example rejected over-generalization ("SSVC replaces CVSS": prioritization decision system vs severity metric) is well grounded in L247/L473. | **The example falsifiable rule is NOT checkable against the pinned capture** — see pitfall P2; re-anchor it (§4 gives two capture-grounded replacements). |
| Q6 documentation-only | Source is public docs; quotes are definitional (Exposure's "attacker… open Internet" is a definition, not an instruction). No probing/scanning/login/submit verbs, no credential/session/private URL, no vault-scheme URI; the only URL is the public source URL. | Keep it that way; no endpoint, portal, or target instruction may enter via the overlap paragraph. |

## 3. Quotability verdict — exact quotes I would accept

All verified against my own fresh capture (word count / occurrences / anchor):

| id | L | words | occ | quote (verbatim) |
|---|---|---|---|---|
| Q1 | 247 | 22 | 1 | `Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability` |
| Q2 | 259 | 12 | 1 | `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.` |
| Q3 | 277 | 25 | 1 | `A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is` |
| Q4 | 367 | 19 | 1 | `Exposure refers to how difficult it would be for an attacker to access a system from the open Internet.` |
| A1 | 281 | 14 | 1 | `Exploitation refers to how much evidence currently exists that the vulnerability is being exploited.` |
| A2 | 467 | 14 | 1 | `If the vulnerability is being actively exploited, the CERT/CC is more likely to publish.` |
| A3 | 473 | 12 | 1 | `SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach.` |
| A4 | 247 | 9 | 1 | `SSVC rates vulnerabilities on risk to the concerned stakeholder.` |
| A6 | 261 | 12 | 1 | `The following categories, listed in increasing order of priority, are suggested end-categories` |
| A7 | 266 | 14 | 1 | `Defer simply means 'do not act at present,' not 'do not act at all.'` |
| A8 | 257 | 21 | 1 | `The three aforementioned roles are not exhaustive and are only the ones for which we have created decision models so far.` |
| A10 | 365 | 11 | 1 | `Exploitation is the same as for Exploitation in the Supplier model.` |
| A11 | 289 | 20 | 1 | `There is no evidence of active exploitation and no public proof of concept (PoC) of how to exploit the vulnerability.` |
| A12 | 295 | 21 | 1 | `Shared, observable, reliable evidence that the exploit is being used in the wild by real attackers; there is credible public reporting.` |

Also verified once-only: `All decision points and decision outcomes (priority categories) must be explainable to the non-expert.` (L277, 14 words — ExecC2Capture's Q2), `These categories reflect the timeliness of action to be taken.` (L259, 10), `Decision Trees are used when asking the series of questions to categorize a vulnerability's priority.` (L259, 15). ExecC2Capture's Q4 nav pin `CISA BOD 26-04 Response Model` (L68, occ 1) is acceptable **only** as a navigation-mention record, never as methodology support.

**Not acceptable as quotes:** `SSVC: Stakeholder-Specific Vulnerability Categorization` occurs 3× (L3 title, L116 nav, +1) — if used as the title-anchor quote it must carry `anchor: 3`; and `SSVC stands for A Stakeholder-Specific Vulnerability Categorization.` is **home-page-only** (0 hits in the bound overview capture) — quoting it would cite an unbound source and fail the binding.

## 4. Pitfalls flagged

- **P1 — stale URL literal in the plan text (must-fix).** The `ScribeEntryF20`/`ScribeRowS054` item texts still say `https://certcc.github.io/SSVC/`; claims-erratum-1 (commit `b3620681`) corrected the capture URL to the overview tutorial and states row cell, manifest record, and capture all use the corrected URL (binding rule B5: exactly one `https://` token per row). The entry's `source:` header and `recheck:` manifest must carry the corrected URL. Verified reason: the home page body has only the definition sentence + nav (home L202-205); all decision-point/outcome text lives on the overview page.
- **P2 — the plan's example falsifiable rule is not checkable against the pinned capture (must-fix before drafting).** "a decision with exploitation=active maps to a higher priority outcome than one with exploitation=none in the deployer model — check the outcome table": the outcome/decision tables are separate pages (nav L198-210: `Outcomes`, `Decision Tables` under Code). The capture supports instead: (a) the Exploitation value ladder None/Public PoC/Active with definitions (L284-295, A11/A12) — `Exploitation (ssvc:E:1.1.0)`; (b) CERT/CC's own publication monotonicity (L467, A2); (c) the priority categories "listed in increasing order of priority" (L261, A6). Re-anchor the rule to one of these; a rule the entry's own capture cannot check fails Q3/Q5 and would be a claim the page does not state.
- **P3 — do not confuse SSVC with CVSS/KEV/EPSS, and do not overstate the separation either.** On this page `CVSS` (L69-71, L156-158), `EPSS` (L90-94: `EPSS Probability as input to Exploitation`), and `In KEV` (L153, under CISA-based decision points) appear **only as navigation** to companion pages — the prose contrast is "technical severity / exploitability" vs "risk to the concerned stakeholder" (L247, L473). So: (i) never quote a nav line as if it were methodology; (ii) the "distinct from CVSS severity, KEV catalog status and EPSS likelihood" framing (frozen predicate + row `teaches`) is **lane analysis** and must be labelled as such; (iii) the nav evidence cuts against any "SSVC excludes/ignores/replaces those signals" phrasing — the SSVC docs themselves ship integrations where EPSS probability and KEV membership become decision-point *inputs*. Correct shape (matching the plan's overlap paragraph): SSVC outputs stakeholder-specific priority categories/actions (L259, L262-265); it is not itself a probability (EPSS), a catalog listing (KEV), or a severity score (CVSS); those signals can enter as inputs. Junk controls J2 ("replaces CVSS") and J4 ("0-1 exploitability score") are correctly rejected (verified: both `MISMATCH reason=quote-not-found`, exit 1).
- **P4 — vendor over-generalization (keep CERT/CC attribution).** Attribute every methodology sentence to CERT/CC's SSVC documentation; do not generalize the four example categories (Defer/Scheduled/Out-of-cycle/Immediate, L262-265) into a universal standard ("We provide these categories as examples", L261), the three roles into an exhaustive taxonomy (L257), or CERT/CC's coordinator practice into all coordinators' ("other coordinators might make different decisions", L268). `FIRST` appears 0× — junk J3 ("maintained by FIRST") is properly rejected; never introduce it.
- **P5 — claiming behaviors the page does not state.** Rejected set verified: fixed remediation deadline (J1 — the page's only clock language is advisory, "perhaps within 90 days", L266, and Defer "not 'do not act at all'", A7), numeric exploitability score (J4), FIRST maintenance (J3), CVSS replacement (J2). Add from my read: no deployer-tree outcome mapping on this page (P2), no acronym-expansion sentence (§3), no claim that SSVC timestamps are enforced — L477 says decisions "should always be timestamped" (advisory), quotable only as CERT/CC's recommendation.

## 5. Verdict

**Plan approved with two must-fix conditions and three phrasing guards.** (1) All URLs/anchors bind to the erratum-1 overview capture (`ff3f3b2c…5fdce21`), never the home page; (2) the falsifiable rule must be re-anchored to capture-checkable text (A2/A6 or the Exploitation value ladder A11/A12). Guards: attribute to CERT/CC (footer-only Carnegie Mellon; no FIRST), phrase the CVSS/KEV/EPSS distinction as different-question-with-optional-inputs (lane analysis, labelled), and keep the page's advisory voice. With those, every load-bearing claim is quotable from the pinned capture: the four sibling-pinned quotes plus my §3 list all pass ≤25 words / exactly-once / anchor-verified through `source-recheck.py` (exit 0), and the fabricated controls fail closed (exit 1/2).

Scope limits: static review of a plan + live-page capture; I did not draft or land the entry, did not run the round-37 manifest in the lane (it is not yet committed), and did not re-derive the C1 suite. Tooling: none installed; used the lane's own `capture-source.py` / `source-recheck.py` copied byte-for-byte into scratch. Scratch `/fast/scratch/hyaku/kasegi-r37/RevEntryF20/` removed after this receipt was written.
