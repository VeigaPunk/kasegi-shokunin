# Round 81 — lesson (kasegi, attempt 1)

Frozen claims: `.ufo/waves/round-81/claims.json` (freeze `7ad3118c86ee14fde433d73671cc407668533cec`, base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`). One v1 wave of **13 seats** — `ExecC1Battery`, `ExecC1RealTree`, `ExecC2Gate`, `ScribeLesson`, `ScoutDistinct`, `ReviewC1`, `ReviewC2`, `ReviewRouted`, `MutC1Hunt`, `MutCounter`, `MutEntryGate`, `CriticClaims`, `ConnectorOverlap` (counted from `.ufo/waves/round-81/w1-spec.json` `items`: 13). Receipts under `.ufo/waves/round-81/w1/`, executed controls under `.ufo/waves/round-81/controls/`.

Written by the scribe seat `ScribeLesson` while the wave runs; the L1 integrates it into `corpus/lessons/round-81.md` after WAVE-DONE and owns every verdict line. Three kinds of value appear below and are not interchangeable: *(measured this draft)* — re-measured by this seat with `sha256sum`, `git show`, `grep -n`, `awk` or `wc`; *control* — a pre-freeze run committed in the freeze commit, quoted from its file and **not re-run** by this seat; **PENDING-L1** — exists only as the claim's target, a landing-commit measurement, a live re-fetch, or an L1 verdict.

## Gate

### C1 — depth:verifiability — the recheck-cwd census successor (case-matched counter, 59-row battery)

In one sentence: the round-81 successor of the recheck-cwd census is killed on the case its row declares by all fifty-six non-neutral frozen mutants — including the twenty-eight round-80 routed survivors the landed r80 bytes let through — passes its three neutral rows, and leaves five stub forgeries that the round-80 counter scores `killed=56` each exiting 1 under the round-81 counter without the byte pin being read.

**Frozen bytes — sha256 re-measured this draft (`sha256sum` over the wave dir) and proved equal to the bytes at the freeze commit (`git show 7ad3118c:<path> | sha256sum`).**

| artifact | path | sha256 (measured, both copies) |
|---|---|---|
| candidate | `.ufo/waves/round-81/c1/recheck-cwd-census.py` | `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0` |
| counter | `.ufo/waves/round-81/c1/mutbat.py` | `fa96223b38f93b5fd9a08d11923dc7f7fe7f35a61b734c0cb3503381062843b4` |
| table | `.ufo/waves/round-81/c1/mutant-table.json` | `abcc834eb21102f11a11cc91b7482f68957f988ea91e68e803a82251a216d095` |
| builder | `.ufo/waves/round-81/c1/build-table.py` | `57ab70e9ff39d591ed98c2de60ee9323b735b981118b3f305ef40d3188f06a7f` |
| entry gate (C2) | `.ufo/waves/round-81/c2/entry-gate.py` | `51ee45fbd19f2efd84d107e35ebccdfd857900a5190e18d44534268c9a4d50d2` |
| forgery driver | `.ufo/waves/round-81/controls/c1-forgeries-r81.py` | `28fde3871e8fc7ead1f9f345dd39ea4779443c3f451003c997acf9cd48539246` |
| claims | `.ufo/waves/round-81/claims.json` | `604b788a31c197fd593614026236b6c3c365c6e7593158725aba5e874b430f40` |

The candidate, counter, table and builder shas are the four the claim pins; the entry-gate and forgery-driver shas are measured here because the claim freezes those bytes without pinning a hash. `git status --porcelain` lists no path under `.ufo/waves/round-81/` as modified, so every control below is the committed copy.

**Table composition (measured from the frozen JSON, `python3` over the list).** **59 rows**: `assertion`=55, `exception`=1 (`K-M3`), `neutral`=3 (`NT1 NT2 NT3`, no `kill_cases`). Twenty-eight rows are the r80 battery carried forward with `kill_cases` rewritten from its frozen `expect` prose — `K-M1 K-M2 K-M3 K-M4 K-M5 K-X1 K-X2a K-X2b K-M8 K-W1 K-W2 K-N1 K-P1 K-P2 K-G1 K-C1 K-NP K-CL K-T1 N10 N11 N21 N25 N26 N27 N30 T1 T2`. Twenty-eight are new — `M1` (ReviewC1 M1, `tmpdir-file`), `M2` (ReviewC1 M2, `timeout-bucket`), and `S01 S02 S04 S05 S37 S07 S19 S20 S21 S22 S08 S09 S10 S41 S40 S11 S12 S13 S14 S16 S15 S43 S25 S30 S31 S39` (MutC1Hunt survivors, spread over `prefix-literal`, `conform-limbs`, `output-lines`, `gate-predicates`, `tmpdir-unset`, `usage-guards`). Three are neutral. The kill-case vocabulary in file order: `gate-regs` (K-M1), `gate-negpolarity` (K-M2, T2), `gate-consume` (K-M3, K-X1), `gate-predicates` (18 rows), `gate-checkids` (5), `gate-wiring` (5), `prefix-census` (N21, N30), `tmpdir-refusal` (K-T1), `tmpdir-file` (M1), `tmpdir-unset` (S25), `timeout-bucket` (M2), `prefix-literal` (S01, S02), `conform-limbs` (S04, S05, S37), `output-lines` (S07, S19, S20, S21, S22), `usage-guards` (S30, S31, S39).

**Receipts that landed while this draft was being written (scratch-mirror runs; the lane's own bytes are still unswapped at draft time — instrument `420151fd…`, pins `cases=15` — so the *landing* values stay **PENDING-L1**).** `w1/ExecC1RealTree.md`: the P5 analogue prints `entries=95` (= `ls corpus/knowledge/*.md | wc -l`, 95, also measured in the real worktree), `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0 restoration_only=0`, `RECHECK-CWD-RESULT conformant`, rc 0; its P6 patch moves `selftest cases=15 failures=0` → `selftest cases=22 failures=0` inside the two pin rows and nothing else (`patch_rc=0`, `dryrun_rc=0`, post-patch anchored rows 1 each, `cases=22` 1 per file, `cases=15` 0 per file). `w1/ExecC2Gate.md`: B0 `S115:sha256 OK` + six `OK occurrences=1 anchor=<n>-ok` at 25,32,34,36,37,38; B3 `FRONTIER-CENSUS rows=57 admitted=57 closed=57 problem-rows=0 registry=115` and `FRONTIER-PASS F57 ids=S115`; B4 `records=95 bound=95 unbound=0`; B8 `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok` / `ENTRY-GATE-RESULT pass` in both the mirror and the landing form. These are receipt values: the L1 re-reads them in the final file.

**The eight predicates, one line each (from `claims.json`), with the status of each.**

- **P1** `TMPDIR=<scratch> python3 -B corpus/instruments/recheck-cwd-census.py --selftest` at the landing commit prints `selftest cases=22 failures=0`, exit 0. **Met on the frozen candidate** — control `c1-candidate-r81.txt` last block (`selftest cases=22 failures=0`, `rc=0`). Landing-commit re-run **PENDING-L1**; at draft time the worktree instrument is still the r80 one (`420151fd…5698`, measured).
- **P2** `sha256sum corpus/instruments/recheck-cwd-census.py` at the landing commit = `a3b58aa5…dbec0`. Frozen copy measured equal to the freeze-commit blob; the landed lane path is **PENDING-L1** (worktree still `420151fd…5698`).
- **P3** `… mutbat.py --target … --table … --expect-cases 22 --work <scratch>` prints a line ending `baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3` and exits 0. **Met on the frozen bytes** — control `c1-candidate-r81.txt`: `MUTBAT target_sha256=a3b58aa5… baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3` / `rc=0`, with all 56 `MUTANT … counted=yes` lines above it and the three `NT*` rows `NEUTRAL-OK`. Landing re-run **PENDING-L1**.
- **P4** `controls/c1-forgeries-r81.py` prints ten `FORGERY` lines; five `counter=r80` lines `killed=56 … rc=0`, five `counter=r81` lines `rc=1`. **Met** — control `c1-forgeries-r81.txt`, all ten lines quoted below (the repeated `target_sha256=` hex is abridged with `…`; nothing else is elided); driver exit `rc=0`.
- **P5** `RECHECK-CWD` over the landing tree prints `entries` = the `ls corpus/knowledge/*.md | wc -l` count with `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0 restoration_only=0`, then `conformant`, exit 0. Not run by this seat; **PENDING-L1** (`ExecC1RealTree` / L1). Note the count it must match is **95** at draft time (measured: the entry already sits in the worktree).
- **P6** the `SKILL.md` row matching `^\| recheck-cwd-census\.py \|` and the `corpus/instruments/README.md` row matching ``^\| `corpus/instruments/recheck-cwd-census.py` \|`` each carry `selftest cases=22 failures=0` and no `cases=15`. **Measured this draft, not yet met:** `SKILL.md:982` and `corpus/instruments/README.md:354` each read `cases22=no cases15=yes`. Landing state **PENDING-L1**.
- **P7** over `corpus/instruments/recheck-cwd-census.py`: `grep -c 'subprocess.run('` = 1, `grep -c '"bash", "-c"'` = 1, `grep -cE "[\"']/tmp"` = 0. **Met on the frozen candidate** — measured this draft, `1 / 1 / 0`. Landing re-run **PENDING-L1**.
- **P8** `mutbat.py --selftest` prints a line beginning `mutbat selftest ok` and exits 0, with `T-MIS` `MISKILLED counted=no`, `T-NEUBAD` `NEUTRAL-BROKEN`, and the location-forgery and baseline-FAIL toys each exiting 1. **Met** — control `c1-candidate-r81.txt` § counter selftest: `mutbat selftest ok got={'T-KILL': 'KILLED', 'T-MIS': 'MISKILLED', …, 'T-NEU': 'NEUTRAL-OK', 'T-NEUBAD': 'NEUTRAL-BROKEN'} counted={'T-KILL': 'yes', 'T-MIS': 'no', …, 'T-EXCA': 'no'} all_killed_exit=True location_forgery_exit=False baseline_forgery_exit=False bad_tables=[True, True, True]` / `rc=0`. Landing re-run **PENDING-L1**.

**The do-nothing floor (control `c1-donothing-r81.txt`, landed r80 bytes `420151fd` under the round-81 counter).**

```
MUTBAT target_sha256=420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698 baseline=bad rows=59 killed=28 survived=28 miskilled=0 dirty=0 notderived=0 neutral_ok=0/3
rc=1
```

The landed r80 bytes keep the 28 inherited kills — `M1 M2` and the 26 `S*` rows all `SURVIVED counted=no`, and the three neutrals `NEUTRAL-BROKEN` because the baseline cases line is missing (`baseline=bad`). The scored target is 56/56 with `neutral_ok=3/3`; the spread 28 → 56 is the round's measured move.

**The forgery table — `controls/c1-forgeries-r81.txt` quoted verbatim (ten lines).**

```
FORGERY F1-location counter=r80 forgery_sha256=bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6 rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=bc552edb… baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F1-location counter=r81 forgery_sha256=bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=bc552edb… baseline=ok rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=0/3
FORGERY F2-selfhash counter=r80 forgery_sha256=196d3ecf39f36eca189b7fffaec01e69e289bf0d956bd2d494ab8c90f207d266 rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=196d3ecf… baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F2-selfhash counter=r81 forgery_sha256=196d3ecf39f36eca189b7fffaec01e69e289bf0d956bd2d494ab8c90f207d266 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 2, "NEUTRAL-OK": 1} MUTBAT target_sha256=196d3ecf… baseline=ok rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=1/3
FORGERY F3-sibling counter=r80 forgery_sha256=c05fadc39828af64cc254046c94910f1fdba230b838d2c70cb24677942e0c502 rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=c05fadc3… baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F3-sibling counter=r81 forgery_sha256=c05fadc39828af64cc254046c94910f1fdba230b838d2c70cb24677942e0c502 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=c05fadc3… baseline=ok rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=0/3
FORGERY F4-baseline counter=r80 forgery_sha256=3dc3018124451ee11b90480f23b9e4821372fcdde4ecdad9d955426762044a9e rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=3dc30181… baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F4-baseline counter=r81 forgery_sha256=3dc3018124451ee11b90480f23b9e4821372fcdde4ecdad9d955426762044a9e rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=3dc30181… baseline=bad rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=0/3
FORGERY F5-allcases counter=r80 forgery_sha256=d60c17cbff3a587883885294076ea5b2baab1d69acc2acbeb32bda848807016d rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=d60c17cb… baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F5-allcases counter=r81 forgery_sha256=d60c17cbff3a587883885294076ea5b2baab1d69acc2acbeb32bda848807016d rc=1 verdicts={"KILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=d60c17cb… baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=0/3
rc=0
```

(The `target_sha256=` values are quoted full on the first `F1` line and elided with `…` on the repeats only; the file carries each full 64-hex hash on its own line.) Reading the table: `F1`–`F4` are rejected by the **kill tally** (`miskilled=56`), i.e. the counter refuses a forgery that fails cases its rows do not declare; `F4` is additionally caught by the **baseline limb** (`baseline=bad`). `F5` is the sharp case and must not be flattened into "the tally rejects every forgery": F5 reproduces the full 56-case kill set (`killed=56 miskilled=0`) and is rejected **only** by the neutral limb (`neutral_ok=0/3`). Under the round-80 counter all five are `killed=56 rc=0`, which is exactly the independence gap CriticClaims (a) routed at r80: the r81 counter's own limbs now separate them without reference to P2's byte pin.

**Two properties of the counter, measured from its source (lines cited and re-grepped in § Cite-check receipts).** (a) The kill is case-matched: `mutbat.py:82` `def verdict(rc, out, kill_cases)`, `:88` `on_target = [exc for case, exc in fails if case in kill_cases]`, `:90` `return "MISKILLED", fails`, `:113`-`:115` refuse a non-neutral row that `lacks kill_cases`, and `:169`/`:172` carry the summary line the predicates read. (b) The neutral limb is a separate branch (`:147`-`:154`): `:150` `tally["neutral_ok"] += 1`, `:152` names the row `NEUTRAL-OK` / `NEUTRAL-BROKEN`, and `:174` makes exit 0 require `tally["neutral_ok"] == n_neutral`. The r80 counter's rows=56 against the r81 table's 59 (visible in every `counter=r80` line) is the same fact from the other side: the r80 counter's source carries no `neutral` token at all (`grep -c -i neutral .ufo/waves/round-80/c1/mutbat.py` = 0, pasted above), so it never scores the neutral rows.

### C2 — coverage — Frontier F57, OSV.dev GET /v1experimental/importfindings/{source} (S115)

In one sentence: admit one entry, `corpus/knowledge/osv-importfindings-record-quality-feedback.md`, on the six pinned clauses of the S115 page, moving the frontier 56 → 57 and `corpus/knowledge` 94 → 95 while the S115 registry row moves `queued -> mined` and no other row changes.

**S115 access record.** URL `https://google.github.io/osv.dev/get-v1-importfindings/`; requested and final URL equal at HTTP 200 (`manifest.json` `http.status`/`http.final_url`); accessed 2026-11-06; `fetched_utc` 2026-11-06T20:11:18Z; raw page **16418 bytes** before tag stripping (manifest `fetch_method` text), capture `corpus/source-snapshots/round-81/S115.txt` — sha256 `e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f` *(measured)*, **44 lines, 2224 bytes** *(measured by `wc -l -c`)*; manifest `corpus/source-snapshots/round-81/manifest.json` — sha256 `7429df80bf425c8132b1325d0cd3b9e8527323f7e6eb61c31ce8b0774c5c05cf` *(measured; the claim does not pin the manifest hash but states it)*. Live re-open: **PENDING-L1** (this seat re-fetched nothing).

**The six located quotes (CORPUS rule 1 — a quote names its location), each ≤25 words.** Measured this draft by containment over the committed snapshot: each quote occurs **exactly once in the file and on its declared line**; word counts by `len(quote.split())`.

| clause | manifest pin | location | words | located quote |
|---|---|---|---|---|
| cl1 purpose | Q01-purpose | S115.txt:25 | 14 | "Given a specific OSV.dev source, report any records that are failing import-time quality checks." |
| cl2 audience | Q02-audience | S115.txt:32 | 12 | "It is targeted to operators of home databases that OSV.dev imports from." |
| cl3 not-imported consequence | Q03-not-imported | S115.txt:34 | 23 | "a machine-readable way to reason about records they have published that do not meet OSV.dev’s quality bar (and therefore have not been imported)." |
| cl4 single source parameter | Q04-only-parameter | S115.txt:36 | 18 | "The only parameter you need for this API call is the source, in order to construct the URL." |
| cl5 URL template | Q05-url-template | S115.txt:37 | 1 | "https://api.osv.dev/v1experimental/importfindings/{source}" |
| cl6 source.yaml name | Q06-source-yaml-name | S115.txt:38 | 12 | "The source value is the same as the name value in source.yaml" |

Each `anchor` in the manifest equals the measured line (`25 32 34 36 37 38`), and the pre-freeze control prints one `OK occurrences=1 anchor=<n>-ok` per pin at exactly those anchors. The entry's own claim table declares the same six word counts (14/12/23/18/1/12), so the entry and this measurement agree rather than agreeing with the manifest only.

**Admitted: these six clauses**, one pinned quote each, on the declared lines.

**Rejected, with reasons** — every rejected item is unpinned in the manifest, so no clause rests on it:

- **S115.txt:32, the status and feedback sentences** — the line reads "This API endpoint is still considered experimental. It is targeted to operators … We would value any and all feedback. …" (measured, verbatim start). Only the audience sentence is pinned; the status and feedback sentences are held ground: F51's Limits bullet already lists the experimental endpoints — `corpus/knowledge/osv-post-v1-query-contract.md:75` (measured by `grep -n`, pasted below). A status sentence is not a contract clause.
- **S115.txt:39, the case-sensitivity note** — "Case Sensitivity: API requests are case-sensitive. … use ‘ghsa’ instead of ‘GHSA’." (measured). Held by F51 `corpus/knowledge/osv-post-v1-query-contract.md:31`, which quotes the same sentence from S108.txt:53 (measured).
- **S115.txt:41, the request sample** — ``curl "https://api.osv.dev/v1experimental/importfindings/example"`` (measured). Sample data, not a rule; and the endpoint's own template is already clause cl5.
- **S115.txt:43, the example 200 response** — the `{"invalid_records":[…]}` JSON (measured). Sample data, not a rule; the finding-type vocabulary shown in it (`IMPORT_FINDING_TYPE_INVALID_JSON`) is not claimed.

**B0–B8 status.**

| predicate | status |
|---|---|
| B0 recheck | **control** `c2-prefreeze-r81.txt`: `S115:sha256 OK` + six `OK occurrences=1 anchor=<n>-ok`, `rc=0`. Landing re-run **PENDING-L1**. |
| B1 one registry row | **measured, uncommitted**: the S115 row (`corpus/SOURCES.md:127`) has 11 cells at the freeze and 11 in the worktree, and exactly two change — `[7] queued -> mined`, `[10] — -> corpus/knowledge/osv-importfindings-record-quality-feedback.md`; registry 115 at both. Landing diff **PENDING-L1**. |
| B2 94 -> 95 / expected list | **measured, uncommitted**: `ls corpus/knowledge/*.md \| wc -l` = 95; `knowledge-expected.txt` +1 line, the new entry, in sorted position. Landing **PENDING-L1**. |
| B3 frontier 56 -> 57 | freeze/do-nothing row from the control: `FRONTIER-CENSUS rows=56 admitted=56 closed=56 problem-rows=0 registry=115`; the landing census (`rows=57 … FRONTIER-PASS F57 ids=S115`) is **PENDING-L1** — not run by this seat. |
| B4 `unbound=0` | **PENDING-L1** (not run by this seat). |
| B5 entry `recheck:` runs from a foreign cwd | payload of the line verified by eye against B0's command; the foreign-cwd run is **PENDING-L1**. |
| B6 distinctness 0/6 | **control** `c2-prefreeze-r81.txt`: `files= 0` for each of the six quotes, `literal_total 0 knowledge_files 94`. Landing re-run **PENDING-L1**. |
| B7 census | **control** `census-start-r81.txt`: `kasegi ok …/corpus/SOURCES.md`, `rc=0`, the six inherited W04 warnings (`S028 S029 S072 S076 S080 S085`) and no new finding. Landing re-run **PENDING-L1**. |
| B8 entry gate | **control** `c2-prefreeze-r81.txt`: selftest `entry-gate selftest ok got={'good': True, 'dump': False, 'moved': False, 'norule': False}`; positive control over the admitted F56 entry `ENTRY-GATE sid=S114 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok` / `pass` / `rc=0`; junk control over `controls/c2-junk-entry-r81.md` `ENTRY-GATE sid=S115 claims=0 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=6 header=ok` / `fail` / `rc=1`. Run over the new entry **PENDING-L1**. |

The B8 pair is the round's new gate and it is a two-sided control: the positive run proves the gate passes a six-claim entry whose six quotes each sit on their pinned line, and the junk run (the same six quotes dumped without claim prose) proves it can fail — `claims=0` against `want=6` and `unpinned=6`.

**Distinctness.** F51 (S108) holds the single-query contract, the case-sensitivity rule (`:31`) and the experimental-endpoint listing (`:75`); F54 (S112) holds the batch contract; F55 (S113) and F56 (S114) hold the two pre-query experimental endpoints. All are consumer-side calls; importfindings is the publisher-side report on import failures. The control's literal sweep is 0 files over the 94 admitted entries for each of the six quotes, and the entry records `grep -rli 'importfindings' corpus/knowledge/` printing nothing and exiting 1 before the entry existed.

### Cite-check receipts (QUALITY R131) — every `path:line` this lesson cites, re-run and pasted

```
$ grep -n -F 'Given a specific OSV.dev source' corpus/source-snapshots/round-81/S115.txt
25:Given a specific OSV.dev source, report any records that are failing import-time quality checks.
$ grep -n -F 'It is targeted to operators' corpus/source-snapshots/round-81/S115.txt
32:This API endpoint is still considered experimental. It is targeted to operators of home databases that OSV.dev import
$ grep -n -F 'machine-readable way to reason' corpus/source-snapshots/round-81/S115.txt
34:The purpose of this endpoint is give OSV record providers (home database operators) a machine-readable way to reason
$ grep -n -F 'The only parameter you need' corpus/source-snapshots/round-81/S115.txt
36:The only parameter you need for this API call is the source, in order to construct the URL.
$ grep -n -F 'v1experimental/importfindings/{source}' corpus/source-snapshots/round-81/S115.txt
23:GET /v1experimental/importfindings/{source}
26:Table of contents GET /v1experimental/importfindings/{source} Experimental endpoint
37:https://api.osv.dev/v1experimental/importfindings/{source}
$ grep -n -F 'The source value is the same' corpus/source-snapshots/round-81/S115.txt
38:The source value is the same as the name value in source.yaml
$ grep -n -F 'Case Sensitivity' corpus/source-snapshots/round-81/S115.txt
39:Case Sensitivity: API requests are case-sensitive. Please ensure that you use the correct case for parameter names an
$ grep -n -F 'curl "https://api.osv.dev' corpus/source-snapshots/round-81/S115.txt
41:curl "https://api.osv.dev/v1experimental/importfindings/example"
$ grep -n -F 'invalid_records' corpus/source-snapshots/round-81/S115.txt
43:{"invalid_records":[{"bug_id":"EX-1234","source":"example","findings":["IMPORT_FINDING_TYPE_INVALID_JSON"],"first_see
$ grep -n 'experimental endpoints' corpus/knowledge/osv-post-v1-query-contract.md
75:- the other endpoints in the page's navigation (POST /v1/querybatch, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are listed, not described.
$ grep -n -i 'case-sensitiv' corpus/knowledge/osv-post-v1-query-contract.md
31:… Parameter names and values are case-sensitive: "Case Sensitivity: API requests are case-sensitive." (S108.txt:53).
$ grep -n guaranteed corpus/knowledge/osv-post-batch-query-contract.md
19:## Claim 2 — the response ordering is guaranteed to match the input
21:"The response ordering will be guaranteed to match the input." (S112.txt:24). …
73:| C3 ordering | Q03-ordering | S112.txt:24 | 10 | "The response ordering will be guaranteed to match the input." |
$ grep -n 'MISKILLED\|kill_cases\|neutral_ok' .ufo/waves/round-81/c1/mutbat.py
9:  case-matched kill  every non-neutral row declares `kill_cases`, the selftest case ids its
12:                     guard, an unrelated check) scores MISKILLED, not killed.
23:"kill_cases": [...] (non-neutral rows), "expect": prose}. The anchor must occur exactly once in
30:  MISKILLED       exit != 0, no 'Traceback', FAIL lines present but none on a kill case
36:survived=<s> miskilled=<m> dirty=<d> notderived=<x> neutral_ok=<o>/<t>'. Exit 0 iff the
82:def verdict(rc, out, kill_cases):
88:    on_target = [exc for case, exc in fails if case in kill_cases]
90:        return "MISKILLED", fails
113:            kc = row.get("kill_cases")
115:                return "row %s lacks kill_cases" % row["id"]
126:             "neutral_ok": 0}
150:                tally["neutral_ok"] += 1
155:        v, fails = verdict(rc, out, row["kill_cases"])
161:        elif v == "MISKILLED":
169:                 "dirty=%d notderived=%d neutral_ok=%d/%d"
172:                    tally["neutral_ok"], n_neutral))
174:          and tally["neutral_ok"] == n_neutral)
236:             "class": "assertion", "kill_cases": ["a"]},
238:             "class": "assertion", "kill_cases": ["a"]},
240:             "class": "assertion", "kill_cases": ["a"]},
242:             "kill_cases": ["a"]},
245:             "kill_cases": ["a"]},
248:             "kill_cases": ["a"]},
255:        want = {"T-KILL": "KILLED", "T-MIS": "MISKILLED", "T-SURV": "SURVIVED",
274:                                      "class": "bogus", "kill_cases": ["a"]}]),
280:               and "neutral_ok=0/1" in lines_loc[-1]
$ grep -n 'ENTRY-GATE\|claimless' .ufo/waves/round-81/c2/entry-gate.py
19:Output: 'ENTRY-GATE sid=<SID> claims=<c> want=<w> spans=<s> mislocated=<m> overlong=<o>
20:claimless=<k> unpinned=<u> header=<ok|bad>' then 'ENTRY-GATE-RESULT pass|fail'. Exit 0 on
54:    claimless = 0
62:            claimless += 1
65:          and claimless == 0 and unpinned == 0)
66:    line = ("ENTRY-GATE sid=%s claims=%d want=%d spans=%d mislocated=%d overlong=%d claimless=%d "
68:                                       overlong, claimless, unpinned, "ok" if header else "bad"))
146:    print("ENTRY-GATE-RESULT %s" % ("pass" if ok else "fail"))
$ grep -n '^| R13[01] ' corpus/QUALITY.md          # long cells elided with …
587:| R130 | Before the lane acts on a routed defect (a closure's or a seat's reason), it re-runs the command
588:| R131 | A `path:line` cite to code names the line that holds the cited token, checked by `grep -n '<token
$ awk 'NR>=147&&NR<=154{printf "%d:%s\n",NR,$0}' .ufo/waves/round-81/c1/mutbat.py
147:        if row["class"] == "neutral":
148:            ok_n = clean_pass(rc, out, expect_cases)
149:            if ok_n:
150:                tally["neutral_ok"] += 1
151:            lines.append("MUTANT %s verdict=%s rc=%d fails=%d failed_cases=%s counted=%s"
152:                         % (row["id"], "NEUTRAL-OK" if ok_n else "NEUTRAL-BROKEN", rc,
153:                            len(fail_lines(out)), failed, "yes" if ok_n else "no"))
154:            continue
$ grep -c -i neutral .ufo/waves/round-80/c1/mutbat.py
0
$ grep -n '^| S115 ' corpus/SOURCES.md          # long row elided with …
127:| S115 | OSV.dev API reference, GET /v1experimental/impo
```

Both greps are pasted in full, not sampled. Note `:155` reads `row["kill_cases"]` unconditionally on the non-neutral branch, and `:113`-`:115` (`validate_rows`) is what refuses a non-neutral row that lacks the key before any battery run: the neutral branch at `:147`-`:153` never reaches `verdict()`, which is why the r80 counter — which has no neutral branch — prints `rows=56` over this 59-row table.

The `:23`/`:26` hits for the URL template are the page's own headings and table-of-contents line, not a second copy of the template: the clause's quote sits on `:37`, the line after the Parameters sentence, which is where the entry puts it.

## Mistakes

### M81-1 — `criterion-landed-without-its-check-run`

R131 — *"A `path:line` cite to code names the line that holds the cited token, checked by `grep -n '<token>' <path>` at the cited revision before the cite lands"* (`corpus/QUALITY.md:588`) — **landed in round 80 together with the lesson that violates it**: at the r80 landing commit `0039d670`, `corpus/QUALITY.md` already carries the R131 row and `corpus/lessons/round-80.md` already cites `osv-post-batch-query-contract.md:19` for the ordering sentence that sits at `:21`. A criterion is not a check that ran.

**Evidence (run by this seat at freeze `7ad3118c`, output quoted).** Two facts, the criterion and the defect, at the same revision:

```
$ git show 0039d6708158f26655ee4fad2af4893a5f6c1cb7:corpus/QUALITY.md | grep -n '^| R131'
588:| R131 | A `path:line` cite to code names the line that holds the cited token, checked by `grep -n '<token>' <path>` at the cited revision before the cite lands. …
$ git show 0039d6708158f26655ee4fad2af4893a5f6c1cb7:corpus/lessons/round-80.md | grep -n 'batch-query-contract.md:19'
88:- **S114.txt:58, leading ordering clause** — … The rule-shape is held by F54 at `corpus/knowledge/osv-post-batch-query-contract.md:19` …
160:- **The unpinned lines and why**: … `:58` leading ordering clause (rule-shape held — `osv-post-batch-query-contract.md:19`) …
```

The cited file's `:19` is a heading, not the sentence:

```
$ sed -n '19p;21p' corpus/knowledge/osv-post-batch-query-contract.md
## Claim 2 — the response ordering is guaranteed to match the input
"The response ordering will be guaranteed to match the input." (S112.txt:24). The guarantee is stated on the page's own summary line, as a guarantee and not as an option (S112.txt:24).
$ grep -n 'guaranteed' corpus/knowledge/osv-post-batch-query-contract.md
19:## Claim 2 — the response ordering is guaranteed to match the input
21:"The response ordering will be guaranteed to match the input." (S112.txt:24). …
73:| C3 ordering | Q03-ordering | S112.txt:24 | 10 | "The response ordering will be guaranteed to match the input." |
```

Every `:19` site in the landed lesson, measured (`grep -n ':19' corpus/lessons/round-80.md`): `14` (the self-flag that names the error), `88`, `160`, `162` (`F54 holds the input-matched ordering rule-shape (:19, measured)`), `169` (`:58 ordering -> F54:19`). The round-80 spot-check's routed defect 1 (`corpus/lessons/round-80-verifier-spotcheck.md:101`) enumerates "three times (lines 88, 160, 162)"; the measured substantive set is four sites, `88 160 162 169` — the routed defect's own count is short by one, which is the same class of defect one level up.

**Captured-by: R131 (not executed at landing).** The criterion exists and its check was not run over the lesson that landed beside it. R130 (paste the output of the command a routed reason rests on) does not cover it: this cite was not a routed reason but the lesson's own prose.

**Fix.** A cite-check run over the lesson **before landing**, one shell command, shown able to fail on `:19` and pass on `:21`:

```
$ cite(){ p=${1%:*}; n=${1##*:}; t=$2; l=$(sed -n "${n}p" "$p"); if [ -z "$l" ]; then echo "FAIL $1 empty"; elif [ "${l#\#}" != "$l" ]; then echo "FAIL $1 is a heading: ${l:0:60}"; elif printf '%s' "$l" | grep -qF -- "$t"; then echo "PASS $1 holds '$t'"; else echo "FAIL $1 lacks '$t'"; fi; }
$ cite corpus/knowledge/osv-post-batch-query-contract.md:19 'The response ordering will be guaranteed'
FAIL corpus/knowledge/osv-post-batch-query-contract.md:19 is a heading: ## Claim 2 — the response ordering is guaranteed to match th
$ cite corpus/knowledge/osv-post-batch-query-contract.md:21 'The response ordering will be guaranteed'
PASS corpus/knowledge/osv-post-batch-query-contract.md:21 holds 'The response ordering will be guaranteed'
```

The token limb alone also fails `:19` and passes `:21` (heading text reads "is guaranteed to match", the sentence reads "will be guaranteed to match"), so the heading guard is a second, cheap limb rather than the only one:

```
$ for n in 19 21; do l=$(sed -n "${n}p" corpus/knowledge/osv-post-batch-query-contract.md); if printf '%s' "$l" | grep -qF 'The response ordering will be guaranteed'; then echo "line $n: PASS token present"; else echo "line $n: FAIL token absent -> ${l:0:70}"; fi; done
line 19: FAIL token absent -> ## Claim 2 — the response ordering is guaranteed to match the input
line 21: PASS token present
```

### M81-2 — `tally-prose-unbound-to-list`

`corpus/lessons/round-80.md:169` (the `Learning` bullet) says "**Six admits and four rejects**", while the `Gate` section's reject block — introduced at `:85` "**Rejected, with reasons** — all three are unpinned in the manifest" — holds **three** bullets (`:87` the `:33` status paragraph, `:88` the `:58` ordering clause, `:89` the payload skeleton and samples). The number in the prose was not derived from the list beside it, and nothing in the lane compared them.

**Evidence (run by this seat, output quoted).**

```
$ grep -n 'Six admits' corpus/lessons/round-80.md
169:- **Discernment.** Six admits and four rejects, and each reject names the held ground it would duplicate …
$ grep -n '^- \*\*S114.txt\|^- \*\*The payload skeleton' corpus/lessons/round-80.md
87:- **S114.txt:33** — the experimental-status paragraph: …
88:- **S114.txt:58, leading ordering clause** — …
89:- **The payload skeleton (`S114.txt:41-46`) and the samples (`S114.txt:48-72`)** — …
```

The reject block's own lead-in already said "all three", so the file contradicted itself at `:85` vs `:169` before any external check ran.

**Captured-by: none.** No criterion in `corpus/QUALITY.md` binds a tally sentence to the list it counts; R131 binds `path:line` cites, R130 binds a routed reason's command, and both were in force when `:169` landed.

**Fix — state the counting rule or derive the tallies by a command.** One-liner over the list, shown failing on the landed prose and passing after correction:

```
$ n=$(sed -n '/^\*\*Rejected, with reasons\*\*/,/^\*\*The S114 status change/p' corpus/lessons/round-80.md | grep -c '^- \*\*'); echo "derived_rejects=$n"
derived_rejects=3
$ if [ "$n" -eq 4 ]; then echo "PASS prose 'four rejects' bound to list"; else echo "FAIL prose says four rejects, list has $n"; fi
FAIL prose says four rejects, list has 3
$ if [ "$n" -eq 3 ]; then echo "PASS corrected 'three rejects' bound to list"; else echo "FAIL corrected count"; fi
PASS corrected 'three rejects' bound to list
$ echo -n 'derived_admits='; grep -c '^| cl[0-9]' corpus/lessons/round-80.md
derived_admits=6
```

So the admits half of the sentence is right (six `cl*` table rows) and the rejects half is off by one; the counting rule to state is "admits = `cl*` rows of the six-clause table; rejects = `- **` bullets of the reject block", each derived by the command above rather than counted by eye.

### Draft of the two appended corrections for `corpus/lessons/round-80.md` (never in place; not applied by this seat)

For the L1 to append after `:172`; this seat edited nothing.

```
## Appended corrections (round 81, 2026-11-06; never in place)

- **Correction to lines 88 and 160 (and the shorthand cites at 162 and 169) — F54 line cite.** The ordering
  sentence is at `corpus/knowledge/osv-post-batch-query-contract.md:21` ("The response ordering will be
  guaranteed to match the input." (S112.txt:24)), not `:19`, which is the section heading "## Claim 2 — the
  response ordering is guaranteed to match the input"; `grep -n guaranteed` prints 19, 21, 73. Re-run at the
  round-81 freeze `7ad3118c`; the `:19` cites were already in this file at its landing commit `0039d670`,
  the same commit that landed R131. Routed defect 1 of `corpus/lessons/round-80-verifier-spotcheck.md:101`;
  mined as M81-1 in `corpus/lessons/round-81.md`.

- **Correction to line 169 — reject tally.** "Six admits and four rejects" is six admits and **three**
  rejects: the `Gate` reject block introduced at `:85` holds three bullets (`:87` `:33` status, `:88` `:58`
  ordering, `:89` skeleton and samples). Derived, not counted by eye:
  `sed -n '/^\*\*Rejected, with reasons\*\*/,/^\*\*The S114 status change/p' corpus/lessons/round-80.md |
  grep -c '^- \*\*'` = 3, and `grep -c '^| cl[0-9]' corpus/lessons/round-80.md` = 6. Routed defect 2 of
  `corpus/lessons/round-80-verifier-spotcheck.md:102`; mined as M81-2 in `corpus/lessons/round-81.md`.
```

### Draft of one QUALITY row (next free id: `R132` — measured, `grep -n '^| R1[0-9][0-9]' corpus/QUALITY.md | tail -3` prints `581 R129`, `587 R130`, `588 R131`)

```
| R132 | A tally sentence in a lesson ("N admits and M rejects") is bound to the list it counts: each number is either derived by a command over that list and pasted beside it, or accompanied by its stated counting rule; a number the list contradicts is not landed. Check: run the derivation over the landed § Gate block and compare with the § Learning sentence. | `corpus/lessons/round-80.md` § Mistakes M81-2; `corpus/lessons/round-80.md:169` said "Six admits and four rejects" while the reject block at `:85`–`:89` held three bullets (`grep -c '^- \*\*'` over that block = 3) |
```

## Learning

- **Expansion.** F57 closes the OSV.dev experimental-endpoint lead list: importfindings is the publisher-side channel — why a record a home database published can be absent from OSV.dev (S115.txt:34) — and the page states the audience the other admitted OSV entries do not (S115.txt:32). The coverage map now holds all four experimental endpoints' contracts (F55 determineversion, F56 ubuntu binary-to-source, F57 importfindings) plus the two query contracts (F51, F54). Frontier 56 → 57, `corpus/knowledge` 94 → 95, one registry row, one expected-list line.
- **Quality.** The instrument move is measurable in the controls instead of asserted: the landed r80 bytes score 28/56 with `baseline=bad` and the three neutrals broken; the frozen candidate scores 56/56 with `neutral_ok=3/3`; the r80 counter scores all five forgeries `killed=56 rc=0` while the r81 counter rejects each of them (`miskilled=56` for F1–F4, `baseline=bad` for F4, `neutral_ok=0/3` for F5) without reading the byte pin. That is the r80 CriticClaims (a) gap answered at the counter's own level: the tally is now an independent limb.
- **Discernment.** Six admits and **four** rejects this round — counted the way M81-2's fix demands rather than by eye: admits = the six `cl*` rows of the entry's claim table, rejects = the four `- **` bullets of § C2's reject block (the `:32` status sentences, the `:39` case-sensitivity note, the `:41` request sample, the `:43` example response) — and each reject names the held ground or the reason it is not a rule. The sharpest cut is again a shared line: `:32` carries the audience sentence that is admitted and the status and feedback sentences that its single reject bullet refuses, so one line splits into one clause and one reject. The round's discernment defect is procedural, not substantive: both mistakes are the same shape — a number or a location asserted in prose that a one-line command settles.
- **Verifiability.** Two procedural lessons, both cheap, both caught only by a post-round spot-check, and both versions of the same failure: a criterion that landed without being run over the artifact it governs (M81-1: R131 and the `:19` cite arrived in the same commit), and a tally that was written rather than derived (M81-2: "four rejects" against a three-bullet list whose own lead-in said "three"). The structural lesson is the counter's new shape: a kill is now the *case* the row declares, not any FAIL (so an unrelated crash is `MISKILLED`), and the neutral rows make the tally reject a forgery that reproduces the whole kill set (F5). The boundary this leaves for r82 is the case-matched table's own construction: `kill_cases` is written by `build-table.py` from the r80 `expect` prose, so a row whose declared case is narrower than the transform's real effect can still be counted killed.

## Sources

- **S115 row, before and after.** Before (freeze commit `7ad3118c`, `corpus/SOURCES.md:127`, measured): 11 cells, status `queued`, used-by `—`, kind `docs`, tier `A`, access `2026-11-06`, retention `90d`; the anchor cell carries "importfindings page, lines 25-38; capture corpus/source-snapshots/round-81/S115.txt (sha256 e304eb88…6f7f, 44 lines, 2224 snapshot bytes, fetched 2026-11-06T20:11:18Z)" and the manifest path. After (worktree, measured, uncommitted): cells `[7] mined` and `[10] corpus/knowledge/osv-importfindings-record-quality-feedback.md`; the other nine cells identical. Landing commit and the one-row diff **PENDING-L1**.
- **Rows added: 1, tier A `docs`.** Registry 114 → 115 (the freeze commit already carries the queued row; the control prints `registry=115` at the freeze and `114 -> 115` is the round's addition per the SOURCES changelog line); `corpus/knowledge` 94 → 95; `knowledge-expected.txt` 96 → 97 lines. Landing values **PENDING-L1**; the worktree values (95 files, +1 expected line) are measured.
- **The six clauses admitted**, by pin and line: Q01-purpose (:25), Q02-audience (:32), Q03-not-imported (:34), Q04-only-parameter (:36), Q05-url-template (:37), Q06-source-yaml-name (:38). Quotes and word counts in the Gate table; each occurred exactly once at its declared line when measured this draft.
- **The four unpinned items and why**: `:32` status/feedback (held — F51 `:75`), `:39` case-sensitivity (held — F51 `:31`), `:41` request sample and `:43` example response (sample data, not rules).
- **Distinctness.** 0 of 94 admitted entries carry any of the six quotes literally (control `c2-prefreeze-r81.txt`); no entry carried `importfindings`, `source.yaml` or `home database` before this one (entry's own sweep, report-only).
- **Access record.** URL `https://google.github.io/osv.dev/get-v1-importfindings/`, HTTP 200, requested = final URL, raw page 16418 bytes, `fetched_utc` 2026-11-06T20:11:18Z (manifest); capture `corpus/source-snapshots/round-81/S115.txt` sha256 `e304eb88…6f7f`, 44 lines, 2224 bytes (measured). Live re-open **PENDING-L1**.

**PENDING-L1 values, collected:** P1/P3/P5/P6/P7/P8 re-runs at the landing commit; P2's landed sha (`a3b58aa5…`) and the instrument swap (worktree still `420151fd…` at draft time); the `cases=22` pin rows in `SKILL.md` and `corpus/instruments/README.md` (both `cases15=yes cases22=no` at draft time); B0–B8 at the landing commit (the one-row SOURCES diff, `FRONTIER-CENSUS rows=57 admitted=57 closed=57 registry=115`, `FRONTIER-PASS F57 ids=S115`, `unbound=0`, B8 over the new entry); the live page's HTTP status and raw byte count; the appended-corrections and R132 landings; the fleet report; and the L1 verdict lines (C1, C2) plus the landing commit itself.
