# R48Review05 — Prior SHONEN archive and candidate through the frozen checker

- Seat: R48Review05 (executor), kasegi round 48, wave1.
- Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Frozen claim: C1 (`claims.json` sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matches `.ufo/waves/round-48/freeze.txt` pin; base `903d47e13058982460f0d90c1c2b9c7c02680646`).
- Seat item: run the actual prior SHONEN archive through the frozen checker, reproduce SF-PREAMBLE, check the candidate for SF-CLEAN.
- Checker (read-only, not edited): `corpus/instruments/shonen-form.py`, measured sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`.

## Verdict (expected vs observed)

| Probe | Input | Expected (C1) | Observed | Match |
|---|---|---|---|---|
| A — before | `.ufo/waves/round-48/controls/shonen-before.txt` (sha256 `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05`) | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` | YES |
| B — candidate | `.ufo/waves/round-48/controls/canonical-candidate.txt` (sha256 `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c`) | `shonen-form canonical=1 finding=SF-CLEAN exit=0` | `shonen-form canonical=1 finding=SF-CLEAN exit=0` | YES |

No defeat observed on either limb. Both expected/after predicates of C1 reproduce exactly on the frozen counter.

## Exact commands and observed output (receipt: this section)

```
sha256sum corpus/instruments/shonen-form.py
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py

python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/shonen-before.txt
shonen-form canonical=0 finding=SF-PREAMBLE exit=1
# process exit status: 1

python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/canonical-candidate.txt
shonen-form canonical=1 finding=SF-CLEAN exit=0
# process exit status: 0
```

Probe A finds SF-PREAMBLE because the drifted archive's third line is the round-35 `> Current pointers:` block-quote, not the canonical `Promotion to shokunin requires all of:` — the drift (52 author marks plus accumulated per-round assessment blocks, per the C1 before-cell) fails at the preamble gate before any box grammar is reached.

## Provenance corroboration (read-only)

```
git rev-parse HEAD
3d7e042ecbb1f17662f5042e8d3da3290722c031   # "round-48: restore canonical checklist and dispatch 64 probes"

git show 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md | sha256sum
596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05  -

git show 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md | cmp - .ufo/waves/round-48/controls/shonen-before.txt && echo IDENTICAL
IDENTICAL
```

The prior-archive fixture is byte-identical to SHONEN.md at the claims base commit, and its sha256 equals the archive hash the C1 kill rule requires to be retained. Probe A therefore measures the real prior state, not a paraphrase. (Review02 owns the git-show verification lane; this corroborates it.)

## Integrated live tree (measurement only, not a promotion read)

```
python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
shonen-form canonical=1 finding=SF-CLEAN exit=0
# process exit status: 0
```

- Working-tree `SHONEN.md` sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, `git status --porcelain -- SHONEN.md` empty (clean at HEAD `3d7e042`).
- The integrated file differs from the controls candidate only in evidence-pointer text: box 1 → `SKILL.md`, box 3 → `corpus/lessons/round-47-verifier-spotcheck.md`, box 4 → `PROVINCE.md`, and box 2 is honestly unchecked `[ ]` (`Evidence: LOG.md — No new end-to-end domain task claimed`). All four pointers resolve as in-root files (`test -f` each → OK), which the SF-CLEAN result itself also proves.
- Box 2 remaining `[ ]` is consistent with the archive's own repeated "no end-to-end domain task ran" admissions and matches what R48Review04 independently checks.

## Controls and rules read

- `.ufo/waves/round-48/controls/do-nothing.txt` records `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` / `PROCESS_EXIT=1` — consistent with probe A's observed before-state.
- Round-47 verifier routes R1/R2 as cited by round-47 reviews resolve to `corpus/QUALITY.md` record criteria R1 (a live-tree/path assertion carries an as-of date and a `test -e` result) and R2 (self-description is a claim: cite the census/counting command). Applied here: every verdict above carries its exact command and observed output, and the live-tree SF-CLEAN verdict names the revision it was measured at (HEAD `3d7e042`, 2026-10-30T11:32:58-0300).
- Protocol source snapshot confirms the normative basis (S077): SHONEN.md seed must diff byte-identical modulo name, marks confined to the box character plus one indented evidence line; `[x]` requires a named non-author verifier — the frozen checker mechanically rejects `x` (SF-VERIFIER), which I did not attempt to defeat; the claim is author-side form, not promotion or semantic truth.

## Defeats, risks, limits

- None observed: expected and observed exit/finding match on both the before archive (SF-PREAMBLE, exit 1) and the candidate (SF-CLEAN, exit 0).
- Limit: verdicts grade the tree measured. The live-tree limb was measured at HEAD `3d7e042` at seat run time; a later integration commit supersedes it.
- Limit: pointer existence was checked by the frozen counter (SF-CLEAN requires it); semantic truth of the four evidence lines is outside this seat and outside the checker's predicate.
- No production, fleet, sibling, or git/jj state was modified. No tools installed. Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review05/` was removed after this report landed.
