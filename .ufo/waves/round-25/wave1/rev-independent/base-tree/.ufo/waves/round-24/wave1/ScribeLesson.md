# ScribeLesson — round 24, wave 1 (kasegi)

Seat: scribe (`L1Kasegi24.ScribeLesson`), read-only. Assignment: mine one round-24 `## Mistakes`
entry from r23 committed bytes and propose it; draft lives in `/tmp`, never in the lane.
Everything below is observed from committed bytes at base
`d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`; `master` has since advanced by one commit,
`c2480b1` ("round-23 verifier spot-check"), which adds only
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-23-verifier-spotcheck.md`
(`git show --stat c2480b1` → `1 file changed, 142 insertions(+)`). Every line cited is identical at
both commits.

## Findings

**F1 — The r23 repair claim "every `recheck:` line now begins `cd …`" is false at 3 of 33, and 3 of 8
on the surface it repaired.** `grep -n 'every `recheck:` line now begins' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-23.md`
→ line 254 (RecheckAsWritten F-RA-1 row). Census over
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/*.md`:
`grep -rh '^recheck: ' … | wc -l` → **33**; `… | grep -c '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&'` → **3**.
Among the eight entries whose recheck invokes `source-recheck.py`: prefixed = `cna-assignment-and-vulnerability-rules`, `cra-manufacturer-reporting-duties`, `multiparty-vulnerability-coordination`; **not** prefixed = `cvss-v4-severity-and-vector`, `coordinated-disclosure-timelines`, `authorization-safe-harbor-and-scope`, `ai-assisted-finding-validation`, `cwe-top25-2025-methodology`.

**F2 — Those five fail from outside the repo with a file error, not with the "no capture" failure the
lane recorded.** Running all eight published `recheck:` commands as written from `/tmp`:

```
ai-assisted-finding-validation rc=2  python3: can't open file '/tmp/corpus/instruments/source-recheck.py': [Errno 2]
authorization-safe-harbor-and-scope rc=2  (same)
cna-assignment-and-vulnerability-rules rc=0  S031:version-4-2-6 OK
coordinated-disclosure-timelines rc=2  (same)
cra-manufacturer-reporting-duties rc=0  S029:art71-general-application OK
cvss-v4-severity-and-vector rc=2  (same)
cwe-top25-2025-methodology rc=2  (same)
multiparty-vulnerability-coordination rc=0  S018:upstream-vendor-def OK
```

From the repo root the five give `S001:source UNAVAILABLE reason=not-listed`, `EXIT=2`
(`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S001`).

**F3 — The manifest cannot hold their source ids, by its own declaration.** `manifest.json` `purpose`:
"Round-23 F06-F08 captured-source assertions. …"; `sources` = `S018, S029, S030, S031` (four), and
`ls /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/` shows exactly
four `S*.txt` plus the manifest. So no S001–S015 row exists to hit.

**F4 — Origin of the five lines is a blind bulk rewrite in a checkpoint, on a tree with no
manifest.** `git show 8bf9807 -- corpus/knowledge/cvss-v4-severity-and-vector.md` replaces the prose
recheck with `--manifest corpus/source-snapshots/round-23/manifest.json --source S001 && … --source S002`;
the commit message is "checkpoint(r23): archive developed corpus and local tooling; policy-paused,
unadmitted, no task resumption"; `git ls-tree -r --name-only 8bf9807 -- corpus/source-snapshots`
→ `S018.txt, S029.txt, S030.txt` only (no `manifest.json`). The same hunk touched eight knowledge
files, of which three eventually got manifest rows and five did not.

**F5 — The r23 record names the symptom and routes the fix, but not the authorship error.**
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-23.md:279-284` says the five
"point at this round's manifest, which lists S018/S029/S030/S031 only, so each exits 2 `not-listed`
(reproduced)" and needs "fifteen snapshots, which is a later round's work". Nothing says the rewrite
was never executed at landing nor that the repair claim covered a 3/8 sample.

**F6 — The "6/6, 13/13" cells are backed by a receipt path that was overwritten five times in-round,
with no commit pin.** `git log --oneline --follow -- .ufo/waves/round-23/c1-fixed.json` → `f6966d4`,
`bf9ce02`, `12edac4`, `2712c99`, `953c278`; `git show <c>:.ufo/waves/round-23/c1-fixed.json` →
`953c278` 13 cases / `5e61a33ed5fa`, `2712c99` 20 / `4e39f65c7c1b`, `12edac4` 23 / `332a5fe95b94`,
`bf9ce02` 24 / `d05b1e0cf627`, `f6966d4` 24 / `d05b1e0cf627`. At HEAD,
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md:403` and
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md:1127` still print "6/6 … 13/13, exit 0" with
`matrix_sha256=5e61a33e…b5e76a9` and `LOG.md:1127` still points at `c1-fixed.json` for it, which now
holds `d05b1e0c`. `5e61a33e` survives at HEAD only in prose and seat reports, never in a receipt
file; the 13/13 bytes live only at commit `953c278`, a pin neither document names.

**F7 — "detector soundness" survives at four claim-bearing sites while the errata says the scope is
otherwise.** `SCORECARD.md:370`, `corpus/lessons/round-23.md:1`, `:71`, `LOG.md:1114`, against
`SCORECARD.md:442-446` ("The axis move is **mirror-fallback soundness**, not 'detector soundness'")
and `resolve.py`'s policy docstring (REL domain: `INTERNAL` "NOT confined"; BOUNTY literal hit
"CARVE-OUT"). `LOG.md:1114` is self-contradicting: its heading says detector soundness, its body two
lines later says "C1 depth:verifiability mirror-fallback soundness". This is not new information —
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/falsify/AnchorDebt.md:99,212`
already names both sites and recommends alignment — so it is an unlanded finding, not a round-24
mine.

