# kasegi round 89 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closure judge for lane-round kasegi r89. Did not author the round. Inputs: report
`.ufo/reports/round-89/kasegi.md` (fleet repo), prompt `.ufo/prompts/kasegi-round-89.md`,
lane base `090a46f89932324787e00ca20b1007f893934c9a`, lane tip `02b6d88f1c059e2f881fd07c73834f502b4f212d`.
Scratch for re-runs: `/fast/scratch/hyaku/closure-kasegi-r89` (removed after; every output
needed is pasted below).

Driver digest (copied from `.ufo/watchdog.log`, mutable):

- `2026-11-07T02:10:38-03:00 launch kasegi round=89 pgid=2629049 driver=hyaku-inline attempt=1`
- `2026-11-07T03:42:08-03:00 complete kasegi round=89; hyaku-inline attempt=1`

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-89/kasegi.md` | `kasegi-shokunin <kasegi@shokunin.local> 1b173088b0505caf35d0d66d66f4dee0726b0cf1 2026-11-07 03:41:39 -0300` | pass |
| report lands last | `git -C kasegi-shokunin log -1 --format=%ci 02b6d88f` | `2026-11-07 03:40:29 -0300` (before the report commit, before `complete`) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | pass |
| cited hashes exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for `090a46f8`, `94573d25`, `eb5f0df8`, `c61c5586`, `50e2632e`, `b9fcf005`, `02b6d88f` | all 7 `OK`; `git rev-parse HEAD master` both `02b6d88f…` | pass |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `state branch=master local=02b6d88f… remote=02b6d88f… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `0`; `02b6d88f1c059e2f881fd07c73834f502b4f212d refs/heads/master` | pass |
| prompt carries the template contract | `grep -nE 'SHONEN\|write scope\|MISSION.md\|L0\|Push scope\|AgentSwarm\|Frontier step\|reports/round-89'` over the prompt (937 lines, committed `17eed2c8` by kasegi-shokunin) | mission/axes binding (l.5-24), §2b frontier step (l.42), §3 L2 floor batched AgentSwarm (l.80-82), report path + SHONEN + hash citation (l.101-118), commit/push scope/L0 (l.131-139), write scope (l.448-450), commit order (l.462-474) | pass |

Report is a real report (work, evidence pointers, landed commits tied to `LOG.md`, resolvable
hashes): status `ok`. No conformance defect found.

## 2. Claims

### C1 — depth:verifiability, sibling-entry repoint tranche 4 (777/1798 → 785/1797)

Re-measured (counter, not a registered gate) in a fresh `git clone --no-hardlinks` of the lane
checked out at `eb5f0df8`, exactly the reported method:

```
$ python3 -B .ufo/waves/round-89/c1/knowledge-meter.py --lane <clone@eb5f0df8> --base-rev 090a46f8… --after-rev eb5f0df8… --map .ufo/waves/round-89/c1/repair-map.json --labels .ufo/waves/round-89/c1/labels.tsv --target 785/1797 --map-sha256 c29f4c21…e2ec --labels-sha256 8aed5bde…050d --work <scratch>
KNOWLEDGE-METER base=777/1798 after=785/1797 target=785/1797 keys=9 mirror_absent=True
LIMB M1 pass … M2 pass removed=9 keys=9 stray_removed=0 stray_added=0 unrepaired=0 … M3 pass … M4 pass … M9 pass labels=9 unbound=none … M5 pass … M7 pass … M6 pass
KNOWLEDGE-METER-RESULT pass rc=0
```

Plain checks:

- `git diff --stat 94573d25 eb5f0df8` → `corpus/knowledge/triage-thresholds.md | 18 +++++++++---------`, 1 file, 9/9 lines.
- The five re-anchors read at `eb5f0df8`: `claim-gates.md:35` = the `decision_sha256` regex; `:36-37` = the three-way `head_sha256` binding; `:78-80` = the not-claimable heuristics; `:81-85` = the prior-submission guard; `claim-package-contract.md:52-53` = the four `claim_review.hard_gates`. Each new range supports its row. Agree 5/5.
- `sha256sum` of map and labels equal the pinned `c29f4c21…` / `8aed5bde…`.

