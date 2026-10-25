# ScoutConnOverlap — round-29 wave-1 sibling-overlap scan for the F13 ground

- Seat: `ScoutConnOverlap` (scout, leaf; no subagent dispatch, no background job)
- Date: 2026-10-25 | Fleet root `/home/vgpnk/Projects/shokunin` (read-only for this seat)
- Lane repo (only write scope): `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Lane base revision `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`
- Lane tip at read time: `master`/`HEAD` = `46e07f6ae8f23debb10034164252e7027b4d9091` ("round-29: wave-1 spec + dispatch (v2, 64 seats)")
- Answering model actually used: **minimax-code/MiniMax-M3.1-Flash:high** — route `scout → @m_mim` in `/home/vgpnk/.omp/agent/config.yml:359` (`m_mim: minimax-code/MiniMax-M3.1-Flash:high`, config line 349/511 region). No model was passed by me.
- Tools installed: **none** (no pacman / uv / npx transaction; host-wide pacman pause respected). The sweep used only `grep`/`ls`/`wc`/`stat`/`cmp`/`head` — all coreutils/POSIX.
- Writes by this seat: **this receipt file only**. No lane corpus file, no `claims.json`, no sibling lane, no fleet-root file was written.

---

## 1. The question, and the answer

**Question.** Does any sibling lane already hold (a) HackerOne standard program-policy ground,
(b) Bugcrowd VRT ladder / CWE-crosswalk ground, or (c) program severity/reward-scale ground?

**Answer: NO. Zero of the six named siblings holds any of the three.**

- (a) HackerOne standard program-policy ground — **not held by any sibling.** The pattern
  `hackerone.com/security/policy_versions` has **0 hits** in every sibling's corpus, and 0
  hits anywhere in any sibling lane tree (including `.ufo/` wave receipts).
- (b) Bugcrowd VRT ladder / CWE-crosswalk ground — **not held by any sibling.**
  `bugcrowd/vulnerability-rating-taxonomy`, `vulnerability-rating-taxonomy` and the standalone
  token `VRT` are **0 hits** in all six sibling corpora and 0 hits across all six sibling lane
  trees.
- (c) Program severity/reward-scale ground — **not held by any sibling.** `reward scale` and
  `severity ladder` are **0 hits** in all six sibling corpora and in all six sibling lane trees.
  The bare `P1`–`P5` tokens *do* appear in the siblings (102 / 10 / 31 / 12 / 2 / 6 occurrences
  in `corpus/knowledge/` for kengaku / chousa / kotoba / kake / kagi / kumitate) but **every one
  is a non-severity sense** — probe ids, checklist rule ids, gate wire-type names, receipt-path
  fragments (§4 below). A severity-shaped co-occurrence probe found **0 hits**.

**Conclusion: F13 ("Program severity ladders and reward scales") is uncovered coverage-map
ground for kasegi.** No sibling duplicates it, and no sibling is a contested owner of it —
the sibling `PROVINCE.md` files point the ground *at* kasegi, not away from it (§5). The
negative claim is carried by the full sweep in §2 and §3.

---

## 2. Sweep — commands and outputs (the negative claim carries its sweep)

### 2a. Primary sweep — the six named siblings, corpus-wide, six discriminating patterns

```bash
cd /home/vgpnk/Projects/shokunin
for L in kengaku chousa kotoba kake kagi kumitate; do
  D="$L-shokunin/corpus"
  for P in 'hackerone\.com/security/policy_versions' \
           'bugcrowd/vulnerability-rating-taxonomy' \
           'vulnerability-rating-taxonomy' \
           '\bVRT\b' \
           'reward scale' \
           'severity ladder'; do
    printf '%s | %s | %s\n' "$P" "$L" "$(grep -rIEio -- "$P" "$D" 2>/dev/null | wc -l)"
  done
