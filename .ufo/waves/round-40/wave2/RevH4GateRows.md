# RevH4GateRows — round-40 falsify wave 2 — H4 attack: round-39 Gate rejected-row blocks (S056/S058/S059)

- Seat `RevH4GateRows` (reviewer, leaf); lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `a7af2ce63bce153757d39bf66b366a96caf30c13`, claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`, verification ref Y = lane tip `3074c7679d6f527ec3930d7748ccce1dbae4a58a`.
- Axes: `depth:verifiability`, `coverage`. Item: attack the round-39 lesson `## Gate` rejected-row evidence blocks for S056/S058/S059 (the "Gate additions (round 40, verifier R6)" fix) — each block must carry a URL, an access date, and a ≤25-word located quote, and every quote must re-locate in the live source.
- Disk guard at start: `/tmp 3% 125.2G free`, `/var/tmp 35% 585.1G`, `/fast/scratch/hyaku 24% 615.8G` — green.

## 1. What was attacked

At Y, `corpus/lessons/round-39.md` (105 lines) carries:

- `### Rejected` bullets at `:37-42` — reason+flip only, no URL/date/quote (the pre-R6 state; R6 routed this as a defect: `corpus/lessons/round-39-verifier-spotcheck.md:183-185` — "Gate rows for the three rejects lack URL/date/quote … Append them").
- The fix under attack: `## Gate additions (round 40, verifier R6)` at `:101`, three bullets at `:103-105`, byte-identical to the wave-1 deliverable `.ufo/waves/round-40/wave1/ExecH4GateRows.txt` (diff clean, verified below).

The blocks (verbatim, at Y):

```
:103  - **S056 — CISA, Minimum Requirements for VEX.** URL `https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex`; accessed 2026-10-26; quote at the publication-page summary paragraph (raw HTML L1146 of the fetched bytes): "These elements are derived from, but may not fully conform to, existing VEX documentation and implementations." (16 words).
:104  - **S058 — OpenVEX Specification v0.2.0.** URL `https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md`; accessed 2026-10-26; quote at `OPENVEX-SPEC.md:373` (section `### Status Justifications`, heading L362, table row `component_not_present`): "The product is not affected by the vulnerability because the component is not included." (14 words).
:105  - **S059 — CycloneDX v1.7 JSON Reference, vulnerability analysis.** URL `https://cyclonedx.org/docs/1.7/json/`; accessed 2026-10-26; quote at section `vulnerabilities[].analysis.state` (anchor `#vulnerabilities_items_analysis_state`; rendered text L24567, raw HTML L770): "Declares the current state of an occurrence of a vulnerability, after automated or manual analysis." (15 words).
```

## 2. Element checklist (block shape)

| row | block line | URL present | access date | quote words (claimed / measured) | locator |
|---|---|---|---|---|---|
| S056 | :103 | yes (matches registry row `corpus/SOURCES.md:63` URL exactly) | `2026-10-26` | 16 / 16 | raw HTML L1146, "publication-page summary paragraph" |
| S058 | :104 | yes (raw form of registry row `:64`'s `github.com/…blob/main` URL) | `2026-10-26` | 14 / 14 | `OPENVEX-SPEC.md:373`, heading L362, row `component_not_present` |
| S059 | :105 | yes (matches registry row `:65` URL exactly) | `2026-10-26` | 15 / 15 | anchor `#vulnerabilities_items_analysis_state`, rendered text L24567, raw HTML L770 |

Word counts measured by whitespace split (`wc -w` and Python `split()` agree): 16, 14, 15 — all ≤25, all matching the blocks' claimed counts. No block lacks any of the three elements.

## 3. Live re-location (the attack proper)

Fetch ledger (curl `-sS -L --max-time 90 -A kasegi-shokunin/1.0`, this seat, scratch `S=/fast/scratch/hyaku/kasegi-r40/RevH4GateRows`):

| fetch | URL | HTTP | bytes | sha256 | UTC |
|---|---|---|---|---|---|
| S056 | cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex | 200 | 49,253 | `67bafe172cb7ba5cee8938235abce59ca2a0069d96c65fa1078dc42f05a8eab8` | 2026-10-26T22:07:22Z |
| S058 | raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md | 200 | 30,580 | `9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884` | 2026-10-26T22:07:22Z |
| S059 | cyclonedx.org/docs/1.7/json/ | 200 | 6,419,901 | `39aad0c6d63919e092d95e67fcf8d4124dde85cc5a6c389b9d10774a873a40e2` | 2026-10-26T22:07:24Z |
| S059 refetch | same | 200 | 6,419,901 | `064a6affbe6f93b8ff7945773021dc96bfaeb28edd8045073d5e84088db3375f` | same session (time not captured) |

Quote re-location in the fetched bytes (Python `bytes.count`/`find`, plus line reads):

