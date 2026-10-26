# ScribeQualityFix — `corpus/QUALITY.md` wave-2 fix (round 31)

Seat: ScribeQualityFix (leaf; no delegation, no subagent dispatch). Answering model actually run on:
`opencode-go/deepseek-v4.1-flash` (workstation config route; no model passed by this seat).
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`.
Single-writer path: `corpus/QUALITY.md` (fixes only). This seat wrote: `corpus/QUALITY.md` (append-only,
61 insertions, 0 deletions) and this receipt. Nothing else.
Tooling: nothing installed or upgraded — no pacman transaction (host-wide pause respected), no uv/npx
download, no official binary. Stdlib `bash`/`awk`/`grep`/`sed`/`sha256sum`/`python3` only.

## 0. Trigger read (bound 9 satisfied)

Polled `until [ -s MutErratumCheck.md ] && [ -s CritMistakes.md ]; do sleep 20; done`, cap exceeded the
item's 40-minute budget at 26 iterations, both files present:

```
iters=26
-rw-r--r-- 1 vgpnk vgpnk 24723 Oct 25 21:38 CritMistakes.md
-rw-r--r-- 1 vgpnk vgpnk  9479 Oct 25 21:39 MutErratumCheck.md
```

A weakness **survived** (three independent weaknesses, all measured in §2–§4 below), so this seat appended
two superseding rows instead of writing `no-change`.

## 1. Subjects, digests, quiescence

```
$ date -u +%Y-%m-%dT%H:%M:%SZ; sha256sum SCORECARD.md LOG.md corpus/QUALITY.md \
    corpus/instruments/recheck-audit.py
2026-10-26T00:41:00Z
5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7  SCORECARD.md
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
96b71caad96979b42422bd7dfc362c94913d54ffc63d2cf2dc0aac62ef2e6b2d  corpus/QUALITY.md   ← pre-append
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
$ sha256sum corpus/QUALITY.md            # after the append (§5), stable across every run in §2–§4
5899e02bc60172ecc1bfff6324fe014ab0b6aa6a6fc7e27335805b678b47e2e5  corpus/QUALITY.md   ← post-append
$ git status --porcelain | head
 M corpus/instruments/limb-mutation-check.py      ← ExecCounterFix's path, not touched here
