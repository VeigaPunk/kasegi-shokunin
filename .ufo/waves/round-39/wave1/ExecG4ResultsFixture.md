# ExecG4ResultsFixture — G4' seat-identity fixtures (round 39)

- Seat: `ExecG4ResultsFixture` (leaf executor, lane `kasegi-shokunin`)
- Frozen item: C1 / G4 — "for every tracked `.ufo/waves/round-39/*-dispatch.json` in
  the export the sibling `-results.json` parses as JSON, lists exactly
  `len(taskCall.tasks)` seats with distinct agent ids (a zero-task dispatch is RED),
  and no duplicate identity satisfies the count"
- Status: complete. Deliverable is a fixture directory; no lane file outside
  `.ufo/waves/round-39/wave1/` was touched.
- Deliverable: `.ufo/waves/round-39/wave1/ExecG4ResultsFixture.fixtures/`
  (22 files, 20646 bytes, 9 fixture trees + 4 top-level files)

## 1. Root of the problem these fixtures close

The round-38 G4 limb compared only the results file's `seats` integer to
`len(taskCall.tasks)` (`corpus/instruments/r38-closure.sh:573-575`):

```
rseats=$(g4_json "$res" seats)
[ "$rseats" -eq "$rtasks" ] && seatsok=$((seatsok + 1))
```

That accepts a results file whose `results` array is empty, short, or full of
the same seat name, as long as `seats` says the right number. The round-39 frozen
rule replaces it with structural facts (`len(results)`, identity distinctness,
non-zero task count). The fixtures below pin exactly those facts, with a
reference checker as the executable statement of the rule.

## 2. Identity field — determined from real bytes (not guessed)

