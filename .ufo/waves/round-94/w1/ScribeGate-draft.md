# Round 94 — Gate, Mistakes and Census blocks (draft for the L1)

Drafted by seat ScribeGate from the committed evidence only: freeze `96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`,
C1 landing `d51220aeb4a538b7b211bb2629e83210669cd56d`, C2 landing `996460861d4130ddb2da6b7554e905d3e47504a3`,
base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`. The L1 owns the final lesson; this file is a drop-in draft,
not a lesson. Receipts for every observation: `.ufo/waves/round-94/w1/ScribeGate-receipts/`.

## Gate

Candidates this round (every row opened 2026-11-07): S140 admitted; S141 rejected.

### S140 — GitLab secret-detection rules (`rules/mit/gitlab/gitlab.toml` at commit 59ada1f4) — admitted, used by the instrument

- **URL:** https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules, file
  `rules/mit/gitlab/gitlab.toml` pinned to commit `59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`; HTTP 200 on the
  commit-pinned API raw URL, and the main-branch raw URL and the commit-pinned URL served identical bytes.
- **Accessed:** 2026-11-07 (fetched 15:22:31Z).
- **Capture:** `corpus/source-snapshots/round-94/S140.txt`, sha256 `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`
  (25,537 bytes, 563 lines). The committed snapshot is the 20,035-byte raw fetch (sha256 `04fc5cfa…`) with the 82
  `examples`/`negativeExamples` element lines replaced by one fixed marker, line numbering preserved. Manifest
  `corpus/source-snapshots/round-94/manifest.json`; `source-recheck.py` rc 0 (anchors 4, 114, 255; `occurrences=1`
  each), and the manifest's `lines`/`bytes`/`sha256` all match the committed file.
- **Located quotes** (each ≤25 words, byte-exact at its anchor, exactly one occurrence in the file):
  - **`S140.txt:4`** (3 words): `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''`
    — the personal access token: an optional 1-20 alphanumeric custom instance prefix plus `-`, then `glpat-`,
    exactly 20 characters of `[0-9a-zA-Z_\-]`, and the right boundary `[^0-9a-zA-Z_\-]` or end of line.
  - **`S140.txt:114`** (3 words): `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glrtr?-(?:t[1-3]_)?[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''`
    — the runner authentication token: `glrt-` or `glrtr-`, an optional `t1_`/`t2_`/`t3_` partition, 20 tail
    characters, the same boundary.
  - **`S140.txt:255`** (3 words): `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?gldt-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''`
    — the deploy token: `gldt-` plus 20 tail characters, the same boundary.
- **Tier and scope:** kind `code` because the artifact is the vendor's machine-readable rule source (TOML), not
  prose; tier A because it is GitLab's own rule for GitLab's own token formats, pinned to a commit so the bytes are
  reproducible. The scope cell confines the row to "GitLab token shapes as the vendor's own machine-readable rules
  publish them", and the teaches cell names the three facts the prose page (S139) does not carry — the alphabet,
  the optional custom instance prefix, and the exact 20-character tail. The anchor cell names the same three lines
  plus lines 30, 51, 136 and 324, which are the routable/versioned rules (`gitlab_personal_access_token_routable`,
  `…_routable_versioned`, `gitlab_runner_auth_token_routable`, `gitlab_deploy_token_routable`, all `{27,300}` tails);
  those stay named limits and are not claimed.
- **Row change (old → new):** new row after S139; status `queued` (freeze `96b5033`) → `mined` (integration);
  used-by `—` → `corpus/instruments/capture-secret-scan.py`.
- **Intake refusal and redaction:** the ruleset is itself a list of published example values shaped like
  credentials, so the gate refused the fetched bytes before any file was written —
  `INTAKE-REFUSED S140 shape=credential line=534 … written=no`, `INTAKE-REFUSED S140 shape=gitlab-pat line=7 …
  written=no`, rc 3 (`.ufo/waves/round-94/controls/capture-intake-r94.txt`). The committed snapshot therefore
  replaces every element line inside an `examples = [` or `negativeExamples = [` array with one fixed marker — 82
  lines, listed by rule id in `.ufo/waves/round-94/controls/redaction-r94.txt` — leaving the array delimiters, ids,
  keywords and regex lines untouched, so line numbering is preserved and the three anchors hold (re-checked
  structurally: 82 markers inside arrays, 0 non-marker element lines). No allowlist row is used, and the committed
  bytes scan clean: `CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 files=0 allowed=0 unused_allow=23 rc=0`.
- **Post-capture check of the trap:** the arrays this file carries are exactly what the intake gate exists to
  refuse, and the refusal keys on bytes, not on a path — the capture was admitted only in the redacted form
  recorded here, and the redaction rule is structural (every element line of every array), not derived from the
  shapes the lane's scanner happens to know.

### Rejected this round

- **S141 — the same repository's `rules/mit/github/github.toml` at commit 59ada1f4**, kind `code`, tier B, status
  `rejected`, opened 2026-11-07, recheck `180d`, used-by `—`. Rejected because no admitted entry cites it and GitLab
  is not the vendor of the GitHub token formats (tier B: a third-party copy); its `ghr_` 76-character refresh-token
  rule is the round-95 lead the decline list names.

## Mistakes

**M94-1 — class `path-shape-keyed-forgery` (recurrence of round-93 M93-4; closed this round).**

- **What happened:** round 93's plant nonce rerooted one directory but left every basename and the `round-1/`
  segment literal, so a round-92-shaped scanner keyed only on the *shape* of the rerooted paths
  (`<dir>/r<8 hex>/round-1/…`, `w/n<8 hex>/…`) recognised the plants and passed all eight limbs at rc=0 (forgery H).
- **Evidence pointer:** `corpus/lessons/round-93.md` § M93-4 and § Wave findings (CriticClaimsC2);
  `.ufo/waves/round-93/w1/CriticClaimsC2.md` § qualifier.
- **Captured-by:** CriticClaimsC2's forgery H; no frozen limb or control was keyed on path shape.
- **Fix:** `relocate(path, nonce)` (`.ufo/waves/round-94/c2/capability-check.py:503-520`, landed in `9964608`)
  derives the leaf directories *and* the basename from `sha256("<nonce>|<path>")[:12]` — directories become
  `r<nonce>` / `p<nonce>` / `n<nonce>`, the basename becomes the digest plus the extension (the `live-` prefix is
  kept only where the name class itself is under test) — while keeping the scan-scope prefix
  (`corpus/source-snapshots/`, `corpus/practice/…/evidence/`, `w/…-receipts/`) that the scanner's file-class rules
  depend on. Every plant, allowlist line and false-positive fixture goes through it. K9 is a new previous-landing
  regression limb (`.ufo/waves/round-94/c2/capability-check.py:634-650`): the round-93 landing instrument must
  still find its 39 hits and may not lose one when a shape is added.
- **Shown able to fail:** committed control `.ufo/waves/round-94/controls/c2-controls-r94.txt:26`
  `CONTROL F1-path-shape-keyed rc=1 want=1 PASS` — the forged path-shape-keyed instrument fails K4 at `:31`
  (`missing=` 30 path|shape pairs, every path a digest basename and no `round-1/` segment anywhere in the list) and
  K9 at `:33` (`lost=` 26 pairs), with K1 catching the tampered instrument by sha at `:28`; the pinned candidate
  passes at `:2` rc 0 with `:9` `LIMB K9 pass prev_rc=1 prev_hits=39 lost=none prev_caught_new=none`.

**M94-2 — class `vacuous-control` (recurrence of round-93 M93-5; closed this round).**

- **What happened:** round 93's counter did `b, a = file_at(...)` inside the M3 labelled-file walk, shadowing the
  argparse namespace `a`; any label citing a file outside `corpus/knowledge` turned `a` into a string, and
  `if a.map_sha256:` raised `AttributeError` before a single LIMB line printed. The frozen control recorded
  `rc=1 want=1 PASS` — a crash read as a detection, on exactly the input the sentence "M3 walks every labelled
  file" exists for.
- **Evidence pointer:** `corpus/lessons/round-93.md` § M93-5; `.ufo/waves/round-93/w1/MutC1Counter.md` § R1
  (`probes/P17-fx7-frozen.txt`, `02-r1-shadow-repro.txt`; `variants/r1fix.py`).
- **Captured-by:** MutC1Counter R1; no control exercised a labelled file outside `corpus/knowledge`.
- **Fix:** the shadowing is gone in `.ufo/waves/round-94/c1/knowledge-meter.py`, and the union is exercised by three
  controls over one label that cites `corpus/QUALITY.md:537` (a repoint `SKILL.md:1224` → `SKILL.md:1225`):
  applied, under the pre-round-93 counter, and with an unmapped edit. Each control asserts a LIMB observation
  (`limb=True` / `traceback=True`), not rc alone.
- **Shown able to fail:** `.ufo/waves/round-94/controls/c1-controls-r94.txt:24`
  `CONTROL m3-union-applied rc=0 want=0 PASS` with `:28` `LIMB M3 pass same_files=True bad_lines=0 …`;
  `:35` `CONTROL m3-union-applied-before-r93 rc=1 want=1 PASS traceback=True`, i.e. the round-93 counter crashes
  on the same input (`:37` `Traceback (most recent call last):`) instead of printing a limb; `:38`
  `CONTROL m3-union-unmapped rc=1 want=1 PASS limb=True` with `:42` `LIMB M3 FAIL same_files=True bad_lines=1 …`,
  so the union is live — an unmapped edit inside the non-knowledge labelled file fails M3 rather than passing.
- **Scope note:** the C1 landing's own 19 labels all cite `corpus/knowledge`, so the union walk is proven by the
  wave control, not by the round's label set; the claim's sentence is about the counter's capability, which is what
  the control exercises.

## Census

- **Command:** `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (run from
  `/home/vgpnk/Projects/shokunin`) → **rc 0, 7 output rows**: six inherited `W04` duplicate-URL warnings (S028,
  S029, S072, S076, S080, S085 — unchanged since round 89) and one
  `kasegi ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`. No `E`-code names S140 or S141:
  E01 (row shape), E05 (kind), E06 (tier), E07 (status), E08 (opened) and E09 (recheck) are all silent, and E11 is
  silent because used-by is `—`.
- **Row count:** `census` mode → `kasegi rows 141` (tier.A 128, tier.B 7, tier.C 6, status.mined 115,
  status.queued 2, status.rejected 24), FLEET identical with `FLEET.invalid 0` and `missing 0`. The same command
  read `rows 140` (tier.B 6, status.rejected 23) before the S141 row appeared; the freeze's own receipts are
  `.ufo/waves/round-94/controls/census-start-r94.txt` (rc 0, 139 rows) → `…/census-mid-r94.txt` (rc 0, 140 rows,
  the same six W04).
- **S140 row, cell by cell:** 11 cells; kind `code`; tier `A`; status `queued`; opened `2026-11-07`; recheck
  `180d`; used-by `—`. The anchor cell's three quoted lines resolve at 4, 114, 255, and its four limit lines at 30,
  51, 136, 324 are the routable/versioned rules kept as named limits.
- **The two round-94 bullets:** `SOURCES.md:335` (S140 added; "Registry 140 rows before the integration status
  change" — true at the freeze, where census-mid read 140) and `SOURCES.md:336` (S141 added; "Registry 141 rows
  after this row (S140 + S141)" — matches the current census, 141). Both sit in the `## Registry changes`
  change-log section as prose, not registry rows, so E12 (row-shaped source outside `## Registry`) is silent.
- **State qualifier:** when this block was drafted, `git status` showed `M corpus/SOURCES.md`; the S141 row and its
  bullet are not committed, and the freeze state (`96b5033`) carries only the S140 bullet and 140 rows. The count
  the integration commits is 141 if S141 is kept.
