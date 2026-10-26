# SimplReport — round-37 report-contract lint checklist

Seat `SimplReport` (report-contract linter, L2 leaf — no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the only lane repo). Read at base
`b56a41680cefd391868c1c370dc063c69d827e7d`, claims freeze `224df74db2a46d627ae1475a72ca48796bbd177c`,
lane HEAD/remote head `b362068195d5489aa94b31e6ec8f880c367e0ba0` (claims-erratum-1). Judged axis:
calibration. Milestone round-37.

**Item.** Lint the report contract — required sections in order, evidence pointers, `grep -c '^## SHONEN'` = 1,
no placeholder content — and deliver the checklist with the exact greps the L1 runs on the final report.

**Writes.** This receipt only — the one lane byte this seat authored (`git status --porcelain` shows it under
the untracked `.ufo/waves/round-37/wave1/`), plus scratch `/fast/scratch/hyaku/kasegi-r37/SimplReport/`
(removed after the receipt was written). No other lane byte, no fleet byte, no sibling-lane or source-tree
byte; no mutating git command; no tool installed or upgraded (no `pacman` transaction attempted — host-wide
pause). This receipt itself quotes the placeholder literal only to name the defect class — a quotation, not a slot (the same exemption `L5` gives the report's E1 row).

**Method.** Contract read from the fleet prompt `.ufo/prompts/kasegi-round-37.md` §4 and its marker rule
(`:99-130`), the pre-report gate (`:434-441`) and report extras (`:446-448`); precedents from the published
round-36 report (fleet `.ufo/reports/round-36/kasegi.md`) and `corpus/lessons/round-36-verifier-spotcheck.md` §1
(Step-1 conformance). Every check below was executed on **ten** controls (§4), not asserted.

---

## 1. Contract authority (what "conformant" means, literally)

| source | clause | bytes |
|---|---|---|
| `.ufo/prompts/kasegi-round-37.md` | §4 required sections, in order: Work performed; Landed changes; Before → after measurements; Sources & frontier; Trend verdicts; SHONEN | `:99-121` |
| same | marker rule: *"placeholder text, missing required sections other than **Sources & frontier** and **Trend verdicts**, or no evidence pointers … counts as the round **failed**"* | `:122-126` |
| same | pre-report gate: `grep -c '^## SHONEN' <report>` must print `1`, **followed by one `[~]`/`[ ]` line per SHONEN.md box** | `:438-440` |
| same | report extras: canonical Trend verdicts section, a `Stale-lane` line, tooling installs | `:446-448` |
| `SHONEN.md` (lane) | four distinct box titles, three rounds of history = 12 checkbox lines: `grep -cE '^\- \[[ x~]\]' SHONEN.md` → `12`; distinct titles → `4` | `SHONEN.md:9,25,38,58,…` |

**Box-count derivation** (the number the report's SHONEN section is graded against):

```
$ grep -hoE '^\- \[[ x~]\] [^—(]*' SHONEN.md | sed -E 's/^- \[[ x~]\] //; s/[[:space:]]+$//' | sort -u | wc -l
4
```

The four titles: `SKILL.md contains real decision tables, error patterns, checklists, cited sources`;
`At least one end-to-end domain task executed and logged in LOG.md`; `Instructions executable by an agent
without oral context`; `No cross-domain bleed (PROVINCE.md still accurate)`.

Calibration note on the marker rule: `grep -c '^## SHONEN'` = 1 is **necessary, not sufficient** — a heading
with zero boxes passes it. That is exactly the run-6 failure the prompt cites (kotoba r69/r71 "filed without
it"), so L2 and L3 are separate checks and L3 is the load-bearing one.

---

## 2. Present-state reading (the draft moved twice while this seat read it)

| read | digest | lines | `[MEASURE` |
|---|---|---|---|
| first read (12:0x) | earlier revision | 397 | 86 |
| pinned read for all numbers below | `78fc7987ef17eac66edff1ff3fb79cb2f26ab27e77f438ad8cfab649fcfba2ca` | 404 | 87 (11 of them bare `[MEASURE]`) |

Placeholders per section at `78fc7987`: Work performed 3, Landed changes 13, Before → after 37,
Sources & frontier 11, Trend verdicts 9, SHONEN 7, Round shape 5. Heading lines: Work performed `:32`,
Landed changes `:116`, Before → after `:144`, Sources & frontier `:252`, Trend verdicts `:295`, SHONEN `:333`,
extra `## Round shape` `:360`. Draft status text at `:1` (`DRAFT skeleton`) and `:8` (`Draft status: **skeleton**`).

---

## 3. The checklist (18 report-byte checks + 5 filing checks; contract clause → command → expected)

Run from the fleet root with `R=.ufo/reports/round-37/kasegi.md` and
`L=/home/vgpnk/Projects/shokunin/kasegi-shokunin`. The executable form is §7 (a script, because these are
section-scoped and a flat `grep` cannot see section boundaries). Severity: **[M]** = marker (a miss fails the
round), **[C]** = conformance defect (status `ok`, logged).

| id | sev | clause | check (script logic) | expected on the final report |
|---|---|---|---|---|
| L0 | [M] | report is contentful | `wc -l < $R` | `>= 40` (r36 precedent 87) |
| L1a | [M] | Work performed, Landed changes, Before → after, SHONEN present once each, in that order | `grep -cFx '## <h>' $R` for each; line numbers strictly increasing | `1,1,1,1` / increasing |
| L1b | [C] | Sources & frontier, Trend verdicts present once each, in order | same | `1,1` / increasing |
| L2 | [M] | prompt gate | `grep -c '^## SHONEN' $R` | `1` |
| L3 | [M] | one line per box | box lines inside the SHONEN section, `^- \[[ x~]\]` | `4`, invalid tokens `0` |
| L3c | [M] | lines are the four canonical boxes | each signature `SKILL\.md` / `end-to-end\|domain task\|LOG\.md` / `oral context\|executable` / `cross-domain\|PROVINCE` appears ≥1 | `4/4` |
| L3b | [C] | `[x]` only with a named non-author verifier | `[x]` lines containing `verif(y\|ied)\|verifier\|spot-check` | `x=0`, or `x == with_verifier` |
| L14 | [M] | `[~]` carries a resolvable pointer | per `[~]` **block** (continuations joined): a backticked token or 7–40 hex | `tilde == with_pointer` |
| L4 | [M] | "no placeholder text" | `grep -c '\[MEASURE'`; `grep -c '⟨'`; `grep -cE '\b(TODO\|TBD\|FIXME\|PLACEHOLDER\|XXX\|INSERT)\b'`; `grep -cE 'DRAFT\|Draft status\|\(skeleton\)\|[Ss]keleton'`; `grep -cE '\$\{?ROUND3[0-9]'` | all `0` |
| L5 | [C] | template literals are quoted provenance, not placeholders | occurrences of `<LANE_HASH>` / `filled by the L1` **outside** a line naming `E1` or carrying `grep -c` | `outside_E1=0` (both) |
| L6 | [M] | Work performed: claims named, one bullet per item each with a pointer | claim tokens `C1\|C2` ≥1; per bullet block a strict pointer (backticked span with `/` or `:`, or 7–40 hex), or a section-level `evidence under \`…/\`` declaration plus any backticked token | `strict_missing=0` (or `decl=1` and `any_missing=0`) |
| L7 | [M] | Landed changes: every change tied to a LOG entry **and** its commit | table data rows count vs rows containing a 7–40 hex; `LOG.md` named | `rows == with_hash`, `log_mention >= 1` |
| L8 | [M] | Before → after: one per claim, counting command + measured commit | `^### ` blocks; backticked command cells; `measured at` / hash per block | `blocks=2`, `command_cells>=2`, `measured>=2` |
| L9 | [C] | Sources & frontier limbs | `SOURCES.md` named; `N → N rows`; "added by tier"; "touched"; "frontier … advanced/row"; `assimilation` or `SOURCES: unchanged —`; **a `grep -c`/`python3`/`awk` counting command over `SOURCES.md`** | all `>= 1` (7/7) |
| L10 | [C] | Trend verdicts: three, enum vocab, no scalar | `expansion|quality|discernment` each followed by `improved|harmed|unchanged|unprovable-but-better` | `1/1/1` |
| L11 | [M] | "no evidence pointers" is a marker | total backticked-path/colon/hash occurrences; ≥1 per required section | `total >= 20`, `sections_missing=none` |
| L12 | [C] | report extras | `Stale-lane`; `Tooling`; `Open L0` | `1 / >=1 / >=1` |
| L13 | [M] | report names real committed work | 7–40 hex count; command-cell count; claims reference | `hashes>=5`, `commands>=5`, `claim_refs>=1` |

**Filing checks** (state, not bytes; run at filing — do not run these against a historical report):

| id | command | expected |
|---|---|---|
| F1 | `H=$(git -C $L ls-remote origin refs/heads/master \| cut -f1)`; `git -C $L cat-file -e $H`; `grep -cF "$H" $R` | remote head resolves and its **full 40-hex** appears in the report (r36 precedent: header names `a23dc478…`, erratum names `c20300df…`) |
| F2 | `git -C $L status --porcelain \| wc -l` | `0` |
| F3 | `git -C /home/vgpnk/Projects/shokunin log --format='%h %s' -1 -- .ufo/reports/round-37/kasegi.md` | one commit, subject `round-37: kasegi report` |
| F4 | `find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 -maxdepth 1 -type d \| wc -l` | `0` (E9's live limb) |
| F5 | `python3 -c 'import json;d=json.load(open("$L/.ufo/waves/round-37/claims.json"));[print(c["id"],x) for c in d["claims"] for x in c["counting_commands"]]'` | every frozen command's counter appears in Before → after / Sources & frontier, with the frozen after-values: SOURCES rows `53 → 54`; frontier `19 → 20`; knowledge `48 → 49`; `harness entries=23 pass=23`; `capture-binding records=44 bound=44`; `recheck-audit strict pass=49/49 expected=49`; `r37-closure.sh --export-ref <final>` `closed=14/14 exit=0`, `--selftest cases=14 failures=0`; both r36 exports `closed<14/14 exit=1` |

---

## 4. Calibration — every check executed on ten controls

Positive controls: `p0-counted.md` = the published r36 report with the missing SOURCES counting command
inserted (sha256 `e9741a6557200a089c1e82c2500c15ff902dc408e4f6534758390f4791a92978`);
`r36-published.md` = the r36 report verbatim (`d2081043d950525e9764cc2166bff6a9a9056518a28c4ca41199013052604020`);
`draft.md` = the round-37 draft at `78fc7987`. Mutants m1–m7 are single-defect edits of `p0-counted.md`.

| control | defect injected | failing checks | verdict |
|---|---|---|---|
| `p0-counted.md` | none | — (`FAILS=0`) | 18/18 pass — the checklist is satisfiable by a real published report |
| `r36-published.md` | none (as filed) | `L9` | `L9` = the counting command is absent — the **independently routed** r36 defect (`SimplReport` round-36 C6: "Sources & frontier lacks the row-counting command"). The checklist agrees with the outside review, and is stricter than the precedent exactly where the contract is explicit. |
| `m1` | second `## SHONEN` heading | `L1a L2` | duplicate heading caught by both the section check and the prompt's own grep |
| `m2` | `## Trend verdicts` renamed | `L1b L10 L11` | non-marker section loss caught; graded [C], not a round failure |
| `m3` | Landed changes moved after Before → after | `L1a L7 L8` | order violation caught at the marker level |
| `m4` | one SHONEN box deleted | `L3 L3c` | 3 boxes caught by the count and by the signature set |
| `m5` | one `[MEASURE: pending]` inserted | `L4` | placeholder class caught alone |
| `m6` | Before → after body emptied of commands/numbers | `L8 L11 L13` | pointer-floor and command checks catch it three ways |
| `m7` | one box flipped to `[x]` with no verifier | `L3b` | over-claim of verification caught |
| `draft.md` @`78fc7987` | in-flight skeleton | `L4 L6 L7 L9` | see §5 |

No check false-fires on prose that legitimately quotes a forbidden literal: `r36-published.md` carries
`grep -cF 'filled by the L1' SCORECARD.md` as a counter and passes `L5`; only a *bare* occurrence fails.

**Known false-positive classes** (deliberate, with the discriminator the L1 should apply):
1. `L4`'s `[Ss]keleton` limb fires on any sentence mentioning the drafting process. The filed report has no
   need for the word — delete it rather than exempting it.
2. `L5` expects the literals `<LANE_HASH>` / `filled by the L1` only on a line that carries `E1` or `grep -c`.
   If the E1 row wraps so the literal lands on a continuation line, `L5` fails on a correct report; keep the
   literal on the `E1` line.
3. `L1a`'s order detection stops advancing after an out-of-order heading, so a later heading can also be
   flagged `ORDER`. That over-reports, never under-reports; with `m3` it produced one true and no false
   attribution.

---

## 5. Defects in the draft at `78fc7987` (fix before filing; each with the exact reproduction)

**S1 [M] — 87 placeholder slots.** `grep -c '\[MEASURE' .ufo/waves/round-37/wave1/ScribeReportDraft.md` → `87`
(11 bare `[MEASURE]`); plus `DRAFT skeleton` (`:1`) and `Draft status: **skeleton**` (`:8`). Fix: fill from the
wave receipts and the post-integration gate run, drop both drafting paragraphs, retitle. A filed report
carrying these fails L4 and the marker rule.

**S2 [M] — 10 of 14 Landed-changes rows carry no commit.**
`awk '/^## Landed changes$/{f=1;next} /^## /{f=0} f' … | grep -E '^\|' | grep -vE '[0-9a-f]{7,40}'` lists the
header, the separator and the rows whose commit cell is still `[MEASURE: commit]` (`C1 counter`, `D1`, `D2`,
`D5`, `E1/E3/E4/E5/E7`, `C2`, `PROVINCE`, `QUALITY R30/R31`, `considerthese-ledger`, `Round close`). Fix: one
hash per row, each an ancestor of the final lane head (F1).

**S3 [C] — Sources & frontier carries no counting command.** The section reads
"`corpus/SOURCES.md` before → after: **53 → 54 rows** (measured at `b56a4168`…)" with no `grep -cE` over
`SOURCES.md` (L9 `counting_cmd=0`). Fix: append the frozen counter verbatim next to the arrow —
``grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`` → `53` / `54`. This is the same
defect the r36 report shipped (§4); do not ship it twice.

**S4 [C] — two Work-performed bullets name receipts with no base directory.** The `C2 build` and
`C2 attack/review` bullets list `ExecC2Capture`, `RevEntryF20`, … with no path/slash/hash and the section has
no `evidence under \`…/\`` declaration (L6 `strict_missing=2 base_dir_decl=0`). Fix: add the round-36 form
(`evidence under \`.ufo/waves/round-37/wave1/\``) once in the section preamble, or one path per bullet.

Everything else passes at this digest: six headings once each in order (`:32,:116,:144,:252,:295,:333`), L2 = 1,
4 SHONEN lines with all four signatures, 4/4 `[~]` blocks carrying pointers, these three verdicts in enum
vocabulary, 177 pointer occurrences, and no `Stale-lane`/`Tooling`/`Open L0` gap.

---

## 6. What this checklist does not certify

- **Truth of the numbers.** L8/L9 check that a command and a commit are *present*; they cannot tell whether the
  printed count is what the command prints. The non-author closure re-derives the counts; the report's job is to
  make each one re-derivable.
- **That `[~]` pointers resolve.** L14 accepts any backticked token. Whether
  `.ufo/waves/round-37/wave1/RevC1Suite.md` says what the box claims is the verifier's read.
- **Verdict quality.** L10 checks three verdicts from the frozen vocabulary, not that `improved` is earned.
- **Trend verdicts and Sources & frontier are [C], not [M]** — per the prompt's marker rule. A report missing
  either is `ok` with a conformance defect, and that is the grading L1 gets from this checklist.
- **No deletion is proposed and no LSP `references` proof applies**: the artifacts here are Markdown prose, not
  code with a call graph. Every statement in §2–§5 rests on the literal command output printed above; no claim
  of semantic-caller evidence is made.

---

## 7. Appendix — `report-lint.sh` (sha256 `cf2af3ef44402f17f3b712b4a5e312398b462fbe442944110fae00896a2e1435`, 157 lines)

Paste to a scratch file, then `bash report-lint.sh .ufo/reports/round-37/kasegi.md` from the fleet root
(cwd = lane also works; pass the lane root as `$2` to override). Exit status is nonzero if any check fails;
`FAILS=<n>` names the count. Read-only: `grep`/`awk`/`printf`, no writes, no network.

```bash
#!/usr/bin/env bash
# report-lint.sh <report> [lane-root] — round-37 report contract lint, read-only.
set -u
R=${1:?report path}
LANE=${2:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
nfail=0
say() { printf '%-4s %-34s %s %s\n' "$1" "$2" "$3" "$4"; }
# section extractor: heading text -> body
sec() { awk -v h="## $1" 'index($0,h)==1 && length($0)==length(h) {f=1;next} /^## /{f=0} f' "$R"; }

# L0 exists, non-empty
n=$( [ -f "$R" ] && wc -l < "$R" || echo 0 )
if [ "$n" -ge 40 ]; then say L0 "exists >40 lines" PASS "lines=$n"; else say L0 "exists >40 lines" FAIL "lines=$n"; nfail=$((nfail+1)); fi

# L1a marker sections (missing one = round FAILED): Work performed, Landed changes,
#     Before -> after measurements, SHONEN. L1b non-marker conformance: Sources & frontier,
#     Trend verdicts (prompt §4 marker rule).
want=("Work performed" "Landed changes" "Before → after measurements" "Sources & frontier" "Trend verdicts" "SHONEN")
marker=(1 1 1 0 0 1)
pos=""; prev=0; a_ok=1; b_ok=1; a_det=""; b_det=""
for i in "${!want[@]}"; do
  h=${want[$i]}; c=$(grep -cFx "## $h" "$R"); ln=$(grep -nFx "## $h" "$R" | cut -d: -f1 | head -1)
  if [ "$c" = 1 ]; then
    if [ "${ln:-0}" -gt "$prev" ]; then prev=$ln; det="$ln"; else det="$ln(ORDER)"; fi
  else det="count=$c"; fi
  if [ "${marker[$i]}" = 1 ]; then
    [ "$det" = "$prev" ] || a_ok=0
    case "$det" in *ORDER*|count*) a_ok=0;; esac
    a_det="$a_det $h:$det"
  else
    case "$det" in *ORDER*|count*) b_ok=0;; esac
    b_det="$b_det $h:$det"
  fi
done
if [ "$a_ok" = 1 ]; then say L1a "marker sections present+ordered" PASS "$a_det"
else say L1a "marker sections present+ordered" FAIL "$a_det"; nfail=$((nfail+1)); fi
if [ "$b_ok" = 1 ]; then say L1b "non-marker sections present+ordered" PASS "$b_det"
else say L1b "non-marker sections present+ordered" FAIL "$b_det"; nfail=$((nfail+1)); fi

# L2 SHONEN heading count
c=$(grep -c '^## SHONEN' "$R")
if [ "$c" = 1 ]; then say L2 "grep -c ^## SHONEN" PASS "1"; else say L2 "grep -c ^## SHONEN" FAIL "$c"; nfail=$((nfail+1)); fi

# L3 SHONEN box lines == 4, tokens valid, [x] carries a verifier word
boxes=$(sec SHONEN | grep -cE '^- \[[ x~]\]')
tok=$(sec SHONEN | grep -cE '^- \[[^x~ ]\]')
if [ "$boxes" = 4 ] && [ "$tok" = 0 ]; then say L3 "SHONEN 4 box lines" PASS "boxes=4 bad_token=0"
else say L3 "SHONEN 4 box lines" FAIL "boxes=$boxes bad_token=$tok"; nfail=$((nfail+1)); fi
# L3c SHONEN covers all four canonical box signatures, one line each
sigs=("SKILL\.md" "end-to-end|domain task|LOG\.md" "oral context|executable" "cross-domain|PROVINCE")
smiss=0; sdetail=""
i=0
for sg in "${sigs[@]}"; do
  i=$((i+1)); k=$(sec SHONEN | grep -cE "$sg"); sdetail="$sdetail $i:$k"; [ "$k" -ge 1 ] || smiss=$((smiss+1))
done
if [ "$smiss" = 0 ]; then say L3c "SHONEN four box signatures" PASS "$sdetail"
else say L3c "SHONEN four box signatures" FAIL "$sdetail"; nfail=$((nfail+1)); fi

# L14 every [~] line carries a pointer token
shblk() { sec SHONEN | awk '/^- \[/{if(n&&t)print buf; buf=$0; n=1; t=($0 ~ /^- \[~\]/); next} {if(n)buf=buf" "$0} END{if(n&&t)print buf}'; }
n=$(sec SHONEN | grep -cE '^- \[~\]'); np=$(shblk | grep -cE '`[^`]+`|[0-9a-f]{7,40}')
if [ "$n" = "$np" ]; then say L14 "[~] lines carry pointers" PASS "tilde=$n with_pointer=$np"
else say L14 "[~] lines carry pointers" FAIL "tilde=$n with_pointer=$np"; nfail=$((nfail+1)); fi

xb=$(sec SHONEN | grep -cE '^- \[x\]')
xv=$(sec SHONEN | grep -E '^- \[x\]' | grep -icE 'verif(y|ied)|verifier|spot-check')
if [ "$xb" != 0 ] && [ "$xb" != "$xv" ]; then say L3b "[x] carries verifier" FAIL "x=$xb with_verifier=$xv"; nfail=$((nfail+1))
elif [ "$xb" = 0 ]; then say L3b "[x] carries verifier" PASS "x=0 (none claimed)"; else say L3b "[x] carries verifier" PASS "x=$xb with_verifier=$xv"; fi

# L4 placeholder / drafting-meta classes == 0
p1=$(grep -c '\[MEASURE' "$R"); p2=$(grep -c '⟨' "$R")
p3=$(grep -cE '\b(TODO|TBD|FIXME|PLACEHOLDER|XXX|INSERT)\b' "$R")
p4=$(grep -cE '^#[^#]*DRAFT|Draft status|\(skeleton\)|[Ss]keleton' "$R")
p5=$(grep -cE '\$\{?ROUND3[0-9]' "$R")
if [ $((p1+p2+p3+p4+p5)) = 0 ]; then say L4 "placeholders 0" PASS "measure=0 guillemet=0 todo=0 skeleton=0 var=0"
else say L4 "placeholders 0" FAIL "measure=$p1 guillemet=$p2 todo=$p3 skeleton=$p4 var=$p5"; nfail=$((nfail+1)); fi

# L5 template literals only inside an E1 line
for lit in '<LANE_HASH>' 'filled by the L1'; do
  tot=$(grep -cF "$lit" "$R"); bad=$(grep -F "$lit" "$R" | grep -vE 'E1|grep -c' | grep -c .)
  if [ "$bad" = 0 ]; then say L5 "literal '$lit' only on E1 lines" PASS "occ=$tot outside_E1=0"
  else say L5 "literal '$lit' only on E1 lines" FAIL "occ=$tot outside_E1=$bad"; nfail=$((nfail+1)); fi
done

# L6 Work performed: claim names + every bullet block carries a pointer
#   strict pointer = backticked span containing / or : , or a 7-40 hex hash
#   lenient fallback = a section-level "evidence under `<dir>/`" declaration plus any backticked token
c=$(sec "Work performed" | grep -cE 'C1|C2')
blk() { sec "Work performed" | awk '/^- /{if(n)print buf; buf=$0; n=1; next} {if(n)buf=buf" "$0} END{if(n)print buf}'; }
tot=$(blk | grep -c .)
strict_miss=$(blk | grep -vcE '`[^`]*[/:][^`]*`|[0-9a-f]{7,40}')
any_miss=$(blk | grep -vcE '`[^`]+`')
decl=$(sec "Work performed" | grep -cE 'evidence under `\.?[A-Za-z0-9_./-]+/`')
if [ "$c" -ge 1 ] && { [ "$strict_miss" = 0 ] || { [ "$decl" -ge 1 ] && [ "$any_miss" = 0 ]; }; }; then
  say L6 "Work performed claims+pointers" PASS "claim_tokens=$c bullets=$tot strict_missing=$strict_miss base_dir_decl=$decl"
else
  say L6 "Work performed claims+pointers" FAIL "claim_tokens=$c bullets=$tot strict_missing=$strict_miss any_missing=$any_miss base_dir_decl=$decl"; nfail=$((nfail+1))
fi

# L7 Landed changes: rows == rows with a commit hash; LOG.md named
rows=$(sec "Landed changes" | awk -F'|' '/^\|/{c=$2; gsub(/[[:space:]]/,"",c); if(c==""||c=="Change"||c ~ /^-+$/) next; n++} END{print n+0}')
withhash=$(sec "Landed changes" | awk -F'|' '/^\|/{c=$2; gsub(/[[:space:]]/,"",c); if(c==""||c=="Change"||c ~ /^-+$/) next; if($0 ~ /[0-9a-f]{7,40}/) n++} END{print n+0}')
log=$(sec "Landed changes" | grep -c 'LOG\.md')
if [ "$rows" -ge 1 ] && [ "$withhash" = "$rows" ] && [ "$log" -ge 1 ]; then say L7 "Landed rows hash+LOG" PASS "rows=$rows with_hash=$withhash log_mention=$log"
else say L7 "Landed rows hash+LOG" FAIL "rows=$rows with_hash=$withhash log_mention=$log"; nfail=$((nfail+1)); fi

# L8 Before->after: one block per claim, each with a command and a measured commit
nb=$(sec "Before → after measurements" | grep -cE '^### ')
cmds=$(sec "Before → after measurements" | grep -cE '`[^`]*(bash|python3|grep|ls |git |scripts/)[^`]*`')
meas=$(sec "Before → after measurements" | grep -ciE 'measured at|at `?[0-9a-f]{7}')
if [ "$nb" -ge 2 ] && [ "$cmds" -ge 2 ] && [ "$meas" -ge 2 ]; then say L8 "Before→after blocks" PASS "blocks=$nb command_cells=$cmds measured_commit_lines=$meas"
else say L8 "Before→after blocks" FAIL "blocks=$nb command_cells=$cmds measured_commit_lines=$meas"; nfail=$((nfail+1)); fi

# L9 Sources & frontier limbs
s=$(sec "Sources & frontier")
c1=$(printf '%s\n' "$s" | grep -c 'SOURCES\.md'); c2=$(printf '%s\n' "$s" | grep -cE '[0-9]+ ?(→|->) ?[0-9]+ ?rows')
c3=$(printf '%s\n' "$s" | grep -ci 'added by tier'); c4=$(printf '%s\n' "$s" | grep -ci 'touched'); c5=$(printf '%s\n' "$s" | grep -ciE 'frontier .*(advanced|row)')
c6=$(printf '%s\n' "$s" | grep -ciE 'assimilation|SOURCES: unchanged —')
c7=$(printf '%s\n' "$s" | grep -cE '`[^`]*(grep -c|python3|awk)[^`]*SOURCES\.md|grep -cE[^`]*S[0-9]{3}')
if [ "$c1" -ge 1 ] && [ "$c2" -ge 1 ] && [ "$c3" -ge 1 ] && [ "$c4" -ge 1 ] && [ "$c5" -ge 1 ] && [ "$c6" -ge 1 ] && [ "$c7" -ge 1 ]; then
  say L9 "S&F limbs (count-cmd, tier, touched, frontier, assimilation)" PASS "cmd=$c7"
else
  say L9 "S&F limbs" FAIL "sources=$c1 rows_arrow=$c2 tier=$c3 touched=$c4 frontier=$c5 assim=$c6 counting_cmd=$c7"; nfail=$((nfail+1))
fi

# L10 Trend verdicts: 3 named verdicts from the allowed vocabulary
t=$(sec "Trend verdicts")
v1=$(printf '%s\n' "$t" | grep -cE 'expansion:? ?\**\s*(improved|harmed|unchanged|unprovable-but-better)')
v2=$(printf '%s\n' "$t" | grep -cE 'quality:? ?\**\s*(improved|harmed|unchanged|unprovable-but-better)')
v3=$(printf '%s\n' "$t" | grep -cE 'discernment:? ?\**\s*(improved|harmed|unchanged|unprovable-but-better)')
if [ "$v1" = 1 ] && [ "$v2" = 1 ] && [ "$v3" = 1 ]; then say L10 "3 trend verdicts, enum vocab" PASS "expansion/quality/discernment=1/1/1"
else say L10 "3 trend verdicts, enum vocab" FAIL "expansion=$v1 quality=$v2 discernment=$v3"; nfail=$((nfail+1)); fi

# L11 evidence pointer floor: >=20 total, >=1 per required section
ptrs=$(grep -coE '`[^`]*[/:][^`]*`|[0-9a-f]{7,40}' "$R")
miss=""
for h in "${want[@]}"; do
  k=$(sec "$h" | grep -cE '`[^`]*[\/:][^`]*`|[0-9a-f]{7,40}')
  [ "$k" -ge 1 ] || miss="$miss $h"
done
if [ "$ptrs" -ge 20 ] && [ -z "$miss" ]; then say L11 "pointer floor" PASS "total=$ptrs sections_missing=none"
else say L11 "pointer floor" FAIL "total=$ptrs sections_missing=${miss:-none}"; nfail=$((nfail+1)); fi

# L12 extras: Stale-lane, tooling, open L0
e1=$(grep -c 'Stale-lane' "$R"); e2=$(grep -ci 'Tooling' "$R"); e3=$(grep -c 'Open L0' "$R")
if [ "$e1" -ge 1 ] && [ "$e2" -ge 1 ] && [ "$e3" -ge 1 ]; then say L12 "extras Stale-lane/Tooling/L0" PASS "1/$e2/$e3"
else say L12 "extras Stale-lane/Tooling/L0" FAIL "stale=$e1 tooling=$e2 l0=$e3"; nfail=$((nfail+1)); fi

# L13 marker rule: names claims, commits, and commands (not contentless)
h=$(grep -coE '[0-9a-f]{7,40}' "$R")
cm=$(grep -coE '`[^`]*(bash|python3|grep|git |ls |scripts/)[^`]*`' "$R")
cl=$(grep -cE 'claims\.json|claims-freeze|C1 —|C2 —' "$R")
if [ "$h" -ge 5 ] && [ "$cm" -ge 5 ] && [ "$cl" -ge 1 ]; then say L13 "marker rule (contentful)" PASS "hashes=$h commands=$cm claim_refs=$cl"
else say L13 "marker rule (contentful)" FAIL "hashes=$h commands=$cm claim_refs=$cl"; nfail=$((nfail+1)); fi

echo "FAILS=$nfail"
exit $((nfail>0))
```

---

## Report

Seat `SimplReport` complete. Delivered: a 23-check report-contract checklist — 18 checks over the report
bytes (one of them, `L5`, holding a two-literal sub-check) plus 5 filing checks — executed on ten controls.
The published round-36 report passes every byte check except `L9` (the Sources &
frontier counting command), which round-36's own review had already routed; the round-37 draft at `78fc7987`
fails four (87 `[MEASURE` slots and the drafting paragraphs; 10 of 14 Landed rows without a commit; no
`SOURCES.md` counting command; two pointer-less Work-performed bullets); seven single-defect mutants are each
caught by the intended check. No lane, fleet, sibling or source-tree file written; no deletion or edit
proposed; no `LSP` `references` query applies to Markdown prose and none is claimed as proof. Tooling: none
installed or upgraded; no pacman transaction attempted (host-wide pause). Scratch removed.
