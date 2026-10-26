# ExecHarnessC2 — round-33 wave 1: final C2 counter run on quiescent bytes

Seat: `ExecHarnessC2` (executor, leaf). Judged on `coverage` / `depth:verifiability`.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`, claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`).
Every value below is a copy-run output; no number is retyped from memory. Commands with an absolute `cd` prefix were also run from a foreign cwd (§2).

## 0. Preconditions and quiescence

Precondition set named in the item: the F16 README row landed (`ScribeReadmeF16.md`), the entry / round-32 manifest / registry rows exist, `ExecExpectedList` is done. Polled with `until [ -s <file> ]`-style waits (20 s interval, cap 30 min); READY at `2026-10-26T01:31:01-03:00`.

```

.ufo/waves/round-33/wave1/ScribeReadmeF16.md 11770 bytes mtime=2026-10-26T01:27:46
.ufo/waves/round-33/wave1/ExecExpectedList.md 10766 bytes mtime=2026-10-26T01:31:09
.ufo/waves/round-33/wave1/ExecCaptureBinding.md 17675 bytes mtime=2026-10-26T01:29:26
.ufo/waves/round-33/wave1/ExecManifest32.md 10479 bytes mtime=2026-10-26T01:25:53
.ufo/waves/round-33/wave1/ExecManifestUpgrade.md 15638 bytes mtime=2026-10-26T01:24:04
.ufo/waves/round-33/wave1/ExecRegistryAppend.md 22560 bytes mtime=2026-10-26T01:29:50
.ufo/waves/round-33/wave1/ExecEntryF16.md 19836 bytes mtime=2026-10-26T01:29:34
corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md 24492 bytes mtime=2026-10-26T01:28:10
corpus/source-snapshots/round-32/manifest.json 5753 bytes mtime=2026-10-26T01:18:46
corpus/instruments/capture-binding-check.py 21527 bytes mtime=2026-10-26T01:23:14
```

Quiescence, not merely presence: the 16 files I measure (README, SOURCES, the entry, the nine manifests, three instruments, `knowledge-expected.txt`) were digested twice 75 s apart before any counter ran, again after the last one, and a third time before this seat yielded. The last prerequisite receipt to finish (`ExecExpectedList.md`, mtime 01:31:09) preceded the first quiescence window (01:31:27).

```
$ sha256sum <16 files> > digests-t0.txt ; sleep 75 ; sha256sum <16 files> > digests-t1.txt
2026-10-26T01:31:27-03:00
2026-10-26T01:32:42-03:00
QUIESCENT: digests identical across 75s
16
```

## 1. C2 counter commands from `claims.json` — copy-run verbatim

Nine commands, read out of `.ufo/waves/round-33/claims.json` (`claims[1].counter_commands`) and executed one per `bash -c` from the lane; the transcript below is the unedited output, `[outer_rc=N]` is the wrapping shell's status.

```

### C2.[1] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
16
[outer_rc=0]

### C2.[2] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && echo -n 'S049='; grep -lE '^source: S049 ' corpus/knowledge/*.md | wc -l; echo -n 'S050='; grep -lE '^source: S050 ' corpus/knowledge/*.md | wc -l
S049=1
S050=1
[outer_rc=0]

### C2.[3] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md
1
[outer_rc=0]

### C2.[4] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S050[[:space:]]*\|' corpus/SOURCES.md
1
[outer_rc=0]

### C2.[5] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
50
[outer_rc=0]

### C2.[6] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
[outer_rc=0]

### C2.[7] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"
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
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
entries=19 pass=19 exit=0
harness_exit=0
[outer_rc=0]

### C2.[8] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049; echo "recheck49_exit=$?"
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
recheck49_exit=0
[outer_rc=0]

### C2.[9] cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050; echo "recheck50_exit=$?"
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
recheck50_exit=0
[outer_rc=0]
```

Labelled values against the C2 kill rule:

