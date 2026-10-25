# RevManifestShape — the exact contract for `corpus/source-snapshots/round-25/manifest.json`

Seat: reviewer (READ-ONLY). Round 25, wave 1. Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
Written 2026-10-25. No lane file was modified; every command below was executed and its output
quoted verbatim.

## 0. Method and honesty boundary

Read in full: `corpus/instruments/source-recheck.py`, `capture-source.py`,
`frontier-recheck-count.py`, `recheck-audit.py`; `scripts/sources-census.sh` (header + mode table).
Read as data: `corpus/source-snapshots/round-24/manifest.json` (19 sources / 76 quotes),
`round-23/manifest.json` (4 sources / 32 quotes, one `anchor`), `.ufo/waves/round-25/capture-log.txt`,
`claims.json`, the two new entries
(`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`,
`vendor-disclosure-policy-commitments-crosswalk.md`).

Live state at the time of writing: `corpus/source-snapshots/round-25/` holds the five committed
snapshots `S036.txt … S040.txt` and **no `manifest.json`**. The two new entries' `recheck:` lines
already name that missing manifest, which is exactly why `recheck-audit.py` currently reports
`paths_fail=2`.

Because the lane manifest does not exist, checks that need one were run against a reference
manifest at `/home/vgpnk/tmp/r25ref/`: byte-identical copies of the five committed snapshots plus a
manifest carrying the real pins and six quotes drawn from the line ranges the entries themselves
cite. The commands in §B are written for the lane path; they were executed with that path
substituted, and the output shape below is the measured shape. This is stated wherever it matters.

---

## A. The schema, field by field

### A.1 File facts

| Property | Value | Enforced? |
|---|---|---|
| Path | `corpus/source-snapshots/round-25/manifest.json` | **Yes, indirectly** — the entries' `recheck:` lines name it, `frontier-recheck-count.py` joins `--root` + that name, and `recheck-audit.py` limb (c) fails if the named `corpus/…json` path is absent |
| Encoding | UTF-8 (decoded with `bytes.decode("utf-8")`) | **Yes** — `reason=unreadable-or-invalid` on failure |
| Resolution base | `Path(manifest).resolve(strict=True).parent` — every `path` is resolved against the manifest's **own directory** | **Yes** — a manifest outside the snapshot dir cannot reach the snapshots (`reason=outside-manifest-directory`) |
| Formatting | r24 precedent: `indent=2`, no trailing newline, `purpose` first prose | No |

### A.2 Top level

| Key | Checker reads it? | Rule (from the code) | Violation |
|---|---|---|---|
| `schema_version` | **READ** | `type(data["schema_version"]) is int` **and** `== 1` | `manifest UNAVAILABLE reason=unsupported-schema`, exit 2 |
| `sources` | **READ** | non-empty `list` of `dict` | `manifest UNAVAILABLE reason=missing-sources`, exit 2 |
| `purpose` | **IGNORED** | free prose | — |

`schema_version` is type-strict: `true`, `1.0` and `"1"` are all rejected. Measured:

```
bool-true  recheck-exit=2 first-line=manifest UNAVAILABLE reason=unsupported-schema
float-1.0  recheck-exit=2 first-line=manifest UNAVAILABLE reason=unsupported-schema
string-1   recheck-exit=2 first-line=manifest UNAVAILABLE reason=unsupported-schema
```

The second reader (`frontier-recheck-count.py`) is **looser** — `data.get("schema_version") != 1` —
so `true` and `1.0` pass *its* gate and fail only when it executes the line
(`problems=recheck-exit-2`). Emit the integer `1`; do not rely on the loose gate.

### A.3 Source record (`sources[i]`)

