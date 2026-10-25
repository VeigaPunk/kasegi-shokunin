# ExecSkillGateSupport — SKILL.md gate-row support measurement

- seat: `ExecSkillGateSupport` (executor, read-only; **no production file written**)
- round/wave: kasegi-shokunin round 28, wave 1 (build+attack)
- axis: `depth:verifiability` · milestone: round-28
- lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` · base `c9f8b115a098c65356e4b3b6048af45a37ab8395`
- worktree HEAD at measure: `94f387cbee71a532a51ce075f01701a557231e85`
- measured (UTC): `2026-10-25T17:24:13Z` … `2026-10-25T17:30:00Z`
- receipt: `.ufo/waves/round-28/receipts/ExecSkillGateSupport.txt`

## 0. State labels — both production edits landed during this seat

The assignment says to label the measurement PRE-STATE if the instrument impl has not landed.
At measurement start that was true; by measurement end both owning seats had landed, so the
receipt records **two** states and the final numbers are POST-IMPL.

| state | SKILL.md | anchorcheck.py | note |
|---|---|---|---|
| P1 PRE-STATE | `fa09d5b8…64f2d` — 1032 lines, == HEAD, mtime 09:35:29 −0300 | `c2a9e6c6…ef748` (frozen C1.before) | `date -u` 17:24:13Z while SKILL.md mtime was still 09:35 −0300 |
| P2 LANDED | `125be37d…6cca6` — 1035 lines, mtime 14:26:18 −0300 (17:26:18Z) | `95333e29…44514` — 523 lines, stable at 17:29:25Z and 17:29:32Z | row at 982 + EOF note at 1035 |

Intermediate bytes, recorded so they are not mistaken for a final pass: SKILL.md `68d1c377…`
(17:26Z — differs only in the EOF note) and instrument digests `29aba084…` (17:27Z —
`--selftest` raised `NameError: name '_selftest' is not defined`, exit 1) then `c3629229…`
(17:27:50Z — selftest 9/0, superseded). All were superseded by the owning seats; the final
re-measure at 17:29:32Z on `95333e29…` reproduced `selftest cases=9 failures=0` and the same
SKILL.md summary. This seat wrote neither production file.

## 1. Registry table shape (assigned grep)

Command (assigned):

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -nE 'gate\|probe|anchorcheck' SKILL.md | head -20
```

- PRE-STATE: exactly **one** hit, line 981 (`recheck-audit.py`).
- LANDED: **two** hits, lines 981 (`recheck-audit.py`) and 982 (`anchorcheck.py`).

Section geometry (LANDED): heading `977` → blank `978` → header `979` → separator `980` →
data rows `981–982` → blank `983` → prose note `984` → blank `985` → next heading `986`.

Declared columns (8): `name | type | entry command | verdict map | self-test |
pinned-value path | write scope | owner`.

### Shape defect measured (pre-existing, now replicated)

Both data rows contain the type marker as an **unescaped** `gate|probe`. That yields 9 cells
against an 8-column header. GFM parsing (markdown-it-py 4.2.0, `commonmark` + `table` rule)
shows both rows rendering 8 `<td>` with every field shifted one position right and the 9th
cell — `owner` — dropped:

```
recheck-audit.py | gate | probe | python3 corpus/instruments/recheck-audit.py [--json <out>] | 0 clean | 1 failed | … | python3 … --selftest | .ufo/waves/round-26/… | corpus/ read-only + its own receipt dir
anchorcheck.py   | gate | probe | python3 corpus/instruments/anchorcheck.py <file.md> | fail-closed: … | python3 … --selftest -> … | .ufo/waves/round-28/… | all inputs read-only + its own receipt dir
```

So on both rows `type` renders as `gate`, `entry command` as `probe`, and the owner
`kasegi` is not rendered at all. The verdict-map/self-test pipes are correctly escaped
(`\|`); only the marker pipe is not.

