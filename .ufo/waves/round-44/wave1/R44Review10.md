# R44Review10 — C2 coverage frontier assessment

## Finding

**No R44 C2 after-state is present at the inspected lane revision; no new coverage credit is supportable.** The frozen control names base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` and baseline 25 admitted frontier rows, 68 source registry rows, and 62 knowledge files (`.ufo/waves/round-44/controls/do-nothing.txt:2,9-13`). I independently ran the frozen-base commands:

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'
25
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
68
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree -r --name-only 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a corpus/knowledge | grep -c '\.md$'
62
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --name-status 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a..HEAD -- corpus/README.md corpus/SOURCES.md corpus/knowledge corpus/source-snapshots
[no output]
```

At inspected HEAD `66314015122b9aa32dc40f2f1815df56624c26d1`, the named production coverage paths have no committed diff from base: there is no F26, new corpus source/knowledge entry, or captured source delta in those paths. The visible frontier ends at F25 and the round-43 note explicitly says its frontier remains 25/25 (`corpus/README.md:591-612`). Thus the claim's strict conjunction (F26 + captured tier-A source + cited new knowledge entry + registry row + reject and independent admit/reject spot-check + passing SOURCES census; `.ufo/waves/round-44/claims.json:18-24`) is unfulfilled, not merely weakly evidenced. The do-nothing control is discriminating: current coverage paths are byte-for-byte unchanged from the frozen base, so the after-state cannot be credited.

## Severity / residual risk

Actionable C2 finding: the reviewed snapshot does not contain the coverage move. This is a snapshot-bound assessment, not a conclusion about later unobserved landing. No judgment on source quality or whether a future F26 is genuinely distinct is possible without the actual captured source, knowledge text, and registry row. No non-author spot-check or R44 census result is present in this reviewed snapshot.

## Verification gaps and provenance

Read-only. Exact commands and stdout above; no tools installed. No scratch directory was created, so no scratch cleanup was required. No LSP status/device was available in this lane; no semantic references/definition/diagnostics are claimed. Report path relative to kasegi lane: `.ufo/waves/round-44/wave1/R44Review10.md`.