| Key | Checker reads it? | Rule | Violation |
|---|---|---|---|
| `id` | **READ** | `ID_RE = [A-Za-z0-9][A-Za-z0-9._-]*\Z`, `fullmatch`; unique across the manifest | `manifest:record-<N> UNAVAILABLE reason=invalid-source-id` / `manifest UNAVAILABLE reason=duplicate-source-id` (whole manifest aborts), exit 2 |
| `path` | **READ** | `str`, non-empty, **not absolute**; `(base / path).resolve(strict=True)`; `os.path.commonpath((base, resolved)) == base` | `reason=invalid-path` (line `<id>:manifest`) / `reason=outside-manifest-directory` / `reason=missing` / `reason=unreadable`, exit 2 |
| `sha256` | **READ** | `SHA256_RE = [0-9a-f]{64}\Z` — exactly 64 lowercase hex | `reason=invalid-sha256`, exit 2; a well-formed but wrong pin → `<id>:sha256 MISMATCH expected=<hex> actual=<hex>`, exit 1 |
| `quotes` | **READ** | non-empty `list` of `dict` | `reason=missing-quotes`, exit 2 |
| any other key | **IGNORED** | — | — |

### A.4 Quote record (`sources[i].quotes[j]`)

| Key | Checker reads it? | Rule | Violation |
|---|---|---|---|
| `id` | **READ** | `ID_RE`, unique **within its source**; printed verbatim in the receipt line | `reason=invalid-quote-id` (line `<id>:quote-<N>`) / `reason=duplicate-quote-id` (line `<id>:manifest`), exit 2 |
| `quote` | **READ** | non-empty `str`; `len(normalize(quote)) >= 12` (`MIN_QUOTE_CHARS`) | `reason=empty-quote` / `reason=quote-too-short-to-be-evidence`, exit 2 |
| `anchor` | **READ** (optional) | `type(anchor) is int`, `1 <= anchor <= len(raw_lines)`; window `" ".join(raw_lines[anchor-1:anchor+3])`, normalized; must contain the normalized quote | note only — `anchor=MISSING` / `OUT-OF-RANGE` / `<N>-BROKEN`. **Never changes the exit code** |
| `location` | **IGNORED** | r24 carries it as documentation | — |

### A.5 Matching and normalization (exact)

```python
MARKUP_RE = re.compile(r"</?u>")
normalize = lambda t: " ".join(MARKUP_RE.sub("", t).split())   # strip <u>/</u>, collapse ALL whitespace
```

Per assertion, in `sorted(quotes, key=id)` order:

1. `occurrences = normalize(source_text).count(normalize(quote))` — non-overlapping count over the
   whole snapshot.
2. If `quote in source_text` (raw, byte-exact) → `OK occurrences=<N>`.
3. elif `occurrences` → `OK normalized=markup-whitespace occurrences=<N>`.
4. else → `MISMATCH reason=quote-not-found`, status 1.

Because `str.split()` treats U+202F (narrow no-break space, which `capture-source.py` leaves in the
bytes) as whitespace, a quote copied across a wrapped line with an ordinary space matches on branch 3.
Measured on the real S040 bytes (lines 185–187 joined by spaces):

```
S040:Q1 OK normalized=markup-whitespace occurrences=1
```

### A.6 Receipt grammar and exit algebra

Line form: `f"{stable_id} {status}"` + `" " + detail` when a detail exists. Records are emitted in
`sorted(id)` order; quotes in `sorted(quote id)` order (lexicographic, so `Q10` precedes `Q2`).

```
status = 0
for record in sorted(records, key=id):
    r = check_source(...)
    if r == 2: status = 2
    elif r == 1 and status == 0: status = 1
```

Exit codes: **0** every assertion holds · **1** at least one `MISMATCH` and no `UNAVAILABLE` ·
**2** any `UNAVAILABLE` (dominates 1 regardless of order — measured: a quote MISMATCH on S036 plus a
missing S040 file exits 2). A manifest-load failure aborts with 2 and emits no per-source lines. A
per-source structural failure aborts that source only (other sources are still checked); a `sha256`
mismatch returns 1 *before* the quotes, so that source emits no quote lines.

