# ExecC2Gate — C2 landing gate on a scratch mirror (round 81, attempt 1)

Wave: one v1 wave, 13 seats. This seat: pre-landing C2 gate only; no lane, corpus or instrument byte edited.
Freeze base: `7ad3118c86ee14fde433d73671cc407668533cec` (lane HEAD matched the freeze at seat start).
Scratch: `/fast/scratch/hyaku/kasegi-r81/ExecC2Gate` (removed before yield).

## Mirrors

- **m** = `git -C <lane> archive 7ad3118c | tar -x -C m`, then: entry copied from
  `.ufo/waves/round-81/w1-input/osv-importfindings-record-quality-feedback.md`; `S115` row flipped
  `queued`→`mined`, used-by `—`→`corpus/knowledge/osv-importfindings-record-quality-feedback.md`;
  one row appended to `corpus/instruments/knowledge-expected.txt`; one F57 row added after the F56 row.
  Mirror-only substitution: the entry's `recheck:` `cd` path rewritten to `m` (see Risk 1).
- **m2** = the same freeze archive + the bytes the L1 had **already written into the lane working tree**
  (`corpus/README.md` `4b7c60da…`, `corpus/SOURCES.md` `0eeac9fc…`, `knowledge-expected.txt`, entry
  `2895011e…`). Read-only copy; the lane was never written by this seat.

Exact rows and diffs: `.ufo/waves/round-81/w1/ExecC2Gate-rows.txt`. Raw outputs:
`.ufo/waves/round-81/w1/ExecC2Gate-receipts/` (`b0-b3-b4-census.txt`, `b5-b8.txt`, `b6.txt`,
`b6-literal-sweep.py`, `m2-l1-integrated-bytes.txt`, `b1-sources-diff.txt`).

## Gate results (mirror m unless stated; every line below is copied from a receipt)

| limb | command | output | rc |
|---|---|---|---|
| B0 | `source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115` | `S115:sha256 OK` + six `OK occurrences=1 anchor=<n>-ok` at 25,32,34,36,37,38 | 0 |
| B3 | `frontier-recheck-count.py` | `FRONTIER-CENSUS rows=57 admitted=57 closed=57 problem-rows=0 registry=115` · `FRONTIER-PASS F57 ids=S115` | 0 |
| B4 | `capture-binding-check.py` | `AUDIT records=95 with_url=95 … orphans=1 orphan=S040-live.txt` · `records=95 bound=95 unbound=0` | 0 |
| B5 | `bash -c '<entry recheck, lane→mirror>'` from `foreign/` | `S115:sha256 OK` + six `anchor=<n>-ok` | 0 |
| B6 | six pinned quotes over the 94 other entries | `Q01..Q06 files=0` · `TOTAL_LITERAL_FILES=0` | 0 |
| B7 | `sources-census.sh validate --today 2026-11-06 --file m/corpus/SOURCES.md` | six inherited `W04` only, then `file ok` | 0 |
| B8 | `entry-gate.py --entry <entry> --manifest <lane-rel manifest> --source S115 --lane m` | `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok` · `ENTRY-GATE-RESULT pass` | 0 |
| B8 (landing form) | same, lane cwd, `--lane <lane>`, lane entry bytes | same line, `header=ok`, `ENTRY-GATE-RESULT pass` | 0 |
| B2 | `ls corpus/knowledge/*.md` / `knowledge-expected.txt` | 95 files, 97 lines (2 comments + 95 `.md`), set-diff empty, `LC_ALL=C sort -c` clean | — |
| B1 shape | `diff <(git show 7ad3118c:corpus/SOURCES.md) m2/corpus/SOURCES.md` | 115→115 registry rows; exactly one `<`/`>` pair, both the S115 line; plus one added `Round-81 S115 added …` prose bullet (not a registry row) | — |
| m2 (L1 bytes) | B0, B3, B4, B7, B2 | identical outputs to the table above, B3 `rows=57 … registry=115`, `unbound=0`, `file ok`, 95/97 `SET_EQUAL` | 0 |

