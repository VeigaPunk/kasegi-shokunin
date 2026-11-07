# ExecC2Gate — C2: pre-landing predicates B0/B4/B5/B6/B8 and the landing simulation for F60 (S118)

Round 84, attempt 1, wave 1, seat `ExecC2Gate`. Scratch `/fast/scratch/hyaku/kasegi-r84/ExecC2Gate` (deleted before yield). No lane file, corpus file, registry, instrument or frozen `c1/` byte was edited; every measurement is read-only over the frozen bytes or the scratch mirror; no git/jj write; no tool installed (nothing needed). Fourteen receipts are beside this report under `ExecC2Gate-receipts/`.

## Inputs (measured)

| object | bytes | lines | sha256 |
|---|---|---|---|
| draft entry `corpus/knowledge/osv-gcs-data-dump-layout.md` (uncommitted, `??`) | 11936 | 98 | `0f9c1486db7756020b935060052ee55455be905da1bc4c0089d1cc816b2b7552` |
| capture `corpus/source-snapshots/round-84/S118.txt` | 5820 | 129 | `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359` |
| manifest `corpus/source-snapshots/round-84/manifest.json` | — | — | `80129310e4880f857a0c2225f028ac8e5985ceff21ad5d5496c1867a7de0a65a` |
| gate `.ufo/waves/round-83/c2/entry-gate.py` (unchanged since r83) | — | — | `42f4b2accf704455325f8d1eb8ca4ec21401e35397af7a36861c33a27ace6302` |

Manifest `final_url == url`, `status 200`; all six quotes occur exactly once at their anchors 102/104/104/114/121/123; word counts by `len(quote.split())` are 17/8/13/7/15/12, matching the entry's Gate table (`ExecC2Gate-receipts/pinned-bytes.txt`). The entry's non-claimed ranges were spot-checked at the snapshot: `:31-60` source list (`31 Current data sources` … `60 V8 / Chromium`), `:61-65` converted data, `:66-96` covered ecosystems, `:97-98` Data Quality, `:99` Data dumps heading, `:109-119` top-level CSV, `:122` ecosystems.txt, `:124-126` contributing data, `:1` title `Data sources | OSV` (`ExecC2Gate-receipts/s118-line-range-check.txt`). No range mismatch found.

## Pre-landing predicates (run over the uncommitted draft)

**B0 — pass.** `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-84/manifest.json --source S118` printed `S118:sha256 OK` plus six `OK occurrences=1 anchor=<n>-ok` lines, rc=0 (`ExecC2Gate-receipts/b0-source-recheck.txt`).

**B8 — pass, gate and selftest.** On the draft the unchanged r83 gate printed `ruleless=0 untied=0 header=ok` / `ENTRY-GATE-RESULT pass`, rc=0; `--selftest` printed `entry-gate selftest ok got={'good': True, … 'copyrule': False}` (all eleven negative fixtures False), rc=0 (`ExecC2Gate-receipts/b8-entry-gate.txt`). This draft is the post-v0 revision: the frozen `c2-draft-v0-r84.txt` control shows v0 failing with `untied=2`, so the two rule rewrites that closed those ties are confirmed by this run.

**B4 — pass.** `python3 corpus/instruments/capture-binding-check.py | tail -1` → `records=98 bound=98 unbound=0`, rc=0 (`ExecC2Gate-receipts/b4-capture-binding.txt`).

**B5 — pass.** The entry's `recheck:` line is `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-84/manifest.json --source S118` — the B0 command exactly behind that `cd`. Run from a fresh foreign cwd `/fast/scratch/hyaku/kasegi-r84/ExecC2Gate/b5`: the same seven lines, rc=0 (`ExecC2Gate-receipts/b5-entry-recheck-freshcwd.txt`).

**B6 — pass.** Literal sweep of the six manifest quotes over the 97 other `corpus/knowledge/*.md` (draft excluded): 0 files for each quote, `literal_sweep_total 0 files 97`, rc=0 (`ExecC2Gate-receipts/b6-literal-sweep.txt`). This independently reproduces the count the entry's Distinctness section cites at `.ufo/waves/round-84/controls/c2-prefreeze-r84.txt`.

## Landing simulation (scratch mirror)

Mirror built as `git archive HEAD | tar -x -C $S/m` (freeze commit `7f76b7e`), the uncommitted draft copied to `$S/m/corpus/knowledge/`, then the five landing edits: README amendment block + F60 row, SOURCES S118 cells and round bullet, and the `knowledge-expected.txt` line. `diff -r` against a second HEAD archive shows exactly the three edited files plus the new entry. The other `changed` paths in `ExecC2Gate-receipts/mirror-diff.txt` are not extra files: `.ufo/waves/round-31/.../corpus/instruments` is a tracked symlink (mode 120000, `readlink` = `../../../../../../../corpus/instruments`), so in the mirror it resolves to the mirror's own `corpus/instruments/` and those paths are the same inode as the edited list (`ExecC2Gate-receipts/fixture-symlink-topology.txt`: one device/inode, nlink=1). No second copy exists and no sync action is needed at landing.

