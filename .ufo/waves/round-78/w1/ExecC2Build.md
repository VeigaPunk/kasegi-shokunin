# ExecC2Build — round 78 w1, C2 landing set (prepared post-state bytes, no lane edits)

Seat: ExecC2Build (leaf executor). Freeze commit 2d81fe84506b323fb32beb137d5bd21db6a5c13d
(= lane HEAD), base 0687cca8645884aba30c8eb5fa2d8ecaca7245cf. Verified `git diff --stat
0687cca8 -- corpus/SOURCES.md corpus/instruments/knowledge-expected.txt corpus/README.md
PROVINCE.md` is empty: all four target files are byte-identical between base and HEAD, so
"current tree" = base for every file prepared here.

## Files written (all under .ufo/waves/round-78/w1/)

| file | bytes | sha256 (first 16) | rule | change |
|---|---|---|---|---|
| c2/SOURCES.md | 205,413 | 7ab76a9b1718df0a | B1 | S112 row only: status `queued`→`mined`, used-by `—`→`corpus/knowledge/osv-post-batch-query-contract.md` (one line changed; diff −1/+1) |
| c2/knowledge-expected.txt | 4,830 | 86daa06ab4f101c2 | B2 | +1 line `corpus/knowledge/osv-post-batch-query-contract.md` between osv-affected-range-events.md and osv-post-v1-query-contract.md; 93→94 lines, 91→92 .md rows |
| c2/README.md | 133,516 | 24431ead3019ac7b | B3 | append-only `## Round-78 admission — coverage map row and Frontier F54 (2026-11-05)` section (+9 lines: R6 intro, coverage-map row, `| F54 |` frontier row, r78 amendment line) |
| c2/PROVINCE.md | 33,605 | 357ce606225a22d6 | wave spec | +1 end-of-file line `[r78 Frontier amendment, appended 2026-11-05, end-of-file append per R6] F54 — … admitted round 78 on source S112 …` |
| c2/bookkeeping.txt | — | — | item 4 | instrument file-list findings |

All four were staged with `cp -p` from the tree, then edited surgically; the L1 copies them
verbatim. `diff -u` sizes (tree → prepared, saved during the run, reproducible):
SOURCES.diff 11 lines (−1/+1) · knowledge-expected.diff 10 (+1) · README.diff 20 (+9) ·
PROVINCE.diff 8 (+1). Zero removed lines outside the SOURCES row rewrite; both appended files
end with a single trailing newline.

## Rule mapping
- **B1** — SOURCES.md: exactly one changed row (S112), zero rows added/removed;
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 112 before and after (measured).
- **B2** — knowledge-expected.txt: 94 lines / 92 `.md` rows; `LC_ALL=C sort -c` clean over the
  .md rows and over the whole file (measured); row matches the to-be-landed entry name.
- **B3** — README.md: `grep -cE '^\| F[0-9]+ \|'` goes 53→54; the F54 row parses under
  FRONTIER_ROW/FRONTIER_SOURCES (topic/status/entry cells contain no `|`; sources cell `S112`
  is registered); B3's full PASS run still needs ScribeEntry's entry file and is the parent's
  gate.
- PROVINCE.md satisfies the seat's Frontier-line item; no C2 counter reads it (see below).

## Deviation from seat wording (routed, evidence-backed)
Seat item (1) specified used-by `osv-post-batch-query-contract.md (F54)`. Prepared instead:
`corpus/knowledge/osv-post-batch-query-contract.md`. Reason: `scripts/sources-census.sh`
E11 (:559-569) requires every comma-separated used-by cell of a mined row to be an existing
repo-relative path (`[ -e "$dir/$path" ]`); the `(F54)` form deterministically emits
`E11 … missing used-by osv-post-batch-query-contract.md (F54)` and breaks frozen **B7**
(validate exit 0 at landing). No registry row uses an F-suffix used-by; claims.json B1 words
the change as "used-by —->the new entry" without pinning a format. `grep -n
'osv-post-batch-query-contract.md (F54)'` on the prepared file → no match, confirming the
seat-literal form was not kept.

## Drift found
1. **S112 anchor cell cites round-77 artifacts**: the frozen row names
   `corpus/source-snapshots/round-77/S112.txt` and "13 pinned quotes in
   corpus/source-snapshots/round-77/manifest.json", while the freeze carries
   `corpus/source-snapshots/round-78/S112.txt` + `round-78/manifest.json` (7 narrowed quotes).
   Both files exist on disk; `sha256sum` of both S112.txt copies = f3ca04652e444125…0907
   (byte-identical), so no dangling path. B1 permits only the two cell changes, so the anchor
   cell was left byte-identical; the round-78 manifest is the claim-bearing one (claims.json
   `manifest` field). Flagging for L1 awareness only.
2. Lane `git status --porcelain` = 7 untracked entries, all `.ufo/waves/round-78/w1*` wave
   dispatch/dispatched/wave-dir files; no tracked-file drift; nothing outside .ufo/ touched.

## Mirror check (item 5) — S=/fast/scratch/hyaku/kasegi-r78/ExecC2Build, TMPDIR=$S/tmp
Fixture: `$S/mirror-root/kasegi-shokunin/{corpus (cp -a of lane corpus), SKILL.md}` +
PROVINCE.md, with the four prepared files applied over the copy, plus a scratch-local
`shokunin.conf` (`LANES="kasegi|kasegi-shokunin|…"`) so the seat's command shape
`--root $S/mirror-root kasegi` resolves to the mirror only (build_roster dies without a conf;
a conf in scratch is a scratch write). Registry count and validate, in order:

- `sources-census.sh census --root $S/mirror-root kasegi` → rc=0:
  `rows=112 tier.A=101 tier.B=5 tier.C=6 status.mined=92 status.queued=1 status.rejected=19
  FLEET missing=0` — mined 91→92, queued 2→1 (S112 flipped; S111 stays queued), as intended.
- `sources-census.sh validate --root $S/mirror-root kasegi` → rc=1 with exactly seven lines:
  the six inherited W04 warnings (S028, S029, S072, S076, S080, S085 — byte-matching B7's
  allowed list) plus the single **documented expected mismatch**:
  `E11 S112 missing used-by corpus/knowledge/osv-post-batch-query-contract.md` — the entry is
  absent because ScribeEntry supplies it at landing; after landing, E11 resolves and validate
  exits 0 with only the six W04 → B7 green. No other E/W code fired.
- Lane untouched: `git status --porcelain` identical before/after the census runs; census
  writes only stdout (selftest temp under TMPDIR, cleaned — $S/tmp empty after the run).

## Bookkeeping (item 4) — see c2/bookkeeping.txt
Filename unused; frontier-recheck-count.py reads exactly corpus/README.md frontier rows,
corpus/SOURCES.md registry, and each row's entry file (plus the entry-internal `source:`/
evidence/`recheck:` line); it does not read knowledge-expected.txt (that is recheck-audit.py's
input) nor PROVINCE.md. Per-entry bookkeeping = the three prepared files + ScribeEntry's entry
file itself; no fourth file exists.

## Tooling record
No tools installed or upgraded (none needed: bash/coreutils, diff, grep, python3 already
present; pacman pause respected). No git/jj writes anywhere — only read-only `git rev-parse`,
`git cat-file -t`, `git diff --stat`, `git status --porcelain` inside the lane. Scratch
deleted before yield; no counter output written under /tmp.

## Not done here (other seats / parent gates)
Entry prose (ScribeEntry); B0/B4/B5 capture-manifest recheck; B6 distinctness sweep; B3 full
census PASS and the lane gate suite (parent owns post-integration execution).
