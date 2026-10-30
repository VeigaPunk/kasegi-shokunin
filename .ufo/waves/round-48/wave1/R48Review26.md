# R48Review26 — Normative source re-open: snapshot byte digest vs live protocol; Gate quote location and word count

- Seat: R48Review26 (reviewer, wave 1, round 48, kasegi lane)
- Axis: depth:verifiability
- Claim reviewed: C1 (routed-defect-closure, `SHONEN.md` canonical four-box author-assessment grammar) — frozen predicate: `shonen-form canonical=1 finding=SF-CLEAN exit=0` at the measured revision; frozen counter `python3 {tool}/corpus/instruments/shonen-form.py --root {tree}`.
- Frozen claim: `.ufo/waves/round-48/claims.json` @ commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` — verified read-only: `git show -s --format='%H %ci %s' 3546f7089c224ac6c8adc68208b1e648bbf3e6a5` → `3546f7089c224ac6c8adc68208b1e648bbf3e6a5 2026-10-30 11:31:09 -0300 round-48: freeze canonical checklist restoration and controls`. The "at 3546f708…" in the seat header is this freeze **commit id** (40 hex), not a content hash. Working-tree `claims.json` sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` matches `freeze.txt` (`claims-sha256: b8022cdf…`), and `git status --porcelain` on the frozen files is clean.
- Round-47 routes read: R1 (`SHONEN.md` canonical-form drift, 13 accumulated assessment blocks / 52 `[~]` lines — basis of C1; `corpus/lessons/round-47-verifier-spotcheck.md` §6 L85), R2 (frozen plain-target phrasing `supersedes S074`; L86). R1 is exercised by C1's counter; R2 is not exercised by this review.
- Production edits: none. Read-only review. Receipts were staged under `/fast/scratch/hyaku/kasegi-r48/R48Review26/` and removed after this report landed.

## Probe 1 — Re-open local normative source path; compare snapshot byte digest

The normative source path (S077 row, `corpus/SOURCES.md` L83: "PROTOCOL.md File contract per shokunin repo, SHONEN.md row and canonical seed") resolves to the main-repo file `/home/vgpnk/Projects/shokunin/PROTOCOL.md` — the kasegi lane root holds no `PROTOCOL.md`, and a full-depth `find /home/vgpnk/Projects/shokunin -name PROTOCOL.md -not -path '*/.git/*'` locates exactly this one file.

Exact commands and observed output:

```
$ sha256sum /home/vgpnk/Projects/shokunin/PROTOCOL.md \
    kasegi-shokunin/.ufo/waves/round-48/controls/protocol-source.txt
886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a  /home/vgpnk/Projects/shokunin/PROTOCOL.md   (live, 533 lines / 46627 bytes)
622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0  kasegi-shokunin/.ufo/waves/round-48/controls/protocol-source.txt   (snapshot, 544 lines / 46958 bytes)

$ diff /home/vgpnk/Projects/shokunin/PROTOCOL.md <snapshot> | grep -c '^[0-9][0-9,cd]*$'
12        # 12 hunks; 30 live-only + 41 snapshot-only changed lines
```

Provenance of both sides (read-only git inspection of the main repo):

- **Live file**: `git status --porcelain -- PROTOCOL.md` is clean; content sha256 `886e459b…` is byte-identical to commits `f47ad6ba` (2026-10-25 09:29:03 -0300, `repair: restore fleet tree deleted by stray commit 35b91714`, author protocol-shokunin) and `7c5b34f0` (round-16 revision) — i.e. the post-repair tree carries the round-16-vintage protocol bytes.
- **Snapshot**: sha256 `622b29a0…` matches **none** of the 27 commits touching `PROTOCOL.md` across all refs (`git log --all --format=%H -- PROTOCOL.md`, each `git show <c>:PROTOCOL.md | sha256sum`), and no second `PROTOCOL.md` copy exists anywhere in the fleet.

Expected vs observed:

| Check | Expected | Observed | Verdict |
|---|---|---|---|
| Snapshot == live normative source bytes | equal digests (S077 describes the snapshot as the protocol's normative form) | `622b29a0…` vs `886e459b…` — whole-file **MISMATCH** (12 hunks) | DRIFT — reported, not repaired (counter bytes/predicate frozen) |
| Claim-relevant region identical in both | SHONEN.md File-contract row + canonical seed + Marks line byte-equal | content-anchored `diff` of `sed -n '/^The canonical .SHONEN.md. seed/,/non-author verifier per \*\*Promotion gates\*\*\./p'` → identical; `grep -m1 '^| .SHONEN.md. |'` row diff → identical | MATCH |

Character of the drift (from the 12 hunks): the snapshot carries material absent from the live file (Trend-verdicts paragraph, watchdog source-census paragraph, `render_prompt()` clause in Gate standard Delivery, `trends`-verdict shape in closure entries, shorter `corpus/SOURCES.md` row) and the live file carries material absent from the snapshot (root-ledgers gate paragraph, `kaika` SOURCES-contract fallback row, `(§Appendix, "Multi-claim rounds")` annotation, "upstream fleet" host-note phrasing). Neither direction is a strict superset.

**Assessment.** The whole-file byte comparison is a **defeat of the expectation** that the frozen snapshot reproduces the live normative source; it is **not** a counter defeat — the frozen counter `shonen-form.py` (sha256 `0ab32a2c…`, matching the R48Probe25 record) grades `SHONEN.md`, not `PROTOCOL.md`, and the exact normative region C1 cites (File-contract `SHONEN.md` row, canonical seed, Promotion-gates Marks rule) is byte-identical in live and snapshot. Because the snapshot's byte state is anchored in neither the working tree nor any commit of the main repo, the drift is recorded here as residual risk for KasegiR48's integration verdict; nothing was edited.

## Probe 2 — Locate the Gate quote; count words

The gate quote carried by the canonical `SHONEN.md` seed (the sentence binding marks to **Promotion gates**, which is the normative basis the frozen checker enforces):

- **Snapshot** `.ufo/waves/round-48/controls/protocol-source.txt` **L464–465**; **live** `PROTOCOL.md` **L450–451** (identical bytes in both, per Probe 1).

```
$ sed -n '464,465p' <snapshot> | wc -w      # live L450-451 yields the same count
Marks: `[~]` asserted by the lane itself (evidence pointer required), `[x]` only with a named
non-author verifier per **Promotion gates**.
20                                          # 20 words by wc -w (whitespace tokenisation; md-stripped recount also 20)
```

Word counts for the other gate quotes in the normative source, same method (`wc -w` on the exact span), snapshot line spans, live counts identical where the span exists in the live file:

| Quote | Snapshot span | Words (`wc -w`) | Live span | Live count |
|---|---|---|---|---|
| Marks line — "…`[x]` only with a named non-author verifier per **Promotion gates**." (canonical seed, quotes the gate rule) | L464–465 | **20** | L450–451 | 20 |
| Gate standard definition — "A **gate** is a committed, re-runnable verdict script… registered as one." | L390–392 | 41 | L377–379 | 41 |
| Promotion gates section intro — "A promotion is a decision backed by artifacts, not a vibe; every gate names its verifier and its evidence." | L61–62 | 19 | L61–62 | 19 |
| shonen → shokunin gate bullet (full rule) | L63–71 | 137 | — | — |

The primary "Gate quote" for C1 is the Marks line: **20 words**, located at snapshot L464–465 / live L450–451, byte-identical in frozen snapshot and live source. Counting command recorded verbatim above; count is stable across both files.

## Conclusions

- Snapshot-vs-live digest comparison: **MISMATCH** at whole-file level (`622b29a0…` vs `886e459b…`, 12 hunks); **MATCH** at the claim-relevant normative region (`SHONEN.md` File-contract row, canonical seed, Marks line byte-identical). The snapshot is not reproducible from any committed or working-tree `PROTOCOL.md` state in the fleet — recorded as residual risk, not repaired.
- Gate quote located and measured: Marks line = 20 words (`wc -w`), snapshot L464–465 = live L450–451; secondary gate quotes counted with exact spans and commands.
- No evidence against the frozen C1 predicate was observed; the frozen counter, canonical candidate, and production `SHONEN.md` hashes at this tree (`0ab32a2c…`, `b476c7aa…`, `b1352168…`) match the values recorded by sibling probes.
- No production, fleet, or sibling files were written; no tools installed (python3 host stdlib, `sha256sum`, `diff`, `sed`, `wc` only); pacman untouched. Scratch receipts (`hashes.receipt.txt`, `gate-quotes.receipt.txt`, `drift.receipt.txt`, `provenance.receipt.txt`, `seed-block.receipt.txt`) were transcribed into this report and the scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Review26/` removed on exit.

## Residual risk / verification gaps

- The provenance of `controls/protocol-source.txt`'s exact byte state is unresolvable inside the fleet (no commit, no second file). Whether it was captured from a since-changed working tree, a sibling worktree outside the fleet root, or the upstream vendored copy cannot be established from this seat's read-only tools — flagged for the integration owner; the claim's mechanics do not depend on it.
- The live protocol's drift from the snapshot (e.g. missing Trend-verdicts/rule paragraphs in the live file) is a main-repo protocol-lane matter outside this lane's write scope; noted here as cross-domain evidence only.
- Word counts use `wc -w` whitespace tokenisation; markdown backtick/asterisk punctuation is attached to tokens and counted (a punctuation-stripped recount of the Marks line returns the same 20).