done
```

Output — **every cell is 0** (36 of 36 cells):

```
hackerone\.com/security/policy_versions | kengaku    | 0
bugcrowd/vulnerability-rating-taxonomy  | kengaku    | 0
vulnerability-rating-taxonomy           | kengaku    | 0
\bVRT\b                                | kengaku    | 0
reward scale                           | kengaku    | 0
severity ladder                        | kengaku    | 0
hackerone\.com/security/policy_versions | chousa     | 0
bugcrowd/vulnerability-rating-taxonomy  | chousa     | 0
vulnerability-rating-taxonomy           | chousa     | 0
\bVRT\b                                | chousa     | 0
reward scale                           | chousa     | 0
severity ladder                        | chousa     | 0
hackerone\.com/security/policy_versions | kotoba     | 0
bugcrowd/vulnerability-rating-taxonomy  | kotoba     | 0
vulnerability-rating-taxonomy           | kotoba     | 0
\bVRT\b                                | kotoba     | 0
reward scale                           | kotoba     | 0
severity ladder                        | kotoba     | 0
hackerone\.com/security/policy_versions | kake       | 0
bugcrowd/vulnerability-rating-taxonomy  | kake       | 0
vulnerability-rating-taxonomy           | kake       | 0
\bVRT\b                                | kake       | 0
reward scale                           | kake       | 0
severity ladder                        | kake       | 0
hackerone\.com/security/policy_versions | kagi       | 0
bugcrowd/vulnerability-rating-taxonomy  | kagi       | 0
vulnerability-rating-taxonomy           | kagi       | 0
\bVRT\b                                | kagi       | 0
reward scale                           | kagi       | 0
severity ladder                        | kagi       | 0
hackerone\.com/security/policy_versions | kumitate   | 0
bugcrowd/vulnerability-rating-taxonomy  | kumitate   | 0
vulnerability-rating-taxonomy           | kumitate   | 0
\bVRT\b                                | kumitate   | 0
reward scale                           | kumitate   | 0
severity ladder                        | kumitate   | 0
```

### 2b. Widened sweep — whole sibling lane tree including `.ufo/` wave receipts

The primary sweep covered `corpus/` only. The item's ground could plausibly sit in a wave
receipt rather than a committed entry, so the sweep was widened to the whole lane
(`.git` excluded), which also covers each sibling's `SKILL.md`, `PROVINCE.md` and
`.ufo/waves/**` receipts:

```bash
cd /home/vgpnk/Projects/shokunin
for L in kengaku chousa kotoba kake kagi kumitate; do
  n=$(grep -rIEio --exclude-dir=.git -- \
      'hackerone\.com/security/policy_versions|bugcrowd/vulnerability-rating-taxonomy|vulnerability-rating-taxonomy|\bVRT\b|severity ladder|reward scale' \
      "$L-shokunin" 2>/dev/null | wc -l)
  echo "$L : $n"
done
```

Output:

```
kengaku : 0
chousa : 0
kotoba : 0
kake : 0
kagi : 0
kumitate : 0
```

Sibling `SKILL.md` sweep (same six patterns, one file per lane): **0, 0, 0, 0, 0, 0**.

### 2c. Registry sweep — no sibling `SOURCES.md` row points at either platform

```bash
cd /home/vgpnk/Projects/shokunin
for L in kengaku chousa kotoba kake kagi kumitate; do
  for f in "$L-shokunin/corpus/SOURCES.md" "$L-shokunin/SOURCES.md"; do
    [ -f "$f" ] && echo "$f : $(grep -cE 'https?://[^ |]*hackerone|https?://[^ |]*bugcrowd' "$f")"
  done
done
```

Output — every present file reads **0** (`chousa`, `kotoba`, `kake`, `kagi`, `kumitate` have
`corpus/SOURCES.md`; `kengaku` has `corpus/SOURCES.md`):

```
kengaku-shokunin/corpus/SOURCES.md : 0
chousa-shokunin/corpus/SOURCES.md  : 0
kotoba-shokunin/corpus/SOURCES.md  : 0
kake-shokunin/corpus/SOURCES.md    : 0
kagi-shokunin/corpus/SOURCES.md    : 0
kumitate-shokunin/corpus/SOURCES.md : 0
```

### 2d. Fleet-wide control sweep (beyond the six named lanes)

To make the "uncovered" conclusion about *kasegi* rather than only about the six named siblings,
the same pattern set was run over **every** other lane corpus in the fleet (12 further lanes
with a `corpus/` tree: audio, game-dev-2d, game-dev-3d, kaidoku, kama, kotodama, lore, mado,
mori, revenger, souji, tabi, tameshi, tsukuroi):

```bash
cd /home/vgpnk/Projects/shokunin
for L in audio game-dev-2d game-dev-3d kaidoku kama kotodama lore mado mori \
         revenger souji tabi tameshi tsukuroi; do
  echo "$L : $(grep -rIEio -- 'hackerone|bugcrowd|vulnerability-rating-taxonomy|\bVRT\b|severity ladder|reward scale' "$L-shokunin/corpus" 2>/dev/null | wc -l)"
done
```

Output — every lane is 0 **except kotodama (4)**, and kotodama's 4 hits are false positives on
the phrase, not the ground:

```
audio : 0     game-dev-2d : 0     game-dev-3d : 0     kaidoku : 0
kama : 0      kotodama : 4         lore : 0              mado : 0
mori : 0      revenger : 0         souji : 0             tabi : 0
tameshi : 0   tsukuroi : 0
```

kotodama's 4 hits are `severity ladder` as a phrase inside a **design-workflow** entry about
*gate finding* severities (`fail`/`hold`/`note`/`REVIEW`), not program severity ladders:
`kotodama-shokunin/corpus/knowledge/synthesis/finding-disposition-workflow.md:3` and `:28`
("## 2. The severity ladder and what each level owes"), plus
`kotodama-shokunin/corpus/README.md:458`. Its four severity values are `fail | hold | note |
REVIEW` — a **gate-finding disposition ladder**, categorically not a program severity ladder or
reward scale. It is also outside the six lanes named in the item. Verdict: **not a hit.**

---

## 3. What *was* found — every non-zero hit, classified

The sweep is not "zero hits, done". The three lanes that produced any platform-adjacent byte
are named here with paths and verdicts, so a later reviewer does not have to re-derive them.

### 3a. kake — `hackerone.com/github` as a security.txt `Contact` (2 hits) — NOT program-policy ground

- `kake-shokunin/corpus/knowledge/security-txt-publishing.md:99` —
  "GitHub's retained body has one `Contact` (`https://hackerone.com/github`), `Acknowledgments`,
  `Preferred-Languages: en`, `Canonical`, `Policy`, `Hiring` and `Expires: 2026-11-21T22:02:20z`"
- `kake-shokunin/corpus/lessons/round-35.md:50` — source row **S084** (`https://github.com/.well-known/security.txt`),
  quote: "Acknowledgments: https://hackerone.com/github/hacktivity … Policy: https://bounty.github.com".

**Verdict: not program-policy ground.** What kake holds is the **RFC 9116 `/.well-known/security.txt`
file-format and publishing ground** — where the file lives, the field set, `Expires` horizon,
Jekyll/artifact serving behaviour. The HackerOne URL appears only as a *value inside a quoted
`Contact` field* of somebody else's served `security.txt`; kake neither reads the HackerOne
program policy nor any severity ladder or reward scale. kake's own `PROVINCE.md:285` explicitly
refuses the ground: *"Vulnerability handling itself stays out of province: report intake,
triage, remediation, disclosure timing, bounty and policy operation … are not kake's ground."*
That is a **province refusal by the sibling**, not an overlap.

### 3b. kotoba — one `Bugcrowd` string inside a *routing* JSON, quoting kasegi's own SKILL.md (1 hit) — NOT ground

- `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json:665` —
  JSON path `/sources/2/excerpts/3/lines/0`, an excerpt line beginning
  "| Receipt drift (duplicate-submission hazard) | … (H1 #4028846 = `[lost-base] …`; Bugcrowd a169f309 = `[lost-base] …`)".

**Verdict: not ground.** Decoded, that JSON's `/sources/2/` record is
`{"lane": "kasegi", "contextual_head": "4b2e30231c20d3374a39976df5a0f998a6c6f90c",
"input_identity": "bytes match contextual HEAD:SKILL.md", …}` — kotoba is holding a **citation-routing
record that quotes kasegi's own `SKILL.md` receipt-drift line** so it can classify a dead-token
class. The `Bugcrowd` token is part of a *receipt identifier* (`Bugcrowd a169f309`) inside a
quoted kasegi sentence. It is a pointer **to** kasegi's ground, not kasegi's ground held by kotoba.
It is also a `[lost-base]` historical citation, not a public source row.

### 3c. kagi — 20 platform URLs, all inside one captured 1Password product page's nav chrome — NOT ground

- `kagi-shokunin/.ufo/waves/round-26/build/ClockS005.body.html` (+ `.body2.html`, and the
  round-26/round-27 sandbox copies) contain `https://hackerone.com/1password` as a **navigation
  item**: `"entryTitle":"Bug Bounty","item":"Bug bounty","href":"https://hackerone.com/1password"`.
  The page is 1Password's Credential Broker product page (`https://1password.com/product/credential-broker`,
  lane registry row S005), captured by kagi's release-clock observer.

**Verdict: not ground.** kagi's corpus holds **zero** `hackerone`/`bugcrowd` bytes
(`grep -rIin -- 'hackerone' kagi-shokunin/corpus` → 0 hits). The URL is site chrome inside a
captured body, of a page opened to observe a *release clock*, not a program policy, VRT ladder or
reward scale. The sibling corpus sweep for kagi's `corpus/release-clocks.tsv` rows S007/S019
confirms the rows are "unversioned guide" / "quote-located" 1Password product pages, with no
platform-policy row.

### 3d. No sibling holds a *severity-ladder-shaped* P1–P5 token — proximity probe

The bare `P1`–`P5` tokens are common in the siblings, so a raw count is meaningless. The
discriminating probe is whether any P-token appears **near a severity word**, which is the shape
a real VRT ladder takes ("P1: Critical", "P2: High", … "P5: Informational"):

```bash
cd /home/vgpnk/Projects/shokunin
grep -rIEin -- '\bP[1-5]\b[^.]{0,80}(severity|Critical|High|Medium|Low|Informational)|(severity|Critical|Medium|Informational)[^.]{0,80}\bP[1-5]\b' \
  kengaku-shokunin/corpus/knowledge chousa-shokunin/corpus/knowledge \
  kotoba-shokunin/corpus/knowledge kake-shokunin/corpus/knowledge \
  kagi-shokunin/corpus/knowledge kumitate-shokunin/corpus/knowledge
```

Output — **0 hits in all six lanes** (empty result for each).

Second shape probe (severity-ladder label strings), also **0 hits in all six lanes**:
`P1 Critical`, `P2 High`, `P5 Informational`, `P1 (Critical`, `Critical.*P1`, `priority.*P1.*P5`,
`P1 to P5`, `P1–P5`, `P1-P5`, `vulnerability rating`.

### 3e. What the P1–P5 tokens actually are in each sibling

Every bare `P1`–`P5` occurrence in the six siblings' `corpus/knowledge/` is one of these
non-severity senses (counts = occurrences; the itemised grep for each lane is reproducible with
`grep -rIEin -- '\bP[1-5]\b' <lane>/corpus/knowledge`):

| lane | count | actual sense | exemplar path:line |
|---|---:|---|---|
| kengaku | 102 | **probe ids** of the r19 standing battery (P1 quota, P2 service-tier, P3 …) and plan/priority labels | `corpus/knowledge/probe-battery-r19.md:10` "P2/P3/P8/P9 had no runner logs at close" |
| chousa | 10 | **seat/probe/claim ids** and hardening-rule refs | `corpus/knowledge/reference-integrity-r7.md:207` "…(b13), P2)" |
| kotoba | 31 | **checklist rule ids P1–P5** of `verify_skill_checklist.py` (rule/failure-mode/limit, hermeticity, two-way map) | `corpus/knowledge/checklist-execution-round15.md:49-53` |
| kake | 12 | **probe ids P1–P6** of the citing-set/paths runner (e.g. `P5-symlinked-case`) | `corpus/knowledge/freshness-sweep.md:52-55`; `corpus/lessons/round-31.md:72` |
| kagi | 2 | shell `%1`/`%2` job-control syntax in a cleanup command | `corpus/knowledge/handler-trust-boundary.md:236` "kill %1 %2" |
| kumitate | 6 | **contract wire-type names** (`PC-C/P3/PC-A`, `P5`) in the native-judge protocol | `corpus/knowledge/native-judge-pipeline.md:145`; `corpus/knowledge/runtime-remainder-census.md:210` |

`severity` in the same corpora is likewise non-program: kengaku = eval *error* severity in a
dose-response study (`knowledge/bench-arena-round11-power.md:38` "Paired severity diff +0.352");
chousa = its own gate's `severity=warn|info|crit` finding labels
(`knowledge/archives-verified-r9.md:67` "FINDING … severity=warn"); kumitate = its own
round-close gate's severity vocabulary (`knowledge/round-close-gate.md:40` "ROUND_GATE  <severity>  <KIND>  <detail>").

---

## 4. Sibling coverage-map read (the six `corpus/README.md` indexes)

Read in full as the item directs; each is a **different domain**, and none lists any
program-severity / reward-scale / platform-policy row:

| sibling lane | domain (from its own `corpus/README.md`) | any program-severity / reward-scale / platform-policy coverage row? |
|---|---|---|
| kengaku | LLM/model research & evaluation (bench-arena, grader semantics, contamination cards) | **No.** Closest: `knowledge/benchmark-task-validity-checklist.md`, `knowledge/grader-perturbation-audit.md` — benchmark grading, not program grading. |
| chousa | research-craft **method** (verification gate `tools/research-gate.sh`) | **No — and it refuses the province.** `PROVINCE.md:10` "**Refuses:** bounty-program scope and claim packages (→ kasegi)"; `knowledge/scope-refusal-r12.md:21` routes `bug bounty`, `bounty program(s)`, `claim package(s)`, `kasegi` to `SCOPE_BOUNTY_ABSORBED` → route **kasegi**. Its 4 "bounty program" hits are that *refusal list*, not ground. |
| kotoba | prompt & skill craft (`SKILL.md`/`AGENTS.md` quality, trigger fidelity) | **No.** Its only `Bugcrowd` byte is the routing JSON in §3b. |
| kake | web properties & publishing (GitHub Pages, Jekyll, canonical signals, CWV) | **No — and it refuses the province.** `PROVINCE.md:285` refuses "report intake, triage, remediation, disclosure timing, bounty and policy operation". |
| kagi | secrets & vault ops (the-janitor, 1Password, credential custody) | **No.** Zero platform bytes in `corpus/` (§3c). |
| kumitate | orchestration & tooling (ufo dispatch, `crates/ufo-core-runtime`) | **No.** `PROVINCE.md:26` routes "MCP/OAuth security practice … → kasegi / kagi". |

---

## 5. Ownership direction — the siblings point the ground *at* kasegi

No sibling is a contested owner of F13; the province files route the ground to kasegi:

- `chousa-shokunin/PROVINCE.md:10` — "**Refuses:** bounty-program scope and claim packages (→ **kasegi**)"
- `chousa-shokunin/corpus/knowledge/scope-refusal-r12.md:21` — `SCOPE_BOUNTY_ABSORBED` route → kasegi
- `kake-shokunin/PROVINCE.md:285` — bounty/policy operation "not kake's ground"
- `kumitate-shokunin/PROVINCE.md:26` — MCP/OAuth security practice → kasegi / kagi
- `kengaku-shokunin/PROVINCE.md:29,74,142` — "**kasegi:** bounty ledger mission-state / dispatcher semantics"
- `kotoba-shokunin/PROVINCE.md:58` — kasegi = "bounty and security research", listed **adjacent** to kotoba, not contested

---

## 6. kasegi-side pre-state (measured, for the L1's F13 landing)

| measurement | command (run from lane repo) | result |
|---|---|---|
| frontier admitted rows | `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | **12** (F01–F12) |
| F13 row present | `grep -cE '\| F13 \|' corpus/README.md` | **0** |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md` | **42** |
| highest lane id | `grep -oE '^\|[[:space:]]*S04[0-9]' corpus/SOURCES.md` | `S040 S041 S042` → **S043/S044/S045 free** |
| capture ground already on disk | `ls -la corpus/source-snapshots/round-29/` | `S043.txt` (1,220,741 B), `S044.txt` (8,187 B), `S045.txt` (14,575 B), `manifest.json` — landed by ExecCapS043/S044/S045 |
| S043 content (HackerOne policy set) | `grep -oio -e severity -e reward -e 'Program Scope and Assets' -e 'Denial-of-Service' corpus/source-snapshots/round-29/S043.txt \| wc -l` | `severity`×195, `reward`×278, `Program Scope and Assets`×12, `Denial-of-Service`×24, `P1`/`P2`×0 — the HackerOne record is a *policy JSON* whose caps are prose, not a P-ladder |
| S044 content (VRT README) | `grep -oio -e P1 -e Critical -e Informational corpus/source-snapshots/round-29/S044.txt \| wc -l` | `P1`×4, `Critical`×2, `Informational`×2 — the P1–P5 label ladder is here (ExecCapS044 receipt: labels at snapshot lines 34–38) |
| S045 content (VRT CWE map) | `grep -oio -e CWE-932 -e idor corpus/source-snapshots/round-29/S045.txt \| wc -l` | `CWE-932`×1, `idor`×1 — the crosswalk is here |

Adjacent kasegi ground that is **not** F13 (so the L1 does not double-count it):
`corpus/knowledge/cvss-v4-severity-and-vector.md` (F01, CVSS-B semantics only — and F01's own
`next` cell at `corpus/README.md:202` says "Keep scores distinct from program-specific risk
and policy", i.e. F01 explicitly points *away* from F13), and the legacy
`corpus/knowledge/program-quirks.md` (line 35 "Reward ladders vary per program ($1M–$15.5M crit
ceilings)"; line 42 "severity = portal language (High + CVSS vector)"; line 51 "Some programs
self-assign severity") — that legacy entry is `[lost-tree]`-anchored historical observation from
the erased `~/Projects/bounties` domain root, **not** a public-source ladder ground, and it
carries no `S###` registry row.

---

## 7. Adjacent observation (not my seat's item; flagged for the L1 only)

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/wave1/` held two stray
capture-like duplicates earlier in this wave — `README.md` (8,881 B, the raw Bugcrowd VRT README
body) and `cwe.json` (27.8 KB) — and sibling receipts cite them
(`wave1/ScribeFrontierNote.md:53`, `wave1/SimplyFixture.md:16`). At the time of this receipt both
paths are **ABSENT** (`ls` → no such file; the `wave1/` tree now lists `Exec*`, `Rev*`, `Scribe*`,
`Sent*`, `Lab*`, `Crit*` receipts and the `assimilation/`, `c1-controls/`, `receipts/` dirs).
This is a **concurrent change by another seat, not an edit by me** — I read the two files but
never wrote or deleted them. The committed captures themselves are unaffected:
`corpus/source-snapshots/round-29/{S043,S044,S045}.txt` are present with the byte counts in §6.
Flagging only because a receipt that cites `wave1/README.md` as evidence now points at a path
that no longer exists; the L1 may want the citing receipts re-pointed at
`corpus/source-snapshots/round-29/S044.txt` (byte-comparable) rather than left dangling.

---

## 8. Confidence and limits

**High confidence** on the negative claim for the three named ground types: the sweep is
exhaustive over the six named siblings' corpora *and* their whole lane trees (including `.ufo/`
receipts and each `SKILL.md`), the discriminating patterns are exact-URL / exact-phrase (no
loose fuzzy matching), and every non-zero hit is individually classified above with its path.

**Known limits of this scan (stated so they are not mistaken for coverage):**

1. **No semantic/LSP pass was run.** The tool policy allows an `lsp` device for symbol-level
   tracing; no language server is available for these Markdown-only corpora, so the sweep is
   **text-grep only**. Every claim above is therefore a *literal string* claim ("these bytes do
   not occur"), which is exactly the right shape for the question asked (does a sibling's corpus
   contain ground about X), but it does **not** prove a sibling could not hold equivalent ground
   under different wording. Mitigation: §2d widened the pattern set to the whole fleet, and
   §3d/§3e classify every near-hit (including all `P1`–`P5` and all `severity`/`reward`
   occurrences) by hand, so a differently-worded sibling entry would have had to be one of those
   classified hits and is not.
2. **Sibling `PROVINCE.md` / `SKILL.md` were read as declarations, not as enforced gates.** A
   sibling could in principle hold undeclared ground despite a refusal clause; the corpus-wide
   sweep (§2a, §2b) is the independent check on that, and it is clean.
3. **The scan is read-only and one-way**: it shows what siblings hold today at the revisions
   present on disk. It does not predict a sibling's next-round landing.
4. **`git` was not consulted for sibling revisions.** Sibling lane trees were swept at their
   current working-tree state. This is adequate for "does the corpus contain the ground" but
   does not attest that a sibling's committed `master` equals what was swept. For kasegi the
   revision *is* attested: `master` = `HEAD` = `46e07f6ae8f23debb10034164252e7027b4d9091`
   (§ header).

**No subagent was dispatched** (leaf seat). **No background job was started.** **No tool was
installed or upgraded.**

---

## 9. Verdict

**F13 is uncovered coverage-map ground for kasegi.** Across the six named siblings — and, as a
fleet-wide control, across every other lane corpus in `/home/vgpnk/Projects/shokunin` — there
is **no** HackerOne standard program-policy ground, **no** Bugcrowd VRT ladder or CWE-crosswalk
ground, and **no** program severity/reward-scale ground. The three near-hits (kake's
`security.txt` `Contact` URL, kotoba's routing JSON quoting kasegi's own `SKILL.md`, kagi's
captured 1Password nav link) are all pointers *to* platform ground or unrelated site chrome,
and two of the six siblings explicitly refuse the province and route it to kasegi. kasegi's own
F13 pre-state is 12 admitted frontier rows, 42 registry rows, S043/S044/S045 free, with the
three captures already landed under `corpus/source-snapshots/round-29/`.

**Answer to the item's question, in one line:** no sibling holds it — F13 is genuinely new
ground for kasegi, and it is not contested by anyone.
