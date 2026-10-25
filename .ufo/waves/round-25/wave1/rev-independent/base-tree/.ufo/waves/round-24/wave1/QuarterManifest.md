# QuarterManifest — exact load contract of `corpus/instruments/source-recheck.py`

Seat: L1Kasegi24.QuarterManifest (read-only scout). Question: the field-level contract of a
source-recheck manifest as the instrument actually loads it. Everything below is read from
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py`
(256 lines, unmodified at lane HEAD `c2480b143120364728b40397926ffcf30a7309c8` —
`git status` lists no change to it) and from executed probes of that file. Observed = a command
I ran; inference is labelled `[INFERENCE]`.

## 0. Verdict in one paragraph

A manifest is a UTF-8 JSON object with exactly two fields that matter to the loader:
`schema_version` (JSON int, value `1`) and `sources` (non-empty array of records). Each record
needs `id`, `path`, `sha256`, `quotes`; each quote needs `id` and the quote text. The loader
validates `schema_version`, `sources`, record `id` and record-id uniqueness **globally, before
any selection** (so one malformed id breaks every `--source` call). Everything else — `path`
shape, `sha256` shape, `quotes` presence, quote ids, quote text, file existence, containment,
digest, UTF-8, substrings — is validated **per record, only when that record is selected or
reached**. Exit codes are `0` all-clear, `1` content mismatch, `2` anything unavailable.
`--source` that names an id absent from a valid manifest emits `not-listed` and exits 2, which is
exactly the current F01–F05 failure.

## 1. CLI surface and exit-code contract

Usage string, lines 3–5:

```
python3 corpus/instruments/source-recheck.py --manifest PATH [--source ID]
python3 corpus/instruments/source-recheck.py --selftest
```

| invocation | behavior | lines |
|---|---|---|
| `--manifest P` (no `--source`) | checks **every** record; the whole-manifest conspectus | 163–170 |
| `--manifest P --source ID` | checks only the records whose `id` == `ID` (exact string) | 157–161 |
| `--selftest` **alone** | 4 isolated control cases in a tempdir; exit 0 all pass, 1 otherwise | 173–234 |
| `--selftest` + `--manifest` or `--source` | `manifest:selection UNAVAILABLE reason=selftest-takes-no-manifest-or-source`, exit 2 | 244–247 |
| neither | `manifest UNAVAILABLE reason=missing-required-argument`, exit 2 | 249–251 |

Exit-code union: **0 / 1 / 2 only**. `recheck` aggregates per record at 163–170: any record
returning 2 forces final 2; a 1 survives only if no 2 appears; else 0. Observed:
`true-1-plus-2` → `S900:Q1 MISMATCH … | S901:source UNAVAILABLE reason=missing`, exit 2;
`agg-1-and-0` → exit 1 with one `MISMATCH` and one clean source.

All output goes to **stdout**; stderr is empty in every failure path observed (no traceback
leaks), so a `&&`-chained `recheck:` line fails by exit code, never by crash.

`emit` (32–36) formats one line as `f"{stable_id} {status}"`, plus `f" {detail}"` when detail is
non-empty: 2 or 3 whitespace-delimited tokens. The selftest asserts on the first token only
(~line 206), so any consumer parsing receipts must treat positions 1 and 2 as id and status.

## 2. Global loader contract (`load_manifest`, 43–73) — evaluated in this order

| # | check | exact condition | emitted line | exit |
|---|---|---|---|---|
| 1 | manifest exists | `Path(path).resolve(strict=True)` raises `FileNotFoundError` (45, 48) | `manifest UNAVAILABLE reason=missing` | 2 |
| 2 | manifest readable/parsable/UTF-8 | `read_bytes` / `raw.decode("utf-8")` / `json.loads` raises `OSError`, `UnicodeError`, `JSONDecodeError` (46–47, 51) | `manifest UNAVAILABLE reason=unreadable-or-invalid` | 2 |
| 3 | top level is an object | `isinstance(data, dict)` (55) | `manifest UNAVAILABLE reason=unsupported-schema` | 2 |
| 4 | schema version | `type(data.get("schema_version")) is int` **and** `== 1` (55). `True`/`"1"`/`1.0`/`2` all fail — `type(...) is int` rejects `bool` | `manifest UNAVAILABLE reason=unsupported-schema` | 2 |
| 5 | sources list | `isinstance(records, list) and records` (58–59). `[]` and `{}` both fail; an empty manifest is not legal | `manifest UNAVAILABLE reason=missing-sources` | 2 |
| 6 | each record is a dict with a valid `id` | `valid_id` = `str` + `ID_RE.fullmatch` (39–40, 65) | `manifest:record-{index} UNAVAILABLE reason=invalid-source-id`, `index` = 1-based position in `sources` | 2 |
| 7 | record ids unique | `record["id"] in seen` (68–70) | `manifest UNAVAILABLE reason=duplicate-source-id` | 2 |

`ID_RE = [A-Za-z0-9][A-Za-z0-9._-]*\Z` (22) — no spaces, no leading `-`/`_`/`.`; letters, digits,
dot, underscore, hyphen after the first character. Observed: `-S900` →
`manifest:record-1 UNAVAILABLE reason=invalid-source-id`; a list `[rec, rec, {"id": ""}]` →
`manifest:record-3 …`; `["S900"]` (string record) → `manifest:record-1 …`.

**Coupling consequence:** steps 1–7 run before the `--source` filter (153 vs 157). One bad or
duplicated `id` anywhere makes *every* entry's recheck exit 2, including entries that select a
different id. Conversely, a record whose `path`/`sha256`/`quotes` are broken but that is *not*
selected is never validated: observed `selection-skips-broken-sibling` → selecting `S901` in a
manifest whose `S900` has `path: "nope.txt"` exits 0.
`[INFERENCE]` This is why the round-24 manifest must be id-clean as a whole even though the
Frontier receipts are per-source.

The whole manifest is read `len(chain)` times by an N-source `&&` chain — negligible, but the
same bytes must parse every time (no partial healing).

## 3. Per-record contract (`check_source`, 76–145) — evaluated in this order

Fields are looked up with `.get`; **missing and wrong-type collapse to the same failure**.

| # | field | exact required shape | emitted line | exit |
|---|---|---|---|---|
| 1 | `id` | already validated (77) | — | — |
| 2 | `path` | `str`, non-empty, **not** `Path(path).is_absolute()` (79) | `{id}:manifest UNAVAILABLE reason=invalid-path` | 2 |
| 3 | `sha256` | `str` matching `[0-9a-f]{64}\Z` — exactly 64 **lowercase** hex chars (23, 84) | `{id}:manifest UNAVAILABLE reason=invalid-sha256` | 2 |
| 4 | `quotes` | `list`, non-empty (88–89) | `{id}:manifest UNAVAILABLE reason=missing-quotes` | 2 |
| 5 | each quote is a dict with a valid `id` | `valid_id` (94) | `{id}:quote-{index} UNAVAILABLE reason=invalid-quote-id` (1-based) | 2 |
| 6 | quote ids unique **within this record** | (97–99) | `{id}:manifest UNAVAILABLE reason=duplicate-quote-id` | 2 |
| 7 | `quote` is non-empty `str` | `isinstance(..., str) and assertion["quote"]` (101) | `{id}:{quote_id} UNAVAILABLE reason=empty-quote` | 2 |
| 8 | capture resolves inside the manifest directory | `base = manifest_path.parent`, both sides `resolve(strict=True)`, `os.path.commonpath((base, resolved)) == base` (105–111) | `{id}:source UNAVAILABLE reason=outside-manifest-directory` | 2 |
| 9 | capture exists | `FileNotFoundError` (113–115) | `{id}:source UNAVAILABLE reason=missing` | 2 |
| 10 | capture readable | `OSError`/`RuntimeError`/`ValueError` (116–118) | `{id}:source UNAVAILABLE reason=unreadable` | 2 |
| 11 | digest | `hashlib.sha256(source_bytes).hexdigest() != expected` (120–123) | `{id}:sha256 MISMATCH expected=<e> actual=<a>` — both digests printed | 1 |
| 12 | capture decodes UTF-8 | `source_bytes.decode("utf-8")`, ran **after** the digest check (125–129) | `{id}:source UNAVAILABLE reason=not-utf8` — note: **no** `:sha256 OK` line precedes it | 2 |
| 13 | digest accepted | (131) | `{id}:sha256 OK` | — |
| 14 | each quote, sorted by quote `id` | (133–144) | `{id}:{qid} OK` / `OK normalized=markup-whitespace` / `MISMATCH reason=quote-not-found` | 1 on any `MISMATCH` |

Two ordering facts that matter for diagnosis:

- Steps 2–7 are **manifest-shape** checks and run before the file is touched; a record with both
  a bad digest and a bad quote id reports the shape error first.
- On digest mismatch the record returns 1 immediately (123): **no** `:sha256 OK` and **no** quote
  lines are printed for that source. Observed `sha-mismatch` → single line
  `S900:sha256 MISMATCH expected=3da66b01… actual=d861de6a…`.

### sha256 semantics

- Digest is over the **raw bytes** of the capture (120), computed before any decode; a trailing
  newline or a BOM changes it.
- Comparison is string equality against a lowercase-hex token; uppercase, 63-char, `null` and
  absent all fail at step 3 with `reason=invalid-sha256` (observed `sha-upper`, `sha-short`,
  `sha-null`).
- The capture is the *whole* file. Round-23 captures carry a 6-line provenance header before the
  body (`S030.txt` lines 1–7: `URL:`, `Content-Type: application/pdf`, `Method: markit`,
  `Notes:`, blank, `---`), and the digest covers it. Editing the header without re-pinning
  `sha256` produces exit 1 on `:sha256`.

### Path semantics

- `path` is resolved **relative to the manifest's own directory**, not cwd (`base =
  manifest_path.parent`, 105). Subdirectories are allowed: `sub/S900.txt` → exit 0 observed.
- Absolute paths are rejected at step 2 (`invalid-path`), and `..` escapes or symlinks that
  resolve outside are rejected at step 8. Observed: `link.txt` symlink to `/tmp/.../other/S900.txt`
  → `outside-manifest-directory`; `../other/S900.txt` where that file exists →
  `S900:source UNAVAILABLE reason=outside-manifest-directory`.
- **Therefore captures cannot be shared across snapshot directories.** A round-24 manifest in
  `corpus/source-snapshots/round-24/` must hold its own copies of S018/S029/S030/S031 (or the
  manifest must stay in `round-23/`). `../round-23/S018.txt` is a hard failure.

### Quote matching semantics (135–144)

1. **Exact substring** of the decoded capture text: `assertion["quote"] in source_text` →
   `{id}:{qid} OK`. Case-sensitive, no word boundaries (a quote of `Verifi` inside
   "Verifiable" is OK — observed `quote-in-larger-word` exit 0).
2. Otherwise the **declared normalization** branch: both sides through
   `normalize()` = `" ".join(MARKUP_RE.sub("", text).split())` (27–29), where
   `MARKUP_RE = </?u>` (24). This strips only `<u>` / `</u>` and collapses all whitespace runs —
   Python `.split()` treats `\xa0` as whitespace, so a non-breaking space in the quote matches an
   ordinary space in the capture (observed `nbsp-normalized` → `OK normalized=markup-whitespace`).
   It does **not** fold case, curly quotes, dashes, or any other Unicode (observed
   `curly-apostrophe-not-normalized` → exit 1). Cost: `normalize(source_text)` is recomputed per
   quote (137) — O(quotes × capture bytes); fine for these sizes.
3. Else `{id}:{qid} MISMATCH reason=quote-not-found` and the record returns 1.

Uniqueness is required on quote **ids within one source only** (97–99). The same quote id may
appear under different sources — round-23 does exactly that (`rule-3-1-1-scope-definition` under
both S030 line 85 and S031 line 128), and `dup-quote-id-across-sources` exits 0. Duplicate quote
*text* with distinct ids is accepted.

**Trap, observed:** a whitespace-only quote passes. `{"quote": " "}` is non-empty (101), exact
substring matches any capture containing a space, exit 0 (`quote-space-only`). The instrument has
no minimum-length or "quote must look like a sentence" gate. The manifest is the only place that
discipline can live — for round 24, quote text must be copied from the capture, and a single
character or single word is a false pass.

**Ceiling (already stated in the r23 `purpose`):** containment only. A quote that matches the
capture's own provenance header, a page marker (`<!-- Page 1 -->`), or a neighbouring rule passes.
Quote-to-location binding is human-verified, not machine-checked.

## 4. `--source` selection and "not-listed"

`recheck` (148–170):

1. `--source` must satisfy `valid_id` (149). An invalid id short-circuits **before** the manifest
   is read: `manifest:selection UNAVAILABLE reason=invalid-source-id`, exit 2. Observed even with
   a nonexistent `--manifest` (`bad id` probe) — the id error masks the manifest error.
2. Load fails → exit 2 (153–155).
3. `records = [r for r in records if r["id"] == source_id]` (158) — **exact, case-sensitive**
   string equality after the id syntax check. `s018` is syntactically valid but not listed.
4. Empty result → `{source_id}:source UNAVAILABLE reason=not-listed`, exit 2 (159–161).

"Not-listed" therefore means: the id is well-formed, the manifest parsed, and no record carries
that id. It is not a missing file and not a bad id. Observed against the committed round-23
manifest at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/manifest.json`:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S001
S001:source UNAVAILABLE reason=not-listed
exit=2
```

That manifest lists only `['S018','S029','S030','S031']` (4 sources, 32 quotes), which is the
whole mechanism behind the frozen C1 baseline "F01–F05 exit 2, they cite S001–S015 with no
capture".

## 5. What the DEFAULT `--source` output looks like

With no `--source`, the instrument prints one line per checked item, in **sorted order** —
records sorted lexicographically by `id` (164), and within a record quotes sorted
lexicographically by quote id (133), so `Q10` precedes `Q2` (observed):

```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
…                         (6 quote lines, alphabetical, not manifest order)
S029:sha256 OK
…                         (9 quote lines)
S030:sha256 OK
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
…
S031:sha256 OK
…
exit=0
```

Observed in full against the committed round-23 manifest: 4 `:sha256 OK` lines + 32 quote lines
= 36 lines, exit 0; exactly one `normalized=markup-whitespace` line, for
`S030:rule-4-1-9-independently-fixable` (the capture carries `<u>4.2.15</u>`-style markup; see
`S030.txt` tail).

Properties a round-level receipt must not assume:

- **No `manifest OK`, no `N/N passed` summary line.** The exit code is the only aggregate; a
  consumer that wants a count must count lines itself.
- Failures interleave with successes in the same stream; `MISMATCH` and `UNAVAILABLE` are the
  only non-`OK` statuses, and `UNAVAILABLE` always carries `reason=` as its 3rd token.
- The sha256 line is emitted before that source's quote lines, so a missing `:sha256 OK` for a
  listed source means the record died at steps 2–12; a `MISMATCH` on `:sha256` means every quote
  line for that source was skipped.
- Exit 1 can coexist with fully `OK` lines for other sources (observed `agg-1-and-0`).

## 6. The round-23 exemplar, quoted structurally

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/manifest.json`
(162 lines). Top level, lines 1–4:

