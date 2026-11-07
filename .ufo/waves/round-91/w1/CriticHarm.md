# CriticHarm — round 91 harm guard (attempt 1, wave 1)

Seat: CriticHarm (attack/critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`; freeze `53ab692a7b544c35141e2b19f7413cbdb767c1ad`;
C1 landing `8a1a00c639ba808a701d1f186aac9ebd0045deaa`; C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`;
landing receipts `bcbfbde63b83c9336e845001323b5c92419e526a` (HEAD; `master` = same commit).
Scratch `S=/fast/scratch/hyaku/kasegi-r91/CriticHarm` (deleted before yield; `TMPDIR=$S` on every run).
All commands below are re-runnable from the lane root; receipts in `CriticHarm-receipts/`.

Scope: five assigned harm probes. Findings are routed defects/qualifiers, not re-scoring.

## Verdict table

| # | Probe | Verdict | Impacted axis |
|---|---|---|---|
| 1 | depth:density at base vs tip | **NO HARM** | depth:density |
| 2 | capture-intake-gate inherits the new shapes | **NO HARM** (behaviour); G0 staleness is by design | coverage |
| 3 | False positives on the lane's own captures | **NO HARM** | coverage |
| 4 | Old capability commands at the C2 landing | **NO HARM** (pin movement only, no behaviour regression) | coverage |
| 5 | ReDoS on the two new regexes | **NO HARM** | coverage |

Routed qualifiers Q1–Q4 below; none blocks C1 or C2 on their frozen predicates.

## 1. depth:density — NO HARM

`SKILL.md` is byte-identical at base and at the C2 landing (and in the working tree):

```
7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552  base/SKILL.md
7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552  tip/SKILL.md
7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552  SKILL.md
```

`python3 -B corpus/instruments/density.py <SKILL.md> --label {base,tip}` (extracted by `git archive` into
`$S/base` and `$S/tip`): both print `mean dens 273.2` and `Total path-citation instances: 932 across 38
blocks` over 1251 lines; the full outputs differ on exactly one line, the `--label` header
(`density-diff.txt` = 1c1). `corpus/instruments/density.py` is unchanged base→tip
(sha256 `ee803726…` both). C1 edits `corpus/knowledge/triage-thresholds.md`, which the instrument never
reads, so the axis is untouched by construction and by measurement.

## 2. capture-intake-gate inheritance — NO HARM (behaviour); G0 FAIL is expected staleness

`capture-source.py` and `claim-package-check.py` are unchanged base→tip
(`0630d32b…` and `8b6f8493…`), so the round-90 counter is run without an instrument pin, as assigned.

Round-90 counter at the C2 landing (`r90-counter-at-c2-nopin.txt`, `r90-counter-at-c2-pin.txt`):

```
LIMB G0 FAIL shapes=12 missing=cloudfront-signed-cookie-signature extra=none
LIMB G1 pass plants=11 bad=none
LIMB G2 pass rc=3 kept=True
LIMB G3 pass clean=6 bad=none
LIMB G4 pass allowed_rc=0 written=True other_path_rc=3 never_allowed_rc=3
LIMB G5 pass rc=3 written=False
LIMB G6 pass rc=0 selftest normalize=ok deterministic=ok
LIMB P  pass sha256=0630d32b…          (capture-source.py, unchanged)
CAPABILITY-CHECK-RESULT fail rc=1
```

Classification: **expected, not a regression.** G0 is the derived-coverage limb added for M89-2
("the case list is derived, not hand-claimed"); it compares the counter's plant shapes with
`capture-secret-scan.patterns()` at `--rev`, so any scanner shape the counter does not plant makes it
fail. The round-90 counter is frozen at round 90: at its own landing `643ddb43` with pin `0630d32b` it
prints `G0 pass shapes=11 … CAPABILITY-CHECK-RESULT pass rc=0` (`r90-counter-own-landing.txt`). The
round-91 counter is the successor and plants the new shape (K4 `missing=none extra=none`, K7, K8
`clauses=13` all pass at the landing; the landing receipt `.ufo/waves/round-91/l1/c2-landing-r91.txt`
records three passing seeds, and `old-counter-r91-master.txt` reproduces K1–K8 pass at `master`, same
instrument bytes).

The gate itself does inherit both new shapes (structural: `intake_gate()` calls
`scan.scan_bytes(data, scan.patterns(), …)`; `patterns()` includes `CLOUD_PATTERNS`). Direct drive of the
landed gate over a loopback HTTP server, synthetic values in scratch only
(`intake-inherit.txt`, `intake-html-pre.txt`):

| input | rc | shape | written | value leaked |
|---|---|---|---|---|
| `Set-Cookie: CloudFront-Signature=<synthetic 58-char value>` (`--kind text`) | 3 | `cloudfront-signed-cookie-signature` | no | no |
| same shape in a `<pre>` block (`--kind html`) | 3 | `cloudfront-signed-cookie-signature` | no | no |
| `sv=…&skdutid=<uuid>&sig=<synthetic 48-char value>` (`--kind text`) | 3 | `azure-sas-signature` | no | no |
| same SAS in a `<pre>` block (`--kind html`) | 3 | `azure-sas-signature` | no | no |
| S134's 28-character documentation example | 0 | — | yes | — |
| clean page | 0 | — | yes | — |

So the gate refuses both new shapes before writing, keeps the value out of stdout/stderr, and does not
refuse the documentation example. No harm to the capability.

## 3. False positives on the lane's own captures — NO HARM

Landed scanner at the C2 landing (`scan-rev-c2.txt`, `scan-files-snapshots.txt`,
`scan-base-scanner-c2.txt`, `scan-tip-at-base.txt`, `scan-rev-head.txt`):

| invocation | scanned | hits | allowed | unused_allow | rc |
|---|---|---|---|---|---|
| tip scanner `--lane . --rev 1dd0723f` | 1734 | 0 | 20 | 0 | 0 |
| tip scanner `--lane . --rev bcbfbde` (HEAD, with landing receipts) | 1734 | 0 | 20 | 0 | 0 |
| tip scanner `--files` over all 113 `corpus/source-snapshots/**/*.txt` at 1dd0723f (repo-relative paths, from `git archive` in `$S`) | 113 | 0 | 5 | 14 | 0 |
| base scanner (95f24a54) `--lane . --rev 1dd0723f` | 1734 | 0 | 20 | 0 | 0 |
| tip scanner `--lane . --rev bb4309f` | 1731 | 0 | 20 | 0 | 0 |

New hits = 0; the new shape does not fire on any of the lane's 1734 capture-path files, on the 113
snapshot `.txt` files, or on the round-91 landing receipts (`.ufo/waves/round-91/l1/*` are outside
capture scope: no path component ends in `-receipts`, no `live-*` basename). The wave-1 tree at the
final scan (63 files, including this report and these receipts, plus concurrent seats' files)
scans clean: `scanned=63 hits=0 files=0 allowed=0 unused_allow=19 rc=0` (`w1-scan.txt`).

Note (pre-existing, not round-91): `--files` allowlist rows are keyed on the path string, so an
absolute-path invocation reports allowlisted matches as hits (4 on the same 113 files: `credential`,
`authorization`, two `cloudfront-signed-url-signature`). Repo-relative invocation is 0. Q4.

## 4. Old capability commands at the C2 landing — NO HARM (pin movement only)

Each SCORECARD `capture-secret-scan` command from row 307, run at `1dd0723f` (`--rev master` in the row
resolves to `bcbfbde`, same instrument; `old-counter-*.txt`):

| round | row form | result at 1dd0723f | classification |
|---|---|---|---|
| 87 | no pin | `K1–K5 pass`, `RESULT pass rc=0` | passes |
| 88 | no pin | `K1–K6 pass`, `RESULT pass rc=0` | passes |
| 89 | pin `95f24a54…` | `K1 FAIL instrument_sha256=89e283c6…`; `K2–K8 pass`; `RESULT fail rc=1` | **pin moving** — the instrument changed at 1dd0723; every behaviour limb passes |
| 89 | no pin (isolation) | `K1–K8 pass`, `RESULT pass rc=0` | confirms the only failure is the pin |
| 91 | pin `89e283c6…` at `--rev master` | `K1–K8 pass`, `RESULT pass rc=0` | passes |

No behaviour regression: K2 (oracle 2/2), K3 (rev scan hits=0, allowed=20, unused=0), K4
(`missing=none extra=none`, STS allow row refused), K6 (base discrimination), K7 (seeded plants), K8
(clause map) pass for every counter. The round-89 pin failure is exactly the documented "the pins hold
until the instrument next changes" (row 307) — the instrument's next change is this landing.

## 5. ReDoS — NO HARM

`redos.py` times the two new regexes individually on 14 adversarial inputs of ~1 MiB each
(`redos.txt`): repeated `CloudFront-Signature=` literals, a single 1 MiB value, name+39-char runs,
near-miss names, `\n`-join runs, lookbehind bait, `&ab=` chains with and without `sv=`, 20 long params,
`sig=`+39-char runs, repeated `sv=`, `&amp;`/`\u0026` chains, 7-letter-name chains.

Worst case **0.031 s** (all inputs ≤ 0.033 s; threshold 2.0 s). Both patterns are linear: the cookie
value class has no trailing constraint (no backtracking), and the Azure window is a bounded lazy
`{0,20}` over a separator-anchored value class that excludes `\`, so the alternatives cannot overlap.
No catastrophic backtracking.

## Routed qualifiers (not HARM to the frozen predicates)

- **Q1 — row 308 lacks the pin/staleness note.** The `capture-intake-gate` row documents the round-90
  counter with `--rev <landing>` and `--instrument-sha256 0630d32b` (capture-source.py). At any rev
  after 1dd0723 the counter fails G0 (new scanner shape unplanted) by design; the pin still passes
  because capture-source.py is unchanged. Row 307 carries "the pins hold until the instrument next
  changes"; row 308 does not. Smallest safe correction: add the same note (documentation only, future
  round). Re-runnable: `r90-counter-at-c2-pin.txt`.
- **Q2 — no committed gate-level plant for the two new shapes.** The round-91 counter proves the
  *scanner* shapes (K4/K7/K8); the gate's inheritance is proven structurally (single `patterns()` call)
  and by the re-runnable drive in `intake-inherit.txt`, not by a committed counter. Smallest safe
  correction: none required; round 92's capture-source.py successor can extend the round-90 counter's
  plant list.
- **Q3 — HTML `href` attributes are dropped before the gate sees bytes (pre-existing).** `html_to_text`
  strips all tags (`TAG_RE.sub("")`), so an Azure SAS that appears only in an `<a href>` is not in the
  converted bytes: the gate returns rc=0 with `snapshot_bytes=2` (`intake-html-href.txt`), while the
  scanner does report `azure-sas-signature` on the raw HTML. This is not a round-91 regression
  (capture-source.py is byte-identical base→tip, `0630d32b…`) and not a C2 defect (C2 binds the
  scanner); it is a real false-negative path for the `capture-intake-gate` capability, already the
  round-92 surface. Smallest safe correction: scan the raw bytes before conversion, or keep `href`
  URLs in the converted text. Re-runnable: serve `<a href="https://a.blob.core.windows.net/c/b?sv=2025-07-05&amp;skdutid=<uuid>&amp;sig=<40+ URL-safe chars>">x</a>`
  on a loopback port and run `capture-source.py --id T --url http://127.0.0.1:<port>/x --out <scratch>/o.txt --kind html`
  → rc=0, `snapshot_bytes=2`; the same URL inside `<pre>` → rc=3, `shape=azure-sas-signature`.
- **Q4 — `--files` allowlist path keying (pre-existing).** Absolute-path invocations turn allowlisted
  matches into hits; the L1's pre-commit scan should pass repo-relative paths.

## Files written

- `.ufo/waves/round-91/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-91/w1/CriticHarm-receipts/` — `density-base.txt`, `density-tip.txt`,
  `density-diff.txt`, `skill-md-sha256.txt`, `r90-counter-at-c2-nopin.txt`, `r90-counter-at-c2-pin.txt`,
  `r90-counter-own-landing.txt`, `intake-inherit.txt`, `intake-html-pre.txt`, `intake-html-href.txt`,
  `scan-rev-c2.txt`, `scan-files-snapshots.txt`, `scan-base-scanner-c2.txt`, `scan-tip-at-base.txt`,
  `scan-rev-head.txt`, `w1-scan.txt`, `old-counter-r87.txt`, `old-counter-r88.txt`,
  `old-counter-r89-pin.txt`, `old-counter-r89-nopin.txt`, `old-counter-r91-master.txt`, `redos.txt`,
  `scorecard-row-diff.txt`, `instrument-shas.txt`, `provenance.txt`

No credential-shaped value is written into any wave file: receipts carry only sha256 digests, limb
lines, HIT/summary lines and rc; fixture and plant values lived only in `$S` and are deleted with it.
Scratch `/fast/scratch/hyaku/kasegi-r91/CriticHarm` is removed before yield.
