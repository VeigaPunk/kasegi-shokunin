# QuarterRouted2 — routed defect 2 (brace/glob dispatch liveness) on committed bytes

Seat: reviewer, read-only. Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin, tip
`c2480b143120364728b40397926ffcf30a7309c8` (2026-10-25 04:01:02 -0300); C1 base
`d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`.

## Byte state (read this first)

The lane working tree is **dirty**: `corpus/instruments/resolve.py` was rewritten at
04:14:32 with an uncommitted fix while this review was open. Two distinct byte sets, both
pinned by sha256:

```
HEAD:corpus/instruments/resolve.py                              690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
.ufo/waves/round-24/c1-baseline-resolver.py                     690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
/tmp/kasegi-r24-qr2/bin/resolve-committed.py  (cp -p of HEAD)   690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
working-tree corpus/instruments/resolve.py (uncommitted edit)   035f8844e66357f6dbe6f1158776978f2ce1103108e222d0746afdef9521b661
HEAD:corpus/instruments/mirror-containment-check.py             dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a  (== working tree)
corpus/instruments/resolve-dispatch-check.py (UNTRACKED)        88090efca9860a83677f7118813f0e34e945b09aaaf2dc8a584464b7b2b47b69
corpus/instruments/resolve-dispatch-fixtures.json (UNTRACKED)   5133e98e656f07d2454f1f4799d4b0b5e5ab260ea69b1fd9d1cade3e0f9628b6
```

`cmp corpus/instruments/resolve.py .ufo/waves/round-24/c1-baseline-resolver.py` was clean at
copy time: **the frozen C1 "before" bytes are exactly HEAD bytes** (690153ad). Every claim
below is against 690153ad unless labelled worktree. Extracted HEAD blobs and the worktree
snapshot live at `/tmp/kasegi-r24-qr2/head/` and `/tmp/kasegi-r24-qr2/wt/`; probe is
`/tmp/kasegi-r24-qr2/probe.py` (invokes `brace_expand`, `exists_any`, `classify` by
`importlib` from the byte-copy). Nothing in the lane or fleet tree was written.

## Finding 1 (HIGH) — empty brace alternative never resolves: `brace_expand()`'s `continue` (HEAD, live)

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py:174-176` (HEAD):

```python
174    for alt in sorted(m.group(1).split(",")):
175        if not alt.strip():
176            continue          # `{}` / `{,x}` empty alternative is not a resolvable expansion
```

Probe, fixture `case1` = `dir/x.md` only (no `dir/sub/`), cite `dir/{,sub}/x.md`, lane root =
fixture root, resolver = 690153ad:

```
cite: dir/{,sub}/x.md
os.path.exists(<case1>/dir/x.md): True
brace_expand: ["/tmp/kasegi-r24-qr2/fixtures/case1/dir/sub/x.md"]
exists_any: (None, None)
classify: ('GONE', '', '', 'rel')
exists_any dir//x.md: ('literal', '/tmp/kasegi-r24-qr2/fixtures/case1/dir//x.md')
```

Code path: `sorted(["", "sub"])` puts `""` first; `:175-176` discards it instead of splicing
`path[:m.start()] + "" + path[m.end():]` — which is `dir//x.md` and **does** exist (the
`('literal', …/dir//x.md)` line proves the expansion is resolvable). The surviving alternative
`dir/sub/x.md` misses; the glob fallback at `:192-196` is ineligible because `{,sub}` contains
no GLOBMETA char and no `<...>` placeholder, so `exists_any` returns `(None, None)` and
`classify` falls through to `GONE`. Affected return sites on HEAD: REL `:264-271`, bounty
fallback `:247-250`, explicit-canonical mirror `:256-259`, REL mirror fallback `:267-270`.
This is a class false negative, not a missing file.

Shell truth for the same idiom — the corpus reads `{,-board}` as a brace set:

```
$ cd /tmp/kasegi-r24-qr2/bashcheck && printf '%s\n' dir/{,sub}/x.md
dir//x.md
dir/sub/x.md
exists dir//x.md yes
exists dir/sub/x.md no
```

Shipped corpus exposure (self-references inside `corpus/instruments/` excluded):

```
SKILL.md:1000:`~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh`
corpus/knowledge/source-tree-loss-2026-09-28.md:92:`.omp{,/agents}`
```

Both put the empty alternative first and denote a genuinely shipped name (`sighting.sh`,
`.omp`); both classify GONE under HEAD. Live-corpus confirmation is blocked here: neither
mirror candidate exists (`~/Projects/the-bounty-hunter False`,
`~/Projects/origin-work/the-bounty-hunter False`), so the claim is instrument-level only.

## Finding 2 (HIGH) — glob branch credits `matches[0]` with no existence test: a dangling symlink sorts before the live file (HEAD, live)

`resolve.py:192-196` (HEAD, `exists_any`):

