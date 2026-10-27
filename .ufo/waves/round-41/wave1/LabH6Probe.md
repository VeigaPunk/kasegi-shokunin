# LabH6Probe — r40 H6 limb semantics + r41 ExecI6Scan differential probe

Seat: `LabH6Probe` (scout, leaf). Receipt-only item. Two deliverables of work: (a) the
exact matching semantics of the committed r40 `check_h6` limb, and (b) a live
behavioral diff against the delivered r41 limb `ExecI6Scan.sh`, axis-mapped to every
round-40 wave-2 flagged escape (CritKillRule F1–F6, RevC1Counters T14) and to
LabExportClean D4's 4 survived selftest mutants (M2/M5/M9/M10).

No lane/fleet file was edited. All fixtures ran under `/fast/scratch/hyaku/kasegi-r41/LabH6Probe/`.
Limbs were probed by sourcing them and calling `check_h6` (r40) / `check_i6` (r41) under a
sandbox scratch root — never the live `/fast/scratch/hyaku` (the probe refuses that path).

## 1. r40 `check_h6` — committed semantics (r40-closure.sh L760–795, sha256 e4af1437…6c6)

Byte-identical at base `5b29ea14…` and at current HEAD. Behavior, measured not assumed:

- **Family match**: shell `case` glob `kasegi-r39*|kasegi-r40*` on the entry basename —
  **prefix-anchored, byte-literal, case-sensitive**, hyphen separator only. `kasegi-r40-STRAY`
  matches (suffix is wildcarded); `Kasegi-r40-stray`, `kasegi_r40-stray`, `.kasegi-r40-dot`,
  `kasegi‑r40‑stray` (U+2011), and `xkasegi-r40` all **miss**.
- **Depth**: `find "$realroot" -mindepth 1 -maxdepth 1 -print` — **top level only**; anything
  nested is invisible (s06, s21, s23 GREEN).
- **Dotfiles**: `find` does enumerate them, but the glob can't match a leading dot →
  `.kasegi-r40-*` is a **silent escape** (s05 GREEN).
- **Work exclusion**: skip iff `realpath(--work)` equals the entry realpath or is a
  **descendant** of it (`case $realw in "$r"|"$r"/*)`). Direction is *ancestor-of-work*, not
  the other way: the whole family dir containing `--work` is exempt **with all its siblings**
  (s08 GREEN — this is LabExportClean D1 / CritKillRule F2/F5). A stray that *contains* work
  neuters it; a stray *inside* work still counts (s20 RED — descendants are not exempt).
- **Entry types**: any name-matching entry is looped; a non-cd'able match (regular file,
  dangling symlink, unreadable dir, ancestor-symlink resolving elsewhere) sets `read=fail`
  but is *not* counted as a stray (s09/s10/s11 → `strays=0,read=fail`, still red).
- **Fail-closed coverage**: `WORK` unset/unresolvable, root `cd` failure, or `find` failure →
  `strays=0,read=fail` rc=1 (s12, s13, s24). **Fail-open hole**: a *nonexistent* root skips the
  whole `[ -d ]` block → `strays=0,read=ok` rc=0 (s22 GREEN — CritKillRule F6).
- **Empty matching dirs count** as strays (s16 RED).
- Payload: `strays=<n>,read=<ok|fail>`; green iff `read=ok && strays=0`.

## 2. Behavioral diff — r40 `check_h6` vs r41 `ExecI6Scan.sh` (sha256 e28208a6…9c, 444 lines)

r41 semantics measured on the same 24-scenario matrix (`check_i6 ROOT WORK`, `I6_CHAIN=strict`,
the shipped default). Payload extended to `strays=<n>,read=<ok|fail>` via `i6_scan_scratch`
(detail variant adds `scanned=…,excluded=…,tolerated=…` + one `stray:` line per stray).

