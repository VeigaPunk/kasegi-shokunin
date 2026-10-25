# LivenessMatrix — C1 counter-B instrument (round 24)

Seat: `L1Kasegi24.LivenessMatrix` (executor, leaf). Work done only in the private clone
`/tmp/kasegi-r24-LivenessMatrix`, created with `git clone --no-hardlinks` and checked out at the
frozen base `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` (`git rev-parse HEAD` = d0a3f6a…). The lane
tree was not edited by this seat except for this report; `corpus/instruments/resolve.py` in the lane
was modified by another seat **before** this report was written (see F4), and is not my edit.

Deliverable (in the clone, for L1 to integrate):
- `corpus/instruments/resolve-dispatch-check.py` — sha256 `acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1`
- `corpus/instruments/resolve-dispatch-fixtures.json` — sha256 `fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c`

## Findings (ranked)

**F1 — The claim's `4/8` before-receipt is reproduced exactly, but only because L4 carries a second
citation.** The item's L4 (a brace whose *first* alternative is a dangling symlink and whose second
is live) **cannot fail the frozen baseline**: `brace_expand` already tests `os.path.exists` per
expansion, so it skips the dangling candidate and lands on the live one. Measured: with L4 as a
single citation the baseline scores **5/8** (`L1`, `L2`, `L3` fail; `L4` passes) — reproducible by
deleting L4's `extra_cites` block from the delivered fixtures and re-running; that intermediate
matrix is `7a1090c4…`, and its baseline receipt is preserved at `/tmp/r24-baseline-receipt.json`.
To keep the item's
L4 shape *and* the frozen claim's 4/8, case L4 keeps `brace/{alpha,beta}.md` as its **primary**
citation and adds one **second** citation for the same empty-alternative defect on the
bounty/mirror-fallback branch (`~/Projects/bounties/{ops,}/rank.mjs`, only the mirror-side empty
alternative `relocated/tbh/rank.mjs` is live). Baseline: primary PASS, second `GONE` → case FAIL →
**4/8**. After the fix: both PASS → **8/8**. The case fails before and passes after for a real
reason, and the L4 primary remains the regression guard against a fix that returns the first
brace expansion regardless of existence (F3).

**F2 — The matrix is satisfiable, and the lane's already-patched resolver satisfies it.**
Scratch reference bytes (two hunks, `/tmp/r24-ref/resolve.py`, sha256 `1bb89770…c31e41`) → **8/8
exit 0**; the lane's current patched bytes (`corpus/instruments/resolve.py`, sha256
`035f8844…9521b661`, authored by another seat, not by me) → **8/8 exit 0**. The reference bytes also
keep the round-23 containment matrix at **24/24 exit 0**.

**F3 — The controls and the L4 guard are load-bearing, measured against the same frozen matrix.**

| probe (scratch bytes) | score | what fails |
|---|---|---|
| always-`GONE` classify (`c0ab46c7…`) | **1/8** | everything except C2 |
| always-`RESOLVES` naming `lane/SKILL.md` (`89f0a8d7…`) | **0/8** | class+path on every case; C2 `gone-with-path`, C4 `path-outside-mirror-equivalent` |
| "first brace candidate wins regardless of existence" (`1463315b…`) | **5/8** | L1-hardening, L4, C4 — all `path-missing-on-disk` |
| "last glob match that exists wins" (`92675505…`) | **7/8** | C3 (`path-not-lane-multi-a.md`) — ordering not deterministic |
| frozen baseline (`690153ad…`) | **4/8** | L1, L2, L3, L4 |

**F4 — Collision: the lane working tree already holds a different counter-B instrument under the
same two filenames** (not written by me): checker `88090efc…2b47b69` (4 568 B), fixtures
`5133e98e…f9628b6` (4 143 B), plus a patched `resolve.py` `035f8844…9521b661`. That pair also scores
4/8 → 8/8, but it is weaker in two measured ways:
- its two-live-glob control asserts class and root only, so a resolver that returns the **last**
  live match still scores **8/8** (probe `92675505…`); mine pins the first sorted file and scores
  7/8 on the same probe.
