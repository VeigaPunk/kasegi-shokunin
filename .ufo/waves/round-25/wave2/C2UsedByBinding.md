# C2UsedByBinding — wave-2 falsification (round 25)

## Item under attack

Wave-1 claim (RowsScratch.md L38–45): "`used-by` names exactly the entries whose headers cite the row
… Result: S036, S038, S039 → both entries; S037 → JP entry only; S040 → crosswalk only."
Corollary receipts: RevSourceRows.md L52–62 ("`used-by` target missing | none … No row in this set has
a … `used-by` defect") and EntryCiscoCrosswalk.md L174–175 (crosswalk "must be added to their `used-by`
cells").

**Verdict: CONFIRMED — the wave-1 result is correct. No correction needed.**

Each row's `used-by` cell (SOURCES.md L42–46, column 11) names exactly the `corpus/knowledge/*.md`
entries whose `source:` headers cite that row, and no other path.

## Evidence — committed bytes at time of audit

`corpus/SOURCES.md` (uncommitted round-25 modification in worktree; rows S036–S040 at L42–46):

| row | used-by cell (col 11) | citing entries found | verdict |
|---|---|---|---|
| S036 | `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md, corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | `source: S036` at objects.md:3 and crosswalk.md:3 | exact |
| S037 | `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` | `source: S037` at objects.md:4 only | exact |
| S038 | objects.md + crosswalk.md | `source: S038` at objects.md:5 and crosswalk.md:4 | exact |
| S039 | objects.md + crosswalk.md | `source: S039` at objects.md:6 and crosswalk.md:5 | exact |
| S040 | `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | `source: S040` at crosswalk.md:2 only | exact |

## Commands, outputs, exits

Parse the five cells (exit 0):

```
$ python3 - <<'EOF'
for i,l in enumerate(open('corpus/SOURCES.md'),1):
    if l.startswith('| S0'):
        c=[x.strip() for x in l.split('|')]
        if c[1] in ('S036','S037','S038','S039','S040'):
            print(i, c[1], '| used-by =', c[11])
EOF
42 S036 | used-by = corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md, corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
43 S037 | used-by = corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
44 S038 | used-by = corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md, corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
45 S039 | used-by = corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md, corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
46 S040 | used-by = corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

Every `source:` header citing the five ids lane-wide (exit 0; 8 hits, all in the two named files):

```
$ grep -rn '^source:' corpus/ --include='*.md' | grep -E 'S03[6-9]\b|S040\b'
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:3:source: S036 — …
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:4:source: S037 — …
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:5:source: S038 — …
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:6:source: S039 — …
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:2:source: S040 — …
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:3:source: S036 — …
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:4:source: S038 — …
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:5:source: S039 — …
EXIT=0
```

Counter-matches the C2 harness (exit 0):

```
$ grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

Negative checks (both exit 1 — zero hits, as required):

```
$ grep -n 'S040' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md   # exit 1: objects does NOT cite S040 → correctly absent from S040's cell
$ grep -n 'products/bug-bounty\|S037' corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md   # exit 1: crosswalk does NOT cite S037 even by URL → correctly absent
```

Completeness over the corpus (exit 0): every `S036`–`S040` token outside the registry rows lives in
the two named entries, in `corpus/lessons/*.md`, `corpus/README.md` L50–51,211 and
`corpus/source-snapshots/round-25/manifest.json` — none of which are `corpus/knowledge` entries.
URL-level check finds no third entry citing the vendors' pages either.

## Why non-entry citations do not falsify

The registry's `used-by` domain is `corpus/knowledge/*.md` entries only — verified by extracting the
distinct paths in all 35+ cells: every value is a `corpus/knowledge/*.md` path or `—`. No cell ever
lists a lesson, README, manifest, or snapshot. `corpus/lessons/round-25.md` L94–127 cites all five ids
and `corpus/README.md` L50–51,211 names them (F10 ground); under the universal convention these are
out of domain, so their omission is correct, not a defect.

Trap checked and rejected: `corpus/lessons/round-24.md` L43 (`S039→S033`, `S040→S034`) and L93 (`S037
payload-absent`) carry **staged-package ids**, not lane-row citations; they match the id regex but are
pre-renumber references — and lessons are not `used-by` values regardless.

## Residual risk / gaps

- If "no other path" were read as *every* file mentioning a row id must be listed, the cells would be
  incomplete (lessons/README/manifest omitted). That reading contradicts the 35-row convention and
  wave-1's own stated basis ("entries whose headers cite the row", RowsScratch L38, L42–43), so the
  wave-1 verdict stands.
- Rows and receipts are uncommitted worktree bytes (`git status`: ` M corpus/SOURCES.md`,
  `??` both entry files, `??` wave-1 .md receipts). Verified on disk; a later byte change voids this
  report only, not the checked property.
- `ScoutCensusWarnings.md` L122–126 lists staged-row E11 "missing used-by" warnings — that was the
  conditional pre-landing state it describes (L116 "sequencing risk"); the landed cells resolve it.

## Tooling record

No installs or updates; read-only commands (python3, grep, git) only.
