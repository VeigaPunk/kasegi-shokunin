# ConnSibling — sibling-lane adjacency scan for the F09 adoption

Seat: connector (read-only). Item: does any sibling lane already own statutory-authorisation,
jurisdiction case law or rules-of-engagement ground; and are there duplicate SOURCES rows across
lanes. Base `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`; lane tip read at `c2480b143120364728b40397926ffcf30a7309c8`.
No production file, lane tree, git/jj state, fleet repo or `/home/vgpnk/Projects/shokuknow` byte was
written. No tools installed or upgraded.

## Findings

### F1 — No sibling claims statutory-authorisation, jurisdiction case law, or rules-of-engagement ground

Each of the three requested provinces was read in full, and each refuses the ground explicitly or is
silent on it:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md:10` — "**Refuses:** bounty-program scope
  and claim packages (→ kasegi)". The nearest thing chousa owns is `:5-8` "question framing; source
  hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution;
  claim-vs-source verification; search-strategy taxonomy; the external-target approval table for a
  research window" — method and *fleet-internal* permission, never substantive law.
- `/home/vgpnk/Projects/shokunin/tabi-shokunin/PROVINCE.md:15` — "**Refuses:** reverse engineering as
  forensics (→ revenger/kaidoku), web *publishing* (→ kake), secrets (→ kagi…)". Nothing on law;
  `:6-14` owns the browser substrate and "interaction records: site-specific gotchas, rate/rights
  discipline, login-session handling rules".
- `/home/vgpnk/Projects/shokunin/kotodama-shokunin/PROVINCE.md:12-14` — "The verification and
  civilization partitions support linguistic-cultural coupling; they do not expand ownership into
  general research method, fleet protocol, historical truth certification or lore's canon"; `:17-18`
  refuses only "real-world rights/attribution rulings on reference works".

Corroboration across every lane, not just the three: a fleet-wide scan for the three candidate source
URLs and their host paths returns **zero** hits in any lane's `corpus/SOURCES.md` (the only
`laws.e-gov.go.jp` occurrences outside kasegi are two kotodama *lesson* JSONs, see F4). Command and
output shape: `grep -rnoE 'https://(laws\.e-gov\.go\.jp|www\.soumu\.go\.jp|www\.npa\.go\.jp|nvlpubs\.nist\.gov|www\.court\.gov\.cn)[^ |)]*' --include='*.md' . | grep -v kasegi-shokunin`
→ only revenger's FIPS 180-4 (different NIST document), mori's SP 800-122, kengaku's AI 800-3 /
TN 2045 — none is the adopted material.

**Verdict:** kasegi absorbs the F09 ground; nothing in it is report-only for ownership reasons.

### F2 — The reciprocal evidence is stronger than the refusals: chousa's own gate routes this ground *to* kasegi

`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/scope-refusal-r12.md:21` is a live
routing table in chousa's research gate:

> `| `bug bounty`, `bounty program(s)`, `bounty hunt(ing)`, `bounty scope`, `claim package(s)`, `kasegi` | `SCOPE_BOUNTY_ABSORBED` | kasegi |`

and `:41` — "The screen reports, never absorbs: a refused declaration is a warn finding that drifts
the record (exit 1), and the record's author routes the work to the owning province (kasegi /
kengaku / kumitate)". So a chousa record that declared programme authorisation scope would be
*warned against itself* and sent to kasegi. That is machine-readable confirmation of the adjacency
direction, and it is the strongest artifact either lane holds on this question.

### F3 — Two real adjacencies exist, but neither is statutory: they bound how F09 may be written

These are the "report, never absorb" items, stated as discriminators rather than as ownership claims:

1. **chousa owns fleet permission to research** — `chousa .../PROVINCE.md:7-8` "the external-target
   approval table for a research window" and `:5-6` the method half. If an F09 entry drifts from
   *what a published instrument authorises a tester to do* into *how this lane decides whether it may
   open a source*, that sentence is chousa's and must be reported, not absorbed. Keep the F09
   subject as the external instrument (NIST ROE; the Japanese statute and its access-manager
   carve-out; a programme's scope list), never as lane-level approval.
2. **tabi owns the fleet-internal interaction-approval taxonomy** —
   `/home/vgpnk/Projects/shokunin/tabi-shokunin/corpus/README.md:19`
   (`knowledge/interaction-approval-table.md`, "every interaction class → autonomous-now /
   operator-asleep-blocked / operator-approval-required … judged on rights · rate · consequence"),
   with `tabi .../PROVINCE.md:10-11` ("rate/rights discipline"). The ROE entry must not restate or
   re-derive that taxonomy; ROE as a *published client-engagement instrument* is kasegi's, tabi's
   table is tabi's. Any cross-reference should be a one-way pointer, not a merged table.
3. **kotodama hands off entirely** — no report needed (F1, `PROVINCE.md:12-14`).

### F4 — The one sibling artifact that touches Japanese statutory text is a retrieval prior, not authority — and its measured limit does not hold for the adopted law

`/home/vgpnk/Projects/shokunin/kotodama-shokunin/corpus/lessons/supplement-opencode-1/sources/color.json:95`
(a lesson retrieval ledger, id `COL-06` at `:70`, not a SOURCES row) records for a *different*
statute (道路交通法施行令, 昭和35年勅令第270号): "e-Gov law-data extraction truncates at Article 1;
document UI needs JavaScript; legacy law.e-gov.go.jp DNS-fails; laws.e-gov.go.jp v2 law_data
endpoint HTTP 404".

Measured this round against the adopted law (public document read with `curl`, allowed as reading):

```
curl -sS --max-time 45 -o /tmp/egov-411.xml -w 'http=%{http_code} bytes=%{size_download}\n' \
  'https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128'
