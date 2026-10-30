# R48Review08 — Independent replay of the six pre-freeze `shonen-form.py` source mutants

- **Seat:** R48Review08 (mutation-tester) · **Round/wave:** 48 / wave1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Date:** 2026-10-30
- **Frozen claim:** `.ufo/waves/round-48/claims.json` — sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` (matches `freeze.txt`; the briefing id `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` is the freeze **commit**, not the file sha — corroborated by R48Review31 "frozen in commit 3546f70" and R48Probe16)
- **Frozen counter:** `corpus/instruments/shonen-form.py`, sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`
- **Canonical target:** `SHONEN.md`, sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`
- **Receipt under replay:** `.ufo/waves/round-48/controls/pre-freeze-mutants.txt` — 6 source mutants, each `caught=1`, divergent_cases 3/2/3/4/4/1
- **Measured revision note:** lane `HEAD` was `40b6b3f7d6980b503e2c718a2a3d87a8e07587c5` at replay time (integration is landing sibling reports; the battery's only lane dependency is read-only evidence resolution of `LOG.md` under `--root`)
- **Round-47 routes:** R1 (SHONEN.md canonical-form drift — the defect C1 closes; the checker operationalizes R1's "seed verbatim + marks confined to the box character + one indented evidence line per box, no other prose", `corpus/lessons/round-47-verifier-spotcheck.md` §6) is the class under replay. R2 (frozen plain-target phrasing) is not exercised by this seat — no plain-grep target is involved.
- **Scope:** author-side form only; never promotion or semantic truth. Production bytes read-only; all mutants live on scratch copies. No tool installs (host `python3` 3.14.8, stdlib only; none needed). No delegation, no background jobs, no commits.

## Godspeed axes

- **depth:verifiability** — convert the receipt's count-only tallies into re-executable evidence: 13 reconstructed checker mutants × the frozen 17-fixture battery, every divergence recorded with before/after outputs and hashes.
- **No other axis** is touched; no production or sibling bytes change (hash-proven below).

## 1. Method

Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Review08/` (explicitly created; removed at the end of this seat, after the receipts below were saved into this report).

The receipt records **counts, not mutant bytes** — the six mutant checker bodies were not retained under `controls/` (the same gap R48Review24 and R48Review31 disclose). Replay is therefore a *reconstruction*: for each named class I derived my own minimal single-anchor source mutation of the frozen checker, applied it to a scratch copy, and ran the **same bounded behavioral detector** — the frozen 17-fixture battery (`controls/fixtures.json`, sha256 `10d2aa79e231d1ac7bb02e9c53df4c7f50d78d07931c42bfa0384a82c0cbb288`) with expectations from `controls/pre-freeze-fixtures.txt`:

```sh
python3 <checker-variant.py> --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file <fixture>.md
```

A case **diverges** when the mutant's full stdout line or process exit differs from the pristine checker's on that fixture. `caught=1` means ≥1 divergent case. Per my role card: a baseline failure would make everything inconclusive — the baseline is green (§2), so verdicts are conclusive. Mutant files were never written into the lane; the pristine copy was hash-checked before and after the whole battery (§6).

Setup command (exact):

```sh
mkdir -p /fast/scratch/hyaku/kasegi-r48/R48Review08 && cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py /fast/scratch/hyaku/kasegi-r48/R48Review08/pristine.py && cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/{fixtures.json,pre-freeze-fixtures.txt} /fast/scratch/hyaku/kasegi-r48/R48Review08/ && sha256sum /fast/scratch/hyaku/kasegi-r48/R48Review08/pristine.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
```

Expected: both checker copies `0ab32a2c…77b313dd`. Observed: both `0ab32a2c…77b313dd`. MATCH.

Replay driver (named scratch fixture): `/fast/scratch/hyaku/kasegi-r48/R48Review08/replay.py` — materializes the 17 fixtures from `fixtures.json` (byte-exact, UTF-8; the `missing-file` case is an **empty file** per its `"text": ""`), asserts every mutant anchor occurs exactly once in the source, runs the battery for pristine + 13 mutants (238 subprocess runs, wall ≈ 6 s), and writes `summary.json` + `battery-matrix.txt`.

## 2. Baseline (pristine checker) — conclusive, not inconclusive

Expected: the pristine copy reproduces all 17 rows of `controls/pre-freeze-fixtures.txt` (exit + finding). Observed: **17/17 MATCH** (`baseline_17_of_17_match_receipt: true`).

