# ScribeEntryF20 — F20 SSVC knowledge entry draft (round 37, C2 / coverage)

Seat `ScribeEntryF20` (leaf, scribe). Item: draft the complete knowledge entry
`corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` as a full file block, fetch the live
SSVC page into scratch, normalize it with the lane's `capture-source.py`, and pin a line number for every quote.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b56a41680cefd391868c1c370dc063c69d827e7d`, claims-freeze
`224df74db2a46d627ae1475a72ca48796bbd177c`; workspace `HEAD` observed `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(read-only). No lane, fleet, sibling-lane or source-tree file was written except this receipt; no mutating git command
and no package transaction was run.

## 1. Pin identity

| role | url | status | fetched_bytes | snapshot_bytes | lines | sha256 | fetched_utc |
|---|---|---|---|---|---|---|---|
| primary (the pin) | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | 200 | 143,053 | 32,623 | 518 | `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21` | 2026-10-26T17:05:59Z |
| control (docs home) | `https://certcc.github.io/SSVC/` | 200 | 105,807 | 7,730 | 286 | `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56` | 2026-10-26T17:05:13Z |

Both fetched with `corpus/instruments/capture-source.py` (UA `kasegi-shokunin/1.0`), so the snapshot is the
instrument's `html_to_text()` output: `<script>`/`<style>` removed, block tags (`p div li tr h1-h6 section article br`)
to newlines, remaining tags stripped, `html.unescape()`, space/tab/NBSP runs collapsed, blank lines dropped, UTF-8,
final newline. The primary URL is the corrected literal of `.ufo/waves/round-37/claims-erratum-1.md` (the home page
body carries only the definition sentence plus navigation; the methodology, decision points and stakeholder contrast
are on the overview tutorial page). The home capture is a control, not the pin: its body lines L202-L205 hold the
definition sentence, and the four manifest quotes occur **0** times in it (re-measured by this seat: `0 0 0 0` against the overview's `1 1 1 1`).

## 2. Delivered artifact — full file block

File: `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (84 lines; within the 60-100 line
budget). Header line 3 is `source: S054`, line 4 `verified-at: 2026-10-26`, line 5 `ground: F20`, line 6 the
executable `recheck:` line (bash -n clean, own `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix).

