# MutJunk — round-39 wave 2 (falsify), seat receipt

Seat: MutJunk (mutation-tester, leaf; no subagents spawned). Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Fleet root and /home/vgpnk/Projects/shokuknow: read-only, untouched. No mutating git/jj command run anywhere; only read-only git (`rev-parse`, `status --porcelain`, `ls-files --error-unmatch`, `diff --quiet`).

## Item

Positive control for the junk instrument: on the committed capture, build a manifest where one fabricated junk claim is REPLACED by the true quote; run source-recheck and record that the true quote is `OK occurrences=1` while the other three remain MISMATCH (exit 1). Then a manifest with all four true quotes must exit 0. This proves the instrument discriminates claims, not just files. Deliverable: `.ufo/waves/round-39/wave2/MutJunk.controls.txt`.

I am not the author of the work under attack (wave-1 C2 capture/junk controls were Exec seats; I read them at HEAD).

## What was run (actual commands and outputs; full transcripts in the deliverable)

All runs used `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py` with `--manifest <path>`; scratch workdir `/fast/scratch/hyaku/kasegi-r39/MutJunk/work` held a byte-identical copy of the committed capture `corpus/source-snapshots/round-39/S057.txt` (sha256 `11c8d6d6…` both sides) because the instrument resolves `path` relative to the manifest directory.

- RUN A — committed manifest `corpus/source-snapshots/round-39/manifest.json --source S057`: 4x `OK normalized=markup-whitespace occurrences=1 anchor=N-ok` (N=12/132/136/184), exit 0. Baseline green on committed bytes.
- RUN B — frozen junk manifest `.ufo/waves/round-39/c2-controls/junk-manifest.json` (4 fabricated claims J1–J4), copied unmodified into the workdir: 4x `MISMATCH reason=quote-not-found`, exit 1. Reproduces the frozen `c2-controls/junk-f22-recheck.txt` shape exactly.
- RUN C — **item control**: mixed manifest `mixed-J1Q1.json` (fabricated J1 replaced by true capture Q1; quote bytes spliced from the committed manifest, verified identical): `S057:J1 OK normalized=markup-whitespace occurrences=1` while J2/J3/J4 remain `MISMATCH reason=quote-not-found`, exit 1.
- RUN D — position probe `mixed-J4Q4.json` (J4 replaced by true Q4): `S057:J4 OK occurrences=1` while J1/J2/J3 MISMATCH, exit 1. Discrimination is per claim, not per position.
- RUN E — all-true `all-true.json` (J1–J4 replaced by true Q1–Q4 incl. declared anchors 12/132/136/184): 4x `OK occurrences=1 anchor=N-ok`, exit 0.
- RUN F — `--selftest`: `selftest cases=10 failures=0`, exit 0.

## Verdict

Positive control SATISFIED. The instrument discriminates claims, not just files: a manifest mixing one true and three fabricated claims is rejected (exit 1) with the true claim individually reported `OK occurrences=1`; the all-true manifest passes (exit 0). No defect found in the junk instrument's discrimination behavior on the committed capture.

## Frozen-byte cross-checks (attack target identity)

- instrument sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` == frozen receipt's instrument line → no instrument drift since wave-1 freeze.
- junk-manifest.json sha256 `9dafce3647086cd082ab5ebb53d9b9601fd43ff76f701e595c5503afc388470a` == frozen receipt's digest line.
- committed manifest.json sha256 `432f2205b368acb39d620bb85fe81c0fd6ccb345dd0878661478085ac1ce6659` == frozen receipt's `capture_seat_manifest` sha.
- capture sha256 `11c8d6d6…` == manifest-declared sha == frozen receipt's capture sha.
- `git ls-files --error-unmatch` ok for S057.txt, manifest.json, source-recheck.py, junk-manifest.json, junk-f22-recheck.txt; `git diff --quiet HEAD` over those paths → clean at HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37`.

## Observations (not defects)

1. Run from its committed location (`.ufo/waves/round-39/c2-controls/`), the frozen junk manifest alone reports `S057:source UNAVAILABLE reason=missing` exit=2: `path` resolves relative to the manifest directory and the capture lives in `corpus/source-snapshots/round-39/`. The frozen receipt documents the designed work-dir run (capture beside manifest); reproduced as RUN B. Reproducibility note only.
2. Lane dirty entries at my run time were only wave-2 dispatch artifacts (`kasegi-r39-falsify.ready*`, `wave2-dispatch.json`, `wave2-run.err`, `wave2/`) — orchestrator/sibling writes, untouched by this seat.

## Tooling

No tools installed or upgraded (python3 3.14, git, coreutils sufficed); tooling authorization not exercised.

## Writes

- `.ufo/waves/round-39/wave2/MutJunk.controls.txt` (deliverable, 12125 bytes, sha256 `898fb50df4b782e246e065462c402c21bea910f7374ae866f01147b05456e314`)
- `.ufo/waves/round-39/wave2/MutJunk.md` (this receipt)
- Scratch `/fast/scratch/hyaku/kasegi-r39/MutJunk/` removed before yield.

No other file in the lane repo, fleet repo, sibling repos, or source trees was created, modified, or deleted.
