# R48Review04 — SHONEN evidence-pointer resolution and box-2 honesty review

Seat: R48Review04 (reviewer, leaf — no subagent dispatch)
Scope: one evidence pointer per box resolves; box 2 honestly remains unchecked; semantic review, not promotion.
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Judged axis: depth:verifiability. Claim under review: C1 (canonical four-box author-assessment grammar).

## Frozen-state identification

- Assignment cites the frozen claim at `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`; that is the git commit `3546f70` ("round-48: freeze canonical checklist restoration and controls"), the last commit touching `corpus/instruments/shonen-form.py` (`git log --format='%H %s' -- corpus/instruments/shonen-form.py` → `3546f7089c224ac6c8adc68208b1e648bbf3e6a5 round-48: freeze …`).
- `claims.json` at freeze and now: sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2b345`, matching `freeze.txt` (`claims-sha256: b8022cdf…`). Claim bytes unchanged after freeze.
- Frozen checker bytes: `corpus/instruments/shonen-form.py` sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`; untouched by HEAD commit `3d7e042` (`show --stat` lists no instrument change). No post-score checker amendment.

## Bounded probe (frozen counter, exactly the claim's counter shape)

Command: `python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (run from scratch; no tree writes).

| Tree | Expected | Observed | Exit |
|---|---|---|---|
| base `903d47e` SHONEN.md (exported to scratch via `git show 903d47e:SHONEN.md`, run with `--file`) | `canonical=0 finding=SF-PREAMBLE exit=1` (expect_before) | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` | 1 ✓ |
| HEAD `3d7e042` / worktree SHONEN.md (identical bytes, sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`) | `canonical=1 finding=SF-CLEAN exit=0` (expect_after) | `shonen-form canonical=1 finding=SF-CLEAN exit=0` | 0 ✓ |
| archive `.ufo/waves/round-48/controls/shonen-before.txt` | preserved historical drift | `canonical=0 finding=SF-PREAMBLE exit=1`; sha256 `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` — exactly the kill rule's required archive hash | 1 ✓ |
| do-nothing control `controls/do-nothing.txt` | before-state witness | `canonical=0 finding=SF-PREAMBLE exit=1 / PROCESS_EXIT=1` | ✓ |

Kill-rule limbs checked:
- `canonical=1` at the final measured revision — yes (HEAD and worktree agree; `git diff HEAD -- SHONEN.md` empty, so the canonical form is landed, not merely in-flight).
- Hidden/commented/duplicate checklist passing — the file is a single 761-byte canonical form; the checker's exact-preamble/exactly-four-boxes/no-trailing-content grammar leaves no room, and the 17 pre-freeze tree fixtures (`controls/fixtures.json`: fenced, commented, duplicate, extra-prose, crlf, no-newline, wrong-label ×4, missing-evidence ×4, canonical) all carry their disclosed exits. No second checklist exists anywhere in SHONEN.md.
- Restoration loses historical bytes — no: archive sha256 matches the frozen required value; the drifted 356-line state is retained byte-for-byte.

## Evidence pointers — one per box, resolution check

The frozen checker's SF-CLEAN result already requires every pointer to be a plain repo-relative existing file; I additionally resolved each by hand:

| Box | Mark | Pointer | Resolves? | Semantic check of the evidence line |
|---|---|---|---|---|
| 1 | `[~]` | `SKILL.md` | yes (134.9 KB, in-root relative) | Line reads "Author assertion; outside promotion verification remains required." — honest author-side assertion; no promotion claim. Pointer exists; content plausibility (decision tables/registry) visible in-file, but semantic truth of box 1 is outside this seat's scope (not promotion review). |
| 2 | `[ ]` | `LOG.md` | yes | Line reads "No new end-to-end domain task claimed; source and diagnostic work only." — verified honest, see below. |
| 3 | `[~]` | `corpus/lessons/round-47-verifier-spotcheck.md` | yes (15,519 B) | File is the round-47 non-author closure; it records "Rechecks execute at the declared lane root: 67/67, gated=22, broken=0, exit 0" — matches the line "Declared-root recheck observations; not promotion." Round-47-era document used as current evidence: historical but topically exact; consistent with held scores. Honest. |
| 4 | `[~]` | `PROVINCE.md` | yes | `git diff --numstat 3546f70 -- PROVINCE.md` empty; neither round-48 commit (`3546f70`, `3d7e042`) touches it. Line "Scope unchanged; live-target testing remains refused" matches the file's standing refusal. Honest. |

## Box 2 — honestly remains unchecked

Verdict: yes. Box 2 is `[ ]` (not even author-asserted `[~]`), and the unchecked state is truthful:

- LOG.md has exactly one round-48 section (`## Round 48 — canonical checklist restoration (L1 KasegiR48)`, :2045): one claim on depth:verifiability, "no coverage claim or domain-task claim"; work described is checklist restoration and probe dispatch.
- LOG.md contains no end-to-end domain-task entry for round 48 (the single `end-to-end` grep hit is a round-36 frontier line about "end-of-file amendments", unrelated).
- Rounds 42–47 each logged "no end-to-end domain hunt ran"; the round-47 non-author closure (`corpus/lessons/round-47-verifier-spotcheck.md` §6) states: "Box 2 (end-to-end domain task) still has no executed end-to-end item — the lane claims none, honestly."
- The round-48 wave (dispatch 1003 lines, 64 seats) is probes/reviews only; no hunt-to-claim seat. The claim's own `mechanical_limits` concede "no source restoration or end-to-end bounty task claimed."
- No `[x]` anywhere in SHONEN.md (`grep -c '\[x]'` = 0): no author-side promotion attestation, and the frozen checker rejects any `[x]` author-side (SF-VERIFIER limb) rather than pretending to verify independence. Marks are `~, space, ~, ~`.

## Round-47 verifier routes R1/R2 (as relevant)

- R1 (canonical-form drift, 52 accumulated marks): answered by this claim — drifted bytes archived, canonical form restored and green on the frozen counter.
- R2 (prose-sensitive plain count `supersedes S074` = 2 vs frozen target 1): cited in LOG.md round-48 as motivation; the round-48 counter is grammar-based, not a bare grep, and lesson R55 requires row-shape anchoring. Frozen round-47 bytes untouched (errata discipline held).

## Findings

No defects found in scope. Expected vs observed match on every measured limb: base SF-PREAMBLE/exit 1, after SF-CLEAN/exit 0, archive sha256 `596122c0…`, claims bytes frozen at `b8022cdf…`, checker bytes frozen at `0ab32a2c…` since commit `3546f70`.

## Residual risk and verification gaps

- The checker validates a deliberately restricted author-side grammar plus pointer *existence* only; it does not and cannot establish evidence meaning, pointer topicality at this round, or independent-verifier identity (the lane discloses the same in `corpus/lessons/round-48.md` §Limits — honest saturation posture: 17 fixtures + 6 mutants are finite, not universal).
- Box 3's evidence is a round-47 document; no round-48 re-execution is cited inside the box. Consistent with held scores, but a future round re-running the declared-root rechecks would strengthen it.
- Worktree carries an uncommitted `SKILL.md` modification from a sibling seat's in-flight work; it does not touch SHONEN.md, LOG.md, PROVINCE.md, or the measured bytes above, and pointer resolution is unaffected.
- Semantic truth of boxes 1/3/4 (promotion-grade evidence) remains unreviewed here by design — this seat is form-and-pointer review, not promotion.

## Commands run (all read-only; scratch under /fast/scratch/hyaku/kasegi-r48/R48Review04)

- `python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` → `canonical=1 finding=SF-CLEAN exit=0` (exit 0)
- `python3 corpus/instruments/shonen-form.py --root <lane> --file <scratch>/base-SHONEN.md` (base `903d47e` export) → `canonical=0 finding=SF-PREAMBLE exit=1` (exit 1)
- `sha256sum` over claims.json, freeze inputs, SHONEN.md (worktree + HEAD export), shonen-before.txt, shonen-form.py — values quoted above
- `git log/show/diff --numstat` over `3546f70`, `3d7e042`, `903d47e` for SHONEN.md, LOG.md, PROVINCE.md, spotcheck lesson, instrument
- `grep -n '^## Round 48'`, `grep -c 'end-to-end'` on LOG.md; `grep -c '\[x]'` on SHONEN.md
- No installs this seat. Scratch removed after filing.
