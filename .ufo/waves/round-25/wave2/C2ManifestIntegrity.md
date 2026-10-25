# Round 25 wave 2 — C2 manifest integrity falsification

Seat: `L1Kasegi25.C2ManifestIntegrity` (reviewer, READ-ONLY). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Item attacked: **manifest schema, 5 pins,
quote uniqueness, all source-recheck invocations, corrupt-quote control** — i.e. the
`corpus/source-snapshots/round-25/manifest.json` produced in wave 1 and the recheck lines
that name it. No production file edited; no tool installed or upgraded (python3 / jq-free
stdlib only; pacman untouched per paused-transactions rule). One scratch receipt was
written and removed in the same session; nothing under `corpus/` was written.

## Verdict

**CONFIRMED — no defect found in the named item.** The committed manifest satisfies the
`source-recheck.py` contract, all five pins bind the committed snapshot bytes, all 39
quotes are unique under `normalize()`, both entries' `recheck:` invocations exit 0 from
the lane root and from a foreign cwd, and the corrupt-quote control fails closed with
exactly one `MISMATCH` and exit 1. The wave-1 summary in the context line
("manifest 5 sources/39 quotes, harness 12/12") is accurate as measured.

## Commands, outputs, exits

### 1. Schema

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 -m json.tool corpus/source-snapshots/round-25/manifest.json > /dev/null   # exit 0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json
# 44 lines: 5 "<id>:sha256 OK" + 39 "<id>:<qid> OK occurrences=1"   EXIT=0
```

- `schema_version` is the JSON integer `1` (`<class 'int'>`) — passes the type-strict gate
  at `source-recheck.py:56` (`type(...) is int`), not just the loose frontier-harness gate.
- Top level: `["schema_version","purpose","sources"]`; `sources` = 5 dicts, ids
  `S036,S037,S038,S039,S040`, each with non-empty relative `path` `S0NN.txt`, a 64-char
  lowercase `sha256`, and a non-empty `quotes` list (`manifest.json:2,6-8,53-55,90-92,
  132-134,184-186`).
- Quote ids: `Q1…Q8` (S036), `Q1…Q6` (S037), `Q1…Q7` (S038), `Q1…Q9` (S039), nine
  `cisco-*` ids (S040) — all match `ID_RE`, no duplicates within a source. Every quote is
  a non-empty string; minimum normalized length measured **16** chars (≥ 12 required at
  `source-recheck.py:129`).

Mutation probes against a byte-identical temp copy (exit codes captured without a pipe):

```
MUT d["schema_version"]=True   → exit 2  "manifest UNAVAILABLE reason=unsupported-schema"
MUT d["schema_version"]="1"    → exit 2  "manifest UNAVAILABLE reason=unsupported-schema"
MUT sources[1].id="S036"       → exit 2  "manifest UNAVAILABLE reason=duplicate-source-id"
MUT sources[2].quotes=[]       → exit 2  "S038:manifest UNAVAILABLE reason=missing-quotes"
MUT quotes[0].quote="short"    → exit 2  "S036:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence"
MUT path="/abs/S036.txt"       → exit 2  "S036:manifest UNAVAILABLE reason=invalid-path"
```

### 2. Five pins — manifest vs committed bytes vs capture log

`sha256sum corpus/source-snapshots/round-25/S0*.txt`:

```
022ca4f4…ceb950  S036.txt   == manifest == capture-log.txt:10 (status=200, snapshot_bytes=4815)
b204aa7f…473cb4  S037.txt   == manifest == capture-log.txt:11 (status=200, snapshot_bytes=11194)
09e077d3…abb68a  S038.txt   == manifest == capture-log.txt:12 (status=200, snapshot_bytes=3093)
657e7b4c…fc191d  S039.txt   == manifest == capture-log.txt:13 (status=200, snapshot_bytes=37126)
b7f7b55f…4e286c  S040.txt   == manifest == capture-log.txt:14 (status=200, snapshot_bytes=33463)
```

All five pins match the committed bytes AND the wave-1 capture log. `snapshot_bytes`
matches `ls -la` sizes (4815/11194/3093/37126/33463).

### 3. Quote uniqueness — recomputed independently

```
python3 -c '… N=lambda t:" ".join(re.sub("</?u>","",t).split()); count occurrences …'
# total_quotes=39 nonunique=none
```

Every quote occurs exactly once in its own snapshot under `normalize()` (receipt confirms
`occurrences=1` on all 39 lines). One quote —
`S040:cisco-jpcert-partner` — matches only through the declared normalization branch
(`OK normalized=markup-whitespace`, wrap at S040.txt:185-187 as documented in
RevManifestShape.md:97-101); the other 38 match byte-exact. No `anchor` fields are
present and none are needed (`occurrences ≤ 1`); `anchor=MISSING/BROKEN` grep of the
receipt → 0. Note (cosmetic): `S036:Q8`, `S038:Q6`, `S038:Q7` are strict substrings of
`S036:Q1`, `S038:Q1`, `S038:Q4` respectively — legal, verified unique, but redundant
assertion coverage, not a defect.

### 4. All source-recheck invocations

Two knowledge entries name the round-25 manifest; their `recheck:` lines executed
verbatim:

- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:8` — `--source S036,
  S037, S038, S039` → 30 OK lines, **exit 0**; covers all four header `source:` ids.
