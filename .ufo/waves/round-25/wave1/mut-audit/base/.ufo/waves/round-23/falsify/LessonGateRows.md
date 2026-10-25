# Falsify — round-23 lesson §Gate field audit (S018, S028, S029, S030)

Seat: `L1Kasegi23.LessonGateRows-2` · lane: round-23 falsify · read-only attack on landed bytes.
Assigned item: "For every new row (S029, S030) and every touched row (S018, S028) verify the Gate
block records the URL, access date and a located quote ≤25 words, and that every
status/recheck/used-by change is logged old→new. Report each missing or wrong field with its line
number; do not rewrite the lesson."

All paths relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Bytes under test

| file | sha256 | note |
|---|---|---|
| `corpus/lessons/round-23.md` | `a8ecf737fb5b46d6f98b2ad8d6120e11b27597be8cfd27ffbace3e4ca688840c` | 296 lines, HEAD `8acb255`, worktree == HEAD blob |
| `corpus/SOURCES.md` | `e64f095b7a86e8c4443e1020ab21def2b424d41193c3975e2363c06b0ebf0ab5` | 31 registry rows |
| `corpus/source-snapshots/round-23/S018.txt` | `d366bf40…27ab4` | |
| `corpus/source-snapshots/round-23/S029.txt` | `82514478…32b8c` | |
| `corpus/source-snapshots/round-23/S030.txt` | `673526db…5ab019` | |
| `corpus/source-snapshots/round-23/S031.txt` | `3c7ae8ba…460678` | |
| `corpus/source-snapshots/round-23/manifest.json` | `e06aa3cd…0eeba` | sources `S018,S029,S030,S031` |

**Drift disclosure.** The lesson changed under me during the audit (236 → 293 → 296 lines as the
post-attack repairs and the Q7/Q8 log landed). Every line number below is pinned to blob
`a8ecf737` at HEAD `8acb255`; `git status --porcelain` is empty for the lesson, the registry and
the snapshots at audit time, so these are committed bytes, not a sibling's half-edit.

## Verdict — the four required fields per row

| row | URL | access date | located quote ≤25 words | location | transition log |
|---|---|---|---|---|---|
| S028 (new, rejected) | **pass** (`:35`) | **pass** 2026-10-20 | **pass** 10 w | **pass** heading given | **FAIL old value** (F4) |
| S029 (new) | **pass** (`:36`) | **pass** 2026-10-20 | **pass** 13 w, byte-exact in capture | **pass** Art. 14(2)(c) (OJ date caveat F8) | **partial** (F5) |
| S030 (new) | **pass** (`:37`) | **pass** 2026-10-20 | **pass** 11 w, byte-exact; page 15 verified | **pass** | **FAIL stale used-by** (F2), no S031 row (F1) |
| S018 (touched) | **FAIL — absent** (F3) | **FAIL — no per-row field** (F3) | **pass** 12 w, byte-exact | **pass** both headings verify | **pass** (status, used-by, recheck logged) |

Quote word counts (mechanical): S028 10, S029 13, S030 11, S018 12 — all within the 25-word cap.

## Findings

### F1 — HIGH — a new registry row (S031) has no Gate entry, and the Gate's own row enumeration is incomplete

`corpus/SOURCES.md:37` is a row added by this round (`git log -S'| S031 |'` → `2712c99`):

```
| S031 | CVE Numbering Authority Operational Rules v4.2.6 — https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | spec | A | … | Approved 2026-10-14, effective 2026-10-20; sections 3.1, 3.2.4.2, 4.1 and 4.2 — rule 4.2.11 page 15 | supersedes S030 — current 4.2.6 makes independent-fixability ID separation a MUST; S030's 4.2.0 SHOULD is historical. | mined | 2026-10-25 | on-release | corpus/knowledge/cna-assignment-and-vulnerability-rules.md |
```

- `grep -cE '^\| S031' corpus/lessons/round-23.md` → **0**. No Gate table anywhere in the lesson
  has a URL, accessed date, quote or location for S031.
