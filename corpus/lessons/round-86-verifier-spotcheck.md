# Round 86 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Closure of lane-round kasegi r86. Report `.ufo/reports/round-86/kasegi.md` (fleet repo); dispatched
prompt `.ufo/prompts/kasegi-round-86.md`. Lane base `d7296645c2cd9f631329fa8e2f38328a4c9c89a5`,
freeze `252df0c90c066d83d229e3107811a6bc05e8feed`, tip `0299cb279cb56431e839557b7ce26cafa3be449e`.
Driver digest (copied from the mutable `.ufo/watchdog.log`):

    2026-11-06T21:55:50-03:00 launch kasegi round=86 pgid=2228949 driver=hyaku-inline attempt=1
    2026-11-06T22:39:03-03:00 complete kasegi round=86; hyaku-inline attempt=1

Measurements below were run by this reviewer on 2026-11-07 (~01:40Z) over committed bytes
(`git show <rev>:<path>`), never over a working tree. No lane gate was executed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-86/kasegi.md` | `kasegi-shokunin fc8671e45229addca299093534aac11a8fd29a82` | pass |
| Prompt committed | same over `.ufo/prompts/kasegi-round-86.md` | `kasegi-shokunin 05e2e48ba68847321c22f4606041c103e7a8ffc5` | pass |
| `SHONEN` heading, one line per box | report §SHONEN vs `SHONEN.md` (4 boxes) | 4 lines, all `[~]` + pointer | pass |
| Cited commits exist and are ancestors of `master` | `git cat-file -e` + `git merge-base --is-ancestor <h> master` for 252df0c9, fdb5f4af, e73c1f94, b079a106, fd45c41e, 1a6ea622, 0299cb27 | 7/7 OK, all authored `kasegi-shokunin` | pass |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …` ; `git status --porcelain` ; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = `0299cb27…` | pass |
| Prompt carries the template contract | section scan of the prompt | §1 MISSION/AXES binding, §2 claims 1–3 + lowest axis, §2b frontier step, §3 L2 floor, §4 report contract (path, SHONEN, hash rule), §5 commit/push scope/L0 | pass |
| Marker vs report | report content | real report, 7 cited commits, evidence pointers | status `ok` |

Mission ran 43 min (launch → complete); no stale-lane question.

## 2. Claims — re-check

### C1 — depth:verifiability (knowledge-scope meter 398/1721 → 596/1716 at landing)

Re-measured independently (own script; counts tokens `corpus/source-snapshots/round-N/S###.txt[:a[-b]]`
vs bare `S###.txt[:a[-b]]` in `corpus/knowledge/*.md`, and resolves each full path against the same
revision's tree with the anchor inside the file's line count):

| Rev | full-path occ / distinct / distinct resolving | bare occ / distinct |
|---|---|---|
| base `d7296645` | 210 / 80 / 80 | 1881 / 931 |
| freeze `252df0c9` | 210 / 80 / 80 | 1881 / 931 |
| landing `fdb5f4af` | 586 / 277 / 277 | 1505 / 761 |
| tip `0299cb27` | 582 / 277 / 277 | 1509 / 765 |

- Pure repoint: 376 occurrences moved bare → full at landing, total conserved (2091 = 210+1881 = 586+1505);
  every full-path token resolves with its anchor in range at landing and at tip (0 bad).
- Distinct resolving full-path citations 80 → 277 (+197). The lane meter (resolve.py classification)
  reads +198 at landing; my token model is not resolve.py's, so this corroborates rather than
  reproduces the exact `596/1716`.
- Map: `sha256sum .ufo/waves/round-86/c1/repair-map.json` = `dd40455a…bce12` (= frozen); 203 keys.
  Exact-token check: 203/203 keys bare at base; 33 still appear bare at landing (37 at tip, +4 reverted)
  — all prose/command mentions resolve.py does not count as citations (e.g.
  `corpus/knowledge/github-repository-security-advisories.md:11,89`, `S076.txt:559` in prose beside the
  repointed backtick form). Not a predicate failure; see routed defect 5.
