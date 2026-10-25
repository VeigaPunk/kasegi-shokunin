# Entry ↔ manifest quote binding — falsify report

Seat: `L1Kasegi23.EntryQuoteBinding-2` (leaf, read-only). Scope: the three F06/F07/F08 knowledge
entries versus `corpus/source-snapshots/round-23/manifest.json`. Every number and string below was
reproduced from the working-tree bytes in this session; no L1 claim is reused as evidence, and no
other seat's report is treated as a measurement.

Artifacts read (absolute paths):

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/multiparty-vulnerability-coordination.md` (F06, 61 lines)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cna-assignment-and-vulnerability-rules.md` (F07, 66 lines)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/cra-manufacturer-reporting-duties.md` (F08, 87 lines)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/manifest.json` (3 sources, 19 assertions)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, `corpus/QUALITY.md`

## Counts: table rows vs manifest assertions

| Source | Entry | Evidence/quote table rows | Manifest assertions | Byte-identical | Markup-normalized | Entry-only | Manifest-only |
|---|---|---|---|---|---|---|---|
| S018 | F06 | 6 (L25–L30) | 6 | 6 | 0 | 0 | 0 |
| S030 | F07 | 7 (L25–L31) | 7 | 6 | 1 (L28) | 1 | 1 |
| S029 | F08 | 6 (L45–L50) | 6 | 6 | 0 | 0 | 0 |
| **Total** | | **19** | **19** | **18** | **1** | **1** | **1** |

Row-level binding (alignment by row order, confirmed by literal equality for the 18 identical rows):

| Source | Entry line | Manifest assertion id | Verdict |
|---|---|---|---|
| S018 | L25 | `coordinator-def` | IDENTICAL |
| S018 | L26 | `upstream-vendor-def` | IDENTICAL |
| S018 | L27 | `comms-prior-to-disclosure` | IDENTICAL |
| S018 | L28 | `finder-documentation` | IDENTICAL |
| S018 | L29 | `minimize-exposure` | IDENTICAL |
| S018 | L30 | `coordinator-lead` | IDENTICAL |
| S030 | L25 | `rule-3-1-1-scope-definition` | IDENTICAL |
| S030 | L26 | `rule-3-1-4-covered-products` | IDENTICAL |
| S030 | L27 | `rule-4-1-2-security-impact` | IDENTICAL |
| S030 | L28 | `rule-4-1-9-independently-fixable` | **NORMALIZED** |
| S030 | L29 | `rule-4-2-1-1-first-opportunity` | IDENTICAL |
| S030 | L30 | `rule-4-2-11-separate-ids` | IDENTICAL |
| S030 | L31 | `rule-4-2-12-uncertainty` | IDENTICAL |
| S029 | L45 | `art14-2a-early-warning` | IDENTICAL |
| S029 | L46 | `art14-2b-vulnerability-notification` | IDENTICAL |
| S029 | L47 | `art14-2c-final-report` | IDENTICAL |
| S029 | L48 | `art14-4c-incident-final-report` | IDENTICAL |
| S029 | L49 | `art71-article-14-start` | IDENTICAL |
| S029 | L50 | `art71-general-application` | IDENTICAL |

**Orphan answers (literal level), stated exactly:**

- Entry quote with no manifest assertion: **exactly one**. F07 L28
  `“CNAs SHOULD consider whether the Vulnerabilities are Independently Fixable.”` The manifest
  assertion `rule-4-1-9-independently-fixable` is
  `"CNAs SHOULD consider whether the Vulnerabilities are <u>Independently Fixable</u>."` — the only
  difference is the two `<u>`/`</u>` markers; stripping them makes the strings equal. The entry
  literal, taken as written, is **not** a substring of `S030.txt`
  (`entry literal in S030 snapshot: False`).
- Manifest assertion with no entry row: **exactly one**, the same pair
  (`rule-4-1-9-independently-fixable`). No other assertion is orphaned in either direction.
- Additional source-worded **claim rows outside the "Exact located quotes" table** with no
  assertion at all: F08 L32 (`Article 14(4)(a)` 24-hour incident clock) and F08 L33
  (`Article 14(4)(b)` 72-hour incident clock); plus the quoted phrase `“without undue delay”` at
  F08 L23. Details in findings F3/F6.

