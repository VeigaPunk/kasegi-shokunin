# CritC2Kill — adversarial review of C2 (round 29, wave 1)

Seat: `CritC2Kill-2` (UFO-FSD critic; leaf — no subagents).
Answering model: `inception/mercury-3` (session default; config route table; none passed by this seat).
Date: 2026-10-25. Lane: kasegi-shokunin. Claim under test: **C2** (coverage 7 held; F13 admission of S043/S044/S045).
Report path: `.ufo/waves/round-29/wave1/CritC2Kill.md` (this file).
Scratch + receipts: `.ufo/waves/round-29/wave1/CritC2Kill-scratch/` (committed-adjacent; R14-style).

All counters below were executed at the current lane HEAD (dispatch commit `46e07f6`); the F13 subject was not yet landed at receipt time, so the reproductions use **scratch trees** that mirror the landed state (README row + entry + manifest) — the counter behavior is byte-identical to what a landed run would exercise.

---

## C1. Counterexample — a manifest assertion that is NOT occurrences=1 passes C2's own recheck counter (exit 0) [CRITICAL]

Predicate/kill-rule limb tested: *"recheck_exit != 0 **or any manifest assertion not occurrences=1**"*.

Reproduction receipt (scratch; the record is under id `S043` but its capture path is `S045.txt`, and the quote occurs 53×, unanchored):

```
$ cat > <scratch>/corpus/source-snapshots/round-29/manifest.json <<'EOF'
{ "schema_version": 1,
  "sources": [ { "id": "S043", "path": "S045.txt",
      "sha256": "f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86",
      "quotes": [ {"id": "Q1", "quote": "\"children\": ["} ] } ] }
EOF
$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/corpus/source-snapshots/round-29/manifest.json --source S043
S043:sha256 OK
S043:Q1 OK occurrences=53 anchor=MISSING
$ echo $?
0
```

Impact: two Q9 clauses are silently unenforced by the frozen counter command:
1. **Path-stem ≠ id.** The record id `S043` binds to `S045.txt` (a Bugcrowd CWE capture); nothing anywhere checks `basename(path) == id`. The kill rule's "pinned capture" binding is therefore id-agnostic — three sources can share one capture, or a capture can be swapped between ids, without failing.
2. **Unanchored multi-occurrence quote passes.** A quote occurring 53× with no `anchor` prints `OK occurrences=53 anchor=MISSING` and exits 0. The instrument treats "visible, not fatal" as PASS (see `anchor_verdict` in `source-recheck.py`). So C2's own phrase *"any manifest assertion not occurrences=1"* is unfalsifiable through `recheck_exit` — the exact exit code the kill rule reads.

This is exactly the routed defect **M28-8** ("C2 Q9 stem check is not instrumented — promote `check_q9.py`"), carried into round 29 **unfixed**: the counter command set does not reference `check_q9.py` (it does not exist in `corpus/instruments/`), and `source-recheck.py` still exits 0 for both defect classes. The round-28 lesson already measured these (ExecHarnessC2 §D); this review re-derives the same from the *committed, unchanged* bytes.

Smallest safe correction: make `source-recheck.py` exit 1 when `occurrences > 1` and `anchor` absent (and when a declared anchor is out of range/broken), and return 2 when `basename(record["path"]) != record["id"]`; or add `check_q9.py` run to C2's counter chain and its kill rule.

---

## C2. Counterexample — the harness can PASS (16/16, exit 0) with a frontier row admitted before its entry exists, by pointing the row's entry cell at an existing unrelated entry [HIGH]

M28-5 class. The current instrument no longer passes in the *empty-cell or absent-file* case only because it crashes. But the crash is not the only path:

