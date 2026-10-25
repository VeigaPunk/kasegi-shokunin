# C1SourceHarness — falsify wave-1 "harness 12/12 and F10 source-id binding"

Seat: `L1Kasegi25.C1SourceHarness` (read-only reviewer). Round 25, wave 2, lane
`kasegi-shokunin`. Lane tip `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` — the wave-1
outputs (all 44 claims/README/knowledge/instrument/snapshot changes) are **uncommitted**
worktree state; nothing below writes production.

Axes named: `depth:verifiability` (C1 — recheck lines must carry their own truth) and
`coverage` (C2 — F10 admitted rows must be re-verifiable with correct source binding).

---

## Verdict (falsifiable)

**Wave-1's harness result is CORRECT as reported: 12/12, exit 0, at the lane tip, and
F10's two entries have valid source-id binding.** All twelve `(frontier row, entry)`
records PASS with `problems=[]`; each F10 entry's `--source` selection matches its declared
`source:` set; the manifest lists exactly those ids; each per-source recheck re-verifies
SHA-256 and quote-pin integrity (exit 0 each).

Three defects found in the harness — none changes the 12/12 verdict, one is a real
laundering hole that future rounds should close:

1. **`; exit 0` / `|| true` exit laundering** — the D limb reads the exit of the whole
   `bash -c` command; a failing recheck can be masked by appending `; exit 0` (measured
   PASS on a tampered snapshot with exit 1 → PASS). The r24 docs only disclose pipe-based
   laundering (`… ; false | tail -1`), not this one. [Residual risk; found at wave-1]
2. **Limb B is tautological for mutations** — `recheck_ids ⊆ cited` can only fail for ids
   *added to the selection*; `cited` is recomputed from the same text the selection was
   mutated into, so no mutation of the recheck line can trip it (measured). It still holds
   as a *static* invariant on the live lines. [Residual risk]
3. **Docstring overstates the binding** — docstring says "must equal the entry's own
   `source:` id set"; code enforces only `declared ⊆ recheck_ids`, and `recheck_ids` may
   also include extra cited ids (M1: declared S036,S037, rechecked all four → PASS).
   This is a doc-vs-code mismatch, not a live-entry defect. [Minor]

No production edits made; no tools installed (no installs needed — `python3` only; no
install/update record required beyond this note).

---

## Evidence

### 1. Harness run — lane tip (final, after all probes; fixture cleaned up)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
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
entries=12 pass=12 exit=0
$ echo $?
0
```

Matches wave-1's predicted receipt exactly: `RevManifestShape.md:247` `entries=12 pass=12
exit=0` (lines 242-251 there state the expectation: F10 contributes two records; the 12 is
arithmetic from the 10-entry post-r24 state). `frontier-after.json` was never written
(wave-1 receipt is prose-only in `RevManifestShape.md`); nothing contradicts it.

### 2. F10 source-id binding (static, on live files)

| entry | declared `source:` header | `recheck:` `--source` | manifest lists |
|---|---|---|---|
| `vendor-disclosure-policies-as-corpus-objects.md` | S036,S037,S038,S039 (lines 3-6) | S036 && S037 && S038 && S039 (line 8) | S036,S037,S038,S039 |
| `vendor-disclosure-policy-commitments-crosswalk.md` | S040,S036,S038,S039 (lines 2-5) | S040 && S036 && S038 && S039 (line 7) | S040,S036,S038,S039 |

Manifest `corpus/source-snapshots/round-25/manifest.json`: `schema_version=1`; sources
list exactly `S036,S037,S038,S039,S040`; per-source quote pins: S036=8, S037=6, S038=7,
S039=9, S040=9 (total 39 quotes — matches wave-1's "manifest 5 sources/39 quotes").
All 39 quote pins are carried on `source-recheck.py` `--source` lines (verified `entry_contract`
`evaluate` path and `manifest_ids` at `frontier-recheck-count.py:85-98,114-128`).

### 3. Per-source re-verification (the D limb, run directly)

```
$ for s in S036 S037 S038 S039 S040; do python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-25/manifest.json --source $s; echo exit($s)=$?; done
exit(S036)=0  exit(S037)=0  exit(S038)=0  exit(S039)=0  exit(S040)=0
```

Each source prints `S###:sha256 OK` plus one `OK occurrences=N` line per pinned quote
(`source-recheck.py:149-180`): sha256 verification against the pinned hex digest, then
normalized quote occurrence check (markup/whitespace stripped, min 12 chars).

### 4. Probe results (all in `/tmp` fixtures — no production writes)

