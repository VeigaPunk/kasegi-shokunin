# CriticHarm — round 98 harm audit (C1 `depth:verifiability`, C2 `coverage`)

Seat: CriticHarm (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `2133f5bd993aaf34efad795d5e0b588485401fb2`; C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`; C1 landing `e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`; freeze `12bb2f98cf9d07bcbc8b62985516cc3ff65d9ae8`.
All reads are `git show`/`git cat-file`; every extract is under `/fast/scratch/hyaku/kasegi-r98/CriticHarm` (removed before yield). No lane file was written except this report.

Environment note (matters for P1 reproducibility): foreground runs of `resolve.py` on the full e2caf4a1 tree were killed by signal 15 at ~180–195 s (`CENSUS-CHECK fail reason=resolve-rc-15 rc=2`; a manual `resolve.py` run returned rc=143 = 128+15). The same command with no deadline (`async`, `timeout: 0`) completed in 454 s and passed. The kill is the harness's background-job cap, not the instrument: the run's `resolve-rc%d` formats `-15` as `resolve-rc-15`.

## 1. Governance files byte-identical base → both landings

```
for f in SKILL.md PROVINCE.md SHONEN.md AGENTS.md; do
  for r in 2133f5b e2caf4a e2d3de7; do git cat-file -p $r:$f | sha256sum; done; done
```

| file | base | C2 landing | C1 landing |
|---|---|---|---|
| SKILL.md | `7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552` | same | same |
| PROVINCE.md | `736299ba5d43f8b8fae299d55287ba0352287ef3c0fc5a81acdbc99cdaf54ac3` | same | same |
| SHONEN.md | `3c2fb3ca31cc2448011ef4781a0a33f8685882dc780689bb471f82949e707bed` | same | same |
| AGENTS.md | `a7ad6e6e5957bffcfc04f7af75db9217e8023d049271fecb16738c83fdea5e9f` | same | same |

`git diff --name-status 2133f5b e2d3de7` touches only `SCORECARD.md`, `corpus/instruments/citation-survival.md`, `corpus/instruments/capture-secret-scan.py`, `corpus/instruments/census-at-rev.py`, `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`, the round-94 receipt, and `.ufo/waves/round-98/**`. No governance file is in the diff.

## 2. `capture-secret-scan.py` loses no earlier shape

Pattern table, loaded from each revision's own module (`patterns()` returns 35 at base, 39 at landing):

```
base 35, land 39
removed: []
added: gitlab-ci-build-token, gitlab-iam-authorization-code,
       gitlab-iam-refresh-token, gitlab-session-cookie
CHANGED (each strictly wider):
  gitlab-feed-token, gitlab-feed-token-v2, gitlab-oauth-app-secret,
  gitlab-runner-registration-token, gitlab-scim-oauth-token
  `(?![A-Za-z0-9_-])` -> `(?![A-Za-z0-9])`
```

No removal, no rename; the five changes only drop `_`/`-` from the refused set (a superset match). Selftest at the two revisions:

```
base:    SELFTEST-RESULT pass cases=148
landing: SELFTEST-RESULT pass cases=170
```

Case-level comparison of the two outputs: 140 distinct case names at base, 162 at landing; `missing at landing: []`; every base case still `ok` with an identical `got=` value (`changed got: 0`). The 22 added names are the four new shapes and the five widened boundaries plus their negatives. This is the empirical form of the same result as the table diff.

The four new regexes match the S140 capture lines quoted by the new knowledge entry (`sed -n '291,294p;478,481p;495,498p;547,551p' corpus/source-snapshots/round-94/S140.txt`): `glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\-]{20}`, `gliamrt-…43.…43`, `gliamac-…43.…43`, `(?:cell-[0-9]+-)?[0-9a-f]{64}` with `_gitlab_session(?:_geo_[0-9a-f]{64})?`. The entry's `recheck` command prints `4`, `2`, `RECHECK-OK`.

## 3. Round-94 receipt redaction

File: `.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt`.

```
base:    76 lines, 3504 bytes
landing: 76 lines, 3515 bytes
differing line indexes: [74]
common prefix: 42 bytes; common suffix: 30 bytes
base middle: abc12_0123456789abcdefghij
land middle: [ci-build-token-fixture-redacted-r98]
```

Line count preserved; every byte outside the literal (including the padding before `rc=0`) is identical; only the fixture literal changed, to a marker in the same `[redacted…]` style the file already uses (`[redacted:credential]`, `[gitlab-deploy-token-in-url-fixture-redacted-r97]`). The literal is still recoverable from git history at `2133f5b`.

Why the redaction was needed, measured with the two instruments on two one-line files:

```
base scanner    on old literal:     CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 ... rc=0
landing scanner on old literal:     HIT shape=gitlab-ci-build-token path=…/f-old.txt line=1
                                    CAPTURE-SECRET-SCAN mode=files scanned=1 hits=1 ... rc=1
landing scanner on redacted line:   CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 ... rc=0
```

So the receipt's `rc=0 shapes=none` was true at round 94 and would be false under the round-98 rule; the redaction removes a live contradiction from the record without touching any other byte. The placeholder itself is not a shape (landing scanner clean).

## 4. Census numbers are not gamed

`corpus/instruments/census-at-rev.py`'s `rate()` counts only `c == "INTERNAL"`; `host_incl()` adds `RESOLVES`/`MIRROR-EQUIVALENT`; `host_owned` is the count of those two classes. The landed header:

```
measured-at: e2caf4a1561b544a6ea684b0bcfa975f7e7f6061
pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2551/7559 = 33.75% | lane 2589/7961 = 32.52%
host-inclusive rate (resolve.py's definition): SKILL 166/732 = 22.68% | corpus 2629/7559 = 34.78% | lane 2667/7961 = 33.50%
host-owned inputs: 78 absolute-path citations resolve outside the lane (reported separately; not revision-stable)
```

Re-measured at the named revision with the frozen command:

```
python3 -B corpus/instruments/census-at-rev.py --lane . \
  --check corpus/instruments/citation-survival.md --work <scratch>
CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 \
  skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78   (rc 0, 454 s)
```

The cached measurement (`work3/cache/e2caf4a1….json`) gives the host numbers `skill_host 166/732`, `corpus_host 2629/7559`, `lane_host 2667/7961` — exactly the file's host-inclusive line. The file's own matrix reconciles the pinned triple: INTERNAL `38 + 124 + 2427 = 2589` (lane), `38 + 124 = 162` (SKILL), `124 + 2427 = 2551` (corpus); RESOLVES `0 + 4 + 74 = 78`; host `162 + 4 = 166`, `2551 + 78 = 2629`, `2589 + 78 = 2667`. No knowledge file was edited: `git diff --name-status 2133f5b e2d3de7 -- corpus/knowledge/` is `A corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` only. The new entry's citations are its own S140/S144 sources; they account for the +3 distinct corpus citations and +1 INTERNAL between the base and e2caf4a1, not for the SKILL numerator (732/162 unchanged base → landing).

Base measurement for comparison (`--rev 2133f5b`): `skill=162/732 corpus=2550/7556 lane=2588/7958 host_owned=78`. The dispatch text's `corpus 2550/7556, lane 2588/7958` are the **base** numbers, not the regenerated census's; see H3.

## 5. No earlier `capture-secret-scan.py:N` citation out of range

The census's own line-anchor table (generated at e2caf4a1) lists every `capture-secret-scan.py` anchor against the 701-line landing file; the largest cited anchor in the corpus is 439 and every such row says `in range`:

```
grep -o 'capture-secret-scan\.py:[0-9]*' corpus/instruments/citation-survival.md | sed 's/.*://' | sort -n | tail -1
439
grep -c 'OUT OF RANGE' corpus/instruments/citation-survival.md
19        # all .gitignore / README.md / SHONEN.md rows; none capture-secret-scan
```

Caveat (not "out of range"): the anchors are numerically in range but semantically drifted — C2 inserts 14 lines at ~175, 13 at ~295 and 24 at ~613, so every anchor after the first insertion now points earlier in the file. The drift predates round 98: at base, `is_capture_path` is at 345 (entry cites `:216-221`), `report()` at 403 (cites `:274-286`), the exit-2 path at 644 (cites `:450-454`), and the allowlist sha256 key at 361 (cites `:232`). Round 98 adds 51 lines of further drift; the census's anchor check cannot detect it (it only compares N with the file length). The round-94 precedent re-anchored after a 33-line growth; round 98 does not re-anchor. This is a verifiability caveat, not a violation of the assigned "out of range" criterion.

## H1 — HARM (provenance): `harness_sha256` matches no committed harness

`claims.json` pins `"harness_sha256": "d39a1fc8cc5ad189b5077dc03c1c3373bca59d77a120493163ccca63eb4f05e0"`. The harness blobs:

```
freeze 12bb2f9  .ufo/waves/round-98/controls/c1-controls-r98.py  0488d79626e54731a8d5be3985fd1edad68b2b612a74d86454d5bca8a3950e7a
landing e2d3de7 .ufo/waves/round-98/controls/c1-controls-r98.py  d97132684455aa6cca5bd65dd0e07a94942b8469801d05f219ba3a52b47ecc1a
grep -rn d39a1fc8 .  ->  only .ufo/waves/round-98/claims.json:16
```

The erratum discloses the harness fix ("the fixture clone now checks out `--base` explicitly … the same 8 controls pass on the fixed instrument") but leaves the pin at the pre-fix draft value. The postfix receipt's harness is the landing one (`d9713268…`). A reader cannot verify the pinned counter from any committed artifact.

Smallest safe correction: in the C1 erratum, record `harness_sha256 d39a1fc8… -> d9713268…` (the harness that produced `c1-controls-r98-postfix.txt`), or add a `harness_sha256_postfix` field. No predicate changes; P2 names the path, not the hash.

## H2 — HARM (regression): new `SyntaxWarning` on every scanner run

C2's docstring at `corpus/instruments/capture-secret-scan.py:184` contains a single-backslash `\-` in a non-raw module docstring:

```
(S140 line 480), right boundary `[^0-9a-zA-Z_\-]`/EOL.
```

Measured:

```
base:    python3 -W error::SyntaxWarning -c 'import … capture-secret-scan.py'  ->  import ok 35
landing: same command -> SyntaxError: "\-" is an invalid escape sequence. Did you mean "\\-"? …
landing: python3 -B capture-secret-scan.py --files …  ->  stderr warning on every run
landing: python3 -B capture-source.py --selftest      ->  stderr carries the same warning (base stderr empty)
```

The selftest still passes (the warning is non-fatal), so K1 is unaffected; but the instrument's stderr is no longer clean, the intake gate's selftest now emits it, and any consumer running with `-W error` fails to compile the module.

Smallest safe correction: double the backslash at line 184 (`\\-`), or make that docstring raw if no other escapes are intended. Then re-run `--selftest` (170 cases) and `capture-source.py --selftest`; the instrument sha256 changes, so the claim's `instrument_sha256` pin needs the same erratum treatment (no shape or boundary changes).

## H3 — documentation discrepancy (not a claim failure)

The dispatch/Goal text says the regenerated census records `corpus 2550/7556, lane 2588/7958`. The landed census records `corpus 2551/7559, lane 2589/7961`, and `--check` passes with those numbers. `--rev 2133f5b` measures `2550/7556, 2588/7958` — the dispatch text quotes the base, not the regenerated census. The SKILL numbers (`162/732` pinned, `166/732` host-inclusive) are the same at both revisions and are correct in the text.

Smallest safe correction: fix the dispatch/lesson sentence to `corpus 2551/7559, lane 2589/7961` (or label the `2550/7556, 2588/7958` pair as the base). Do not change the census: it is the correct e2caf4a1 measurement.

## Caveats (no verdict)

- **C1 body is host-dependent, the pinned line is not.** The cached generated body and the landed body differ only in the `.ufo/watchdog.log` line count in the anchor table (`3233` in my run vs `3230` in the landed file). The pinned line is revision-stable and passes; the body's host-owned anchor rows are not byte-reproducible, as the header's "not revision-stable" note says.
- **The 19 out-of-range anchors are pre-existing.** They are `.gitignore`, `README.md` and `SHONEN.md` citations, none touched by C1/C2.
- **C2 plants are generated, not copied.** `capability-check.py`'s `PLANT_SPEC` builds every positive from `gen(rnd, ALNUM/ALNUMU/HEX, n)` with a run-time nonce; no selftest literal appears in the builders. K5's SCORECARD row is one row, names all nine shape ids, first-working-round `87`.

VERDICT: SKILL.md / PROVINCE.md / SHONEN.md / AGENTS.md byte-identical base → C1 landing — NO HARM
VERDICT: capture-secret-scan.py loses no earlier shape (35→39 patterns, no removal, five strict widenings; 140/140 base selftest cases still ok with identical got; 148→170) — NO HARM
VERDICT: round-94 receipt redaction preserves line count (76/76) and every byte outside the literal (prefix 42 / suffix 30), marker consistent with the file's existing redaction style — NO HARM
VERDICT: census numbers not gamed (pinned numerator INTERNAL-only in code and in the matrix; no knowledge file edited; `--check` pass 162/732, 2551/7559, 2589/7961, host_owned 78; host-inclusive 166/732, 2629/7559, 2667/7961) — NO HARM
VERDICT: no earlier `capture-secret-scan.py:N` citation out of range (max 439 ≤ 701; all such rows `in range`; 19 out-of-range rows are other files) — NO HARM
VERDICT: H1 stale `harness_sha256` pin (`d39a1fc8…` matches no committed harness; freeze `0488d796…`, landing `d9713268…`) — HARM (provenance; fix by erratum pin update)
VERDICT: H2 new `SyntaxWarning` at capture-secret-scan.py:184 (`\-` in a non-raw docstring; fails under `-W error`, pollutes the intake gate's stderr) — HARM (regression; fix by `\\-`, re-pin)
VERDICT: H3 dispatch text quotes the base census numbers (2550/7556, 2588/7958) as the regenerated census's (2551/7559, 2589/7961) — HARM (documentation only; claim P1 passes)
VERDICT: overall — HARM (two low-severity fixable defects, H1/H2; C1 P1 and C2 K1 both pass as written)
