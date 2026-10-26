# ExecErratumCheck — round-33 erratum red/green receipts (D5/M33-1 manifest, D1 LOG entry, D4 watchdog digest)

Seat: ExecErratumCheck (leaf, round-33 wave 1). Model actually run on:
`opencode-go/deepseek-v4.1-flash` (route-table decision; this seat never passed a model).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Judged axes: depth:verifiability
(primary), coverage. No repo edits: **this receipt is the only file this seat wrote inside the
lane**; every mutation in this receipt ran on scratch copies under
`/fast/scratch/hyaku/kasegi-r33/ExecErratumCheck` (`HYAKU_SCRATCH` unset, default used), which is
removed before yield (§7). Tooling: nothing installed or upgraded; `bash`, `grep`, `find`,
`python3` (stdlib) only. No build/lint/test gate run here (wave policy: the parent owns the
post-integration gate). In every command block below, `$S` =
`/fast/scratch/hyaku/kasegi-r33/ExecErratumCheck` (`HYAKU_SCRATCH` unset, default root), created
with `mkdir -p` and removed in §7.

## 0. Subject digests and states

| Subject | State | Digest |
|---|---|---|
| `corpus/source-snapshots/round-32/` | RED-before: `S049.txt`, `S050.txt`, **no** `manifest.json` | S049 `962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8`; S050 `2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888` (blobs `8ac0c7b8…`, `7bf32b34…` at 690b69d and unchanged in the worktree) |
| `corpus/source-snapshots/round-32/manifest.json` | GREEN-after (mtime 01:18) | `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774` |
| `LOG.md` | frozen with the round-32 entry; unchanged across this run | `52c04d267453881d0caba372c46497f0590df081399b54b8dc8ef7ba133cf5f8` (1595 lines) |
| `.ufo/waves/round-33/watchdog-digest.txt` | committed at 6e55c8d | `7bf40db684a7427c156e8f8912d01b5897278dbbec6874f0f21339f78f63ed85` |

HEAD during RED-before: `a6a5023` (round-33 wave-1 spec). Lane registry rows at that moment: 48;
no `S049`/`S050` rows yet (SOURCES.md `5a03c696…`).

## 1. The closure check (design, bytes, hash)

One script, two checks, one bash-parseable line per check plus a summary line; exit 0 only when
every selected check passes, 1 on any failure, 2 on usage/read error. `--root` re-points the same
bytes at a scratch tree (that is how the able-to-fail controls in §6 run), `--checks` selects a
subset. Consumers can branch on either the exit status or
`grep -q '^CHECK round-32-manifest PASS'`.

Semantics:
- **`round-32-manifest`** — the D5/M33-1 closure. FAIL if the snapshot dir or its `manifest.json`
  is absent (naming the dir and the capture files actually present), if the manifest does not
  parse, if the record ids are not exactly `S049,S050`, if a record lacks `url` or `fetched_utc`
  (naming the record id), or if a `url` is not the contracted registry URL (naming the record id).
- **`round-32-log`** — the D1 closure. FAIL unless
  `grep -cE '^## .*[Rr]ound[- ]32' LOG.md` is exactly 1 (naming the observed count and lines).

The item's minimum is "exits 0 once the manifest exists". Existence alone would pass a manifest
whose urls point nowhere, which is M33-1's failure mode plus one file; the shipped check binds the
two contracted records as well (a strict superset — every green state here also satisfies the
existence minimum, and the PASS line reports `captures=` for the existence fact).

Script hash used for every run below:
`438709fdfa82ef5d58ee432f4c1f8152166f64f0454c31f30eb62b17b8712895`
(`$S/closure-check.sh`, 119 lines; the fenced block below is byte-identical — §7).

