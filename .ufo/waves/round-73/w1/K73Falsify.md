# K73Falsify — falsification of round-73 claims C1 and C2 (attempt 1, wave w1)

Seat: K73Falsify (leaf, read-only for the lane). Items attacked: claims.json C1 (Q10 recheck cwd repair, `recheck-cwd-census.py`) and C2 (F51 OSV.dev POST /v1/query on S108, incl. its counter list) and the round's control logic. Scratch: `/fast/scratch/hyaku/kasegi-r73/K73Falsify/` (base export, scratch clone `lane/` at HEAD 3b53ff8, candidate copies `cand/`, `fgn/`). Lane writes: none. Installs: none (stdlib python3, bash, git only; pacman untouched). Lane state at end: HEAD 3b53ff8, no tracked change; untracked entries were siblings' (see F26).

Evidence copies (named, under this report dir): `K73Falsify-ev-*.txt` (8 files, listed at the end).

## Summary verdicts

| # | Item | Verdict |
|---|------|---------|
| 1 | C1 after_predicate is one checkable sentence, re-derived | holds |
| 2 | C1 base before-values re-derived equal to receipt | holds |
| 3 | C1 66/22/10 arithmetic and candidate simulation | holds on the tracked tree; host-dependent (weakened) |
| 4 | 22 fail-closed exit-1 lines are by design | holds |
| 5 | C1 "re-derive from committed bytes" | weakened (counter executes the live working tree) |
| 6 | C1 "every corpus/knowledge recheck line" | weakened (2 `restoration-recheck:` lines uncounted) |
| 7 | C1 non-claim "every recheck replays the pinned capture" | falsified (27 of 88 first lines do not) |
| 8 | C1 tree_scope "C2 entry does not move this predicate" | falsified on a merged tree (prints entries=89 exit0=67) |
| 9 | C1 "from any cwd" | weakened (one foreign tempdir) |
| 10 | C1 selftest kill clause | weakened (fixture does not exercise exit 1) |
| 11 | "the 9 cited sources" premise | falsified: 10 sources |
| 12 | C2 S108 capture sha256 and line count | holds (sha/lines); committed bytes: weakened (untracked) |
| 13 | C2 contract list is located in S108 | holds (coverage); unenumerated by any counter; quote-form hazard |
| 14 | C2 before-values (frontier, entries, knowledge-expected, files, sort) | holds |
| 15 | C2 capture-binding exit | weakened (exit 1 on current tree; receipt has no exit code; claim has no manifest step) |
| 16 | C2 `scripts/sources-census.sh` command | weakened (cwd unstated; fails from lane root) |
| 17 | C2 kill "exits nonzero from a foreign cwd" | weakened (no C2 counter runs from a foreign cwd) |
| 18 | C2 kill "any quote in the entry is located" | weakened (only manifest-pinned quotes are checked) |
| 19 | C2 kill "knowledge-expected drifts from the file set" | weakened (counter compares counts, not sets) |
| 20 | C2 non-claim "no live osv.dev query by any lane check" | holds for the 88 recheck lines (grep); unenumerated for instrument internals |
| 21 | C2 F51 row | weakened (row not named in targets; must be appended to PROVINCE.md) |
| 22 | PROVINCE F31 wording: "named as out of scope" vs "gap" | "named as out of scope" holds; "gap" weakened |
| 23 | C1 population = glob of corpus/knowledge/*.md | holds |
| 24 | C1 counter reads first `recheck:` line only | holds today (each file has exactly one), latent gap |

## Findings

### F1 — C1 after_predicate is one sentence, re-derivable (holds)
Quote (claims.json, C1.after_predicate): "on the C1 candidate tree with C2 not landed, the census prints exactly `RECHECK-CWD entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0` and `RECHECK-CWD-RESULT conformant` with exit 0, and `--selftest` prints `selftest cases=1 failures=0` with exit 0"
It is one sentence with three conjuncts; each conjunct is a printed string the counter emits (lines 91–95, 157 of recheck-cwd-census.py). Re-derived in F3; the printed string matched exactly (grep of the summary line, exit 0; `tail -2` of `c1-candidate-sim.txt`).

### F2 — C1 before-values re-derived equal to the receipt (holds)
Commands (exit codes shown):
- `git -C <lane> cat-file -e fdf17413` → exit 0.
- `mkdir -p .../base && git -C <lane> archive fdf17413 corpus/knowledge | tar -x -C .../base` → exit 0; `ls base/corpus/knowledge/*.md | wc -l` → 88.
- `TMPDIR=.../tmp python3 <lane>/corpus/instruments/recheck-cwd-census.py --root <base> --lane <lane> --verbose > c1-base-verbose.txt` → exit 1 (nonconformant, expected at base).
- `cmp c1-base-verbose.txt .ufo/waves/round-73/controls/c1-donothing-r73.txt` → exit 0 (byte-identical; `wc -l` of the output file = 90).
- Same counter with `--root <lane>` at HEAD 3b53ff8 (verbose) → `diff` vs receipt exit 0.
- Summary line re-derived: `RECHECK-CWD entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT nonconformant`, exit 1.
- Knowledge dir delta fdf17413→3b53ff8: `git -C <lane> diff --stat fdf17413 3b53ff8 -- corpus/knowledge` → no output, exit 0. So base and HEAD knowledge are identical.
The receipt equals the re-derivation.

Breakdown of the 11 prefix-less lines (`noprefix=1`): bugzilla-rest-api-bug-endpoints (exit 2), cisa-vulnrichment-adp-enrichment (2), cisa-vulnrichment-record-list (2), github-repository-security-advisories-rest-api (2), nvd-api-2.0-response-schema (2), nvd-api-2.0-retrieval-interface (2), openssf-scorecard-checks (2), osv-affected-range-events (2), project-zero-big-sleep-sqlite-variant-analysis (2), project-zero-fuzzilli-vs-bigsleep-comparison (2), root-loss-2026-10-12 (**0**). So 10 exit-2 + 1 exit-0. Their relative paths resolve only from the lane root.

### F3 — the 66 arithmetic and the candidate simulation (holds on the tracked tree)
66 = 56 (current exit 0, which already includes root-loss) + 10 (exit-2 lines that the repair turns to 0). The census's 56 already includes root-loss, so "root-loss keeps exit 0" is part of the 56, not an extra.

Simulation 1 (scratch `cand/`, copy of base knowledge with 11 prefixes `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `; `mkcand.py` log `prefixed 11`; census with `--root cand --lane <canonical>`):
`RECHECK-CWD entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`, exit 0. Non-zero-exit lines: the 22 exit-1 entries only.

Simulation 2 (scratch clone `lane/` = `git clone --shared` of the lane, HEAD 3b53ff8, no untracked files; knowledge prefixed to the clone path; `--root` and `--lane` both the clone): same printed line, exit 0. `git -C <clone> rev-parse --show-toplevel` = clone dir (asserted).

Selftest: `recheck-cwd-census.py --selftest` → `selftest case=prefix-census ok got=… want=…`, `selftest cases=1 failures=0`, exit 0.

So "66 is a fact" of HEAD+repair on this host. It is an artefact in three ways:
(a) capture dependence: deleting the scratch clone's `corpus/source-snapshots/round-50/S080.txt` (a tracked capture) and rerunning gives `ENTRY osv-affected-range-events.md noprefix=0 foreign_exit=2` and `RECHECK-CWD entries=88 noprefix=0 exit2_foreign=1 exit0_foreign=65 exit1_foreign=22 …`, `RECHECK-CWD-RESULT nonconformant`, exit 1 (evidence: `K73Falsify-ev-c1-s080-deleted.txt`). One deleted capture flips C1 — so the predicate is a property of the checkout, not of a commit alone.
(b) host guard: root-loss's line is `test ! -e ~/Projects/bounties && test ! -e ~/Projects/the-bounty-hunter && test ! -e ~/Projects/origin-work && test -e ~/Projects/ufo-fsd-alpha` (no prefix in the file). Its exit 0 requires three paths absent and one present on this host (`ls -d` of bounties/the-bounty-hunter/origin-work: "No such file" each; ufo-fsd-alpha present).
(c) the 21 guarded fail-closed lines (F4) become a function of ~/Projects/bounties presence. I did not restore a base to test the flip (not run; [INFERENCE] that a restored base changes their exit).

### F4 — the 22 exit-1 lines are fail-closed by design (holds)
I ran each of the 22 lines from a foreign tempdir with `bash -c`, exit codes recorded: all 22 exit 1 (`citation-bases`, `claim-anatomy-sample`, `ev-model`, `evidence-dir`, `intake-and-finalize`, `intake-surface`, `mission-control`, `mission-ledger`, `operator-queue`, `ops-invariants`, `policy-access-playbook`, `program-quirks`, `repo-git-state`, `retirement-autopsies`, `source-tree-loss-2026-09-28`, `submitted-registry`, `target-checkouts`, `terminal-classes`, `triage-thresholds`, `ufo-archive-2026`, `ufo-workspaces`, `vdp-disclosure-packages`).
Quote, claim-anatomy-sample.md line 6: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-anatomy-sample.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15`. Run: exit 1, no output — `test -d` on the absent base. This is the designed fail-closed (Q1). `citation-bases` has no `test` guard: `anchorcheck.py corpus/knowledge/citation-bases.md` exit 1, output `== … 10 in-range cite instances, 0 bad; … LOST-RECORDED=1 … BASE-ABSENT=1` with `BASE-ABSENT md:31 ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58 (base tree absent …)`. Also fail-closed on a lost base, by anchorcheck's own rule. Holds.

### F5 — C1 "re-derive from committed bytes" is not what the counter does (weakened)
`recheck-cwd-census.py` reads the knowledge files under `--root` (line 62, 69–72) but runs each value with `bash -c value` (line 51) where every prefixed value begins with `cd <DEFAULT_LANE> && ` (lines 32, 66, 77). Thus the exit codes of the 56+10 prefixed lines come from the working tree at `--lane` (live checkout, including untracked files), not from the `--root` bytes. My base-export census (F2) reproduced the receipt only because the live lane's captures and instruments equal base's for these lines. The live lane currently has an untracked `corpus/source-snapshots/round-73/` (S108, no manifest) and an untracked `upstream-post-v1-query.md` (see F26); neither feeds C1 lines today, but the counter cannot distinguish them. The claim "from committed bytes" should read "from the lane working tree at --lane".

### F6 — C1 "every corpus/knowledge recheck line" (weakened)
Census reads only the first line starting `recheck:` per file (lines 36–41, 72). `grep -c '^recheck:'` over all 88 files: every file has exactly one (no file with count ≠ 1). But two entries carry a second recheck-type line that the counter cannot see:
- corpus/knowledge/claim-gates.md:126 `restoration-recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md …`
- corpus/knowledge/claim-package-contract.md:69 (same shape, claim-package-contract.md).
Run from a foreign cwd: both exit 1 (`fgn` run, exit=1 each). Prefix present, so `noprefix` is unaffected, but their exit codes are not in any census count, and "every recheck line" is not what the counter enumerates. Verdict: weakened.

### F7 — C1 non-claim "every recheck replays the pinned capture" (falsified)
Quote (claims.json non_claims): "no live osv.dev query is made by any lane check; every recheck replays the pinned capture". Counter-examples, enumerated by grep of the first `recheck:` line: 27 of 88 do not call `source-recheck.py`: citation-bases, claim-anatomy-sample, claim-gates (`r46-c1-gate.py`), claim-package-contract (`r46-c1-gate.py`), claim-package-gate (`claim-package-check.py --selftest`), considerthese-proposals-ledger (`density.py`), ev-model, evidence-dir, intake-and-finalize, intake-surface, mission-control, mission-ledger, operator-queue, ops-invariants, policy-access-playbook, program-quirks, repo-git-state, retirement-autopsies, root-loss-2026-10-12 (host `test`), source-tree-loss-2026-09-28, submitted-registry, target-checkouts, terminal-classes, triage-thresholds, ufo-archive-2026, ufo-workspaces, vdp-disclosure-packages. The 61 that do call it: `source-recheck.py --manifest … --source …`. Verdict: falsified as a universal. The "no live osv.dev query" half holds for the recheck lines (`grep -h -m1 '^recheck:' | grep -i -c 'curl\|wget\|http://\|https://'` → 0, exit 1 from grep with no match — counted as 0 matches).

### F8 — C1 tree_scope contradicts its own printed predicate (falsified on a merged tree)
Quote (claims.json, C1.tree_scope): "C1 population is the 88 knowledge entries present at base; the C2 entry is measured by C2 and does not move this predicate". The census enumerates `corpus/knowledge/*.md` (line 69), so any new entry changes `entries=`. Simulation: copy `osv-affected-range-events.md` to `zz-sim-89th.md` in the scratch clone's knowledge (C2-like addition) and rerun: `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`, exit 0 (`K73Falsify-ev-c1-sim-89th-entry.txt`). So the exact string in after_predicate is unreachable on a tree where C2's entry lands, and the tree_scope sentence says C2 "does not move" the predicate. The after_predicate's qualifier "with C2 not landed" saves it only if C1 is judged before C2 lands. Verdict: weakened (contradiction); falsified for a merged tree. Fix wording, not the numbers.

### F9 — "from any cwd" (weakened)
C1.type: "repair (QUALITY Q10: recheck line executable from any cwd …)". The counter runs one fresh `tempfile.mkdtemp` foreign cwd per line (lines 44–58). "Any cwd" is not enumerated: one foreign cwd is tested. Verdict: weakened.

### F10 — selftest does not exercise the exit-1 kill clause (weakened)
C1.kill_rule includes "if exit1_foreign differs from 22". The selftest fixture (lines 108–112) has three entries and expects `exit1_foreign=0` (line 125). So the selftest cannot detect an exit-1 classification regression; only the live census count does. Selftest itself is green (`selftest cases=1 failures=0`, exit 0). Verdict: weakened.

### F11 — "the 9 cited sources" premise (falsified)
The seat brief says "the 9 cited sources are live pinned captures". The 10 prefix-less exit-2 lines cite 10 distinct sources: S080 (round-50), S081 (round-51), S083 (round-52), S085 (round-53), S086 (round-54), S087 (round-55), S088 (round-56), S093 (round-60), S094 (round-61), S107 (round-72). Each manifest and capture pair is tracked at 3b53ff8 (`git ls-tree -r --name-only 3b53ff8 -- corpus/source-snapshots/roundNN` → manifest.json and SNNN.txt; 2 rows per round). Claims.json does not state 9. The number is wrong; the captures are live and tracked.

### F12 — C2 source S108 (holds for sha/lines; committed bytes weakened)
`sha256sum corpus/source-snapshots/round-73/S108.txt` → `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9` (matches claims); `wc -l` → 150 (matches). But `git status` shows `?? corpus/source-snapshots/round-73/` — the capture is untracked, and round-73 has no `manifest.json`. The C2 sourced_claim says "opened and captured this round"; the capture header/fetch metadata was not checked in this seat ([INFERENCE]-free: not inspected). Verdict: sha/lines hold; "committed" is not true yet.

### F13 — C2 contract list (holds; unenumerated; quote-form hazard)
C2.target lists: "the request payload, the version rule, the Git-tag query, pagination and the 32 MiB HTTP/1.1 limit". grep of S108 located all five:
- request payload: lines 34 (`commit string …`), 35 (`version string …`), 37 (`page_token string …`).
- version rule: line 40 `Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both.`; line 41 `Requests that specify the version in both places return 400 Bad Request.`
- Git-tag query: line 56 `You can also query for git tags via this API. To do so, set the ecosystem to GIT …`; line 79 example.
- pagination: lines 134–146 (section "Pagination"); line 136 `… more than 1,000 vulnerabilities …`.
- 32 MiB HTTP/1.1: line 148 `The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2.`
Hazard: the capture spells it `32MiB`; the claim writes `32 MiB`. An entry quoting "32 MiB" fails any exact-quote check. Also line 8 `POST /v1experimental/ determineversion` is a different endpoint and must not be folded into the v1/query entry. No counter enumerates the five-item list; coverage is by reading, not by a counter. Verdict: holds (located), unenumerated (by counters).

### F14 — C2 before-values (holds)
Run from the lane root, TMPDIR scratch, read-only:
- `python3 corpus/instruments/frontier-recheck-count.py` → exit 0; `FRONTIER-CENSUS rows=50 admitted=50 closed=50 problem-rows=0 registry=107`; `entries=53 pass=53 exit=0`. Matches before_values. (Output: `K73Falsify-ev-c2-frontier-count-head.txt`.)
- `wc -l corpus/instruments/knowledge-expected.txt` → 90; `grep -vc '^#'` → 88; `ls corpus/knowledge/*.md | wc -l` → 88; `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` → exit 0. Set equality: `diff <(grep -v '^#' knowledge-expected.txt | awk 'NF' | sort) <(ls corpus/knowledge/*.md | sort)` → exit 0.
Matches "knowledge_expected: 90 lines / 88 rows", "knowledge_files: 88".
Note the frontier counter reads its rows from PROVINCE.md amendments (`grep -c '^\[r[0-9]* Frontier amendment' PROVINCE.md` → 30).

### F15 — C2 capture-binding (weakened)
`python3 corpus/instruments/capture-binding-check.py` on the current lane tree → final line `records=86 bound=86 unbound=0`, but the output contains `FAIL rule=missing-manifest dir=round-73` and the process exits **1** (`K73Falsify-ev-c2-capture-binding-lane-tree.txt`). Cause: the untracked S108 directory has no manifest. The same counter in the scratch clone at HEAD 3b53ff8 → `records=86 bound=86 unbound=0`, exit 0 (`K73Falsify-ev-c2-capture-binding-clone-head.txt`; that clone was restored from git objects before this run, see below). Consequences: (a) the C2 do-nothing receipt `controls/c2-donothing-r73.txt` records the summary line with no exit code, so its "exit 0" half is unrecorded; (b) C2.after_predicate requires `capture records=87 bound=87 unbound=0 with exit 0`, which needs a committed round-73 manifest.json; the kill rule names only "an unbound record", not "missing-manifest", so a manifest-less candidate fails the predicate without tripping any kill rule. Verdict: weakened.
Scratch note: I deleted the clone's S080.txt for F5(a) and the capture-binding run on the clone showed `FAIL rule=capture-missing record=S080`, exit 1 (`records=86 bound=85 unbound=1`), before I restored it from `git show 3b53ff8:corpus/source-snapshots/round-50/S080.txt` into the scratch clone. The restored clone then gave exit 0.

### F16 — C2 `sources-census` command (weakened)
C2.counter.command includes `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`, a path relative to cwd. `ls scripts/sources-census.sh` in the lane → exit 2 (absent). Run from the lane root → exit 127 (`No such file or directory`); from a foreign cwd → exit 127. The script exists only at the fleet root `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`ls` exit 0). Run from the fleet root → exit 0, with a line `kasegi W04 S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes` and `kasegi ok …/corpus/SOURCES.md` (`K73Falsify-ev-c2-sources-census-fleet-root.txt`). The script does not write (`grep` of its writes → only `--out` / stdout). Verdict: weakened: cwd unstated; the command as written does not run from the lane.

### F17 — C2 kill rule "exits nonzero from a foreign cwd" has no C2 counter (weakened)
C2.kill_rule: "… if the new entry's recheck exits nonzero from a foreign cwd …". The C2 counter list is frontier-recheck-count.py, capture-binding-check.py, wc/grep/ls, sources-census. frontier-recheck-count.py runs each recheck "from the lane root" (its header, item D), not from a foreign cwd. The only foreign-cwd enumerator is recheck-cwd-census.py, which is not in C2's counter list. Verdict: weakened.

### F18 — C2 "any quote in the entry is located in the S108 capture" (weakened)
source-recheck.py checks quotes listed in the manifest (`quotes: [{id, anchor, quote}]`, verified by reading round-50/manifest.json). A quote in the entry that is not pinned in the round-73 manifest is not checked by any counter; the entry does not exist yet and no round-73 manifest exists, so "every quote … located" is unenumerated. Verdict: weakened. Fix: the entry's quotes must all be pinned, or the kill rule must name the manifest as the enumerated set.

### F19 — C2 "knowledge-expected drifts from the file set" (weakened)
The counter command prints only counts (`wc -l`, `grep -vc`, `ls | wc -l`). Set equality holds at base (`diff` exit 0, F14), but no command in C2.counter compares sets, and "drifts" is not a count test. Verdict: weakened.

### F20 — C2 non-claim "no live osv.dev query is made by any lane check" (holds for recheck lines)
`grep -h -m1 '^recheck:' corpus/knowledge/*.md | grep -i -c 'curl\|wget\|http://\|https://'` → 0 matches (grep exit 1, no match). Instrument internals (`source-recheck.py`, `anchorcheck.py`, `frontier-recheck-count.py`) were not audited for network calls here. Verdict: holds for recheck lines; unenumerated for instrument bodies.

### F21 — C2 F51 row is not in the target list (weakened)
C2.target says "frontier F51 … admitted on S108 as one knowledge entry". The frontier counter takes its rows from `[rNN Frontier amendment …]` lines in PROVINCE.md (F50 at PROVINCE.md:217 is the precedent). `grep -n 'F5[01]\b' PROVINCE.md` → no match (exit 1). C2's kill rule and after_predicate require `FRONTIER-CENSUS rows=51` and `PASS F51`, which need a new PROVINCE amendment row; the target never says to append it. Verdict: weakened: the claim omits an edit its counters require.

### F22 — PROVINCE F31 wording: "named as out of scope" vs "gap" (split)
Quote, PROVINCE.md:178 (line verbatim, `grep -n 'osv.dev service API' PROVINCE.md`, exit 0): "… scope limit: the format's range/event semantics only — the osv.dev service API, the JSON Schema validation artifact, individual database exports and per-database database_specific values stay out".
- "named as out of scope": holds. The osv.dev service API is named inside a clause labelled "scope limit" and excluded ("stay out").
- "a gap F31 named" / "fills the surface": weakened. The row does not name a gap, a deferral or a later frontier; it is an exclusion from F31's admission. F51 therefore reverses a scope exclusion by opening a new frontier, not filling a gap F31 recorded. The non_claim "the F31 scope limit stays as written" is consistent with this reading.

### F23 — C1 population (holds)
Counter enumerates `glob.glob(os.path.join(root, "corpus", "knowledge", "*.md"))` (line 69), sorted; under `--root <HEAD or base export>` that is 88 files, equal to `knowledge-expected.txt`'s 88 rows (F14 set diff exit 0). "present at base": `git diff --stat fdf17413 3b53ff8 -- corpus/knowledge` empty (F2). Verdict: holds.

### F24 — first-line-only reading (holds today; latent gap)
`first_recheck` returns on the first `recheck:` line (lines 36–41). Each of the 88 files has exactly one such line (F6), so no count is hidden today. Latent: any entry with a second `recheck:` line would be silently partial. Not a current falsifier.

### F25 — Scratch hygiene and host guard
- Lane write: none. Scratch writes: `/fast/scratch/hyaku/kasegi-r73/K73Falsify/{base,cand,lane,fgn,tmp,knowledge-head-backup}`.
- Every git call was read-only (`cat-file`, `archive`, `show`, `ls-tree`, `ls-files`, `diff --stat`, `status`, `log`, `rev-parse`, `clone --shared` into scratch). No checkout/reset/commit. The scratch clone's knowledge was restored by `cp`, not `git checkout`.
- The lane's `git status --short` before and after my runs: same tracked state (no M entries); untracked entries are siblings' (see F26).
- Running the 88 recheck lines executes read-only instruments; `anchorcheck.py` creates its own temp fixtures (`os.makedirs` at lines 312–319 are inside its fixture path; verified by `git status` unchanged after the runs).

### F26 — sibling-owned untracked entries observed (not mine)
At 04:50 `git status --short` showed `?? upstream-post-v1-query.md` at the lane root, which I did not create; the count grew from 7 to 8 during my run. Reported for the integrator; not touched.

## Universal words in claims.json (quoted, each with a verdict)
- C1.type "from any cwd" → one foreign tempdir → **unenumerated** (F9).
- C1.target "every corpus/knowledge recheck line" → enumerates first line only; 2 `restoration-recheck:` lines unseen → **weakened** (F6).
- C1.target "the 11 prefix-less recheck lines" → noprefix=11 → **enumerated**.
- C1.target "the 10 that exit 2 from a foreign cwd exit 0" → exit2_foreign=10, candidate sim 0 → **enumerated** (F3).
- C1.target "the 22 fail-closed lost-base lines keep exit 1" → exit1_foreign=22 → **enumerated**; "lost-base" depends on host (F3b, F4).
- C1.after "exactly" → printed-string equality → **enumerated** (F1, F3).
- C1.after "with C2 not landed" → conditional; the tree_scope clause conflicts (F8) → **weakened**.
- C1.kill "any knowledge entry has noprefix=1 or exit2_foreign=1" → per-entry first line → **enumerated**.
- C1.kill "if the selftest is not green" → selftest run → **enumerated** (F10 limits its reach).
- C1.tree_scope "the 88 knowledge entries present at base" → glob → **enumerated** (F23); "does not move this predicate" → **falsified** (F8).
- C1.non_claims "every recheck replays the pinned capture" → **falsified** (F7).
- C2.target "the request payload, the version rule, the Git-tag query, pagination and the 32 MiB HTTP/1.1 limit" → listed items → **unenumerated** by any counter; located in S108 (F13).
- C2.after "PASS F51 ... ids=S108" → PASS-line mechanism → **enumerated** (needs F51 row, F21).
- C2.after "knowledge-expected 91 lines / 89 rows with `LC_ALL=C sort -c` clean" → sort checked by me, not in the counter list → **weakened** (F19).
- C2.after "89 knowledge files" / "sources-census exit 0" → counted / exit-checked → **enumerated** (F16 cwd).
- C2.kill "if the F51 row or its entry is absent or duplicated" → rows/entries counts would move on duplication → **enumerated by count**, duplication not named (F21).
- C2.kill "any quote in the entry is not located in the S108 capture" → manifest-pinned quotes only → **weakened** (F18).
- C2.kill "if capture-binding reports an unbound record" → unbound count → **enumerated**; missing-manifest exit 1 not covered (F15).
- C2.kill "if the new entry's recheck exits nonzero from a foreign cwd" → no C2 counter → **weakened** (F17).
- C2.kill "if knowledge-expected drifts from the file set" → counts only → **weakened** (F19).
- C2.kill "if sources-census exits nonzero" → exit checked → **enumerated**, cwd unstated (F16).
- C2.sourced_claim "every quote in the entry is located in the capture" (C2.source.note) → same as F18 → **weakened**.
- C2 non_claims "no live osv.dev query is made by any lane check" → recheck lines 0 (F20) → **holds for recheck lines**; instrument internals unaudited.
- C2 non_claims "every recheck replays the pinned capture" → **falsified** (F7).

## Re-derived counter outputs (for the integrator)
- C1 base (fdf17413 export, --root base, --lane canonical, verbose) = receipt, byte-identical: `RECHECK-CWD entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 exit_other=0 norecheck=0` / `RECHECK-CWD-RESULT nonconformant`, exit 1.
- C1 candidate sim (11 prefixes, canonical lane): `RECHECK-CWD entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0` / `RECHECK-CWD-RESULT conformant`, exit 0; clean-clone sim identical.
- C1 selftest: `selftest cases=1 failures=0`, exit 0.
- C1 with an extra entry (sim): `entries=89 … exit0_foreign=67 …`, conformant, exit 0.
- C1 with S080 deleted (clone sim): `entries=88 noprefix=0 exit2_foreign=1 exit0_foreign=65 exit1_foreign=22 …`, nonconformant, exit 1.
- C2 frontier (lane tree, HEAD): `FRONTIER-CENSUS rows=50 admitted=50 closed=50 problem-rows=0 registry=107`, `entries=53 pass=53 exit=0`.
- C2 capture-binding: lane tree `records=86 bound=86 unbound=0` + `FAIL rule=missing-manifest dir=round-73`, exit 1; clone HEAD `records=86 bound=86 unbound=0`, exit 0.
- C2 knowledge-expected: 90 lines, 88 rows, 88 files; sort -c exit 0; set diff exit 0.
- C2 sources-census (fleet root): exit 0.

## Recommended corrections (no edits made; lane untouched)
1. C1.tree_scope: replace "the C2 entry … does not move this predicate" with "the predicate is judged before C2 lands; after C2 the printed entries count is 89 and exit0 is 67".
2. C1: replace "every corpus/knowledge recheck line" with "the first `recheck:` line of every corpus/knowledge entry", or have the counter also enumerate `restoration-recheck:` lines (2 uncounted, both exit 1).
3. C1 non_claims: drop "every recheck replays the pinned capture" (27 of 88 do not).
4. C1: state that exit codes are from the working tree at --lane, and that the 22 + root-loss are host-state dependent.
5. C1.type: "from any cwd" → "from a fresh foreign cwd".
6. C1 selftest: add an exit-1 fixture so the "exit1 = 22" clause is guarded.
7. C2: add to the target the PROVINCE amendment row for F51 and the round-73 manifest.json pinning S108 quotes (verbatim, "32MiB").
8. C2 counter: use an absolute path for sources-census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), add the recheck-cwd-census run for the new entry, add a set comparison for knowledge-expected.
9. C2 kill rule: name the missing-manifest case and make "any quote located" say "every quote pinned in the round manifest".
10. "9 cited sources" in the brief → 10.

## Evidence files (under this report dir)
K73Falsify-ev-c1-base-rederived-verbose.txt; K73Falsify-ev-c1-candidate-sim.txt; K73Falsify-ev-c1-sim-89th-entry.txt; K73Falsify-ev-c1-s080-deleted.txt; K73Falsify-ev-c2-frontier-count-head.txt; K73Falsify-ev-c2-capture-binding-lane-tree.txt; K73Falsify-ev-c2-capture-binding-clone-head.txt; K73Falsify-ev-c2-sources-census-fleet-root.txt.

## Not run
- No live osv.dev or network fetch (none needed; none claimed).
- Restoring ~/Projects/bounties to observe the 21 guarded lines flipping: not run (host state not mine to change).
- S108 capture header/fetch metadata (2026-11-05T07:40:48Z, HTTP 200): not inspected.
- F20 instrument bodies: not audited for network calls.
