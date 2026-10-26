# RevClaimsFreeze — round 33 wave 1 (claims-falsification seat)

Seat: RevClaimsFreeze · 2026-10-26 · answering model: devin/glm-5-3-flash-1m.
Scope: falsify the frozen claims in `.ufo/waves/round-33/claims.json` before data. Read: claims.json, `c1-controls/*`, `c2-controls/before.txt`, prompt `kasegi-round-33.md` §2 (lines 9-41) and §9 (lines 439-458). Lane base `690b69da`; freeze commit `6e55c8d`.
Scratch: all fixtures under `/fast/scratch/hyaku/kasegi-r33/RevClaimsFreeze/` (base tree = `git archive 690b69da`, read-only git only); removed before yield; decisive outputs are quoted below.

**State label (bound 6).** The lane was mid-landing during every lane-bytes run below (instrument rewritten to erratum-1 semantics at 01:19:52Z during my first driver run; S049/S050 registry rows and the SCORECARD capability row still absent at 04:23:09Z — measured `grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md` → `0`, `grep -c capture-binding-check SCORECARD.md` → `0`). Lane-bytes numbers here are IN-FLIGHT/PRE-STATE and never compared to an after column. Base-bytes runs are on git-frozen bytes (citable). Re-run before citing any after-number: the frozen counter commands of claims.json C1/C2, verbatim, on quiescent bytes.

---

## Attack 1 — is C1's target reachable by a do-nothing control?

**Verdict: NO.** The control is rejected by the kill rule's fake-checker clause, and the rejection is demonstrated on git-frozen base bytes.

```
$ git archive 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 | tar -x -C $S/base
$ ls $S/base/corpus/instruments/capture-binding-check.py   # instrument absent on base
ls: cannot access ...: No such file or directory
$ python3 .ufo/waves/round-33/c1-controls/fake-checker.py --root $S/base
records=38 bound=38 unbound=0
fake_on_base_exit=0
$ python3 corpus/instruments/capture-binding-check.py --root $S/base   # erratum-semantics instrument
AUDIT records=38 with_url=0 with_fetched_utc=0 with_archival=0 snapshot_dirs=9 manifest_dirs=8 missing_manifest=1 multi_row_url=0
FAIL rule=missing-manifest dir=round-32
FAIL rule=url-mismatch record=S018 detail=absent dir=round-23
... (38 records named: url-mismatch detail=absent + provenance-missing each)
records=38 bound=0 unbound=38
real_on_base_exit=1
```

Kill-rule clause that rejects the fake: *"the real checker must exit 1 on the base bytes and name unbound records, never print bound=N when the records carry no url."* On base bytes all 38 records carry no `url` (c1-controls/before.txt: `TOTAL records=38 with_url=0`), so the fake's `bound=38` is a false bound; the real checker exits 1 and names all 38.

**Residual the closure must know:** on the LANE bytes the fake prints the exact target summary — in-flight run: `python3 .ufo/waves/round-33/c1-controls/fake-checker.py --root .` → `records=40 bound=40 unbound=0`, `fake_on_lane_exit=0`. Counter command 1's lane output alone therefore cannot exclude a do-nothing control; the exclusion lives entirely in the base-bytes clause. Any C1 closure that cites only the lane-bytes summary is citing a non-discriminating observation; the closure must also cite the base-bytes run (a PRE-STATE run on frozen bytes by construction — label it so).

### Second cheap control (half-checker: rules A+C, no url/registry check)

Built by deleting `bind_record`'s url/registry block (`return True, []` in its place) from a copy of the landed instrument.

```
$ python3 $S/half-checker.py --root $S/base          # base bytes
AUDIT records=38 ... missing_manifest=1 ...
FAIL rule=missing-manifest dir=round-32
records=38 bound=0 unbound=38
exit=1                                                  # agrees with the real checker
$ python3 $S/half-checker.py --root $S/fix-url-unknown  # record url matches no registry row
records=1 bound=1 unbound=0
exit=0                                                  # contradicts the kill rule's B-clause
$ python3 $S/half-checker.py --root $S/fix-url-empty    # record S002 carries no url
records=2 bound=2 unbound=0
exit=0                                                  # contradicts "every manifest record has a url"
$ python3 $S/half-checker.py --selftest
selftest problem=exit=0 want=1 case=record-without-url
selftest problem=exit=0 want=1 case=url-mismatch
selftest cases=11 failures=2
exit=1                                                  # kill rule's selftest clause fires
```

