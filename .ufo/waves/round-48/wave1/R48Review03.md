# R48Review03 — S077 tier & scope attack: own-work normative protocol vs bounty knowledge; overclaim rejection

- Seat: R48Review03 (critic, leaf — no subagent dispatch), kasegi round 48, wave1.
- Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Frozen claim: C1 only (`.ufo/waves/round-48/claims.json` sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matches `freeze.txt` pin; frozen commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`; base `903d47e13058982460f0d90c1c2b9c7c02680646`).
- Seat item: attack source S077 tier and scope — own-work normative protocol versus bounty knowledge; reject overclaims.
- Counter (read-only, not edited): `corpus/instruments/shonen-form.py`, sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (working tree == freeze commit `3546f70`).

## Verdict

**No defeat of C1 from the S077 tier/scope angle, and no overclaim found in the claim package or any landed wave-1 report.** S077 is correctly scoped as a procedural, normative protocol source; nothing in the round-48 package presents it as bounty knowledge, frontier ground, promotion evidence, or an executed domain task. Two minor non-blocking items are recorded for the integrator: an anchor-provenance precision defect (true origin path not named in the row; live main-repo `PROTOCOL.md` has drifted from the snapshot whole-file) and a kind-label tradeoff (`own-work` vs `spec`). Neither touches the claim-relevant normative region, the frozen counter, or the measured before/after limbs.

## Probe 1 — S077 row vs the CORPUS.md contract (tier and shape)

Exact commands and observed output:

```
$ sed -n '83p' corpus/SOURCES.md | cut -c1-200
| S077 | Canonical Shokunin protocol checklist contract — .ufo/waves/round-48/controls/protocol-source.txt | own-work | A | Normative form of this lane's promotion checklist, not bounty policy or promotion evidence | ...

$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {...enum check...}' corpus/SOURCES.md
(enum check)            -> no output (kind own-work valid; tier A valid; status mined valid; no tier-inflation)

$ awk duplicate-id check / used-by existence check (CORPUS.md lint block)
                          -> no output; corpus/lessons/round-48.md exists
```

- Kind `own-work` is a valid CORPUS.md enum value (`spec · docs · paper · code · tool · dataset · talk · book · community · own-work`); the fleet census validator also reports zero findings (`R48Review25`: registry 76→77 rows, exactly +1 tier-A +1 mined = S077, `DIFF_EXIT=0` against `controls/census-before.txt`).
- Tier A is scoped to the row's scope cell ("this lane's promotion checklist" form). Per CORPUS.md, tier A includes "spec … maintainer statement" authoritative for the scope; the protocol is exactly that for checklist form. Not inflation.
- `used-by` = `corpus/lessons/round-48.md` resolves; lesson `## Gate` records access date 2026-10-30, origin path, and a 16-word located quote ("marks are confined to the box character plus one indented evidence line per box") satisfying SOURCES rule 1.

**Tradeoff (not a defect):** the protocol is fleet normative infrastructure maintained by the protocol lane/operator, not bytes authored by the kasegi lane; its kind could equally be argued `spec`. CORPUS.md assigns no exclusive per-kind semantics beyond the source-field note ("a repo path or command for `own-work`"), the S077 source cell is exactly an in-repo snapshot path, and C1's validity does not depend on the kind label. Accepted as curation judgment.

## Probe 2 — scope attack: is any bounty knowledge smuggled in as S077?

I read the full 544-line snapshot (`controls/protocol-source.txt`) cover to cover. Content: lifecycle, promotion gates, round-robin rules, evidence standard, gate standard, file contract, invariants, fleet-2 conventions, appendix pointer. **Zero bounty-policy, target, program, or vulnerability-knowledge content.** The claim-relevant region — File contract `SHONEN.md` row, the canonical four-box seed, and the Promotion-gates Marks rule — is procedural checklist grammar only.

Cross-checked every place the round cites S077:

| Surface | Statement | Observed |
|---|---|---|
| C1 `source` / `mechanical_limits` | "normative protocol File contract and Promotion gates"; "form validation, not promotion or evidence truth"; "no source restoration or end-to-end bounty task claimed" | consistent, no overreach |
| LOG.md Round 48 | "Source S077 is the normative protocol, opened this round, not a bounty policy"; "no coverage claim or domain-task claim" | consistent |
| `corpus/lessons/round-48.md` Gate | "S077 admitted as own-work/tier A for this lane's normative checklist form only"; Reject list: "promotion, semantic evidence verification, an executed bounty task, or restored lost sources"; "The source snapshot is a procedural source, not new bounty-domain knowledge" | consistent |
| SOURCES search log | "The Bugcrowd reporting page was opened as a preliminary lead, not admitted or used as support … no coverage claim was declared" | consistent — an opened-but-unadmitted page stays a lead, never a row (CORPUS.md Leads rule) |

**Overclaim sweep across all 40+ landed wave-1 reports** (`grep -rinE 'frontier (row|ground)|coverage claim|new (domain )?(source|knowledge)|bounty'` with negation for disclaimers): no affirmative overclaim found; every hit is a disclaimer ("no promotion claimed", "not promotion", "author assertion", "form-only").

## Probe 3 — provenance precision defect (fixable, reported, not repaired)

Independently reproduced `R48Review26`'s drift finding:

```
$ sha256sum /home/vgpnk/Projects/shokunin/PROTOCOL.md
886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a
$ sha256sum /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md \
            .ufo/waves/round-48/controls/protocol-source.txt
622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0   (both identical)
$ diff <(sed -n '/^The canonical .SHONEN.md. seed/,/non-author verifier per \*\*Promotion gates\*\*\./p' PROTOCOL.md) <(same sed on controls/protocol-source.txt)
(empty)   -> REGION-IDENTICAL
$ diff <(grep -m1 '^| .SHONEN.md. |' PROTOCOL.md) <(grep -m1 '^| .SHONEN.md. |' controls/protocol-source.txt)
(empty)   -> ROW-IDENTICAL
```

- The row's anchor names "PROTOCOL.md File contract per shokunin repo". A reader resolving `PROTOCOL.md` naturally lands on the fleet main-repo file (`886e459b`), which has drifted from the snapshot by 12 hunks. The snapshot's true origin — `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` — is recorded only in the lesson Gate, not in the row.
- The claim-relevant region is byte-identical in all copies, so C1's normative basis is stable and the frozen counter is unaffected. The snapshot is itself committed at `3546f70`, so the normative bytes C1 cites are durably anchored.
- **Smallest safe correction:** name the true origin path in the S077 anchor cell (or route a precision defect to the lane's next round). Counter bytes/predicate are frozen — nothing was edited.

## Probe 4 — frozen counter kill-rule limbs, independently exercised

Scratch trees only (`/fast/scratch/hyaku/kasegi-r48/R48Review03/run1`, exported via `git show` exactly like `.ufo/waves/round-48/measure.py`):

| Tree | Expected (C1) | Observed | Match |
|---|---|---|---|
| before `903d47e:SHONEN.md` + 4 pointers | `canonical=0 finding=SF-PREAMBLE exit=1` | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` | YES |
| after `3d7e042:SHONEN.md` + 4 pointers | `canonical=1 finding=SF-CLEAN exit=0` | `shonen-form canonical=1 finding=SF-CLEAN exit=0` | YES |
| do-nothing control (base tree) | matches `controls/do-nothing.txt` | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` | YES |

All 17 frozen fixtures (`controls/fixtures.json`) reproduce expected exit/finding exactly, including the kill-rule shapes: hidden (`fenced`→SF-PREAMBLE), commented (`commented`→SF-PREAMBLE), duplicate (`duplicate`→SF-TRAILING) checklists are all rejected by the frozen checker.

Archive limb: `git show 903d47e:SHONEN.md | sha256sum` = `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` = `controls/shonen-before.txt` (byte-identical, 356 lines, 52 `- [` marks — the "52 author marks" before-figure verified). No-amendment limb: counter sha256 `0ab32a2c…` identical at freeze commit and working tree.

## Probe 5 — adversarial variants beyond the frozen fixtures (grammar edges)

18 extra scratch-tree variants, all correctly classified by the frozen counter:

| Variant | Observed | | Variant | Observed |
|---|---|---|---|---|
| hidden box as 2nd indented line | SF-BOX exit=1 | | fifth extra box | SF-TRAILING exit=1 |
| `[x]` verifier mark | SF-VERIFIER exit=1 | | two evidence lines under one box | SF-BOX exit=1 |
| `[X]` / `[-]` mark | SF-BOX exit=1 | | tab-indented evidence | SF-EVIDENCE exit=1 |
| `../` traversal pointer | SF-POINTER exit=1 | | empty pointer token | SF-POINTER exit=1 |
| absolute `/etc/hostname` pointer | SF-POINTER exit=1 | | trailing-slash `LOG.md/` | SF-POINTER exit=1 |
| directory pointer | SF-POINTER exit=1 | | non-UTF8 bytes | SF-UNREADABLE exit=2 (declared) |
| symlink escape for evidence file | SF-POINTER exit=1 | | verbatim protocol seed (no evidence lines) | SF-CLEAN exit=0 |
| swapped box order | SF-BOX exit=1 | | seed + protocol `Marks:` paragraph | SF-TRAILING exit=1 |
| unchecked `[ ]` box, no evidence line, mixed in | SF-CLEAN exit=0 | | | |

Notable confirmations: the checker's canonical grammar deliberately excludes the protocol template's trailing `Marks:` prose paragraph (File contract: "no other prose"), and it accepts the unchecked-box-no-evidence form — both consistent with the frozen predicate "author-assessment grammar with existing local evidence pointers". The `verbatim-seed` pass also shows the checker is not merely a hash-match of the candidate.

## Pointer existence (predicate limb)

All four evidence pointers in the integrated `SHONEN.md` (`3d7e042`) exist as in-root files: `SKILL.md`, `LOG.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md` (`test -f` each; also implied by SF-CLEAN, which fails SF-POINTER otherwise). Box 2's honest `[ ]` with "No new end-to-end domain task claimed" matches the mechanical limit exactly — no end-to-end bounty task is claimed anywhere in the package.

## Impacted axes and disposition

- **depth:verifiability (C1):** unaffected. Expected vs observed match on before/after, do-nothing, 17 frozen fixtures, kill-rule limbs (hidden/commented/duplicate rejected; archive hash retained; counter frozen). Author-side form only — promotion and semantic truth remain independently judged, as the predicate requires.
- **Findings for the integrator (non-blocking):** (1) S077 anchor provenance precision — name the true origin path (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`) in the row or route a defect; the live main-repo `PROTOCOL.md` drift (12 hunks, claim-region byte-identical) is a residual risk already recorded by `R48Review26`. (2) S077 kind label `own-work` vs `spec` — curation tradeoff, validator-clean, claim-independent.
- **Bounty-scope:** clean. S077 carries no bounty knowledge; no frontier, coverage, promotion, or target-testing overclaim exists in the claim package, LOG, lesson, registry, or any landed wave-1 report.

## Hygiene

- Rules read first: `/home/vgpnk/.omp/agent/RULES.md`. No tools installed or updated; pacman untouched (host-wide pause respected). No target testing, no delegation, no background jobs, no production/fleet/sibling edits, no git/jj mutations — all probes ran on scratch fixture trees.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review03/` (fixture trees, frozen counter copy, `receipts.txt` with the full battery transcript) removed after this report landed.
