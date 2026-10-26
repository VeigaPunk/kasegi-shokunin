# MutCounterBase — C2 do-nothing control on base bytes (round 35)

- Seat: MutCounterBase (mutation-tester, leaf; no subagents dispatched)
- Round: kasegi-shokunin 35, hyaku run 8, dispatched by L1 agent KasegiR35
- Lane repo (only write scope): `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Lane base: `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit under test: `617496b9c6e92bc671e7e78b83df69a04470d0e9`
- Assignment: prove the C2 counters cannot be met by a do-nothing control on base bytes — export `git archive 617496b9` to scratch, run the five C2 counting commands plus source-recheck S052 there, and require every probe to print the BEFORE values from `.ufo/waves/round-35/claims.json` (17 / 51 / 0 / 0 / entries=20 pass=20 / manifest-missing exit 2).
- Mutant under test: the do-nothing control itself — pristine base bytes at `617496b9`, no C2 work applied. Expected detector: the six C2 probes. A probe printing an AFTER value on base bytes would mean the counter is vacuous (claim met without work); every probe printing BEFORE means the counter discriminates.

## Report

### 1. Base-byte export and provenance

Scratch root: `/fast/scratch/hyaku/kasegi-r35/MutCounterBase` (created with `mkdir -p`; deleted in §6).

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git rev-parse 617496b9c6e92bc671e7e78b83df69a04470d0e9
617496b9c6e92bc671e7e78b83df69a04470d0e9
$ git rev-parse '617496b9c6e92bc671e7e78b83df69a04470d0e9^{tree}'
1fc4f63e8c75765c1a4b9e35d36f23ebdb78da25
$ git archive 617496b9c6e92bc671e7e78b83df69a04470d0e9 > "$S/base.tar"
$ sha256sum "$S/base.tar"
a008adf24ed9fa5c93e35b51c84b2dc2df0fe60722098a481f222ac71782467a  /fast/scratch/hyaku/kasegi-r35/MutCounterBase/base.tar
$ tar -xf "$S/base.tar" -C "$S/base"
$ find "$S/base" -type f | wc -l
6934
$ cd "$S/base" && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum
acb28d7d272e00c16b3f625ecda72c02b89bd2fafeeb593f2c3502e55f985acb  -
```

Key-file provenance — extracted bytes vs `git cat-file blob 617496b9:<path>` (all OK, so the probes ran on the frozen commit's bytes, not on working-tree bytes):

```
OK corpus/README.md sha256=876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29
OK corpus/SOURCES.md sha256=4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6
OK corpus/instruments/frontier-recheck-count.py sha256=1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249
OK corpus/instruments/source-recheck.py sha256=fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003
```

`python3 --version` → `Python 3.14.8`. No tools installed (grep/coreutils/git/tar/python3 preexisting); the operator tooling authorization was not exercised.

### 2. C2 counting commands on base bytes (cwd = scratch base tree)

#### C2.1 — frontier admitted rows — BEFORE 17 (after-claim 18)

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md
17
rc=0
$ grep -oE '^\| F[0-9]+' corpus/README.md | tr -d '| '
F01
F02
F03
F04
F05
F06
F07
F08
F09
F10
F11
F12
F13
F14
F15
F16
F17
```

F18 is absent; the last admitted row id at base is F17.

