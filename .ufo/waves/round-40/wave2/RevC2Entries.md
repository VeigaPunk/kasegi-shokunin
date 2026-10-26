# RevC2Entries — falsify-wave 2, round 40 (kasegi)

Seat: reviewer (leaf, no subagents). Item: attack the C2 knowledge entries — for each mined
entry among the nine decided rows (S016, S017, S019, S020, S021, S023, S025) and the S060+
mined entry (S060), re-run `source-recheck.py`, verify QUALITY Q1–Q6, and re-open quotes in
the captures. Lane HEAD (= judged head J; the receipt `.ufo/waves/round-40/final-gates/` is
still untracked, so committed bytes = J): `3074c7679d6f527ec3930d7748ccce1dbae4a58a`. Claims
freeze `5e985b74075dd3813a63d7750966bf8abf693465`. No lane file was edited; no mutating git
command; no pacman; no tool installed (existing python3/curl/git only). Scratch
`/fast/scratch/hyaku/kasegi-r40/RevC2Entries/` removed before yielding.

## 0. What was attacked and how

- **Recheck re-runs** against committed bytes: `git archive HEAD` exported to scratch
  (7,932 files) and every command run there; the lane working tree re-run diffed identical.
- **Q1–Q6** verified per entry by reading all 8 entries in full and by mechanical checks
  (span extraction, normalization identical to the instrument's, word counts, header shape,
  `bash -n` + cold-cwd dry-run of every `recheck:` line, credential/URL scans).
- **Quote re-open**: all 144 block-quoted spans and all 95 inline quoted spans in the 8
  entries were matched against the captures under the instrument's own normalization
  (whitespace collapse, `<u>` stripped), with a strict start-line check (141/144 block spans
  start on their declared line; the 3 exceptions are sentence-start-vs-fragment-start on
  wrapped lines, below). Every FC grep tally stated in the entries was re-run.
- **Live re-open**: all 8 source URLs re-fetched (`curl -sS -L --max-time 90 -A
  kasegi-shokunin/1.0`, HTTP 200 ×8, 2026-10-26T22:11:07–09Z) and normalized with the lane's
  own `corpus/instruments/capture-source.py` (`html_to_text()` / `pdf_to_text()`).

## 1. source-recheck exits (reproduced — all green)

Command shape (run in the HEAD export; lane re-run identical):
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S###`

| source | exit | pins |
|---|---|---|
| S016 | 0 | sha256 OK; Q1/Q2/Q3 OK, occ=1, anchors 17/16/12-ok |
| S017 | 0 | sha256 OK; Q1/Q2/Q3 OK, occ=1, anchors 23/34/34-ok |
| S019 | 0 | sha256 OK; Q1/Q2 occ=2 anchor=80-ok, Q3 occ=1 anchor=97-ok |
| S020 | 0 | sha256 OK; Q1 normalized=markup-whitespace occ=1 anchor=142-ok |
| S021 | 0 | sha256 OK; Q1 occ=1 anchor=133-ok |
| S023 | 0 | sha256 OK; Q1 anchor=151-ok, Q2 anchor=154-ok |
| S025 | 0 | sha256 OK; Q1 anchor=32-ok, Q2 anchor=507-ok (normalized) |
| S060 | 0 | sha256 OK; Q1/Q2/Q3 OK, occ=1, anchors 7/15/50-ok |

Full manifest (no `--source`): 8 sources, 18 quote assertions, all OK, exit 0. No record in
the manifest fails; no mined row lacks a manifest record.

## 2. Live re-open of the captures (reproduced — 8/8)

