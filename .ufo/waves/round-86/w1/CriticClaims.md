# CriticClaims — kasegi round 86, attempt 1

Seat: CriticClaims. Base `d7296645c2cd9f631329fa8e2f38328a4c9c89a5`, freeze `252df0c90c066d83d229e3107811a6bc05e8feed`.
Scratch: `/fast/scratch/hyaku/kasegi-r86/CriticClaims/` (TMPDIR explicit; deleted before yield). Receipts: `.ufo/waves/round-86/w1/CriticClaims-receipts/`.
All measurements are over committed bytes in `git clone --shared` checkouts under the scratch root (`.git` present, parent holds no `MISSION.md`), never the worktree of another seat.
No lane file outside my wave dir was written; no `S<digits>.txt` was copied into the wave dir.

**Verdicts up front.**

| Claim | Verdict | One-line reason |
|---|---|---|
| C1 depth:verifiability | **HOLDS at landing `fdb5f4af` (596/1716); SUPERSEDED at the tip `e73c1f9` (596/1720)** | map rebuilds byte-identically and 596/1716 passes at `fdb5f4af`; but **4 of the 203 keys are quoted round-40 manifest `path` field values, not citations** (L1 ReviewC1Semantics Finding 1, independently confirmed in A9). Commit `e73c1f9` reverts them; the corrected tip reads 596/1720 in a clone and 597/1720 at the real lane path, and the frozen 596/1716 target fails M1/M2/M3 there. Nominal in class (internal repoint, score held at 4); 79/89 exclusions mechanical; 75 unbackticked residue. |
| C2 coverage | **BREAKS — unsatisfiable as frozen; L1 killed it as frozen** | E2 requires a byte-identical copy of S122 inside the package; the frozen S122 carries a presigned S3 URL with an AWS `X-Amz-Security-Token`; the r43 gate's R-NOSECRET rejects those bytes. E1 passes only when S122 is absent, E2 only when present. P1 (`E0–E5 pass`) and P2 (`WELL-FORMED`) cannot both hold. The L1's post-freeze redaction + rebuilt package passes E0–E5 at the worktree, but that is post-freeze repair, not admission evidence, and it stales the frozen P2 pins of both claims (B8). |
| C2 subject binding (E0) | **BREAKS its stated purpose** | a package whose body is the r85 1913733 package, or the r43 CVE-2025-9086 exemplar, passes E0/E3/E4 and full E0–E4 once the heading, one URL and the Pricing block are swapped. |

---

## 1. C1 — depth:verifiability (knowledge-scope repoint)

### A1. Is the move nominal? (HOLDS, nominal in class)

The instrument is `resolve.py`'s own classification, and the move is the lane's citation-vocabulary rule already exercised at r49 (`citation-ground-check.py`) and at r85 C1 (SKILL.md 158/741 → 167/732). The r86 scope (`corpus/knowledge/*.md`, 98 files) is a new input for the same rule; the claim itself says the integer score is not claimed to move. Under the r85 spot-check precedent ("internal-citation repoint", score held at 4) this is admissible as a measured move, but it is not a new capability and not a score move. The gain is internal only: every map value is a lane-root-relative path that `resolve.py` classifies INTERNAL; external RESOLVES do not move.

Workload, reproduced from the base scope: **203 map keys, 376 backticked occurrences, 292 lines** (`keys_hit=203`, `bad_lines=292` in the do-nothing limb; `c1-excluded.txt`). Of those keys, **4 are not citations** (quoted round-40 manifest `path` values; A9), so the honest count is 199 citations + 4 quoted data values; the claim's "203 distinct bare snapshot citations" is false by 4. The report must say "distinct" and must not say "203 citations changed".

### A2. Independent rebuild and positive (HOLDS)

```
cd <clone of 252df0c at base rev d729664>
python3 -B .ufo/waves/round-86/c1/build-map.py --lane . --rev d729664 --out rebuilt-map.json --excluded rebuilt-excluded.json
```
Observed: `MAP keys=203 excluded=89`; rebuilt map sha256 `dd40455a…0bce12` = frozen map; rebuilt excluded sha256 `920641e6…218ac4` = frozen `excluded.json` (`c1-map-rebuild.txt`). The frozen map is exactly the builder output on this host.

