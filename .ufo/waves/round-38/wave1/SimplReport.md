# SimplReport — round-38 report-contract lint

Seat `SimplReport` (report-contract linter, L2 leaf — no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the only lane repo). Base
`a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims-freeze commit
`9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`; lane HEAD at my reads
`700153593eb586c70a6499c8ca225ee4d673bc9b` (mid-round, `git status --porcelain` = 15 — seats were
landing files while I read; not a defect). Judged on: calibration. Milestone round-38.

**Item.** Lint the report contract for `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md`:
required sections in order (Work performed, Landed changes, Before → after measurements, Sources &
frontier, Trend verdicts, SHONEN with one line per box), plus Stale-lane, tooling and the
residual-call/round-shape lines; `grep -c '^## SHONEN'` must be 1. Read the round-37 report and its
verifier §1/§5 and list each overreach sentence class to avoid. Deliver the exact greps the L1 runs on
the final report. Receipt only.

**Writes.** This receipt only (`git status --porcelain` lists it under the untracked
`.ufo/waves/round-38/wave1/`), plus scratch `/fast/scratch/hyaku/kasegi-r38/SimplReport/` (removed
after the receipt was written; §8). No deliverable sidecar — the item is receipt-only, so the landable
bytes sit in the one `## DELIVERABLE` block (§5). No mutating git/jj command; no tool installed or
upgraded; no pacman transaction attempted (host-wide pause).

---

## 1. Contract authority (what "conformant" means, literally)

| source | clause | bytes |
|---|---|---|
| `.ufo/prompts/kasegi-round-38.md` | §4 required sections, in order: Work performed; Landed changes; Before → after measurements; Sources & frontier; Trend verdicts; SHONEN | `:99-121` |
| same | marker rule: *"placeholder text, missing required sections other than **Sources & frontier** and **Trend verdicts**, or no evidence pointers … counts as the round **failed**"* | `:122-126` |
| same | per-wave record: *"Record the round shape, each wave's seat count, role mix and dead seats, any residual call, and the round total in the report"* | `:307-309` |
| same | §6.6 report extras: canonical **Trend verdicts**; a `Stale-lane` line (respawn-per-round driver; no other mission open); any tool installs | `:446-448` |
| same | §6 (v2 shape) attack share: *"≥25% of its seats attack roles (reviewer, critic, mutation-tester, labrat)"* | `:282-284` |
| same | §5 L0 side channel: an open operator question is named in the report, never blocked on | `:136-139` |
| `SHONEN.md` (lane) | four distinct box titles over four historical blocks: `grep -cE '^- \[[ x~]\]' SHONEN.md` → `16`; distinct titles → `4` | `SHONEN.md:9,25,38,58,…` |

**Box-count derivation** (the number the SHONEN section is graded against):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -hoE '^- \[[ x~]\] [^—(]*' SHONEN.md | sed -E 's/^- \[[ x~]\] //; s/[[:space:]]+$//' | sort -u | wc -l
4
```

The four titles: `SKILL.md contains real decision tables, error patterns, checklists, cited sources`;
`At least one end-to-end domain task executed and logged in LOG.md`; `Instructions executable by an
agent without oral context`; `No cross-domain bleed` (title truncates at the parenthetical
`(PROVINCE.md still accurate)`, which is why the box-4 prose check in §4/§5 looks for the amendment
evidence, not the adjective).

`grep -c '^## SHONEN'` = 1 is **necessary, not sufficient** — a heading with zero boxes passes it. The
box-line and box-signature checks (A3/B1–B3 in §5) carry the load.

---

## 2. Present state (why this lint is prospective)

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T18:41:57Z
$ ls -la /home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md
ls: cannot access '/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md': No such file or directory
$ ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-38/
chousa.md kaidoku.md kake.md kama.md kengaku.md kotodama.md kumitate.md mado.md mori.md tameshi.md tsukuroi.md
```

The round-38 report does not exist at 18:41:57Z and again at 18:43:06Z (two reads, 69 s apart); no
report draft exists under `.ufo/waves/round-38/wave1/` either. So this seat delivers the **check list the
L1 runs when it files**, calibrated now against controls whose outcome is already known (§4). Nothing
below claims to have been run on the round-38 report, because that file cannot be read yet.

Round-38 contract deltas against round 37 (each one is a grep in §5):

- the `Wave shape:`/`Round shape:` line must reconcile with the dispatched wave: `python3 -c` over
  `.ufo/waves/round-38/wave1-spec.json` → `items` count **73**, role mix `executor 21, scribe 15,
  reviewer 11, critic 7, mutation-tester 6, scout 6, connector 3, sentinel 2, simplifier 2`; attack
  roles (reviewer + critic + mutation-tester for a v2 wave) `24/73 = 32.9 %` ≥ 25 %;
- the judged head is **named only by reference** — `export-ref=` in
  `.ufo/waves/round-38/final-gates/all-gates.txt` — and no other head may wear a "final" label
  (claims.json `judged_head_rule`; round-37 defect D-B);
- `Final lane commit:` must not appear in the report at all (round-37 defect D-D);
- the round-37 lesson's `⟨pending` markers must stay at 0 and the report must not reintroduce them
  (D-C); the ledger's filled section is `corpus/knowledge/considerthese-proposals-ledger.md:45`
  (`## Round-37 dispositions — filled (round 38)`), while the empty r37 heading remains at `:37`
  append-only (D-F);
- SHONEN box 4 needs the G1 fence/`declared-blocks.txt` result, not the words "still accurate"
  (round-37 D-A contradicted that box).

---

## 3. Overreach sentence classes to avoid (round-37 report × verifier §1/§5)

