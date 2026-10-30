# R47ExecMergeGuard

## Results

- Assimilation guard completed verbatim. Receipt files: `.ufo/waves/round-47/assimilation/reg-ids`, `staged-ids`, `collisions`.
- Printed counts: `reg-ids 74`; `staged-ids 94`; `collisions 44`. Collision IDs are S031–S074 inclusive (listed in the `collisions` receipt). This is a positive collision finding; the guard itself does not establish whether these repeated IDs are intended or erroneous.
- Indented-row fixture: with fixture registry containing `  | S002 | fixture |` and staged IDs containing `S002`, the exact `^ {0,3}\|[[:space:]]*S[0-9]{3,}` extraction yielded `reg-ids: S002`, `collisions: S002`, `fixture collision count: 1`. This demonstrates the intended 2-space-indented row is detected. Control: an empty registry produces no extracted IDs and therefore no comm intersection; no-output collision is the do-nothing baseline.
- Absent-defect register: awk filtered rows whose lane cell is `` `kasegi` `` and counted 8 rows. Kasegi rows exist: evidence `.ufo/waves/corpus-expansion-1/absent-defect-register.md:99-100,322-326` (8 total). Command: `awk -F'|' '$2 ~ /`kasegi`/ {n++} END{print n+0}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` → `8`. The accessible seat contract specifies the row-count slice but does not include an awk expression; this direct lane-cell filter was used.

## Evidence / limits

Command outputs above are from the required guard and scratch fixture; scratch was removed on shell exit. Disk guard reported `/fast/scratch/hyaku` 375.3G free (its status command timed out at 30s after printing the available-space table). No files in shokuknow were changed; no adoption or verdicts beyond the requested row count were made. No package/tool installation. No tests/builds run.