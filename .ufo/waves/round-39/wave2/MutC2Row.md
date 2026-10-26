# MutC2Row-4 — receipt (kasegi round-39 wave 2, falsify)

Seat: MutC2Row-4, mutation tester, leaf (no subagents spawned). Dispatched by L1
KasegiR39 (hyaku run 9). Date: 2026-10-26 (UTC). Judged axis: depth:verifiability.

## Item

Mutate the S057 row on a scratch mirror of SOURCES.md (single-cell changes):
tier A→C, kind docs→spec, status mined→queued, NF 13→12, source cell with two
URLs, opened date future; run `sources-census.sh validate --file` on each mirror
and record which mutations the census catches (E-code) and which pass (W01 etc.,
report-only fleet property); also run the lane's own awk census commands from
CORPUS.md on each mirror. Deliverable: `.ufo/waves/round-39/wave2/MutC2Row.mutations.txt`.

I am an ATTACK seat and did not author any byte under attack: the S057 row, the
census script and CORPUS.md are wave-1/fleet work I only read and executed.

## What I ran (actual outputs in the deliverable)

1. Read the frozen claims (`claims.json`, `claims-erratum-1.md`), the fleet
   CORPUS.md §SOURCES.md census block, `scripts/sources-census.sh` (806 lines),
   and the landed S057 row at lane HEAD 5006097a84305267c9a3e8c1e1d560e60fe41d37
   (SOURCES.md last touched by 1a139e0 wave-1 integration; `git diff --stat --
   corpus/SOURCES.md` empty → mirror = landed HEAD bytes).
2. Built S=/fast/scratch/hyaku/kasegi-r39/MutC2Row-4/ with a byte-identical
   mirror tree `$S/lane` (cp -a of the lane corpus/, 6.6M; cmp identical;
   sha256 f33d10f45142b6d59969cedbfc35a1d29a3ba672d62067da8424fc0d32a728f2) and
   six mutant trees `$S/mut-{tier,kind,status,nf,twourl,opened}`; each mutant
   verified to differ from pristine in exactly one line (the S057 row).
3. Baselines: frozen counting command `sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kasegi` → exit 0 (two pre-existing W04
   warnings S028/S029, report-only); pristine `validate --file` → exit 0,
   identical shape; `selftest` → "selftest ok" exit 0 (96 killed / 0 SURVIVED);
   pristine awk census rows=59 (matches erratum E1), malformed=0, tier
   A=55 B=2 C=2, status mined=44 queued=9 rejected=6, all must-print-nothing
   checks clean.
4. Census on each mutant (`validate --file`) and the seven CORPUS.md awk
   commands on each mirror (cwd = lane root for the used-by `[ -e ]` check).

## Results (detail in MutC2Row.mutations.txt)

| mutation | fleet census | lane awk | caught? |
|---|---|---|---|
| tier A→C | W01 S057 tierC mined used-by=… , exit 0 | tier hist A=54 C=3 | warning-only; census exit unmoved (frozen kill-rule "new W/E code" limb would trip) |
| kind docs→spec | silent, exit 0 | identical to pristine | NO |
| status mined→queued | silent, exit 0 | status hist mined=43 queued=10 | NO (histogram shift only) |
| NF 13→12 | E01 S057 fields=10, exit 1 | malformed=1 | YES (both) |
| source cell two URLs | silent, exit 0 | identical to pristine | NO (url_of reads first URL only) |
| opened 2027-01-01 | E08 S057 opened=2027-01-01, exit 1 | identical to pristine | YES (census only) |

## Findings (coverage, report-only — no contract change proposed here)

- The C2 kill-rule limb "census exit != 0" guards 2/6 frozen S057 cells (NF
  shape, opened date). Tier, kind, status and source-cell content drift without
  moving the census exit code; kind drift moves nothing at all (no E, no W, no
  histogram — kind has no histogram command).
- The E5 binding "source cell carries exactly <page URL>" is unenforced: the
  census normalizes only the first URL per cell; a second URL — even the row's
  own linked 508c PDF — passes silently.
- In-enum drift is invisible to the enum checks by design; catching status
  drift requires a pinned expected histogram, which CORPUS.md's census block
  does not pin.
- Tier downgrade of a mined, used row is W01-only: the tool's own contract
  prints `file ok` and exits 0 ("warnings do not affect clean lanes").
- Minor defense-in-depth gap shared by both instruments: malformed rows
  (NF!=13) are exempt from the used-by existence check (NF==13 condition / E01
  `next`), so a malformed mined row escapes the path check.
- Do-nothing controls all hold: frozen counting command exit 0 on the real
  lane; pristine mirror reproduces it; selftest 96/0; pre-existing W04×2 are
  the only baseline findings.

## Compliance

- Writes: only `.ufo/waves/round-39/wave2/MutC2Row.mutations.txt` (deliverable),
  this receipt, and scratch under /fast/scratch/hyaku/kasegi-r39/MutC2Row-4/
  (removed after the copy; trap-equivalent explicit rm -rf executed before
  yield). No lane/fleet/sibling/source-tree file edited; no mutating git/jj
  command anywhere (read-only `rev-parse`, `status`, `log`, `diff --stat` on
  the lane only); no pacman (paused); no tool installed or upgraded (gawk
  5.4.1, bash, coreutils already present — tooling record: none installed).
- Disk guard green before the pass: /fast 615G available (24% used).
- TMPDIR bound to scratch for the selftest run; /tmp unused.
- Scratch contents destroyed post-copy: mirror trees, mutant trees,
  census-mut-*.out, awk-matrix.{sh,out}, selftest.out, tmp/.

## Verdict

The S057-row frozen cells are NOT uniformly guarded: 3 of 6 single-cell
mutations (kind docs→spec, status mined→queued, second URL in the source cell)
pass both the fleet census and the lane awk census silently; tier A→C passes
the census exit code and surfaces only as a new W01 warning. NF-shape and
future-opened mutations are caught (E01/E08, exit 1). This is a coverage
finding against C2's census-based guard limbs, not a kill: the frozen C2
predicate's other limbs (row counts, entry binding, harness, binding, audit)
were not attacked by this seat.

Report: .ufo/waves/round-39/wave2/MutC2Row.md
