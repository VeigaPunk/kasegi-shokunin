# MutC2Row — S055 registry-row mutation probe (census gate)

Axis: coverage. Milestone: round-38. Leaf seat, no dispatch. Judged on: coverage.

Item: mutate the planned S055 registry row and show the census rejects each of seven defects —
tier C; kind community with tier A; NF!=13 (extra pipe); used-by → missing file; duplicate id
S054; opened date malformed; recheck prose — running
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>` per
mutant, recording exit codes and E/W codes, and flagging any mutant that survives (exit 0).

## Baseline (pristine planned row, before any mutation)

Row under test: `.ufo/waves/round-38/wave1/ScribeRowS055.row.md` — 1 line, 1713 bytes,
sha256 `901309af744b32383f3c8fe4c8023a960201baa65028600f0b9c31da59ff96cc`, NF=13 (11 cells:
`spec` / `A` / `mined` / `2026-10-26` / `180d` / used-by
`corpus/knowledge/csaf-vex-product-status-and-justifications.md`). This is the landing
candidate: the scribe receipt declares these bytes final, and mid-probe the L1 landed them
byte-exact at `corpus/SOURCES.md:61` (see "Mid-probe lane landing" below).

Mirror (scratch only): `cp -a <lane>/corpus $S/mirror/corpus` at lane HEAD
`700153593eb586c70a6499c8ca225ee4d673bc9b` (registry sha256
`ead94cc69c09afc2da890c7124f09852b4da26880de193e782dfba03eaf6e671`, 54 rows, S054 at `:60`),
planned row inserted after line 60
(`awk -v rowf=<row.md> 'NR==60{print; while ((getline l < rowf) > 0) print l; close(rowf); next} {print}'`),
and the sibling entry deliverable `ScribeEntryF21.entry.md` (sha256
`0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a`) copied to the used-by path
so the baseline is clean (E11 is existence-only, `sources-census.sh:538-574`).

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r38/MutC2Row/mirror/corpus/SOURCES.md
exit=0
```

Baseline registry sha256 `451dba0ffac6470bb8eb83f2e4c83afeb8ad72b47f170c986f83205e347fae1b`
(55 rows, row at `:61` byte-identical to the deliverable). Only the two pre-existing W04
warnings — matches `.ufo/waves/round-38/census-before.txt`.

## Mutants and verdicts

Every mutant is the baseline registry with ONE cell of the S055 row changed; verified per
mutant: `diff` vs baseline = exactly one changed line (`changed_lines=2` = one `<` + one `>`),
and the changed cell shown below. Generation template (line 61 only):

```
gawk -v p='<pattern>' -v r='<replacement>' 'NR==61{sub(p,r); print; next} {print}' \
  $S/mirror/corpus/SOURCES.md > $S/mirror/corpus/SOURCES.<name>.md
```

| mutant | one-cell change (pattern → replacement) | census code line | exit | verdict |
|---|---|---|---|---|
| M1 | `[|] spec [|] A [|]` → `\| spec \| C \|` | `W01 S055 tierC mined used-by=corpus/knowledge/csaf-vex-product-status-and-justifications.md` | 0 | **SURVIVED** |
| M2 | `[|] spec [|] A [|]` → `\| community \| A \|` | `E10 S055 community-at-A` | 1 | killed |
| M3 | `[|]$` → `\| \|` (extra trailing pipe) | `E01 S055 fields=12` | 1 | killed |
| M4 | `csaf-vex-product-status-and-justifications[.]md` → `absent-mutc2row-probe.md` | `E11 S055 missing used-by corpus/knowledge/absent-mutc2row-probe.md` | 1 | killed |
| M5 | `[|] S055 [|]` → `\| S054 \|` | `E03 S054 duplicate id` | 1 | killed |
| M6 | `[|] 2026-10-26 [|]` → `\| 2026-10-26T18:17:40Z \|` | `E08 S055 opened=2026-10-26T18:17:40Z` | 1 | killed |
| M6b | `[|] 2026-10-26 [|]` → `\| 2026-02-30 \|` (impossible ISO) | `E08 S055 opened=2026-02-30` | 1 | killed |
| M7 | `[|] 180d [|]` → `\| next errata, then 180d \|` (punctuated prose) | `E09 S055 recheck=next errata, then 180d` | 1 | killed |
| M7b | `[|] 180d [|]` → `\| when the next CSAF errata ships \|` (alphabetic prose) | *(none — output identical to baseline)* | 0 | **SURVIVED** |

