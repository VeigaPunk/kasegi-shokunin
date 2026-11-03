# LedgerReplay — VERDICT: OK (replay agrees with the lane instrument on 35/35 ids, 0 disagreements; selftest green; 4 advisory findings on the ledger's own derive forms, no ledger edit made)

Seat LedgerReplay, kasegi round-57 w1. Task: re-derive every `figure-audit-ledger.json`
figure with an implementation independent of `corpus/instruments/figure-audit.py`, and
compare verdict sets.

Environment: Linux 7.2.11-arch1-1 x64, `Python 3.14.8`, `GNU bash, version 5.3.20(1)-release`,
`/usr/bin/python` and `/usr/bin/python3` are both 3.14.8. No tool install or upgrade was
performed this seat (none was needed), so there is no install record to file.

Artifacts under test (read-only, hashes taken before the run):

```
$ sha256sum corpus/instruments/figure-audit-ledger.json
94d8ac9b48e1d96d6579f622feed53a4a53cb3e92319e6d7521716bcee5602cd  .../corpus/instruments/figure-audit-ledger.json
$ sha256sum .ufo/waves/round-57/w1/LedgerReplay/replay.py
af30bbfda4f8b23ea3a3e696c4c18529da04be0fb5dc4cff71edbb93e032c03d  .../w1/LedgerReplay/replay.py
```

Lane state at the time of the run (read-only git, no mutation):

```
$ git -C L rev-parse --show-toplevel   -> /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git -C L rev-parse HEAD              -> cd3029876eac7189aaff0d32b26031c0defa35aa
$ git -C L status --porcelain -- corpus/ SCORECARD.md LOG.md PROVINCE.md
 M LOG.md
 M SCORECARD.md
```

The two modified files are the fleet-root-trailer edits made by the round's own driver, not
by this seat; nothing under `corpus/` is dirty, so every working-tree read below is the
committed byte image. `git merge-base --is-ancestor eae1d61 HEAD` -> `base IS ancestor of HEAD`.

---

## 1. The replay script

