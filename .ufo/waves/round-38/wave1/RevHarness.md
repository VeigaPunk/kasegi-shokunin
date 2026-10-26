# RevHarness — independent recomputation of the frontier-recheck harness delta (round 38, C2 coverage)

Seat: RevHarness (leaf reviewer; no subagent dispatch, no labrat probe — reviewers get none).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo; nothing written outside this receipt).
Base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims-freeze `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`;
lane HEAD observed during this seat: `700153593eb586c70a6499c8ca225ee4d673bc9b` (adds only
`.ufo/waves/round-38/wave1-dispatch.json`, `wave1-run.err`, `wave1-spec.json` over the freeze; `git status --porcelain`
shows only `?? .ufo/waves/round-38/wave1*`). F21 is **not landed in the lane yet** — this seat verifies the delta by
scratch mirror, as the item specifies.

Item: recompute the harness delta independently — (1) base `entries=23 pass=23` maps exactly to the admitted F-rows
(listed); (2) simulate F21 in a scratch mirror → `entries=24 pass=24`; (3) a fabricated capture (sha mismatch) makes
F21 FAIL. Receipt only; no deliverable file.

## 0. Instruments unchanged base..HEAD (precondition for recomputation)

```
$ git -C …/kasegi-shokunin diff --stat a173b0c2… 9a10b02… -- corpus/instruments/frontier-recheck-count.py   (empty)
$ git -C …/kasegi-shokunin diff --stat a173b0c2… HEAD -- corpus/                                            (empty)
$ sha256sum corpus/instruments/frontier-recheck-count.py   -> 1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249
$ sha256sum corpus/instruments/source-recheck.py           -> fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003
```

Both identical in the base export and the lane working tree, so one harness version measures both ends of the delta.
`corpus/` is untouched base..HEAD, which also means the lane captures equal the base captures (relevant in §2).

## 1. Base: entries=23 pass=23, mapped exactly to admitted F-rows

```
$ git -C …/kasegi-shokunin archive a173b0c2b98c5ae39599fa9be76027fbbead0b9e | tar -x -C $S/base
$ find $S/base -type f | wc -l -> 7290;  tracked blobs: 6825 regular + 465 exec + 58 symlinks = 7348
  (the 58 are symlinks; `find -type f` skips them; `find \( -type f -o -type l \)` -> 7348 = ls-tree count — export faithful)
$ TMPDIR=$S python3 $S/base/corpus/instruments/frontier-recheck-count.py --json $S/base-recheck.json
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
entries=23 pass=23 exit=0
```

