# kasegi round 91 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

I am the closure judge for lane-round kasegi r91. I did not author the round. Inputs: report
`.ufo/reports/round-91/kasegi.md` (fleet repo), prompt `.ufo/prompts/kasegi-round-91.md`,
lane base `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`, lane tip `d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d`.
I ran every re-check in the scratch dir `/fast/scratch/hyaku/kasegi-r91-closure`, which I removed afterwards. The outputs I relied on are pasted below.

Driver digest (copied from `.ufo/watchdog.log`, which is mutable):

```
2026-11-07T04:45:36-03:00 launch kasegi round=91 pgid=387969 driver=hyaku-inline attempt=1
2026-11-07T05:53:09-03:00 complete kasegi round=91; hyaku-inline attempt=1
```

## 1. Conformance (step 1)

- **Report author.** `git log --format='%an %ae %H %ci' -- .ufo/reports/round-91/kasegi.md` (fleet repo) → `kasegi-shokunin kasegi@shokunin.local 0c123b9c71ff6e4ea816230564a6a7773f322898 2026-11-07 05:52:32 -0300`. The lane identity committed it, after the lane tip (05:51:16) and before the completion line (05:53:09). It lands last.
- **SHONEN.** The `## SHONEN` heading is present, with 4 lines, one per box. All four are `[~]` with pointers; none is `[x]`.
- **Ancestry.** `git cat-file -e` + `git merge-base --is-ancestor <h> master` → ok for all eight cited hashes: bb4309ff, 53ab692a, 8a1a00c6, 1dd0723f, bcbfbde6, 2bdde26b, d0bd4758, and labels rev e993fd18.
- **Lane state.** `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin` → `branch=master local=d0bd4758… remote=d0bd4758… ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` is empty. `git ls-remote origin refs/heads/master` → `d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d`.
- **Prompt.** 937 lines, committed by the lane identity at `df1202fc` (04:45:32, before launch). It carries the template sections §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN), §5 commit/push/L0, §6 hyaku addendum and §7 scratch discipline. Conformant.
- **P3 paths** (`git diff-tree --no-commit-id --name-only -r <c>`):
  - `8a1a00c6` → `corpus/knowledge/triage-thresholds.md` (1 path).
  - `1dd0723f` → `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py`.
  - Both match the frozen predicates.
- **Frozen pins** (sha256 of the bytes at the tip):
  - `knowledge-meter.py` = `be7a100b…b1c1`, identical at the freeze `53ab692a` and the tip.
  - `repair-map.tsv` = `55d50b66…0c8c0a7a`.
  - `capability-check.py` = `39deae67…37b6f0`.
  - The candidate scanner, the scanner landed at `1dd0723f` and the scanner at the tip all read `89e283c6…26d7`.
  - Every value equals `claims.json`, so C2 P2 holds.

## 2. Claims

### C1 — depth:verifiability, tranche 6 (pinned knowledge-scope meter 890/1883 → 891/1880)

**Re-measured.** I ran the frozen meter from committed bytes (`git show d0bd4758:.ufo/waves/round-91/c1/knowledge-meter.py`), with `--work` in scratch. It is a wave counter, not a registered gate.

```
--base-rev bb4309ff… --after-rev 8a1a00c6… --map …/repair-map.tsv --labels-rev e993fd18… --base-target 890/1883 --target 891/1880 --map-sha256 55d50b66…
KNOWLEDGE-METER base=890/1883 after=891/1880 … sites=6 labels=6 pinned=archive
LIMB M0 pass · M1 pass · M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0 · M4 pass bad=none
· M5 pass out_of_range=none · M9 pass rows=6 unbound=none · M10 pass labelled=6 mapped=6 unapplied=none unlabelled=none · M6 pass
KNOWLEDGE-METER-RESULT pass rc=0
--measure-rev bb4309ff → 890/1883 · 8a1a00c6 → 891/1880 · d0bd4758 → 947/1947 (tip; the admitted entry adds citations; not claimed)
do-nothing (--after-rev = base): LIMB M1 FAIL after=890/1883 · LIMB M3 FAIL bad_lines=6 → rc=1
```

**Plain independent check** (`git show` / `git diff`, not the lane counter):
- `round91-labels.tsv@e993fd18` has 6 rows. `repair-map.tsv` has 6 rows, one per labelled site.
- `git diff -U0 bb4309ff 8a1a00c6 -- corpus/knowledge/triage-thresholds.md` changes exactly lines 141, 142, 226, 368, 454 and 457. The file is 487 → 487 lines.
  - Lines 141, 142, 226 and 368: `MATCHES: <tok>` → `—`.
  - Line 454: first token → `corpus/knowledge/ev-model.md:13-25`; the second token is untouched.
  - Line 457: → `corpus/knowledge/claim-package-contract.md:9-16`.
  - Each change is the edit its label names.
