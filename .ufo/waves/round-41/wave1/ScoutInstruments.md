# ScoutInstruments — receipt (kasegi-shokunin round 41, wave 1)

Seat: ScoutInstruments (leaf, write-scope: this receipt + ScoutInstruments.txt only).
Assignment: inventory the C2 instrument chain (source-recheck.py, capture-binding-check.py,
frontier-recheck-count.py, recheck-audit.py) with exact CLI shapes and current base
outputs; run each on the base tree; flag F24-integration assumptions.

## Method / base of record

- Lane HEAD b3b08b2; claims-freeze fbba3d9; base 5b29ea1439450b712581edf5f0f0bf98dfb262ab
  (40-char hash per claims.json erratum 1 — the dispatch prompt's literal was 38 chars and
  unresolvable; `git rev-parse 5b29ea1` resolves to the 40-char value above, prefix 5b29ea14).
- `git diff 5b29ea1 b3b08b2 -- corpus/` and `git diff fbba3d9 b3b08b2 -- corpus/` are both
  EMPTY: corpus/ is byte-identical across base, freeze and wave-1 HEAD. Lane-tree runs below
  ARE the base-tree outputs.
- Cross-check: base tree exported to scratch via
  `git -C <lane> archive 5b29ea1439450b712581edf5f0f0bf98dfb262ab | tar -x` and re-run:
  - capture-binding-check.py on the export: output byte-identical to the lane run.
  - source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json on the
    export: `diff` vs lane run = BYTE-IDENTICAL.
  frontier-recheck-count.py and recheck-audit.py were run on the lane tree only: 58/59 base
  recheck lines `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` absolutely, so an export
  run still measures the lane (cdroot limb), which would be a misleading "base" number.
- Disk guard was green before every run. No tools installed/upgraded this seat.
- No mutating git/jj commands anywhere; no lane/fleet files touched. Scratch:
  /fast/scratch/hyaku/kasegi-r41/ScoutInstruments (removed at yield).

## Deliverable

- `.ufo/waves/round-41/wave1/ScoutInstruments.txt` — the landable inventory
  (per-instrument CLI + semantics + base outputs summary + 13 F24 risk flags F1–F13).

## Base outputs (verbatim)

### 1. source-recheck.py
Run: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json`
```
S016:sha256 OK
S016:Q1 OK occurrences=1 anchor=17-ok
S016:Q2 OK occurrences=1 anchor=16-ok
S016:Q3 OK occurrences=1 anchor=12-ok
S017:sha256 OK
S017:Q1 OK occurrences=1 anchor=23-ok
S017:Q2 OK occurrences=1 anchor=34-ok
S017:Q3 OK occurrences=1 anchor=34-ok
S019:sha256 OK
S019:Q1 OK occurrences=2 anchor=80-ok
S019:Q2 OK occurrences=2 anchor=80-ok
S019:Q3 OK occurrences=1 anchor=97-ok
S020:sha256 OK
S020:Q1 OK normalized=markup-whitespace occurrences=1 anchor=142-ok
S021:sha256 OK
S021:Q1 OK occurrences=1 anchor=133-ok
S023:sha256 OK
S023:Q1 OK occurrences=1 anchor=151-ok
S023:Q2 OK occurrences=1 anchor=154-ok
S025:sha256 OK
S025:Q1 OK normalized=markup-whitespace occurrences=1 anchor=32-ok
S025:Q2 OK normalized=markup-whitespace occurrences=1 anchor=507-ok
S060:sha256 OK
S060:Q1 OK occurrences=1 anchor=7-ok
S060:Q2 OK occurrences=1 anchor=15-ok
S060:Q3 OK occurrences=1 anchor=50-ok
exit=0
```
--selftest: `selftest cases=10 failures=0`, exit 0 (10 SELFTEST lines, all PASS).
Negative sample: `--source S062` on the round-40 manifest →
`S062:source UNAVAILABLE reason=not-listed`, exit 2 (S062 has no capture; registry row only).

### 2. capture-binding-check.py
Run: `python3 corpus/instruments/capture-binding-check.py` (lane; identical on base export)
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
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
AUDIT records=54 with_url=54 with_fetched_utc=16 with_archival=38 snapshot_dirs=16 manifest_dirs=16 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=54 bound=54 unbound=0
exit=0
```
--selftest: `selftest cases=23 failures=0`, exit 0.

