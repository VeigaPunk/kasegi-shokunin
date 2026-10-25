# ConnectorSiblings — sibling-overlap scan (kasegi round 25, wave 1)

seat: connector | scope: READ-ONLY | lane base: `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`
question: does another fleet lane already hold (a) vendor security/disclosure policy as corpus
objects, or (b) corpus recheck-line / provenance-field discipline, and would this round's move collide?

All counts below were measured by me on 2026-10-25 over the **live worktrees** (siblings are editing
kasegi while I scan), except where a frozen receipt is named. No file outside this report was written;
no sibling gate was executed (only `bash -n -c` parses, `test -e`, `grep`, `sha256sum`, and the
read-only fleet census).

## (a) Evidence table

| lane | file:line | what it holds | same / adjacent |
|---|---|---|---|
| **chousa** | `chousa-shokunin/tools/research-gate.sh:684-688`, `:3670-3684` | Metadata mode reads a knowledge entry's `recheck:`; the first token must be an ISO date, `NNd`, or `on-release`, else `META_RECHECK_UNSCHEDULED` (info); a `--root ..` recheck emits `META_RECHECK_ROOT_PARENT` (info) | **adjacent, opposite grammar** — chousa's `recheck` is a *cadence/date*, kasegi's Q10 makes it *one executable command*. Same field name, same file class (`corpus/knowledge/*.md`), incompatible first token |
| chousa | `chousa-shokunin/PROVINCE.md:10` | `**Refuses:** bounty-program scope and claim packages (→ kasegi)` | adjacent, cedes — chousa names kasegi as owner |
| **kengaku** | `kengaku-shokunin/plans/sources_adopt.py:109-111`, `:16`, `:522-545`; `PROVINCE.md:224-227` | Registry-adoption gate that rejects/normalizes a prose `recheck` **cell** (`recheck-prose`, `recheck-empty`) to a default cadence; composes with the fleet census, which "remains the registry's authority" | **adjacent, different surface** — a `SOURCES.md` table *cell* holding a due date, not a knowledge-entry command line. Closest match on the *defect name* (`recheck-prose`), not on the object |
| kagi | `corpus/lessons/round-15.md:55`; `corpus/README.md:35` | Execution-found defect: selftest re-invoked as `"$0"` → `exit 127` **from a foreign cwd**; listed among nine defects found by running the checklist | adjacent — same *failure class* as kasegi D24-5, one lane over, on a shell instrument's self-test, not on markdown recheck lines |
| kotoba | `corpus/knowledge/checklist-execution-round15.md:222` | Lane-run evidence row: `live, from /tmp` → `exit 0` (cwd-independent) | adjacent — a recorded per-command cwd probe, not a gate over entry lines |
| souji | `tools/souji-landing-gate.py:18,284,298` | Landing gate runs `bash -n FILE` on candidate shell files; never executes repo code | adjacent — `bash -n` as a gate exists fleet-wide, applied to `.sh` files |
| mori | `tools/mori-round13-regressions.py:2596` | Mutation harness rejects a mutant that "fails bash -n" | adjacent — syntax parse as a mutation discriminator |
| **fleet** | `scripts/sources-census.sh:4`, `:28` | `SOURCES-CONTRACT-v1`: "recheck carries **cadence**"; `E09 invalid recheck (ISO date, NNd, or symbolic cadence)` | adjacent, **and a homonym hazard** — the fleet's frozen meaning of the token `recheck` is cadence |
| **kagi** | `corpus/sources-census.sh` (sha256 `8d30d627…`; `PROVINCE.md:55`) | Lane-local copy of the same contract **plus** a `corpus/knowledge/` citation handshake, 70 selftest cases | adjacent, **divergent implementation** — not byte-equal to the fleet script (`3fb7261…`); see risk R2 |
| **kake** | `PROVINCE.md:204-208`; `:283-288`; `corpus/README.md:361-363`; `corpus/SOURCES.md:86,92-93` | Holds `security.txt` *publishing* (RFC 9116 = S078; GitHub/Google served files = S084/S085) and explicitly refuses "**disclosure timing, bounty and policy operation**" | **adjacent, refuses toward kasegi's ground without naming kasegi** — kake holds the channel artifact and the serving mechanics; kasegi's F10 holds policy *content* |
| kagi | `PROVINCE.md:65` | Core = vendor **documentation** for secret custody (1Password, SOPS/age, Vault/OpenBao) | adjacent only — vendor docs, different subject (secrets), never disclosure policy |
| kengaku | `corpus/knowledge/extraction-policy-comparison.md:1-3` | "Extraction-policy" = parser/extractor policy in eval harnesses | adjacent only — homonym on "policy"; no security-disclosure object |
| kotoba | `PROVINCE.md:56` | kasegi classified `adjacent`, basis kotoba, commit `1fafde8…` | adjacent, already recorded by kotoba's own sibling census |
| revenger | `SKILL.md:495-499` | "The script is fleet-owned (`scripts/sources-census.sh`): run it, never edit it" | adjacent, confirms ownership of the C2 instrument |

