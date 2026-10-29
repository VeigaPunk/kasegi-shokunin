# R46bW2ExecRerunC2 — re-run of the C2 counting chain at the integration export

VERDICT: HOLDS

Seat item: re-run the C2 counting chain at the integration export (f29-gate 7/7; frontier-count --expect 29; source-recheck S074 exit 0; capture-binding unbound=0; census exit 0; then r46-c1-gate 7/7 and r46-c2-gate 7/7 on the same export). Everything re-run, nothing trusted. Scratch exports via `git archive`; no commits, no pushes, no git/jj/index mutation; no live-target fetches; scratch deleted before yield.

## Headline

- **Claim C2's counting chain HOLDS at the true wave-1 integration commit `96379ae`** — every C2 limb this item names re-runs green: `f29-gate fixed=7/7 exit=0`, `frontier rows=29 admitted=29 rc=0`, `source-recheck` exit 0 (sha256 OK + 9/9 quotes), capture-binding `records=61 bound=61 unbound=0 rc=0`, census exit 0, and the claims' plain counts read exactly 29 F-rows / 74 S-rows / 66 entries / absence sweep 4 files.
- **The dispatch header pinned the wrong sha**: it names `fe0f56b` as "integration of wave 1", but `fe0f56b` is the *freeze* commit. The lane's own history puts the wave-1 integration at `96379ae` (= lane HEAD). At `fe0f56b` the chain reads exactly the claims file's `freeze_tree_reading` (`f29-gate fixed=2/7 exit=1`, H4+H7 green) — i.e. the claims file is honest about the intermediate state, and the dispatch label is the defect.
- Two of the item's seven literal expectations are unmet as stated: `r46-c1-gate` reads `2/7` (identically at base, freeze, and integration — the C1 re-ground work is wave a2w2 and has not landed), and `r46-c2-gate` v1.3 reads `5/7` at the integration **matching its own committed receipt byte-for-byte** (`gate-v13-66-entries-29-rows.txt`), because G1/G6 hard-pin the attempt-1 state (1 F-row / 65 entries). Neither fires any kill rule of claims C1/C2; both are dispatch-expectation defects, detailed below.

## Environment and integrity pins (measured, not assumed)

- `HYAKU_SCRATCH` unset → scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2ExecRerunC2/` (with `tmp/` as `TMPDIR`); `/tmp` never used.
- `git rev-parse fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4^{commit}` → `rc=0`, same sha; `git rev-parse 04af9bc92229232ea5cce8b32bfe59dd969eb26d^{commit}` → `rc=0`, same sha. Exports: `git archive <rev> | tar -x -C <scratch/{integ,base}>` rc=0 (158,351,360 / 158,259,200 bytes); later a third export `integ-96379ae` (162,590,720 bytes).
- S074 snapshot: `sha256sum integ/corpus/source-snapshots/round-46-a2/S074.txt` →
  `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039` — equals the claims' pin; `wc -l` → `42` lines.
- Manifest `round-46-a2/manifest.json`: `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f` — byte-identical across the live lane, the `fe0f56b` export, and the `96379ae` export.
- Instruments, export(`fe0f56b`) vs live lane: `r44-frontier-count.py`, `source-recheck.py`, `capture-binding-check.py`, `r46-c1-gate.py` IDENTICAL; `r46-f29-gate.py` and `r46-c2-gate.py` DIFFER (freeze has f29-gate v1 / c2-gate v1.2; live has the integrated f29-gate v1.1 / c2-gate v1.3). All six live instruments are sha-identical to the `96379ae` export copies, so "live instrument" == "integration instrument"; primary runs below use the item-named live paths with `--root` at the exports.

## Finding 1 — the dispatch's "integration of wave 1" sha `fe0f56b` is actually the freeze commit

Artifact attacked: the wave-2 dispatch header's tree pin. Command: `git log --oneline 04af9bc92229232ea5cce8b32bfe59dd969eb26d..HEAD` and `git show --stat -s fe0f56b...`. Quoted output:

```
96379ae round-46 (attempt 2): wave-1 integration — F29 entry + S074 row + admission blocks + ledger dispositions; instruments (selftests 83/147, selftest-f29, mutbat v1.1, f29-gate v1.1, c2-gate v1.3); errata E1-E4; lesson M46-4..6, QUALITY R53, LOG, SCORECARD, SHONEN, registry rows
ee03806 round-46 (attempt 2): wave a2w1 spec (64 seats, v2) + dispatch payload + builders + ready file
fe0f56b round-46 (attempt 2): freeze claims C1 counter-mutation coverage + C2 frontier F29, counters v1 (mutbat, f29-gate), S074 capture + manifest-a2, R50 receipt, controls
```

`git diff-tree` at `fe0f56b` adds only claims/controls/`r46-f29-gate.py`/`r46-mutbat.py`/`S074.txt`/`manifest.json` — no F29 entry, no README row, no SOURCES row. `fe0f56b` is an ancestor of HEAD (rc=0); HEAD = `96379ae`. The item's expectations are testable only at `96379ae`, so the chain was run at both trees.

## Finding 2 — at the dispatch-named `fe0f56b` export the chain reads the freeze values, exactly as claims.json predicts

Artifact attacked: claim C2's `freeze_tree_reading` ("f29-gate fixed=2/7 exit=1 at the freeze tree (H4 capture + H7 census green)"). Commands as item-named, `--root <fe0f56b export>`. Quoted outputs:

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=2/7 exit=1
```

