# CritC2Claim — is the F20 / SSVC admission genuinely new ground? (round 37, C2 / coverage)

Seat `CritC2Claim` (leaf critic). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read-only except this
receipt and `/fast/scratch/hyaku/kasegi-r37/CritC2Claim/` (removed before yield). No lane, fleet, sibling-lane
or source-tree file was written; no mutating git command; no package or tool install.

Read for this review: frozen claims `224df74d…` (`.ufo/waves/round-37/claims.json`), `claims-erratum-1.md`
(`b3620681`), before-controls `.ufo/waves/round-37/c2-controls/before.txt`, and the six C2 artifacts already in
`wave1/` (`ScoutF20Open`, `ExecC2Capture`, `ExecC2QuoteOnce`, `ExecC2JunkControl`, `ExecC2Harness`,
`ScribeEntryF20`, `ScribeFrontierAmendments`, `ScribeRowS054`, `RevEntryF20`). `ScoutF20Sibling` has no receipt
yet (state, not a defect of this claim).

## 0. Verdict

**ADMIT F20 as a distinct coverage surface; narrow the novelty sentence and scope the sweep. One correction,
four conditions, no kill.**

I could not construct a counterexample that makes F20 a duplicate of an existing frontier entry. What I did find:

1. **The corpus already holds SSVC references**, including one tier-A *prose* sentence that states SSVC's role
   (§2). That does not duplicate the mechanism, but it falsifies any "SSVC appears nowhere in this lane" wording.
2. **The nearest neighbour is F14, not F18/F19** (§3): the corpus already holds an inputs→categorical-posture
   matrix (CVSS band × impact scope → 簡易/通常/優先). The entry's overlap paragraph names KEV, EPSS and CVSS and
   silently omits F14.
3. **The counters cannot witness novelty** (§5, measured): a one-quote thin entry and a chimera whose body is the
   *EPSS* entry with genuine SSVC manifest quotes both reach the exact frozen after-state
   (`entries=23 pass=23 exit=0`, `audit expected=49`, `binding records=44`). Only a naive copy whose *quotes*
   were also copied is caught. So "new ground" rests on the entry's claims and a real sweep — never on
   `entries=23 pass=23`.
4. **The pinned page is the right page for the claims the entry makes**, and the draft stays inside it (§4), with
   one measured trap: this capture's outcome labels are `Defer / Scheduled / Out-of-cycle / Immediate`, *not* the
   canonical SSVC `Track / Track* / Attend / Act`, and BOD 26-04 is navigation only.

Impacted axes: **coverage (C2) only**. Depth axes untouched; C1 literals untouched.

## 1. Pin identity — independent reproduction

Fetched once with the lane's own instrument, so the normalization is the manifest's:

```
$ python3 corpus/instruments/capture-source.py --id S054 \
    --url https://certcc.github.io/SSVC/tutorials/ssvc_overview/ --out "$S/S054-inst.txt"
S054 status=200 fetched_bytes=143053 snapshot_bytes=32623 sha256=ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21 utc=2026-10-26T17:10:46Z
$ wc -l -c S054-inst.txt  ->  518 32623
```

That digest/byte-count/line-count equals what `ExecC2QuoteOnce` (17:02:11Z), `ExecC2JunkControl` (17:02:19Z),
`ScribeEntryF20` (17:05:59Z) and `ScoutF20Open` (17:12:36Z) recorded, so the capture is reproducible across
five independent fetches rather than one seat's snapshot. The home-page control (`a6613315…`, 286 lines,
§2 of `ExecC2QuoteOnce`) I did not re-fetch; I used the peer measurement only.

## 2. Negative sweep — what is actually new, and what the corpus already held

Command (base `b3620681`, the claims-erratum head; the only delta from `b56a4168` is the erratum file):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for t in SSVC Stakeholder-Specific "Stakeholder Specific" "decision tree" "decision point" \
         Deployer Automatable "Mission Prevalence" "Public Safety Impact" Carnegie; do
  printf '%s knowledge=%s README=%s SOURCES=%s SKILL=%s PROVINCE=%s\n' "$t" \
    "$(grep -rilF -- "$t" corpus/knowledge | wc -l)" "$(grep -icF -- "$t" corpus/README.md)" \
    "$(grep -icF -- "$t" corpus/SOURCES.md)" "$(grep -icF -- "$t" SKILL.md)" \
    "$(grep -icF -- "$t" PROVINCE.md)"
