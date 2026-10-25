# MatrixFreezeOrder — C1 fixture-matrix freeze order and control falsifiability

Seat: `L1Kasegi23.MatrixFreezeOrder-2` (critic, read-only). Frozen claim read: `.ufo/waves/round-23/claims.json` C1.
Artifacts attacked: `corpus/instruments/mirror-containment-fixtures.json`, `corpus/instruments/mirror-containment-check.py`,
`.ufo/waves/round-23/c1-baseline{,-resolver}.{json,py}`, `c1-fixed.json`.
All replays ran on copies under `/tmp/kasegi-r23-falsify-MatrixFreezeOrder`; the only repo write is this report.
No installs, no network, no live-target traffic.

Axes: `depth:verifiability` (does the freeze order support the fail-before/pass-after contrast, and is every pinned class falsifiable) and `coverage` (which C1 behaviours are pinned at all).

**Because the artifacts changed twice while I was reviewing them, every finding below is labelled with the state it holds in.** State table first; the substance follows.

| state | where | matrix | resolver `sha256` | receipts |
|---|---|---|---|---|
| S1 | `953c278`, files written 03:27:44–03:28:32 | 13 cases / 6 escapes, `sha256 5e61a33e…b5e76a9` | `ed9a9dae…2840e9` | 13 cases, matrix `5e61a33e` |
| S2 | working tree at 03:43, transient, uncommitted | 20 cases / 9 escapes, `4e39f65c…c2400b` | `9e0b5751…5d7cde` | **17 cases**, matrix `5c64e014…`, i.e. stale by 3 |
| S3 | HEAD `4d9231e` (after `2712c99`), post-attack repair | 20 cases / 9 escapes, `4e39f65c…c2400b` | `8dd45bc8…388648` | 20 cases, matrix `4e39f65c` — consistent |

---

## 1. Answer: tuning after the baseline run is **excluded**; tuning before it is **not**

**Excluded at S1, by content-addressed binding and inode time.** Both S1 receipts record the matrix they ran:

```text
$ sha256sum corpus/instruments/mirror-containment-fixtures.json        # S1 bytes
5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9
$ python3 -c "import json;[print(f, json.load(open(f))['matrix_sha256']) for f in ('.ufo/waves/round-23/c1-baseline.json','.ufo/waves/round-23/c1-fixed.json')]"
.ufo/waves/round-23/c1-baseline.json 5e61a33e…b5e76a9
.ufo/waves/round-23/c1-fixed.json    5e61a33e…b5e76a9
```

S1 `stat` shows one inode lifetime (`ctime == mtime` to the nanosecond, so the file was created and never edited afterwards), and the matrix predates both receipts:

```text
resolve.py                       mtime=2026-10-25 03:27:44.381977020
mirror-containment-fixtures.json mtime=2026-10-25 03:28:11.864283451 ctime=same
mirror-containment-check.py      mtime=2026-10-25 03:28:25.572284895
c1-baseline-resolver.py          mtime=2026-10-25 03:28:28.805308795
c1-baseline.json                 mtime=2026-10-25 03:28:29.159339383
c1-fixed.json                    mtime=2026-10-25 03:28:32.643994999
```

Any S1 expectation edited after the baseline run would break the recorded hash, and no second 13-case version exists in VCS: `git rev-parse` returns the same blob `4ede1bcc` in all four commits that carry the file (`953c278 52ee05c 87dbd03 b284aff`), `git cat-file -e 8bf9807:…fixtures` fails, and `git log --follow` names `953c278` as the introducing commit. I replayed both S1 receipts byte-for-byte (per-case, not just totals):

```text
$ python3 mirror-containment-check.py --json A-fixed.json | tail -1
cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=ed9a9dae… matrix_sha256=5e61a33e…
$ python3 mirror-containment-check.py --resolver c1-baseline-resolver.py --json B-baseline.json | tail -1
cases=13 escape=6 controls=7 pass=7 fail=6 resolver_sha256=d6a3c3f1… matrix_sha256=5e61a33e…
committed==replayed baseline per-case: True
committed==replayed fixed per-case: True
```

The do-nothing control is genuine provenance, not a weakened copy:

