# ExecBeforeVerify — round-30 wave-1 freeze-authenticity receipt

Seat: `ExecBeforeVerify` (L2 executor/leaf, hyaku run-7 inline spawn). Lane: `kasegi-shokunin`.
Fleet root (read-only): `/home/vgpnk/Projects/shokunin`. Lane write scope: this lane only.
Measured at: 2026-10-25T18:43–18:51Z (UTC stamps per run block).

Revisions:
- Lane base `a94871315cafa368f79c17d8c62d71fddd967986` (`git cat-file -t` → commit).
- Claims-freeze commit `3c5573541300ba0fd3d89372dda3d841172eaa3f` (commit subject "round-30: claims freeze + before receipts (C1 harness/Q9 fixtures; C2 census-before)", 2026-10-25 15:45:26 -0300); `git merge-base --is-ancestor 3c557354 HEAD` → exit 0.
- Lane HEAD at measurement: `002e92ce07ed398334ef7cd8ca08d3fd99631351` (wave-1 spec + dispatch).

## 1. Receipt integrity — freeze commit vs working copy (byte-identical)

`sha256sum` on working-copy files vs `git show 3c557354:<path> | sha256sum`; `diff` of both sides empty for all four.

| File | sha256 (freeze = working copy) |
|---|---|
| `.ufo/waves/round-30/claims.json` | `68d77757c71f1779be89ac97efe3f1299a5858187c7f95e06d9da4e52cae523b` |
| `.ufo/waves/round-30/c1-controls/before.txt` | `88e8fa237b79c395e7492b32cd03a9e9b80407a6cd2d556eb67ef62d57119c52` |
| `.ufo/waves/round-30/c2-controls/before.txt` | `6ab84e65e99eaa939fcbbf0d84b1462178a627161815e7ca77dec337d7ba0705` |
| `.ufo/waves/round-30/census-before.txt` | `1b6e550107eeb8a936802c0ba1fca32dcb1dfab08784aea4826231ddfa449bd4` |

`claims.json` parses: `python3 -c "import json,sys; d=json.load(sys.stdin); print(...)"` →
`JSON_OK 2 30 a94871315cafa368f79c17d8c62d71fddd967986` (2 claims, round 30, base a94871315).

## 2. C1 controls — four probes reproduce the committed before receipts

Probes run twice: (a) on the live working tree (15:xxZ, before wave edits landed), and (b) on a fully isolated export of the freeze commit (`git archive 3c557354 | tar -x -C /tmp/freeze-verify`). Both runs reproduce the receipt outputs; the exported-tree run is byte-fresh and immune to in-flight wave edits.

| Probe (command) | Recorded in `c1-controls/before.txt` | Measured (exported freeze tree) | Match |
|---|---|---|---|
| A1 `frontier-recheck-count.py --root …/harness-root-a1` | FileNotFoundError traceback (line 65 `entry_contract`, `zz-missing.md`), `a1_exit=1`, no named-row marker | identical traceback class + `a1_exit=1` (path prefix differs: `/tmp/freeze-verify/…` vs lane root — same missing-file, same code line) | ✓ |
| A2 `frontier-recheck-count.py --root …/harness-root-a2` | `PASS F98/F97 knowledge/dup-entry.md ids=S003 exit=0` ×2, `entries=2 pass=2 exit=0`, `a2_exit=0` | byte-identical, `a2_exit=0` | ✓ |
| B1 `source-recheck.py --manifest …/q9/manifest-b1.json --source S043` | `S043:sha256 OK`, `S043:Q1 OK normalized=markup-whitespace occurrences=1`, `b1_exit=0` | byte-identical, `b1_exit=0` | ✓ |
| B2 `source-recheck.py --manifest …/q9/manifest-b2.json --source S045` | `S045:sha256 OK`, `S045:Q1 OK occurrences=2 anchor=MISSING`, `b2_exit=0` | byte-identical, `b2_exit=0` | ✓ |

