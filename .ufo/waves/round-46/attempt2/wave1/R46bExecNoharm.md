VERDICT: DRAFT-READY

# R46bExecNoharm — round-46 attempt-2 no-harm sheet (executor seat)

## What was built

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm.sh`
— usage `noharm.sh [<base-rev>] [<tree>]`; defaults: base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`,
tree `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. It prints the seven carded items in order:
(1) the no-harm budget (numstat + every DELETED line outside the wave dir, named by file and classified
`PRE-JUSTIFIED` / `FINDING`), (2) `density.py`, (3) `anchorcheck.py`, (4) `capture-binding-check.py`,
(5) `recheck-audit.py`, (6) `frontier-recheck-count.py`, (7) the two prior-attempt counters
`r46-c1-gate.py` / `r46-c2-gate.py` at base-vs-base (do-nothing control), base-vs-live, and at the
attempt-1 receipt inputs. It writes nothing in the lane; scratch is created under
`$HYAKU_SCRATCH/kasegi-r46/R46bExecNoharm-*` and removed by an EXIT trap; `TMPDIR` is set explicitly and
`PYTHONDONTWRITEBYTECODE=1` so no `.pyc` is written into the lane.

Receipts copied into the draft dir (citable; the scratch tree was deleted after the runs):
- `R46bExecNoharm.draft/noharm-live.txt` — full run, base-vs-live (live lane tree)
- `R46bExecNoharm.draft/noharm-control-do-nothing.txt` — same script, tree = the base export (do-nothing control)
- `R46bExecNoharm.draft/noharm-replay-attempt1-base-inputs.txt` — the attempt-1 receipt replay (section 7e)

No tool was installed or upgraded: the sheet needed only `git`, `tar`, `awk` and the lane's own
instruments, so the operator tooling directive has nothing to record (no pacman, no `uv tool`, no binary).

## Findings

### F1 — (1) no-harm budget: nothing is deleted outside the wave dir (budget unspent)

Command (the carded one, run from the lane):

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --numstat 04af9bc92229232ea5cce8b32bfe59dd969eb26d -- . ':(exclude).ufo/waves/round-46/attempt2'
    1	0	.ufo/waves/round-46/a2w1.ready
    367	0	corpus/instruments/r46-f29-gate.py
    184	0	corpus/instruments/r46-mutbat.py
    42	0	corpus/source-snapshots/round-46-a2/S074.txt
    68	0	corpus/source-snapshots/round-46-a2/manifest.json
    exit=0
```

Every entry is an addition (second column `0`); the script's per-line classification prints:

```
--- (1b) deleted lines, named by file, classified
    SUMMARY deleted_lines=0 pre_justified=0 findings=0
```

Reading: at this moment the wave has deleted **no** line outside `.ufo/waves/round-46/attempt2`, so the
no-harm budget is unspent and there is no finding. The pre-justified exceptions (the two prior-attempt
recheck replacements) have not been spent either — they are already inside the base.

### F2 — (1c) the two prior-attempt recheck replacements are exactly the pre-justified class

Against the round-15 base (`914ca0b`), the same derivation the attempt-1 errata used
(`.ufo/waves/round-46/counter-errata.md`, "append-only: deletions per entry == 1 (the replaced recheck line)"):

```
--- (1c) the same diff restricted to the two prior-attempt re-grounded entries
    36	1	corpus/knowledge/claim-gates.md
    32	1	corpus/knowledge/claim-package-contract.md
    (expect: 1 deletion per entry -- the replaced recheck line)
    DELETED corpus/knowledge/claim-gates.md: recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15
    DELETED corpus/knowledge/claim-package-contract.md: recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15
```

