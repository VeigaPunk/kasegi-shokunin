# Wave 2 — falsify F10 as new coverage ground from the base corpus

Seat: `L1Kasegi25.C2CoverageGround` (critic, READ-ONLY). Lane base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41` (same base the claims.json C2 claim and
wave-1's `CritC2Ground.md` measured against). No production edit, no VCS mutation, no
spawn, no tool installed or upgraded (RULES.md record: none). All evidences below were
produced against the **committed base bytes** (`git show b49948f:…` or
`git grep b49948f`), not the working tree.

## 1. Verdict

**F10 as "new admitted frontier ground" SURVIVES under the admitted-entry reading, but
the claim's literal ground statement "frontier ground the lane did not hold: vendor-side
disclosure policies as corpus objects" is PARTIALLY FALSIFIED.** The lane's base corpus
already held a vendor's own published disclosure policy as a corpus object — a queued
source row, S016 — and held a mined vendor-intake route fragment whose intake-channel limb
is exactly one of the F10 object set's limbs. The true novelty is narrower: no **admitted
entry** read a product vendor's own product-handling policy. No exact full-entry overlap
exists; the overlaps are a registry object (S016), an intake fragment
(`vdp-disclosure-packages.md`), and a round-24 fetch record of the very Cisco page F10
now admits.

## 2. Counterexample (strongest from the base corpus)

Base row `corpus/SOURCES.md:22` — **S016**:

> | S016 | Anthropic Coordinated Vulnerability Disclosure for Claude-Discovered
> Vulnerabilities — https://www.anthropic.com/coordinated-vulnerability-disclosure |
> docs | A | **Anthropic's own labeling, pacing and disclosure policy** for
> AI-discovered vulnerabilities | Vulnerability Disclosure Reporting and Coordination;
> last updated 2026-03-06 | … | **queued** | 2026-10-19 | 90d | — |

This is a vendor's own published disclosure policy registered at the base as a corpus
object (tier A, `queued`). The wave-1 ground verdict's probe set checked only tracked
*knowledge entries* and four vendor names (Cisco/Cybozu/Pepabo/Hitachi); it never grepped
`corpus/SOURCES.md` rows. It therefore missed that the object kind "vendor-side disclosure
policy" already existed in the corpus registry.

Second limb: base `corpus/knowledge/vdp-disclosure-packages.md:13` (ROUTE.md row) and
`:23` record an **observed vendor intake route** derived from a vendor's published policy
surface:

> official VDP intake via security.txt `Contact:` → HackerOne **embedded_submissions**
> URL (`hackerone.com/<uuid>/embedded_submissions/new`), not the program's bounty form.
> …
> VDP intake can be the vendor's `security.txt` Contact route even when the vendor also
> runs a paid HackerOne program — the disclosure bypassed the bounty queue deliberately.

The F10 object set as defined in wave-1 (`CritC2Ground.md` §1) begins with the
**intake-channel list**; that limb has prior base presence.

Third limb: base `corpus/lessons/round-24.md:97` already records a fetch of the round-25
F10 Cisco page:

> | S068 | could not be fetched | Cisco policy page 200/94 027 B | reachable; not adopted |

The lane's own past record knew the Cisco policy page was reachable; it was not adopted,
which supports F10 being new *admitted* ground — but it also means "the lane did not
hold" is false in the literal sense: the lane had already held a record of that vendor's
policy page.

## 3. Evidence (commands, outputs, exits)

| probe | command | output | exit |
|---|---|---|---|
| base knowledge entry list | `git ls-tree -r --name-only b49948f corpus/knowledge/` | 35 `.md` files, none named vendor-*; **no vendor-disclosure entry** | 0 |
| base source rows | `git show b49948f:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} '` | **35** (S001–S035) | 0 |
| S016 row | `git show b49948f:corpus/SOURCES.md \| sed -n '20,24p'` | S016 = Anthropic CVD policy, `queued`, 2026-10-19 (`SOURCES.md:22`) | 0 |
| vendor-name sweep | `git grep -niE 'cisco\|cybozu\|pepabo\|hitachi\|psirt\|ldos\|29147\|30111\|JVN\|JPCERT' b49948f -- corpus/ SKILL.md PROVINCE.md README.md` | hits only in snapshots/leads/round-24 lesson; **0 hits in base knowledge entries** | 0 |
| vendor-policy sweep | `git grep -niE 'vendor.*(policy\|disclosure)\|disclosure.*polic\|security\.txt' b49948f -- corpus/knowledge/` | only `coordinated-disclosure-timelines.md:22,24` (CERT/CC, Project Zero — coordinators/finders, not product vendors), `authorization-safe-harbor-and-scope.md:38` (CISA template), `vdp-disclosure-packages.md:23` (intake route) | 0 |
| frontier rows | `git show b49948f:corpus/README.md \| sed -n '190,220p'` | F01–F09 only; no row topic names a vendor policy | 0 |
| F10 entries (working tree, wave-1 results) | `read corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`, `read corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | ground: F10, S036–S040, four/five captures | 0 |
| AXES coverage definition | `read /home/vgpnk/Projects/shokunin/AXES.md:12` | coverage = "Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes)" | 0 |

The wave-1 report's own probes are re-affirmed independently: `git grep -niE 'cisco\|cybozu\|pepabo\|hitachi' b49948f -- corpus/knowledge SKILL.md` → 0 hits (all 22 current-tree hits are inside the untracked round-25 entry); `git grep -n 'ISO/IEC 29147' b49948f -- corpus/` → only `SOURCES.md:63` (unopened lead) and `round-23/S018.txt:3` (FIRST cross-reference); `grep -c '^\| F10' corpus/README.md` → 0 at base.

## 4. Candidate overlaps tested and rejected as exact entry overlaps

| base object | why not an exact F10 overlap |
|---|---|
| S016 Anthropic CVD policy (`SOURCES.md:22`) | **registry row, queued — not an admitted entry**; and it is Anthropic's *finder-side* disclosure policy, not a policy for handling reports about its own products |
| S004 CERT/CC disclosure policy (`coordinated-disclosure-timelines.md:22`) | CERT/CC is a coordinator, not the vendor of the products; form overlap only (published policy object) |
| S005 Project Zero 90-day policy (`coordinated-disclosure-timelines.md:24`) | finder-of-others'-bugs policy, not product vendor's own-product policy |
| S008 CISA VDP template (`authorization-safe-harbor-and-scope.md:38`) | government template, not a vendor's policy |
| S006/S007 HackerOne/Bugcrowd safe-harbor docs | platform/programme policies, not product-vendor policies |
| S018 FIRST v1.1 (`multiparty-vulnerability-coordination.md`) | industry guideline, not a vendor's own policy |
| `vdp-disclosure-packages.md:13,23-24` | holds the intake **route**, not the policy object; fragment overlap with F10's intake-channel limb |

No tracked base entry reads a product vendor's own published product-handling policy.

## 5. Impacted axes

- **coverage (C2)**: the claim's `surface`/`before` wording ("frontier ground the lane did
  not hold: vendor-side disclosure policies as corpus objects") is overbroad — the object
  kind existed in the registry (S016) and one limb existed as a mined fragment. Remove the
  literal "did not hold" framing.
- **calibration**: wave-1's `CritC2Ground.md` conclusion ("No tracked entry at the lane
  base documents a vendor's own published policy… the object it adds … is held by no
  existing entry") is correct on *entries* but omitted the SOURCES registry and the round-24
  lesson record; a report carrying that as "no presence in the base corpus" would overstate.
- **depth/verifiability**: untouched — the claim's counter and the F10 entries are unaffected.

## 6. Smallest safe correction (no production edit; for the wave-1/claims text)

1. Restate the C2 surface/before as: *"no admitted frontier entry read a product vendor's
   own product-handling disclosure policy (S016 is a queued registry row, not an admitted
   entry; `vdp-disclosure-packages.md` holds the intake route, not the policy object)"* —
   keeping the counter and target unchanged.
2. In the F10 entry (`vendor-disclosure-policies-as-corpus-objects.md`), add one boundary
   note: S016 (Anthropic CVD, queued at base) is registration, not ground; and the round-24
   lesson's S068 record (`round-24.md:97`) shows the Cisco page was reachable but unadopted
   — admission, not discovery, is what round 25 adds.
3. Wave-1's ground sentence already names the F02-form/F03-limb overlaps; keep it, and add
   the S016/intake-fragment presence so the "new ground" verdict is not reported as
   "no corpus presence".

## 7. Consistency with the canonical claim

The C2 predicate (frontier=10, entry with `source: S0(3[6-9]|[4-9][0-9])`, census exit 0)
is not attacked here; the F10 row and entries satisfy it. The attack is only on the
**ground framing** in `claims.json` and in wave-1's ground report.

## 8. Report trail

- F10 row: `corpus/README.md:211` (working tree).
- F10 entries: `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`,
  `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md`.
- Base S016: `corpus/SOURCES.md:22` (committed b49948f).
- Base intake fragment: `corpus/knowledge/vdp-disclosure-packages.md:13,23-24` (committed).
- Base Cisco fetch record: `corpus/lessons/round-24.md:97` (committed).
- Wave-1 ground report: `.ufo/waves/round-25/wave1/CritC2Ground.md` (§1, §2, §4).
- AXES coverage definition: `/home/vgpnk/Projects/shokunin/AXES.md:12`.