```markdown
# SSVC — stakeholder-specific vulnerability categorization (CERT/CC): risk to a named stakeholder, not a severity score and not a likelihood

source: S054 — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — capture corpus/source-snapshots/round-37/S054.txt (518 lines, 32,623 bytes; sha256 ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21): brand L6 and L17, title L1, risk continuum L244, supplier/deployer example L246, contrast sentence L247, caveats L249, roles L251-L257, priority synthesis L259, category ladder L261-L266, decision-point mechanism L277, Supplier Exploitation L280-L295, Deployer Exposure L366-L386, publication reuse L463-L468, nav rows EPSS L90-L94, CVSS L69-L71 and L156-L159, CISA-based nav L150-L153, footer copyright L503-L507
verified-at: 2026-10-26
ground: F20
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054   # prints S054:sha256 OK then S054:Q1 OK occurrences=1 anchor=247-ok through S054:Q4 OK occurrences=1 anchor=367-ok; exits 2 when the manifest or capture is absent and 1 when the sha256 differs or a quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

CERT/CC's own overview tutorial, read as the project's description of its own method and nothing wider (Q4). The site brand is `CERTCC/SSVC` (L6, L17); the coordinator prose speaks as an institution — "the CERT/CC" appears 14 times, L268 and L448-L468 — and the footer is "Carnegie Mellon University" (L505) with the CERT marks (L506-L507). So the method statements are first-party CERT/CC statements; "Carnegie Mellon" ownership appears only in the footer, and the tutorial body never claims authorship. Nothing here is a standard, a directive, or a claim about any other organization's practice.

## Claim 1 — the rated quantity is risk to the concerned stakeholder, not severity and not exploitability

> "Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability" — L247

The same sentence names all three quantities and finishes on its own subject: "SSVC rates vulnerabilities on risk to the concerned stakeholder." (L247, 9 words). The page opens the section with the same point — "Risk exists on a continuum, and different stakeholders have different threat models and risk appetites." (L244) — and restates it at the end: "Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach." (L473). Severity and exploitability are named as other systems' axes; they are not what SSVC rates.

The worked example makes the divergence concrete: for a Supplier that does not use the vulnerable part of a library, the page's imagined answer is "probably not" at risk, while "the upstream Supplier probably wants the vulnerability patched as quickly as possible" (L245-L246). The page's own gloss on the difference is "this vulnerability is not very risky to your business, so you are not very concerned" (L246).

## Claim 2 — the output is an ordered priority category, chosen per role, and offered as an example

> "SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders." — L259

For Suppliers and Deployers the page lists four categories "in increasing order of priority" (L261), from "Defer: do not act at present." (L262) through Scheduled (L263), Out-of-cycle (L264) and Immediate (L265). Coordinators get separate tables for triage (L269-L272) and publication (L273-L275).

Three qualifications sit in the same bytes, and each limits the output's authority:

- the categories are examples: "We provide these categories as examples and encourage Suppliers and Deployers to define prioritization categories that match their needs." (L261);
- Defer is not ignore: "Defer simply means 'do not act at present,' not 'do not act at all.'" (L266);
- the roles are a starting set: "The three aforementioned roles are not exhaustive and are only the ones for which we have created decision models so far." (L257), and "All three stakeholders, even if within the same organization, will have different perspectives on risk, and therefore have different decisions to make." (L255).

## Claim 3 — decision points feed the outcome; no single point is the risk

> "A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is" — L277 (exactly 25 words; the page's "decisions point values" is quoted verbatim)

The Supplier's first point is Exploitation (L280), a mutable evidence state with three values: "Exploitation refers to how much evidence currently exists that the vulnerability is being exploited." (L281), and L281 adds "This value is mutable because new evidence of exploit can arise at any time." None: "There is no evidence of active exploitation and no public proof of concept (PoC) of how to exploit the vulnerability." (L289). Public PoC: a typical public PoC exists or "the vulnerability has a well-known method of exploitation" (L292). Active: "Shared, observable, reliable evidence that the exploit is being used in the wild by real attackers; there is credible public reporting." (L295). The input is therefore evidence about exploitation, in three discrete classes — not a probability.

The Deployer's Exposure is explicitly per-target: "Exposure refers to how difficult it would be for an attacker to access a system from the open Internet." (L367), and L367 continues "determined on a per-system basis". Utility (L296-L314) and Human Impact (L390-L446) are declared combinations of other points (L300, L429), so the model is composed of decision points rather than one score.

## Claim 4 — the one directional priority statement the page makes is a Coordinator publication rule

> "Exploitation - If the vulnerability is being actively exploited, the CERT/CC is more likely to publish." — L467

That is the publication table, which "reuses the Exploitation decision point and adds two new ones (Supplier Involvement and Public Value Added)" (L463), and it is the CERT/CC's own practice, not a rule for other coordinators (L462). The corresponding Supplier/Deployer decision-tree table that would map Exploitation values onto Defer through Immediate is not in this capture — only its navigation row "Deployer Decision Model" (L62) is. So "active exploitation ranks above PoC-only" is checkable on the deployer model page, not here.

## Sources overlap — SSVC against KEV catalog status (F18) and EPSS likelihood (F19)

S054's own navigation shows what SSVC consumes and what it does not emit. EPSS appears only in the "Using EPSS with SSVC" branch, as an input: "EPSS Probability as input to Exploitation" (L93) and "EPSS Percentiles as an Amplifier" (L94). KEV appears once, as one CISA-based decision point: "In KEV" (L153, under "CISA-based decision points" L150-L152). CVSS appears only as separate model branches, "CVSS v4 Analyst Models" (L69-L70) and "CVSS-based decision points" (L156-L157).

The axes therefore stack rather than compete. F19's EPSS is a 0–1 probability that a published CVE will be exploited in 30 days (S053 L216) and is fed into Exploitation; F18's KEV is catalog membership carrying a per-record remediation clock (S052), usable as a decision point. SSVC consumes such exploitation evidence and emits a stakeholder-specific action category (L262-L265) — it is neither a probability nor a catalog listing, and this capture defines neither EPSS nor KEV, so their definitions must come from those entries.

## Falsifiable rule and checks

**Falsifiable rule.** A statement about SSVC is falsified by any of: (a) presenting its output as a number, probability or severity band, when the outputs are four named categories (L262-L265) and `score` occurs 0 times; (b) equating Public PoC with active exploitation, when L289 defines None as no active exploitation *and* no public PoC while L295's Active requires use in the wild by real attackers; (c) assigning one priority to a vulnerability for every stakeholder, when L255 and L259 say the priority varies; (d) treating the ladder as mandatory, when L261 calls the categories examples; (e) claiming active exploitation makes the CERT/CC *less* likely to publish, contradicting L467; (f) the four pinned quotes must each occur exactly once with the pinned digest — the `recheck:` line prints `occurrences=1` per quote and exits non-zero otherwise.

**FC-1 — every cited span is unique, ≤25 words, on its anchor line.** Observed `spans 24 occ_all_1 True words_max 25 anchors_ok 24 of 24` (list and command in the seat receipt).

**FC-2 — vocabulary.** `score=0 scoring=1 probability=1 percentile=1 severity=3 CVSS=6 EPSS=5 KEV=1 CVE=0 risk=16 priority=13`; the single `scoring` is L473's "other vulnerability scoring systems", and `probability`/`percentile` are the EPSS nav rows L93-L94.

**FC-3 — the Exploitation value set.** `grep -n` returns L289 (None definition), L292 (Public PoC definition) and L295 (Active definition); each value line L287/L290/L293 carries None/Public PoC/Active.

**FC-4 — the ladder is ordered and labelled examples.** `grep -n 'Defer: do not act at present'` returns L262; L261 says "in increasing order of priority" and "as examples".

**FC-5 — the publication mapping.** `grep -n 'more likely to publish'` returns L467 only.

**FC-6 — the input branches.** `grep -n 'input to Exploitation\|Amplifier\|In KEV'` returns L93, L94 and L153.

## Rejected over-generalizations

1. **"SSVC replaces CVSS."** Rejected: SSVC rates "risk to the concerned stakeholder" and explicitly contrasts itself with systems that "rate on technical severity" (L247); CVSS appears only as separate model branches (L69-L70, L156-L157), and `score` occurs 0 times. Severity and prioritization answer different questions, and a CVSS metric is at most an input to a decision point, not an output of SSVC.
2. **"SSVC gives a risk score."** Rejected: the outputs are four named categories (L262-L265), and a decision point "is not representative of risk" (L277); the only `scoring` in the capture describes other systems (L473).
3. **"Every organization gets the same categories."** Rejected: L261 calls them examples and invites replacements, L249 says "define to define their own decision points" (the page's doubled word), and L255 says the stakeholders' decisions differ.
4. **"Public PoC means active exploitation."** Rejected: L289's None value already excludes "public proof of concept (PoC)", so PoC-only is above None but below L295's Active, which requires evidence of use "in the wild by real attackers" plus "credible public reporting".
5. **"SSVC membership is KEV status."** Rejected: KEV occurs once, as the decision-point name "In KEV" (L153); KEV catalog status (F18/S052) is an input, and the output is a priority category, not a listing.
6. **"SSVC predicts exploitation."** Rejected: EPSS is the probability source and the site routes it as "input to Exploitation" (L93); SSVC's Exploitation takes evidence states (L289-L295), not a forecast.
7. **"Carnegie Mellon authored the method."** Rejected: the footer carries the copyright and marks (L505-L507) but the tutorial body makes no authorship statement; cite the footer if that attribution is wanted, and do not attribute a methodology sentence to it.

## Honest limit

- **One page of a documentation site.** The Supplier, Deployer and Coordinator decision tables and the whole EPSS-integration branch are named in navigation (L61-L67, L90-L94) but absent from these bytes; only the general ladder and the coordinator publication sentence are quoted as mappings here.
- **Pinned, not live.** The recheck compares this entry's quotes with the captured bytes of the fetch that produced sha256 `ff3f3b2c…fdce21`; a later fetch is a new pin, not a correction.
- **Page typos.** "define to define" (L249), "decisions point values" (L277) and "remidiation" (L251) are the page's own spellings; a quote must reproduce them.
- `verified-at: 2026-10-26` is when this entry was written and its quotes checked against the pin, not the capture instant.
- Documentation only: the capture holds no credential, session or private URL, and this entry quotes none (Q6). Nothing here authorizes probing, scanning, logging in, or submitting against any target.
```