Fixture provenance (committed at freeze; `git ls-tree -r 3c557354 .ufo/waves/round-30/`):
- `harness-root-a1/corpus/README.md` only — no `knowledge/` dir; the admitted-row entry `zz-missing.md` is absent (A1 trigger).
- `harness-root-a2/corpus/source-snapshots/round-24/{manifest.json,S003.txt}` + `knowledge/dup-entry.md` (duplicate-target trigger).
- `q9/manifest-b1.json`: id `S043`, path `S045.txt` (stem mismatch by construction), sha256 `f583a396…0f86` = round-29 S045 capture; quote `{ "metadata": … "cwe":` matches only under `normalized=markup-whitespace` (raw single-line grep: 0; the capture is pretty-printed JSON → the instrument's normalization collapses whitespace → `occurrences=1`).
- `q9/manifest-b2.json`: id `S045`, path `B2.txt`, sha256 `55124b0e…5fb06`; quote `vulnerability rating taxonomy crosswalk node` occurs **2** times in `B2.txt` (`grep -cF` → 2) with no anchor → `occurrences=2 anchor=MISSING`.

Instrument digest binding: `git show 3c557354:corpus/instruments/frontier-recheck-count.py | sha256sum` →
`c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261`; `source-recheck.py` → `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` — both equal the digests recorded in `c1-controls/before.txt` lines 3–4. Instruments were byte-unchanged base → freeze.

## 3. C2 census — all before values reproduce

On the exported freeze tree (`validate --file /tmp/freeze-verify/corpus/SOURCES.md` plus in-tree counts):

| Value | Receipt (`census-before.txt` / `c2-controls/before.txt`) | Measured | Match |
|---|---|---|---|
| census exit | 0 | `census_exit=0`; stdout `W04 S028/S029 duplicate url …` warnings + `ok <lane>/corpus/SOURCES.md` — byte-identical shape | ✓ |
| registry rows | 45 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 45; `census` mode → `rows 45` (tier A 42 / B 1 / C 2; mined 33 / queued 9 / rejected 3) | ✓ |
| frontier admitted | 13 | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → 13 | ✓ |
| entries citing S046/S047 | 0 | `grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md | wc -l` → 0; registry rows S04[6-7] → 0 | ✓ |
| harness | entries=16 pass=16 exit=0 | `python3 corpus/instruments/frontier-recheck-count.py` → `entries=16 pass=16 exit=0`, `harness_exit=0`, all 16 PASS rows incl. F13 `ids=S043,S044,S045` | ✓ |

## 4. Observed wave-state notes (context, not receipt defects)

- During verification the editing wave was active: after the initial live probe runs, `git status --porcelain` showed ` M corpus/instruments/frontier-recheck-count.py` and untracked `.ufo/waves/round-30/{assimilation/,c1-controls/before-run-2.txt,c1-controls/mutants/,kasegi-r30-build.ready*.dispatched,plan.err,run.err,wave1/*}` + `corpus/source-snapshots/round-30/`. Re-running the B1/B2 probes later returned `S043/S045:manifest MISMATCH reason=stem-mismatch` (fix limb landing) and A1 returned `FAIL F98 … problems=missing-entry`; A2 momentarily showed a `NameError` in the partially edited instrument. These are wave-in-flight states of the working tree — they do not affect the frozen receipts, which are byte-verified at the freeze commit.
- Two live census runs returned silent `exit 1` with zero stdout/stderr while peers were concurrently editing the lane corpus; 7 runs on quiescent/exported trees (2 + 5-loop + exported) all returned `exit 0` with receipt-identical output. The transient is recorded as an observed anomaly during concurrent edits; it is not attributable to the frozen bytes.
- No tool was installed (no pacman/npm/cargo/uv action). No writes outside the lane report path; git operations were read-only (`show`/`ls-tree`/`cat-file`/`merge-base`/`status`/`rev-parse`); corpus entries were documentation-only; no live target contacted.

## 5. Conclusion

The freeze receipts are intact and authentic at `3c557354`:
1. `claims.json` parses and is byte-identical to the working copy (fixed 68d77757…).
2. All four C1 controls reproduce the committed `before.txt` outputs on an isolated freeze-tree export (A1 exit 1 FileNotFoundError traceback, A2 exit 0 pass=2 duplicate, B1 exit 0 occurrences=1, B2 exit 0 occurrences=2 anchor=MISSING); instrument digests at freeze equal the receipt digests (`c8a62888…` / `9fe6a4a0…`).
3. C2 census-before values reproduce: census exit 0, rows 45, frontier admitted 13, entries citing S046/S047 0, harness 16/16 exit 0.
