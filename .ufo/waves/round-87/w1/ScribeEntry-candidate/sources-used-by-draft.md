# S124 / S125 registry `used-by` change text (draft for the L1)

Scope: the two SOURCES rows the round-87 C2 claim opened, `corpus/SOURCES.md:136` (S124) and
`corpus/SOURCES.md:137` (S125). CORPUS.md rule 2 permits only `status`, `recheck` and `used-by`
to change in place, and requires each change to be logged old → new in the round lesson.

Measured cell values (11-column table, header at `corpus/SOURCES.md:5`, so `used-by` is the
11th cell and `status` the 8th):

| revision | S124 `status` | S124 `used-by` | S125 `status` | S125 `used-by` |
|---|---|---|---|---|
| `git show 132e16c588a2424c06b5ca15ea01fce1ee9a396d:corpus/SOURCES.md` | `queued` | `—` | `queued` | `—` |
| working tree at the time of writing | `mined` | `corpus/instruments/capture-secret-scan.py` | `mined` | `corpus/instruments/capture-secret-scan.py` |

## The change

If the C2 landing's in-place edit (`queued` → `mined`, `—` → the instrument path) is kept, the
change this entry needs is an append to the same cell:

```text
S124 (corpus/SOURCES.md:136)  used-by  old: corpus/instruments/capture-secret-scan.py
                                      new: corpus/instruments/capture-secret-scan.py, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md
S125 (corpus/SOURCES.md:137)  used-by  old: corpus/instruments/capture-secret-scan.py
                                      new: corpus/instruments/capture-secret-scan.py, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md
```

If the landing edit is instead deferred, both fields move at once:

```text
S124 (corpus/SOURCES.md:136)  status   old: queued   new: mined
                              used-by  old: —        new: corpus/instruments/capture-secret-scan.py, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md
S125 (corpus/SOURCES.md:137)  status   old: queued   new: mined
                              used-by  old: —        new: corpus/instruments/capture-secret-scan.py, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md
```

Commas separate `used-by` paths (CORPUS.md field definition); the two paths are ordered
instrument first, entry second, matching the order in which the round cites them.

## Lesson log line (rule 2)

```text
SOURCES in-place edits, r87: S124 used-by <old> -> <new>; S125 used-by <old> -> <new>; both rows' status queued -> mined iff the used-by cell is non-empty (CORPUS.md status definition).
```

## Census after the edit

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

Measured: `125` rows on both sides. `git show 132e16c:corpus/SOURCES.md` reads
`mined=103 queued=3 rejected=19` (S111, S124, S125 queued); the working tree, after the landing
edit, reads `mined=105 queued=1 rejected=19` (S111 is the remaining `queued` row). The
used-by-existence loop prints nothing on both sides.

**Order dependency.** That last loop exits non-zero-in-spirit (prints `missing: …`) if the
`used-by` cell names this entry before the entry file exists. Land the entry file in the same
commit or before the row edit, then re-run the loop; it must print nothing.

**Out of scope of this draft.** Claim 1 also cites S122 (`corpus/source-snapshots/round-86/S122.txt:1`),
whose row currently reads `used-by: corpus/practice/curl-ibb-h1-1997312/report.md`. Adding the new
entry there is a third cell the ticket did not assign; the L1 should decide it, and if it is taken
the append is `corpus/practice/curl-ibb-h1-1997312/report.md, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`.