Complete inventory of emitted lines (all measured):

| Line | Exit |
|---|---|
| `manifest UNAVAILABLE reason=missing` / `unreadable-or-invalid` / `unsupported-schema` / `missing-sources` / `duplicate-source-id` | 2 |
| `manifest UNAVAILABLE reason=missing-required-argument` (no `--manifest`) | 2 |
| `manifest:selection UNAVAILABLE reason=invalid-source-id` (bad `--source` shape) | 2 |
| `manifest:selection UNAVAILABLE reason=selftest-takes-no-manifest-or-source` | 2 |
| `manifest:record-<N> UNAVAILABLE reason=invalid-source-id` | 2 |
| `<id>:manifest UNAVAILABLE reason=invalid-path` / `invalid-sha256` / `missing-quotes` / `duplicate-quote-id` | 2 |
| `<id>:quote-<N> UNAVAILABLE reason=invalid-quote-id` | 2 |
| `<id>:<qid> UNAVAILABLE reason=empty-quote` / `quote-too-short-to-be-evidence` | 2 |
| `<id>:source UNAVAILABLE reason=missing` / `unreadable` / `not-utf8` / `outside-manifest-directory` | 2 |
| `<id>:source UNAVAILABLE reason=not-listed` (`--source` id absent from the manifest) | 2 |
| `<id>:sha256 MISMATCH expected=<hex> actual=<hex>` | 1 |
| `<id>:<qid> MISMATCH reason=quote-not-found` | 1 |
| `<id>:sha256 OK` | 0 |
| `<id>:<qid> OK occurrences=<N>[ anchor=…]` / `OK normalized=markup-whitespace occurrences=<N>[ anchor=…]` | 0 |

### A.7 Which reader reads what

| Reader | Fields it actually reads | Fields it ignores |
|---|---|---|
| `source-recheck.py` | `schema_version`, `sources[].id`, `.path`, `.sha256`, `.quotes[].id`, `.quote`, `.anchor` | `purpose`, `quotes[].location`, every other key; the *value* of `path` beyond "relative, inside the manifest dir, exists" — it is **never compared to `id`** |
| `frontier-recheck-count.py` | `schema_version` (loose `!= 1`), `sources[].id` only | `path`, `sha256`, `quotes` entirely |
| `recheck-audit.py` | nothing inside the file — only that the `corpus/…json` path named on the recheck line exists | all fields |
| `scripts/sources-census.sh validate` | nothing inside the file — the id must be a registered `corpus/SOURCES.md` row (E02/E03/E11) | all fields |

### A.8 Ready skeleton (real pins, verified with `sha256sum` and against `capture-log.txt`)

`__QUOTE__`/`__LOCATION__` are the scribes' choices; everything else is fixed by the contract.

```json
{
  "schema_version": 1,
  "purpose": "Round-25 captured-source assertions for the F10 vendor-disclosure admissions (S036-S040), captured 2026-10-25T08:14Z by corpus/instruments/capture-source.py.",
  "sources": [
    {"id": "S036", "path": "S036.txt",
     "sha256": "022ca4f40b9e07a4e052c4d6ac8a9b4195503489417eb7fd0760d28c35ceb950",
     "quotes": [{"id": "Q1", "quote": "__QUOTE__", "location": "__LOCATION__"}]},
    {"id": "S037", "path": "S037.txt",
     "sha256": "b204aa7f60ec2e70713ecd8c605fb1adb6e39549f0ef09d32a297c10f473cb4c",
     "quotes": [{"id": "Q1", "quote": "__QUOTE__", "location": "__LOCATION__"}]},
    {"id": "S038", "path": "S038.txt",
     "sha256": "09e077d31ce3b5e366fa435f5c474db7405eef8dd313b64be46f88047dabb68a",
     "quotes": [{"id": "Q1", "quote": "__QUOTE__", "location": "__LOCATION__"}]},
    {"id": "S039", "path": "S039.txt",
     "sha256": "657e7b4c67e67d00b190b31942d749a28d0988f15d1e6f5f506130accffc191d",
     "quotes": [{"id": "Q1", "quote": "__QUOTE__", "location": "__LOCATION__"}]},
    {"id": "S040", "path": "S040.txt",
     "sha256": "b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c",
     "quotes": [{"id": "Q1", "quote": "__QUOTE__", "location": "__LOCATION__"}]}
  ]
}
```

