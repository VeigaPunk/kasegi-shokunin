# Sibling-Overlap Scan and Connector Scope Report (Round 71)

## 1. C1 Gate Overlap and Per-Script Census Scan

### 1.1 Fleet and Lane Search for Read-Only Admission Patterns
Measured command:
```bash
grep -rn 'derive-not-read-only\|READ_ONLY_HEADS\|segment_ok' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/instruments 2>/dev/null
```
Observed output:
```
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py:24: "return head.startswith(READ_ONLY_HEADS)", "return True"),
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py:36: "return head.startswith(READ_ONLY_HEADS)",
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py:37: "return head.startswith(READ_ONLY_HEADS)  "),
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py:40:GATE_ANCHORS = ("return head.startswith(READ_ONLY_HEADS)",
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py:41:                "return parts[0] in READ_ONLY_HEADS")
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:90:READ_ONLY_HEADS = (
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:297:        if head_name in READ_ONLY_HEADS:
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:508:def segment_ok(root, parts):
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:517:    return parts[0] in READ_ONLY_HEADS
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:540:            if not argv or not segment_ok(root, argv):
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:548:    if not argv or not segment_ok(root, argv):
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:580:            eprint("FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=%s" % ent["id"])
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:706:    run_case("derive-not-read-only-refused", 2, SELFTEST_LEDGER_NOT_RO)
```

### 1.2 Fleet-Wide Search for Per-Script Census Logic
Measured command:
```bash
grep -rn -I --exclude='*.pyc' -E '(derive-not-read-only|READ_ONLY_HEADS|PY_SCRIPT_CENSUS|PY_DENIED_ANY|PY_HEAD_REFUSED)' /home/vgpnk/Projects/shokunin/*-shokunin/ 2>/dev/null | grep -v 'kasegi-shokunin'
```
Observed output:
```
(exit 1 - zero matches outside kasegi-shokunin)
```

Measured command:
```bash
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do if [ -d "$d/corpus/instruments" ]; then echo "$d has corpus/instruments"; fi; done
```
Observed output:
```
/home/vgpnk/Projects/shokunin/kasegi-shokunin has corpus/instruments
```

### 1.3 Pattern Finding
`kasegi-shokunin` is **ALONE**. None of the 20 sibling lanes (`audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kaidoku`, `kake`, `kama`, `kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi`) have a `corpus/instruments/` directory. Across the entire fleet, the per-script Python allowlist census (`PY_SCRIPT_CENSUS`, `PY_DENIED_ANY`, `PY_DENIED_BY_SCRIPT`, `PY_HEAD_REFUSED`) exists solely in `kasegi-shokunin/corpus/instruments/figure-audit.py` (lines 143-207, 490-504) and its selftest limb `python-census-covers-instruments` (lines 915-922). There is no sibling lane instrument implementing this pattern to cross-link.

---

## 2. Six-Party Disclosure and Coordination Comparison Table

