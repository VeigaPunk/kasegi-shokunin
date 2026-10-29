VERDICT: BROKEN

Scope: seat R46bRevF29H6H7 — attacks on `corpus/instruments/r46-f29-gate.py` limbs H6+H7 only.
No edits made anywhere; counters/claims untouched. All runs are re-runs I performed
2026-10-29 against fixture trees built from the frozen base export
(`git -C <lane> archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x`),
under scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevF29H6H7` (removed after this report).

Gate invocation for every run:
`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root <tree>`

Do-nothing control (base export + one stub entry `corpus/knowledge/github-repository-security-advisories.md`,
8800 bytes, to satisfy H6's 66-name count and the >=3000-byte entry check):
```
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=2/7 exit=1
```
(H1–H5 are red by construction in this fixture — README has 28 rows and there is no
S074 row/manifest at base; those limbs belong to other seats. Only the H6/H7 read
tokens discriminate below.)

FINDINGS

F1 (H6 HOLDS) — ledger shrunk below its floor but keeping its name: KILLED.
Attack: `head -c 20000 <tree-a>/corpus/knowledge/considerthese-proposals-ledger.md` (floor is
LEDGER_MIN_BYTES=30696; the base ledger is exactly 30696 bytes — the floor equals the freeze size).
```
$ stat -c %s ...  -> 20000 ledger-after-truncate
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
```

F2 (H6 HOLDS) — nested .md under a symlinked subdir: KILLED.
Attack: `mkdir -p $S/evilhost/nested && printf '# evil nested doc\n' > $S/evilhost/nested/bad.md &&
ln -s $S/evilhost/nested <tree-b>/corpus/knowledge/zz-linked-dir`
(the symlink target lives outside the tree; the nested .md never appears in listdir).
```
gate H6 pass=0 read=knowledge=66 entries=67 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=1
```
Note: `nested-md` stays 66 because `os.walk` does not follow directory symlinks
(followlinks=False, gate line 245); the kill comes from `entries=67` (listdir shows the
symlink) and `symlinks=1` (the explicit islink scan). Both catch it; limb is red either way.

F3 (H6 HOLDS) — base entries swapped pairwise, name set unchanged: KILLED.
Attack: swapped the full bytes of `github-private-vulnerability-reporting.md` and
`cna-assignment-and-vulnerability-rules.md` (names untouched, so the name-set pin still matches).
```
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1 symlinks=0
```
The content pin catches the swap: the pinned digest is over `name + sha256(content)` per
base file (gate line 249: `"%s %s" % (n, sha(...))`), so swapping contents changes two
pin lines. A pure name permutation with content attached to names cannot evade it.

F4 (H7 HOLDS) — Registry section duplicated verbatim (heading + table, same 73 rows): KILLED.
Attack: `sed -n '3,80p' corpus/SOURCES.md >> corpus/SOURCES.md` (Registry spans lines 3–80,
verified via `grep -n '^## '`: Registry at 3, next section `## Paths` at 81; 73 rows).
```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <tree-d1>/corpus/SOURCES.md
d1-census-rc=1
file  E03  S001 duplicate id     (73 E03 lines total, one per re-emitted id; also E04s)
(no `ok` line emitted)
gate H7 pass=0 read=census-rc=1 ok-line=0
```
(First capture piped census through `head`, so the quoted rc there was head's; this clean
rerun quotes census rc=1 directly.)

F5 (H7 BROKEN) — a second `## Registry` heading with header but no rows: census passes, H7 GREEN.
Attack: append only the 3-line Registry preamble (`## Registry`, `| id | ... |`, `|---...---|`)
to the end of SOURCES.md.
```
$ bash .../sources-census.sh validate --file <tree-d2>/corpus/SOURCES.md
file  W04  S028 ... (3 pre-existing warnings only)
file  ok   /fast/.../tree-d2/corpus/SOURCES.md
d2-census-rc=0
gate H7 pass=1 read=census-rc=0 ok-line=1
```
Root cause: the census row parser sets `in_registry=(trim(...)=="Registry")` on every
`## ` heading (scripts/sources-census.sh:611) and has no "exactly one Registry section"
check, so a duplicate empty section heading is invisible to it. H7 faithfully relays
census, so a structurally corrupted SOURCES.md grades green. Severity: low–medium —
cosmetic corruption only; no row data changes.

F6 (H7 BROKEN) — a second `## Registry` section carrying fabricated rows: census passes, H7 GREEN.
Attack: append `## Registry` + header + separator + 3 fabricated rows
(`| S901 | Fabricated one — https://fabricated.example/one | docs | B | fake scope one | p1 |
fabricated evidence one | queued | 2026-10-01 | 90d | — |`, and S902/S903 likewise with
unique URLs/scopes; queued status so W03 "mined with used-by = —" does not even warn).
```
$ bash .../sources-census.sh validate --file <tree-d3>/corpus/SOURCES.md
file  W04  S028 ... (same 3 pre-existing warnings only)
file  ok   /fast/.../tree-d3/corpus/SOURCES.md
d3-census-rc=0
gate H7 pass=1 read=census-rc=0 ok-line=1
```
This is semantic corruption, not cosmetic: the registry gains sources that were never
opened. No gate limb sees it — H3 checks only the S074 row (still unique), H1/H2/H4/H5/H6
never read SOURCES.md — so on a fully-built wave tree this bloat leaves
`f29-gate fixed=7/7` unchanged. Severity: medium. The defect lives in the fleet census
validator (outside this lane); candidate fixes are a census-side "exactly one Registry
section" error, or an H7 amendment (logged errata — the instrument is read-only for seats)
counting `^## Registry` occurrences before delegating. No fix applied by this seat.

LIMITATIONS

- Fixture trees are base+stub; H1–H5 read red throughout and are not evidence about those
  limbs. Discrimination claim rests on the H6/H7 read tokens: control green, each attack
  flips the attacked limb to 0 (F5/F6 excepted).
- F2's `nested-md=66` reflects os.walk not following symlinks; the entry-count and islink
  sub-checks are what fired (both are part of H6's boolean, so the limb is red).
- Only the four seat-assigned vectors were built. Untested H6 shapes visible in code but
  out of scope here: extra top-level .md (would fail `names==66`), non-md file in
  knowledge/ (would fail `everything==66`), entry-as-symlink (would fail `links`), ledger
  growth above the floor (by-design exempt from the content pin).
- F5/F6 demonstrated at the H7 limb level; I did not construct a synthetic full wave tree
  (README F29 row + real entry + S074 capture) to print the literal `fixed=7/7` under bloat.
- No tools installed; nothing committed; scratch dir removed on exit.
