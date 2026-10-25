# QuarterSpotcheck — rulings on round-23 spot-check defects 3 and 4

Seat: read-only. No production file, lane byte, git/jj state, fleet byte or sibling lane was modified.
Every counter below was executed or read from committed bytes in this session; nothing restates a
claim I did not run. Scratch receipts I wrote: `/tmp/r24qs_{s030,s031}.txt`,
`/tmp/r24qs_recheck_{S018,S029,S031}.txt` (read-only-seat rule otherwise honoured; the lane tree
received nothing).

Inputs read: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json`
(frozen), `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-23-verifier-spotcheck.md`,
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md:46-52` (R7/R8/R9),
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md:394-458`,
`/home/vgpnk/Projects/shokunin/.ufo/prompts/kasegi-round-23.md`,
`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`.

Lane endpoints used: base `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`, live tip
`c2480b143120364728b40397926ffcf30a7309c8` (= `d0a3f6a4` + the spot-check file only:
`git diff --stat d0a3f6a4 c2480b1` → `corpus/lessons/round-23-verifier-spotcheck.md | 142 +`).

---

## Verdicts

| Defect | Ruling | Mechanism |
|---|---|---|
| **3 — attempt numbering** ("attempt 2" in the r23 report/SCORECARD/lesson vs driver `attempt=1`) | **Fix this round, append-only.** The label is false against the host's committed dispatch evidence, so it must be reconciled — but the label text itself may not be rewritten (R9). One appended M-row declares the counter and the contradiction. | R9 (append erratum, never rewrite a filed assertion) + R7 (a label is not an axis move; no credit) |
| **4 — SCORECARD r23 C1 cell shows the first landing (6/6, 13/13) with errata appended** | **Fix this round, append-only — and it is *not* cosmetic.** The cell's numbers are true, but the errata block never names the revision that still holds them, and the receipt paths the cell cites were overwritten in place. One appended errata bullet supplies the base (`953c278`), the changed-file scope (`bf9ce02`) and the re-derivation command. Cell text stays untouched. | R9 (“names its base and changed-file scope”) |
| **Third question — any r23 claim left unverified by the spot-check?** | **No declared claim is left unverified.** Two claim-parts were verified by the spot-check only at receipt level; I closed both by execution. Four things remain UNVERIFIED and are named in §D. | PROTOCOL §Gate standard (evidence-verified is allowed; execution is stronger) |

Neither defect 3 nor defect 4 appears in `claims.json.routed_defects` (which lists spot-check defects
1 and 2 only). They are therefore **record hygiene, not claim surfaces**: landing them earns no
`depth:verifiability` credit and must not be folded into C1's counter A/B narrative.

---

## A. Defect 3 — attempt numbering

### What the host actually recorded

```
$ grep -n "kasegi round=23" /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
519:2026-10-20T18:30:58-03:00 launch kasegi round=23 pgid=1137022 driver=hyaku-inline attempt=1
1090:2026-10-23T20:41:47-03:00 launch kasegi round=23 pgid=3508145 driver=hyaku-inline attempt=1
1259:2026-10-25T03:23:48-03:00 launch kasegi round=23 pgid=1759483 driver=hyaku-inline attempt=1
1268:2026-10-25T03:57:08-03:00 complete kasegi round=23; hyaku-inline attempt=1
```

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h %ci %s' -3 -- .ufo/prompts/kasegi-round-23.md
04411e88 2026-10-25 03:23:46 -0300 round-23: kasegi dispatch evidence (hyaku inline attempt 1)
c6a48745 2026-10-23 20:41:45 -0300 round-23: kasegi dispatch evidence (hyaku inline attempt 1)
848f4d3d 2026-10-20 18:30:56 -0300 round-23: kasegi dispatch evidence (hyaku inline attempt 1)
```

`/home/vgpnk/Projects/shokunin/.ufo/prompts/kasegi-round-23.md:161` — the rendered prompt the lane
was handed, committed as dispatch evidence — reads:

```
parent omp session) for exactly ONE steered round: **kasegi round 23** (attempt 1;
```

So the number the lane was given is 1, and three separate fleet commits attest it. The label the lane
filed is 2: `SCORECARD.md:394` (`## Round 23 — result (attempt 2, 2026-10-25)`),
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/kasegi.md:1`
(`# kasegi — round 23 report (attempt 2)`), `corpus/lessons/round-23.md:71`
(`## Attempt 2 — 2026-10-25: ...`).

### The only reading under which "2" is true