```sh
#!/usr/bin/env bash
# closure-check.sh - round-33 erratum closure checks (D5/M33-1 manifest, D1 LOG entry).
# usage: closure-check.sh [--root DIR] [--checks manifest,log]
#   --root   lane root holding corpus/source-snapshots/round-32/ and LOG.md
#            (default: /home/vgpnk/Projects/shokunin/kasegi-shokunin)
#   --checks comma list, subset of {manifest,log} (default: manifest,log)
# output: one self-describing line per check,
#   CHECK <name> PASS|FAIL reason=<token> [key=value ...]
# exit: 0 = every selected check PASS; 1 = at least one FAIL; 2 = usage/read error.
set -u

ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
CHECKS=manifest,log
while [ $# -gt 0 ]; do
  case $1 in
    --root)   [ $# -ge 2 ] || { echo "USAGE reason=missing-value flag=--root" >&2; exit 2; }; ROOT=$2; shift 2 ;;
    --checks) [ $# -ge 2 ] || { echo "USAGE reason=missing-value flag=--checks" >&2; exit 2; }; CHECKS=$2; shift 2 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 2 ;;
    *) echo "USAGE reason=unknown-arg arg=$1" >&2; exit 2 ;;
  esac
done
[ -d "$ROOT" ] || { echo "USAGE reason=root-missing root=$ROOT" >&2; exit 2; }

# Round-32 captures must be paired with a manifest in the snapshot dir, and the
# manifest must carry the two contracted records with url + fetched_utc.
# Contract URLs: S049 https://zc.cnvd.org.cn/news/helpList
#                S050 https://security.360.cn/Reward/rules
check_manifest() {
  local d="$ROOT/corpus/source-snapshots/round-32" m caps out prc
  if [ ! -d "$d" ]; then
    echo "CHECK round-32-manifest FAIL reason=snapshot-dir-absent dir=$d"
    return 1
  fi
  caps=$(find "$d" -maxdepth 1 -type f ! -name manifest.json -printf '%f\n' 2>/dev/null | sort | paste -sd, -)
  m="$d/manifest.json"
  if [ ! -f "$m" ]; then
    echo "CHECK round-32-manifest FAIL reason=manifest-absent dir=$d captures=${caps:-none}"
    return 1
  fi
  out=$(python3 - "$m" <<'PY'
import json, sys
p = sys.argv[1]
try:
    with open(p, encoding="utf-8") as fh:
        doc = json.load(fh)
except Exception as exc:
    print("reason=manifest-unparseable error=%s" % type(exc).__name__)
    sys.exit(1)
srcs = doc.get("sources") if isinstance(doc, dict) else None
if not isinstance(srcs, list):
    print("reason=no-sources-array")
    sys.exit(1)
want = {
    "S049": "https://zc.cnvd.org.cn/news/helpList",
    "S050": "https://security.360.cn/Reward/rules",
}
records = [s for s in srcs if isinstance(s, dict)]
ids = sorted(str(s.get("id", "?")) for s in records)
problems = []
if len(srcs) != len(records):
    problems.append("non-object-record")
if set(ids) != set(want):
    problems.append("ids:" + (",".join(ids) or "none"))
else:
    for s in records:
        i = str(s.get("id"))
        if not s.get("url"):
            problems.append("no-url:" + i)
        elif s.get("url") != want[i]:
            problems.append("url-mismatch:" + i)
for s in records:
    if not s.get("fetched_utc"):
        problems.append("no-fetched_utc:" + str(s.get("id")))
fetched = sum(bool(s.get("fetched_utc")) for s in records)
exact = sum(1 for s in records if want.get(str(s.get("id"))) == s.get("url"))
print("records=%d ids=%s fetched_utc=%d url_exact=%d%s" % (
    len(srcs), ",".join(ids) or "none", fetched, exact,
    "" if not problems else " reason=" + ",".join(problems)))
sys.exit(0 if not problems else 1)
PY
)
  prc=$?
  if [ "$prc" -eq 0 ]; then
    echo "CHECK round-32-manifest PASS $out captures=${caps:-none}"
    return 0
  fi
  echo "CHECK round-32-manifest FAIL $out captures=${caps:-none}"
  return 1
}

# The round-32 LOG entry exists exactly once (D1: the L1 appended it at 6e55c8d).
check_log() {
  local f="$ROOT/LOG.md" n lines
  if [ ! -f "$f" ]; then
    echo "CHECK round-32-log FAIL reason=log-absent file=$f"
    return 1
  fi
  n=$(grep -cE '^## .*[Rr]ound[- ]32' "$f")
  lines=$(grep -nE '^## .*[Rr]ound[- ]32' "$f" | cut -d: -f1 | paste -sd, -)
  if [ "$n" -eq 1 ]; then
    echo "CHECK round-32-log PASS count=1 line=${lines}"
    return 0
  fi
  echo "CHECK round-32-log FAIL reason=count-$n count=$n lines=${lines:-none}"
  return 1
}

rc=0
failed=0
IFS=, read -r -a sel <<< "$CHECKS"
for c in "${sel[@]}"; do
  case $c in
    manifest) check_manifest || { rc=1; failed=$((failed + 1)); } ;;
    log)      check_log      || { rc=1; failed=$((failed + 1)); } ;;
    *) echo "USAGE reason=unknown-check check=$c" >&2; exit 2 ;;
  esac
done
echo "CLOSURE checks=${#sel[@]} failed=$failed exit=$rc"
exit "$rc"
```

