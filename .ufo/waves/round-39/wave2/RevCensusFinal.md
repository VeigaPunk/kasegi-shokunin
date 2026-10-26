# RevCensusFinal — wave-2 falsify receipt (round 39)

Seat: RevCensusFinal (leaf, attack seat, non-author of the attacked work).
Dispatch: L1 KasegiR39, kasegi-shokunin round 39 wave 2 (falsify), hyaku run 9.
Date: 2026-10-26. Item: final non-author census + audit runs on the lane tree at
HEAD, verified against the frozen C2 predicates in `.ufo/waves/round-39/claims.json`
and `claims-erratum-1.md` (E1 registry after-count 59; E5 non-vacuous semantics).

## Ground state

- Lane HEAD: `5006097a84305267c9a3e8c1e1d560e60fe41d37` (receipt Y; parent
  `46c66c2` = content head). Claims-freeze commit `dcd3170…` and base `480b1a50…`
  both present in history.
- Tracked working tree == HEAD: `git status --porcelain` = 5 entries, all
  untracked wave-2 artifacts (`.ufo/waves/round-39/wave2*`, `wave2-run.err`,
  `falsify.ready*`); `diff -r` of a `git archive HEAD` extraction vs the working
  `corpus/` shows only two git-ignored artifacts (`corpus/instruments/__pycache__/`,
  mtimes 02:35–03:32 -03:00; `corpus/instruments/r35-fixtures/D4/.ufo/waves/round-34/wave1-results.json`)
  — both pre-date this seat's session (scratch dir created 17:31) and neither
  enters any counted predicate. So every run below measured the LANDED bytes.
- All four instruments were source-checked before running: read-only on the lane
  in normal mode (writes only under `--selftest` / `--json` / selftest scratch;
  capture-binding-check docstring: "writes nothing outside its scratch directory").

## 1. The four claimed instruments — actual output at HEAD

### 1.1 census (`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`)

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
rc=0
```

Matches the item expectation exactly: W04 S028/S029 only (pre-existing,
warnings do not affect a clean lane per the script's contract), exit 0, no new
W/E code.

### 1.2 recheck-audit (`python3 corpus/instruments/recheck-audit.py --quiet`, cwd = lane)

```
strict pass=51/51 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=27 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=51 total=51 pass=51 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=51 missing=0 unexpected=0 exit=0
rc=0
```

### 1.3 capture-binding-check (`python3 corpus/instruments/capture-binding-check.py`)

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=46 with_url=46 with_fetched_utc=8 with_archival=38 snapshot_dirs=15 manifest_dirs=15 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=46 bound=46 unbound=0
rc=0
```

(the single orphan `S040-live.txt` is manifest-declared — exit 0 per rule A2.)

### 1.4 frontier-recheck-count (`python3 corpus/instruments/frontier-recheck-count.py`)

25 `PASS` lines (F01–F22, F09/F10/F11 split rows), ending:

```
PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0
entries=25 pass=25 exit=0
rc=0
```

**All four greens match the frozen C2 predicates** (audit expected=51
missing=0 unexpected=0; binding 46/46; harness entries=25 pass=25; census exit 0
with no new W/E code).

## 2. Independent recounts (not through the instruments)

| predicate | frozen (as corrected) | measured | verdict |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 22 | 22 | hold |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **59 per E1** (58 as-frozen) | **59** | hold (E1 confirmed) |
| `ls corpus/knowledge/*.md \| wc -l` | 51 | 51 | hold |
| `knowledge-expected.txt` entries (non-comment) | 51 | 51 | hold |
| `grep -rlE '^source: S057' corpus/knowledge \| wc -l` | 1 | 1 | hold |
| S057 row NF | 13 | 13 (11 columns) | hold |
| S057 status / tier / kind / opened | mined / A / docs / 2026-10-26 | same | hold |
| S057 source cell URL | exactly `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information` | exact | hold (E5.9) |
| S056/S058/S059 | `status rejected` + `flip:` in teaches | all three: col9=rejected, `flip:` present (SOURCES.md L63–L65) | hold |
| F22 row admits | entry `knowledge/cisa-when-to-issue-vex.md`, sources S057 | README.md L506: `admitted \| knowledge/cisa-when-to-issue-vex.md \| S057` | hold |
| S057 entry body | ≥ 10 lines beyond provenance trio | 144 lines total | hold |
| registry arithmetic (E3) | 55 base + S056/S057/S058/S059 = 59 | 59 rows, S057 at L62, S056/S058/S059 at L63–L65, no dup ids (binding B2 passed) | hold |

