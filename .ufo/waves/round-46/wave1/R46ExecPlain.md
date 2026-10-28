VERDICT: DRAFT-READY

Seat R46ExecPlain (executor), kasegi round 46. Draft only; nothing committed, no tracked file touched (`git status --porcelain` after the work lists only untracked `.ufo/waves/round-46/...` paths). Scratch `/fast/scratch/hyaku/kasegi-r46/R46ExecPlain` removed before yield. Tools installed: none.

## Built (drafts, `.ufo/waves/round-46/wave1/R46ExecPlain.draft/`)

| File | sha256 | What |
|---|---|---|
| `plain-measure.sh` | `2ae9e76fec3a6b077712f3821d7cbfc8cdd31e605f7c428233328b3343f841c3` | `plain-measure.sh <tree>` prints exactly six `name=value` lines (c1a, c1b, c2a, c2b, c2c, c2d). bash/grep/sed/ls/wc only: no python, no counter. c1b strips a leading `cd <path> &&` (same regex shape as `recheck-audit.py` `CD_RE`), runs the first `^recheck:` line per entry under `bash -c` with cwd = `<tree>`, timeout 120, output discarded, `PYTHONDONTWRITEBYTECODE=1`; counts non-zero exits that `bash -n` accepts. |
| `plain-controls.sh` | `d2ec743823e616a78b0499f9be1d0f49f4275d17ec12d480a946e516c1d26663` | Builds the control variants below as copies (pure tree never edited) and prints plain-measure beside `recheck-audit.py --root <variant>`. |

## 1. The plain lines on the frozen trees (re-run by me)

Command: `bash plain-measure.sh /fast/scratch/hyaku/kasegi-r46/L1/pure` (about 2.8 s) printed:

```
c1a=23
c1b=24
c2a=27
c2b=72
c2c=64
c2d=0
```

Same script on a `git archive 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` export (freeze tree) printed the identical six lines: `c1a=23 c1b=24 c2a=27 c2b=72 c2c=64 c2d=0`. These equal the claims' before-values (23 `test -d` lines, 24 gated, 27 F rows, 72 S rows, 64 entries, empty sweep). The claimed work is not done at freeze, and no plain line moves at freeze (the do-nothing base control).

## 2. c1b against recheck-audit.py

- `python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet` printed `executes=40 gated=24 broken=0 ...`, `lines=64 total=64 pass=64 fail-closed=24 ... exit=0`.
- `--root /fast/scratch/hyaku/kasegi-r46/L1/pure` printed the same `executes=40 gated=24 broken=0`. `--root <freeze export>` printed the same. So c1b = 24 = audit's gated at all three trees; no difference at the freeze tree.

What stripping the `cd` changes. Every committed recheck line opens `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ...` (63 of 64; the 64th is a `test ! -e` line, `recheck-audit.py` strict reading `cdroot_fail=63` at the pure root, `strict pass=1/64`). `recheck-audit.py` runs the line with the `cd` intact, so for any `--root` other than the live lane, every relative `corpus/...` path in the command is resolved in the live lane, not in the audited tree. The audit's `gated` figure is therefore a statement about the live lane whatever `--root` says. c1b runs the stripped line with cwd = the tree, so it measures the tree's own bytes. The 23 `test -d ~/Projects/...` gates are unaffected (they depend on HOME, not cwd), which is why both agree at the freeze tree. They diverge on any tree that is not the live lane:

- Control K11 (pure copy with `corpus/source-snapshots/round-24/manifest.json` deleted; seven source-recheck lines read it): plain `c1b=31`, audit on that root `executes=40 gated=24 broken=0` (unchanged; it ran the live lane's manifest). Audit blind to the damage, plain sees it.
- `r46-c1-gate.py` docstring line 37 states the same design ("Rechecks run with the leading `cd <path> &&` stripped and cwd = TREE"), so c1b is an independent re-derivation of the counter's gated set, not of audit's.

## 3. Do-nothing / marker-only controls (each re-run; pure copy + one edit)

Format: plain line values; audit = `recheck-audit.py --root <variant>`.

| Ctl | Edit | c1a | c1b | c2a | c2b | c2c | c2d | audit |
|---|---|---|---|---|---|---|---|---|
| K0 | none | 23 | 24 | 27 | 72 | 64 | 0 | e40 g24 b0 |
| K1 | `claim-package-contract.md` recheck := `true` | 22 | 23 | 27 | 72 | 64 | 0 | e41 g23 b0 |
| K2 | recheck := `test -s <own file>` | 22 | 23 | 27 | 72 | 64 | 0 | e41 g23 b0 |
| K3 | recheck := `false` (still gated, marker text gone) | 22 | 24 | 27 | 72 | 64 | 0 | e40 g24 b0 |
| K4 | recheck := `if then` (syntax error) | 22 | 23 | 27 | 72 | 64 | 0 | e40 g23 **b1** |
| K5 | recheck := `cd <lane> && true # test -d ~/Projects/bounties` | 23 | 23 | 27 | 72 | 64 | 0 | e41 g23 b0 |
| K12 | recheck := `true` in both claim-package-contract.md and claim-gates.md | **21** | **22** | 27 | 72 | 64 | 0 | e42 **g22** b0 |
| K6 | C2 marker-only: junk F28 row + junk S073 row + 2-line stub entry (no capture, no quotes) | 23 | 24 | **28** | **73** | **65** | 2 | e41 g24 b0 |
| K7 | junk `| F28 | marker |` row only | 23 | 24 | 28 | 72 | 64 | 0 | e40 g24 b0 |
| K8 | junk `| S073 | marker |` row only | 23 | 24 | 27 | 73 | 64 | 0 | e40 g24 b0 |
| K9 | one sentence "privately report" appended to an old entry | 23 | 24 | 27 | 72 | 64 | 1 | e40 g24 b0 |
| K10 | empty file `corpus/knowledge/zz-empty.md` | 23 | 24 | 27 | 72 | 65 | 0 | e40 g24 b0 |
| K11 | deleted a manifest an executing recheck reads | 23 | 31 | 27 | 72 | 64 | 0 | e40 g24 b0 |

Counter on K12 (`r46-c1-gate.py --root K12 --baseline pure`) printed `gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64`, `gate L2 pass=1 ... regrounded=2 claim-gates.md,claim-package-contract.md`, `gate L3 pass=0`, `gate L4 pass=0`, `gate L5 pass=0`, `gate L6 pass=0 read=mutants=0`, `gate L7 pass=1`, `c1-gate fixed=3/7 exit=1`. So the C1 plain targets (c1a<=21, c1b/gated<=22, the claims.json `plain` lines 18-19) are met by a two-line `true` softening, while the counter rejects it (3/7).

## 4. What a verifier may trust alone

- Not trustable alone (each moves with the claimed work NOT done): c1a (K1, K12: reaches 21), c1b (K1, K12: reaches 22), audit gated (same), c2a (K7), c2b (K8), c2c (K10: an empty file), c2d (K9: one sentence), and all four C2 lines together (K6: 28/73/65, sweep non-empty, with no capture or quote; note K6's README junk row did not match the sweep regex because it spelled the topic only as a hyphenated filename, so c2d read 2 not 3).
- Direction caveats: c1a can fall without c1b moving (K3, marker removed, still gated); c1b can fall while the line is merely unparseable (K4: c1b 23, but audit broken=1; c1b alone silently drops parse-broken lines, so c1b is only valid beside `lines == executes + gated + parse-broken` and parse-broken = 0); c1b can rise with no corpus change in the audited lane (K11).
- Trustable as a necessary-condition (null) check: all six lines at the base and freeze trees read 23/24/27/72/64/0, so a verifier can trust that "no movement" means "not done" (K0, freeze). A movement is never sufficient evidence of the claimed work. The content-bearing plain checks that do discriminate: (C2) `sha256sum corpus/source-snapshots/round-46/S073.txt` on the freeze tree printed `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930` (matches freeze.txt S073-sha256), `wc -c` 15568; the same command on the K6 stub printed `25cf54c697a69632c5952486ec189be371ddddc422bca30910f17b2c3a0ba31d`; `jq` on the manifest reports 8 quotes (`.quotes | length` printed `8`) to be located with `grep -F` in the capture; (C1) a per-entry check of every `## Re-ground (round 46)` row's anchor/token (not built here; the c1b number cannot stand in for it, K12).
- Recommendation for the L1: report c1b only paired with the parse-broken count, and name (c2a, c2b, c2c, c2d) as "necessary, not sufficient" next to the sha256 and quote-location lines above.

## Limitations

- c1b executes the recheck commands (the 24 gated ones exit at `test -d ~/Projects/bounties`; the one `git -C ~/Projects/bounties` line sits behind that test). On a host where the base is restored, the count changes by design; any recheck line that mutates a tree would be run against the tree given. Bytecode writing was disabled; I did not diff the lane for side effects beyond `git status --porcelain` (no tracked change).
- The plain-measure.sh c1b treats a command it cannot strip as run-as-is; the strip regex matches `recheck-audit.py` `CD_RE` only for `cd <path> &&` with a single path and no `;`.
- Controls were run on the pure base (and K12 count also via the freeze-archive-free pure copy); the final L1 tip with the real S073 and entry was not available to me, so no tip reading exists. `r46-c1-gate.py` L1 to L7 were run only on K12 (above) and the c2-gate only on the freeze tree (`c2-gate fixed=2/7 exit=1`).
- The labrat probe was not used.