Vendor-name sweep for F10's actual objects — `Cybozu`, `GMO Pepabo`, `HIRT`/Hitachi, `JPCERT`, `JVN`,
`IPA` — over every `*/corpus/{SOURCES.md,knowledge}`, `*/PROVINCE.md`, `*/SKILL.md`, `*/corpus/README.md`
outside kasegi: **zero hits** (only kotodama's phonetic "IPA" and audio/game-dev "thirteen" false
positives). No sibling holds the Cybozu/Pepabo/Hitachi/Cisco documents F10 adopts.

### Measured fleet state for the recheck criterion (C1's surface class)

`bash -n -c "<value>"` over every `^recheck:` line in each lane's `corpus/knowledge`; `cd `-prefix counted separately:

```
lane             lines  bash_n_ok  parse_fail   cd-prefixed
audio              4        4          0            0
chousa            54       19         35            0
game-dev-2d        3        0          3            0
game-dev-3d        2        2          0            0
kagi               4        1          3            0
kaidoku           49       17         32            0
kake              40       21         19            0
kama              30       19         11            0
kasegi            37       37          0           36   <- this round's worktree
kengaku           24       16          8            0
kotoba            23       21          2            0
kumitate          18       12          6            0
lore              12        5          7            0
mado              30       26          4            0
mori              47       18         29            0
revenger          15        6          9            0
souji             13       12          1            0
tabi              19        8         11            0
tameshi           28       13         15            0
tsukuroi          71       45         26            0
------------------------------------------------------
fleet total      523      302        221           36  (36 all in kasegi)
outside kasegi   486       265        221            0
```

So: **221 of 486 sibling recheck lines fail `bash -n`, and 0 of 486 carry a `cd <lane-root> &&` prefix.**
Kasegi's Q10 convention is lane-local, not a fleet norm — no lane's instrument gates knowledge-entry
recheck lines, and `corpus/instruments/recheck-audit.py` is **untracked** (`git status` → `?? `), i.e.
built this round, absent at the base revision (`git cat-file -e b49948f:corpus/instruments/recheck-audit.py`
→ "exists on disk, but not in 'b49948f…'").

## Contradictions found (stated, not smoothed)

1. **C1 and C2 are declared `independent_of` each other, but C1's counter literal is a function of C2.**
   The frozen predicate prints `lines=35`; the base tree has 35 entries / 35 lines
   (`git ls-tree b49948f corpus/knowledge/ | wc -l` → 35), and the live worktree now has **37 files /
   37 recheck lines** because two F10 entries are landing (`vendor-disclosure-policies-as-corpus-objects.md`,
   `vendor-disclosure-policy-commitments-crosswalk.md`, both untracked). An after-receipt that prints
   `lines=35` will not describe the tree it scored; one that prints `lines=37` contradicts the claim text.
