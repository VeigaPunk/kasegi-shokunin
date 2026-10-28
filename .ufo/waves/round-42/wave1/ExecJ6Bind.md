# ExecJ6Bind — F-BIND capture-binding hardening (round 42, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `5053a7f46de35784cff4b56756906e9014a38276`;
lane HEAD at work time `514ff62` (three round-42 claims-erratum commits). `git diff --stat 5053a7f HEAD --
corpus/instruments/capture-binding-check.py corpus/source-snapshots corpus/SOURCES.md` is empty, so every
measurement below holds for the base ref as well as the working tree. Working tree == HEAD (`git status
--porcelain` lists only untracked wave-dir files).

## 1. Deliverables

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-42/wave1/ExecJ6Bind.capture-binding-check.py` | 1129 | 52275 | `ebc206d433b334a9f844ef9726fe87fb9cb2a78cf8f41943add605869da00ec7` |
| `.ufo/waves/round-42/wave1/ExecJ6Bind.transcript.txt` | 285 | 18653 | `717ba82c514e82ab7115124f7395a023a74264e25daa7a246f0bbee8ec12734b` |
| committed instrument it replaces | 892 | — | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |

The deliverable is landable bytes only: `corpus/instruments/capture-binding-check.py` replacement, same CLI
(`--root/--selftest/--scratch`), same exit contract (0 pass, 1 failure, 2 usage/read error). Diff vs the
committed file: 383 diff lines, +257/−20, and every removed line is an accounted-for docstring/format edit
(the "rules B **and** C" bound sentence, the AUDIT description, the stale known-limit bullet, the
`write_manifest` signature, the `if url_ok and prov_ok` condition).

## 2. What the defect was, measured on the committed bytes

Each variant is one change on a scratch copy of `corpus/` (full copy, round-41 record S063), the committed
instrument run with `--root <copy>`:

| # | mutation | committed bytes | patched bytes |
|---|---|---|---|
| a | `round-41/S063.txt` removed, record still names it | **exit 0, `records=55 bound=55 unbound=0`** | exit 1 `FAIL rule=capture-missing record=S063 path=S063.txt dir=round-41`, `records=55 bound=54 unbound=1` |
| b | `url` case variant (`/rfc/`→`/RFC/`) | exit 1 `rule=url-mismatch` (already rejected) | exit 1, same token |
| c | `sha256` `925512e7…`→`ffff…` | **exit 0, `bound=55`** | exit 1 `FAIL rule=digest-mismatch record=S063 sha256=ffff…` |
| d | `url` trailing slash | exit 1 `rule=url-mismatch` (already rejected) | exit 1, same token |
| e | `capture_url` trailing slash, `http.final_url` untouched | **exit 0, `bound=55`** | exit 1 `FAIL rule=capture-url-mismatch record=S063 capture_url=…/ final_url=…` |
| f | `snapshot_sha256`→`ffff…`, `sha256` untouched | **exit 0, `bound=55`** | exit 1 `FAIL rule=digest-mismatch field=snapshot_sha256 record=S063 sha256=ffff…` |

Real defects on the committed bytes: an absent capture path, a `sha256` that no file satisfies, a
`snapshot_sha256` that no file satisfies, and a free-text `capture_url`. All four are now rejections.

**Correction to the round-41 wave-2 F-BIND narrative** (it matters to whoever grades the family): that receipt
reports URL case *and* trailing-slash mutations as surviving on the then-current bytes. Measured here, the
committed instrument rejects both (`url-mismatch`, exit 1) as soon as it is pointed at the mutated copy. That
receipt prints the identical `records=63 bound=63` on both sides of its mutation, which a mutation of a bound
record cannot produce — it measured the lane root, not its scratch copy. So two of the five claimed survivors
never survived, and the URL hole that did exist is the *second* URL field (`capture_url`), closed by E3 below.

## 3. The patch — rule E (E1/E2/E3), wired into `bound`

`capture_binding(record, dirpath, round_no)` returns `([FAIL fragments], digest_unpinned)`; `check()` counts a
record `bound` only when rules B **and** C **and** E pass, so a manifest with absent or tampered captures can no
longer print `bound=records`.

- **E1 path.** `path` must be a string, resolve (realpath) inside its own snapshot directory and name a regular
  file: `FAIL rule=capture-missing record=<id> path=<p>`. A `../` escape is the same line — the record names bytes
  outside the directory under audit.
- **E2 digest.** The capture file is hashed once per record. `sha256` must be 64 lowercase hex and equal it
  (`rule=digest-mismatch record=<id> sha256=<pinned>`); non-hex is `rule=digest-invalid`; absent/empty/`"0"*64` is
  `rule=digest-missing` in round-32+ and a *printed* exemption (`AUDIT … digest_unpinned=N`, exit unchanged) in
  legacy rounds. `snapshot_sha256`, when present and not the sentinel, must equal the file digest
  (`rule=digest-mismatch field=snapshot_sha256 …`). `full_text_sha256` is shape-checked only.
- **E3 URL fields.** `capture_url` and `http.final_url` must be byte-identical when both are present, and a
  `http.final_url` must be the record's `url` or its `capture_url`: `rule=capture-url-mismatch record=<id>`.
  `url` vs `capture_url` may differ (documented redirects), which is why E3 is an internal-agreement rule.

Why the sentinel/legacy exemption instead of strict-everywhere: `"0"*64` is the lane's own fixture vocabulary for
"no digest declared" — the committed `kill-rule-check.py` `record()` writes exactly that, and its `punctuated-url-cell`
and `nested-legacy-round` probes pin `exit 0` on round-30/31 fixtures. A strict rule would turn those probes red
(harm to a committed gate). The exemption is the same declared-exemption shape rule C already uses for `archival`,
it is printed on AUDIT, and it is closed for round-32+ — measured no-harm in §5.

## 4. Digest-field semantics (transcript §2b, measured so E2 pins what it can)

| field | records carrying | equals capture bytes | differs |
|---|---|---|---|
| `sha256` | 55 | 55 | 0 |
| `snapshot_sha256` | 7 | 7 | 0 |
| `full_text_sha256` | 2 | 1 | 1 (S060: extracted text ≠ its HTML bytes) |
| `raw_sha256` | 11 | 0 | 11 (pre-normalization fetch bytes, by design) |

`capture_url` on 5 records, `http.final_url` on 13, disagreements between them: 0.

## 5. Extant evidence (all in `ExecJ6Bind.transcript.txt`, section numbers below)

1. **Base run, patched bytes on the committed lane:** exit 0, 0 `FAIL` lines,
   `AUDIT records=55 … multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt`,
   `records=55 bound=55 unbound=0` — the frozen 55/55 no-harm requirement.
2. **`--selftest`:** `selftest cases=33 failures=0`, exit 0 (was 23). Ten new cases: `capture-path-missing-rejected`,
   `capture-path-escape-rejected`, `digest-mismatch-rejected`, `digest-invalid-rejected`,
   `digest-unpinned-modern-rejected`, `digest-unpinned-legacy-listed`, `capture-url-mismatch-rejected`,
   `url-trailing-slash-rejected`, `snapshot-digest-mismatch-rejected`, `snapshot-digest-matches`. The fixture
   writer now pins each fixture record's `sha256` to the bytes it wrote (after all captures exist, so a record
   naming a shared path pins the surviving file), with `pin_digests=False` for the deliberate-defect cases.
3. **Replay over scratch manifests** — the table in §2, both instruments, real exits.
4. **No-harm probe, committed sibling counter over the patched bytes:**
   `HYAKU_SCRATCH=$S/krc python3 corpus/instruments/kill-rule-check.py --instrument <deliverable> --scratch $S/krc2`
   → `KILL-RULE … sha256=ebc206d4… bytes=52275 lines=1129 floor=19`, all nine probes `pristine=pass` (including
   `punctuated-url-cell exit=0` and `nested-legacy-round exit=0`), `mutants=3 killed=3 survivors=0 invalid=0`,
   `survivors=0`, exit 0. Its three mutant anchors were kept byte-identical (each `find` count is 1 by construction
   of that run).
5. **`r-defect-closure.sh` textual constraints, checked on the patched bytes:** `url-matching-two-rows` count 0;
   case tuples matching `^[[:space:]]*\("[a-z0-9-]+",` = 31 (≥11); all nine R9 names present
   (`per-file-orphan-detected`, `per-file-orphan-listed`, `nested-snapshot-dir`, `fetched-utc-pending-rejected`,
   `fetched-utc-local-offset-rejected`, `dup-record-in-manifest`, `double-https-row`, `rejected-row-anchor`,
   `summary-only-selftest-rejected`); R5's seeding pattern `("duplicate-id-rows", case_duplicate_id_rows` present
   exactly once, so R5's mutated-tree fixture still seeds.
6. **CLI contract:** `--root /nonexistent` → `UNAVAILABLE reason=no-snapshot-tree …`, exit 2; `--bogus` → argparse
   error, exit 2; default root is script-relative three levels up (unchanged, correct at `corpus/instruments/`).

## 6. Landing notes for the L1

1. Land the deliverable bytes at `corpus/instruments/capture-binding-check.py`.
2. Append the R6-style `SKILL.md` correction for that row: digest `3d9e5e0d…` → `ebc206d4…`, 892 → 1129 lines,
   `--selftest` `cases=23` → `cases=33`, and the round-34 "known limit" sentence that a record naming an absent
   file is not a rule here is superseded by rule E1.
3. `r42-closure.sh` J6 should run the landed instrument with `--root <mutated scratch copy>` (never the lane
   default root) and assert the tokens in §3; the r41 missing-path replay is `variant a` and the URL replay is
   `variant b/d` (pre-existing `url-mismatch`) plus `variant e` (`capture-url-mismatch`). Contract also messaged to
   `ExecSuiteCore-2`.
4. Nothing else in the lane reads this instrument's internals; no other instrument breaks (measured, item 4/5).

## 7. Deliberate boundary, risks

- Still accepted, by measurement and printed rather than silent: a legacy-round (round<32) record that pins no
  digest (`digest_unpinned=N` on AUDIT, exit unchanged); a `raw_sha256` or `full_text_sha256` mutated to another
  *valid* digest (pre-normalization bytes / extracted text are not the capture bytes — a J6 digest replay must use
  `sha256` or `snapshot_sha256` on a round-32+ record, which the corpus's post-round-32 records all are).
- `capture_url` may legitimately differ from `url` (S057, S025), so no rule can anchor it to the registry row; E3
  only forbids the fields disagreeing with each other about the same fetch.
- Risk to a reader: the round-41 F-BIND receipt overstates the surviving defects (see §2); the patch closes the
  two real digest holes that receipt did not find.
- No tools installed or upgraded this seat. No tracked lane/fleet file written; scratch
  `/fast/scratch/hyaku/kasegi-r42/ExecJ6Bind/` removed before this receipt was written.