```python
192    q = PLACEHOLDER.sub("*", p)
193    if any(ch in q for ch in GLOBMETA):
194        matches = sorted(globmod.glob(q, recursive=True))
195        if matches:
196            return "glob", matches[0]
```

Probe, fixture `case2`: `dir2/a.md` is a symlink to `/tmp/kasegi-r24-qr2/no-such-target`,
`dir2/b.md` is live; cite `dir2/<note>.md`:

```
glob pattern: /tmp/kasegi-r24-qr2/fixtures/case2/dir2/*.md
sorted glob: ['/tmp/kasegi-r24-qr2/fixtures/case2/dir2/a.md', '/tmp/kasegi-r24-qr2/fixtures/case2/dir2/b.md']
exists_any: ('glob', '/tmp/kasegi-r24-qr2/fixtures/case2/dir2/a.md')
returned resolved_path exists: False
resolved_path islink: True
classify: ('INTERNAL', '/tmp/kasegi-r24-qr2/fixtures/case2/dir2/a.md', 'glob', 'rel')
live sibling exists: True
```

`glob.glob` enumerates dangling symlinks, so `sorted(...)[0]` selects a path that is not on
disk even though `dir2/b.md` is a live match. `classify` still returns a resolving class
(`INTERNAL`) with a phantom `resolved_path`; the same single-path selection decides
containment on the lure for the mirror/bounty fallbacks, so a live confined sibling cannot
rescue the row. Class-only instruments pass this row; the frozen matrix's own path column
(`path_verdict`, `mirror-containment-check.py:145-158`, `path-missing-on-disk`) falsifies it:

```
FAIL     glob-dangling-first-match   expect=INTERNAL  actual=INTERNAL  method=glob  path=<CASE>/lane/refs/a-lure.md path_check=path-missing-on-disk
```

## Finding 3 (HIGH for C1's counter) — the fix exists only as an uncommitted working-tree edit; HEAD still scores 4/8 and 0/3

The 04:14:32 worktree edit (035f8844) removes the `continue`, adds `sorted(set(out))[:64]`,
and replaces `matches[0]` with a first-`os.path.exists` loop. Pinned on that snapshot, the
same matrices go green; on HEAD they stay red:

```
HEAD 690153ad:  cases=8 pass=4 exit=1   (dispatch matrix)
HEAD 690153ad:  cases=3 pass=0 fail=3   (r23 brace-empty-alt matrix)
worktree 035f8844: cases=8 pass=8 exit=0
worktree 035f8844: cases=3 pass=3 fail=0
```

Consequence for C1: the frozen "before" artifact (`c1-baseline-resolver.py`, 690153ad) is
byte-identical to HEAD, so the do-nothing control reproduces 4/8 and 0/3 exactly as claimed —
but any after-receipt taken now measures uncommitted bytes. Until 035f8844 is committed, a
clean checkout still scores 4/8 and C1's after-target is not evidenced from committed state.
HEAD's docstring is self-consistent with its own defective code (`resolve.py:71-74` says
"first match wins", never mentions the empty alternative), so there is no docstring-truth
finding at HEAD; the truthfulness of the docstring exists only in the uncommitted edit.

## Finding 4 (MEDIUM) — the round-23 `brace-empty-alt` matrix is not committed; only a `/tmp` copy survives

```
$ git ls-files --error-unmatch .ufo/waves/round-23/falsify/brace-empty-alt-fixtures.json
Did you forget to 'git add'?
$ ls .ufo/waves/round-23/falsify/*.json
refusal-1.json  swarm-registry.json
```

`BraceGlobProbe.md:36-38` claims `.ufo/waves/round-23/falsify/brace-empty-alt-fixtures.json`
(3 cases, sha256 `8ebd1a53…`). It exists only at
`/tmp/kasegi-r23-falsify-BraceGlobProbe/brace-empty-alt-fixtures.json`, sha
`8ebd1a53922d96ea5acc6fae0461a344a80d8712f4a8db162d398ec0d0fc2f91` — matching the claim, but
volatile. Any receipt keyed to it stops being reproducible once `/tmp` is cleared.

## Finding 5 (MEDIUM) — counter B's instrument and matrix are untracked, so the counter is not reproducible from a clean checkout

```
corpus/instruments/resolve-dispatch-check.py        UNTRACKED
corpus/instruments/resolve-dispatch-fixtures.json   UNTRACKED
corpus/instruments/resolve.py                       tracked
corpus/instruments/mirror-containment-check.py      tracked
```

The claims' counter-B command
(`python3 corpus/instruments/resolve-dispatch-check.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json`)
has no committed input on a fresh clone. Both files must be committed before the receipt
counts; their current bytes are pinned above (88090efc / 5133e98e).

## Re-ran round-23 `brace-empty-alt-fixtures.json` claim (0/3) — CONFIRMED on HEAD

