# R45RevGateG2 — attack on gate G2 of corpus/instruments/r45-c2-gate.py

VERDICT: BROKEN

Scope: read-only attack on `def g2` (r45-c2-gate.py:121-129) against the frozen C2 `after`
(.ufo/waves/round-45/claims.json, C2) and the docstring predicate (r45-c2-gate.py:13-14).
Scratch: /fast/scratch/hyaku/kasegi-r45/R45RevGateG2 (removed on exit). Nothing committed,
no git mutation, no shared file touched; the counter was run from the lane tree read-only.

## What G2 actually tests (r45-c2-gate.py:121-129, quoted)

```
p, why = entry_path(root)                       # F27 row cell 4 must name an existing knowledge/*.md
head = (txt(root, p) or "").splitlines()[:8]
ok_s = any(h.startswith("source: S071 — " + URL) for h in head)
ok_v = any(h == "verified-at: 2026-10-28" for h in head)
ok_r = any(h.startswith("recheck:") and len(h) > 10 for h in head)
```

G2 is three string tests on the first eight lines of the entry file. It does not:
- read the F27 row status (G2 accepts `rejected`, see V3);
- check the source line against SOURCES.md, the snapshot, or the manifest (G3/G4 do that for
  the row and capture, never for the entry header);
- execute or verify the `recheck:` line. `grep -n recheck r45-c2-gate.py` prints only the
  docstring lines 14/18 and the G2/G4 code (lines 127-129, 160-166); no gate runs the entry's
  recheck command. G4 runs `source-recheck.py` on the manifest, not on the entry header;
- check that `verified-at` corresponds to any run. It is a literal string.

The docstring says the entry "opens with" the trio (line 13); the code accepts it at any of
lines 1-8, in any order, with arbitrary text after the URL (`startswith`). The docstring
and the code disagree.

## Finding 1 — G2 is satisfied by a fabricated header (the defect class the task names)

Recipe (cheapest found: 1 README row + 1 entry file, 3 header lines):

```
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}; SCR=$HYAKU_SCRATCH/kasegi-r45/R45RevGateG2
export TMPDIR=$SCR/tmp
D=$(mktemp -d -p "$SCR") && git -C "$D" init -q && git -C "$D" rev-parse --show-toplevel   # -> $D
mkdir -p "$D/corpus/knowledge"
printf '%s\n' '| F27 | Linux kernel security-bugs reporting process | admitted | knowledge/linux-kernel-security-bugs.md |' > "$D/corpus/README.md"
printf '%s\n' 'source: S071 — https://docs.kernel.org/process/security-bugs.html' 'verified-at: 2026-10-28' 'recheck: ok' > "$D/corpus/knowledge/linux-kernel-security-bugs.md"
python3 corpus/instruments/r45-c2-gate.py --root "$D"     # lane copy, read-only
```

Printed (verbatim, run performed this session):

```
gate G1 pass=0 read=rows=1 admitted=1 dup=0
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4
gate G6 pass=0 read=knowledge=1
gate G7 pass=0 read=census-rc=2
c2-gate fixed=1/7 exit=1
```

Realistic variant (same counter, pure frozen base export copied to scratch, one row appended to
corpus/README.md, the same fake entry written as a 4-line file with a `# title` line first;
nothing else touched):

```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=4/7 exit=1
```

So G2 prints pass=1 with the real defect present (no S071 row, no snapshot quote, no recheck
executed, no body at all). The entry body in this recipe is empty apart from the header.

Variant showing G2 ignores the row status (fixture: same as minimal, row cell 3 = `rejected`):

```
gate G1 pass=0 read=rows=1 admitted=0 dup=0
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
...
c2-gate fixed=1/7 exit=1
```

Variant showing G2 accepts a URL suffix (`...security-bugs.html.invalid`), re-run this session
(minimal fixture, row admitted, header line 1 = `source: S071 — https://docs.kernel.org/process/security-bugs.html.invalid`):

```
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
```

Cause: `startswith` at r45-c2-gate.py:126 accepts any suffix after the URL.

## Finding 2 — do-nothing control discriminates (G2 is not vacuous at base)

