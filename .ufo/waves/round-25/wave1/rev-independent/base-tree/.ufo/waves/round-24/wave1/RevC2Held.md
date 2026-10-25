# RevC2Held — is C2's "ground not held" premise true?

Read-only seat. Base observed: lane master `c2480b143120364728b40397926ffcf30a7309c8`;
claims frozen at `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` (parent, present, `git cat-file -t` =
`commit`). Every pointer below is a lane-relative path + line, resolvable from committed bytes.

## Verdict

| question | answer | evidence |
|---|---|---|
| Do the seven C2 patterns occur in the lane? | **NO — 0 hits**, exit 1 | §1 |
| Does that hold repo-wide, not just on the claim's file list? | **YES — 0 hits** on `master` | §1 |
| Do C2's counters read 8 and 0 at base? | **YES** — but the second counter cannot reach its own after-target (F-7) | §1.3, F-7 |
| Is "the lane holds **neither** an engagement document **nor** a statute" true? | **TRUE only for the two named objects. FALSE as a statement about authorisation ground or about "a statute".** | §2, §3 |
| Would a reader of `SKILL.md` alone know what an ROE is? | **NO** | §3 |
| Would that reader know whether the JP statute defines unauthorised access? | **NO — `SKILL.md` has zero legal vocabulary** | §3 |

So: C2 may proceed **only if it lands short on its own counter B** — with the round's own
renumbering, at most one of the two entries can cite an `S1xx` row, so the maximum attainable
after-value is 1 against a frozen target of 2 (F-7). Its coverage gain is also **narrower than
its `surface_changed` sentence suggests**, and the two entries must avoid seven already-held
propositions (§4). The exact false step is not the grep — it is inferring "0 string hits ⇒ empty
conceptual ground".

Disclosure: I did **not** open S123 / S039 / S040 / S041 (other seats own that; my item is
lane-internal ground). Whether those primaries say what the package claims is **UNVERIFIED here**.

---

## 1. (a) Detection run and classification

### 1.1 The claim's command, verbatim

```
$ grep -riE 'rules of engagement|engagement document|authorization letter|authorisation letter|statutory authorization|statutory authorisation|不正アクセス' SKILL.md corpus/ PROVINCE.md SCORECARD.md LOG.md
grep-exit=1   hits=0   bytes=0   stderr empty
```
Run at master `c2480b1`. Same pattern set via `git grep … d0a3f6a -- <same paths>`: **0 hits**
— the premise is true at the frozen base, not only at HEAD.

### 1.2 Classification: held-ground vs incidental

**Zero rows to classify.** No exact-pattern hit exists in any committed lane byte, so nothing
in the lane is scored "held-ground" by this detector.

Two gaps in the detector itself, both closed here:

1. The file list omits `README.md`, `AGENTS.md`, `SHONEN.md`, `considerthese/`, `plans/`.
   `git grep -inE '<same 7 patterns>' master` (all 227 tracked files) = **0 hits**. The zero is
   repo-wide, not list-shaped.
2. The only in-repo occurrences of these strings are in the **untracked assignment artifacts**
   (`claims.json:37`, `wave1-spec.json`, `wave1-dispatch.json`) — the task text, not lane
   knowledge. They must not be read as prior ground.

**Near-miss tier (concept-adjacent, classified incidental), so the next seat does not re-litigate:**

| hit | what it is | class |
|---|---|---|
| `SKILL.md:129` `engagement_known_issues.json` | Bugcrowd JSON object name in the policy-access row | incidental |
| `corpus/knowledge/policy-access-playbook.md:10` same object, `:12` `security.txt` stub ≠ scope | fetch-route bookkeeping | incidental |
| `corpus/instruments/citation-survival.tsv:369,1436` `/engagements/<slug>.json` | citation census rows for that Bugcrowd object | incidental |
| `corpus/knowledge/retirement-autopsies.md:82,134` `engagement in_progress_paused` | Bugcrowd state string — but `:134` draws an authorisation rule from it ("`engagement in_progress_paused` announcement → no testing grant exists → retire") | **incidental string, held-ground rule** (see §2.3) |

