# CritExpansion — expansion-credit attack on F15 (round 31, wave 2)

Seat: critic (leaf). Scope: does any existing lane entry — F06, F10's two entries, F11, SKILL.md —
already say what F15 says? Read-only on the lane; the only write is this receipt. No network, no
subagents, no background jobs, tooling installed: none.

Answering model (rule 10, read from the harness project context, not passed by me):
`opencode-go/deepseek-v4.1-flash`.

Bytes reviewed (2026-10-25, quiescent; sha256 re-measured immediately before this file was written):

```
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md  (160 lines)
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
```

The entry hash is the same pin CritC2Kill §8 recorded, so nothing is in flight (§M30-3 satisfied).
Every earlier entry cited below is read at base `b374febbb` and at HEAD; both readings agree on the
lines I quote (one knowledge file added — the F15 entry; `considerthese-proposals-ledger.md` is the only other
knowledge file touched, a non-claim ledger flip).

## VERDICT

**`partial`.** Not `restatement`: F15's two load-bearing residuals are absent from all 43
pre-round knowledge files, from README's coverage map and from SKILL.md, proven by the base-tree
sweep in §1. So C2's restatement clause **does not fire** and the admission stands.

But the entry's sentence at L74 — "S048 adds three things the lane did not hold" — is **overstated
for addition 3 and under-qualified for addition 2**. One named addition (#3) is falsified in its
stated form by F10's own Claim 2, and one (#2) is a new *value* for a recording rule F06/F02 already
hold, not a new rule. A reviewer applying the kill rule's restatement clause literally to addition 3
as written would be entitled to strike it. Smallest safe correction is §6: three sentence-level
edits, no new source, no new row.

## §1 The sweep (base tree, i.e. before F15 existed)

I ran the sweep against `b374febbb` rather than HEAD so the new entry cannot supply its own hits:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities' 'not developed by' \
           '他社' 'third-party product' 'multi-vendor' 'multiple vendors'; do
    printf '### %s\n' "$t"
    git grep -n -i -- "$t" b374febbb -- corpus/knowledge corpus/README.md SKILL.md | head -6
  done
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
### multiple vendors
```

Seven of the nine terms are **0-hit at base**; the two that hit are both inside F10's two entries and
all in the *vendor-as-recipient / vendor-as-downstream-user* direction (§2 rows 5 and 8). On the landed
tree the entry's own sweep command prints exactly one file per term, as the entry claims:

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
corpus/knowledge/vendor-third-party-finding-coordination.md
corpus/knowledge/vendor-third-party-finding-coordination.md
corpus/knowledge/vendor-third-party-finding-coordination.md
corpus/knowledge/vendor-third-party-finding-coordination.md
```

SKILL.md, checked on its own, is empty on this ground at both commits:

```
$ grep -c -i -E 'MSVR|MSRC|research programme|coordinator|multi-vendor|third-party product' SKILL.md
0
$ git show b374febbb:SKILL.md | grep -c -i -E 'MSVR|MSRC|research programme|coordinator|multi-vendor|third-party product'
0
```

One precision note for the record: there is **no literal `他社`** in any knowledge entry
(`grep -rn '他社' corpus/knowledge/*.md` → no output); the earlier scout sweep's "他社" row was its
English `other vendors` hits. No impact on the verdict, but it must not be retyped as a Japanese
hit.

## §2 What each neighbour already says — quote, location, gap

| # | entry / map | overlapping line (≤25 words) | what it holds | what it does not hold |
|---|---|---|---|---|
| 1 | F06 `multiparty-vulnerability-coordination.md:25` | "Optional participant that can assist vendors and finders in handling and disclosing vulnerability information." | coordinator is a party that *assists* vendors and finders, i.e. sits outside both; the entry's own consequence column reads "A coordinator is optional; record whether one exists rather than inventing one." | a vendor occupying the coordinator seat |
| 2 | F06 `:29` | "Vendors should be aware that publication of fixes can disclose the presence of the same vulnerability in other vendors' components." | a vendor's action touches *other* vendors' components | any finder role; the direction is upstream-supplier, not finder |
| 3 | F10 `vendor-disclosure-policies-as-corpus-objects.md:13` | "the named vendor's own position about its own handling" | attribution discipline (whose statement it is) | — this is about *whose position*, not *whose products* (§3) |
| 4 | F10 `:23` (S036.txt:19) | "external reports including the bounty programme, and internal detection" | a vendor's intake list already names **internal detection** as one channel | that the internally-detected vulnerabilities are in *third-party* software |
| 5 | F10 `:33`, `:35` (S036.txt:14-15) | "Handling scope covers services and products Cybozu creates, plus third-party products it uses" + "当社が利用しているサードパーティー製品" | a vendor's published statement whose **scope already includes third-party products** (as products it *uses*) | a programme aimed *into* other vendors' products; a finder seat |
| 6 | F10 crosswalk `:2`, `:49` (S040.txt:185-186, 190-191) | "The Cisco PSIRT works with third-party coordination centers" / "to manage a coordinated industry disclosure for vulnerabilities reported to Cisco that may impact multiple vendors" | a vendor **managing** a multi-vendor coordinated disclosure, with the centres named | the coordinator *of record* being the vendor itself, with no centre named (§3) |
| 7 | F10 `:152` (S039.txt:520) | "脆弱性対策の調整機関であるCERT/CCやJPCERT/CCの協力を得て" | Hitachi names external 調整機関 | Hitachi as coordinator |
| 8 | F10 `:158-162` (S039.txt:506) | "a finding from its development flow whose impact reaches another vendor's product" | vendor-internal discovery spilling to another vendor, handed to the national 届出窓口 | deliberate research *targeting* other vendors' products |
| 9 | F11 `iso-29147-and-30111-division-of-labour.md:11` | "product developers, online-service providers and intermediate vendors" | 29147 = the vendor's outward exchanges about **its own** products | any finder or coordinator seat for a vendor |
| 10 | F02 `coordinated-disclosure-timelines.md:9` | "must name the policy or coordinator, the event that starts its clock" | the *record-the-coordinator* instruction already exists | which party may legitimately occupy it |
| 11 | F13 `program-severity-ladders-and-reward-scales.md:1-3` | "Program severity ladders and reward scales" (HackerOne, Bugcrowd) | a **programme already is a corpus object** in this lane | a vendor-run *finding* programme |
| 12 | SKILL.md | 0 hits for MSVR / MSRC / research programme / coordinator of vulnerabilities / multi-vendor | — | nothing on this ground |
| 13 | README map `:211` (F10 row) | "A vendor's published policy is a standing first-party statement, not a programme" | the map itself drew the policy/programme line | the programme side of that line |

## §3 Counterexample: the entry's addition 3 is falsified by F10's own Claim 2

The entry (L84-86) says:

> 3. **A published programme about *other vendors'* products as a corpus object.** F10's
>    thesis is a vendor's standing statement about the handling of findings in its *own*
>    products; S048 is a vendor's standing statement about its routes into *other* vendors'
>    products.

The premise is false on lane bytes. F10's Claim 2 heading reads "Handling scope covers services and
products Cybozu creates, plus third-party products it uses"
(`vendor-disclosure-policies-as-corpus-objects.md:33`), quoting "当社が利用しているサードパーティー製品"
(`:35`, S036.txt:15). F10 therefore already admits a vendor's published statement whose *subject
matter* is third-party products. What F10 does not have is the **direction**: Cybozu is the
downstream *user* of those third-party products; MSVR is the *finder* reporting into them. Addition
3 must state the direction, not "own products vs other vendors' products".

A second, smaller defect in the same sentence: "as a corpus object" is not new either — F13 already
admits *programmes* as corpus objects (`program-severity-ladders-and-reward-scales.md:1-3`). The
novelty is the kind of programme, not the object type.

## §4 Counterexample: the entry's addition 2 is a new value, not a new rule

The entry (L80-83) contrasts Microsoft's self-named coordinator role with Cisco routing out and
Hitachi filing with the partnership. That contrast is real, but the entry overstates it in one
direction. Cisco's own sentence already puts the vendor in a managing seat for a multi-vendor
disclosure: "to manage a coordinated industry disclosure for vulnerabilities reported to Cisco that
may impact multiple vendors" (S040.txt:190-191, paragraph recorded in the crosswalk at `:2`). F06's
role vocabulary is not vendor-excluding: nothing in `:25` or `:30` says the coordinator cannot be a
vendor — `:25` only positions the coordinator as a party that *assists* vendors and finders. And F02
`:9` already requires the coordinator be named.

So what S048 adds on this axis is narrower than "the vendor stated as coordinator itself": it is that
the **coordinator of record is the vendor, with no external centre named** (S048 L35; `grep -c
'CERT/CC'` on the capture → 0 per the entry's own rejection #5). That is a genuine new value on
F06+F02's recording rule — it is what makes the F15 row's `next` column usable — but calling it a
new *thing the lane did not hold* invites the restatement reading.

Addition 1 survives as written: `S039.txt:506` places Hitachi's discovery inside its own
"製品開発工程" (design review, development, test), whereas S048 route 3 targets products "that are
not developed by Microsoft" (L34). Note for completeness that Hitachi's first sentence states an
*active* find-and-remove activity ("積極的に進めています"), so the "internal effort" half is held;
only the **target scope** is new.

## §5 Residual, named precisely (falsifiable)

*A vendor's published programme that (a) targets vulnerabilities in products another company
develops — not third-party products it uses and not its own development-flow findings that spill
over — and (b) claims the coordinator seat for multi-vendor findings as itself, naming no external
coordination centre.*

Checkable: base-tree sweep §1 gives 0 hits for `MSVR|MSRC|research programme|coordinator of
vulnerabilities|not developed by`; F10's third-party-product rows (`:33`, `:35`) are user-direction;
F10's Cisco row (`crosswalk:2`, `:49`) names four centres; F11 (`:11`) assigns no seat. A package
that states this residual from F06+F10+F11+F02 alone is not constructible from those entries.

## §6 Verdict against C2's kill rule, and the smallest safe correction

- C2 kill-rule clause "the entry repeats ground the coverage map already holds … reviewer must show
  F15 is not a restatement of F06/F10 entries with the sweep command": **passes**. The sweep is in
  §1 and is in the entry (L93-100); F15 is not a restatement of F06/F10.
- C2 is **not** failed by this review. Coverage stays held at 7; nothing here asserts a score move.
- Expansion trend (`LEARNING.md:33`, "net new admitted entries on uncovered ground"): satisfied by
  the entry as a whole, carried by residual (a) and residual (b) above — narrower than the entry's
  three-item claim.
- False-provenance check, reported not charged: `ground: F15` names a row minted in the same round
  (`git show b374febbb:corpus/README.md | grep -c F15` → 0; F13/F14 were minted the same way in
  rounds 29/30). Established lane pattern, not a defect — but it means "15/15 admitted" is not
  independent evidence of breadth, and expansion credit must rest on the content tests above.

Smallest safe correction (three edits to one paragraph, no new source, owner = the entry's writer;
the L1 routes it):

1. **Addition 3 (L84-86).** Replace the "own products" premise with the direction: F10's Cybozu row
   already puts third-party products the vendor *uses* inside handling scope (S036.txt:15, quoted
   at `vendor-disclosure-policies-as-corpus-objects.md:35`); S048 is the finder-direction
   counterpart, and drop "as a corpus object" (F13 holds programme objects).
2. **Addition 2 (L80-83).** Add the two qualifications: Cisco already "manage[s] a coordinated
   industry disclosure" (S040.txt:190-191), and F06 `:25` positions the coordinator as a party that
   assists vendors and finders without excluding a vendor; the new fact is coordinator-of-record =
   the vendor, with no centre named. Point at F02 `:9` for the recording rule it instantiates.
3. **The F10-ground paragraph (L63-72).** It currently says "F10's vendor rows both keep
   coordination outside the vendor" and omits F10's internal-detection channel (`:23`/S036.txt:19)
   and its third-party-products-in-scope line (`:33-35`). Name both as the conceded overlap.

## §7 Reproduce

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities' 'not developed by' \
         '他社' 'third-party product' 'multi-vendor'; do
  printf '### %s\n' "$t"; git grep -n -i -- "$t" b374febbb -- corpus/knowledge corpus/README.md SKILL.md | head -6; done
sed -n '13p;23p;33p;35p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
sed -n '25p;29p;30p' corpus/knowledge/multiparty-vulnerability-coordination.md
sed -n '9p' corpus/knowledge/coordinated-disclosure-timelines.md
sed -n '11p' corpus/knowledge/iso-29147-and-30111-division-of-labour.md
sed -n '185,192p' corpus/source-snapshots/round-25/S040.txt
sed -n '506p' corpus/source-snapshots/round-25/S039.txt
sed -n '74,101p' corpus/knowledge/vendor-third-party-finding-coordination.md
git show b374febbb:corpus/README.md | grep -c F15     # 0 — the F15 row is minted this round
```
