# ExecSeatIdentitySpec — results.json seat-identity shape for the r39 G4' parser

Item: analyze the real `*-results.json` shape so the r39 G4' parser is exact; deliver the parse spec and validate it against the real files.

Deliverable: `.ufo/waves/round-39/wave1/ExecSeatIdentitySpec.results-shape.md` — 113 lines, 7417 B, sha256 `0c67745f9495fca1efd907094ac45771bfc1754fe67871c0e0c659bb3041043b`. Spec text only (field paths, uniqueness rule, resolver, reference parser); all validation evidence is below, outside the deliverable.

## Files read (authoritative inputs, byte hashes)

```
round-38/kasegi-r38-build-results.json  361358 B  sha256 611cab452930ade182f73d390cb6a0b8683e6cf27c9de4f40f217c095e6a4e53
round-37/kasegi-r37-build-results.json  326389 B  sha256 429035b9ca954eec14a9b7c58138b5efc18f0326b5a3aa5421d8fcddbda4bda7
```

Both parsed fully (`json.load`), every entry inspected, plus the sibling dispatch documents and all 15 historical results files in `.ufo/waves/` (rounds 28-38). No git commands run (none needed; read-only reads only).

## Answers to the item's four questions

1. Per-seat entry keys — **not** `(name, agent, id, status, final output)`. The modern shape is exactly `['agent','name','note','output']` in all 13 build/wave results files of rounds 28-38; the legacy rounds 28/29 `wave1-results.json` use `['agent','id','name','output']`. **There is no `status` key and no `final output` key in any results file**; the seat's final output is the `output` string.
2. Identity field — `results[i].name` (required non-empty `str`). Present in every entry of every file: 73/73 (r38), 64/64 (r37), 0 missing/non-string across all 15 files.
3. `id` unique? — The `id` key is **absent** from the modern shape (0/73 r38, 0/64 r37, 0/64 r36). Where present (r28/r29 `wave1-results.json`) it is unique but it is the run-instance id: `name` plus an optional retry suffix (`ScoutDatawalk-2`, `ConnClaims-3`); 23/64 entries decorated in round 29, `id != name` for those 23, and every id still starts with its name. It must never be joined to `taskCall.tasks`.
   `agent` is the role label and never unique — r38: 21 executor, 15 scribe, 11 reviewer, 7 critic, 6 mutation-tester, 6 scout, 3 connector, 2 sentinel, 2 simplifier = **9 distinct values for 73 entries**. Accepting `agent` as identity (as the draft G4' wording "accept `id` or `agent` when unique" allows) is measurably wrong.
4. How a died seat appears — the entry is still present, name intact and unique; `output` is the **empty string** and `note` is the explanatory string `orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat report file in the wave dir`. Counts: r30 build-results 64/64 empty, r31 wave1 38/38 empty, r28 build-results 68/69 empty, r29 build-results 63/64 empty; every fully collected file has 0 empty outputs and `note: null`. A death never changes the entry count or the identity set.

## Cross-check: entries == `taskCall.tasks` length, distinct ids == entries

Resolved every dispatch in `.ufo/waves/` to its results sibling (precedence `<dispatch.wave>-results.json` then `<dispatch stem>-results.json`, same directory):

```
round/dispatch        N  resolved results file            entries distinct setEq order empt
round-28/wave1       69  kasegi-r28-build-results.json        69       69  True  True   68
round-28/wave1       69  wave1-results.json                   69       69  True  True    0
round-29/wave1       64  kasegi-r29-build-results.json        64       64  True  True   63
round-29/wave1       64  wave1-results.json                   64       64  True  True    0
round-30/wave1       64  kasegi-r30-build-results.json        64       64  True  True   64
round-31/wave1       38  wave1-results.json                   38       38  True  True   38
round-31/wave2       42  wave2-results.json                   42       42  True  True    0
round-31/wave3        5  wave3-results.json                    5        5  True  True    0
round-31/wave4        2  wave4-results.json                    2        2  True  True    0
round-33/wave1       64  wave1-results.json                   64       64  True  True    0
round-34/wave1       65  wave1-results.json                   65       65  True  True    0
round-35/wave1       64  wave1-results.json                   64       64  True  True    0
round-36/wave1       64  kasegi-r36-build-results.json        64       64  True  True    0
round-37/wave1       64  kasegi-r37-build-results.json        64       64  True  True    0
round-38/wave1       73  kasegi-r38-build-results.json        73       73  True  True    0
round-39/wave1       49  <none yet — results not written>      -        -     -     -    -
```

`entries == N == distinct(name)` holds in 15/15 resolved pairs; `set(names) == set(task names)` and entry order == task order also hold in all 15 (recorded as non-gating observations in the spec). Dispatch documents with **no** results sibling exist historically (rounds 23, 24, 25, 26, 32) — a resolver must stay scoped to the round-39 directory, or those become spurious REDs.

Round-39 dispatch facts measured: `wave = "kasegi-r39-build"`, `taskCall.tasks` = **49** items (keys `['agent','name','task']` only), `registry.members` = 49 keys identical to the task names, `counts = {'spawn': 49, 'resume': 0, 'total': 49}`. Expected results path: `.ufo/waves/round-39/kasegi-r39-build-results.json`; expected line `G4 entries=49 distinct=49`.

## Validation: the spec's own reference parser, extracted from the deliverable, executed

Parser extracted with `re.findall(r"```python\n(.*?)```", md, re.S)[0]` and `exec`'d — the bytes validated are the bytes shipped.

Real pair:
```
round-37/wave1-dispatch.json -> (True, 'entries=64 distinct=64')
round-38/wave1-dispatch.json -> (True, 'entries=73 distinct=73')
round-39/wave1-dispatch.json -> (False, 'RED results file missing')      # correct fail-closed state: round-39 results not written yet
```

Mutant matrix (synthetic round-39 dispatch copies + results variants in scratch; scratch removed):
```
a_n_distinct       (True,  'entries=49 distinct=49')
b_dup_name         (False, 'RED duplicate identity')
c_n_minus_1        (False, 'RED entries=48 tasks=49')
d_zero_tasks       (False, 'RED zero-task dispatch')
e_unparseable      (False, "RED unparseable (Expecting property name enclosed in double q)")   # json.load raises; caller maps to RED
f_missing_name     (False, 'RED missing identity field')
g_wave1_fallback   (True,  'entries=49 distinct=49')      # <stem>-results.json resolution branch
h_results_missing  (False, 'RED results file missing')
i_null_name        (False, 'RED missing identity field')
```

`agent`-as-identity counter-demo on the real file: `r38 entries=73 distinct_name=73 distinct_agent=9` — the `agent` branch of the draft wording yields a false RED on a healthy file.

## Risks / notes for the suite author

- The frozen G4' wording "accept `id` or `agent` when unique" is wrong for this corpus: `agent` collapses to 9 values over 73 entries, and `id` does not exist in the modern shape. The spec therefore fixes identity = `name`, with `id` tolerated-but-not-required and `agent` explicitly excluded. If the L1 keeps the literal wording, add `agent` only as a **last** resort guarded by distinctness — it will fail open→closed only on a healthy modern file, i.e. it will RED a good wave.
- Do not require `output` to parse: 1/73 r38 entries (`ConnC1C2`) has an `output` that decodes once to a `str` whose inner text fails `json.loads` (`JSONDecodeError` at char 4406, truncated payload).
- Do not gate on `set(names) == set(tasks)` or order, and do not read `counts`/`policy`/`registry`/`compaction` (absent in round 31 waves 3-4 dispatches).
- Round-39 currently has **no** results file (wave in flight). Any G4' run before the dispatcher emits `kasegi-r39-build-results.json` is correctly RED; that is the expected pre-results state, not a suite bug.

## Housekeeping

- Scratch `S=/fast/scratch/hyaku/kasegi-r39/ExecSeatIdentitySpec/` created with `mkdir -p`, all fixtures under `$S/fx/`, removed before yield (`rm -rf`, verified absent).
- Disk guard green before work: `/tmp 3% 125.2G, /var/tmp 35% 585.6G, /fast/scratch/hyaku 24% 610.6G`.
- No tools installed or upgraded; no pacman; no network fetches; no mutating git/jj; no writes outside the receipt, the deliverable and scratch.