?? .ufo/waves/round-31/wave2/                     ← wave-2 receipts (this file included)
?? corpus/lessons/round-31.md                     ← ScribeLesson's file, landed 21:40, not touched here
```

`SCORECARD.md` `5fa41aef…` and `LOG.md` `864deb7d…` are byte-identical to the wave-1 after digests, so the
wave-1 specimens and this seat's mutants are compared on like bytes (bound 6). `recheck-audit.py` is **not**
at its base digest `3fc0d751…` — the C1 limb work changed it to `5d4842da…`, and that is exactly the trigger
`SCORECARD.md:853` names ("If `recheck-audit.py` bytes change later this round … re-run and label any new
value with its date"). Live audit at that digest:

```
$ python3 corpus/instruments/recheck-audit.py --quiet 2>&1 | grep -E '^strict pass|^lines=|^expect='
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
```

So the erratum's filed/un-timestamped claim (`SCORECARD.md:839`, "the audit **now** prints `strict pass=43/43`")
is superseded on landed bytes and no label was appended (`grep -c '44/44' SCORECARD.md` → `0`). This seat may
not write `SCORECARD.md`; §6 routes it.

## 2. R18 — `supersedes R16`: the shipped M31-1 closure check, measured

### 2.1 The shipped CHECK A, verbatim from `wave1/ExecErratumCheck.md` §1, on eleven byte-states

All mutants are scratch copies in `mktemp -d` (`/tmp/tmp.AxAgOazzWT`), never lane writes. `old-A.sh` is the
wave-1 check with `$1` bound to the file under test.

| # | byte-state (scratch) | construction | shipped CHECK A | exit |
|---|---|---|---|---|
| 1 | `sc.md` | landed `SCORECARD.md` `5fa41aef…` | `stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1` `erratum_closure=closed` | 0 |
| 2 | `sc-base.md` | `git show b374febb:SCORECARD.md`, `cac64dbd…` (835 lines) | `stale_paragraphs=1 erratum_anchor=none …=0` `open` | 1 |
| 3 | `m1-delete-filed.md` | filed paragraph `813-818` deleted, erratum intact | `stale_paragraphs=1 erratum_anchor=831 …=1` **`closed`** | **0 — WRONG** |
| 4 | `m2-reword-filed.md` | `:814` `exit=1` → `exit=0` (in-place reword), erratum intact | `stale_paragraphs=2 erratum_anchor=837 …=1` **`closed`** | **0 — WRONG** |
| 5 | `m3-delete-erratum.md` | `head -n 836` (erratum block removed) | `stale_paragraphs=1 erratum_anchor=none …=0` `open` | 1 |
| 6 | `m4-unrelated-erratum.md` | erratum block replaced by an unrelated r31 `errata` section quoting both phrases, naming no address | `stale_paragraphs=2 erratum_anchor=838 …=1` **`closed`** | **0 — WRONG** |
| 7 | `m5-n0-escape.md` | filed paragraph deleted **and** phrase stripped from the erratum (no erratum at all) | `stale_paragraphs=0 erratum_anchor=831 …=0` **`closed`** | **0 — WRONG** |
| 8 | `sc-forge.md` | landed + one fabricated line carrying the live pair and a digest, naming nothing | `stale_paragraphs=2 errata…=1` **`closed`** | **0 — WRONG** |
| 9 | `sc-relabel.md` | landed + the labelling erratum §6 asks for (address + live pair + live digest) | `stale_paragraphs=3 …=1` `closed` | 0 (correct) |
| 10 | `sc-relabel-baddigest.md` | label with a wrong (`deadbeef…`) digest | `stale_paragraphs=3 …=1` **`closed`** | **0 — WRONG** |
| 11 | `sc-relabel-stalevalue.md` | label citing `strict pass=43/43` with the live digest | `stale_paragraphs=3 …=1` **`closed`** | **0 — WRONG** |

Rows 3, 4, 6, 7, 8, 10, 11 are the survivors: the shipped predicate
`if [ "$n" -eq 0 ] || [ "$c" -eq 1 ]` closes on *absence of the phrase* (7), on a reworded premise (4), on any
`Errata` line that quotes both phrases regardless of which paragraph it addresses (6), and on a fabricated,
wrong-digest or stale-value citation (8, 10, 11). Independently reproduced by the two peer receipts this seat
was told to read: `MutErratumCheck.md` §2 mutant (c) (`stale_paragraphs=0 … closed`, exit 0) and
`CritMistakes.md` §2.1 ("base bytes minus the stale paragraph, with no erratum at all, read
`erratum_closure=closed` and exit 0").

### 2.2 The tightened CHECK A' — now carried by `corpus/QUALITY.md` R18, run as recorded

The command is in `corpus/QUALITY.md:110-133` (fenced block, extracted verbatim to `/tmp/sqf-block1.sh`,
`bash -n` clean). It adds three arms the shipped form lacked: the filed span `813-819` must still hash to the
digest pinned at filing (`d6c6ea77…`), the phrase must occur at least twice, and the last `strict pass=`
reading at/after the span must carry — within itself or the two lines above — the live value and the live
`recheck-audit.py` 8-hex digest **and** the filed address.

```
$ bash /tmp/sqf-block1.sh                      # landed lane SCORECARD.md
file=SCORECARD.md filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0 live=strict pass=44/44 instrument=5d4842da
erratum_closure=open
exit=1
$ bash /tmp/sqf-block1.sh /tmp/tmp.AxAgOazzWT/sc-relabel.md     # green-after shape (scratch)
file=/tmp/tmp.AxAgOazzWT/sc-relabel.md filed_byte_identical=y phrases=3 anchor=837 naming_erratum=1 live_citation_self_naming=1 live=strict pass=44/44 instrument=5d4842da
erratum_closure=closed
exit=0
```

Verdicts over the same eleven byte-states (same scratch files, `bash /tmp/sqf-block1.sh <path>`):

| byte-state | 1 `sc` | 2 base | 3 m1 | 4 m2 | 5 m3 | 6 m4 | 7 m5 | 8 forge | 9 relabel | 10 baddigest | 11 stalevalue |
|---|---|---|---|---|---|---|---|---|---|---|---|
| shipped CHECK A | 0 | 1 | **0** | **0** | 1 | **0** | **0** | **0** | 0 | **0** | **0** |
| tightened CHECK A' | **1** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |

Diagnostic fields on the decisive states:

```
m1-delete-filed.md     filed_byte_identical=n phrases=1 … naming_erratum=1 live_citation_self_naming=0
m2-reword-filed.md     filed_byte_identical=n phrases=2 … naming_erratum=1 live_citation_self_naming=0
m4-unrelated-erratum   phrases=2 anchor=838 naming_erratum=0 live_citation_self_naming=0
m5-n0-escape.md        filed_byte_identical=n phrases=0 … naming_erratum=0 live_citation_self_naming=0
sc-forge.md            filed_byte_identical=y phrases=2 … naming_erratum=1 live_citation_self_naming=0
sc-relabel-baddigest   filed_byte_identical=y phrases=3 … naming_erratum=1 live_citation_self_naming=0
sc-relabel-stalevalue  filed_byte_identical=y phrases=3 … naming_erratum=1 live_citation_self_naming=0
```

State 1 is red **on the citation arm only** (`filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1`):
the tightened check is not red-for-the-wrong-reason; it reports that the landed erratum cites a superseded
audit reading. Stated plainly: **R18 has no conforming specimen on landed bytes today** — state 9 is the
demonstrated conforming shape, and closing the item is an append to `SCORECARD.md`, which is not this seat's
path (§6).

### 2.3 CHECK B — shipped vs tightened (`corpus/QUALITY.md:137-144`)

Scratch copies: `log-cur.md` = landed `LOG.md` `864deb7d…`; `log-base.md` = `git show b374febb:LOG.md`
`0a1865e9…`; `log-d1.md` = `## Round 30 —` relabeled `## Round 29 —`, h3 kept; `log-h2body-deleted.md` =
entry lines `1469,1549` deleted, `### Round-30 checks re-run` at `1550` kept; `log-d3.md` = base bytes plus
`### Round-30 backfill (appended)` (the wave-1 matrix-C2 cost shape).