| row | quote occurrence | pinned line hit? | context pins verified |
|---|---|---|---|
| S056 | 1 | yes — quote at raw HTML **L1146** exactly | line 1146 is `<p>This document specifies the minimum elements … These elements are derived from, …</p>` inside `<div class="l-page-section__content">` — the publication-page summary paragraph as claimed |
| S058 | 1 | yes — quote at **L373** exactly | line 373 is the `` `component_not_present` `` table row; `### Status Justifications` heading at **L362** exactly; live H1 is `# OpenVEX Specification v0.2.0`, matching the block's title |
| S059 | 1 (in both fetches) | yes — quote at raw HTML **L770** in both | line 770 contains the exact anchor `id="vulnerabilities_items_analysis_state"` and the quote inside that card-body (`…analysis.state` accordion) |

Byte offsets: S059 quote first offset **4,189,124** in my fetch — identical to wave-1's recorded offset despite a different raw digest. S056 quote offset 36,996 (see O1).

## 4. Cross-checks

- **Digest anchors.** S056 and S058 fetch digests are byte-identical to the committed round-38 ledger anchors in their registry rows (`67bafe17…a8eab8`, `9375415c…19f884` — `corpus/SOURCES.md:63,64,131,132`), so the pinned line numbers are reproducible against the recorded bytes. S059's raw digest differs from the ledger (`afb22b46…88f3f9`) and from every other fetch (wave-1 ×2: `c5384e39…`, `ccbf7e69…`; mine ×2: `39aad0c6…`, `064a6aff…`) at the same 6,419,901-byte length — the drift the lane already documents (`S060` row: Cloudflare email tokens; `wave1/ScoutF23Lead.md:40`). The committed block pins no digest for S059, and the quote re-located at L770 in every fetch checked, so nothing committed is contradicted.
- **Rendered-text pin L24567 reproduced.** Normalizing my S059 fetch (strip `<script>/<style>`, tags→newline, entities decoded, blank lines dropped, whitespace collapsed) puts the quote at exactly line **24567** (1 occurrence; 33,978 total lines). It also falls inside the r38 ledger's `analysis.state` stripped-text range L24562-L24582 — two independent strippers agree on the region. Wave-1's extra S056 pin "normalized visible-text line 107" also reproduces (exactly 107) under the same normalization.
- **Deliverable byte-exactness.** `git show HEAD:.ufo/waves/round-40/wave1/ExecH4GateRows.txt` vs lesson lines 103-105: `diff` clean — the committed additions are byte-identical to the wave-1 deliverable.
- **Freeze state.** At claims-freeze `5e985b7`, `grep -c 'Gate additions'` on round-39.md = 0 — the additions are round-40 wave-1 work landing after freeze, present at Y. The attacked delta is the right one.
- **Suite scope note.** The C1 suite's own H4 check (`corpus/instruments/r40-closure.sh:640-706`) is shape-only: URL token + ISO date + location token + one double-quoted 1..25-word span per row id. It cannot verify quote-vs-live-source. This seat's live re-location is the complementary evidence and it is green; the suite's H4 selftest mutations (nos059/oversize/nourl) are not re-run here (C1's lane, other seats).

## 5. Findings

**Verdict: REPRODUCED — no defect.** All three rejected-row blocks carry a URL, an access date, and a ≤25-word located quote; every quote re-locates in fresh live fetches at exactly the pinned positions (S056 L1146; S058 L373 with heading L362 and row `component_not_present`; S059 raw HTML L770 with exact anchor id, rendered-text L24567 reproduced). The R6 demand ("Append them") is satisfied.

Minor observations (none contradict a committed claim):

- **O1 — wave-1 receipt S056 byte offset off by 10.** `wave1/ExecH4GateRows.md` §3 records "byte offset 36,986" for the S056 quote; the byte-identical bytes (same sha256) put the quote at 36,996 (offset 36,986 lands on `document. ` immediately before it). The committed block carries no byte offset, so only the receipt prose is imprecise.
- **O2 — landing point differs from the wave-1 receipt's plan.** The receipt planned the three bullets inside `### Rejected` (after `:42`); at Y they sit in the separate `## Gate additions (round 40, verifier R6)` section at `:101-105`. Content is byte-identical; the labeled section is arguably clearer (round-40 additions not mixed into the round-39 list). Integration choice, not a defect.
- **O3 — S059 page not byte-stable** (5 fetches on 2026-10-26, same length, 5 distinct digests; quote at L770 in all checked). Already documented by the lane; the block correctly pins anchor+quote, not a digest.
- **O4 — S058 block URL form** is the `raw.githubusercontent.com` fetch URL while the registry row anchors the `github.com/…blob/main` human URL; same content, block URL is the one that returns the quoted bytes.

No captures exist for S056/S058/S059 (rejected rows; `corpus/source-snapshots/` holds only S057 for round 39) and the blocks claim none — consistent.

## 6. Scope and hygiene

- Writes: only this receipt `.ufo/waves/round-40/wave2/RevH4GateRows.md` plus scratch under `S=/fast/scratch/hyaku/kasegi-r40/RevH4GateRows` (removed before yield). No lane/tracked file, fleet-root file, sibling repo, PATH dir, config, or service touched; no fixture needed (no defect found).
- Read-only git only (`show/ls-tree/status/rev-parse`); no git/jj mutation; no subagent dispatch; no tool installation; no campaign tool run in `shokuknow`.
- Fetches: 4 (ledger §3), all HTTP 200, UA `kasegi-shokunin/1.0`, `--max-time 90`.
