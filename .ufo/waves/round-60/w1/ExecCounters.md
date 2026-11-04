ALL-MATCH — all 17 counting commands of the frozen round-60 claims (C1: 8, C2: 9) reproduce their wants in a fresh `--shared` clone at `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`; C2 #8 is compared at the erratum value 2; the runner's exit code is 0.

# Seat ExecCounters — round 60 w1

Scope: run every entry of `counting_commands` for C1 and C2 from `.ufo/waves/round-60/claims.json` with cwd = clone root, verbatim, and check each against its `# want:` comment. Read-only on the lane; the only lane writes are `W/ExecCounters.md` and `W/ExecCounters.json`. No tool was installed or upgraded.

Records (machine-readable, one object per command with `command`, `want_frozen`, `want_effective`, `exit_code`, `stdout_first_three_lines`, `stdout`, `stderr`, `assertions[{clause, ok, observed}]`, `verdict`): `.ufo/waves/round-60/w1/ExecCounters.json` (22282 bytes, sha256 `c4d32c58e3e7835f0c8e510a90e568478f302a7cfab3395c0d339c1f65ac32a8`).

## 1. Setup — fresh clone, exact commit, frozen claims

1.1 Clone and pin. `L=/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `S=/fast/scratch/hyaku/kasegi-r60/ExecCounters`.

```
$ D=$(mktemp -d -p "$S") && git clone -q --shared "$L" "$D/clone" \
    && git -C "$D/clone" checkout -q 7f7dd267283d2a16ca38d4cb05bed92165cb35cd
$ git -C "$D/clone" rev-parse HEAD
7f7dd267283d2a16ca38d4cb05bed92165cb35cd
$ git -C "$D/clone" rev-parse --show-toplevel
/fast/scratch/hyaku/kasegi-r60/ExecCounters/tmp.v0nxEx7BP8/clone
$ git -C "$D/clone" log -1 --format='%H %ci %s'
7f7dd267283d2a16ca38d4cb05bed92165cb35cd 2026-11-04 10:36:15 -0300 round-60: C1 escape-aware derive gate ...
```
exit 0. The clone root equals the created fixture dir (toplevel check above); no commit was made in it.

1.2 The claims the script reads are byte-identical to the lane's frozen record:

```
$ sha256sum "$L/.ufo/waves/round-60/claims.json" "$D/clone/.ufo/waves/round-60/claims.json"
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  .../kasegi-shokunin/.ufo/waves/round-60/claims.json
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  .../tmp.v0nxEx7BP8/clone/.ufo/waves/round-60/claims.json
```
exit 0. Recorded as `claims_sha256` in the JSON's header.

1.3 Runner. `$S/run.py` (10990 bytes, sha256 `61e14ae239ac254d185d7cd95cf7ed13b13ada145991d1ee2147c1816a22a787`). It reads claims.json, splits every entry at its `# want:` comment, runs the command verbatim through `bash -c` with cwd = clone root and `TMPDIR=$S`, and applies exactly one checker per (claim, n). Each checker encodes the want text as assertions — exact last-line equality, required `key=value` substrings, exact sha256 first field, exact integer stdout, or exit-code-only — so no checker consumes an observed value as its expectation. It exits 0 iff every gating assertion holds.

```
$ TMPDIR=$S python3 "$S/run.py" "$D/clone" "$D/clone/.ufo/waves/round-60/claims.json" \
    "$L/.ufo/waves/round-60/w1/ExecCounters.json"; echo "SCRIPT_EXIT=$?"
wrote /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/w1/ExecCounters.json records=17 all_match=True
SCRIPT_EXIT=0
```
17 = 8 (C1) + 9 (C2). Recorded `clone_head` = `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`, `all_match` = true.

## 2. C1 — 8 commands, each MATCH

Every command below ran with cwd = the clone root §1.1; "exit" is the recorded `exit_code`.

2.1 `bash .ufo/waves/round-60/controls/c1-probe-run-r60.sh corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r60/l1/c1-after` — exit 0.
Want: Q1..Q7 each exit=2 markers=0 reason=derive-not-read-only; CTRL-quoted-semicolon exit=0 derived=35; CTRL-plain-count exit=0 derived=1.

