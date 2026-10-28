# MutBind — mutation battery for F-BIND and F-FLIP (round 42, wave 1)

Receipt-only item: enumerate the capture-binding (>=8) and frontier-counter (>=6)
mutation battery the J6/J7 repairs must reject, and run every mutant against the
current committed instruments on an isolated scratch corpus. Role rule honored:
pristine → mutate → detect → restore-exact-bytes, before/after hashes recorded,
lane bytes never touched.

## Target and detectors

- F-BIND detector: `python3 corpus/instruments/capture-binding-check.py --root $S/lane`
  (committed bytes, sha256 `3d9e5e0d…da99fa`). Baseline on live lane and on scratch
  copy: `records=55 bound=55 unbound=0`, exit 0 (`AUDIT … orphans=1 orphan=S040-live.txt`,
  declared orphan, consistent green).
- F-FLIP detector: `python3 corpus/instruments/frontier-recheck-count.py --root $S/lane`
  (committed bytes, sha256 `1be79af6…8249`). Baseline: `entries=27 pass=27 exit=0`
  (24 `| F<n> |` rows; F09–F11 carry two entries each → 27 evaluations).
- Fixture: `cp -a corpus` of the live lane into `$S/lane` (scratch only); S063
  record = `corpus/source-snapshots/round-41/manifest.json` sources[0],
  `path=S063.txt`, url/capture_url `https://www.rfc-editor.org/rfc/rfc9116.txt`,
  `sha256=925512e7…71e2faa`; F24 row = `corpus/README.md:563`
  (sha256 `55710368…f512db`); entry = `corpus/knowledge/rfc-9116-security-txt.md`
  (sha256 `eab59fdf…b059f0`).
- Committed defeats replicated: `.ufo/waves/round-41/wave2/MutBindingExistence.md`
  (missing-path + URL case/slash variants survived; missing filename variant was
  confounded by source-recheck's stem rule — this battery isolates existence by
  keeping `path=S063.txt` and deleting the file) and `MutC2Chain.md`
  (status flip `admitted→explored` → `entries=26 pass=26 exit=0`, row silently
  dropped — the routed F-FLIP blind spot).

## F-BIND battery — 11 mutants, 5 SURVIVED

Subject file unless noted: `corpus/source-snapshots/round-41/manifest.json`
(scratch baseline sha256 `6845702b…e7315`); capture `S063.txt` sha256
`925512e7…71e2faa`.

| # | Mutant | Expected post-J6 detector | Observed on current instrument | Verdict |
|---|--------|---------------------------|-------------------------------|---------|
| B1 | `path=S063.txt` kept; `S063.txt` deleted | FAIL rule=missing-capture (record.path must exist) | `records=55 bound=55 unbound=0` exit 0 | **SURVIVED** |
| B2 | `url` += trailing `/` | already: `rule=url-mismatch` | `FAIL rule=url-mismatch record=S063 row=S063 dir=round-41`, bound=54, exit 1 | KILLED |
| B3 | `url` https→http | already: `rule=url-mismatch` | `FAIL rule=url-mismatch record=S063 row=S063 dir=round-41`, bound=54, exit 1 | KILLED |
| B4 | `url` + `capture_url` case-flipped `/rfc/`→`/RFC/` (r41 artifact shape) | already: `rule=url-mismatch` | `FAIL rule=url-mismatch record=S063 row=S063 dir=round-41`, bound=54, exit 1 | KILLED |
| B5 | `sha256` ← sha256(round-40 `S060.txt`) | FAIL rule=sha-mismatch (record sha must equal file sha256) | `records=55 bound=55 unbound=0` exit 0 | **SURVIVED** |
| B6 | `id` S063→S999 (no registry row) | already: `rule=no-row` | `FAIL rule=no-row record=S999 dir=round-41`, bound=54, exit 1 | KILLED |
| B7 | extra record `id=S998, path=S063.txt` | already: `rule=no-row` + `rule=dup-record field=path` | `FAIL rule=no-row record=S998` + `FAIL rule=dup-record field=path value=S063.txt count=2`, `records=56 bound=55`, exit 1 | KILLED |
| B8 | `schema_version` 1→2 | FAIL rule=schema-version (manifest must declare schema_version==1) | `records=55 bound=55 unbound=0` exit 0 | **SURVIVED** |
| B8b | `sources` → `{"S063": …}` (valid JSON, wrong shape) | already: `UNAVAILABLE reason=manifest-shape` | exit 2, `UNAVAILABLE reason=manifest-shape …manifest.json` | KILLED |
| B9 | S063 record duplicated verbatim | already: `rule=dup-record` | `FAIL rule=dup-record field=id …` + `field=path …`, `records=56 bound=56`, exit 1 | KILLED |
| B10 | `path` → `../round-40/S060.txt`, `S063.txt` deleted | FAIL rule=capture-escape (path must stay inside its own dir) | `records=55 bound=55 unbound=0` exit 0 | **SURVIVED** |
| B11 | `files` → `["S063-ghost.txt"]`, `path` unchanged | FAIL rule=files-path-mismatch (files[] must equal {path}) | `records=55 bound=55 unbound=0` exit 0 | **SURVIVED** |