Reading: exactly **one** deleted line per re-grounded entry, and both are `recheck:` lines in the two
entries the prior attempt re-grounded (`corpus/knowledge/claim-gates.md:125`,
`corpus/knowledge/claim-package-contract.md:68` hold their current re-ground recheck lines). These are the
pre-justified replacements; nothing else is deleted anywhere. The script classifies a deleted line as
`PRE-JUSTIFIED` only when it is a `recheck:` line in one of those two files — every other deletion
(including a non-`recheck:` deletion inside those two entries) is reported as `FINDING`.

### F3 — (2) density (unchanged by the wave so far)

```
--- (2) $ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/density.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md
    | | **mean dens** | | | | | | | | **258.7**
    Total path-citation instances: 839 across 33 blocks.
    exit=0
```

### F4 — (3) anchorcheck (no broken pin)

```
--- (3) $ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/anchorcheck.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md
    == /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
    exit=0
```

### F5 — (4) capture-binding-check: currently RED, and the reason is the un-landed S074 row

```
--- (4) $ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
    MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
    MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
    AUDIT records=61 with_url=61 with_fetched_utc=23 with_archival=38 snapshot_dirs=23 manifest_dirs=23 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
    FAIL rule=no-row record=S074 dir=round-46-a2
    records=61 bound=60 unbound=1
    exit=1
```

Quote of the current reading, as the card asked: **`records=61 bound=60 unbound=1` (exit 1)** — the card's
expectation `records=61 bound=61 unbound=0` is **not met yet and is not met by a fault of the wave**: the
S074 capture and its `round-46-a2` manifest are committed (freeze commit `fe0f56b`), but the S074 row in
`corpus/SOURCES.md` and the F29 entry are not in the tree yet, so the capture has no row to bind to
(`FAIL rule=no-row record=S074 dir=round-46-a2`). Corroboration that the F29 side is not landed:
`ls corpus/knowledge/ | wc -l` prints `65` and no `github-repository-security-advisories.md` exists
(the entry the card names as the F29 target).

Discrimination against the do-nothing control (same script, tree = the base export, which does not
contain the `round-46-a2` capture at all):

```
    AUDIT records=60 with_url=60 with_fetched_utc=22 with_archival=38 snapshot_dirs=22 manifest_dirs=22 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
    records=60 bound=60 unbound=0
    exit=0
```

So the sheet is sensitive to the S074 row: base reads `records=60 bound=60 unbound=0` (green), the live
tree reads `records=61 bound=60 unbound=1` (red, because the committed capture has no registry row yet).
After the S074 row and the F29 entry land, this item must read `records=61 bound=61 unbound=0`.

### F6 — (5) recheck-audit (live lane): green

```
--- (5) $ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
    strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
    executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
    lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
    expect=present expected=65 missing=0 unexpected=0 exit=0
    exit=0
```

Do-nothing control (tree = base export) — the discriminating lines:

```
    strict pass=1/65 cdroot_fail=64 instrument_fail=0 own_fail=0
    lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
    expect=present expected=65 missing=0 unexpected=0 exit=1
    exit=1
```

(The export's `recheck:` lines `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …` do not resolve from
the export root, so the control reads `cdroot_fail=64`; the live-lane reading is the meaningful one.)

### F7 — (6) frontier-recheck-count: the frontier has not moved yet

```
--- (6) $ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/frontier-recheck-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
    FRONTIER-CENSUS rows=28 admitted=28 closed=28 problem-rows=0 registry=73
    PASS     F28  corpus/knowledge/github-private-vulnerability-reporting.md ids=S073           exit=0
    entries=31 pass=31 exit=0
    exit=0
```

The do-nothing control prints the same census line (`rows=28 admitted=28 closed=28 problem-rows=0
registry=73`, `entries=31 pass=31 exit=0`) — i.e. F29 is not admitted yet, and the sheet's baseline for
the wave is `rows=28 … registry=73`.

### F8 — (7) the prior-attempt counters: same green/red as their receipts

Base-vs-base (do-nothing control) and base-vs-live, from `noharm-live.txt`:

```
--- (7a) do-nothing control: c1 --root <base export> --baseline <base export>
    c1-gate fixed=2/7 exit=1
    exit=1

--- (7b) base-vs-live: c1 --root <tree> --baseline <base export>
    c1-gate fixed=2/7 exit=1
    exit=1

--- (7c) do-nothing control: c2 --root <base export>
    c2-gate fixed=7/7 exit=0
    exit=0

--- (7d) base-vs-live: c2 --root <tree>
    c2-gate fixed=7/7 exit=0
    exit=0
```

Reading: `r46-c2-gate.py` stays **green** (7/7) at the attempt-2 base and on the live tree — the prior
attempt's C2 counter is unharmed. `r46-c1-gate.py` reads **red** (2/7) at the attempt-2 base and
base-vs-live. That red is structural, not a regression: limb L2 requires the regrounded set
`R = gated(BASE) − gated(TREE)` to be non-empty (`|R| >= 2`), and the attempt-2 base `04af9bc9` already
contains attempt 1's re-grounding of `claim-gates.md` and `claim-package-contract.md`, so `R` is empty by
construction at this base. The correct comparison for "the prior-attempt instruments stay green/red
exactly as their receipts say at the same inputs" is the attempt-1 receipt inputs, replayed in F9.

### F9 — (7e) receipt replay: the prior-attempt instruments reproduce their attempt-1 receipts line for line

Receipt: `.ufo/waves/round-46/controls/final-measure.txt` (`measured-at-rev: eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7 base: 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`).
Replay receipts: `R46bExecNoharm.draft/noharm-replay-attempt1-base-inputs.txt`.

| input | attempt-1 receipt | my re-run |
|---|---|---|
| `r46-c1-gate.py --root <r15base> --baseline <r15base>` | `final-measure.txt:11` → `c1-gate fixed=1/7 exit=1` | `c1-gate fixed=1/7 exit=1` (same seven limb lines: `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64` … `gate L7 pass=1 read=still-gated=24 changed=none`) |
| `r46-c1-gate.py --root <live lane> --baseline <r15base>` | `final-measure.txt:21` → `c1-gate fixed=7/7 exit=0` | `c1-gate fixed=7/7 exit=0` with the identical limb lines (`gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64`, `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`, `gate L3 pass=1 read=recheck-lines-exact=2`, `gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2`, `gate L5 pass=1 read=append-only-restoration-kept=2`, `gate L6 pass=1 read=mutants=46 survivors=none`, `gate L7 pass=1 read=still-gated=22 changed=none`) |
| `r46-c2-gate.py --root <r15base>` | `final-measure.txt:60` → `c2-gate fixed=1/7 exit=1` | `c2-gate fixed=1/7 exit=1` (identical limb lines: `gate G1 pass=0 read=rows=27 admitted=27 dup=0` … `gate G7 pass=1 read=census-rc=0 ok-line=1`) |
| `r46-c2-gate.py --root <live lane>` | `final-measure.txt:70` → `c2-gate fixed=7/7 exit=0` | `c2-gate fixed=7/7 exit=0` (identical limb lines: `gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md` … `gate G7 pass=1 read=census-rc=0 ok-line=1`) |

Reading: at the attempt-1 receipt inputs, both prior-attempt counters print exactly what their receipt
says — `c1-gate 1/7` red at the base and `7/7` green at the tree, `c2-gate 1/7` red at the base and
`7/7` green at the tree. The attempt-1 C1/C2 counter claims are unharmed by the attempt-2 tree.

### F10 — the whole sheet discriminates against a do-nothing control

`noharm-live.txt` (live lane) vs `noharm-control-do-nothing.txt` (tree = base export) differ in exactly
the readings that should differ — items (4) and (5) — plus the printed paths. Full `diff` output
(52 lines) is in the two receipt files; the substantive hunks:

```
<     MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
<     AUDIT records=61 with_url=61 ... snapshot_dirs=23 manifest_dirs=23 ...
<     FAIL rule=no-row record=S074 dir=round-46-a2
<     records=61 bound=60 unbound=1
<     exit=1
---
>     AUDIT records=60 with_url=60 ... snapshot_dirs=22 manifest_dirs=22 ...
>     records=60 bound=60 unbound=0
>     exit=0
<     strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
---
>     strict pass=1/65 cdroot_fail=64 instrument_fail=0 own_fail=0
<     lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
---
>     lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
```

Items (1), (6) and (7) read identically on both trees — correct, because the wave has not yet changed the
frontier, the corpus or the counters' inputs.

## Limitations

1. The (1) budget is read from the **working tree** (`git diff <base>`), so it reflects committed + uncommitted
   lane state at the moment of the run (lane HEAD `ee03806`, plus the L1's uncommitted wave files). Re-run the
   script after the integration commit for the final budget statement; the script takes the base as an argument,
   so the L1 can pass any base.
2. The `PRE-JUSTIFIED` class is narrow on purpose: a deleted `recheck:` line in
   `corpus/knowledge/claim-gates.md` or `corpus/knowledge/claim-package-contract.md`. Every other deleted line
   outside the wave dir is a `FINDING` and needs a fresh justification from the L1.
3. Item (4) is **red now** (`records=61 bound=60 unbound=1`) and becomes green only when the S074 row and the
   F29 entry land. I could not run the card's expected `records=61 bound=61 unbound=0` — that tree does not
   exist yet, so that reading is *unrun*, not passed. After the landing, re-run: the expectation is
   `records=61 bound=61 unbound=0` with `FAIL rule=no-row record=S074` gone.
4. `r46-c1-gate.py` reads red (2/7) against the attempt-2 base for a structural reason (L2 needs a regrounded
   set relative to the baseline; the attempt-2 base already holds attempt 1's re-grounding). Do not read that
   as "the prior attempt's C1 claim is broken": F9's replay at the attempt-1 inputs is the comparison the card
   asks for, and it reproduces the receipts exactly.
5. Items (2) and (3) grade `SKILL.md` only. They are lane-wide numbers (density mean 258.7, 16 in-range cite
   instances, 0 bad) and are unaffected by the F29 landing unless `SKILL.md` changes; they are a no-harm tripwire,
   not an F29 measurement.
6. Item (5) is the live-lane reading; the base-export control reads `cdroot_fail=64` because the exported
   entries' `recheck:` lines `cd` into the live lane path. That is an artefact of exporting, not a lane defect.
7. I did not run the mutation battery (`r46-mutbat.py`) or the F29 admission gate (`r46-f29-gate.py`): they are
   outside this seat's card (item 7 names only the two prior-attempt counters) and belong to the C1/C2 seats
   and the L1's final measurement. The battery before-value remains the frozen receipt
   `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (`c1 uncaught=7`, `c2 uncaught=13`).
8. Live-target testing was refused: every reading above comes from committed bytes or local `git archive`
   exports; no network call was made.
9. The script is a builder draft: it is not committed, is not referenced by any lane instrument, and the L1
   must integrate it (and decide where the final no-harm receipt lives). Nothing outside
   `.ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/` and this report was written; the lane working
   tree is unchanged by this seat (`git status --porcelain` shows only the L1's own wave files).

## Commands run (all re-runs by this seat, 2026-10-29)

```
bash .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm.sh 04af9bc92229232ea5cce8b32bfe59dd969eb26d /home/vgpnk/Projects/shokunin/kasegi-shokunin
bash .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm.sh 04af9bc92229232ea5cce8b32bfe59dd969eb26d /fast/scratch/hyaku/kasegi-r46/R46bExecNoharm/base
bash -n .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm.sh
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive <rev> | tar -x -C <scratch>   # base 04af9bc9 and round-15 base 914ca0b
```