```
frontier rows=28 admitted=28
frontier expected=29 admitted=28 verdict=SHORT exit=1
```

```
MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
FAIL rule=no-row record=S074 dir=round-46-a2
records=61 bound=60 unbound=1
```

(running capture-binding-check; middle MANIFEST lines round-23…round-46 identical in shape to the integration run, elided here — untrimmed in transcript)

```
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
... (Q2..Q8 identical form) ...
S074:Q9 OK occurrences=1 anchor=38-ok
```
rc=0 — H4's capture+manifest are committed at the freeze, as the claims state.

```
file	ok	<fe0f56b export>/corpus/SOURCES.md      # census rc=0, W04 warnings on S028/S029/S072 (pre-existing)
c1-gate fixed=2/7 exit=1        (L1 pass, L2-L6 pass=0, L7 pass)
c2-gate fixed=7/7 exit=0        (v1.2 at this tree; reads rows=28, row-S073=ok, quotes-ok=8, knowledge=65)
```

The freeze reading `2/7` with H4+H7 green is exactly the claims' `freeze_tree_reading`. No deviation.

## Finding 3 — at the true integration `96379ae` the C2 counting chain fully holds

Artifact attacked: claim C2's `after` (`expect_after: "f29-gate fixed=7/7 exit=0"`, `secondary: r44-frontier-count --expect 29`, recheck exit 0, binding unbound=0, census exit 0). Commands as item-named, `--root <96379ae export>` (live instruments, sha-verified equal to the export copies). Quoted outputs:

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=19 xrefs=7/7 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

```
frontier rows=29 admitted=29          # r44-frontier-count --expect 29, rc=0, no SHORT verdict
```

```
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
S074:Q2 OK occurrences=1 anchor=13-ok
S074:Q3 OK occurrences=1 anchor=17-ok
S074:Q4 OK occurrences=1 anchor=24-ok
S074:Q5 OK occurrences=1 anchor=25-ok
S074:Q6 OK occurrences=1 anchor=25-ok
S074:Q7 OK occurrences=1 anchor=26-ok
S074:Q8 OK occurrences=1 anchor=31-ok
S074:Q9 OK occurrences=1 anchor=38-ok
```
rc=0 (`--manifest` at the item-named live path; manifest bytes identical in the export, sha above).

```
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=61 with_url=61 with_fetched_utc=23 with_archival=38 snapshot_dirs=23 manifest_dirs=23 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=61 bound=61 unbound=0
```
rc=0 (round-23…round-39 MANIFEST lines elided; `url_bound=1` for round-46-a2 vs `url_bound=0` at the freeze).

```
file	ok	<96379ae export>/corpus/SOURCES.md     # census rc=0
```

Claims' plain counting commands (from `claims.json` C2 `plain[]`), re-run at all three trees:

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                          base=28  fe0f56b=28  96379ae=29
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md base=73  fe0f56b=73  96379ae=74
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l               base=65  fe0f56b=65  96379ae=66
grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l
                                                                     base=2   fe0f56b=2   96379ae=4