`W/LedgerReplay/replay.py` (stdlib only: `json`, `os`, `subprocess`, `sys`; no import of the
instrument, no shared helper). Per figure: `subprocess.run(["bash","-c",derive], cwd=L,
stdout=PIPE, stderr=STDOUT, timeout=120)`; first non-empty line of the merged stream,
stripped, whole-value compared to `want`; one line per id; `REPLAY-TOTAL`; exit 1 on any STALE.

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-57/w1/LedgerReplay/replay.py
```

## 2. Replay output — full, 35 ids, exit 0

```
REPLAY frontier-rows                      derived=34   want=34   ok
REPLAY registry-rows                      derived=85   want=85   ok
REPLAY knowledge-expected-entries         derived=72   want=72   ok
REPLAY knowledge-files                    derived=72   want=72   ok
REPLAY capture-lines-s085                 derived=542  want=542  ok
REPLAY capture-bytes-s085                 derived=7590 want=7590 ok
REPLAY capture-lines-s086                 derived=731  want=731  ok
REPLAY capture-sha256-s086                derived=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f want=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f ok
REPLAY frontier-rows-r54                  derived=35   want=35   ok
REPLAY registry-rows-r54                  derived=86   want=86   ok
REPLAY entries-r54                        derived=38   want=38   ok
REPLAY knowledge-expected-r54             derived=73   want=73   ok
REPLAY knowledge-files-r54                derived=73   want=73   ok
REPLAY figure-audit-mentions-base-scorecard            derived=2 want=2 ok
REPLAY figure-audit-mentions-base-log                  derived=0 want=0 ok
REPLAY figure-audit-mentions-base-knowledge-expected   derived=0 want=0 ok
REPLAY frontier-rows-r55                  derived=36   want=36   ok
REPLAY registry-rows-r55                  derived=87   want=87   ok
REPLAY entries-r55                        derived=39   want=39   ok
REPLAY knowledge-expected-r55             derived=74   want=74   ok
REPLAY knowledge-files-r55                derived=74   want=74   ok
REPLAY census-fresh-literal-r55           derived=stale want=stale ok
REPLAY census-internal-r55-receipt        derived=1118 want=1118 ok
REPLAY census-gone-r55-receipt            derived=3883 want=3883 ok
REPLAY census-fixedpoint-internal-r55     derived=1119 want=1119 ok
REPLAY census-fixedpoint-gone-r55         derived=3882 want=3882 ok
REPLAY fail-entry-records                 derived=33   want=33   ok
REPLAY frontier-rows-r56                  derived=37   want=37   ok
REPLAY registry-rows-r56                  derived=88   want=88   ok
REPLAY entries-r56                        derived=40   want=40   ok
REPLAY knowledge-expected-r56             derived=75   want=75   ok
REPLAY knowledge-files-r56                derived=75   want=75   ok
REPLAY census-fresh-literal-r56           derived=ok   want=ok   ok
REPLAY census-internal-r56-receipt        derived=1130 want=1130 ok
REPLAY census-gone-r56-receipt            derived=3915 want=3915 ok
REPLAY-TOTAL figures=35 ok=35 stale=0
```

`EXIT=0`. Wall time `0.08s`. Two consecutive runs are byte-identical (`cmp -s` -> IDENTICAL,
exits 0/0), so the table is deterministic.

(The columns above are whitespace-collapsed for this file; the script itself pads
`derived=`/`want=` to 70 columns. Raw stdout is reproduced whole in the summary section.)

## 3. Lane instrument over the lane root — full, exit 0

```
$ cd L && python3 corpus/instruments/figure-audit.py .
```

Every line verbatim:

```
FIG frontier-rows recorded=34 derived=34 ok
FIG registry-rows recorded=85 derived=85 ok
FIG knowledge-expected-entries recorded=72 derived=72 ok
FIG knowledge-files recorded=72 derived=72 ok
FIG capture-lines-s085 recorded=543 (filed; superseded by the r54 D53-2 correction) derived=542 ok
FIG capture-bytes-s085 recorded=7590 derived=7590 ok
FIG capture-lines-s086 recorded=731 derived=731 ok
FIG capture-sha256-s086 recorded=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f derived=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f ok
FIG frontier-rows-r54 recorded=35 derived=35 ok
FIG registry-rows-r54 recorded=86 derived=86 ok
FIG entries-r54 recorded=38 derived=38 ok
FIG knowledge-expected-r54 recorded=73 derived=73 ok
FIG knowledge-files-r54 recorded=73 derived=73 ok
FIG figure-audit-mentions-base-scorecard recorded=2 (the receipt's limb; the filed prose 0 superseded) derived=2 ok
FIG figure-audit-mentions-base-log recorded=0 derived=0 ok
FIG figure-audit-mentions-base-knowledge-expected recorded=0 derived=0 ok
FIG frontier-rows-r55 recorded=36 derived=36 ok
FIG registry-rows-r55 recorded=87 derived=87 ok
FIG entries-r55 recorded=39 derived=39 ok
FIG knowledge-expected-r55 recorded=74 derived=74 ok
FIG knowledge-files-r55 recorded=74 derived=74 ok
FIG census-fresh-literal-r55 recorded=stale (the receipt's printed limb; the filed prose ok superseded) derived=stale ok
FIG census-internal-r55-receipt recorded=1118 derived=1118 ok
FIG census-gone-r55-receipt recorded=3883 derived=3883 ok
FIG census-fixedpoint-internal-r55 recorded=1119 derived=1119 ok
FIG census-fixedpoint-gone-r55 recorded=3882 derived=3882 ok
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=33 ok
FIG frontier-rows-r56 recorded=37 derived=37 ok
FIG registry-rows-r56 recorded=88 derived=88 ok
FIG entries-r56 recorded=40 derived=40 ok
FIG knowledge-expected-r56 recorded=75 derived=75 ok
FIG knowledge-files-r56 recorded=75 derived=75 ok
FIG census-fresh-literal-r56 recorded=ok derived=ok ok
FIG census-internal-r56-receipt recorded=1130 derived=1130 ok
FIG census-gone-r56-receipt recorded=3915 derived=3915 ok
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
```

`EXIT=0`, 36 stdout lines, no `UNAVAILABLE` / reject line anywhere
(`grep -nE 'UNAVAILABLE|REJECT|reject|skipped'` -> `none`). The summary line equals the
C1 counting-command literal `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`.

## 4. Agreement verdict over the 35 ids

Set comparison done by a third program (`$S/agree.py`) that parses both programs' stdout and
diffs the verdict per id — not by eye:

```
$ python3 $S/agree.py L/corpus/instruments/figure-audit-ledger.json L
replay ids=35 instrument ids=35 ledger ids=35
replay exit=0  instrument exit=0
ids missing from one side: [] []
VERDICT DISAGREEMENTS: 0
replay ok=35 stale=0 ; instrument ok=35 stale=0
```

**AGREEMENT: 35/35, zero disagreements, no id present on only one side.**
Both sides read `ok` on every id, including all eight new r56 ids and the amended
`fail-entry-records`.

The agreement is empirical, not structural — the two implementations differ by design, and
two synthetic cases do make them diverge (finding F4). Those cases are unreachable from the
real ledger: a per-id probe over all 35 recorded derives shows every one exits 0 with exactly
one non-empty stdout line and zero stderr bytes, and none is self-referential
(`derive` mentioning `figure-audit-ledger.json`):

```
$ python3 $S/probe.py
PROBE <each id>  exit=0 stdout_lines=1 stderr_bytes=0 ledger_self_ref=False   (35 rows)
PROBE-TOTAL figures=35 anomalous=0
```

## 5. Selftest

```
$ cd L && python3 corpus/instruments/figure-audit.py --selftest
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest cases=5 failures=0
```

`SELFTEST_EXIT=0`, summary line `selftest cases=5 failures=0` — matches the C1 kill-rule limb.

## 6. Non-vacuity of both programs (positive + negative controls I ran myself)

A green table is only evidence if the machinery can go red. Independent mutants, all on
scratch copies (`--ledger` points outside the lane; the lane ledger is never written):

```
$ python3 .../replay.py --ledger $S/mut-want.json           # registry-rows-r56 want 88 -> 87, 1 field changed
REPLAY registry-rows-r56  derived=88  want=87  STALE
REPLAY-TOTAL figures=35 ok=34 stale=1        REPLAY_EXIT=1
$ cd L && python3 corpus/instruments/figure-audit.py --ledger $S/mut-want.json .
FIG registry-rows-r56 recorded=88 derived=88 want=87 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1  INSTRUMENT_EXIT=1
```

Reproduced the two frozen C1 red controls from committed bytes alone:

```
--- RED1 (registry-rows-r56 want=87) ---
FIG registry-rows-r56 recorded=88 derived=88 want=87 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
--- RED2 (same amended derive pointed at a 34-bearing receipt copy) ---
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=34 want=33 stale
FIGURE-AUDIT figures=35 ok=34 stale=1 exit=1
```

Each red control prints exactly 1 stale line, on exactly the intended id, and exits 1 — the
C1 kill-rule conditions on red controls 1 and 2 are not tripped.

Base-state red, for the frozen `before` (`figures=27 ok=26 stale=1 exit=1`):

```
$ git show eae1d61:corpus/instruments/figure-audit-ledger.json > $S/base-ledger.json   # 27 ids
$ cd L && python3 corpus/instruments/figure-audit.py --ledger $S/base-ledger.json .
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=UNAVAILABLE reason=derive-exit-1 stale
FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1     BASE_AUDIT_EXIT=1
```

The base ledger's 27 ids are a strict subset of the current 35: `added: 8` (exactly the eight
r56 ids), `removed: 0`. Only one pre-existing entry changed a field between base and
working tree — `fail-entry-records`, fields `derive` and `record` (the recorded amendment), as
the claim requires.

---

## 7. The eight r56 ids: rev-pinned vs working-tree, item by item

Classification method: inspect the `derive` string for `git show <rev>:<path>` or
`git ls-tree <rev>` (reads the object database at a named commit) versus a plain path read
(resolves through the working tree). Line numbers are the ledger's own.

| # | id | ledger | derive shape | CLASS |
|---|----|--------|--------------|-------|
| 1 | frontier-rows-r56 | :217-224 | `git show 8a5d753…:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | **rev-pinned** |
| 2 | registry-rows-r56 | :225-232 | `git show 8a5d753…:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | **rev-pinned** |
| 3 | entries-r56 | :233-240 | `git show 8a5d753…:corpus/README.md \| grep -E … \| awk -F'\|' '{n=split($5,p,","); s+=n} END{print s}'` | **rev-pinned** |
| 4 | knowledge-expected-r56 | :241-248 | `git show 8a5d753…:corpus/instruments/knowledge-expected.txt \| grep -c '^corpus/knowledge/'` | **rev-pinned** |
| 5 | knowledge-files-r56 | :249-256 | `git ls-tree --name-only 8a5d753… -- corpus/knowledge/ \| grep -c '\.md$'` | **rev-pinned** |
| 6 | census-fresh-literal-r56 | :257-263 | `grep -oE 'CENSUS-FRESH=[a-z]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | **working-tree** |
| 7 | census-internal-r56-receipt | :264-270 | `grep -oE 'internal=[0-9]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | **working-tree** |
| 8 | census-gone-r56-receipt | :271-278 | `grep -oE 'gone=[0-9]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | **working-tree** |

**Count: 5 rev-pinned, 3 working-tree.** Which kind each is, stated plainly: ids 1-5 read
committed bytes at the round-56 results tip `8a5d7538b0caa50300b1eee88442a230d9a433f2` and
are therefore immune to the working tree moving under them; ids 6-8 read the file
`.ufo/waves/round-56/controls/gate-final-r56.txt` as it currently sits on disk.

Small corollaries I verified rather than assumed:

- `git ls-tree` without `-r` (id 5) is still an object-database read, and the flat count is the
  right count here: `corpus/knowledge/` has **0 subdirectories at every rev this ledger pins**
  (`32782bd` flat=72 rec=72, `5108584a` 73/73, `133c5753` 74/74, `8a5d7538` 75/75 — all
  equal). So the non-recursive form is not silently under-counting, today.
- `awk -F'|' $5` (id 3) is the knowledge-path cell, not the sources cell. At the r56 tip the
  two candidate cells sum to 40 and 60 respectively, and 40 is the receipt's `entries=40`;
  cross-checked against all four counter receipts (see §8). Field layout at the r56 tip:
  `f5=< knowledge/cvss-v4-severity-and-vector.md > f6=< S001, S002 >`.
- The three working-tree ids read a receipt whose bytes have **not moved**: the git blob for
  `gate-final-r56.txt` is identical at base, at the r56 tip and at HEAD
  (`rev-parse` -> `b5fca99a3211f9ca4092b9a2c19bb233ae370a7e` three times;
  `git log base..HEAD -- <path>` -> 0 commits; working-tree sha256 == r56-tip blob sha256).
  Same for the r53 receipt behind `fail-entry-records` (`fbc866a7…` at base, r56 tip and HEAD;
  0 commits in between). So id 6-8 and `fail-entry-records` are *stable* working-tree reads,
  not *drifted* ones — the classification stands, but there is no live staleness today.
- The value side is genuinely live: tampering a scratch export's r56 receipt
  (`internal 1130->1131`, `gone 3915->3914`, `CENSUS-FRESH ok->stale`) flips exactly those
  three figures to stale, while the five rev-pinned r56 figures are untouched by the same edit.

---

## 8. Cross-validation of the four rev-pinned counter forms against their own receipts

The five rev-pinned derives are not compared against a single hand-written number — each rev
also carries its own counter receipt, and my derives reproduce it:

```
rev=32782bd       derive rows=34 registry=85 entries=37 | receipt FRONTIER-CENSUS rows=34 … registry=85 / entries=37 pass=4
rev=5108584aab38  derive rows=35 registry=86 entries=38 | receipt FRONTIER-CENSUS rows=35 … registry=86 / entries=38 pass=5
rev=133c57539409  derive rows=36 registry=87 entries=39 | receipt FRONTIER-CENSUS rows=36 … registry=87 / entries=39 pass=6
rev=8a5d7538b0ca  derive rows=37 registry=88 entries=40 | receipt FRONTIER-CENSUS rows=37 … registry=88 / entries=40 pass=7
```

8/8 coincidences across four rounds of three figures: the `grep -cE` and `awk $5` forms are
form-validated, not merely value-validated. The `entries` derive's `$5` cell choice is
corroborated by the counter's own parser, which splits the *entry* cell the same way
(`corpus/instruments/frontier-recheck-count.py:515`,
`entries = [part.strip() for part in cell.split(",") if part.strip()]`).

---

## 9. Findings (text only — no ledger, claims, SOURCES, README, PROVINCE or knowledge file was edited)

**F1 (advisory, C1 depth:verifiability) — two pinned figures are green-blind to a failed git read.**
`figure-audit-mentions-base-log` (ledger:119-126) and
`figure-audit-mentions-base-knowledge-expected` (ledger:127-134) use
`git show <rev>:<path> | awk '/figure-audit/{n++} END{print n+0}'`. The awk form prints `0`
and exits `0` even when the pipe's left side died, so the instrument's whole-value comparison
reads `derived=0 == want=0 -> ok`:

```
$ bash -c "git show deadbeef…:LOG.md 2>/dev/null | awk '/figure-audit/{n++} END{print n+0}'"
0                                    (exit 0)
$ bash -c "git show deadbeef…:LOG.md 2>/dev/null | grep -c 'figure-audit'"
0                                    (exit 1 — correctly red)
```

The zero-is-real claim is true today (I confirmed `grep -c 'figure-audit'` exits 1 on both
files at `32782bd`, i.e. genuine zeros), and the trade-off is disclosed in each entry's
`record` field. But 2 of the 35 figures cannot fail on a bad or missing git object — the audit
would still print `figures=35 ok=35 stale=0 exit=0` if those two revs stopped resolving. The
audit also agreed with the replay on these two ids in the pure-export probe precisely because
both read `0`/`ok` where the honest answer is "the object was unavailable" (see F2).
Severity: low today (commits are immutable in this repo; no history rewrite is in play).

**F2 (advisory, instrument safety claim) — `check_read_only` is bypassable with `;`.**
The instrument's docstring and the ledger's `what` field both claim "the audit never runs a
mutating command". The gate only splits on `|` and `>`
(`corpus/instruments/figure-audit.py:76`, `head = cmd.split("|")[0].split(">")[0].strip()`),
so a `;`-chained write passes and executes:

```
$ # synthetic ledger: derive = "cat g.txt; echo PWNED > side-effect.txt", want = 35
$ cd L && python3 corpus/instruments/figure-audit.py --ledger $S/mut-chain.json --root $FX
FIG chain-write recorded=35 derived=35 ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0        (exit 0)
$ ls $FX
g.txt  side-effect.txt                            <-- the write happened
```

Not reachable from the current ledger: all 35 recorded derives were probed and each is a
single clean pipeline with exit 0, one stdout line, zero stderr bytes, no `;`
(`PROBE-TOTAL figures=35 anomalous=0`). So this is a gate hardening note, not a live breach.

**F3 (advisory, C1 host-portability limb confirmed, with its cost stated) — the amended
`fail-entry-records` derive is host-portable but is now a receipt-transcription, not a
re-derivation.** Verified portability: it prints `33` both at the lane root and in a bare
scratch directory containing only the receipt bytes, with no instrument and no lane layout
present, while the *old* base derive dies in that same bare directory:

```
at-lane-root:  33
detached-copy: 33
old-derive-in-bare-dir: 0   (exit 1 — needs corpus/instruments/frontier-recheck-count.py and a lane)
```

Verified it is still a live read, not a literal: tampering a scratch copy of the receipt
`FAIL_entry_records=33 -> 34` makes the derive print `34`. What is given up: `33` is no longer
re-derivable from tree bytes at any rev. At the r53 rev the README yields
`entries=37`, `pass=4` (arithmetic `37 - 4 = 33` corroborates the recorded subtraction, and the
receipt's own `entries=37 pass=4 exit=1` line matches), but the `FAIL` class itself has 0 lines
on this host (`python corpus/instruments/frontier-recheck-count.py | grep -c '^FAIL'` -> `0`,
exit 1). The figure therefore pins a Windows-host observation as recorded, exactly as the C1
frozen sentence says. Worth stating plainly in the round report: for this one id the
`depth:verifiability` guarantee is "the receipt says 33 and the receipt bytes are pinned",
not "33 recomputes from the corpus".

**F4 (advisory, comparison scope) — the two implementations do diverge on edge policies; the
35/35 agreement is empirical.** Two synthetic one-figure ledgers with read-only heads:

```
# (i) right line, nonzero exit: "cat g.txt; false"
REPLAY exit1-right-line  derived=35  want=35  ok            REPLAY_EXIT=0
FIG exit1-right-line recorded=35 derived=UNAVAILABLE reason=derive-exit-1 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1                  INSTRUMENT_EXIT=1
   -> replay ok / instrument STALE   (instrument is fail-closed on exit; replay grades stdout only)

# (ii) stderr line before the wanted stdout line: "cat nosuchfile-abc; cat g.txt"
REPLAY stderr-first  derived=cat: nosuchfile-abc: No such file or directory  want=35  STALE
FIG stderr-first recorded=35 derived=35 ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
   -> replay STALE / instrument ok   (instrument grades stdout alone; replay merges stderr as specified)
```

Neither policy is wrong against its own spec, and neither case is reachable from the recorded
ledger (all 35 derives are exit-0, single-line, stderr-free). Recorded so the agreement is not
over-read: the two programs are independent, and the 35/35 result is a measurement of *this*
ledger, which is what makes it worth something.

**F5 (note, not a defect) — "rev-pinned" still needs the object database.** Over a pure
`git archive HEAD` export (10 615 files, `.ufo` receipts included) the 24 rev-pinned figures go
red with `fatal: not a git repository`, taking the audit to
`figures=35 ok=13 stale=22 exit=1`. That is correct behaviour for an audit designed to run in
the lane root, not a ledger fault; recorded only so a later reader does not mistake an
export-run red for ledger drift. In the same export two ids diverged between the programs —
again exactly the awk-zero pair of F1.

**F6 (note) — degenerate ledgers.** The instrument guards the empty ledger
(`{"figures":[]}` -> `FIGURE-AUDIT: UNAVAILABLE reason=ledger-shape want=figures-array`,
exit 2), while the replay would print `REPLAY-TOTAL figures=0 ok=0 stale=0` and exit 0. The
replay was specified as a grader of the delivered ledger, not as a harness, so this is a
scope observation only; the real ledger has 35 unique ids (`unique=35`, `dups: none`, every
entry carries `derive`/`want`/`record`/`recorded`, every cited rev resolves under
`git rev-parse --verify <rev>^{commit}`).

---

## 10. Tooling and hygiene

- Tools installed or upgraded this seat: **none**. `python3` 3.14.8, `bash` 5.3.20 and the
  git already on the host covered everything; no `pacman`, `uv tool`, `npx` or binary install
  was run, so the paused-package-manager rule was never engaged.
- Scratch root `S=/fast/scratch/hyaku/kasegi-r57/LedgerReplay`, created with `mkdir -p`,
  `TMPDIR=<S>` exported for every run, contents deleted before yield. **No leftover.**
- Lane repo: read-only throughout. No `git add/commit/stash/checkout/switch/reset/pull/push`,
  no `jj`. Only `rev-parse`, `status`, `show`, `ls-tree`, `cat-file`, `log`, `merge-base`,
  `archive`, `grep`, `rev-parse --verify` were used. All mutants, exports and tampered receipts
  live under `S`; `--ledger`/`--root` pointed the instrument outside the lane for every
  negative control.
- Writes: only `W/LedgerReplay/replay.py` and this file. No fleet-root file touched; no
  sibling lane, no `shokuknow`.
- Credential material: none encountered, none written. No secrets, tokens, cookies, session
  values or `op://` references appear in this file or in `replay.py`.

## 11. What this seat does not claim

This seat verified the ledger's replay, the instrument's agreement with it, and the
classification of the eight r56 derives. It did **not** re-judge C1's or C2's frozen sentences,
did not touch `claims.json`, did not run the lane test suite, and did not verify any C2 figure
(S089/S090 captures, frontier counters, knowledge counts) beyond the five counter forms quoted
in §8. F1-F6 are findings for the round report; every one is reported as text, and the ledger
was not modified.