```json
{
  "schema_version": 1,
  "purpose": "Round-23 F06-F08 captured-source assertions. … Ceiling (measured round 23): the instrument asserts substring containment only; quote-to-location binding is human-verified and is not machine-checked, so exit 0 does not prove a sentence sits at the article or rule the entry names.",
  "sources": [
```

- `purpose` is **not read by the instrument** — any top-level key but `schema_version`/`sources`
  is ignored (verified: a manifest with `purpose` exits 0). It is prose convention, and the r23
  text is the ceiling disclosure the round-24 manifest should carry forward (updated).
- Note the exemplar's `purpose` describes **F06–F08** only; the round-24 manifest must not carry
  a purpose that claims coverage it lacks.

Record shape, S018 at lines 5–35 (`id` 6, `path` 7, `sha256` 8, `quotes` 9):

```json
{
  "id": "S018",
  "path": "S018.txt",
  "sha256": "d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4",
  "quotes": [
    { "id": "coordinator-def",
      "quote": "Optional participant that can assist vendors and finders in handling and disclosing vulnerability information." },
    …
  ]
}
```

Quote objects are exactly two keys — `id` and `quote` (lines 11–12, 15–16, 19–20, …). **No
`location` key appears anywhere in the exemplar**, even though the instrument's own selftest
fixture builds one (line 191: `{"id": "Q1", "quote": "…", "location": "fixture line 1"}`). The
instrument never reads `location`, so a round-24 manifest may include it for humans but must not
rely on it being checked.