The as-frozen C2 number `registry 58` is the E1 arithmetic slip; the landed bytes
carry 59 and E1's reading (`registry != 59` kill) is the one the tree satisfies.

## 3. Non-vacuity probes (E5 semantics: do the greens discriminate?)

Workspace: `git archive HEAD` of the lane extracted to scratch (byte-identical
tracked corpus, `diff -r` verified); mutations applied only in scratch.

- **P1 — audit expect-set (rename entry):** `mv corpus/knowledge/cisa-when-to-issue-vex.md → zz-renamed.md`, rerun audit (`--root <copy> --cdroot <lane>` to isolate the limb):
  `missing=corpus/knowledge/cisa-when-to-issue-vex.md` / `unexpected=corpus/knowledge/zz-renamed.md`,
  `expect=present expected=51 missing=1 unexpected=1 exit=1`, rc=1. The green
  `missing=0 unexpected=0` is a live set-equality check, not decoration.
- **P2 — binding (manifest URL drift):** S057 record `url` → `https://example.invalid/…`:
  `FAIL rule=url-mismatch record=S057 row=S057 dir=round-39`, `records=46 bound=45 unbound=1`, rc=1. Discriminates.
- **P3 — frontier harness (misbound source):** entry recheck `--source S057` → `--source S056`:
  `FAIL F22 knowledge/cisa-when-to-issue-vex.md ids=S057 exit=- problems=header-sources-not-rechecked,selection-not-declared-by-entry,selection-not-cited-by-entry,manifest-missing-ids`,
  `entries=25 pass=24 exit=1`, rc=1. Discriminates.
- **P4 — census (invalid status):** S057 status `mined` → `watch` in a single-lane
  fixture fleet: `kasegi E07 S057 status=watch`, rc=1; control with the unmutated
  full HEAD corpus: W04 S028/S029 only, `ok`, rc=0. Discriminates; E07 is the
  new code, W04-only stays the clean signature.

### P1b — precision note (no falsification, documented semantics)

The same `--source S056` misbinding leaves **recheck-audit green** (exit=0,
`pass=51/51`), with the mutated line reclassified `executes→gated`
(`executes=26 gated=25 fail-closed=25`). Source-verified: `audit_entry()` runs
every line against the root, but `pass` = form limbs only (parse/cwd/paths);
`lane_rc != 0` is the documented fail-closed class — "counts as passing its form
limbs and is reported separately, because the base it guards is absent"
(recheck-audit.py docstring), and the delta IS visible in the receipt
(`fail-closed` 24→25). The audit is a FORM verdict; it does not assert the
rechecks pass. Actual recheck success is carried by frontier-recheck-count
(`exit_code != 0 → problems`; all 25 lines `exit=0`) — which caught the same
mutation red. No frozen predicate claims otherwise (C2's audit command asserts
only `expected=51 missing=0 unexpected=0`), so this is a wording-precision note
for future freezes, not a defect: "audit green" must never be cited as "rechecks
pass". 24 of 51 lines never exit 0 on the real lane (absent base) by design.

## 4. Findings

Severity: none — no actionable defect found in the landed bytes bearing on this
item. All four instrument greens reproduce at HEAD; all independent recounts
match the frozen predicates as corrected by erratum E1; every instrument proven
non-vacuous by mutation (P1, P2, P3, P4).

Residual risk / observations:

1. recheck-audit's fail-closed pass semantics (P1b above) make "audit expected=51
   exit=0" a form claim only; keep frontier-recheck-count as the success claim.
2. Two pre-existing git-ignored artifacts under `corpus/instruments/` (see
   §Ground state) — inert, no predicate touches them; left untouched.
3. The E11 flood seen in the minimal P4 fixture (control run before the full-corpus
   fix) is fixture minimalism (used-by paths absent from the fixture), not a lane
   property; the full-corpus control is clean.

## Tooling

No tools installed or upgraded (none needed). Read-only git only
(`rev-parse`, `status`, `log`, `show`, `archive`); no mutating git/jj anywhere;
no network fetches; no writes outside this receipt and scratch
`/fast/scratch/hyaku/kasegi-r39/RevCensusFinal/` (removed after this receipt was
written). Disk guard green throughout (617G free).