The lane's own integrated bytes (m2) pass every limb; the lane's F57 row (README:1243) and my modelled
row both bind (`FRONTIER-PASS F57 ids=S115`) — integrate one, not both.

## Entry-content facts re-measured against the capture (depth:verifiability spot-check)

- `S115.txt` sha256 `e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f`, 44 lines,
  2224 bytes; manifest sha256 `7429df80bf425c8132b1325d0cd3b9e8527323f7e6eb61c31ce8b0774c5c05cf` — both
  exactly as the entry's Gate table states. `fetched_utc 2026-11-06T20:11:18Z`, url as claimed.
- Manifest quote word counts `14, 12, 23, 18, 1, 12` — identical to the entry's table.
- The three `Limits` greps (credential/rate-limit, pagination, error/status-code) each exit 1 on the capture.
- `Distinctness` subject sweeps over the 94 other entries: `importfindings`, `source.yaml`,
  `home database` each exit 1; the cited F51 lines hold what the entry says (`osv-post-v1-query-contract.md:31`
  is the case-sensitivity line quoting `S108.txt:53`; `:75` is the Limits bullet listing the experimental endpoints).
- Pinned snapshot lines 25/32/34/36/37/38 print the six claimed sentences; :39 is the case-sensitivity note,
  :41/:43 the sample and example response — all correctly left unclaimed.

## Risks / routed observations (no verdict change; r82 material)

1. **B8's header limb is lane-relative.** `man["_path"] = relpath(abspath(manifest), abspath(lane))`, and the
   expected `recheck:` line is rebuilt from `--lane`; an off-lane run therefore always reports `header=bad`
   unless the entry's `cd` path is rewritten (or the manifest sits under the same root). Measured: same
   byte-identical entry, `--lane m2` → `header=bad` rc1; `--lane <lane>` from the lane cwd → `header=ok` rc0.
   Consequence: the gate cannot be exercised on a byte-identical entry off the landing root — a future round
   should either add a `--manifest-rel`/path-normalisation or state in the predicate that the run is from the
   lane root. Also note `subprocess`-free pure read, so no other limb is affected.
2. **The lane working tree at the freeze commit is already dirty** (`M PROVINCE.md`, `M corpus/README.md`,
   `M corpus/SOURCES.md`, `M corpus/instruments/knowledge-expected.txt`, untracked entry). B1's "exactly one
   registry row changed, adds none, removes none" holds only over the committed landing tree; the S115 row and
   the expected-list insert I diffed are byte-identical to the lane's, and the extra `Round-81 S115 added`
   bullet in `corpus/SOURCES.md` is prose, not a registry row.
3. The entry's "16418 raw bytes before stripping" figure was **not** re-measured (this seat made no network
   call); it stands on `controls/c2-prefreeze-r81.txt`.
4. Cosmetic, no gate: the lane's F57 `next` cell names only `:39` as unclaimed; the r81 amendment line adds the
   request sample and example response. The F56 precedent carried the unclaimed set in the row itself.
5. `knowledge-expected.txt` holds two `#` comment lines, so a naive line-count comparison (97) against the entry
   listing (95) mismatches; the set-equal check is the correct one and passes.

## Tooling

Nothing installed, upgraded or reconfigured; no pacman/uv/npm transaction was run. No network fetch.

## Files written

- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate.md` (this report)
- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate-rows.txt`
- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate-receipts/b0-b3-b4-census.txt`
- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate-receipts/b5-b8.txt`
- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate-receipts/b6.txt`
- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate-receipts/b6-literal-sweep.py`
- `kasegi-shokunin/.ufo/waves/round-81/w1/ExecC2Gate-receipts/m2-l1-integrated-bytes.txt`

No blockers. No lane/corpus/instrument byte was modified; scratch removed.
