VERDICT: BROKEN

# R45RevGateG3 — C2 gate G3 attack (round 45, kasegi)

Scope: `corpus/instruments/r45-c2-gate.py` `def g3` (lines 132-153) against the frozen C2 "after" in `.ufo/waves/round-45/claims.json` (C2 `after`: "SOURCES.md row S071: 11 cells, tier A, status `mined`, opened 2026-10-28, source cell holds the canonical URL, `used-by` lists the entry path, and the anchor cell carries the snapshot's sha256"). Read-only: counter run with `python3 -B` (no bytecode written into the lane), all edits in scratch fixtures; no git mutation (only `git show`/`git archive` read exports).

## What G3 actually checks (g3, lines 132-153)

- Row selection: `re.match(r"^ {0,3}\|\s*S071\s*\|", ln)` over raw lines of `corpus/SOURCES.md` (line 136). It does not know about code fences or HTML comments. Every 11-cell match overwrites `row` (lines 137-139), so the last 11-cell match wins.
- Cell tests are string equality or substring: tier `row[3]=="A"`, status `row[7]=="mined"`, opened `row[8]=="2026-10-28"` (lines 147-149); URL substring `URL in row[1]` (line 150); entry path substring `p in row[10]` (line 151).
- Source binding (line 143, 152): `sha256(corpus/source-snapshots/round-45/S071.txt)` is computed over whatever bytes are on disk and checked only for substring presence in `row[5]`.
- G3 never reads snapshot content, never reads `corpus/source-snapshots/round-45/manifest.json`, and never compares the row to the manifest. A zero-byte file therefore satisfies the sha pin.

So a registry row whose "source" is an empty (or arbitrary) file, with the sha of that file pasted into the anchor cell, is a claim without the source behind it that G3 grades green.

## Finding 1 — cheapest construction: G3 pass=1 with the defect present (BROKEN)

