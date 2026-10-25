# ExecEntryF13 — round 29 wave 1

## Scope and result

Implemented the F13 entry at `corpus/knowledge/program-severity-ladders-and-reward-scales.md` only. Final entry SHA-256: `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6`.

Header source ids are S043, S044, S045; `verified-at: 2026-10-25`; `ground: F13`; one executable recheck chains three separate `source-recheck.py --source` invocations from the lane-root `cd`. The body records the VRT P1–P5 labels and a verbatim <25-word excerpt from its override sentence; HackerOne's asset-control rule and per-asset DoS/per-finding same-issue reward limits; the `idor` → CWE-932 mapping and explicit `cwe: null` examples; falsifiable checks, rejected over-generalizations, platform attribution, and documentation-only boundary. `## Limits` names the non-adoption of CNVD 众测 and BILISRC and the staged S032/S033 → lane S044/S045 document remapping.

## Recheck evidence

Ran from the lane root against `corpus/source-snapshots/round-29/manifest.json` after the final entry bytes were written:

- S043: exit **0**; Q1–Q4 each `occurrences=1`, with verified anchors 31, 40, 170, and 92 respectively.
- S044: exit **0**; four quote assertions OK, each `occurrences=1`.
- S045: exit **0**; four quote assertions OK, each `occurrences=1`.

The CWD-independent recheck command passed `bash -n` and ran successfully from `/tmp` after the final entry bytes were written; each source invocation exited 0. Capture/manifest pins: S043 `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199`; S044 `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf`; S045 `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86`; manifest `910608e6bba69b32423a260332853e28f737affeaeb9011f6c9faef6702fb16a` (ExecManifestC2 receipt).

## Retained evidence, caveats, and handoff

- The S043 capture receipt records the initial raw API fetch and the later deterministic extraction of record 3787452's `new_policy` into the final 204-line snapshot. This gives verifiable line anchors; the final manifest reports all 12 assertions exactly once with anchors verified. Its S045 locations use corrected JSON paths (`$.content[5].children[2]` and `$.content[6].children[8]`).
- `corpus/README.md`, `corpus/SOURCES.md`, and `SKILL.md` are owned by other seats and intentionally unchanged here. No tests/build/lint were run; no tools installed. No commit was made (lane bounds prohibit Git index/jj-state writes).
- F13 entry presence was notified to `ScribeReadmeC2-2` and `ExecRecheckAudit`; manifest occurrence/anchor concern was reported to `ExecManifestC2`, which corrected the anchors before the final recheck.