```text
$ git show 922a4dd:corpus/instruments/resolve.py | sha256sum  → d6a3c3f1…d869f903
$ sha256sum .ufo/waves/round-23/c1-baseline-resolver.py       → d6a3c3f1…d869f903   (cmp - → identical)
```

**Not excluded: the matrix was authored with the fixed bytes already on disk, and no claim-level artifact pre-registers it.** At S1 the fixed `resolve.py` hit disk at `03:27:44`, 27 s *before* the matrix (`03:28:11`), and the matrix's only committed version arrives in the same commit as the fix and its receipts. `claims.json` pre-registers nothing about the matrix: it contains no 64-hex digest and no `matrix_sha256` key (`re.findall(r'[0-9a-f]{64}', raw)` → `[]`; `'matrix_sha256' in raw` → `False`), and its only occurrences of "fixture" are prose inside `C1.after` ("identical fixture inputs"). Its C1 fields are `['after','axis','before_observed','claim','detector','guard']` with no hash/fixture field. So the only dated evidence of expectations is the matrix file itself, produced after the fix existed; nothing distinguishes "written from the claim" from "written after watching the fixed resolver".

**The churn then materialised live.** At 03:43, between two of my reads, the working tree held the 20-case matrix (`4e39f65c`) while both receipts still described a **17-case** matrix (`5c64e014`); the three unreceipted cases were exactly `brace-expansion-escape`, `glob-expansion-escape`, `brace-expansion-confined-control`. That transient is direct evidence for the structural point: a receipt binds the matrix only until the next edit, and nothing in `claims.json` anchors either.

By HEAD `4d9231e` the receipts were re-cut to 20 cases and the binding is consistent again. S3 on-disk order: checker `03:43:01`, fixtures `03:43:38`, receipts `03:46:26`/`03:46:27`; commits `2712c99` (author date 03:36:25) and `4d9231e` (03:46:43). `2712c99` claims the 20-case matrix while its author date precedes the file's 03:43:38 mtime, so commit dates in this jj-exported history do not order file states — only mtimes plus the receipt hashes do.

```text
$ python3 -c "…"   # S2 observation
matrix cases 20 receipt cases 17
in matrix not receipt: ['brace-expansion-escape', 'glob-expansion-escape', 'brace-expansion-confined-control']
receipt matrix_sha 5c64e014…  actual matrix sha 4e39f65c…
# after 2712c99/4d9231e:
receipt totals {'cases': 20, 'controls': 11, 'escape': 9, 'fail': 0, 'pass': 20} matrix_sha 4e39f65c… actual 4e39f65c…
```

---

## 2. The authoring record matches **no** landed matrix

`.ufo/waves/round-23/build/CountMirror.md` is the seat that authored the fixtures; it is present in commit `8bf9807` with on-disk mtime 2026-10-20 18:46:39, and states:

> `:30` The committed JSON matrix has 15 IDs. Its eight distinct escaped-path cases all pin `GONE`:
> … `placeholder-expansion-escape`, `glob-expansion-escape`, `canonical-tilde-alias-parent-escape`, `canonical-absolute-alias-symlink-escape`, … `empty-citation-produces-no-row`

Landed matrices observed: 13 IDs (S1), 17 (S2 receipts), 20 (S3, committed). None is 15, and the dropped IDs appear in four commits always and only inside that note:

```text
$ grep -rln "empty-citation-produces-no-row\|placeholder-expansion-escape\|glob-expansion-escape\|canonical-tilde-alias-parent-escape" --exclude-dir=.git .
./.ufo/waves/round-23/build/CountMirror.md        # only hit
$ for c in 893b816 f9462ad e812b74 8bf9807; do git ls-tree -r --name-only $c | grep -i mirror-containment; done
(no output: no mirror-containment file in any pre-953c278 commit)
$ for c in 8bf9807 e812b74 f9462ad 893b816; do git grep -l "placeholder-expansion-escape" $c; done
→ CountMirror.md in each commit, nothing else
```

