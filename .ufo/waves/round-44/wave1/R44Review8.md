# R44Review8 — C1 defect 8

## Finding
**Defect confirmed in the round-43 committed evidence; current round-44 correction not yet present in the inspected tree.** The round-43 spot-check §6 item 8 says C1 `before` and its report assert exit 127 but cite a control whose `ls` returned exit 2; see `corpus/lessons/round-43-verifier-spotcheck.md:108`. The frozen original control itself records exit=2 (`.ufo/waves/round-43/c1-controls/do-nothing.txt` §A, identified by the spot-check). Running `ls` on a missing path is not the same operation as directly executing a missing script.

## Commands / observed outputs
From lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`:

```sh
corpus/instruments/r43-closure.sh >/dev/null 2>&1; printf 'direct-command-exit=%s\\n' "$?"
# direct-command-exit=2

sh -c 'exec /no/such/script' >/dev/null 2>&1; printf 'exec-not-found-exit=%s\\n' "$?"
# exec-not-found-exit=127

git cat-file -e 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a:corpus/instruments/r43-closure.sh; printf 'base-suite-presence=%s\\n' "$?"
# base-suite-presence=0
```

The initial attempted run of `corpus/instruments/r43-closure.sh` was **not** a missing-path reproduction: the frozen base `5ab3a60a...` contains that suite (the command above proves presence), and executing it yielded 2. Therefore do not call that run evidence for 127. The standalone `exec` control models the shell's missing-executable status (127), but is a generic `/no/such/script`, not a direct execution of an absent suite at the frozen base. The correction should state the precise command/path and exit being claimed, and distinguish shell lookup failure (127) from the cited `ls` probe (2); do not silently claim that the suite is absent at the round-44 frozen base.

## Do-nothing discrimination / limitation
At the frozen round-44 base given by `.ufo/waves/round-44/controls/do-nothing.txt:2`, the round-43 suite is present, so a direct invocation cannot yield 127 by absence. Do-nothing cannot cure the historical mismatch between the cited `ls` output (2) and the report's asserted 127. The round-44 claims JSON currently has no correction text (`.ufo/waves/round-44/claims.json:11-15` only defines the claims/counter/control), and the visible round-44 directory has no R44Review8 receipt at inspection. I did not inspect a final lane revision or run a committed correction checker; closure remains unproven.

## Scratch / tooling
Attempted `mkdir -p "$HYAKU_SCRATCH/kasegi-r44/R44Review8"`; failed with `Permission denied`, so no scratch was created. No tool installed or updated.