```

All C2 after-values hold exactly (29 rows, 74 S-rows, 66 entries, sweep 2→4 with README/SOURCES/the F28 entry + the new `github-repository-security-advisories.md` entry).

## Finding 4 — `r46-c1-gate` reads 2/7 at the integration; the item's "expect 7/7" cannot hold yet

Artifact attacked: the item's prior-attempt-instrument expectation for r46-c1-gate. Command: `python3 …/r46-c1-gate.py --root <96379ae export> --baseline <base export>`. Quoted output:

```
gate L1 pass=1 read=gated=22 broken=0 lines=66/base=65
gate L2 pass=0 read=base-gated=22 regrounded=0 
gate L3 pass=0 read=recheck-lines-exact=0
gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
gate L5 pass=0 read=append-only-restoration-kept=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=2/7 exit=1
```

Identical `fixed=2/7 exit=1` at the base export and the `fe0f56b` export (quoted in Finding 2 block and the control run). Wave 1 did not move this gate — its L2–L6 limbs are the C1 re-ground/battery work that lands with wave a2w2 (the commit graph shows only wave-1 integrated; the claims scope C1's counter as `r46-mutbat.py`, "at the final lane revision", which is not this tree). Not a C1/C2 kill; a premature dispatch expectation.

## Finding 5 — `r46-c2-gate` v1.3 reads 5/7 at the integration, byte-for-byte matching its committed receipt

Artifact attacked: the item's "(expect 7/7 — its v1.3 amendment if landed)" for r46-c2-gate. Command: `python3 …/r46-c2-gate.py --root <96379ae export>`. Quoted output:

```
gate G1 pass=0 read=rows=29 admitted=29 dup=0
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=5/7 exit=1
```

This equals, line for line, the commit's own receipt `.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v13-66-entries-29-rows.txt` (`fixed=5/7 exit=1`, G1 `pass=0 read=rows=29…`, G6 `pass=0 …base-intact=0`) — the integrated gate behaves exactly as its committed receipt documents. Cause is structural, from the gate source:

```
190:    if len(raw) != 1 or (False):
191:        return False, "F28-row-not-the-pinned-line"
192:    return True, f"rows=28 admitted=28 {why}"
...
357:    return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized), f"knowledge={len(names)} entries={len(everything)} nested-md={nested} base-intact={int(base_ok)} entry-bytes-ok={int(sized)}"
```

G1 admits exactly one F-row (the attempt-1 F28 pin); G6 admits exactly 65 knowledge entries. The integrated v1.3 (erratum E3) only added the considerthese ledger to the content-exempt set plus a junk-table-row check; it did not lift the 28-row/65-entry pins, so 7/7 at the grown tip is unreachable by construction. Context: at the attempt-1 adjudication state (base `04af9bc`) the gate reads `c2-gate fixed=7/7 exit=0` (control run below), so the counter still proves what it was built for; the 5/7 at the new tip is a disclosed state, not a falsified receipt. Action for the L1: either correct the dispatch expectation or log the pin-lift as a further erratum.

## Finding 6 — do-nothing control (base export `04af9bc`) discriminates on the right limbs

Command set: same chain, `--root <base export>`. Quoted key outputs:

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1
```
— exactly the claims' `expect_before` (`fixed=1/7 exit=1 (base export…)`).

```
frontier expected=29 admitted=28 verdict=SHORT exit=1
census → rc=0, file	ok	<base export>/corpus/SOURCES.md
capture-binding → records=60 bound=60 unbound=0   (rc=0: no round-46-a2 record exists at base)
c1-gate → fixed=2/7 exit=1
c2-gate → fixed=7/7 exit=0   (v1.2, attempt-1 state)
source-recheck (live manifest, S074) → rc=0, all 9 quotes OK   (manifest+snapshot shipped beside the live lane, not in the base tree)
```

Discrimination reading: f29-gate walks 1/7 (base) → 2/7 (freeze) → 7/7 (integration) and frontier-count 28 → 28 → 29 — these are the discriminative limbs, and no control tree grades f29-gate 7/7 (C2 kill-limb "any control grades 7/7" not fired). Census is exit-0 at all three trees and capture-binding is unbound=0 at both base (no record) and integration (row bound) — neither is state-discriminative by itself; the freeze's `FAIL rule=no-row … unbound=1` is the intermediate signal.

## Limitations

- No live-target testing was authorized or performed: S074's nine quotes were re-verified only against the sha-pinned snapshot and manifest, not against the live GitHub page (also outside this item).
- This is a wave-1-integration checkpoint, not the claims' "final lane revision": a2w2 (C1 battery/selftests, per the roster "Waiting for wave a2w2 and the battery receipt") had not landed at `96379ae`. C1/C2 final-adjudication limbs (mutbat uncaught=0, c1-gate 7/7) are not yet due; none were run as if they were.
- mutbat/selftest instruments are other wave-2 seats' items; not run here.
- The live `r46-f29-gate.py` docstring still reads "…v1." although the integration commit and its diff implement the v1.1 amendments (frontier_anywhere cross-check, HTML-comment stripping, source-cell hardening); the commit message and errata carry the version — cosmetic labeling only, noted for the errata file.
- Middle MANIFEST lines of two capture-binding runs are elided in this report for length (marked where); full untrimmed output is in the seat transcript and was quoted in full where decisive.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2ExecRerunC2/` (including all three exports) is deleted immediately after this report is written; nothing was written under `/tmp`, no fleet-root tracked file, no sibling-lane or `.ufo/state` path was touched, and no git/jj/index state was mutated (`git archive`/`rev-parse`/`diff-tree` only).
