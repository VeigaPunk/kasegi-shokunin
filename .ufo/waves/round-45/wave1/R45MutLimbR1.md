VERDICT: BROKEN

# R45MutLimbR1 — C1 mutation probe of counter limb R1 (S070 supersede row, snapshot pin, S070 byte-identity, lesson correction)

Seat: R45MutLimbR1 (leaf, read-only on the lane; no edits to the counter, no commits, no git mutation).
Attacked: `corpus/instruments/r45-routed-defects.py`, function `limb_r1` (lines 99-140), frozen at commit `8cf62c879e6e6b031e67412f8fac1fba0bd378cf`.

## Survivors (the finding): 2 of 8 required mutants are accepted while the defect is present

Both survivors are single edits on a hand-built tree in which R1 is satisfied. In both, the R1 defect (`corpus/lessons/round-44-verifier-spotcheck.md` §6 item 1) is present in the artifact. The counter prints `fixed=1` in each case.

1. **flip-TBD** — `rejected=0`. Edit on the S072 row of `corpus/SOURCES.md` (teaches cell):
   - old: `flip: the directory gains a rule paragraph that appears on no program's own rules page.`
   - new: `flip: TBD`
   - Counter output: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`
   - Why it survives: `limb_r1` line 110 tests only `re.search(r"flip:\s*\S", teaches)`, a presence check. The §6 item 1 defect is precisely "replace the vacuous flip condition with a checkable one"; `flip: TBD` is the vacuous form and is accepted.

2. **correction-emptied** — `rejected=0`. Edit on the appended line 205 of `corpus/lessons/round-44.md`:
   - old: `Correction (round 45, appended): the S070 reject reason is superseded by S072 — the article API returns a readable 10029-character body; the reject stands on overview-only content, not on an unreadable shell.`
   - new: `Correction (round 45): S072 10029`
   - Counter output: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`
   - Why it survives: `limb_r1` lines 136-137 accept any line that starts with `Correction (round 45`, and contains `S072` and the size token. The correction never has to state the reason it claims to correct. The literal predicate is met; the intent (state the true reason: overview, no program-specific rule beyond S069 Q5) is not checked. Judgment: defect present, since the correction carries no reason.

Not survivors (the counter rejects these, reason printed):

| mutant | edit (on satisfied tree) | rejected | counter `read=` token |
|---|---|---|---|
| verb-relates | `supersedes S070 —` → `relates to S070 —` (S072 teaches) | 1 | `teaches-not-supersedes` |
| status-mined | S072 row `\| rejected \| 2026-10-28` → `\| mined \| 2026-10-28` | 1 | `status=mined` |
| size-10028 | `10029-character body` → `10028-character body` (S072 teaches) | 1 | `size-token-absent` |
| S070-row-181d | `absent from the linked policy text. \| rejected \| 2026-10-28 \| 180d` → `…181d` (S070 row) | 1 | `S070-row-changed-or-baseline-absent` |
| sha-anchor-nibble | `sha256 364166c4a23e…` → `sha256 464166c4a23e…` (S072 anchor) | 1 | `snapshot-sha-not-in-anchor` |
| manifest-quote-drift | `handles reasonably sensitive user data"` → `…user datum"` (manifest S072 Q1) | 1 | `recheck-rc=1-quotes=1` |

Supplementary single-edit mutants (outside the required eight; run as extra coverage of the same facets):

| mutant | edit | rejected | `read=` |
|---|---|---|---|
| snapshot-one-byte | append `\n` to `corpus/source-snapshots/round-45/S072.txt` | 1 | `recheck-rc=1-quotes=0` |
| lesson-base-edited | `# Round 44 — Kasegi` → `# Round 45 — Kasegi` (line 1 of round-44.md, base portion) | 1 | `round-44-lesson-not-append-only` |
| correction-size-only | `readable 10029-character body; the reject` → `readable 10028-character body; the reject` (line 205) | 1 | `lesson-correction-absent` |

## Commands run and printed output

Counter identity (read-only): `sha256sum corpus/instruments/r45-routed-defects.py` printed `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee`; `git show 8cf62c879e6e6b031e67412f8fac1fba0bd378cf:corpus/instruments/r45-routed-defects.py | sha256sum` printed the same digest. The base export has no counter (added at the freeze commit), so a byte-identical copy was run with `--baseline` pointing at the base.

Base: `git archive dc5bb8c | tar -x -C <scratch>/base`; `diff -rq <scratch>/base /fast/scratch/hyaku/kasegi-r45/L1/pure` printed no differences (identical trees).

Recipe run (`RSCR=<scratch> TMPDIR=<scratch>/tmp python3 <scratch>/recipe.py`), full output:

