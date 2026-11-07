# ScribeGate — round 96, w1 (drafting seat: lesson Gate, Mistakes, knowledge entry)

Seat: leaf scribe. No claim judged, no product file edited, no commit made.
Lane HEAD when the seat opened: `7ef1d36`; the L1 landed its integration
`b7f59c6` mid-seat, so the drafts below are an independent second reading of the
same evidence, compared against the landed text rather than written into it.

## Verdict

DRAFTS COMPLETE — three artifacts written under this seat's receipts
(`01-gate-draft.md`, `02-mistakes-draft.md`, `03-knowledge-entry-draft.md`), no
claim re-scored. I re-derived the landed numbers I could check and AGREE with
them: registry 143 → 145, census `kasegi ok` rc 0 with exactly seven W04
warnings, S144 capture digest/bytes, S145 fetch size, and the landed entry's own
`recheck:` line (rc 0, `anchorcheck` 0 bad). Seven findings (F1-F7) are routed against
the landed round-96 integration; none changes a frozen claim, and one (F1) is
already being repaired in the working tree while this seat ran.

## Deliverables (draft, not landed)

1. **Gate block** — `.ufo/waves/round-96/w1/ScribeGate-receipts/01-gate-draft.md`.
   Round-95 shape: three candidates, S144 ADMIT (`docs`, tier A, `mined`) with
   URL, opened 2026-11-07, and a 20-word quote at
   `corpus/source-snapshots/round-96/S144.txt:346-347`; S145 REJECT with reason
   and flip; S140 re-opened with no status change. Registry and census lines
   carry the commands and their observed outputs.
2. **Mistakes table** — `.ufo/waves/round-96/w1/ScribeGate-receipts/02-mistakes-draft.md`.
   Six rows (class / evidence pointer / captured-by / fix): the two pre-freeze
   fixture defects, the `declared=None` harness path, the successor `LABELS_PATH`
   constant, the scratch log that carries two summaries, and the entry
   misstatement F1.
3. **Knowledge entry** — `.ufo/waves/round-96/w1/ScribeGate-receipts/03-knowledge-entry-draft.md`.
   Opens with `source:` / `verified-at: 7ef1d365…` / `recheck:`; states the seven
   shapes with their S140 line cites, the two tails, the boundaries the scanner
   enforces, and the remaining known limits. `anchorcheck` on the draft: 11
   in-range cites, 0 bad, 9 distinct anchors, rc 0.

## What I re-derived (AGREE)

| number | command | observed |
|---|---|---|
| registry 143 at base, 145 now | `git show d8a2bb0:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` and the same grep on the tree | `143` / `145` |
| census `kasegi ok` rc 0, seven W04 | `cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok …/corpus/SOURCES.md`, W04 on S028, S029, S072, S076, S080, S085, S143, rc 0 |
| S144 capture identity | `sha256sum` + `wc -lc` | `d6e529275deb3ecf4ea2c3edaff2caa882760680cf23c1a134424e6acffdb83d`, 17,591 bytes, 418 newlines |
| S144 quote | `sed -n '346,347p' … \| tr '\n' ' ' \| wc -w` | 20 words |
| S145 fetch size | `stat -c '%s' /fast/scratch/hyaku/kasegi-r96/l1/gitlab-api-auth.html` | 53,671 |
| landed entry recheck | the entry's own `recheck:` line, verbatim | `RECHECK-OK`, rc 0; `anchorcheck` 8 in-range, 0 bad |

## Findings (routed; none re-scores a frozen claim)

- **F1 — `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md:78-79`
  misstates S140 line 136.** The entry says "the runner versioned rule publishes
  none"; S140 line 136 publishes `(?:[a-zA-Z0-9]{1,20}-)?` before `glrtr?-`.
  The landed matcher does omit it (`capture-secret-scan.py:249`), and that is
  harmless: a probe with a custom prefix and the versioned tail still hits,
  because the left boundary `(?<![A-Za-z0-9_])` (`:237`) accepts the hyphen that
  precedes `glrtr-`; the only effect is a shorter matched span. The working tree
  has already repaired the table row (`:42`) with the correct statement, which
  now *contradicts* the sentence at `:78-79` still standing in the same file.
  Fix: replace `:78-79` with the table row's wording, or drop the sentence.
- **F2 — `corpus/lessons/round-96.md:47` gives a census command that does not
  resolve from the lane.** `bash scripts/sources-census.sh …` returns
  `No such file or directory` rc 127 from the lane root; the script is at
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. The result it
  reports is correct once run from the fleet root (F-table above). Fix: prefix
  `cd /home/vgpnk/Projects/shokunin &&`.
- **F3 — `corpus/lessons/round-96.md:18` says the S144 quote is "21 words"; it is
  20** (`sed -n '346,347p' … | tr '\n' ' ' | wc -w` prints `20`).
- **F4 — the capture line count is off by one in three places.** The round-96
  manifest says `"lines": 419`, and the lesson (`:15`) and the entry (`source:`)
  repeat 419; `wc -l` and `awk 'END{print NR}'` both print 418 and the file ends
  with a newline. The round-94 manifest's `"lines": 563` matches its `wc -l`, so
  the round-96 figure is not a different convention — it is +1.