```
instrument=/fast/scratch/hyaku/kasegi-r60/ExecCounters/tmp.v0nxEx7BP8/clone/corpus/instruments/figure-audit.py sha256=35f7bcd3e673b81b
probe=Q1-escape-single derive=cat g.txt \'; touch MARK-Q1; \' exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q1-escape-single
probe=Q2-escape-double derive=cat g.txt \"; touch MARK-Q2; \" exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q2-escape-double
probe=Q3-sed-in-program derive=sed -n '1e touch MARK-Q3' g.txt exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q3-sed-in-program
probe=Q4-awk-system derive=awk 'BEGIN{system("touch MARK-Q4")}' exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q4-awk-system
probe=Q5-sort-output-flag derive=sort -o MARK-Q5 g.txt exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q5-sort-output-flag
probe=Q6-git-show-output derive=git show --output=MARK-Q6 HEAD exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q6-git-show-output
probe=Q7-git-show-ext-diff derive=git show --ext-diff HEAD exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q7-git-show-ext-diff
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
probe=RESIDUAL-python-traversal derive=python3 corpus/instruments/../../../above-evil.py exit=1 markers=0 :: FIG RESIDUAL-python-traversal recorded=35 derived=UNAVAILABLE reason=derive-exit-2 stale
```
All 10 need clauses hold (7 refusals + 2 admitted controls). The last line is informational and not part of the want: the named-open residual `RESIDUAL-python-traversal` is still admitted (exit 1 from python, not gate exit 2), matching the residual listed in the claim.

2.2 `python3 corpus/instruments/figure-audit.py --selftest | tail -1` — exit 0. Want: selftest cases=20 failures=0, exit 0.
```
selftest cases=20 failures=0
```

2.3 `python3 corpus/instruments/figure-audit-mutbat.py | tail -1` — exit 0. Want: mutbat killed=2/2 survivors=0 controls=pass, exit 0.
```
mutbat killed=2/2 survivors=0 controls=pass
```

2.4 `python3 corpus/instruments/figure-audit.py | tail -1` — exit 0. Want: FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0.
```
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
```

2.5 `python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json 2>&1 | grep d53-1` — exit 0. Want: FIG d53-1-trailer recorded=34 derived=33 want=34 stale.
```
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
```

2.6 `sed -n '1,40p' corpus/instruments/figure-audit.py | grep -c 'allow-list:.*head'` — exit 0. Want: 1 (R74 docstring limb).
```
1
```

2.7 `sha256sum corpus/instruments/figure-audit.py` — exit 0. Want: `35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2`.
```
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  corpus/instruments/figure-audit.py
```
The run's own probe header also printed `sha256=35f7bcd3e673b81b`, the same file the gate executed.

2.8 `sha256sum corpus/instruments/figure-audit-ledger.json` — exit 0. Want: `28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b`.
```
28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b  corpus/instruments/figure-audit-ledger.json
```

## 3. C2 — 9 commands, each MATCH

3.1 `python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F41|entries='` — exit 0. Want: FRONTIER-CENSUS rows=41 admitted=41 closed=41 problem-rows=0 registry=93; FRONTIER-PASS F41 ids=S093; entries=44 pass=44 exit=0.
```
FRONTIER-CENSUS rows=41 admitted=41 closed=41 problem-rows=0 registry=93
FRONTIER-PASS F41 ids=S093
entries=44 pass=44 exit=0
```

