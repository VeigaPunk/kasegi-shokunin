# CritSourceTruth — round-40 falsify wave 2 · source-truth attack

Seat: `CritSourceTruth` (leaf member, no subagents). Lane repo:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo). All fetches used
`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; times are UTC.

Attacked items (per seat): two newly mined rows — one from the nine (S016) and one
S060+ (S060) — plus one rejected row (S022). For each: source fetched live now, HTTP
status / bytes / sha256 compared against the manifest record, quotes re-located in the
live text, and the row's `teaches`/flip confirmed. Green re-runs are recorded as
evidence. **No defects found.**

---

## 0. Baseline checks (committed bytes, at judged head 3074c76)

- All 8 round-40 captures (`corpus/source-snapshots/round-40/*.txt`) match their manifest
  records: sha256, `snapshot_bytes`, and `lines` all equal — `records checked: 8,
  failures: none` (sweep over `manifest.json`).
- `manifest.json` committed bytes == working-tree bytes (sha256
  `b227767905a499f95b8e6e7b7ef98e143a83bc10fb70a2262e7c8dac0cbedc2c` at both).
- `corpus/instruments/source-recheck.py --manifest ... --source S016` and `--source S060`
  both green: `S016:sha256 OK` + `Q1 OK occurrences=1 anchor=17-ok`, `Q2 OK occurrence=1
  anchor=16-ok`, `Q3 OK occurrences=1 anchor=12-ok`; `S060:sha256 OK` + `Q1 OK
  occurrences=1 anchor=7-ok`, `Q2 OK occurrences=1 anchor=15-ok`, `Q3 OK occurrences=1
  anchor=50-ok`.

---

## 1. S016 — Anthropic coordinated-disclosure policy (mined, one of the nine)

**Row** (SOURCES.md): `https://www.anthropic.com/coordinated-vulnerability-disclosure`,
status `mined`, teaches: *"Ask for AI provenance labels and maintainer-aware submission
pacing when automated finding volume exceeds review capacity."* Entry:
`corpus/knowledge/anthropic-cvd-provenance-and-pacing.md`.

**Manifest record**: status 200; fetched 2026-10-26T21:15:52Z; `raw_bytes`/`size_bytes`
164126; `raw_sha256` `fa4e70bc2217b566be7dec67fe0bacc2fe32fd81d6308c177410852220eac56d`;
snapshot 32 lines / 4481 B / `sha256` `91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b`.

**Live fetch (2026-10-26T22:07:06Z)**: HTTP **200**; **164126 bytes**; final URL identical
(0 redirects); raw sha256 **`fa4e70bc…` — byte-identical to the manifest's raw record**.
Normalizing the live body with the lane's `capture-source.py html_to_text()` yields 32
lines / 4481 B / sha256 `91cc996f…` — **byte-identical to the committed snapshot S016.txt**
(`cmp` clean). Therefore every pinned quote occurs in the live text at exactly its declared
capture line.

**Quote re-location in live text (15/15 hold, all `occ=1`)**:
L8 scope sentence; L9 90-day aim; L10 "whichever comes first" default; L11 14-day
extension; L12 7-day active-exploitation target; L13 ecosystem-wide pattern; L14
7-day-overrides-maintainer + 30-day escalation; L16 45-day details buffer + deployment
rationale; L17 human-review, AI-origin label ("Reports originating from AI-powered
discovery are clearly labeled as such."), no-large-volumes, agreed-pace, and active-
exploitation pacing exemption. Manifest Q1 (L17), Q2 (L16), Q3 (L12) all `anchor=N-ok`.

**Teaches / flip confirmed**: the teaches is exactly the two source-supported clauses —
AI-origin labelling (L17) and submission pacing agreed with the maintainer (L17), with the
active-exploitation exemption (L17). Source supports both verbatim.

**Note (not a defect)**: the entry's `verified-at` block records that a second fetch on
the capture day (21:16:37Z) saw a different raw size (164307 B) and footer wording at L28;
today's live fetch (22:07:06Z) returns byte-for-byte the manifest's raw. The page's raw
is therefore variable (footer/A-B content) while the body lines L5-L17 — every quoted
line — are stable and today match the committed capture exactly. This is documented
honestly in the entry (`## Honest limit`) and changes no claim.

---

## 2. S060 — CycloneDX v1.7 JSON Reference, `analysis` subtree (mined, S060+)

**Row** (SOURCES.md): `https://cyclonedx.org/docs/1.7/json/`, status `mined`, teaches:
the six analysis states, the nine justifications and the response values (scoped
analysis-subtree capture beyond CSAF/VEX product status). Entry:
`corpus/knowledge/cyclonedx-analysis-subtree.md`.

**Manifest record**: status 200; fetched 2026-10-26T21:16:18Z; `raw_bytes` 6419901;
`raw_sha256` `4d9c10da73aedb78727cbfeefd2a07551f25acae92a0dc6900cd976d6e947874`; snapshot
111 lines / 4889 B / `sha256` `d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`; slice = title line + page-text L16060-L16169.

**Live fetch (2026-10-26T22:07:13Z)**: HTTP **200**; **6419901 bytes** (equals
`raw_bytes` exactly); final URL identical. Raw sha256 `c7dc9995f422d2796782a801387791478b526e823824594bd4f32fb180f6aa9d` — differs from the recorded raw digest, matching the manifest/entry's documented cause: the raw page carries Cloudflare `data-cfemail` mail-obfuscation tokens (68 markers present in today's raw), which churn between fetches without changing size or normalized text.

**Normalized live page**: 22794 lines (recorded page was 22795; the one-line deficit lies after the slice — the slice region itself is byte-identical, verified below).

**Slice re-derivation**: live normalized lines 16060-16169 (110 lines) are **byte-identical** to committed S060.txt L2-L111 (`diff` clean); live title line == capture L1. Hence the whole capture is re-derived from live text.

**Quote re-location in live text (14/14 hold in the live slice)**: L4 impact/exploitability definition; L7 state definition; L15 not_affected + "Justification should be specified…"; L18 justification rationale; L32 response definition + "More than one response is allowed." + encouraged-for-exploitable; L44 detail `should` sentence; L47 firstIssued; L50 lastUpdated; L53 affects; L71 zero-or-more versions; L105 `Type: enum (of string) Default: "affected"`; L106 version-status definition. Manifest Q1 (L7), Q2 (L15), Q3 (L50) all `anchor=N-ok`.

**Teaches / flip confirmed**: live slice contains exactly the six `state` values (L10-L15), nine `justification` values (L21-L29), five `response` values (L37-L41) and three version `status` values (L109-L111), matching the teaches cell and the F23 admission. The round-39 S059 flip clause (scoped analysis-subtree capture) is satisfied by this capture. Minor wording note only: the row's "nine not-affected justifications" is a slight compression — the page defines nine general justifications and recommends them for `not_affected` cases (L15); the entry itself always says "nine reasons/justifications" and is precise.

---

## 3. S022 — CNA Operational Rules v4.1.0 (rejected, one of the nine)

**Row** (SOURCES.md): `https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf`, status `rejected`; reason+flip recorded in row and lesson Gate: superseded by S030 (v4.2.0), later itself superseded by S031 (v4.2.6, current). No capture/manifest record exists (rejected rows carry none), so this verdict compares the row's recorded claims against the live source.

**Live fetches (2026-10-26T22:07:25Z)**:
- `CNA_Rules_v4.1.0.pdf`: HTTP **200**, 250107 bytes, final URL identical (0 redirects), sha256 `9c55618efcc632b2b498e87ecf8eb9dcc2c724754b6bfacf5270f6b606b29cf0`. `pdftotext`: "Version 4.1.0 / Effective May 14, 2025 / Approved by CVE Board on May 14, 2025" — matches the row's recorded `effective and approved 2025-05-14`.
- `CNA_Rules_v4.2.6.pdf` (current version, per S031): HTTP **200**, 271367 bytes, sha256 `e296c9376cabcd09879f03920d99bb17e545a0e9c270d94478e45eda99677a22`. `pdftotext`: "Version: 4.2.6 / Approved date: 2026-October-14 / Effective date: 2026-October-20" — matches S031.

**Flip confirmed**: v4.1.0 is not current; the live rules have moved to 4.2.6 (itself newer than the 4.2.0 that superseded 4.1.0). The rejection reason is therefore not merely standing but reinforced — no citing source quotes v4.1.0 section numbering that 4.2.x no longer holds, so the flip condition does not fire. Rejection is consistent with the live source.

---

## 4. Verdict

| source | item | live status | live bytes | raw sha256 vs manifest | normalized/quote check | teaches/flip |
|---|---|---|---|---|---|---|
| S016 | mined (nine) | 200 | 164126 = recorded | **identical** (`fa4e70bc…`) | snapshot re-derived byte-identical; 15/15 quotes on recorded lines | confirmed |
| S060 | mined (S060+) | 200 | 6419901 = recorded | differs (documented Cloudflare cfemail churn; 68 markers) | slice re-derived byte-identical; 14/14 quotes in live slice | confirmed |
| S022 | rejected (nine) | 200 (both PDFs) | 250107 / 271367 | no manifest record (rejected) | version stamps match row + S031; supersession live-confirmed | confirmed |

**Defects found: 0.** No failed byte-identity, no missing/moved quote. The only raw-digest
delta (S060) is exactly the one the manifest and entry disclose (Cloudflare mail-
obfuscation tokens), with raw bytes and normalized slice identical; the S016 raw is today
byte-identical to the record despite the entry's honest note about footer instability on
the capture day.

Evidence artifacts (scratch, removed at yield): `live/s016-raw.html`, `live/s016-live.txt`,
`live/s060-raw.html`, `live/s060-full.txt`, `live/s060-live-slice.txt`,
`live/s022-cna-v4.1.0.pdf`, `live/s022-cna-v4.2.6.pdf`, `live/cna-roles.html`.
All numbers above were computed from those bytes.