Positive in a clean clone with the frozen applier and meter:

```
APPLY files_changed=14 keys=203
KNOWLEDGE-METER base=398/1721 after=596/1716 target=596/1716 keys=203 mirror_absent=True
LIMB M1..M6 pass
KNOWLEDGE-METER-RESULT pass rc=0
```
(`c1-meter.txt`). Do-nothing on the same clone: 398/1721, M1/M2/M3 FAIL, rc 1. The frozen `c1-controls-r86.sh` replayed under my scratch reproduces the committed receipt after normalising only the scratch path (`diff` rc 0; `c1-controls-replay.txt`, `c1-controls-diff.txt`).

### A3. Does the frozen root hide a defect? (root dependence is real; the root choice understates, it does not inflate)

- Base measured **against the real lane path** (lane sits in the fleet root, so `../MISSION.md:49-56` in `corpus/knowledge/source-tree-loss-2026-09-28.md:315` resolves to the fleet MISSION): `rate=399/1721`.
- Base measured in the frozen `git clone --shared` root (parent has no `MISSION.md`): `398/1721`.

(`c1-meter.txt`, last block.) The one-line delta is exactly that walk-out token, which `resolve.py` classifies INTERNAL at the fleet root by its documented unconfined REL branch. The frozen root therefore **deflates** the claim by one resolution; it does not manufacture one. The host_note discloses it, but the C1 statement ("moves from 398/1721") omits the qualifier. Carry it: 398/1721 and 596/1716 are scratch-clone numbers; at the real lane path the same two states read 399/1721 and (predicted by the same +1) 597/1716. P1's "parent holds no MISSION.md" is what pins it.

### A4. Do-nothing / cheaper forgery hunt (no forgery found; the 89 exclusions are the real finding)

- **Do-nothing**: fails M1/M2/M3 (rc 1).
- **Partial / de-cite / pad / wrong-file / wrong-sha**: all rc 1; replayed (`c1-controls-replay.txt`).
- **Structure of the limbs**: M2 (`removed == keys`, `added ⊆ values`) plus M3 (per-line base→after equality with key replacements, `hit == keys`) fixes the after token set exactly; M4 forces each value to be the unique tracked file with the key's basename, with the key's anchor; M5 is range; M6 pins the map bytes. I found no alternative tree that prints 596/1716 without the frozen map. The one residual avenue is editing `corpus/instruments/resolve.py` at landing to inflate INTERNAL; the counting command alone cannot see that. **P2 is load-bearing** — the L1 must run it, not only P1.
- **The 89 excluded tokens are not 89 genuine ambiguities.** `git ls-files` basename multiplicity:

| basename | excluded tokens | tracked copies | distinct sha256 | verdict |
|---|---:|---:|---:|---|
| S102.txt | 70 | 2 | 1 (`6ebb8552…`) | mechanical (byte-identical scout copy) |
| S041.txt | 6 | 23 | 1 (`e18acbf9…`) | mechanical (round-26 fixtures) |
| S029.txt | 1 | 41 | 1 (`82514478…`) | mechanical (round-25 fixtures + nested lane copy) |
| S040.txt | 1 | 33 | 1 (`b7f7b55f…`) | mechanical |
| S100.txt | 1 | 3 | 1 (`cf834a65…`) | mechanical |
| S069.txt | 10 | 3 | **3** | genuine ambiguity (three different bytes: round-44 canonical `0932279c`, round-44 source-recon `7e2004ba`, round-29 fetch `41c79a5d`) |

So **79 of 89 excluded tokens (89%) have byte-identical duplicates**; the exclusion is forced by M4's strict "exactly one tracked file with this basename" rule, not by an unresolvable referent. The duplicate basenames come from tracked copies under `.ufo/waves/` — including a 115-file nested lane copy at `.ufo/waves/round-25/c1-after-35/`. The claim's 34.73% is therefore a **conservative floor**, not a ceiling. This does not falsify the frozen claim (the map is exactly what the claim says), but the L1 must not present it as the reachable maximum, and a round-87 rule ("all tracked copies of the basename are byte-identical and exactly one lies under `corpus/source-snapshots/` ⇒ repoint to it") would safely repair 79 more tokens.

