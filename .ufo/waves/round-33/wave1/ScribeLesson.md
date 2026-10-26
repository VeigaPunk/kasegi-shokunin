# ScribeLesson — round-33 lesson (`corpus/lessons/round-33.md`)

Seat: `ScribeLesson` (scribe, leaf). Round kasegi-shokunin 33, wave 1, hyaku run 8.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims-freeze
`6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`. Answering model (rule 10, session route table, not passed by me):
`opencode-go/deepseek-v4.1-flash`.

**Landing.** `corpus/lessons/round-33.md` — the only path this seat wrote besides this receipt.

```
$ sha256sum corpus/lessons/round-33.md ; wc -l -c corpus/lessons/round-33.md
120937c6b6d19e4b49e44bf3ea7314976b8f9c191305519d08680196123c9fb2  corpus/lessons/round-33.md
    138  42602 corpus/lessons/round-33.md
```

(Sections present: `# Round 33 — kasegi`; `## Frozen claims — before → after`; `## Gate — F16 / S049 / S050 and the
assimilation set` with `### Admitted`, `### Id-collision evidence`, `### Refused package candidates`,
`### Quarantine slice`, `### Registry changes`, `### Gate caveats`; `## Mistakes (M33-*)`; `## considerthese`;
`## Census before → after`; `## No-harm`; `## Open items / unverified`; `## Touched surfaces and provenance`.)
`grep -c 'WAVE_DISPATCH_PENDING\|LANDED_HASH_PENDING'` → **2** (both placeholders left for the L1, as the item requires).

Scratch: `/fast/scratch/hyaku/kasegi-r33/ScribeLesson/` (two bookend digest files only) → `scratch_removed`; `ls`
after removal shows only other seats' trees. No clone/worktree/fixture. No tool installed or upgraded. No git/jj
mutation (read-only `rev-parse`, `log`, `show`, `ls-tree`, `diff`, `status`). No network fetch by this seat; no
`/home/vgpnk/Projects/shokuknow` write; no package tool run; no credential material read or reproduced.

## 1. What the item asked to wait for, and what arrived

```
$ W=.../wave1; for f in ScoutPackageThemes ExecQuarantine ExecHarnessC2 ExecRegressionC1 ExecCensusAfter ExecErratumCheck; do
    [ -s "$W/$f.md" ] || echo "absent $f"; done   # polled every 20 s
READY at 2026-10-26T04:47:05Z (ExecNoHarmFinal last; 56 receipts of 64 seats present)
```

Arrival order observed: `ScoutPackageThemes` (early), `ExecQuarantine` 01:19, `ExecErratumCheck` 01:31,
`ExecHarnessC2` 01:33, `ExecCensusAfter` 01:34, `ExecRegressionC1` 01:35, `ExecNoHarmFinal` 01:47. Polls capped per
bound 9; the wait ended inside the item's 50-minute cap.

```
$ python3 - <<'PY'  # wave1-spec.json names vs wave1/*.md
receipts 56 missing ['ScribeScorecard', 'ScribeLesson', 'ScribeReportDraft', 'RevGateSpot',
                     'CritMistakes', 'SimplifierCleanup', 'ExecScratchDiscipline', 'RevC1BeforeAfter']
```

## 2. Re-runs this lesson made (quiescence check, not a new claim)

The C1/C2 counters of record (`ExecRegressionC1`, `ExecHarnessC2`) measured a working-tree entry digest
(`53c48b3b…`) that the integration commit does not carry (`1f7ac0a2…`). Per bound 6 the after-column must rest on
quiescent committed bytes, so every counter that any cited cell depends on was re-run here with bookends:

```
$ sha256sum corpus/SOURCES.md corpus/README.md corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md \
            corpus/instruments/knowledge-expected.txt corpus/source-snapshots/round-32/manifest.json > t0 ; date -Is
2026-10-26T01:42:45-03:00
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json

$ python3 corpus/instruments/capture-binding-check.py | tail -3
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0                                             # binding_exit=0

$ python3 corpus/instruments/capture-binding-check.py --selftest | tail -2
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0

$ python3 corpus/instruments/frontier-recheck-count.py | tail -3
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0                                                 # harness_exit=0

$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print "frontier_admitted="n+0}' corpus/README.md
frontier_admitted=16
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md     # 50
$ grep -lE '^source: S049 ' corpus/knowledge/*.md | wc -l                  # 1
$ grep -lE '^source: S050 ' corpus/knowledge/*.md | wc -l                  # 1

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
… S049:Q8 OK occurrences=1                                               # recheck49_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050
… S050:Q6 OK occurrences=1                                               # recheck50_exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0

$ sha256sum <same five files> > t1 ; diff t0 t1 && echo BOOKEND_IDENTICAL
BOOKEND_IDENTICAL
```

