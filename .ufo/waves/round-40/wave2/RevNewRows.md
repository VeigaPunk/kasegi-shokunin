# RevNewRows — wave-2 falsify receipt (round 40, FALSIFY wave 2)

- Seat: RevNewRows (leaf member, no subagent dispatch). Run UTC: 2026-10-26T22:10Z–22:25Z.
- Item attacked: the new S060+ registry rows promised by frozen claim C2 — "new registry rows S060+ opened this round, with at least one mined knowledge entry citing an S060+ row" — verified at the verification ref Y = lane tip `3074c7679d6f527ec3930d7748ccce1dbae4a58a` over committed bytes (`git archive 3074c76…` extracted to scratch; every count below ran on that export, not the working tree).
- Method: re-ran each counting command from claims.json against the Y export; re-fetched every URL the three rows rest on (UA `kasegi-shokunin/1.0`, `curl -sS -L --max-time 90`); re-derived the S060 capture with the lane's own `capture-source.py` normalization; re-ran `source-recheck.py`; mutation-tested the recheck gate on scratch copies.

## Counts delivered (all at Y)

| check | command | result | verdict |
|---|---|---|---|
| S060+ rows exist | `grep -cE '^\|[[:space:]]*S06[0-9][[:space:]]*\|' corpus/SOURCES.md` | **3** (S060 L66, S061 L67, S062 L68) | reproduced (≥1) |
| row shape | `awk -F'|'` over all registry rows | **all 62 rows NF=13** (11 cells + 2 empty ends); no `\|` inside any cell | reproduced |
| statuses valid | distinct `$9` across table | vocabulary = {mined: 52, rejected: 10}; S060=mined, S061=rejected, S062=rejected | reproduced |
| opened today | `$10` of the three rows | all `2026-10-26` (= today; live clock 2026-10-26T22:10Z) | reproduced |
| entry citing S060+ | `grep -rlE '^source: S06[0-9]' corpus/knowledge \| wc -l` | **1** — `corpus/knowledge/cyclonedx-analysis-subtree.md`, `source: S060` only; no entry cites S061/S062 anywhere | reproduced (≥1; exactly one citing entry for the mined row) |
| source-recheck | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S060` | `S060:sha256 OK`, `Q1/Q2/Q3 OK occurrences=1 anchor=7/15/50-ok`, **exit=0** | reproduced |
| id collision | duplicate-id grep over the table + census | **no duplicates**; registry 59 (base) → 62 (Y); 0 S060+ rows at base `a7af2ce6…` | reproduced |
| census | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **exit 0**; `W04 S028`, `W04 S029` only — identical to `census-before.txt` | reproduced |
| frontier harness | `python3 corpus/instruments/frontier-recheck-count.py` | **entries=26 pass=26 exit=0**, incl. `PASS F23 knowledge/cyclonedx-analysis-subtree.md ids=S060` | reproduced |
| frontier rows | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | **23** (F23 row at README L534, path + ids=S060 match the entry) | reproduced |

## Live re-open of each new row (fetch ledger, this seat)

All fetches `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, UTC 2026-10-26T22:10:20Z–22:10:22Z.

| URL | wave-1 record | this re-fetch | verdict |
|---|---|---|---|
| cyclonedx.org/docs/1.7/json/ (S060) | HTTP 200, 6,419,901 B; raw sha varies (Cloudflare tokens, disclosed in manifest) | HTTP 200, **6,419,901 B**, raw sha `ba6e8881…` (differs as disclosed) | reproduced: normalized full text sha **`ffe8c0b6…f4` EXACT**; slice L1+L16060–L16169 re-derived with `capture-source.py html_to_text()` is **byte-identical** (`cmp` clean) to committed `S060.txt` sha `d6862622…79`, 4,889 B, 111 lines |
| cisa.gov/news-events/news/vex-status-justifications (S061 lead) | 404, 46,957 B, `ec8e69c7…` | 404, 46,957 B, `ec8e69c7…` | **EXACT** |
| cisa.gov/resources-tools/…/vex-…-june-2022 (S061 page) | 200, 56,383 B, `2cb3a40b…` | 200, 56,383 B, `2cb3a40b…` | **EXACT**; "Publish Date" + "June 01, 2022" + archive notice present |
| cisa.gov/…/VEX_Status_Justification_Jun22.pdf (S061) | 200, 313,386 B, `9a4027c6…`; pdftotext -layout `2b480ac8…` | 200, 313,386 B, `9a4027c6…`; pdftotext -layout sha **`2b480ac8…` EXACT** | **EXACT**; L46–47 quote verbatim |
| docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html (S062) | 200, 1,231,332 B, `fdb4bf01…` | 200, 1,231,332 B, `fdb4bf01…` | **EXACT (byte-identical)** |
| …/v2.1/ directory listing (S062) | 200, 1,097 B, `5e59949c…` | 200, 1,097 B, `5e59949c…` | **EXACT**; csd01–csd04 + schema, no `os/` |
| …/csaf/ parent listing (S062) | 200, 392 B, `64a94196…` | 200, 392 B, `64a94196…` | **EXACT**; v2.0/ and v2.1/ only |
| …/v2.1/os/ and …/os/csaf-v2.1-os.html (S062 probes) | 404, 41,334 B, `e416b400…` | 404, 41,334 B, `e416b400…` | **EXACT** — flip monitor has not fired |

