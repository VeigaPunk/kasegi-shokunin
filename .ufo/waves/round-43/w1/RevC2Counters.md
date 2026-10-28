# RevC2Counters — pre-freeze satisfiability of C2's counting commands

Seat: RevC2Counters (leaf, reviewer). Round 43, kasegi lane.
Frozen claims read first: `.ufo/waves/round-43/claims.json` (never edited).
Base under test: `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Measured: 2026-10-28T16:44Z–16:55Z.

## Method

1. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive ab98fac9… | tar -x -C $S/base`
   with `S=/fast/scratch/hyaku/kasegi-r43/RevC2Counters`. Every base reading below
   is from that export unless the row says "in lane root".
2. `git diff --name-only ab98fac9..4cb6d4a` prints nothing outside `.ufo/`, and
   `git status --porcelain` on the lane shows only untracked `.ufo/waves/round-43/*`
   files — so the lane's tracked corpus content IS the base content, and
   in-place runs are base-content measurements. No mutating git command was run.
3. Reachability probes were built in `$S/reach` (a copy of the base export) with
   synthetic S067/S068 rows, a synthetic `claim-package-gate.md`, and a synthetic
   `corpus/source-snapshots/round-43/manifest.json`. Nothing was written to the
   lane corpus.
4. No tool installed; no network fetch performed; `/bin/sh` is bash on this host.

## Counter table (claims.json C2.counting_commands, all 11 entries)

Base value = what the command literally prints at `ab98fac9`. "After" = the
claim's own after column. Reachable? is answered against the observed base and
the probe, not against plausibility.

| # | command as written | base value at ab98fac9 | claim before | claim after target | reachable? |
|---|---|---|---|---|---|
| 1 | `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` | `python3: can't open file '…/claim-package-check.py': [Errno 2] No such file or directory`, exit 2, no stdout | instrument absent | `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` | yes, only after the instrument+exemplar land. Not pre-satisfiable (deliverable path absent). |
| 2 | `python3 corpus/instruments/claim-package-check.py --selftest` | same absent-file error, exit 2 | instrument absent | `selftest cases=10 failures=0 exit=0` | yes, only after landing. Not pre-satisfiable. |
| 3 | `grep -c '^RULE ' <(python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar)` | `0`, exit 1 (stderr carries the absent-file error) | — | `8` | yes, only after landing. Not pre-satisfiable. Runs under both `bash` and `sh` here (`/bin/sh -> bash`); a dash `sh` would reject the process substitution. |
| 4 | `ls corpus/instruments/fixtures/claim-package/ \| grep -c '^defect-'` | `0`, exit 1 (`ls: cannot access '…/fixtures/claim-package/': No such file or directory`) | fixtures dir absent | `9` | yes, only after landing (see constraint F6: the degenerate control must not be named `defect-*`). |
| 5 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `66` (54 mined + 12 rejected) | 66 | `>=68` | **yes, demonstrated**: probe with S067 (`mined`) + S068 (`rejected`) appended in registry grammar prints `68`. Rejected rows match the regex (S022/S024/S026/S027/S028 are rejected). |
| 6 | `grep -rlE '^source: S067' corpus/knowledge \| wc -l` | `0` | 0 | `1` | **yes, demonstrated**: probe knowledge entry with frontmatter `source: S067 — …` (column 0, matching the existing convention, e.g. `cvss-v4-severity-and-vector.md:2`) prints `1`. |
| 7 | `ls corpus/knowledge/*.md \| wc -l` | `61` | 61 | `62` | **yes, demonstrated**: one added `claim-package-gate.md` prints `62`. |
| 8 | `python3 corpus/instruments/capture-binding-check.py` | `records=56 bound=56 unbound=0`, exit 0 | `records=56 bound=56 unbound=0` | `records=57 bound=57 unbound=0` | **yes, demonstrated**: probe `corpus/source-snapshots/round-43/manifest.json` with one S067 record (URL matching the S067 row, strict-UTC `fetched_utc`, pinned `sha256`) prints `AUDIT records=57 … multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt` and `records=57 bound=57 unbound=0`, exit 0. Round-43 ≥ MODERN_ROUND=32, so the archival exemption is closed: `fetched_utc` is mandatory. |
| 9 | `python3 corpus/instruments/recheck-audit.py --quiet` | from the lane root: `strict pass=61/61 cdroot_fail=0 …`, `lines=61 total=61 pass=61 … exit=0`, `expect=present expected=61 missing=0 unexpected=0 exit=0`, exit 0. From an export of the same bytes: `strict pass=1/61 cdroot_fail=60`, `expected=61 … exit=1`, exit 1. | `expected=61` | `expected=62` | **yes, demonstrated, but location-locked**: probe with the entry appended to `corpus/instruments/knowledge-expected.txt` prints `expected=62 missing=0 unexpected=0`; the same tree without that append prints `expected=61 … unexpected=1 exit=1`. The audit is green only where the entries' `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` equals the audited root (`--cdroot` exists, but the line is then executed from that root, so an export cannot be greened). |
| 10 | `python3 corpus/instruments/frontier-recheck-count.py` | `FRONTIER-CENSUS rows=25 admitted=25 closed=25 problem-rows=0 registry=66` … `entries=28 pass=28 exit=0`, exit 0 (identical in export and lane root) | `entries=28 pass=28 exit=0` | `entries=28 pass=28 exit=0` ("no frontier row changes") | **already satisfied at base — delta 0.** Do-nothing reachable target; it is a non-regression guard, not increment evidence. Only the informational `registry=66` token changes (to 68). Registry limb is one-directional (`bound - registry`), so the two new registry rows cannot make it red. |
| 11 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `<two W04 lines>`, `kasegi ok …/corpus/SOURCES.md`, `census-exit=0` | `exit 0` | `exit 0` | **already satisfied at base — delta 0.** Do-nothing reachable target: the arrow constrains only the exit status, and the command prints no increment token at all. It also cannot be aimed at a Y export — it resolves the lane directory from the fleet root, so it measures whatever is checked out. |