Post-battery re-run on restored bytes: `records=55 bound=55 unbound=0` exit 0;
`S063.txt` restored sha256 `925512e7…` (prefix-verified per mutant above).
Restoration evidence: per-mutant `restored:` lines in `fbind-out.txt` transcript —
every mutated file's sha256 re-matched its pristine backup; post-run detector
green is the end-to-end proof.

J6 repair surface (line refs to committed instrument): record-path existence and
same-directory containment — `capture_files()`/`bound_paths` at lines 434-444 is
file→record only; sha256 equality — `bind_record()` lines 283-305 never reads
`sha256`; `schema_version` — `check()` lines 383-386 checks only that `sources`
is a list; `files` field — never read anywhere.

## F-FLIP battery — 8 mutants, 5 SURVIVED

Subject file: `corpus/README.md` F24 row (`| F24 | RFC 9116 security.txt … | admitted |
knowledge/rfc-9116-security-txt.md | S063 | … |`), or the entry's `recheck:` line.

| # | Mutant | Expected post-J7 detector | Observed on current instrument | Verdict |
|---|--------|---------------------------|-------------------------------|---------|
| F1 | F24 status `admitted`→`queued` (committed MutC2Chain defeat) | FAIL rule=status-flip / non-admitted row must be named and rejected | `entries=26 pass=26 exit=0` — F24 silently absent | **SURVIVED** |
| F2 | F24 row deleted (no PASS line for it) | FAIL rule=missing-row (expected frontier inventory must enumerate it) | `entries=26 pass=26 exit=0` | **SURVIVED** |
| F3 | F24 sources cell `S063`→`S999`; entry still declares/rechecks S063 | FAIL rule=row-entry-id-mismatch (README S-cell must equal entry declared ids) | `PASS F24 … ids=S063 exit=0`, `entries=27 pass=27 exit=0` — S-cell never parsed | **SURVIVED** |
| F4 | entry `recheck:` gains `; exit 1` before the `#` comment | already: `problems=recheck-exit-N` | `FAIL F24 … exit=1 problems=recheck-exit-1`, exit 1 | KILLED |
| F5 | F24 row truncated to 3 cells (fails `FRONTIER_ROW` regex) | FAIL rule=unparsed-frontier-row (a `| F` line the parser can't bind) | `entries=26 pass=26 exit=0` — row silently skipped | **SURVIVED** |
| F6 | F24 status `admitted`→`Admitted` (case) | FAIL rule=unknown-status (status vocabulary enforced, or case-folded admit) | `entries=26 pass=26 exit=0` | **SURVIVED** |
| F7 | extra admitted `| F999 | … | knowledge/rfc-9116-security-txt.md |` (same entry as F24) | already: `DUPLICATE-ENTRY` | `DUPLICATE-ENTRY F24,F999 knowledge/rfc-9116-security-txt.md`, `entries=28 pass=28 exit=1` | KILLED |
| F8 | F24 entry cell `…rfc-9116-security-txt.md, knowledge/ghost.md` | already: `missing-entry` | `FAIL F24 knowledge/ghost.md … problems=missing-entry`, exit 1 | KILLED |

Post-battery re-run on restored bytes: `entries=27 pass=27 exit=0`; README sha256
`55710368…f512db` and entry `eab59fdf…b059f0` re-matched per mutant (`restored:`
lines in `fflip-out.txt`).

J7 repair surface (line refs): `admitted = [r for r in rows if r[2] == "admitted"]`
at `main()` line 393 drops every non-admitted row without a word — F1/F2/F5/F6 all
shrink `entries` instead of failing. `FRONTIER_ROW` (line 86) captures only four
cells, so the `Sxxx` sources cell (F3) is never bound to the entry's declared ids.
J7 must: enumerate every `| F<n> |`-shaped line (including unparseable ones),
assert status ∈ vocabulary with `admitted` required for claimed admissions, require
one PASS line per admitted row, and bind the README S-cell to the entry's declared
set. J9/J13 side note: expected-row count must come from a declared inventory
(`grep -cE '^\| F[0-9]+ \|'` = 24), not from `entries=N` alone — F2 keeps
`pass == entries` green.

## Cross-cutting finding for J7 (root isolation)

59 of 60 `recheck:` lines in `corpus/knowledge/` begin `cd /home/vgpnk/…/kasegi-shokunin`,
an absolute path. `frontier-recheck-count.py` executes them `bash -c` with
`cwd=root` (line 224), so under `--root <scratch>` the absolute `cd` silently
redirects every recheck to the LIVE lane — data mutations inside the scratch copy
(corrupting `S063.txt`, manifest lies) are invisible to the executed recheck.
Observed indirectly: this is why F4 mutated the *line* (adding `; exit 1`) rather
than capture bytes — a corrupted scratch capture would still pass. J7 should flag
or rewrite absolute-root `cd` in recheck lines (evaluated inside the export),
and J9's nested-export controls will otherwise re-verify the live lane, not the
export. (`grep -h '^recheck:' corpus/knowledge/*.md | grep -c 'cd /home'` → 59;
the sole exception is a non-source-recheck `test -e` line.)

## Evidence index

- `fbind.py` (driver) sha256 `4a1fdf08…0c1f45`; `fflip.py` sha256 `e58c9be4…f9d8a5d`
  — both under scratch, removed with it; transcript excerpts reproduced above.
- Commands: baselines `capture-binding-check.py` (live) → `records=55 bound=55
  unbound=0` exit 0; scratch `--root` runs of both instruments → same green;
  each mutant: backup → apply → `python3 <instr> --root $S/lane` → verdict →
  restore → sha256 equality assert → post-battery green re-runs (shown above).
- No network fetch, no tooling installed, no git/jj mutation, no lane writes.
- Scratch `/fast/scratch/hyaku/kasegi-r42/MutBind` removed at yield.

## Verdict summary

F-BIND: 11 mutants → 6 killed, 5 survived (B1, B5, B8, B10, B11). The routed r41
defeat (missing path) reproduces exactly; the URL-variant arm of MutBindingExistence
is now killed by rule B5 byte-equality — J6's replay limb must pin B1/B5/B8/B10/B11
as its positive-defeat fixtures.
F-FLIP: 8 mutants → 3 killed, 5 survived (F1, F2, F3, F5, F6). The routed
status-flip defeat reproduces exactly; the survivor class is "the row vanishes
and pass==entries still holds" — J7 must make frontier rows a counted inventory,
not a filter.