- `corpus/lessons/round-23.md:192` states the round's opened-row set: "Opened rows this round are
  S018, S029, S030 and S028 (rejected)" — false at HEAD: `git diff 922a4dd..HEAD -- corpus/SOURCES.md`
  adds four rows (S028, S029, S030, S031), and S031's `opened` is 2026-10-25, inside this round.
- The only S031 records are repairs prose `:252` ("new row S031 + normalized `pdftotext` snapshot
  `S031.txt` + 10 manifest assertions"), `:273`, `:280`, `:291`. None carries the four Gate fields.

Consequence: F07's current-rule authority (v4.2.6, 4.2.11 SHOULD→MUST) is the row with no Gate
record, while the superseded v4.2.0 row still holds the only Gate row.

### F2 — HIGH — S030's registered `used-by` contradicts the entry it names, and the rebinding is not logged old→new

- `corpus/SOURCES.md:36` (S030) `used-by` = `corpus/knowledge/cna-assignment-and-vulnerability-rules.md`.
- That entry's own header, `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:3`:
  `source: S031 — https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf — CNA Operational Rules 4.2.6, approved 2026-10-14, effective 2026-10-20; …`
- `corpus/SOURCES.md:37` (S031) also carries `used-by` = the same entry.

So two rows claim the same consumer and one of them is false. The Gate's `used-by` requirement is
exactly this field (R8: "Log every status/recheck/used-by old→new change"), and the attempt-2 Gate
table (`:196-204`) has **no** row for S030 `used-by` and no row for S031. The repairs section says
only "S030/S022 kept as historical rows" (`:252`), which is not a field-level old→new log.

Cell-level base→HEAD registry diff (script below) reports exactly two modified cells
(`S018.status`, `S018.used-by`) and four added rows — so no literal S030 cell edit occurred; the
defect is that the rebinding needed one and the Gate never records the new state.

### F3 — MEDIUM — S018 (touched row) has no Gate table row: URL missing from the entire lesson, access date only block-collective

- Gate table `:33-37` has three rows; `awk 'NR>=33&&NR<=37' … | grep -c '| S018'` → **0**.
- S018's Gate content is prose at `:39-42` and contains **no URL**:
  `grep -c 'first\.org' corpus/lessons/round-23.md` → **0** (whole lesson).
- Access date: `:29` "Opened public official sources on 2026-10-20" is block-level; `:39` says only
  "Existing S018 re-opened" with no date. The registry keeps `opened` = 2026-10-19
  (`corpus/SOURCES.md:24`) and the entry records `verified-at: 2026-10-20`
  (`corpus/knowledge/multiparty-vulnerability-coordination.md:3`). No field states S018 was accessed
  on 2026-10-20; a reader must infer it from a sentence that names no row.

The two present fields are correct: quote `:40-41` (12 words) is byte-exact in `S018.txt:36`;
location (`Maintain clear and consistent communications` → `Prior to disclosure`) verifies against
`S018.txt:32` and `:34`.

### F4 — MEDIUM — S028 is logged as a status no-op although the row is new relative to the frozen base

- `git show 922a4dde90b60b465e2b8b241d1fe363f1f27e98:corpus/SOURCES.md | grep -cE '^ *\| *S028'` → **0**.
- `git show HEAD:corpus/SOURCES.md | grep -cE '^ *\| *S028'` → **1**; introduced at `8bf9807`
  (`git log --oneline -S'| S028 |' -- corpus/SOURCES.md`).
- `corpus/lessons/round-23.md:204`: `| S028 | status | rejected | rejected (duplicate-row proposal; flip unchanged) |`

The `old` cell asserts a prior `rejected` status that did not exist at the frozen base. The same
table uses the correct convention one screen earlier (`:201-202`, `(new row) | — | …`). S028's
creation fields — `opened: 2026-10-20`, `recheck: 90d`, `used-by: —` (`corpus/SOURCES.md:34`) —
are logged nowhere.

### F5 — MEDIUM — new-row transition rows omit the `recheck` and `used-by` values those rows gained

- `:201` `| S029 | (new row) | — | mined, spec/A, supersedes S024 |`
- `:202` `| S030 | (new row) | — | mined, spec/A, supersedes S022 |`
- Registry: `S029` recheck `on-release`, used-by `corpus/knowledge/cra-manufacturer-reporting-duties.md`;
  `S030` recheck `on-release`, used-by `corpus/knowledge/cna-assignment-and-vulnerability-rules.md`.

R8 names status, recheck and used-by as the fields to log. S018 gets a per-field `recheck` row
(`:200`) for a value that did **not** change (`180d → 180d (unchanged)`), while S029/S030 — which
did acquire recheck and used-by values — get none. The logging is inverted relative to the rule.

### F6 — LOW — the Gate section's census tallies are stale against the registry they describe

- `:207` → "exit **0**, 30 registry rows"; `:233-236` → "registry rows 27 → 30 (tier A=28, C=2;
  status mined 18, queued 9, rejected 3; 18 rows carry `used-by`)".