```
log-cur.md             OLD_exit=0 NEW_exit=0 | round30_h2_headings=1 round30_h2_or_h3_headings=2
log-base.md            OLD_exit=1 NEW_exit=1 | round30_h2_headings=0 round30_h2_or_h3_headings=0
log-d1.md              OLD_exit=0 NEW_exit=1 | round30_h2_headings=0 round30_h2_or_h3_headings=1
log-h2body-deleted.md  OLD_exit=0 NEW_exit=1 | round30_h2_headings=0 round30_h2_or_h3_headings=1
log-d3.md              OLD_exit=0 NEW_exit=1 | round30_h2_headings=0 round30_h2_or_h3_headings=1
```

The tightened form (close iff `[ "$h2" -ge 1 ]`, both counts still printed) kills `MutErratumCheck`'s survivor
(d1) and `CritMistakes`' §3 mutant (entry body deleted, h3 retained), keeps the landed `LOG.md` green and the
base bytes red. Disclosed cost, measured: the h3-only backfill shape (d3) flips 0 → 1, i.e. the `R-2` h3
tolerance is withdrawn — no round entry in `LOG.md` is filed at `###` level (`## Round 29 …` `:1404`,
`## Round 28 …` `:1338`, `## Round 27 …` `:1315`, `## Round 26 …` `:1305`, `## Round 25 …` `:1246`), so the
tolerance defended a shape the file does not use.

## 3. R19 — `supersedes R13`: the stale selftest figure inside `QUALITY.md`

Filed row `corpus/QUALITY.md:77` (R13) cites `selftest cases=4 failures=0 exit=0`. The instrument prints no
such summary line at any digest this seat measured, and the live selftest prints 18 case lines:

```
$ python3 corpus/instruments/recheck-audit.py --selftest 2>&1 | grep -c '^selftest .* ok$'
18
$ python3 corpus/instruments/recheck-audit.py --selftest 2>&1 | grep -cE '^selftest cases=[0-9]+ failures=[0-9]+'
0
```

Appended row R19, and its closure check at `corpus/QUALITY.md:148-158`, extracted to `/tmp/sqf-b3.sh`,
`bash -n` clean. `Q-pre.md` = pre-append `QUALITY.md` `96b71caa…`; `Q-stub.md` = pre-append + a row naming R13
with no command; `Q-good.md` = pre-append + a row naming R13 that cites `--selftest`.)

```
$ bash /tmp/sqf-b3.sh                     # landed post-append
live_selftest_ok_lines=18 instrument_cases_summary_lines=0 supersedes_r13_rows=1 row_cites_selftest=1
r13_specimen_closure=closed
exit=0
Q-pre.md     exit=1 live_selftest_ok_lines=18 instrument_cases_summary_lines=0 supersedes_r13_rows=0 row_cites_selftest=0
Q-stub.md    exit=1 live_selftest_ok_lines=18 instrument_cases_summary_lines=0 supersedes_r13_rows=1 row_cites_selftest=0
Q-good.md    exit=0 live_selftest_ok_lines=18 instrument_cases_summary_lines=0 supersedes_r13_rows=1 row_cites_selftest=1
```

