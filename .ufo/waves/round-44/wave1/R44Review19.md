# R44Review19 — source census: invocation, expected warnings, exit-0 conformance

Seat item: *check source census invocation, expected warnings, and what makes exit 0 conformance.*
Read-only leaf lane. No lane/fleet file was created, modified or deleted by this seat; the only write
is this report. No tool installed or updated. No LSP server was available in this tool inventory, so
every check below is literal text / exit-code / committed-byte evidence, never semantic proof.

Measured against lane `kasegi-shokunin` at `HEAD = 66314015122b9aa32dc40f2f1815df56624c26d1`
(freeze commit) with a **dirty worktree** (see MED-3) and against the frozen base
`5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` exported read-only with `git archive`.

Instrument: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`; fleet repo clean for that
path: `git -C /home/vgpnk/Projects/shokunin status --porcelain -- scripts/sources-census.sh` → empty;
fleet `HEAD = cf186fd40299e32ac84bd007f0b8bfec6594d58c`).

## 1. What exit 0 is, mechanically

Documented taxonomy (`scripts/sources-census.sh:16-17`): `0 clean or warnings · 1 E/overdue findings
(or census missing) · 2 usage/env/missing registry · 3 selftest failure`. Enforced at the tail
(`:803-805`):

```
if [ "$MODE" = census ] && [ "$missing" -gt 0 ]; then exit 1; fi
[ "$missing_error" = 1 ] && exit 2
[ "$findings" = 1 ] && exit 1
exit 0
```

`findings` is set **only** by an `E`-code line (`:740`), and `W01`–`W04` are emitted without touching
it (`:645`, `:674`; header text `:31-33`: "warnings do not affect clean lanes"). Therefore:

**exit 0 == every resolved target's `corpus/SOURCES.md` exists, parses, and produces no `E`-code line.**
It is *not* "no findings", *not* "rows present", *not* "revision-pinned", and *not* knowledge/frontier
conformance.

## 2. Invocation: the root must be the fleet root, not the lane

The prompt-literal form exits **2** (tool-contract error, not a registry finding):

```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin/kasegi-shokunin kasegi
ERROR: config not found: /home/vgpnk/Projects/shokunin/kasegi-shokunin/shokunin.conf
ERROR: unknown lane (not a dir, not in conf or root): kasegi
exit=2
```

Cause: `build_roster` needs `$ROOT/shokunin.conf` (`:454`), and the lane has no `scripts/` and no
`shokunin.conf` (`ls -d …/kasegi-shokunin/scripts` → *No such file or directory*). The first ERROR is
emitted from a **command substitution** (`roster=$(build_roster)`), so its `die` kills only the
subshell; the terminating message is the misleading `unknown lane` (`:525`). Both are exit 2, so the
status is right and the diagnosis is not.

Correct invocation — reproduces the frozen control byte for byte (`.ufo/waves/round-44/controls/do-nothing.txt:17-22`):

```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

Equivalent variants, all exit 0 with the same warning rows:

- `--root` may be **omitted** — `ROOT` defaults to the script's parent (`SHOKUNIN_ROOT`/`realpath
  $(dirname $0)/..`): running `…/scripts/sources-census.sh validate kasegi` from a scratch cwd gives
  the identical three lines.
- Passing the lane **directory** instead of the lane id gives the same registry verdict but labels the
  lane `kasegi-shokunin`, not `kasegi` — so the token `kasegi ok` is produced only by the conf-based
  invocation. A receipt that quotes `kasegi ok` must therefore have used `--root <fleet> kasegi`.
- Fleet-wide `validate --root <fleet>` (no lane arg) also exits 0 today, over 453 output lines and 21
  `ok` lanes; it is not a kasegi receipt.

Self-test (scratch `TMPDIR`, no `/tmp`): `selftest` → 96 `killed`, 0 `SURVIVED`, `selftest ok`, `exit=0`.

## 3. Expected warnings: exactly two, and structurally explainable

At the frozen base, exactly two rows are the *second* occurrence of a normalised URL in a different
scope (re-derived from `git show 5ab3a60:corpus/SOURCES.md` with the script's own `url_of` rule —
lower-case host, strip trailing `/` and `#fragment`, keep path case):