#### C2.2 — registry rows — BEFORE 51 (after-claim 52)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
51
rc=0
$ grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md
1
rc=0
```

S051 is the last registry row at base.

#### C2.3 — S052 row — BEFORE 0 (after-claim 1)

```
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md
0
rc=1
```

rc=1 is grep's zero-match exit — the BEFORE signal itself.

#### C2.4 — knowledge entries citing `source: S052 ` — BEFORE 0 (after-claim 1)

```
$ grep -lE '^source: S052 ' corpus/knowledge/*.md
grep_rc=1            (no file matches; nothing printed)
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l
0
pipeline_rc=0
$ ls corpus/knowledge/*.md | wc -l
46
```

Knowledge entry count at base is 46 (claims before-state: 46; after-claim 47).

#### C2.5 — harness — BEFORE entries=20 pass=20 exit=0 (after-claim 21/21)

```
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
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
rc=0
```

20 admitted entries (F01–F17, F09/F10/F11 each carrying two entries), highest declared id S051 — no F18 entry exists at base. The harness resolves its lane root from the script's own location (`--root` default = three `dirname` levels above `corpus/instruments/frontier-recheck-count.py`), so this run measured the scratch base tree, not the live lane. It executes each entry's `recheck:` line via `bash -c` with cwd = the scratch base tree; all 20 executed recheck lines were read-only `source-recheck.py` runs inside the scratch copy. No `--json` was passed; nothing was written.

#### C2.6 — source-recheck S052 — BEFORE manifest UNAVAILABLE reason=missing, exit 2 (after-claim exit 0)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
manifest UNAVAILABLE reason=missing
rc=2
$ ls corpus/source-snapshots/round-35/manifest.json
ls: cannot access 'corpus/source-snapshots/round-35/manifest.json': No such file or directory
rc=2
$ ls corpus/source-snapshots/
round-23
round-24
round-25
round-26
round-28
round-29
round-30
round-31
round-32
round-34
```

The round-35 manifest does not exist at base (snapshot rounds stop at round-34), so `load_manifest` hits `FileNotFoundError` → `manifest UNAVAILABLE reason=missing` → exit 2, exactly the claims before-state.

### 3. Verdict

**Control killed — all six probes print the BEFORE values; no C2 counter is satisfiable by do-nothing.**

| probe | base output | claims before | claims after | discriminates? |
|---|---|---|---|---|
| frontier rows (`grep -cE '^\| F[0-9]+ \|' corpus/README.md`) | 17, rc=0 | 17 | 18 | yes |
| registry rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`) | 51, rc=0 | 51 | 52 | yes |
| S052 row (`grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md`) | 0, rc=1 | 0 | 1 | yes |
| entries citing S052 (`grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l`) | 0 | 0 | 1 | yes |
| harness (`python3 corpus/instruments/frontier-recheck-count.py`) | entries=20 pass=20 exit=0 | entries=20 pass=20 | entries=21 pass=21 | yes |
| source-recheck S052 (`--manifest corpus/source-snapshots/round-35/manifest.json --source S052`) | `manifest UNAVAILABLE reason=missing`, rc=2 | exit 2, manifest missing | exit 0 | yes |

Every AFTER value (18 / 52 / 1 / 1 / 21/21 / recheck exit 0) is unreachable on the frozen bytes: the F18 row, the S052 registry row, the `cisa-kev` knowledge entry, the round-35 manifest + S052 capture, and the harness delta all require the claimed C2 work to exist. The census probe (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`) is out of this control's scope: it runs against the live fleet root, not base bytes, and was not assigned to this seat.

### 4. File digests (evidence files quoted above)

| file (at base `617496b9`) | sha256 |
|---|---|
| `git archive` tarball of `617496b9` | `a008adf24ed9fa5c93e35b51c84b2dc2df0fe60722098a481f222ac71782467a` |
| extracted tree fingerprint (`find \| sort -z \| xargs -0 sha256sum \| sha256sum`) | `acb28d7d272e00c16b3f625ecda72c02b89bd2fafeeb593f2c3502e55f985acb` |
| `corpus/README.md` | `876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29` |
| `corpus/SOURCES.md` | `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6` |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` |
| `corpus/instruments/source-recheck.py` | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |

### 5. Restoration / containment evidence

- The control ran entirely on an exported copy under scratch; the lane repo bytes were never mutated. Lane commands used by this seat were read-only (`git rev-parse`, `git archive`, `git cat-file blob`, `grep`, `ls`, `test`).
- The scratch copy is declared disposable by the tasking, so no byte restoration is required; deletion is the restoration record (§6).
- This seat's only write inside the lane repo is this receipt file: `.ufo/waves/round-35/wave1/MutCounterBase.md`.

### 6. Scratch cleanup

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/MutCounterBase
rm_rc=0
$ test -e /fast/scratch/hyaku/kasegi-r35/MutCounterBase
test_e_rc=1 (1 = absent)
```

Scratch tree deleted and verified absent before yielding. Sibling seat dirs under `/fast/scratch/hyaku/kasegi-r35/` were not touched.

### 7. Incidents

- The first battery invocation aborted after C2.3 because the persistent shell retained `set -e` from the export step and the S052 grep's zero-match exit 1 terminated the script; rerun with `set +e +u` captured C2.3's rc and all remaining probes. No evidence was lost; C2.1/C2.2 outputs from the first run are quoted in §2 and were not re-executed.
- No defects found in the C2 counters: the do-nothing control cannot reach any AFTER value.