```
preflight counter_sha=82004c700dec S072_sha_ok=True
preflight S072 chars(rstrip-newline)=10028 chars(total)=10030 bytes=10032
== controls ==
control do-nothing-base R1 fixed=0 read=row-S072=absent
control marker-only R1 fixed=0 read=row-S072=absent
control satisfied-tree R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
== mutants ==
mutant=verb-relates rejected=1
  R1 fixed=0 read=teaches-not-supersedes
mutant=status-mined rejected=1
  R1 fixed=0 read=status=mined
mutant=flip-TBD rejected=0
  R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
mutant=size-10028 rejected=1
  R1 fixed=0 read=size-token-absent
mutant=S070-row-181d rejected=1
  R1 fixed=0 read=S070-row-changed-or-baseline-absent
mutant=sha-anchor-nibble rejected=1
  R1 fixed=0 read=snapshot-sha-not-in-anchor
mutant=correction-emptied rejected=0
  R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
mutant=manifest-quote-drift rejected=1
  R1 fixed=0 read=recheck-rc=1-quotes=1
mutant=SUPP:snapshot-one-byte rejected=1
  R1 fixed=0 read=recheck-rc=1-quotes=0
mutant=SUPP:lesson-base-edited rejected=1
  R1 fixed=0 read=round-44-lesson-not-append-only
mutant=SUPP:correction-size-only rejected=1
  R1 fixed=0 read=lesson-correction-absent
exit=0
```

Edit verification (quoted): `diff` of the satisfied tree against the flip-TBD mutant shows the S072 row changed; `grep -o "flip: TBD | rejected | 2026-10-28 | 180d | — |" mut/flip-TBD/corpus/SOURCES.md` printed `flip: TBD | rejected | 2026-10-28 | 180d | — |`. `grep -n "^Correction (round 45" mut/correction-emptied/corpus/lessons/round-44.md` printed `205:Correction (round 45): S072 10029`, and the file is still 205 lines.

Full counter on the satisfied tree (`python3 counter/r45-routed-defects.py --root sat --baseline base`):

```
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=1 unresolved=4 exit=1
```

Snapshot size (`wc -c -m corpus/source-snapshots/round-45/S072.txt`): `10030 10032` (characters, bytes).

## Discrimination against controls

- The do-nothing base and the marker-only tree are both red on R1 (`fixed=0`), so the committed controls in `controls/freeze-controls.txt` discriminate only the gross cases (no row; no correction). Neither detects the two survivors: a row with `flip: TBD` plus any correction line is not a control shape present in the freeze controls.
- The satisfied tree is green on R1 (`fixed=1`), which shows the mutations are the sole cause of the flip between green and red for the rejected mutants.

## Observations (not single-edit survivors)

- **Size token is an unanchored literal.** `10029` is accepted in two cells (teaches, correction) but never derived from the pinned bytes. The snapshot is 10030 characters including its final newline and 10032 bytes; 10029 equals the character count minus one final newline. The counter does not compute it, so a consistent two-cell edit to another count (not run here) would pass R1.
- **R1 checks tokens, not reasons.** Items 1 (flip) and the correction both reduce to presence checks; that is the same presence-only class the R47-R49 criteria (`QUALITY.md`) are meant to forbid.

## Limitations

- The satisfied tree is hand-built by this seat: an S072 row (11 cells, anchor carries the S072.txt sha `364166c4…a025`, status `rejected`, teaches opening `supersedes S070 —`) and a `Correction (round 45…)` line appended to `round-44.md`. The lane's HEAD (`5242db6`) carries neither artifact; the probe therefore grades the counter's predicate, not the lane's final bytes. Re-run after the L1 lands the artifacts.
- Mutants are single-substring edits chosen to cover R1's six facets; the set is not exhaustive. Other single edits (e.g., word substitutions inside the flip clause that keep `\S`) were not enumerated.
- The counter was run from a byte-identical copy in scratch (sha verified), with `--baseline` pointing at the `dc5bb8c` export. Scratch was removed on exit; the quoted outputs above are the evidence.
- Nothing was committed, pushed, or written to git/jj/index. Counter, lane files, MANIFEST.json, .ufo/state and sibling lanes were not touched; the only lane write is this Report file.
- No installs. `read`/`write`/`bash` only.

## Suggested repairs (drafts, not applied; counter not edited)

- flip: replace `flip:\s*\S` with a check that the flip clause names a manifest quote id (`Q\d+`) or a line anchor, and rejects placeholder tokens (`TBD`, `none`, `n/a`, `TODO`). Add a committed control tree with `flip: TBD` expected RED.
- correction: require the correction to contain the true-reason phrase (or a minimum-length body beyond the three tokens), and add a committed control with `Correction (round 45): S072 10029` expected RED.
- size: compute the character count from the pinned snapshot (with the final-newline convention stated) and compare, rather than matching a literal.
