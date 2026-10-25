# Round 9 aggregator corpus verdict — kasegi

> **Path convention.** Bare `CORPUS.md`, `PROTOCOL.md`, `MANIFEST.json`, `SCORECARD.md`, `LOG.md`, `.ufo/…` and `<lane>-shokunin/…` pointers in this file are **main-repo (`shokunin`) relative** — they do not resolve inside this checkout. Paths inside this checkout are written `corpus/…`, `SKILL.md`, `SHONEN.md`, `PROVINCE.md`.

Audited revision: `b7180b0` (landed). Main measurement stamp: main HEAD `62fdfbe`; kasegi worktree status `git status --porcelain | wc -l` → 6, so worktree r15 changes are provisional. The landed tree was measured from `git archive b7180b0`.

## Verdict table (CORPUS.md rules 1–10)

| Rule | Verdict | Re-executed command / observed |
|---|---|---|
| 1 | FAIL | `python3 /tmp/kasegi-r9-resolve.py /tmp/kasegi-r9-kasegi head` → 782 distinct / 1001 occurrences; 740 distinct path citations unresolvable after `ls -d /home/vgpnk/Projects/bounties` → exit 2. |
| 2 | PASS | lesson sweep for `round-[0-9]` or `Round: [0-9]` → no lesson lacking round identity. |
| 3 | FAIL | `grep -RniE '592|1088|486|280|7227' corpus` finds claims whose only live source was the vanished tree; landed HEAD has no loss/anchor qualification. |
| 4 | FAIL | `git show b7180b0:corpus/knowledge/mission-ledger.md | grep -nE '[0-9]+ — '` → no output; SCORECARD retains an uncommanded knowledge-entry count. |
| 5 | FAIL | `git show b7180b0:corpus/knowledge/evidence-dir.md | grep -n -C1 george` → “Zero claims dirs reference it” without a sweep in the entry. |
| 6 | PASS | `grep -cE ':[0-9]+' corpus/knowledge/triage-thresholds.md` → 23 location-bearing citations; sampled quotes name source location. |
| 7 | PASS (disclosed minor gap) | README/file comm sweep → no missing knowledge row; README explicitly discloses missing round-2 lesson. |
| 8 | FAIL-literal / PASS-intent | `git grep -n 'op://' b7180b0 -- corpus/` → 2 schematic sweep-description hits (`round-5-aggregator-audit.md:50`, `round-6-aggregator-audit.md:31`), no real vault path. Literal rule text bans every `op://`; secret-pattern sweep for `sk-/ghp_/github_pat_/xox/AKIA/private-key` → 0. |
| 9 | FAIL (contested) | README says r12 repairs were “in place”; `git log --oneline b7180b0 -- corpus/knowledge/` shows repair churn, conflicting with “corrections are new entries.” |
| 10 | PASS for this review | This lesson and its evidence file emit the required revision-named per-repo verdict; AGGREGATE §13 residual had no prior per-repo table. |

**Overall: not conformant.** Failed rules: 1, 3, 4, 5, literal 8, and contested 9.

## Lost-source blast radius

Extraction command: `python3 /tmp/kasegi-r9-resolve.py /tmp/kasegi-r9-kasegi head`, run twice with `diff`; output was `DETERMINISTIC`, `782 distinct`, `1001 occurrences`, `740 unresolvable`, md5 `e67165be25c0bfd87a1a1deb5fb79b19`. By scope: SKILL 173 unresolvable distinct, PROVINCE 1, corpus 566. `PROVINCE.md` still declares `~/Projects/bounties`; `git status --short -- PROVINCE.md` → empty, so the §File contract correction was not made. A vanished cited source cannot pass rules 1/3/5 strictly: path resolution, falsifiability, and re-runnable negative sweeps are all lost. Historical command output can remain provenance only with as-of and loss/anchor qualification, absent from landed HEAD.

## Box-3 re-run

At landed `b7180b0`, `ls -d /home/vgpnk/Projects/bounties/claims` → exit 2, so the live r8 command set is not executable. The verdict is **still provisional / could-not-evaluate**, not firm/broken. The wrong-path `program-quirks` citation is a **firm break**. Mirror-only `ev-report.mjs` checks (copied to `/tmp`, not substituted for the lost tree): no-arg → exit 2; nonexistent program → exit 2. This firms only the frozen mirror, while the r8 live result and `check-freshness` exit claim remain unevaluable; the committed 30/280 sampling claim remains provisional because its 280-package evidence tree is gone.

## Movement from round-6 §11.1

Round-6 baseline: `not conformant — 4,5,7,9(contested),1/6; 7 majors / 11 defects` at `fb9ac8e`. Rule 1/6 improved through citation repairs but **regressed in present resolvability** (740 gone); rule 4 **improved but still fails** (archive count corrected, mission-ledger commands absent); rule 5 **unchanged/fail** (george negative lacks sweep); rule 7 **improved** (program-quirks row added; round-2 gap disclosed); rule 9 **unchanged contested/fail** (in-place repairs continue); literal rule 8 is a new failure. The old 7/11 defect totals are not recomputable after source-tree loss.

## Routed rows

| owner | severity | claim | evidence | command |
|---|---:|---|---|---|
| operator/integrator | 2 | CORPUS rule 8 literal `op://` ban conflicts with intended schematic-placeholder practice | landed corpus has 2 schematic hits, no secret values | `git grep -n 'op://' b7180b0 -- corpus/` |
| kasegi | 3 | PROVINCE still names absent bounties root | `PROVINCE.md` unchanged; root absent | `ls -d /home/vgpnk/Projects/bounties`; `git status --short -- PROVINCE.md` |
| kasegi | 3 | 740 distinct citations are unresolvable as written | deterministic census output above | `python3 /tmp/kasegi-r9-resolve.py ...` |
| kasegi | 2 | negative george claim lacks embedded sweep | `corpus/knowledge/evidence-dir.md` line 78 | `git show b7180b0:corpus/knowledge/evidence-dir.md | grep -n -C1 george` |