## Entry-level verification (cyclonedx-analysis-subtree.md, 322 lines)

- All **12 anchored blockquote spans** verbatim on their declared capture lines, each exactly once, longest 21 words (L44) — FC-1 reproduced by independent recount.
- Table-cell quotes: 6 state descriptions (L10–L15) + 3 version-status descriptions (L109–L111) + `Default: "affected"` type line (L105) all on-line.
- FC-2 reproduced: `VEX CSAF CVSS severity score product_status known_affected known_not_affected under_investigation` + all five CSAF label names = **0 occurrences each** in the capture; `SHALL`=0, `MUST`=0, `should`=2 (L15, L44).
- FC-3 reproduced: `Must be one of:` blocks at L8/L19/L35/L107 count **6 / 9 / 5 / 3** (states, justifications, responses, version statuses) — matches the row's "six analysis states, nine not-affected justifications" and the entry's counts.
- Cross-references spot-checked in the pinned captures: S055.txt L2151–2152 ("impact statement SHALL exist as machine readable flag"), L2844 (four mandatory categories), L1855 (product_status) all present as cited.
- Header convention (`source:` / `verified-at:` / `ground: F23` / `recheck:`) matches sibling entries (e.g. S055 entry).
- Lesson Gate: S061 and S062 rejection **reason + flip** logged in `corpus/lessons/round-40.md` (Rejected block, L140–L150); S060 admission block present.

## Mutation test of the recheck gate (scratch copies only; lane untouched)

| mutation | expected | observed |
|---|---|---|
| baseline | exit 0 | exit 0 |
| corrupt 1 byte of S060.txt | fail | `sha256 MISMATCH expected=d68626… actual=14c9b9…`, **exit 1** |
| capture removed | fail | `S060:source UNAVAILABLE reason=missing`, **exit 2** |
| manifest Q1 quote tampered | fail | `Q1 MISMATCH reason=quote-not-found`, **exit 1** |

The gate fails closed in all three directions — not a rubber stamp.

## Defects found

No kill-class defect: no malformed row (all NF=13), no id collision, no unbound mined row, census exit 0, statuses valid, opened-today holds, the single mined S060+ row is bound to exactly one entry whose recheck passes and whose capture reproduces byte-identically from a fresh live fetch.

Minor findings (recorded, none binding):

1. **S062 locator provenance gap (minor).** The row's anchor cell and `wave1/ScoutS060Leads.txt` cite located quotes at "csaf21.txt L498 / L7611" of a scout-derived "tag-stripped HTML" text (sha256 `626cac7f…473158`, recorded in `wave1/ScoutS060Leads.md`) that is **not committed** and whose exact pipeline is not specified. I could not reproduce that sha with ~15 plausible tag-strip/normalization pipelines; the closest structural match (tag-boundary split + strip + collapse) puts the two quotes at L497/L7610 — exactly one line short. The **quoted text itself is verified present verbatim** in the live page, whose raw sha256 is byte-identical to wave 1's fetch (`fdb4bf01…`), so the substantive rejection evidence stands; only the line locators depend on the uncommitted derived artifact. S062 is rejected and nothing binds to these locators.
2. **S061 second-quote locator tail (nit).** Ledger and row anchor say "L208-209 (section 3.7.3 distinction)"; the quoted sentence's last word "distinctions." falls on **L210** (L209 ends "…are similar, but with some key"). Quote text verified present; off-by-one on the locator tail only.
3. **Line-count bookkeeping (nit).** Ledger says the pdftotext text is "274 lines"; `wc -l` gives 273 because the final line ends `\f` without `\n` (274 by awk-NR counting). The sha256 is byte-identical, so no content issue.

## Verdict

**C2's S060+ row claims REPRODUCE at Y.** 3 new rows (S060 mined, S061/S062 rejected), all opened 2026-10-26, structurally uniform (NF=13, no embedded `|`), statuses within the table's {mined, rejected} vocabulary, no id collisions (59→62), census exit 0 with the before-state's W04 S028/S029 codes only, exactly one knowledge entry citing S060 whose source-recheck passes and whose capture is byte-reproducible from the live web today, harness 26/26 with PASS F23 ids=S060, frontier 23. The recheck gate is mutation-hardened. Three minor locator-provenance nits recorded above on the two rejected rows; none affects a binding or a count.
