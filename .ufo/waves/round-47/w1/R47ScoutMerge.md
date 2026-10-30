# R47ScoutMerge — assimilation scan

Axes: depth:verifiability; coverage. Report-only; adopted nothing.

## Finding

**Assimilation: none is honest for F30 this round.** The staged package has adjacent vendor/coordinator disclosure material, but no identified third-party bug-broker acquisition/disclosure policy, ZDI entry, or broker acquisition timeline. This is a scope judgment about this staged package, not a claim that disclosure-policy themes are absent altogether. Confidence: high for the staged inventory and collision result; medium-high for the no-adopt recommendation (no live source re-open or adoption gate performed).

## Observed adjacent themes

All paths below beginning `knowledge/` are relative to `/home/vgpnk/Projects/shokuknow/merge/kasegi/`.

- **State coordinator timelines:** `MERGE-REPORT.md:24` names `japanese-domestic-disclosure-workflow.md`. Its staged entry `knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md:12-15,23-38` explicitly describes a state-coordinated, non-marketplace flow, a first-attempted-developer-contact clock and a one-year non-disclosure-request withdrawal rule. Adjacent as a clock comparator, not broker acquisition ground.
- **Vendor disclosure commitments:** `MERGE-REPORT.md:39` names `vendor-cvd-policy-crosswalk-2026-10-23.md`. Its staged entry `knowledge/corpus/knowledge/vendor-cvd-policy-crosswalk-2026-10-23.md:14-34,43-50` describes Cisco PSIRT lifecycle commitments, partners and expedited-disclosure triggers. Vendor-side policy, not a buyer/broker timeline.
- **Vendor-as-finder/third-party coordinator:** `MERGE-REPORT.md:47` names `vendor-third-party-finding-coordination-2026-10-23.md`. Its staged entry `knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md:15-24,33-35` describes MSVR's three intake routes and vendor/finder/coordinator roles; explicitly does not document unpublished coordination agreements. “Third-party” here means affected products, not a bug-acquisition broker.
- **Japanese vendor policies:** `MERGE-REPORT.md:34` names `japanese-vendor-disclosure-policies-2026-10-23.md`. Its staged entry `knowledge/corpus/knowledge/japanese-vendor-disclosure-policies-2026-10-23.md:30-43` describes negotiated Cybozu/JPCERT publication timing, a bounty paid two months after resolution, and Hitachi cross-vendor routing. Payment is vendor bounty timing, not broker purchase/acquisition timing.
- Supporting legal/standards context appears at `MERGE-REPORT.md:29-30,36,45`: domestic disclosure law and ISO/IEC 29147/30111. These are adjacent context, not direct F30 content.

The full staged knowledge inventory was read at `MERGE-REPORT.md:15-85` (67 entries; count stated at lines 5-7). Text search across the package for `ZDI|Zero Day Initiative|zerodayinitiative|bug.broker|acquisition|acquire[ds]?` found no ZDI/broker entries: only unrelated uses of acquisition/acquires/acquired and an account-acquisition disclaimer. Search is literal evidence, not semantic proof of all possible paraphrases; the adjacent entries above were read to distinguish roles and clocks. No exported code contract was at issue. No LSP device is mounted in this seat; these are Markdown document findings, not semantic symbol/reference claims.

## ID-collision guard receipt

Contract source: lane `.ufo/waves/round-47/build-wave1-spec.py:109-110` prescribes the zero-to-three-leading-spaces expression. Executed the prescribed extraction/sort/comm pipelines below, changing only output root `A` to this seat's scratch to honor the binding write boundary; did not write the shared `assimilation/` directory. `LC_ALL=C` pins sorting. The source inputs were the live read-only working files, not a freeze-tree export.

```sh
set -eu
export LC_ALL=C
A="$PWD"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
wc -l "$A/reg-ids" "$A/staged-ids" "$A/collisions"
```

Printed output:

```text
  74 /fast/scratch/hyaku/kasegi-r47/R47ScoutMerge/reg-ids
  94 /fast/scratch/hyaku/kasegi-r47/R47ScoutMerge/staged-ids
  44 /fast/scratch/hyaku/kasegi-r47/R47ScoutMerge/collisions
 212 total
```

**Observed collision count: 44**, S031–S074 inclusive. The seat card's elsewhere-mentioned 42 is not this run's result. The registry has S001–S074, while staged IDs are S031–S124. `MERGE-REPORT.md:9` still states the packaging-time lane count was 30, explaining why its “continuing the lane's S-space” premise at line 13 cannot be used for a current blind append. These are identifier collisions, not proof of equivalent content.

