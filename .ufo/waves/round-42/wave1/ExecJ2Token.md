# ExecJ2Token — round 42, wave 1 (seat receipt)

- **Seat**: `ExecJ2Token` (executor, leaf — no subagent dispatch; no labrat probe was needed).
- **Lane**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `5053a7f46de35784cff4b56756906e9014a38276`.
- **Item**: family **F-TOKEN** — the J2 limb of the round-42 C1 closure suite
  (`corpus/instruments/r42-closure.sh`), closing the round-41 **I3** token-boundary/tally defect.
- **Deliverables** (written beside this receipt, in `.ufo/waves/round-42/wave1/`):
  - `ExecJ2Token.sh` — the sourceable limb. **682 lines**,
    sha256 `2ae17efebe09eca90beca06e8b3b644c7e983b882a5b09e47b7894118136e408`.
  - `ExecJ2Token.transcript.txt` — the teed transcript. **114 lines**,
    sha256 `7bd2d26391b84756411c925b551774f4125d4315bc4c4fc4824027b1ffcdfc61`.
  - this receipt.
- The lane's `corpus/instruments/r42-closure.sh` does **not** exist yet (the L1 lands it), so this
  seat delivers the limb as a **sourceable file**, not as an edit of a suite that does not exist.

## The defect it repairs, and the repair

The committed defeat is `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-41/wave2/RevC1Counters.md`
(selftest detail `mutant=mangled-value-token rejected=0`; reproduced LIVE in transcript §5):
the r41 `selftest_case_i3` rewrites the **first** `Correction (round 41)` line of `SCORECARD.md` with a
synthetic line whose truth tally reads `closed=10/100`, and the r41 I3 grader still reports
`tally=3/3 mangled=0` (`selftest case=I3 mutants=0/1 … verdict=fail`). Two independent holes:

1. **value presence instead of value equality** — `closed=10/10` is a substring of `closed=10/100`, so a
   substring/prefix presence test never distinguishes the mangled form from the truth;
2. **per-record union instead of per-line grading** — I3 breaks on the first line of a record that hits, and
   its `mangled` counter only runs when *no* line in the record hits, so the mangled line is masked by its
   surviving duplicated twin (D-r41-1 put 8 `Correction (round 41)` lines in `SCORECARD.md`).

J2 closes both: every `closed=<n>/<m>`, `failures=<k>`, `cases=<k>` value is **extracted as a whole token**
and compared by **full value equality** against an expected value **derived from the tree's own committed
closure receipts**, and **every graded rule is per line**, so a sibling cannot mask a defect.

### Whole-token rule (implemented once, in `J2_AWK.scan_line`)

A tally token is `KEY=VALUE`, `KEY ∈ {closed, failures, cases}`, `VALUE = <digits>` or (`closed` only)
`<digits>/<digits>`. It is a whole token only when the character before `KEY` is neither `[A-Za-z0-9_]`
nor `/`, the value immediately follows `=`, the value is the maximal digit run (one `/` with digits on both
sides) and the character after it is neither `[A-Za-z0-9_]` nor `/`. Consequences, all exercised by the
probe battery: `closed=10/100`, `closed=13/130`, `closed=13/13x`, `closed=13/13/7`, `closed=13/` never yield
`closed=10/10` or `closed=13/13`; `xclosed=`, `unclosed=` and `/closed=` do not yield `closed=`;
`closed= 13/13` and `closed =13/13` are residuals. **Regex word boundaries are not sufficient** — `\b` treats
`/` as a non-word character, so `\bclosed=10/10\b` matches inside `closed=10/10/12`, and a plain substring
test matches `closed=10/10` inside `closed=10/100`.

### What `check_j2 TREE REF` grades (payload keys)

