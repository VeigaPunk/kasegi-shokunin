# R44Exec5 — SKILL registry location and basename entries for `claim-package-check` / `r43-closure`

Seat: R44Exec5 (leaf executor, read-only). Round 44, lane `kasegi-shokunin`.
Assigned item: *"Locate exact SKILL registry location and basename entries for claim-package-check and r43-closure; report."*
Scope: research only. No lane file was edited, no git/jj mutation, no gate or selftest executed.
Revisions: base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`, claims-freeze `66314015122b9aa32dc40f2f1815df56624c26d1`, round-43 freeze commit `4cb6d4a`. Report path relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

**Bottom line.** The instrument registry is `SKILL.md` § `## Gates & probes registry` (line **977**, table header line **979**, basename in the **first cell**) plus nine append-only per-round blocks, all of whose headings contain the literal `Gates & probes registry`. At every **committed** revision (base = freeze = HEAD, SKILL.md blob `073a7b61…`, sha256 `9eef84d1…`, 1134 lines) both basenames have **0** exact-name registry rows. During this measurement another seat appended an uncommitted `## Round-44 registry correction — round-43 instrument basenames` block (working-tree SKILL.md:1136) that carries both rows at **1142** (`claim-package-check.py`) and **1143** (`r43-closure.sh`), but its heading omits the literal `Gates & probes registry` — so the documented round-36 E3 / QUALITY R29 counter still prints **0/0** on the post-append tree.

---

## 1. Exact registry location

| item | value | evidence |
|---|---|---|
| registry section | `SKILL.md:977` `## Gates & probes registry` | `grep -n '^## .*[Rr]egistry' SKILL.md` |
| table schema | `SKILL.md:979` `\| name \| type \| entry command \| verdict map \| self-test \| pinned-value path \| write scope \| owner \|`; separator `:980` | `sed -n '977,980p' SKILL.md` |
| basename position | **first cell of the row** (`\| <basename> \|`) | every row, e.g. `SKILL.md:1134` `\| r42-closure.sh \| gate \| …` |
| append-only per-round blocks (headings all contain `Gates & probes registry`) | `1037` R29, `1050` R30, `1060` R31, `1073` R33, `1094` R35, `1107` R36, `1118` R40, `1124` R41, `1130` R42 | `python3 …/registry-locate.py` (below), `registry_section` lines |
| normative rule | "An instrument is registered at the `SKILL.md` § Gates & probes registry **under its exact basename** — one row whose name cell is exactly the file name … not under a name of which it is a substring … a registry count reached by a substring literal is a false green" | `corpus/QUALITY.md:264` (rule R29) |
| canonical measurement pattern | "rows in `## …Gates & probes registry…` sections whose first cell is the exact basename" | `corpus/lessons/round-36-verifier-spotcheck.md:55` (check E3) |
| instrument CLIs the rows must describe | `r43-closure.sh:4-7` (`--export-ref <hash>`, `--selftest --export-ref <hash>`, `--leaf`); `claim-package-check.py:10-13` (`<package-dir>`, `<package-dir> --json`, `--selftest`) | `sed -n '1,12p' corpus/instruments/r43-closure.sh`; `sed -n '8,34p' corpus/instruments/claim-package-check.py` |
| file modes | `100755 97038e41… 0 corpus/instruments/r43-closure.sh`; `100755 31a6259f… 0 corpus/instruments/claim-package-check.py` | `git ls-files -s <both>` |

### Homonyms — which "registry" is *not* the instrument registry

| file | what it actually registers | basename hits for the two instruments |
|---|---|---|
| `SKILL.md:715` `## Submitted-state registry — the do-not-refile set` | submission do-not-refile set | n/a |
| `corpus/SOURCES.md` | source registry rows `S###` (68 at base) | 0 / 0 |
| `corpus/README.md` | frontier table `F##` + per-round notes; the round-43 note (heading `:602`) mentions `instruments/claim-package-check.py` at `:608` as **prose** | `claim-package-check` 1 (`:608`), `r43-closure` 0 |
| `corpus/instruments/README.md` | descriptive per-round instrument documentation (sections at `136,149,206,337,530,675,800,891`; 977 lines), **not** a registry | 0 / 0 |
| `corpus/QUALITY.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md` | lesson/score/report records | 1/2, 3/4, 3/2, 2/4 respectively |