The note is therefore not a description of any artifact that ever existed in the repository. It is also not the only stale description: it advertises JSON-Lines output, duplicate/unexpected-citation checks and matrix-size bounds. The S1 checker had none of those (`grep -n "distinct\|duplicate\|unexpected\|MAX_\|bound" …` → no output); the S3 checker added `MAX_STDOUT_STORED`, `MAX_TSV_BYTES`, `safe_path()` fixture-name confinement and a `resolved_path` assertion (`bound = {"MIRROR-EQUIVALENT": mirror, "INTERNAL": lane}.get(expect, root)`), but still no distribution invariant (see §4).

---

## 3. Escape-set changes: one new escape is green **before** the fix, and the over-rejection is still unpinned

At S3 the matrix has 9 escapes and 11 controls. Replaying it against the ancestor resolver:

```text
$ python3 check-now.py --fixtures fixtures20.json --resolver c1-baseline-resolver.py | tail -1
cases=20 escape=9 controls=11 pass=12 fail=8 resolver_sha256=d6a3c3f1… matrix_sha256=4e39f65c…
```

Eight escapes fail pre-fix; **`glob-expansion-escape` passes pre-fix**. Its fixture explains why:

```json
{"id":"glob-expansion-escape","cite":"~/Projects/bounties/<name>.md:1",
 "dirs":["relocated/outside-vault"],
 "files":{"relocated/outside-vault/x.md":"glob match outside the mirror\n"},
 "note":"Placeholder rewrite matches only outside the mirror through a relative hop; …"}
```

The cite contains no relative hop, and `x.md` sits under neither candidate root (`home/Projects/bounties/*.md`, `relocated/tbh/*.md`), so no candidate can ever match it. The case names a "relative hop" its own citation does not have. Its expected `GONE` is entailed by fixture construction, not by resolver behaviour — it cannot move under either resolver, and it cannot detect the leak it is labelled for. Compare `brace-expansion-escape` (`~/Projects/bounties/{../outside.md,missing.md}:1`, file `relocated/outside.md`), which does carry the hop and does fail pre-fix: `MIRROR-EQUIVALENT` at baseline → `GONE` at S3. So the escape denominator is 9 but the red-before set is 8.

Still unpinned at S3 — the confined-alongside-escaping shape. `brace-expansion-confined-control` (`~/Projects/bounties/{ops,missing}/rank.mjs:1`) has a *missing* first alternative, not an escaping one; it never exercises candidate filtering. Replaying both shapes the build notes describe, on the current checker and resolver:

```text
$ python3 check-now.py --fixtures fixtures-probe20.json --resolver resolve-now.py | grep -E "alongside|cases="
glob-confined-alongside-escaping-sibling   control expect=MIRROR-EQUIVALENT actual=GONE FAIL
brace-confined-alongside-escaping-sibling  control expect=MIRROR-EQUIVALENT actual=GONE FAIL
cases=22 escape=9 controls=13 pass=20 fail=2
```

Expectations are the authoring seat's, not mine:

- `build/GlobEscape.md:10-11` — "**Expected under C1:** `MIRROR-EQUIVALENT`, with `resolved_path == <selected-mirror>/ops/z-confined.mjs` … the valid confined match must remain usable, while no outside target is credited"; compatibility invariant: "Filter every glob candidate by realpath containment before selecting the first acceptable result."
- `build/BraceEscape.md:20` — "For bounty fallback, a real file under the selected mirror must remain `MIRROR-EQUIVALENT`."

`classify()` still takes `matches[0]`, tests `under_mirror()` on that one path, and on failure returns `GONE` for the whole citation — discarding a confined candidate in the same directory. The S3 matrix cannot register that, because it has no case where an escaping candidate sorts before a confined one.