Landings that produced committed **round-23** bytes:

- `8bf9807` (2026-10-20 19:33:51, `checkpoint(r23): … policy-paused, unadmitted, no task resumption`) → 1
- `953c278` … `d0a3f6a4` (2026-10-25 03:35–03:56) → 2

The 2026-10-23T20:41 launch landed **no** round-23 commit: the only lane commit between that launch
and the next is `7916542 considerthese: 2026-10-24 daily reflection` (adds
`considerthese/2026-10-24.md` only, scheduled daily reflection, not round work — `git show --stat
7916542`). Three launches, two landing attempts. That is a defensible convention, but it is
**unstated**, and a non-author reading `attempt 2` against the prompt's `(attempt 1;` will re-file
this defect every round.

### Exact minimal edit (one row, appended; no filed text changes)

Append to the Mistakes table of `corpus/lessons/round-24.md` (this round's lesson — the row is the
receipt that the routed defect was adjudicated). If L1 prefers the correction beside the label
instead, the same text goes as one errata bullet at the end of `corpus/lessons/round-23.md` §
“Attempt 2 — 2026-10-25”. One location only.

```
| M? | Round-attempt label disagrees with the host's attempt record | Labels: `SCORECARD.md:394`, `.ufo/reports/round-23/kasegi.md:1`, `corpus/lessons/round-23.md:71` all say "attempt 2". Host record: `.ufo/prompts/kasegi-round-23.md:161` "(attempt 1;" and three dispatch commits `848f4d3d`/`c6a48745`/`04411e88`, each titled "round-23: kasegi dispatch evidence (hyaku inline attempt 1)"; `.ufo/watchdog.log:519,1090,1259` launch `attempt=1`, `:1268` complete `attempt=1` | R9; R7 | Convention declared: this lane's prose "attempt N" counts the Nth round landing that produced committed round bytes (`8bf9807` = 1, `953c278`…`d0a3f6a4` = 2); the 2026-10-23 launch landed no round-23 commit. The driver's `attempt=` and the rendered prompt's `(attempt N;` are the host's retry counter and are authoritative for dispatch. Historical label text is not rewritten (R9); future labels state which counter they use. |
```

Do **not** edit `SCORECARD.md:394`, the r23 report title, or `corpus/lessons/round-23.md:71` — R9
forbids rewriting filed assertions, and those strings are the evidence this row cites.

### Closing sentence if L1 defers the row (not recommended)

> Round-23's “attempt 2” is a lane-minted landing count (`8bf9807` → `d0a3f6a4`), not the driver's
> field: `.ufo/prompts/kasegi-round-23.md:161` and all three dispatch commits (`848f4d3d`,
> `c6a48745`, `04411e88`) say `attempt 1`; the convention is stated in
> `corpus/lessons/round-24.md` M-nn and the historical labels are not rewritten (R9).

---

## B. Defect 4 — the SCORECARD r23 C1 cell

### The cell's numbers are true; only their address is lost

```
$ git show 953c278:.ufo/waves/round-23/c1-fixed.json | python3 -c "..."
matrix 5e61a33e resolver ed9a9dae cases 13 pass 13 escape_GONE 6       # 6/6, 7/7 controls, 13/13
$ git show 953c278:.ufo/waves/round-23/c1-baseline.json | python3 -c "..."
matrix 5e61a33e resolver d6a3c3f1 cases 13 pass 7  escape_GONE 0       # 0/6 GONE, 7/13, exit 1
```

That is exactly `SCORECARD.md:403`: before **0/6 GONE, matrix 7/13**; after **6/6 escape GONE, 7/7
controls preserved, matrix 13/13, exit 0**; both runs on `matrix_sha256=5e61a33e…b5e76a9`. No
numerical correction is due.

The defect that *is* due is R9's “names its base and changed-file scope”:

```
$ git show d0a3f6a4:.ufo/waves/round-23/c1-fixed.json  → matrix d05b1e0c, resolver 690153ad, cases 24, pass 24
$ for c in 2712c99 12edac4 bf9ce02 d0a3f6a; do ... ; done
2712c99 matrix 4e39f65c cases 20 pass 20
12edac4 matrix 332a5fe9 cases 23 pass 23
bf9ce02 matrix d05b1e0c cases 24 pass 24      ← the receipt paths were overwritten here
```

The cell names `.ufo/waves/round-23/c1-baseline.json` and `c1-fixed.json` as its reproduction path.
Those two paths now hold the 24-case runs. A reader executing the cell's own command today gets
`d05b1e0c`, not `5e61a33e` — the cell is reachable only through `git show 953c278:<path>`, a revision
neither the cell (correctly frozen) nor the errata block names. That is why the routed word
“cosmetic” understates it: it is a one-line address gap, not a formatting quibble.

### Second finding folded into the same bullet: one recheck receipt is a duplicate

```
$ diff <(git show d0a3f6a4:.ufo/waves/round-23/c2-recheck-S030.txt) \
       <(git show d0a3f6a4:.ufo/waves/round-23/c2-recheck-S031.txt) && echo IDENTICAL
IDENTICAL
```

`c2-recheck-S030.txt` is byte-identical to `c2-recheck-S031.txt` — same header
(`--source S031`), same `EXIT=0`. So the errata bullet “Receipts: four rechecks exit 0” counts one
duplicate; **distinct sources rechecked = 3** (S018, S029, S031), which is exactly the three cited
entries. No claim is harmed (no document cites `c2-recheck-S030.txt`:
`grep -rn "c2-recheck-S030"` over the r23 report, `corpus/lessons/round-23.md`, `SCORECARD.md` and
`corpus/knowledge/*.md` → 0 hits), but the count is a numerical assertion that R9 says must name its
scope.

### Exact minimal edit (one bullet, appended to the errata block after `SCORECARD.md:458`)

```
- **First-landing receipts are history at one revision, and one recheck receipt is a duplicate.**
  The table's 13-case C1 run (`matrix_sha256=5e61a33e…b5e76a9`, resolver `ed9a9dae…`, 6/6 GONE,
  13/13; control 7/13, `d6a3c3f1…`) is committed at lane revision **`953c278`**;
  `.ufo/waves/round-23/c1-{baseline,fixed}.json` were overwritten in place at **`bf9ce02`** by the
  24-case runs (`d05b1e0c…b809`). Re-derive the cell with
  `git show 953c278:.ufo/waves/round-23/c1-fixed.json` (and `…/c1-baseline.json`); the worktree
  path answers the errata's 24-case numbers, not the cell's. Distinct sources rechecked: **three** —
  `.ufo/waves/round-23/c2-recheck-S030.txt` is byte-identical to `c2-recheck-S031.txt` (both run
  `--source S031`, both `EXIT=0`), so "four rechecks" counts one duplicate; S018, S029 and S031 each
  have their own receipt. (R9 base + changed-file scope.)
```

Append only. Do not touch `SCORECARD.md:401-404` or the four existing errata bullets; the block's own
preamble (“the earlier cells stand as the first landing's assessment”) is the correct disposition and
stays.

### Closing sentence if L1 defers the bullet (not recommended)

> The r23 C1 cell's 13/13 is a real committed measurement at `953c278` (`git show` receipts reproduce
> 6/6 escape GONE, 7/7 controls, 13/13, exit 0); its two receipt paths were overwritten at `bf9ce02`
> by the 24-case run, and the errata block now names that revision, that changed-file scope and the
> re-derivation command — no cell text is rewritten (R9).

---

## C. Third question — what the spot-check's per-claim re-checks leave unverified

Declared r23 claims: C1 (`depth:verifiability`) and C2 (`coverage`) — two, not more. I re-derived
both at their endpoint before ruling.

**C1 — verified, and the spot-check's arithmetic is exact.** At `d0a3f6a4`:

```
c1-baseline.json  matrix d05b1e0c  resolver d6a3c3f1  cases 24  escape_GONE 0/12  pass 12/24
c1-fixed.json     matrix d05b1e0c  resolver 690153ad  cases 24  escape_GONE 12/12 pass 24/24
```

and the bound resolver is the live byte at that revision:
`git show d0a3f6a4:corpus/instruments/resolve.py | sha256sum` → `690153ad…ea2d` (fixtures
`d05b1e0c…b809`, checker `dddd5549…f98a`). Same matrix in both runs, so the delta is the resolver
only — the do-nothing control cannot meet the target. The spot-check's “improved, score held 4” holds.

**C2 — verified at both counters.** At `922a4dde` (before) and `d0a3f6a4` (after):

```
before: frontier=5  F06-F08=0
after:  frontier=8  F06-F08=3
corpus/SOURCES.md rows `S\d{3,}`: 31
```

**Claim-parts the spot-check verified only at receipt level, closed here by execution:**

1. **C2 / F06 source S018 was never re-opened by the spot-check.** Its discernment table re-opens
   S028, S029 and S031 — not S018, the authority for `corpus/knowledge/multiparty-vulnerability-coordination.md`.
   I executed the entry's own published recheck and matched its quotes against committed bytes:

   ```
   $ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018
   S018 exit=0 (7 lines)
   $ grep -c "Optional participant that can assist vendors and finders in handling and disclosing vulnerability information" corpus/source-snapshots/round-23/S018.txt  → 1
   $ grep -c "Vendor that provides a product or technology to a downstream vendor" corpus/source-snapshots/round-23/S018.txt  → 1
   ```

   (I confirmed `source-recheck.py` has no write path — `grep -c 'open(.*"w\|\.write('` → 0 — before
   running it.) S029 and S031 likewise exit 0 by execution, so all three entry rechecks are now
   executed evidence, not receipt text.

2. **C1's guard clause (“report all changed verdicts, density and anchorcheck”) was not reproduced by
   the spot-check** — it wrote “byte-same or regenerated identically per the guard”, which mixes a
   file-identity check with an instrument run it did not perform. Closed here:

   ```
   $ git diff --stat 1fafde8f d0a3f6a4 -- SKILL.md corpus/instruments/citation-survival.md corpus/instruments/citation-survival.tsv
   (empty)                                    # density inputs byte-identical, no regeneration needed
   $ python3 corpus/instruments/density.py SKILL.md --label r23
   mean dens 154.0 over 19 blocks, 652 path-citation instances, exit 0      # matches corpus/lessons/round-23.md:331
   $ python3 corpus/instruments/anchorcheck.py SKILL.md
   7 in-range / 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0, exit 0  # matches :333
   ```

   Both numbers reproduce from committed bytes; the guard is satisfied, and it is satisfied
   *vacuously* on this host (see §D.1).

**So: no declared r23 claim is left unverified.** Both claims survive at committed-evidence level,
and both weak spots are now closed at execution level.

---

## D. Residual risk and genuinely UNVERIFIED items

1. **The no-harm guard cannot speak for a mirror-bearing host.** `falsify/NoHarmDiff.md`'s
   `changed=0 added=0 dropped=0` is vacuous here (`mirror=0`, `KASEGI_MIRROR` unset) — the lane
   discloses this itself. UNVERIFIED and unverifiable on this host: that the resolver fix changes no
   verdict where a real mirror exists. The claim rests on the frozen 24-case matrix, which is stated
   in the errata (“C1 scope wording”) and is enough for the claim as written, but it is not a
   no-harm proof of the instrument.
2. **C1's matrix execution was not re-run by anyone.** Spot-check parsed receipts; I re-parsed them
   and re-derived the digests. Executing `mirror-containment-check.py` would write JSON and temp
   trees, so a read-only seat may not — the claim is therefore evidence-verified, not executed, for
   the *matrix* (unlike C2's rechecks, which I executed). Protocol-sanctioned; recorded, not papered
   over.
3. **The driver digest block in the spot-check is a copy of a mutable log.** `watchdog.log` is the
   only source for launch/complete lines; I reproduced the same four kasegi round-23 lines, so the
   copy is faithful *now*, but a log is an attestation, not a receipt.
4. **F01–F05 still exit 2.** Not an r23 claim (no claim covered them), but five admitted entries in
   the r23 tree still carry a failing `recheck:` assertion. That debt is exactly what r24 C1 counter A
   measures; nothing in this review changes it.
5. **The live instrument has already moved.** `git status --porcelain` in the lane shows
   `M corpus/instruments/resolve.py` (working tree `035f8844…`, HEAD/instrument-of-record for r23
   `690153ad…`). The diff is the round-24 C1 item-B work (empty brace alternative allowed, brace set
   deduped, glob skipping a dangling symlink:
   `git diff corpus/instruments/resolve.py` → +14/−7 at `brace_expand()` / `exists_any()`). r23's
   receipts bind `690153ad` at `d0a3f6a4` and are unaffected; but **any** re-run of an r23 command
   today answers with r24 bytes. State that in the round report so a later verifier does not read a
   changed digest as a falsified receipt.
6. **`claims.json.routed_defects` carries defects 1 and 2 only.** Defects 3 and 4 (this item) were
   routed in the spot-check text but never frozen into the round-24 claims. They are hygiene fixes:
   land them, report them as no-credit corrections, and do not let them appear as a third claim.

No tool was installed or upgraded this round (nothing was needed; pacman was not touched).