## 3. Quote / line table

Every quotation in the entry, measured with `source-recheck.py`'s own `normalize()` (`" ".join(text.split())`,
`</?u>` markup dropped) on the 518-line snapshot: occurrence count over the whole normalized capture, word count of
the exact string, and the anchor-window test `" ".join(lines[anchor-1:anchor+3])`.

| line | words | occ | role |
|---|---|---|---|
| L247 | 22 | 1 | contrast sentence, blockquote of Claim 1 |
| L247 | 9 | 1 | the claim's own subject |
| L244 | 15 | 1 | risk continuum, page opening |
| L473 | 17 | 1 | final-notes restatement |
| L246 | 12 | 1 | worked example, upstream supplier |
| L246 | 15 | 1 | worked example, supplier's own risk |
| L259 | 12 | 1 | priority synthesis, blockquote of Claim 2 |
| L261 | 19 | 1 | categories are examples |
| L262 | 6 | 1 | ladder start |
| L266 | 14 | 1 | Defer is not ignore |
| L257 | 21 | 1 | roles not exhaustive |
| L255 | 22 | 1 | stakeholders decide differently |
| L277 | 25 | 1 | decision-point mechanism, blockquote of Claim 3 |
| L281 | 14 | 1 | Exploitation definition |
| L281 | 14 | 1 | Exploitation is mutable |
| L289 | 20 | 1 | None value |
| L292 | 8 | 1 | Public PoC value (fragment) |
| L295 | 21 | 1 | Active value |
| L367 | 19 | 1 | Deployer Exposure |
| L463 | 19 | 1 | publication reuses Exploitation |
| L467 | 16 | 1 | publication mapping, blockquote of Claim 4 |
| L93 | 6 | 1 | EPSS probability as input (nav) |
| L94 | 5 | 1 | EPSS percentiles as amplifier (nav) |
| L153 | 2 | 1 | KEV as one decision point (nav) |

