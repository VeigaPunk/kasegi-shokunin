# round-56 claims erratum 1 — the C2 counting-command line for the lead line was mis-typed in the freeze (appended file; the freeze commit 6a4cef0 is never amended, R44/R39)

Filed by round 56 against its own freeze. In `.ufo/waves/round-56/claims.json` (freeze commit
`6a4cef002891d2e23253a187fb61a58c2fc18c7c`), C2's `counting_commands` list ends with:

    grep -c 'CISA ADP list page' corpus/SOURCES.md   # the lead line, bytes unchanged: want 1

The expectation `want 1` is wrong as typed: the string `CISA ADP list page` appears in THREE
pre-existing lines of the registry (the round-53 hunt bullet at SOURCES.md:141, the lead line
itself at :143, and the round-54 hunt bullet at :200) — the count is **3 at the base
(`git show 133c575…:corpus/SOURCES.md` prints 3) and 3 at the tip**, which is exactly the
unchanged-bytes fact the limb was trying to pin. The measured pins, both sides of the round:

- the lead line alone (`CISA ADP list page (the Vulnrichment`) prints **exactly 1 at base and
  exactly 1 at the tip**, and its line bytes hash equal:
  sha256 `90b336a2b0a3cd6ee2dceecf6eaf2a45b5954741b6eb45e8a2abc8892ed31a98` at base and tip;
- the frozen kill-rule limb proper ("the CISA ADP lead line's bytes differ" → C2 fails) is
  unaffected: it re-derives green — the line is byte-identical across the round.

Disposition: the superseding expectation is **want 3, with the base count also 3** (unchanged),
or equivalently the exact-line count 1 = 1 with the sha256 pin above. The C2 after-literals in
the frozen sentence (rows=37, registry=88, entries=40 pass=7, FAIL 33, binding 71/71, expected 75
sorted, recheck 6 Q-OK occurrences=1) are unaffected and landed exactly as frozen
(`controls/c2-counter-final-r56.txt`, `controls/c2-expect-and-counts-r56.txt`). Mined in
`corpus/lessons/round-56.md` § Mistakes (the never-re-type-from-memory rule, applied to the
freeze's own counting commands: the expectation was typed from the r55 report's prose — which
said "exactly once at the tip" about the exact-line form — not from the command's actual output).
