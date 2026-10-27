# RevC2Shape — C2 counter-chain discrimination verification (receipt)

Item: run every frozen C2 counting command on base `5b29ea1439450b712581edf5f0f0bf98dfb262ab`
(the claims-literal 38-char `…5f0bf98…` does not resolve; corrected per
`.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` — the 40-char form is used below and was verified
`git cat-file -t` → commit), confirm the `c2-controls/before.txt` BEFORE values, then re-run the
same commands on a scratch tree with ONLY the F24/S063 structural rows (do-nothing-plus) and
identify which kill-rule limbs fire. Verdict follows; transcripts are byte-exact in the sidecar.

Deliverable: `.ufo/waves/round-41/wave1/RevC2Shape.transcripts.txt`
(823 lines, sha256 `4598aa491d57edaf6cbdb784ce39cb45671e0782fb14226e6e1152cb5e82f042`).

## Method

- `git -C <lane> archive 5b29ea1439450b712581edf5f0f0bf98dfb262ab | tar -x` → `base-export`
  (scratch `/fast/scratch/hyaku/kasegi-r41/RevC2Shape/`; removed after receipt).
- `control-export` = `base-export` + exactly: `## Round-41 admission` block + `| F24 … admitted
  | knowledge/rfc-9116-security-txt.md | S063 | … |` row in `corpus/README.md` (EOF append, F23
  shape); `| S063 | RFC 9116 … rfc9116 | spec | A | … | mined | 2026-10-27 | on-release |
  corpus/knowledge/rfc-9116-security-txt.md |` inside `## Registry` (after S062, line 69);
  `[r41 Frontier amendment …]` EOF append in `PROVINCE.md`. NO `corpus/source-snapshots/round-41/`,
  no manifest record, no `corpus/knowledge/` file, no `knowledge-expected.txt` change.
- Variants (each = control + one more element): **B** + `round-41/manifest.json` S063 record
  (matching URL/fetched_utc, no capture file); **C** + expected-list row only; **D** + junk
  `corpus/knowledge/junk-f24-twin.md` citing `source: S063` (not in expected list); **E** =
  control with used-by `—`; **F** = maximal twin (record + fabricated `S063.txt` whose quotes
  self-verify + entry at the canonical path + expected row); **FL** = F with the entry recheck
  `cd`'d at the committed lane (the shape a landed row carries).
- The nine frozen commands ran verbatim per tree (`cwd=<tree>` for relative paths; census ran
  `--root <scratch-fleet> kasegi` over a `kasegi-shokunin` copy + 4-line `shokunin.conf`, and also
  verbatim `--root /home/vgpnk/Projects/shokunin kasegi` for the base reference).

## A. Base tree — every frozen command prints the frozen BEFORE value

| frozen command | frozen before | observed on base-export | match |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 23 | **23** | yes |
| `grep -cE '^\|[ \t]*S[0-9]{3,}[ \t]*\|' corpus/SOURCES.md` | 62 | **62** | yes |
| `awk -F'|' … S063 status==mined` | 0 | **0** | yes |
| `grep -rlE '^source: S063' corpus/knowledge \| wc -l` | 0 | **0** | yes |
| `ls corpus/knowledge/*.md \| wc -l` | 59 | **59** | yes |
| `frontier-recheck-count.py` | entries=26 pass=26 exit=0 | **entries=26 pass=26 exit=0** (26 PASS lines; F09/F10/F11 carry two entries each — 23 rows ↔ 26 entries) | yes |
| `capture-binding-check.py` | records=54 bound=54 unbound=0 | **records=54 bound=54 unbound=0**, 16 `MANIFEST` lines, `orphans=1 orphan=S040-live.txt`, exit=0 | yes |
| `recheck-audit.py --quiet` | expected=59 missing=0 unexpected=0 exit=0 | **`expect=present expected=59 missing=0 unexpected=0`**; `lines=59 total=59 pass=59 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0` | yes (values); see §D artifact note on `exit` |
| `sources-census.sh validate --root <fleet> kasegi` | exit 0 (W04 S028/S029) | verbatim fleet-root run: `W04 S028`, `W04 S029`, `ok`, **exit=0** — byte-matches `census-before.txt`; scratch-fleet run identical modulo path | yes |
| extra `before.txt` fields (not in the frozen list) | F24 rows 0; queued 0; admitted 23 | **0 / 0 / 23** | yes |