Every class below was shipped by the round-37 report and routed by the non-author verifier
(`corpus/lessons/round-37-verifier-spotcheck.md`). The quoted sentences are **reading matter for the
L1 — never copy them into the round-38 report**; §5's section F greps them to 0.

| # | class | round-37 evidence | why it was false | round-38 form | grep |
|---|---|---|---|---|---|
| O1 | universal closure over routed defects | `kasegi.md:41` "after: all six routed defects closed (E10–E14 green)" | D3 had no E-check and recurred: `83975acc` landed 28 s after `complete` (verifier `:79-81`, `:175-177`) | name each defect with its G-check, one per line; never "all … closed" | F1 |
| O2 | unmeasured quiescence | `kasegi.md:41` "quiescent at filing (worktree clean, scratch empty)" | `/fast/scratch/hyaku/kasegi-r37/build-spec.py` remained (verifier `:181-183`) | print the two counters: `git status --porcelain \| wc -l` and the `find … \| wc -l` | D3, D5, F2, F3 |
| O3 | "final" label on a head that is not the judged head | `kasegi.md:8` "Measured at the final lane head `2387dcf6`"; `:15` "`aa88877b` (F2 final head …)"; `:73` "(round 37, final head `2387dcf6`)" | three artifacts named three "final" heads: report `2387dcf6`, `SCORECARD.md`/`SHONEN.md` `aa88877b`, receipt `9492c776` (verifier `:36-38`, §5 D-B `:165-168`) | "judged head J" (by reference) and "lane tip Y"; never `final head` | F8, F9, D1 |
| O4 | completeness claim the results file does not back | `kasegi.md:11` "Dead seats: 0 — all 64 receipts filed (… `wave1-results.json` had not finalised at filing …)" | the sentence asserts the total in the same breath as admitting the artifact is unfinished; the results commit landed after `complete` (verifier `:34-36`, §5 D3 `:175-177`) | if the sentence stays, it must name the committed `results.json` and its hash | F10 |
| O5 | "every change is tied to …" universal | `kasegi.md:15` "Every change is tied to the round-37 LOG entry and to commits `224df74d` … `2387dcf6`" | the enumeration omitted the post-`complete` commit `83975acc`; the report itself later added a WAVE-DONE addendum (`:88`) | "the changes listed below", or an enumeration that is literally complete | F5 |
| O6 | range notation wider than the checked set | `kasegi.md:8` "routed defects D1–D6"; `:68` "routed defects D1–D6 close" | the frozen predicate names D1, D2, D4, D5, D6 only; D3 was unaddressed (verifier `:79-81`) | spell `D-A → G1`, `D-B → G2`, … never a dash range | F7 |
| O7 | landed-artifact claim contradicted by the tree | `kasegi.md:25` "`considerthese-proposals-ledger.md`: round-37 18-row disposition table" | the section was an empty heading at `corpus/knowledge/considerthese-proposals-ledger.md:37-39` (D-F, L1-found) | every landed claim carries a counting command over committed bytes at J | B11, B12, G1–G14 |
| O8 | SHONEN box evidence contradicted by a same-round defect | `kasegi.md:76` box 4 "(PROVINCE.md still accurate) — evidence: PROVINCE.md F20 amendment appended" | the r37 `PROVINCE.md:80-152` append carried a whole receipt's scaffolding with unbalanced fences (verifier `:113-121`, §5 D-A `:159-163`) | box 4 cites the G1 fence/`declared-blocks.txt` equality | B7 |
| O9 | unqualified verdict while an offsetting defect is open | `kasegi.md:68` "**quality: improved** — … no admitted entry failed a re-check" | D-A and D-C were record defects open at filing; the verifier could accept the verdict only with an explicit offset clause (`:151-153`) | keep the enum token, add the `Offsetting defects:` clause | G14 |
| O10 | evidence adjective instead of evidence | `kasegi.md:8` "(genuine transcript of the F1 run, `all-gates v1` header, suite digest bound …)" | the judge could not execute it: "Not verified by this judge: a committed transcript of a run over A" (verifier `:75-77`) | the receipt's digest binding is the evidence; drop adjectives | F6 |

Two round-37 behaviours that are **not** sentence classes but are routed defects, and their report-side
consequence: D3 — a lane commit landing after `complete` must be disclosed as a post-measurement commit
with its hash, never folded into the measured state; D-C/D-F — the round-38 lesson and ledger must show
zero `⟨pending` markers and a filled ledger section before the report cites them (G3/G7 own the checks;
the report cites their outputs).

---

## 4. Calibration — every check executed on controls

**Harness.** `report-lint38.sh` (sha256 `39dee7f5295be364c6c5d09a8919040c3d30f61a91e06cfc8e787b87e405e182`,
180 lines) is the executable form of §5 with assertions and a `PASS/FAIL` line per id: 26 checks over
the report bytes (`S*`, `V*`) plus 6 filing checks (`F1`–`F6`), with a 7th filing check (the live suite
run) behind `RUN_SUITE=1`. Runs below use `SKIP_FILING=1` — the report does not exist yet (§2). Controls (all read-only, scratch copies):

| control | sha256 | bytes | result |
|---|---|---|---|
| `fixture-positive.md` (synthetic conformant report, never landable) | `3d0d567ff8a24f3697b87924a5e573931449a9ef98520cb457ea9a58769a747d` | 72 lines | `CHECKS=26 FAILS=0` — the list is satisfiable |
| `r37-published.md` (round-37 report verbatim) | `e4b4d7f571dc5dce932a7cc96885e44b4e52312a84817994b688f78b5267933f` | 88 lines | `CHECKS=26 FAILS=9` — mapped below |

