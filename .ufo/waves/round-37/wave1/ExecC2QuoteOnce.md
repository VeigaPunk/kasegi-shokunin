# ExecC2QuoteOnce — occurrence-count pin for the S054 quotes (round 37, C2 / coverage)

Seat: `ExecC2QuoteOnce` (leaf, executor). Item: pin the occurrence rule for the four S054 quotes.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat except this receipt and scratch).
No file in the lane repo was written except this receipt; no git command was mutating.

## 1. Pin identity

| page | url | status | fetched_bytes | snapshot_bytes | lines | sha256 | fetched_utc |
|---|---|---|---|---|---|---|---|
| primary (pin) | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | 200 | 143053 | 32623 | 518 | `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21` | 2026-10-26T17:02:11Z |
| control (home) | `https://certcc.github.io/SSVC/` | 200 | 105807 | 7730 | 286 | `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56` | 2026-10-26T17:02:11Z |

Both fetched with the lane's own `corpus/instruments/capture-source.py` (UA `kasegi-shokunin/1.0`), so the
normalization is the instrument's `html_to_text()`: `<script>/<style>` removed, block tags (`p div li tr
h1-h6 section article br`) to newlines, remaining tags stripped, `html.unescape()`, runs of space/tab/NBSP
collapsed, blank lines dropped, UTF-8, final newline. Counts below use `source-recheck.py`'s
`normalize()` (`" ".join(text.split())`, `<u>` markup dropped) on that snapshot, i.e. exactly the rule the
manifest recheck applies.

Primary URL is the corrected literal of `claims-erratum-1.md` (commit `b3620681`) and the L1's live
message: the home page body (L202-L205) carries only the definition sentence — *"SSVC stands for A
Stakeholder-Specific Vulnerability Categorization. It is a methodology for prioritizing vulnerabilities
based on the needs of the stakeholders involved in the vulnerability management process."* — plus
navigation; the decision-point/decision-tree text and the severity/exploitability contrast exist only on
the overview page. Measured control: each of the four final quotes below occurs **0** times in the home
capture.

## 2. Final four quotes (selected, ≤25 words, load-bearing for F20)

All four are exact substrings of the normalized overview snapshot; occurrence = number of matches in the
whole normalized snapshot (`str.count`), `raw` = matches in the un-normalized snapshot bytes, `home` =
matches in the home-page snapshot, `anchor-ok` = `source-recheck.py`'s anchor window
`" ".join(lines[anchor-1:anchor+3])` contains the quote. Word count is whitespace tokens of the exact
quote string.

| id | anchor | occurrences | raw | home | words | anchor-ok | quote |
|---|---|---|---|---|---|---|---|
| Q1 | L247 | 1 | 1 | 0 | 22 | true | `Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability` |
| Q2 | L259 | 1 | 1 | 0 | 12 | true | `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.` |
| Q3 | L277 | 1 | 1 | 0 | 25 | true | `A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is` |
| Q4 | L367 | 1 | 1 | 0 | 19 | true | `Exposure refers to how difficult it would be for an attacker to access a system from the open Internet.` |

Load-bearing role of each, from the bytes:

- **Q1 (L247)** — the distinctiveness clause: other systems "rate on technical severity … or
  exploitability", SSVC rates "risk to the concerned stakeholder". This is the sentence that grounds
  F20's *distinct from CVSS severity and from exploitability/EPSS likelihood* without the capture having
  to name those systems in prose. The full sentence is 40 words, so the pin is the 22-word span ending at
  `or exploitability`; the cut is at the comma before *"(how likely it is that there will be an
  exploit)"*.
- **Q2 (L259)** — prioritization varies by stakeholder: "priority based on risk that varies among
  stakeholders"; same line states the categories "reflect the timeliness of action to be taken".
- **Q3 (L277)** — the decision-point/outcome mechanism: a decision point alone is not risk; the *series*
  of point values is what a stakeholder reads to determine risk to their operation. Exactly 25 words.
  **The page's own typo `decisions point values` must be quoted verbatim.**
- **Q4 (L367)** — a named Deployer decision point whose input is per-system: how hard the system is to
  reach from the open Internet, "determined on a per-system basis". This is the strongest single-line
  demonstration that an SSVC input is stakeholder/system-specific rather than a universal score.

Every quote has occurrences = 1, so `anchor` is not required by `source-recheck.py`'s B2 rule
(`anchor_verdict`: unique quote needs no anchor); declaring it anyway costs nothing and self-documents.
All four are ≥12 normalized chars (`MIN_QUOTE_CHARS`).

### Manifest-ready records (for `corpus/source-snapshots/round-37/manifest.json`)

```json
[
  {"id": "Q1", "quote": "Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability", "anchor": 247, "location": "L247; the distinctiveness clause of the opening contrast sentence (the full sentence is 40 words; the pin is the 22-word span ending 'or exploitability')."},
  {"id": "Q2", "quote": "SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.", "anchor": 259, "location": "L259; first sentence of 'How vulnerabilities are categorized in SSVC': priority varies by stakeholder."},
  {"id": "Q3", "quote": "A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is", "anchor": 277, "location": "L277; second sentence of 'How decision models are designed' (page typo 'decisions point values' quoted verbatim); exactly 25 words."},
  {"id": "Q4", "quote": "Exposure refers to how difficult it would be for an attacker to access a system from the open Internet.", "anchor": 367, "location": "L367; Deployer decision point Exposure, first sentence; L367-L368 adds 'determined on a per-system basis'."}
]
```

Expected `source-recheck.py` lines: `S054:sha256 OK`, then `S054:Q1 OK occurrences=1 anchor=247-ok` …
`S054:Q4 OK occurrences=1 anchor=367-ok`, exit 0.

## 3. Duplicate handled explicitly (not pinned)

The most tempting fourth decision-point quote occurs **twice**:

```
Automatable is a simple yes or no, can the attacker reliably automate all four steps (reconnaissance, weaponization, delivery, exploitation) of the kill chain?
```

- occurrences = **2** (L299 Supplier "Utility"; L389 Deployer "Automatable"); words = 23.
- Both anchors verify (`anchor=299-ok`, `anchor=389-ok`); L388 says "Automatable is the same question as
  contained in the Supplier's Utility decision point", so the two bytes are identical by design.
- Resolution used: **replaced** with unique quotes (Q2/Q4 carry the same stakeholder/per-system point).
  If a later entry wants this sentence anyway, it may pin it as e.g. `{"anchor": 389}` (Deployer) or
  `{"anchor": 299}` (Supplier Utility) and `source-recheck.py` accepts it via `anchor=N-ok`; without an
  anchor it fails `reason=occurrence-not-unique`.

## 4. Alternates measured (available, not in the four)

| anchor | occurrences | words | quote / use |
|---|---|---|---|
| L247 | 1 | 12 | `SSVC follows a stakeholder-defined decision model to make these determinations of risk.` — definition of the method |
| L259 | 1 | 15 | `Decision Trees are used when asking the series of questions to categorize a vulnerability's priority.` — tree phrasing |
| L473 | 1 | 17 | `Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach.` — final-notes restatement |
| L281 | 1 | 14 | `Exploitation refers to how much evidence currently exists that the vulnerability is being exploited.` — Exploitation (mutable evidence) |
| L391 | 1 | 18 | `Human Impact is similar to the Supplier's decision point Public Safety Impact in that it factors Safety Impact` — compound Human Impact |
| L249 | 1 | 6 | `it is not a one-size-fits-all system` — caveat (note page's doubled "define to define" earlier in the same sentence) |
| L262 | 1 | 6 | `Defer: do not act at present.` — outcome category |

If the entry cites Exploitation/Exposure/Automatable/Human Impact beyond the four pins, the honest
single-line anchors are L281 (Exploitation), L367 (Exposure), L388-L389 (Automatable), L390-L391 (Human
Impact); all of those spans occur once except the Automatable sentence above.

## 5. Attribution evidence the row/entry must not overstate

- `CERT/CC` occurs **14** times, including body lines 268, 448-453, 457, 459, 462, 466-468 ("At the
  CERT/CC, a decision to publish is determined after criteria for Publication are met", L462). The site
  nav/header reads `CERTCC/SSVC` (L6, L17); the human-readable "CERT/CC" is in the prose.
- `Carnegie` / `Mellon` occur **only in the site footer copyright** (L505-L507: "© Carnegie Mellon
  University", "CERT®, Carnegie Mellon® and CERT Coordination Center® are registered … by Carnegie
  Mellon University") — not in any SSVC methodology sentence. "CERT/CC/Carnegie Mellon" is therefore a
  site-owner statement, not a claim the overview page makes about the method's authorship.
- `severity` occurs **1** time and `exploitability` **1** time, both in the Q1 sentence (L247); the page
  does not define either, and it names no CVSS metric.
- `CVSS` 6, `EPSS` 5, `KEV` 1 — all in site navigation only (CVSS L69-L71, L156-L158; EPSS L90-L94; KEV
  L153), never in body prose. S054 therefore names those systems but grounds no definition of them; the
  F20 entry must source any CVSS/KEV/EPSS definition from S001/S002, S052 and S053, not from S054.
- `stakeholder` occurs 19 times; `decision point` is used repeatedly in body prose (L259, L277, L365,
  L391, L462-L463, L465).

## 6. Reproduction

Run from the lane root; output observed exactly as the table above (`occ`, `words`, `lines`,
`anchor_ok`; then the duplicate and vocabulary lines):

```sh
S=$(mktemp -d) && cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 corpus/instruments/capture-source.py --id S054 --url https://certcc.github.io/SSVC/tutorials/ssvc_overview/ --out "$S/S054.txt"
python3 - "$S/S054.txt" <<'PY'
import sys, importlib.util
spec=importlib.util.spec_from_file_location("sr","corpus/instruments/source-recheck.py")
sr=importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
t=open(sys.argv[1],encoding="utf-8").read(); L=t.splitlines(); n=sr.normalize(t)
qs=[(247,"Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability"),
    (259,"SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders."),
    (277,"A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is"),
    (367,"Exposure refers to how difficult it would be for an attacker to access a system from the open Internet.")]
for a,q in qs:
    w=" ".join(L[max(0,a-1):a+3])
    print(n.count(sr.normalize(q)), len(q.split()), a, sr.normalize(q) in sr.normalize(w))
PY
```

Observed for the 2026-10-26T17:02:11Z fetch: `1 22 247 True` / `1 12 259 True` / `1 25 277 True` /
`1 19 367 True`.

## 7. Risks and cautions

1. **These counts bind to sha256 `ff3f3b2c…fdce21` (518 lines).** If the committed `S054.txt` is a
   different fetch, its bytes are a new pin: re-run §6 against the committed file before filing the
   manifest. Line 247/259/277/367 numbers are only valid for this snapshot.
2. **Q3 contains the page's own typo** `decisions point values` (not "decision point values"). A
   corrected quote will read occurrences=0 and fail `reason=quote-not-found`.
3. **Q1 cuts mid-sentence** at `or exploitability`; the full sentence is 40 words. Do not pad the quote
   with an ellipsis — the recheck matches literal bytes.
4. **Q4 is one decision point, not the set.** The four-name list (Exploitation, Exposure, Automatable,
   Human Impact) cannot be one ≤25-word quote; pin one and cite the others by line as in §4.
5. **`Carnegie Mellon` is footer-only** (§5), so do not cite S054 for "authored by Carnegie Mellon";
   cite the site's copyright line (L505-L507) if the attribution is wanted at all.
6. Live-drift: the page is served from `certcc.github.io`; a later fetch may change line numbers. The
   digest, not the URL alone, is the pin.

## 8. Tooling, scope, cleanup

- No installs or upgrades (python3 stdlib + the lane's committed instruments only).
- Writes: this receipt only; scratch under `/fast/scratch/hyaku/kasegi-r37/ExecC2QuoteOnce/`
  (`S054-overview.txt`, `S054-home.txt`), removed before yield.
- No lane, fleet, sibling or source-tree file touched; no mutating git command run.
- Retained evidence: fetch lines quoted in §1 (`status=200`, byte counts, digests, UTC), the four
  `occ/words/anchor-ok` tuples in §2, the duplicate pair in §3 and the vocabulary counts in §5.
