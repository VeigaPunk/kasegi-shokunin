# Round 45 — Kasegi

Lane: `kasegi`; attempt `<L1 fills>`. Round-open base: `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`. Frozen claims commit: `8cf62c879e6e6b031e67412f8fac1fba0bd378cf` (freeze record `.ufo/waves/round-45/freeze.txt`, `claims-sha256 bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`). Frozen claims are `.ufo/waves/round-45/claims.json`; they were not edited. C1 targets five routed round-44 defects (items 1–5 of `corpus/lessons/round-44-verifier-spotcheck.md` §6) on `depth:verifiability`; C2 targets frontier F27, the Linux kernel security-bugs reporting process, on `coverage`.

## Mistakes

| ID | Class | Error | Evidence pointer | Captured by | Correction / fix | Evidence that the correction can fail closed |
|---|---|---|---|---|---|---|
| M45-1 | stale-premise | S070 was rejected because its "accessible body is a JavaScript shell", on a meta-description read of a plain page capture. The same directory is readable through the article API the lane used to admit S069 (10,029-character body; overview, no program-specific rule beyond S069 Q5). The reject rested on a premise that was never checked with the admit's capture method. The row's flip condition is vacuous (spot-check §6 item 1). | `corpus/SOURCES.md:76` (S070 status `rejected`; reason cell "the page's accessible body is a JavaScript shell"); `corpus/lessons/round-44.md:22` and `:131` (the same premise in the Gate); `corpus/lessons/round-44-verifier-spotcheck.md:66` (§4 row: the article API returns the body) and `:79` (§6 item 1) | none, so routed to R49 (the QUALITY criterion drafted in `wave1/R45ScribeQuality.draft/`). Checked at base: `grep -niE 'capture method\|parity\|capture-method' corpus/QUALITY.md` prints nothing. | R1: new registry row S072 whose `teaches` opens `supersedes S070 —`, status `rejected`, a `flip:` clause, the sha-pinned article-API capture `corpus/source-snapshots/round-45/S072.txt` (sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`); S070 row byte-identical to base; a `Correction (round 45` line appended to `corpus/lessons/round-44.md` (drafted by `wave1/R45ScribeCorrections.draft/`); R49 criterion in `corpus/QUALITY.md`, enforced by `corpus/instruments/source-recheck.py`. Counter limb R1 in `corpus/instruments/r45-routed-defects.py`. | `<L1 fills>` the "fix shown able to fail" row: red-before receipt path, the exact `limb R1 ...` line it printed on the tree with the pre-correction S070 row only, and its exit code. |

Class note: `stale-premise`, not `scope`. The scope verdict (reject: overview, no program rule beyond S069 Q5) survived; the premise under it (body unreadable) was false under the admit's capture method. `<L1 confirms class>`.

## Gate — frontier, source, and rejection

Each row is a single located quote, verified by `sed -n` against the pinned snapshot. Access date for both rows: 2026-10-28.

| Row | URL | Access (UTC capture) | Quote (≤25 words) | Located at | Verification output |
|---|---|---|---|---|---|
| S071 — admit, tier A, `mined`, F27 | `https://docs.kernel.org/process/security-bugs.html`; capture `https://docs.kernel.org/_sources/process/security-bugs.rst.txt` (manifest `capture_url`, final_url, HTTP 200) | 2026-10-28 (`fetched_utc` 2026-10-28T20:52:44Z) | "for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days" (21 words) | `corpus/source-snapshots/round-45/S071.txt:310-311` | `sed -n '310,311p'` → "the reporter or an affected party for up to 7 calendar days from the start" / "of the release process, with an exceptional extension to 14 calendar days" |
| S072 — reject with correction, tier `<L1 fills>`, supersedes S070 | `https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section` (manifest `url`, `capture_url`, final_url, HTTP 200) | 2026-10-28 (`fetched_utc` 2026-10-28T20:53:00Z) | "Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data" (16 words) | `corpus/source-snapshots/round-45/S072.txt:148-149` | `sed -n '148,149p'` → "<td>Security issues affecting any Google Cloud product or web service that" / "handles reasonably sensitive user data" |

S072 supporting facts (for the corrected reject reason, not a second admit quote):

- Overview: "an overview of the different vulnerability reward programs Google maintains" at `S072.txt:2-3`.
- No customer-resource rule: `grep -ci customer corpus/source-snapshots/round-45/S072.txt` → `0`.
- Corrected reject reason: overview with no program-specific rule beyond S069 Q5 (`S072.txt:148-149` restates the Q5 scope phrase).

Frozen-core quotes in the S071 snapshot, which the F27 knowledge entry must cite (all re-located in the pinned snapshot; the admit row above is Q1):

| Core | Located quote | Lines | Verification output |
|---|---|---|---|
| 7-day ceiling, 14-day exception | see S071 row above | `S071.txt:310-311` | as above |
| AI-found bugs treated as public | "If you resorted to AI assistance to identify a bug, you must treat it as public" | `S071.txt:95-96` | `sed -n '95,96p'` → "**If you resorted to AI assistance to identify a bug, you must treat it as" / "public**." |
| Binary-only reproducers refused | "Binary-only executables are not accepted." | `S071.txt:39-40` | `sed -n '39,40p'` → "instructions, file-system image etc).  Binary-only executables are not" / "accepted.  Working exploits are extremely helpful and will not be released" |
| Unreproducible is not exploitable | "By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug." | `S071.txt:41-43` | `sed -n '41,43p'` → "without consent from the reporter, unless they are already public.  By" / "definition if an issue cannot be reproduced, it is not exploitable, thus it" / "is not a security bug." |

F27 row and knowledge entry `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`: `<L1 fills: landed at tip; cites the four cores above>`.

## Status, recheck and used-by changes (old → new)

None expected among pre-existing rows. Verified at base: the S070 row has status `rejected`, recheck `180d`, used-by `—`. Expected after landing: status `rejected` → `rejected`; recheck `180d` → `180d`; used-by `—` → `—`. The correction changes the reason text only, appended, not a cell change. `<L1 confirms at tip>`.

New rows: S071 (`mined`, tier A) and S072 (`rejected`). Counts: SOURCES rows 70 → 72; frontier rows 26 → 27; knowledge entries 63 → 64.

## Wave and result

- Wave: `<L1 fills: wave id, seat count, settled count>`. Wave-1 spec has 64 items (`.ufo/waves/round-45/wave1-spec.json`).
- Do-nothing base, re-run by the drafter on the freeze-committed counter bytes (`git archive 8cf62c8 corpus/instruments`) against the pure base export:
  - C1: `routed-defects total=5 fixed=0 unresolved=5 exit=1`. Limb lines: R1 `fixed=0 read=row-S072=absent`; R2 `fixed=0 read=quality-not-append-only-or-unchanged`; R3 `fixed=0 read=selftest-rc=2-tokens=None`; R4 `fixed=0 read=freeze-check-absent`; R5 `fixed=0 read=refiled-absent`.
  - C2: `c2-gate fixed=1/7 exit=1`. Gates: G1 `rows=26 admitted=26`; G2 `F27-rows=0`; G3 `row-S071=absent-or-malformed`; G4 `manifest-absent`; G5 `F27-rows=0`; G6 `knowledge=63`; G7 `census-rc=0`. Secondary: `frontier expected=27 admitted=26 verdict=SHORT exit=1`.
  - Freeze control (`.ufo/waves/round-45/controls/freeze-controls.txt`, not re-run by the drafter): `controls total=5 red=5 green=0`.
- Final lane revision: `<L1 fills>` C1 `routed-defects total=5 fixed=5 unresolved=0 exit=0` and C2 `c2-gate fixed=7/7 exit=0` (the frozen expectations; the L1 fills the actual lines).
- Census and recheck gates: `<L1 fills>`.
- Score and trend verdicts: `<L1 fills>`.

## Assimilation and open questions

Assimilation: none.

Open questions for the L1 (not resolved by this draft):

1. S072 manifest quote Q2 has `anchor` 1, but its text is located at `S072.txt:2-3`. `corpus/instruments/source-recheck.py` still prints `S072:Q2 OK ... anchor=1-ok` because its anchor check reads a four-line window from the anchor. A located quote should carry the true line. `<L1 fills: correct the manifest anchor, or disclose>`.
2. Registry URL for S072: the manifest `url` is the article-API URL, whereas the S070 row carries the HTML URL. The manifest `url` must match one registry-row URL (R20), so the S072 row URL is the API URL. `<L1 confirms>`.
3. S072 tier letter and its checkable `flip:` clause (the counter requires the clause). `<L1 fills>`.
4. Several S071 quotes wrap across lines. A line-anchored `grep -F` misses them; normalised matching finds them. Limitation, not a defect.
5. Sibling seats: at drafting, `.ufo/waves/round-45/wave1/` held only `R45ScribeRowsB.draft`. `<L1 confirms no sibling reported otherwise>`.
