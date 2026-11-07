# MutC2Scanner — round 91, attempt 1: mutation probe of the landed C2 scanner change

Seat: mutation tester (leaf). Object: `corpus/instruments/capture-secret-scan.py`
at C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70` (sha256
`89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7`).
Judged against the frozen counter `.ufo/waves/round-91/c2/capability-check.py`
(sha256 `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`).

Verdict: **23 mutants, 13 killed, 10 survived, 0 inconclusive — at both seeds.**
Findings below are routed defects and qualifiers; the claim is not re-scored.

## Method

- `git clone --shared` of the lane into scratch, `git checkout` (inside the clone)
  `1dd0723…`; toplevel asserted; instrument sha256 re-checked against the pin.
- Per mutant: one or two exact-string replacements (each asserted to apply exactly
  once), `git -c user.name=mutant … commit`, counter run, `git reset --hard HEAD~1`.
- Frozen counter invoked **without** `--instrument-sha256` / `--gate-sha256`, so
  only behavioural limbs judge:

  ```
  python3 -B .ufo/waves/round-91/c2/capability-check.py --lane $S/lane-clone \
      --rev HEAD --work $S/work --seed {9191,1}
  ```

- Baseline on the restored landing bytes: `K1 K2 K3 K4 K6 K7 K8 K5` all pass,
  `CAPABILITY-CHECK-RESULT pass rc=0` at seeds 9191 and 1 (`baseline-seed*.txt`).
- The eight pre-freeze forgeries (`controls/c2-forgeries.py`, F1–F8) are excluded;
  all eight are recorded killed in `controls/c2-controls-r91.txt`.
- Credential hygiene: all fixtures lived in scratch only. Receipts carry diffs of
  the scanner regexes, `HIT shape=/path=`-free shape-set comparisons and limb
  lines — no fixture bytes. The landed scanner reports
  `scanned=31 hits=0 files=0` over the copied receipt set.

## Verdict table

Verdicts are identical at seed 9191 and seed 1; "killed by" lists every failing
limb (K1 selftest, K4 plant repo, K7 generated plants, K8 clause map, K3 lane scan).

| # | Mutant (round-91 point) | Verdict | Killed by | Survivor evidence / why it matters |
|---|---|---|---|---|
| M01 | `_PARAM` name window `{2,7}` → `{1,7}` | survived | — | **FN gap.** Plant `?sv=…&x=<v>&sig=<ASIG>`: pristine `none`, mutant `azure-sas-signature`. No fixture has a 1-letter intermediate name. |
| M02 | `_PARAM` name window `{2,7}` → `{2,9}` | killed | K1,K4,K7,K8 | extra `S018|azure`, `g6`-family (`live-n7`) |
| M03 | `_PARAM` name window `{2,7}` → `{3,7}` | killed | K1,K4,K7,K8 | missing `S014`, `E1`, `E3`, `live-g3`, `live-g6` (2-letter `sr` splits the chain) |
| M04 | `_PARAM` repeat cap `{0,20}?` → `{0,1}?` | killed | K1,K4,K7,K8 | missing `S014`, `live-g6` |
| M05 | `_PARAM` repetition lazy → greedy (`{0,20}?`→`{0,20}`) | survived | — | **Equivalent (argument + 5 968-case differential, 0 divergences).** Lazy and greedy both enumerate counts 0..20 in opposite order; every intermediate value stops at the separator, so the accepted language and the matched span are identical; `scan_bytes` only consumes shape, start line and whole-match hash, all unchanged. |
| M06 | `_PARAM` name class `[A-Za-z]` → `[A-Za-z0-9]` | survived | — | **FN gap.** Plant `?sv=…&x1=<v>&sig=<ASIG>`: pristine `none`, mutant `azure-sas-signature`. |
| M07 | `_PARAM` value class `[^&\s"'<>\\]*` → `[^&\s]*` | survived | — | **FP gap.** Plant `?sv=…&aa="&sig=<ASIG>`: pristine `none`, mutant `azure-sas-signature` (quote no longer terminates the value). 67 differential divergences, none in the frozen corpora. |
| M08 | `_CK_LB` drops `(?<=%26)` | survived | — | **FN gap, asymmetric with Azure.** Plant `x?%26CloudFront-Signature=<CKSIG>`: pristine hits, mutant `none`. `_LB` (Azure) keeps `%26`; the round-91 cookie boundary copy does not have a `%26` fixture, while the Azure `\u0026`/`&amp;` forms do. |
| M09 | `_CK_LB` left lookbehind `(?<![A-Za-z0-9_-])` → `(?<![A-Za-z0-9_])` | killed | K1,K4,K7,K8 | extra `S020`, `live-n5` (`X-` prefix) |
| M10 | same lookbehind → `(?<![A-Za-z])` | killed | K1,K4,K7,K8 | extra `S020`, `live-n5` |
| M11 | `_CK_LB` JSON join `(?<=\\n)` → `(?<=\\r\\n)` | killed | K1,K4,K8 | missing `E4.json` |
| M12 | cookie entry boundary `_CK_LB` → `_CF_LB` (reuse the URL boundary) | killed | K1,K4,K8 | missing `E4.json`; also re-admits `X-` in selftest |
| M13 | cookie class loses `-` | killed | K1,K4,K8 | missing `S015`, `E4`, `live-h` |
| M14 | cookie class gains `+` | survived | — | **FP gap.** Plant `CloudFront-Signature=` + 20 `A` + `+` + 19 `B`: pristine `none`, mutant hits. `+` is not in the CloudFront URL-safe set. |
| M15 | cookie floor `{40,}` → `{41,}` | killed | K4,K8 | missing `S022` (40-char boundary) |
| M16 | cookie floor `{40,}` → `{32,}` | killed | K4,K7,K8 | extra `S021` (39-char), `live-n6` |
| M17 | cookie floor `{40,}` → `{40}` (exact) | survived | — | **Equivalent modulo matched span.** A 40-char prefix still matches, so shape sets, counts and rc are unchanged (0/5 968 divergences; 0/46 counter-run cases). Difference: `m.group(0)` is truncated, so an allowlist row keyed on a longer cookie value would stop matching — the landed allowlist has no cookie/azure rows (distinct shapes: `authorization`, `cloudfront-signed-url-signature`, `credential`). Not exercised, not currently observable. |
| M18 | cookie literal name lowercased | killed | K1,K4,K7,K8 | missing every cookie plant, extra lowercase `live-n4` |
| M19 | cookie literal `=` → `\s*=` | survived | — | **FP gap.** Plant `CloudFront-Signature =<CKSIG>` (space before `=`): pristine `none`, mutant hits. 76 differential divergences, none in the frozen corpora. |
| M20 | cookie literal `-` → `[-_]` | survived | — | **FP gap.** Plant `CloudFront_Signature=<CKSIG>`: pristine `none`, mutant hits. |
| M21 | cookie shape renamed `cloudfront-signed-cookie` | killed | K1,K4,K7,K8 | name mismatch everywhere (K5 is unaffected: it reads SCORECARD, not the shape) |
| M22 | cookie entry removed from `CLOUD_PATTERNS` | killed | K1,K4,K7,K8 | missing all five cookie plants |
| M23 | cookie entry moved before the CloudFront-URL entry | survived | — | **Equivalent (0/5 968 + 0/46 divergences).** `scan_bytes` breaks per *shape*; the HIT set, counts and rc are order-free. Only raw stdout HIT-line order changes, which no limb and no allowlist row consumes. |

## Routed defects (quality of the frozen detector, not of the claim)

The counter kills every mutation that changes a *covered* dimension. The ten
survivors are coverage gaps of the frozen predicate. Each below is a re-runnable
plant that would kill its mutant if added to `PLANTS` (+ `NEW_EXPECT`/`CLAUSES`),
using run-time-drawn values in the K7 style so no literal secret-shaped value is
needed in the wave file.

1. **`_PARAM` lower bound is untested (M01).** One-letter intermediate parameter
   between `sv` and `sig` is invisible to the frozen plants. Plant shape:
   `https://acct.blob.core.windows.net/c/b.txt?sv=<SV>&x=<n>&sig=<ASIG>` →
   expect `azure-sas-signature`.
2. **`_PARAM` name class does not reject digits (M06).** Same shape with a
   digit-bearing name (`x1=<n>`) → expect hit.
3. **`_PARAM` value class is untested against a quote-terminated value (M07).**
   `…?sv=<SV>&aa="&sig=<ASIG>` → expect **no** hit (mutant hits).
4. **The cookie `%26` join alternative has no fixture (M08),** even though the
   Azure boundary keeps the same alternative and the counter carries Azure
   `\u0026`/`&amp;` fixtures. `x?%26CloudFront-Signature=<CKSIG>` → expect hit.
5. **Over-broad cookie class is unpoliced (M14).** A value containing `+` must
   not hit; no negative plant exists for it.
6. **Whitespace tolerance around `=` is unpoliced (M19).** `CloudFront-Signature`
   + space + `=` + value must not hit.
7. **A second spelling of the cookie name is unpoliced (M20).** Underscore
   spelling must not hit.
8. **Floor equality is covered only at 40 and 39 (M15/M16 killed),** which is
   sufficient; no action.
9. **Equivalences (M05, M17, M23)** are not defects. M17 is worth a note: the
   exact-floor mutant is invisible only because no allowlist row keys a cookie
   match; if such a row is ever added, `{40,}` vs `{40}` becomes observable.

Ordering of the gaps by risk: M08 (a real S133/S134-shaped capture form silently
missed) > M01/M06 (Azure user-delegation variants) > M19/M20 (scanner false
positives, cheap noise in receipts) > M07/M14.

## Evidence

Files under `.ufo/waves/round-91/w1/MutC2Scanner-receipts/`:

- `M01…M23.diff` — 23 unique-hunk diffs against the landed instrument.
- `mutants.tsv` — mutant, description, prediction, verdict, failing limbs, commit, plant.
- `mutant-runs.tsv` — per seed: rc, failing limbs, mutant commit sha.
- `survivor-plants.tsv` — pristine vs mutant shape sets per survivor plant.
- `differential.tsv` — pristine-vs-mutant divergences over the 5 968-case corpus.
- `corpus.txt` — corpus size line (`5 968` = systematic 13×4×4×9×2 + Azure cross
  product 4×7×4×2, plus 4×500 random cases, seeds 9191, 1, 2, 3).
- `baseline-seed9191.txt`, `baseline-seed1.txt` — frozen-counter runs on the
  restored bytes: `CAPABILITY-CHECK-RESULT pass rc=0`.
- `restoration.txt` — post-run restoration evidence.

Restoration: after all 23 committed mutants, the clone worktree instrument is
byte-identical to the pin (`sha256 89e283c6…26d7`), `HEAD` is back at
`1dd0723f…adb70`, `git status --porcelain` is empty, and the counter still exits 0
at both seeds. The lane tree was never written; the clone lives only in scratch.

Scratch `/fast/scratch/hyaku/kasegi-r91/MutC2Scanner` held the clone, mutants,
fixtures and probe staging; it has been deleted before this report was yielded
(`rm -rf`, verified gone). No tool was installed or upgraded.