All 19 assertions are unique (`assertions: 19 unique: 19`), and every one is a single-line
substring of its pinned capture with occurrence count 1, except `art14-2a-early-warning`, which
occurs **twice** (`S029.txt:10` and `S029.txt:20`). Longest entry quote is 20 words
(`minimize-exposure`, `rule-4-2-12-uncertainty`), inside every table's "at most 25 words" header.

## Exact commands used

Primary extraction/binding command (run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
output is the "Counts" table above, verbatim):

```bash
python3 - <<'PY'
import json, re, pathlib
B = pathlib.Path('.')
man = json.loads((B/'corpus/source-snapshots/round-23/manifest.json').read_text())
ent = {'S018':'corpus/knowledge/multiparty-vulnerability-coordination.md',
       'S030':'corpus/knowledge/cna-assignment-and-vulnerability-rules.md',
       'S029':'corpus/knowledge/cra-manufacturer-reporting-duties.md'}
Q = re.compile(r'\u201c(.+?)\u201d', re.S)
grand = [0,0,0,0]
for s in man['sources']:
    sid=s['id']; lines=(B/ent[sid]).read_text().splitlines()
    rows=[(i,Q.findall(l)[0]) for i,l in enumerate(lines,1) if l.startswith('|') and '\u201c' in l]
    mq=[(q['id'],q['quote']) for q in s['quotes']]
    same=sum(1 for (_,r),(_,q) in zip(rows,mq) if r==q)
    norm=sum(1 for (_,r),(_,q) in zip(rows,mq) if r!=q and r==re.sub(r'</?u>','',q))
    only_entry=[r for _,r in rows if r not in [q for _,q in mq]]
    only_man=[i for i,q in mq if q not in [r for _,r in rows]]
    grand[0]+=len(rows); grand[1]+=len(mq); grand[2]+=same; grand[3]+=norm
    print(f'{sid}: rows={len(rows)} assertions={len(mq)} byte_identical={same} markup_normalized={norm} entry_only={len(only_entry)} manifest_only={len(only_man)}')
    for (ln,r),(qid,q) in zip(rows,mq):
        print(f'  L{ln:<3} {qid:<42} {"IDENTICAL" if r==q else "NORMALIZED" if r==re.sub(r"</?u>","",q) else "MISMATCH"}')
    for x in only_entry: print('  ENTRY-ONLY :',repr(x))
    for x in only_man: print('  MANIFEST-ONLY:',x)
print('TOTAL rows=%d assertions=%d byte_identical=%d markup_normalized=%d' % tuple(grand))
PY
```

Observed tail:

```
S018: rows=6 assertions=6 byte_identical=6 markup_normalized=0 entry_only=0 manifest_only=0
S029: rows=6 assertions=6 byte_identical=6 markup_normalized=0 entry_only=0 manifest_only=0
S030: rows=7 assertions=7 byte_identical=6 markup_normalized=1 entry_only=1 manifest_only=1
  ENTRY-ONLY : 'CNAs SHOULD consider whether the Vulnerabilities are Independently Fixable.'
  MANIFEST-ONLY: rule-4-1-9-independently-fixable
TOTAL rows=19 assertions=19 byte_identical=18 markup_normalized=1
```

Supporting greps (each run from the repo root, outputs quoted in the findings):

```bash
grep -n -i -E "24 hours|72 hours|14 days|one month|undue delay|severe incident|actively exploited" \
  corpus/source-snapshots/round-23/S029.txt
grep -c "within 72 hours of the manufacturer becoming aware of the incident" \
  corpus/source-snapshots/round-23/S029.txt
grep -n "Page " corpus/source-snapshots/round-23/S030.txt
grep -n -E "^(3\.1\.[0-9]|4\.1\.[0-9]|4\.2\.1\.1|4\.2\.11|4\.2\.12)\b" \
  corpus/source-snapshots/round-23/S030.txt
grep -c "1\.1" corpus/source-snapshots/round-23/S018.txt          # 0
grep -ci "first\.org\|guidelines" corpus/source-snapshots/round-23/S018.txt   # 0
grep -rl "S022" corpus/source-snapshots/                          # no files
grep -rn "manifest.json\|source-recheck" --include=Makefile --include=*.yml \
  --include=*.yaml --include=*.toml --include=*.sh --include=justfile . | grep -v "^\./\.ufo/"   # no matches
```

## Findings

### F1 — HIGH — The executable rechecks never read the knowledge entries; entry quotes can be fabricated with the gate green