Red-before (`:0` rows) → green-after (1 row, 1 citing command), and the vacuous shape (a row naming R13 with no
runnable command) stays red — the check is not satisfied by the mere presence of the word.

Authoring correction, recorded because it happened inside this seat's own bytes: the first cut of the R19 block
counted `grep -c 'supersedes R13 -'`, which self-matched the fenced block once the block was committed into
`QUALITY.md` (`supersedes_r13_rows=2` on landed bytes) and had no `$1` fixture hook. Both were fixed before any
commit or citation; the corrected form is what §3 above measures.

## 4. What changed in `corpus/QUALITY.md` (append-only, R6-safe)

```
$ git diff -U0 corpus/QUALITY.md | grep -c '^-[^-]'
0
$ git diff --stat corpus/QUALITY.md
 corpus/QUALITY.md | 61 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 61 insertions(+)
$ wc -l corpus/QUALITY.md
157 corpus/QUALITY.md
$ awk 'NR==95||NR==96||NR==77{printf "%d: %s\n", NR, substr($0,1,40)}' corpus/QUALITY.md
77: | R13 | A counter's before and after are
95: | R16 | A result paragraph that states a
96: | R17 | An instrument limb is claimed lo
```

New: `## Round-31 wave-2 additions — byte-bound closure checks (append-only)` at `:98`, rows `R18`
(`:102`, `supersedes R16`) and `R19` (`:103`, `supersedes R13`), and three `bash -n`-clean fenced command
blocks (CHECK A' `:110-133`, CHECK B' `:137-144`, R19 `:148-158`). Every existing line kept its number, so
`SKILL.md`-style `QUALITY.md:NN` anchors elsewhere still resolve; the rows use `\|`-escaped pipes and each new
table row has exactly 4 pipes (3 columns), checked. No instrument parses `QUALITY.md` structurally
(`grep -rn "QUALITY" corpus/instruments/` → docstring citations only), so no counter's input changed.

## 5. Findings routed, not fixed (not this seat's path)

1. **`SCORECARD.md` needs the label the erratum asked for** (owner: ScribeScorecard / L1). The green shape this
   seat measured in scratch is appended to the landed file as:

   ```
   ### Round-31 errata — instrument relabel for the C1 limb change

   r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at `SCORECARD.md:813-819` is re-labelled, not rewritten: after the C1 limb work `corpus/instruments/recheck-audit.py` sha256 `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` prints `strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0` (`lines=44 total=44`), measured 2026-10-26T00:45Z.
   ```

   With that block appended in scratch, CHECK A' printed `filed_byte_identical=y phrases=3 anchor=837
   naming_erratum=1 live_citation_self_naming=1` / `erratum_closure=closed` / exit 0.
2. **`LOG.md` needs no change** under R18: CHECK B' is green on landed bytes (`round30_h2_headings=1`).
3. **`corpus/lessons/round-31.md` now exists** (`??` at this seat's start timestamp was stale — the file landed
   21:40, 50258 B, with `## Mistakes (M31-*)` at `:88`, M31-1…M31-7, and `### Critic additions … O1–O6` at
   `:101`), so `CritMistakes.md` §6's dangling-cite finding for R16/R17 resolved itself during this wave. Not
   re-verified beyond the headings listed; the lesson is ScribeLesson's file.
4. **R17 scope, not R17 weakness** (`CritMistakes.md` §6 last paragraph): two behaviour-bearing FR mutants sit
   outside R17's "claimed limb" scope. Owner: the C1 counter seats (`ExecCounterFix` / `ExecLedgerMerge`), not
   `QUALITY.md`.
5. **Residual, disclosed in R18 and not closable by a file-shape check:** a fabricated line carrying the live
   pair *and* the filed address would still read as closure. R18 binds bytes, not intent; the forgery is a
   forgery, and the row says so rather than claiming semantic verification.

## 6. Bounds