Control: pure frozen base export (/fast/scratch/hyaku/kasegi-r45/L1/pure, copied, not edited)
run through the counter:

```
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G2 pass=0 read=F27-rows=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=F27-rows=0
gate G6 pass=0 read=knowledge=63
gate G7 pass=1 read=census-rc=0
c2-gate fixed=1/7 exit=1
```

This matches the frozen control line `control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1`
(.ufo/waves/round-45/controls/freeze-controls.txt:2). G2 fails at the base because the F27 row is
absent, so the do-nothing control does not discriminate G2's header test at all; the header test
is only ever exercised once a F27 row and a file exist. That is why a 2-file fixture is enough.

## Finding 3 — G2 false-REDs correct landings (format and date variants)

Matrix (one fresh `git init` fixture per row, header lines varied, row and entry path fixed;
run with the counter, G2 line quoted verbatim; output file /fast/scratch/hyaku/kasegi-r45/R45RevGateG2/variants.out):

```
T0 canonical (docstring form)              -> gate G2 pass=1 read=source=1 verified-at=1 recheck=1
T1 trailing space on verified-at           -> gate G2 pass=0 read=source=1 verified-at=0 recheck=1
T2 ASCII hyphen instead of em dash         -> gate G2 pass=0 read=source=0 verified-at=1 recheck=1
T3 capitalised Source:                     -> gate G2 pass=0 read=source=0 verified-at=1 recheck=1
T4 bold label **source:**                  -> gate G2 pass=0 read=source=0 verified-at=1 recheck=1
T5 URL as markdown link                    -> gate G2 pass=0 read=source=0 verified-at=1 recheck=1
T6 same doc at other canonical URL         -> gate G2 pass=0 read=source=0 verified-at=1 recheck=1
T7 later re-verification date              -> gate G2 pass=0 read=source=1 verified-at=0 recheck=1
T8 timestamp verified-at                   -> gate G2 pass=0 read=source=1 verified-at=0 recheck=1
T9 recheck 10 chars (recheck:ok)           -> gate G2 pass=0 read=source=1 verified-at=1 recheck=0
T10 trio at line 9 after front-matter      -> gate G2 pass=0 read=source=0 verified-at=0 recheck=0
T11 blockquoted source line                -> gate G2 pass=0 read=source=0 verified-at=1 recheck=1
```

Rejected-but-correct landings G2 would false-RED: a bold or capitalised label (T3, T4); a hyphen
or other dash in place of U+2014 (T2); a markdown-linked URL (T5); the same document cited at
its other canonical kernel URL (T6, e.g. www.kernel.org/doc/html/latest/process/security-bugs.html);
a trailing space or a timestamp in verified-at (T1, T8); a genuine re-verification in a later
round, since the date is pinned to 2026-10-28 (T7); a header placed below a title or front-matter
block so the trio starts at line 9 (T10); a blockquote (T11); a recheck line of 10 characters or
fewer (T9, low realism: no real recheck command is that short, but it is a literal threshold).
T0 is the only form that passes, and T0 passes equally when `recheck: ok` is fabricated (Finding 1).
So G2 is format-strict and truth-blind: it rejects some correct spellings and accepts a fabricated one.

## Limitations

- I attacked the frozen base export plus fixtures, not a real S071 landing. The lane tree at
  the frozen base has no F27 row (control above), and I did not inspect builder drafts for an
  F27 entry; if a final entry carries a real recheck line, G2 still cannot tell it from `recheck: ok`.
- The realistic variant's 4/7 score equals the frozen c2-junk-row control's score
  (controls file line 4). The junk-row control tree is not in the repo, so I cannot confirm that
  it passes G2 the same way; that equality is [INFERENCE] only.
- G2 was not run against the frozen controls' own fixtures (not in the repo).
- Recommended repair (for the L1, not applied): have G2 require the entry's `recheck:` command to
  be executed (or check it against the manifest's sha) and bind verified-at to the capture's
  run date, and anchor G2 to the row's status (`admitted`) so a rejected F27 cannot pass the
  header test on its own.