| # | measurement | target | measured | verdict |
|---|---|---|---|---|
| 1 | Frontier rows with status `admitted` | 16 (15 -> 16, F16) | `16` | met |
| 2 | knowledge entries citing `source: S049 ` / `source: S050 ` | 1 / 1 | `S049=1` `S050=1` | met |
| 3 | `S049` rows in registry | 1 | `1` | met |
| 4 | `S050` rows in registry | 1 | `1` | met |
| 5 | registry rows total | 50 (48 -> 50) | `50` | met |
| 6 | `sources-census.sh validate --root ... kasegi` | exit 0; only `W04 S028`, `W04 S029`, `ok` | `census_exit=0` with exactly those three lines, no E and no new W | met |
| 7 | `frontier-recheck-count.py` harness | `PASS F16 ... ids=S049,S050`, `entries=19 pass=19 exit=0` | `PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0`, `entries=19 pass=19 exit=0`, `harness_exit=0` | met |
| 8 | `source-recheck.py --source S049` | exit 0, each assertion exactly-once-or-anchored | `S049:sha256 OK`, `Q1`-`Q8` `OK occurrences=1`, `recheck49_exit=0` | met |
| 9 | `source-recheck.py --source S050` | exit 0, same | `S050:sha256 OK`, `Q1`-`Q6` `OK occurrences=1`, `recheck50_exit=0` | met |

Assertion count observed on the rounds: S049 8 quotes + 1 capture digest, S050 6 quotes + 1 capture digest = 14 quote assertions, matching the entry's own `recheck:` comment ("S049 Q1-Q8, S050 Q1-Q6"). Every one reports `occurrences=1`, i.e. the Q9 duplicate-occurrence rule was not needed to pass and no anchor relaxation was invoked.

## 2. Foreign-cwd run of the entry's own `recheck:` line

The line was extracted verbatim from `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, syntax-checked, then executed with the parent process in `/` and again in `/tmp`:

```

## entry: corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
## extracted recheck line (verbatim)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050   # 14 assertions on the round-32 manifest (S049 Q1-Q8, S050 Q1-Q6), each `occurrences=1` under source-recheck.py's declared normalization; the strings marked hand-measured below are not manifest-bound; a captured-source comparison, not a fresh network verification

### bash -n -c "<line>"
rc=0
stdout:

stderr:


### cd / && bash -c "<line>"   (process cwd=/)
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
exit=0

### cd /tmp && bash -c "<line>"   (process cwd=/tmp)
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
exit=0
```

`bash -n` rc=0, and the line exits 0 from `/` and `/tmp`: the entry carries its own `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix, so the harness (which runs the line with `cwd=root`) and a foreign-cwd reader get the same result. The `&&` chain means the S050 half only runs when S049 exits 0 — visible in the output order (S049 block, then S050 block).

## 3. Base-vs-now on fixed base bytes (the increments, measured rather than quoted)

Same shell shapes run against the committed base snapshot `690b69da` via `git show` (read-only) and against the working tree:

```

## base-vs-now on the same command shapes (base = 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4)
base_frontier_admitted=15
now_frontier_admitted=16
base_registry_rows=48
now_registry_rows=50
base_S049_rows=0
now_S049_rows=1
base_S050_rows=0
now_S050_rows=1
base_knowledge_tree_lines_matching_chinese-crowdsourced=0   # `git show <base>:corpus/knowledge/` listing; the base has no such entry path
base_entry_file_present=no
## context: manifest record shape (C1 rule C data, not my claim)
corpus/source-snapshots/round-23/manifest.json records=4 url=4 fetched_utc=0 archival_true=4
corpus/source-snapshots/round-24/manifest.json records=19 url=19 fetched_utc=0 archival_true=19
corpus/source-snapshots/round-25/manifest.json records=5 url=5 fetched_utc=0 archival_true=5
corpus/source-snapshots/round-26/manifest.json records=1 url=1 fetched_utc=0 archival_true=1
corpus/source-snapshots/round-28/manifest.json records=2 url=2 fetched_utc=0 archival_true=2
corpus/source-snapshots/round-29/manifest.json records=3 url=3 fetched_utc=0 archival_true=3
corpus/source-snapshots/round-30/manifest.json records=3 url=3 fetched_utc=0 archival_true=3
corpus/source-snapshots/round-31/manifest.json records=1 url=1 fetched_utc=0 archival_true=1
corpus/source-snapshots/round-32/manifest.json records=2 url=2 fetched_utc=2 archival_true=0
```