- Writes: `corpus/QUALITY.md` and this receipt only. No instrument, entry, registry, README, `SKILL.md`,
  `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, lesson, `templates/`, `scripts/`, `.ufo/state/`,
  `.ufo/watchdog.log`, `MANIFEST.json`, `/home/vgpnk/Projects/shokunin/.scratch/`, fleet root, sibling lane,
  lane Git index or jj state was written. No `git`/`jj` mutation of any kind (read-only `git show`, `git diff`,
  `git status`, `git cat-file -e`).
- All mutants lived in `/tmp/tmp.AxAgOazzWT` (`mktemp -d`); deleted at exit (see §7). No network fetch, no live
  bounty target, no credential material, no campaign-package access.
- Waited per bound 9 with `until [ -s … ]`; no busy loop, no background job, no delegation, no broadcast.
- Peer coordination: answered `agent://MutErratumCheck`'s survivor report by id; no `agent://all`.

## 7. Result

| Check | Red-before | Green-after | Discrimination |
|---|---|---|---|
| CHECK A' (R18) | landed `SCORECARD.md` `5fa41aef…` exit **1** (`live_citation_self_naming=0`; stale `43/43` cited while the instrument prints `44/44`) | exit **0** once the labelling erratum is appended (scratch, state 9) | 7 of 11 states flip from the shipped check's exit 0 to exit 1 (deleted, reworded, unrelated erratum, absent phrase+erratum, forged line, wrong digest, stale value); base bytes and the erratum-deleted control stay 1 |
| CHECK B' (R18) | — (shipped check already green on landed) | landed `LOG.md` `864deb7d…` exit **0** (`round30_h2_headings=1`) | d1, entry-body-deleted, h3-only backfill flip 0 → 1; base bytes stay 1 |
| R19 closure | pre-append `QUALITY.md` `96b71caa…` exit **1** (`supersedes_r13_rows=0`); stub row exit **1** | post-append `QUALITY.md` `5899e02…` exit **0** | vacuous stub stays red |

Scratch removal:

```
$ rm -rf /tmp/tmp.AxAgOazzWT /tmp/sqf-block1.sh /tmp/sqf-block2.sh /tmp/sqf-block3.sh /tmp/sqf-b3.sh \
    /tmp/sqf-scratch-dir /tmp/sqf-*.txt /tmp/sqf-stub-row.txt /tmp/sqf-good-row.txt && ls -d /tmp/tmp.AxAgOazzWT
ls: cannot access '/tmp/tmp.AxAgOazzWT': No such file or directory
```

Lane bytes at exit: `corpus/QUALITY.md` `5899e02bc60172ecc1bfff6324fe014ab0b6aa6a6fc7e27335805b678b47e2e5`
(append-only vs `96b71caa…`), `SCORECARD.md`/`LOG.md` untouched by this seat, `recheck-audit.py` `5d4842da…`.

## 8. Addendum — subject drift after this seat's first write, and the defect it exposed

`agent://MutErratumCheck` reported (and this seat re-measured) that `SCORECARD.md` moved past the boost-spec
`5fa41aef…` that §2 pins:

```
2026-10-26T00:51:10Z
4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da  SCORECARD.md   (947 lines, was 860)
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
$ git diff -U0 SCORECARD.md | grep -c '^-[^-]'          → 0        (append-only)
$ sed -n '813,819p' SCORECARD.md | sha256sum            → d6c6ea77… (span pin unchanged)
$ grep -nE '(([Rr]31)|([Rr]ound[- ]31))[[:space:]]+[Ee]rrata?' SCORECARD.md | head -1
837:### Round-31 erratum to the round-30 section        (first anchor line unchanged)
```

Re-run of the recorded CHECK A' on the drifted bytes:

```
$ bash "$T/b1.sh"          # SCORECARD.md 4076091c…
file=SCORECARD.md filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0 live=strict pass=44/44 instrument=5d4842da
erratum_closure=open
exit=1
```

Same verdict, and §2's `5fa41aef…` reading is labelled as its era, not silently carried forward (bound 6).

**The drift exposed a defect in this seat's own arm (iii), now fixed.** The first shipped predicate took the
**last** `strict pass=` line at/after `:813` as the citation under test. On the drifted file that line is now
`:875`, a C1 move-log row (`| C1 | depth:verifiability …`), not the erratum's citation at `:852` — so:
(a) an unrelated row quoting the audit could mask a correct label appended earlier (a false red), and
(b) the arm's subject was chosen by file position rather than by content.

```
$ k=$(awk 'NR>=813 && /strict pass=/ {m=NR} END{print m+0}' SCORECARD.md); echo "k=$k"
k=875
$ awk -v k="$k" 'NR>=k-2 && NR<=k' SCORECARD.md | grep -o '3fc0d751\|5d4842da' | sort -u
(no output: neither the cited nor the live instrument digest appears in the window)
```