The harness `entries=26` for 23 `| F<n> |` rows is correct: the harness counts (row → entry)
pairs, and F09/F10/F11 each name two entries.

## B. Do-nothing-plus control — kill limbs that fire vs limbs that cannot

`control-export` results (full lines in sidecar `control.txt`):

| counter | observed on control | before→after | kill limb fired |
|---|---|---|---|
| frontier rows | **24** | matches after-value | none — by design, the row IS the claim |
| registry rows | **63** | matches | none |
| S063 mined | **1** | matches | none |
| citing S063 | **0** (needs 1) | at before | "the entry missing" limb |
| knowledge files | **59** (needs 60) | at before | "the entry missing" limb |
| harness | **entries=27 pass=26 exit=1**; `FAIL F24 knowledge/rfc-9116-security-txt.md problems=missing-entry` | yes — harness-not-27/27 fires, and names the row + the missing path | "no PASS F24 line" + "entries=27 pass=27" |
| binding | **records=54 bound=54 unbound=0 exit=0** | still at before | **none** — see finding 1 |
| audit `--quiet` | `lines=59 expected=59 missing=0 unexpected=0` | expected!=60 fires; **`unexpected` cannot see a row** | "recheck-audit expected!=60" — but see finding 2 |
| census | `E11 S063 missing used-by corpus/knowledge/rfc-9116-security-txt.md`, **exit=1** | new E code + exit!=0 | "census exit!=0 or a new W/E code" |

**Fired: harness (missing-entry, names F24), census (E11, exit 1), citing/knowledge counters
(below floor), source-recheck probe (`manifest UNAVAILABLE reason=missing` exit 2), audit
`expected!=60`. The kill rule's disjunction holds — a row-only twin is rejected.**

## C. Variant discrimination map — what each limb can and cannot see

| tree | adds | binding | audit | source-recheck | census | net |
|---|---|---|---|---|---|---|
| control | rows only | 54/54 unbound=0 green | expected=59≠60 | manifest missing exit=2 | E11 exit=1 | REJECTED |
| B | + manifest record (no capture file, no quotes) | **55/55 unbound=0 exit=0 — still green** | expected=59≠60 | `missing-quotes` exit=2 (record-shape limb fires first) | E11 exit=1 | REJECTED |
| C | + expected-list row only | 54/54 green | **expected=60 missing=1 exit=1** — `missing` limb fires | — | E11 exit=1 | REJECTED |
| D | + junk entry file `junk-f24-twin.md` | 54/54 green | **unexpected=1 exit=1** — the `unexpected` limb fires on the unlisted file | — | E11 exit=1 | REJECTED; citing→1 and knowledge→60 hit AFTER-values on a junk file — string-presence only |
| E | rows with used-by `—` | 54/54 green | expected=59≠60 | — | **exit=0, W03 warning only** | REJECTED anyway (harness/citing/knowledge/audit) |
| F | full fabricated set | **55/55 unbound=0** | `expected=60 missing=0 unexpected=0` (counted fields green; strict `cdroot` limb reds the scratch `cd` — artifact) | **`S063:sha256 OK; Q1/Q2 OK exit=0`** | `ok` exit=0 | **all nine counted values reach after-state** |
| FL | F but recheck `cd`s the committed lane | 55/55 | **`--cdroot` run: exit=0** fully green | harness `FAIL F24 recheck-exit-2` (lane lacks the manifest) | `ok` exit=0 | limb-pair cross-check, see §D |

## D. Findings (precision, not admission — recommendation surfaces for the L1/judge)