Matches the C2 before-control `entries=23 pass=23 exit=0`. Independent row mapping (my own regex over the base
README, not the harness's code): 20 F-rows total, **all 20 `admitted`** (no other status present), expanding to
**23 (row, entry) pairs** because F09, F10, F11 each name two entries in one cell:

| row | entries |
|---|---|
| F01 | knowledge/cvss-v4-severity-and-vector.md |
| F02 | knowledge/coordinated-disclosure-timelines.md |
| F03 | knowledge/authorization-safe-harbor-and-scope.md |
| F04 | knowledge/ai-assisted-finding-validation.md |
| F05 | knowledge/cwe-top25-2025-methodology.md |
| F06 | knowledge/multiparty-vulnerability-coordination.md |
| F07 | knowledge/cna-assignment-and-vulnerability-rules.md |
| F08 | knowledge/cra-manufacturer-reporting-duties.md |
| F09 | knowledge/authorised-testing-rules-of-engagement.md; knowledge/statutory-authorization-and-unauthorized-access.md |
| F10 | knowledge/vendor-disclosure-policies-as-corpus-objects.md; knowledge/vendor-disclosure-policy-commitments-crosswalk.md |
| F11 | knowledge/iso-29147-and-30111-division-of-labour.md; knowledge/iso-29147-divergence-and-clause-crosswalk.md |
| F12 | knowledge/japanese-domestic-disclosure-workflow.md |
| F13 | knowledge/program-severity-ladders-and-reward-scales.md |
| F14 | knowledge/japanese-severity-vocabulary-and-impact-model.md |
| F15 | knowledge/vendor-third-party-finding-coordination.md |
| F16 | knowledge/chinese-crowdsourced-testing-scope-and-rewards.md |
| F17 | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md |
| F18 | knowledge/cisa-kev-catalog.md |
| F19 | knowledge/epss-exploit-prediction-scoring.md |
| F20 | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |

Cross-check: my 23 pairs == the harness JSON receipt's 23 (frontier, entry) pairs, `sorted(...) == sorted(...) -> True`;
receipt `entries=23 pass=23`, `duplicate_entry=None`. So 23/23 maps exactly to the admitted rows — no row skipped,
no extra record, no duplicate realpath.

Execution-limb note (pre-existing property, also flagged by ExecC2Harness §8): committed entries' `recheck:` lines
begin `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …` (verified on F01's entry at base), so under
`--root <export>` the executed line still runs against the lane working tree. Faithful here because `corpus/` is
untouched base..HEAD (§0) and the lane tree is clean for corpus/ — the 23 exits read captures identical to base's.
Rules A/B/C (the binding limbs) are root-scoped and did bind to the export.

## 2. Mirror simulation: F21 added → entries=24 pass=24

Mirror = reflink-free `cp -a` of the base export + four additions, all under `$S/m` (no lane write):

1. `corpus/README.md`: the planned F21 row inserted directly under the F20 row (line 416→417):
   `| F21 | OASIS CSAF 2.0 (Common Security Advisory Framework) — VEX product-status categories and machine-readable not-affected justification flags | admitted | knowledge/csaf-vex-product-status-and-justifications.md | S055 | PLUMBING STUB … |` (ExecC2Harness §5 row; the harness regex reads only cells 1–4, so the note cell is harness-invisible and cannot change the delta).
2. `corpus/knowledge/csaf-vex-product-status-and-justifications.md` (704 bytes, sha256
   `a4604cb438802955003c56a7514fe96211157808e5eb64cfd4b8a51c17277d0c`): the planned header (ExecC2Harness §6) with
   ONE documented mutation — the `recheck:` line drops the `cd <lane> && ` prefix so the mirror run's execution limb
   binds to the mirror; the `--manifest`/`--source` tokens are byte-identical to the landed line's tail (verified:
   `tails byte-identical: True`; landed line `bash -n` -> parse ok). Body cites `S055` once (`S055.txt:L2135, …`),
   satisfying the citation limb.
3. `corpus/source-snapshots/round-38/S055.txt` — copied from the capture seat's wave-dir deliverable
   `ExecC2Capture.S055.txt`, hash-verified before copying: sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`
   (272441 bytes, 5146 lines) — matches ExecC2Capture's declared sha.
4. `corpus/source-snapshots/round-38/manifest.json` — copied from `ExecC2Capture.manifest.json`, sha256
   `95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f` (3841 bytes, 57 lines) — matches ExecC2Capture's
   declared sha.

```
$ TMPDIR=$S python3 $S/m/corpus/instruments/frontier-recheck-count.py --root $S/m --json $S/mirror.json
… (F01–F20 lines identical to base) …
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
entries=24 pass=24 exit=0
```

F21 JSON record: `declared_ids=["S055"]`, `evidence_declared_ids=[]`, `cited_ids=["S055"]`, `recheck_ids=["S055"]`,
`manifest="corpus/source-snapshots/round-38/manifest.json"`, `exit=0`, `problems=[]`, `status=PASS`;
`duplicate_entry=None`. **Delta is exactly one line**: base body (23 lines) is byte-identical to the mirror body's
first 23 lines; the only extra line is the F21 PASS line. So 23→24 comes solely from the added F21 binding, with the
real capture bytes — not the harness seat's stub.

Post-landing simulation of the landed (cd-prefixed) line — the lane's own instrument, run from the lane root, against
the real capture via the mirror manifest's absolute path (byte-equivalent to what the landed line does once the
manifest lands in the lane; the manifest path is the only difference and it resolves to the same 3841 bytes):

```
$ (cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && TMPDIR=$S python3 corpus/instruments/source-recheck.py \
     --manifest $S/m/corpus/source-snapshots/round-38/manifest.json --source S055)
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
exit=0
```

## 3. Fabricated capture (sha mismatch) → F21 FAIL

Probe 1 — one byte of the mirror capture flipped (`dd seek=100000`):

```
$ TMPDIR=$S python3 $S/m/corpus/instruments/source-recheck.py --manifest …/manifest.json --source S055
S055:sha256 MISMATCH expected=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 actual=ea06e6963e289c2066376275e9941821492a3c6d7a462bab26a85f5732f4238b
(source-recheck exit=1)
$ TMPDIR=$S python3 $S/m/corpus/instruments/frontier-recheck-count.py --root $S/m
FAIL     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=1    problems=recheck-exit-1
entries=24 pass=23 exit=1
```

Probe 2 — fabricated manifest sha (mirror clone `$S/m2`, manifest `sha256` field replaced with 64 zeros):

```
S055:sha256 MISMATCH expected=0000000000000000000000000000000000000000000000000000000000000000 actual=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
FAIL     F21  … ids=S055 exit=1 problems=recheck-exit-1
entries=24 pass=23 exit=1
```

Restore (re-copy the verified deliverable bytes) → `PASS F21 … exit=0`, `entries=24 pass=24 exit=0` — the FAIL was
caused solely by the sha mismatch, in either direction (capture bytes or manifest field). The harness inherits the
capture limb's fail-closed behavior: a fabricated capture cannot pass F21.

## 4. Harness selftest (sanity of the measuring instrument itself)

```
$ TMPDIR=$S python3 $S/base/corpus/instruments/frontier-recheck-count.py --selftest --scratch $S/st
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0   (exit=0)
```

## 5. Findings

- The claimed harness delta is real and exactly scoped: base 23/23 (20 admitted rows, F09/F10/F11 double-entry),
  +F21 → 24/24, all pre-existing records byte-identical, F21 PASS with `ids=S055` against the real capture bytes.
- The capture limb is genuinely fail-closed: a sha mismatch (either side) fails F21 with `recheck-exit-1` and drops
  the run to `entries=24 pass=23 exit=1`.
- No defect found in the harness or the delta. Residual observations (both pre-existing / other seats' scope, not
  defects in this delta): (a) the `cd <lane>` execution-limb property (§1/§2) means a `--root <export>` run measures
  binding against the export but executes against the lane — fine while corpus/ is untouched, worth remembering if a
  future round mutates captures in-flight; (b) the landed entry bytes are still being drafted by ScribeEntryF21 — my
  mirror used the planned header with the single documented root-relative mutation; the landed entry must keep
  `--source S055` as the only selection and cite `S055` in the body, or the delta above does not transfer.

## 6. Tooling / scratch

No tools installed or upgraded; no pacman; no network fetch (the capture was already fetched by ExecC2Capture — this
seat only re-hashed and re-ran it). Scratch `/fast/scratch/hyaku/kasegi-r38/RevHarness/` (base export, mirror `$S/m`,
clone `$S/m2`, run transcripts, JSON receipts, selftest dir) removed before yield; this receipt is the only lane
write. No mutating git command was run (read-only: rev-parse, status, diff, ls-tree, archive, grep via git-grep).