```
$ cd /tmp/kasegi-r24-qr2/head   # HEAD:resolve.py + HEAD:mirror-containment-check.py, pinned above
$ python3 mirror-containment-check.py --fixtures /tmp/kasegi-r23-falsify-BraceGlobProbe/brace-empty-alt-fixtures.json --resolver ./resolve.py
brace-empty-alt-live-root                  control expect=RESOLVES         actual=GONE             FAIL path_check=missing-path
brace-empty-alt-mirror-fallback            control expect=MIRROR-EQUIVALENT actual=GONE             FAIL path_check=missing-path
brace-empty-alt-dotted-idiom               control expect=RESOLVES         actual=GONE             FAIL path_check=missing-path
cases=3 escape=0 controls=3 pass=0 fail=3 resolver_sha256=690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d matrix_sha256=8ebd1a53922d96ea5acc6fae0461a344a80d8712f4a8db162d398ec0d0fc2f91
```

Exactly the matrix exists (not "not committed" and not "no such claim"): 0/3 on HEAD. The
same 0/3 holds on the round-24 baseline artifact because the bytes are the same blob, which
also proves no r23/r24 edit ever touched the empty-alternative path before 04:14:32 today.

## Frozen dispatch matrix on HEAD — 4/8, and all four failures are these two defects

```
$ cd /tmp/kasegi-r24-qr2/head && python3 resolve-dispatch-check.py --fixtures resolve-dispatch-fixtures.json --resolver ./resolve.py
checker_sha256=88090efca9860a83677f7118813f0e34e945b09aaaf2dc8a584464b7b2b47b69
FAIL     lane-brace-empty-first-alternative                   expect=INTERNAL         actual=GONE             method=         path=- path_check=missing-path
FAIL     lane-brace-empty-second-alternative                  expect=INTERNAL         actual=GONE             method=         path=- path_check=missing-path
FAIL     glob-dangling-first-match                            expect=INTERNAL         actual=INTERNAL         method=glob     path=<CASE>/lane/refs/a-lure.md path_check=path-missing-on-disk
FAIL     bounty-brace-empty-alternative-mirror-fallback       expect=MIRROR-EQUIVALENT actual=GONE             method=         path=- path_check=missing-path
PASS     control-literal-hit                                  expect=INTERNAL         actual=INTERNAL         method=literal  path=<CASE>/lane/plain/present.md
PASS     control-absent-face                                  expect=GONE             actual=GONE             method=         path=-
PASS     control-glob-two-live-matches                        expect=INTERNAL         actual=INTERNAL         method=glob     path=<CASE>/lane/refs4/a-live.md
PASS     control-skill-brace-idiom                            expect=INTERNAL         actual=INTERNAL         method=brace    path=<CASE>/lane/ops/finalize-all.mjs
cases=8 pass=4 exit=1
```

`lane-brace-empty-second-alternative` (`notes/{sub,}/b.md`) also fails: `sorted()` puts `""`
first regardless of its written position, so both empty-alternative orders hit the same
`continue`. The `glob-dangling-first-match` row is the only failure whose class looks right;
its `path_check` is what catches the dangling credit — a class-only scoring of this matrix
would report 5/8 and hide the defect.

Worktree snapshot 035f8844 for contrast (pinned, same runner dddd5549):

```
cases=8 pass=8 exit=0
glob-dangling-first-match  path=<CASE>/lane/refs/z-live.md   (first live match, not the lure)
lane-brace-empty-first-alternative  path=<CASE>/lane/notes//a.md
bounty-brace-empty-alternative-mirror-fallback  path=<CASE>/relocated/tbh//rank.mjs
```

## Residual risk / verification gaps

- Live-corpus impact of Finding 1 on the two shipped cites (`SKILL.md:1000`,
  `corpus/knowledge/source-tree-loss-2026-09-28.md:92`) is UNVERIFIED on this host: both mirror
  candidates are absent, so the referenced bounty files cannot be confirmed on disk. The
  defect is proved at instrument level only.
- No symlink exists anywhere in the lane tree
  (`find . -path ./.git -prune -o -type l -print` → empty), so Finding 2's exposure is
  fixture/matrix level today; it goes live as soon as a cited directory holds a broken link
  whose name sorts before a live match.
- Finding 3 is a moving target I do not own: the integration seat may commit or further edit
  035f8844. My after-side measurement is pinned to that sha256 and the HEAD runner; re-run
  `resolve-dispatch-check.py` against the committed resolver after L1 commits.
- C1's counter-B command still names an untracked instrument (Finding 5); until both files
  are committed, C1's kill rule ("either counter is not reproducible from committed bytes by
  one command") is unsatisfied even at 8/8.
- Fix shape is L1's design call; the probes imply: splice the empty alternative (a real
  expansion once the surrounding path resolves) and, in the glob branch, return the first
  match that exists rather than `matches[0]` (035f8844 does exactly this and passes 8/8).

## Installs
None. No package manager, tool, or runtime was installed or upgraded for this seat (pacman is
paused host-wide per the contract; nothing was needed).