- it has no dangling-first-alternative brace assertion; the naive-brace probe scores **6/8** on it
  versus **5/8** on mine, and the L4 primary that catches it does not exist there.
L1 must integrate exactly one pair; copying mine over the lane pair flips the counter-B before
receipt from 4/8 to 4/8 only because of F1's reconciliation — both reproduce the claim, mine adds
the two guards above. Do not leave both files or mix their fixtures with the other checker (the lane
checker loads its own schema and my checker rejects any matrix that is not 8 unique cases split
4 liveness / 4 control).

## The frozen matrix (8 cases, 10 assertions)

Case roots: `home` (isolated HOME), `relocated/tbh` (`KASEGI_MIRROR`), `lane` (CLI root argument).
"extra" rows are additional citations inside the same case; a case passes only if every assertion
passes.

| id | nature | citation | expected class | expected file | baseline |
|----|--------|----------|----------------|---------------|----------|
| L1 | liveness | `dir/{,sub}/file.md` | INTERNAL | `lane/dir/file.md` | **GONE** FAIL |
| L1 extra | liveness | `ops/{,registry-check}.mjs` | INTERNAL | `lane/ops/registry-check.mjs` | INTERNAL PASS |
| L2 | liveness | `dir/{sub,}/file2.md` | INTERNAL | `lane/dir/file2.md` | **GONE** FAIL |
| L3 | liveness | `glob/<n>.md` (`a-dangling.md` → missing; `b-live.md` live) | INTERNAL | `lane/glob/b-live.md` | INTERNAL, **path-missing-on-disk** FAIL |
| L4 | liveness | `brace/{alpha,beta}.md` (`alpha.md` dangling, `beta.md` live) | INTERNAL | `lane/brace/beta.md` | INTERNAL PASS |
| L4 extra | liveness | `~/Projects/bounties/{ops,}/rank.mjs` (only mirror `rank.mjs` live) | MIRROR-EQUIVALENT | `relocated/tbh/rank.mjs` | **GONE** FAIL |
| C1 | control | `docs/exists.md` | INTERNAL | `lane/docs/exists.md` | INTERNAL PASS |
| C2 | control | `docs/absent.md` | GONE | *(empty)* | GONE PASS |
| C3 | control | `multi/*.md` (`a.md`, `b.md` live) | INTERNAL | `lane/multi/a.md` (first sorted) | INTERNAL PASS |
| C4 | control | `~/Projects/bounties/ops/{import-board,finalize-all}.mjs` (bounty literal absent, mirror has `import-board.mjs`) | MIRROR-EQUIVALENT | `relocated/tbh/ops/import-board.mjs` | MIRROR-EQUIVALENT PASS |
| C4 extra | control | `~/Projects/bounties/ops/{validate,registry-check,reroute-drill,check-freshness}.mjs` (SKILL.md:1000 verbatim; mirror has `check-freshness.mjs`) | MIRROR-EQUIVALENT | `relocated/tbh/ops/check-freshness.mjs` | MIRROR-EQUIVALENT PASS |

Why each class, from the CLI's own documented policy (`resolve.py` docstring, "Existence test for a
candidate path"): a relative token that exists under the lane root is `INTERNAL`; a bounty-root
token whose literal is absent but whose suffix exists under the selected mirror (realpath-confined)
is `MIRROR-EQUIVALENT`; a relative token with no expansion on disk is `GONE`. L1/L2 must reach
`dir/file.md` and `dir/file2.md` through the **empty** alternative (`dir//file.md` — `realpath`
normalises it); L3 must land on the first *existing* sorted glob match; L4 must keep skipping the
dangling candidate for the primary citation and must credit the mirror-side empty alternative for
its extra citation; C3 must land on `a.md`, not on the other live match.

L1's extra citation is the hardening the item asks for: the real-world `prefix/{,name}.ext` shape
must keep resolving after the empty-alternative fix (the naive-brace probe fails it). C4's extra
citation is SKILL.md:1000 verbatim (`~/Projects/bounties/ops/{validate,registry-check,reroute-drill,check-freshness}.mjs`),
so the fix is pinned against the line that motivated it, not only a two-way toy.

