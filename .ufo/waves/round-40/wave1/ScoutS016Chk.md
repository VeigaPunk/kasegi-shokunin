# ScoutS016Chk — independent cross-check of ScoutS016's S016 capture

Role: attack-on-build reviewer for wave-1 seat ScoutS016 (row S016, https://www.anthropic.com/coordinated-vulnerability-disclosure). I did not trust the scout's receipt: every number below is from bytes I fetched or files I hashed myself, 2026-10-26. No tools installed; no lane/fleet file besides my deliverable + this receipt touched; scratch removed.

## Deliverable
- `ScoutS016Chk.txt` — 1 line, 993 bytes, sha256 8a750865391d599bf52014c88737648dd2ad8ec84272be9476f705bb7f0d964c.

## 1. Mechanical verification — all pass

Independent refetch with the prescribed incantation (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`), 2026-10-26T21:17:21Z:
- `HTTP_STATUS=200 FINAL_URL=https://www.anthropic.com/coordinated-vulnerability-disclosure SIZE=164126` (0 redirects)
- raw sha256 `fa4e70bc2217b566be7dec67fe0bacc2fe32fd81d6308c177410852220eac56d`

Against `ScoutS016.manifest-record.json` (fetched_utc 2026-10-26T21:15:52Z):
| field | manifest | my refetch | match |
|---|---|---|---|
| status | 200 | 200 | yes |
| raw_bytes / size_bytes | 164126 | 164126 | yes |
| raw_sha256 | fa4e70bc…ac56d | fa4e70bc…ac56d | yes (two fetches ~90 s apart byte-identical) |
| snapshot sha256 / snapshot_bytes / lines | 91cc996f…957a3b / 4481 / 32 | sha256sum of `ScoutS016.capture.txt` = 91cc996f…957a3b, wc -c 4481, wc -l 32 | yes |

Faithfulness of the extraction (not just self-consistency): I ran the lane's own instrument over my raw refetch — `html_to_text()` from `corpus/instruments/capture-source.py` — and got 4481 bytes, sha256 `91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b`: byte-identical to the shipped snapshot. The capture is reproducible from the live page, independently of the scout's environment.

Quotes in capture (`grep -c`, each ≥1):
- Q1 `Reports originating from AI-powered discovery are clearly labeled as such.` → 1, anchor L17 = the "Vulnerability Disclosure Reporting and Coordination" paragraph — anchor correct.
- Q2 `Once a patch is available, we would generally wait 45 days before publishing full technical details.` → 1, anchor L16 "Patch Details" — correct.
- Q3 `For actively exploited critical vulnerabilities, we target a 7-day timeline for a patch or mitigation.` → 1, anchor L12 — correct.
- Word counts 10 / 16 / 15 — all ≤25 (QUALITY.md Q3 bound). Quote text also occurs in the raw HTML (`grep -c 'AI-powered discovery'` on raw = 1), so it is not an extraction artifact.
- Registry row SOURCES.md:22 ("last updated 2026-03-06") matches capture L6 ("Last updated Mar 6, 2026") — right page, right revision.

## 2. Verdict assessment per QUALITY.md Q1-Q6 and the corpus guide

Where the criteria live: Q1-Q6 are corpus/QUALITY.md:14-19 ("An entry failing any of Q1–Q6 is rejected", :28). No file named CORPUS.md exists in the lane at maxdepth 2; the corpus guide is corpus/README.md (frontier rows F01-F22 at :202-:506, all `admitted`). I assessed against both.

`mined` = new ground not already held; `rejected` = covered/superseded or Q1-Q6 failure.

- **Reachable + substantive (a):** yes. First-party Anthropic policy prose at capture L5-L17 (~3.2 KB of policy body; L1-L4/L18-L32 site chrome).
- **New ground (b): yes — nothing in the lane holds it.** My own greps, independent of ScoutS016's receipt:
  - F01-F22 (README.md): F02 = coordinated-disclosure timelines (S003 CERT guide, S004 45-day receiver clock, S005 90+14); F04 = AI-assisted finding *validation* (S009-S012); F10 = vendor policies as corpus objects (S036-S040); F15 = vendor research programme as intake route (S048). No row covers an AI-discoverer's **outbound** disclosure policy. No AI-vendor-policy F-row exists.
  - Distinctive S016 content greps over corpus/knowledge/: "AI-powered discovery", "provenance label…", "labeled as such", "submission pacing" — zero policy-content hits. "45 days" hits are only S004 (Project Zero receiver-side 45-day clock, coordinated-disclosure-timelines.md:22) and the Japanese statutory 45-day purchase clock (japanese-domestic-disclosure-workflow.md:69,85,91) — neither is Anthropic's discoverer-side post-patch publication buffer.
  - "anthropic" hits in knowledge/ are the lane's own VDP filings/queue notes (intake-surface.md, submitted-registry.md, vdp-disclosure-packages.md, …) plus F04's S012 quotes — Anthropic's *inbound validation harness* description, not its outbound labeling/pacing policy. Zero knowledge files cite `S016`.
- **Q1-Q6 supportability (c):** the capture can source a conforming entry: verbatim ≤25-word located quotes exist (Q3 — the three above); first-party attribution is natural and required content ("Anthropic labels/reports", Q4); falsifiable rules a reader can check against any future Anthropic report (Q5 — e.g. the 7-day exploited-clock and 45-day buffer commitments, plus the natural rejected over-generalization "no AI-origin report is labeled"); documentation-only policy page, no probing/credential content (Q6). Q1/Q2 (provenance fields, tier-A/B support) are authoring mechanics for the admitting entry, satisfiable from this capture + SOURCES row.

**Verdict: agree with ScoutS016 — recommend S016 → `mined`.** Not covered by any held entry or F-row, not superseded (the frozen-claim rejections are S022→S030 and S024→S029; neither touches S016), and Q1-Q6 are satisfiable from this capture. This also matches the frozen C2 shape (≥4 of the nine mined).

## Caveats / residual risk
- Page served with `s-maxage=300` (Next.js); content can change later — the pinned sha256s bind the 2026-10-26 fetches only. Two byte-identical fetches 90 s apart is the verification basis, not permanence.
- Manifest `sha256` is the *snapshot* hash and `raw_sha256` the raw-page hash — both checked; a naive gate comparing `sha256` against raw bytes would false-fail. Manifest `path: S016.txt` vs delivered `ScoutS016.capture.txt` — rename needed at landing (ScoutS016's receipt already flags it). `http.date` carries the second fetch's header; disclosed, cosmetic.
- The mined verdict is my recommendation as evidence for the gate; the decision itself belongs to the L1 per the C2 claim.