Read-only state checks this lesson also made (no claim beyond the pointer):

```
$ git rev-parse HEAD                       → 9f9848816503aa0cd566fc2efdc5e69ea501a253
$ git ls-tree -r -l HEAD -- .ufo/waves/round-33 | awk '{s+=$4;n++} END{print n,s}'
132 1366042
$ grep -n 'capture-binding-check' SCORECARD.md  → 1001 1048 1064 1071 1078 1084 (capability table row at :1078; `## Round-33 capabilities` heading at :1074)
$ sha256sum SCORECARD.md                   → e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3
$ grep -nE '^\| *S0(48|49|50) ' corpus/SOURCES.md   → 54, 55, 56   (rows 48 → 50)
$ git diff 690b69da:corpus/SOURCES.md corpus/SOURCES.md  '>' 6 / '<' 0
$ stat -c %y corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md → 01:33:57 -03 (306 lines)
```

## 3. Where each lesson section's numbers come from

| lesson section | receipt authority |
|---|---|
| header (shape, roles, route, models) | `wave1-spec.json`, `wave1-dispatch.json`, `wave1.ready`, `wave1/watchdog-digest.txt`; `ls wave1/*.md` for coverage; per-file model grep over those receipts |
| `## Frozen claims` before column | `.ufo/waves/round-33/c1-controls/before.txt`, `c2-controls/before.txt` |
| `## Frozen claims` C1 after | `wave1/ExecRegressionC1.md` §1–§2.2, `wave1/ExecCaptureBinding.md` §2/§4, `wave1/ExecManifestUpgrade.md` §6, `wave1/ExecManifest32.md`; capability row `wave1/ScribeScorecard.md` §3 |
| `## Frozen claims` C2 after | `wave1/ExecHarnessC2.md` §1 tables, `wave1/ExecCensusAfter.md` §1–§2, `wave1/RevEntryF16.md` §1/§7 |
| erratum paragraph | `.ufo/waves/round-33/claims-erratum-1.md`; `wave1/CritC1Kill.md` §Verdict 3, `wave1/RevManifestUpgrade.md`, `wave1/RevClaimsFreeze.md`, `wave1/MutCtrUnbound.md` §PRE-STATE |
| `### Admitted` | `wave1/ExecManifest32.md`, `wave1/ScoutLiveDrift.md`, `wave1/ExecRegistryAppend.md` §2, `wave1/RevEntryF16.md`, `wave1/ExecHarnessC2.md` §1; quotes re-located by this seat in `corpus/source-snapshots/round-32/S049.txt:214` and `S050.txt:591` |
| `### Id-collision` | `assimilation/{reg-ids,staged-ids,collisions,guard-proof.txt}`, `wave1/ScoutPackageThemes.md` §1, `wave1/ConnOwnership.md` |
| `### Refused package candidates` | `wave1/ScoutPackageThemes.md` §2 (five standing + two extra), flip conditions quoted from `corpus/lessons/round-31.md:62-67` |
| `### Quarantine slice` | `wave1/ExecQuarantine.md` §1, §4–§6 (verdicts + installable Gate blocks) |
| `### Registry changes` | `wave1/ExecRegistryAppend.md` §2, §4–§6, §8–§9 |
| `### Gate caveats` | `wave1/CritC2Kill.md` §5, `wave1/CritC1Kill.md` H1–H3 + § corrections, `wave1/MutCtrUnbound.md` §Verdict |
| `## Mistakes` | `wave1/ScribeQuality.md` (R20/R21), `wave1/ExecErratumCheck.md` §2–§6, `wave1/ConnOwnership.md` F4, `wave1/RevQuoteSweep.md` §5–§6, `wave1/RevEntryF16.md` §0, `wave1/ExecCensusAfter.md` §0, `wave1/MutCtrUnbound.md`, `wave1/MutEntryF16.md`, `wave1/MutCtr*`, `wave1/MutLegacyManifestDrop.md`, `wave1/MutManifestLegacy.md` |
| `## considerthese` | `wave1/ExecGrowthMeasurement.md` §0–§6; `corpus/knowledge/considerthese-proposals-ledger.md` round-31 block |
| `## Census before → after` | `census-before.txt`, `wave1/ExecCensusAfter.md` §1–§3, this seat's `census_exit=0` re-run |
| `## No-harm` | `wave1/ExecNoHarmFinal.md` §1–§5, `wave1/RevNoHarm.md` §5–§6, `wave1/ExecRegressionC1.md` §2.5/§2.8–§2.10 |

## 4. Sweep (mistakes section, command + counts as filed)

```
$ cd .../wave1 && for w in BLOCKED DEFECT SURVIVOR survivor FAIL traceback PRE-STATE; do
    printf '%-10s files=%-3s hits=%s\n' "$w" "$(grep -l "$w" *.md | wc -l)" "$(grep -o "$w" *.md | wc -l)"; done
BLOCKED    files=3   hits=10
DEFECT     files=0   hits=0
SURVIVOR   files=3   hits=4
survivor   files=8   hits=20
FAIL       files=22  hits=161
traceback  files=0   hits=0
PRE-STATE  files=34  hits=91
```

`:204 BLOCKED: none.` (`ExecExpectedList`) and `ScribeProvince:41` "No `BLOCKED:` line is" are negative assertions;
the remaining `BLOCKED` hits are `ExecWaveEvidencePack.md`'s token-total table. No seat reported a blocker. The two
real survivor events are `MutCtrUnbound` (plain-run rule-B url limb) and `MutEntryF16` (one-directional harness rule A);
`ScribeScorecard.md` only cites them.

## 5. Defects, deviations and limits this seat found (recorded, not repaired)

1. **Rule-B semantics vs the frozen kill text.** The landed instrument is id-scoped per `claims-erratum-1`; the frozen
   kill rule still reads "0 or 2+ matches = failure". Measured both readings: 40 (erratum) vs 38 (literal) on the same
   bytes. Recorded in the lesson's erratum paragraph and open item 8; this seat did not touch `claims.json` or the
   instrument. Earlier PRE-STATE run that opened it (this seat, before the erratum landed):
   `records=40 bound=36 unbound=4` with `FAIL rule=url-ambiguous record=S029/S006` — superseded, not cited as an after
   column; it was messaged to `ExecCaptureBinding`, who confirmed erratum-1 and the final digest `b4182665…`.
2. **`anchorcheck.py` in-range 7 → 12** (`ExecRegressionC1` D-R33-1) is a base-state literal, not a class change;
   `LOST-RECORDED` stays 306 and every failure class stays 0 (`ExecNoHarmFinal` §4).
3. **Entry digest churn inside the wave** (M33-5): counters of record ran on `53c48b3b…`; the integration commit
   carries `1f7ac0a2…`. No counter value changes (none reads the entry body); all nine C2 cells re-verified here on
   `1f7ac0a2…` with identical bookends. `ExecCensusAfter` §0 discloses the same gap.
4. **`SOURCES.md` anchor drift** (M33-3): the 6-line append moves sections +2/+2/+3/+3 and the S043 change-cell line
   87 → **90**, so the filed `SOURCES.md:83` citations are now off by **+7**. `ConnOwnership` F4 predicted +6 pre-land
   and corrected to +7; the lesson files carrying that citation are outside this seat's write scope.
5. **`resolve.py` was not run in the lane by this seat** — it writes `citation-survival.{md,tsv}` beside itself, an
   unowned path. The No-harm figures are `ExecNoHarmFinal`'s scratch-tree runs; the lane copies keep mtime
   `2026-10-25T04:15:16`.
6. **`records=40` is 40 entries over 38 ids** (S041 recurs in rounds 26/28/30); `fetched_utc` is the capture-commit
   time, not a fetch instant; no rule binds a record to its capture bytes (H1/H2) — all three disclosed in the lesson
   because they bound C1's wording.
7. **Pre-existing QUALITY finding untouched**: `corpus/QUALITY.md:77` (R13) cites `README.md:159` (PAST-EOF; the file
   has 14 lines) — inherited, reported by `wave1/ScribeQuality.md` F1, out of scope for this seat.

## 6. Out of scope this seat (not touched)

`claims.json`, `claims-erratum-1.md`, `c1-controls/`, `c2-controls/`, `census-before.txt`, `assimilation/`,
`watchdog-digest.txt`, the wave report, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `PROVINCE.md`,
`corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/*` (all read-only this round),
`corpus/source-snapshots/**`, `corpus/knowledge/**`, every other seat's receipt. No score move is claimed anywhere in
the lesson; the two header placeholders are the L1's edit.