Fix: the predicate now scans **every** `strict pass=` window at/after `:813` and closes on any window that
carries the live value, the live 8-hex instrument digest **and** the filed address; R18's arm (iii) says "a
`strict pass=` reading", not "the last". Re-measured over 13 byte-states (scratch rebuilt from the drifted
bytes; `sc.md` = `4076091c…`, `sc-base.md` = `cac64dbd…`):

| byte-state | exit | decisive field |
|---|---|---|
| landed `4076091c…` | 1 | `live_citation_self_naming=0` |
| `m1` filed span deleted | 1 | `filed_byte_identical=n` |
| `m2` `exit=1`→`exit=0` reword | 1 | `filed_byte_identical=n` |
| `m3` erratum block removed | 1 | `anchor=none` |
| `m4` unrelated r31 erratum, both phrases | 1 | `naming_erratum=0` |
| `m5` paragraph+phrase removed | 1 | `phrases=0` |
| `sc-forge` fabricated live-pair line | 1 | `live_citation_self_naming=0` |
| `sc-base` `cac64dbd…` | 1 | `naming_erratum=0` |
| label, wrong digest | 1 | `live_citation_self_naming=0` |
| label, stale value | 1 | `live_citation_self_naming=0` |
| label (`sc-relabel`) | **0** | `live_citation_self_naming=1` |
| label **then** an unrelated later row quoting the audit | **0** | the §8 false-red case, now green |
| label then a later forged window | **0** | genuine closure stands |

All eleven verdicts of §2.2 are unchanged by the fix; the two new states are the drift cases it exists for.
`corpus/QUALITY.md` under this seat's single-writer tenure, digest transitions (each cause named, none silent):

| sha256 | state |
|---|---|
| `96b71caa…` | pre-append (R18/R19 absent) |
| `5899e02b…` | after the R18/R19 append of §4 (157 lines) |
| `5c2903ff…` | after the §8 window fix (`for k … done`, 158 lines) |
| `300f9962e3017ca0846038d193cfe83f674989dccf78d4488caa59e578badaba` | after the R18 row gained the "re-measured on drifted `4076091c…`, 13 byte-states, §8" clause (158 lines, final) |

Final state: 158 lines, append-only vs `96b71caa…` (`git diff -U0 | grep -c '^-[^-]'` → 0); R13 `:77`, R16
`:95`, R17 `:96`, R18 `:102`, R19 `:103` held; blocks `:110-133`, `:137-144`, `:148-158`; all three `bash -n`
clean, and on landed bytes CHECK A' exits 1 (`live_citation_self_naming=0`), CHECK B' exits 0
(`round30_h2_headings=1`), R19 exits 0 (`supersedes_r13_rows=1`).
The qualification in §0 of `MutErratumCheck.md` about the boost-spec `5fa41aef…` era does not transfer to
this seat's verdicts: the tightened check is digest-bound and re-measured on `4076091c…`.

Scratch (second round) removed:

```
$ ls -d /tmp/tmp.8NUPEIqH9o /tmp/tmp.gg30Lap0hz /tmp/tmp.HxvcoJUvfz /tmp/tmp.0dNUwAe6XR
/tmp/tmp.0dNUwAe6XR
/tmp/tmp.8NUPEIqH9o
/tmp/tmp.HxvcoJUvfz
/tmp/tmp.gg30Lap0hz
$ rm -rf /tmp/tmp.8NUPEIqH9o /tmp/tmp.gg30Lap0hz /tmp/tmp.HxvcoJUvfz /tmp/tmp.0dNUwAe6XR /tmp/sqf-t \
    /tmp/sqf-t2 /tmp/sqf-t3 /tmp/sqf-d2 /tmp/sqf-x.txt && echo cleaned
cleaned
$ ls -d /tmp/tmp.8NUPEIqH9o /tmp/tmp.gg30Lap0hz /tmp/tmp.HxvcoJUvfz /tmp/tmp.0dNUwAe6XR
ls: cannot access '/tmp/tmp.8NUPEIqH9o': No such file or directory
ls: cannot access '/tmp/tmp.gg30Lap0hz': No such file or directory
ls: cannot access '/tmp/tmp.HxvcoJUvfz': No such file or directory
ls: cannot access '/tmp/tmp.0dNUwAe6XR': No such file or directory
```
