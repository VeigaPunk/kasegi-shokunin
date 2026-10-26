# CritExpansion2 — expansion-credit re-attack on the repaired F15 entry (round 31, wave 3)

Seat: critic (leaf). Scope: on the CURRENT bytes, decide (a) whether the F15 entry now concedes the
F10/F06 overlap wave 2 found it omitting, (b) whether any addition still rests on a warrant refuted by
a committed byte, (c) whether F15 is `new-ground`, `partial` or `restatement` against
`corpus/README.md`'s coverage map + frontier F01-F14 + every knowledge entry.

Bounds: read-only on the lane. The only file written is this receipt. No network. No subagent, no
background job. No `git`/`jj` mutation (read-only `rev-parse`/`status`/`show`/`grep` only). No tool
installed (rule 5 not exercised). Answering model (rule 10, from the harness project context — not
passed by me): `opencode-go/deepseek-v4.1-flash`.

## 0. Bytes reviewed, quiescence, and what changed since wave 2

```
$ sha256sum corpus/knowledge/vendor-third-party-finding-coordination.md corpus/README.md corpus/SOURCES.md corpus/source-snapshots/round-31/S048.txt
8c0b7331e2809ee529266d99cedb853bbce22acca7cbfaec92b307b2e5756eba  corpus/knowledge/vendor-third-party-finding-coordination.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
$ wc -l corpus/knowledge/vendor-third-party-finding-coordination.md
170 corpus/knowledge/vendor-third-party-finding-coordination.md
$ git rev-parse HEAD
a155310d1ee9aacc07c3ce62328105a46c0392b4
$ git status --porcelain -- corpus/knowledge/vendor-third-party-finding-coordination.md
(no output — the entry is committed state, nothing in flight; §M30-3 satisfied)
```

The entry hash differs from wave-2's `1f16e371…`/160 lines: the L1 repair at `fd29aac` is present, so
this review judges repaired bytes, not the bytes wave 2 struck. The capture pin (`2001ad77…`) and the
README/SOURCES hashes are unchanged from wave 2. S048 recheck re-run on these bytes:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "exit=$?"
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
S048:Q9 OK occurrences=1
S048:Q10 OK occurrences=1
S048:Q11 OK occurrences=1
exit=0
```

Every cited line was opened (§E below). Registry row is one row, tier A:

```
$ grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md
1
$ grep -n '^| S048' corpus/SOURCES.md | cut -c1-120
54:| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | docs | A |
```

## (a) Does the entry now concede the F10/F06 overlap? — F10 yes, F06 half

**F10: conceded, and the three concessions are accurate on bytes.** The repaired paragraph names all
three overlap lines wave 2's §6 correction 3 required, and each line says what the entry says it says:

```
$ sed -n '13p;19p;23p;33p;35p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
Every statement below is the named vendor's own position about its own handling: a
## Claim 1 — intake is a policy-level list, and a bounty programme is one channel on it
> 情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。
Handling scope covers services and products Cybozu creates, plus third-party products it uses:
> 当社が利用しているサードパーティー製品
```

- (a) Hitachi spill → 届出窓口: `S039.txt:506` (`日立グループ製品に留まらない`) quoted at F10 objects
  `Claim 7` lines 132/135 (verified: `grep -n '506' …objects.md` → `132:`, `135:`), entry L71-73.
- (b) Cybozu third-party-products scope: S036.txt:15 quoted at F10 objects:35, entry L76-78. Correct
  line, correct capture line.
- (c) vendor-internal detection channel: F10 objects:23 holds `社内での検出`, entry L78-79. Correct.
- Cisco contrast: `S040.txt:185-193` opened — the paragraph begins `Incidents that may impact other
  vendors: The Cisco PSIRT works with third-party coordination centers such as … CERT/CC … CERT-FI …
  JP-CERT … and … NPSA to manage a coordinated industry disclosure for vulnerabilities reported to
  Cisco that may impact multiple vendors`. Entry L73-76 quotes it accurately; crosswalk row exists at
  `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:49`.

**F06: only half conceded.** The accurate half is L66-67 (`F06 has no row for a vendor occupying the
finder and coordinator seats itself`) and L94 (`the recording rule it instantiates is F06's worksheet
line`). The unqualified half survives in two places:

- L64: `in it the coordinator is a participant *outside* the vendor — "Optional participant that can
  assist vendors and finders" (line 25)`.
