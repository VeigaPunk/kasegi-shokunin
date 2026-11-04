# RevengerMultiHead — round 67, wave 1: native multi-head SIGPIPE probe (C1)

Report: `.ufo/waves/round-67/w1/RevengerMultiHead.md`

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.
Seat: leaf revenger. **No production byte was edited.** The production gate was executed
unchanged, read-only, over scratch ledgers only (`--ledger`/`--root` under my scratch); its
sha256 was re-verified as
`51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` before and after.

## 0. Scope

C1 (`depth:verifiability`) only. I tested the **native premise** behind the intended repair:
a read-only head that streams dies of SIGPIPE (`-13`) before reaching a later named operand,
so a green `FIG` line can report success on a world where a named input was never read.
C2 (F45 PSIRT Maturity) is not touched by this seat.

## 1. Hypothesis (falsifiable)

H: *On this host, `cut|wc|grep|sort|head|tail|sha256sum|tr|ls` with two file operands, piped
into `head -n 1`, can die of `-13` before opening the second operand; whether that happens
depends on the size of the first operand; therefore "SIGPIPE with more than one input
operand ⇒ an input may have been skipped" is a sound refusal rule.*

The hypothesis is falsified if (a) a head's `-13` occurs only after the later operand was
read, or (b) a head can never reach `-13` with a later operand, or (c) the first-operand size
does not matter.

## 2. Method

* Fixtures: 1024-byte lines, deterministic. Line 1 = `alpha:` + `a`×1017 + `\n`; lines 2..k =
  `x`×1023 + `\n`. So `grep x` matches every line, `grep alpha` exactly one, `cut -f1 -d:`
  yields `alpha` then `x`×1023. `missing.txt` is **never created**. Sizes are exact
  multiples of 1024 (64 KiB = 65536 B … 4 MiB = 4194304 B).
* Every pipeline stage is an argv list started with `subprocess.Popen`; **no shell**, no
  string parsing. `subprocess` restores `SIGPIPE` to `SIG_DFL` in children (verified by the
  `cat` baseline reading `-13`, not `141`).
* Parent closes its copy of each pipe write end immediately, so the writer really gets EPIPE.
* Repeats: 7 (full table), 15 (size sweep), 20 (wc falsifier), 40 (4 MiB stability). A status
  seen in one repeat is never reported as stable.
* Positive proof that a later operand **was** opened: stage-0 stderr naming `missing.txt`
  (and, for the two decisive cases, `strace -f -e trace=openat`).
* Pipe capacity on this host: **65536 bytes** (`F_GETPIPE_SZ`).
* Host tools: `cut wc sort head tail sha256sum tr ls cat` = **uutils 0.8.0**;
  `grep` = **`grep (pi-uu-grep) 0.2.0`**; `python3` 3.14.8; Linux 7.2.11-arch1-1 x86_64.

Reproduction (all paths absolute; scratch was `/fast/scratch/hyaku/kasegi-r67/RevengerMultiHead`):

```
python3 -B probe.py    --work <S>/work --out <S>/probe.json --reps 7
python3 -B followup.py <S>/work <S>/followup.json
python3 -B stage3.py   <S>/work <S>/stage3.json      # + gate read-only observation
python3 -B emit_table.py > <S>/table.txt
```

Receipts (in `.ufo/waves/round-67/w1/RevengerMultiHead/`): `table.txt` (full human table),
`probe.json`, `followup.json`, `stage3.json`, `order.json`, the five `strace-*.log`, both
scratch ledgers, the four harness scripts, `MANIFEST.txt` (sha256 of each).

## 3. Fixture digests

