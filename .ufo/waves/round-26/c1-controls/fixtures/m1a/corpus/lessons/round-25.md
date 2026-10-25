# Round 25 — kasegi

Lane: kasegi-shokunin. Round base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Two frozen claims
(`.ufo/waves/round-25/claims.json`, frozen 2026-10-25T08:13:38Z before any seat scored):
C1 depth:verifiability (the lane's lowest non-retired axis, score 4) and C2 coverage (score 7).
The round also carries the §2b frontier step and the §10 assimilation of one theme from
`/home/vgpnk/Projects/shokuknow/merge/kasegi/`.

**Which bytes each number reads.** `committed bytes` = the lane at `b49948f`, extracted with
`git archive`. `frozen surface` = the same 35 `corpus/knowledge/*.md` files at their post-fix
bytes (the round-25 copy at `.ufo/waves/round-25/c1-after-35/corpus/`, the two F10 entries
removed). `final tree` = the lane at round close (37 entries). All three C1 receipts were
produced by ONE instrument, `corpus/instruments/recheck-audit.py`
sha256 `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`; the index is
`.ufo/waves/round-25/c1-receipt-index.txt`.

## Claims

### C1 — depth:verifiability: every entry's own recheck line is a cwd-independent command

| surface | frozen limbs (the claim) | strict limbs (added after an attack) | exit |
|---|---|---|---|
| committed bytes (before) | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0` | `strict pass=6/35` | 1 |
| frozen surface (after) | `lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0` | `strict pass=35/35` | 0 |
| final tree (after, with F10) | `lines=37 total=37 pass=37 …` | `strict pass=37/37` | 0 |

Classes per receipt: before `executes=12 gated=0 broken=23`; frozen surface `executes=12
gated=23 broken=0`; final tree `executes=14 gated=23 broken=0`.

Before state, measured and independently re-derived (zero disagreements on 35/35 verdicts,
limbs, exit codes and command text, by a seat that implemented the predicate itself):
23 lines are `recheck: on-restoration — <cmd> (<note>)` hybrids that `bash -n` rejects
(`syntax error near unexpected token '('`), and 6 are cwd-dependent (`python3: can't open
file '//corpus/instruments/source-recheck.py'`, exit 0 at the lane root, 2 from `/`). Only
`pass=6` of 35 was ever executable from a foreign cwd. Fix: the 23 became
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && <cmd>  # on-restoration — <note>` and the
6 gained the same prefix; 29 files changed with `numstat 1 1` each, so no line moved (R6).

**The frozen limbs are equality checks, not success checks, and a critic showed it.** Limb (b)
asks that the two cwd runs agree, never that either succeeds, so `false corpus/knowledge/x.md`
or a `cd` to a nonexistent path passes the frozen three — the 23 syntax-error lines passed
limb (b) trivially by failing identically in both cwds. The claim is therefore met through the
strict exit rule, not through the frozen predicate alone, and the report says so. Adding a
fourth FROZEN limb would have re-worded the claim after seats had scored, which is why the
strict limbs sit beside it.

**The counter was repaired after the freeze, and that is disclosed rather than smoothed.** A
mutation-tester built the cheapest controls that skip the work and found the frozen three-limb
predicate reachable without doing it: `cd <lane> && true` in the `~/Projects/` spelling scored
`pass=35`, `cd <lane> && test -e corpus/knowledge/<own>.md` scored `pass=35`, and
`python3 corpus/instruments/recheck-audit.py --selftest` scored `pass=35` — and deleting one
line would have made `lines=35 pass=35` reachable again once C2 added a 36th entry. Four
strict limbs were therefore added BESIDE the frozen three (`cdroot`: the `cd` target is the
audited root; `instrument`: an existing `corpus/instruments/*.py` or a `test -d/-e ~/Projects/`
base test; `own`: the entry's own file, or `--source` with a `corpus/source-snapshots/`
manifest, or a bare base-state assertion; plus a completeness rule that `lines == total` and
`total > 0`), and the frozen three keep their original meaning. An `artifact` limb was tried
and dropped because `instrument` already implies it — a limb that cannot fail alone is not
reported as if it could. The instrument's `--selftest` carries one isolating fixture per limb
(14 cases, `failures=0`), including the degenerate controls the critic and the mutation-tester
produced. Receipts: `.ufo/waves/round-25/{c1-before-strict,c1-after-35,c1-after}.{json,txt}`,
controls in `.ufo/waves/round-25/c1-controls/`, mutant receipts in
`.ufo/waves/round-25/wave1/{mut-audit,mut-skip}/`.

**What the number means, in the counter's own words.** The receipt separates three classes by
what a line does at the lane root: `executes` (exit 0), `gated` (it parses and fails closed
because the base it guards is absent), `broken` (it cannot run at all). Before:
`executes=12 gated=0 broken=23`. Frozen surface after: `executes=12 gated=23 broken=0`. Final
tree: `executes=14 gated=23 broken=0`. So the honest sentence is **37/37 form-conformant, 14
execute today, 23 gated** — not "37 entries re-verified today". The 23 gated bases were
deleted in 2026-09-28 / 2026-10-12 and no recheck can make them live. A reviewer also showed that `anchorcheck.py` has no failing
exit path (`main()` returns `None`, so every verdict class exits 0) and that 19 of the 23
fail-closed lines would produce zero checked citations even after restoration; that is
routed debt for a later round, not a property this round's fix creates.

### C2 — coverage: F10, vendor-side disclosure policies as corpus objects

| counter | before | after |
|---|---|---|
| `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | 9 | **10** |
| `grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md \| wc -l` | 0 | **2** |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, rows 35 | **exit 0, rows 40** |
| `frontier-recheck-count.py` | `entries=10 pass=10 exit=0` | `entries=12 pass=12 exit=0` |

Two entries, one theme: `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`
(213 lines, four Japanese vendor pages) and
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (133 lines, Cisco's PSIRT
crosswalked against them on eleven dimensions). Both are re-grounded from this round's own
captures, not copied from the package. The before claim is specifically **no admitted frontier
entry** covered a product vendor's own product-handling policy: base `SOURCES.md:22` already
had S016 (Anthropic CVD policy) queued, not admitted, and `vdp-disclosure-packages.md:13,23-24`
held an intake-route fragment, not the vendor's standing policy object. A critic confirmed no
exact admitted entry overlap, and a connector confirmed no sibling lane holds F10 (chousa cedes
bounty-program scope by name; kake refuses disclosure timing and policy operation).

## Gate — assimilation set (S036–S040), opened 2026-10-25

Captures: `corpus/source-snapshots/round-25/S0NN.txt`, fetched by `capture-source.py` at
`2026-10-25T08:14:25Z`–`08:14:28Z`, http 200 each, sha256 as below. Manifest
`corpus/source-snapshots/round-25/manifest.json` binds 5 records / 40 assertions; every
assertion prints `occurrences=1` (`source-recheck.py --manifest … --source S0NN`, exit 0 for
all five). Lane ids continue the append-only registry from S035; the staged-package ids in
parentheses are pointers, never ids.

| admit | document | URL | capture sha256 (prefix) | located quote (≤25 words / ≤70 chars) | capture line |
|---|---|---|---|---|---|
| S036 (S055) | 脆弱性情報ハンドリングポリシー (Cybozu) | https://cybozu.co.jp/company/security-policy/ | `022ca4f4…` | 「クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。」 | 30 |
| S037 (S056) | FAQ（脆弱性報奨金制度） (Cybozu) | https://cybozu.co.jp/products/bug-bounty/faq/ | `b204aa7f…` | 「ご報告いただけます。ただし、サイトによっては報奨金制度の対象外の可能性があります。報奨金制度の対象製品をご確認ください。」 | 109 |
| S038 (S057) | 脆弱性報告制度 (GMOペパボ) | https://pepabo.com/contact/vulnerability-reporting/ | `09e077d3…` | 「また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。」 | 17 |
| S039 (S060) | 日立グループにおける製品脆弱性情報の開示プロセス (HIRT-PUB10008) | https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html | `657e7b4c…` | 「「対策情報を公表日に同時に公開する」「公表日一致の原則に従う」の２つです。」 | 519 |
| S040 (S068) | Cisco Security Vulnerability Policy | https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html | `b7f7b55f…` | "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018," | 58 |

**Reject — `vendor-cvd-policy-crosswalk-2026-10-23.md` (staged package file).** Three measured
grounds: (1) Q7 — its `recheck:` is prose with a command inside it, `bash -n` → exit 2;
(2) its `ground:` names `F20`, which the lane frontier does not have (`grep -cE '\| F20 '` → 0);
(3) Q3 — its own bytes of record list FOUR disclosure-trigger conditions
(`S040.txt` L301, L302–L304, L305–L308, L309), not the "two conditions" the entry asserts.
Flip condition: restate the count with line anchors, cite the lane id S040, and ground on an
indexed row — which is what the admitted lane entry does under a different name, so the
refusal is of the staged text, not of the theme.

**Corrections forced by the captures** (each is why the package is a pointer, not evidence):
the staged S056 anchor quotes a FAQ item that does not exist (`招待` occurs 0 times in all four
Japanese captures, so "invitation-only" is unsupported — the gate is an お申し込み form,
S037:101); the staged S060 anchor names no heading; the staged S068 "two conditions" is four;
and the non-litigation sentence refers to conditions the page does not enumerate; its prohibition list is separate, not an enumeration of those conditions.

**Access note.** A plain `curl -L` with a browser UA returns http 403 for S040; the capture
instrument's UA returns 200. A recheck must re-fetch with the instrument, or the row fails
closed on 403. `claims.json`'s planned reject reason ("Cisco unreachable this round") was
falsified by this round's own capture log and is corrected in place; the reject above stands
on the three criteria, not on reachability.

## Mistakes

**M25-1 · a `recheck:` field that is prose with a command inside it.** Class:
gate-not-applied-to-legacy-entries. Evidence: on committed bytes, 23 of 35 `recheck:` fields
begin with `on-restoration` and fail `bash -n`; all 23 are inside the 25 entries carrying the
round-22 provenance block, and the form entered at `c8b719d` (`git log -S'on-restoration —'
-- corpus/knowledge/claim-gates.md`). Captured-by: **Q7** (`corpus/QUALITY.md`, "an executable
recheck field contains a command, not prose beginning 'On each'") was written for newly
admitted entries and never swept over the legacy 25; and **R2** was already violated in the
same family — `SCORECARD.md:327` claimed "`recheck:` lines runnable 0/25 → 25/25", a
self-description no command backed. Fix: keep the fail-closed test, prefix the command with
`cd <lane root> &&`, demote the prose to a trailing `#` comment (29 files, `numstat 1 1`).

**M25-2 · a routed defect measured with one limb under-counts the surface.** Class:
under-measured-routed-defect. Evidence: D24-5 said "5 of 35 `recheck:` lines carry the cwd
prefix, so 30 are cwd-dependent"; the real split is 6 cwd-dependent + 23 unparseable = 29
non-conforming, and the two classes are disjoint. Captured-by: the round-24 closure compared
exit codes across two cwds and never ran a parse check; R3 ("an instrument verdict names its
matcher and definition") would have required the classes to be named. Fix: `recheck-audit.py`
prints `parse_fail` / `cwd_fail` / `paths_fail` separately and never a prefix count.

**M25-3 · one artefact, three numbers; one inference, four "measurements".** Class:
self-description-as-claim (R2). Evidence: the round-24 snapshot holds 76 quote assertions
(`sum(len(s['quotes']))` over `corpus/source-snapshots/round-24/manifest.json` = 76; receipt
95 OK = 19 sha + 76), while `instruments/README.md` said 62, `corpus/lessons/round-24.md:77`
and `SCORECARD.md:510` said 77. Separately, the bound-64→8 mutant's "8/8" was cited as
measured in four places while only the baseline-base 4/8 had a receipt. Captured-by: R2 for
the count; R11 for the mutant, which R11 itself only asked to be *disclosed*, not receipted.
Fix: one number with its counting command beside it; the mutant is now MEASURED on the landed
bytes (`88122e10…`: dispatch 8/8, containment 24/24 — `.ufo/waves/round-25/d24-3/receipt.txt`).

**M25-4 · two seats wrote into the fleet root.** Class: misroot (lane-relative path resolved
from the session cwd). Evidence: `ScoutFetchCisco.md` and `RevD24Counts.md` landed under
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-25/wave1/`. Root cause found and fixed in the
round's own spec generator: `item()` never interpolated the lane root into the owned-path
sentence, so 38/38 dispatched bodies carried a relative `Report:` path. Captured-by: none at
dispatch time — the wave `context` said "every `Report:` trailer path is relative to <lane>",
which is a rule for the seat, not a control on the renderer. Fix: the generator now emits
absolute owned paths; the misrooted file was copied byte-exact into the lane, verified with
`cmp`, and the fleet copy deleted (this is the one fleet-root deletion a lane may make).

**M25-5 · the pre-freeze control was not the cheapest control.** Class:
control-not-cheapest. Evidence: the round froze C1 with a do-nothing control (unchanged bytes
→ `pass=6`), which the target passes; a mutation-tester later showed a degenerate line
substitution reaches `pass=35`. Captured-by: the phase-4 rule ("build the cheapest control
that skips the claimed work") — the cheapest control here is a *substituted* line, not an
unchanged tree. Fix: the strict limbs, and `--selftest` now carries the three degenerate
fixtures (`degenerate.md`, `ownonly.md`, `selftest.md`) so the counter cannot be re-frozen
without them.

## Fixes that can fail

1. **Legacy recheck rewrite (M25-1).** Controls: the do-nothing control (unchanged bytes still
   print `pass=6`); the M2 control (strip one `cd` prefix → `cwd_fail=1`, `pass` falls);
   the M1 control (a prose tail outside the `#` → `parse_fail` rises).
   Receipts: `.ufo/waves/round-25/c1-controls/{do-nothing,M1-parse,M2-cwd,M3-paths,M4-degenerate}.*`.
2. **Per-class counting (M25-2).** Control: one synthetic prose-only value and one synthetic
   bare-relative command must land in different buckets; and the published total must be
   23 + 6 = 29 (a receipt printing 30 fails).
3. **One measured number per artefact (M25-3).** Control: run the counting command against a
   scratch copy with one quote removed — it must print 75; and
   `grep -rn '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md
   corpus/lessons/round-24.md` returns 0 hits after this round's corrections (the round-24
   lesson keeps its historical sentence and carries an appended erratum, R9).
4. **A mutant score is a measurement only with its receipt (M25-3, second limb).** Control:
   every "scores N/M" sentence must name a receipt file that exists and that prints the same
   figures; `.ufo/waves/round-25/d24-3/receipt.txt` is the specimen.
5. **Misroot control (M25-4).** Control: `git -C /home/vgpnk/Projects/shokunin status
   --porcelain` at round close lists only orchestrator-owned paths; any lane artefact there is
   the fail signal. Observed at close: 22 entries, none lane-authored (see the round report).

## Routed debt (named, not hidden)

- `anchorcheck.py` returns 0 for every verdict class and its `CITE` matcher has no
  `~/Projects/bounties/` arm: 22 of the 23 fail-closed recheck lines have their exit status
  decided solely by their `test` clause, and `citation-bases.md` prints a live loss while
  exiting 0. Not fixed this round (it would change an instrument's semantics mid-round).
- `capture-source.py`'s `TAG_RE = r"<[^>]+>"` is lossy: re-rendering S010's committed bytes
  deletes literal `<cassert>`/`<iostream>` text (36,452 → 26,571 B), and manifest records
  carry no `render`/`raw_sha256` field (0/23 at base). This is `considerthese/2026-10-24.md`
  proposal 2, mined this round: `considerthese: proposal 2 mined — snapshots record neither
  rendering nor raw digest (0/23 records), and the capture-time stripper silently deletes
  literal <cassert> from S010 (36,452→26,571 B); land a render/raw_sha256 record field and a
  snapshot-hygiene counter.` The code change is deferred to a round that can re-capture, so
  this round's captures stay comparable with the instrument that produced them.
- S040's capture carries U+FFFD at L108/L193/L203/L222/L479 (cp1252 bytes decoded with
  `errors=replace`); no quote crosses those lines. A future capture should declare its
  charset handling.
- `source-recheck.py --source` is a single-value argparse option: `--source A --source B`
  verifies only B. Both new entries chain one invocation per id; the instrument should accept
  repeats.
- The fleet's `recheck` census counts 523 lines across lanes, 221 of which fail `bash -n` and
  0 of which carry a `cd <lane-root> &&` prefix outside kasegi. This lane's convention is
  lane-local and is NOT a fleet standard: the SOURCES contract uses `recheck` for a cadence
  cell, and chousa/kengaku gate that field differently. Adjacency reported, not absorbed.