Usage-error paths (exit 2, never a false PASS):

```
$ bash "$S/closure-check.sh" --root /nonexistent --checks manifest
USAGE reason=root-missing root=/nonexistent
exit=2
$ bash "$S/closure-check.sh" --checks bogus
USAGE reason=unknown-check check=bogus
exit=2
$ bash "$S/closure-check.sh" --root
USAGE reason=missing-value flag=--root
exit=2
$ bash "$S/closure-check.sh" --help ; echo $?
help_exit=2
```

## 2. RED-before — live lane, manifest absent (D5/M33-1)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin   # HEAD a6a5023
$ bash "$S/closure-check.sh"                          # default root = the lane, both checks
CHECK round-32-manifest FAIL reason=manifest-absent dir=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-32 captures=S049.txt,S050.txt
CHECK round-32-log PASS count=1 line=1593
CLOSURE checks=2 failed=1 exit=1
exit=1
```

Manifest-only selection gives the same verdict (`--checks manifest` → `CHECK round-32-manifest
FAIL …`, exit 1). This is the D5 state the round-32 captures shipped in: two capture files, no
manifest.

Reproduction on the **base-tree bytes** (`git archive 690b69d corpus/source-snapshots/round-32
LOG.md` into `$S/baseroot`), same script hash — both the manifest and the (pre-D1) LOG check are
red, exit 1:

```
$ bash "$S/closure-check.sh" --root "$S/baseroot"
CHECK round-32-manifest FAIL reason=manifest-absent dir=/fast/scratch/hyaku/kasegi-r33/ExecErratumCheck/baseroot/corpus/source-snapshots/round-32 captures=S049.txt,S050.txt
CHECK round-32-log FAIL reason=count-0 count=0 lines=none
CLOSURE checks=2 failed=2 exit=1
exit=1
```

## 3. CHECK `round-32-log` — D1 entry present exactly once

| Root | `grep -cE '^## .*[Rr]ound[- ]32'` | Check line | Exit |
|---|---|---|---|
| `690b69d:LOG.md` (base) | 0 | `FAIL reason=count-0 count=0 lines=none` | 1 |
| `6e55c8d:LOG.md` (freeze commit) | 1 | `PASS count=1 line=1593` | 0 |
| worktree `LOG.md` | 1 | `PASS count=1 line=1593` | 0 |

```
$ grep -cE '^## .*[Rr]ound[- ]32' LOG.md
1
$ grep -nE '^## .*[Rr]ound[- ]32' LOG.md
1593:## Round 32 — 2026-10-25 — honest stop: claims frozen, wave-1 spec validated, no seat ran (run-7 dispatcher cap 0) — re-dispatched as round 33
```

Heading anchor (≤25 words): `## Round 32 — 2026-10-25 — honest stop` at `LOG.md:1593`; the rest of
the line names the run-7 dispatcher cap and the re-dispatch as round 33. The entry is a pure
append at the freeze commit (`LOG.md` +4 insertions, 0 deletions):

```
$ git show --stat --oneline 6e55c8d -- LOG.md | tail -1
 1 file changed, 4 insertions(+)
$ git show 6e55c8d -- LOG.md | grep -c '^-[^-]'
0
```

The seed command in the item is exactly the one tabled above; it reads 1 at the freeze commit and
0 on the base tree, i.e. the check can fail.

## 4. D4 — committed watchdog digest opens, hashes, carries the round-33 launch line

```
$ ls -l .ufo/waves/round-33/watchdog-digest.txt
-rw-r--r-- 1 vgpnk vgpnk 272 Oct 26 01:12 .ufo/waves/round-33/watchdog-digest.txt
$ sha256sum .ufo/waves/round-33/watchdog-digest.txt
7bf40db684a7427c156e8f8912d01b5897278dbbec6874f0f21339f78f63ed85  .ufo/waves/round-33/watchdog-digest.txt
$ wc -l < .ufo/waves/round-33/watchdog-digest.txt
3
$ grep -n 'round=33' .ufo/waves/round-33/watchdog-digest.txt
3:1468:2026-10-26T01:10:54-03:00 launch kasegi round=33 pgid=99020 driver=hyaku-inline attempt=1
```