**All five ids are mandatory.** Entry A declares `S036, S037, S038, S039`; entry B declares
`S040, S036, S038, S039`; the harness requires each entry's `--source` set to be a **superset of its
header ids** and a **subset of the manifest ids**, so the union — exactly `S036–S040` — must be
listed. Dropping any one id fails that entry with `problems=manifest-missing-ids` (measured on a
fixture root).

---

## B. The four checks — exact commands and expected output

Run all of them **from the lane root** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

### (a) Build check — the manifest is well-formed and pinned to the committed bytes

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 -m json.tool corpus/source-snapshots/round-25/manifest.json > /dev/null; echo "exit=$?"
```

Expected: no output, `exit=0`.

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 -c "import json,hashlib,re,pathlib,sys;M=re.compile(r'</?u>');N=lambda t:' '.join(M.sub('',t).split());D=json.load(open('corpus/source-snapshots/round-25/manifest.json'));B=pathlib.Path('corpus/source-snapshots/round-25');S=D['sources'];pins=[(s['id'],s['path'],hashlib.sha256((B/s['path']).read_bytes()).hexdigest()==s['sha256']) for s in S];occ=[(s['id'],q['id'],N((B/s['path']).read_text(encoding='utf-8')).count(N(q['quote']))) for s in S for q in s['quotes']];print('schema=%r sources=%d'%(D['schema_version'],len(S)));print('pins',' '.join('%s=%s'%(i,'ok' if p else 'BAD') for i,p,_ in pins));print('quotes=%d nonunique=%s'%(len(occ),[o for o in occ if o[2]!=1] or 'none'));sys.exit(0 if all(p[2] for p in pins) and all(o[2]>=1 for o in occ) else 1)"
```

Expected on the reference manifest (measured):

```
schema=1 sources=5
pins S036=ok S037=ok S038=ok S039=ok S040=ok
quotes=6 nonunique=[('S040', 'Q2', 4)]
exit=0
```

`nonunique=none` is the value to aim for: every quote exactly-once under `normalize()`, so no
`anchor` is required (r24 shipped 76/76 that way). A non-unique entry in that list is legal but
**must** carry an `anchor` in the manifest (see T5).

Third, the ids must be registered rows (`corpus/SOURCES.md` currently ends at `S035`):

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 -c "import json,re;m={s['id'] for s in json.load(open('corpus/source-snapshots/round-25/manifest.json'))['sources']};r=set(re.findall(r'^\| (S\d{3,}) ',open('corpus/SOURCES.md').read(),re.M));print('unregistered=',sorted(m-r) or 'none')"
```

Expected: `unregistered= none`. (Command shape verified against the round-24 manifest, which scores
`unregistered= none`; no instrument checks this, so it is the L1's manual gate.)

### (b) Every entry's `recheck:` line exits 0

Primary counter — binds each line to its own entry before running it:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/frontier-recheck-count.py --json .ufo/waves/round-25/frontier-after.json
```

Current measured output (F10 row not yet admitted, 10 entries from F01–F09):

```
entries=10 pass=10 exit=0
```

Once the F10 row is admitted with both entries, expect **12** lines of the form

```
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
entries=12 pass=12 exit=0
```

and exit 0. (The 12 is arithmetic from the measured harness: one line per `(frontier row, entry in
the entry cell)` pair; F10 contributes two.)

