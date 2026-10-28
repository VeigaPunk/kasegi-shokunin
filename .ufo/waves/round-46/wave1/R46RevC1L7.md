# R46RevC1L7 — C1 limb L7 attack report

VERDICT: BROKEN

Seat: R46RevC1L7 (leaf reviewer). Scope: limb L7 of `corpus/instruments/r46-c1-gate.py` (frozen, sha256 `b0c730c8...dd82294` — matches `freeze.txt` line `c1-gate-sha256`). Frozen sentence under attack (claims.json C1 "after"): "Entries still gated keep their BASE recheck line byte-identical."

## Limb under test (counter lines 237-239)

```python
still = sorted(gb & gt)
bad7 = [e for e in still if cb[e]["line"] != ct[e]["line"]]
res.append(("L7", not bad7, "still-gated=%d changed=%s" % (len(still), ",".join(bad7) or "none")))
```

`recheck_line` (lines 78-83) returns the FIRST `^recheck:` line, `.strip()`ped. L7 therefore guards exactly one stripped string per still-gated entry.

## Scaffold (honest work the attack rides on)

Tree = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` + counter installed in `corpus/instruments/` + the intended pair re-grounded (`claim-package-contract.md`, `claim-gates.md`: base recheck line replaced by a no-`cd` `--entry` line; 8-row `## Re-ground (round 46)` section appended; anchors on `claim-package-check.py` / `claim-package-selftest.py`, tokens verified present at the cited lines).

```
$ python3 r46-c1-gate.py --root tree --baseline base --work work
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=16 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

This is also the C1 re-ground demonstration: the intended pair carries 7/8 located rows over 2 committed files, and L6 graded all 16 row mutants non-zero (`survivors=none`).

## Constructions (5 distinct, all re-run)

**A — still-gated entry body edited to hide provenance + fabricated re-ground section: L7 passes, counter 7/7.** On still-gated `ev-model.md` (confirmed in `still:` list via a `classify()` probe: `ev-model still-gated: True`): (1) scrubbed the honesty markers — `source: [lost-base] ~/Projects/the-bounty-hunter/ops/ev-report.mjs, header and computation; [lost-tree] ~/Projects/bounties/bounty-map/schema.json, ev_inputs properties.` became `source: corpus/instruments/claim-package-check.py header and computation; committed corpus notes.`; (2) appended a 7-row `## Re-ground (round 46)` section whose rows point at real bytes of `claim-package-check.py`/`claim-package-selftest.py` but support nothing about the EV model; (3) first recheck line untouched.

```
$ python3 r46-c1-gate.py --root tree --baseline base --work work
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
$ python3 r46-c1-gate.py --entry corpus/knowledge/ev-model.md --root tree
row G1 ok=1 read=token-located   ... (7 rows) ...
reground entry=ev-model.md rows=7 ok=7 files=2 exit=0
```

No limb reads a non-reg entry's body: the counter prints 7/7 on a tree where a gated entry's lost-tree admission was erased and it now LOOKS re-grounded. The per-entry mode even grades the fake section green on demand.

**B — second recheck line: both instruments blind.** Appended `recheck: test -s corpus/knowledge/ev-model.md && grep -q "Adjusted-EV model" corpus/knowledge/ev-model.md` (green) as line 74; gated base line stays line 60.

```
$ python3 r46-c1-gate.py --root tree --baseline base --work work
c1-gate fixed=7/7 exit=0
$ python3 tree/corpus/instruments/recheck-audit.py --root tree --quiet
executes=42 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
$ python3 tree/corpus/instruments/score-gap.py --root tree
[5] gap
gap: 22 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

All three cited instruments (counter, recheck-audit, score-gap) read only the first `recheck:` line (counter line 78-83; audit `audit_entry` `break`s on first match) — the second line is invisible to every one of them, and the claim's own metrics (`gated=22 broken=0`, `gap: 22 of 64`) read exactly on-target.

**C — "byte-identical" is enforced as strip()-equal.** Two trailing spaces appended to `ev-model.md`'s base recheck line:

```
$ sed -n 60p base/.../ev-model.md | cat -A | tail -c 60
6-09-28; not re-verifiable; re-scope is L0 kasegi round-15$
$ sed -n 60p tree/.../ev-model.md | cat -A | tail -c 60
09-28; not re-verifiable; re-scope is L0 kasegi round-15  $
$ python3 r46-c1-gate.py --root tree --baseline base --work work
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