So the C2 increments hold on bytes: admitted 15 -> 16, registry 48 -> 50, S049 0 -> 1, S050 0 -> 1, entry file absent at base -> present (base-side zero for the citing-entry count follows from the entry path not existing at base, not from a `grep` over an absent file). The 38 legacy manifest records now carry `url` and `archival: true` (4+19+5+1+2+3+3+1 = 38); the two round-32 records carry `url` and `fetched_utc` and no archival flag. That shape is C1's data; reported here only as context for the round-32 manifest existing and being populated (C2's surface), not as a C1 verdict.

## 4. Bookend digests (every measured byte unchanged during the run)

```

## bookend: digests before my runs (t1) vs after (t2)
IDENTICAL: measured bytes unchanged across the counter runs

3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70  corpus/source-snapshots/round-23/manifest.json
77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3  corpus/source-snapshots/round-24/manifest.json
251cb5b2c1bacb5ba47758fb60e41aaf1e367ae11df05ed19886361b35f7aea2  corpus/source-snapshots/round-25/manifest.json
1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247  corpus/source-snapshots/round-26/manifest.json
89f51e052eaefcb56a880d48e6778ee88b46e55cafde1275c69992304e7ef75e  corpus/source-snapshots/round-28/manifest.json
b24a485ff3d2d03abe3ef2022e211c7092bcf7509f3913cfa44145216e2c8d15  corpus/source-snapshots/round-29/manifest.json
8aacf77cf2f3d9c7912eea419a05e10604959b2faacb4ae3b0e097f8ab81f94b  corpus/source-snapshots/round-30/manifest.json
5fa37fd7249d043af1e36f98a549ee4ac8d6181e29f5def78116d3c637cb50e8  corpus/source-snapshots/round-31/manifest.json
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
```

Third digest immediately before yielding, to prove the bytes I report are the bytes the lane still holds:

```
$ date -Is ; sha256sum <16 files> > digests-t3.txt ; diff -q digests-t2.txt digests-t3.txt
2026-10-26T01:33:51-03:00
STABLE since the run: t2 == t3
```

## 5. Misses and handoffs

None. All nine C2 counter commands met their kill-rule targets on quiescent bytes, so no defect message was due and none was sent. Two things a later seat may still move, which would force a re-run and are outside my write scope:

- `RevRowS050`, `RevEntryF16`, `RevQuoteSweep`, `RevTranslation` were still running when I measured; reviewers are read-only, but a defect they route back through an owning scribe would change `corpus/SOURCES.md` or the entry. The digests in §4 are the exact bytes I measured, so a later change is detectable by re-hashing those 16 paths.
- `ExecCensusAfter` owns the six contract census commands and the `diff -u` against `census-before.txt`; I ran only the frozen C2 census command (#6) and make no census-table claim.

## 6. Scope, hygiene, authority

- Wrote one path: this receipt. No git/jj mutation, no commit, no network fetch, no credential material read or echoed (`SentCred`/Q6 domain untouched).
- No tool install or upgrade was needed; nothing was installed.
- Scratch `/fast/scratch/hyaku/kasegi-r33/ExecHarnessC2/` (raw transcripts `c2-counters.txt`, `foreign-cwd.txt`, `base-vs-now.txt`, `digests-t0/t1/t2.txt`, `quiescence-bookend.txt`) removed before this seat yielded; every value above is reproduced inline.
`