### A5. Meter-invisible residue (qualifier)

75 occurrences of map keys remain **unbackticked** in the after knowledge scope, so the meter cannot see them and the applier does not touch them. They are mostly prose references such as `— S016.txt:L9` in `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` (23) and table/quote attributions in the GitHub/CVE/ZDI knowledge files (`c1-excluded.txt`, second half). Same class as the r85 spot-check's wording note ("16 bare non-backtick occurrences remain"); say "the backticked tokens were repointed", not "every reference".

### A6. Does any repoint break an existing lane gate? (no)

- `corpus/instruments/citation-ground-check.py` (r49 C1 gate) run at base and at map-applied after, same lane: **byte-identical output**, `verdict=failed`, rc 1, 8 pre-existing findings (`SOURCES.md:142`, seven fleet-relative cites in lessons/QUALITY), `ledger-rows=68` (`c1-ground-base.txt`, `c1-ground-after.txt`, `c1-ground-diff.txt`). It does not see the bare snapshot names at all (it tests `corpus/<token>`, not a basename search), so C1 neither helps nor harms it.
- No key occurrence sits inside a fenced code block (0 of 376), so no reproducible command string is rewritten.
- `density.py SKILL.md --label x` → mean 273.2; `git diff d729664 252df0c -- SKILL.md` is empty, so P4 is a true no-harm check but a do-nothing one (C1 cannot lower density because it does not touch SKILL.md).
- `corpus/instruments/citation-survival.*` (census of record) is not regenerated. It was already stale (r85 routed defect 4); C1 changes more of the tree it describes without refreshing it. `census-freshness-check.py` was already failing; C1 does not make it pass. Carry the routed debt explicitly.

### A7. Anchors (range holds; semantic pass not in the predicate)

197 of 203 keys carry an anchor; **0 anchors land on an all-blank target**; six sampled anchors (GitHub advisories, CVE Services API, ZDI policy, kernel reporting, Anthropic CVD) match the citing sentence, including the ZDI `S075.txt:22` quote at the end of a long line (`c1-anchor-samples.txt`). M5 is range-only (`1 ≤ N ≤ M ≤ lines`); a semantically wrong but in-range anchor would still pass. No wrong anchor was found in the sample, but the claim should not be read as "anchors verified".

### A8. Worktree drift (none)

The lane's uncommitted `corpus/knowledge/*.md` changes equal the frozen map applied to the base bytes for **all 98 files, 0 mismatches** (`c1-worktree-drift.txt`) at the pre-correction state. Freeze does not touch `corpus/knowledge` (`git diff d729664 252df0c -- corpus/knowledge` empty), so base == freeze for this scope and P3/M3 coincide. The L1 committed those bytes at `fdb5f4af` and then reverted 4 keys at `e73c1f9` (A9); the tip is no longer the map-applied state.

### A9. Four of the 203 keys are not citations — the frozen claim is false by 4 (L1 corrected at `e73c1f9`; confirmed here)

The four keys `S020.txt`, `S021.txt`, `S023.txt`, `S025.txt` occur on the `- Pin:` lines of four knowledge files. Each line already cites the full snapshot path (`corpus/source-snapshots/round-40/S0XX.txt`); the backticked bare name is the **quoted round-40 manifest `path` field value** (`id \`S020\`, path \`S020.txt\`, same digest…`). Repointing it rewrites the quoted manifest record, not a citation. The L1's ReviewC1Semantics Finding 1 caught it; commit `e73c1f9` restores the four lines to base bytes.

Confirmed independently over the corrected tip `e73c1f9` at the real lane path:

```
KNOWLEDGE-METER base=399/1721 after=597/1720 target=596/1716 keys=203
LIMB M1 FAIL after=597/1720
LIMB M2 FAIL removed=199 keys=203 … unrepaired=4
LIMB M3 FAIL same_files=True bad_lines=4 keys_hit=203
KNOWLEDGE-METER-RESULT fail rc=1
```

