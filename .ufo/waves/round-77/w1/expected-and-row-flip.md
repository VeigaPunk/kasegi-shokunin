# DRAFT — corpus/instruments/knowledge-expected.txt line and corpus/SOURCES.md S112 cell flips for round 77 (ScribeEntry; NOT APPLIED)
# Status 2026-11-05: the L1 (KasegiR77) refused C2 at B6 distinctness, so neither the expected-list row nor the registry cell flips were applied. `corpus/instruments/knowledge-expected.txt` still holds 93 lines / 91 `.md` rows and the S112 registry row is still `queued` with `used-by —`. Retained as successor-round material.
# Placement of the expected-list row: INSERT, do not append. Insert the line below between line 67 (corpus/knowledge/osv-affected-range-events.md) and line 68 (corpus/knowledge/osv-post-v1-query-contract.md). The file is LC_ALL=C sorted (claim B2 requires `sort -c` clean); an end-of-file append places this row after zdi-disclosure-process-and-vendor-coordination.md and breaks the sort. Lines after 67 shift down one; no existing line's text changes.
# Expected after integration (if a successor round admits F54): 94 lines, 92 corpus/knowledge/ rows (base 93 lines, 91 rows).
# Sourcing: S112 (frozen capture, sha256 f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907); the entry path is corpus/knowledge/osv-post-v1-querybatch-contract.md.
==========
corpus/knowledge/osv-post-v1-querybatch-contract.md

# ---- corpus/SOURCES.md S112 row cell flips (old -> new) ----
# The S112 row is committed at corpus/SOURCES.md:124 with status `queued` and used-by `—`. Two cells change at a landing that admits F54; every other cell of the row stays byte-identical.
#
# status cell, old -> new:
#   queued
#   mined
#
# used-by cell, old -> new:
#   —
#   corpus/knowledge/osv-post-v1-querybatch-contract.md
#
# Registry-changes note for the round lesson (old -> new text, R8/R31 form):
#   old: - S112 row added (docs, scoped tier A, queued at the freeze, opened 2026-11-05, recheck 180d, used-by —); the capture corpus/source-snapshots/round-77/S112.txt (sha256 f3ca0465...0907, 216 lines, 4575 bytes, fetched 2026-11-05T12:22:10Z) and its manifest are committed with the row; the row's teaches cell names the queries-array payload, the ids-and-modified-only return shape, the input-matched ordering, the per-item version rules with the 400 Bad Request consequence and the per-query pagination semantics only.
#   new: - S112 row added (docs, scoped tier A, mined at the landing, opened 2026-11-05, recheck 180d, used-by corpus/knowledge/osv-post-v1-querybatch-contract.md); the capture corpus/source-snapshots/round-77/S112.txt (sha256 f3ca0465...0907, 216 lines, 4575 bytes, fetched 2026-11-05T12:22:10Z) and its manifest are committed with the row; the row's teaches cell names the queries-array payload, the ids-and-modified-only return shape, the input-matched ordering, the per-item version rules with the 400 Bad Request consequence and the per-query pagination semantics only. Status cell old -> new: `queued` -> `mined`; used-by cell old -> new: `—` -> `corpus/knowledge/osv-post-v1-querybatch-contract.md`; no other cell of the row changed.
#
# If F54 is refused again, neither cell flips: the row stays `queued` with `used-by —` and the registry-changes note above keeps the old text.