- `git diff --stat 8a1a00c6 d0bd4758 -- triage-thresholds.md` is empty, so nothing changed after the landing.
- Semantic sample (I read the label claims against the cited entries at `8a1a00c6`):
  - `mission-control.md` mentions `--max` only at L17 (as a loop bound) and has no `stagger` at all, so the 141/142 ties were unsupported. Correct.
  - `claim-gates.md` contains `readJson` 0 times (226). Correct.
  - `ev-model.md:13-25` is the formula block plus the "Missing inputs print `UNKNOWN`… fail-closed" bullet (454). Correct.
  - `claim-package-contract.md:9-16` is the six-file table header, separator and six rows (457). Correct.

Reported vs observed: equal. **C1 verified.** The lane's own qualifier stands. Row 454's second token `SKILL.md:494-506` was never labelled and is not part of the claim, so it is routed below.

### C2 — coverage, capability extension `capture-secret-scan` (S133, S134)

**Re-measured** with the frozen counter from committed bytes, at a fresh seed and at the claim's seed 9191:

```
CAPABILITY-CHECK rev=1dd0723f… seed=77031  (and seed=9191: identical limbs)
LIMB K1 pass selftest_rc=0 instrument_sha256=89e283c6… gate_sha256=8b6f8493…
LIMB K2 pass · K3 pass summary=scanned=1734,hits=0 · K4 pass missing=none extra=none files_hits=2
LIMB K6 pass base_hits=16 new_caught_by_base=none · K7 pass missing=none extra=none · K8 pass clauses=13 failing=none · K5 pass rows=1
CAPABILITY-CHECK-RESULT pass rc=0
base bb4309ff, seed 77031: K4 FAIL (cloudfront-signed-cookie-signature / azure-sas-signature plants missing), K7 FAIL, K8 FAIL, K5 FAIL → rc=1
```

**Independent probe.** I wrote my own fixtures, not the lane's plants, and ran the scanner from `git archive <rev> corpus/instruments` with `--files`. The cookie value and the SAS sig are synthetic.

| fixture | base `bb4309ff` | landing `1dd0723f` |
|---|---|---|
| p1 `Set-Cookie: CloudFront-Signature=<48 url-safe chars>` | hits=0 rc=0 | `HIT shape=cloudfront-signed-cookie-signature` rc=1 |
| p2 `?sv=2025-07-05&skdutid=<guid>&sig=<43+%3D>` | hits=0 rc=0 | `HIT shape=azure-sas-signature` rc=1 |
| n1 `CloudFront-Signature=<28 chars>` (doc-length example) | hits=0 | hits=0 |
| n2 `?sv=…&abcdefgh=x&sig=…` (8-letter name ends the window) | hits=0 | hits=0 |
| n3 `xCloudFront-Signature=<48>` (letter-prefixed name) | hits=0 | hits=0 |

`--selftest` at the landing gives `SELFTEST-RESULT pass cases=53`. The output never printed a matched value.

Reported vs observed: equal. **C2 verified.** The lane's qualifiers are real but do not falsify the frozen predicate:
- K8 has no clause for FC1–FC4.
- SentinelCookie found bypasses F1–F3: colon-form dumps, cookie jars and quoted values.

### Integration anchor repair (M91-3 / R143; not a claim)

- The committed receipt `.ufo/waves/round-91/l1/quote-anchor-r91.txt` shows `checked=38 bad=4` against the C2 landing and `checked=57 bad=0 cites=228 out_of_range=0` after the re-anchor. I verified the evidence; I did not re-run the check.
- Spot read at the tip:
  - `capture-intake-gate.md:69` → `capture-secret-scan.py:94-95` reads "A row binds one exact matched value at one path, so a different value at the …". It resolves.
  - `:109` → `:81` reads "Known limits: GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed". It resolves.

### Gate evidence vs re-measurement

- C1 and C2 were re-measured with the frozen wave counters (not registered gates) and with independent plain checks.
- The anchor repair was evidence-verified only.
- I did not execute any registered lane gate (`source-recheck.py` and the like). Running the scanner on my own fixtures and its `--selftest` is a probe of the claimed capability over isolated scratch inputs.

### Harm guard

- `git diff bb4309ff d0bd4758 -- SCORECARD.md`:
  - The `capture-secret-scan` capability row is replaced by the frozen candidate row.
  - The Round-91 section is appended.
  - No axis score is lowered: depth:verifiability holds at 4 and coverage holds at 8.
- `git diff --stat bb4309ff d0bd4758 -- SKILL.md PROVINCE.md SHONEN.md` is empty, so depth:density reads 273.2 → 273.2 as reported. `corpus/QUALITY.md` +1 (R143); `corpus/SOURCES.md` +3 rows and 4 change-log lines.
- K3 at the landing gives hits=0 on the 1734 capture files at that revision, so no new false positive appeared in the corpus. K6 `new_caught_by_base=none` shows the round-89 shapes are kept.
- No harm found.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth (verifiability, C1) | improved | pinned meter re-run 890/1883 → 891/1880 rc=0 (do-nothing control fails); plain diff binds 6/6 edits to their labels; 4/4 sampled label premises hold |
| coverage (C2) | improved | counter pass at fresh seed 77031 and seed 9191, base fails K4/K7/K8; independent fixtures: cookie and skdutid SAS caught only at landing, three negatives clean |
| depth:density (guard) | unchanged | SKILL.md untouched |