### 3. frontier-recheck-count.py
Run: `python3 corpus/instruments/frontier-recheck-count.py`
```
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md        ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0
PASS     F23  knowledge/cyclonedx-analysis-subtree.md              ids=S060           exit=0
entries=26 pass=26 exit=0
exit=0
```
--selftest: `selftest cases=6 failures=0`, exit 0. --json receipt schema:
{kasegi-frontier-recheck-receipt-v1, root, entries, pass, duplicate_entry, records[]};
record keys: entry, frontier, title, declared_ids, evidence_declared_ids, cited_ids,
recheck_ids, manifest, realpath, exit, problems, status.

### 4. recheck-audit.py
Run: `python3 corpus/instruments/recheck-audit.py --quiet --json <scratch>/recheck-audit.json`
```
strict pass=59/59 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=35 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=59 total=59 pass=59 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=59 missing=0 unexpected=0 exit=0
exit=0
```
JSON receipt fields: instrument_sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09,
root=cdroot=/home/vgpnk/Projects/shokunin/kasegi-shokunin, foreign_cwd=/, lines=59,
total_knowledge_files=59, complete=True, pass=59, pass_strict=59, fail_closed=24,
executes_today=35, gated=24, broken=0, expect=present, expected_entries=59,
missing_entries=[], unexpected_entries=[].

### 5. Adjacent gate: sources-census.sh
Run: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

## Key findings / flags for the F24 integration (full list F1–F13 in the deliverable)

1. frontier `ids=` prints header `source:` ids ONLY — `PASS F24 ids=S063` needs a header
   line `source: S063` (also the exact shape of the counting command
   `grep -rlE '^source: S063' corpus/knowledge`).
2. README F24 row must start at column 0 (`grep -cE '^\| F[0-9]+ \|'`); status cell
   exactly `admitted`; registry status is the 8th cell (awk $9) and must be `mined`.
3. S063 row source cell: exactly one https token; manifest record `url` byte-equal
   (only `url` binds — `capture_url` is ignored by the binding rules).
4. round-41 dir must hold exactly manifest.json + S063.txt (extra files → orphan-capture
   FAIL unless declared in top-level `orphans`); fetched_utc strict UTC mandatory
   (round ≥ 32, archival exemption closed).
5. source-recheck B1: path stem == id; normalized quote ≥ 12 chars; non-unique quotes
   need a verifying integer anchor.
6. knowledge-expected.txt gains `corpus/knowledge/rfc-9116-security-txt.md` between
   lines 47 and 48 (sorted); audited gate expected=59 → 60.
7. F24 recheck line must be cwd-independent (absolute cd; 58/59 base lines use
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`) and satisfy the strict
   limbs (cdroot/instrument/own); the canonical `--manifest corpus/source-snapshots/round-41/manifest.json --source S063` shape satisfies `own`.
8. F24 entry realpath must be unique across rows (DUPLICATE-ENTRY fails the run).
9. Ordering is safe: os.walk sorts round-41 after round-40; records sorted by id;
   quotes sorted per record — but receipts must not assume manifest record order.
10. multi_row_url stays informational at 3 provided the S063 URL appears in no other
    registry row's source cell.
11. "measure 44/44 = 1.000" is NOT one of these four instruments — no `measure` script
    exists under scripts/ or scripts/hyaku/; it is an adjacent fleet-side gate outside
    this inventory's scope.

## Fidelity notes

- S062 (round-40 registry row) intentionally has no capture/manifest — manifests total
  54 records across 16 dirs while the registry has 62 rows; the 8 uncaptured rows are
  registry-only provenance rows. S063 must be captured+bound (records 54→55, bound→55).
- Base negative-control spotcheck: `--source S062` prints `reason=not-listed` exit 2 —
  matching the instrument's not-listed limb that F24's `--source S063` must not trip
  (manifest must list S063).
- Verbatim evidence files were staged in scratch during the run and are reproduced
  above; scratch removed before yield.

No blockers. All four instruments + census + three selftests exercised on the base state.