Round-37 report failures, each attributable:

| check | observed | attributable to |
|---|---|---|
| `S3b` | `tilde=4 with_pointer=2` | boxes 2 and 4 (`:74`, `:76`) carry no backticked pointer or hash — a real conformance miss |
| `S3e` | `0` | box 4 cites "PROVINCE.md F20 amendment appended", no G1/fence result (O8) |
| `S5` | `stated=64 spec=73` | cross-round artifact of the calibration stub — S5 is only meaningful against the round's own `wave1-spec.json` |
| `S7` | `hashed_bullets=1` | `Landed changes` is a bullet list whose only hash sits in the preamble `:15`, not per change |
| `S8` | `blocks=0` | no per-claim `### ` blocks (round-37 used bold labels); the §5 form requires one block per claim |
| `V1` | 12 frozen values absent | round mismatch (r38 values by definition absent from a r37 report) |
| `V3` | `all six routed defects closed=1`, `scratch empty=1`, `quiescent at filing=1`, `every change is tied=1`, `genuine transcript=1`, `D1–D6=3` | exactly the verifier's routed overreach (O1, O2, O5, O6, O10) |
| `V4` | `final_lane_commit=2` | `:28` and `:41` both carry `Final lane commit: <hash>` (D-D class) |
| `V5` | `J=aaaaaaaa occurrences=0` | round mismatch (the r38 judged head cannot appear in a r37 report) |

**Harness ↔ deliverable ids.** The harness names its checks `S*`/`V*`; the deliverable names them by
section. Mapping by subject: `S0`→A1, `S1a`→A2, `S2`→A3, `S12`→A4, `S11`→A5, `S6`→A6, `S3*`→B1–B9,
`S8`→B10, `S7`→B11/B12, `S4`→C1–C3/C6, `S5`→C4, `S5b`→C5, `S9`→H1–H6, `S10`→G13, `V1`→G1–G12,
`V2`→E1–E4, `V3`→F1–F7, `V4`→F8/F9, `V5`→D1, `V6`→F7 (per-defect mapping), `V7`→E5. The mutants table
below uses harness ids for that reason.

**Mutants.** Sixteen single-defect edits of `fixture-positive.md`; each fires its intended check and no
other (except where the defect genuinely breaks two):

| mutant | defect injected | failing checks |
|---|---|---|
| m1 | duplicate `## SHONEN` heading | `S1a S2` |
| m2 | `## Trend verdicts` renamed | `S1b S10` |
| m3 | `## Landed changes` moved after `Before → after` | `S1a` |
| m4 | one SHONEN box deleted | `S3 S3c S3e` |
| m5 | `⟨pending` marker inserted | `V2` |
| m6 | judged-head run changed to `closed=6/8` | `V1` |
| m7 | "all seven routed defects closed" inserted | `V3` |
| m8 | `Final lane commit: deadbeef` inserted | `V4` |
| m9 | shape line `73 seats` → `64 seats` | `S5` |
| m10 | `SOURCES.md` counting command removed | `S9` |
| m11 | seat-receipt scaffolding heading pasted | `V7` |
| m12 | attack share `24/73` → `12/73` | `S5b` |
| m13 | `Stale-lane` removed from section and shape line | `S4` |
| m14 | one `[~]` line stripped of its pointer | `S3b` |
| m15 | judged head J relabelled to another hash | `V5` |
| m16 | box 4 evidence replaced by "amendment appended" | `S3b S3e` |

No check false-fires on legitimate quoting: the fixture passes `V3` and `V7` while quoting frozen
values, and the r37 report passes `V6` (every one of its seven `D-` tokens sits on a line that names an
E-check), so `V6` is not a blanket ban on defect ids.

---

## 5. DELIVERABLE

The landable bytes: the check list the L1 runs at filing. `89` lines, sha256
`6429d17bc2f137ec73eaf9c91c5a31111475846804a1f4ad9b0d929e77b59bf8`. Run from the fleet root; every
check prints a number to compare against its `# expected` annotation. The `sec()` helper and the
`J`/`Y` derivation are part of the block.

