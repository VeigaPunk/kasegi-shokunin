# ExecHarnessAfter — C2 harness after-state (round 34, wave 1)

Seat: `ExecHarnessAfter`, executor, leaf of the L2 wave. Axes: `depth:verifiability`, `coverage`.
Assigned: run `corpus/instruments/frontier-recheck-count.py` on the **landed** F17 bytes and record
`entries=20 pass=20 exit=0` incl. `PASS F17 … ids=S051`; confirm the junk twin is not counted as an
entry. Scope decision by the L1 (`agent://KasegiR34`, 05:36Z message): *"Authorized: you own the
`corpus/README.md` F17 row append and the harness after-state … append exactly one F17 row in the
same 6-column frontier-table shape as F16 … Do NOT add any second row later; I will not add one."*
No seat among the 65 wave-1 items owned that row (ScribeEntryF17 confirmed the same by searching all
prompts; round 33 had a dedicated `ScribeReadmeF16`).

Files I wrote: `corpus/README.md` (append-only, 26 inserted / 0 deleted lines, one `## Round-34
admission` section) and this receipt. Nothing else.

## Report

### 1. Landing state before my append (polled, 10 s interval, exact timestamps UTC)

```
05:31:39 capture=1  manifest=0  entry=0  s051row=0  frontier=16     (S051.txt present, 8502 B)
05:33:49 capture=1  manifest=1  entry=0  s051row=0  frontier=16     (round-34 manifest lands)
05:34:49 capture=1  manifest=1  entry=1  s051row=0  frontier=16     (F17 entry lands)
05:37:39 capture=1  manifest=1  entry=1  s051row=1  frontier=16     (S051 registry row lands)
```
All three prerequisites present; `frontier=16` — the README F17 row did not exist and no seat owned
it, so without the append the harness could only print `entries=19`.

### 2. Pre-append harness run on identical instrument bytes (`sha256 87b14892…`)

```
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0                      EXIT=0
```
This is the exact before-value for the append delta: same instrument digest as the after-run below,
so `19 → 20` is attributable to the README row alone.

### 3. The append (verbatim, `corpus/README.md:343-368`)

```markdown

## Round-34 admission — coverage map row and Frontier F17 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-34 entry
`knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (Frontier F17, source S051; source basis:
Immunefi's own Vulnerability Severity Classification System v2.2 at
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/, captured
2026-10-26 under `corpus/source-snapshots/round-34/`) is recorded here as an appended amendment so
every existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F17 frontier row is listed here on the same table shape as the frontier
above.

| Area | Entry | Source basis |
|---|---|---|
| Web3/smart-contract bounty severity classification (round 34) | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F17 | Immunefi Vulnerability Severity Classification System v2.2 — Web3/smart-contract bounty severity classification | admitted | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 | Read a level from Immunefi's own per-asset-class table: the five numbered levels rank impacts inside one scope table, the level is fixed largely by impact — "finalizes them largely by the impact that they cause" (S051.txt:52) — under a downgrade-or-reject carve-out for elevated privileges or uncommon user interaction (S051.txt:55-56), and the funds boundary is whose funds and for how long they stay frozen: theft of any user funds is Critical (S051.txt:75) while "Temporary freezing of funds" is High (S051.txt:88). The page carries no CVSS mapping, no reward figure and no version-selection rule (FC-2/FC-3/FC-4), so neither a payout nor portability across asset classes follows from a level. |

[r34 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 34 the frontier stands at **17/17 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34. The 0/18 sentence is untouched: the lost-domain
denominator still holds 0 of 18 surfaces present, and the frontier count stays outside it.
```

Shape mirrors the round-33 precedent (`git diff 9f98488^ 9f98488 -- corpus/README.md`: appended
`## Round-33 admission` section holding both a coverage-map row and the F16 row on the
`| id | topic | status | entry | sources | next |` shape), so no existing line moves:

```
$ git diff --numstat -- corpus/README.md
26	0	corpus/README.md              # insertions 26, deletions 0
```

Every claim in the row cell is grounded in the landed entry / capture, and I checked each citation
line before writing it:

```
$ grep -n "finalizes them largely\|The development of this scale\|simplified 5-level\|Temporary freezing of funds\|Direct theft of any user funds\|The table below is mostly" corpus/source-snapshots/round-34/S051.txt
46:At Immunefi, we classify bugs on a simplified 5-level scale:
52:The development of this scale took into consideration multiple factors that may affect a vulnerability and its likelihood of exploitation, but finalizes them largely by the impact that they cause.
53:The table below is mostly concerned with the consequence of a successful
75:- Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield
88:- Temporary freezing of funds
```
The cell deliberately does **not** claim a v2.2-vs-v2.3 programme selector: the landed entry's
`## Honest limit` records that the capture names v2.2 twice and `v2.3` zero times and prints no
version-selection rule (`grep -c 'v2\.3' corpus/source-snapshots/round-34/S051.txt` → `0`), so the
row says "no version-selection rule".