| bytes | KiB | lines | sha256 |
|---|---|---|---|
| 65536 | 64 | 64 | `65f4ca4d510a66c0c7d84350edb94070bce7c5fba5f160f1cad8d4c57f583a50` |
| 66560 | 65 | 65 | `db83ab8539b6bb137c5432217ea7f24f8407629750c4f42d6fa24a0f061b4875` |
| 69632 | 68 | 68 | `36406efcab250699ec9da83c750ee90c014cd22b91ba2e7206dc1b0a30c1abfa` |
| 73728 | 72 | 72 | `fbd75bda73be5161bb8603c1305966d6dc04f932b753e4b66cc786798eebecd4` |
| 81920 | 80 | 80 | `672d6fd24c53c7743556631602622b6864462d3807b02b9413db4215393ac9b4` |
| 98304 | 96 | 96 | `c7fb1141711b291f04dc9eaa52035092e01b221e2f620318187b3cec5e7496ef` |
| 131072 | 128 | 128 | `23485911bebf3bc913c473b0757638cf0e327094996d3e8a68ac3827c8ba39e2` |
| 262144 | 256 | 256 | `2933a035fa36f362be8d9621614275bfe799ec9846466342c9e4cea47d283760` |
| 524288 | 512 | 512 | `6a9d0e2109d6130de9f81cddbcccb72a35475bd5417dcf78ce3719bb8791e27d` |
| 1048576 | 1024 | 1024 | `bf68d0f84c859e89d0d373293495b06988c0f324b602d2214cf10da7e50c31e7` |
| 2097152 | 2048 | 2048 | `addc8713cd0f5b4abc152e46b6ee22dbe2a94865c1a6d50571b4c3ccd2a47665` |
| 4194304 | 4096 | 4096 | `3116362bec339b7f6f0d63e28607647b354e834c073f20ec6b629f1bf61da2ee` |

Note: these are **my** fixtures; the round-67 no-work control's `big.txt`
(`3ed4e02b…`, 4193286 B, 4096 lines, first line `alpha`) is a different byte layout of the
same shape, and every status below matches the control's measured P9/P10/P11 lines.

## 4. Exact argv (stage lists)

| name | stage 0 | stage 1 |
|---|---|---|
| cat | `['cat', F, (M)]` | `['head','-n','1']` |
| cut | `['cut','-f1','-d:', F, (M)]` | `['head','-n','1']` |
| wc | `['wc','-l', F, (M)]` | `['head','-n','1']` |
| grep-many | `['grep','x', F, (M)]` | `['head','-n','1']` |
| grep-few | `['grep','alpha', F, (M)]` | `['head','-n','1']` |
| sort | `['sort', F, (M)]` | `['head','-n','1']` |
| head-n5 | `['head','-n','5', F, (M)]` | `['head','-n','1']` |
| head-all | `['head','-n','100000', F, (M)]` | `['head','-n','1']` |
| tail | `['tail', F, (M)]` | `['head','-n','1']` |
| tail-all | `['tail','-n','+1', F, (M)]` | `['head','-n','1']` |
| sha256sum | `['sha256sum', F, (M)]` | `['head','-n','1']` |
| ls | `['ls', F, (M)]` | `['head','-n','1']` |
| tr (file) | `['tr','a','b', F, (M)]` — tr accepts no file operand | `['head','-n','1']` |
| cat\|tr | `['cat', F, M]` \| `['tr','a','b']` | `['head','-n','1']` |

`F` = absolute fixture path, `M` = `<work>/missing.txt` (absent).

## 5. Results

### 5.1 The requested full table (64 KiB / 1 MiB / 4 MiB, 7 repeats)

`rc0` = stage-0 status (negative = signal). `miss` = stage-0 stderr named `missing.txt`
(positive proof the later operand **was** opened). Full per-repeat rows are in `probe.json`;
the authoritative stability column is 5.2.

| shape | 64 KiB rc0 | 1 MiB rc0 | 4 MiB rc0 | miss |
|---|---|---|---|---|
| cat | 0 | -13 | -13 | – |
| cat+missing | 1 | -13 | -13 | yes / no / no |
| cut | 0 | -13 | -13 | – |
| cut+missing | 1 | -13 | -13 | yes / no / no |
| wc | 0 | 0 | 0 | – |
| wc+missing | **{-13, 1}** | **{-13, 1}** | **{-13, 1}** | **always yes** |
| grep-many | {-13, 0} | -13 | -13 | – |
| grep-many+missing | {-13, 2} | -13 | -13 | no (flaky) / no / no |
| grep-few | 0 | 0 | 0 | – |
| grep-few+missing | 2 | 2 | 2 | yes |
| sort | 0 | -13 | -13 | – |
| sort+missing | 2 | 2 | 2 | yes |
| head-n5 | 0 | 0 | 0 | – |
| head-n5+missing | 1 | 1 | 1 | yes |
| head-all (`-n 100000`) | {-13, 1} | -13 | -13 | – |
| head-all+missing | {-13, 1} | -13 | -13 | flaky / no / no |
| tail | 0 | 0 | 0 | – |
| tail+missing | 1 | 1 | 1 | yes |
| tail-all (`-n +1`) | -13 | -13 | -13 | – |
| tail-all+missing | {-13, 1} | -13 | -13 | flaky / no / no |
| sha256sum | 0 | 0 | 0 | – |
| sha256sum+missing | 1 | 1 | 1 | yes |
| ls | 0 | 0 | 0 | – |
| ls+missing | 2 | 2 | 2 | yes |
| tr-one-arg / tr-file / tr-two-file | 1 | 1 | 1 | no (never opens anything) |
| cat\|tr | 1 | -13 | -13 | – |