- `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:7` — `--source S040,
  S036, S038, S039` → 34 OK lines, **exit 0**; covers all four header ids.
- Union `S036–S040` == manifest id set exactly; no manifest id is left unchecked.
- Foreign-cwd: `cd / && bash -c "<recheck line subset --source S040>"` → exit 0 (the
  `cd /home/vgpnk/…/kasegi-shokunin &&` prefix pins cwd); naive bare
  `python3 corpus/instruments/source-recheck.py …` from `/` fails "can't open file",
  confirming the prefix is load-bearing (T13 holds).
- Round-23 manifest recheck: exit 0, 36 lines, 0 MISMATCH. Round-24: exit 0, 95 lines,
  0 MISMATCH — the new manifest did not disturb prior receipts.
- `frontier-recheck-count.py` (harness binding line→entry): **entries=12 pass=12 exit=0**,
  including both F10 rows.
- `recheck-audit.py` (C1 instrument, sha `c3c19adc…` matches frozen digest):
  **lines=37 total=37 pass=37 paths_fail=0 exit=0** — the `paths_fail=2` defect from
  wave-1 CritC2Ground §4.2 is resolved; the manifest now exists at the named path.
- `python3 corpus/instruments/source-recheck.py --selftest` → 4 PASS, exit 0.
- C2 counter verbatim: `frontier=10`; `entries-citing-new-rows` grep → **2**
  (`vendor-disclosure-policies-as-corpus-objects.md`, `vendor-disclosure-policy-
  commitments-crosswalk.md`); `sources-census.sh validate --root …/shokunin kasegi` →
  exit 0, `rows=40` (S036–S040 registered, `corpus/SOURCES.md:42-46`), only the two
  pre-existing W04s (S028, S029). F10 row present at `corpus/README.md:211`.

### 5. Corrupt-quote control

Temp copy of the five snapshots + manifest; appended ` ZZZ-CONTROL` to S037's first quote
(`grep -c ZZZ-CONTROL S0*.txt` → 0 in all five first):

```
python3 corpus/instruments/source-recheck.py --manifest $T/manifest.json
# S037:Q1 MISMATCH reason=quote-not-found  — exactly one MISMATCH, a :Q line not :sha256
# all 5 sha256 lines still OK
control-exit=1
```

Second control — corrupted bytes (`printf 'tampered\n' >> $T/S038.txt`):

```
# S038:sha256 MISMATCH expected=09e077d3… actual=9cc9309f…   (no S038 quote lines emitted)
control2-exit=1
```

Both controls behave exactly as `RevManifestShape.md §B(c)` specified, now measured on the
real lane-path manifest rather than the `/home/vgpnk/tmp/r25ref` reference it had to use.

## Residual risk / verification gaps

1. **Durability, not integrity**: `git status --porcelain` shows
   `corpus/source-snapshots/round-25/` (manifest + five .txt) and both new
   `corpus/knowledge/vendor-disclosure-*.md` files **untracked** in this lane worktree;
   round-23/24 snapshot dirs are tracked (`git ls-files`). The pins bind current disk
   bytes — a `git clean` or worktree loss would destroy every green receipt above. This is
   a wave-level/VCS gap outside my named item (the manifest itself verifies perfectly),
   but it is the one finding that can void the whole C2 evidence chain; flag to the
   integration owner.
2. **`.ufo/waves/round-25/` is untracked** too (contains claims.json, capture-log,
   receipts) — same class of risk, lower severity since it's wave bookkeeping.
3. `location:` fields remain free text (unread by instruments); the quote→claim binding is
   still human-checked only, matching RevManifestShape E2. Measured `location` values do
   carry real `S0NN.txt:LINE` anchors, including correct ones I spot-checked
   (S036:Q1→:19, S037:Q1→:109, S039:Q9→:557, S040 locations L57/L162/L300/L482-489).
4. Exit-code algebra unchanged: a `MISMATCH` can hide behind an `UNAVAILABLE` (T19). The
   receipt lines — not `$?` alone — are the evidence; all 44 were read verbatim above.

## Tool install/update record

None. Stdlib `python3`, `sha256sum`, `grep`, `awk`, `git` only; pacman paused and not
touched.