### 1.3 C2's own counters at base (reproduced)

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
8
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l
0
```
`corpus/knowledge/*.md` = 33 files = 8 frontier + 25 legacy. Both `before_expected` values hold.

---

## 2. (b) What the lane already says about authorisation

### 2.1 Frontier entries — the authorisation-bearing lines

| entry | line(s) | proposition held |
|---|---|---|
| F01 `cvss-v4-severity-and-vector.md` | 28, 41 | a score is not proof of existence, reachability, or **scope**; regulatory factors are outside CVSS |
| F02 `coordinated-disclosure-timelines.md` | 25, 38 | a coordinator "grants" its own grace; neither source "establishes a general legal requirement" |
| **F03 `authorization-safe-harbor-and-scope.md`** | 7-9, 13-16, 17, 20-25, 33-34, 37-39 | safe harbor, asset scope, **testing grant**, prohibited methods are separate observations; a badge does not establish permission; **"distinguishes a policy representation from a case-specific authorization decision"** (:17); rejects "badge authorises everything" (:33-34); **"These sources do not resolve third-party asset ownership, external legal protection, or whether an unlisted activity is authorized in a particular jurisdiction"** (:39) |
| F04 `ai-assisted-finding-validation.md` | 38 | guidance is not "authorization to examine any system" |
| F05 `cwe-top25-2025-methodology.md` | 8, 19, 32, 36 | a rank is not a "scope decision"; does not establish "authorization" |
| F06 `multiparty-vulnerability-coordination.md` | 15-16, 53-54 | FIRST practice is not a "universal legal deadline… or authorization to test"; "does not grant testing rights" |
| F07 `cna-assignment-and-vulnerability-rules.md` | 10, 32-33, 36, 53-56, 79 | assignment scope ≠ authority from expertise; no "permission to test" |
| **F08 `cra-manufacturer-reporting-duties.md`** | 18-19, 24, 73-76, 87 | jurisdiction/legal assessment not resolved; **explicitly rejects "CRA … therefore authorizes testing" — "Article 15 … does not establish an asset-scope or testing grant"** (:73-76); "no legal protection or compliance conclusion is inferred" (:76) |

### 2.2 Legacy entries — every authorisation-bearing line found

| entry:line | proposition held |
|---|---|
| `SKILL.md:39-40` | pipeline names the two artefacts: `scope-snapshot.json` from the policy read, `authorization-envelope.json` from scope bytes |
| `SKILL.md:50-52` | **"The only standing grant is one bounded passive policy read (AR14). Everything else needs a grant derived from verbatim policy text."** |
| `SKILL.md:61-97` | scope-snapshot schema: `in_scope_assets[]` (:63-66), `out_of_scope[]`+`prohibitions_verbatim[]` (:67-72), `testing_grant_verbatim[]` (:73-75), `safe_harbor` incl. null (:77-80), `coverage.status:"insufficient_for_authorization"` (:88-89) |
| `SKILL.md:158`, `:552`, `:559` | custodian chain: nonempty `matched_grant_id`, `scope_signal` exactly `NO_SCOPE_OBJECTION`; hard gates `written_scope`, `authorization` |
| `SKILL.md:240` | census: `authorization-envelope.json` 580/592 program dirs |
| `SKILL.md:615-618` | anti-pattern 4: authorisation/scope records are internal artifacts, never attached to a submission |
| `SKILL.md:636-640` | anti-pattern 6: empty `in_scope_assets` is "not observed", not "no scope"; anti-pattern 7: **"Claiming safe harbor the program doesn't grant"** |
| `SKILL.md:912-913` | ledger ladder carries `AUTHORIZED` — "which the live ledger never recorded a transition for" |
| `SKILL.md:1014-1023` | Frontier decision table (round 22): **5 rows only** (F01-F05); F06-F08 absent |
| `policy-access-playbook.md:12-13` | stub ≠ scope; terms acceptance is a forbidden external effect |
| `policy-access-playbook.md:17-24` | generic invitation prose "does NOT bind an asset"; `in_scope_assets:[]` = not observed |
| `policy-access-playbook.md:27-29` | **grant record fields: actor, asset, action, purpose, impact_ceiling, data_classes, time_window, credential_policy, `external_effect_authorization`** |
| `policy-access-playbook.md:35` | fail-closed recheck precedent (base absent ⇒ cannot pass) |
| `claim-package-contract.md:14`, `:52` | custodian receipts + `hard_gates` incl. `authorization`, `written_scope` |
| `claim-gates.md:31-38`, `:75` | `NO_SCOPE_OBJECTION` exact-signal rule, `matched_grant_id` required, hard-gate list |
| `retirement-autopsies.md:22-24` | RETIRE_AUTH classifier: `SPA shell\|login-walled\|no testing grant\|testing paused\|requires agreement\|…` |
| `retirement-autopsies.md:79-82`, `:104`, `:115`, `:122`, `:131`, `:134` | grant-absence retirement classes; terms-gated = forbidden external effect; paused engagement ⇒ no grant exists |
| `evidence-dir.md:25`, `:49` | `authorization-envelope.json` = "grant scope derived from snapshot bytes"; `authorization-envelope.v1.json` + `scope-supersession.json` |
| `ops-invariants.md:108` | "permission-limited staleness" |
| `ufo-archive-2026.md:47`, `:105` | "nothing authorized" non-execution manifests; `redaction-scan-authorization.json` |
| `ufo-workspaces.md:209` | the 5 hard gates, incl. `authorization` |
| `mission-control.md:78` | AR14 standing grant + policy playbook + NEVER list |

Zero authorisation hits: `mission-ledger`, `intake-and-finalize`, `repo-git-state`,
`target-checkouts`, `source-tree-loss-2026-09-28`, `root-loss-2026-10-12`, `citation-bases`,
`submitted-registry`, `operator-queue`, `vdp-disclosure-packages`, `claim-anatomy-sample`,
`ev-model`, `terminal-classes`.

### 2.3 The held propositions, rolled up (these are the ground that exists)

1. A grant is **written and verbatim**, derived from policy text — never inferred (`SKILL.md:50-52`).
2. A grant record has **fixed fields** (actor/asset/action/purpose/time_window/…) (`policy-access-playbook.md:27-29`).
3. Every action needs a **nonempty grant id + exact `NO_SCOPE_OBJECTION`** (`claim-gates.md:31-38`; `claim-package-contract.md:14`).
4. A **safe-harbor statement/badge does not expand scope or create permission** (`F03:8,20-21,33-34`; `SKILL.md:640,1021`).
5. **Policy representation ≠ case-specific authorisation decision** (`F03:17`).
6. **Prohibited methods are a separate observation** from the authorisation section (`F03:25`).
7. **Absent scope/authorisation stays unknown**; empty ≠ none (`F03:15`; `policy-access-playbook.md:23-24`; `SKILL.md:636-639`).
8. **Grant absence is a retirement class**, incl. paused engagement and terms-gated policy (`retirement-autopsies.md:22-24,134`).
9. **A statutory duty is not a testing grant** (`F08:73-76`), and legal/jurisdictional protection is explicitly **out of scope** of the held sources (`F03:39`; `F08:18-19`).
10. `AUTHORIZED` is a ladder state the ledger never exercised (`SKILL.md:912-913`).

What is genuinely absent: (a) a **named pre-engagement instrument** that confers authority prospectively from the asset owner; (b) **any statutory definition of unauthorised access**, incl. the consent carve-out; (c) the **access-manager = scope-owner** identification.

---

## 3. (c) The `SKILL.md`-alone reader

Pattern checks inside `SKILL.md` (1023 lines):

```
grep -nE 'jurisdiction|\blaw\b|legal|statute|prosecut|criminal|court' SKILL.md   → 0 hits
grep -nE 'rules of engagement|engagement document'                SKILL.md       → 0 hits
grep -nE 'S018|S029|S031|multiparty|cna-assignment|cra-manufacturer' SKILL.md    → 0 hits
```

- **ROE: not known.** The word "engagement" reaches `SKILL.md` only at `:129` as the Bugcrowd
  filename `engagement_known_issues.json`. The reader gets a different, narrower instrument:
  a per-action `authorization-envelope` whose grant is **derived from platform policy bytes**
  (`:39-40`, `:50-52`) — not an owner-agreed document written **before** the work, and with no
  concept of the document itself conferring authority for defined activities.
- **JP statute: not known, and no statute at all.** `SKILL.md` contains **no** legal, statutory,
  jurisdictional, prosecutorial or court vocabulary. It cannot tell a reader what 不正アクセス
  means, that a definition with a consent carve-out exists, or that a platform policy is not law.
  (The policy≠law distinction lives in corpus `F03:17,39` and `F08:73-76`, i.e. outside `SKILL.md`.)
- Additional lag: `SKILL.md:1014-1023` is the "Frontier decision table (round 22)" with **5 rows
  (F01-F05)**. F06-F08 were admitted in round 23 and never reached `SKILL.md`. A new F09 would be
  the fifth admitted topic absent from that table, so "SKILL.md alone" already under-reports the
  frontier by 3.

**Answer: no on both counts.** The ground `SKILL.md` alone covers is procedure (snapshot schema,
grant fields, custodian receipts, gates), not the two objects F09 would add.

---

## 4. What the new entries MUST NOT restate

Each line below is already load-bearing in the lane; a new entry that repeats it spends coverage
without adding it. "Instead" names the only defensible increment.

| # | do not restate | already held at | the new entry may only add |
|---|---|---|---|
| N1 | "safe-harbour text is not the legal definition of authorisation" **as the finding** | `F03:17` ("distinguishes a policy representation from a case-specific authorization decision"), `F03:39`, `F08:73-76` | the statutory **definition** (limbs), the **carve-out**, the **penalty**, the **受任者 identity**. At most one cross-reference sentence to F03's limit, not a section. |
| N2 | "a badge/statement does not expand scope" | `F03:8,20-21,33-34`; `SKILL.md:640,1021` | nothing — drop it or cite it |
| N3 | "an authorisation is a defined scope, written down" as a **generic** claim | `F03:7`; `SKILL.md:50-52`; `policy-access-playbook.md:27-29` | ROE-specific: **named instrument**, **pre-engagement timing**, **authority for defined activities without further permissions**, **published template (App. B)**, **glossary term** |
| N4 | "every action needs a grant / verbatim scope excerpt" | `claim-gates.md:31-38`, `claim-package-contract.md:14`, `SKILL.md:552,559` | a check that asks whether a **written ROE exists, is dated before the test, and names the activity** — the pre-work document, not the per-action receipt |
| N5 | "a statutory duty is not a permission to test" | `F08:73-76` (explicit rejection of "CRA … therefore authorizes testing") | the **offence definition**, not a second rejection of statute-as-grant |
| N6 | "prohibited methods are separate from the grant" | `F03:25` | nothing |
| N7 | "absent scope must stay unknown" | `F03:15`; `policy-access-playbook.md:23-24`; `SKILL.md:636-639` | nothing |

Also prohibited by the held record, and easy to copy in by accident from the package:

- **`authorised-testing-rules-of-engagement.md:34`**: "the corpus … has never held an English-language
  statement of what an authorisation *is* when it is not exceeded." **False as written** — see F-1.
- **`statutory-authorization-in-three-traditions.md:9`**: `ground: F12 (new frontier item…)` —
  wrong id (C2 admits **F09**) and, in the lane, an F12 does not exist. **:2** titles the entry
  "three traditions" while its own `:43-47` admits only the Japanese tradition is grounded.
- The statutory entry's own H1 thesis (`:13-15`) is N1 verbatim; keep the statute, cut the thesis.

---

## 5. Findings

*(ranked by severity; ids follow discovery order)*

### F-7 (critical, claim-killing) — C2's counter B cannot reach 2 under the round's own renumbering

The frozen instrument:

```
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l     # before 0, after_target 2
```

`S1[0-9][0-9]` matches **S100-S199 only**. Under the plan the `SOURCESRows` seat derived
(`.ufo/waves/round-24/wave1/SOURCESRows.md:30-32`, `:100-103`):

| admitted entry | rows it cites | matches `S1[0-9][0-9]`? |
|---|---|---|
| `authorised-testing-rules-of-engagement.md` | S123 → **S124** | **yes** |
| `statutory-authorization-and-unauthorized-access.md` | S039→S040, S040→S041, S041→S042 | **no** (S040-S042) |

So the **maximum attainable after-value is 1**, against a frozen target of 2. The counter is not
mis-executed or unreproducible — it is reproducible and reads one short of its own target, which
is the claim failing its own predicate. The three statutes cannot move it: staged ids S039-S041
were never S1xx, and no renumbering rule in the lane allocates them there.

Options, and only one is honest under `claims.json`'s own note ("a rule changed after a seat
scored is not the claim's rule"):

1. **land C2 short and say so** — counter A 8→9 achieved, counter B 0→1 against target 2, with
   the reason (instrument scoped to S1xx row numbering, only one candidate carries such a row).
   This is the "honest stop" the kill rule contemplates.
2. Re-register the two statute rows as S1xx rows *before* any entry lands, and record that the
   allocation was chosen to fit the instrument — which converts the counter from a measurement
   into a definition and should be refused.

Option 1 is the only one that keeps the counter meaningful. A reader who wants a number that
actually measures "entries citing rows first registered this round" must have such a counter
frozen for round 25, not substituted into round 24.

### F-1 (major) — the ROE package's novelty claim is falsified by held bytes

`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md:31-35`
asserts the corpus "has never held an English-language statement of what an authorisation *is*
when it is not exceeded." The lane holds exactly that:

- `SKILL.md:50-52`: "The only standing grant is one bounded passive policy read (AR14). Everything
  else needs a grant derived from verbatim policy text."
- `corpus/knowledge/policy-access-playbook.md:27-29`: grant fields `actor, asset, action, purpose,
  impact_ceiling, data_classes, time_window, credential_policy, external_effect_authorization`.
- `corpus/knowledge/authorization-safe-harbor-and-scope.md:7-9`: assets, grant, prohibitions are
  separate observations a reviewer checks every claimed action against.

The accurate gap is narrower and is the one worth writing: the lane has never held an
**owner-side engagement document** (agreed with the asset owner, established **before** the work,
conferring authority for defined activities) nor any **legal** statement of authorisation.
If EntryRoE copies the package sentence, Q4/Q5 fail on a false claim of novelty; the reviewer of
the entry should require the sentence be replaced by the narrower one.

### F-2 (major) — the statutory package's thesis is held; only its content is new

`…/statutory-authorization-in-three-traditions.md:13-15` opens "Safe-harbor text tells you what a
platform promises. It does not tell you what 'authorized' means in law." That is `F03:17`+`:39`
and `F08:76`. The increment is `:17-33` (three limbs, carve-out, アクセス管理者, penalty
divergence). As drafted, roughly half of the entry's prose is restatement, so the coverage credit
would be "new file, old rule" — exactly the thing C2's kill rule is meant to catch.

### F-3 (major) — C2's "rows first registered this round under addendum 10" has no referent

`claims.json` C2 predicate requires "two knowledge entries, each sourced from rows first
registered this round under addendum 10". Searches, all read-only:

- lane: `git grep -in 'addendum' master` → 7 hits, all round-report/lesson prose
  (`.ufo/reports/round-21/kasegi.md:217`, `.ufo/waves/round-23/…`, `LOG.md:435`,
  `corpus/lessons/round-23-verifier-spotcheck.md:17`) — **no source-row addendum ledger**.
- merge package: `SOURCES.append.md` has **no headings**; `MERGE-REPORT.md` has 0 "addendum".
- shokuknow: no `addendum N` numbering outside `.deepresearch`/`.qcache` prose.

Additionally `SOURCESRows` is told to read
`.ufo/waves/round-24/assimilation/renumber-map.tsv`, which **does not exist**; that directory
holds only `census-before.txt`, `collisions` (5 B), `reg-ids`, `staged-ids`.

Consequence: as written the predicate is not checkable by a verifier. Either the append block
produced by the `SOURCESRows` seat *is* the "addendum", in which case the claim must name that
artifact, or the clause must be struck. (Registry reality: `corpus/SOURCES.md` holds S001-S031
only; S039-S041 and S123 are absent, so any new row is an append, which R8 permits for new ids.)

Independently confirmed after my check: `.ufo/waves/round-24/wave1/SOURCESRows.md:17` reports
"`find … -name '*renumber*'` returns nothing" and derives the map itself:
**S123→S124, S039→S040, S040→S041, S041→S042** (`:30-32`). That mapping is what makes F-7 land.

### F-4 (major, cross-claim) — F09's sources are outside the round-24 capture plan

State observed at 04:18-04:20 (after my baseline runs):

- `corpus/source-snapshots/round-24/` now holds `S001..S015.txt` + `S032..S035.txt`, **no
  `manifest.json`** — so no recheck can run yet, for F01-F08 or for F09.
- The `CaptureTool` item's own scope is "a `corpus/source-snapshots/round-24/manifest.json`
  covering **S001-S015**". The rows F09 would cite are **S124** and **S040-S042**; none of them
  is in the capture set and none is planned by that item.

| candidate | line | shape | offline outcome |
|---|---|---|---|
| ROE | `:4` | `recheck: 90d — re-fetch the PDF and grep -F the four lines (ran 2026-10-24)` | prose, not a command; no capture ⇒ cannot exit 0 |
| statute | `:8` | `recheck: 730d — curl -sSL https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 …` | network-only; no capture |

`QUALITY.md` Q7 requires "an executable recheck field … a pinned captured-source comparison";
`Q1` requires the command to fail closed when the base is absent. Neither candidate satisfies
both, and the round's capture seat is not scoped to fix them. C1's predicate is explicitly "the
**eight** Frontier knowledge entries", so C1 survives F09 landing with these lines — but round 24
then ends with **9** frontier entries whose newest cannot be re-derived from committed bytes, and
any downstream sentence of the form "every frontier entry rechecks from committed captures"
becomes false. Required before admit (and it is a new requirement, not a silent scope add):
capture S124/S040/S041/S042 into `corpus/source-snapshots/round-24/`, add their manifest records,
and make `recheck:` the `source-recheck.py --manifest … --source …` shape used by F06-F08.

### F-5 (minor) — admitting F09 leaves two committed files stale

- `PROVINCE.md:35-38`: "Frontier … **F01–F08**".
- `SKILL.md:1014-1023`: decision table has 5 rows (F01-F05) — already 3 behind; F09 makes it 4.
- `SCORECARD.md:328,404` cite "frontier 8/8" / "5/8" figures; a 9-topic set needs the new
  denominator stated, not silently re-read.

If any of these is touched, R6 applies (existing cited line numbers must not move).

### F-6 (minor) — detector hygiene, for the record

The claim's grep file list is not repo-wide (omits `README.md`, `AGENTS.md`, `SHONEN.md`,
`considerthese/`, `plans/`). I closed it via `git grep … master` = 0 hits, so the C2 premise
stands on all tracked bytes; a later verifier should cite the repo-wide command, not the list.

---

## 6. Residual risk and verification gaps

1. **UNVERIFIED:** whether S123 / S039 / S040 / S041 exist and say what the package claims
   (status, bytes, sha256, the 第十一条 拘禁刑-vs-懲役 divergence). Owned by `SrcNISTROE` /
   `SrcJPStatute`; nothing in the lane can answer it today.
2. The 25-legacy sweep used an authorisation vocabulary set
   (`authoriz|authoris|consent|permission|scope|permitted|lawful|statute|legal|grant|prohibited|forbidden|may not`)
   plus targeted reads of the 14 files with hits. A proposition phrased without any of those
   stems (e.g. "the owner said yes") would not surface; I found none in the 14 files read.
3. `corpus/lessons/` was not swept (lessons are history, not knowledge entries); if an r22/r23
   lesson already frames the ROE gap, an entry restating it would be redundant in a different way.
4. No file outside `.ufo/waves/round-24/wave1/RevC2Held.md` was written. No build/lint/test run
   (not part of this item). No tool installed or upgraded.