Bytes differ; the frozen sentence says byte-identical; the limb passes.

**D — moved entry: route closed (negative control).** Renaming still-gated `terminal-classes.md` → `terminal-classes-renamed.md` on a fresh scaffold:

```
gate L1 pass=0 read=exception-KeyError  (all seven limbs)
c1-gate fixed=0/7 exit=1
```

The base-keyed mapping (`ct[e]` for e in `gb-gt`) crashes and `main` fails closed. An entry cannot silently vanish from the gated count; the cost is a crash, not a message.

**E — L7 can fail alone: load-bearing (negative control).** Fresh scaffold; still-gated `terminal-classes.md` line 49 tail `anchorcheck.py` → `anchorcheckX.py` (parses; runs; exits non-zero → still gated; line differs):

```
gate L1 pass=1 ... gate L6 pass=1 read=mutants=16 survivors=none
gate L7 pass=0 read=still-gated=22 changed=terminal-classes.md
c1-gate fixed=6/7 exit=1
```

## Can the limb fail alone?

Yes — construction E shows L7 red with L1-L6 green. It is load-bearing, but only for the first recheck line's stripped bytes. Constructions A/B/C show its green carries no information about still-gated entries' bodies, extra recheck lines, or byte-level whitespace.

## Discrimination vs controls

Do-nothing (frozen controls + my re-run on base vs base): `L7 pass=1 ... c1-gate fixed=1/7 exit=1` — L7 green is free without work. My scaffold reached 7/7 (work done, no defect); attack trees reached 7/7 WITH the defect present; treeE reached 6/7 (defect-free, line mutated). L7's pass/fail tracks line-bytes only, never the hide.

## Secondary spec-vs-gate divergence found while building

Frozen claim says re-grounded entries keep "every BASE line ... (append-only)". L5 (lines 197-201) compares base vs tree with RECHECK lines filtered out on BOTH sides, so wholesale REPLACING the base recheck line of a re-grounded entry passes L5 (my scaffold did exactly that). The gate is weaker than the sentence for regrounded entries' recheck lines; still-gated entries have no L5 coverage at all (see A/B/C).

## Limitations

- Scratch-only (HYAKU_SCRATCH/kasegi-r46/R46RevC1L7, removed on exit); nothing in the lane repo touched; no git/jj mutations; no installs performed (none needed).
- The re-ground scaffold is a draft demonstration: its rows are token-located and L6-load-bearing, but the semantic "rows support the entry's claims" review belongs to the kill_rule's non-author reading, not to this seat.
- `recheck-audit.py`'s `strict pass=1/64 cdroot_fail=61` on the scratch tree is its own strictness about live-lane `cd` targets, not a C1 limb; quoted only for the `executes=/gated=` line.
- Cheap hardening exists but is the counter author's call: extend L5's append-only prefix check to ALL still-gated entries (or byte-equality of whole files), which would have caught A, B and C at ~zero cost.

## Recipe (construction A, cheapest full chain)

1. `cp -r /fast/scratch/hyaku/kasegi-r46/L1/pure tree && cp <counter> tree/corpus/instruments/`
2. Re-ground the intended pair honestly (append `## Re-ground (round 46)` sections; replace their recheck lines with `python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>.md`) → counter prints 7/7.
3. On any still-gated entry: edit its body (scrub `[lost-base]`/`[lost-tree]` markers), append a fake `## Re-ground (round 46)` section with real committed tokens, optionally append a green second `recheck:` line or trailing whitespace.
4. `python3 r46-c1-gate.py --root tree --baseline base` → `c1-gate fixed=7/7 exit=0` with `gate L7 pass=1 read=still-gated=22 changed=none`.
