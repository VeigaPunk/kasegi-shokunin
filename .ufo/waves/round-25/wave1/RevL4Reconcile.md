# RevL4Reconcile — D24-4, L4's fail-before (round 25, wave 1)

Seat: reviewer (read-only). Item D24-4 from
`corpus/lessons/round-24-verifier-spotcheck.md:207`: "L4's fail-before is described three
incompatible ways (erratum 3, `ResolverAttack.md:176`, `c1-control-baseline.txt`) … One sentence
in the next lesson reconciling them, with the receipt as the authority."

Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. No production edit; the only lane write is
this file. All three artefacts were read at the bytes committed in `d3614a2`
(`git status --short` clean for `SCORECARD.md` and `ResolverAttack.md`; the two receipt files are
untracked round-24 wave artefacts, unchanged since `04:25:54 -0300`).

---

## 1. The three descriptions, quoted

### (A) `SCORECARD.md:492-496` — round-24 erratum 3

```
3. The wave-1 `LivenessMatrix` item's L4 (dangling *brace* alternative) could not
   fail the baseline: `brace_expand` already tested `os.path.exists` per
   expansion. The landed matrix's L4 keeps that citation as a post-fix guard and
   adds a bounty/mirror empty-alternative citation, which is what fails on the
   baseline; the receipt prints both citations per case.
```

Reads as: the dangling-brace primary **cannot** fail the baseline, so it is retained as a
post-fix guard; the case fails **only** on the added bounty/mirror empty-alternative citation;
both citations print per case. L4 stays in the `L` (liveness) block.

### (B) `.ufo/waves/round-24/wave1/ResolverAttack.md` — the pointer D24-4 gives is `:176`

Line 176 is a **blank line** (the `## F6 …` heading is `:175`). The claim the pointer names is the
F6 bullet at `:179-180`; the same claim is stated in full in §F1 at `:34-39`:

```
179|- L4 should be re-labelled a **control** (its primary assertion is green on the baseline), and the before-count
180|  restated as `3 liveness + 4 controls + 1 duplicate-class citation = 4/8`.
```

```
34|`L4`'s primary assertion carries **no** `path_check` reason, while every genuinely failing assertion does
35|(`path_check=missing-path` / `path-missing-on-disk`). In
36|`corpus/instruments/resolve-dispatch-check.py:188-210`, `status = PASS` iff `cls == expect` **and**
37|`path_check == ""`; the case-level `FAIL` is the aggregation of the two citations
38|(`record["status"] = PASS iff all assertions PASS`). Therefore **L4's primary citation
39|(`brace/{alpha,beta}.md`, dangling first, live second) passes on the frozen baseline.** The case only fails
40|because of its added bounty/mirror citation `~/Projects/bounties/{ops,}/rank.mjs` — an *empty-alternative*
```

Reads as: L4's primary assertion is green on the baseline, so L4 is really a control and **should be
re-labelled**; the before-count is `3 liveness + 4 controls + 1 duplicate-class citation = 4/8`.

### (C) `.ufo/waves/round-24/c1-control-baseline.txt:5-6` — the receipt

```
5|L4   liveness expect=INTERNAL         actual=INTERNAL         FAIL
6|     also expect=MIRROR-EQUIVALENT actual=GONE             FAIL path_check=missing-path
```

with `:12` `cases=8 pass=4 exit=1`.

As printed: L4's nature is **`liveness`**, and the line carrying the primary citation
(`expect=INTERNAL actual=INTERNAL`) ends in **`FAIL` with no `path_check` reason**. Read at face
value this is the only one of the three that attributes the fail-before to the primary assertion,
and it shows a FAIL that its own expect/actual pair does not explain.

### Where they are incompatible

1. **Label.** (B) says relabel L4 a control; (C) prints `liveness`; (A) keeps L4 in the liveness
   block and calls the primary a "post-fix guard".
2. **Which citation fails the case.** (A) and (B) agree it is the added bounty/mirror citation;
   (C), read without the printer, says the primary assertion FAILed (`expect == actual`, no reason).
3. **Count framing.** (A) counts the case once; (B) restates the before-count as
   `3 + 4 + 1 = 4/8`, summing cases (3 liveness, 4 controls) with one case re-counted by its
   citation class — arithmetically opaque, and not a field the receipt prints.

---

## 2. What the receipt actually shows for L4

**Primary assertion result: PASS.** **`path_check` ran on it and corroborated it.** The case, not
the primary assertion, is what fails.

Evidence chain, all committed bytes:

- **JSON receipt** `.ufo/waves/round-24/c1-control-baseline.json` (`checker_sha256`
  `acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1`, `resolver_sha256`
  `690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d`, `matrix_sha256`
  `fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c` — all three match receipt
  line 13), case `L4`, `"nature": "liveness"`, `"status": "FAIL"`, `"problems": []`:
  - `assertions[0]`: `"cite": "brace/{alpha,beta}.md"`, `"expect": "INTERNAL"`, `"actual":
    "INTERNAL"`, `"expect_file": "lane/brace/beta.md"`, `"resolved_path": "<CASE>/lane/brace/beta.md"`,
    `"method": "brace"`, `"domain": "rel"`, `"path_check": ""`, **`"status": "PASS"`**.
  - `assertions[1]`: `"cite": "~/Projects/bounties/{ops,}/rank.mjs"`, `"expect":
    "MIRROR-EQUIVALENT"`, `"actual": "GONE"`, `"path_check": "missing-path"`, `"status": "FAIL"`.
  - `totals`: `{"cases": 8, "liveness": 4, "controls": 4, "pass": 4, "fail": 4, "exit": 1}`.