```bash
# round-38 report contract — exact checks (run at filing, from the fleet root)
R=.ufo/reports/round-38/kasegi.md
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
J=$(grep -m1 -oE 'export-ref=[0-9a-f]{40}' "$L/.ufo/waves/round-38/final-gates/all-gates.txt" | cut -d= -f2)
Y=$(git -C "$L" rev-parse master)
sec() { awk -v h="## $1" 'index($0,h)==1 && length($0)==length(h){f=1;next} /^## /{f=0} f' "$R"; }

## A. shape of the report
wc -l < "$R"                                                              # [A1] >= 40
grep -nE '^## (Work performed|Landed changes|Before → after measurements|Sources & frontier|Trend verdicts|SHONEN)$' "$R"   # [A2] 6 lines, one each, ascending
grep -c '^## SHONEN' "$R"                                                 # [A3] 1
grep -cE '[0-9a-f]{7,40}' "$R"                                            # [A4] >= 5
grep -coE '`[^`]*(bash|python3|grep|git |ls |scripts/)[^`]*`' "$R"        # [A5] >= 5
sec 'Work performed' | grep -cE 'C1|C2'                                   # [A6] >= 1 (claims named)

## B. SHONEN — one line per box, pointers, no over-claim
sec SHONEN | grep -cE '^- \[[x~]\]'                                       # [B1] 4
sec SHONEN | grep -cE '^- \[[^x~ ]\]'                                     # [B2] 0
sec SHONEN | grep -cF 'SKILL.md'                                          # [B3] >= 1
sec SHONEN | grep -cE 'end-to-end|domain task|LOG\.md'                    # [B4] >= 1
sec SHONEN | grep -cE 'oral context|executable'                           # [B5] >= 1
sec SHONEN | grep -cE 'cross-domain|PROVINCE'                             # [B6] >= 1
sec SHONEN | grep -F 'cross-domain' | grep -cE 'G1|declared-blocks|fence' # [B7] >= 1
sec SHONEN | grep -cE '^- \[x\]'                                          # [B8] 0, or every [x] names a verifier
sec SHONEN | awk '/^- \[/{if(n&&t)print buf; buf=$0; n=1; t=($0 ~ /^- \[~\]/); next} {if(n)buf=buf" "$0} END{if(n&&t)print buf}' | sed -E 's/`?\[~\]`?//g' | grep -cE '`[^`]+`|[0-9a-f]{7,40}'   # [B9] 4 = one pointer per [~] line

## B2. per-claim blocks and hashed landings
sec 'Before → after measurements' | grep -cE '^### '                     # [B10] 2 (one per claim)
sec 'Landed changes' | grep -cE '^(\||- ).*[0-9a-f]{7,40}'               # [B11] >= 3 rows/bullets, each with its commit
sec 'Landed changes' | grep -c 'LOG\.md'                                  # [B12] >= 1

## C. extras and round shape
grep -c 'Stale-lane' "$R"                                                 # [C1] >= 1
grep -ci '^## Tooling\|^Tooling:' "$R"                                    # [C2] >= 1
grep -ci 'residual call' "$R"                                             # [C3] >= 1
grep -nE '^(Wave|Round) shape:' "$R"                                      # [C4] 1 line: "<N> seats" (N = items in wave1-spec.json = 73), "Dead seats", "Round total: N"
grep -oE 'attack[^)]*' "$R" | grep -oE '[0-9]+/[0-9]+' | head -1          # [C5] n/d with 100n >= 25d
grep -cE 'L0[: ]' "$R"                                                    # [C6] >= 1 (open L0 named or "unchanged")

## D. judged head and receipt binding (D-B / D-D)
grep -cF "$J" "$R"                                                        # [D1] >= 1
git -C "$L" diff --name-only "$J" "$Y"                                    # [D2] exactly .ufo/waves/round-38/final-gates/all-gates.txt
git -C "$L" status --porcelain | wc -l                                    # [D3] 0
git -C "$L" merge-base --is-ancestor "$J" "$Y"; echo $?                   # [D4] 0 (J is an ancestor of Y)
find /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38 -mindepth 1 | wc -l   # [D5] 0
bash "$L"/corpus/instruments/r38-closure.sh --export-ref "$J"             # [D6] closed=8/8 exit=0

## E. placeholders and scaffolding == 0
grep -c '⟨' "$R"                                                          # [E1] 0
grep -c '\[MEASURE' "$R"                                                  # [E2] 0
grep -cE '\b(TODO|TBD|FIXME|PLACEHOLDER|XXX|INSERT)\b' "$R"               # [E3] 0
grep -cE 'Draft status|\(skeleton\)|[Ss]keleton|^#[^#]*DRAFT' "$R"        # [E4] 0
grep -cE '^## [0-9]+\. |Validation on a scratch mirror|^## Report$' "$R"  # [E5] 0

## F. overreach classes from round 37 (verifier §2/§5) == 0
grep -cE 'all (six|seven|eight|[0-9]+) routed defects closed|all routed defects (are )?closed' "$R"   # [F1] 0
grep -c 'scratch empty' "$R"                                              # [F2] 0
grep -c 'quiescent at filing' "$R"                                        # [F3] 0
grep -cE 'no harm anywhere|fully verified' "$R"                           # [F4] 0
grep -ci 'every change is tied' "$R"                                      # [F5] 0
grep -cE 'genuine transcript' "$R"                                        # [F6] 0
grep -cE '\bD1 ?[–-] ?D6\b|D-A ?\.\.[ ]?D-F' "$R"                         # [F7] 0 (name each defect with its G-check)
grep -iE 'final (lane )?head' "$R" | grep -vciE 'round-37|r37'            # [F8] 0
grep -cE 'Final lane commit: *`?[0-9a-f]{7,40}' "$R"                      # [F9] 0
grep -E 'all [0-9]+ (receipts|seats) filed' "$R" | grep -vE 'results\.json.*[0-9a-f]{7,40}|[0-9a-f]{7,40}.*results\.json' | grep -c .   # [F10] 0 (a completeness claim must name the committed results file)

## G. frozen after-values present (claims.json) — each >= 1
grep -c 'closed=8/8' "$R"                                                 # [G1] >= 1
grep -c 'selftest cases=8' "$R"                                           # [G2] >= 1
grep -c 'entries=24 pass=24' "$R"                                         # [G3] >= 1
grep -c 'records=45 bound=45' "$R"                                        # [G4] >= 1
grep -c 'expected=50' "$R"                                                # [G5] >= 1
grep -c 'S055' "$R"                                                       # [G6] >= 1
grep -c 'a173b0c2' "$R"                                                   # [G7] >= 1 (base red)
grep -c '2387dcf6' "$R"                                                   # [G8] >= 1 (r37 judged-head red)
grep -c 'exit 2' "$R"                                                     # [G9] >= 1 (plain run refused)
grep -cE '(→|->) ?`?21' "$R"                                              # [G10] >= 1 frontier 21
grep -cE '(→|->) ?`?55' "$R"                                              # [G11] >= 1 registry 55
grep -cE '(→|->) ?`?50' "$R"                                              # [G12] >= 1 knowledge 50
sec 'Trend verdicts' | grep -cE '(expansion|quality|discernment):? ?\**\s*(improved|harmed|unchanged|unprovable-but-better)'   # [G13] 3
sec 'Trend verdicts' | grep -i 'quality' | grep -ci 'offset'               # [G14] >= 1 (offset line for any still-open defect)

## H. Sources & frontier limbs (prompt §4)
sec 'Sources & frontier' | grep -cE '[0-9]+ ?(→|->) ?`?[0-9]+'            # [H1] >= 1 (rows before -> after)
sec 'Sources & frontier' | grep -ci 'added by tier'                       # [H2] >= 1
sec 'Sources & frontier' | grep -ci 'touched'                             # [H3] >= 1
sec 'Sources & frontier' | grep -ciE 'frontier .*(advanced|row|rows)'     # [H4] >= 1
sec 'Sources & frontier' | grep -ciE 'assimilation|SOURCES: unchanged —'  # [H5] >= 1
sec 'Sources & frontier' | grep -cE '`[^`]*(grep -c|python3|awk)[^`]*SOURCES\.md'   # [H6] >= 1 (a counting command over SOURCES.md)
```

---

## 6. What this checklist does not certify

- **Truth of the numbers.** B11/B12 and G1–G14 check that commands, hashes and values are *present*; only
  `r38-closure.sh --export-ref "$J"` (D6) executes the claim. The report's job is to make each number
  re-derivable; the non-author closure re-derives the rest.
- **That `[~]` pointers resolve.** B9 accepts any backticked token; whether
  `.ufo/waves/round-38/wave1/RevNoHarm.md` says what box 1 claims is the verifier's read.
- **Verdict quality.** G13 checks three verdicts from the frozen vocabulary, not that `improved` is
  earned.
- **D3's residual.** G4 (in the suite) can only observe that a round-38 `*-results.json` exists at J;
  a commit landing after `complete` is visible only in hindsight, so the report must disclose one if it
  happens (§3, O4/D3) — no grep can prove its absence.
- **A non-existent report cannot be linted.** §5 was calibrated, not executed against
  `.ufo/reports/round-38/kasegi.md`; at 18:43:06Z that path still returned ENOENT.
- **No deletion is proposed and no `lsp` `references` proof applies**: the artifacts are Markdown prose,
  not code with a call graph. Every statement in §2–§4 rests on the literal command output printed
  above.

---

## 7. Appendix — harness (scratch-only, `39dee7f5…`, 180 lines)

The executable form of §5 (same checks, with assertions and `FAILS=<n>`). It is not a deliverable and
its scratch copy is removed; it is reproduced here so the calibration in §4 stays reproducible after
that removal.

```bash
#!/usr/bin/env bash
# report-lint38.sh <report> [lane-root] — round-38 kasegi report contract lint, read-only.
# Byte checks run always. Filing checks run unless SKIP_FILING=1.
# Env: LANE (default the kasegi lane), ONLINE=1 to also hit the remote.
set -u
R=${1:?report path}
LANE=${2:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
FLEET=/home/vgpnk/Projects/shokunin
nfail=0; ncheck=0
say() { printf '%-4s %-38s %-4s %s\n' "$1" "$2" "$3" "$4"; }
ok()  { ncheck=$((ncheck+1)); say "$1" "$2" PASS "$3"; }
bad() { ncheck=$((ncheck+1)); nfail=$((nfail+1)); say "$1" "$2" FAIL "$3"; }
sec() { awk -v h="## $1" 'index($0,h)==1 && length($0)==length(h) {f=1;next} /^## /{f=0} f' "$R"; }
blk() { sec "$1" | awk '/^- /{if(n)print buf; buf=$0; n=1; next} {if(n)buf=buf" "$0} END{if(n)print buf}'; }
hex() { grep -oE '[0-9a-f]{7,40}' <<<"$1" | sort -u; }

J=$(grep -m1 -oE 'export-ref=[0-9a-f]{40}' "$LANE/.ufo/waves/round-38/final-gates/all-gates.txt" 2>/dev/null | cut -d= -f2)
Y=$(git -C "$LANE" rev-parse master 2>/dev/null || true)
Js=$J; Ys=${Y:-}; [ -n "$Js" ] || Js=$(printf '0%.0s' {1..40})

# S0 contentful length
n=$([ -f "$R" ] && wc -l <"$R" || echo 0)
[ "$n" -ge 40 ] && ok S0 'exists, >=40 lines' "lines=$n" || bad S0 'exists, >=40 lines' "lines=$n"

# S1 six required sections, once each, in order
want=("Work performed" "Landed changes" "Before → after measurements" "Sources & frontier" "Trend verdicts" "SHONEN")
marker=(1 1 1 0 0 1)
prev=0; a_ok=1; b_ok=1; a_det=""; b_det=""
for i in "${!want[@]}"; do
  h=${want[$i]}
  c=$(grep -cFx "## $h" "$R"); ln=$(grep -nFx "## $h" "$R" | cut -d: -f1 | head -1)
  if [ "$c" = 1 ] && [ "${ln:-0}" -gt "$prev" ]; then prev=$ln; det=$ln; elif [ "$c" = 1 ]; then det="$ln(ORDER)"; else det="count=$c"; fi
  if [ "${marker[$i]}" = 1 ]; then
    case "$det" in *ORDER*|count*) a_ok=0;; esac; a_det="$a_det ${h%% *}:$det"
  else
    case "$det" in *ORDER*|count*) b_ok=0;; esac; b_det="$b_det ${h%% *}:$det"
  fi