1. **The `binding` counter cannot fire `unbound!=0` on a structural twin.** Rule B binds manifest
   records to rows; there is no row→record requirement. Rows-only → `records=54 bound=54`;
   even a *record whose capture file is absent* binds green (variant-B: `MANIFEST round-41
   records=1 url_bound=1 … records=55 bound=55 unbound=0 exit=0`) — the record→file direction is
   documented as not-a-rule (`capture-binding-check.py` docstring: "the reverse direction (a
   record naming a file that is absent) is not a rule here — `source-recheck.py` fails closed on
   a missing capture"). The kill-rule phrasing "its manifest record unbound" and the
   `before.txt` verdict line "a mined-marked junk S063 row … fails binding" are measured
   overstatements for the row-only shape: binding stays green; the twins are killed by harness +
   census + citing/knowledge + audit limbs instead. The O4 precedent (round-40) differs: that
   twin flipped rows to `rejected` *over existing records*, firing `rejected-row-anchor` —
   `unbound=7`. Round-41's shape has no such record at control time.
2. **`recheck-audit`'s `unexpected` limb is file-driven, not row-driven.** The spec'd "audit
   unexpected" fires only on an unlisted knowledge FILE (variant-D: `unexpected=1`). The row-only
   control trips `expected!=60`; the expected-row-without-file twin trips `missing=1`
   (variant-C). All three directions red the counter — the limb is bidirectional — but the
   literal limb name matters for receipt wording.
3. **Residual bound — maximal twin greens every frozen counter.** Variant-F (fabricated 301-byte
   `S063.txt` whose quotes/sha256 self-verify, fabricated entry citing S063, expected-list row,
   structurally sound rows) reaches: 24, 63, 1, 1, 60, `entries=27 pass=27 exit=0` with
   `PASS F24 … ids=S063`, `records=55 bound=55 unbound=0`, `expected=60 missing=0 unexpected=0`,
   census `ok` exit 0 — and `source-recheck S063` exits 0 (`sha256 OK`, `Q1/Q2 OK`). This is the
   M34-5/"no landed check rejects the junk twin" class, reproduced end-to-end this round: the
   counters measure internal consistency, never upstream truth. The kill rule's wording ("a
   mined-marked row **without capture+entry+harness pass**") does not reach a twin that carries
   all three — discrimination for that class remains outside the counter chain (S063's
   fetch-evidence anchor cell + human/reviewer verification). At-scratch audit `exit` still reds
   on the strict `cdroot` limb only because the fabricated entry `cd`s into scratch (§4's
   artifact); FL shows audit `exit=0` when the entry `cd`s the lane.
4. **Scratch-run artifact disclosure (not a counter defect):** `recheck-audit.py --quiet`
   verbatim on an export prints `strict pass=1/59 cdroot_fail=58 … exit=1` because entries' `cd`
   lines name the committed lane while `cdroot` defaults to `--root`. With
   `--cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin` the same bytes print `strict
   pass=59/59 … exit=0` on base, matching `before.txt`. The counted contract fields
   (`lines/total/expected/missing/unexpected/fail-closed`) are unaffected by `cdroot`. Per-entry
   rechecks execute in the committed lane by design (`cd <lane>` inside each `recheck:` line),
   which is also why FL's harness reds on `recheck-exit-2` while its audit greens — the
   instrument pair reads different roots for a scratch tree.

## Verdict

**The C2 counter chain is sound for its stated purpose**: on base every frozen command
reproduces `c2-controls/before.txt` exactly (9/9 values + 3 extra fields), and the
do-nothing-plus control is rejected by multiple independent limbs — `FAIL F24
problems=missing-entry` + `entries=27 pass=26 exit=1` (harness), `E11 … missing used-by` +
exit 1 (census), citing/knowledge below floor, audit `expected!=60`, `source-recheck` exit 2.
Two receipt-precision notes (binding limb and `unexpected` limb cannot literally fire on a
row-only shape — other limbs carry the kill, so the kill-rule disjunction still holds) and one
residual bound (a full self-consistent fabricated package greens all nine counters; outside this
claim's wording and consistent with the M34-5 disclosure) are recorded for the L1/judge.

## Command anchors

- runner: `$S/run-counters.sh <tree> <scratch-fleet> <out>` — verbatim frozen commands per tree.
- transcripts: `base.txt`, `control.txt`, `variant-{B,C,D,E,F,FL}.txt`, `probes.txt`
  (source-recheck probes + verbatim fleet census + extra fields) — all in the sidecar.
- tools: none installed (git/python3/bash/gawk/grep only). No mutations anywhere outside
  `$S` and this wave dir; scratch removed on receipt write.
