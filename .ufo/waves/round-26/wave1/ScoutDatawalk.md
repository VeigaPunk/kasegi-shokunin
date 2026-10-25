# Round 26 wave 1 — planner data-walk (ScoutDatawalk)

Seat: L1Kasegi26.ScoutDatawalk. Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Access date: 2026-10-25 (UTC). Facts only; no edits made.

## 1. C1 counter commands — exact current outputs (run from lane root)

Command 1 (registry row probe):
```
$ grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md
0            (grep exit 1 = no match)
```
Cross-check: `grep -cF 'gate|probe' SKILL.md` → 0 (zero occurrences of the literal text in SKILL.md).

Command 2 (selftest receipt):
```
$ grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt
grep: .ufo/waves/round-26/c1-receipt-index.txt: No such file or directory (os error 2)   (exit 2)
```
File is ABSENT as expected.

Command 3 (fix-control, excluding the retained historical line):
```
$ grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l
0            (pipe exit 0)
```
**Toolchain caveat (verified).** On this host the shell `grep` is a builtin `pi-uu-grep 0.2.0`; `/usr/bin/grep` is GNU grep 3.12-modified. NEITHER treats `\|` as alternation in ERE:
```
$ printf '62 assertions\n77 assertions\n' | grep -cE '62 assertions\|77 assertions'   → 0 (exit 1)
$ printf '62 assertions\n77 assertions\n' | grep -cE '62 assertions|77 assertions'      → 2
$ printf '62 assertions\n77 assertions\n' | /usr/bin/grep -cE '62 assertions\|77 assertions' → 0
```
So the frozen regex forms in C1 counters 1 and 3 compile `\|` as a literal pipe/backslash form; their 0 outputs are vacuous under the regex semantics, not a content guarantee. **Content ground truth:** plain-ERE `grep -nE '62 assertions|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md` yields exactly one hit — `corpus/lessons/round-24.md:77` (`…`source-recheck.py` exits 0 over 19 records / 77 assertions.`), i.e. the retained historical line. Excluding that line → 0. This matches the R25-4 end state ("restated grep returns 0 hits"; the one remaining occurrence is the retained line), but if the verbatim frozen counters are the verification path, they cannot detect a reintroduced non-:77 "62 assertions"/"77 assertions" string (they stay 0). Flag for L1/executor.

Command 4 (deletion fixture) is defined as:
```
python3 corpus/instruments/recheck-audit.py --root <scratch-tree-with-one-knowledge-entry-deleted> --cdroot <lane-root>
```
Not run in this data-walk: it requires constructing a scratch tree with a knowledge entry deleted (executor instrumentation domain). `corpus/instruments/recheck-audit.py` exists.

## 2. Knowledge file census

```
$ git ls-files corpus/knowledge/*.md | wc -l
37
```
Glob count of `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/*.md` (gitignore=false, on disk) = **37** — same set of files.
`git status --porcelain corpus/knowledge/` → empty. **No untracked knowledge files; none modified.**

## 3. C2 frontier (corpus/README.md) + frontier-recheck-count.py

Frontier rows currently listed: F01..F10, all `admitted` (states: F01-F05 admitted at round 23; F06-F08 round 23; F09 round 24; F10 round 25 per README prose). **No F11 row present.**

C2 awk counter:
```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
10            (exit 0)
```

`corpus/instruments/frontier-recheck-count.py` exists. It counts per frontier row: `FRONTIER_ROW` regex parses each README frontier row into (id, title, status, entry_path); for each entry `entry_contract` collects the header `source:` id set (declared), every S-id in the body (cited), the `recheck:` line and its `--manifest`; the harness enforces (A) declared == cited ⊆ recheck ids (no cross-entry credit, no dropped id), (B) manifest exists, schema-valid, lists those ids, (C) invocation shape (`source-recheck.py` with `--manifest` + `--source`; no `true`, no `--selftest`, no whole-manifest run), then (D) executes the line from the lane root and uses its exit code as the entry's result. Exit 0 when every admitted frontier row passes, 1 otherwise, 2 on harness/read error. It measures recheck coverage only.

## 4. Sources census CLI

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```
Exit code = **0** (W04 warnings do not affect clean-lane exit).

## 5. SOURCES.md rows S039/S040

Actual registry header (line 5) is:
```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```
(11 columns). The assignment's expected label set `id|title|source|category|grade|read|recheck|used-by` does NOT match the file's actual header; the file is authoritative.

S040 row (line 46): id `S040` · source `Cisco Security Vulnerability Policy — https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` · kind `docs` · tier `A` · status `mined` · opened `2026-10-25` · **recheck = `180d`** · used-by = `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (only).

S039 row (line 45) exists: `日立グループにおける製品脆弱性情報の開示プロセス (HIRT-PUB10008) — https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html` · kind `docs` · tier `A` · mined · opened `2026-10-25` · recheck `180d` · teaches includes the ISO/IEC 29147:2014 and ISO/IEC 30111:2013 mapping (L497-L499) · used-by = both F10 entries (`vendor-disclosure-policies-as-corpus-objects.md`, `vendor-disclosure-policy-commitments-crosswalk.md`).

## 6. claims.json existence/immutability

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-26/claims.json` exists. HEAD = `1b076fa7f2fb5e7dd9d87449514eba526043421b` (commit "round-26: freeze claims.json (C1 gate conformance, C2 F11 assimilation) before any measurement or dispatch").
`git diff 1b076fa7f2fb5e7dd9d87449514eba526043421b -- .ufo/waves/round-26/claims.json` → empty (exit 0); `git status --porcelain -- .ufo/waves/round-26/claims.json` → empty. **Untouched, matches the freeze commit.**

## Notes

- Repo working tree has no modified tracked files. Untracked items (wave scaffolding, not part of this walk): `.ufo/waves/round-26/{assimilation/, build-wave1-spec.py, c1-live.json, wave1-dispatch.json, wave1-plan.json, wave1-spec.json, wave1/}`, `corpus/instruments/knowledge-expected.txt`, `corpus/source-snapshots/round-26/`. None under `corpus/knowledge/`.
- C2 counter `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` currently returns **1** (not 0): `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` line 2 begins `source: S040 — …` (round-25 entry). The frozen claims "before" says 0; the S04[0-9] span also matches S040 (first registered round 25), so the counter as frozen does not isolate rows first registered this round (S041+). Flag for L1/executor.
