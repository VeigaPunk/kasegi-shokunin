# ExecBeforeReceipts — frozen before-receipt reproducibility

Seat: ExecBeforeReceipts (executor, leaf). Milestone: round-33. Axes: depth:verifiability, coverage.
Answering model (runtime-reported): `opencode-go/deepseek-v4.1-flash`.
No peer waits, no delegation, no labrat, no background jobs. No git/jj mutation; read-only git only.

## Verdict

**PASS — no drift.** Both committed before receipts reproduce byte-for-byte from a `git archive` export of the freeze commit:

- `.ufo/waves/round-33/c1-controls/before.txt`: `diff` exit 0, `cmp` identical on the first run and on a second run.
- `.ufo/waves/round-33/c2-controls/before.txt`: `diff` exit 0 after normalizing the archive root prefix in the census `ok` line (that line is the only path-dependent line; raw diff shown below — exactly one line differs, the census targets the archive root by construction).
- Fake checker on the base manifests: `records=38 bound=38 unbound=0`, `fake_exit=0`, with `with_url=0` on the same bytes — the kill-rule clause it must fail is confirmed by construction.

No difference was found, so per the item no drift report is owed to the L1.

## Method note (recorded because it bounds the claim)

The frozen receipts are **output-only**: neither `before.txt` holds the command line that produced it, and no command transcript is committed in the lane. The reproduction below therefore **reconstructs** the commands from the receipt's own sections and re-derives every number from the freeze archive; only the static `#`/`##` header lines are echoed literally. Byte-identity of the derived file is evidence that the frozen values are reproducible from the frozen bytes, not proof that the L1's original invocation was character-identical (that is not knowable from the committed artifacts).

The C2 census line embeds an absolute registry path (`kasegi<TAB>ok<TAB><root>/kasegi-shokunin/corpus/SOURCES.md`), so an archive-root run cannot be byte-identical without a prefix substitution; the substitution is applied only to that line's root and is shown verbatim. The live lane was **not** used for census because it is being edited in-flight this wave (M30-3); the census was run against the archived freeze bytes.

## Inputs

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
FREEZE=6e55c8d58a3e63efe11c0df47068bfc479bfc8e0
BASE=690b69dae23ab9f4ccf056ba2d619cadc2abb3c4
S=/fast/scratch/hyaku/kasegi-r33/ExecBeforeReceipts   # $HYAKU_SCRATCH default
```

Commit identity and exports:

```
$ git -C "$LANE" rev-parse "$FREEZE" "$FREEZE^{tree}" "$BASE"
6e55c8d58a3e63efe11c0df47068bfc479bfc8e0
627a720f25cb149c13ad072907ffb07114903eaf
690b69dae23ab9f4ccf056ba2d619cadc2abb3c4
$ git -C "$LANE" log -1 --format='%H %aI %s' "$FREEZE"
6e55c8d58a3e63efe11c0df47068bfc479bfc8e0 2026-10-26T01:09:27-03:00 round-33: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard, watch-dog digest, LOG r32 entry (D1)

$ mkdir -p "$S/freeze" "$S/base"
$ git -C "$LANE" archive "$FREEZE" | tar -x -C "$S/freeze"
$ git -C "$LANE" archive "$BASE"   | tar -x -C "$S/base"
- freeze export files: 6675; base export files: 6663

$ git -C "$LANE" archive "$FREEZE" | tar -x -C "$S/freeze2" && diff -r "$S/freeze" "$S/freeze2"
second_extract_identical

$ git -C "$LANE" diff --quiet "$FREEZE" a6a502351bb90c8cd6d9b8f45f55109b7848e0d1 -- \
    .ufo/waves/round-33/c1-controls .ufo/waves/round-33/c2-controls
controls_identical_at_HEAD
```

Committed control-file hashes, archive export vs `git show` (fidelity of the extraction path) and vs the live lane copy:

```
before.txt (c1)          git-show=78aeae5d72eb368b02883ad0581fc81a93a5305230623c2563b1a349c0312815
                         archive =78aeae5d72eb368b02883ad0581fc81a93a5305230623c2563b1a349c0312815  MATCH
                         live    =78aeae5d72eb368b02883ad0581fc81a93a5305230623c2563b1a349c0312815  MATCH