`empty-citation-produces-no-row` (dropped from the note's 15) also diverged by state: on S1 bytes the CLI aborted (`max() arg is an empty sequence`, `problems=cli-exit-1`); S2's `max(..., default=0)` and S3 fixed it. The note's plan to submit it "beside non-empty citations" remains unimplementable in a harness that gives every case its own root, which is presumably why it is absent.

---

## 4. Control audit: all 11 are pre-fix invariants; two classes are entailed by construction; the guard is 9 cases

Baseline on the S3 matrix passes 12 cases: **all 11 controls plus the vacuous `glob-expansion-escape`**. So every control's expected class equals its pre-fix class, and `11/11 controls preserved` restates "nothing moved" rather than evidencing the fix. Controls can only detect over-correction.

Two expectations are unfalsifiable by construction in the strict sense — no other outcome is reachable from the fixture:

- `missing-bounty-target-control` (`GONE`) — no file is created anywhere; nothing exists to confine.
- `glob-expansion-escape` (`GONE`) — the only file is outside both candidate roots and the cite has no hop (§3). Labelled `escape`, it belongs in the control column.

Two of the eleven controls also pin `GONE`, the same value as every escape, so a classifier that answers `GONE` universally satisfies them:

```text
$ python3 check-now.py --fixtures fixtures20.json --resolver degenerate-gone.py | tail -1
cases=20 escape=9 controls=11 pass=11 fail=9      # 9 escapes + 2 GONE controls
```

The anti-degeneracy guard is therefore 9 cases (the non-`GONE` controls), not 11, and not 20. S3's `resolved_path` assertion does now catch the degenerate stub (`path_check=missing-path` on the non-`GONE` rows), which is a real improvement over S1.

The checker still enforces no distribution invariant: a matrix whose every expectation is `GONE` is accepted at `2/2, exit 0`.

```text
$ python3 check-now.py --fixtures fixtures-goneonly.json --resolver degenerate-gone.py
cases=2 escape=0 controls=2 pass=2 fail=0 … exit=0
```

That is the mechanism by which an escape-set edit (8 → 9, with one vacuous member) can raise a pass count without raising discriminating power; nothing in the instrument objects.

---

## 5. Smallest safe correction

1. **Pre-register the matrix.** Put `matrix_sha256` and the case IDs in `claims.json` (or a dated wave-spec field) before the resolver changes. This wave has no such anchor, and the 03:43 file/receipt divergence shows why the in-receipt hash is not a substitute. If back-filling, date it as a back-fill; do not claim the S3 matrix predates the fix.
2. **Fix or relabel `glob-expansion-escape`.** Either give it a cite that carries the hop (`~/Projects/bounties/../outside-vault/<name>.md:1`) and keep `expect: GONE`, or declare it a control. As written it is green pre-fix and its expected class is entailed.
3. **Add the two `confined-alongside-escaping-sibling` cases** with `expect: MIRROR-EQUIVALENT` (per `GlobEscape.md`/`BraceEscape.md`). They currently fail on committed bytes, so adding them forces the candidate-filtering fix; omitting them leaves the over-rejection unpinned.
4. **Add a distribution invariant** to the checker: refuse a matrix with no `MIRROR-EQUIVALENT`/`RESOLVES` expectation, and reject an `escape`-natured case that passes on the baseline resolver (a red-before self-check). `--resolver` already exists, so the second check is a few lines.
5. **Reconcile `build/CountMirror.md:30-47`.** It describes 15 IDs and four families that no landed matrix contains; either mark it as the unarchived private-clone draft or delete the claim.

---

## 6. Scope limits

- Only `/tmp` scratch with copied bytes; no live corpus run, no `mirror=` claim, no score or admission claim.
- Byte anchors: §1 S1 replays use `resolve.py ed9a9dae`; §3/§4 use the committed `8dd45bc8` with checker `53742c8d` and matrix `4e39f65c` at HEAD `4d9231e`. The S2 observation is a snapshot of an uncommitted intermediate state and is reported as such.
- The confined-alongside expectations come from the 10-20 build notes, not from frozen C1 text; C1's "Preserve valid confined mirror … controls" is the claim-level hook, but it does not say "expansion controls". I report the behaviour as unpinned and note-contradicting, not as a C1 violation on its own.
- Pattern citations (`*.mjs`, `<name>.md`, `{a,b}`) are synthetic and flagged `noise=synthetic` by the resolver; whether the corpus ever contains one is untested here.
- I did not inspect C2 artifacts, did not run the fleet repo, and read no tool beyond local ones.
- Sibling writes during the review changed `resolve.py`, the fixtures, the checker and both receipts, and added commits `2712c99`/`4d9231e`; those are their changes, not mine. The `resolve.py` modification was still uncommitted at the time of my `git status` check and is committed by HEAD `4d9231e`.