| source | HTTP | raw bytes | raw sha256 (this fetch, 22:11Z) | normalized vs capture |
|---|---|---|---|---|
| S016 | 200 | 164,126 | `fa4e70bc…` (= manifest raw) | **byte-identical** (4,481 B) |
| S017 | 200 | 14,764 | `83030d82…` (3rd distinct raw; per-request nonce, disclosed in wave1 scribe receipt) | **byte-identical** (5,058 B) |
| S019 | 200 | 44,658 | `68de5685…` (entry recorded `1703b295…`, same size) | **byte-identical** (4,901 B) |
| S020 | 200 | 140,909 | `d0cfa766…` (= manifest and entry) | **byte-identical** (16,693 B) |
| S021 | 200 | 127,832 | `5dea96fd…` (entry recorded `fc726728…`, same size) | **byte-identical** (58,004 B) |
| S023 | 200 | 75,587 | `383792fd…` (= manifest and entry) | **byte-identical** (14,357 B) |
| S025 | 200 | 602,933 | `334417c3…` (= manifest and entry) | **byte-identical** (71,851 B) |
| S060 | 200 | 6,419,901 | `2d8bbf26…` (raw unstable, disclosed) | slice recomputed from live page = capture **byte-identical** (`d6862622…`); live normalized full-page sha256 `ffe8c0b6…` **equals** the manifest's `full_text_sha256` |

Raw-body churn on S016/S017/S019/S021/S060 is disclosed where it matters (S016 footer A/B in
the entry; S017 nonce in `wave1/ScribeEntriesG1.md`; S060 Cloudflare tokens in manifest and
entry); the normalized text every quote cites is stable and reproduced live today.

## 3. Per-entry verdicts (Q1–Q6)

Common facts verified for all 8: header block directly under the H1 is `source:` /
`verified-at:` (ISO 2026-10-26) / `ground:` / `recheck:` — the three Q1 lines present in
order, `ground:` being the round-40 convention recorded in `wave1/ScribeEntriesG1.md`; every
`recheck:` line parses under `bash -n`, carries the `cd <lane> &&` prefix, and exits 0 when
run from `/` (cold cwd); every own-source row is tier A and opened 2026-10-26 (Q2); every
entry has an Attribution section with first-party labelling (Q4), a falsifiable-rule block
and a rejected-over-generalizations block (Q5), and no credential, session or private URL —
the credential-token grep hits are descriptive prose (CVE-Bench's brute-force ban, CycloneDX
field names) and the only named addresses are public CISA inboxes (Q6). All 8 committed
entries are byte-identical to their wave1 deliverables (sha256 match vs
`wave1/ScribeEntriesG1.*`, `ScribeEntriesG2.*`, `ScribeF23.entry.md`).

| # | entry (source) | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | anthropic-cvd-provenance-and-pacing (S016) | ✓ | ✓ | ✓ 22 spans occ=1, ≤24 w, start-on-line 22/22; 12 inline clean | ✓ | ✓ rule a–f + 8 rejected | ✓ | **PASS** |
| 2 | pz-reporting-transparency-trial (S017) | ✓ | ✓ | ✓ 24 spans occ=1, ≤25 w, 24/24; 8 inline clean | ✓ | ✓ rule a–f + 7 rejected | ✓ | **PASS** |
| 3 | nist-sp800-216-vdp-framework (S019) | ✓ | ✓ | ✓ 14 spans (8 occ=1, 6 occ=2–3 anchored), ≤24 w; 14 inline clean | ✓ | ✓ rule a–f + 7 rejected | ✓ | **PASS** |
| 4 | doj-vdp-framework-scope-and-authorization (S020) | ✓ | ✓ | ✓ 14 spans; FC-7 run: anchors_ok 15/15; 2 minor findings (D1, D3) | ✓ | ✓ rule a–e + 6 rejected | ✓ | **PASS** w/ minor findings |
| 5 | cisa-bod-20-01-vdp-minimums (S021) | ✓ | ✓ | ✓ 21 spans; FC-10 run: anchors_ok 27/27; 1 minor finding (D1) | ✓ | ✓ rule a–f + 7 rejected | ✓ | **PASS** w/ minor finding |
| 6 | cisa-cvd-program-stages (S023) | ✓ | ✓ | ✓ 16 spans; FC-9 run: anchors_ok 17/17; 1 minor finding (D2) | ✓ | ✓ rule a–e + 7 rejected | ✓ | **PASS** w/ minor finding |
| 7 | cve-bench-agent-exploitation-benchmark (S025) | ✓ | ✓ | ✓ 21 spans; FC-9 run: anchors_ok 32/32; 2 minor findings (D1, D3) | ✓ | ✓ rule a–e + 6 rejected | ✓ | **PASS** w/ minor findings |
| 8 | cyclonedx-analysis-subtree (S060) | ✓ | ✓ | ✓ 12 spans occ=1 ≤21 w + table cells; S055/S057 cross-cites verified; 1 minor defect (D4) | ✓ | ✓ rule a–f + 7 rejected | ✓ | **PASS** w/ minor defect |

