VERDICT: INFO

## Findings

### C2 / coverage — H1 accepts an appended junk table row

Built from the positive fixture, appended this admitted row immediately after F29 in the frontier table: `| JUNK | extra admitted junk row | admitted | corpus/knowledge/not-a-real-entry.md | S999 | fabricated row with no valid frontier identifier |`.

Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/junk-id --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`

Printed:
```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

This is a literal extra table row, but `frontier()` only collects lines matching `^\| F\d+ \|` (`corpus/instruments/r46-f29-gate.py:137-143`), so H1 ignores it. The exact discriminator command was `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/junk-f30 --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`; its output included `gate H1 pass=0 read=rows=30 admitted=30 dup=0` and `f29-gate fixed=6/7 exit=1`. The do-nothing command was `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/base --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`, which printed `f29-gate fixed=1/7 exit=1`; the positive command was `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/positive --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`, which printed `f29-gate fixed=7/7 exit=0`. These controls discriminate the false accept from the intended count-based rejection.

### C2 / coverage — an entry with no decision rule passes all seven limbs

Built a positive-derived entry whose scope and “Falsifiable package rule” prose merely describe page topics; removed the authorial decision rule and changed G6 to ask neutrally what fix-version wording appears. Required sections, table, xrefs, citations and source quotations remain, but no authorial sentence tells a maintainer what decision to make.

Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/no-decision-rule --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`

Printed:
```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

H2 enforces headings, word floors, table rows, xrefs and anchoring, not decision-rule meaning (`r46-f29-gate.py:183-219`). H5 verifies quoted strings against the snapshot (`:282-308`); it cannot distinguish an unadapted source quotation from the entry's own actionable rule. This passes a case the C2 kill rule says must kill the claim (`claims.json:33-34`).

### C2 / coverage — H1 accepts extra source attribution on F29

Built a positive-derived tree with F29's sources cell changed from `S074` to `S074; S999 (claimed same-ground source)`; S999 has no registry row in this fixture.

Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/source-spray --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`

Printed:
```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

H1 tests only whether `S074` occurs in that cell (`r46-f29-gate.py:170-171`), not that the attribution is exactly S074 or that every listed source exists. This bypasses the source-exclusivity condition in `claims.json:34`.

### C2 / coverage — fabricated quotes are caught, but the frozen junk receipt does not replay

The frozen fixture's fabricated mode changes the quoted “72 hours” and “doesn't make ... public” claims while retaining citations. Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/fabricated --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`.

Printed relevant lines: `gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5` and `f29-gate fixed=6/7 exit=1`. This control is correctly rejected by H5.

Re-ran the frozen helper's `--mode junk` tree. Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/junk-entry --work /fast/scratch/hyaku/kasegi-r46/R46bCritKillC2/work`.

Printed relevant lines: `gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1`, `gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5`, and `f29-gate fixed=6/7 exit=1`. Frozen receipt `controls/f29-r50-receipt.txt:6-7` says junk and fabricated trees each read `fixed=3/7` and describes junk H2/H5 as red. This replay of the frozen gate and frozen fixture helper disagrees: fabricated reads 6/7, and junk reads 6/7 with H2 green. The gate hash matched the freeze pin: the command `sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py` printed `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd` (also `freeze.txt:5`).

### Kill-rule operationalization

The weakest sentence is the C2 kill-rule clause: “or if the non-author closure re-opening the page cannot locate the cited quotes” (`claims.json:34`). It is not operational: it identifies no reviewer, checkpoint/deadline, page-reopening tool, per-quote procedure, or evidence receipt. The gate's H4 runs the local `source-recheck.py` against the manifest (`r46-f29-gate.py:257-279`); that tool says it reads only local files and checks captured bytes, not upstream availability or freshness (`source-recheck.py:2-9`). It is not a live-page reopening step.

Smallest safe correction: make the human check a required closeout receipt naming a non-author reviewer and UTC time, canonical S074 URL, the quote IDs/line mappings checked, the browser/manual method used, a pass/fail result, and whether the entry states an actionable decision rule. Separately, tighten H1 to validate every physical frontier-table row and require the F29 source set to be exactly S074 (with source IDs bound to registry rows); keep the fabricated-quote test as-is because it catches the exercised corruption.

## Limitations

Controls were synthetic positive-derived trees, not the eventual integrated lane tree; their temporary scratch was removed. I did not reopen the live documentation URL or evaluate the final landed entry. No canonical claim verdict is made. No tools were installed or updated.