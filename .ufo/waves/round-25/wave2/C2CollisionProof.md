# C2CollisionProof — wave-2 falsification of the §10 id-collision scan and S002 guard fixture

Lane: `kasegi-shokunin`. Round 25, wave 2. Base revision `b49948f1`.
Target attacked: `.ufo/waves/round-25/assimilation/ids/{reg-ids,staged-ids,collisions}` and
`fixture/` + `guard-proof.{sh,txt}` as reported in `.ufo/waves/round-25/wave1/CollisionGuard.md`
and `.ufo/waves/round-25/assimilation/ids/renumber-map.md`. Scope: S031–S035 only.

## Verdict

**WAVE-1 RESULT STANDS — confirmed, not refuted.** Re-running the 0-3-space collision scan
reproduces exactly the claimed `S031 S032 S033 S034 S035` set against the receipt's 35-row
registry, and a byte-for-byte sandboxed re-run of `guard-proof.sh` reproduces the indented-S002
proof (`a-collisions` = `S002`, `b-collisions` = empty). Every S031–S035 collision is an
id-space overlap between different documents, as `renumber-map.md` §3 claims. No production
file was edited; all scratch went to `/tmp/c2proof` and `/tmp/c2fix`.

Two honest caveats, neither fatal to the claim: (1) today's raw re-run yields **10** collisions,
not 5 — the delta S036–S040 is caused by the post-receipt, still-uncommitted append of five rows
to `corpus/SOURCES.md`, not by a wave-1 error; (2) `guard-proof.sh` is **cwd-dependent** and its
transcript only reproduces when run from the lane root (details §3).

## 1. Re-run of the 0-3-space collision scan (real inputs)

Commands (lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`), identical in form to
`CollisionGuard.md` §2:

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > /tmp/c2proof/reg-ids.now        # exit 0
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > /tmp/c2proof/staged-ids.now   # exit 0
$ comm -12 /tmp/c2proof/reg-ids.now /tmp/c2proof/staged-ids.now > /tmp/c2proof/collisions.now     # exit 0
$ wc -l reg-ids.now staged-ids.now collisions.now
 40  94  10
$ cat collisions.now
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
```

Scoped back to the receipt's registry (`comm -12` of the committed `reg-ids` receipt vs today's
staged scan) — the named scope S031–S035:

```
$ comm -12 .ufo/waves/round-25/assimilation/ids/reg-ids /tmp/c2proof/staged-ids.now
S031
S032
S033
S034
S035        # exit 0 — byte-identical to committed assimilation/ids/collisions
```

Diffs vs committed receipts:

- `staged-ids` (94 ids): **identical** — `diff` exit 0. Staged file untouched since
  Oct 24 23:33 (`ls -la`), still S031–S124 contiguous (verified by script).
- `reg-ids` (35 ids): today's scan adds `S036–S040` — `diff` exit 1, `35a36,40`.
  Cause: `git status` shows `corpus/SOURCES.md` **modified-uncommitted**; `git show
  HEAD:corpus/SOURCES.md | grep -cE '^ {0,3}\|…'` = **35** (matches the receipt), while the
  worktree file has 40 pattern hits. `git diff` shows exactly five `+| S036…S040` rows, bound to
  the URLs `renumber-map.md` predicted (cybozu.co.jp ×2, pepabo.com, hitachi.co.jp, cisco.com).
- `collisions`: same delta; receipt content S031–S035 is a strict subset of today's set.

**Each S031–S035 collision is between different documents** (row-level evidence, `grep -nE
'^\| S03[1-5] \|'` on both files):

| id | lane URL (corpus/SOURCES.md L37–L41) | staged URL (SOURCES.append.md L7–L11) |
|---|---|---|
| S031 | `…cve.org/…/CNA_Rules_v4.2.6.pdf` | `hackerone.com/security/policy_versions` |
| S032 | `nvlpubs.nist.gov/…/nistspecialpublication800-115.pdf` | `raw.githubusercontent.com/bugcrowd/…/README.md` |
| S033 | `laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` | `…/bugcrowd/…/mappings/cwe/cwe.json` |
| S034 | `www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` | `zc.cnvd.org.cn/news/helpList` |
| S035 | `www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` | `security.360.cn/Reward/rules` |