done
[ "$a_ok" = 1 ] && ok S1a 'marker sections present+ordered' "$a_det" || bad S1a 'marker sections present+ordered' "$a_det"
[ "$b_ok" = 1 ] && ok S1b 'conformance sections present+ordered' "$b_det" || bad S1b 'conformance sections present+ordered' "$b_det"

# S2 prompt gate
c=$(grep -c '^## SHONEN' "$R")
[ "$c" = 1 ] && ok S2 "grep -c '^## SHONEN'" "1" || bad S2 "grep -c '^## SHONEN'" "$c"

# S3 four box lines, valid tokens, four signatures
boxes=$(sec SHONEN | grep -cE '^- \[[ x~]\]'); tok=$(sec SHONEN | grep -cE '^- \[[^x~ ]\]')
[ "$boxes" = 4 ] && [ "$tok" = 0 ] && ok S3 'SHONEN 4 box lines' "boxes=4 bad_token=0" || bad S3 'SHONEN 4 box lines' "boxes=$boxes bad_token=$tok"
sigs=('SKILL\.md' 'end-to-end|domain task|LOG\.md' 'oral context|executable' 'cross-domain|PROVINCE')
smiss=0; sdet=""; i=0
for sg in "${sigs[@]}"; do i=$((i+1)); k=$(sec SHONEN | grep -cE "$sg"); sdet="$sdet $i:$k"; [ "$k" -ge 1 ] || smiss=$((smiss+1)); done
[ "$smiss" = 0 ] && ok S3c 'SHONEN four signatures' "$sdet" || bad S3c 'SHONEN four signatures' "$sdet"
til=$(sec SHONEN | grep -cE '^- \[~\]')
tilp=$(sec SHONEN | awk '/^- \[/{if(n&&t)print buf; buf=$0; n=1; t=($0 ~ /^- \[~\]/); next} {if(n)buf=buf" "$0} END{if(n&&t)print buf}' | sed -E 's/`?\[~\]`?//g' | grep -cE '`[^`]+`|[0-9a-f]{7,40}')
[ "$til" = "$tilp" ] && ok S3b '[~] each carries a pointer' "tilde=$til with_pointer=$tilp" || bad S3b '[~] each carries a pointer' "tilde=$til with_pointer=$tilp"
xb=$(sec SHONEN | grep -cE '^- \[x\]'); xv=$(sec SHONEN | grep -E '^- \[x\]' | grep -icE 'verif(y|ied)|verifier|spot-check')
if [ "$xb" = 0 ] || [ "$xb" = "$xv" ]; then ok S3d '[x] carries a verifier' "x=$xb with_verifier=$xv"; else bad S3d '[x] carries a verifier' "x=$xb with_verifier=$xv"; fi