### 5.2 4 MiB stability (40 repeats each; `stage3.json`)

| shape | stage-0 status | SIGPIPE rate |
|---|---|---|
| cat+missing | -13 | 40/40 |
| cut+missing | -13 | 40/40 |
| grep-many+missing | -13 | 40/40 |
| wc+missing | -13 | 40/40 in this pass (see 6.1: race) |
| head-all+missing | -13 | 40/40 |
| tail-all+missing | -13 | 40/40 |
| grep-few+missing | 2 | 0/40 |
| sort+missing | 2 | 0/40 |
| head-n5+missing | 1 | 0/40 |
| tail+missing | 1 | 0/40 |
| sha256sum+missing | 1 | 0/40 |
| ls+missing | 2 | 0/40 |

### 5.3 First-operand size sweep (2-operand shapes)

| head | first size with any `-13` | first size with `-13` in every repeat | note |
|---|---|---|---|
| cat | 513 KiB (525312 B): 35/40 | 524 KiB (536576 B): 40/40 | 512 KiB = **0/40**, rc 1 |
| cut | 65 KiB (66560 B): 37/40 | 69 KiB (70656 B): 40/40 | 64 KiB = 0/40, rc 1; 66/67/68 KiB = 4/40, 6/40, 7/40 reach the operand |
| grep-many | 64 KiB (65536 B): 38/40 | 69 KiB (70656 B): 40/40 | 65/67/68 KiB = 2/40, 1/40, 2/40 reach the operand; 66/69/70/72 KiB 40/40 in that pass (not monotone) |
| head-all | 64 KiB: flaky | 68 KiB (69632 B): 40/40 | 64–67 KiB flaky |
| tail-all | 64 KiB: flaky | 65 KiB (66560 B): 40/40 | |
| wc | no threshold | never stable | race at every size (6.1) |

Pipe capacity is 65536 B, but that is **not** the boundary: `cut`/`grep`/`head`/`tail` cross it
almost immediately while `cat` needs **>512 KiB** of first operand before its second write can
hit EPIPE. Near each threshold the status is **nondeterministic** (measured counts above), so
no single repeat can freeze a reason there.

### 5.4 Production gate, unchanged, read-only (`stage3.json`, `revenger-ledger.json`)

Each ledger entry recorded exactly what its shape prints, so `derived == recorded` whenever
the derive runs; the only possible reason for `stale` is the status rule.

| figure (4 MiB) | base verdict |
|---|---|
| `cut -f1 -d: F M \| head -n 1` | **ok (green)** |
| `grep x F M \| head -n 1` | **ok (green)** |
| `wc -l F M \| head -n 1` | **ok (green)** |
| `head -n 100000 F M \| head -n 1` | **ok (green)** |
| `tail -n +1 F M \| head -n 1` | **ok (green)** |
| `cat F M \| head -n 1` | stale (R66 rule already refuses 2 operands) |
| `sort F M \| head -n 1` | stale (`derive-upstream-exit-2`) |
| `sha256sum F M \| head -n 1` | stale (`derive-upstream-exit-1`) |
| `ls F M \| head -n 1` | stale (`derive-upstream-exit-2`) |
| `tr a b F \| head -n 1` | stale (`derive-upstream-exit-1`) |
| `head -n 5 F M \| head -n 1` | stale (`derive-upstream-exit-1`) |
| 1-operand controls (`cut`, `wc`, `grep-many`, `cat`, `sort`, `tail -n +1`) | all ok |

`FIGURE-AUDIT figures=17 ok=11 stale=6 exit=1`. So base masking is **not** limited to
`cut`/`wc`/`grep`: `head -n 100000 …` and `tail -n +1 …` are green on a world whose second
operand was never opened, and all five are expressible in the gate's own allow-list
(`READ_ONLY_HEADS` has no denied flags for `head`/`tail`).