done
```

Observed: **every one of those eleven terms is 0 in `corpus/knowledge` (48 files), `corpus/README.md`,
`corpus/SOURCES.md`, `SKILL.md` and `PROVINCE.md`.** `stakeholder` is 1 file — `multiparty-vulnerability-coordination.md:29`
("Minimize exposure for stakeholders"), a FIRST table cell, not SSVC ground.

But the sweep scoped that way is **not** a whole-corpus statement, and this is where it must be corrected:

| surface | occurrences | what it is |
|---|---|---|
| `corpus/source-snapshots/round-24/S003.txt` L238-L240 | 1 | **prose, tier-A, entry-used**: "Suppliers should leverage risk assessment and decision support systems such as Stakeholder-Specific Vulnerability Categorization (SSVC) to help prioritize reports." |
| `corpus/source-snapshots/round-24/S003.txt` L252 | 1 | footnote 10: "CISA uses SSVC to help prioritize the remediation of vulnerabilities in FCEB agencies." |
| `corpus/source-snapshots/round-24/S004.txt` L9, L21 | 2 | site navigation ("SSVC" link on CERT/CC's VDP site) |
| `corpus/source-snapshots/round-24/S008.txt` L174 | 1 | "Related Resources" link, not prose |
| `LOG.md:1669` | 2 | round-36 entry: "nearest neighbour is a retained kagi NVD/SSVC probe — the SSVC *Exploitation* decision point, a different framework; reported, not absorbed" |
| `corpus/lessons/` | 0 | — |

`S003` is registry row tier A, status mined, `used-by corpus/knowledge/coordinated-disclosure-timelines.md`
(F02). So the corpus has held a **tier-A sentence naming SSVC and its role since round 24**, and a sibling lane
(kagi) already holds an SSVC probe per `LOG.md:1669`. The honest novelty statement is therefore
*mechanism-level*: **no entry holds SSVC's decision points, stakeholder roles, or priority categories** — which
is true and is what F20 actually adds. "SSVC is absent from the corpus" is false.

This is exactly the failure mode `corpus/SOURCES.md:115` records for round 35 ("the zero-hits claim is not a
whole-corpus statement (R8)").

## 3. Overlap — F18, F19, and the neighbour the entry misses (F14)

**F19 (EPSS).** S054 *consumes* EPSS: navigation rows "EPSS Probability as input to Exploitation" (L93) and
"EPSS Percentiles as an Amplifier" (L94) — both occurrences = 1 and outside body prose. F19's artifact is a 0–1
probability at FIRST; S054 emits no probability (`probability` 1, `percentile` 1, both the nav rows; `score` 0).
Distinct output form. ✔

**F18 (KEV).** "In KEV" occurs once, at L153, under the navigation group "CISA-based decision points"
(L150-L152). The KEV capture (S052) carries no severity and no SSVC vocabulary (`automatability` 0,
`public exposure` 0 in S052.txt). Distinct: S054 emits a priority category, S052 emits membership plus a
remediation clock. ✔

**But the sharpest F18 contact is one page away.** The CISA BOD 26-04 *response model* — whose four binary
decision points are InKEV / Publicly Exposed / Automatable / Technical Impact and whose outcomes are FSU / 60D /
14D / 3D — lives on `howto/cisa_response/`, **not** on the pinned page (`ScoutF20Open` §3(e), measured again
here: `BOD` 1 hit on the pin, L68, nav label only). F18's README `next` cell already states that four-factor
model ("public exposure, KEV status, automatability, technical impact", `corpus/README.md:388`). So:
**if any F20 artifact imports the CISA response model from S054, F20 collides with F18's ground and the
distinctness clause becomes false.** The drafted entry and row do not (§4) — this is a boundary to keep, not a
defect found.

**F14 — the overlap the draft does not name.** `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`
already holds an inputs→categorical-posture scheme: S041's three-by-three response matrix (`簡易な対応 /
通常の対応 / 優先対応`) driven by CVSS v3 band × impact scope (`S041.txt:1465-1490`). Structurally that is
"score plus context in, action posture out" — adjacent to SSVC's "decision points in, priority category out".
What remains distinct is real and checkable: **role-partitioned models** (Supplier / Deployer / Coordinator,
S054 L251-L257), a **per-system input** ("determined on a per-system basis", L367), and categories the page
offers as examples (L261). The entry's "Sources overlap" section compares KEV/EPSS/CVSS only; adding F14 is one
sentence, and without it the closest existing scheme is unmentioned.

## 4. Source choice (tier A) and entry scope against the pinned bytes

**Tier A is right.** `certcc.github.io` is the project's own documentation host, the corpus already carries
CERT/CC's site at tier A (S004), and the overview page speaks as the institution ("the CERT/CC", 14 occurrences;
"we"/"our" throughout; L268, L448). Attribution limits, all verified: `Carnegie` = 3 hits, footer copyright only
(L503-L507) — the body makes no authorship statement; `CVSS` 6, `EPSS` 5, `KEV` 1 are **navigation only**
(L69-L71, L156-L159 / L90-L94 / L153) and the page defines none of them. So Q2 for severity/likelihood/catalog
claims must route to S001/S002, S052, S053 — the drafted row and entry do exactly that.
One provenance gap worth recording in the row/entry, not a defect: **the page shows no publication or revision
date**; the only date evidence is the HTTP `last-modified` (peer-measured 2026-10-23), which is a server header,
not a content date. The row's `opened 2026-10-26` is the access date, and that is the honest cell.

**Scope check against the bytes (my own verification, `source-recheck.py`'s `normalize()`).** I re-ran the
draft's load-bearing spans and 24 auxiliary spans: all unique (occurrences = 1) and anchor-window-true except
four short structural pointers cited by line/range rather than quoted (`Exploitation` 13 files-wide token,
`Utility` 13, `Human Impact` 8, `CVSS v4 Analyst Models` 2 — every one of those is cited as a heading pointer,
not as a manifest quote). Spot-checked verbatim and correct: L247 (contrast, 22 words), L247 ("SSVC rates
vulnerabilities on risk to the concerned stakeholder.", 9), L244 (risk continuum), L473 (restatement), L259
(priority varies), L261 ("as examples"), L262-L265 (the four categories), L266 (Defer ≠ ignore), L255/L257
(roles are a starting set), L277 (decision-point series, 25 words, page typo `decisions point values`), L281
(Exploitation definition), L367 (Exposure, per-system), L467 (publication row), L462 (CERT/CC's own practice),
L93/L94/L153 (input nav), L249 (`define to define`), L251 (`remidiation`), L6/L17 (`CERTCC/SSVC`).

**The trap this guard closes.** Word-boundary counts on the pin: `Track` 1 (the Coordinators' "Track information
about the reported vulnerability", L271), `Track*` **0**, `Attend` **0**, `Defer` 3, `Act` 5, `outcome` 0.
The canonical SSVC outcome set `Track / Track* / Attend / Act` is **not in this capture**; this page's outcome
vocabulary is `Defer / Scheduled / Out-of-cycle / Immediate` plus the Coordinator triage/publication tables.
The draft uses the page's own labels and therefore stays in scope. A later revision that "corrects" to the
canonical names from outside the capture would be out of scope and would fail its own recheck on any pinned
quote.

## 5. Would a do-nothing control reach the counters? — measured, yes (with one exception)

I built four fixture lanes from `git archive HEAD` (`b3620681`), each carrying a complete, plausible round-37
after-state (F20 row, S054 row with one `https://` token, `corpus/source-snapshots/round-37/` capture +
manifest, expected-list line), and ran the four instruments in each. Fixtures are scratch-only; the lane was
never written.