2. **`claims.json` says Cisco is unreachable this round** (`assimilation.planned_reject: …crosswalk… (S068
   Cisco policy unreachable this round)`), **but the worktree crosswalk entry cites `S040` = Cisco
   `security-vulnerability-policy.html` with line anchors** (`:2`), and `renumber-map.md:13-18` assigns
   `S068 → S040`. Either the reject is stale or that entry is unadmitted ground. (The map itself is
   consistent and self-aware: `§2` says admitting vs rejecting Cisco is the C2 seat's call.)
3. **The C2 census limb cannot see what C2 asserts.** `scripts/sources-census.sh` reads only
   `corpus/SOURCES.md` — `grep -nE 'knowledge|handshake' scripts/sources-census.sh` returns no
   knowledge read. Measured: with `S036`–`S040` **not** registered (registry still 35 rows) and two
   entries citing them, `scripts/sources-census.sh validate --root … kasegi` → **exit 0**
   (`W04 S028`, `W04 S029` pre-existing). So "census validates exit 0" is not evidence that the new
   entry's ids are registered; only the `grep` limb carries that. Kagi's divergent copy
   (`8d30d627…`, 70 cases) *does* carry the handshake; the fleet copy (`3fb7261…`) does not.

## (b) Verdict

**`adjacent — report as adjacency`** (neither `no collision` nor `collision`).

- **F10 (vendor disclosure policy): no collision.** No lane holds the objects; chousa cedes the domain
  to kasegi by name; kake refuses exactly this ground (`disclosure timing, bounty and policy operation`)
  while holding the adjacent channel artifact (RFC 9116 / served `security.txt`).
- **C1 (recheck-line hygiene): no collision on the surface, but the token is contested.** Four lanes hold
  ingredients (chousa's field parser, kengaku's prose-recheck normalizer, kagi's foreign-cwd lesson,
  kotoba's cwd probe) and the fleet contract freezes `recheck` = *cadence*. Nobody gates knowledge-entry
  recheck lines as commands; nobody prefixes `cd`. The move must therefore stay lane-local and must not
  be phrased as a fleet standard — a fleet-wide "every recheck line is one shell command" rule would
  contradict `SOURCES-CONTRACT-v1:4`, `E09`, chousa's `META_RECHECK_UNSCHEDULED`, and kengaku's
  normalization, and would fail 221 sibling lines on sight.

## (c) One sentence for the L1's report (Sources & frontier / Trend verdicts)

> C1's after-receipt audits **37** recheck lines — the 35 frozen before-lines plus the 2 that C2's F10
> entries add — and the census limb is the fleet implementation `scripts/sources-census.sh`
> (sha256 `3fb72615…`), which reads only `corpus/SOURCES.md` and therefore does not itself evidence that
> the new entries' `S036`–`S040` ids are registered; the kasegi-only recheck convention is adjacent to
> chousa's `recheck`-as-cadence gate and kengaku's prose-recheck normalizer and is not a fleet standard
> (0 of 486 sibling lines carry a `cd <lane-root> &&` prefix, 221 fail `bash -n`).

## Affected axes

- `depth:verifiability` (4, lowest non-retired) — the move improves it: a receipt whose denominator
  matches the tree it scored, and whose census limb names the implementation actually run.
- `coverage` (7) — untouched; no F10 object is ceded, no frontier row changes.
- No harm limb: nothing here asks a sibling to change a byte, and nothing re-words C1/C2.

## Proposed move (one, bounded)

Amend only C1's **after-receipt and the report sentence**, not the claim text: have
`corpus/instruments/recheck-audit.py --json` emit `lines=37` with the two added lines marked
`added_by: C2` (the 35 before-lines keep their frozen identity), and have the report name the census
script by path **and sha256** while stating that its exit 0 covers the registry only. This is a
receipt-shape change inside kasegi's own instruments — no sibling file, no fleet script, no claim
re-wording — and it removes a D24-2-class "three different counts for one artefact" defect before a
verifier can file it.

## Risks

- **R1 (accepted, named):** restating `lines=35` in the receipt would make C1's own target unreachable
  by construction, since C2's admission adds the lines the counter counts. Fixing the denominator is
  the only option that keeps both claims true; the alternative (sequence C2 after C1's receipt) cannot
  hold because both land in one round commit.
- **R2 (report as adjacency, do not fix here):** two `sources-census.sh` implementations claim
  `SOURCES-CONTRACT-v1` (fleet `3fb7261…` vs kagi `8d30d627…`, the latter with the knowledge
  handshake and 70 cases). C2's verdict is only meaningful against the fleet copy; a reader comparing
  kagi's selftest count with kasegi's exit 0 conflates them.
- **R3 (report, do not act):** chousa's 2 command-form recheck lines
  (`corpus/knowledge/archived-export-intake.md:4,19`, `bash tools/research-gate.sh … --root .`) are
  relative-path invocations; measured from `/`, `test -e tools/research-gate.sh` → 1, from chousa's
  root → 0. Chousa therefore carries the same latent cwd defect kasegi is fixing (D24-5 class)
  alongside its 35 parse-fail lines. Kasegi must not present its criterion as a remedy for siblings.
- **R4:** kake refuses disclosure-policy operation without naming kasegi as the owner
  (`PROVINCE.md:283-288`). The report may claim adjacency; it must not claim that kake assigned the
  ground.

## Verification actually run

```
./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi   -> exit 0 (W04 x2)
git cat-file -e b49948f:corpus/instruments/recheck-audit.py                        -> absent at base
git ls-tree --name-only b49948f corpus/knowledge/ | wc -l                          -> 35
ls corpus/knowledge/*.md | wc -l                                                   -> 37 (2 untracked)
grep -rhE '^recheck:' corpus/knowledge | wc -l                                     -> 37
per-lane bash -n -c + cd-prefix census (table above)                               -> 523 / 221 / 36
sha256sum scripts/sources-census.sh kagi-shokunin/corpus/sources-census.sh          -> 3fb72615… / 8d30d627…
cd / && bash -c 'test -e tools/research-gate.sh' ; (from chousa root)              -> 1 / 0
```

No tool was installed or upgraded for this item. No sibling gate was executed; no file outside
`.ufo/waves/round-25/wave1/ConnectorSiblings.md` was created or modified.