Each digest line is `source-line-number:source-line-text`; all three payloads compare equal to the
same line of the fleet watchdog log (`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`, read-only):

```
$ awk -F: '{n=$1; sub(/^[0-9]+:/,""); print n"\t"$0}' "$D" | while IFS=$'\t' read -r n text; do live=$(sed -n "${n}p" "$W"); [ "$live" = "$text" ] && echo "line $n: MATCH" || echo "line $n: MISMATCH"; done
line 1455: MATCH
line 1457: MATCH
line 1468: MATCH
```

Committed, and identical to the worktree copy:

```
$ git rev-parse 6e55c8d:.ufo/waves/round-33/watchdog-digest.txt
2bf6491a0015e82cc0a3027fe5a1f802dd0a6488
$ git show 6e55c8d:.ufo/waves/round-33/watchdog-digest.txt | sha256sum
7bf40db684a7427c156e8f8912d01b5897278dbbec6874f0f21339f78f63ed85  -
$ git diff --stat 6e55c8d -- .ufo/waves/round-33/watchdog-digest.txt
diff_exit=0
```

Round-33 launch line, verbatim: `2026-10-26T01:10:54-03:00 launch kasegi round=33 pgid=99020
driver=hyaku-inline attempt=1` (digest line 3, source line 1468). The digest also carries the
round-32 launch (1455) and completion (1457) lines, so the round-32 honest-stop record is
reconstructible from committed bytes alone (D4/M33-2).

## 5. GREEN-after — poll for `ExecManifest32.md`, re-run on quiescent bytes

Poll: `[ -s .ufo/waves/round-33/wave1/ExecManifest32.md ]` every 20 s from 01:17; the receipt
appeared at 01:20 (`poll_rounds=8`, 160 s, well inside the 30-minute cap). Quiescence (M30-3):
manifest sha256 **and** mtime identical immediately before and after the run; HEAD unchanged.
The manifest is still untracked in the worktree at run time (`?? corpus/source-snapshots/round-32/
manifest.json`), so this is the landed worktree state, not a committed state — the L1's helper
commit is outside this seat.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
head=53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f
pre_sha=6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774
pre_mtime=2026-10-26 01:18:46.001229897 -0300
$ bash "$S/closure-check.sh"
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S049.txt,S050.txt
CHECK round-32-log PASS count=1 line=1593
CLOSURE checks=2 failed=0 exit=0
exit=0
post_sha=6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774
post_mtime=2026-10-26 01:18:46.001229897 -0300
head_after=53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f
```

Re-derived, not trusted: the producing seat's `ExecManifest32.md` reports the same sha256 for the
same artifact, and this seat's check reads the bytes itself. The manifest carries the C1 rule-C
data exactly — record `S049` `url=https://zc.cnvd.org.cn/news/helpList`,
`fetched_utc=2026-10-25T23:14:00-03:00`; record `S050`
`url=https://security.360.cn/Reward/rules`, same `fetched_utc`; no `archival` key on either
(round-32+ records are exempt from the archival path and must carry `fetched_utc`).

## 6. ABLE-TO-FAIL — the check can go red on every failure mode (scratch copies only)

Three families, all with the same script hash, all mutations in `$S` (lane never written):

1. base-tree bytes at 690b69d → exit 1 (§2, second block);
2. delete the manifest from a **copy** of the landed state, then restore;
3. content mutants of the manifest shape (valid / missing `fetched_utc` / non-contract `url` /
   truncated JSON), each written to `$S/mutants` and copied over the scratch fixture.

```
$ cp -a "$L/corpus/source-snapshots/round-32" "$S/greenroot/corpus/source-snapshots/"; cp -a "$L/LOG.md" "$S/greenroot/LOG.md"
copy_sha=6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774
=== (a) scratch copy WITH the landed manifest ===
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S049.txt,S050.txt
CHECK round-32-log PASS count=1 line=1593
CLOSURE checks=2 failed=0 exit=0
exit=0
=== (b) delete the manifest in the scratch copy (able-to-fail) ===
CHECK round-32-manifest FAIL reason=manifest-absent dir=/fast/scratch/hyaku/kasegi-r33/ExecErratumCheck/greenroot/corpus/source-snapshots/round-32 captures=S049.txt,S050.txt
CHECK round-32-log PASS count=1 line=1593
CLOSURE checks=2 failed=1 exit=1
exit=1
=== (c) restore from the lane and re-run ===
restored_sha=6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S049.txt,S050.txt
CHECK round-32-log PASS count=1 line=1593
CLOSURE checks=2 failed=0 exit=0
exit=0
=== lane untouched by the delete test ===
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
```