- **Why the text receipt prints `FAIL` beside the primary citation.**
  `corpus/instruments/resolve-dispatch-check.py:329-337` prints `record["status"]` — the **case**
  aggregate, computed at `:268-270` as PASS iff *all* assertions pass — on the line that carries
  `assertions[0]`'s `expect`/`actual`; the `path_check=` suffix on that line is drawn only from
  `assertions[0]`'s own field (`:332-335`), and an empty reason prints nothing. So the `FAIL` on
  line 5 is the case verdict; the primary assertion's own status never appears on that line.
- **Whether `path_check` ran.** Yes, for every assertion: `check_assertion` assigns
  `rec["path_check"] = path_verdict(...)` unconditionally at `:206`, and PASS requires
  `cls == item["expect"] and rec["path_check"] == ""` at `:208`. For the primary, `path_verdict`
  (`:168`) compared the resolved realpath with `lane/brace/beta.md` and returned `""` — a
  corroboration, not a skip. For the second assertion it returned `missing-path`.
- **The label in the instrument.** `corpus/instruments/resolve-dispatch-fixtures.json:72-73` fixes
  L4 as `"id": "L4", "nature": "liveness"`, and `load_matrix` rejects any split other than exactly
  4 liveness / 4 control (`resolve-dispatch-check.py:288-293`, message `nature-split-%d-%d`).
  Relabelling L4 a control therefore requires editing the frozen matrix — the post-hoc rule change
  `ResolverAttack.md:180-181` itself warns against.
- **Reproduced today (read-only, temp dirs only).**
  `python3 corpus/instruments/resolve-dispatch-check.py --resolver
  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/c1-baseline-resolver.py`
  printed 13 lines byte-identical to the receipt (`diff` empty → `IDENTICAL_TO_RECEIPT`),
  `EXIT=1`, closing line `sha256 resolver=690153ad…7ff3ea2d matrix=fef0f02d…f9414c8c
  checker=acbb6870…a0569e1`. The receipt is the authority and it reproduces.

---

## 3. The reconciling sentence for the round-25 lesson (43 words)

> The receipt is authority: L4's printed FAIL is the case verdict; its primary citation passed
> (INTERNAL, lane/brace/beta.md, path_check empty) and the case failed only on the added
> bounty/mirror citation (GONE, path_check=missing-path), so L4's fail-before is that second
> citation; the receipt labels L4 liveness.

**How a future reader checks it against the receipt.** Line 5 shows `FAIL` on the L4 line while
the primary's `path_check` is empty — empty means corroborated, because `:206-208` runs the check
for every assertion and requires `""` for PASS; line 6 shows the only failing assertion, `GONE`
with `path_check=missing-path`; `c1-control-baseline.json` records `assertions[0].status: "PASS"`
and `nature: "liveness"`; line 12 gives `cases=8 pass=4 exit=1`, i.e. the case is one of the four
failures and the primary is not why.

---

## 4. Findings

**Low — D24-4's own citation.** `ResolverAttack.md:176` is a blank line. The substantive claim is
at `:179-180` (F6 bullet) and `:34-39` (F1). Quote the bullet, not the heading offset.

**Medium — root cause of the misreading, not fixed here (outside this seat's write scope).**
`resolve-dispatch-check.py:329-337` prints the *case* status on the line that presents the
primary citation's expect/actual, and omits an empty `path_check` reason. Every reader who has not
read the printer will read `expect=INTERNAL actual=INTERNAL FAIL` as an unexplained assertion
failure — which is exactly what description (C) shows. Correcting it (print
`detail.get("status")`, or add an explicit `case=` token) changes receipt bytes, so it belongs to
the round-25 instrument owner; this reconciliation must not rewrite round-24 receipts.

**Resolved by the receipt.** (A) and (B) agree on the substance — the dangling-brace primary is
green on the baseline and the case fails on the second, bounty/mirror empty-alternative citation.
They differ only in the label and in the count framing, and the receipt's own `nature` field plus
the instrument's frozen 4/4 split settle both in favour of keeping `liveness`: the "control /
duplicate-class citation" reading is a true statement about *which defect classes the matrix
exercises*, not a licence to relabel a frozen case. Description (C) is correct as bytes and
misleading only because the printer conflates two statuses.

---

## 5. No-harm, tooling, gaps

- **Read-only.** Commands run: `read`; `sha256sum`; `diff`; `awk`; `stat`; `git log`/`git status`
  (read-only); one `resolve-dispatch-check.py --resolver …` run without `--json`, which writes only
  into its own `tempfile.mkdtemp` case roots and removes them (`:274` `shutil.rmtree`). No lane file
  was modified by any of it.
- **Tooling.** No installs, no upgrades, no package-manager calls (the host-wide pacman pause is
  respected).
- **Verification gap, named.** The JSON quote is the committed `c1-control-baseline.json`; I did
  not regenerate it, because `--json` would write a lane file. The text re-run covers the same
  checker/resolver/matrix hashes (line 13), so the per-assertion records are bound to the same
  three inputs.
- **Blocker:** none.