| variant | entry body | manifest quotes | frontier | source-recheck | audit | binding |
|---|---|---|---|---|---|---|
| **copy** — verbatim EPSS entry, only `source:`/`ground:`/`recheck:` swapped | EPSS claims | EPSS quotes | `FAIL F20 … problems=recheck-exit-1`, `entries=23 pass=22 exit=1` | 4× `MISMATCH reason=quote-not-found`, exit 1 | 49/49 exit 0 | 44/44 |
| **chimera** — same copied EPSS body | EPSS claims | **genuine SSVC sentences** | **`entries=23 pass=23 exit=0`** | 4× `OK occurrences=1`, exit 0 | **`expected=49 … exit=0`** | **44/44** |
| **thin** — one page sentence, no mechanism | 1 quote (L259) | that quote | **`entries=23 pass=23 exit=0`** | `OK occurrences=1`, exit 0 | **49/49 exit 0** | **44/44** |
| **dup** — F20 row re-pointed at the F19 entry | (thin entry unused) | — | `DUPLICATE-ENTRY F19,F20 …`, `entries=23 pass=23 exit=1` | — | — | — |

Base reproduced first, so the deltas are the fixtures': `frontier rows 19`, `registry rows 53`,
`knowledge 48`, `entries=22 pass=22 exit=0`, `expected=48 missing=0 unexpected=0 exit=0`,
`records=43 bound=43 unbound=0` — identical to `c2-controls/before.txt`.

Reading:

- **A naive copy is caught** — but by the citation limb and the quote comparison, not by any novelty rule.
- **A copy whose *manifest* is genuine passes every counter.** No instrument reads the entry's blockquotes; the
  frontier harness executes the `recheck:` line (manifest↔capture) and never compares body prose to it
  (verified by `grep -n "blockquote" corpus/instruments/*.py`: the word appears only in the harness's docstring,
  about *attribution references*, not about comparing quotes).
- **A one-sentence entry passes every counter.** So `entries=23 pass=23 exit=0` is evidence that a new
  frontier row is bound to a capture whose manifest lists genuine sentences, and nothing more. The frozen C2
  kill rule cannot distinguish this round's admitted entry from a do-nothing; the discrimination is the
  reviewers' Q2/Q3/Q5 read plus the sweep above.