## Flags

**F1 — command count disagrees with the seat text.** `claims.json` C2
`counting_commands` has **11** entries (`.claims[1].counting_commands|length` = 11);
the seat brief says "ten counting commands". All 11 are tabled above. No counter is
missing from claims.json; the brief's number is the stale one.

**F2 — counters that already print the after-value at base (do-nothing reachable).**
- Fully: **#10** (`entries=28 pass=28 exit=0`) and **#11** (`exit 0`). A do-nothing
  solution satisfies both. This is consistent with the claim's own wording
  ("no frontier row changes"; census exit 0) but it means neither counter can
  evidence the C2 increment; the increment rests on #5–#9.
- Partially: **#8** already prints `exit=0`, `bound=records`, `unbound=0` at base —
  only the literal `records=57` discriminates. **#9** already prints `exit=0`,
  `pass=61/61` in place — only `expected=62` (and `lines=62`) discriminate.

**F3 — commands not runnable as written at base.**
- #1–#4: the instrument and fixture tree do not exist, so they print errors/0. That
  is the acquisition gap the claim names, not a syntax defect; recorded because a
  pre-freeze red-test of these four is impossible — there is no base-side substitute
  to prove the counters can ever go red before the instrument exists.
- #9: as written (no `--root`/`--cdroot`) it is root-identity-bound. Run from any
  export it prints `exit=1` (`cdroot_fail=60`). It is green only with cwd = lane root.
- #11: as written it cannot target an export at all (fleet-root + lane-name
  resolution). It validates the checked-out working tree.
- #3: bash-only syntax (process substitution). Fine here (`/bin/sh -> bash`), a
  hazard under dash.

**F4 — paths that do not exist at base.** `corpus/instruments/claim-package-check.py`,
`corpus/instruments/fixtures/` (the parent itself is absent), therefore
`corpus/instruments/fixtures/claim-package/` and its `exemplar/`, and
`corpus/knowledge/claim-package-gate.md`. Every non-deliverable path named by the 11
commands exists at base (`corpus/SOURCES.md`, `corpus/knowledge/`,
`capture-binding-check.py`, `recheck-audit.py`, `frontier-recheck-count.py`,
`knowledge-expected.txt`, the fleet census script). No unexpected missing
dependency was found.

**F5 — coupling constraints that the claim's after column implies but does not name.**
- #5 needs **two** rows, not one (66 + 2 ≥ 68): one `mined` plus one `rejected`.
- #8 needs a **new capture manifest** with a pinned `sha256` and a strict-UTC
  `fetched_utc`; a capture without a manifest fails `missing-manifest`, and an
  unpinned digest prints `unbound=1`, so the file alone does not move the counter.
- #9 needs **`corpus/instruments/knowledge-expected.txt` extended to 62 entries**;
  without it the audit prints `unexpected=1` and exits 1 (demonstrated). It also
  needs the new entry's `recheck:` line to pass all six strict limbs, which requires
  the manifest to carry at least one quote assertion — `source-recheck.py` refuses
  a quote-less manifest with `UNAVAILABLE reason=missing-quotes`, exit 2
  (demonstrated; adding `{"id":"q1","quote":"…","anchor":1}` yields
  `S067:sha256 OK` / `S067:q1 OK occurrences=1 anchor=1-ok`, exit 0).

**F6 — exact-count fragility.**
- #4 is exactly `9` while #2's selftest needs **10** cases: the degenerate
  always-pass control must not be a top-level entry whose name starts `defect-`,
  or the two after targets collide.
- #6 is exactly `1` and #7 is exactly `62`: any sibling seat that lands a second
  `corpus/knowledge/*.md`, or a second file declaring `source: S067`, breaks #7
  (and #9's `expected=62`). Exact-count counters are cross-seat hazards; they must
  be re-read at Y after every wave-1/2 write.

**F7 — control fidelity.** `.ufo/waves/round-43/c2-controls/before.txt` sections
A, B, C, D, F, G reproduce exactly at base (66 rows / 0 S067+; 61 knowledge / 0
citing S067; `records=56 bound=56 unbound=0` with `orphan=S040-live.txt`;
`entries=28 pass=28 exit=0`; census `exit 0` with the same two W04 lines). Section E
reproduces only **in place** (`… exit=0`); run against an export of the same bytes
it prints `exit=1` (`strict pass=1/61 cdroot_fail=60`). The control is accurate for
its stated conditions but is not export-reproducible.

## Residual risk and verification gaps

1. #1–#4's after values cannot be exercised before the instrument exists; they
   remain design-satisfiable only. No red path for `--selftest` was observable.
2. #9 is the only C2 counter that cannot be run against an export copy. C1's
   instrument runs in export mode; C2's #9 does not, so a verifier who pastes both
   claim counters into one export-based script gets a false red on C2.
3. #10 and #11 supply no increment signal; C2's coverage evidence must be carried by
   #5–#9 and the gate's own fixture outputs.
4. #6/#7/#4 are exact counts that any concurrent writer can break; they need a
   post-landing read at Y, not a pre-freeze assumption.
5. Not verified here (out of seat): whether the exemplar's eight rules can actually
   all pass on one captured public report, and whether the nine defect fixtures each
   fail exactly their own rule — both are only testable after the gate lands.