Manifest correspondence: the four `source-recheck` pins are **Q1 = L247** (22 words, the contrast clause), **Q2 =
L259** (12 words), **Q3 = L277** (exactly 25 words; the page typo `decisions point values` quoted verbatim), **Q4 =
L367** (19 words, Deployer Exposure) — identical to `.ufo/waves/round-37/wave1/ExecC2QuoteOnce.md` §2, which pinned
the same four strings at the same anchors against the same digest.

Short inline fragments (each occurs exactly once, checked by `grep -F`):

| line | string | occ |
|---|---|---|
| L261 | `in increasing order of priority` | 1 |
| L249 | `define to define their own decision points` | 1 |
| L251 | `remidiation` | 1 |
| L367 | `determined on a per-system basis` | 1 |
| L473 | `other vulnerability scoring systems` | 1 |
| L62 | `Deployer Decision Model` | 1 |
| L69 | `CVSS v4 Analyst Models` | 1 |
| L150 | `CISA-based decision points` | 1 |
| L156 | `CVSS-based decision points` | 1 |
| L505 | `Carnegie Mellon University` | 1 |
| L245 | `probably not` | 1 |

Page typos quoted verbatim: `decisions point values` (L277), `define to define` (L249), `remidiation` (L251). A
corrected spelling reads `occurrences=0` and the recheck fails `reason=quote-not-found`.

## 4. Checks exercised

### 4.1 The entry's own recheck, rehearsed on identical bytes