Entries' own FC one-liners executed against the lane captures all reproduce their claimed
outputs: S020 `anchors_ok 15 of 15`, S021 `27 of 27`, S023 `17 of 17`, S025 `32 of 32`.
FC grep tallies reproduced exactly: S016 (`90-day=2, 45 days=1, 7-day=3, 14-day=1, AI=4,
labeled=2, pacing=1, coordinator=1`; `30-day=0`; `Responsible Disclosure Policy` L8 only),
S017 (`trial=7, upstream=9, patch gap=4, downstream=4, 90+30=2, 90-day=2`, five catalogue
acronyms 0), S019 (`federal=9, disclosure=11, recommends=2, NIST=7, policy=3`,
`deadline`/`timeline`/CVSS/KEV/EPSS/CSAF 0; dates L96/L97/L74/L75), S020 (FC-1/2/3/4/5/6/8 =
1/1/4/3/1/0/1), S021 (FC-1…FC-9 = 1/1/1/6/10/4/2/2/1), S023 (FC-1…FC-8 = 7/3/1/1+1/0/0/1/5+3),
S025 (FC-1…FC-8 all reproduce; four rate sentences each count 1 under whitespace collapse),
S060 (SHALL=0, MUST=0, should=2; 14 zero-counts; enum sizes 6/9/5/3; rare states 1/1/1;
`Default` L105 only; 111 lines, sha `d6862622…`) — **except D4 below**.

## 4. Findings

### D4 (minor, defect) — cyclonedx-analysis-subtree.md FC-2 lane counts do not reproduce
`corpus/knowledge/cyclonedx-analysis-subtree.md` FC-2 states, under its own named command
(`grep -oiF <word> | wc -l`, case-insensitive): `state=3 … response=3 … detail=1 …`.
Measured on `corpus/source-snapshots/round-40/S060.txt` with exactly that command:
`state=4` (L5 field name, L7, L18, L32), `response=4` (L30; L32 ×3 — "A response", "More
than one response", "Responses"), `detail=3` (L42; L44 "Detailed" + "details"). The other
five counts and all zero-counts reproduce. The drawn conclusion (no vocabulary overlap with
CSAF) is unaffected, but the figure is not reproducible as stated — a wrong specimen figure
in an FC line (R19/R2 territory). Repro: `grep -oiF state corpus/source-snapshots/round-40/S060.txt | wc -l` → 4.

### D1 (minor) — four inline quotes are not verbatim: ASCII apostrophe where the capture has U+2019
Under the lane's declared normalization (whitespace + `<u>` only, no apostrophe folding)
these four inline quoted spans do not match the capture, though every word is identical:
- `cisa-bod-20-01-vdp-minimums.md` entry L10 — "…Security Agency's Binding Operational
  Directive 20-01" (capture L91 has `Agency’s`);
- same file entry L116 — "…the Department of Justice's Framework…" (capture L198 `Justice’s`);
- `cve-bench-agent-exploitation-benchmark.md` entry L10 — title "…AI Agents' Ability…"
  (capture L1 `Agents’`);
- `doj-vdp-framework-scope-and-authorization.md` entry L84 — "…that the individual's
  actions…" (capture L293 `individual’s`).
None is in the entry's own FC anchor list (those lists use the correct curly forms and pass
27/27, 32/32, 15/15), so the entries' "every quoted anchor holds its quote" phrasing
overstates coverage by these four. No pinned manifest quote is affected (all 18 pins are
verbatim-clean). Fix is a 4-character class of edits; no claim changes.