Matches `renumber-map.md` L53–L57 verbatim → "no arithmetic" conclusion is grounded, and the
new S036–S040 overlaps are also id-space (staged S036–S040 = BILISRC, GB/T 30279 ×2, e-Gov,
総務省 — different documents again).

**Scan blind spots probed** (real inputs): `uniq -d` self-collisions = 0/0; rows indented ≥4
spaces = 0/0; tab-indented rows = 0/0; so `^ {0,3}\|` misses nothing present today. Rows with
interior decoration (e.g. `| **S001**`) would be missed — none exist (every row hits the pattern;
94/94 and 40/40 = column-zero counts).

## 2. Indented S002 guard fixture — sandboxed re-run

`guard-proof.sh` writes its six scratch outputs next to the committed receipts, so the re-run
was sandboxed (`cp -r` of `fixture/` + script to `/tmp/c2fix`), preserving the lane tree
read-only:

```
$ cd /tmp/c2fix && bash .ufo/waves/round-25/assimilation/ids/guard-proof.sh > guard-proof.now.txt 2>&1   # script exit 0
$ for f in a-reg-ids a-staged-ids a-collisions b-reg-ids b-staged-ids b-collisions; do diff -q <lane>/fixture/$f /tmp/c2fix/…/fixture/$f; done
→ all six files IDENTICAL
$ wc -c fixture/a-collisions fixture/b-collisions
5 a-collisions        # "S002\n"
0 b-collisions        # empty — column-zero-only pattern misses the indented row
```

Transcript diff vs committed `guard-proof.txt`: only two hunks —
lane-root echo line (sandbox cwd) and one D-section grep erroring on a relative path (§3).
All A/B/C output lines identical: A catches `S002` (2 reg ids, 2 staged ids, 1 collision);
B reports 1 reg id, 0 collisions.

Fixture byte check: `sed -n '10p' fixture-SOURCES.md | od -c` → line starts with two spaces
then `| S002` — the "indented by two spaces" premise is true.

## 3. Findings

1. **[Low] `guard-proof.sh` is cwd-dependent; transcript not reproducible off lane root.**
   `guard-proof.sh:52` greps `corpus/SOURCES.md` (relative) while its sibling D commands at
   lines 51/53/54 use absolute paths. Run from any other cwd the command prints
   `grep: corpus/SOURCES.md: No such file or directory` and exits **2**, whereas the committed
   transcript claims `0` / `[exit 1]` (`guard-proof.txt:86-88`). In the lane root it
   reproduces exactly (re-run: `0`, exit 1). Smallest correction: make line 52 absolute like
   its siblings, or `cd` to the lane root at the top of the script. Cosmetic — the
   reproducibility claim "reproducible via `bash …/guard-proof.sh`" is only true from lane root.
2. **[Info] Post-receipt drift, not error.** `guard-proof.txt:98` and `CollisionGuard.md:139`
   summarise "94 staged, 35 registered". Today the registered side is 40 (uncommitted append of
   S036–S040). Same re-run: append greps still `0`/`94`/`94`; corpus greps `0` (exit 1) /
   `40`. Receipt numbers were correct at scan time.
3. **[Info] The assimilation/ids tree is untracked.** `git status` reports
   `?? .ufo/waves/round-25/assimilation/ids/` — "committed wave-1 receipts" is loose language;
   they are worktree files, not VCS objects. No evidence of tampering: file mtimes (05:25–05:29)
   bracket the round-25 wave-1 window and contents re-derive byte-identically.

## 4. Residual risk

- The 0-3-space guard still misses `^\t\|` and `^ {4,}\|` rows (CommonMark code blocks, not table
  rows) and duplicate ids *within* one file — all measured absent today (0 hits each).
- `comm -12` correctness rests on identical `LC_COLLATE` for `sort` and `comm`; ids are ASCII
  `S`+digits so collation order is unambiguous.
- Today's 10-collision raw scan is the *correct* current answer; anyone diffing receipts against
  a fresh scan must filter to the pre-append 35-id registry, as done here.

## 5. Tooling record

None installed or upgraded. `grep`, `comm`, `sort`, `wc`, `diff`, `od`, `git`, `python3`,
`bash` from the base system; pacman pause respected (no transaction attempted).