b4=$(sec SHONEN | grep -F 'cross-domain' | grep -cE 'G1|declared-blocks|fence')
[ "$b4" -ge 1 ] && ok S3e 'box-4 cites G1 fence evidence' "$b4" || bad S3e 'box-4 cites G1 fence evidence' "$b4"

# S4 extras: Stale-lane, Tooling, residual call, L0
e1=$(grep -c 'Stale-lane' "$R"); e2=$(grep -ci '^## Tooling\|^Tooling:' "$R"); e3=$(grep -ci 'residual call' "$R"); e4=$(grep -cE 'L0[: ]' "$R")
if [ "$e1" -ge 1 ] && [ "$e2" -ge 1 ] && [ "$e3" -ge 1 ] && [ "$e4" -ge 1 ]; then ok S4 'Stale-lane/Tooling/Residual/L0' "$e1/$e2/$e3/$e4"; else bad S4 'Stale-lane/Tooling/Residual/L0' "stale=$e1 tooling=$e2 residual=$e3 l0=$e4"; fi

# S5 round shape: seat total == dispatch count, role mix, dead seats, round total
spec_n=$(python3 -c "import json;print(json.load(open('$LANE/.ufo/waves/round-38/wave1-spec.json'))['items'].__len__())" 2>/dev/null || echo 0)
shape=$(grep -nE '^(Wave|Round) shape:' "$R" | head -1)
if [ -n "$shape" ] && grep -qE '[0-9]+ seats' <<<"$shape" && grep -q 'Dead seats' <<<"$shape" && grep -qE 'Round total: [0-9]+' <<<"$shape"; then
  stated=$(grep -oE '[0-9]+ seats' <<<"$shape" | head -1 | grep -oE '[0-9]+')
  atk=$(grep -oE 'attack[^)]*' <<<"$shape" | grep -oE '[0-9]+/[0-9]+' | head -1)
  if [ "$stated" = "$spec_n" ]; then ok S5 'round shape (seats/dead/total)' "stated=$stated spec=$spec_n"; else bad S5 'round shape (seats/dead/total)' "stated=$stated spec=$spec_n"; fi
  an=${atk%%/*}; ad=${atk##*/}
  if [ -n "$atk" ] && [ "$ad" -gt 0 ] && [ $((an*100)) -ge $((ad*25)) ]; then ok S5b 'attack share >=25%' "$atk"; else bad S5b 'attack share >=25%' "${atk:-absent}"; fi
else bad S5 'round shape (seats/dead/total)' "shape_line=${shape:-absent}"; bad S5b 'attack share >=25%' "no shape line"; fi

# S6 claims named
c=$(sec 'Work performed' | grep -cE 'C1|C2')
[ "$c" -ge 1 ] && ok S6 'claims named in Work performed' "claim_tokens=$c" || bad S6 'claims named in Work performed' "0"