The capture and `manifest.json` are not yet in the tree (see §5), so the lane path in the entry line cannot run yet.
I staged the manifest exactly as it will be filed — `sources[0]` id `S054`, `path` `S054.txt`, the overview URL, the
digest above, and the four Q1-Q4 assertions — beside an identical copy of the capture, and ran the instrument:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/source-recheck.py --manifest "$S/manifest.json" --source S054; echo "exit=$?"
```

Observed, exit 0 — the five lines the entry's `recheck:` note predicts:

```
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=247-ok
S054:Q2 OK occurrences=1 anchor=259-ok
S054:Q3 OK occurrences=1 anchor=277-ok
S054:Q4 OK occurrences=1 anchor=367-ok
exit=0
```

### 4.2 Fail-closed controls (Q7: a missing/corrupted source must fail)

| control | mutation | observed | exit |
|---|---|---|---|
| missing capture | manifest alone, no `S054.txt` | `S054:source UNAVAILABLE reason=missing` | 2 |
| corrupted capture | one byte appended, digest changes | `S054:sha256 MISMATCH expected=ff3f3b2c… actual=212eecc2…` | 1 |

### 4.3 Form checks

- `bash -n` on the extracted `recheck:` line: **OK**.
- Entry shape: 84 lines, H1 at line 1, header keys in order `source, verified-at, ground, recheck` at lines 3-6.

### 4.4 FC-1 — 24 spans, unique, ≤25 words, anchor verified

Observed: `spans 24 occ_all_1 True words_max 25 anchors_ok 24 of 24`. Command (run from the lane root; `$S` is the
scratch capture; the 24 `(line, quote)` pairs are those in the §3 table):

```sh
python3 - "$S/S054.txt" <<'PY'
import sys, importlib.util
spec=importlib.util.spec_from_file_location("sr","corpus/instruments/source-recheck.py")
sr=importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
t=open(sys.argv[1],encoding="utf-8").read(); L=t.splitlines(); n=sr.normalize(t)
qs=[(247,"Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability"),(247,"SSVC rates vulnerabilities on risk to the concerned stakeholder."),(244,"Risk exists on a continuum, and different stakeholders have different threat models and risk appetites."),(473,"Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach."),(246,"the upstream Supplier probably wants the vulnerability patched as quickly as possible"),(246,"this vulnerability is not very risky to your business, so you are not very concerned"),(259,"SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders."),(261,"We provide these categories as examples and encourage Suppliers and Deployers to define prioritization categories that match their needs."),(262,"Defer: do not act at present."),(266,"Defer simply means 'do not act at present,' not 'do not act at all.'"),(257,"The three aforementioned roles are not exhaustive and are only the ones for which we have created decision models so far."),(255,"All three stakeholders, even if within the same organization, will have different perspectives on risk, and therefore have different decisions to make."),(277,"A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is"),(281,"Exploitation refers to how much evidence currently exists that the vulnerability is being exploited."),(281,"This value is mutable because new evidence of exploit can arise at any time."),(289,"There is no evidence of active exploitation and no public proof of concept (PoC) of how to exploit the vulnerability."),(292,"the vulnerability has a well-known method of exploitation"),(295,"Shared, observable, reliable evidence that the exploit is being used in the wild by real attackers; there is credible public reporting."),(367,"Exposure refers to how difficult it would be for an attacker to access a system from the open Internet."),(463,"The publication decision reuses the Exploitation decision point and adds two new ones (Supplier Involvement and Public Value Added)."),(467,"Exploitation - If the vulnerability is being actively exploited, the CERT/CC is more likely to publish."),(93,"EPSS Probability as input to Exploitation"),(94,"EPSS Percentiles as an Amplifier"),(153,"In KEV")]
oc=[];wm=0;ao=0
for a,q in qs:
    nq=sr.normalize(q); w=" ".join(L[max(0,a-1):a+3]); occ=n.count(nq); ok=nq in sr.normalize(w)
    oc.append(occ); wm=max(wm,len(q.split())); ao+=ok
    print(f"L{a}\tocc={occ}\twords={len(q.split())}\tanchor_ok={ok}")