→ http=200 bytes=36058
grep -c '第十一条' /tmp/egov-411.xml                       → 4
grep -o '三年以下の拘禁刑又は百万円以下の罰金' /tmp/egov-411.xml → match (present)
grep -o '三年以下の懲役' /tmp/egov-411.xml                 → no match
```

So the v1 lawdata API serves the full consolidated text of 不正アクセス行為の禁止等に関する法律,
including the penalty article the package entry quotes, and the entry's own divergence claim (MIC
page still reads 懲役, e-Gov reads 拘禁刑) is reproducible at the byte level. kotodama's truncation
limit is document-specific, not an e-Gov-wide property — do not import it as a blocker, and do not
import the ledger row as a source row.

### F5 — Duplicate SOURCES rows: none for the adopted material; the hazard is a *new* third in-lane pair

- Fleet-wide: 21 lane registries (`*/corpus/SOURCES.md`, row counts 31 kasegi … 783 kotodama; command
  `grep -cE '^\| S[0-9]{3} ' */corpus/SOURCES.md`). Across them there are **58 distinct URLs held by
  two or more lanes** (python set intersection over extracted `https?://` tokens), all developer /
  OS / tool documentation pairs (`docs.python.org/3/library/json.html` in 7 lanes, `git-scm.com/docs/*`,
  `docs.jj-vcs.dev/*`, `raw.githubusercontent.com/torvalds/linux/v7.2/*`…). **Zero** of kasegi's 31
  row URLs appears in any other lane's registry (per-URL `grep -qF` loop over every other
  `*/corpus/SOURCES.md` → no `DUP` line).
- In-lane: the registry already carries **two deliberate same-URL pairs**, both declared:
  `.ufo/waves/round-24/assimilation/census-before.txt:1-2` prints
  `S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes`
  and `S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes`; their rationale
  is QUALITY R8 (a corrected scope is a new "supersedes S###" row). Line 3 of that file is
  `kasegi ok` for the registry itself.
- Consequence for this round: the four adopted rows must each carry a URL *not already in kasegi's
  registry* and not already in a sibling registry. The only near-miss is the e-Gov **host**, which
  kotodama holds in a lesson ledger for a different statute (F4) — registering 道路交通法施行令 would
  be a new kind of duplicate; registering 411AC0000000128 is not.
- Cross-lane *id* collisions are not defects (ids are lane-local) but are a routing hazard worth one
  line in any report that quotes two lanes: kasegi S031 (CNA 4.2.6) is simultaneously chousa S031,
  tabi S031, kotodama S031. Quote registry ids with the lane name.