| Party & Source | Coordination Window & Clock Trigger | Escalation Rule | Who Publishes | Vendor Refusal Lead to Publication? |
|---|---|---|---|---|
| **CISA** (`S003`) | Flexible / negotiated default starting point (`S003.txt:202-203`); 2–3 business days acknowledgment (`:231-232`); no universal deadline. | Collaborative adjustment of embargo periods (`:204`); third-party coordinators (CISA, CSIRTs) engaged when coordination stalls (`:210-212`). | Product supplier/vendor in collaboration with researcher and coordinators (`:209-212`). | **Guidance only**: S003 is supplier guidance, not an enforcement publisher; warns that uncoordinated leaks or independent researcher disclosure occur if suppliers stall (`:207-208`). |
| **CERT/CC Policy** (`S004`) | **45 days** from initial report (`S004.txt:24-25`), regardless of patch/workaround availability. | Earlier disclosure for active exploitation or serious threats; later for standards/core OS changes (`:26-29, 67-69`). | CERT/CC publishes public Vulnerability Notes with reporter credit (`:29-30, 45`). | **YES**: Published regardless of patch availability (`:25-26`). Vendor disagreements/statements posted alongside, but disclosure is not withheld because vendor disagrees (`:75-79`). |
| **Google Project Zero** (`S005`) | **90 days** from initial report; **30 days** post-fix if fixed early (90+30 rule, `S005.txt:18, 20`); 7 days for active exploitation (`:44`). | 14-day grace extension granted ONLY if vendor commits to ship within grace period (max 120 days total, `:21-23`); notice filed within 1 week (`:19`). | Project Zero derestricts bug in public issue tracker (`:25-26`). | **YES**: Automatically derestricted at deadline expiry (`:18`). Tagged `Deadline-Exceeded` (95 historical bugs disclosed unpatched, `:27, 29-30`). |
| **Japan IPA / JPCERT/CC** (`S041`, `S042`) | **起算日** (date JPCERT/CC first attempted contact, `S041.txt:340`, `S042.txt:145`) + **45-day 目安** (guide, not hard deadline) for software (`S041.txt:648`). Web path has no clock apparatus (`S042.txt:162-182`). | Unreachable developer listed on public registry (`S042.txt:142`); 4 adjustment factors (`S041.txt:649-653`); 1-year withdrawal of non-disclosure request (`S041.txt:305-306, 430-431`). | IPA & JPCERT/CC jointly publish on JVN (Japan Vulnerability Notes) portal (`S041.txt:1281`, `S042.txt:159`). | **CONDITIONAL / NO**: Unreachable developer listed publicly (`S042.txt:142`), but JPCERT/CC can call off publication on 5 grounds (`S041.txt:662-671`) or close handling upon contact (`S042.txt:143`). Non-disclosure request removable after 1 year (`S041.txt:305`). |
| **CERT Guide CVD Phases** (`S095`) | Conceptual 6-phase lifecycle: Submission, Validation, Prioritization, Remediation, Disclosure/Awareness, Deployment (`S095.txt:56-74`). No fixed numerical days. | Role-gated matrix: Analyst/Vendor/Coordinator validate and prioritize response (`:129-140`); Vendor develops patch/workaround; Coordinator handles multiparty (`:141-146`). | Vendor and/or Coordinator publish advisory in Awareness phase (`:69`); Deployer applies fix (`:153-158`). | **Conceptual / Deferred**: Role table separates Reporter fix confirmation (Remediation) from Vendor/Coordinator report validation; binary publication rules deferred to operational policies (`S004`). |
| **TrendAI ZDI** (`S106`, `S075`) | **120-day standard window** from private sharing/first contact (`S106.txt:70`, `S075.txt:24`); shortened to **30, 60, or 90 days** for faulty/incomplete patches (`S106.txt:70`, `S075.txt:25`). | 15-business-day non-response escalates to limited advisory (`S106.txt:70`, `S075.txt:23`); rare extensions at ZDI sole discretion (`S075.txt:24`). | TrendAI ZDI publishes on advisory portal: "full advisory" (with patch link/credit) or "limited advisory" (withholding exploit info) (`S106.txt:51-52, 71-72`). | **YES**: Guaranteed not to remain undisclosed due to vendor inaction (`S106.txt:62`, `S075.txt:26`: never "kept quiet" because vendor refuses). Publishes full or limited advisory upon vendor refusal (`S106.txt:72`). |

---

## 3. Overlap Scan and Scope Determination

### 3.1 Frontier Row Overlap List
In Round 47, an attempt to admit ZDI's disclosure timeline as an independent frontier row (F30) was rejected:
`corpus/README.md:702`:
> "No F30 row is admitted: the proposed ZDI timeline frontier duplicates F02's existing coordinator/trigger/interval discipline. The opened policy is useful enrichment, not a new frontier count."

The specific overlaps between F49's declared timeline numbers and the existing `F02` coordinator case (`corpus/knowledge/zdi-disclosure-policy.md` on S075) are:
1. **Row `F02`** (`zdi-disclosure-policy.md:17`):
   - Overlapping text: `“four months (120 days) to address the vulnerability” (S075.txt:24)`
   - Duplicated by F49 declared claim: `a 120-day standard coordination window` (`S106.txt:70`).
2. **Row `F02`** (`zdi-disclosure-policy.md:24`):
   - Overlapping text: `The 15-business-day branch is permissive, not an automatic publication promise (S075.txt:23).`
   - Duplicated by F49 declared claim: `escalation after 15 business days of vendor silence` (`S106.txt:70`).
