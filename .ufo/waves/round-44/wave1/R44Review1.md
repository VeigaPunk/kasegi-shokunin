# R44Review1 — C1 defect 1: unsupported `closed=13/19`

## Finding

**Actionable, unresolved in the inspected evidence.** The frozen defect says the round-43 SCORECARD move-log and claims C1-before assert base result `closed=13/19 exit=1 with exactly K14-K19 open`, but no committed execution of landed suite `a832908e…` at base `ab98fac9` backs that composite. It traces the number to stub/draft evidence; committed per-limb runs instead derive 12/19 or 11/19. The required repair is either an append-only `Correction (round 43)` explicitly superseding the 13/19 literal with the per-limb base result (six red transcripts), or a committed base run of the landed suite. Source: `corpus/lessons/round-43-verifier-spotcheck.md:97-102`, especially :101.

## Do-nothing discrimination

The frozen control records base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` and states no R44 correction/counter existed; its C1 scan observed 8 routed defects. This establishes do-nothing does not satisfy the R44 target, but is not itself evidence that the historical 13/19 claim is supported. Exact frozen evidence: `.ufo/waves/round-44/controls/do-nothing.txt:2-7`.

At current lane HEAD `66314015122b9aa32dc40f2f1815df56624c26d1`, the assigned spot-check is present; the workspace also has an unrelated untracked `.ufo/waves/round-44/wave1.ready.partial`. I made no production/shared edits. Attempted scratch setup failed (`mkdir: Permission denied`); `HYAKU_SCRATCH` was empty, so no scratch was created and none could be cleaned. No tools installed.

## Limits / evidence

Commands run:
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` → `66314015122b9aa32dc40f2f1815df56624c26d1`.
- `git -C ... status --short` → `?? .ufo/waves/round-44/wave1.ready.partial`.
- `git -C ... show ab98fac9:corpus/instruments/r43-closure.sh` → fatal: path exists on disk, but not in `ab98fac9` (thus the landed suite is not present at that revision under this path).

I did not run the counter, independently enumerate committed per-limb transcripts, or inspect current correction files; the underlying exact 12/19-versus-11/19 derivation remains an asserted finding of the cited committed lesson, not independently recomputed here. A clean fail-closed correction must not preserve `13/19` as fact absent committed base-suite output; it should reject/mark unsupported any base count that cannot be derived from committed per-limb evidence or a committed landed-suite run. No runtime verdict is offered.