| case | expected (receipt) | observed (pristine) | verdict |
|---|---|---|---|
| canonical | 0 SF-CLEAN | `canonical=1 finding=SF-CLEAN exit=0` | MATCH |
| actual-r47-drift | 1 SF-PREAMBLE | `canonical=0 finding=SF-PREAMBLE exit=1` | MATCH |
| missing-file | 1 SF-NEWLINE | `canonical=0 finding=SF-NEWLINE exit=1` | MATCH |
| fenced | 1 SF-PREAMBLE | `canonical=0 finding=SF-PREAMBLE exit=1` | MATCH |
| commented | 1 SF-PREAMBLE | `canonical=0 finding=SF-PREAMBLE exit=1` | MATCH |
| duplicate | 1 SF-TRAILING | `canonical=0 finding=SF-TRAILING exit=1` | MATCH |
| extra-prose | 1 SF-TRAILING | `canonical=0 finding=SF-TRAILING exit=1` | MATCH |
| crlf | 1 SF-NEWLINE | `canonical=0 finding=SF-NEWLINE exit=1` | MATCH |
| no-newline | 1 SF-NEWLINE | `canonical=0 finding=SF-NEWLINE exit=1` | MATCH |
| wrong-label-0…3 | 1 SF-BOX ×4 | `canonical=0 finding=SF-BOX exit=1` ×4 | MATCH |
| missing-evidence-0…3 | 1 SF-EVIDENCE ×4 | `canonical=0 finding=SF-EVIDENCE exit=1` ×4 | MATCH |

Fixture-materialization check: each fixture's first differing line vs `canonical` is the intended mutation (e.g. `wrong-label-3` = box-4 line `…(PROVINCE.md still accurate)x` at line 11; `duplicate`/`extra-prose` append at line 13; `crlf`/`no-newline` differ only in line endings/trailing newline — no spurious byte differences).

## 3. Replay of the six receipt classes — all six killed

Constructions (single-anchor edits of the frozen source; each anchor verified unique before substitution):

| # | class | my construction (old → new) | divergent cases observed | receipt | verdict |
|---|---|---|---|---|---|
| 1 | preamble-bypass | `if i >= len(lines) or lines[i] != value:` → `…and lines[i] != value:` (or→and: line content never checked) | **3**: actual-r47-drift, fenced, commented | 3 | **KILLED — count MATCH** |
| 2 | trailing-bypass | `if i != len(lines):` → `if i > len(lines):` (i never exceeds len: full bypass) | **2**: duplicate, extra-prose | 2 | **KILLED — count MATCH** |
| 3 | newline-bypass | `if not text.endswith('\n') or '\r' in text:` → `if False:` | **3**: missing-file, crlf, no-newline | 3 | **KILLED — count MATCH** |
| 4 | box-bypass | `re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label), …)` → `re.fullmatch(r'- \[([ ~x])\] .*', …)` (label text unchecked) | **4**: wrong-label-0…3 | 4 | **KILLED — count MATCH** |
| 5 | evidence-bypass | `elif mark != ' ':` → `elif False:` (missing evidence line accepted) | **4**: missing-evidence-0…3 | 4 | **KILLED — count MATCH** |
| 6 | label-count | ambiguous name — four candidates, see §4 | **1** under candidate A | 1 | **KILLED — count MATCH under A** |

Observed divergences (pristine → mutant), verbatim:

- **preamble-bypass** (mutant sha256 `4c02656c7ec2b2f08b4e131ab45b3e67a1191f41be9f17c7fb9e96a843297e71`): `actual-r47-drift`, `fenced`, `commented` each `finding=SF-PREAMBLE exit=1` → `finding=SF-BOX exit=1` (finding-only divergence; boxes are then matched against preamble/fence/comment bytes).
- **trailing-bypass** (`1fe9f9bd73cd54aeacf76142673cba95e15f1e5e710c483b344198eabfe06ddf`): `duplicate`, `extra-prose` each `canonical=0 finding=SF-TRAILING exit=1` → **`canonical=1 finding=SF-CLEAN exit=0`** (two false greens).
- **newline-bypass** (`cf6523377411856276e652a3cce6197a8cc7f212758b9a32ef71dc73500b2f0d`): `missing-file` `SF-NEWLINE exit=1` → `SF-PREAMBLE exit=1`; `crlf` and `no-newline` `SF-NEWLINE exit=1` → **`canonical=1 finding=SF-CLEAN exit=0`** (two false greens, including the CRLF-dressed checklist — the same false-green family round-47 disclosed for C2).
- **box-bypass** (`802184f57301f737e68ddc883a9a189cfd5af935a82b338fe1fb8ae33983cd15`): `wrong-label-0…3` each `SF-BOX exit=1` → **`canonical=1 finding=SF-CLEAN exit=0`** (four false greens; label text is arbitrary once the `- [mark] ` shape matches).
- **evidence-bypass** (`425127c2c48c55dc6b0d8e6e84ba5081fedb38c3c1165cadc0e5cd914b8e1038`): `missing-evidence-0…3` each `SF-EVIDENCE exit=1` → **`canonical=1 finding=SF-CLEAN exit=0`** (four false greens).