Recipe (all in scratch, base = pure export of `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`):
1. `: > corpus/source-snapshots/round-45/S071.txt` (zero bytes; sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
2. `corpus/README.md`: after the F26 row add `| F27 | Linux kernel security-bugs reporting process | admitted | knowledge/linux-kernel-security-bugs-process.md | S071 | next |`; create the empty file `corpus/knowledge/linux-kernel-security-bugs-process.md` (G3 needs only that the path exists).
3. `corpus/SOURCES.md`: after the S070 row insert:
   `| S071 | Linux kernel security-bugs reporting process — https://docs.kernel.org/process/security-bugs.html | docs | A | scope | sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | teaches | mined | 2026-10-28 | on-release | corpus/knowledge/linux-kernel-security-bugs-process.md |`

Command and printed output (G1..G7 shown; census stubbed, see limitations):
```
$ SOURCES_CENSUS=<scratch>/census-stub.sh python3 -B corpus/instruments/r45-c2-gate.py --root <scratch>/attack1
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-process.md
gate G2 pass=0 read=source=0 verified-at=0 recheck=0
gate G3 pass=1 read=row-S071=ok
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=4/7 exit=1
```
Printed gate line: `gate G3 pass=1 read=row-S071=ok`.

Variants of the same defect that also print `gate G3 pass=1 read=row-S071=ok` (all run, `$ ... variants.py`):
- `[B-junk-nonempty-snapshot]` snapshot = `Lorem ipsum dolor sit amet\n`, sha of that pinned in anchor: `gate G3 pass=1 read=row-S071=ok`.
- `[C-real-frozen-snapshot-correct]` snapshot = real frozen S071.txt (sha `0918dcfa…f40`, 20152 bytes, from `git show 8cf62c8:corpus/source-snapshots/round-45/S071.txt`): `gate G3 pass=1 read=row-S071=ok` (correct landing control).
- `[D-row-only-inside-code-fence]` the same zero-byte row placed inside a ``` fence in SOURCES.md: `gate G3 pass=1 read=row-S071=ok` (G3 scans raw lines, not the registry table).

### Finding 1b — G3 alone is BROKEN; the composite counter catches this exact construction only via G4

Freeze-tree variant (`git archive 8cf62c8`, real frozen `manifest.json` kept, zero-byte S071.txt, same row/F27 edits):
```
gate G3 pass=1 read=row-S071=ok
gate G4 pass=0 read=recheck-rc=1 quotes-ok=0 frozen-cores-missing=0
c2-gate fixed=4/7 exit=1
```
So the defect is green at G3 and red only because G4 binds the bytes to the frozen manifest. G3 itself does not bind. An attacker who also rewrites `manifest.json` (sha/bytes and the five quote cores, which G4 checks by substring) moves the binding problem into G4/G5, which then must be attacked separately; I did not run that second-stage attack.

## Finding 2 — control discrimination

Do-nothing control (pure base, no S071/F27):
```
gate G3 pass=0 read=row-S071=absent-or-malformed
c2-gate fixed=1/7 exit=1
```
G3 discriminates absence from the attack (pass=0 vs pass=1), so the green in Finding 1 is not a trivially-passing check.

Coverage gap in the frozen controls: `controls/freeze-controls.py` (read from `git show 8cf62c8:.ufo/waves/round-45/controls/freeze-controls.py`, lines 73-83) builds `c2-junk-row` by appending a README F27 row and an entry, with no SOURCES S071 row at all (despite its comment "registry row"). No frozen control therefore exercises G3's green path. The attack tree above also prints `fixed=4/7`, the same number as the frozen `c2-junk-row` control (`freeze-controls.txt:4`), so the printed totals cannot tell the two apart.

## Finding 3 — G3 false-RED on correct spellings (variants of a correct landing)

Baseline correct landing = real frozen S071.txt with the row as in Finding 1 with the true sha: `gate G3 pass=1 read=row-S071=ok` (C above). Each variant below is a correct-content landing with one spelling changed; each printed red:
- `[F]` opened cell `2026-10-28T20:52Z` (the timestamp the L1 uses in claims.json `sourced_claim`; S069 house style uses a bare date): `gate G3 pass=0 read=bad=opened`
- `[G]` used-by `knowledge/linux-kernel-security-bugs-process.md` (README-relative, no `corpus/`): `gate G3 pass=0 read=bad=used-by`
- `[H]` uppercase hex sha in anchor: `gate G3 pass=0 read=bad=anchor-sha`
- `[I]` sha in the scope cell, anchor says "see scope": `gate G3 pass=0 read=bad=anchor-sha`
- `[J]` an unescaped `|` in the teaches cell (12 cells): `gate G3 pass=0 read=row-S071=absent-or-malformed`
- `[K]` bare host URL `docs.kernel.org/process/security-bugs.html` in the source cell: `gate G3 pass=0 read=bad=url`
- `[L]` tier cell `A (primary)`: `gate G3 pass=0 read=bad=tier`
- `[M]` a second, later S071 row (e.g. superseded/annotated copy) with a different used-by: last-11-cell-wins (lines 137-139) makes G3 read it: `gate G3 pass=0 read=bad=used-by`
- `[E]` tier `B` (control that G3 does fail a wrong tier): `gate G3 pass=0 read=bad=tier`

Other spellings G3 would reject by reading lines 136-151, not separately run: leading indentation of 4+ spaces (regex `^ {0,3}`), bold or linked ids (`**S071**`, `[S071]`), a `| ` separator missing one pipe (cell count != 11), status with annotation (`mined (2026-10-28)`), recheck or teaches cells that are fine but a sha written with CRLF-altered snapshot bytes (sha is on-disk bytes).

## Limitations

- G7 was stubbed with `SOURCES_CENSUS=<scratch>/census-stub.sh` (prints and exits 0) so that the counter does not run the fleet census script; G7's line in my runs is therefore not authoritative. G3 does not depend on G7.
- The "final lane revision" does not exist yet; the attacks run on the pure base and on the frozen 8cf62c8 tree, which is the closest reproducible state. The F27 row and knowledge path in the fixtures are my own minimal insertions.
- One attempt hung for 300 s because my first census stub was a Python file invoked through bash; the stub was rewritten as a bash script and all printed results above come from the rerun. A `BrokenPipeError` trace in one run came from piping the counter to `head -3` and does not affect the gate lines.
- I did not run the frozen `freeze-controls.py` itself; the control rows above are from `freeze-controls.txt` and the code read via `git show`.
- I did not attack G4/G5 beyond the single zero-byte case in Finding 1b; no second-stage (rewritten manifest) attack was run.
- No claim here is a pass for G3: the verdict is BROKEN for G3 in isolation.

## Install/update record

None. No tools installed or upgraded.