Verdict: **verified (re-measured)**. Score 4 held as declared → axis `improved` (the measured
move is real; no score change claimed).

Finding (defect, status-neutral): the meter's absolute readings depend on the `--lane` tree it
classifies against, not only on the measured revision. Same revisions, different `--lane`:

```
--lane <clone@eb5f0df8> --measure-rev b9fcf005  → rate=812/1827
--lane <live lane @02b6d88f> --measure-rev b9fcf005 → rate=815/1827
--lane <live lane> --measure-rev 090a46f8 → 778/1798 ; --measure-rev eb5f0df8 → 786/1797
```

The report's and `tip-reading-r89.txt`'s "814/1827 at `b9fcf005`" reproduces in neither
environment. The C1 delta (+8 resolving, −1 distinct) is invariant across both, so the claim
stands; the tip reading is not a re-derivable number as filed.

### C2 — coverage, capability extension of `capture-secret-scan` (CloudFront signed URLs; Azure `\u0026`/`%26` boundary)

The claim rests on a lane-owned gate; per §Gate standard I did not execute the scanner's CLI or
self-test. Evidence-verified: landing receipt `.ufo/waves/round-89/l1/c2-landing-r89.txt` at
`c61c5586` (K1 `selftest_rc=0`, K2–K8 pass, `CAPABILITY-CHECK-RESULT pass rc=0`, K3 tree scan
`hits=0 allowed=20 unused_allow=0`, P3 `changed=3 outside=0 verdict=PASS`); live `sha256sum`
of scanner `95f24a54…20ec` and allowlist `76245bba…1985` equal the receipt's pins.

Re-measured with a plain probe of my own: imported only `CLOUD_PATTERNS` from
`git show <rev>:corpus/instruments/capture-secret-scan.py` at base and landing and matched
committed snapshots plus closure-authored fixtures (not lane plants):

```
grep -c cloudfront-signed-url-signature: eb5f0df8 → 0 ; c61c5586 → 6
eb5f0df8 S128 [] | S130 [] | cf-mine-canned [] | cf-mine-json-kpi-first [] | cf-mine-no-kpi [] | azure-mine-u0026-mid []
c61c5586 S128 [cloudfront] | S130 [cloudfront] | cf-mine-canned [cloudfront] | cf-mine-json-kpi-first [cloudfront] | cf-mine-no-kpi [] | azure-mine-u0026-mid [azure-sas-signature]
```

The new class fires on canned and custom, `&`/`\u0026`, either order; not on `Signature=`
without `Key-Pair-Id`; the r88 F1 fix (Azure SAS starting after a mid-query `\u0026`) holds.
Real-world: the two sibling lines the report names are tracked and carry both parameters
(`git ls-files --error-unmatch` ok; `Key-Pair-Id=` 1, `Signature=` 1 on each line). Verdict:
**verified (re-measured + evidence-verified)** → coverage `improved`. Lane's own qualifier
M89-2 (K8 clause map overstated) accepted as reported, not a falsification.

### Harm guard

- `git diff 090a46f8 02b6d88f -- SCORECARD.md`: one capability-row edit (`capture-secret-scan` extended) and the appended Round 89 section; no axis score lowered.
- `SKILL.md`, `PROVINCE.md`, `SHONEN.md` absent from `git diff --stat 090a46f8 02b6d88f` → depth:density `unchanged` (273.2 → 273.2 as reported).
- Integrated entry `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` spot-read: quote `S128.txt:94-95` and `S130.txt:77-78` match the snapshots byte-for-byte; instrument cite `capture-secret-scan.py:106-107` = `_CF_SIG`/`_CF_KPI`, `:106-114` = the threshold block + `CLOUD_PATTERNS`. No harm found.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth (verifiability, C1) | improved | meter re-run 777/1798 → 785/1797 rc=0; 5/5 re-anchors read correct |
| coverage (C2) | improved | new class absent at base, fires at landing on S128/S130 and closure fixtures |
| depth:density (guard) | unchanged | SKILL.md untouched |

