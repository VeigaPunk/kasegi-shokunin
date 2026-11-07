
## Round-84 admission — coverage map row and Frontier F60 (2026-11-06)

Appended amendment (R6): the round-84 entry `corpus/knowledge/osv-gcs-data-dump-layout.md` (Frontier F60, source S118) rests on the OSV.dev project's own "Data sources" page at https://google.github.io/osv.dev/data/, captured `corpus/source-snapshots/round-84/S118.txt` (sha256 e824a735...5359, 129 lines, 5820 snapshot bytes, 6 pinned quotes), manifest `corpus/source-snapshots/round-84/manifest.json`. The coverage map above is not edited in place (R6); the coverage-map row is appended here, and the F60 frontier row follows.

| Area | Entry | Source basis |
|---|---|---|
| What the OSV.dev GCS data dump holds and how it is laid out, as the OSV project's own Data sources page states it: the full-database zip that includes withdrawn records, per-record JSON paths under each ecosystem directory, the [EMPTY]/ directory for ecosystem-less records, per-ecosystem modified_id.csv rows without the directory prefix, colon-suffixed ecosystems folded into their base directory, and the stopped export of prefixed ecosystem entries (round 84) | knowledge/osv-gcs-data-dump-layout.md | S118, the OSV.dev Data sources page's own text, opened 2026-11-06 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F60 | OSV.dev GCS data-dump layout — the full-database zip includes withdrawn records, one JSON object per record under its ecosystem directory, the [EMPTY]/ directory for ecosystem-less records, per-ecosystem modified_id.csv rows without the ecosystem directory prefix, colon-suffixed ecosystems folded into their base directory, and prefixed-ecosystem exports stopped | admitted | knowledge/osv-gcs-data-dump-layout.md | S118 | Read the six layout clauses at their pinned lines (S118.txt:102 the full zip includes withdrawn; :104 the per-record path and the [EMPTY]/ directory; :114 the per-ecosystem prefix omission; :121 the folded colon suffix; :123 the stopped prefixed exports); the source list and licences (:31-60), the converted-data and covered-ecosystems lists (:61-96), the top-level modified_id.csv format and order (:109-119; F59 holds the FAQ statement of the same file) and the ecosystems.txt listing (:122) stay unclaimed. |

[r84 amendment, appended 2026-11-06] The frontier as of round 84 is F01-F60 admitted: F60 at round 84. The C2 admission claims six export-layout statements of S118 only; post-import record handling stays F59, the import bar stays F58, the import-findings endpoint stays F57, and the source list, licences and covered-ecosystems list are not claimed.