- **F5 — two pre-freeze repairs have no durable receipt.** The `unlabelled-only`
  duplicate-pair repair is evidenced only by the harness's own comment
  (`c1-controls-r96.py:215-218`) and the receipt's `dup_rows=0`; the
  `declared=None` harness crash is evidenced only by the fix's shape
  (`:117-126`) and the receipt's `missing-labels` line, which carries no
  `attribution=` field. My M96-2/M96-3 rows are therefore corroborated, not
  directly evidenced — a future seat cannot re-derive them. Also, the pre-freeze
  scratch log `c1-controls-run.log:125-129` carries two summaries in one file
  (`pass controls=12` then `fail controls=12`); only the single-run receipt was
  committed, which is the right call, but the log should not be cited as
  evidence anywhere.
- **F6 — the landed Gate's S140 item asserts an HTTP 403 (Cloudflare) for the
  live raw URL** (`corpus/lessons/round-96.md:36`) with no fetch receipt in the
  lane. It is L1 testimony; my draft omits it rather than repeat an observation
  I did not make. If it is kept, it needs the fetch log path.
- **F7 — a coverage qualifier, not a claim change.** The plain `glagent-`
  50-character form (S140 line 213) is still undetected: the landed pattern list
  (`capture-secret-scan.py:247-254`) has only the versioned `glagent-` shape.
  C2's frozen statement names seven shapes and is unaffected; the L1's live
  working-tree edit already adds this to the entry's known limits.

## Out of scope / not done

- No edit to any product, lesson, entry, SOURCES row, SCORECARD or LOG file; no
  `git add`/`commit`/`checkout`/`reset`/`stash`; no jj command.
- No C1 or C2 verdict: this seat drafts, and the frozen predicates belong to the
  wave's critics and reviewers.
- The live working tree moved during the seat (entry `:42` and known-limits
  edit, uncommitted). Findings F1/F7 describe that state as read; the L1 should
  re-read before landing.

## Receipts

All under `.ufo/waves/round-96/w1/ScribeGate-receipts/`:

| file | command(s) | observed |
|---|---|---|
| `10-registry-and-census.txt` | registry grep at `d8a2bb0` and in the tree; census from the lane (rc 127) and from the fleet root (rc 0) | `143`, `145`; `No such file or directory` rc 127; `kasegi ok` rc 0 with seven W04 |
| `11-fixture-defect-fx-dbg.txt` | `git -C …/l1/fx-dbg show 7dc5d52 -- …labels.tsv`; the post-fix `ctl/fx-snap` row; `sed -n '199,207p' c1-controls-r96.py` | pre-fix row `…:136 S020.txt range <path> evidence`; post-fix row `<path> <path>`; harness writes the path twice |
| `12-harness-fixture-lines.txt` | `sed -n '117,126p'` and `'215,220p'` of the harness | `declared is None` branch; line-89 no-op fixture |
| `13-counter-expected-edit.txt` | `sed -n '242,254p' knowledge-meter.py` | `range` edit is `key` → `label` |
| `14-frozen-receipt-controls.txt` | `grep -E 'CONTROL (snapshot-missing-only\|unlabelled-only\|missing-labels)\|^ATTRIBUTION\|^C1-CONTROLS-RESULT'`; `grep 'LIMB M3'`; `wc -l` | `limbs=M4,M5 declared=M4,M5 attribution=PASS`; `limbs=M10,M9 declared=M10,M9 attribution=PASS`; `missing-labels … declared=-`; `dup_rows=0`; `ATTRIBUTION pass fixtures=11`; `C1-CONTROLS-RESULT pass controls=12`; 126 lines |
| `15-s140-s144-anchors.txt` | seven `sed -n` reads of S140; S144 quote, word count, digest, bytes | the seven regex lines; quote 20 words; `d6e5292…`, 17,591 bytes |
| `16-landed-entry-recheck.txt` | the landed entry's `recheck:` line verbatim | `anchorcheck` 8 in-range 0 bad; `7`; `RECHECK-OK`; rc 0 |
| `17-runner-prefix-probe.txt` | `capture-secret-scan.py --files` on two synthetic fixtures (bytes not reproduced) | both hit — `gitlab-runner-auth-token-versioned` and `gitlab-pat-versioned`; `hits=2 … rc=1` |
| `18-landed-gate-numbers.txt` | quote word count; `stat` of the two scratch fetches; `grep -n` for the census path and the `publishes none` sentence | `20`; `53,671`; `67,805`; `round-96.md:47`; `gitlab-routable-and-versioned-token-forms.md:79` |
| `19-draft-entry-anchorcheck.txt` | `anchorcheck.py` on the draft entry | 11 in-range, 0 bad, 9 anchors, rc 0 |
| `20-self-scan.txt` | the lane's own `capture-secret-scan.py --files` over this report and every receipt | `scanned=15 hits=0 files=0 allowed=0 unused_allow=25 rc=0` |

Every receipt ends with the `rc=` of its last command: `10` records both the
lane-root census failure (rc 127) and the fleet-root run (rc 0); `11`-`16` and
`18`-`19` record rc 0; `17` records rc 1, which is the scanner's "hits found"
exit, not an error.