## 4. Discernment spot-check (`corpus/lessons/round-89.md` § Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S128 CloudFront canned-policy signed URL | admit (mined) | live https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html, HTTP 200, 34341 B, 2026-11-07 | agree | live text holds "A hashed, signed, and base64-encoded version of the JSON policy statement", `Key-Pair-Id= K2JCJMDEHXQW5F &Hash-Algorithm= SHA256` and the example `Signature= nitfHRCr…`; first-party, defines exactly the shape the scanner encodes |
| S129 GCS V2 signing (legacy) | reject | live https://docs.cloud.google.com/storage/docs/access-control/signed-urls-v2, HTTP 200, 121500 B | agree | tag-stripped text: `GoogleAccessId` 1 mention ("the GoogleAccessId you need when assembling the signed URL"), `GoogleAccessId=` 0, `Signature=` 0, `legacy` 1 — no query-string form to encode; flip condition is apt |
| S130 SOURCES row (new) | admit (mined), quote check | live custom-policy page, HTTP 200, 50387 B; snapshot `S130.txt:163` | agree | lesson quote "anyone with the signed URL can access all of the files in any distribution that is associated" = 17 words (≤25), present live and at `S130.txt:163` |

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok
…/corpus/SOURCES.md`, rc=0, six inherited `W04` duplicate-URL warnings (S028, S029, S072, S076,
S080, S085), none new. Registry rows: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` →
127 at `090a46f8`, 130 at `02b6d88f` (matches report).

## 5. Trend verdicts

- **expansion: improved** — two tier-A first-party sources mined (S128, S130), one rejected with flip; registry 127 → 130; a new detection class on a committed instrument, confirmed firing on real tracked sibling captures.
- **quality: unprovable-but-better** — 9 bare/wrong citations now resolve to supported ranges (5 re-anchors read correct by me); the falsified knowledge entry was repaired in-round; R141 added with a fail demonstration. Not `improved`: I did not re-check every admitted entry, the C2 counter leaves clauses unbound (M89-2), and the tip meter reading is not reproducible (§2 C1 finding).
- **discernment: improved** — the outside spot-check agrees with the gate on the admit (S128, S130 quote) and the reject (S129).

## 6. Routed defects (the lane fixes next round)

1. **Meter environment dependence.** `knowledge-meter.py --measure-rev` classifies against the `--lane` working tree (and absolute fleet paths), so absolute readings differ by checkout/location (812 clean clone vs 815 live at `b9fcf005`; filed 814). Pin the classification tree to the measured revision or record the `--lane` path/state in every receipt; file a correction for "814/1827 at `b9fcf005`" in the r90 report.
2. **M89-2 / M89-3** (lane-reported): C2 counter clause list must derive from the statement with boundary plants; control inputs must be commit-bound. Carry to r90 as planned.
3. **R140 scoped out**: `r140-check.py` cannot parse four-column labels; fix the checker so tranche 5 runs under R140.
4. **Composite token** `triage-thresholds.md:457` (`claim-package-contract.md:9-16, 28-38`) still bare.
5. **Sibling credential material** (kengaku `.ufo/waves/round-95/w1/ScoutSources/receipts/net/config.headers:5`, kama `.ufo/waves/round-47/w1/out/S1Rows/model-head.txt:4`): confirmed tracked; owned by those lanes / operator via L0 `kasegi | round-89`. Not kasegi's to fix; kept here so the queue does not drop it.
6. **considerthese intake gate** (`considerthese/2026-10-24.md:49-52`): declined with a stated flip for the fourth routing; take it in the first round without a `capture-secret-scan` claim.

Operator note: SHONEN boxes are all `[~]` with pointers to `corpus/lessons/round-47-verifier-spotcheck.md`
and `corpus/practice/curl-h1-1913733/report.md`; they look checkable by a non-author promotion
review (operator-owned; not checked here).