3.2 `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S093` — exit 0. Want: sha256 OK + 15 Q OK lines.
```
S093:sha256 OK
S093:Q1 OK occurrences=2 anchor=12-ok
S093:Q2 OK occurrences=1 anchor=16-ok
S093:Q3 OK occurrences=1 anchor=40-ok
S093:Q4 OK occurrences=1 anchor=51-ok
S093:Q5 OK occurrences=1 anchor=61-ok
S093:Q6 OK occurrences=1 anchor=65-ok
S093:Q7 OK occurrences=1 anchor=68-ok
S093:Q8 OK occurrences=1 anchor=71-ok
S093:Q9 OK occurrences=1 anchor=74-ok
S093:Q10 OK occurrences=1 anchor=82-ok
S093:Q11 OK occurrences=1 anchor=88-ok
S093:Q12 OK occurrences=1 anchor=16-ok
S093:Q13 OK occurrences=1 anchor=16-ok
S093:Q14 OK occurrences=1 anchor=281-ok
S093:Q15 OK occurrences=1 anchor=281-ok
```
15 Q OK lines, each with `occurrences=` and an `anchor=<line>-ok` note (Q1 at occurrences=2 passes through its anchor, per the instrument's non-unique-quote rule at `corpus/instruments/source-recheck.py:196-203`).

3.3 `python3 corpus/instruments/capture-binding-check.py | tail -1` — exit 0. Want: records=76 bound=76 unbound=0.
```
records=76 bound=76 unbound=0
```

3.4 `ls corpus/knowledge/*.md | wc -l` — exit 0. Want: 79. → `79`
3.5 `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` — exit 0. Want: 79. → `79`
3.6 `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` — exit 0. Want: exit 0. → no stdout.
3.7 `grep -cE '^\| F41 ' corpus/README.md` — exit 0. Want: 1. → `1`
3.8 `grep -c 'the tracker is opened as S092' corpus/SOURCES.md` — exit 0. Want: **2** per `claims-erratum-1.md` (frozen want was 1). → `2`
   The JSON keeps both: `want_frozen` = the frozen comment text (want 1) and `want_effective` = `2` with `want_overridden_by` = `.ufo/waves/round-60/claims-erratum-1.md`. Observed 2 is the two declared occurrences: the corrected lead bullet `corpus/SOURCES.md:142` and the registry-changes bullet quoting it `corpus/SOURCES.md:221`.
3.9 `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` — exit 0. Want: exit 0.
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
file	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
file	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
file	ok	/fast/scratch/hyaku/kasegi-r60/ExecCounters/tmp.v0nxEx7BP8/clone/corpus/SOURCES.md
```
exit 0 (the want). The six `W04` duplicate-url notes are on pre-existing rows (S028, S029, S072, S076, S080, S085 — none is S093); the validator still reports `file ok` and exits 0.

## 4. Caveats — recorded, not fixed

4.1 Erratum override. C2 #8 is the only want changed by `.ufo/waves/round-60/claims-erratum-1.md` (1 → 2). Recorded structurally in the JSON (`erratum_applied`, and per record `want_frozen` / `want_effective` / `want_overridden_by`). No claims file, erratum or lane file was edited.

4.2 Pipeline exit masking. In bash without `pipefail`, the recorded `exit_code` of a piped counted command is the last stage's, not the instrument's. Affected: C1 #2–#6 and C2 #1, #3, #4. Demonstrated with the same shape:
```
$ bash -c 'python3 -c "import sys; print(1); sys.exit(7)" | tail -1'; echo "pipeline_exit=$?"
1
pipeline_exit=0
```
The wants of those commands are content wants and all reproduced, so no verdict changes; a future counter that needs the instrument's own exit must not read it through a pipe. C1 #1, #7, #8, C2 #2, #5–#9 are unpiped, and their recorded exit codes are the instrument's.

4.3 C1 #1's frozen scratch argument is `/fast/scratch/hyaku/kasegi-r60/l1/c1-after`, not this seat's dir. It is part of the frozen command and was run literally; the runner `rm -rf`s it at start and removes it in its `EXIT` trap (`c1-probe-run-r60.sh:9-10`). Verified after the run: `ls -d /fast/scratch/hyaku/kasegi-r60/l1/c1-after` → `No such file or directory` (exit 2). No residue.

4.4 Recheck-line cd prefix (the assigned caveat; `claims.json` non-claim item on the ExportReplay class). Counted over the clone's knowledge files:
- knowledge recheck lines: `grep -h '^recheck:' corpus/knowledge/*.md | wc -l` → `79`
- of which start with the absolute lane `cd`: `... | grep -c '^recheck: cd '` → `70`
- this round's new entry `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:6` is `recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S093   # run from the lane root (…)` — no `cd` prefix.

So 70 pre-round-60 entries still bake the absolute lane `cd` (and 9, including this round's, do not); the pre-round-60 class is unchanged by this round, as declared. Recorded as an observation, not repaired. It also means the new line is cwd-dependent by design: the frontier counter executes recheck lines with cwd = the counted root, which is why no `cd` is baked in.

4.5 `sources-census.sh validate` exits 0 with six pre-existing `W04` duplicate-url notes (3.9). Not a mismatch against the want (exit 0), but the "ok" line is not a silent-clean signal.

## 5. Boundaries and state

- Lane read-only: the only writes under `L` are `.ufo/waves/round-60/w1/ExecCounters.md` and `.ufo/waves/round-60/w1/ExecCounters.json`. No lane instrument, ledger, SOURCES/README/PROVINCE/QUALITY file or knowledge file was edited; no git mutation was run against `L`.
- Scratch `S=/fast/scratch/hyaku/kasegi-r60/ExecCounters` held the clone (`tmp.v0nxEx7BP8/clone`) and `run.py`; both are removed at yield (see §6). No `/tmp` writes.
- No tool was installed or upgraded for this seat, so there is no tool record to file.
- No credential material appears in either artifact; the only URLs quoted are public registry URLs printed by `sources-census.sh`.

## 6. Scratch removal

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r60/ExecCounters
$ ls -d /fast/scratch/hyaku/kasegi-r60/ExecCounters; echo "ls_exit=$?"
ls: cannot access '/fast/scratch/hyaku/kasegi-r60/ExecCounters': No such file or directory
ls_exit=2
$ ls -d /fast/scratch/hyaku/kasegi-r60/l1/c1-after; echo "residue_ls_exit=$?"
ls: cannot access '/fast/scratch/hyaku/kasegi-r60/l1/c1-after': No such file or directory
residue_ls_exit=2
```
No leftovers; the clone, `run.py` and the C1 probe scratch are all gone. Artifacts retained: `W/ExecCounters.md` and `W/ExecCounters.json` only.