**F8 — Result of the mine.** One entry survives as new and is worth the round's `## Mistakes` row:
M24-1, "a repair's universal claim landed on a partial fix" (class: universal quantifier wider than
the receipt's sample, plus a rewrite executed at no point). Candidates C-a ("detector soundness") and
C-b ("6/6, 13/13") each survive scrutiny but are not new mines for the reasons in F7 and in the draft;
C-b is the stronger second row if the round wants two (class: number kept as history, evidence path
rewritten in place, no commit pin; captured-by: R3 not extended to superseded measurements).
C-c (F01–F05 vs an impossible manifest) folds into M24-1 rather than repeating it.

## Behavior

- Read the frozen claims (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json`)
  and both r23 lesson files before touching evidence; read r23 falsify seats only where a finding's
  provenance mattered.
- Reproduced, read-only: the eight `recheck:` commands from `/tmp` and from the repo root, the
  manifest purpose/source dump, the `8bf9807` tree and hunk, the receipt-file history and per-commit
  case counts. No network, no live target, no lane write, no git state change, no jj.
- Draft written to `/tmp/kasegi-r24-lesson-mistakes.md` (9 380 B). This report is the only lane file
  written.

## Gates

- Read-only seat honoured: only `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/ScribeLesson.md`
  written in the lane; draft in `/tmp`; no commit/push/jj, no `git add/checkout/reset/stash`.
- `/home/vgpnk/Projects/shokuknow` untouched; no sibling repo, fleet `templates/`, `scripts/`,
  `MANIFEST.json`, `.ufo/state/`, `watchdog.log` touched.
- Build/lint/test/formatter suite skipped per assignment (L1 runs round-level verification).
- Tooling: nothing installed, nothing upgraded (host pacman pause respected). No package need arose.

## Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/ScribeLesson.md`,
  `/tmp/kasegi-r24-lesson-mistakes.md`.
- Read: `…/.ufo/waves/round-24/claims.json`, `…/corpus/lessons/round-23.md`,
  `…/corpus/lessons/round-23-verifier-spotcheck.md`, `…/corpus/knowledge/*.md` (recheck lines),
  `…/corpus/instruments/resolve.py`, `…/corpus/instruments/source-recheck.py` (executed read-only),
  `…/corpus/source-snapshots/round-23/{manifest.json,S0*.txt}`, `…/SCORECARD.md`, `…/LOG.md`,
  `…/.ufo/waves/round-23/falsify/{AnchorDebt,RerunMatrix,…}.md`, `…/.ufo/waves/round-23/build/{CvssRecheck,AiRecheck}.md`,
  `…/.ufo/waves/round-23/c1-{fixed,baseline}.json` (HEAD and five historical commits).

## Out of scope (not done, by contract)

- No edit to `corpus/lessons/`, `SCORECARD.md`, `LOG.md`, `resolve.py`, the manifest, or any r23
  receipt — the M24-1 row is a proposal for the round-24 author, and the r23-hosted defects (F6, F7)
  are routed, not repaired.
- No install/upgrade; no pacman; no host service action.
- No verification of the round's own C1/C2 work and no re-run of r23 measurements beyond what the
  mined entry needed.

## Limits / UNVERIFIED

- "Cannot list S001–S015" is verified of the **committed** manifest only (`purpose` + four source
  entries + four snapshot files). The manifest is a file, not a frozen schema; the draft therefore
  asserts "cannot hold the source id as scoped and populated", which is what the bytes show.
- Whether the five un-prefixed lines were *intended* to run from the repo root (they predate the r23
  standard) is UNVERIFIED; no commit states an intent. The row does not rest on it.
- C-b's consumer impact is UNVERIFIED beyond the two committed sites that still print `5e61a33e`
  (`SCORECARD.md:403`, `LOG.md:1127`); I did not search the fleet repo for readers of those cells
  (out of this seat's scope and its tree).
- `corpus/lessons/round-23.md:254`'s sentence could be read as "every line this repair touched"; the
  repair row's own wording ("every `recheck:` line") and the 3/8 source-recheck subset falsify it on
  either reading, which is why the entry states both the `3/33` and `3/8` numbers.

## Artifact paths

- Report: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/ScribeLesson.md`
- Draft (proposed `## Mistakes` row + candidate dispositions + reproduction block):
  `/tmp/kasegi-r24-lesson-mistakes.md`