Per-source, the five lines the entries actually run:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for s in S036 S037 S038 S039 S040; do
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source "$s"; echo "exit($s)=$?"
done
```

Expected per source, two lines and exit 0 (measured against the reference):

```
S036:sha256 OK
S036:Q1 OK occurrences=1
exit(S036)=0
```

C1 limb (b)+(c) — cwd invariance and path existence, i.e. what makes those lines *auditable*:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json
```

Measured **now** (manifest absent):

```
strict pass=35 cdroot_fail=0 instrument_fail=0 artifact_fail=0 own_fail=0
lines=37 pass=35 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=2 exit=1
```

After the manifest lands, the two `paths_fail` entries flip and the expected shape is
`paths_fail=0 exit=0`. **`lines=` will read 37, not the frozen 35** — see §D1.

### (c) Control that must FAIL — a corrupted quote

Builds a throwaway copy of the five snapshots plus a manifest whose **S037 first quote** carries a
sentinel that cannot occur in any snapshot (verified: `grep -c 'ZZZ-CONTROL' S0*.txt` → 0 in all
five), then requires exit 1 with exactly one `MISMATCH`.

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
T=$(mktemp -d -p /home/vgpnk/tmp) && cp corpus/source-snapshots/round-25/S0*.txt "$T"/ &&
python3 -c "import json,sys;d=json.load(open('corpus/source-snapshots/round-25/manifest.json'));q=d['sources'][1]['quotes'][0];q['quote']=q['quote']+' ZZZ-CONTROL';json.dump(d,open(sys.argv[1]+'/manifest.json','w'),ensure_ascii=False)" "$T" &&
python3 corpus/instruments/source-recheck.py --manifest "$T/manifest.json"; echo "control-exit=$?"; rm -rf "$T"
```

Measured (against the reference manifest, same five snapshot bytes):

```
S036:sha256 OK
S036:Q1 OK occurrences=1
S037:sha256 OK
S037:Q1 MISMATCH reason=quote-not-found
S038:sha256 OK
S038:Q1 OK occurrences=1
S039:sha256 OK
S039:Q1 OK occurrences=1
S040:sha256 OK
S040:Q1 OK normalized=markup-whitespace occurrences=1
S040:Q2 OK occurrences=4 anchor=56-ok
control-exit=1
```

Pass condition: `control-exit=1`, exactly **one** `MISMATCH` line, and it is a `:Q…` line — never a
`:sha256` line (that would mean the copy, not the quote, was corrupted). Every `sha256` line must
still read `OK`.

Second control, one level up — corrupt the **bytes** and confirm the pin is what fires:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
T=$(mktemp -d -p /home/vgpnk/tmp) && cp corpus/source-snapshots/round-25/S0*.txt "$T"/ &&
cp corpus/source-snapshots/round-25/manifest.json "$T"/ &&
printf 'tampered\n' >> "$T/S038.txt" &&
python3 corpus/instruments/source-recheck.py --manifest "$T/manifest.json"; echo "control-exit=$?"; rm -rf "$T"
```

Expected: `<id>:sha256 MISMATCH expected=<pinned> actual=<new>` on the S038 line only, **no S038
quote lines** (the sha256 check returns before the quotes), `control-exit=1`.

### (d) Selftests

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/source-recheck.py --selftest; echo "exit=$?"
```

Measured:

```
SELFTEST clean PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
exit=0
```

`--selftest` takes **no** `--manifest`/`--source`; combining them exits 2 with
`manifest:selection UNAVAILABLE reason=selftest-takes-no-manifest-or-source` (measured).

Producer selftest (the instrument that made the five snapshots):

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/capture-source.py --selftest; echo "exit=$?"
```

Measured: `selftest normalize=ok deterministic=ok`, `exit=0`.

