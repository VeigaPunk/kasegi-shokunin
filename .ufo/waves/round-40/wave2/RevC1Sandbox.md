# RevC1Sandbox — round 40 wave 2 receipt (C1 sandbox falsification)

Seat: `RevC1Sandbox` (leaf member; no subagent dispatch). Wave: FALSIFY wave 2,
dispatched by the L1 (agent `KasegiR40`, hyaku run 9). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` used read-only throughout; no
lane file edited; no mutating git/jj command run anywhere; no campaign tool run
in `/home/vgpnk/Projects/shokuknow`.

Refs and bytes:

- base `a7af2ce63bce153757d39bf66b366a96caf30c13`; claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`.
- Judged head J = `3074c7679d6f527ec3930d7748ccce1dbae4a58a` (lane HEAD at
  attack time). **Y did not yet exist as a lane commit**: the round-40 receipt
  `.ufo/waves/round-40/final-gates/all-gates.txt` is untracked on disk at J
  (`git log --all -- <receipt>` is empty), so every Y-scoped run below executed
  at **Y′ = `da42d1af7614209aec9bb29026047da8ae7d9a9a`** — a fixture commit in a
  read-only clone carrying exactly J's tree plus the on-disk receipt bytes
  (sha256 `7b8cda36c793c5855fa6ffcb78d241fca47f0d3679b2d7c38f7a959042463484`).
  The baseline run at Y′ reproduces those bytes byte-for-byte (`cmp` equality).