Defect 7's own ground text reproduces exactly: `corpus/lessons/round-43-verifier-spotcheck.md:30` — "the report's SHONEN bullet says the two new instruments are registered in `corpus/instruments/README.md`; `git grep` there → 0 hits (the gate is registered in `corpus/README.md`'s round-43 note; `r43-closure.sh` in neither)."

---

## 2. Basename entries — committed state (base `ab98fac9`, freeze `4cb6d4a`, HEAD `6631401`)

All three revisions carry the identical SKILL.md blob, so one measurement covers them:

```
ab98fac9 blob=073a7b61f0b0c63d86fe7d58dedc7e40af3f9e14 sha256=9eef84d163173c8e840732458d70b5c14050289cbf0c4f0d2414780a74f92b57 lines=1134
4cb6d4a  blob=073a7b61f0b0c63d86fe7d58dedc7e40af3f9e14 sha256=9eef84d163173c8e840732458d70b5c14050289cbf0c4f0d2414780a74f92b57 lines=1134
6631401  blob=073a7b61f0b0c63d86fe7d58dedc7e40af3f9e14 sha256=9eef84d163173c8e840732458d70b5c14050289cbf0c4f0d2414780a74f92b57 lines=1134
```

Exact-basename registry rows (QUALITY R29 / round-36 E3 predicate), committed bytes:

| basename | exact rows | lines | positive controls in the same counter |
|---|---|---|---|
| `r43-closure.sh` | **0** | — | `r42-closure.sh` 1 @1134; `r41-closure.sh` 1 @1128; `r40-closure.sh` 1 @1122; `r39-closure.sh` 1 @1116; `r38-closure.sh` 1 @1115; `r37-closure.sh` 1 @1113; `r36-closure.sh` 2 @1112,1114; `r35-defect-closure.sh` 1 @1111 |
| `claim-package-check.py` | **0** | — | same counter; 39 registry rows, 19 distinct name cells |

Substring-literal control (the R29 false-green generator), same file:

```
grep -cF 'closure.sh'            SKILL.md -> 12
grep -cF 'r43-closure.sh'        SKILL.md -> 0
grep -cF 'r43-closure'           SKILL.md -> 0
grep -cF 'claim-package-check.py' SKILL.md -> 0
grep -cF 'claim-package-check'   SKILL.md -> 0
grep -cF 'claim-package'         SKILL.md -> 5     (all origin-work `claim-packages/` paths: :206, :695, :711, :730, :1013 — no row)
```

So a `grep -c claim-package` "registration" prints 5 while the exact-basename row count is 0: precisely the false green R29 forbids. `SHONEN.md:286`'s own figure (`grep -c 'r43-closure\|claim-package-check' SKILL.md` = 0 at the freeze commit) is confirmed; `SHONEN.md:286` also states "any Gates & probes row for the two new instruments is an L1 landing append not covered here".

Series structure: r35 → r42 each has a registry row; the only break in that sequence is r43. (Pre-existing anomaly, reported not fixed: `r36-closure.sh` is registered twice inside the same R36 block — `SKILL.md:1112` type `gate|probe` with the E1–E9 payload grammar, `SKILL.md:1114` type `gate` with a generic `0 closed | 1 open | 2 could-not-evaluate` map. `anchorcheck.py` also appears twice, `:981` and `:1041`, which is the intended per-round re-registration pattern.)

---

## 3. Live post-append state (working tree, **uncommitted**, not this seat's edit)

Snapshot `2026-10-28T16:08:13-03:00`: SKILL.md sha256 `b066b4dbf7fd16c659cbcae088db2ae4bb61ef86fe9cf40accd5a38859414ece`, 1143 lines, `git diff --stat -- SKILL.md` → `1 file changed, 9 insertions(+)` (append at EOF only, no base line moved — R6 honoured).

```
SKILL.md:1136  ## Round-44 registry correction — round-43 instrument basenames (appended 2026-10-28)
SKILL.md:1142  | claim-package-check.py | gate | `python3 corpus/instruments/claim-package-check.py <package-dir>` | …
SKILL.md:1143  | r43-closure.sh | gate | `bash corpus/instruments/r43-closure.sh --export-ref <hash> …` | …
```

Measured both ways on that same tree:

| predicate | `claim-package-check.py` | `r43-closure.sh` |
|---|---|---|
| section-name-scoped (round-36 E3 / QUALITY R29: `## …Gates & probes registry…` sections) | **0** | **0** |
| exact first cell anywhere in SKILL.md | 1 @1142 | 1 @1143 |

The gap is the heading wording: the new block is titled `## Round-44 registry correction …` and does not contain the literal `Gates & probes registry`, while every prior block does (`…Gates & probes registry addition…`). **Consequence for C1 defect 7:** the documented counter prints 0/0 on the appended tree, so either (a) the heading is renamed to the established pattern — `## Round-44 Gates & probes registry addition (appended 2026-10-28)` — and the rows stay at 1142/1143, or (b) the counter's section predicate is widened to `Gates & probes registry|registry correction`, which weakens the R29 section contract. (a) is the minimal, pattern-preserving fix; it is an L1 act, not this seat's.

The two appended rows' content matches the committed instruments' own CLIs (§1) and the frozen expected tokens (`claim-package-check.py --selftest` → `selftest cases=10 failures=0`, `.ufo/waves/round-44/controls/do-nothing.txt`; `r43-closure.sh --selftest --export-ref` → `selftest cases=19 failures=0`, `.ufo/waves/round-43/claims.json`). Those tokens are **cited, not re-executed** here.

---

## 4. Discrimination and do-nothing

- **Do-nothing:** at base, freeze and HEAD the exact-row count for both basenames is 0 and no r43/r44 registry block exists; a do-nothing replay therefore cannot present either basename as registered. The frozen control (`.ufo/waves/round-44/controls/do-nothing.txt`) records no source/knowledge/claim/frontier change at base, consistent with this.
- **Near-name mutant control** (scratch copy of SKILL.md, lane bytes untouched): appending `| claim-package-check |` (no `.py`) plus the exact rows gives, on the section-scoped counter, `claim-package-check.py exact_rows=0 substring_lines=2` and `claim-package-check exact_rows=0 substring_lines=3` — a wrong-row / near-name mutant is **rejected** by the exact-cell predicate, matching R29. Appending the exact `| claim-package-check.py |` row moves the count to 1 (positive control).
- **Section-predicate mutant (the live risk):** the same appended block is invisible to the section-name-scoped counter (§3) — i.e. a *correct* row set can still read as 0 when the heading is off-pattern, and conversely a lane could take a 1 from a differently-worded counter. Any r44 closure receipt for defect 7 must state which predicate it used and print the section heading it matched.

### Locator used (reproducible; scratch script, deleted on exit, sha256 `52875228e3fccc551eeef7e3ff02714cadd35c4e571deaa52c123e877aed0c52`)

```python
import sys
root = sys.argv[1]; names = sys.argv[2:]
lines = open(f"{root}/SKILL.md", encoding="utf-8").read().split("\n")
heads = [(i, l) for i, l in enumerate(lines, 1) if l.startswith("## ")]
reg = [i for i, l in heads if "Gates & probes registry" in l]
def in_registry(i):
    prior = [s for s in reg if s <= i]
    if not prior: return False
    start = max(prior); after = [h for h, _ in heads if h > start]
    return i < (min(after) if after else len(lines) + 1)
rows = {}
for i, l in enumerate(lines, 1):
    if in_registry(i) and l.startswith("|"):
        rows.setdefault(l.split("|")[1].strip(), []).append(i)
for n in names:
    hit = rows.get(n, [])
    print(f"basename={n} exact_rows={len(hit)} lines={hit} substring_lines={sum(1 for l in lines if n in l)}")
```

Committed-bytes run (`python3 … kasegi-shokunin r43-closure.sh claim-package-check.py r42-closure.sh r36-closure.sh claim-package`):

```
skill_lines=1135 registry_sections=10
registry_section line=977  heading=## Gates & probes registry
registry_section line=1037 heading=## Round-29 Gates & probes registry addition (appended 2026-10-25)
registry_section line=1050 heading=## Round-30 Gates & probes registry addition (appended 2026-10-25)
registry_section line=1060 heading=## Round-31 Gates & probes registry addition (appended 2026-10-25)
registry_section line=1073 heading=## Round-33 Gates & probes registry addition (appended 2026-10-26)
registry_section line=1094 heading=## Round-35 Gates & probes registry addition (appended 2026-10-26)
registry_section line=1107 heading=## Round-36 Gates & probes registry addition (appended 2026-10-26)
registry_section line=1118 heading=## Round-40 Gates & probes registry addition (appended 2026-10-26)
registry_section line=1124 heading=## Round-41 Gates & probes registry addition (appended 2026-10-27)
registry_section line=1130 heading=## Round-42 Gates & probes registry addition (appended 2026-10-28)
basename=r43-closure.sh exact_rows=0 lines=[] substring_lines=0
basename=claim-package-check.py exact_rows=0 lines=[] substring_lines=0
basename=r42-closure.sh exact_rows=1 lines=[1134] substring_lines=1
basename=r36-closure.sh exact_rows=2 lines=[1112, 1114] substring_lines=2
basename=claim-package exact_rows=0 lines=[] substring_lines=5
```

(`skill_lines=1135` is `split("\n")` on a trailing newline; the file's last content line is 1134, `wc -l` = 1134.)

---

## 5. Limitations

- `HYAKU_SCRATCH` is unset in this environment (siblings `R44Review8/9/15` recorded the same and hit `Permission denied` on `mkdir`). Scratch was created instead at the existing fleet scratch root `/home/vgpnk/Projects/shokunin/.scratch/kasegi-r44/R44Exec5/` (never `/tmp`), and removed on exit — see §6.
- SKILL.md changed under this seat mid-measurement (uncommitted integrator append at `16:04:14-03:00`). All committed figures are pinned by blob digest; the §3 working-tree figures are timestamped and unstable until committed. The lane working tree is concurrently dirty across `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt` — none of it this seat's.
- No gate, selftest or suite was run (editing wave in flight); the `cases=10` / `cases=19` tokens are quoted from the frozen control and claims, not re-executed. No LSP symbol service applies (markdown/registry prose item).
- This seat makes no verdict on C1/C2 closure. It reports: defect 7's registry target is `SKILL.md:977` with basename-in-first-cell rows; committed state is 0/0; the uncommitted append supplies 1/1 but is invisible to the R29-scoped counter until its heading matches the established `Gates & probes registry` pattern.

## 6. Scratch cleanup

`/home/vgpnk/Projects/shokunin/.scratch/kasegi-r44/R44Exec5/` (locator script + one SKILL.md fixture copy) was deleted after the report was written; deletion verified in the transcript. No file under `kasegi-shokunin/` was written except this report.