M6b and M7b are sub-variants of the assigned "opened date malformed" and "recheck prose"
defect classes, run to test whether each class is fully rejected or only partially. Every run
used exactly the item's command shape:
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>`.

## Findings (survivors — census exit 0)

**F1 — tier downgrade A→C survives with a warning (M1).** The census prints
`W01 S055 tierC mined used-by=…` and exits 0 (`sources-census.sh:669`; doc `:31`). The only
tier-integrity *error* is E10 community-at-A (`:668`); tier C is a valid enum for any kind, so
a tier downgrade of a tier-A spec row is warned, never rejected. Bound: the frozen C2 kill
rule ("census exit != 0 **or a new W/E code**") still catches a landed tier-C row through the
new-W-code clause, so the claim is not exposed — the gap is in the gate, not the claim.

**F2 — punctuation-free prose recheck survives with no code at all (M7b).**
`symbolic()` (`sources-census.sh:582`) accepts any `^[A-Za-z][A-Za-z0-9 _-]*$` string as a
cadence, so alphabetic prose passes E09 (`:664-666`) with no code: M7b's output is
byte-identical to the baseline (W04 S028, W04 S029, `ok`, exit 0). This mutant is invisible to
the census exit **and** to the C2 kill rule's "new W/E code" clause — a landed row with
recheck `when the next CSAF errata ships` would satisfy the frozen census predicate
unchanged. Punctuated prose (M7) is rejected (E09). Coverage finding: the symbolic-cadence
escape cannot distinguish a cadence token from a prose sentence.

Per the seat role these are coverage findings, not permission to change the contract; no
census or claim file was touched.

## Killed mutants — verbatim census outputs

All outputs below are the actual stdout of the runs (lane name `file` in `--file` mode);
each also carried the two pre-existing `W04` lines (S028, S029) shown once here:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
```

```
M2-community-atA      exit=1   file	E10	S055 community-at-A
M3-extra-pipe         exit=1   file	E01	S055 fields=12
M4-dangling-usedby    exit=1   file	E11	S055 missing used-by corpus/knowledge/absent-mutc2row-probe.md
M5-dup-id-S054        exit=1   file	E03	S054 duplicate id
M6-opened-timestamp   exit=1   file	E08	S055 opened=2026-10-26T18:17:40Z
M6b-opened-impossible exit=1   file	E08	S055 opened=2026-02-30
M7-recheck-prose-punct exit=1  file	E09	S055 recheck=next errata, then 180d
```

Cell-level proof the mutations landed (line 61 of each mutant): M1 `| spec | C |`;
M3 tail `…justifications.md | |`; M4 used-by cell `absent-mutc2row-probe.md`;
M5 `| S054 | …`; M6 tail `… | mined | 2026-10-26T18:17:40Z | 180d | …`;
M7 tail `… | mined | 2026-10-26 | next errata, then 180d | …`;
M7b tail `… | mined | 2026-10-26 | when the next CSAF errata ships | …`.
Mutant registry sha256s: M1 `fcb963d7…60215`, M2 `531eeac6…7dd58`, M3 `8dd66858…aa91`,
M4 `c1c0858e…a6ff`, M5 `47c712e3…95b27`, M6 `71ff70f3…f2219`, M6b `66865b34…b2722`,
M7 `f0d8d751…072c`, M7b `5cde9f1f…0dc3` (full hashes in the transcript; scratch since removed).

## Mid-probe lane landing (not this seat's write)

At `2026-10-26 15:40:18 -0300`, after my mirror was built, the lane working tree received the
L1's landing: `corpus/SOURCES.md` now hashes `451dba0f…` — byte-identical to my mirror
baseline (`diff` empty; row at `:61` identical to the planned-row deliverable) — plus
`corpus/knowledge/csaf-vex-product-status-and-justifications.md` (22887 bytes) and the other
C2 surfaces, all uncommitted (HEAD still `7001535`). This seat wrote nothing outside its
scratch and this receipt; every seat command only read the lane. Live census on the real lane
post-landing:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
live exit=0
```

The C2 census predicate holds on the landed bytes; because the landed registry is
byte-identical to my mutant baseline (sha `451dba0f…`), every mutant verdict above transfers
1:1 to the landed state.

## Notes

- M4's first generation emitted a benign `gawk: warning: escape sequence '\.' treated as
  plain '.'` (from `-v p='…\.md'`); the substitution and E11 result were correct. Re-run clean
  with a `[.]` class — the evidence above is the clean run.
- Row-version drift observed: `RevRowS055.md:3` reviewed a 1671-byte revision (sha
  `c4309a21…`); the on-disk deliverable is the 1713-byte final (sha `901309af…`) that
  `ScribeRowS055.md` declares and the L1 landed. My baseline used the on-disk final bytes.
  (Informational; owned by ScribeRowS055/RevRowS055.)
- The entry deliverable on disk (sha `0343ef45…`) differs from the sha `ScribeRowS055.md`
  recorded for it (`96899762…`) — revised after that receipt; E11 is existence-only, so no
  result here is affected. (Informational.)
- Tooling: nothing installed — bash 5.3.20, gawk 5.4.1 already present; no pacman, no network
  fetch, no mutating git (read-only `git -C <lane>` log/status/rev-parse/diff only).

## Touched surfaces

- Wrote: this receipt only (`.ufo/waves/round-38/wave1/MutC2Row.md`). No `<SEATNAME>.<suffix>`
  deliverable — the item lands findings, not landable text.
- Scratch `/fast/scratch/hyaku/kasegi-r38/MutC2Row/` removed before yield (verified:
  `ls` → No such file or directory; `grep -c MutC2Row` over the scratch root → 0).
- Read-only: lane `corpus/` tree, `scripts/sources-census.sh` (sha256
  `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`), frozen
  `claims.json`, `census-before.txt`, `c2-controls/before.txt`, wave receipts. No fleet-root,
  shokuknow, or sibling-lane write; lane `corpus/SOURCES.md` sha unchanged by this seat
  (`ead94cc6…` before the L1's landing, `451dba0f…` after it — the L1's bytes, not mine).
