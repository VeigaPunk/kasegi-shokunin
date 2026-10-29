# Equivalent-mutant proofs — f29 gate battery (attempt 2, wave-2 integration)

The f29 battery (r46-mutbat.py --counter f29) on the landed tree leaves exactly three of the 21
mutants uncaught: H1b-raw-loose, H7a-verdict-or, H7c-okline-loose (receipt:
`.ufo/waves/round-46/attempt2/controls/f29-battery-f29.txt`). Each is equivalent-on-tree:

## H1b-raw-loose (`if len(raw) != 1:` -> `if len(raw) < 1:`)

The raw clause counts live `| F29 |` lines in the README. A tree that changes the count to 2+
necessarily duplicates the F29 id (both lines parse as rows), so the `dup` clause and the
`entry-shared` guard fire first and H1 is red through them — the mutant changes no H1 verdict on
any input where the raw clause is the deciding one, because there is no such input: raw >= 2
implies dup >= 1. A tree with raw = 0 is a tree whose F29 row vanished from the live table, which
the row checks (f29[0] missing) reject independently. This is R50 disclosure (a) restated for the
raw clause specifically; the wave-1 pairing could not isolate it and the selftest's 30 cases
(30/0) do not grade it. Classified equivalent-on-tree; the clause remains belt-and-braces behind
`dup` and the F29-presence checks.

## H7a-verdict-or (`rc == 0 and ok_line` -> `or`) and H7c-okline-loose (ok-line tab anchor loosened)

Both grade the census OUTPUT shape. The census script lives at the fleet root
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) and no lane-side tree can change its
output contract; on every tree the battery can build, `rc == 0` implies the `ok` tab line and
`rc != 0` implies its absence, so `and`/`or` and the tab anchor coincide on every reachable input.
Identical argument to the c2 gate's G7a/G7c proofs (`G6b-G7a-G7c-equivalence-probe.txt`, R50
disclosure (f)). Classified equivalent-on-tree; the census itself is gated upstream by the fleet
SOURCES contract, and H7 additionally carries the lane-side single-Registry-heading check
(v1.1), which IS graded (mutant H7b-registry-count would be caught by the selftest's duplicated-
heading case).