(`c1-tip-vs-landing.txt`; in a scratch clone the same tip is 596/1720, per L1 `c1-correction-r86.txt`.) So:

- At the landing commit `fdb5f4af` the frozen predicate P1–P4 passes (L1 `c1-landing-r86.txt`; my clone reproduces 596/1716).
- At the lane tip the frozen target is false in both roots and the claim's "203 distinct bare snapshot citations" is false by 4 — there are **199 citations and 4 quoted data values**.
- The builder's rule (any backticked `S<digits>.txt`, GONE, unique basename) over-captures quoted manifest fields; the r85 ExecC1Hunt rule ("a command string is not a citation") was not applied to quoted `path` values. This is the substantive C1 defect, and the L1's correction is right. The frozen claim must be reported as superseded/refiled with 199 keys and a 596/1720 target, not as a clean pass at the tip.

---

## 2. C2 — payer-side package for HackerOne IBB 1997312

### B1. The frozen claim is unsatisfiable: E1 and E2 are mutually exclusive on S122 (BREAKS)

`corpus/source-snapshots/round-86/S122.txt` contains two presigned S3 avatar URLs with `X-Amz-Date=20261107T005829Z`, `X-Amz-Expires=3600`, `X-Amz-Credential`, `X-Amz-Security-Token` and `X-Amz-Signature` (values masked; 2 occurrences each; `c2-s122-credential.txt`). The generated token's window is 2026-11-07T00:58:29Z + 3600 s = **01:58:29Z**; at review time (01:20:12Z) it was **still inside its validity window** — a live AWS STS session token committed in tracked lane bytes at the freeze. It expires within the hour, but the capture pipeline commits live credentials for one hour after every fetch.

Scanning every tracked `corpus/source-snapshots/**/*.txt` with the same six gate patterns finds one other hit, `round-49/S078.txt`; its value is a 17-char lowercase/digit documentation placeholder (`abc123…`), not a credential. S122 is the only real one.

The frozen r43 gate's R-NOSECRET walks the **whole package tree** and its `credential` pattern matches `Token=<99 chars>`:

```
RULE R-NOSECRET verdict=fail detail=hits=1,first=evidence/S122.txt,shape=credential
package=… rules=8 pass=7 fail=1 verdict=DEFECT exit=1
```

(`c2-mutual-exclusion.txt`, FA.) The frozen e2e counter E2 requires `evidence/manifest.json` artifacts whose **bytes equal** the committed `S122.txt` and whose recorded sha equals the round-86 manifest sha (`e2e-check.py` E2). Therefore:

| package state | gate (E1/P2) | E2 |
|---|---|---|
| S122 + S123 in `evidence/` and the manifest | **FAIL** R-NOSECRET `shape=credential` | pass (`bound=S122,S123`) |
| S122 + S123 removed from the package | **pass** 8/8 `WELL-FORMED` | **FAIL** `bound=none` |

Both rows are executed receipts (`c2-mutual-exclusion.txt`; FA is the r85 package plus r86 evidence/pricing, FA-noev is the same minus S122/S123). There is no third state: the gate rejects `..`/absolute/symlink artifact paths, skips no directory in the walk, and fails closed on unreadable files. P1 (`E0–E5 pass`, `limbs=6 rc=0`) and P2 (`verdict=WELL-FORMED`) cannot both hold at any landing commit. The claim's kill rule says C2 fails if any predicate is false — so **C2 must be reported failed/blocked this attempt**, not landed with a note.

This is the control-suite gap: the frozen controls contain **no positive full-package run**. `positive-pricing` runs `--pricing-only`; the b3 controls' `E1 FAIL gate_rc=1` was never diagnosed, and the suite therefore never exercised P1/P2 together. P6 itself is honest (I replayed it: 22 `rc=1` negatives, 1 `rc=0` pricing positive; `c2-controls-replay.txt`), but a green P6 does not mean a green C2.

### B2. E0 does not bind the report subject (BREAKS the claim's "subject-bound" wording)