- `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi`:
  `rows 31`, `tier.A 29`, `tier.C 2`, `status.mined 19`, `status.queued 9`, `status.rejected 3`;
  `awk` used-by count → **19**.
- The control in the same paragraph still reproduces exactly: `validate` → exit **0** with the two
  W04 warnings (`S028`, `S029`) and `/…/corpus/SOURCES.md` `ok`.

The S031 landing (`2712c99`) moved every one of these numbers by one and the later "Corrected C1/C2
measurement" paragraphs (`:263-278`) update only C1/C2, not the Gate census.

### F7 — LOW — S018's Gate quote is line-split, and its version claim has no supporting artifact

- `grep -c "All parties should clearly and securely communicate and negotiate expectations and timelines" corpus/lessons/round-23.md` → **0**; the sentence is broken at `:40|:41` ("…communicate and" / "negotiate…"). Joining the block reproduces it, so a line-oriented checker cannot locate it.
- `:41-42` asserts "The HTML metadata title says version 1.0; the document body explicitly says
  version 1.1 and Spring 2020". `grep -cE 'Version|1\.1|Spring 2020' corpus/source-snapshots/round-23/S018.txt` → **0** (8,372-byte capture starts at `## Definitions`). M18 (`:296`) discloses the capture gap for the *entry*; the Gate statement stays unqualified, so the filed record asserts a basis no repo byte carries.

### F8 — LOW — S029's Gate location carries an OJ date that is not in the pinned capture

`:36` location ends "…Article 14(2)(c), OJ 20.11.2024". `grep -c '20.11.2024' corpus/source-snapshots/round-23/S029.txt` → **0**; the capture's only date line is `S029.txt:128` "Done at Strasbourg, 23 October 2024". Disclosed at M18 (`:296`) for the entry; the Gate's location cell is the only place the date appears as if sourced.

### F9 — MEDIUM (verifiability) — S028's Gate quote has no local evidence at all

- No capture and no manifest assertion: `manifest.json` sources are `['S018','S029','S030','S031']`;
  `find . -name '*S028*' -o -name '*S006*'` → **no files**.
- The quote "Adopting a Safe Harbor does not change the program scopes." exists in-repo only at
  `corpus/lessons/round-22.md:82` (the record M5 declares mislocated) and
  `corpus/knowledge/authorization-safe-harbor-and-scope.md:20` — both authored transcriptions.

So `:30-31` ("S028 is a rejected duplicate proposal: its scope quote is real") is not reproducible
from repo bytes: S028 is the one Gate row of the four whose quote, heading claim and accessed date
can only be re-read from another lesson's prose.

## Controls that hold (checked, not assumed)

| check | command | result |
|---|---|---|
| S029 quote exactness | substring test in capture | `True`, inside `S029.txt:14` |
| S029 section | `S029.txt` structure: `Article 14` `:2`, `2.For the purposes…` `:8`, `(c)` `:14` | Article 14(2)(c) correct |
| S030 quote exactness | same | `True`, `S030.txt:211` verbatim incl. final period |
| S030 page claim | `<!-- Page 15 -->` at `S030.txt:209`, rule at `:211` | "page 15" correct |
| S030 version/effective | `S030.txt:12,16` | 4.2.0 / effective 2026-August-25 correct |
| S018 quote + location | `S018.txt:32`, `:34`, `:36` | heading, sub-heading and sentence all match |
| S018 status/used-by transitions | base cell diff | `queued→mined`, `—→corpus/knowledge/multiparty-vulnerability-coordination.md` — both logged at `:198-199` |
| S022/S024 untouched | base→HEAD cell diff | zero modified cells; `:203` statement accurate |
| 25-word cap | word counts | 10 / 13 / 11 / 12 |
| Gate table shape | `:33-34` header has `row | URL | accessed | exact quote (≤25 words) | location` | as specified |

