# ExecCensusFinal — C2 counters on quiescent bytes + census/junk-row controls

- Seat: ExecCensusFinal (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Answering model: `opencode-go/deepseek-v4.1-flash` (runtime route table; no model passed to any tool).
- Lane HEAD during every run: `eecad59db166e0626ca2472e96ea48bc28a35153` (wave-1 integration commit). `git status --porcelain corpus/` printed nothing before and after the runs; the untracked paths under `.ufo/waves/round-31/` were the pre-existing `wave1.ready` / `wave2.ready` markers plus the `wave2/` receipt directory, and this seat's only write there is this receipt.
- Write scope exercised: this receipt only. No lane byte outside this file was written; every instrument/corpus measurement below is read-only. Scratch trees lived in `/tmp/ecf/`.
- Gate: `.ufo/waves/round-31/wave1/ExecHarnessC2.md` existed before the first measurement (16.9 kB, mtime shown by `ls -la .ufo/waves/round-31/wave1/` in the first call). No `BLOCKED:` — no gate file was missing.

## 0. Quiescence — two hash sets, 107 s apart, identical

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && date -u +%FT%TZ && sha256sum <surfaces>
2026-10-26T00:31:28Z
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be  corpus/source-snapshots/round-31/manifest.json
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
d6f25227b6025bb070740cd38c03783092dbcb51340e5c99689c9c1737b8f156  corpus/instruments/knowledge-expected.txt
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ git status --porcelain corpus/          # (empty)

$ (same sha256sum set, 2026-10-26T00:33:15Z)
… all ten lines byte-identical …
$ diff /tmp/ecf/hashes-1.txt /tmp/ecf/hashes-2.txt && echo "hashes_identical=yes"
hashes_identical=yes
```

No discard happened between the two sets; the AFTER column below is measured on these bytes. The C2 surfaces (`README.md`, `SOURCES.md`, the F15 entry, the round-31 manifest, the two harness instruments) are single-writer paths owned by no wave-2 seat, so no peer edit is expected on them during this wave; the hash proof above is the empirical check.

## 1. The seven C2 counter commands — run verbatim from `claims.json`

Extraction was programmatic: `json.load(claims.json)["claims"][1]["counter_commands"]`, each run with `subprocess.run(cmd, shell=True, text=True, capture_output=True)` from a Python process whose cwd was irrelevant because every command begins with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`. The strings below are the frozen strings, not retyped.

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

Labelled values (each label names the probe that produced the number; nothing retyped from a document):

| # | label | value | target | verdict |
|---|---|---|---|---|
| 1 | Frontier rows whose status cell is `admitted` in `corpus/README.md` (`awk` above) | 15 | 15 | met |
| 2 | files in `corpus/knowledge/*.md` with a line matching `^source: S048 ` (trailing space; the landed line is `corpus/knowledge/vendor-third-party-finding-coordination.md:2`) | 1 | 1 | met |
| 3 | lines in `corpus/SOURCES.md` matching the `\| S048 \|` row shape (`corpus/SOURCES.md:54`) | 1 | 1 | met |
| 4 | lines in `corpus/SOURCES.md` matching the general `\| Sxxx \|` row shape | 48 | 48 | met |
| 5 | `sources-census.sh validate` process exit, with findings `W04 S028`, `W04 S029`, `ok` and no `E`/new `W` line | 0 | 0 | met |
| 6 | `frontier-recheck-count.py` summary, including the new `PASS F15 … ids=S048` line (18th of 18) | `entries=18 pass=18 exit=0` | same + `PASS F15` | met |
| 7 | `source-recheck.py --manifest round-31 --source S048` process exit, 8 `OK occurrences=1` assertions | 0 | 0 | met |

No value missed its frozen target. Every measured surface is at the digest recorded in §0.

## 2. Frozen contract census — seven labelled commands in the block, all run before and after

Locator: fleet `CORPUS.md:131` heading `### Census — run from the lane root (tested 2026-10-19 on a synthetic table)`, command block `CORPUS.md:133-148`. The block carries **seven** labelled commands (rows, malformed rows, tier histogram, status histogram, duplicate ids, enum violations + tier inflation, mined rows with missing `used-by` paths). The item says "six"; the block has seven, so all seven were run and reported — the count discrepancy is recorded here as an observation, not a defect claim. Commands are quoted from the block verbatim (the scratch/base column ran the same text against `/tmp/ecf/rootbase/kasegi-shokunin`).

BEFORE (base bytes, re-derived in scratch from `git archive b374febbb33ccadade78a787279707fd5d2e6e1d`; `/tmp/ecf/census-contract-base.txt`):

```
### base-1 rows
47
### base-2 malformed
0
### base-3 tier
A=44 B=1 C=2
### base-4 status
mined=35 queued=9 rejected=3
### base-5 dup-ids
### base-6 enum+tier-inflation
### base-7 used-by-missing
```

AFTER (live lane, `/tmp/ecf/census-contract.txt`):

```
### C-census-1 rows
48
[exit=0]
### C-census-2 malformed
0
[exit=0]
### C-census-3 tier
A=45 B=1 C=2
[exit=0]
### C-census-4 status
mined=36 queued=9 rejected=3
[exit=0]
### C-census-5 dup-ids
[exit=0]
### C-census-6 enum+tier-inflation
[exit=0]
### C-census-7 used-by-missing
[exit=0]
```

Delta: exactly one row joined the registry (47→48), tier A 44→45, status mined 35→36; every fail-if-nonzero probe (`malformed`, `dup-ids`, `enum+tier-inflation`, `used-by-missing`) is empty in both columns, so the S048 append introduced no shape defect and no dangling `used-by` path.

## 3. Maintained census — frozen before file vs now, plus a re-derived base summary

**3a. Frozen control vs now (the item's comparison).** `census-before.txt` is the claims-freeze run (`# C2 base control … run 2026-10-25T23:12:30Z`, header line; file body is four lines).

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi > /tmp/ecf/census-now.txt 2>&1; echo "exit=$?"
exit=0
$ diff -u .ufo/waves/round-31/census-before.txt /tmp/ecf/census-now.txt
--- .ufo/waves/round-31/census-before.txt
+++ /tmp/ecf/census-now.txt
@@ -1,4 +1,3 @@
 kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
 kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
 kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
-census_exit=0
```

The only diff line is the wrapper `census_exit=0` that the frozen file carries as its last line and a bare `validate` run does not print; the three finding/ok lines are byte-identical. The frozen file's own last line states `census_exit=0`. Therefore: before = `W04` S028 and S029 only, exit 0; after = the same two `W04` lines only, exit 0. No new finding was added by the S048 append.

**3b. Maintained census summary (cross-check, not the frozen control).**

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh --root /tmp/ecf/rootbase kasegi      # base scratch
ERROR: config not found: /tmp/ecf/rootbase/shokunin.conf
ERROR: unknown lane (not a dir, not in conf or root): kasegi
```

The maintained parser resolves lanes through `shokunin.conf` first; copying the fleet config into scratch would copy fleet configuration values, so the scratch columns use the documented `--file` mode instead (`usage` block of `scripts/sources-census.sh` lists `--file PATH` as a specific registry). Live lane keeps the frozen `--root … kasegi` form.

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /tmp/ecf/rootbase/kasegi-shokunin/corpus/SOURCES.md
file	rows	47
file	tier.A	44
file	tier.B	1
file	tier.C	2
file	status.mined	35
file	status.queued	9
file	status.rejected	3
FLEET	rows	47
FLEET	tier.A	44
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	35
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
filemode_census_exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh --root /home/vgpnk/Projects/shokunin kasegi   # live lane
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
census_summary_exit=0
```

| census cell | base `b374febb…` (scratch, `git archive`; cross-check) | frozen `census-before.txt` (at freeze) | after (live lane, §0 digests) |
|---|---|---|---|
| rows | 47 | (not printed by validate) | 48 |
| tier A / B / C / invalid | 44 / 1 / 2 / 0 | — | 45 / 1 / 2 / 0 |
| status queued / mined / rejected / invalid | 9 / 35 / 3 / 0 | — | 9 / 36 / 3 / 0 |
| FLEET.missing | 0 | — | 0 |
| validate findings | W04 ×2, ok | W04 ×2, ok | W04 ×2, ok |
| exit | 0 | 0 | 0 |

Base re-derivation agrees with the frozen control on its only comparable cell (validate findings and exit) and adds the row/status counts the frozen file does not print.

## 4. Junk-row control re-derivation — a bare S048 row with no entry and no capture

Construction (all in `/tmp/ecf/rootjunk/`, never in the lane): copy the `git archive` base tree to `/tmp/ecf/rootjunk/kasegi-shokunin`, then insert one row inside the `## Registry` table (immediately before the `## Paths` heading at line 55, so the maintained parser does not file it as `E12 row outside Registry section`). The exact row appended:

```
| S048 | MSVR junk-row probe — https://www.microsoft.com/en-us/msrc/msvr | docs | A | MSVR third-party intake routes | page, opened 2026-10-25 | Junk-row control: registry row with no knowledge entry and no capture | mined | 2026-10-25 | 90d | — |
```

Shape check and counters:

```
$ awk -F'|' '/^\|[[:space:]]*S048[[:space:]]*\|/ {print "NF="NF}' corpus/SOURCES.md
NF=13

$ cd /tmp/ecf/rootjunk/kasegi-shokunin && … the seven C2 probes …
frontier_admitted=14
entries_citing_S048=0
rows_S048=1
registry_rows=48

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/ecf/rootjunk/kasegi-shokunin/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W03	S048 mined but unused
file	ok	/tmp/ecf/rootjunk/kasegi-shokunin/corpus/SOURCES.md
junk_census_exit=0

$ cd /tmp/ecf/rootjunk/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
manifest UNAVAILABLE reason=missing
junk_recheck_exit=2
```

(One early, discarded attempt placed the row after `## Paths` and produced `E12 S048 row outside Registry section`, exit 1; that is a construction error on my side, fixed by inserting inside the Registry table — the run above is the valid one. These blocks are transcribed from this session's captured command output; on review the first draft mistyped the S029 URL, and it was corrected against the captured run before commit — the two `W04` lines are byte-identical to the live-lane run in §1 item 5 apart from the leading lane label.)

Harness in the junk scratch. The base entries' `recheck:` lines begin `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`; from a scratch root they would otherwise execute against the real lane. In the scratch copies only, that absolute prefix was rewritten to `cd /tmp/ecf/rootjunk/kasegi-shokunin &&` (a path-only substitution; entry text, source ids and manifest names unchanged), so the harness measures the junk tree end-to-end:

```
$ (grep -rl '^recheck: cd /home/…/kasegi-shokunin &&' corpus/knowledge/ | wc -l)   # before retarget
42
$ python3 corpus/instruments/frontier-recheck-count.py
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
entries=17 pass=17 exit=0
junk_harness_exit=0
```

Junk-row verdict, re-derived:

| cell | claim's do-nothing/junk-row expectation | measured in junk scratch |
|---|---|---|
| frontier admitted | 14 | 14 |
| entries citing S048 | 0 | 0 |
| S048 registry rows | 1 (row exists) | 1 |
| registry rows | 48 | 48 |
| census | flags the unused mined row | `W03 S048 mined but unused`, exit 0 |
| harness | 17/17 | `entries=17 pass=17 exit=0` |
| source-recheck S048 | cannot pass without a capture | `manifest UNAVAILABLE reason=missing`, exit 2 |

Conclusion: a registry row alone moves only the registry-row count. Frontier stays 14, entries citing S048 stay 0, the harness stays 17/17 (no F15 row admitted), the census names the row `W03 … mined but unused`, and S048 has no capture to recheck. The junk row cannot meet the C2 predicate; the predicate's cells therefore carry the work claimed for them.

Base do-nothing re-derivation in the same scratch form (`/tmp/ecf/rootbase`, base `git archive` bytes, recheck prefix retargeted in scratch copies only) printed `frontier_admitted=14`, `entries_citing_S048=0`, `rows_S048=0`, `registry_rows=47`, base census `W04 ×2 + ok` exit 0, `entries=17 pass=17 exit=0`, `manifest UNAVAILABLE reason=missing` exit 2 — matching the frozen `c2-controls/before.txt` cell for cell (`frontier_admitted=14`, `entries_citing_S048=0`, `rows_S048=0`, `registry_rows=47`, `census_exit=0`, `entries=17 pass=17 exit=0`, `manifest UNAVAILABLE reason=missing`, `recheck_exit=2`).

## 5. Risks / notes for the integrator

1. **Nothing outside this receipt was written in the lane.** Scratch: `/tmp/ecf/rootbase`, `/tmp/ecf/rootjunk`, `/tmp/ecf/*.txt`. No git/jj mutation (only read-only `git rev-parse`, `git log`, `git status`, `git archive`). No pacman, no network fetch, no tool install (nothing to record under the tooling rule). No `agent://all` message.
2. **Scratch census uses `--file` mode, not `--root` + lane id.** The lane id path requires `shokunin.conf`; copying fleet configuration into scratch was avoided deliberately. The live lane counter in §1/§3 still uses the frozen `--root … kasegi` form, so the AFTER column is the real command.
3. **Harness scratch runs retarget the `recheck:` `cd` prefix.** Without that, the entries' absolute lines would read the live lane from a scratch root. The retarget is confined to `/tmp/ecf/…/corpus/knowledge/*.md` copies and changes no source id, manifest name or assertion; the live-lane harness run in §1 is untampered.
4. **The frozen contract census block has seven labelled commands, not six.** All seven were run; recorded as a count observation only.
5. **Quiescence evidence is hash-based, not promise-based.** If any C2 surface is written after `2026-10-26T00:33:15Z`, the AFTER column must be re-measured with the seven commands in §1; this receipt speaks only for the digests in §0.
6. **Scope.** These runs measure the C2 counter cells, the junk-row control and the census. They do not judge the F15 entry against `QUALITY.md` Q1–Q10, do not run the C1 limb ledger/counter, and say nothing about whether the capture's upstream URL still serves the same page (the recheck reads local pinned bytes only, as `source-recheck.py`'s docstring states).