- **True absence** (entry path does not exist): `entry_contract()` raises an uncaught `FileNotFoundError` — traceback, exit 1. That satisfies the kill rule *by accident* (nonzero), but violates M28-5's routed fix ("fail with a named row"). Reproduced:
```
$ python3 <scratch>/corpus/instruments/frontier-recheck-count.py --root <scratch>
...
FileNotFoundError: [Errno 2] No such file or directory: '.../corpus/knowledge/program-severity-ladders-and-reward-scales.md'
```
- **Row points at an existing, contract-satisfying entry** (the F13 row's entry cell = `knowledge/japanese-domestic-disclosure-workflow.md`, the F12 entry): harness counts it and passes:
```
PASS  F13  knowledge/japanese-domestic-disclosure-workflow.md  ids=S041,S042  exit=0
entries=16 pass=16 exit=0        # exit 0 — subject "admitted" with zero new content
```
The harness has no notion that F13 should name a **new** entry; it only opens whatever path the cell names. Counter 1 (awk) counts the row as admitted (13), counter 2 (grep) is satisfied by a *different* file (see C4) that is never bound to any row. Result: all six counters pass while the frontier row contributes no new entry — the exact "row admitted before its entry exists / entry present but unhooked" false-pass shape.

Smallest safe correction: (a) harness rejects duplicate entry targets across admitted rows (same realpath twice); (b) require `open(entry)` to succeed and ALSO fail with a named row (no traceback) when it does not; (c) bind counter 2 to the row's entry cell: `grep -lE '^source: S04[3-5] '` must name the file referenced by F13's row, not any file in `corpus/knowledge/`.

---

## C3. Counterexample — a vacuous entry (headers only + a valid recheck line) passes the harness; the harness measures form, not admission substance

From code (`frontier-recheck-count.py` `evaluate()`): PASS requires exactly (1) ≥1 `source:` header line; (2) a `recheck:` line that is a `source-recheck.py` invocation with `--manifest`/`--source`; (3) declared ids ⊆ recheck ids; (4) recheck ids ⊆ body-cited ids (the header lines themselves satisfy this); (5) manifest lists the ids; (6) the executed recheck exits 0. No content, quote, or quality check exists. A 6-line stub (headers + one body line + chained recheck) passes if its manifest assertions pass. Counter 6 then passes on the same manifest.

Reproduction: in the same scratch, the stub entry with the *packaged prose recheck* was correctly rejected (`problems=not-a-recheck-invocation,no-source-selection,no-manifest`) — good — but a stub with a conforming chained recheck would not be. This confirms the harness's contract is "file exists + headers + runnable line", which is the documented scope; the claim's "admitted" wording, however, presents this as an admission measure. The only substantive gate is the human Q1–Q10 review, which is not part of C2's counters.

Smallest safe correction: state in the claim's surface that counters measure structural admission only; if substance is required, add a Q-bar counter (e.g. a `check_q10.py`-style form check) to C2.

---

## C4. Counterexample — counter 2 does not require all three ids, and can be satisfied by an unrelated file; S043 may be orphaned [MEDIUM]

- `grep -lE '^source: S04[3-5] ' corpus/knowledge/*.md | wc -l` counts **files**, not per-id coverage: a file with only `source: S043` (and no S044/S045 lines) still yields 1 — the kill rule's "entries citing S04[3-5] != 1" passes.
- The file counted by counter 2 need not be the F13 row's entry (see C2): in the scratch, counter 2 = 1 via the stub file while the row pointed at the F12 entry.
- The registry counter (`grep -cE '^\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md`) counts rows regardless of URL/used-by/tier/status: a row with a blank URL or a used-by pointing elsewhere still counts. Tier inflation is not visible to any counter (today's staged tiers are all A, so no inflation is present — but nothing would catch one).
- Net: S043 can be registered and captured yet cited by no entry, and C2 still passes. The predicate sentence "exactly 1 knowledge entry cites a row first registered this round (S043/S044/S045)" is materially weaker than its wording.

Smallest safe correction: counter 2 should assert the *set* `{S043,S044,S045} ⊆ header ids of the file named by F13's row` (and exactly that file), plus a "used-by" cross-check in the census (E11 already checks used-by targets exist — extend it to require every new row's used-by names the F13 entry).

---

## C5. Counterexample — the packaged F13 entry cannot honestly cite S043/S044/S045; the claim presumes a rewrite it never specifies [HIGH]

The staged entry `program-severity-ladders-and-reward-scales.md` (merge package) discusses **four ladders: CVSS-B, Bugcrowd VRT (staged S032/S033), CNVD 众测 (staged S034), BILISRC/360SRC (staged S036)**. The HackerOne standard program policy (staged S031 → lane S043) is the subject of the **other** staged entry (`program-scope-rules-and-asset-boundaries.md`). The claim says F13 "cites three rows first registered this round (S043/S044/S045)". ExecCensusDry's plan is "source: headers remapped to S043/S044/S045; **body carried verbatim**". That combination produces:

1. **False provenance / unanchored content:** the entry will declare `source: S043` while its body never discusses HackerOne's policy (the VRT/CNVD/BILISRC ladders are the body). The header is a provenance claim Q1 requires to be load-bearing; the counters cannot see it is dangling.
2. **Q2 violation invisible to all counters:** the CNVD and BILISRC sections remain load-bearing but have **no lane-registered rows this round** (package S034/S036 are not adopted; lane S034/S036 are different documents — 総務省/Cybozu). A reader would resolve `source: S034` to the 総務省 citizen page, not to CNVD 众测. The census gate explicitly defers this ("Q1–Q10 conformance is the owning seat's task, not part of this census gate"), and C2 has no limb that checks it.
3. The packaged recheck form (`90d — curl -sSL …` prose hybrid) fails the harness's own condition C (reproduced in C3: `not-a-recheck-invocation`), so the landed entry must be rewritten anyway; nothing in C2 validates that the rewrite preserved Q1–Q10.

Smallest safe correction: the claim's surface must name the entry transformation (which staged rows are dropped/re-sourced) before freeze, or the counters must include a `source:`→body cross-citation check (each declared `source:` id must appear in `cited` body claims — not merely in the header lines — with the quoted anchor present).

---

## C6. Context — S043 capture provenance (not a defect, but a degeneracy to record)

`capture-source.py --kind html` cannot fetch the HackerOne policy API (server returns a JS-disabled HTML stub; the 128 B capture is the stub). ExecCapS043 used the assignment's curl fallback and kept the **minified, single-line JSON** (1,220,741 B) with the server ETag cross-binding the snapshot (sha256 first-32-hex equals ETag). This is honest and reproducible. Degeneracy: `normalize()` and `anchor` windows operate on a one-line document, so `anchor: 1` is trivially true for every quote and cannot pin a sub-location; the only meaningful binding is the exactly-once occurrence of a unique quote. The receipt's own recommendation (prefer Q1-unique; treat repeated boilerplate as shared policy text) is the correct discipline, but neither C2's counters nor the kill rule enforce it.

---

## Impacted axes

- **coverage (C2's axis)** — all six counters can pass while: (a) manifest assertions violate the claim's own occurrences=1 wording (C1); (b) the frontier row names an existing/unrelated or vacuous entry (C2/C3); (c) S043 is orphaned and counter 2 counts the wrong file (C4); (d) the admitted entry is a rewritten stub with quarter-provenance (C5).
- **depth:verifiability (C1's axis)** — only incidentally: the shared Q9 binding (`source-recheck.py`) is the same instrument C1's anchor work protects; the C1 fix path (M28-8) is the natural home for the C1 corrections.
- No other axis is touched; no score claims are made here.

## Reproduction artifacts

- Scratch tree + receipts: `.ufo/waves/round-29/wave1/CritC2Kill-scratch/` (README.A.md/README.B.md variants, `absent.out`/`absent.err`, round-29 manifest + S045.txt copy).
- All commands above are runnable from the lane root; each cites the exact counter from `claims.json`.

## Bottom line

The frozen C2 counters are structurally sound at counting **rows and files**, but they cannot see **binding quality** (Q9 stem/occurrence), **row↔entry identity** (C2/C3), or **entry provenance/quality** (C4/C5). The claim's "any manifest assertion not occurrences=1" and "exactly 1 knowledge entry cites … S043/S044/S045" limbs are both weaker than their wording and unenforced by exit codes. Minimum safe corrections: (1) make `source-recheck.py` fail on duplicate-unanchored quotes and stem≠id (or gate on `check_q9.py`); (2) harness: reject duplicate entry targets, fail with a named row, and bind counter 2 to the row's file; (3) the claim must specify the F13 entry rewrite (which staged rows survive), and a counter must verify every declared `source:` id is actually load-bearing in the body.