# S7 Landed rows carry a hash; LOG named
rows=$(sec 'Landed changes' | awk -F'|' '/^\|/{c=$2; gsub(/[[:space:]]/,"",c); if(c==""||c=="Change"||c ~ /^-+$/) next; n++} END{print n+0}')
wh=$(sec 'Landed changes' | awk '/^- /{if(n)print buf; buf=$0; n=1; next} {if(n)buf=buf" "$0} END{if(n)print buf}' | grep -cE '[0-9a-f]{7,40}')
log=$(sec 'Landed changes' | grep -c 'LOG\.md')
[ "$wh" -ge 3 ] && [ "$log" -ge 1 ] && ok S7 'Landed changes hash+LOG' "hashed_bullets=$wh log=$log" || bad S7 'Landed changes hash+LOG' "hashed_bullets=$wh log=$log"

# S8 before->after: 2 claim blocks, commands, measured commit
nb=$(sec 'Before → after measurements' | grep -cE '^### ')
cmds=$(sec 'Before → after measurements' | grep -cE '`[^`]*(bash|python3|grep|ls |git |scripts/)[^`]*`')
meas=$(sec 'Before → after measurements' | grep -ciE 'measured at|at `?[0-9a-f]{7}|before .*after ')
[ "$nb" -ge 2 ] && [ "$cmds" -ge 2 ] && [ "$meas" -ge 2 ] && ok S8 'Before→after blocks' "blocks=$nb cmd_lines=$cmds measured=$meas" || bad S8 'Before→after blocks' "blocks=$nb cmd_lines=$cmds measured=$meas"

# S9 Sources & frontier limbs
s=$(sec 'Sources & frontier'); mis=""
p() { local pat=$1 nm=$2; printf '%s\n' "$s" | grep -qiE "$pat" || mis="$mis $nm"; }
p 'SOURCES\.md' sources; p '[0-9]+ ?(→|->) ?`?[0-9]+' rows_arrow; p 'added by tier' tier
p 'touched' touched; p 'frontier .*(advanced|row|rows)' frontier; p 'assimilation|SOURCES: unchanged —' assim
p '`[^`]*(grep -c|python3|awk)[^`]*SOURCES\.md' counting_cmd
[ -z "$mis" ] && ok S9 'S&F limbs' "7/7" || bad S9 'S&F limbs' "missing:$mis"

# S10 Trend verdicts: three, enum, no scalar
t=$(sec 'Trend verdicts'); v=""
for k in expansion quality discernment; do
  kk=$(printf '%s\n' "$t" | grep -cE "$k:? ?\**\s*(improved|harmed|unchanged|unprovable-but-better)"); v="$v $k:$kk"
done
[ "$v" = " expansion:1 quality:1 discernment:1" ] && ok S10 '3 trend verdicts, enum' "$v" || bad S10 '3 trend verdicts, enum' "$v"

# S11 pointer floor
ptrs=$(grep -coE '`[^`]*[/:][^`]*`|[0-9a-f]{7,40}' "$R")
[ "$ptrs" -ge 20 ] && ok S11 'pointer floor >=20' "total=$ptrs" || bad S11 'pointer floor >=20' "total=$ptrs"

# S12 contentful marker rule
h=$(grep -coE '[0-9a-f]{7,40}' "$R"); cm=$(grep -coE '`[^`]*(bash|python3|grep|git |ls |scripts/)[^`]*`' "$R")
[ "$h" -ge 5 ] && [ "$cm" -ge 5 ] && ok S12 'contentful (hashes+commands)' "hashes=$h commands=$cm" || bad S12 'contentful (hashes+commands)' "hashes=$h commands=$cm"

# V1 frozen after-values must appear verbatim
vmiss=""
for pat in 'closed=8/8' 'selftest cases=8' 'entries=24 pass=24' 'records=45 bound=45' 'expected=50' 'S055' 'a173b0c2' '2387dcf6' 'exit 2' '(→|->) ?`?21' '(→|->) ?`?55' '(→|->) ?`?50'; do
  grep -qE "$pat" "$R" || vmiss="$vmiss $pat"
done
[ -z "$vmiss" ] && ok V1 'frozen after-values present' "12/12" || bad V1 'frozen after-values present' "missing:$vmiss"

# V2 placeholder classes
p1=$(grep -c '⟨' "$R"); p2=$(grep -c '\[MEASURE' "$R"); p3=$(grep -cE '\b(TODO|TBD|FIXME|PLACEHOLDER|XXX|INSERT)\b' "$R")
p4=$(grep -cE 'Draft status|\(skeleton\)|[Ss]keleton|^#[^#]*DRAFT' "$R"); p5=$(grep -cE '\$\{?ROUND3[0-9]' "$R")
[ $((p1+p2+p3+p4+p5)) = 0 ] && ok V2 'placeholders 0' "guillemet=0 measure=0 todo=0 draft=0 var=0" || bad V2 'placeholders 0' "guillemet=$p1 measure=$p2 todo=$p3 draft=$p4 var=$p5"

# V3 overreach phrases (minus lines that negate/supersede them)
ov=""
for ph in 'all (six|seven|eight|[0-9]+) routed defects closed' 'all routed defects (are )?closed' 'scratch empty' 'quiescent at filing' 'no harm anywhere' 'fully verified' 'every change is tied' 'genuine transcript' '\bD1 ?[–-] ?D6\b' 'D-A ?\.\.[ ]?D-F'; do
  tot=$(grep -icE "$ph" "$R"); neg=$(grep -iE "$ph" "$R" | grep -icE 'not |no longer|superseded|was not|is not')
  bad_n=$((tot-neg)); [ "$bad_n" -gt 0 ] && ov="$ov [$ph]=$bad_n"