Two executed forgeries, both with the correct 9-field Pricing block and correct S122/S123 evidence:

- **FA**: the round-85 `corpus/practice/curl-h1-1913733/report.md` body, whose prose still says `has_bounty? false` and "No captured record shows who paid it", with line 1 changed to name 1997312 and the record URL added.
- **FB**: the r43 exemplar body, which describes **CVE-2025-9086** (CWE-125, curl 8.13.0–8.15.0, `Bug bounty: 505 USD`), with line 1 changed to name 1997312/CVE-2023-28319, `3294999` replaced by `1913733`, and the Pricing block appended.

Observed (`c2-forgeries.txt`):

```
FA pricing-only: LIMB E0 pass heading=True url=True stray=none; E3 pass; E4 pass; rc=0
FA full:         E0 pass, E1 FAIL gate 7/8, E2 pass, E3 pass, E4 pass, E5 FAIL (path/log)
FB pricing-only: LIMB E0 pass heading=True url=True stray=none; E3 pass; E4 pass; rc=0
FB full:         E0 pass, E1 FAIL gate 7/8, E2 pass, E3 pass, E4 pass, E5 FAIL (path/log)
```

E0 tests: first line starts `# `, contains `1997312` and the CVE; the report contains the 1997312 URL; the set of `hackerone.com/reports/<N>` ids is a subset of {1997312, original-report}. Nothing binds the body to the subject. A relabeled package — including one about a different CVE — passes E0–E4. The claim's statement that "E0 binds the report subject" is false; C2's subject evidence must be an independent reviewer read (as the r85 spot-check did by hand), not E0.

### B3. Field provenance (each field is derivable, but three carry a join the counter does not check)

- **payer `internet-bug-bounty`** — derived from S122 `team.handle == "ibb"` + `has_bounty? true` + S123's general sentence "the awesome Internet Bug Bounty project, which has paid the bounties for us for many years". This is a sound inference (the IBB team's report carries a bounty; the maintainer says IBB funded curl's bounties), not a direct "IBB paid this report" sentence. The package must label it derived. `has_bounty?` is a **report-level** flag, not the "team configuration" reading the r85 report used; the r86 derivation is the better one.
- **reward-current-policy `ended 2026-01-31`** — S123:13 is **curl's** program ("There is no longer a curl bug-bounty program. It officially stops on January 31, 2026."), not the IBB program's end; IBB itself is not said to end. Read the field as "curl's reward policy for this CVE ended 2026-01-31", never "the payer ended". S121 is the post-change policy page ("There is no bug bounty…").
- **reward-at-disclosure `2400 USD`** — only S120 (curl advisory `Bug bounty: 2400 USD`); S122 leaves the amount null (SOURCES row S122 says so). The counter derives the amount from S120, not from the payer record; the join must be stated in the report. 
- **original-report `1913733`** — S122's structured `original_report_id` / `original_report_url` are **null**; the id is in the free-text `vulnerability_information` ("The original submission can be found here: …1913733"), corroborated by S120's `Original report:` line. Sound, but not a structured-field fact.
- **kev** — S052 catalogVersion 2026.10.23, captured 2026-10-26 (r35), not the package date; the r85 live feed (2026.11.06) also had 0 hits. Say "as of 2026.10.23".
- **E3's kev limb does not verify the suffix**: `price-kev: not-listed catalogVersion 1999.01.01 (invented)` passes E3 (executed, rc 0, `c2-forgeries.txt`). The catalogVersion is reviewer-checked, not counter-checked.

### B4. Coverage or duplicate? (capability extension, not new vulnerability coverage)

The r85 package is about report 1913733 (team curl, `has_bounty? false`, "no captured record shows who paid"); the r86 package is about report 1997312 (team ibb, `has_bounty? true`, original submission 1913733). Different report, team, flag and payer; same CVE and same underlying finding. The marginal coverage is the payer side + the capability (a subject-bound, payer-resolved counter), not a new vulnerability. Present it as a capability extension, not as new CVE coverage; the `status.json` of a landed package should still record the duplicate/retrospective blocker (the r85 package did).