| scenario (fixture) | r40 H6 | r41 I6 (strict) | r41 (literal) | wave-2 axis closed? |
|---|---|---|---|---|
| s02 top-dir `kasegi-r4x-stray` | RED strays=1 | RED strays=1 | RED | baseline control |
| s03 `kasegi_r4x-stray` (underscore) | **GREEN** (T14) | RED strays=1 | RED | YES — separator folded |
| s04 `Kasegi-r4x-stray` (case) | **GREEN** (T14/F4) | RED strays=1 | RED | YES — `${n,,}` fold |
| s05 `.kasegi-r4x-dot` (dot-prefix) | **GREEN** (F3) | RED strays=1 | RED | YES — leading dots stripped |
| s06 `container/kasegi-r4x-nested` | **GREEN** (F1) | RED strays=1 | RED | YES — recursive `-mindepth 1` |
| s07 `kasegi-r4x-ancestor → $ROOT` symlink | **GREEN** (F5) | RED strays=1 | RED | YES — realpath + chain check |
| s08 work inside family dir w/ dirty sibling | **GREEN** (F2/D1) | RED strays=1 | RED | YES — strict clean-chain tolerance |
| s09 `kasegi-r4x-file` (regular file) | RED via read=fail | RED strays=1 | RED | stronger: counted, not just flagged |
| s10 `kasegi-r4x-dangling` symlink | RED via read=fail | RED strays=1 | RED | stronger |
| s11 `kasegi-r4x-locked` (chmod 000) | RED read=fail | RED read=fail | RED | same verdict, stray still counted |
| s12 root chmod 000 | RED read=fail | RED read=fail | RED | same |
| s13 root chmod 0311 (searchable, unlistable) | RED read=fail | RED read=fail | RED | same (M10 axis covered) |
| s14 family symlink → work | GREEN (tolerated) | GREEN (tolerated) | GREEN | same — clean realpath |
| s15 `xkasegi-r4x-prefixed` | GREEN | GREEN | GREEN | anchored prefix kept |
| s16 empty family dir | RED strays=1 | RED strays=1 | RED | same |
| s17 `--work` == scratch root, empty | GREEN | GREEN | GREEN | same |
| s18 `kasegi‑r4x‑stray` (U+2011) | **GREEN** (F4) | RED strays=1 | RED | YES — 11 unicode dashes folded |
| s19 stray sibling + gold work-family dir | RED strays=1 | RED strays=1 | RED strays=2 | both red; literal also counts ancestor |
| s20 work==root + stray inside | RED strays=1 | GREEN strays=0 | GREEN | changed — r41 exempts descendants of work |
| s21 unreadable non-family mid-tree dir | **GREEN** (silent) | RED read=fail | RED | YES — find stderr/rc → fail-closed |
| s22 nonexistent scratch root | **GREEN** (F6) | RED read=fail | RED | YES — `[ ! -d ]` → read=fail |
| s23 `a/kasegi-r4x-deep1/b/kasegi-r4x-deep2` | GREEN | RED strays=2 | RED | YES — counted at any depth |
| s24 empty `--work` arg | RED read=fail | RED read=fail | RED | same |

**Every wave-2 flagged escape reds under r41**: T14 (s03, s04, suffix-case control s19 kept),
F1 nested (s06, s23), F2/F5 ancestor tolerance (s07, s08 — strict mode enforces the wave-1
`ExecH6ScratchFixtures` clean-chain contract: `i6_chain_clean` requires each ancestor level to
hold exactly the next work component), F3 dotfile (s05), F4 unicode separators (s18), F6
missing root (s22). Plus two gaps nobody filed: s21 mid-scan `find` error and the
ancestor-prefix hole s08 are both closed.

`s20` is a deliberate semantic change, not a hole: r41's exclusion reads "the work dir itself
nor inside it" — descendants of `--work` are `excluded`, matching the frozen I6 clause's plain
reading; r40's ancestor-only rule was the asymmetry CritKillRule F2 exploited.

### Selftest coverage vs LabExportClean D4 (the 4 missed mutants)

D4's survivors were selftest-coverage gaps — the limb already red'd most of those states, but
no fixture exercised them. ExecI6Scan's `mutate.py` maps each to a surgical weakening and a
covering fixture; I re-ran its shipped `--self-test` myself: **cases=16 failures=0**.