- `S028` (base line 34) duplicates `S006` (line 12) — `docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq`;
- `S029` (base line 35) duplicates `S024` (line 30) — `eur-lex.europa.eu/eli/reg/2024/2847/oj/eng`.

`S029` does **not** trip `E04` (same-scope duplicate) because its `teaches` cell carries
`supersedes S024`; `S028` cannot trip `E04` because `E04` skips `status=rejected`. `W04` has no status
filter (`:645`), so both warnings are permanent under the append-only rule — they are an invariant, not
noise. The same invariant is recorded by six prior non-author spot-checks (round-25/29/30/31 lessons
all read "W04 S028/S029 only"), and `corpus/lessons/round-43-verifier-spotcheck.md:66` reads
`W04 S028`, `W04 S029`, `ok`, **exit 0**.

**Expected warning set for the round-44 receipt = `{W04 S028, W04 S029}` and nothing else.** Any third
`W`-line (e.g. `W03 mined but unused`, or a `W04` on the new row) is expected-warning drift that still
exits 0 (see HIGH-2).

## 4. Findings

### HIGH-1 — Census exit 0 has zero discriminating power for C2; it is green under do-nothing

Exporting the frozen base and validating it read-only:

```
$ git -C …/kasegi-shokunin archive 5ab3a60 | tar -x -C base
$ scripts/sources-census.sh validate --today 2026-10-28 base
base	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
base	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
base	ok	/fast/scratch/hyaku/kasegi-r44/R44Review19/base/corpus/SOURCES.md
exit=0
```

The frozen base exits 0 with the identical warning set. `claims.json:21-22` lists "SOURCES census
validates exit 0" as part of C2's *after* state, but the *before* state already satisfies it. The census
must not be cited as evidence that the new row landed; only the row metric (68 → 68+N), the absence of
new `W`-codes, and `E11` green at the judged revision discriminate.

### HIGH-2 — exit 0 ≠ no findings; a new warning or a mined-but-unused row reads as clean

Fixtures built from the base archive (`cp -a --reflink=auto`), each mutating only
`corpus/SOURCES.md`:

```
M4  mined row, used-by = —            → m4 W03 S069 mined but unused ; m4 ok ; exit=0
M5  new row reusing S006's URL        → m5 W04 S069 duplicate url … ; m5 ok ; exit=0
M11 rejected row, used-by = "-"       → m11 ok ; exit=0            (no W, no E)
```

So a row that carries no knowledge entry at all (M4) and a row that introduces a *third* duplicate-URL
warning (M5) both pass as "conformance". The report must enumerate the `W`-set, not quote `exit 0`.

### HIGH-3 — exit 0 ≠ rows; and `census` mode silently ignores misplaced rows

```
M6  registry with header+separator only → m6 ok ; exit=0 ; census m6 → rows 0
M1  valid row appended at EOF            → validate m1: E12 S069 row outside Registry section ; exit=1
                                            census   m1: rows 68 ; exit=0        (row uncounted, no error)
```

`census` mode does not emit `E12` (that branch is `mode=="validate"`, `:621`), so the row metric alone
would under-report without failing. The C2 row evidence must be the **pair**: `validate` (E12) *and*
`census … rows` *and* the frozen grep counter, which must agree.

They do agree on the base: `census … rows` → `68`; frozen counter
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `68`.

### HIGH-4 — Row placement: the Registry section is not the file tail

`corpus/SOURCES.md` at base: `## Registry` line 3, `## Paths` line 76, `## Search log` 84,
`## Leads (unopened)` 102, `## Registry changes` 108. A "cheap append" of `S069` at EOF lands under
`## Registry changes` and fails:

```
M1 → m1 E12 S069 row outside Registry section ; exit=1
M2 (same row inserted before `## Paths`) → m2 ok ; exit=0 ; census m2 → rows 69
```

Live tree at measurement: `S069` line 75, `S070` line 76, `## Paths` line 78 — correctly inside the
Registry table. The census is the only gate that catches this; a reviewer re-deriving with
`tail`/`grep -c` alone would not.

### HIGH-5 — (adjacent to the census, same frozen claim) the C2 counter's frontier leg is unsatisfiable