## 4. Discernment spot-check (`corpus/lessons/round-91.md` § Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S134 CloudFront signed cookies, custom policy | admit (mined) | live https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-custom-policy.html, HTTP 200, 51673 B, 2026-11-07; snapshot `S134.txt:17,123` (sha256 `ddf45b80…49f1cc`, equal to the lesson) | agree | Live text has "a CloudFront signed cookie requires three name-value pairs" and "hashed, signed, and base64-encoded version of the JSON". It is the first-party definition of the cookie-borne signature the new shape detects. The 28-char doc example `dtKhpJ3a…NXQ_` (S134:123) is correctly kept as a negative plant below the 40-char floor. |
| S133 Microsoft Learn, user delegation SAS | admit (mined) | live https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas, HTTP 200, 118382 B; snapshot `S133.txt:177,571` (sha256 `56d858ac…786cd6`) | agree | Live text has "sduoid and skdutid fields are supported with version 2025-07-05 and later". The 7-letter field is exactly why the 2–6 name window missed the token. First-party, tier A. |
| S135 CloudFront signed cookies, canned policy | reject | live https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-canned-policy.html, HTTP 200, 36439 B | agree | Live text: "CloudFront-Expires, CloudFront-Signature, and". The signature cookie example `CloudFront-Signature=yXrSIgyQ…CA8_` has the same name and value form as S134, and `CloudFront-Expires` is a Unix time, not a credential. The page adds no detectable shape, and the flip (binding the shape to companion pairs) is apt. |
| S133 / S134 SOURCES.md rows (new, lines 145–146) | quote check | `S133.txt:571`, `S134.txt:17` (`sed -n`) | agree | S133: "The sduoid and skdutid fields are supported with version 2025-07-05 and later." (13 words). S134: "and a CloudFront signed cookie requires three name-value pairs." (10 words). Both are ≤25 words and present verbatim in the snapshot and live. The rows' line anchors and used-by cells resolve. |

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` gave `kasegi ok …/corpus/SOURCES.md`, rc=0. The six inherited `W04` duplicate-URL warnings remain (S028, S029, S072, S076, S080, S085); none are new. Registry rows by `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`: 132 at `bb4309ff`, 135 at `d0bd4758`, matching the report.

## 5. Trend verdicts

- **expansion: improved.** Two tier-A first-party sources were mined (S133, S134) and one rejected with a flip (S135); the registry went 132 → 135. One new knowledge entry was admitted. On the landed bytes, the capture scanner catches two edge classes it missed at base (cookie-borne signature, user-bound SAS), which my own fixtures confirm.
- **quality: improved.**
  - Six non-author-labelled citation sites carry exactly their labelled edits, and the meter went 890/1883 → 891/1880.
  - The r90 closure's routed defect 1 (completeness limb) is closed: M10 passes `labelled=6 mapped=6`.
  - The anchors the landing shifted were repaired (quote check bad=4 → 0, spot-read resolves), and R143 was added.
- **discernment: improved.** The outside spot-check agrees with the gate on both admits (S133, S134), the reject (S135) and both new-row quotes.

## 6. Routed defects (the lane fixes next round)

1. **Row 454's second token.** `triage-thresholds.md:454` still cites `SKILL.md:494-506`, which does not state the EV formula (ReviewC1Sites D1). It also routes D2/D3: rows 367/369/370 and SKILL.md token drift.
2. **M10 granularity.** It compares site sets, not (site, key) pairs (CriticClaims C1-F1). The counter successor should bind the pairs.
3. **C2 K8 gaps FC1–FC4.** The `\u0026`/`%26` cookie boundary, the preceding letter/digit/`_`, the generic `\n` join and the Azure 2-letter lower bound are implemented but have no clause or plant. Add plants or mutants that kill them.
4. **SentinelCookie F1–F3 bypasses:** colon-form dumps, cookie jars and quoted values. Fix them or list them as named known limits in the docstring and the entry.
5. **S135 capture lives in scratch only.** The row cites "scratch capture … not committed" with a sha. For a reject this is tolerable, because the live page re-opens. Commit rejected-source captures where the row cites line numbers, so the anchors resolve at closure (§Evidence standard).
6. **Carried from r90:**
   - `capture-source.py` `file://` status=None crash (M90-2).
   - A missing explicit `--allow` file loads as empty (C2-F4).
   - The r90 C2 counter clauses `line=`/whole-bytes/`--kind text` (C2-F1..F3).
   - All were declined in `claims.json` and are still open.
7. **Assimilation quarantine slice.** Its 7 rows were not hand-checked; carry it.
8. **Fleet root.** Untracked `f.txt` and `trail-ids.txt` predate this round and are not attributed to kasegi. Sibling credential material stays operator-owned (L0 `kasegi | round-89`).

Operator note: the SHONEN boxes are all `[~]`, with pointers to `corpus/lessons/round-47-verifier-spotcheck.md`
and `corpus/practice/curl-h1-1913733/report.md` / `curl-ibb-h1-1997312/report.md`. They look
checkable by a non-author promotion review. That review is operator-owned and was not done here.