Marker counter from the round-26 lesson (control #4, `grep -cE '^\| [^|]+\| gate\|probe '`):

| bytes | count |
|---|---|
| PRE-STATE | 1 |
| LANDED | 2 |
| scratch variant with `gate\|probe` (escaped) | 1 — the counter cannot see the row |

This is the trade-off the owner faces: the escaped form renders 8 correct cells but is
invisible to the round-26 marker counter; the unescaped form keeps both rows aligned with
each other and the counter at 2, but reproduces the one-field shift and drops `owner`.

## 2. Appended-row line number and R6 no-shift check (assigned)

### 2.1 Pre-state arithmetic (base `fa09d5b8…`, 1032 lines)

`wc -l` = 1032; the file ends with `\n` after line 1032, which is the last row of the
4-column “Frontier decision table”. There is **no trailing blank line**, and the last
section is *not* the gates registry. Measured variants on scratch copies:

| variant | block appended | row lands at | file lines | GFM result |
|---|---|---|---|---|
| A | bare table row immediately at EOF | **1033** | 1033 | absorbed as a 6th row of the frontier table; only 4 cells survive |
| B | blank + `## …` heading + blank + header + separator + row | **1038** | 1038 | proper 8-column table |
| C | in-table insert after line 981 | **982** | 1033 | correct table continuity, but shifts lines |

R6 proof: `head -1032` of variants A and B is **byte-identical** to `git show HEAD:SKILL.md`
(`cmp` → no difference). Appending at EOF therefore moves **zero existing anchors**.
The largest external anchor at that base is `SKILL.md:1021`; the only live-production
reference file is `corpus/instruments/resolve-dispatch-fixtures.json` (2 occurrences, both
`SKILL.md:1000`).

### 2.2 Landed reality — the shift did happen

The owner chose variant C (row at 982) plus an EOF note at 1035. The measured +1 shift:
old lines 982..1032 moved to 983..1033. Each affected anchor now resolves one line early
(the old content sits at *n+1*):

| anchor | HEAD content | LANDED content at same line |
|---|---|---|
| `SKILL.md:993` | `docs/autopsies/` | `docs/review-verdicts.jsonl` |
| `SKILL.md:1000` | `ops/shared.mjs` | `evidence/<program>/` |
| `SKILL.md:1014` | `.ufo/bh*/` | `fleets/registry.json` |
| `SKILL.md:1019` | `{README.md,.gitignore}` | `.omp/{config.yml,agents/,skills/}` |
| `SKILL.md:1021` | `pendle-core-v2-public/` | `.git/` |

In-file anchorcheck position: the only citation at or below the insertion point moved
`md:998 → md:999` (visible as the assigned `tail -1` output in §3).

Reference sites now off by one (measured by `grep -rn`):

- live production: `corpus/instruments/resolve-dispatch-fixtures.json` (2 occurrences);
- frozen prior-round evidence: 7 refs at 993, 12 at 1014, 3 at 1019, 3 at 1021,
  119 at 1000 across `.ufo/` (including round-23/24/25/26 wave files and scratch copies).

Anchor numbers ≤ 981 — including the row itself, the round-26 lesson’s `977`/`981`
references — are unaffected.

**Pre-existing drift, independent of this round.** The fixture’s `why` calls the
`{validate,registry-check,reroute-drill,check-freshness}.mjs` set “`SKILL.md:1000`”. At the
fixture’s own landing commit `d3614a2` (round 24) that set was at line **998** — already 2
off. At HEAD it is at **1007**; at LANDED bytes it is at **1008**. (The +9 comes from
round-26’s insertion of the gates section, `1023 → 1032` lines.)

### 2.3 If a further append-at-EOF is made

On the landed 1035-line file: a bare row lands at **1036** (1036 lines); a sectioned block
puts the row at **1041** (1041 lines). Both measured with `cmp` to leave the first 1035
bytes byte-identical — zero existing anchors move.

## 3. anchorcheck.py SKILL.md summary (assigned)

Assigned command:

```bash
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | tail -1
```

Verbatim (LANDED bytes, POST-IMPL instrument):

```
LOST-RECORDED md:999 [lost-base] check-freshness.mjs:61 (not checked)
```

`tail -1` returns a **verdict line**, not the summary. The summary is stdout line 2 (line 1
is empty). Verbatim:

```
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

- `exit=0`; stderr 0 bytes; stdout 315 lines.
- class counts: `OK=7`, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `ORIGIN=0`,
  `OUTSIDE-BASE=0`, `BASE-ABSENT=0`.
- instrument that produced it: `95333e29…44514` (523 lines, stable across 17:29:25Z and
  17:29:32Z); on these bytes `--selftest` prints `selftest cases=9 failures=0`, exit 0.
  The digest moved during the seat (`29aba084…` → `c3629229…` → `95333e29…`); all three
  produced this same SKILL.md summary, and the L1 must re-run against the digest it commits.

**PRE-STATE cross-check:** the identical summary (7 / 0 / 306, other classes 0, exit 0,
315 lines) was produced by the pre-change instrument `c2a9e6c6…` on the pre-edit SKILL.md
`fa09d5b8…`, and again by `c2a9e6c6…` on the first landed SKILL.md `68d1c377…`. The row and
the EOF note moved **no** verdict class; the only observable delta is the in-file position
`md:998 → md:999` caused by §2.2.

**State label:** POST-IMPL (the instrument digest is no longer the frozen
`c2a9e6c6…`). This is the post-impl no-harm input the item asks for, at the digest above.
The L1 should still re-run after the wave settles, because both files were being written
during this seat.

## 4. Frozen-counter defect (claims.json C1 counter #4)

The frozen `bad` extractor prints nothing:

```bash
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null \
  | sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'
```

The summary contains a single `N bad;`, while the pattern demands a second `N bad` after
it. Verbatim frozen-counter run (lane root): `0`, then an empty line where `bad=` should be,
then `lost=306`. Corrected equivalent, measured: `bad=0` from
`s/^== .* \([0-9]*\) bad;.*/bad=\1/p`. The `lost` extractor in the same counter is correct.
Evidence only — `claims.json` is frozen and was not edited.

## 5. Risks / routed observations (no edits made)

1. **R6 deviation is live.** The registry row is at 982, not an EOF append; five external
   anchor line numbers now resolve one line early. Only one live production file is
   affected (the dispatch fixture, 2 occurrences); the frozen prior-round evidence carries
   25 refs at 993/1014/1019/1021 plus 119 refs at 1000 (all under `.ufo/`). The EOF note
   itself is R6-clean.
2. **Registry render is one field off on both rows** because of the unescaped marker; the
   `owner` cell does not render. Fixing it for the new row only (escaped) would make the
   round-26 marker counter stay 1; fixing the old row too is the consistent option.
3. **The new row’s self-test claim is now true** (`selftest cases=9 failures=0`), but it was
   briefly false mid-write (`NameError`). Any receipt citing the intermediate digest would
   be wrong; the final measured digest is `95333e29…44514` (and still worth re-running at
   the committed digest).
4. **Fixture anchor drift predates this round** (2 lines at creation, 8 now at `SKILL.md:1008`
   for a comment that says `:1000`). Not caused here; worth a same-line suffix fix if the
   fixture is ever touched.
5. **Assigned `tail -1` does not return the summary** — the summary is stdout line 2. Any
   downstream counter written as `tail -1` would silently record a verdict line.

## 6. L1 re-run (required — this seat ran no build/lint/test gate)

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum SKILL.md corpus/instruments/anchorcheck.py
wc -l SKILL.md
grep -nE 'gate\|probe|anchorcheck' SKILL.md | head -20
python3 corpus/instruments/anchorcheck.py SKILL.md > /tmp/r28-skillgate-post.out 2>&1; echo exit=$?
sed -n '2p' /tmp/r28-skillgate-post.out
awk '{print $1}' /tmp/r28-skillgate-post.out | sort | uniq -c
grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md
python3 corpus/instruments/density.py SKILL.md --label r28-post | grep -E 'mean dens|Total path|^# Density'
```

Expected on final bytes: exit 0; summary `7 in-range / 0 bad / LOST-RECORDED=306 /
PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0`; marker counter ≥ 2. Density is
`20 blocks / 656 path cites / mean 160.2` with the row in the existing block (pre-edit
`20 / 652 / 150.3`); it becomes `21 blocks / 656 / 147.9` if the row is moved into a new
`##` section.

## 7. Tooling

Ephemeral only: `uv run --with markdown-it-py` (uv 0.13.0, markdown-it-py 4.2.0,
CPython 3.14.8) for the GFM table checks. No pacman transaction, no persistent install, no
write outside `$TMPDIR`, this receipt, and this report.