### F6 — Contradiction to state, not smooth: the frozen C2 counter cannot be met with the package's own ids, and its enabling artifact does not exist

1. `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json:44` defines counter B as
   `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l` (target 2). The package's own
   source lines are `S039`, `S040`, `S041`
   (`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/statutory-authorization-in-three-traditions.md:4-6`)
   and `S123` (`…/authorised-testing-rules-of-engagement.md:2`). Keeping the package ids gives **1**
   matching file (the ROE entry, via S123), not 2 — the Japanese entry would score 0. The frozen
   counter therefore forces the Japanese rows into the `S1xx` band; it is not a free choice.
2. `claims.json:38` conditions the predicate on "rows first registered this round under **addendum
   10**", and `claims.json:54` names the collision map
   `.ufo/waves/round-24/assimilation/renumber-map.tsv`. That file **does not exist**
   (`read` → not found; the directory holds only `census-before.txt`, `collisions`, `reg-ids`,
   `staged-ids`). `grep -rn 'addendum 10' /home/vgpnk/Projects/shokunin` matches **only**
   `claims.json`; the fleet has no "addendum" convention in `PROTOCOL.md`/`CORPUS.md`/`QUALITY.md`.
   `assimilation/collisions` contains exactly `S031` — the package's first staged id — and
   `staged-ids` runs S031–S124, i.e. 94 ids overlapping the live registry at S031.
3. Consequently, as the round stands, C2's counter is reproducible but the numbering it demands is
   undefined, and the map the claim says it reads is absent. This is a claim-side gap for L1 to close
   with an artifact, not a reason to bend the counter.

### F7 — Both candidate entries fail the lane's executable-recheck criterion as filed, and F09 sits outside C1's frozen counter

- Package `recheck:` lines are non-executable: `authorised-testing-rules-of-engagement.md:4`
  "90d — re-fetch the PDF and `grep -F` the four lines (ran 2026-10-24)" (`bash -c` → `90d: command
  not found`), and `statutory-authorization-in-three-traditions.md:8` `curl … then confirm …` (a live
  fetch, and the word `then` lands as a curl argument). That is the Q7/M2 class the lane already
  mined (`corpus/QUALITY.md` Q7; `corpus/lessons/round-23.md` M2).
- C1 counter A (`claims.json` counter_A) iterates **eight hard-coded file names**. Once F09 exists,
  two admitted entries carry rechecks that no frozen counter exercises — an asymmetry against
  `depth:verifiability` unless a separate receipt covers them.
- Baseline for the instrument: `python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-23/manifest.json` → 36 lines, exit 0; it lists only
  `S018, S029, S030, S031`, which is exactly why F01–F05 exit 2. `corpus/source-snapshots/round-24/`
  already holds `S001`–`S015` and copies of those four, but **no manifest and no S1xx capture** yet.

## Proposed move (one, bounded)

**Make the adopted block an explicit, declared id band driven by captures, so the frozen counters can
see it and the verifiability axis is earned rather than asserted.**

1. Before any entry lands, write the missing `.ufo/waves/round-24/assimilation/renumber-map.tsv`
   (named by `claims.json:54`) with four rows mapping package ids to a declared reserved band:
   `S039→S100` (e-Gov 411AC0000000128), `S040→S101` (MIC citizen page), `S041→S102` (NPA commentary),
   `S123→S103` (NIST SP 800-115). Declare in `corpus/SOURCES.md`'s header that `S100–S199` is the
   adopted-block band and `S032–S099` is reserved for the unadopted package rows — this is the
   "addendum 10" the claim names, given a byte artifact and a reason the S1xx counter shape works.
2. Capture each row with the lane's own instrument, `corpus/instruments/capture-source.py --id S10x
   --url … --out corpus/source-snapshots/round-24/S10x.txt`, and add the four records to
   `corpus/source-snapshots/round-24/manifest.json` (its own copies — `source-recheck.py:105-111`
   rejects `../round-23/...` cross-directory reuse).
3. Rewrite both entries' `recheck:` to the per-source selection, in the F06–F08 form:
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py
   --manifest corpus/source-snapshots/round-24/manifest.json --source S10x`, so the same string works
   from the repo root (where every counter runs) and from anywhere else.