- Suite under attack: `corpus/instruments/r40-closure.sh` at Y, sha256
  `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e` (matches the
  receipt's `suite-sha256`). 1734 lines, read in full before attacking.
- Attack fixture lane: `git clone --no-hardlinks` of the lane into my scratch;
  every attack fixture is a commit on top of Y′ with identity
  `r40-fixture@local`. Run template:
  `bash r40-closure.sh --export-ref <ref> --lane <fixclone> --work <w-dir> --scratch-root <sr-dir>`
  with an isolated empty scratch root per run so H6 cannot mask the target check.

Axes attacked: **depth:verifiability** (primary — C1's sandbox: export
containment, work-dir state, scratch-root scan), **coverage** (every check
H1–H10 probed at least once). No claim authored, edited, judged or shipped.

## Verdict

The sandbox leaks on the read side and holds on the write side. Three defect
classes demonstrated against the export boundary, one of which reaches a full
`closed=10/10 exit=0` with the receipt bytes living **outside the export** (in
the live lane); H8 executes tree-controlled bytes and records forged
negative-control values as a green check; `--receipt-out` can overwrite a
tracked lane file. The write-side traversal, the stale-`--work` defense, the
scratch-root stray scan and the `--work` lane guard all held. All five C1
counting commands reproduced. Every file-reading check (H1–H5, H7, H9, H10) was
individually flipped green by an export symlink while the committed tree
carried a symlink instead of the claimed bytes; the overall tally stayed red in
all those cases only because H7's diff-clean clause independently reds any
non-receipt tree change.

## Item 1 — symlink inside the tree pointing outside the export

Attack: fixture commits replace an export path with a symlink (mode `120000`,
verified with `git ls-tree` per ref) whose target is outside the export root.
The suite extracts with `git archive | tar -xf` and never validates members, so
the symlink lands in the export and every subsequent read follows it.

| Fixture (ref) | Symlink planted | Check flipped | Result |
|---|---|---|---|
| F1 `990b153f…` | `corpus/QUALITY.md` → live lane's `corpus/QUALITY.md` (absolute) | H3 | **H3 green** `mentions=1,rows=1 closed=1` reading the live lane's file; committed tree carries a symlink, not the criterion bytes. H7 red (`diff-clean=0`) → `closed=9/10 exit=1`. |
| F1r `8f981819…` | `corpus/QUALITY.md` → `../../../outside-qual.md` (relative `..` escape resolving to my scratch) | H3 | Same green payload via a file outside the export; `closed=9/10`. |
| F2 `24f1f63d…` | `corpus/instruments/density.py` → copy of the original bytes in my scratch | H10 density limb | **`density=1 closed=1`** via outside bytes while the committed density instrument is a symlink (not byte-identical bytes in the tree). `closed=9/10`. |
| F3 `a958f236…` | `corpus/instruments/r40-closure.sh` → doctored script in my scratch | H8 | **H8 executed the doctored bytes** (proof file written at `2026-10-26T22:13:13Z`) and recorded forged negative controls `base=0/10,base-exit=1,r39=0/10,r39-exit=1` as **green** — honest values are `base=3/10`, `r39=2/10`; the negative controls never ran. H1 red (`digest=0`), H5 red (`control=5/8`) → `closed=6/10`. |
| F4b `ce14fd99…` | `.ufo/waves/round-40/final-gates/all-gates.txt` → **the live lane's own receipt file** | H7 (and the whole run) | **`closed=10/10 exit=0`** with the receipt bytes held outside the export; the committed tree carries no receipt bytes (mode `120000`). H7 green: `ancestor=1,diff-clean=1,payload-match=9` — the only tree change is the receipt path itself, so the diff-clean clause does not fire. Live-receipt sha256 unchanged before/after the run. |
| F4c `405f7373…` | receipt → garbage file in my scratch | H5, H7 | Red (`control=0/8`, `sentinel=0`) → `closed=8/10` — non-canonical outside bytes fail closed; only canonical-equivalent outside bytes green. |
| F5 `f6445bae…` | whole `corpus` dir → live lane's `corpus` | H1, H2, H3, H4 | All four green reading **live-lane corpus bytes** (suite digest, lesson corrections, criterion row, located quotes). H5 red (`control=6/8`), H9 red (`valid=154/172` — the numstat limb catches the tree change), H10 red (`deleted=276`), H7 red → `closed=6/10`. |
| F6 `2e760db1…` | `SCORECARD.md` → live lane's `SCORECARD.md` | H2 | **H2 green** `corrections=8,named=5` via live-lane bytes; `closed=9/10`. |
| F7 `31989a54…` | `SKILL.md` → live lane's `SKILL.md` | H1 registry limb | **H1 green** (`registry=1`) via live SKILL.md; H10's numstat limb caught the substitution (`skill-del=1115`) → `closed=7/10`. |

Transcripts: `RevC1Sandbox.f1-quality-symlink-live.txt`, `.f1r-quality-symlink-rel.txt`,
`.f2-density-symlink.txt`, `.f3-suite-symlink-exec.txt`, `.f4b-receipt-symlink-green.txt`,
`.f4c-receipt-symlink-garbage-red.txt`, `.f5-corpus-symlink.txt`,
`.f6-scorecard-symlink.txt`, `.f7-skill-symlink.txt` (byte-exact, beside this receipt).

**Verdict: DEFECT FOUND (three classes, D1–D3 below).** The header's claim
"every tree limb reads bytes only under that export root" is false: reads (and,
for H8, execution) follow committed symlinks out of the export, including into
the live lane.

## Item 2 — path traversal candidate

- (a) A tree member named `../trav-marker-1`: `git mktree` refuses
  slash-containing names, so the entry was crafted as a raw tree object
  (`hash-object -t tree -w --stdin --literally`, sorted per git tree order) and
  committed as T1 `8dfda64f…` on Y′. `git archive` itself refuses it:
  `error: invalid path '../trav-marker-1'` / `fatal: failed to unpack tree
  object` — the suite dies **exit 2** (harness error, fail-closed) and **nothing
  escaped the export root** (no marker found at `$WORK/` or above). A second
  member `corpus/../../../trav-marker-2` was included in the same fixture; same
  refusal. Transcript: `RevC1Sandbox.t1-traversal-refused.txt`.
  **Verdict: GUARD HOLDS (write-side traversal neutralized at the archive
  layer; tar never sees a `..` member).**
- (b) Declared-block paths containing `..` (fixture H9T `c8d160ca…` appends
  `../outside-declared.md`, `corpus/../corpus/QUALITY.md`, `corpus//QUALITY.md`,
  `/etc/passwd` to `declared-blocks.txt`, outside file present with matching
  sha): `path_safe` rejects all four → `H9 payload=declared=176,valid=172,…,paths=0 closed=0`
  → `closed=7/10 exit=1`. Transcript: `RevC1Sandbox.h9t-declared-traversal-red.txt`.
  **Verdict: GUARD HOLDS (declared `..`/`//`/absolute rejected; no read outside
  the export via a declared path).**

## Item 3 — reused `--work` with a previous export (stale-state trick)

- Stale-1: the Y′ green run left a complete stale green export and a green
  `payloads.tsv` in `--work w-base` (the suite's exit cleanup removes
  `export/`, `mut/`, `neg-*` — but see D5: loose work files survive). Re-running
  the **same work dir** at base `a7af2ce…`: `closed=3/10 exit=1` with **fresh**
  payloads (`H1 suite=0,digest=0,registry=0` — base-tree values; `payloads.tsv`
  head is the fresh red line). The stale green export and stale green payloads
  were cleared (`rm -rf` + re-extract; `: > "$PAYFILE"` truncation).
- Stale-2: planted a forged green `payloads.tsv` (rebuilt from the Y′
  transcript) into the work dir, then ran at base again: `closed=3/10 exit=1`,
  payloads fresh. The planted green bytes never reached any check.

Transcripts: `RevC1Sandbox.stale-work-base-red.txt`, `.stale-work-planted-red.txt`.
**Verdict: GUARD HOLDS — a reused `--work` cannot satisfy a check with stale
bytes; no stale green reproduced.**

## Item 4 — `--scratch-root` with unrelated strays / empty

| Run | Scratch root contents | H6 payload | Verdict |
|---|---|---|---|
| Sc-1 | `kasegi-r40-unrelated-a/` (+nested leftover), `kasegi-r39-unrelated-b/` | `strays=2,read=ok closed=0` → `closed=7/10 exit=1` | **RED as required** — unrelated family strays counted. |
| baseline (sr-base) | empty dir | `strays=0,read=ok closed=1` → `closed=10/10 exit=0` | **GREEN as required.** |
| Sc-3 | non-family stray `unrelated-r42-stray/` | `strays=0,read=ok` → `closed=10/10` | GREEN — family scoping (`kasegi-r39*`/`kasegi-r40*`) works. |
| Sc-4 | root `chmod 000` | `strays=0,read=fail closed=0` → red | fail-closed on an unreadable root. |
| Sc-7 | broken symlink `kasegi-r40-broken` → nonexistent | `read=fail` → red | fail-closed on an unreadable family entry. |
| Sc-5 | `--work` inside `sr/kasegi-r40-gold/work` + stray `sr/kasegi-r40-gold/nested-stray` | `strays=0,read=ok` → `closed=10/10` | GREEN — the **disclosed blind spot**: entries nested inside the family dir containing `--work` are never audited (D7). |
| Sc-6 | scratch root is a regular **file** | `strays=0,read=ok` → `closed=10/10` | GREEN — a non-directory root skips the scan entirely instead of failing closed (D6). |

Transcripts: `RevC1Sandbox.scratch-strays-red.txt`, `.scratch-nonfamily-green.txt`,
`.scratch-unreadable-red.txt`, `.scratch-broken-symlink-red.txt`,
`.scratch-nested-blindspot-green.txt`, `.scratch-file-root-green.txt`
(the empty-root green is `RevC1Sandbox.y-baseline-green.txt`).

## Counting commands re-run (C1, claims.json)

| Command | Expected | Observed | Fixture |
|---|---|---|---|
| `bash corpus/instruments/r40-closure.sh --export-ref <Y>` | `closed=10/10 exit=0` | `closed=10/10 exit=0` at Y′ (Y not yet a lane commit; see header) | `RevC1Sandbox.y-baseline-green.txt` |
| `… --export-ref 3074c76…` (J, receipt absent) | documented green window | `closed=9/10 exit=1`, `H7 …receipt=0…` | `RevC1Sandbox.counting-j-greenwindow.txt` |
| `… --export-ref a7af2ce…` | `closed<10/10 exit=1` | `closed=3/10 exit=1` | `RevC1Sandbox.counting-base-red.txt` |
| `… --export-ref 8371e7a…` | `closed<10/10 exit=1` | `closed=2/10 exit=1` | `RevC1Sandbox.counting-r39-red.txt` |
| `bash corpus/instruments/r40-closure.sh` | exit 2 | exit 2, refusal message | `RevC1Sandbox.counting-plain-refused.txt` |

The four lane-scoped runs executed literally in the lane root with
`TMPDIR` inside my seat scratch (so the auto work dir sits inside the
`kasegi-r40` family dir and H6 excludes it; `strays=0,read=ok` observed). All
five reproduce the frozen claims; the green re-run is recorded evidence.

## Findings (defects), by severity

- **D1 (high) — H8 executes tree-controlled bytes; forged negative controls
  recorded green.** `check_h8` runs `bash "$tree/corpus/instruments/r40-closure.sh"`
  with no requirement that the file be a regular file matching the pinned
  digest. Fixture F3: the export's suite is a symlink to a doctored script; the
  suite **executed it** (proof file `/fast/scratch/hyaku/kasegi-r40/RevC1Sandbox/h8-exec-proof.txt`
  written at `2026-10-26T22:13:13Z` — arbitrary code execution with the runner's
  privileges, from untrusted tree content) and H8 recorded
  `base=0/10,base-exit=1,r39=0/10,r39-exit=1 closed=1` — negative-control values
  the honest suite never prints (honest: `base=3/10`, `r39=2/10`), i.e. H8
  "verified" controls that never ran. The overall tally stayed red only because
  H1's digest limb independently reds (`digest=0`). Fix direction: H8 must gate
  execution on the H1 limbs (regular file + digest equal to `suite_digest()`),
  or `prepare_export` must refuse symlink members (wave-1 memo T6 guard).
- **D2 (high) — H7 accepts a receipt that is a symlink to bytes held outside
  the export; full `closed=10/10 exit=0` with no receipt bytes in the tree.**
  Fixture F4b: the only tree change vs Y′ is the receipt path becoming a symlink
  to the live lane's own receipt file. H7 greens (`ancestor=1,diff-clean=1,
  payload-match=9`, `cmp` equality) because the outside bytes equal the
  canonical transcript. The "Y = J + receipt bytes" contract is bypassed at the
  sandbox layer: the committed tree carries a pointer; the validated bytes live
  in the live lane and are read at run time. Honest caveat: no value forgery —
  H7 re-derives every payload and `cmp`s the bytes, so the outside file must
  equal the canonical transcript (F4c: garbage target reds, `closed=8/10`). The
  defect is the boundary violation ("every tree limb reads bytes only under that
  export root" is false), not a tally forgery.
- **D3 (medium) — every file-reading check follows symlinks out of the export.**
  `[ -f ]`, `grep`, `awk`, `sed`, `tail`, `sha256sum` all follow; no check
  rejects a non-regular file. Demonstrated per check: H3 (F1/F1r), H10 density
  limb (F2), H2 (F6), H1 registry limb (F7), H1/H2/H4 (F5 corpus-dir symlink),
  H9 tail-sha reads (F5: `got==sha` via live bytes; the numstat limb then
  catches the tree change), H5/H7 receipt reads (F4b/F4c). Per-check false
  greens; the overall tally is protected by H7's diff-clean clause (any
  non-receipt tree change reds H7 — held in all seven content fixtures).
- **D4 (medium) — `--receipt-out` has no lane guard (asymmetric with
  `--work`).** `make_work` refuses a work dir inside `--lane`; `--receipt-out`
  is written wherever the caller points it. Demonstrated on my own fixture lane:
  `--receipt-out $FIX/SCORECARD.md` overwrote the tracked `SCORECARD.md` with
  receipt bytes, exit 0, no complaint (fixture restored afterwards; the real
  lane was never touched). A mistyped `--receipt-out` clobbers a lane file.
  Transcript: `RevC1Sandbox.receipt-out-lane-write.txt`.
- **D5 (medium-low) — the `--work` guard is scoped to the `--lane` argument
  only.** With `--lane` overridden (fixture runs), a `--work` resolving into the
  real lane was **accepted** and the suite wrote `export/`, `mut/`, `neg-base/`,
  `neg-r39/`, `payloads.tsv`, `pay.tsv`, `h7row.tsv` under the real lane during
  the run. This was an accident of my own probe (symlink `--work` → real lane
  while `--lane` pointed at the fixture clone); I removed the three surviving
  loose files immediately and verified `git status --porcelain` matches the
  pre-existing four untracked `.ufo/waves/round-40` entries (the suite's own
  cleanup had removed `export/`, `mut/`, `neg-*`). With the canonical
  invocation (`--lane` = the lane being verified) the guard fires correctly —
  direct and symlinked paths into the lane both die exit 2 with no trace
  (`RevC1Sandbox.work-guard-symlink-refused.txt`, `.work-guard-inside-refused.txt`).
- **D6 (low) — H6 fail-open on a non-directory scratch root.** A scratch root
  that is a regular file (or, by the same `[ -d ]` branch, a nonexistent path)
  skips the scan and prints `strays=0,read=ok` → green (`RevC1Sandbox.scratch-file-root-green.txt`).
  The header promises "fail-closed on a scan error"; a root that cannot be
  scanned as a directory is silently treated as clean. An empty-but-existing
  root must green (per seat spec) — but a bogus root is indistinguishable from
  "caller passed a wrong path" and should red (`read=fail`).
- **D7 (low, disclosed limit with fleet-layout bite) — H6 never audits entries
  nested inside the family dir containing `--work`.** Disclosed in the header,
  but the fleet's actual layout puts every seat's scratch inside
  `/fast/scratch/hyaku/kasegi-r40/<SEAT>/` — one family dir. Any leftover a seat
  leaves under `kasegi-r40/` is structurally invisible to H6 (Sc-5: nested stray
  + work in the same family dir → `strays=0` green), so the H6 green is weaker
  than the kill rule's "any leftover kasegi-r39*/r40 scratch entry at filing"
  wording, which reads as covering nested entries too.
- **D8 (low) — `--export-ref` accepts aliases contrary to the wave-1 memo.**
  `CritC1AntiSuite.txt` §T6(b) demands refusing any non-40-hex ref with exit 2
  (`cases=ref-alias-head`, `ref-short`, `ref-blob`). The built suite resolves
  `HEAD` and short hashes and runs them (`RevC1Sandbox.ref-alias-head.txt`,
  `.ref-alias-short.txt`: both `closed=10/10 exit=0` at Y′). Mitigation: the
  transcript's `export-ref` line comes from the receipt and H7 binds the
  resolved commit via ancestor+diff-clean, and blob refs are refused exit 2
  (`RevC1Sandbox.ref-blob-refused.txt`) — so no mis-binding was demonstrated;
  the memo's refusal requirement is simply not implemented.
- **Meta-finding — the wave-1 adversarial spec's extraction guard was dropped
  in build.** `CritC1AntiSuite.txt` §T6 specifies: "after extraction, canonicalize
  every member and refuse any member that is a symlink whose normalized target
  escapes `$EXPORT` … (mirror `g1_path_safe`)", proven by graded selftest
  mutants `cases=export-traversal-symlink` / `export-traversal-path`. The built
  suite has **no extraction containment step** (D1–D3 are the direct
  consequence) and **no such selftest mutants** (none of the ten
  `selftest_case_H*` functions contains an export-symlink case; H9's `escape`
  mutant covers only the declared-path `..` clause). The memo's freeze-gap note
  explicitly said this defense is mandatory even if H1–H10 read as closed.

## Guards confirmed (green/red evidence, recorded even where the attack failed)

1. Plain run refused, exit 2 (`counting-plain-refused.txt`).
2. Write-side `../` traversal: `git archive` refuses the member; suite dies
   exit 2; nothing escaped the export root (`t1-traversal-refused.txt`).
3. Declared-block `path_safe` rejects `..`, `//`, absolute (`h9t-declared-traversal-red.txt`).
4. Stale `--work`: export/`mut`/`neg-*` cleared, `payloads.tsv` truncated;
   reused work at base prints fresh red payloads; planted green payloads
   overwritten (`stale-work-base-red.txt`, `.stale-work-planted-red.txt`).
5. Scratch-root scan: family strays red (`strays=2`), empty root green,
   non-family strays ignored, unreadable root and broken-symlink entries fail
   closed (`scratch-*.txt`).
6. `--work` into the `--lane` (direct or via symlink) refused exit 2, no trace
   (`work-guard-*.txt`) — for the canonical `--lane`.
7. H7's diff-clean clause contains every content-level attack: all seven
   content fixtures (F1, F1r, F2, F3, F5, T1, H9T) closed <10/10; only the
   receipt-path change (F4b) can go green, and then only with canonical bytes.
8. Non-canonical outside receipt bytes red (F4c).
9. Blob ref refused exit 2 (`ref-blob-refused.txt`).

## Residual risk and verification gaps

- The symlink class was tested on QUALITY.md, density.py, the suite file, the
  receipt, `corpus/` as a dir, SCORECARD.md and SKILL.md. H2's LOG.md/SHONEN.md
  and H1's instruments-README limb were not individually symlinked — same read
  mechanism as the demonstrated cases ([INFERENCE] they behave identically; F5
  already covers the corpus-side files).
- The write-side traversal was only reachable through a hand-crafted tree
  object (git plumbing refuses `..`/slash names); `git archive`'s own path
  validation blocked it. A hostile tar stream is unreachable through the suite's
  own archive call, so the tar layer itself was not fuzzed.
- F4b's outside bytes were the canonical transcript; the "outside file mutated
  between producing and verifying runs reds" claim follows mechanically from
  H7's `cmp` (F4c demonstrates the red path) — not separately timed.
- D5's real-lane write was an accident of my probe, cleaned immediately; the
  lane's `git status --porcelain` was verified equal to the pre-existing four
  untracked `.ufo/waves/round-40` entries before and after cleanup.
- H6 is a live scan: sibling seats were active during my runs; every recorded
  run showed `strays=0,read=ok` except the crafted scratch fixtures.
- `--selftest` was not run (other seats' scope); the missing
  `export-traversal-symlink` mutant is established by reading the ten
  `selftest_case_H*` functions in the committed suite bytes (`bdbd18a3…`), not
  by executing the selftest.

## Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r40/RevC1Sandbox/` removed before yielding
(`rm -rf`), including the fixture clone, all work dirs and the doctored script.
Deliverables: this receipt plus the 30 byte-exact transcripts
`RevC1Sandbox.*.txt` beside it. No other lane/fleet file created, modified or
deleted; no mutating git/jj command run; the three accidental real-lane work
files (D5) were removed and the lane state verified restored.
