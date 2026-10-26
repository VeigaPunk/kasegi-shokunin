# ConnClaims — cross-claim pattern check, round 33 (wave 1)

Seat: ConnClaims (leaf). Model run on: kimi-code/kimi-for-coding (config route table; no model passed).
Scope: pattern check of `.ufo/waves/round-33/claims.json` only. No lane bytes edited by this seat.
State note (bound 6): seats were mid-flight while this check ran (ExecCaptureBinding,
ExecManifestUpgrade, ExecManifest32 had landed; ExecRegistryAppend / ExecEntryF16 /
ScribeScorecard had not). Every counter number cited below is labeled MID-FLIGHT or
PRE-STATE and is evidence of emission only, not of the after-column. The after-numbers
belong to the claim seats' receipts on quiescent bytes.

## Check matrix (per claim)

| # | Check | C1 verdict | C2 verdict |
|---|-------|-----------|-----------|
| 1 | Predicate ≡ counter semantics ≡ receipt label scheme | PASS with one erratum-narrowed clause + one uncovered conjunct (below) | PASS for numeric clauses; three reviewer clauses outside counter semantics (below) |
| 2 | Kill rule names a failing control receipt | PASS (names fake-checker.py in c1-controls; both receipts exist) | PASS via do_nothing_control only (asymmetry, below) |
| 3 | Every counter parses (`bash -n`) and emits its number | PASS (3/3 parse; 3/3 emit) | PASS (9/9 parse; 9/9 emit) |
| 4 | C1/C2 causally separable | PASS (shared files listed; field-disjoint) | PASS (same) |
| 5 | Fake-checker kill clause | PASS (clause coherent; real/fake boundary verified) | n/a (C2's analog is the junk-row control, prose-only, no receipt) |

---

## C1 — depth:verifiability

### Check 1 — predicate ≡ counters ≡ labels

Predicate clauses vs counter semantics (cmd1–cmd3 of claims.json C1):

- `records=40 bound=40 unbound=0` + exit 0 → cmd1 runs the instrument; cmd's echo
  label `binding_exit=$?` matches the receipt label scheme the INTERFACE CONTRACT prints.
- `--selftest` prints failures=0, exit 0 → cmd2; label `selftest_exit=$?`.
- "every snapshot directory carries a manifest" → rule A inside cmd1's instrument
  (cmd3's `*/manifest.json` glob alone cannot see a manifest-less dir; rule A and the
  `missing-manifest-dir` selftest case carry it).
- "two round-32 records carry fetched_utc; 38 pre-round-32 records carry archival: true"
  → cmd3 prints per-dir `fetched=` / `archival=` (MID-FLIGHT run: 38 archival across
  rounds 23–31; round-32 fetched=2 archival=0 — matches contract rule C).
- "capability `capture-binding-check` enters the SCORECARD capabilities table" →
  **no counter command covers this and C1's kill rule does not name it.** The
  predicate asserts a conjunct the claim's own apparatus cannot fail. Mitigation is
  external: ScribeScorecard (append-only SCORECARD.md) had not landed at check time
  (`grep -i capture-binding SCORECARD.md` → no line). Flagged, not smoothed.

Receipt label scheme, INTERFACE CONTRACT vs instrument (MID-FLIGHT run of the landed
`corpus/instruments/capture-binding-check.py`, md5 da280392ce1074ab6c2ad219fe2fcd4a at read time):

- Contract: `MANIFEST <round> records=N url_bound=M fetched=K archival=L` →
  emitted: `MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4` … byte-shape exact.
- Contract summary `records=<total> bound=<total> unbound=0` → emitted (failure shape):
  `records=40 bound=38 unbound=2` — same label scheme, computed values.
- Contract `selftest cases=N failures=F` → emitted: `selftest cases=9 failures=0`
  (9 cases ≥ the 6 required; all six required case names present:
  clean-all-pass, missing-manifest-dir, record-without-url, url-matching-two-rows,
  round-32-record-without-fetched_utc, pre-round-32-record-without-archival;
  plus url-not-in-registry and two pass-shapes).
- Contract scratch discipline (`$HYAKU_SCRATCH` default /fast/scratch/hyaku, deleted at
  exit) → implemented: `scratch_base()` order --scratch → $HYAKU_SCRATCH → $TMPDIR →
  platform temp; `shutil.rmtree(scratch, ignore_errors=True)` in `finally`.

**Erratum-narrowed clause (contradiction stated, not smoothed):** the frozen kill rule's
rule-B clause — "any record's `url` matches zero or two+ registry-row URLs … = failure"
(global URL-text reading) — is jointly unsatisfiable with C2's frozen requirement that the
W04 duplicate-URL pairs remain in the registry (S024/S029 eur-lex; S006/S028 HackerOne).
Under the global reading, S006 and S029 could never bind, so `bound=40 unbound=0` would be
unreachable without touching immutable registry rows. Resolution on record:
`.ufo/waves/round-33/claims-erratum-1.md` (L1 ruling filed before any measurement, citing
ScoutManifestAudit §4) re-scopes rule B to id-scoped binding (no-row / dup-id / url-mismatch
against the record's OWN row; cross-row duplicate URLs informational via `multi_row_url=N`).
The instrument implements exactly this; its docstring names the erratum. Verdict: the
predicate's `unbound=0` target is reachable only under erratum-1 semantics; the erratum
leaves predicate, counters, kill rule and 40/40/0 target text unchanged, so the pattern
holds with the erratum as an appended correction file — the sanctioned correction path.

### Check 2 — kill rule names a failing control receipt

Kill rule names "a fake checker (fake-checker.py in c1-controls)". Both artifacts exist:
`c1-controls/before.txt` (base audit: ls_exit=2; 38 records, with_url=0, with_fetched_utc=0;
round-32 dir manifest-less; source-recheck exit 2) and `c1-controls/fake-checker-receipt.txt`
(fake prints `records=38 bound=38 unbound=0`, fake_exit=0, no validation). PASS.

### Check 3 — parse + emission

- `bash -n` on cmd1–cmd3: all exit 0.
- Emission (MID-FLAG, labeled): cmd1 → 9 MANIFEST lines + AUDIT + FAILs + summary +
  binding_exit=1 (unbound = S049/S050 no-row pending ExecRegistryAppend; multi_row_url=2
  informational per erratum). cmd3 → per-dir records/url/fetched/archival for all 9 dirs.
  cmd2 (`--selftest`) → `selftest cases=9 failures=0`, selftest_exit=0. Each emits the
  number its predicate clause claims.

### Check 4 — causal separability

C1 reads: `corpus/instruments/capture-binding-check.py`, every
`corpus/source-snapshots/*/manifest.json`, and `corpus/SOURCES.md` (registry source cells
only). C1 never reads `corpus/README.md` or `corpus/knowledge/*`, so its counters do not
depend on the F16 row, the entry, or QUALITY rows. C1's `bound=40` does require the
S049/S050 registry ROWS to exist with byte-exact URLs (ExecRegistryAppend) — file-coupled
to C2's surface, field-disjoint from C2's measurements. The erratum itself is the evidence
of this coupling: rule-B semantics had to be reconciled with registry bytes C2 freezes.

### Check 5 — fake-checker kill clause

Clause: "the real checker must exit 1 on the base bytes and name unbound records, never
print bound=N when the records carry no url."
- Never-print-bound-without-url: `bound` counts only records passing rules B AND C
  (`if url_ok and prov_ok: totals["bound"] += 1`); a record with no `url` yields
  `rule=url-mismatch … detail=absent` and cannot count bound. Selftest case
  `record-without-url` pins exit 1 for exactly that fixture.
- Exit 1 on base bytes naming records: base manifests carry 38 records with no url →
  every record fails B → exit 1 with one FAIL line per record (before.txt documents the
  base state; do-nothing control consistent).
- Fake fails the clause: fake-checker.py counts only `len(sources)` and prints
  `bound=records` with zero validation, exit 0 — rejected by the kill rule; the
  demonstrating receipt exists (fake-checker-receipt.txt).
- Boundary nuance: on the true base commit the instrument is absent (ls exit 2,
  before.txt); the testable content of the clause is the checker's behavior on base
  manifest bytes, which the selftest fixture + do-nothing control jointly demonstrate.
  The clause is coherent and the real/fake boundary is well-posed. PASS.

**C1 verdict: PATTERN HOLDS**, subject to (a) erratum-1 standing as the recorded
correction for the rule-B clause, and (b) the SCORECARD capability conjunct being
verified outside the claim's own apparatus (ScribeScorecard receipt / report), since no
frozen counter or kill-rule clause can fail it.

---

## C2 — coverage

### Check 1 — predicate ≡ counters ≡ labels

Numeric clauses map 1:1 to cmd1–cmd9:

- frontier admitted 15→16 → cmd1 (awk over README frontier rows: `$2 ~ /^ *F[0-9]+ /`,
  `$4 ~ /^ *admitted *$/`; PRE-STATE run emitted 15; README rows confirmed
  `| F01 | … | admitted | … |` shape).
- exactly 1 entry cites S049 / S050 on `source:` lines → cmd2 (`grep -lE '^source: S049 '`).
  Entry convention verified on landed multi-source entries: one `source: Sxxx — url — note`
  line per source (e.g. statutory entry has separate S033/S034/S035 lines), so the F16
  entry's two source: lines each match exactly one grep; semantics hold.
- S049/S050 rows exactly once; registry 48→50 → cmd3–cmd5 (PRE-STATE: 0/0/48; emitted).
- census exit 0, no new E/W beyond W04 S028/S029 → cmd6 (PRE-STATE run: W04×2 + ok line,
  census_exit=0; matches do_nothing_control exactly).
- harness entries=19 pass=19 exit=0 incl. `PASS F16 ids=S049,S050` → cmd7 (PRE-STATE run:
  entries=18 pass=18 exit=0 — F16 row/entry not yet landed; label format `PASS F16 …
  ids=S049,S050` matches the harness's existing row format).
- source-recheck S049/S050 exit 0 on round-32 manifest → cmd8/cmd9 (MID-FLIGHT run on the
  landed manifest: sha256 OK + Q1..Q8 / Q1..Q6 all OK occurrences=1; recheck49_exit=0,
  recheck50_exit=0 — emitted the labels the kill rule names: "any assertion not
  exactly-once-or-anchored" fails; all assertions exactly-once here).

Reviewer clauses in the predicate — "passes QUALITY Q1-Q10 under a non-author reviewer",
"names CNVD and 360SRC as stating parties (Q4)", "not a restatement of F13/F14/F15 or the
refused staged entries (sweep command)" — are enforced by named reviewer seats
(CloseKotobaR74.C2SiblingRecheck / C1SpecRecheck on the roster), not by the printed
counter commands. Same structural shape as C1's SCORECARD conjunct, but C2's kill rule
DOES name these clauses, so the claim's own apparatus can fail them. C2's kill rule is a
superset of its counter-command semantics; C1's is not (see C1 check 1).

### Check 2 — kill rule names a failing control receipt

C2's kill rule sentence names no receipt path inline (asymmetry vs C1, which names
fake-checker.py inside the kill rule). The claim's `do_nothing_control` names
`.ufo/waves/round-33/c2-controls/before.txt`, which exists and shows every base number
(frontier 15; entries 0/0; rows 0/0/48; census exit 0 W04×2; harness 18/18; recheck exit 2).
The junk-row control is described only in prose inside claims.json — `c2-controls/`
contains no junk-row receipt. PASS via do_nothing_control; asymmetry recorded.

### Check 3 — parse + emission

- `bash -n` on cmd1–cmd9: all exit 0.
- Emission demonstrated for all nine (PRE-STATE/MID-FLIGHT labels above). Each emits the
  number its clause claims; cmd8/cmd9 emit the per-assertion `OK occurrences=1` lines the
  kill rule's "exactly-once-or-anchored" clause reads.

### Check 4 — causal separability

C2 reads `corpus/README.md` (cmd1), `corpus/knowledge/*` (cmd2), `corpus/SOURCES.md`
(cmd3–cmd5, census), `corpus/instruments/frontier-recheck-count.py` + entry recheck lines
(cmd7), `corpus/instruments/source-recheck.py` + captures (cmd8/cmd9), and
`corpus/source-snapshots/round-32/manifest.json` (cmd8/cmd9). Verified field-independence
from C1's measured fields: `grep url|fetched|archival corpus/instruments/source-recheck.py`
→ zero matches (it reads id/path/sha256/quotes/anchors only);
`frontier-recheck-count.py` reads only record `id`s from manifests (`manifest_ids`);
census reads SOURCES.md only. So C2's counters cannot move when C1's url/fetched_utc/archival
fields change, and C1's counters cannot move when the F16 README row or entry changes.
Shared files and coupling stated above (SOURCES.md; round-32 manifest). PASS.

### Check 5 — fake-checker kill clause

C1-specific. C2's structural analog — the junk-row control ("a bare S049/S050 registry row
with no entry and no capture … cannot meet the target") — is asserted in prose with no
committed receipt at freeze time; it is a described control, not a receipted one. Recorded
under check 2's asymmetry.

**C2 verdict: PATTERN HOLDS** — numeric clauses are 1:1 with counters whose labels match
the predicate; reviewer clauses are kill-rule-enforced via named reviewers; the only
soft spots are the inline-receipt asymmetry (check 2) and the prose-only junk-row control,
neither of which weakens a measured clause.

---

## Commands exercised (all read-only; lane not written)

1. `bash -n` over each counter command string extracted from claims.json → 12/12 exit 0.
2. C1 counters: instrument run + `--selftest` + per-dir manifest audit → labels above.
3. C2 counters: awk frontier count; two `grep -lE '^source: S0(49|50) '`; three row greps;
   `scripts/sources-census.sh validate`; `frontier-recheck-count.py`;
   `source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049/S050`.
4. `grep -n "rejected|status|registry…"`, `sed -n` reads of the landed instrument;
   `grep url|fetched|archival` over source-recheck.py / frontier-recheck-count.py.
5. Read of `.ufo/waves/round-33/claims-erratum-1.md`, `c1-controls/before.txt`,
   `c1-controls/fake-checker.py`, `c1-controls/fake-checker-receipt.txt`,
   `c2-controls/before.txt`, `census-before.txt`.
6. `grep -i capture-binding SCORECARD.md` → no line at check time (ScribeScorecard pending).

## Cross-claim summary

- Frozen-claims contradiction found and already repaired on-record: C1's global rule-B
  reading vs C2's frozen W04 duplicates → `claims-erratum-1.md` (id-scoped binding;
  predicate/counters/targets unchanged). Both claims' measured targets remain reachable.
- One unenforced predicate conjunct: C1's SCORECARD capability line has no counter and no
  kill-rule clause; it depends on ScribeScorecard landing and the report citing it.
- One asymmetry: C2's kill rule names no control receipt inline; C1's does.
- C1/C2 are causally separable: two shared files (SOURCES.md; round-32 manifest.json),
  measurements field-disjoint in both directions; the erratum is the visible scar of the
  file-level coupling and is exactly the sanctioned appended-correction form.
- All 12 counter commands parse and emit; no counter's emission was faked or assumed.