Note on `supersedes` placement (observation, not a defect): all three superseding rows carry
"supersedes S### —" at the head of the `teaches` cell (`SOURCES.md:35,36,37`), consistent across
the set; no row begins with it, so R8's "new row beginning 'supersedes S### —'" is satisfied
under the teaches-cell reading only.

## Scope limits

- I did not evaluate admission, score movement, C1 matrix numbers, README frontier counts, or the
  knowledge entries' bodies; those belong to other seats and to the canonical judge.
- No network fetch: S028/S006 (HackerOne), the FIRST HTML metadata, and the OJ publication date are
  unverified **because no permitted traffic exists for this seat and no capture exists in-repo** —
  that is F9/F7/F8's premise, not a shortcut.
- S031's own quote/location could not be audited as a Gate field because no Gate row exists (F1);
  only its registry cells were read.
- Sequential dependency: F1/F2 constrain each other — F2's remedy (repoint or clear S030 `used-by`)
  and F1's remedy (a Gate row for S031) are one landing.

## Reproduction

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/lessons/round-23.md corpus/SOURCES.md   # a8ecf737… / e64f095b…
git rev-parse --short HEAD                               # 8acb255

grep -cE '^\| S031' corpus/lessons/round-23.md            # 0   (F1)
awk 'NR>=33 && NR<=37' corpus/lessons/round-23.md | grep -c '| S018'   # 0   (F3)
grep -c 'first\.org' corpus/lessons/round-23.md           # 0   (F3)
awk -F'|' '$2 ~ /^ *S030 /{gsub(/^ +| +$/,"",$12); print $12}' corpus/SOURCES.md   # entry path (F2)
sed -n '3p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md             # source: S031 (F2)
git show 922a4dde90b60b465e2b8b241d1fe363f1f27e98:corpus/SOURCES.md | grep -cE '^ *\| *S028'   # 0 (F4)
bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi   # rows 31 (F6)
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi # exit 0, W04 x2
grep -c "All parties should clearly and securely communicate and negotiate expectations and timelines" corpus/lessons/round-23.md  # 0, wrapped (F7)
grep -cE 'Version|1\.1|Spring 2020' corpus/source-snapshots/round-23/S018.txt      # 0 (F7)
grep -c '20.11.2024' corpus/source-snapshots/round-23/S029.txt                     # 0 (F8)
python3 -c "import json;print([s['id'] for s in json.load(open('corpus/source-snapshots/round-23/manifest.json'))['sources']])"  # no S028 (F9)
```

Base→HEAD registry cell diff used for the transition audit:

```python
import subprocess, re
def rows(rev):
    t = subprocess.run(['git','show',f'{rev}:corpus/SOURCES.md'],capture_output=True,text=True).stdout
    out={}
    for l in t.split('\n'):
        m=re.match(r'\s*\|\s*(S\d{3,})\s*\|',l)
        if m:
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            out[m.group(1)]=dict(zip(['id','source','kind','tier','scope','anchor','teaches','status','opened','recheck','used-by'],c))
    return out
b=rows('922a4dde90b60b465e2b8b241d1fe363f1f27e98'); h=rows('HEAD')
print('added:',[k for k in h if k not in b])                      # S028 S029 S030 S031
print('changed:',[(k,c) for k in h if k in b for c in b[k] if b[k][c]!=h[k][c]])  # S018.status, S018.used-by
```

## Result

Two HIGH (F1: Gate row missing for a new row; F2: stale `used-by` with no old→new log), four
MEDIUM (F3, F4, F5, F9), three LOW (F6, F7, F8). The four named rows' URL/date/quote/location cells
are otherwise correct and byte-checkable except where noted; the transition ledger is where the
Gate record is materially wrong. No production file was modified; no commit, push, or index change
was made; nothing here is an admission or a score claim.