**B1 (simulated) — pass.** Registry rows 118 at freeze and 118 in the mirror; exactly one row differs, `S118`: cell 7 `queued` → `mined`, cell 10 `—` → `corpus/knowledge/osv-gcs-data-dump-layout.md`; no row added or removed (`ExecC2Gate-receipts/mirror-b1-b2.txt`).

**B2 (simulated) — pass.** `corpus/knowledge/*.md` 97 (freeze) → 98 (mirror); `knowledge-expected.txt` gained exactly `corpus/knowledge/osv-gcs-data-dump-layout.md`, lost nothing, and its entry set equals the mirror tree set (98 == 98, no missing, no unexpected) (`ExecC2Gate-receipts/mirror-b1-b2.txt`).

**B3 (simulated) — pass.** `python3 corpus/instruments/frontier-recheck-count.py` in the mirror printed `FRONTIER-CENSUS rows=60 admitted=60 closed=60 problem-rows=0 registry=118` and `FRONTIER-PASS F60 ids=S118`, then `entries=63 pass=63 exit=0`, rc=0 (`ExecC2Gate-receipts/mirror-frontier-count.txt`). The do-nothing baseline is rows=59 in the frozen control, so the row moved exactly one.

**B7 (simulated) — pass on the mirror registry.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/m/corpus/SOURCES.md` → `file ok …` rc=0, with the same six pre-existing W04 duplicate-URL warnings as the live lane file and no other code (`ExecC2Gate-receipts/mirror-census-validate.txt`). The fleet-root `--root` form of B7 is left to the landing commit; it reads sibling lanes, which this seat must not do.

Extra axis check (not one of B0-B8): `corpus/instruments/recheck-audit.py --root <live lane> --expect <mirror knowledge-expected.txt>` → `strict pass=98/98 cdroot_fail=0 instrument_fail=0 own_fail=0`, `lines=98 total=98 pass=98 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0`, `expect=present expected=98 missing=0 unexpected=0 exit=0`, rc=0 (`ExecC2Gate-receipts/recheck-audit-live-with-mirror-expect.txt`). This binds the F60 recheck line to its entry and the expected-list edit to the tree.

## Candidate bytes for integration

All six are pure file bytes; digests are in the directory listing.

| file | placement |
|---|---|
| `ExecC2Gate-candidate-readme-row.txt` | the `| F60 | … |` row, inserted on the line after the `| F59 | … |` row of `corpus/README.md` (it is carried inside the amendment block too) |
| `ExecC2Gate-candidate-readme-amendment.txt` | appended verbatim at end of `corpus/README.md`; it starts with a blank line, matching the r83 block's separator |
| `ExecC2Gate-candidate-sources-row.txt` | replaces the live `| S118 | … | queued | 2026-11-06 | 90d | — |` row; only the status and used-by cells differ |
| `ExecC2Gate-candidate-sources-amendment.txt` | appended directly after the r83 `- Round-83 S117 added …` bullet, **no blank line** (r82/r83 are contiguous bullets) |
| `ExecC2Gate-candidate-province-line.txt` | end-of-file PROVINCE.md amendment line, shaped like the r83/F59 line; not read by any counter, provided for the L1's admission |
| `ExecC2Gate-candidate-knowledge-expected-line.txt` | one line, inserted after `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` (line 69), before `osv-high-quality-record-import-bar.md` |

## Risks and notes

- The receipts are bound to the draft digest `0f9c1486…`; if the entry is edited after this gate, B8 and the mirror B3 must be re-run (the counter executes the entry's own `recheck:` line).
- Mirror B1/B2/B7 are simulations over exact candidate bytes, not measurements at the landing commit; the remaining landing-time limbs are the real `git diff <freeze> <landing> -- corpus/SOURCES.md` (B1), the landing tree's `ls` (B2) and the fleet `--root` census (B7).
- No mirror execution touched the working tree: `frontier-recheck-count` runs each entry's line with `cwd=$S/m`, and entries whose line starts `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` re-ran `source-recheck.py` read-only against the live manifests.
- The README amendment block adds a coverage-map area row that restates the entry's scope; the frontier counter reads only `| F<n> |` rows, so it does not affect the census, but an L1 preferring no duplicate prose can drop the area table and keep the amendment paragraph and F60 row.
- The live `corpus/SOURCES.md` still carries S118 as `queued`/`—` (freeze state); nothing in this seat changed it.
- Scratch deleted before yield; no host configuration, package or service was touched.