- P2: frozen instrument sha256 at landing 10/10 match; at tip 8/10 (`S122.txt`, `round-86/manifest.json`
  changed by the post-freeze redaction) — matches the report's qualifier (c).
- P3: `git diff --name-only 252df0c9 fdb5f4af | grep -vc '^corpus/knowledge/'` → 0; 14 files +292 −292.
- Revert `e73c1f94`: 4 files, 4 lines (`cisa-bod-20-01-vdp-minimums.md`, `cisa-cvd-program-stages.md`,
  `cve-bench-agent-exploitation-benchmark.md`, `doj-vdp-framework-scope-and-authorization.md`).
- Evidence-verified (committed receipts, not re-run): `.ufo/waves/round-86/l1/c1-landing-r86.txt`
  (`KNOWLEDGE-METER base=398/1721 after=596/1716 target=596/1716 keys=203`, M1–M6 pass, rc 0, P4 density
  273.2) and `.ufo/waves/round-86/l1/c1-correction-r86.txt` (tip 596/1720).

Ruling: **verified on its frozen predicates at the landing commit**, re-measured. Qualifier stands:
4/203 keys were quoted manifest fields, so the tip reads 596/1720, not the frozen 596/1716; the move is
an internal-citation repoint (score held at 4).

### C2 — coverage (second priced package, subject-bound counter)

- Lane's own verdict: NOT VERIFIED, killed as frozen (E1 R-NOSECRET refuses the captured S122 bytes; E2
  requires them). Evidence-verified: `.ufo/waves/round-86/l1/c2-postfreeze-r86.txt` shows on the frozen
  bytes `LIMB E1 FAIL gate_rc=1`, `LIMB E2 FAIL bound=S123`, `E2E-RESULT fail limbs=6 rc=1`; on the
  redacted bytes `E2E-RESULT pass limbs=6 rc=0` (post-freeze, not admission).
- Re-measured: credential shape `X-Amz-Security-Token=<≥20 chars>` via `git grep -l` → 2 files at freeze
  `252df0c9`, 0 files at tip `0299cb27`.
- Controls receipts present (`controls/c1-controls-r86.txt`, `controls/c2-controls-r86.txt`).

Ruling: **not verified** (kill rule fired; honest stop). The package itself is real post-freeze work.

### Harm check

`git diff d7296645 0299cb27 -- SCORECARD.md` appends only the Round 86 section; no axis row lowered.
depth:density 273.2 → 273.2 (evidence-verified, `c1-landing-r86.txt` P4). The 4 misquoting repoints
were reverted before the tip, so no knowledge entry is left false. The credential push is a
conformance/safety incident (§7), not an axis measurement.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | C1 re-measured (80 → 277 distinct resolving full-path citations; receipts 398/1721 → 596/1716 at landing) |
| coverage | unchanged | C2 not verified; score held 8; package is post-freeze evidence only |
| depth:density | unchanged | 273.2 → 273.2 (evidence-verified) |

## 4. Discernment spot-check (`corpus/lessons/round-86.md` § Gate)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S123 end-of-bounty post | admit | https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/ (HTTP 200) + capture `S123.txt:13,16,27` | agree | live page contains "has paid the bounties for us for many years" and "officially stops on January 31, 2026"; capture lines match; maintainer's own statement about his own program is tier A |
| S122 IBB record 1997312 | admit | https://hackerone.com/reports/1997312.json (HTTP 200) | agree | live JSON: `team.handle=ibb`, `has_bounty?=true`, body links 1913733, title CVE-2023-28319; the record has no amount field, as the revised scope says. Capture hygiene was the failure (M86-2), not the admission |
| IBB 80/20 split | reject (anachronistic for the 2023 award) | arquivo.pt `id_` captures of https://www.hackerone.com/internet-bug-bounty | agree | "providing 80% to the finder and 20% to the open-source project" count: 2023-02-04 0, 2023-08-02 0, 2024-01-25 0, 2024-07-27 1, 2024-08-13 1. Wayback unreachable from this host (timeouts), so arquivo.pt only. Wording nit: the lesson dates the award "2023-05-17 disclosure"; S122 records the IBB report submitted 2023-05-23, disclosed 2023-06-25 (05-17 is curl's advisory date) — the ruling holds under either date |