Manifest content mutant matrix (`--root $S/mutantroot --checks manifest`):

| Fixture copied to `manifest.json` | Check line | Exit |
|---|---|---|
| *(absent)* | `FAIL reason=manifest-absent … captures=S049.txt,S050.txt` | 1 |
| `base.json` (contract shape) | `PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2` | 0 |
| `no-fetched.json` (S049 drops `fetched_utc`) | `FAIL … fetched_utc=1 url_exact=2 reason=no-fetched_utc:S049` | 1 |
| `bad-url.json` (S050 url → `https://example.invalid/rules`) | `FAIL … fetched_utc=2 url_exact=1 reason=url-mismatch:S050` | 1 |
| `broken.json` (truncated JSON) | `FAIL reason=manifest-unparseable error=JSONDecodeError` | 1 |
| `base.json` restored (+ LOG check) | `PASS …` / `PASS count=1 line=1593`, `CLOSURE checks=2 failed=0` | 0 |

The two negation controls therefore bite exactly where M33-1's failure modes are: an absent
manifest, a manifest without provenance, a manifest pointing at a non-registry URL, and a
manifest that is not JSON.

## 7. Risks, limits, and cleanup

- **Superset semantics.** The item's stated minimum is "exit 0 once the manifest exists"; the
  shipped check also binds the two records (ids, urls, `fetched_utc`). Every green state measured
  here satisfies both, and the PASS line reports `captures=` so the existence fact is explicit.
  The cost is a coupling: if the lane ever renames the manifest record key (`sources`) or changes
  the contract URLs, the check must be updated in the same commit — by design it fails loudly
  rather than passing a mis-pointed manifest.
- **Deliberately not duplicated here:** C1 rule B's `SOURCES.md` row matching. The registry rows
  land from another seat and may postdate the manifest; coupling this closure check to them would
  create a race and would double-count the C1 instrument's job.
- **Read-only.** The check reads the lane and writes nothing; fixture trees are passed explicitly
  with `--root` under `$S`. No `/tmp` path appears anywhere in the script; `TMPDIR` is not used
  because the script creates no temporary files.
- **Scope of the green.** Measured on the worktree bytes at HEAD `53bfa59` with the manifest
  untracked. The committed-state run is the parent's `capture-binding-check.py`/gate job; this
  receipt's byte hashes let that run be compared (`6e4e719a…` must persist). Actionable: as of
  this receipt `corpus/source-snapshots/round-32/manifest.json` is still
  `?? …/manifest.json`, so the L1's helper commit must pick it up — M33-1's closure is the
  manifest landing in the same history as the captures, not merely on disk.
- **No credential material touched.** The S049 capture page carries platform-issued tester
  credentials (QUALITY Q6); nothing here read, quoted, or referenced any part of it — the seat
  inspected only file names, JSON provenance fields, and the LOG/watchdog lines.
- **Tooling:** nothing installed or upgraded (no pacman transaction, no uv/npx/official binary).

Embedded-script integrity: the code block in §1 was extracted from this file and diffed against
the run copy — identical bytes, 119 lines, hash `438709fd…` on both sides:

```
$ awk '/^```sh$/{f=1;next} f && /^```$/{exit} f{print}' ExecErratumCheck.md > "$S/embedded.sh"
$ diff -u "$S/closure-check.sh" "$S/embedded.sh" && echo embed_identical
embed_identical
$ sha256sum "$S/embedded.sh" "$S/closure-check.sh"
438709fdfa82ef5d58ee432f4c1f8152166f64f0454c31f30eb62b17b8712895  embedded.sh
438709fdfa82ef5d58ee432f4c1f8152166f64f0454c31f30eb62b17b8712895  closure-check.sh
$ bash -n "$S/embedded.sh" && echo embedded_syntax_ok
embedded_syntax_ok
```

Scratch removal (all trees — `baseroot`, `log-base`, `log-freeze`, `mutantroot`, `mutants`,
`greenroot`, `scratchroot`, the script — live under `$S` and nothing else does):

```
$ rm -rf -- "$S" && { [ ! -e "$S" ] && echo "scratch_removed $S"; }
scratch_removed /fast/scratch/hyaku/kasegi-r33/ExecErratumCheck
```
