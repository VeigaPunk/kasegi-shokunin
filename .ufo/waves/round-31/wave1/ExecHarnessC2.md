# ExecHarnessC2 receipt — round 31, C2 counter harness on quiescent bytes

- Seat: ExecHarnessC2 (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Answering model: `devin/deepseek-v4-1-flash` (config route table; no model passed to any tool).
- Lane HEAD during every run: `8a8916c7043bd873d191b30dd1744b241b91f4d9` (base `b374febbb…` + claims-freeze `738a779…` + wave-1 spec `8a8916c…`; the C2 deliverables are uncommitted working-tree bytes, as in the frozen claims).
- Write scope exercised: this receipt only. No instrument, corpus, README, SOURCES, knowledge, manifest or claims byte was written by this seat; all runs are read-only over the lane and the fleet census script. Scratch lived in `/tmp/ehc2/`.
- Item gate (all five receipts present before any measurement; mtimes are lane-local, UTC+3 host clock):

| gate | receipt | size | mtime |
|---|---|---|---|
| capture + manifest | `.ufo/waves/round-31/wave1/ExecCapManifest.md` | 8057 B | 2026-10-25T20:32:54Z |
| registry row S048 | `.ufo/waves/round-31/wave1/ExecRegistryAppend.md` | 18427 B | 2026-10-25T20:43:37Z |
| knowledge entry | `.ufo/waves/round-31/wave1/ExecEntryF15.md` | 17592 B | 2026-10-25T20:45:44Z |
| expected list | `.ufo/waves/round-31/wave1/ExecExpectedList.md` | 8306 B | 2026-10-25T20:44:41Z |
| F15 README row | `.ufo/waves/round-31/wave1/ScribeReadmeF15.md` | 10156 B | 2026-10-25T20:45:06Z |

Waiting method (bounds 9): `until`-style poll capped at 260–280 s per call, four calls; no busy loop. No `BLOCKED:` — every gate file appeared.

Gate precision (one late rewrite, measured): `ExecEntryF15.md` was still present at poll 3 but was rewritten at `20:45:44Z` lane-local (`23:45:44Z`), 38 s after my first counter run at `23:45:06Z`. The rewrite touched the receipt only: its declared entry digest (`1f16e371…bb692bb`, `ExecEntryF15.md:6`) equals the digest I measured before (`23:45:06Z`) and after (`23:47:11Z`, `23:49:29Z`), and the entry file's mtime stayed `20:41:30Z`. No measured byte changed across that rewrite.

## 0. Quiescence — two identical digest sets, 125 s apart

Every C2 surface was digested twice with no intervening write. Both runs printed the same eight digests, so the AFTER column below is measured on bytes that did not move under it (M30-3).

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && date -u +%FT%TZ && sha256sum …
2026-10-25T23:45:06Z
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be  corpus/source-snapshots/round-31/manifest.json
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
d6f25227b6025bb070740cd38c03783092dbcb51340e5c99689c9c1737b8f156  corpus/instruments/knowledge-expected.txt
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py

$ (same sha256sum set, 2026-10-25T23:47:11Z)
1f16e371…bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
2001ad77…c67e55  corpus/source-snapshots/round-31/S048.txt
b80f7f92…a2f87be  corpus/source-snapshots/round-31/manifest.json
5a03c696…295f6f5  corpus/SOURCES.md
d9865b2e…2146f98  corpus/README.md
d6f25227…7b8f156  corpus/instruments/knowledge-expected.txt
aa60b581…d5dc0893  corpus/instruments/frontier-recheck-count.py
fd2e01e8…b5b9c003  corpus/instruments/source-recheck.py
```

A third digest set taken after this receipt was written (`2026-10-25T23:49:29Z`) re-measured the seven mutable surfaces (all but the immutable `S048.txt` capture) and printed the same digests byte-for-byte, so no measured surface moved during the seat's work.

Last write to any measured file before the run: `corpus/knowledge/vendor-third-party-finding-coordination.md`, 2026-10-25T20:41:30Z lane-local (≈23:41:30Z), i.e. ~3.5 min of quiet before the first counter run.

Cross-check against the owners' own receipts (no digest retyped from another document — these are my own `sha256sum` lines, compared to theirs):

| surface | my digest | owner receipt line |
|---|---|---|
| entry | `1f16e371…bb692bb` | `ExecEntryF15.md:6`, `ExecExpectedList.md:25` — same |
| `corpus/SOURCES.md` | `5a03c696…295f6f5` | `ExecRegistryAppend.md` §8 `sha256sum` — same |
| `corpus/README.md` | `d9865b2e…2146f98` | `ScribeReadmeF15.md:177` `df04b049…` → `d9865b2e…` — same |
| `knowledge-expected.txt` | `d6f25227…7b8f156` | `ExecExpectedList.md:90` — same |
| `S048.txt` | `2001ad77…c67e55` | `ExecCapManifest.md` §1 — same |

## 1. Do-nothing control vs AFTER

Base control is the frozen one, read from the claims-freeze bytes (not re-run by me, not compared to any in-flight reading): `.ufo/waves/round-31/c2-controls/before.txt`, `# C2 base control (base b374febb…), run 2026-10-25T23:12:30Z` — `frontier_admitted=14`, `entries_citing_S048=0`, `rows_S048=0`, `registry_rows=47`, `census_exit=0`, `entries=17 pass=17 exit=0`, `manifest UNAVAILABLE reason=missing`, `recheck_exit=2`.

| C2 predicate cell | base `b374febb…` (frozen control) | AFTER (23:45–23:47Z, digests §0) | target | verdict |
|---|---|---|---|---|
| Frontier admitted rows (F15) | 14 | 15 | 15 | met |
| knowledge entries citing S048 on a `source:` line | 0 | 1 | 1 | met |
| S048 rows in `corpus/SOURCES.md` | 0 | 1 | 1 | met |
| registry rows | 47 | 48 | 48 | met |
| sources census `validate` exit | 0 (W04 ×2) | 0 (W04 ×2, no new E/W) | 0 | met |
| `frontier-recheck-count.py` | `entries=17 pass=17 exit=0` | `entries=18 pass=18 exit=0`, `PASS F15 … ids=S048` | 18/18 + `PASS F15` | met |
| `source-recheck.py` on round-31 manifest, `--source S048` | `manifest UNAVAILABLE reason=missing`, exit 2 | 9 OK lines, `recheck_exit=0` | 0 | met |

No cell missed its target. Nothing was messaged: no fix is owed by any seat for this item.

## 2. The seven C2 counter commands, copy-run verbatim from `claims.json`

Each command was extracted programmatically from `.ufo/waves/round-31/claims.json` → `claims[1]` (C2) → `counter_commands` and run with `shell=True` from the lane root, so the strings below are the frozen strings, not retyped. Output is the command's stdout+stderr.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
15
[exit=0]

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -lE '^source: S048 ' corpus/knowledge/*.md | wc -l
1
[exit=0]

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md
1
[exit=0]

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
48
[exit=0]

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
[exit=0]

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
entries=18 pass=18 exit=0
harness_exit=0
[exit=0]

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "recheck_exit=$?"
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
recheck_exit=0
[exit=0]
```

Value labelling (one label per measured value, none retyped from a document):
- `15` — Frontier rows whose status cell is `admitted` in `corpus/README.md` at digest `d9865b2e…`; base control 14. The 15th row is `corpus/README.md:309` (`| F15 | … | admitted | knowledge/vendor-third-party-finding-coordination.md | S048 | …`).
- `1` — files under `corpus/knowledge/*.md` carrying a line matching `^source: S048 ` (trailing space: the landed entry writes `source: S048 — https://…`). Base 0.
- `1` — lines in `corpus/SOURCES.md` matching the row shape `| S048 |`. Base 0. The row is `corpus/SOURCES.md:54`.
- `48` — lines matching the general `| Sxxx |` row shape. Base 47.
- `census_exit=0` with exactly the two pre-existing `W04` warnings (S028, S029) and no `E`/new `W` finding. Base control also `census_exit=0` with the same two W04 lines, so the append added no finding.
- `entries=18 pass=18 exit=0` — the harness's own binding rule (A–D) passed on every admitted row; the `PASS F15 … ids=S048` line is the new row, and its `--source` set equals the entry's own `source:` set (the harness would print a mismatch, not PASS).
- `recheck_exit=0` with 8 assertion `OK` lines — every quote exactly-once in the pinned capture (`occurrences=1`), the sha256 pin matches, the record's `path` stem equals its `id` (no `stem-mismatch`).

Independent second measurement of the registry count (not a claim counter, used as a cross-check): the census's own parser counts rows, and it agrees:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh --root /home/vgpnk/Projects/shokunin kasegi
kasegi	rows	48
kasegi	tier.A	45
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	36
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	48
FLEET	tier.A	45
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	36
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
census_census_exit=0
```

`rows 48` from the census parser equals the grep count `48`; `FLEET.missing 0` and `tier.invalid 0` mean the new row is well-formed and every `used-by` path exists (the census `E11` class would otherwise fire).

## 3. Foreign-cwd run of the entry's own `recheck:` line

The line was read out of the landed entry (`corpus/knowledge/vendor-third-party-finding-coordination.md:4`), the `recheck: ` prefix stripped by parameter expansion, syntax-checked, then executed from the lane root and from `/`. Both runs print byte-identical output.

```
$ line=$(grep -m1 '^recheck:' corpus/knowledge/vendor-third-party-finding-coordination.md); line=${line#recheck: }; printf 'LINE=%s\n' "$line"
LINE=cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048   # 8 assertions, every quote exactly-once in the pinned capture; a captured-source comparison, not a fresh network verification
$ bash -n -c "$line"; echo "syntax_exit=$?"
syntax_exit=0
$ bash -c "$line" > /tmp/ehc2/recheck-laneroot.txt 2>&1; echo "laneroot_exit=$?"
laneroot_exit=0
$ ( cd / && bash -c "$line" ) > /tmp/ehc2/recheck-foreign.txt 2>&1; echo "foreign_exit=$?"
foreign_exit=0
$ sha256sum /tmp/ehc2/recheck-laneroot.txt /tmp/ehc2/recheck-foreign.txt
09946c9509a4f525e1e04f591cb35c9f447c32dec8d3d84ee7c617b7961051d5  /tmp/ehc2/recheck-laneroot.txt
09946c9509a4f525e1e04f591cb35c9f447c32dec8d3d84ee7c617b7961051d5  /tmp/ehc2/recheck-foreign.txt
$ diff -u /tmp/ehc2/recheck-laneroot.txt /tmp/ehc2/recheck-foreign.txt && echo "outputs_identical=yes"
outputs_identical=yes
$ cat /tmp/ehc2/recheck-foreign.txt
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
```

The line is cwd-independent by its own construction (`cd <lane> && …`) and its output bytes are identical from `/`; it also satisfies the audit's `(c) paths` shape (it names `corpus/source-snapshots/round-31/manifest.json`, which exists) and `(d) cdroot` (the `cd` target is the audited lane root).

## 4. In-flight readings — recorded, not used (M30-3)

One earlier snapshot was taken at 2026-10-25T23:31:56Z while peers were still writing (manifest had just landed at 23:31:21Z; entry, README row and registry row had not). Its values — `admitted=14`, `citing_S048=0`, `S048_rows=0`, `registry_rows=47`, `harness 17/17`, and a `recheck_exit=0` already green on the just-landed manifest — are a mid-wave partial state. They are **not** compared to the AFTER column and are not cited as a before column; the base control in §1 is the frozen `c2-controls/before.txt` instead.

Also recorded for honesty: in that same 23:31:56Z block, the admitted-row `awk` printed `0` once. The identical command printed `15` (and `14` before the append) on every later invocation, including both grouped and plain forms, so the `0` is treated as an in-flight read of a file being rewritten and is not used as a measurement. No defect is claimed against the counter, and no seat was messaged.

## 5. Risks / notes for the integrator

1. **Instrument drift after my run.** Measured by me at `2026-10-25T23:52:09Z` against the base blobs (`git show b374febb…:corpus/instruments/<f> | sha256sum`):
   - `source-recheck.py`: base `33602a9d…` → live `fd2e01e8…` (mtime `20:37:16Z` lane-local), i.e. already changed by the C1 SR-limb seat before my run.
   - `frontier-recheck-count.py`: base `aa60b581…` → live `aa60b581…`, unchanged.
   - `recheck-audit.py` (not mine to measure, recorded for the C1 seats' cross-check): base `3fc0d751…` → live `5d4842da…`.
   My `recheck_exit=0` and `entries=18 pass=18` hold for the live bytes above. If ExecSRLimbs or ExecFRLimbs changes either instrument again before the L1 commits, the C2 harness cell must be re-run (the two commands are §2 items 6 and 7); my receipt cannot speak for later bytes.
2. **Uncommitted bytes.** Every C2 surface is a working-tree change on top of `8a8916c`; the digests in §0 are the ones the L1 should expect to commit. If the commit changes any of them, the AFTER column is stale.
3. **Capture is not refetchable.** `S048.txt` line 2 is a per-request Trace Id (`ExecCapManifest.md` §1); the pin binds the committed bytes only. My `recheck_exit=0` reads local files and says nothing about current upstream availability — the same limit `source-recheck.py`'s own docstring states.
4. **Scope of what I measured.** These runs verify the C2 predicate's counter cells and the entry's own recheck line. They do **not** judge the entry against `QUALITY.md` Q1–Q10, do not check that F15 is not a restatement of F06/F10, and say nothing about the C1 limb ledger — those belong to `RevSourceBar`, `CritC2Kill` and the C1 seats respectively.

## 6. Tooling

No install or upgrade this seat; no pacman transaction (host-wide pause respected); no network fetch (all seven counters plus the foreign-cwd run read local bytes and the fleet census script). Scratch files stayed in `/tmp/ehc2/`; nothing was written into the lane tree except this receipt, and no git/jj mutation was run (only read-only `git rev-parse`, `git log`, `git status`).