- L154 (rejection 5): `F06's coordinator is an optional participant outside the vendor`.

The cited byte does not say *outside*:

```
$ sed -n '6p' corpus/source-snapshots/round-23/S018.txt
- **Coordinator:** Optional participant that can assist vendors and finders in handling and disclosing vulnerability information.
```

"assist vendors and finders" positions the coordinator as a distinct participant; it does **not**
exclude a vendor from occupying the seat (S018:82-83 has the coordinator "help connect researchers,
vendors, and other stakeholders" — still no exclusion). So this is an unsupported strengthening, not a
refuted one: it is a sentence-level defect (wave-2 §4's exact point, left in place by the repair), and
it no longer carries the novelty load — L93-94 now says the new fact is `coordinator-of-record being
the vendor`, which is the correct narrower form. It must be qualified, not struck.

## (b) Additions resting on a warrant refuted by a committed byte — one: addition 1's "by-product" clause

**Counterexample (entry L85-88, the entry's own citation):**

```
$ sed -n '506p' corpus/source-snapshots/round-25/S039.txt | cut -c1-220
HIRTと製品開発に関わる関連部門では、製品セキュリティの向上に向けた活動のひとつとして、脆弱性を発見し、除去するための活動を積極的に進めています。このため、設計レビューやテストなど、設計、開発、検査などの製品開発工程において脆弱性が発見されることがあります。なお、発見さ
```

The entry says route 3 is "not a by-product of the vendor's own product QA — which is the shape Hitachi
describes (S039.txt:506)". The cited line says the opposite about intentionality: Hitachi *actively
pursues* a find-and-remove activity (`脆弱性を発見し、除去するための活動を積極的に進めています`,
S039.txt:506, §1.2 脆弱性情報の入手, 製品開発工程においての問題発見) and only then notes that discoveries
occur in its design/review/test stages (`このため、…製品開発工程において脆弱性が発見されることがあります`,
same line). Hitachi's route is a deliberate internal research-and-removal effort located in its own
development flow — not a by-product. So:

- **Refuted:** "not a by-product" (deliberateness is *held* by the lane's Hitachi row).
- **Survives:** the target-scope difference — S048 route 3 aims at `products that run on Microsoft
  operating systems, but that are not developed by Microsoft` (S048 L34, entry L32/L86-87), while
  S039.txt:506's discovery happens inside Hitachi's own 製品開発工程 and only later spills
  (`日立グループ製品に留まらない`). Addition 1's headline (`a conditional internal-research route into
  other vendors' products`, conditioned by `As time and resources permit`, S048 L34) is warranted by
  those two bytes; only its stated differentiator is wrong.

This is the strongest counterexample available: the defect is inside the entry's own citation, so a
reader can falsify it without any other file. It does **not** kill addition 1 and therefore does not
kill C2 — the fix is a clause substitution, not a withdrawal.

**Addition 2 — warrant stands.** `grep` on the capture:

```
$ grep -c 'CERT/CC' corpus/source-snapshots/round-31/S048.txt; grep -c 'JPCERT' …S048.txt; grep -c 'IPA' …S048.txt
0
0
0
$ grep -n -i 'cert' corpus/source-snapshots/round-31/S048.txt
48:Certified Refurbished
```

So `with no external centre named` (L90) is true of the bytes, and the Cisco/Hitachi contrasts it draws
(L91-93) are the S040/S039 lines quoted in (a). What remains is a **value-level** difference (who holds
the coordinator seat), not a new rule — the entry now says exactly that at L93-94, and F02's recording
rule is the closer pointer (see correction 3).

**Addition 3 — repaired, warrant stands.** L95-97 now reads as a *direction* difference against
Cybozu's third-party-products scope and explicitly drops the "new corpus-object type" claim. Checked
against F10:33/35 (user direction) and S036.txt:15; accurate. The concession that programmes are
already corpus objects rests on F13 (`program-severity-ladders-and-reward-scales.md:1-3`) but F13 is not
named — an un-attributed concession, not a false one.

**Rejected as a finding (reported, not charged):** Claim 2's heading (L41) says `Microsoft's MSVR
states three roles for itself`, while L35's subject is Microsoft's CVD (`CVD clarifies how Microsoft
responds as a vendor …, as a finder …, and as a coordinator …`). The body (L57-59) is correct
(`Microsoft describes itself`); only the heading's holder word is loose. No Q4 consequence — the
attribution stays first-party either way.

## (c) new-ground / partial / restatement — `partial`; the restatement clause does NOT fire

### The sweep (base tree, before F15 existed)

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities' 'not developed by' \
           '他社' 'third-party product' 'multi-vendor'; do
    printf '### %s\n' "$t"; git grep -n -i -- "$t" b374febbb -- corpus/knowledge corpus/README.md SKILL.md | head -6; done
### MSVR
### MSRC
### research programme
### coordinator of vulnerabilities
### not developed by
### 他社
### third-party product
b374febbb:corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:33:Handling scope covers services and products Cybozu creates, plus third-party products it uses:
### multi-vendor
b374febbb:corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:160:remediation starts on that basis, and multi-vendor publication is aligned across the
```

Seven terms are 0-hit at base; the two hits are F10's user-direction line (:33) and F10's
Hitachi-spill sentence (:160). Plain `coordinat` per file at base, and the vendor-seat probe:

```
$ git grep -c -i 'coordinat' b374febbb -- corpus/knowledge
…:cna-assignment-and-vulnerability-rules.md:1
…:coordinated-disclosure-timelines.md:6
…:cra-manufacturer-reporting-duties.md:1
…:iso-29147-divergence-and-clause-crosswalk.md:1
…:japanese-domestic-disclosure-workflow.md:3
…:japanese-severity-vocabulary-and-impact-model.md:1
…:multiparty-vulnerability-coordination.md:9
…:statutory-authorization-and-unauthorized-access.md:1
…:vendor-disclosure-policies-as-corpus-objects.md:3
…:vendor-disclosure-policy-commitments-crosswalk.md:8
$ git grep -n -i -E 'vendor (is|as|itself) (a |the )?coordinator|vendor.{0,20}coordinat' b374febbb -- corpus/knowledge corpus/README.md
b374febbb:corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:15:… for a vendor taking on 29147:2014 conformance …   (no coordinator-seat assignment)
```

No base entry assigns the coordinator seat to a vendor, and no base entry holds a vendor research
programme: the residual is genuinely uncovered. On the landed tree the entry's own sweep prints exactly
one file per term, as it claims:

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
corpus/knowledge/vendor-third-party-finding-coordination.md
corpus/knowledge/vendor-third-party-finding-coordination.md
corpus/knowledge/vendor-third-party-finding-coordination.md
corpus/knowledge/vendor-third-party-finding-coordination.md
$ grep -c -i -E 'MSVR|MSRC|research programme|coordinator of vulnerabilities|multi-vendor|third-party product' SKILL.md
0
```

Neighbours re-opened on current bytes (CritExpansion §7, with the F02 line pointers corrected):

```
$ sed -n '25p;29p;30p' corpus/knowledge/multiparty-vulnerability-coordination.md
| Definitions — Coordinator | “Optional participant that can assist vendors and finders …” | A coordinator is optional; record whether one exists rather than inventing one. |
| Minimize exposure for stakeholders | “Vendors should be aware that publication of fixes can disclose the presence of the same vulnerability in other vendors’ components.” | … |
| Use coordinators when appropriate | “To reduce confusion when multiple coordinators are involved, one coordinator should be selected as lead.” | … |
$ sed -n '7p;9p;11p' corpus/knowledge/coordinated-disclosure-timelines.md
A disclosure timeline in a report or case record must name the policy or coordinator, the event that starts its clock, the stated interval, the patch/publication relationship, and any documented extension or exception.
A reviewer can check the cited policy against each recorded trigger and date; if the applicable policy or its trigger is not identified, mark the timeline unknown.
- the policy or coordinator is named;
$ sed -n '11p' corpus/knowledge/iso-29147-and-30111-division-of-labour.md
- **ISO/IEC 29147:2014** covers the vendor's dealings with parties outside the company ("社外とのやりとり", S041.txt:1669) …
$ grep -n -i -E 'finder|coordinat|発見者' corpus/knowledge/iso-29147-and-30111-division-of-labour.md
(no output)
$ git show b374febbb:corpus/README.md | grep -c F15
0
```

`grep` on F11's division-of-labour entry returns nothing for finder/coordinator, so the entry's
statement that F11 "assigns no finder or coordinator seat to a vendor" is true as written. F15 minted in
the same round (`0` at base) is the established lane pattern wave 2 reported; it means `15/15 admitted`
is a self-count, not independent breadth evidence.

### Verdict

**`partial` — not `restatement`.** C2's kill-rule clause — "the entry repeats ground the coverage map
already holds (reviewer must show F15 is not a restatement of F06/F10 entries with the sweep command)" —
**does not fire**: the base sweep is 0-hit for MSVR / MSRC / research programme / coordinator of
vulnerabilities / not developed by, and the two base hits are the user-direction and Hitachi-spill rows
that argue *for* the residual rather than against it. The residual, stated falsifiably on current bytes:

> A vendor's published programme that (i) deliberately researches products another company develops —
> not third-party products it uses (F10 :33/:35) and not its own development-flow findings that spill
> over (S039.txt:506) — and (ii) names itself the coordinator of multi-vendor vulnerabilities with no
> external centre named (S048 L35; `CERT/CC`/`JPCERT`/`IPA` counts 0).

It is `partial` rather than `new-ground` because: addition 1's stated differentiator is refuted by its
own cited line (§b), addition 2 is a value on an existing recording rule rather than new ground, and
the F06 "outside the vendor" reading is left unqualifed (§a). The entry's own framing — "adds two
things the lane did not hold, and a third that is a difference of kind" — is one notch wider than what
the bytes support: one addition of ground (target scope) plus one new value (coordinator-of-record).

**Axis reading (no score move asserted):** `coverage` — C2 survives the restatement attack; expansion
credit is narrower than the entry text implies. `depth:verifiability` — the L87-88 paraphrase
contradicts its own cited line, a Q3/Q4 paraphrase defect inside a passing recheck (11/11
`occurrences=1`, exit 0); it is fixable in one clause.

## Smallest safe corrections (owner = the entry's writer; the L1 routes)

1. **L87-88 (addition 1).** Replace `not a by-product of the vendor's own product QA — which is the
   shape Hitachi describes (S039.txt:506)` with the scope statement: Hitachi's captured route discovers
   in its own design/review/test stages (`製品開発工程`, S039.txt:506), while S048 route 3 targets
   `products … that are not developed by Microsoft` (S048 L34). Keeps the addition, drops the refuted
   half.
2. **L64 and L154 (F06).** Qualify: S018:6's definition positions the coordinator as a participant that
   assists vendors and finders and does not exclude a vendor from the seat; what F06 lacks is a row for
   the finder+coordinator combination — which L66-67 already says correctly.
3. **L94 (recording rule).** Also name F02's rule — `must name the policy or coordinator`
   (`coordinated-disclosure-timelines.md:7`, restated at `:11`). Note for the L1: wave-2 §6's suggested
   pointer `:9` is the reviewer-check line, not the rule line; `:7`/`:11` is the correct pointer.
4. **Optional, L41.** Change `Microsoft's MSVR states three roles for itself` to `Microsoft states three
   roles for itself` (L35's subject is Microsoft's CVD; the body is already correct).

Nothing here rewrites a frozen claim, an axis score or another seat's receipt; the entry stays admitted
and C2 stays held at 7 on the evidence above.

## Reproduce (all read-only; lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/knowledge/vendor-third-party-finding-coordination.md
git status --porcelain -- corpus/knowledge/vendor-third-party-finding-coordination.md
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "exit=$?"
for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities' 'not developed by' \
         '他社' 'third-party product' 'multi-vendor'; do
  printf '### %s\n' "$t"; git grep -n -i -- "$t" b374febbb -- corpus/knowledge corpus/README.md SKILL.md | head -6; done
for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
grep -n -i -E 'finder|coordinat|発見者' corpus/knowledge/iso-29147-and-30111-division-of-labour.md
sed -n '506p' corpus/source-snapshots/round-25/S039.txt
sed -n '185,192p' corpus/source-snapshots/round-25/S040.txt
sed -n '6p' corpus/source-snapshots/round-23/S018.txt
sed -n '13p;23p;33p;35p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
sed -n '7p;9p;11p' corpus/knowledge/coordinated-disclosure-timelines.md
sed -n '55,110p' corpus/knowledge/vendor-third-party-finding-coordination.md
sed -n '135,159p' corpus/knowledge/vendor-third-party-finding-coordination.md
grep -c 'CERT/CC' corpus/source-snapshots/round-31/S048.txt; grep -n -i 'cert' corpus/source-snapshots/round-31/S048.txt
git show b374febbb:corpus/README.md | grep -c F15     # 0 — the F15 row is minted this round
```

## Entry falsifiable checks re-run (they still print what the entry says)

```
$ grep -cE '^(Internal Microsoft engineers|External reports to the Microsoft Security Response Center \(MSRC\)|Internal research projects):' corpus/source-snapshots/round-31/S048.txt
3
$ grep -c 'in three ways' corpus/source-snapshots/round-31/S048.txt ; grep -ci 'only' corpus/source-snapshots/round-31/S048.txt
1
0
$ grep -c 'as a coordinator of vulnerabilities that affect multiple vendors' corpus/source-snapshots/round-31/S048.txt
1
$ grep -ciE '90[ -]day|deadline|embargo|timeline' corpus/source-snapshots/round-31/S048.txt ; grep -ci '@microsoft' corpus/source-snapshots/round-31/S048.txt
0
0
$ sed -n '28,35p' corpus/source-snapshots/round-31/S048.txt | grep -ci bounty ; grep -ci bounty corpus/source-snapshots/round-31/S048.txt
0
1
$ grep -c 'affected vendor' corpus/source-snapshots/round-31/S048.txt
2
$ grep -ci 'http' corpus/source-snapshots/round-31/S048.txt
0
```

Header/limit facts also check out: `wc -c` → 3755, `wc -l` → 97, L2 = `This is the Trace Id:
f97e6b1cb578f714d23850f80f018bb3`, L15 = `Microsoft Bug Bounty Programs`, L36 = `Surface Laptop Ultra`,
L97 = `About our ads`. Report path for this receipt: `.ufo/waves/round-31/wave3/CritExpansion2.md`.

## Operational note (bounds, disclosed)

The first write of this receipt used a relative path from the fleet root cwd and landed at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-31/wave3/CritExpansion2.md` (outside my write scope).
Corrected immediately: copied to the lane path, `cmp` confirmed identical, removed the stray file, then
`rmdir`'d the two directories that write had created (`stat` birth time 22:15:46, no other entries; the
fleet-root `round-31` directory did not exist before and does not now — `ls` reports
`No such file or directory`). No fleet-root or sibling-lane byte from before my write was touched; the
lane subject bytes were re-hashed after the move and are unchanged
(`8c0b7331… corpus/knowledge/vendor-third-party-finding-coordination.md`). This receipt is the only
lane write; the wave3 directory is untracked and left for the L1's commit helper.