Evidence (reproduced, scratch copy only, `/tmp/kasegi-r23-falsify-EntryQuoteBinding/knowledge/`):
I copied each entry, replaced the **first** Evidence-table quote in each with
`“FABRICATED QUOTE NOT IN THE SOURCE SNAPSHOT”`, and ran each entry's own `recheck:` command line
verbatim (only the manifest and source paths are read by the tool):

```bash
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source S018   # exit 0, all OK
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source S030   # exit 0, all OK
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source S029   # exit 0, all OK
```

Observed: all three exits `0` and every line `OK` despite a fabricated evidence row in each entry.
Root cause is visible in the instrument: `source-recheck.py:37-68` (`load_manifest`) and
`source-recheck.py:70-125` (`check_source`, which validates the manifest record and the snapshot)
never open a knowledge file, and the only quote test is
`source-recheck.py:128-133` → `if assertion["quote"] in source_text:` at :129. The `--selftest`
exercises four cases only
(`SELFTEST clean / corrupt / missing-source / missing-manifest … exit=0`); none touches
`corpus/knowledge`. Repo-wide, no Python file matches `u201c|“`
(`grep -rn -E 'u201c|\\u201c|“' --include=*.py .` → no matches outside `.ufo/`), so no other script
parses entry quotes; `anchorcheck.py` only validates `path:NN[-MM]` citations. No CI/config file
invokes either tool (grep above → no matches).

Falsifiable consequence: F06/F07/F08's "exact located quotes" are bound to the manifest **by human
convention only**. C2's wording joins "exact located quotes" and "executable local rechecks"; the
second does not test the first. Falsifier for this finding: any instrument or test that fails when
an entry table quote is altered to text absent from its snapshot.

### F2 — MEDIUM — One of 19 rows is not the asserted literal (F07 L28)

Entry: `“CNAs SHOULD consider whether the Vulnerabilities are Independently Fixable.”`
Manifest `rule-4-1-9-independently-fixable`:
`"CNAs SHOULD consider whether the Vulnerabilities are <u>Independently Fixable</u>."`
`S030.txt:165` carries the `<u>` form, so the entry literal is not in the capture and the manifest
literal is. Re-binding the manifest to the entry's rendered rows proves the mismatch is live:

```bash
# scratch manifest whose S030 quotes are the entry's row strings
python3 corpus/instruments/source-recheck.py --manifest /tmp/kasegi-r23-falsify-EntryQuoteBinding/manA-entry-rows.json --source S030
# S030:sha256 OK
# … rule-4-1-9-independently-fixable MISMATCH reason=quote-not-found
# exit=1
```