4. Since C1's counter list is frozen at eight, add a separate round-24 receipt that runs both F09
   entries' recheck lines verbatim and shows exit 0, plus the negative control below — the claim is
   not edited, the evidence is added.

### Why this is the non-obvious move and not just bookkeeping

- The `S1xx` assignment is *forced* by `claims.json:44` against the package's `S039`/`S040`/`S041`
  (F6.1); doing it without the reserved-band note re-collides on the next merge (the package's
  S031–S124 block already collides at S031, `assimilation/collisions`).
- The e-Gov capture is *known obtainable* at quote granularity (F4 probe: 200, 36,058 B, 4×第十一条,
  拘禁刑 present), so the depth:verifiability half is reachable rather than aspirational — and the
  sibling's recorded truncation limit must not be inherited as a reason to skip it.
- Ids are read by nothing but `source-recheck.py`'s `ID_RE` and `capture-source.py --id` (grep of
  `corpus/instruments/*.py` finds no S0xx range or contiguity logic), so a banded assignment with a
  gap harms no existing detector.

### Affected axes

- `coverage` — makes C2 counter B reachable at its declared target 2 and supplies the collision map
  the predicate already assumes; F09 becomes admissible in the lane's own numbering.
- `depth:verifiability` — two new entries get captured-source rechecks that a committed manifest
  actually answers, closing the F7 asymmetry without touching C1's frozen counter.
- No harm: C1 counter A's eight files are untouched; no sibling loses ground (F1–F3); no existing
  registry row is renumbered (R8), only appended.

### Risks

- A banded registry with a gap (`S032–S099` empty) departs from the present contiguous practice; the
  header note is the mitigation, and no instrument enforces contiguity.
- The one-entry-per-file requirement of counter B means each entry needs at least one `S1xx` line; the
  Japanese entry's three rows all land in the band, so this holds, but do not leave the primary as
  `S039` "for fidelity" — that is exactly the shape that scores 1.
- The round-24 manifest must be id-clean **globally**: `source-recheck.py` validates every record id
  before the `--source` filter (`:153` vs `:157`), so one duplicate id zeroes all four rechecks.
- If MIC or NPA cannot be re-opened with a located quote this round, refuse that row with reason and
  flip condition (QUALITY Q2/Q3) — do not pad the manifest to keep S101/S102 occupied; a band gap is
  legal, a fabricated quote is not.
- F09 entries must keep their subject external (F3), or the chousa/tabi adjacency becomes a real
  absorption and the report-out obligation is skipped.

### Verification (L1 runs once, after the wave)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
test -e .ufo/waves/round-24/assimilation/renumber-map.tsv
grep -c '^source: S10[0-3] ' corpus/knowledge/statutory-authorization-in-three-traditions.md \
                            corpus/knowledge/authorised-testing-rules-of-engagement.md   # ≥1 and ≥1
grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l                          # 2  (C2 counter B)
for s in S100 S101 S102 S103; do python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-24/manifest.json --source $s; done            # each exit 0
bash -c "$(grep -m1 '^recheck: ' corpus/knowledge/<f09-entry>.md | sed 's/^recheck: //')" # exit 0, BOTH entries
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json \
  --source S104                                                                          # exit 2 not-listed (control)
```

Negative control on the capture itself: flip one byte in an `S10x.txt` → the recheck for that source
must exit 1 (`:sha256 MISMATCH`), proving the receipt reads bytes rather than a hard-coded exit 0.

## UNVERIFIED

- **UNVERIFIED:** whether the MIC citizen page (S040) and the NPA commentary PDF (S041) still serve
  the quoted clauses; I did not fetch them (only the e-Gov API was read, as the one probe that decides
  whether the statutory capture is obtainable at all).
- **UNVERIFIED:** whether any *unwritten* fleet convention ("addendum 10") exists outside the repo
  tree; `grep -rn 'addendum 10' /home/vgpnk/Projects/shokunin` matches only `claims.json:38`.
- **UNVERIFIED:** sibling lanes' *uncommitted* work — only committed files were read; a sibling could
  be drafting authorisation material right now without a registry row.