before.txt (c2)          git-show=2997b92b786c445b3f2aa2272d3ee60b3b3d2d178db4bdcb5d5bee005e227bcc
                         archive =2997b92b786c445b3f2aa2272d3ee60b3b3d2d178db4bdcb5d5bee005e227bcc  MATCH
                         live    =2997b92b786c445b3f2aa2272d3ee60b3b3d2d178db4bdcb5d5bee005e227bcc  MATCH
fake-checker.py          git-show=c67d60a1464375a5e00998908336b13b01cf37c821e8f9d72d57ee936efa9e11
                         archive =c67d60a1464375a5e00998908336b13b01cf37c821e8f9d72d57ee936efa9e11  MATCH
                         live    =c67d60a1464375a5e00998908336b13b01cf37c821e8f9d72d57ee936efa9e11  MATCH
fake-checker-receipt.txt git-show=f167cfada0ca63ee72e463597be3d5cc0f8206ca5a844c56eebf9a42e5a5d70e
                         archive =f167cfada0ca63ee72e463597be3d5cc0f8206ca5a844c56eebf9a42e5a5d70e  MATCH
                         live    =f167cfada0ca63ee72e463597be3d5cc0f8206ca5a844c56eebf9a42e5a5d70e  MATCH
```

Base vs freeze corpus bytes (the receipts say "base 690b69da"; the archive runs at freeze):

```
$ diff -r "$S/base/corpus/source-snapshots" "$S/freeze/corpus/source-snapshots"   -> IDENTICAL snapshots
$ diff "$S/base/corpus/SOURCES.md" "$S/freeze/corpus/SOURCES.md"                  -> IDENTICAL
$ diff "$S/base/corpus/README.md"  "$S/freeze/corpus/README.md"                   -> IDENTICAL
```

## C1 reproduction

Script used verbatim (written to `$S/repro-c1.sh`, run with `$S/freeze` and then `$S/base`):

```bash
#!/usr/bin/env bash
set -u
S=$1; ROOT=$2; OUT=$3
cd "$ROOT" || exit 2
{
  echo "# C1 before (frozen at claims time; base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4)"
  echo "## instrument absent"
  ls corpus/instruments/capture-binding-check.py 2>/dev/null
  echo "ls_exit=$?"
  echo "## manifest audit (all snapshot dirs)"
  for m in corpus/source-snapshots/*/manifest.json; do
    r=${m%/manifest.json}; r=${r##*/}
    python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(sys.argv[2], "records=", len(d.get("sources", [])))' "$m" "$r"
  done
  python3 -c 'import glob,json
t=u=f=0
for m in sorted(glob.glob("corpus/source-snapshots/*/manifest.json")):
    for s in json.load(open(m)).get("sources",[]):
        t+=1; u+=("url" in s); f+=("fetched_utc" in s)