`claims.json:23` freezes `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`. Run exactly as
decoded, at the frozen base:

```
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md        → 0
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md  → 25   (the do-nothing control's form)
```

The rows are `| F01 | CVSS v4.0 severity and vector semantics | admitted | knowledge/… | … |`
(`corpus/README.md:202`), so the frozen pattern cannot emit 25 now or 26 after F26 lands. The
do-nothing control (`controls/do-nothing.txt:10`) uses the working `.*` variant. The census leg of the
counter is sound (`68` = census `rows` `68`); the frontier leg is not, and the round-44 receipt must not
quote the frozen counter verbatim as frontier evidence without naming this defect.

### MED-1 — Exit-code taxonomy must be stated in the receipt, and 2 outranks 1

Observed across all fixtures: `0` (A2, M2, M4, M5, M6, M11, selftest), `1` (`E12` M1, `E11` M3/M12,
`E01` M7, `E08` M8, `E03` M9), `2` (wrong root A1; missing registry M10 →
`m10 missing …/corpus/SOURCES.md ; exit=2`). In `validate` mode a missing registry sets
`missing_error` (`:713`) and the tail tests it **before** `findings`, so exit 2 masks a simultaneous
exit-1 condition. A receipt that reports only the number cannot distinguish "registry absent" from
"registry present with `E` findings".

### MED-2 — The census reads the working tree, not a commit; the current receipt is unpinned

```
$ git -C …/kasegi-shokunin status --porcelain -- corpus/SOURCES.md corpus/README.md corpus/knowledge
 M corpus/README.md
 M corpus/SOURCES.md
?? corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
$ sha256sum corpus/SOURCES.md            → 56032a4f450e01ebcee64a51846c2e6c6e6fbc55942d265483480516514f54ca (70 rows)
$ git show HEAD:corpus/SOURCES.md | sha256sum → fd96d38b03585db8952740958e87db6aa0a4b54f0abb30d9ca3f9a7a1b60c358 (68 rows)
$ git show 5ab3a60:corpus/SOURCES.md | sha256sum → fd96d38b… (identical to HEAD)
```

At 70 rows the census is green with the unchanged warning set (`rows 70`, `W04 S028`, `W04 S029`, `ok`,
`exit=0`) — but that green depends on an **untracked** knowledge file existing on disk (see MED-3), and
the committed revision still holds 68 rows. The round-44 receipt must name the revision, the digest of
`corpus/SOURCES.md`, and the fleet-root invocation; a receipt taken on a dirty tree is not
reproducible at the judged commit.

### MED-3 — `E11` binds the new row to a working-tree path, only for `mined`

```
M3  mined row, used-by corpus/knowledge/absent-entry.md → m3 E11 S069 missing used-by … ; exit=1
M12 mined row, used-by "-"                             → m12 E11 S069 missing used-by - ; exit=1
```

This is the usable red-before control for the C2 gate: run the census before the entry lands → `E11`,
exit 1; after → exit 0. It also fixes the sequencing: the row and the entry must be in the same
revision (or the census must run only after both are on disk). But `E11` is **path existence only**
(`:567`), and only for `status=mined` — it proves nothing about whether the entry cites `S069`. The
`source: S069` binding must be shown separately (`grep -rlE '^source: S069' corpus/knowledge | wc -l`).

### LOW-1 — `used-by` dash convention is enforced asymmetrically

`W03` compares against the em dash `—` (U+2014) exactly (`:674`). A `mined` row written with ASCII `-`
is treated as a path and fails `E11` (M12, exit 1), while a `rejected` row with ASCII `-` passes
silently (M11, exit 0). The live `S070` cell is the correct em dash (`xxd` → `20 e2 80 94 20`).

### LOW-2 — Per-lane `census` output omits zero buckets

`kasegi` lines carry only seen keys (`rows`, `tier.A|B|C`, `status.mined|rejected`) while the `FLEET`
block prints every bucket including zeros. A consumer that greps a per-lane `status.queued` line gets
nothing rather than `0`.

## 5. Do-nothing discrimination