print("spans",len(qs),"occ_all_1",all(o==1 for o in oc),"words_max",wm,"anchors_ok",f"{ao} of {len(qs)}")
PY
```

### 4.5 FC-2 — vocabulary (case-insensitive `grep -oiF … | wc -l`)

`score=0 scoring=1 probability=1 percentile=1 severity=3 CVSS=6 EPSS=5 KEV=1 CVE=0 risk=16 priority=13`.
The single `scoring` is L473 "other vulnerability scoring systems"; `probability` and `percentile` are the EPSS
navigation rows L93 and L94; `severity` is L78 and L159 (nav "Qualitative Severity") plus L247 (body prose);
`CVSS` is nav only (L69-L71, L156-L158); `KEV` is L153 only.

```sh
for t in score scoring probability percentile severity CVSS EPSS KEV CVE risk priority; do printf '%s=%s ' "$t" "$(grep -oiF -- "$t" "$S/S054.txt" | wc -l)"; done; echo
```

### 4.6 FC-3..FC-6

| check | command body | observed |
|---|---|---|
| FC-3 Exploitation value set | `grep -nF` on the None / Public PoC / Active definitions | `289`, `292`, `295`; value labels on L287/L290/L293 |
| FC-4 ladder | `grep -nF 'Defer: do not act at present'`; counts of `increasing order of priority`, `as examples` | `262`; `1`; `1` |
| FC-5 publication mapping | `grep -nF 'more likely to publish'` | `467` |
| FC-6 input branches | `grep -nF 'input to Exploitation' / 'Amplifier' / 'In KEV'` | `93`, `94`, `153` |

## 5. Cross-seat consistency and pre-landing state

- Independent fetch agreement: my primary fetch produced the same 518 lines, 32,623 bytes and sha256
  `ff3f3b2c…fdce21` that `ExecC2QuoteOnce` recorded at 2026-10-26T17:02:11Z, so the normalization is deterministic and
  the entry's line numbers agree with that seat's four pins.
- Control agreement: the home-page control digest `a6613315…ce58bb56` (full: `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56`; a second fetch at 17:11:48Z produced the same bytes) matches that seat's control. I re-measured the four manifest quotes in the home capture myself under `source-recheck`'s `normalize()`: `0 0 0 0` occurrences, while the overview capture gives `1 1 1 1`. Its only prose is L202-L205 plus navigation, which reproduces the "overview page is the pin" finding without relying on the other seat's claim.
- Pre-landing tree at `b3620681`: `corpus/source-snapshots/round-37/` **absent**; `grep -c '^| S054 ' corpus/SOURCES.md`
  → `0`; `ls corpus/knowledge/*.md | wc -l` → `48`; `corpus/instruments/knowledge-expected.txt` → 50 lines (2 comment
  lines + 48 entries), `grep -c ssvc` → `0`. So the entry, the capture, the manifest, the S054 registry row and the
  expected-list sync all still have to be landed by the L1.

## 6. Limits and risks

1. **Not yet runnable in-lane.** The entry's `recheck:` points at `corpus/source-snapshots/round-37/manifest.json`,
   which does not exist at `b3620681`. §4.1 exercises the identical bytes and an identically shaped manifest record
   under scratch; the first in-lane run is the L1's post-landing check.
2. **Line numbers bind to one digest.** If the landed `S054.txt` is a different fetch, every `L<n>` in the entry and
   the four anchors in the manifest are invalid; re-derive before filing (`ExecC2QuoteOnce` §7 says the same).
3. **The capture is one page of a docs site.** Decision-tree tables, the deployer model page, the EPSS/SSC integration
   page and the CVSS analyst models are named in navigation only. The entry therefore states one directional priority
   rule (the Coordinator publication sentence, L467) and marks the deployer mapping as checkable off-capture, rather
   than quoting a mapping that is not in the bytes.
4. **Attribution.** "CERT/CC" and the method statements are the page's own; "Carnegie Mellon" is footer-only
   (L505-L507). The entry says so and refuses authorship claims the body does not make.
5. **Cross-entry facts are referenced, not re-captured.** EPSS's 30-day 0–1 probability is cited as F19/S053 L216 and
   KEV membership with a remediation clock as F18/S052; no new capture for either is claimed here.
6. **`verified-at: 2026-10-26`** is the authoring date and pin-check date, not the capture instant.

## 7. Out-of-scope observations (for the L1; this seat changed nothing)

- **S054 id history.** Rounds 24-35 lessons use `S054` as a *staged/quarantine* id for a 内閣府 vulnerability-information
  request PDF (`payload-absent`), and the registry never admitted it: `grep -c '^| S054 ' corpus/SOURCES.md` → `0` and
  `grep -c '府連' corpus/SOURCES.md` → `0`. The r37 erratum assigns `S054` to SSVC. The append is a new registry row,
  not a `supersedes S###` correction; worth stating in the row note so a reader does not read the lessons' `S054` rows
  as that row.
- **Expected-list insertion point.** The entry path sorts C-locale between `corpus/knowledge/source-tree-loss-2026-09-28.md`
  and `corpus/knowledge/statutory-authorization-and-unauthorized-access.md` (verified: the appended path sorts there;
  `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` → clean). After landing, expected entries 48 → 49.
- **Home-page body.** The control capture's only prose is the definition on L202-L205 ("SSVC stands for A
  Stakeholder-Specific Vulnerability Categorization." / "It is a methodology for prioritizing vulnerabilities based on
  the needs of the stakeholders involved in the vulnerability management process."). The overview page is the right
  pin for a substantive entry.

## 8. Scope, tooling, cleanup

- Writes: this receipt only (`.ufo/waves/round-37/wave1/ScribeEntryF20.md`); scratch under
  `/fast/scratch/hyaku/kasegi-r37/ScribeEntryF20/` (`S054-overview.txt`, `S054.txt`, staged `manifest.json`,
  `entry.md`, control dirs), removed before yield.
- Tooling: none installed or upgraded (python3 stdlib + the lane's committed `capture-source.py`,
  `source-recheck.py`). No pacman; no mutating git.
- Read-only git used: `rev-parse`, `status --porcelain`; file facts from `grep`/`ls`/`wc` over the working tree.
- Q6: no credential, session, private URL or vault reference appears in the entry or this receipt; nothing here
  authorizes probing, scanning, login or submission against any target.