Auditor selftest (only if the C1 line forms were touched):

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py --selftest; echo "exit=$?"
```

Measured: 11 per-case `ok` lines, then
`selftest completeness lines=11 total=13 complete=False ok` and
`selftest cases=12 failures=0 exit=0`, exit 0.

---

## C. Traps

Each is measured, not inferred.

**T1 — `path` is never bound to `id`.** Renaming `S040.txt` to `cisco-policy.txt` and setting
`"path": "cisco-policy.txt"` still exits 0. The lane convention (`S0NN.txt`, set by
`capture-source.py --out`) is what keeps the manifest readable and the capture log comparable; the
checker will not defend it.

**T2 — absolute `path` is fatal.** `"path": "/abs/…/S036.txt"` →
`S036:manifest UNAVAILABLE reason=invalid-path`, exit 2. Note the `:manifest` suffix, not `:source`.

**T3 — `..` escapes are fatal.** `"../../r25demo/S036.txt"` →
`S036:source UNAVAILABLE reason=outside-manifest-directory`, exit 2. Resolution is
`resolve(strict=True)` **then** `commonpath`, so a symlink pointing out is caught the same way. The
manifest must live beside the snapshots.

**T4 — `anchor` never changes the exit code.** All four measured, all exit 0:
`occurrences=5 anchor=MISSING` (no `anchor` on a non-unique quote), `anchor=OUT-OF-RANGE`
(`0`, `"1"`, `true`, `> len(raw_lines)`), `anchor=300-BROKEN` (valid line, window lacks the quote),
`anchor=10-ok`. A `$?`-only gate therefore **cannot** certify QUALITY Q9 — grep the receipt:
`grep -c 'anchor=MISSING\|anchor=.*-BROKEN\|OUT-OF-RANGE'`.

**T5 — a non-unique quote must carry `anchor`.** The window is `raw_lines[anchor-1:anchor+3]` joined
with a space and normalized, so the anchor must point at the line *and* the three after it must
contain the quote. r23's precedent: `S029:art14-2a-early-warning OK occurrences=2 anchor=10-ok`.
r24 needed none (76/76 `occurrences=1`). In the round-25 material, the S040 lines the entries cite
are the risky ones — measured duplicate counts inside the cited ranges: `L56 occ=4`, `L161 occ=2`,
`L299 occ=2`, `L303 occ=2`, `L304 occ=2`, `L307 occ=2` (8 duplicate candidates out of 24). Prefer a
unique line; if you quote one of these, add `"anchor": <line>`.

**T6 — `anchor` must be a JSON integer.** `"10"`, `0`, `true` → `OUT-OF-RANGE` (still exit 0).

**T7 — `schema_version` is type-strict.** `true` / `1.0` / `"1"` → `unsupported-schema`, exit 2.
The frontier harness accepts `true` and `1.0` and only fails later as `recheck-exit-2`, which reads
like an evidence failure rather than a schema failure.

**T8 — duplicate source id aborts the whole manifest.** `manifest UNAVAILABLE
reason=duplicate-source-id`, exit 2, **no per-source lines at all**. A duplicate *quote* id aborts
only that source (`S036:manifest UNAVAILABLE reason=duplicate-quote-id`) and the other four still
report.

**T9 — an empty `quotes` list is fatal.** `reason=missing-quotes`, exit 2. Every listed source must
carry at least one assertion; a captured source with nothing pinned must not be listed.

**T10 — short quotes are rejected.** `len(normalize(quote)) < 12` → `quote-too-short-to-be-evidence`,
exit 2. `<u></u> <u>  </u>` normalizes to the empty string and is caught by the same gate (this
closes the r24 RevC1Control forgery route).

**T11 — normalization is whitespace-collapse + `<u>`/`</u>` strip, nothing else.** Adding spaces
next to punctuation breaks the match: measured `、  ` → `MISMATCH reason=quote-not-found`. A quote
spanning a raw line break matches on branch 3 if you join it with a single space (measured on
S040:185–187), and on branch 2 if you keep the newline. Never reflow Japanese text with inserted
spaces.

**T12 — `occurrences=N` alone means the *raw* branch matched.** Only branch 3 prints
`normalized=markup-whitespace`. Do not read a bare `OK occurrences=1` as proof the quote was
normalized.

**T13 — a bare relative command is not cwd-invariant.** Measured on the round-24 manifest:
lane-root `exit=0`; from `/`, `python3: can't open file '//corpus/instruments/source-recheck.py'`,
`exit=2`. Every round-25 `recheck:` line **must** begin
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `. `recheck-audit.py`'s strict `cdroot` limb also
requires that `cd` target to `abspath`-equal the audited root, so no `cd .` or `cd ..`.

**T14 — the manifest must exist before the C1 receipt.** `recheck-audit.py` limb (c) requires every
`corpus/…(md|py|json|txt|tsv)` path named on the line to exist. With the manifest absent the two new
lines measure `paths_fail=2` and the audit exits 1 even though both commands are otherwise perfect.
The manifest is the single blocker between the current 35/37 and a clean C1 receipt.

**T15 — the frontier harness binds the line to the entry.** Measured problem labels on a fixture
root: `header-sources-not-rechecked` (entry declares `S036` and `S037`, line selects only `S036`);
`no-source-selection` (`--manifest` but no `--source`); `not-a-recheck-invocation` (`recheck: true`,
or `--selftest` on the line); `manifest-missing-ids` (selection not listed in the named manifest);
`manifest-unreadable` (manifest absent); `no-source-line` (no column-0 `source:` header);
`recheck-exit-1` (the line itself failed). Each FAILs the entry.

**T16 — the harness does not require *every* cited id to be selected.** Only the header `source:`
ids must be a subset of the `--source` set. An entry that cites `S036, S037` in prose but selects
only `S036` passes. Cover the cited ids anyway; the counter will not ask.

**T17 — header syntax is literal.** `SOURCE_LINE = ^source:\s*(S\d{3,})` at column 0. `Source:`,
`source :`, an indented `source:`, or a two-digit `S36` are all invisible → `no-source-line`. The
same `S\d{3,}` shape applies to `--source` on the line, so `S36` selects nothing.

**T18 — the manifest token is `\S+`, first match, quotes stripped.** Do not wrap the path in
backticks containing a space and do not route it through a shell variable; the harness reads the
literal token, not the shell expansion.

**T19 — exit 2 dominates 1.** Measured: quote MISMATCH on S036 plus a missing S040 file → exit 2.
A `MISMATCH` can therefore hide behind any `UNAVAILABLE`; read the receipt lines, not just `$?`.

**T20 — id ordering is lexicographic.** `Q10` sorts before `Q2`, and sources sort by id, so the
receipt order is fixed but not numeric. Harmless for pass/fail; relevant only if you ever diff two
receipts.

**T21 — `--source` typos fail as 2, not 1.** `S099:source UNAVAILABLE reason=not-listed`; a
malformed id (`bad/id`) gives `manifest:selection UNAVAILABLE reason=invalid-source-id`.

**T22 — `purpose` and `location` are free text.** Neither instrument reads them. Keep both anyway:
`location` is how r24 records which claim each quote backs, and it is the only in-file link between
a quote and the entry sentence it supports.

**T23 — one quote may appear in several sources.** r24 ships the identical
"Numerical CVSS Scores have very different meanings…" as `S001:Q2` and `S002:Q2`; quote ids are
per-source, so this is legal and useful when two documents assert the same thing.

**T24 — the auditor's root is the *cwd*.** `recheck-audit.py` defaults `--root` to `os.getcwd()`;
run it from the lane root (as `claims.json`'s counter does) or pass `--root` explicitly. Running it
from `/` makes every entry fail `cdroot`.

**T25 — `/tmp` is full on this host.** `/dev/nvme0n1p1` (mounted `/tmp`) measured **128G used,
580K free, 100%**. `mktemp -d` in `/tmp` fails with `No space left on device` (I hit it). Use
`mktemp -d -p /home/vgpnk/tmp` (as in §B(c)) — `/home` has 562G free. The big consumers are other
rounds' scratch dirs (`/tmp/r30fx-kengakuPred` 36G, `/tmp/r30fx-considhere` 3.8G, …); they are not
mine to delete.

---

## D. Findings for the L1 that are outside this seat's write scope

**D1 — C1's frozen `lines=35` can no longer match its own counter.** `claims.json` C1 freezes the
surface at "35 lines" and the target at `lines=35 pass=35`. The lane now has **37** knowledge
entries, and the measured audit prints `lines=37 total=37 … exit=1`. The counter cannot emit
`lines=35` again without deleting an entry. Either the claim is re-frozen against 37 lines, or the
predicate is re-worded to `pass == lines` (the audit already exits 0 on
`pass == len(entries) and complete and strict_passed == total`). The `c1-before.json` receipt is
frozen at `lines=35`; the after-receipt will not be comparable on that field.

**D2 — F10 is not in `corpus/README.md` yet.** Measured: `grep -nE '^\| F10 ' corpus/README.md` →
no match, and the harness prints `entries=10 pass=10`. The two vendor entries are invisible to
`frontier-recheck-count.py` until the row exists, so their manifest work cannot be scored by the
counter until then.

**D3 — S040/Cisco contradicts `claims.json`.** `assimilation.planned_reject` says the Cisco policy
row (staged S068) was rejected as unreachable; `capture-log.txt` records
`S040 status=200 … sha256=b7f7b55f…` with the instrument UA and says a ScoutFetchCisco seat
reproduced the fetch. If the manifest lists S040 — and both new entries do cite it — then the
`corpus/SOURCES.md` row for S040 cannot be `rejected` without the lane asserting two contradictory
things. Decide the row status before the manifest is committed; no instrument cross-checks it, so
nothing will catch the inconsistency.

**D4 — `corpus/SOURCES.md` still ends at S035.** No `S036–S040` rows exist, so the census has no
rows for the manifest's ids (E02/E03/E11 surface) and C2's `grep -lE '^source: S0(3[6-9]|[4-9][0-9])'`
can only succeed on the entries, not on the registry. `sources-census.sh validate` currently exits 0
with only the two pre-existing W04 warnings.

**D5 — the entries' cited ranges leave ample unique material.** Measured unique-candidate counts
(`len(normalize(line)) >= 12`, `occurrences == 1`) inside the ranges the entries cite: S036 20/21,
S037 24/24, S038 7/7, S039 26/27, S040 16/24. `nonunique=none` is achievable without quoting a
duplicate line.

---

## E. Residual risk and verification gaps

1. **The checker certifies captured bytes, not upstream truth.** Its own docstring: "a successful
   check verifies captured bytes, not current upstream availability or freshness." A green receipt
   says the quotes are in the snapshot; it says nothing about whether the vendor still publishes it.
2. **Nothing binds a quote to the sentence it supports.** No instrument checks that a manifest quote
   is drawn from the line range the entry cites, or that it asserts what the entry claims. That is a
   human read; `location` is the only in-file pointer.
3. **Nothing cross-checks manifest ids against `corpus/SOURCES.md`.** The §B(a) one-liner is the
   only gate, and it is manual.
4. **`anchor` compliance is invisible to `$?`.** Q9 needs a grep of the receipt (T4/T5).
5. **The frontier harness's `schema_version` gate is loose** (T7) and its `cited` set includes the
   `recheck:` line itself, so `selection-not-cited-by-entry` is nearly untrippable — that limb
   proves less than it looks.
6. **I could not run the literal lane-path commands in §B(a)–(d)** because
   `corpus/source-snapshots/round-25/manifest.json` does not exist. The byte-identical command
   bodies were executed against `/home/vgpnk/tmp/r25ref` (five committed snapshots + a reference
   manifest with the real pins). Expected-output shapes are measured; the only difference at the
   lane path is the quote set the scribes choose.