**Which clause catches it:** NOT the base-bytes clause (on base it exits 1, agreeing with the real checker). It is caught by (i) the kill rule's selftest clause — `--selftest` prints failures=2 and exits 1, because the interface contract mandates the `record-without-url` and `url-mismatch` cases expecting exit 1 — and (ii) the kill rule's rule-B clause at fixture level (it prints `bound=1 unbound=0 exit 0` on a state the kill rule declares failing).

**Clause composition map** (no single clause catches the whole control family; the kill rule works as an ensemble, and the contract's mandated case list is what makes the selftest clause bite for partial controls):

| control | base-bytes clause | selftest clause | rule clause at fixture level |
|---|---|---|---|
| fake-checker (no validation) | catches (bound=38 false) | does NOT (cases=0 failures=0 exit 0) | n/a |
| half-checker (A+C, no B) | does NOT (agrees) | catches (failures=2) | B-clause catches |
| M1/M2/M3 (below) | does NOT | catches (failures=1 each) | B/C-clause catches |

### The four counter mutants (claims.json `mutants_of_the_counter`)

Each is a copy of the landed instrument with the named acceptance mutation; each was run with `--selftest` and on its matching fixture.

- **M1 accept-a-record-without-url** (`return False, [...detail=absent...]` → `return True, []`): `--selftest` → `selftest cases=11 failures=1` exit 1 (case `record-without-url`: `exit=0 want=1`); on the url-empty fixture prints `records=2 bound=2 unbound=0` exit 0 where the predicate requires every record to carry a url. **Fails the kill rule — caught.**
- **M2 accept-url-not-in-registry** (`if url not in row_tokens(own[0]):` → `if False:`): `--selftest` → `cases=11 failures=1` exit 1 (case `url-mismatch`); on the url-unknown fixture prints `records=1 bound=1 unbound=0` exit 0 where rule B (erratum: url-mismatch) requires failure. **Caught.**
- **M3 skip-fetched_utc-requirement** (`if round_no is None or round_no >= MODERN_ROUND:` → `if round_no is None:`): `--selftest` → `cases=11 failures=1` exit 1 (case `round-32-record-without-fetched_utc`); on the r32-nofetch fixture prints `records=1 bound=1 unbound=0` exit 0 where the kill rule requires "either round-32 record lacks `fetched_utc`" to fail. **Caught.**
- **M4 skip-selftest** (`return selftest(args.scratch)` → `print("selftest cases=9 failures=0"); return 0`): prints `selftest cases=9 failures=0` exit 0 **without running any fixture**. The kill rule's selftest clause as written ("`--selftest` prints any failure or exits non-zero") does **NOT** catch it — and the fake-checker itself prints `selftest cases=0 failures=0` exit 0 (measured). The only guards are the interface contract's ≥6-cases clause and the visible absence of per-case `selftest case=...` lines; neither is kill-rule text. **NOT caught — finding F-5.**

---

## Attack 2 — universal clauses without an enumerating command

§9: *"Use no universal clauses ('all', 'complete', 'every', 'no harm anywhere') unless the counting command enumerates the full set."*

| # | universal clause | enumerating mechanism | verdict |
|---|---|---|---|
| 1 | C1 "every snapshot directory carries a manifest" | checker rule A: `snapshot_dirs` enumerates every dir under `source-snapshots/` incl. manifest-less ones; `AUDIT ... snapshot_dirs=9 manifest_dirs=9 missing_manifest=0`; `FAIL rule=missing-manifest dir=<name>` | BACKED — but frozen counter command 3 (`for f in corpus/source-snapshots/*/manifest.json`) is blind to manifest-less dirs; the enumeration lives only in the checker's own output. A dir holding only subdirectories (no regular file) is not a snapshot dir by the checker's definition — edge, not exercised by current bytes. |
| 2 | C1 "every manifest record has a `url` that matches exactly one registry-row URL" | per-record FAIL naming + `AUDIT with_url=40` + `multi_row_url=2` | BACKED post-erratum-1 — the literal "exactly one" now reads through the erratum (own-row byte-equal; a URL shared with another row is informational). See erratum section. |
| 3 | C1 "the two round-32 records carry `fetched_utc`" / "the 38 pre-round-32 records carry `archival: true`" | counter command 3 per-manifest `fetched=`/`archival=` sums; `AUDIT with_fetched_utc=2 with_archival=38` | BACKED |
| 4 | C1 "`--selftest` prints failures=0 and exits 0" | counter command 2 | BACKED with the cases≥6 gap (M4/fake-checker print `failures=0` exit 0 without cases; finding F-5) |
| 5 | C1 "the capability `capture-binding-check` enters the SCORECARD capabilities table in the same round" | **NONE — no counter command, no kill-rule clause** | UNBACKED. PRE-STATE measured: `grep -c capture-binding-check SCORECARD.md` → `0`. Finding F-6: add a counter (e.g. `grep -c 'capture-binding-check' SCORECARD.md` ≥ 1) and a kill-rule clause. |
| 6 | C1 contract "The checker NEVER writes into the lane" | no frozen counter command | Demonstrated here by enumeration: sha256 snapshot of a scratch lane copy before/after a checker run — `diff nowrite-before.txt nowrite-after.txt` → empty (`NOWRITE-DIFF-EMPTY`); `--selftest` scratch leftover check → `[]`. Suggest adding a before/after `git status --porcelain` (or hash) enumeration to the counter set. Finding F-7 (minor). |
| 7 | C2 "exactly 1 knowledge entry cites S049/S050" | `grep -lE '^source: S049 '` over `corpus/knowledge/*.md` (full set) | BACKED |
| 8 | C2 "S049/S050 rows exactly once" / "registry rows 48→50" | `grep -cE` over the full registry | BACKED |
| 9 | C2 "census exits 0 with no new E/W finding beyond base W04 S028/S029" | census enumerates every finding; diff vs frozen `c2-controls/before.txt` | BACKED (bare-row control confirmed below: new W03 x2 fires the clause) |
| 10 | C2 "harness entries=19 pass=19 exit=0 incl. `PASS F16 ids=S049,S050`" | harness enumerates every admitted row | BACKED |
| 11 | C2 "source-recheck exits 0 for both" | counters 8/9 | BACKED |
| 12 | C2 "the entry passes QUALITY Q1-Q10 under a non-author reviewer" (+ the Q4 stating-parties and non-restatement clauses) | **not a counting command — a reviewer-judged checklist** | The only stop for the junk+empty-entry commit (attack 3). Disclosed in the kill rule, so not a letter violation; but the closure MUST cite the non-author reviewer's per-Q receipt, and no receipt may cite the mechanical counters alone as the C2 proof. |

---

## Attack 3 — can a junk-row + empty-entry commit meet any counter?

**Verdict: YES — it meets every mechanical C2 counter; it is stopped only by the non-mechanical reviewer clauses.** The frozen `do_nothing_control` considered only a bare row with no entry; the empty-entry variant is the escape it did not consider.

Fixture: base bytes + junk S049/S050 rows inserted inside `## Registry` (11-column shape, `used-by` → the empty entry, so no W03) + junk F16 admitted row appended to README + an empty entry (`# title`, two `source:` lines, one `recheck:` line invoking source-recheck on the round-32 manifest) + the real round-32 captures/manifest copied in. Every frozen C2 counter command run against it:

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
16                                                    # target 16 ✓
$ echo -n 'S049='; grep -lE '^source: S049 ' corpus/knowledge/*.md | wc -l; ...
S049=1
S050=1                                                # target 1/1 ✓ (empty entry)
$ grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md   # → 1 ✓ (S050 → 1 ✓)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
50                                                    # target 50 ✓
$ sources-census.sh validate <junk-lane>
junk-lane	W04	S028 duplicate url docs.hackerone.com/... across scopes
junk-lane	W04	S029 duplicate url eur-lex.europa.eu/... across scopes
junk-lane	ok	.../junk-lane/corpus/SOURCES.md
census_exit=0                                         # no NEW finding ✓
$ python3 corpus/instruments/frontier-recheck-count.py
...
PASS     F16  knowledge/junk-empty-f16.md                          ids=S049,S050      exit=0
entries=19 pass=19 exit=0
harness_exit=0                                        # target 19/19 ✓ — the EMPTY entry passes
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
S049:sha256 OK / S049:Q1..Q8 OK occurrences=1
recheck49_exit=0                                      # (S050 likewise) ✓
```

The claims' own bare-row control IS confirmed: with `used-by —` and no entry, the census prints `W03 S049 mined but unused` / `W03 S050 mined but unused` — new E/W findings beyond the base W04 x2, so the kill rule's census clause fires. The empty-entry variant evades W03 by pointing `used-by` at the (empty) entry, which also satisfies E11 (used-by path exists).

**Fabricated-capture variant (stronger form):** captures + manifest authored by the committer (self-chosen text, quotes drawn from it, correct sha256, `fetched_utc` self-asserted) also pass: harness `entries=19 pass=19 exit=0`, source-recheck `S049:sha256 OK / S049:S049-q1 OK occurrences=1 / recheck49_exit=0`. The mechanical chain verifies internal consistency only — capture↔manifest↔registry **text** — never capture↔upstream truth. That is consistent with C1's own surface sentence ("the registry-documented URL" = internal binding); the external-truth guards are the documentation-only fetch discipline, Q3/Q6 and the non-author reviewer, all outside the counters. Observation, no rule change implied.

**What actually stops junk+empty-entry:** the kill-rule clauses *"the entry fails any QUALITY.md Q1-Q10 under the non-author reviewer"* (an empty entry fails Q1 — no `verified-at:`/anchor header; Q3 — no ≤25-word verbatim quotes; Q4 — no attribution; Q5 — no falsifiable rule) and *"the entry does not name CNVD and 360SRC as the stating parties for every platform claim (Q4)"*. Both are reviewer clauses. Consequence for the round's closure: the C2 proof must cite the non-author reviewer receipt; the nine mechanical counters are necessary, never sufficient.

---

## Attack 4 — is C1's 'verifiability' axis name the surface the round changes?

**Verdict: YES.**

- §9: *"Name the axis by the surface the round changes, not by the number it produces."* The surface sentence names a property, not a number: captures become **verifiable** — bindable, from committed bytes alone, to the registry-documented URL and to fetch provenance, audited by a committed instrument. `depth:verifiability` names exactly that property.
- Not the kaidoku-r29 trap cases: it is not re-scoring a rule the lane already holds on new inputs (the instrument is new — a capability acquisition per §2.6), and it does not count rows a sourceless fixture also counts (rule B binds against the real registry).
- Depth vs coverage: the round deepens the hold on **existing** capture bytes (rounds 23-32); no new frontier ground is staked, so depth is the right family, and it works the lowest non-retired axis (4) as §2.2 requires.
- Disclosure note: the axis's r15-r32 operationalization was citation resolvability (`resolve.py`/`anchorcheck.py` percentages, SCORECARD line 33/66); round 33 moves the same property family through a different instrument on a different byte surface. The SCORECARD row should say which surface moved — the capabilities row plus the claim row do. No defect.

---

## Erratum-1 assessment (L1 request, replied to KasegiR33)

**Verdict: interface clarification, permissible — not a rule change under the fleet's own timing rule.**

1. Filed pre-scoring (erratum mtime 01:18:23Z; no wave1 receipt had scored) — the kumitate-r42 bar ("a rule changed after any seat has scored is not the claim's rule") is met.
2. Target `40/40/0`, counters, and exit codes unchanged; only Rule B's matching semantics are redefined (own-row lookup, byte-equal URL, `no-row`/`dup-id` failures, `multi_row_url` informational).
3. The frozen global reading made the frozen target **unreachable on immutable R8 rows**: record S029 (round-23 manifest) and record S006 (round-24 manifest) carry URLs present in two registry rows each (S024/S029, S006/S028 — measured at SOURCES.md lines 12/34 and 30/35). The frozen clause was defective; the erratum repairs it.
4. Net-tightening: byte-equal URL + `no-row`/`dup-id` are stricter than substring-any-row; the single relaxation (multi-row URL informational) is exactly the unreachable clause. The fake-checker clause and all four mutants survive: base bytes carry no url fields at all, and url-not-in-registry remains a failure as `url-mismatch`.

Caveats recorded for the L1:
- (a) The instrument landed at 01:18:05Z implementing the pre-erratum global semantics and was rewritten at 01:19:52Z (measured: pre-rewrite run printed `FAIL rule=url-ambiguous record=S029 rows=S024,S029`; post-rewrite run prints `multi_row_url=2` with S029/S006 binding). Selftest now 11 cases, `cases=11 failures=0` exit 0, scratch cleaned (`leftover: []`).
- (b) The predicate's literal words "matches exactly one registry-row URL" now read through the erratum; receipts must cite erratum-1 alongside the predicate.
- (c) The new QUALITY criterion R20 carries the same global phrasing ("a `url` matching exactly one `corpus/SOURCES.md` registry-r…") — ScribeQuality should word R20 through the erratum or it will contradict the instrument's behavior on the landed bytes.
- (d) Naming nit: selftest case `url-matching-two-rows` survives from the frozen contract's case list but now builds a **dup-id** fixture (two rows with the same id, `FAIL rule=dup-id record=S001 rows=2`); the erratum's actual multi-row-URL semantics live in the new `shared-url-not-a-failure` case. The name no longer describes its content.

---

## Findings summary (routed as appended corrections; the L1 decides; claims.json not edited)

- **F-1 (attack 3, main):** junk-row + empty-entry meets all nine mechanical C2 counters (demonstrated); the stop is exclusively the non-mechanical reviewer clauses. The frozen `do_nothing_control` considered only the bare row. Closure requirement: cite the non-author reviewer receipt as the C2 clause evidence.
- **F-2 (attack 3):** fabricated-capture variant passes the whole mechanical chain — the counters verify internal consistency, never capture↔upstream truth; `fetched_utc` is self-asserted. Consistent with C1's surface; no rule change implied.
- **F-3 (attack 1):** on lane bytes the fake-checker prints the exact target summary (`records=40 bound=40 unbound=0` exit 0, in-flight run) — the lane-bytes counter alone is non-discriminating; the base-bytes clause is the exclusion and is inherently a PRE-STATE run on git-frozen bytes. Closures must cite both.
- **F-4 (attack 1):** the second control (A+C, no B) is caught by the selftest clause (via the contract's mandated cases) + the B-clause at fixture level, NOT by the base-bytes clause. The kill rule is an ensemble; the contract's ≥6-case list is what makes the selftest clause bite.
- **F-5 (mutants):** M1/M2/M3 caught (selftest failures=1 exit 1 + fixture-level acceptance of a kill-rule-failing state). **M4 skip-selftest is NOT caught by the kill rule text** — a mutant printing `selftest cases=9 failures=0` exit 0 without running anything passes the letter; the fake-checker itself prints `cases=0 failures=0` exit 0. Suggested correction: selftest clause reads "prints `cases<6`, any failure, or exits non-zero".
- **F-6 (attack 2):** the SCORECARD-capability predicate clause has no counter command and no kill-rule clause (PRE-STATE grep → 0). Suggested correction: add `grep -c 'capture-binding-check' SCORECARD.md` ≥ 1 as a counter and a kill-rule clause.
- **F-7 (attack 2, minor):** the contract's "checker NEVER writes into the lane" has no frozen counter; demonstrated here by hash-snapshot diff (empty). Suggest a before/after enumeration command in the counter set.
- **F-8 (attack 2, minor):** rule A's enumeration lives only in the checker's own AUDIT output; frozen counter command 3 is blind to manifest-less dirs (`*/manifest.json` glob). Also, a manifest-less dir holding only subdirectories is not a snapshot dir by the checker's definition (edge, unexercised).
- **F-9 (erratum-1):** clarification, permissible; caveats (b)-(d) above (predicate reads through the erratum; R20 wording; case-name nit).
- **F-10 (edge, minor):** `row_tokens` collects every `https://` token of the own row's source cell; a row carrying two URLs would let a record bind to either. Not exercised by current bytes (every row carries one URL; the S048 URL in the Search-log prose is not a row cell — erratum ground 3 confirmed).
- **F-11 (nit):** selftest scratch precedence is `--scratch` → `$HYAKU_SCRATCH` → `$TMPDIR` → `/fast/scratch/hyaku` → platform temp; the interface contract's letter says default `/fast/scratch/hyaku`. Bound 12 requires honouring `TMPDIR`, so the implementation satisfies the operator bound and deviates from the contract's precedence letter only; no committed default hardcodes `/tmp`.

## Bounds compliance

Writes: this receipt only (`.ufo/waves/round-33/wave1/RevClaimsFreeze.md`). Scratch `/fast/scratch/hyaku/kasegi-r33/RevClaimsFreeze/` removed before yield. Read-only git only (`archive`, `status`, `log`); no git/jj mutations; no pacman; no live-target contact; the S049/S050 capture contents were never opened by this seat (manifest fields only) and no credential material appears here. Peer messages: one reply to KasegiR33 (erratum verdict).