F07 L39–L42 does disclose this ("the captured 4.1.9 line marks its final term with `<u>` emphasis …
The table above quotes the rendered text"), so it is **not** a hidden defect. What it demonstrates
is that the only row that diverges is invisible to the gate and is admitted by prose, and that
the pin is byte-brittle: a future re-capture that drops `<u>` markup — while the entry stays
correct — fails `rule-4-1-9` (would return `MISMATCH reason=quote-not-found`) and requires a
manifest edit, not a content fix.

### F3 — MEDIUM — Two Article-14 incident-track claim rows have no assertion; their support can vanish silently

F08's `Two separate Article 14 reporting tracks` table (L27–L34) asserts six clocks, and its own
header now promises "Clock (paraphrase; exact wording in the quotes table)" (L27). Four rows map to
S029 assertions (`14(2)(a)`, `(2)(b)`, `(2)(c)`, `(4)(c)`); **L32 (`Article 14(4)(a)`) and L33
(`Article 14(4)(b)`) have no exact wording in the quotes table and no manifest assertion**, so the
header's promise fails for 2 of its 6 rows. The 24-hour cell is only incidentally covered: the
manifest's `art14-2a-early-warning` literal `within 24 hours of the manufacturer becoming aware of
it` occurs at both `S029.txt:10` (14(2)(a)) and `S029.txt:20` (14(4)(a)), and a plain substring
check cannot say which locus it certifies. The 72-hour incident wording has no assertion at all
(`grep -c "within 72 hours of the manufacturer becoming aware of the incident" S029.txt` → `1` in
the capture, `0` occurrences in the manifest). The collision half is disclosed in the entry at
L52–L56 ("a substring recheck cannot distinguish the two rows"), so only the missing-assertion half
is undisclosed.

Scratch test: deleting exactly the two incident-track sentences (`S029.txt` lines 20 and 22) from
a copy, re-pinning its sha256 in a scratch manifest, leaves the gate completely green:

```
[manB.json S029] exit=0
S029:sha256 OK … art14-4c-incident-final-report OK … art71-general-application OK
after deletion, incident-24h in capture: True      # survives only via the 14(2)(a) substring at line 10
after deletion, incident-72h in capture: False     # the entry's 14(4)(b) support is gone, gate silent
```

Delta versus the sibling `falsify/S029Quotes.md` (which independently established the six table
rows are byte-exact and flagged the `:10`/`:20` duplication as an attribution note, explicitly
"not a defect"): the collision is now disclosed in-entry (L52–L56) and the summary column is
labelled a paraphrase (L27), so attribution ambiguity is no longer the live issue. What survives is
coverage: two incident-track rows advertised as carrying their exact wording in the quotes table
carry none, and loss of their support is undetectable by the declared recheck.

### F4 — MEDIUM — The entries' "exact location" columns are entirely unasserted

The manifest asserts only quote substrings. Scratch test: renumber every cited S030 section
(`3.1.1→7.7.7`, `3.1.4→7.7.4`, `4.1.2→9.9.2`, `4.1.9→9.9.9`, `4.2.1.1→9.8.1`, `4.2.11→9.8.11`,
`4.2.12→9.8.12`) and shift **every** `<!-- Page N -->` marker by +50, then re-pin:

```
[C S030 renumbered sections + shifted pages] exit=0
S030:sha256 OK … rule-4-2-12-uncertainty OK
page-11 marker still present: False | shifted to 61: True
```

All seven assertions stay `OK`. Two concrete location defects therefore survive the gate:

- `grep -n "Page " S030.txt` shows markers `1,2,8,9,10,11,12,13,14,15,16,17` — pages **3–7 have no
  marker in the capture**, so F07's "3.1.1, page 7" and "3.1.4, page 7" cannot be checked from the
  pin (they sit at `S030.txt:64,73`, before the page-8 marker; no contradiction, no proof).
- F07 prose (L33–L37) cites "section 3.2.4.2, pages 9–10"; `S030.txt:110` (3.2.4.2) is followed by
  the page-10 marker at `S030.txt:112`, i.e. the paragraph is on **page 9 only**. With five page
  markers missing from the capture, this is best described as an unverifiable and probably
  imprecise citation rather than a proven false one.

QUALITY Q3 (`corpus/QUALITY.md:16`) requires "a verbatim quote of ≤25 words with its exact
location (section heading, page, or line plus revision)". The quote half is gated one-way
(manifest→capture); the location half is gated nowhere (F1, F4).

### F5 — LOW — A cross-version claim has no local capture at all (F07 L17)

F07 L17 states "independently fixable guidance moved from 4.1.10 in 4.1.0 to 4.1.9 in 4.2.0."
No snapshot of 4.1.0 exists: `grep -rl "S022" corpus/source-snapshots/` returns no files, and
`corpus/SOURCES.md:28` lists S022 with status `queued`. The S030 side of the claim is capture-
supported (`S030.txt:165` = 4.1.9 Independently Fixable; `S030.txt:166` = 4.1.10 interdependent
conditions), but the "moved from 4.1.0 §4.1.10" half is unverifiable from pinned artifacts and is
not fenced as a capture gap the way F06's version claim is (F06 L56–L61 explicitly discloses that
`S018.txt` has no title/version banner). Falsifier: an S022/4.1.0 capture in which §4.1.10 does not
carry the Independently Fixable text.

### F6 — LOW — One quoted source phrase and two quoted claim cells carry no assertion

- F08 L23 quotes `“without undue delay”` as Article 14 wording. It is a genuine capture substring
  (`S029.txt:10,12,20,22,…`), but the manifest has no assertion for it, so it is a quoted phrase
  bound to nothing.
- F08 L32/L33 (see F3) are the claim-row instances.

These are not false quotes; they are quoted source material outside the assertion set, i.e. the
assertion set is a strict subset of the quoted-source surface of the three entries.

## Extraction completeness control (so "no orphan" is not an artifact of a narrow regex)

Every U+201C…U+201D span was enumerated per entry (11 / 9 / 9 spans for F06 / F07 / F08), not only
table lines. Non-substring spans, with classification:

| Entry | Span | Classification |
|---|---|---|
| F06 L36 | `vendor` | reviewer vocabulary ("one undifferentiated 'vendor' row") |
| F06 L39 | `not affected`, `fixed` | reviewer states the worksheet must not convert unknown into |
| F06 L43 | `The upstream vendor shipped, …` | `Rejected:` strawman |
| F06 L57 | `version 1.1, Spring 2020` | provenance attribution; entry already discloses the capture carries no version banner (`grep -c "1\.1" S018.txt` → `0`, `grep -ci "first\.org\|guidelines"` → `0`) |
| F07 L47 | `two CVE IDs because two weakness names are present` | hypothetical worksheet being rejected |
| F07 L55 | `Every fix, vulnerable dependency upgrade, …` | `Rejected:` strawman |
| F08 L61 | `14 days after awareness` | hypothetical worksheet label |
| F08 L70 | `CRA requires every researcher to publish …` | `Rejected:` strawman |

No source quote is presented without either a manifest assertion or a disclosed capture gap, apart
from F08 L23/L32/L33 above. This makes the "exactly one literal orphan pair" statement safe.

## Residual risk

1. **Binding is conventional, not enforced** (F1). Any future edit to F06–F08 can falsify or
   silently replay quotes with every declared gate green; nothing in CI or the instrument suite
   reads entry quotes.
2. **One-way verification** (F1/F2): manifest→capture is checked; entry→manifest is eye-checked.
   The single existing divergence (F07 L28) is admitted by prose, which is exactly the class of
   change the gate cannot police.
3. **Byte brittleness** (F2): one assertion (`rule-4-1-9`) depends on presentation markup. A
   format-only re-capture breaks the pin even though the entry text is correct, encouraging
   assertion weakening rather than content review.
4. **No locus or uniqueness check** (F3): substring matching accepts a quote found anywhere in the
   capture; attribution to the named article/section is unproved, and duplicate loci (`:10`/`:20`)
   are indistinguishable.
5. **Location column unbound** (F4): section/page citations can drift or be imprecise with no gate
   movement; the S030 capture itself lacks page markers 3–7.
6. **Unsatisfied coverage claims** (F5): the 4.1.0→4.2.0 section-move claim has no local capture.

## Verification gaps and scope limits

- Live-tree note: F06 and F08 changed while this review ran (F06 +7 lines: the disclosed capture
  gap at L56–L61; F08 +10 lines: the L52–L56 non-uniqueness disclosure, the L27 column relabel, and
  the L79–L81 OJ-date disclosure). The binding measurement and every line reference above were
  re-run against the final observed bytes; counts stay 6/6, 7/7, 6/6 and the row blocks stay at
  F06 L25–L30, F07 L25–L31, F08 L45–L50. Because entries can change without the gate noticing (F1),
  a byte-level review of a live tree is a snapshot in time.
- Read-only w.r.t. production: the only persistent write is this report. All mutation experiments
  used copies under `/tmp/kasegi-r23-falsify-EntryQuoteBinding/` (S018/S029/S030, manifest copies
  `manA-entry-rows.json`, `manB.json`, `manC.json`, mutated entries under `knowledge/`). No git/jj
  index or state was touched, nothing was committed, and the lane tree, sibling reports, and fleet
  repo were not modified. Scratch lives outside the repo and is disposable: every experiment's exit
  code and output is inlined above, so no conclusion in this report depends on those files
  surviving, and each experiment is reconstructible from its quoted command.
- I did not re-fetch upstream sources; freshness, legal correctness, and bounty/entitlement
  conclusions are out of scope. A pin proves captured bytes only.
- I did not run the repository's full test suite; I ran `source-recheck.py --selftest` (exit 0, four
  cases) to establish what the instrument covers, not to certify repo health.
- Word-count and "exact location" judgments use `str.split()` on the quoted span; punctuation is
  counted as part of a word, so counts are conservative relative to the "at most 25 words" header.
- Page-number statements about `S030.txt` are limited by the capture's own missing markers
  (pages 3–7 absent, and the page-2 marker spans the table of contents and the start of §3), so I
  report them as unverifiable rather than falsified except where the marker ordering contradicts a
  cited span.
- No installs or upgrades were needed or performed; no package transactions were attempted
  (host-wide pacman pause respected).