Sibling capture files in that directory: `S018.txt` (8372 B), `S029.txt` (19900 B),
`S030.txt` (26660 B), `S031.txt` (49350 B) — all flat, named by `path`, all inside the manifest
directory. Any one changed byte flips `:sha256` to exit 1.

Per-source quote budgets in the exemplar: S018 6, S029 9, S030 7, S031 10 (32 total). Nothing in
the instrument caps or requires a count beyond "≥ 1".

## 7. Contract the round-24 manifest MUST satisfy (derived, not a decision on layout)

1. **Single manifest**, JSON object, `"schema_version": 1` as a JSON integer.
2. **Every id selected by any Frontier `recheck:` line must be listed**, or that entry exits 2
   `not-listed`. Current citing set, from `grep -n '^recheck:' corpus/knowledge/*.md`:
   F01 `S001,S002`; F02 `S003,S004,S005`; F03 `S006,S007,S008`; F04 `S009,S010,S011,S012`;
   F05 `S013,S014,S015`; F06 `S018`; F07 `S029`; F08 `S031`. F09's two new entries add their
   own `S1xx` ids per C2. (S030 is listed in r23 but no entry selects it today; keeping it is
   harmless and it carries the CNA branch quotes.)
3. **All ids syntactically valid and unique** — one violation zeroes every per-source receipt.
4. **Each record needs its own capture beside the manifest**; cross-directory `../` reuse is
   rejected. A round-24 directory means re-copying S018/S029/S030/S031.
