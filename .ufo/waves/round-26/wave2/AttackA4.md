# AttackA4 — C1 counter (c): fix-control semantics, frozen vs restated spelling

- Seat: `L1Kasegi26.AttackA4` (leaf, read-only; no subagents spawned)
- Date: 2026-10-25 UTC; all commands run from lane root
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Attack target: C1 claim `fix_control_3_hits_excluding_historical: "0"` (after),
  counter_commands[2] (frozen spelling) vs the restated spelling.
- Tooling: no tools installed/updated this run (nothing to record).

## Grep resolver on this host (recorded)

- Bare `grep` resolves to a shell builtin: `grep (pi-uu-grep) 0.2.0`.
- `/usr/bin/grep` is GNU grep 3.12-modified.
- Both resolvers were run for every command below; results identical.

## (a) Frozen spelling — `-E` with `\|` (claims.json counter_commands[2] verbatim)

```
grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l
```

- With exclusion: **0** (both resolvers).
- Without exclusion (raw grep, no `grep -v`): **0 matches**, grep exit 1, no output
  (both resolvers).

Interpretation: under `-E`, `\|` is a literal pipe character, so the pattern is the
literal string `62 assertions|77 assertions`; none of the three files contains that
text. The count `0` is therefore **vacuous** — it never exercises the `grep -v
'round-24.md:77'` exclusion, and it would return 0 identically against the
pre-fix (do-nothing) state, where the historical line is retained. This frozen
counter cannot discriminate the claimed AFTER state from BEFORE, and cannot detect
a regression of the fix. Claimed "GNU grep treats `\|` as literal under `-E`"
confirmed on both resolvers (exit 1, no matches).

## (b) Restated spelling — `-E` with bare `|`

```
grep -rnE '62 assertions|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l
```

- With exclusion: **0** — expected 0, matches the claimed AFTER state. ✓
- Without exclusion (raw):
  **1** — expected 1, the retained historical line. ✓

Note: the assignment labels (b) "BRE alternation without `-E`", but the command as
given still carries `-E`; the operative change versus (a) is `\|` → `|`. The two
spellings differ only in the escaped pipe.

## Exact retained line text (line 77 of corpus/lessons/round-24.md)

Grep output line (verbatim):

```
corpus/lessons/round-24.md:77:it was written; `source-recheck.py` exits 0 over 19 records / 77 assertions.
```

File content at line 77 (verbatim, via read):

```
it was written; `source-recheck.py` exits 0 over 19 records / 77 assertions.
```

(Historical transcription line; round-25 errata D24-2 notes the manifest actual is 76
assertions and 77 is historical. The exclusion filter retains exactly this one line.)

## Verdict

- C1 AFTER state `fix_control_3_hits_excluding_historical: 0` is **verified** by the
  restated spelling (0 with exclusion; the single excluded line is round-24.md:77).
- The **frozen** counter spelling in claims.json (counter_commands[2]) is defective:
  `\|` under `-E` is literal, so it returns 0 by vacuity and would also pass against
  the do-nothing control. It does not verify the claim and cannot fail closed. The
  restated spelling should be the canonical counter. (claims.json is frozen and was
  not edited; this is reported as a finding, not a change.)

## Residual risk / verification gaps

- None in scope beyond the frozen-counter defect above (observable, reproduced on both
  resolvers; no further checks needed).
- Commands were run exactly as specified from the lane root; outputs recorded verbatim.