### D2 (minor) — cisa-cvd-program-stages.md renders a line join inside the quote marks
Entry L44 quotes `"In scope → CVE / Out of scope → Referred / closed" (L125-L126)`. The
capture prints the branches on separate lines — L125 `In scope → CVE`, L126 `Out of scope →
Referred / closed` — with no slash between them; the first `/` is the entry's join notation
presented as quotation (the second `/` is capture text). The claim it supports ("a two-way
branch") is accurate; the quote is not.

### D3 (minor) — four spans cite the sentence's first line, not the fragment's
The quoted fragment starts one line later than the declared location (sentence-start
convention on wrapped lines; inside the instrument's window semantics, so anchors print
`ok`): `doj-vdp…md` entry L20 inline `(L23)` — fragment starts capture L22; same file block
span entry L94 `— L298` — starts L299; `cve-bench…md` block spans entry L48 `— L333` —
starts L334, entry L74 `— L507` — starts L508. S025's honest limit discloses window
matching ("anchors … are ranges rather than single points"); S020's does not for these two.

### Benign (not defects)
- Two inline elided quotes marked with `…` (S021 L305, S020 L283) — elisions, and the S020
  one is the entry's own flagged source-typo reference; both fragments verbatim.
- `cyclonedx…md` cites `S055.txt:L2151-L2152` (round-38 capture): verified — the quoted
  "an impact statement SHALL exist as machine readable flag" is on L2152 of
  `corpus/source-snapshots/round-38/S055.txt` (sha `63c8ad52…`, last touched round 38);
  likewise S055 L1855/L2844/L3096 and S057 L136-138 all hold as cited.
- S021's checklist dates rendered as ISO (`2020-10-02`, …) are the entry's paraphrase of
  "Friday, October 2, 2020" etc. (L186–L196), not quote-marked; values and lines correct.

### Outside the entry files (noted for the C2 owner)
- `corpus/lessons/round-40.md` line 27 carries a stray `?` in "tier A +3?mined S016/…"
  (intended a dash/paren); cosmetic, numbers correct (59→62, +3 tier A).
- Rejected-row Gate evidence verified: S022 and S024 rejection blocks carry reason + flip
  (lesson §Rejected), and the claimed supersessions exist — `supersedes S022` ×1 (S030 row)
  and `supersedes S024` ×1 (S029 row) in `corpus/SOURCES.md`; S061/S062 rejected with
  reason+flip; S060 row status mined, used-by the S060 entry.

## 5. C2 counting commands re-run at the HEAD export (all reproduced)

1. queued among the nine → **0** (was 9); 2. mined among the nine → **7** (≥4); 3. entries
citing the nine → **7** (= mined count); 4. S060+ registry rows → **3** (≥1); 5. entries
citing S060+ → **1** (≥1); 6. frontier rows → **23**; 7. `frontier-recheck-count.py` →
`entries=26 pass=26 exit=0` incl. `PASS F23 … ids=S060`; 8. fleet census validate →
**exit 0**, warnings exactly `W04 S028` + `W04 S029` (matches `census-before.txt` shape and
the claim's "W04 S028/S029 only"). Junk control (`c2-controls/junk-decisions.md`, all-nine
flip-to-rejected with no evidence) is the do-nothing baseline and is owned by the junk seat;
its counter requirements (mined ≥4 + Gate-block evidence) are not met by it by construction.

## 6. Result

No entry fails Q1–Q6; no recheck is non-zero; every capture reproduces live today. The C2
entry layer stands. Defects found: **1 minor defect (D4)** and **7 minor verbatim/location
infidelities (D1×4, D2, D3×4 spans in 3 findings)** — none load-bearing, none pinned, none
claim-changing; listed with exact coordinates for the C2 owner to fix in a follow-up round.