SOURCES row re-opened: **S123** (`corpus/SOURCES.md:135`). Anchor "snapshot lines 13, 15-16 and 27"
resolves; Gate quote "the awesome Internet Bug Bounty project, which has paid the bounties for us for
many years" is 16 words (≤25) at `S123.txt:16` and on the live page.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`,
rc 0, the same 6 inherited W04 warnings (S028, S029, S072, S076, S080, S085). Registry rows
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`: 121 at base, 123 at tip.

## 5. Trend verdicts

- **expansion: unprovable-but-better** (lane said `improved`). Two tier-A rows mined (121 → 123) and a
  payer-resolved second package exists, but CORPUS rule 4 counts admitted `knowledge/` entries citing
  mined rows, and this round admitted none (knowledge diff is the repoint only); C2 is not credited.
- **quality: unprovable-but-better** (agrees with lane). The countable move is a citation-form repoint
  (re-measured, all resolving), not an entry re-verified or superseded; the 4 misquotes were caught and
  reverted; no entry left false.
- **discernment: improved**. The spot-check agrees with the gate on two admits and one reject; R137 is
  grounded in lesson M86-1 and shown able to fail (`l1/r137-check-r86.txt`).

## 6. Routed defects (lane fixes next round)

1. **Capture secret hygiene.** M86-2's fix (scan every capture with the gate's `SECRET_PATTERNS`
   before its first commit) is stated, not yet a committed check with a self-test; land it as a
   pre-commit/pre-freeze step with a failing fixture, and run it over existing `source-snapshots/` and
   `.ufo/` receipts.
2. **SOURCES append-only.** S122's `scope` cell was edited in place (b079a106) after the row was pushed
   queued in the freeze; CORPUS rule 2 allows only `status`, `recheck`, `used-by` in place. Record the
   correction per rule 2 (new row or named correction), or state why a same-round row is exempt.
3. **Reject-reason date.** Correct "2023-05-17 disclosure" for the IBB award to the S122 dates
   (submitted 2023-05-23, disclosed 2023-06-25) in the next lesson; ruling unchanged.
4. **Frozen pins at tip.** C1 P2 fails at tip for `S122.txt` and `round-86/manifest.json`; the r87
   re-freeze must pin the redacted bytes and exclude quoted manifest fields from any repoint map.
5. **Mixed citation forms.** 33 map keys still appear bare in prose next to their repointed form
   (e.g. `github-repository-security-advisories.md:11,89`); either repoint or state the prose rule.
6. **Carried from r85:** E0 binds labels, not body (CriticClaims B2; MutC2Counter 15/39 killed); census
   of record stale (`citation-survival.md` 132/701). `w1-results.json` holds no outputs (kernel restart).

## 7. Operator notes

- **Credential exposure.** The freeze `252df0c9` (and the r85 receipt) carry a HackerOne-issued AWS STS
  presigned profile-picture token (`X-Amz-Date` 2026-11-07T00:58:29Z, 3600 s → expiry 01:58:29Z) in a
  **public** repo (`gh repo view VeigaPunk/kasegi-shokunin` → PUBLIC); it was still unexpired at this
  closure (~01:41Z). Tip redacted; history untouched; the lane filed the L0 question. Rewrite/report
  decision is the operator's.
- SHONEN: all four boxes `[~]`; box 2 now cites two packages. Boxes 1–3 point at the r47 non-author
  spot-check and look checkable by a non-author; promotion is operator-owned.