**Replay verdict:** 5 of 6 classes reproduce the receipt's divergent-case counts exactly under unique, minimal constructions, each caught via exit-or-finding divergence; the sixth is consistent under one of four candidate readings (§4). Every replayed mutant is killed by the frozen battery — the pre-freeze claim "6/6 caught" is corroborated as re-executable evidence at the class level.

## 4. `label-count` reconciliation — receipt counts are not self-identifying bytes

The receipt names the class but not its edit. Four plausible single-anchor readings, all actually run:

| candidate construction | divergent cases | count |
|---|---|---|
| **A** — final `return 'SF-CLEAN'` → `return 'SF-TRAILING'` (`3a4ff883eefe897f99ad5f4dd30ca4d0e8f455403811ba2fb353e52a62fe06dd`) | canonical: `SF-CLEAN exit=0` → `SF-TRAILING exit=1` | **1 — matches receipt** |
| B — `for label in LABELS:` → `for label in LABELS[:3]:` (`e0f651dbaa61155f…`) | canonical → `SF-TRAILING`; wrong-label-3: `SF-BOX` → `SF-TRAILING` | 2 |
| C — `for label in LABELS:` → `for label in LABELS + (LABELS[0],):` (`fb401b22c556016f…`) | canonical → `SF-MISSING-BOX`; duplicate, extra-prose: `SF-TRAILING` → `SF-BOX` | 3 |
| D — evidence prefix slice `lines[i][16:]` → `lines[i][17:]` (`6485fc6af9003645…`) | canonical, duplicate, extra-prose, wrong-label-1/2/3 → `SF-POINTER` | 6 |

On the 17-case battery, the only single-fixture-divergent mutation sites are the clean-completion path (reached by `canonical` alone), because every other fixture already died at an earlier check. Naive LABELS-tuple-count edits (B/C) give 2–3, not 1. **Honest statement:** the receipt's `label-count caught=1 divergent_cases=1` is corroborated as a real, catchable defect class, but its exact bytes are not uniquely reconstructable from the frozen receipt; only a clean-path-only reading reproduces the count. This is a receipt-granularity defeat, reported — not silently fixed. (Fix for a future round, not this one: commit each mutant's diff alongside its tally, as round-47 did with `r47-mutbat.py`.)

## 5. Missing mutation classes — four reconstructed mutants **survive** the frozen battery

These classes are absent from the receipt and from the 17 fixtures; each mutant below leaves all 17 cases byte-identical (`caught=0 divergent=0`). Survivors are **coverage findings, not permission to change the contract** — the counter bytes are frozen and were not touched.

| # | missing class | construction | mutant sha256 | survivors | why the battery is blind |
|---|---|---|---|---|---|
| M1 | **pointer-validation bypass** | `if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():` → `if not resolved.is_file():` (root-containment guard dropped) | `6f753822c54fd8fb4a632519125f3ced446c26c2256c0e944d4cdb5d46c69d2d` | 17/17 identical | No fixture ever exercises `SF-POINTER`: every fixture's evidence token is `LOG.md`, inside the root. A mutant that accepts evidence resolving **outside the lane root** grades identically. The same holds for the sibling guards (`is_absolute`, `'..'`, `token != path.as_posix()`). Corroborates R48Review23's note that the committed selftest has no `SF-POINTER` case. |
| M2 | **verifier-independence bypass** | `if mark == 'x':` → `if False:` (`SF-VERIFIER` unreachable) | `11baf9f3abbf0baa300ff5e67b91e6529702cc8bab1e03c6d357df993098c652` | 17/17 identical | No fixture carries an `[x]` mark. Under the mutant, an author's self-attested `[x]` + evidence grades `canonical=1 SF-CLEAN exit=0` — the exact class the claim's own `mechanical_limits` names ("x marks are rejected (independence cannot be established mechanically)"). Nothing in the battery pins that rejection. |
| M3 | **truncation / `SF-MISSING-BOX` branch** | `return 'SF-MISSING-BOX'` → `return 'SF-TRAILING'` | `7f37d8d2e730844852e577faf9d02db72533891aa8935cb1615e253074135197` | 17/17 identical | No fixture truncates the box sequence (a file ending mid-boxes). The branch's finding is unpinned. |
| M4 | **unreadable / strict-decode channel** | `raw.decode('utf-8')` → `raw.decode('utf-8', 'replace')` | `3148d23bf8ee273b9742fd7bfbac21461b9122f41d8b921f33f390baa5dbec21` | 17/17 identical | All 17 fixtures are valid UTF-8, and `missing-file` models an **empty file** (its `"text": ""` → `SF-NEWLINE`), not a failed read. The `OSError`/`UnicodeError` → `SF-UNREADABLE exit=2` channel is never reached, so exit-2/finding mutations there survive. |