done
[ -z "$ov" ] && ok V3 'no overreach phrase' "0/10 classes" || bad V3 'no overreach phrase' "$ov"

# V4 final-head label discipline: "final head" only for the r37 defect narrative; never a lane label
flc=$(grep -cE 'Final lane commit: *`?[0-9a-f]{7,40}' "$R")
fh=$(grep -icE 'final (lane )?head' "$R"); fhx=$(grep -iE 'final (lane )?head' "$R" | grep -vciE 'round-37|r37')
[ "$flc" = 0 ] && [ "$fhx" = 0 ] && ok V4 'final-head label discipline' "final_lane_commit=0 final_head_off_r37=0 (r37-context=$fh)" || bad V4 'final-head label discipline' "final_lane_commit=$flc final_head_off_r37=$fhx"

# V5 J named in the report and export-ref parity
jocc=$(grep -coF "$Js" "$R")
[ "$jocc" -ge 1 ] && ok V5 'judged head J named (export-ref)' "J=${Js:0:8} occurrences=$jocc" || bad V5 'judged head J named (export-ref)' "J=${Js:0:8} occurrences=$jocc (all-gates.txt export-ref)"

# V6 routed-defect dispositions: every D token carries a state word, no bare closure claim
dbad=0; ddet=""
for d in 'D-A' 'D-B' 'D-C' 'D3' 'D-D' 'D-E' 'D-F'; do
  hits=$(grep -cF "$d" "$R")
  if [ "$hits" -gt 0 ]; then
    stated=$(grep -F "$d" "$R" | grep -cE 'closed|held|routed|open|no check|check=|G[0-9]')
    [ "$stated" -eq 0 ] && { dbad=$((dbad+1)); ddet="$ddet $d"; }
  fi
done
[ "$dbad" = 0 ] && ok V6 'routed defects carry state' "7 tokens checked" || bad V6 'routed defects carry state' "bare:$ddet"

# V7 seat-receipt scaffolding must not appear in the report (D-A class)
sc=$(grep -cE '^## [0-9]+\. |^## DELIVERABLE|Validation on a scratch mirror|^## Report$' "$R")
[ "$sc" = 0 ] && ok V7 'no receipt scaffolding' "0" || bad V7 'no receipt scaffolding' "$sc"

# Filings
if [ "${SKIP_FILING:-0}" = 1 ]; then
  say F0 'filing checks' SKIP "SKIP_FILING=1"
else
  if git -C "$LANE" cat-file -e "$Js^{commit}" 2>/dev/null; then ok F1 'J resolves in lane' "${Js:0:8}"; else bad F1 'J resolves in lane' "${Js:0:8}"; fi
  pc=$(git -C "$LANE" status --porcelain | wc -l)
  [ "$pc" = 0 ] && ok F2 'lane porcelain 0' "0" || bad F2 'lane porcelain 0' "$pc"
  if git -C "$LANE" merge-base --is-ancestor "$Js" "$Ys" 2>/dev/null; then ok F3 'J ancestor of master tip' "${Js:0:8}->${Ys:0:8}"; else bad F3 'J ancestor of master tip' "${Js:0:8}->${Ys:0:8}"; fi
  df=$(git -C "$LANE" diff --name-only "$Js" "$Ys" 2>/dev/null)
  [ "$df" = ".ufo/waves/round-38/final-gates/all-gates.txt" ] && ok F4 'J..tip = receipt only' "$df" || bad F4 'J..tip = receipt only' "${df:-empty-or-unknown}"
  sc_n=$(find /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38 -mindepth 1 2>/dev/null | wc -l)
  [ "$sc_n" = 0 ] && ok F5 'scratch quiescent' "0 entries" || bad F5 'scratch quiescent' "$sc_n entries under /fast/scratch/hyaku/kasegi-r3[678]"
  rc=$(git -C "$FLEET" log --format=%s -1 -- .ufo/reports/round-38/kasegi.md 2>/dev/null)
  case "$rc" in *round-38*) ok F6 'report committed on fleet' "$rc";; *) bad F6 'report committed on fleet' "${rc:-none}";; esac
  if [ "${RUN_SUITE:-0}" = 1 ]; then
    out=$(cd "$LANE" && bash corpus/instruments/r38-closure.sh --export-ref "$Js" 2>&1); rcs=$?
    grep -q 'closed=8/8' <<<"$out" && [ "$rcs" = 0 ] && ok F7 "suite over J: $(tail -1 <<<"$out")" "exit=0" || bad F7 'suite over J' "exit=$rcs last=$(tail -1 <<<"$out")"
  fi
fi
echo "CHECKS=$ncheck FAILS=$nfail"
exit $((nfail>0))
```

---

## 8. Report

Seat `SimplReport` complete. Delivered: the round-38 report-contract check list (89 lines, sha256
`6429d17b…`) — 6 required sections in order with `grep -c '^## SHONEN'` = 1 and one line per SHONEN
box, the `Stale-lane`/`Tooling`/`residual call`/`Wave shape:`/`Round total:` lines, the judged-head
binding to `export-ref=` in `all-gates.txt`, and ten overreach classes lifted from the round-37 report
and its verifier §1/§5. Calibration: a synthetic conformant control passes 26/26; sixteen single-defect
mutants each fire the intended check; the published round-37 report fails nine checks, each mapped to a
verifier-routed defect or to a deliberate cross-round mismatch. Tooling: none installed or upgraded; no
pacman transaction attempted (host-wide pause). Scratch `/fast/scratch/hyaku/kasegi-r38/SimplReport/`
removed.