### 4. Harness after-state — the measured claim value

```
$ python3 corpus/instruments/frontier-recheck-count.py
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
EXIT=0
```
Two identical runs (`--json` receipt and plain), `final_exit=0`, 21 output lines; **no F-row
failed**, so there is no failing line to quote.

Machine receipt (`--json`):

```
entries 20 pass 20 dup None
PASS knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ['S051'] ['S051'] corpus/source-snapshots/round-34/manifest.json 0 []
```
→ `declared_ids == recheck_ids == ['S051']`, `manifest` bound, `exit=0`, `problems=[]`.

This satisfies C2's harness limb verbatim: `PASS F17 … ids=S051` and `entries=20 pass=20 exit=0`.

### 5. Junk twin is NOT counted — three measurements

(a) Live output names no junk path:
```
$ grep -c 'junk-f17' <harness output>     -> 0
$ grep -c 'junk-f17' corpus/README.md     -> 0
```
(b) The counter enumerates only **admitted README rows** (`read_frontier()` reads
`corpus/README.md`; `evaluate()` resolves the row's entry cell). A junk file's presence on disk
contributes nothing — control in a scratch root with the junk twin copied to
`corpus/knowledge/junk-f17.md` and *no* admitted row:
```
entries=0 pass=0 exit=1        ctlC_exit=1
```
(c) Conversely, a junk twin **pointed at by an admitted row** is counted — and the current
instrument **passes** it (see §7 residual gap):
```
PASS     F99  knowledge/junk-f17.md                                ids=S051           exit=0
entries=1 pass=1 exit=0        ctlB_exit=0
```

Fail-closed controls on the same instrument (E/F from the docstring):
```
# control E — admitted row, entry file absent
FAIL     F98  knowledge/does-not-exist.md                          ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1        ctlE_exit=1

# control F — two admitted rows resolving to one entry realpath
FAIL     F96  knowledge/real.md                                    ids=S051           exit=-    problems=manifest-unreadable
FAIL     F97  knowledge/real.md                                    ids=S051           exit=-    problems=manifest-unreadable
DUPLICATE-ENTRY F96,F97 knowledge/real.md
entries=2 pass=0 exit=1        ctlF_exit=1
```

### 6. Adjoining C2 counters I happened to re-derive (owned by ExecCensusAfter / ExecRegressionC2)

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                                   -> 17
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md         -> 51
grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md               -> 1
grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l                      -> 1
ls corpus/knowledge/*.md | wc -l                                             -> 46
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
  -> S051:sha256 OK, Q1-Q18 each `occurrences=1` (Q9/Q17 normalized), EXIT=0
```

### 7. Findings (reported, not judged)

**F-A — README frontier row had no owner (process gap, closed here under L1 authorization).**
No seat among the 65 wave-1 items mentions `corpus/README.md`; round 33 had `ScribeReadmeF16`. The
C2 predicate (`PASS F17 …` / `entries=20`) is unmeasurable without that row. The L1 authorized this
seat to append it; the row is in §3, 26/0 lines, and no second row was added. If integration adds
another F17 row, the counter will print `DUPLICATE-ENTRY` (control F, §5) — do not.

**F-B — the harness does not read entry bodies; the junk twin's rejection lives in the reviewer,
not in this counter (residual, measured).** Control (c) shows a junk-shaped entry admitted by a row
passes: declared `S051`, recheck `--source S051`, and `cited` is satisfied because the junk body's
own prose contains the token `S051` ("… a `source:` line citing S051 …"). `source-recheck.py`
likewise cannot see entry text: it re-verifies the *manifest's* assertions against the capture. Its
rejection power is real only when the fabricated string is itself asserted:
```
# scratch manifest asserting the junk twin's fabricated sentence
$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json --source S051
S051:sha256 OK
S051:Q1 MISMATCH reason=quote-not-found
junkman_exit=1
$ grep -c "five severity levels for smart-contract exploits" corpus/source-snapshots/round-34/S051.txt
0                              grep_exit=1
```
So C2's kill-rule wording "junk twin rejected by the admission gate (source-recheck exit != 0;
reviewer REFUSE)" holds through the **reviewer** limb (`RevEntryF17`'s `grep -c` of each quoted
string against `S051.txt`, plus non-admission to the frontier table), not through the counter and
not through the landed manifest's recheck. The honest boundary for the harness limb is: *it counts
what the README admits and it fails closed on missing/duplicate rows — it is not a body-content
gate.*

**F-C — mid-flight instrument regression I observed and reported (now resolved).** At
instrument `sha256 2cff234e751c…` the live run was:
```
FAIL     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=-    problems=selection-not-in-header-sources
FAIL     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=-    problems=selection-not-in-header-sources
FAIL     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=-    problems=selection-not-in-header-sources
FAIL     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=-    problems=selection-not-in-header-sources
FAIL     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=-    problems=selection-not-in-header-sources
entries=19 pass=14 exit=1
```
(In-flight `ExecFrontierBidirectional` patch requiring `recheck_ids ⊆ header source:` ids; F01–F05
legitimately select a second source via per-source evidence bullets.) Reported to that seat
(`agent://ExecFrontierBidirectional`) with the R9 wording from
`.ufo/waves/round-33/wave1/MutEntryF16.md:179`; also relayed to `RevC2BeforeAfter`, who had seen the
same red run. Green again from 05:35:47 (report showed a transient
`ValueError: too many values to unpack (expected 5, got 6)` at 05:36 warm-up — instrument mid-edit).
The landed rule A is bidirectional as
`declared_set = header source: ids ∪ per-source evidence bullets`; `header-sources-not-rechecked`
(`declared ⊄ recheck`) **and** `selection-not-declared-by-entry` (`recheck ⊄ declared`) both fire,
and `cited` now excludes `source:`/`recheck:`/`evidence:` declaration lines (closes the vacuous
`selection-not-cited-by-entry` that R9 named). My after-state is measured on that green digest.

### 7b. Quiescence confirmation (instrument owner) + its selftest, measured by this seat

`ExecFrontierBidirectional` messaged at 05:5xZ that its bytes are final at
`sha256 87b14892…` — the same digest I measured. Independently re-run here:

```
$ sha256sum corpus/instruments/frontier-recheck-count.py
87b14892dfc42792056c7a9f09a0783e9d749d0478f376841c98bfc25e0a7c29  (427 lines)
$ python3 corpus/instruments/frontier-recheck-count.py --selftest
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0                       selftest_exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0                         EXIT=0
```
The owner also measured the F16 header-drop mutant (scratch copy, `source: S050` deleted): base bytes
`PASS F16 / entries=19 pass=19 exit=0`, landed bytes `problems=selection-not-declared-by-entry /
entries=19 pass=18 exit=1` — the reverse limb is load-bearing, not decorative. Selftest and mutant are
that seat's evidence (`.ufo/waves/round-34/wave1/ExecFrontierBidirectional.md` §3, §6); I record them
only as corroboration that the after-state I measured is on final bytes.

### 8. Digests (after-state, measured)

```
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md                       (after my append)
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
87b14892dfc42792056c7a9f09a0783e9d749d0478f376841c98bfc25e0a7c29  corpus/instruments/frontier-recheck-count.py   (uncommitted; in the working tree)
2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026  .ufo/waves/round-34/c2-controls/junk-f17.md   (committed at 29f606db)
```
`git ls-tree -r --name-only 29f606db -- .ufo/waves/round-34/c2-controls/` →
`.ufo/waves/round-34/c2-controls/before.txt`, `…/junk-checker.py`, `…/junk-f17.md` (the twin is
committed, as C1 requires).

### 9. Scratch + tooling

Scratch root `/fast/scratch/hyaku/kasegi-r34/ExecHarnessAfter/` held only fixtures (`ctl`, `ctl3`,
`ctlE`, `ctlF`, `junkman`) and output captures; removed with `rm -rf` before this receipt was
finalised — verified gone (`test -d` → exit 1). No tool installed or upgraded; every command above
is `python3` (system) plus git plumbing already in the lane. No git/jj mutation was performed; the
only working-tree writes are the README append and this receipt.

### 10. What the L1 must still do

1. Commit `corpus/README.md` (the 26-line append) together with the other C2 bytes; my run reads
   working-tree bytes, so a post-integration re-run at the committed tip is the record.
2. Do **not** add a second F17 row (control F shows `DUPLICATE-ENTRY` + `entries=2 pass=0 exit=1`).
3. If `corpus/instruments/frontier-recheck-count.py` changes after `87b14892…`, re-run the counter
   before quoting `entries=20 pass=20 exit=0`: that figure is pinned to that digest plus the README
   `876be9cc…`.

Report: .ufo/waves/round-34/wave1/ExecHarnessAfter.md