### Registry ID list (74 lines)

```text
S001
S002
S003
S004
S005
S006
S007
S008
S009
S010
S011
S012
S013
S014
S015
S016
S017
S018
S019
S020
S021
S022
S023
S024
S025
S026
S027
S028
S029
S030
S031
S032
S033
S034
S035
S036
S037
S038
S039
S040
S041
S042
S043
S044
S045
S046
S047
S048
S049
S050
S051
S052
S053
S054
S055
S056
S057
S058
S059
S060
S061
S062
S063
S064
S065
S066
S067
S068
S069
S070
S071
S072
S073
S074
```

### Staged ID list (94 lines)

```text
S031
S032
S033
S034
S035
S036
S037
S038
S039
S040
S041
S042
S043
S044
S045
S046
S047
S048
S049
S050
S051
S052
S053
S054
S055
S056
S057
S058
S059
S060
S061
S062
S063
S064
S065
S066
S067
S068
S069
S070
S071
S072
S073
S074
S075
S076
S077
S078
S079
S080
S081
S082
S083
S084
S085
S086
S087
S088
S089
S090
S091
S092
S093
S094
S095
S096
S097
S098
S099
S100
S101
S102
S103
S104
S105
S106
S107
S108
S109
S110
S111
S112
S113
S114
S115
S116
S117
S118
S119
S120
S121
S122
S123
S124
```

### Collision ID list (44 lines)

```text
S031
S032
S033
S034
S035
S036
S037
S038
S039
S040
S041
S042
S043
S044
S045
S046
S047
S048
S049
S050
S051
S052
S053
S054
S055
S056
S057
S058
S059
S060
S061
S062
S063
S064
S065
S066
S067
S068
S069
S070
S071
S072
S073
S074
```

## Indented-row guard proof and do-nothing control

Scratch fixture `fixture-reg` contained exactly `  | S002 |` plus newline; `fixture-staged` contained `| S002 |` plus newline. S002 is **not** in the actual staged set, so a staged fixture is essential: the genuine staged set cannot prove an S002 collision. No production or staged source bytes were changed.

Executed:

```sh
set -eu
export LC_ALL=C
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-reg | grep -oE 'S[0-9]+' | sort > fixture-reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-staged | grep -oE 'S[0-9]+' | sort > fixture-staged-ids
comm -12 fixture-reg-ids fixture-staged-ids > fixture-collisions
wc -l fixture-reg-ids fixture-staged-ids fixture-collisions
```

Printed:

```text
 1 fixture-reg-ids
 1 fixture-staged-ids
 1 fixture-collisions
 3 total
zero-space control: exit=1 stdout=''; corrected fixture collisions='S002\n'
```

The do-nothing control used `grep -oE '^\|[[:space:]]*S[0-9]{3,}' fixture-reg`: exit 1, empty stdout. The corrected pattern extracted S002 from the same indented row and `comm -12` returned S002 (one collision). Thus leaving the zero-space expression unchanged misses the collision; the requested expression detects it. This is a bounded guard probe, not the round counters or full mutation battery.

## Recommendation and limits

- No staged direct F30 adopt candidate identified; keep the four adjacent themes as comparators only. Do not conflate vendor coordination or vendor bounty payment with a third-party broker's acquisition/disclosure clock.
- Any later assimilation must remap IDs and dependent references before adoption; 44 collisions prohibit blind append. No remapping, re-open, adoption mirror, or full adoption gate was attempted by this report-only seat.
- No C1/C2 counter pass, survivor closure, or full battery result is asserted. The disclosed 34 mutation survivors remain outside this scan; no battery rerun.
- Wrote only this report; scratch fixtures and intermediate receipt files were removed in `finally: shutil.rmtree(S)` after retaining their output in this report. Observed `Scratch removed: True`. No git/jj mutation, background job, installation, fleet-root write, or shokuknow write occurred. No heavy pass was needed.

## Self-evaluation

Accuracy 4/5 (literal search cannot exclude every paraphrase); completeness 4/5 (adoption gates intentionally out of scope); clarity 4/5 (full requested ID lists add length); actionability 4/5 (future adoption requires a separate gate); conciseness 4/5 (receipts retained verbatim). Overall 4.0/5. Main improvement if adoption becomes in-scope: re-open a selected primary source and prove its gate before recommending adoption. This report distinguishes adjacent themes from F30 ground; the user should be able to reproduce the guard without treating the recommendation as an adoption verdict.

Report: .ufo/waves/round-47/w1/R47ScoutMerge.md
