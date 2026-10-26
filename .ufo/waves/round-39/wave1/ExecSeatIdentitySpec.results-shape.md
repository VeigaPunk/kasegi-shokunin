# Seat-identity shape of the kasegi `-results.json` files (G4' parse spec)

Read-only reference shapes: `.ufo/waves/round-37/kasegi-r37-build-results.json` (326389 B, sha256 `429035b9ca954eec14a9b7c58138b5efc18f0326b5a3aa5421d8fcddbda4bda7`) and `.ufo/waves/round-38/kasegi-r38-build-results.json` (361358 B, sha256 `611cab452930ade182f73d390cb6a0b8683e6cf27c9de4f40f217c095e6a4e53`).

## 1. Locating the pair

A dispatch file is `<dir>/<stem>-dispatch.json`; `taskCall` is at the top level of the same document (`d["taskCall"]["tasks"]`, a list of objects with keys `name`, `agent`, `task`). `d["wave"]` is the dispatcher wave name (round-39: `kasegi-r39-build`).

The results document lives in the **same directory** as its dispatch, under one of two observed names, resolved in this order:

1. `<d["wave"]>-results.json` — round-39 target: `.ufo/waves/round-39/kasegi-r39-build-results.json`. Used alone by rounds 30, 36, 37, 38; one of two in rounds 28, 29.
2. `<stem>-results.json` — round-39 fallback: `.ufo/waves/round-39/wave1-results.json`. Used alone by rounds 31 (waves 1-4), 33, 34, 35.

If neither exists in that directory, the file is unresolved and the check is RED (do not fall through to another round's directory, where same-named historical files would satisfy it). A third fallback — a single unique `*-results.json` beside the dispatch — is admissible only inside the round-39 directory.

Both names in rounds 28/29 carry the same 69/64 seat set, so either candidate is safe there; do not treat their co-existence as an error.

## 2. Count rule

```
n = len(d["taskCall"]["tasks"])
entries = r["results"]            # r = json.load(results file)
n == 0                     -> RED  (frozen rule: a zero-task dispatch is RED)
len(entries) != n           -> RED  (N-1 entries, or a pad entry, is RED)
```

A dispatch or results document that does not parse as JSON is RED: `json.load` raises and the caller maps that exception to RED, never to GREEN.

`len(entries)` is the authoritative entry count. The top-level `seats` integer mirrors it in every results file from rounds 28-38 but is not the source of truth. `d["counts"]["total"]` also equals `n` when present, but `counts` (with `policy`, `registry`, `compaction`) is absent in some dispatches (round 31 waves 3-4), so the parser may read only `taskCall.tasks`.

## 3. Identity field

The identity is the per-entry string field `name`:

```
identity(entry) = entry["name"]         # required, non-empty str
```

`name` is present and a non-empty string in every entry of every results file in the lane (rounds 28-38, all 12 dispatch/results pairs). It is the seat name, identical to the `name` of the dispatched task.

Fields that are **not** the identity:

- `id` — absent from the modern shape (0/73 in round 38, 0/64 in round 37). It appears only in the legacy `wave1-results.json` of rounds 28 and 29, where it is the run-instance id: `name` optionally suffixed with a retry counter (`ScoutDatawalk-2`, `ConnClaims-3`, 23 of 64 entries decorated in round 29). It is unique when present, but it is neither equal to the task name nor joinable to `taskCall.tasks`; it must not be required and must not be used for the count/uniqueness rule.
- `agent` — the role label (`executor`, `scribe`, `reviewer`, `critic`, `mutation-tester`, `connector`, `scout`, `sentinel`, `simplifier`). Round 38 carries 21 `executor` entries, so `agent` is never unique and MUST NOT be accepted as an identity value.
- `note`, `output` — provenance/payload, never identity (see §5, §6).

There is no `status` field and no `final output` field in any results file. The per-entry keyset is exactly `{name, agent, note, output}` in all 13 build/wave results files of rounds 28-38 (legacy rounds 28/29 `wave1-results.json` add `id`). The seat's final output is the `output` string.

## 4. Uniqueness rule

```
len({identity(e) for e in entries}) == len(entries) == n
```

Equivalently: identity values must be pairwise distinct, and their count must equal the dispatch task count. A missing `name`, an empty `name`, a non-string `name`, or a duplicate `name` is RED. When `id` is present it is also pairwise distinct in the observed files, but that is a derived property and is not part of the accept rule.

A stronger check — `set(names) == set(task names)` and entry order equal to task order — holds in all 12 resolved pairs (rounds 28-31, 33-38), but the frozen rule is count + distinctness only; do not gate on set equality or on order.

## 5. How a seat that died appears

A dead or lost seat keeps its entry: the count is never reduced and its identity is still present and unique. What changes is the payload:

```
entry["output"] == ""            # empty string, not null, not missing
entry["note"] == "orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat report file in the wave dir"
```

Observed in the partial-collection files: round 30 `kasegi-r30-build-results.json` 64/64 empty, round 31 `wave1-results.json` 38/38 empty, round 28 `kasegi-r28-build-results.json` 68/69 empty, round 29 `kasegi-r29-build-results.json` 63/64 empty. In every fully collected file `note` is null and no `output` is empty (rounds 28/29 `wave1-results.json`, rounds 31-38).

Therefore: an empty `output` is not a failed seat for the identity check — RED only on a missing identity, a duplicate identity, or a count mismatch. `note` may be null or an explanatory string and carries no identity.

## 6. Payload is opaque to the identity check

`output` is a JSON-encoded string, normally decoding to an object. It is not reliably decodable: in round 38, entry `ConnC1C2` has an `output` that decodes once to a string and whose inner text fails to decode (`JSONDecodeError` at char 4406, i.e. truncated). The identity check MUST NOT parse, require, or validate `output`.

## 7. Reference parser

```python
import json, os

def g4_identity_ok(dispatch_path):
    with open(dispatch_path) as f:
        d = json.load(f)
    tasks = d["taskCall"]["tasks"]
    n = len(tasks)
    if n == 0:
        return False, "RED zero-task dispatch"
    ddir = os.path.dirname(dispatch_path)
    cands = []
    if d.get("wave"):
        cands.append(os.path.join(ddir, d["wave"] + "-results.json"))
    stem = os.path.basename(dispatch_path)[:-len("-dispatch.json")]
    cands.append(os.path.join(ddir, stem + "-results.json"))
    path = next((p for p in cands if os.path.exists(p)), None)
    if path is None:
        return False, "RED results file missing"
    with open(path) as f:
        r = json.load(f)
    entries = r["results"]
    if len(entries) != n:
        return False, "RED entries=%d tasks=%d" % (len(entries), n)
    ids = []
    for e in entries:
        name = e.get("name") if isinstance(e, dict) else None
        if not isinstance(name, str) or not name:
            return False, "RED missing identity field"
        ids.append(name)
    if len(set(ids)) != len(ids):
        return False, "RED duplicate identity"
    return True, "entries=%d distinct=%d" % (len(ids), len(set(ids)))
```

Round-39 expectation at the judged head: one dispatch (`.ufo/waves/round-39/wave1-dispatch.json`, `wave` = `kasegi-r39-build`, 49 tasks) and one results document `kasegi-r39-build-results.json` with 49 entries and 49 distinct `name` values, printing `G4 entries=49 distinct=49`.