Reversed operand order (missing first, 4 MiB second; `order.json` + `revorder-ledger.json`):
`cut`, `grep`, `head-all`, `tail-all`, `cat` all give stage-0 `-13` **with** `missing.txt`
already reported on stderr; base gate is **green** for `cut`/`grep`/`head-all`/`tail-all`
(stale only for 2-operand `cat`). `wc` gives `-13` or `1` (race), green either way.

### 5.5 openat evidence (`strace -f -e trace=openat`)

```
cut+missing@4MiB   rc=[-13,0]  openat(f-4194304.txt)=3  openat(missing.txt)=<absent>  SIGPIPE
wc +missing@4MiB   rc=[-13,0]  openat(f-4194304.txt)=3  openat(missing.txt)=-1 ENOENT  SIGPIPE
head-all@4MiB      rc=[-13,0]  openat(f-4194304.txt)=3  openat(missing.txt)=<absent>  SIGPIPE
tail-all@4MiB      rc=[-13,0]  openat(f-4194304.txt)=3  openat(missing.txt)=<absent>  SIGPIPE
cut+missing@64KiB  rc=[-13,0]  openat(f-65536.txt)=3    openat(missing.txt)=<absent>  SIGPIPE
```

`head-all` and `tail-all` traces were repeated 3× each, identical every time. Caveat: `strace`
slows the child enough to change the outcome at 64 KiB (native, untraced,
`cut+missing@64KiB` is rc 1 in 40/40). The 64 KiB trace is therefore evidence of **timing
sensitivity**, not of native behaviour; the 4 MiB traces agree with the untraced result.

## 6. Answers to the four questions

**6.1 Which read-only heads can be SIGPIPE'd before reaching a later named operand?**
`cut`, `grep` (many matches), `tail -n +1`, `head -n <large>`, and `cat` (already handled by
R66). `tr` cannot be given a file operand at all (`tr a b F` → exit 1 `extra operand`), so the
"later named operand" concept does not apply to it; its SIGPIPE is stdin-only.
**`wc` is the exception that contradicts the wording of the claim**: it *does* reach the later
operand — at every size its stderr names `missing.txt` and the strace shows
`openat(missing.txt) = -1 ENOENT` — and then dies of `-13` on a later write of its own summary
lines. Its status is a race between its per-file write and the reader's exit: `probe.json` and
`followup.json` recorded both `-13` and `1` at every size, `stage3.json` recorded `-13` 40/40
in one pass, and L1's addendum measured the same instability. The mask is still real (base is
green while `wc` exited 1), but the cause is "the stage's own exit status and stderr are lost",
not "the operand was never read".

**6.2 Does the required first-operand size matter?**
Yes, decisively, and the boundary is **head-specific**, not the 64 KiB pipe capacity:
`cut`/`grep`/`head`/`tail` mask from ≈65–70 KiB, `cat` only above ≈512 KiB. At 64 KiB exactly,
`cut` never masks (0/40, rc 1) while `grep` mostly does (38/40). Near each threshold the
status flips run to run, so a fixture at 64 KiB cannot freeze a verdict; at 4 MiB
`cat`/`cut`/`grep`/`head-all`/`tail-all` are stable 40/40 (wc stays a race, 6.1).

**6.3 Does any head never SIGPIPE, so the rule can never fire for it?**
In the two-operand shape: `sort` (reads every input before writing → exit 2), `sha256sum`
(exit 1), `ls` (exit 2), `head -n 5` (exit 1), default `tail` (exit 1), `grep` with few matches
(exit 2), and `tr` (no file operands; exit 1). For these the rule is a no-op — they never
produce `-13` there, and their non-zero exit already makes the gate stale.
Two qualifications matter for the repair:
* `sort` **can** SIGPIPE in other shapes (1 operand, or 2 *existing* operands), but it never
  masks an unread operand; the rule would flag those worlds stale anyway (see 6.4).
* `head`/`tail` only mask with an option value that streams the whole file (`-n 100000`,
  `-n +1`). Default `head -n 5` / `tail` never SIGPIPE. A rule that counts **file operands**
  still catches them (2 operands > 1); a rule that keyed only on the head name would refuse
  harmless shapes and is unnecessary — but is not unsound.

**6.4 Does the rule's premise hold on this host?**
* "SIGPIPE on a >1-input stage ⇒ a named input may have been skipped" — **sound as a refusal**
  and confirmed by the gate: green at base for `cut`, `grep`, `wc`, `head-all`, `tail-all` in
  both operand orders, with `missing.txt` absent from stderr (or, for `wc` and the reversed
  order, present but the exit status lost).