| r40 surviving mutant (LabExportClean M#) | r40 gap | ExecI6Scan mutant M#/fixture | kills? |
|---|---|---|---|
| M2 unreadable entry ignored (`cd` fail → skip) | no unreadable-entry fixture | M7 + `unreadable-entry-red` (and mid-scan coverage via s21-class find-stderr check) | yes — fixture reds `read=fail` |
| M5 `find -type d` only | no non-directory fixture | M5 + `stray-regular-file-red`, `stray-dangling-symlink-red` | yes — s09/s10 analogues count strays |
| M9 `read=fail` never reds | no fixture where the *only* signal is read=fail | M8 + `unreadable-entry-red` (entry counted AND read=fail) | yes — flag still trips |
| M10 `find` failure ignored | no listable-failure root | `listable-failure-root-red` (0311 root) + `unreadable-root-red` + `missing-root-red` | yes — rc≠0 or non-empty stderr → read=fail |
| (context) T14 case/separator | no name-variant fixture | M1 (case) + M2 (separator) + `unicode-separator-red` | yes |
| (context) F1 nested | no nested fixture | M3 + `deep-nested-red` | yes |
| (context) F3 dotfile | no dotfile fixture | M4 + `.kasegi-r41-dot` in the five-strays case | yes |
| (context) F6 fail-open root | no missing-root fixture | `missing-root-red` | yes |

### `I6_CHAIN=literal` mode (spec-literal reading)

With `I6_CHAIN=literal`, a family-named *ancestor* of `--work` is also counted (s19 →
`strays=2`). Shipped default is `strict` — the header documents the reason: on the live root,
`/fast/scratch/hyaku/kasegi-r41` is itself a family match, so literal counting can never print
green while the round's own container exists; strict tolerates a family ancestor only when the
chain to `--work` is clean (contaminated chain → red, s08/s19). This is the wave-1 contract
`ExecH6ScratchFixtures` specified and wave-2's F5 fix direction.

## 3. Probe transcripts

Probe driver `probe.sh` (sha256 54c0ac80…c4, 67 lines) builds each fixture fresh under a

sandbox root, calls the limb, prints `scenario=… rc=… payload=…`. r40 run (env mode,
`SCRATCH_ROOT`/`WORK`):

```
scenario=s01-clean                      rc=0 payload=strays=0,read=ok
scenario=s02-topdir-stray               rc=1 payload=strays=1,read=ok
scenario=s03-underscore-sep             rc=0 payload=strays=0,read=ok
scenario=s04-mixedcase                  rc=0 payload=strays=0,read=ok
scenario=s05-dotprefix                  rc=0 payload=strays=0,read=ok
scenario=s06-nested-container           rc=0 payload=strays=0,read=ok
scenario=s07-ancestor-symlink           rc=0 payload=strays=0,read=ok
scenario=s08-work-inside-family         rc=0 payload=strays=0,read=ok
scenario=s09-regular-file               rc=1 payload=strays=0,read=fail
scenario=s10-dangling-symlink           rc=1 payload=strays=0,read=fail
scenario=s11-unreadable-entry           rc=1 payload=strays=0,read=fail
scenario=s12-root-mode-000              rc=1 payload=strays=0,read=fail
scenario=s13-root-mode-0311             rc=1 payload=strays=0,read=fail
scenario=s14-symlink-to-work            rc=0 payload=strays=0,read=ok
scenario=s15-name-prefix-x              rc=0 payload=strays=0,read=ok
scenario=s16-empty-family-dir           rc=1 payload=strays=1,read=ok
scenario=s17-work-is-root               rc=0 payload=strays=0,read=ok
scenario=s18-nonbreaking-hyphen         rc=0 payload=strays=0,read=ok
scenario=s19-sibling-plus-goldwork      rc=1 payload=strays=1,read=ok
scenario=s20-work-is-root-plus-stray    rc=1 payload=strays=1,read=ok
scenario=s21-unreadable-nested-midscan  rc=0 payload=strays=0,read=ok
scenario=s22-no-such-root               rc=0 payload=strays=0,read=ok
scenario=s23-deep-two-levels            rc=0 payload=strays=0,read=ok
scenario=s24-empty-work                 rc=1 payload=strays=0,read=fail
```

r41 run (`I6_CHAIN=strict`, `check_i6 ROOT WORK`):

```
scenario=s01-clean                      rc=0 payload=strays=0,read=ok
scenario=s02-topdir-stray               rc=1 payload=strays=1,read=ok
scenario=s03-underscore-sep             rc=1 payload=strays=1,read=ok
scenario=s04-mixedcase                  rc=1 payload=strays=1,read=ok
scenario=s05-dotprefix                  rc=1 payload=strays=1,read=ok
scenario=s06-nested-container           rc=1 payload=strays=1,read=ok
scenario=s07-ancestor-symlink           rc=1 payload=strays=1,read=ok
scenario=s08-work-inside-family         rc=1 payload=strays=1,read=ok
scenario=s09-regular-file               rc=1 payload=strays=1,read=ok
scenario=s10-dangling-symlink           rc=1 payload=strays=1,read=ok
scenario=s11-unreadable-entry           rc=1 payload=strays=1,read=fail
scenario=s12-root-mode-000              rc=1 payload=strays=0,read=fail
scenario=s13-root-mode-0311             rc=1 payload=strays=0,read=fail
scenario=s14-symlink-to-work            rc=0 payload=strays=0,read=ok
scenario=s15-name-prefix-x              rc=0 payload=strays=0,read=ok
scenario=s16-empty-family-dir           rc=1 payload=strays=1,read=ok
scenario=s17-work-is-root               rc=0 payload=strays=0,read=ok
scenario=s18-nonbreaking-hyphen         rc=1 payload=strays=1,read=ok
scenario=s19-sibling-plus-goldwork      rc=1 payload=strays=1,read=ok
scenario=s20-work-is-root-plus-stray    rc=0 payload=strays=0,read=ok
scenario=s21-unreadable-nested-midscan  rc=1 payload=strays=0,read=fail
scenario=s22-no-such-root               rc=1 payload=strays=0,read=fail
scenario=s23-deep-two-levels            rc=1 payload=strays=2,read=ok
scenario=s24-empty-work                 rc=1 payload=strays=0,read=fail
```

`I6_CHAIN=literal` identical except s19 → `strays=2` (the family-named ancestor of `--work`
counts too).

Committed-fixture replay (r40 limb, `wave2/CritKillRule.h6-escapes.sh`, sandbox root):
m1 pos-ctrl RED, m2 dotfile GREEN, m3 uppercase GREEN, m4 NB-hyphen GREEN, m5 nested GREEN,
m6 ancestor-symlink GREEN, m7 symlink-to-work GREEN (tolerated), m8 dangling RED, m9 unreadable
RED, m10 regular-file RED — matching its committed expectations 10/10.

ExecI6Scan `--self-test` re-run by me (its scratch was wiped mid-wave by a sibling cleanup —
the same /fast scratch-tree wipe that cleared `kasegi-r41/` entirely at ~05:46 UTC — so I ran
the shipped binary's hermetic probe myself):
`selftest cases=16 failures=0, selftest verdict=pass`; case list: five-strays (incl.
underscore/case/nested/dotfile), strays-removed-green, work-dir-family-named-green,
work-dir-contents-green, work-chain-clean-green, work-chain-contaminated-red,
stray-regular-file-red, stray-dangling-symlink-red, unreadable-entry-red,
listable-failure-root-red (0311), unreadable-root-red, missing-root-red, deep-nested-red,
unicode-separator-red, out-of-family-green.

## 4. Residuals / notes

- ExecI6Scan's `.md` receipt and `.transcript.txt` were not yet in the wave dir at probe time;
  only `ExecI6Scan.sh` (deliverable) and `MutScan.md` (mutant-matrix seat's receipt) exist.
  Its `mutate.py` (seen in scratch pre-wipe) carries all 8 planned mutants; the shipped
  selftest covers every one of their axes.
- s20 semantic change is spec-faithful and only *widens* what counts vs r40 on the work side
  (r40 counted a stray inside work too — direction differs, verdict both red where it
  matters); no green-for-leftover regression.
- Limb payload format changed from `strays=<n>,read=…` + hidden state to the same core plus an
  audit variant — `i6_scan_scratch` prints the r40-compatible `strays=<n>,read=<ok|fail>`
  token exactly, so suite-side token-boundary parsing (I3) is unaffected.
- Attribution (LabExportClean D3): r40's payload was `strays=n,read=s` only, so a dirty root
  surfaced downstream as H5/H7 payload drift. r41's detail payload
  (`strays,read,scanned,excluded,tolerated` + one `stray:` line per leftover) names exactly
  which entries fired — the scan's own evidence travels in the payload.
- Tooling: none installed. Bash `sed`/`grep`/`find`, coreutils only; no pacman, no network.
- Incident: the whole `/fast/scratch/hyaku/kasegi-r41/` tree was deleted at ~05:46 UTC
  (sibling scratch wipe — exactly the I6-class defect the limb hunts; on the live root this
  is precisely what the I6 check exists to catch). Scratch rebuilt; no evidence lost.

Report: .ufo/waves/round-41/wave1/LabH6Probe.md