**Missing fixture classes (the dual finding):** the battery has no `SF-POINTER`-positive case (absolute path, `..` traversal, outside-root file, missing file), no `[x]`-marked case, no truncated case, and no unreadable/invalid-UTF-8 case. Four checker responsibilities with zero battery witnesses. One harness note: exit-code mutants (`return code` → `return 0`) are caught **only because** the harness records `PROCESS_EXIT` (format visible in `controls/do-nothing.txt`); a stdout-only comparison would pass them.

## 6. Restoration evidence

Detector re-run on the never-mutated pristine copy after all 238 mutant runs (restored/never-touched bytes must behave identically):

| case | pristine after battery | identical to baseline |
|---|---|---|
| canonical | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| wrong-label-0 | `canonical=0 finding=SF-BOX exit=1` | yes |
| missing-evidence-3 | `canonical=0 finding=SF-EVIDENCE exit=1` | yes |

Hashes, before vs after the entire battery:

| bytes | before | after | unchanged |
|---|---|---|---|
| scratch `pristine.py` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | yes |
| production `corpus/instruments/shonen-form.py` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | yes |

All 13 mutant checker bodies lived only at `/fast/scratch/hyaku/kasegi-r48/R48Review08/mut-*.py`; no lane path was ever written by the battery (the checker is read-only by design; fixtures resolve evidence against the lane root read-only).

## 7. Defeats and limits (reported, never silently fixed)

1. **Receipt granularity:** `pre-freeze-mutants.txt` tallies counts without bytes; five classes reconstruct uniquely, `label-count` does not (§4). The mutation-testing claim is re-executable at class level, not byte level.
2. **Four survivor classes** (§5) — pointer guards, `[x]`/`SF-VERIFIER`, `SF-MISSING-BOX`, unreadable/exit-2 — plus four missing fixture classes. The 17+6 finiteness is already named in the claim's `mechanical_limits`; this seat adds the *specific* uncovered responsibilities.
3. **Baseline semantics:** the `missing-file` fixture is an empty file (`SF-NEWLINE`), not a missing path; the battery's name is misleading even though its expectation row is internally consistent.
4. **Counter/command id:** the tasking's `3546f708…` is the freeze commit id, not the sha256 of `claims.json` (`b8022cdf…` per `freeze.txt`, observed identical here). No action taken; recorded to prevent hash confusion in later seats.
5. `HEAD` advanced during the wave (`3d7e042…` cited by early probe reports → `40b6b3f7…` at my replay). The battery's findings are insensitive to that drift; the drift itself is integration-owned, not judged here.
6. **No counter was hardened, no fixture added, no receipt rewritten** — frozen bytes are frozen. Everything above is evidence about coverage, not a predicate change.

## 8. Summary verdict

- Baseline: pristine checker 17/17 vs `controls/pre-freeze-fixtures.txt` — **conclusive**.
- Six receipt classes: **6/6 KILLED** on independent replay (counts 3, 2, 3, 4, 4 match exactly; `label-count` matches under the unique count-consistent construction, candidate A).
- Missing classes: **4 SURVIVED** probe mutants (pointer-containment, x-verifier, missing-box, decode/exit-2) — each 0/17 divergent, each a coverage finding for the battery, disclosed for the integrator (KasegiR48) to weigh; no bytes changed.
- Restoration: hash-proven (§6). Production, siblings, git/jj state untouched. Scratch removed after this report was saved.

**Exact commands of record:**

```sh
# setup (see §1)
python3 /fast/scratch/hyaku/kasegi-r48/R48Review08/replay.py
# per-case detector invocation (238 runs):
python3 <checker-variant.py> --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Review08/fixtures/<case>.md
```

Full per-run matrix and machine summary were saved at `battery-matrix.txt` and `summary.json` inside the scratch dir and are embedded in this report before scratch removal.