| probe | mutation | harness result | interpretation |
|---|---|---|---|
| control | F10 row + both real entries, absolute `cd` | 2/2 exit 0 | reproduces live |
| rel control | same, relative paths | 2/2 exit 0 | absolute `cd` prefix is unneeded for PASS |
| M1 | entry-1 declares only S036,S037 (drop two headers), recheck all four | PASS | docstring "equality" not enforced; superset allowed |
| M2 | drop `--source S039` from selection | FAIL `header-sources-not-rechecked` | A limb works |
| M3 | add `--source S037` to selection | PASS | B limb is tautological (cited recomputed from same text) |
| M4 | add `--source S068` (cited in prose, absent from manifest) | FAIL `manifest-missing-ids` | C limb works |
| M5 | append byte to S036.txt snapshot | FAIL `recheck-exit-1` (both entries) | D limb works on real tamper |
| M6 | README row status admitted→staged | entries=0 exit 1 | non-admitted rows invisible by design |
| M7 | M5 + append `; exit 0` to recheck line | entry-1 PASS | **laundering hole** |
| M8 | move `--source S039` into a comment | FAIL `recheck-exit-1` | comment tokens *are* harvested (r24 finding) but entry-1 exit 1 here because tamper; on clean snapshot comment move would PASS |
| M10 | `recheck: true` | FAIL `not-a-recheck-invocation` | r24 docstring route still blocked |

### 5. The three findings in code

- **Exit laundering** — `frontier-recheck-count.py:125-129`: `subprocess.run(["bash","-c",
  recheck], cwd=root)`; the record's exit is `proc.returncode` of the *whole* `-c`
  string, so `… ; exit 0` or `… || true` masks any failing source check. Wave-1's
  `RevFrontierHarness.md:158` discloses only the pipe route (`… ; false | tail -1`).
  Measured: M5 (exit 1) → M7 (PASS) with the exact same tampered snapshot.
- **Tautological B limb** — `frontier-recheck-count.py:67,78,116`: `cited` is rebuilt via
  `re.findall(r"S\d{3,}", body)` (line 67) from the *same* file that the mutation just
  edited, and `recheck_ids` is a subset of it; adding an id to the selection adds it both
  to `recheck_ids` and `cited`, so `selection-not-cited-by-entry` is unreachable by any
  selection mutation (M3). It still catches ids *introduced* outside the recheck line
  (e.g. in a different file's body) — a static invariant, not a mutation detector.
- **Docstring-vs-code** — `frontier-recheck-count.py:13-16`: "the `--source` ids on the
  `recheck:` line must **equal** the entry's own `source:` id set"; actual check
  (`:114-117`) is `declared ⊆ recheck_ids ⊆ cited`. M1 shows the weaker subset accepted.

---

## Residual risks (post-verification)

1. `; exit 0` / `|| true` laundering (finding 1) also bypasses the whole C1 audit — the
   audit checks parse/cwd/path, not exit semantics of the command tail.
2. The harness trusts the `cd` prefix inside recheck lines; if a future line pointed
   `cd` at a mirror/degenerate root with a same-named manifest, binding checks would run
   against that root while the entry claims the lane (static check has no cwd awareness).
3. Row/entry atomicity: an admitted row naming a missing entry crashes with uncaught
   `FileNotFoundError` (traceback, exit 1) rather than a FAIL record
   (`frontier-recheck-count.py:61-64`; already flagged wave-1 `RevFrontierHarness.md:154-156`).

## Verification gaps

- The lane's `source-snapshots`/`manifest.json` were checked in the worktree; their
  *committed* hashes were not (the files are untracked `??`). `frontier-recheck-count.py`
  hash `c8a6288…` matches wave-1's `RevFrontierHarness.md:42-44` byte-for-byte on the
  worktree; base-commit comparison done by that seat.
- Quote equality was measured (39/39 OK), not re-read against the original web pages;
  that is upstream-fetch scope, not harness scope.

## Hand-off

- **Given verdict**: "harness 12/12 + F10 source-id binding" is CONFIRMED at the lane tip.
- **Smallest corrections to record** (no production edits made):
  - `frontier-recheck-count.py:125-129` — mask command-exit laundering (`; exit 0`,
    `|| true`, pipes are partially documented; this is not).
  - `frontier-recheck-count.py:13-16` — docstring should say "the `--source` ids must be
    a superset of the entry's `source:` set and a subset of its cited ids" (current code
    behavior), or the code should be tightened to equality if the docstring is the contract.
- Main-agent checks to run: (a) `python3 corpus/instruments/frontier-recheck-count.py` →
  `entries=12 pass=12 exit=0`; (b) `sha256sum corpus/instruments/frontier-recheck-count.py`
  → `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261`.