| observable | do-nothing (base `5ab3a60`) | round-44 after-state must show | discriminating? |
|---|---|---|---|
| `validate` exit | 0 | 0 | **no** |
| `W`-set | `{W04 S028, W04 S029}` | same set, no additions | weak (drift detector only) |
| census `rows` | 68 | 68 + N_new (70 live) | **yes** |
| frozen counter row leg | 68 | 69 (one new row) / 70 | **yes** |
| knowledge entries | 62 (committed) | 63 | **yes** (not a census observable) |
| `E11` for the new row | n/a (no row) | green only with the entry on disk | **yes** |

Conclusion: **the census contributes a guard, not a discriminator.** C2's kill rule is satisfied only
by the row/knowledge counters plus `E11`/`E12` being green; "SOURCES census validates exit 0" alone is
reached by do-nothing and must not be scored as coverage movement.

## 6. Conformance predicate the round-44 receipt must satisfy (copy-ready)

Run from the fleet root (or with `--root /home/vgpnk/Projects/shokunin`); never with the lane root:

1. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `exit=0`.
2. Output is exactly `W04 S028`, `W04 S029`, then `kasegi\tok\t…/kasegi-shokunin/corpus/SOURCES.md`; no third `W`, no `E`.
3. `…/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi` → `rows` equals the frozen
   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` value (68 at base).
4. The new row is inside `## Registry` (before `## Paths`), `status=mined`, `used-by` = a path that
   exists at the judged revision (else `E11`), and that entry is the one that cites `S069`.
5. The tree is clean at the judged revision and `git show <rev>:corpus/SOURCES.md | sha256sum` is quoted
   (base/HEAD digest `fd96d38b…`; the 70-row worktree digest is `56032a4f…` and is not evidence).
6. Cite the instrument digest `3fb72615…` and the fleet revision, since the census lives outside the lane.

## 7. Fixture recipe (reproducible without the deleted scratch)

```bash
S=$(mktemp -d /fast/scratch/hyaku/kasegi-r44/R44Review19.XXXX)      # never /tmp
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 5ab3a60 | tar -x -C "$S"
cp -a --reflink=auto "$S" "$S/m4"                                    # one mutant per finding
# insert a row immediately before `## Paths` (M2/M3/M4/M5/M8/M9/M11/M12):
awk -v r='<row>' '/^## Paths$/ && !done {print r; done=1} {print}' "$S/m4/corpus/SOURCES.md" > x && mv x "$S/m4/corpus/SOURCES.md"
# M1 appends the same row at EOF instead: >> "$S/m1/corpus/SOURCES.md"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-28 "$S/m4"; echo "exit=$?"
```

Row template (11 cells): `| S069 | Fixture — <url> | docs | A | <scope> | meta, opened 2026-10-28 |
operative text | <status> | 2026-10-28 | 90d | <used-by> |`. Mutations: M3 `used-by` =
`corpus/knowledge/absent-entry.md`; M4/M11 `used-by` = `—`; M12 `used-by` = `-` and `status` = `mined`;
M5 `url` = `https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq`, `scope` = a new
string; M8 `opened` = `2026-12-31`; M9 id = `S028`; M7 drops the `recheck` cell; M6 rewrites
`corpus/SOURCES.md` to header + separator + `## Paths` only.

## 8. Limitations

- The live lane tree was being mutated by sibling seats during measurement; every tree-level number
  above is a timestamped observation at `HEAD 6631401` + dirty tree digest `56032a4f…`, not a
  revision-pinned fact. The revision-pinned facts are the `git archive 5ab3a60` fixture results.
- I did not verify the semantic content of the new knowledge entry, the F26 frontier row, the C1
  counter, or the claim-package gate — out of this seat's item. HIGH-5 is reported because it sits in
  the same frozen claim's counter and is materially false, not because it was assigned.
- All checks are literal-text/exit-code; no LSP server was available, so no semantic reference or
  definition check was run. `grep` output here is text evidence only.
- Scratch: `/fast/scratch/hyaku/kasegi-r44/R44Review19` (`HYAKU_SCRATCH` was unset; used the round
  default `/fast/scratch/hyaku`). Contains the base export, eleven mutant trees, the fixture driver and
  transcripts; removed on exit.
