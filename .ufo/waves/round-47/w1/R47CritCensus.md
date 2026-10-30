# R47CritCensus

Axes: **depth:verifiability; coverage**. Census-only review; no admission or integration judgment.

## Result

The assembled round-end census candidate **validates with exit 0**, 76 registry rows and exactly four warning-only W04s. No malformed rows, duplicate IDs, enum violations, or missing mined used-by paths were printed with the F30 entry present.

Exact commands were extracted verbatim from fleet `CORPUS.md:135,137,143,145,147`; maintained invocation was `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md`, run from each isolated mirror root. Complete argv/stdout/stderr/exit receipts: `.ufo/waves/round-47/w1/R47CritCensus.draft/receipts.json`; frozen manual commands also preserved in `R47CritCensus.draft/manual-commands.json` under the same wave directory.

| Check | Do-nothing base | Candidate | Candidate without F30 entry |
|---|---|---|---|
| Rows | 74, exit 0 | 76, exit 0 | 76, exit 0 |
| Malformed rows | `0`, exit 0 | `0`, exit 0 | `0`, exit 0 |
| Duplicate IDs | empty, exit 0 | empty, exit 0 | empty, exit 0 |
| Enum/tier violations | empty, exit 0 | empty, exit 0 | empty, exit 0 |
| Mined used-by | empty, exit 0 | empty, exit 0 | `missing: corpus/knowledge/zdi-disclosure-policy.md`, **exit 0** |
| Maintained validate | 3 W04 + `file ok`, exit 0 | 4 W04 + `file ok`, exit 0 | 4 W04 + **E11 S075**, **exit 1** |

## Warning derivation

The parser emits W04 when a URL was seen but its scope differs (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:643-645`); warnings do not make validation fail (`:16-18`). Expected pairs, independently observed in receipts:

- S028 / S006: `docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq`.
- S029 / S024: `eur-lex.europa.eu/eli/reg/2024/2847/oj/eng`.
- S072 / S070: `bughunters.google.com/about/rules/about-this-section`.
- **New S076 / S074:** `docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories`.

The first three are in the do-nothing control; only the fourth is added. The distinct-scope S076 row starts teaches with `supersedes S074 —`; no E04 was emitted. Do not remove historical S074 or suppress W04 to obtain a cleaner-looking output.

## Strongest counterexample and smallest correction

**Counterexample:** integrate S075 before its actual entry. The unchanged frozen manual mined-used-by command prints a missing path yet returns **0**, because its loop echoes the defect successfully. Therefore “all manual commands exit 0” is not a sufficient acceptance criterion. The maintained parser catches the same state with `file E11 S075 missing used-by corpus/knowledge/zdi-disclosure-policy.md`, exit **1**. This is an exercised failure, not a hypothetical.

**Smallest safe correction:** land the actual F30 entry with its mined row; require both the manual command's empty output and maintained-parser exit 0. Preserve the frozen manual command rather than silently repairing that contract. Green census alone is also not D5 closure: the unchanged base still validates with the scaffold present.

## Mirror identity and limitations

Named do-nothing control: **unaltered SOURCES.md exported read-only from fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8**. Both arms copied the lane's real knowledge and lesson files; the positive candidate additionally copied the real `R47SrF30Entry.draft/zdi-disclosure-policy.md`, not a placeholder.

Candidate assembly retained base bytes except: unwrapped D5 using the exact deletion map `R47ScoutScaffold.md:73-82`; inserted S075 and the search/change bullets from `R47SrRegistry.md:19,25,31`; inserted S076's actual available proposed row from `R47RevCounterC1.draft/attack-A/corpus/SOURCES.md:82` **without that attack fixture's comment wrappers**; changed only S074 status to rejected and used-by to `corpus/lessons/round-46.md`, per the frozen proposal. Preserved candidate/base files and SHA identities: `.ufo/waves/round-47/w1/R47CritCensus.draft/{candidate-SOURCES.md,base-SOURCES.md,assembly.json}`.

This exercises the assembled **census-affecting** edits, not a final integrated author tree. No complete D5/D7 integration draft was available; S076 came from the explicitly identified review fixture. D6 entry edits, D8 non-row prose, README admission and final correction-log wording are not certified. L1 must rerun against its exact integrated tree. Census does not verify cited-file contents, source truth, capture binding, or frontier novelty; in particular its acceptance does not resolve the separately reported S074 rejection/capture-binding conflict (`R47RevD7.md:11-13`). No frozen C1/C2 counter, full battery, live capture or survivor closure was run; the disclosed 34 survivors remain gaps.

Disk guard reported scratch **375.7G free, 54% used** before the probe; its subsequent top-consumer phase timed out at 30 seconds, so the guard was not an overall successful run. Probe fixtures stayed under `/fast/scratch/hyaku/kasegi-r47/R47CritCensus/`; Python `finally` removed that directory and printed `SCRATCH_REMOVED True`. No installs, git/jj mutations, production edits or intentional background work. The guard tool auto-backgrounded before delivering its timeout.

Self-evaluation: accuracy 4 (explicit candidate identity, not integrated evidence); completeness 4 (all requested census checks exercised, final integration unavailable); clarity 4 (full outputs separated into receipts); actionability 4 (specific entry dependency and acceptance rule); conciseness 4 (fixture limitations retained). Overall 4.0. Highest-impact improvement: L1 repeats the same checks on final bytes. User-facing scope remains census conformance, not claim acceptance.

Report: .ufo/waves/round-47/w1/R47CritCensus.md