* "…because the later operand was never read" — **false as stated**, twice: (a) `wc` at every
  size reads it and reports it before `-13`; (b) in reversed order `cut`/`grep`/`head`/`tail`/
  `cat` report the missing operand on stderr and *then* die of `-13`. The correct statement is
  "a `-13` on a multi-input stage destroys the stage's own exit status and its stderr-based
  error is invisible to the gate".
* The rule is **conservative, not exact**: with both operands present and fully read,
  `cat F G`, `cut F G`, `grep x F G`, `sort F G`, `tail -n +1 F G` all give `-13`
  (7/7 stable at 1 MiB and 4 MiB) → the rule marks those green worlds stale. For `cat` this is
  already R66's accepted cost; for `sort` it is a pure false positive (sort cannot mask).

## 7. Contradictions with the claim, stated plainly

1. **`wc`** contradicts "the stage dies of SIGPIPE *before* reaching a later named operand":
   it reaches it (strace `openat` ENOENT), reports it, and only then dies of `-13`.
   Consequence: do not justify the `wc` repair as "unread operand"; justify it as lost exit
   status. Do not freeze `wc`'s reason either way (race).
2. **Reversed operand order** contradicts the same clause for `cut`/`grep`/`head-all`/
   `tail-all`/`cat`: `-13` arrives *after* the missing operand was reported. The rule still
   refuses those worlds correctly (status-based), so only the wording needs correcting.
3. **`sort`** never masks but the rule fires on it (2 existing operands) → accepted false
   staleness, worth naming in the reason text.
4. **`tr`** has no file operands; any operand-count rule must not treat its `SET1 SET2` as
   inputs, or `tr a b` (stdin filter) would be mis-scored.

## 8. Residuals (measured, not assumed)

* **git** (unknown head, old benign rule): `git -C D ls-files` (20 000 index entries,
  220 000 B) `| head -n 1` → stage-0 `-13`, 5/5. So the benign residual is a **live** hole
  class, not vacuous: a SIGPIPE'd git head is exempt at base. Fixture repo created with
  `D=$(mktemp -d) && git -C "$D" init -q`, toplevel asserted equal to `$D` before use, then
  removed.
* **python** (unknown head): a 200 000-line `sys.stdout.write` flood `| head -n 1` → stage-0
  `1` (`BrokenPipeError` traceback), never `-13`. For python the benign rule is sound.
* Not measured: any head outside the dispatch list; other hosts; whether a `-13` can arise
  from a *first* operand that is itself a pipe.

## 9. Confidence

* Full table at 4 MiB: **high** (40/40 stable, two independent passes, matches the round-67
  no-work control's P9/P10/P11 statuses).
* Threshold values: **medium** — the counts are exact for the repetitions run, but the
  boundary is a race; treat "≈65–70 KiB for cut/grep/head/tail, >512 KiB for cat" as the
  claim, not a single byte.
* Gate verdicts: **high** for these 17 scratch figures (production executed unchanged,
  read-only, sha256 re-verified). They are a secondary observation; `ExecMultiHeadGate` owns
  the gate evidence.
* Not claimed: shell correctness, sandbox or semantic-emulator resistance, behaviour on other
  hosts or other coreutils builds.

## 10. Handoff to the integrator (L1)

* The C1 masking is real and wider than `cut`/`wc`/`grep`: add `head -n 100000 …` and
  `tail -n +1 …` shapes to the frozen repair set (both are allow-listed and both read green at
  base). `cat` stays on the R66 path.
* Keep the rule **status-based** (any `-13` on a stage with >1 decoded file operand is stale)
  and phrase the reason as lost exit status / hidden stderr, not "operand never read".
* `wc` must be refused under **both** observed statuses (`-13` and `1`) — it already is, since
  `1` is `derive-upstream-exit-1`.
* Count **file operands**, not raw tokens, for `cut` (`-f1 -d:` options) and `tr` (no file
  operands); `grep`'s pattern is the single non-file operand.
* Do not key the rule on the head name alone: `head`/`tail` only mask with a streaming `-n`.
* Fixtures at 64 KiB cannot freeze a reason for `cut`/`grep`/`head`/`tail`; the 4 MiB fixture
  is stable. If a selftest case is added at 64 KiB, assert only the refusal, never the reason.
* Residual to name: `git` heads can die of `-13` and remain exempt; `python` cannot
  (`BrokenPipeError` → exit 1).