3. **Row `F02`** (`zdi-disclosure-policy.md:20-22`):
   - Overlapping text: `For critical-rated bugs where active exploitation is detected or imminent, the vendor will have 30 days... 60 days... 90 days (S075.txt:25)`
   - Duplicated by F49 declared claim: `a shortened window for incomplete or problematic patches (30, 60, or 90 days)` (`S106.txt:70`).
4. **Row `F02`** (`zdi-disclosure-policy.md:24, 42`):
   - Overlapping text: `In no cases will an acquired vulnerability be "kept quiet" because a product vendor does not wish to address it. (S075.txt:26)`
   - Duplicated by F49 declared claim: `guarantees that your work will not disappear into a backlog or remain undisclosed due to vendor inaction` (`S106.txt:62`) and `the full-versus-limited advisory choice` (`S106.txt:51-52, 72`).

### 3.2 Scope Determination: `SCOPE CLEAR`
`SCOPE CLEAR` holds for Frontier F49 if and only if the entry strictly defines its primary ground on the **Commercial Vulnerability Acquisition and Brokered CVD Flow**, not the coordination clock numbers. Specifically, F49's distinct, non-overlapping ground comprises:
1. The financial acquisition lifecycle: `validate -> formal monetary offer -> payment -> private vendor coordination -> credit or anonymity` (`S106.txt:49, 60, 61`), which is unheld by F02 (coordinator timelines), F13 (platform severity ladders), and F15 (vendor intake for third-party bugs).
2. The commercial bug bounty broker intake model (`S106.txt:31`).
3. Complete technical dossier provision to vendors including proof-of-concept and reproducibility steps (`S106.txt:69`).
4. The structural distinction between a **Full Advisory** (published post-patch with patch links and credit) and a **Limited Advisory** (published upon vendor inaction/refusal while withholding sensitive exploit information to protect users) (`S106.txt:51-52, 71-72`).

---

## 4. UFO-FSD Connector Move: Live Figure Derivation in Figure Audit

### 4.1 Evidence
1. **Gate capability expansion (C1)**: `corpus/instruments/figure-audit.py` introduces `PY_SCRIPT_CENSUS` to allow Python counters (`capture-binding-check.py`, `r44-frontier-count.py`, `claim-package-check.py`) as read-only derive commands (positive probes R1–R8 in `c1-probe-run-r71.py`).
2. **Historical isolation**: `corpus/instruments/figure-audit-ledger.json` contains 35 figure entries, all pinned to commit `32782bd` (Round 53). None derive against the live working tree.
3. **Uncovered live figures (C2)**: In Round 71, C2 asserts structural targets (`records=85 bound=85`, `frontier rows=49 admitted=49`, `registry=106`, `knowledge_files=87`). These figures are validated only by ad-hoc shell commands in `claims.json:67`, re-exposing the repository to the exact silent number-drift defect class (D53-1/D53-2) that originally created `figure-audit.py`.

### 4.2 Affected Axes
- `depth:verifiability` (C1)
- `coverage` (C2)

### 4.3 Proposed Move
Bind the live corpus invariants directly into `figure-audit-ledger.json` (or a dedicated current-round ledger) using the newly admitted C1 Python counter heads:
1. Re-derive live frontier rows using `python3 corpus/instruments/r44-frontier-count.py --root .` (`want: "frontier rows=49 admitted=49"`).
2. Re-derive live capture bindings using `python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=85` (`want: "1"`).
3. Re-derive live registry row count using `git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` (`want: "106"`).

### 4.4 Risks
If a future wave adds a frontier row or source snapshot without updating the ledger in the same commit, `figure-audit.py` will exit 1 (`stale`).
*Mitigation*: This is the intended behavior of a fail-closed verifiability gate. It prevents undocumented corpus growth and ensures all figure claims remain continuously synchronized.

### 4.5 Verification
Run `figure-audit.py` against the updated ledger:
```bash
python3 corpus/instruments/figure-audit.py --ledger corpus/instruments/figure-audit-ledger.json --root .
```
Confirm:
1. `FIGURE-AUDIT figures=38 ok=38 stale=0 exit=0` on committed tree.
2. Introducing a synthetic discrepancy (e.g. mutating `want: 50`) immediately produces `stale=1 exit=1`.