- Instrument nit, not a claim defect: `dup` prints `entries=23 pass=23 exit=1` — the summary counter reads clean
  while the run is red. Any record quoting `pass=23` must quote `exit=1` beside it (the kill rule already
  requires `exit=0`, so the claim is safe).

## 6. Literals and after-state sanity

- Before-state matches the frozen `before` array exactly (§5).
- The after-state is reachable with the real artifacts: the four pinned quotes (Q1-Q4) each occur once with
  verifying anchors against my independent capture, so `source-recheck S054` reaches exit 0; `entries=23
  pass=23 exit=0` requires only that the landed entry cite `S054` in prose (the harness's citation limb) —
  the drafted entry does, in its header, overlap section and scope paragraph.
- Erratum-1 ordering, noted for `RevClaimsFreeze` and not scored here: `claims.json` says
  `frozen_at_utc 2026-10-26T16:30:00Z`, the erratum text says "Filed 2026-10-26T14:04Z, before the
  kasegi-r37-build seats began scoring", and `git log` gives commit times `224df74 13:57:07-03:00` (freeze),
  `b362068 14:00:19-03:00` (erratum) — i.e. the erratum commit is ~3 minutes *after* the freeze commit and the
  frozen_at stamp reads ~2.5 h later than both. Whether that is a defective stamp or a clock conversion is not
  my item; the *substance* (home page cannot carry the entry's load-bearing claims) is independently confirmed
  by three seats and by my own fetch.

## 7. Smallest safe correction

**One correction, in the round-37 C2 evidence record (not the frozen claim, which stays intact):** the novelty
evidence must be a *scoped* sweep plus an explicit limit line, because the counters are form-only.

Required wording/logic:

1. State the sweep per surface — `corpus/knowledge` 0/48, `corpus/README.md` 0, `corpus/SOURCES.md` 0 rows,
   `SKILL.md` 0, `PROVINCE.md` 0 — **and name the pre-existing SSVC references it excludes**: S003 L238-L240 and
   L252 (tier-A prose, entry-used by F02), S004 L9/L21 (nav), S008 L174 (related-resource link), `LOG.md:1669`
   (kagi SSVC probe). Classify them as *references, not held mechanism*.
2. State the limit in R21's shape: "the counters bind row↔entry↔manifest↔capture; a one-quote entry and a
   copy-with-genuine-manifest both reach `entries=23 pass=23 exit=0` (measured, §5), so novelty rests on the
   entry's claims and this sweep, not on the passing counters."

Conditions on the artifacts (each already satisfied by the drafts — keep them):

3. The entry keeps its mechanism-scoped distinctness: inputs routed to S001/S002/S052/S053; output a
   stakeholder-specific priority category; **the CISA BOD 26-04 response model is not claimed from S054**
   (nav-only, L68; its content is a different URL and F18's ground).
4. The entry's categories stay `Defer / Scheduled / Out-of-cycle / Immediate` (page labels); no `Track/Track*/
   Attend/Act` import.
5. Add F14 to the overlap paragraph (§3), so the corpus's existing inputs→posture matrix is named as the nearest
   neighbour rather than omitted.
6. `Carnegie Mellon` stays footer-scoped (L503-L507), and severity/likelihood/catalog definitions are never
   sourced to S054.

This improves coverage without touching C1 or any counter literal; no other axis moves.

## 8. What I did not establish

- I did not re-measure the home-page control capture (peer digest `a6613315…`, 286 lines) — used as reported.
- I did not run the round-37 census or the C1 closure suite (other seats' items).
- `ScoutF20Sibling` has not landed; the sibling-lane SSVC question is therefore open, and `LOG.md:1669` is my
  only evidence that a sibling already holds an SSVC probe.
- My fixtures are a plausible reconstruction of the after-state, not the landed tree; they were adapted by
  rewriting each entry's `cd <lane>` prefix to the fixture root so `recheck-audit.py`'s cdroot limb is measured
  rather than short-circuited. That rewrite is fixture-only and does not change any limb's meaning.
- The `chimera` result proves a structural property of the instruments; it is not an accusation that any seat
  filed a chimera. The drafted entry's body and its manifest quotes agree.

## 9. Tooling, scratch, cleanup

- No install or upgrade (python3 3.14.8, curl, the lane's own instruments).
- Scratch: `/fast/scratch/hyaku/kasegi-r37/CritC2Claim/` (captures, four fixture lanes) — removed before yield.
- Writes: this receipt only. Lane, fleet, sibling lanes and source trees untouched.

Report: .ufo/waves/round-37/wave1/CritC2Claim.md
