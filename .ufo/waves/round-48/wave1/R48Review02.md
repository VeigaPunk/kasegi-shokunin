# R48Review02 — Historical SHONEN archive SHA verified against base 903d47e via git show

- **Seat:** R48Review02 (reviewer, leaf member; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Assignment:** Verify historical SHONEN archive SHA against base
  `903d47e13058982460f0d90c1c2b9c7c02680646` via `git show`, no working-tree assumptions.
- **Rules read first:** `/home/vgpnk/.omp/agent/RULES.md` (tooling directive noted; no installs
  performed — git, coreutils, python3 only; all pacman transactions honored as paused).
- **Round-47 routes:** R1 (SHONEN.md canonical-form drift) is the routed defect C1 closes;
  R2 (frozen plain-target phrasing) read for context only.
- No production edits. No git/jj mutation. No commits. Scratch
  `/fast/scratch/hyaku/kasegi-r48/R48Review02/` created, receipts saved here, removed at exit.

## Frozen inputs (measured this seat)

| Artifact | sha256 / id |
|---|---|
| base commit `903d47e13058982460f0d90c1c2b9c7c02680646` | commit, "round-47 verifier spot-check (integrator, hyaku): non-author admit/reject", 2026-10-30 10:31:51 -0300 |
| freeze commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` | commit, "round-48: freeze canonical checklist restoration and controls"; parent of HEAD |
| `corpus/instruments/shonen-form.py` (frozen counter) | sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (unchanged) |
| `.ufo/waves/round-48/controls/shonen-before.txt` | sha256 `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` |
| `.ufo/waves/round-48/controls/canonical-candidate.txt` | sha256 `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c` |
| `.ufo/waves/round-48/claims.json` (working tree) | sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`; git blob `f52264e7ca651cc99b064bb72b407c767c35d4c7` |
| `SHONEN.md` at HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031` | sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` |

The frozen claim id `3546f708…` names the freeze commit (not a blob); `claims.json` was
introduced by that commit and is byte-identical to the working-tree copy measured here
(sha256 matches R48Probe16's independent freeze-time measurement). It did not exist at base —
consistent with base being the round-47 commit.

## Verification

### 1. Historical archive SHA at base, via git show (no working-tree assumptions)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git show 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md | sha256sum
596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05  -
```

Blob identity and size from the object database (not the worktree):

```
$ git ls-tree 903d47e13058982460f0d90c1c2b9c7c02680646 -- SHONEN.md
100644 blob b0bd443a55dd0aac1fe86684bc3cae96454a6f7d	SHONEN.md
$ git rev-parse 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md
b0bd443a55dd0aac1fe86684bc3cae96454a6f7d
$ git cat-file -s 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md
41339
```

Independent second path over the same object:

```
$ git cat-file blob b0bd443a55dd0aac1fe86684bc3cae96454a6f7d | sha256sum
596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05  -
```

**Result: `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` — exactly the
archive SHA the frozen C1 kill_rule requires** ("restoration loses historical bytes (archive
must retain SHA256 596122c0…)").

### 2. Frozen control capture is the historical bytes, byte-for-byte

```
$ git show 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md | cmp - .ufo/waves/round-48/controls/shonen-before.txt
cmp_exit=0            # both 41339 bytes
```

`controls/shonen-before.txt` (sha256 `596122c0…`) is byte-identical to the committed
historical archive; the pre-freeze capture carries no working-tree contamination.

### 3. Historical bytes match the claim's declared "before" state

The historical blob carries exactly 52 `- [` marks, matching C1's before text ("52 author
marks and accumulated assessment blocks"). Running the frozen counter on a scratch copy of the
historical bytes:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md > /fast/scratch/hyaku/kasegi-r48/R48Review02/historical-SHONEN.md
$ sha256sum /fast/scratch/hyaku/kasegi-r48/R48Review02/historical-SHONEN.md
596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05  historical-SHONEN.md
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py \
    --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --file /fast/scratch/hyaku/kasegi-r48/R48Review02/historical-SHONEN.md
shonen-form canonical=0 finding=SF-PREAMBLE exit=1
exit=1
```

Observed `canonical=0 finding=SF-PREAMBLE exit=1` == `claims.json` `expect_before`, and ==
the committed `controls/do-nothing.txt` control. The drift fixture and the historical archive
are one and the same bytes.

### 4. Historical bytes retained after the repair (kill_rule clause c)

```
$ git merge-base --is-ancestor 903d47e13058982460f0d90c1c2b9c7c02680646 HEAD; echo exit=$?
exit=0
$ git log --oneline 903d47e13058982460f0d90c1c2b9c7c02680646..HEAD
3d7e042 round-48: restore canonical checklist and dispatch 64 probes
3546f70 round-48: freeze canonical checklist restoration and controls
$ git status --porcelain -- SHONEN.md .ufo/waves/round-48/claims.json .ufo/waves/round-48/controls
(empty)
```

History is append-only: base → freeze → repair. The repair commit `3d7e042` replaced
`SHONEN.md` (354 lines removed; landed bytes sha256 `b1352168…`, == working tree, clean) but
did not rewrite history — the drifted archive remains reachable at blob
`b0bd443a55dd0aac1fe86684bc3cae96454a6f7d`, digest `596122c0…`. **No historical bytes lost.**

## Adjacent observations (not defects; for the integration owner)

- Landed `SHONEN.md` (`b1352168…`) differs from `controls/canonical-candidate.txt`
  (`b476c7aa…`) in five evidence lines and box 2's mark (`[ ]` vs `[~]`). Both are valid
  grammar instances: the landed file grades `canonical=1 finding=SF-CLEAN exit=0` (measured
  by peer seats; the candidate is the pre-freeze `case=canonical` positive). The landed form
  is the more conservative one — box 2 unchecked with "No new end-to-end domain task claimed;
  source and diagnostic work only." All four landed evidence pointers exist on disk:
  `LOG.md`, `SKILL.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md`.
  Within C1's form-only predicate ("canonical four-box author-assessment grammar with
  existing local evidence pointers"), this is conformant.
- Sibling probe reports (R48Probe11–16) cite working-tree `SHONEN.md` sha256 `b1352168…` as
  the canonical positive; that is the landed repair, consistent with this seat's git-history
  verification — the "historical archive" and "canonical candidate" are distinct byte strings
  and must not be conflated.

## Verdict

**PASS.** Historical SHONEN archive at base `903d47e13058982460f0d90c1c2b9c7c02680646` hashes
to `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` via `git show`, matching
the C1 kill_rule's required retained archive SHA; the frozen control capture is byte-identical
to it; the historical bytes reproduce `expect_before` (`SF-PREAMBLE` exit 1) under the frozen
counter; and the post-repair history still retains them. No counter defeat observed; the
frozen predicate was not amended.

Expected vs observed: expected archive SHA `596122c0…` (kill_rule) — observed `596122c0…` via
two independent git object-database paths. Expected `expect_before` `SF-PREAMBLE` exit 1 —
observed identical. All commands recorded verbatim above.

## Hygiene

- Read-only git only (`rev-parse`, `cat-file`, `ls-tree`, `show`, `log`, `merge-base`,
  `hash-object`, `status`); zero git/jj mutations; no production, fleet, or sibling files
  written; no commits; no tool installs (none needed — git + coreutils + python3 3.14.8 host).
- Production `SHONEN.md` sha256 `b1352168…` before and after this seat: unchanged (never read
  into any write path).
- Frozen counter `shonen-form.py` sha256 `0ab32a2c…` before/after: unchanged.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review02/` removed at exit after these receipts
  were saved (`rm -rf`, removal confirmed).