### B5. C1 and C2 are causally separable (HOLDS)

The map has **no S122/S123 keys and no round-86 values** (`c1-excluded.txt`: map values spread over rounds 40, 45, 46, 47, 49, 57, 69, 70, 71). C1 touches only `corpus/knowledge/*.md`; C2 touches `corpus/practice/curl-ibb-h1-1997312/`, `corpus/SOURCES.md`, `LOG.md`, `SHONEN.md`. No file is shared and no predicate reads the other claim's artifact. A blocked C2 does not block C1; a landed C1 does not repair C2's E1.

### B6. Freeze-time false provenance in SHONEN (routed defect)

At the freeze commit, `SHONEN.md:8` (box 2 evidence) already says: "round 86: second package `corpus/practice/curl-ibb-h1-1997312/report.md` … logged in `LOG.md` Round 86." But:

- `corpus/practice/` contains only `curl-h1-1913733` — the named package does not exist;
- `grep -c "Round 86" LOG.md` = 0 — the named log section does not exist.

(`c2-freeze-state.txt`.) E5's `shonen` half is therefore pre-satisfied at freeze, and the only landing change it needs is LOG. If C2 is not landed, the pointer is false provenance and must be corrected (and `shonen-form.py` re-run — M85-1's gate). If C2 is landed, the LOG must make it true. Either way the L1 owns this; it is outside my edit scope.

### B7. What does hold at freeze

P3: `source-recheck.py` S122/S123 both `sha256 OK`, all 9 quotes anchored, rc 0 (`c2-recheck.txt`). P5: `sources-census.sh validate` → `kasegi ok …/corpus/SOURCES.md`, rc 0, six inherited W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085) (`c2-census.txt`). P4: registry rows 123 at freeze; S122/S123 rows are `queued`, used-by `—` (`c2-freeze-state.txt`). P6: 22 negatives rc 1, 1 positive rc 0 (`c2-controls-replay.txt`). The failure is P1/P2 only.

### B8. Post-freeze repair observed at 22:20:22 — the right fix, but it stales both claims' P2 pins

At 22:20:22 the worktree `corpus/source-snapshots/round-86/S122.txt` changed from the frozen sha `ceb01841…` to `08cab370…` (9131 → 5361 bytes; both presigned query strings removed), the round-86 manifest was rewritten (frozen `8d3b7d35…` → `2de425ba…`) with an S122 `redaction` block naming `.ufo/waves/round-86/l1/redact-presigned.py`, and the package appeared at `corpus/practice/curl-ibb-h1-1997312/`.

Observed at the worktree:

- gate `rules=8 pass=8 verdict=WELL-FORMED exit=0`; frozen e2e E0–E5 pass, `E2E-RESULT pass limbs=6 rc=0` (E2 `bound=S122,S123`); `source-recheck` S122 rc 0; census rc 0; `redaction-scan-r86.txt` `artifacts=4 bad=0 rc=0`.
- With the **frozen pre-redaction S122 bytes** substituted, the same package gives E1 FAIL and E2 FAIL (`l1-c2-postfreeze-r86.txt`; my FA/FB/FA-noev receipts agree).

The repair is real and is the right correction, but it is not admission evidence for the frozen C2 (the L1's own receipt says `Post-freeze, NOT admission evidence`), and it has a **collateral P2 failure for both claims**: the claims' shared `instruments` block still pins S122 `ceb01841…` and the manifest `8d3b7d35…`. At the tip, C1's P2 (and C2's P2) fail on those two pins even though C1's scope is untouched. The L1's `c1-landing-r86.txt` P2 passed at `fdb5f4af` **before** the redaction; quote P2 there, or refreeze the pins. C1's A9 correction (596/1720) and the S122 redaction are both post-freeze changes; together they mean the frozen claim set cannot be reported green at the tip. The L1's LOG already says "C2 killed as frozen" and records M86-1/2/3; this section supplies the P2 consequence it does not state.