print("TOTAL records=%d with_url=%d with_fetched_utc=%d" % (t,u,f))'
  echo "## round-32 snapshot dir (no manifest)"
  ls corpus/source-snapshots/round-32
  echo "## source-recheck on absent round-32 manifest"
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
  echo "recheck_exit=$?"
} > "$OUT" 2>/dev/null
```

Run:

```
$ "$S/repro-c1.sh" "$S" "$S/freeze" "$S/c1-repro-freeze.txt"
$ "$S/repro-c1.sh" "$S" "$S/base"   "$S/c1-repro-base.txt"
```

Output (`$S/c1-repro-freeze.txt`; `$S/c1-repro-base.txt` is identical):

```
# C1 before (frozen at claims time; base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4)
## instrument absent
ls_exit=2
## manifest audit (all snapshot dirs)
round-23 records= 4
round-24 records= 19
round-25 records= 5
round-26 records= 1
round-28 records= 2
round-29 records= 3
round-30 records= 3
round-31 records= 1
TOTAL records=38 with_url=0 with_fetched_utc=0
## round-32 snapshot dir (no manifest)
S049.txt
S050.txt
## source-recheck on absent round-32 manifest
manifest UNAVAILABLE reason=missing
recheck_exit=2
```

Byte comparison against the committed receipt:

```
$ diff -u "$S/freeze/.ufo/waves/round-33/c1-controls/before.txt" "$S/c1-repro-freeze.txt"
diff_exit=0
$ diff -u "$S/c1-repro-base.txt" "$S/c1-repro-freeze.txt"
base_vs_freeze_diff_exit=0
$ cmp "$S/c1-repro-freeze.txt" "$S/c1-repro-freeze-2.txt"    # second run
c1_second_run_identical
```

## C2 reproduction

The census target is a scratch root carrying the archived lane plus the fleet `shokunin.conf` (read-only copy), so the archive bytes are what the census validates:

```
$ mkdir -p "$S/root"
$ cp /home/vgpnk/Projects/shokunin/shokunin.conf "$S/root/shokunin.conf"
$ cp -a "$S/freeze" "$S/root/kasegi-shokunin"
$ grep -n '^kasegi' "$S/root/shokunin.conf"
46:kasegi|kasegi-shokunin|depth + coverage (bounty and security research)
```

Script used verbatim (written to `$S/repro-c2.sh`):

```bash
#!/usr/bin/env bash
set -u
ROOT=$1; CENSUS_ROOT=$2; OUT=$3
cd "$ROOT" || exit 2
{
  echo "# C2 before (frozen at claims time; base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4)"
  echo "## frontier admitted"
  awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
  echo "## entries citing S049 / S050 on a source: line"
  echo -n 'S049='; grep -lE '^source: S049 ' corpus/knowledge/*.md | wc -l
  echo -n 'S050='; grep -lE '^source: S050 ' corpus/knowledge/*.md | wc -l
  echo "## registry rows S049 / S050 / total"
  echo -n 'S049_rows='; grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md || true
  echo -n 'S050_rows='; grep -cE '^\|[[:space:]]*S050[[:space:]]*\|' corpus/SOURCES.md || true
  echo -n 'total_rows='; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md || true
  echo "## census"
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$CENSUS_ROOT" kasegi
  echo "census_exit=$?"
  echo "## harness"
  python3 corpus/instruments/frontier-recheck-count.py
  echo "harness_exit=$?"
  echo "## source-recheck S049/S050 on absent round-32 manifest"
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
  echo "recheck_exit=$?"
} > "$OUT" 2>/dev/null
```

Run and output (`$S/c2-repro-raw.txt`):

```
$ "$S/repro-c2.sh" "$S/freeze" "$S/root" "$S/c2-repro-raw.txt"
# C2 before (frozen at claims time; base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4)
## frontier admitted
15
## entries citing S049 / S050 on a source: line
S049=0
S050=0
## registry rows S049 / S050 / total
S049_rows=0
S050_rows=0
total_rows=48
## census
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/fast/scratch/hyaku/kasegi-r33/ExecBeforeReceipts/root/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
## harness
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
## source-recheck S049/S050 on absent round-32 manifest
manifest UNAVAILABLE reason=missing
recheck_exit=2
```

Normalization (only the census `ok` line carries the archive root) and byte comparison:

```
$ sed "s|$S/root/kasegi-shokunin/|/home/vgpnk/Projects/shokunin/kasegi-shokunin/|g" \
    "$S/c2-repro-raw.txt" > "$S/c2-repro-freeze.txt"
$ grep -n '	ok	' "$S/c2-repro-freeze.txt"
14:kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md

$ diff -u "$S/freeze/.ufo/waves/round-33/c2-controls/before.txt" "$S/c2-repro-freeze.txt"
diff_exit=0
$ cmp "$S/freeze/.ufo/waves/round-33/c2-controls/before.txt" "$S/c2-repro-freeze.txt"
cmp=identical

$ diff -u "$S/freeze/.ufo/waves/round-33/c2-controls/before.txt" "$S/c2-repro-raw.txt"   # un-normalized
@@ -11,7 +11,7 @@
 kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
 kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
-kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
+kasegi	ok	/fast/scratch/hyaku/kasegi-r33/ExecBeforeReceipts/root/kasegi-shokunin/corpus/SOURCES.md
 census_exit=0
raw_diff_exit=1   # exactly one line, the root prefix; values and exit codes identical

$ cmp "$S/c2-repro-raw.txt" "$S/c2-repro-raw-2.txt"    # second run
c2_second_run_identical
```

Census date-window control (the frozen command does not pin `--today`; validate's E08 compares `opened` to today):

```
$ grep -oE '2026-[0-9]{2}-[0-9]{2}' "$S/freeze/corpus/SOURCES.md" | sort -u | tail -5
2026-10-16
2026-10-19
2026-10-20
2026-10-23
2026-10-25
$ sources-census.sh validate --root "$S/root" --today 2026-10-26 kasegi > pinned.txt   # pinned_exit=0
$ sources-census.sh validate --root "$S/root"            kasegi > default.txt          # default_exit=0
$ diff -u pinned.txt default.txt
census_today_pinned_identical
```

No `opened` date in the archived registry is later than 2026-10-26, so the unpinned command is stable on these bytes.

## Fake checker control (C1 kill-rule clause)

Command (fake checker taken from the freeze export; base manifests are the target):

```
$ cd "$S/base"
$ python3 "$S/freeze/.ufo/waves/round-33/c1-controls/fake-checker.py" --root .
records=38 bound=38 unbound=0
fake_exit=0
$ diff -u <(head -4 "$S/freeze/.ufo/waves/round-33/c1-controls/fake-checker-receipt.txt") "$S/fake-repro.txt"
fake_diff_exit=0
```

The same bytes carry no binding fields at all, so `bound=38` is unvalidated by construction:

```
$ python3 -c '<manifest audit over $S/base/corpus/source-snapshots>'
records=38 with_url=0 with_fetched_utc=0 with_archival=0
```

Its `--selftest` is itself a no-op (no fixture cases), which the contract's `--selftest >=6 cases` clause rejects:

```
$ python3 "$S/freeze/.ufo/waves/round-33/c1-controls/fake-checker.py" --selftest
selftest cases=0 failures=0
fake_selftest_exit=0
```

Kill-rule clause confirmed: a checker that exits 0 with `bound=N` while every record lacks `url`/`fetched_utc`/`archival` cannot be validated; the real `capture-binding-check.py` must exit 1 on these bytes and name the 38 unbound records (C1's red-before state).

## Findings and residual risks

1. **No drift.** Both receipts reproduce; every derived number equals the frozen value: frontier 15, S049/S050 entry citations 0/0, registry rows 0/0/48, census exit 0 with only W04 S028/S029, harness 18/18 exit 0, both source-rechecks `UNAVAILABLE reason=missing` exit 2, C1 audit 38/0/0, instrument absent `ls_exit=2`.
2. **Receipts are output-only (process gap, carried from round 33's own M33-2 lesson direction).** `before.txt` does not record its command lines; a verifier must reconstruct them. Recommendation for the round-33 lesson: freeze receipts should carry the literal command next to each output line, otherwise "re-run the commands" is reconstructed inference, not replay.
3. **C2's census line is root-path-dependent.** The frozen value embeds `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`; an archive-root replay can only match after prefix normalization. Pin `--root` to a stable path or drop the absolute path from the receipt if byte-level replayability is a goal.
4. **Census `--today` is unpinned.** It is stable today on these bytes (no future `opened` dates; pinned/default identical), but the receipt is not date-independent by construction.
5. No lane writes, no git/jj mutations, no network access, no credential material touched. No peer waited on; no drift, so no L1 message was owed.

## Scratch cleanup

`/fast/scratch/hyaku/kasegi-r33/ExecBeforeReceipts/` (freeze/base/second-extract exports, scratch census root, scripts, intermediate outputs) was removed after this receipt was written; all cited outputs are transcribed above.

```
$ S=/fast/scratch/hyaku/kasegi-r33/ExecBeforeReceipts
$ rm -rf -- "$S"
$ if [ ! -e "$S" ]; then echo "removed: $S"; else echo "STILL PRESENT: $S"; fi
removed: /fast/scratch/hyaku/kasegi-r33/ExecBeforeReceipts
```
