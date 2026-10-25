# ExecManifestC2 — round 29 wave 1

## Scope and outcome

Created `corpus/source-snapshots/round-29/manifest.json` for S043, S044, and S045. All three paths match their source ids, with four quote assertions per record. S043 now binds the record-scoped HackerOne policy capture and anchors its assertions to the decoded capture's line numbers; Q4 is the policy's per-finding severity/reward statement. S044 covers VRT baseline severity, P1–P5 labels, and context overrides. S045 covers the CWE-932 mapping and null-mapping examples with corrected JSON paths.

Final pinned file set:

| File | Bytes | SHA-256 |
|---|---:|---|
| `corpus/source-snapshots/round-29/manifest.json` | 3,857 | `910608e6bba69b32423a260332853e28f737affeaeb9011f6c9faef6702fb16a` |
| `corpus/source-snapshots/round-29/S043.txt` | 7,298 | `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199` |
| `corpus/source-snapshots/round-29/S044.txt` | 8,187 | `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf` |
| `corpus/source-snapshots/round-29/S045.txt` | 14,575 | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` |

## Exact retained evidence

Ran the single-valued `source-recheck.py --source` separately for each id from the lane root:

- S043 — exit **0**; Q1 `occurrences=1 anchor=31-ok`; Q2 `occurrences=1 anchor=40-ok`; Q3 `occurrences=1 anchor=170-ok`; Q4 `occurrences=1 anchor=92-ok`.
- S044 — exit **0**; Q1–Q4 each `occurrences=1`.
- S045 — exit **0**; Q1–Q4 each `occurrences=1`.

The reported per-capture timestamp is unavailable; the earlier UTC clock read after capture work (`2026-10-25T18:17:20Z`) is not claimed as the fetch timestamp.

## Risks / blockers

None known for manifest assertions: all twelve report exactly one occurrence, and every declared S043 anchor verifies against the final record-scoped capture. Capture files were not changed by this manifest owner; S043's record-scoped replacement was present before this final pin/recheck.