The candidate under `w1/ExecC2Package-candidate/` still carries the **old** S122 bytes (`ceb01841…`); against the redacted snapshot it gives E2 `bound=S123` and gate R-NOSECRET fail (`c2-candidate-vs-redacted.txt`). Do not land that directory as-is; the integrated package under `corpus/practice/` has the redacted bytes.

---

## 3. Qualifiers the L1 must carry

**C1**
1. "Internal-citation repoint on a new scope"; axis score held at 4; no external RESOLVES; do not call it a score move.
2. **State the commit.** The frozen claim is true at `fdb5f4af` (596/1716 in a scratch clone) only. The tip `e73c1f9` reads 596/1720 in a clone and 597/1720 at the real lane path; the frozen 596/1716 target fails M1/M2/M3 there. Do not write "the lane measures 596/1716" without naming `fdb5f4af`.
3. **4 of the 203 keys are not citations** (`S020`, `S021`, `S023`, `S025`: quoted round-40 manifest `path` values on `- Pin:` lines; A9). The honest count is 199 citations + 4 quoted data values; the L1 correction is right; refile with 199 keys and a 596/1720 target, or present the frozen claim as landing-commit-only and superseded.
4. At `fdb5f4af`: 376 backticked occurrences on 292 lines; 5 map values were already cited, so the denominator is 1716 and the gain is 198 distinct internal resolutions, not 203. The corrected tip changes 288 lines.
5. The 89 exclusions: 79 are byte-identical duplicates (S102 70, S041 6, S029 1, S040 1, S100 1) forced by M4's exact-uniqueness rule; only S069's 10 are genuinely ambiguous (3 distinct bytes). 34.73% is a floor.
6. 75 unbackticked occurrences of map keys remain and are meter-invisible.
7. M5 is range-only; anchors sampled correct, but "anchors verified" is not claimed.
8. P2 is load-bearing: a landing that edits `corpus/instruments/resolve.py` could satisfy P1 alone. Run P2.
9. The census of record is not regenerated (r85 routed defect 4); `census-freshness-check.py` was already failing and remains failing.
10. **P2 is stale at the tip.** The claims' shared `instruments` block pins S122 `ceb01841…` and the round-86 manifest `8d3b7d35…`; the post-freeze redaction (S122 `08cab370…`, manifest `2de425ba…`) makes C1's P2 (and C2's) fail at the tip even though C1's scope is untouched. Quote C1 P2 at `fdb5f4af` (where the L1 receipt shows all 10 OK) or refreeze the pins.

**C2**
1. **Do not land C2 under the frozen predicates.** E1 and E2 are mutually exclusive on S122 (presigned S3 `X-Amz-Security-Token` vs R-NOSECRET). The L1 has already killed it as frozen; keep that verdict. Do not edit a frozen limb, map, field, control or subject.
2. The L1's post-freeze repair is the right path: S122 is now `08cab370…` (both presigned query strings removed), the manifest `2de425ba…` records the redaction, and the integrated `corpus/practice/curl-ibb-h1-1997312/` package passes E0–E5 and the gate 8/8 at the worktree. It is post-freeze repair, not admission evidence; a refreeze with the new pins is required.
3. Amend E0 to bind the body (derived CVE/severity/title must occur in the body; no other CVE id; a second reviewer read), and add a "relabeled heading" control — the current b3 controls only test "heading left at 1913733". My FA/FB prove a relabeled body passes E0–E4.
4. Field wording: payer is derived (S122 team + flag + S123 general statement); the 2400 USD is joined from S120 (S122 amount null); original-report is from free text (structured field null); reward-current-policy is curl's program end, not IBB's; kev is as of catalogVersion 2026.10.23 and E3 does not verify the suffix.
5. SHONEN.md:8 was false provenance at freeze (package absent, no "LOG.md Round 86"); at the tip the package and LOG Round 86 exist, so it is now true — verify `shonen-form.py` at the landing.
6. Do not land `w1/ExecC2Package-candidate/` as-is: it carries the **old** S122 bytes (`ceb01841…`) and fails E2 `bound=S123` and R-NOSECRET against the redacted snapshot (`c2-candidate-vs-redacted.txt`). Use the integrated `corpus/practice/` package.

---

## 4. Smallest safe corrections

- **C1**: report it as **verified at `fdb5f4af` (596/1716) and superseded at `e73c1f9` (596/1720)**, with the 4 non-citation keys named (A9). Refile/refreeze with 199 keys and the 596/1720 target if the round wants a claim true at the tip; otherwise state the landing-commit scope explicitly and do not quote 596/1716 for the tip.
- **C2**: keep the "killed as frozen" verdict; the L1's redaction is the right repair. Refreeze with S122 `08cab370…` and manifest `2de425ba…`, land the rebuilt package, and add (a) a full-package positive control that binds S122 and (b) a relabeled-heading E0 control. Do not land the w1 candidate.
- **P2 / tip**: any final receipt that runs P2 at the tip fails on S122 and the manifest; either quote P2 at `fdb5f4af` or refreeze the shared pins.
- **SHONEN**: now true at the tip; run `corpus/instruments/shonen-form.py` (R136) after any SHONEN edit.

---

## 5. Receipts (all under `.ufo/waves/round-86/w1/CriticClaims-receipts/`)

| File | Contents |
|---|---|
| `c1-pins.txt` | all 10 frozen instrument sha256 values match `claims.json` at freeze |
| `c1-map-rebuild.txt` | independent `build-map.py` at base: 203/89, map and excluded byte-identical |
| `c1-meter.txt` | positive 596/1716 rc 0; do-nothing 398/1721 rc 1; real-lane base 399/1721 |
| `c1-controls-replay.txt`, `c1-controls-diff.txt` | frozen C1 controls replayed; receipt reproduces (diff rc 0) |
| `c1-excluded.txt` | 89 exclusions by basename; 79 byte-identical (1 distinct sha), S069 3 distinct; 376 occurrences/292 lines; 197 anchors/0 blank; 75 unbackticked residue |
| `c1-ground-base.txt`, `c1-ground-after.txt`, `c1-ground-diff.txt` | r49 citation-ground gate identical at base and after (rc 1, 8 pre-existing findings) |
| `c1-worktree-drift.txt` | worktree knowledge files == map-applied base, 0 mismatches / 98 files |
| `c1-anchor-samples.txt` | six citing-line vs anchored-target comparisons |
| `c2-forgeries.txt` | FA/FB pricing-only and full runs; body mismatch lines; kev-suffix forgery rc 0 |
| `c2-mutual-exclusion.txt` | gate 7/8 on FA/FB (R-NOSECRET); gate 8/8 on FA-noev; E2 pass/fail pair |
| `c2-s122-credential.txt` | masked `X-Amz-Security-Token` context, counts, date/expiry; S120/S121/S123 clean |
| `c2-recheck.txt` | `source-recheck.py` S122/S123 rc 0 |
| `c2-census.txt` | `sources-census.sh validate` rc 0 |
| `c2-freeze-state.txt` | package absent; SHONEN pointer; LOG has no Round 86; registry 123; S122/S123 queued |
| `c2-controls-replay.txt` | 22 negatives rc 1, 1 pricing positive rc 0 |
| `c1-tip-vs-landing.txt` | frozen meter at the corrected tip `e73c1f9`: 597/1720 lane, M1/M2/M3 FAIL; L1 landing 596/1716; L1 correction 596/1720 |
| `l1-c1-landing-r86.txt`, `l1-c1-correction-r86.txt` | L1 receipts copied: P1–P4 at `fdb5f4af` (P2 all 10 OK); correction to 596/1720 |
| `l1-c2-postfreeze-r86.txt` | L1 receipt: worktree package E0–E5 pass; frozen pre-redaction S122 → E1/E2 FAIL |
| `l1-redaction-scan-r86.txt`, `l1-redact-presigned-r86.txt` | L1 redaction scan (4 artifacts, 0 hits) and redaction tool/log |
| `c2-candidate-vs-redacted.txt` | w1 candidate (old S122 bytes) vs redacted snapshot: E2 `bound=S123`, R-NOSECRET fail |

Files written: this report and the receipts above. Scratch `/fast/scratch/hyaku/kasegi-r86/CriticClaims/` deleted before yield.