5. **`sha256` recomputed and re-pinned after the last byte edit** of every capture, lowercase,
   64 hex.
6. **Quote text verbatim from the capture**, long enough to be locating (not one token, not a
   bare `" "`), avoiding reliance on `<u>` stripping unless the emitted
   `normalized=markup-whitespace` token is acceptable in the receipt. Verbatim quotes produce the
   plain `OK` token, which is the stronger receipt.
7. **Any `recheck:` line that changes path must move to the new manifest**; the current eight
   entry lines all hardcode `corpus/source-snapshots/round-23/manifest.json`, so an extended
   round-23 manifest needs no entry edit, while a `round-24/manifest.json` requires editing all
   eight (F01–F05 lines currently end in per-source chains of the same hardcoded path).
8. `purpose` (optional, unread) should state the coverage actually present and the unchanged
   containment ceiling.

## 8. Falsifiers available to L1 (each one command, all local)

```
python3 corpus/instruments/source-recheck.py --manifest <M>                      # 0 only if all sources clean
python3 corpus/instruments/source-recheck.py --manifest <M> --source S001        # 2 not-listed if absent
python3 corpus/instruments/source-recheck.py --selftest                          # 0; proves instrument itself intact
python3 -c 'import json,sys;d=json.load(open("<M>"));print(len(d["sources"]),sum(map(lambda s:len(s["quotes"]),d["sources"])))'
sha256sum corpus/source-snapshots/<dir>/*.txt                                   # must equal every pinned sha256
```

Observed instrument selftest (bare `--selftest`, exit 0):

```
SELFTEST clean PASS expected-exit=0 … | SELFTEST corrupt PASS expected-exit=1 … |
SELFTEST missing-source PASS expected-exit=2 … | SELFTEST missing-manifest PASS expected-exit=2 …
```

## 9. Unverified / open (not blockers for the contract)

- **UNVERIFIED:** whether L1 chooses to extend `round-23/manifest.json` in place or create
  `corpus/source-snapshots/round-24/manifest.json` and rewrite the eight `recheck:` lines. Both
  satisfy the instrument; only the in-place option avoids re-copying four captures. This is an
  integration decision (L1 owns it).
- **UNVERIFIED:** the concrete S-ids the two F09 entries will cite; C2 only fixes "rows first
  registered this round" (`S1xx`), and `corpus/source-snapshots/round-24/` does not exist yet
  (`ls corpus/source-snapshots/` → `round-23` only).
- **UNVERIFIED:** whether the untracked `corpus/instruments/capture-source.py` (present at HEAD
  as `??`, authored by another seat this wave) is the sanctioned capture writer; it is not
  referenced by `source-recheck.py` and I did not run or assess it.
- No tools installed or upgraded by this seat.