## Why the controls cannot be satisfied by a resolver that answers GONE for everything

Measured: always-GONE scores **1/8**; the only passing case is C2.

| control | expected | always-GONE result | why |
|---|---|---|---|
| C1 | INTERNAL | FAIL (`GONE`) | a literal file on disk must be credited |
| C2 | GONE | **PASS** | this is the *negative* control: the one case always-GONE satisfies. Its job is the opposite degenerate — always-RESOLVES, measured **0/8**, which fails C2 with `gone-with-path` and also fails C1/C3/C4 on class and path |
| C3 | INTERNAL, first sorted of two live matches | FAIL | GONE cannot name a path; and an "any existing match" resolver is caught by the exact-file assertion (`path-not-lane-multi-a.md`) |
| C4 | MIRROR-EQUIVALENT, confined mirror path | FAIL | the real SKILL.md brace idiom under the bounty root requires brace + mirror dispatch to produce an existing, realpath-confined path |

Together: always-GONE = 1/8, always-RESOLVES = 0/8, class-only dispatch without an existence check
= 5/8 (naive-brace), non-deterministic match choice = 7/8 (last-live-glob). No degenerate policy
passes the matrix.

## Verification method (what the checker actually does)

- Copies the selected `resolve.py` **bytes** into a fresh temp case root (`tool/resolve.py`), runs
  `python3 tool/resolve.py <lane>` with `HOME=<case>/home`, `KASEGI_MIRROR=<case>/relocated/tbh`,
  `cwd=tool`, `start_new_session=True`, 120 s limit, `SIGKILL` on the process group on timeout;
  bounded capture (`MAX_STDOUT_STORED=400`, `MAX_TSV_BYTES=8 MiB`); temp root removed per case.
- Reads the CLI's **own** `tool/citation-survival.tsv` and asserts per citation: the `class` column
  equals the expected class; `resolved_path` is empty exactly when the class is `GONE`; otherwise
  the path exists on disk, is realpath-confined to the root the class implies (lane / mirror / case
  root), and — where the case names one — equals the exact expected file. A class that looks right
  with a path that is not on disk does not pass (this is what catches L3 and the naive-brace probe).
- Fixture containment before any disk write: absolute names, `..` segments, parents resolving
  outside the case root, and symlink targets escaping the root are rejected. Exercised:

```
safe_path ../escape.md          REJECT unsafe-file:'../escape.md'
safe_path /abs/path.md          REJECT unsafe-file:'/abs/path.md'
safe_path ok/fine.md            -> <CASE>/ok/fine.md
link_target @ROOT@/../outside   REJECT escape-t:'@ROOT@/../outside'
link_target /etc/passwd         REJECT escape-t:'/etc/passwd'
```

- Matrix validation: rejects anything but 8 unique cases split exactly 4 liveness / 4 control
  (`fixtures UNAVAILABLE reason=…`, exit 2), so the frozen matrix cannot silently drift.
- Exit codes: `0` all cases pass, `1` any failure, `2` fixtures/resolver unavailable. Last line is
  `cases=8 pass=K exit=0|1` plus a `sha256 resolver=… matrix=… checker=…` bind; `--json` writes the
  same values plus per-assertion records.

## Receipts (verbatim)

Fail-before, frozen baseline bytes, exactly the item's command:

```
$ python3 corpus/instruments/resolve-dispatch-check.py \
    --resolver /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/c1-baseline-resolver.py
L1   liveness expect=INTERNAL         actual=GONE             FAIL path_check=missing-path
     also expect=INTERNAL         actual=INTERNAL         PASS
L2   liveness expect=INTERNAL         actual=GONE             FAIL path_check=missing-path
L3   liveness expect=INTERNAL         actual=INTERNAL         FAIL path_check=path-missing-on-disk
L4   liveness expect=INTERNAL         actual=INTERNAL         FAIL
     also expect=MIRROR-EQUIVALENT actual=GONE             FAIL path_check=missing-path
C1   control  expect=INTERNAL         actual=INTERNAL         PASS
C2   control  expect=GONE             actual=GONE             PASS
C3   control  expect=INTERNAL         actual=INTERNAL         PASS
C4   control  expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
     also expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
cases=8 pass=4 exit=1
sha256 resolver=690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d matrix=fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c checker=acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1
EXIT=1
```