| Field | Requirement |
|---|---|
| `records=3` | `SCORECARD.md`, `LOG.md`, `SHONEN.md` all present |
| `graded=N` | live `Correction (round N)` line sets found (fence-aware; a fenced correction-shaped line is counted in `fenced=` and is **not** graded — verified with a ```` ```text ```` pseudo-row fixture: `fenced=1,near=0`, still CLOSED) |
| `resid=0` | no residual tally occurrence in any live correction line: fused key, spaced key, spaced value, truncated ratio, trailing word character, trailing slash |
| `near=0` | no extracted value is a **deletion variant** of an expected truth value (same key, same arity, one numeric field obtained from the corresponding expected field by deleting ≥1 digit — `10/100` vs `10/10`, `13/130` vs `13/13`, `1/13` vs `13/13`, `10` vs `1`). This is what makes a mangled citation RED while a sibling still carries the exact truth: the defect is **detected**, never masked |
| `cited=K/M` | for every graded round N, every record whose round-N lines carry tally citations carries the expected truth `closed=<T(N)>` as a whole token (M must be > 0) |
| `anch=K/M` | every round-N line that cites the round-(N-1) receipt **path** and carries a `closed=` token carries the exact truth token — the per-line truth enforcer |
| `probe=K/M` | the extractor battery passes (22 probes: 10 accept, 12 reject) |
| `truth=ok` | no round cites tallies while its round-(N-1) receipt is missing (fail-closed; a missing receipt with citations reds — measured `truth=missing,cited=6/9,anch=3/7`) |

`T(N)` is **derived from committed bytes**, not hardcoded: the round-(N-1) receipt's summary
`closed=<n>/<m>` line and, when present, its `selftest cases=<k> failures=<f>` line. The r40 receipt carries
no selftest summary line (the lane's own round-41 correction says so), so rounds citing round-40 tallies get
`closed=10/10` only — no invented `cases`/`failures` expectation.

### Replay limb (the C1 kill-rule requirement)

`j2_replay_fixtures WORK TREE` builds fixtures **from the tree under test**, applies mutations, and requires
`check_j2` to reject each mutant and accept the unmutated tree. The committed defeat is applied **verbatim**:
the replacement text is read out of the tree's committed `corpus/instruments/r41-closure.sh` (the line that
carries `closed=10/100`), so the replay is the committed artifact, not a paraphrase.

## Evidence (commands and their real output)

Full teed transcript: `ExecJ2Token.transcript.txt`. Key lines:

**1. Green over the lane HEAD export** (`514ff62d…`, 8228 files) and over the spawn HEAD `0566bd6`
(8225 files) — the limb is green before and after the L1's later landings:

```
J2 payload=records=3,graded=3,fenced=0,resid=0,near=0,cited=9/9,anch=7/7,truth=ok,probe=22/22,accept=10/10,reject=12/12 closed=1
```

**2. Extractor battery + replay** (`--selftest` over `--export-ref HEAD`):

```
probe=22/22,accept=10/10,reject=12/12
replay fixture=unmutated-tree accepted=1 limb=positive payload=…cited=9/9,anch=7/7,truth=ok…
replay fixture=committed-mangled-value-token rejected=1 limb=near payload=…near=1…
replay fixture=boundary-closed-13-130      rejected=1 limb=near  payload=…near=1,anch=6/7…
replay fixture=boundary-closed-1-13        rejected=1 limb=near  payload=…near=1,anch=6/7…
replay fixture=boundary-leading-space-value rejected=1 limb=resid payload=…resid=1…
replay fixture=boundary-leading-space-key   rejected=1 limb=resid payload=…resid=1…
replay fixture=boundary-xclosed             rejected=1 limb=resid payload=…resid=1…
replay fixture=boundary-trailing-word       rejected=1 limb=resid payload=…resid=1…
replay fixture=boundary-ratio-tail          rejected=1 limb=resid payload=…resid=1…
replay fixture=boundary-failures-10         rejected=1 limb=near  payload=…near=1…
replay fixtures=10 failures=0
```

Note the shape of the repair: the committed defeat is caught by `near=1` **while `cited=9/9` and `anch=7/7`
still pass** — exactly the masking that made r41's I3 green. The boundary mutants that relocate the truth
also drop `anch` to 6/7.

**3. The committed defeat, live, side by side** (§5 of the transcript):

```
$ bash corpus/instruments/r41-closure.sh --selftest --export-ref 1f74646… --lane <lane>
selftest detail=I3 positive=pass payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
selftest detail=I3 mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
selftest case=I3 mutants=0/1 positive=fail payload-match=0 verdict=fail

$ bash ExecJ2Token.sh --export-ref 1f74646… --selftest   (same ref, same committed mutation)
J2 payload=records=3,graded=3,…,near=0,…,truth=ok,probe=22/22,accept=10/10,reject=12/12 closed=1
replay fixture=committed-mangled-value-token rejected=1 limb=near payload=…near=1…
replay fixtures=10 failures=0
```

**4. Negative-control refs** — the limb is **green at base `5053a7f…` and at the round-41 judged head
`1f74646…`** (same payload as §1). This is deliberate and documented below: J2 grades the *frozen* closure
corpus, so it does not manufacture the suite's base/r41-head reds; those are carried by the checks that grade
round-42 artifacts (J1 per-correction evidence, J8 receipt, J11 dedup marker). **The L1 must not rely on J2
for the base/r41-head negative controls.**

**5. Y simulation** — appending a round-42 correction to each record in the round-41 shape (citing the r41
receipt truth) keeps the limb green and raises the counts as expected:

```
J2 payload=records=3,graded=4,fenced=0,resid=0,near=0,cited=12/12,anch=10/10,truth=ok,probe=22/22,… closed=1
```

and a round-42 correction that additionally **quotes** the repaired defect (`closed=10/100`) and the round-42
target (`closed=13/13`) also stays green (`graded=4,cited=12/12,anch=9/9,near=0`) — quoting the defect is not
a defect.

**6. Fail-closed behaviour measured** (fixtures, scratch only): removing the round-40 receipt while round-41
citations exist →
`records=3,graded=3,…,cited=6/9,anch=3/7,truth=missing` → RED. A fenced pseudo-correction → `fenced=1,near=0`,
CLOSED.

## Integration contract for the L1 (how to land it)

`ExecJ2Token.sh` is **sourceable**: it defines `J2_AWK`, `J2_RECORDS`, `j2_scan_text`, `j2_has_token`,
`j2_probe_battery`, `j2_receipt_files`, `j2_grade`, `check_j2`, `j2_fixture`, `j2_replace_first_corr`,
`j2_subst_line`, `j2_committed_defeat_text`, `j2_replay_fixtures`. It sets **no** shell options and runs
nothing at source time, so it can be sourced into `corpus/instruments/r42-closure.sh` beside the suite's own
helpers. Dispatch exactly like the r41 checks:

```bash
payload=$(check_j2 "$EXPORT" "$REF"); rc=$?
printf 'J2 payload=%s closed=%s\n' "$payload" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)"
```

and call `j2_replay_fixtures "$WORK" "$EXPORT"` from the J2 selftest case (it prints
`replay fixture=… rejected=…` / `replay fixtures=N failures=K`, returns non-zero on any failure).

**The one coordination dependency.** For a round N whose corrections cite tallies, J2 requires each such
record to cite the round-(N-1) receipt truth as a whole token. For round 42 that truth is
`closed=10/12` (derived from `.ufo/waves/round-41/final-gates/all-gates.txt`, which is committed). If the
round-42 corrections cite a **different** closed tally (e.g. only `closed=13/13`), `cited` drops below `M` and
J2 reds; if they cite **no** tally at all, the round is not graded for presence (no false red). The payload
makes this visible (`cited=K/M`). This is the same presence requirement I3 carried, with the token-exact
repair; it is not a new demand.

## Risks / known limits (stated, not hidden)

- **The deletion-variant relation** is calibrated against the truth sets of the committed receipts. It is
  sound on the committed corpus (0 false positives at base, spawn HEAD, current HEAD, and all Y
  simulations), and it deliberately reds a *variant of the new round's truth* (e.g. a round-42 correction
  citing `closed=10/120`). It does **not** red round-42 prose quoting older defect shapes
  (`closed=10/100`, `closed=13/130`) — verified.
- **Rounds ≤ 38** are graded only if their correction lines carry citations (they carry none in the committed
  corpus), and their receipts exist (r36…r41 are all committed at HEAD), so `truth=missing` cannot silently
  appear.
- **Not in J2's scope**: per-correction evidence naming (J1), the round-42 receipt (J8), correction
  duplication (J11), scratch/quiescence (J5/J13), density/deletions (J12). J2 grade is *tally tokens only*.
- No blockers. Both deliverables are in place; nothing outside my write scope was touched, and no lane file
  was edited (the L1 lands the suite).

## Tooling, hosts, scratch

- **No tool was installed or upgraded** (no `pacman`, no `uv`, no `npx`, no binary downloads).
- All work ran under the seat scratch `S=/fast/scratch/hyaku/kasegi-r42/ExecJ2Token/`; every export/work dir
  lived under `S`; nothing was written under the lane except the two deliverables and this receipt; no
  fleet-root file was touched; no git/jj mutation was run anywhere (only `git archive` / `git show` /
  `git rev-parse`, all read-only).
- Scratch was removed before this receipt was filed (`remove: yes`); the transcript and deliverables were
  copied into `.ufo/waves/round-42/wave1/` first and verified byte-identical (`cmp -s`).
- Messages: one inbound IRC notice from `TsukuroiR48` about a round-48 artifact in another lane was
  acknowledged and acted on only by *not* touching it (out of my lane and write scope).