Commands (lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`):

```
$ jq -r 'to_entries[]|"\(.key) \(.value|type)"' \
    .ufo/waves/round-38/kasegi-r38-build-results.json
lane string / round number / wave string / seats number / results array

$ jq -r '[.results[]|keys_unsorted]|add|unique[]' \
    .ufo/waves/round-38/kasegi-r38-build-results.json
agent
name
note
output

$ jq -r '[.results[]|{name:(.name|type),agent:(.agent|type),output:(.output|type),note:(.note|type)}]
         |group_by(.)|map({k:.[0],n:length})|.[]|"\(.k|tojson) n=\(.n)"' \
    .ufo/waves/round-38/kasegi-r38-build-results.json
{"name":"string","agent":"string","output":"string","note":"null"} n=73

$ jq -r '[.results[]|select((.name//"")=="")]|length' \
    .ufo/waves/round-38/kasegi-r38-build-results.json
0

$ jq -r '[.results[].agent]|group_by(.)|map({a:.[0],n:length})|.[]|"\(.a) \(.n)"' \
    .ufo/waves/round-38/kasegi-r38-build-results.json
connector 3 / critic 7 / executor 21 / mutation-tester 6 / reviewer 11 /
scout 6 / scribe 15 / sentinel 2 / simplifier 2        (9 distinct values)

$ jq -r '.results|length' kasegi-r38-build-results.json ; jq '.seats' ...
73
73

$ jq -r '.taskCall.tasks[].name' .ufo/waves/round-38/wave1-dispatch.json | sort > disp.names
$ jq -r '.results[].name'        .ufo/waves/round-38/kasegi-r38-build-results.json | sort > res.names
$ diff disp.names res.names ; echo $?
0                       # identical sets, 73 distinct names each
```

Conclusion the suite author's parser must encode:

- **Identity field is `results[].name`.** It is the only string field with one
  distinct value per seat (73/73), and its set is exactly the dispatch name set.
- **`results[].agent` is the role, not the identity** (9 distinct values over 73
  seats). A literal reading of "distinct agent ids" as `agent` would make G4
  unsatisfiable on real data.
- There is no `id` key anywhere in the real dispatch or results documents.

## 3. Exact shapes (record for the suite author)

Round-38 dispatch `.ufo/waves/round-38/wave1-dispatch.json`
(round-39 `.ufo/waves/round-39/wave1-dispatch.json` is identical in shape):

```
top-level: schema=string, wave=string, policy=object, counts=object,
           registry=object, compaction=object, taskCall=object,
           resumeSends=array, note=string
taskCall:  {context, tasks}
tasks[]:   {name: string, agent: string, task: string}
r38: wave="kasegi-r38-build", len(tasks)=73, counts={"spawn":73,"resume":0,"total":73}
r39: wave="kasegi-r39-build", len(tasks)=49, counts={"spawn":49,"resume":0,"total":49}
```

Round-38 results `.ufo/waves/round-38/kasegi-r38-build-results.json`:

```
top-level: lane="kasegi", round=38, wave="kasegi-r38-build",
           seats=73, results=[73 items]
results[]: {name: string (non-empty), agent: string, output: string, note: null}
```

Pairing fact that matters on real bytes: the round-38 wave dir contains
`wave1-dispatch.json` and **no** `wave1-results.json`; the only results file is
`kasegi-r38-build-results.json`, whose `wave` equals the dispatch's `wave`.
A sibling-only resolver reads real exports as RED. The reference checker
resolves sibling first, then family `<wave>-results.json` in the same directory.

## 4. Payload grammar implemented and pinned by the expected lines

`check-g4.sh TREE` prints one line `G4 payload=<counters> closed=<0|1>` and exits
0/1; it writes nothing.

```
dispatches=D,pairs=P,parsed=J,tasks=T,entries=E,ids=U,ids-ok=I,read=ok|fail

D  number of `*-dispatch.json` files in .ufo/waves/round-39
P  dispatches whose results file was found (sibling, else family `<wave>-`)
J  pairs where both files are JSON and yield a `taskCall.tasks` list and a
   `results` list
T  sum of len(taskCall.tasks) over dispatch-parsed entries
E  sum of len(results) over results-parsed entries
U  sum of distinct non-empty string `name` values over the same entries
   (a row without one contributes nothing, so U < E in that case)
I  dispatches with: J, len(tasks) >= 1, len(results) == len(tasks),
   every row carries a non-empty string `name`, distinct names == len(results)
read  ok when the wave dir is a readable directory, else fail
closed=1 iff read=ok and D >= 1 and I == D
```

`-` is printed for a counter no parsed entry contributed to (E/U when no results
parsed, T when no dispatch parsed).

## 5. Required fixtures (a)–(f), frozen-rule mapping

All fixture trees are `TREE/.ufo/waves/round-39/g4fixture-dispatch.json` (+
`g4fixture-results.json` where the case has results). N=8, names `Seat01..Seat08`,
dispatch wave `g4fixture`.

Expected lines were authored from the rule before the checker was run against the
trees; the observed column is `bash run.sh` output, which compares string equality
and exit code, so `match=1` is a real assertion, not a transcription.

| # | case | how it violates/satisfies the rule | expected = observed line | rc |
|---|---|---|---|---|
| a | `a-distinct` | 8 tasks, 8 distinct names -> satisfies | `G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=8,ids-ok=1,read=ok closed=1` | 0 |
| b | `b-duplicate` | duplicate id fills count (entries 8, distinct 7) | `G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=7,ids-ok=0,read=ok closed=0` | 1 |
| c | `c-short` | N-1 entries (7 vs 8 tasks) | `G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=7,ids=7,ids-ok=0,read=ok closed=0` | 1 |
| d | `d-zero` | zero-task dispatch (N=0, results []) | `G4 payload=dispatches=1,pairs=1,parsed=1,tasks=0,entries=0,ids=0,ids-ok=0,read=ok closed=0` | 1 |
| e | `e-unparseable` | results file is truncated JSON | `G4 payload=dispatches=1,pairs=1,parsed=0,tasks=8,entries=-,ids=-,ids-ok=0,read=ok closed=0` | 1 |
| f | `f-missing` | results file absent | `G4 payload=dispatches=1,pairs=0,parsed=0,tasks=8,entries=-,ids=-,ids-ok=0,read=ok closed=0` | 1 |

`e-unparseable` results bytes (101 B, invalid JSON, verified `jq` exit non-zero):

```
{"lane": "kasegi", "round": 39, "wave": "g4fixture", "seats": 8, "results": [
 {
  "name": "Seat01",
```

`d-zero` dispatch: `"taskCall": {"context": ..., "tasks": []}` (8 lines, 140 B);
its results: `"seats": 0, "results": []` (7 lines, 87 B).

## 6. Controls beyond the six (composition and fail-closed edges)

| # | case | what it pins | expected = observed line | rc |
|---|---|---|---|---|
| g | `g-two-valid` | two dispatch/results pairs, both valid -> aggregate GREEN (`D=2,I=2`) | `G4 payload=dispatches=2,pairs=2,parsed=2,tasks=16,entries=16,ids=16,ids-ok=2,read=ok closed=1` | 0 |
| h | `h-nodir` | tree with no `.ufo/waves/round-39` at all -> fail-closed | `G4 payload=dispatches=0,pairs=0,parsed=0,tasks=-,entries=-,ids=-,ids-ok=0,read=fail closed=0` | 1 |
| i | `i-family` | results only at family `<wave>-results.json` (`g4fixture-build-results.json`), mirroring the real round-38 layout | `G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=8,ids-ok=1,read=ok closed=1` | 0 |

`h-nodir` carries a single `.keep` so the tree exists in git (an empty dir is not
committable). `g-two-valid` also proves the aggregate is an AND: breaking one of
its two pairs yields `ids-ok=1 ... closed=0` (probe P11).

Harness run over the delivered directory (from `/tmp`, absolute path):

```
$ bash /…/wave1/ExecG4ResultsFixture.fixtures/run.sh
case=a-distinct rc=0 match=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=8,ids-ok=1,read=ok closed=1
case=b-duplicate rc=1 match=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=7,ids-ok=0,read=ok closed=0
case=c-short rc=1 match=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=7,ids=7,ids-ok=0,read=ok closed=0
case=d-zero rc=1 match=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=0,entries=0,ids=0,ids-ok=0,read=ok closed=0
case=e-unparseable rc=1 match=1 G4 payload=dispatches=1,pairs=1,parsed=0,tasks=8,entries=-,ids=-,ids-ok=0,read=ok closed=0
case=f-missing rc=1 match=1 G4 payload=dispatches=1,pairs=0,parsed=0,tasks=8,entries=-,ids=-,ids-ok=0,read=ok closed=0
case=g-two-valid rc=0 match=1 G4 payload=dispatches=2,pairs=2,parsed=2,tasks=16,entries=16,ids=16,ids-ok=2,read=ok closed=1
case=h-nodir rc=1 match=1 G4 payload=dispatches=0,pairs=0,parsed=0,tasks=-,entries=-,ids=-,ids-ok=0,read=fail closed=0
case=i-family rc=0 match=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=8,ids-ok=1,read=ok closed=1
fixtures=9 failures=0
RUN_RC=0
```

## 7. Mutation probes (identity-shape hardening beyond the six)

Eleven mutations applied to copies of `a-distinct` (P11 to `g-two-valid`) in
scratch, each run through the same checker:

```
probe=P1-missing-name   rc=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=7,ids-ok=0,read=ok closed=0
probe=P2-empty-name     rc=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=7,ids-ok=0,read=ok closed=0
probe=P3-numeric-name   rc=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=7,ids-ok=0,read=ok closed=0
probe=P4-extra-seat     rc=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=9,ids=9,ids-ok=0,read=ok closed=0
probe=P5-results-key-gone rc=1 G4 payload=dispatches=1,pairs=1,parsed=0,tasks=8,entries=-,ids=-,ids-ok=0,read=ok closed=0
probe=P6-broken-dispatch  rc=1 G4 payload=dispatches=1,pairs=1,parsed=0,tasks=-,entries=8,ids=8,ids-ok=0,read=ok closed=0
probe=P7-whitespace-id  rc=0 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=8,ids-ok=1,read=ok closed=1
probe=P8-results-object rc=1 G4 payload=dispatches=1,pairs=1,parsed=0,tasks=8,entries=-,ids=-,ids-ok=0,read=ok closed=0
probe=P9-scalar-row    rc=1 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=8,entries=8,ids=7,ids-ok=0,read=ok closed=0
probe=P10-tasks-object  rc=1 G4 payload=dispatches=1,pairs=1,parsed=0,tasks=-,entries=8,ids=8,ids-ok=0,read=ok closed=0
probe=P11-two-dispatch-one-bad rc=1 G4 payload=dispatches=2,pairs=2,parsed=2,tasks=16,entries=16,ids=15,ids-ok=1,read=ok closed=0
```

P7 is deliberately GREEN: identity comparison is exact-string, with no trim or
case folding, so `" Seat08"` is a distinct seat id. That is the honest reading of
"distinct agent ids"; if the L1 wants normalization, the fixture set needs a
mutant that declares it.

## 8. Validation against real bytes

Real round-38 dispatch + real round-38 family results, parked under a scratch
tree's `.ufo/waves/round-39/` (so the same code path sees real 73-seat data):

```
$ cp .ufo/waves/round-38/wave1-dispatch.json           $T/.ufo/waves/round-39/
$ cp .ufo/waves/round-38/kasegi-r38-build-results.json $T/.ufo/waves/round-39/
real=r38-family  rc=0 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=73,entries=73,ids=73,ids-ok=1,read=ok closed=1
```

Real round-39 dispatch as it exists in the lane now (no results file committed
yet — this is the state the results-writing step must change):

```
real=r39-nopair  rc=1 G4 payload=dispatches=1,pairs=0,parsed=0,tasks=49,entries=-,ids=-,ids-ok=0,read=ok closed=0
```

Real round-39 dispatch + a synthetic results file carrying the real 49 dispatch
names in the real results shape (proves the pairing on round-39 bytes):

```
real=r39-synth   rc=0 G4 payload=dispatches=1,pairs=1,parsed=1,tasks=49,entries=49,ids=49,ids-ok=1,read=ok closed=1
```

`r39-synth` is a scratch artifact only; it is not delivered and must never be
mistaken for the round-39 results file.

## 9. Deliverable manifest

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39/wave1/ExecG4ResultsFixture.fixtures/`
— 22 files, 20646 bytes.

```
sha256                                                            lines  bytes  mode  path
62debdf59d01466dfee153531217c264d312fb52e584b7fbd5a3e0eb5bb1b50b    182   5766  755  check-g4.sh
c9c5e4b8c46f27f438a4fe892c51b0c21247f28edc3cadafcb9dec02cb1270df     36   1170  755  run.sh
d69da86abe80b8dcb1137ac7926dc1fa801af7eb124116bc3996878a1c5bb96c      7    721  644  expected.tsv
bb0538b33204ab7bb81fda2e6aeac31954ea924f9675debac440dafa08824538      4    402  644  expected-controls.tsv
2f274c00d1c533d17c6365736bd5655e92bec884cad0e5b33262d40e4e16013a     49    830  644  a-distinct/.ufo/waves/round-39/g4fixture-dispatch.json
78e868268d756cdce724c1ec9476b00f33f21c9c7a67e0f44a7b0c38dc338593     56    952  644  a-distinct/.ufo/waves/round-39/g4fixture-results.json
2f274c00d1c533d17c6365736bd5655e92bec884cad0e5b33262d40e4e16013a     49    830  644  b-duplicate/.ufo/waves/round-39/g4fixture-dispatch.json
26393446a2a2d1f32c72616b13646b803815664109d8de0a1bce2f7f81fb5851     56    952  644  b-duplicate/.ufo/waves/round-39/g4fixture-results.json
2f274c00d1c533d17c6365736bd5655e92bec884cad0e5b33262d40e4e16013a     49    830  644  c-short/.ufo/waves/round-39/g4fixture-dispatch.json
a7912b4b64899dfa8badf7b9a7c362ccd0b91b22ae06aebf807125be7caba878     50    845  644  c-short/.ufo/waves/round-39/g4fixture-results.json
8d6a674a7c97a996796a264f651d50747d677c39f8f9c41bf386b9826aea0a43      8    140  644  d-zero/.ufo/waves/round-39/g4fixture-dispatch.json
add9da2273ef2050da10b1b0780a964f0ddc1b43bc69a424d972034cc22901c9      7     87  644  d-zero/.ufo/waves/round-39/g4fixture-results.json
2f274c00d1c533d17c6365736bd5655e92bec884cad0e5b33262d40e4e16013a     49    830  644  e-unparseable/.ufo/waves/round-39/g4fixture-dispatch.json
2a6412b8fb88f77de3ab8eec3db5ec4937e1a02da374228dcb99a9208900fddf      3    101  644  e-unparseable/.ufo/waves/round-39/g4fixture-results.json
2f274c00d1c533d17c6365736bd5655e92bec884cad0e5b33262d40e4e16013a     49    830  644  f-missing/.ufo/waves/round-39/g4fixture-dispatch.json
2f274c00d1c533d17c6365736bd5655e92bec884cad0e5b33262d40e4e16013a     49    830  644  g-two-valid/.ufo/waves/round-39/g4fixture-dispatch.json
78e868268d756cdce724c1ec9476b00f33f21c9c7a67e0f44a7b0c38dc338593     56    952  644  g-two-valid/.ufo/waves/round-39/g4fixture-results.json
46a31c91186b0b4456cd14c2416cda5558836da901b93a6517f8a36b70fd52fa     49    831  644  g-two-valid/.ufo/waves/round-39/g4fixture2-dispatch.json
5d21c1a250d28a976bc416aa928aea45dc3a8fb721122f73ed2344c0647c53f8     56    953  644  g-two-valid/.ufo/waves/round-39/g4fixture2-results.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855      0      0  644  h-nodir/.keep
ba85bfad97c4a580b394a45a21cd92652e4ec236048166bb87f37e8bcae7f6d7     49    836  644  i-family/.ufo/waves/round-39/g4fixture-dispatch.json
2861a1768e84ebb9c1b90a6cd703b8587ee7bcb96ce0d39b49d8c50b37b02b3c     56    958  644  i-family/.ufo/waves/round-39/g4fixture-build-results.json
```

Every `.json` in the directory is `jq`-valid except
`e-unparseable/.ufo/waves/round-39/g4fixture-results.json`, which is invalid by
design. `check-g4.sh` and `run.sh` are pure readers: no chmod, no temp files, no
writes inside the deliverable.

## 10. Decisions the suite author inherits (and one wording risk)

1. **Identity = `results[].name`, compared exactly.** Documented in §2.
2. **Results resolution must include the family fallback.** Sibling
   `<base>-results.json`, else `<wave>-results.json` in the same directory. Real
   round-38 exports resolve only through the fallback (control `i-family`).
3. **Fail-closed edges added by the reference checker**: `read=fail` when
   `.ufo/waves/round-39` is missing/unreadable (control `h-nodir`), and
   `dispatches >= 1` (a tree with the dir but no `*-dispatch.json` is RED). The
   frozen sentence does not state the `>= 1` clause explicitly; it is carried over
   from round-38's `disp -ge 1` guard and closes the vacuity hole. If the L1 wants
   the literal vacuous-true reading, remove that clause and the `h-nodir`
   expectation changes with it.
4. **`seats` must not be used.** The round-38 limb trusted it; a results file can
   claim `seats` while its `results` array disagrees.
5. **A dispatch whose `taskCall.tasks` is not a list can never be GREEN** (P10).
6. **`parsed` counts only pairs where both sides parse**; `entries`/`ids` are
   still reported for a valid results file whose dispatch is broken (P6), so the
   payload distinguishes the two failure modes.

Residual risks:

- Round-39 reads `closed=0` today because no `-results.json` is committed in
  `.ufo/waves/round-39/` (§8 `r39-nopair`). G4 at the judged head depends on the
  results-writing step landing a parseable results file with 49 distinct names.
- The real round-39 results identity multiset is not yet observable; `r39-synth`
  proves the pairing, not the future file's content.
- If a wave legitimately resumes fewer seats than tasks, the frozen rule is still
  RED; no such case exists in round 38/39 (`spawn == total`).

## 11. Environment

- Scratch `S=/fast/scratch/hyaku/kasegi-r39/ExecG4ResultsFixture` held the build,
  the probe matrix and the real-bytes trees; removed at the end of this seat.
- Disk guard before the pass: `bash scripts/hyaku/disk-guard.sh status` -> exit 0,
  `/fast/scratch/hyaku` 24% used, 618.3G free.
- No packages installed, no tool upgrades, no LSP refactors (no symbol work was
  needed); no mutating git/jj command was run anywhere.