The frozen baseline copy is byte-identical to the lane's base `resolve.py`
(`diff` exit 0, sha256 `690153ad…7ff3ea2d`).

Pass-after on the lane's **current** patched bytes (another seat's patch; read-only use):

```
$ python3 corpus/instruments/resolve-dispatch-check.py \
    --resolver /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py
L1   liveness expect=INTERNAL         actual=INTERNAL         PASS
     also expect=INTERNAL         actual=INTERNAL         PASS
L2   liveness expect=INTERNAL         actual=INTERNAL         PASS
L3   liveness expect=INTERNAL         actual=INTERNAL         PASS
L4   liveness expect=INTERNAL         actual=INTERNAL         PASS
     also expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
C1   control  expect=INTERNAL         actual=INTERNAL         PASS
C2   control  expect=GONE             actual=GONE             PASS
C3   control  expect=INTERNAL         actual=INTERNAL         PASS
C4   control  expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
     also expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
cases=8 pass=8 exit=0
sha256 resolver=035f8844e66357f6dbe6f1158776978f2ce1103108e222d0746afdef9521b661 matrix=fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c checker=acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1
EXIT=0
```

Same result with the scratch reference bytes (`/tmp/r24-ref/resolve.py`, sha256 `1bb89770…c31e41`):
`cases=8 pass=8 exit=0`. Round-23 containment matrix on those bytes:

```
$ python3 mirror-containment-check.py --resolver /tmp/r24-ref/resolve.py
cases=24 escape=12 controls=12 pass=24 fail=0
resolver_sha256=1bb8977009f63de703ba3384fd7976bb2e093c3b27c50af65e9b123c40c31e41
matrix_sha256=d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809
EXIT=0
```

Probe summary (same matrix, same checker):

```
always-GONE      1/8   only C2
always-RESOLVES  0/8   wrong class+path everywhere
naive-brace      5/8   L1-extra, L4, C4 (path-missing-on-disk)
last-live-glob   7/8   C3 (path-not-lane-multi-a.md)
baseline         4/8   L1, L2, L3, L4
lane patch       8/8
```

## Integration handoff (L1)

1. The lane already contains a **different** pair under the same filenames (F4). Pick one pair; do
   not merge checker A with fixtures B (schema and case ids differ).
2. To integrate mine: copy `corpus/instruments/resolve-dispatch-check.py` and
   `corpus/instruments/resolve-dispatch-fixtures.json` from `/tmp/kasegi-r24-LivenessMatrix` over the
   lane copies, keep `resolve.py` as landed by the patch seat, then run the claims.json counter_B
   command unchanged:
   `python3 corpus/instruments/resolve-dispatch-check.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json`
   → must print `cases=8 pass=8 exit=0`. Without `--resolver` the default is the sibling
   `resolve.py`, so no flags are needed for the round receipt.
3. If L1 prefers the lane's own instrument, it should still add two assertions it lacks: the exact
   first-sorted file for the two-live-glob control (otherwise last-match passes 8/8, F4) and a
   dangling-first-alternative brace citation (otherwise the naive-brace fix is not caught).
4. `corpus/instruments/README.md` does not index either file (out of this seat's assignment); index
   whichever pair lands.

## Risks and limits

- All non-lane probe bytes live in `/tmp` and are evidence, not deliverables; production
  `resolve.py` is untouched by this seat.
- The matrix measures dispatch on isolated fixture trees only. It does not claim how many real
  SKILL.md citations move — that is the `ScoutSKILLLiveness` / `QuarterResolve` evidence.
- L4's fail-before is driven by its second citation (mirror-side empty alternative), not by the
  dangling-brace primary; the primary is a regression guard. This is a deliberate reconciliation of
  the item's L4 wording with the claim's frozen 4/8, and is visible per-assertion in the receipt.
- Rough cost: 8 cases × 1 CLI run ≈ 40 s wall time on this host.

## Tooling

No installs or upgrades; no package-manager calls (PACMAN pause respected).
