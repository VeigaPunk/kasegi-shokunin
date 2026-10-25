# Recheck-audit expected-list regeneration probe

- **Axes:** depth:verifiability (load-bearing audit), coverage (one newly landed expected entry).
- **Scope:** all mutations and runs used an isolated `/tmp/labprobe.ZTngTa` copy of `corpus/`; the lane checkout was only read to copy fixtures and run `corpus/instruments/recheck-audit.py`. No production files changed. Fixture F13 entry had source headers S043/S044/S045, `verified-at: 2026-10-25`, `ground: F13`, and a chained source-recheck line. A placeholder `corpus/source-snapshots/round-29/manifest.json` made its path tokens exist in the copy; this was only to satisfy the instrument's path limb, not a real manifest or source verification.
- **Tool/model:** no tool installed. Running model: openai-codex/gpt-6-luna (workstation/runtime route as supplied; no model override).

## Exact runs

**PRE-STATE baseline copy (before fixture entry):** copied live corpus had 40 knowledge files; expected list had 42 lines (40 entries + 2 comments). Audit with `--root "$T" --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin` printed `lines=40 total=40 pass=40 ... exit=0` and `expect=present expected=40 missing=0 unexpected=0 exit=0`.

**RUN A — RED-BEFORE (fixture entry exists, copied expected list remains stale):** copied F13 fixture made 41 actual files; expected list remained 40. Command: `python3 corpus/instruments/recheck-audit.py --root "$T" --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --json "$T/runA-stale-list.json"`. Exact relevant output:

```text
unexpected=corpus/knowledge/program-severity-ladders-and-reward-scales.md
lines=41 total=41 pass=41 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=40 missing=0 unexpected=1 exit=1
```

Process exit: **1**. This is the requested stale-list failure after F13 exists.

**RUN B — regenerated from actual copied tree:** generated a sorted list from every `corpus/knowledge/*.md`, retaining the first two comment lines. Regenerated file: **43 total lines, 41 entry lines**. Command as above with `--json "$T/runB-regenerated.json"`. Exact summary:

```text
lines=41 total=41 pass=41 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=41 missing=0 unexpected=0 exit=0
```

Process exit: **0**.

## Load-bearing mutations

The equality checker is symmetric set comparison (`missing = expected - actual`, `unexpected = actual - expected`), so the two distinct directions were tested rather than conflated.

**RUN C — delete an actual file, keep it listed:** deleted `ai-assisted-finding-validation.md` from copied knowledge tree, without changing the regenerated expected list. Output: `missing=corpus/knowledge/ai-assisted-finding-validation.md`; `lines=40 total=40 ... exit=1`; `expect=present expected=41 missing=1 unexpected=0 exit=1`. Process exit: **1**. This proves expected-only names are caught as missing.

Restored the actual file, then **RUN D — delete one filename from the expected list, actual file remains:** rebuilt the expected list from all actual entries except `ai-assisted-finding-validation.md` (40 expected, 41 actual). Output:

```text
unexpected=corpus/knowledge/ai-assisted-finding-validation.md
lines=41 total=41 pass=41 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=40 missing=0 unexpected=1 exit=1
```

Process exit: **1**. The requested one-entry deletion flips the audit red; the reverse mutation also independently demonstrates the `missing=1` branch.

## Evidence paths / limitations

Temporary outputs: `$T/runA-stale-list.out`, `$T/runB-regenerated.out`, `$T/runC-missing.out`, `$T/runD-missing-list.out`; JSON receipts are the corresponding `*.json` files under `/tmp/labprobe.ZTngTa`. Live baseline output was captured at `/tmp/labprobe-live-baseline.txt` before F13 landed in the lane: it reported `lines=40 total=40 ... exit=0` and `expect=present expected=40 missing=0 unexpected=0 exit=0`. That live reading is PRE-STATE, not a post-integration counter.

No F13 production entry was present when this probe began. The fixture tests list mechanics and actual instrument behavior, not the production entry's evidence quality, capture validity, or final lane state. Main should compare this receipt's sandbox counts with the post-integration production counter; the lane result is unmeasured here.