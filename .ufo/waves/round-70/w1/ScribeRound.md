# Round 70 — ScribeRound (w1): lesson draft evidence for the L1

Seat: ScribeRound (scribe, leaf, no subagent). Lane `kasegi-shokunin`. Frozen claims `e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`
(pins `controls/pins-r70.txt`, unchanged since freeze). C1 implementation `c1051749571caf6a0383b15187fc02cdd21785b5`
(gate sha256 `7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5`). C2 landing `b4afd8a0206b23a69d8cd65d92070cdfcd4680a7`.
Lane HEAD observed at the end of this seat: `master = afcced409abc151e9a45995491bc6900ae9b39ff` (the L1 kept committing after
my first read; every claim below names the commit it was read at).

Scope kept: no lane file edited, no git/jj mutation, no commit. Reads were `git show`, `git archive` into scratch, `grep`, `sha256sum`,
`wc`, a `curl` GET of the EUVD page and two runs of the lane's own `capture-binding-check.py` on a scratch fixture. Scratch
`/fast/scratch/hyaku/kasegi-r70/ScribeRound/` removed before yield.

Disclosures:
- One `jj --at-op … file show` call ran without `--ignore-working-copy` (early, exploratory). jj may have appended a working-copy
  snapshot operation to the lane's op log. All later jj calls used `--ignore-working-copy`. I did not verify whether an op was added.
- Tool installs/upgrades: none. Used the host's `git`, `python3`, `jj` (read-only), `curl`, `sha256sum`, `grep`.

---

## 0. Bottom line for the L1

1. **The HEAD lesson (`afcced4`, `corpus/lessons/round-70.md`) omits the strongest defect of the round.** The freeze commit
   `e74ba6b5` pins `controls/c1-forgery-blanket-r70.txt` at sha256 `d74ba3f9…` (pins line 9), but the blob that commit
   carries is 915 bytes / 10 lines, sha256 `fdbcc484…`. The 14-line file with `d74ba3f9…` (1226 bytes, carrying the `VERIFY … mode=forgery`
   line) first appears in a later commit `7f6e39a9`. The pinned control was rewritten after its pin. R97 forbids this and R98 is the
   check that should have caught it at freeze. Section 2, row A.
2. **M70-1 (README) is wrong as written.** The committed `e7c02bd..b4afd8a0` README diff contains exactly one removed line, the
   old F47 row, which is re-added with one changed clause in its `next` cell. The diff does not show "no deletion of F47" as
   the lesson states. The intermediate "deleted row" state is not recoverable from the jj op log (no snapshot between 21:02:05 and
   21:19:35). Section 2, row B.
3. **S105 gate quote miscounted.** The lesson gives its quote as 18 words; `S105.txt:601` is 17 words (exact match, checked).
4. **S104 has no located quote.** The static EUVD body is one line (0 newline bytes) whose only text token is `<title>Vulnerability Database</title>`
   at byte 627. The rejection's ground is a measured absence, not a line. Section 1.
5. **M70-2 (snapshot dir before manifest) is not in any committed or scratch byte.** The instrument rule does print the exact
   line on a fixture (Section 2, row C), so the capability is verified; the historic occurrence is attested only by the lesson text.
6. **Trend verdicts:** expansion `improved`; quality `unchanged` (the HEAD lesson says `improved`; the LEARNING.md quality row is
   about entries, and no entry was re-verified or superseded); discernment `improved`, grounded in R107/R108 from non-author
   seats, with the un-recorded pin defect in item 1 as the caveat. Section 3.

---

## 1. `## Gate` block — the two new rows

Row order and column names follow the HEAD lesson's `## Gate — the two rows written this round` table.

| row | URL | access date | located quote (≤25 words) | teaches-cell ground |
|---|---|---|---|---|
| S104 (rejected) | https://euvd.enisa.europa.eu/apidoc | 2026-11-05 (lane re-fetch; my live GET 2026-11-05 UTC reproduces it: HTTP 200, 3062 bytes, sha256 `6fb32b61a3f44c7aa137699de08cf3a240aab7315f0d68ec7012e69d0a0a38d5`) | **none exists.** The static body has 0 newline bytes (one line), 0 occurrences of `endpoint` and 0 of `/api/`; its only text token is `<title>Vulnerability Database</title>` (byte 627). Grounded by absence, not by a quote. | `REJECTED: the served HTML is an SPA shell with no documentation text` — the measured absence is the ground; receipt `.ufo/waves/round-69/controls/euvd-refusal-r69.txt` (`static_html_bytes=3062`, `static_html_has_endpoint_text=0`). |
| S105 (mined, tier A) | https://docs.github.com/en/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database | 2026-11-05T00:14:43Z (`manifest.json` `fetched_utc`; capture sha256 `9dd51a8e…e3350`, 656 lines, 22791 bytes) | "Unreviewed advisories are published automatically into the GitHub Advisory Database, directly from the National Vulnerability Database feed." — `S105.txt:601`, **17 words** (exact match against the committed snapshot) | The `teaches` cell's first cited item is `S105.txt:602`: "Dependabot doesn't create Dependabot alerts for unreviewed advisories as this type of advisory isn't checked for validity or completion." (19 words; exact). Use 602 if the L1 wants the cell's own clause; 601 grounds the class. |

Other located lines the `teaches` cell cites, verified exact against `S105.txt`: `:571` (malware carries no fix version: "Malware alerts do not contain a fix version …", 23 words), `:639` (EPSS percentiles "will only be updated when significantly different", inside a 30-word sentence). Only the 25-word limit matters for the lesson table.

---

## 2. `## Mistakes` candidates for this round

Each row: class · evidence pointer · captured-by (criterion / rule id) · fix. Pointers are commits or committed paths unless marked
scratch (not a committed byte).

### A. Pinned control rewritten after its pin; freeze commit does not contain the pinned bytes (NOT in the HEAD lesson)

- **Class:** pinned-control edit after pin; evidence-integrity at freeze.
- **Evidence:**
  - `git show e74ba6b5:.ufo/waves/round-70/controls/pins-r70.txt` line 9: `d74ba3f9c61aa293728ccb59230328c656aa424bb773a4d01640f0b500bc0a0b  .ufo/waves/round-70/controls/c1-forgery-blanket-r70.txt`.
  - `git cat-file -s` of that path at `e74ba6b5` = **915 bytes**, `sha256sum` `fdbcc4847464…`, 10 lines (ends `MEASURE selftest FAIL selftest cases=86 failures=47 rc=1`). No `VERIFY` line.
  - Same path at `7f6e39a9` / `master` = **1226 bytes**, `sha256sum` `d74ba3f9c61a…`, 14 lines, ends `VERIFY measurements=12 failures=4 gate_sha256=126de75d… mode=forgery`. `git log --format='%h %s' -- <path>` lists only `15d4da8` and `7f6e39a` (the freeze did not touch the blob).
  - The jj op log has snapshot `8664a17d5e94` (21:19:41.229) with the file at 10 lines / 915 bytes and snapshot `17988bc1c294` (21:19:56.151) with it at 14 lines / 1226 bytes. The four lines were added in that 15-second window, i.e. inside the freeze window, after the pre-freeze commit `15d4da8` (21:19:41) and before the freeze commit `e74ba6b5` (21:19:56) was exported. The git freeze commit did not receive the four lines; the pin did.
  - The jj commit that the op log records as the freeze (`300b18b2d626…`, op at 21:19:56.274) carries the 14-line file (`d74ba3f9`), while git `e74ba6b5` carries the 10-line file. The jj-to-git export of the freeze did not carry the bytes the freeze pinned. The mechanism is not visible from the bytes; the divergence is.
  - Receipt truncation: the 10-line committed copy stops before the counter's last four lines (`mutbat`, `real-ledger`, `no-write-side-effect`, `VERIFY`). A run whose tail was printed to the terminal and appended later matches this shape; the bytes cannot show whether that happened (scratch: none).
  - At HEAD (`afcced4`) the pin matches (`d74ba3f9`), so the pin is now consistent with the file, but only because the file was rewritten after the freeze.
  - Claims exposure: `controls/c1-forgery-blanket-r70.txt` is cited in `claims.json` (`blanket_refusal_forgery`) as "positive controls fail, exit 1". At the freeze commit that file shows no exit line and no VERIFY line.
- **Captured-by:** R97 (a pinned control has exactly one writer; post-pin edits are reverted and recorded — not reverted here, not recorded in the lesson); R98 (every digest in a frozen record is recomputed from the committed bytes at freeze — this check fails at `e74ba6b5`); R99 (a final measurement is written to its receipt by the same command that runs it — the 10-line file is not that).
- **Fix:** the lesson records it as an erratum row. Either revert `7f6e39a9`'s rewrite and keep the 10-line file as the pinned bytes (then the pin is wrong and an erratum must name it), or record that the pin named bytes absent from the freeze commit. Add an R98 check to the freeze step: `git show <freeze>:<path> | sha256sum` must equal each pin line before the freeze commit is accepted. Do not edit `pins-r70.txt` (frozen).

### B. README F47 row "deleted then restored" (HEAD M70-1): the stated evidence is wrong

- **Class:** record-integrity, edit-shape (as the lesson names it). The lesson's *evidence sentence* is the defect.
- **Evidence (committed):** `git diff e7c02bd b4afd8a0 --numstat -- corpus/README.md` → `11 1 corpus/README.md`. The one removed line is the old F47 row; the re-added F47 row differs only in its `next` cell (`…are unopened and are not ground here.` → `…are held by F48/S105.`). Hunk header `@@ -1084,4 +1084,14 @@`. F-row count `grep -cE '^\| F[0-9]+ \|'`: base `e7c02bd` = **47**, landing `b4afd8a0` = **48**, HEAD `afcced4` = **48**. ReviewC2 row 9 (`w1/ReviewC2.md` §10): "F47 altered only in the one recorded next-cell clause — VERIFIED".
- **Evidence (intermediate state):** the jj op log has no snapshot between `87f737239a64` (21:02:05.260, F47 only) and `6863d3bda47d` (21:19:35.933, F47 + F48). The intermediate state, whether or not F47 was deleted in it, is not recoverable from the op log. The lesson's "intermediate working-tree state was a deleted row" is therefore an unevidenced assertion (scratch: the jj probes; no committed byte).
- **Captured-by:** R104 (row count before+1) — **passes** at landing (47→48). R104 would not have caught an edited-in-place F47 clause; the diff review did.
- **Fix:** rewrite M70-1 as: the F48 edit rewrote the F47 `next` cell in the same hunk; the committed diff shows one removed and one added F47 line (one clause changed); the row count is 47→48. Drop the "deleted row" intermediate claim unless a dated receipt is produced. Keep R104.

### C. Snapshot directory created before its manifest (HEAD M70-2): capability verified, incident unattested

- **Class:** capture-binding order (R105).
- **Evidence (committed):** the base receipt `controls/c2-base-counters-r70.txt` (at `15d4da8`) shows `records=83 … snapshot_dirs=42 manifest_dirs=42 missing_manifest=0` and no `FAIL` line. My re-run on `git archive e7c02bd corpus` (scratch `base/`) prints exactly the same `AUDIT` line (`snapshot_dirs=42 manifest_dirs=42 missing_manifest=0 … orphan=S040-live.txt`) and `records=83 bound=83 unbound=0`.
- **Fixture (scratch, reproducible):** `base/` plus `corpus/source-snapshots/round-70/S105.txt` only (copied from `b4afd8a0`, no manifest) → `capture-binding-check.py --root <fixture>` prints `AUDIT … snapshot_dirs=43 manifest_dirs=42 missing_manifest=1` and **`FAIL rule=missing-manifest dir=round-70`**, exactly the string in the lesson.
- **Incident evidence:** `grep -rn "missing-manifest dir=round-70"` over the lane tree, `.ufo/`, the fleet root and `/fast/scratch/hyaku/kasegi-r70/` returns **no hit**. The "polluted" base receipt is not a committed or scratch byte. Note the committed base receipt's header says the base is `e7c02bd`, which does not contain `round-70/` at all, so a base measurement could not have been polluted by that directory; only a working-tree measurement could.
- **Captured-by:** capture-binding-check rule A (verified above). Whether the incident happened as described is not evidenced.
- **Fix:** keep R105. Reword M70-2 as "rule A catches a tracked directory with no manifest (fixture-verified); the round's own occurrence is not in the committed bytes". Record the base receipt's header as the authoritative base.

### D. `git archive` is not a committed-input closure (HEAD M70-3): verified

- **Class:** input-closure (R34/R65/R106).
- **Evidence (committed, master):** `controls/final-verification-r70-archive-export-failed.txt` → `MEASURE real-ledger FAIL FIGURE-AUDIT figures=35 ok=11 stale=24 exit=1 rc=1` and `VERIFY measurements=12 failures=1 … mode=candidate`. `controls/final-verification-r70.txt` → `MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` and `VERIFY measurements=12 failures=0 … mode=candidate`, with the NOTE line naming the clone closure.
- **Captured-by:** R106 (as the lesson says) with R34/R65 as the prior rule. Verified.
- **Fix:** as the lesson has it.

### E. Frozen C2 after-receipt overwritten (HEAD M70-5): verified; the detector was the pin

- **Class:** evidence-integrity (R107).
- **Evidence:** at freeze `e74ba6b5`, `controls/c2-after-counters-r70.txt` = sha256 `f20fd6e7…` (pin). At `7f6e39a9` the file starts `# C2 after counters on committed landing b4afd8a0… (shared clone)`, sha `338d4f44…`; restored at `ede38bf` (`git show ede38bf --stat`: the file and a new `c2-after-counters-r70-clone.txt`). HEAD sha `f20fd6e7…` = pin (`pins-r70.txt` check, Section 4).
- **Captured-by:** `pins-r70.txt` (the pin detected it once `ExecCountersC2` re-hashed the file, `w1/ExecCountersC2.md`).
- **Fix:** as the lesson has it, R107.

### F. Selftest pin strength (HEAD M70-6 / V70-1): verified

- **Evidence:** `w1/ExecR103.md` and `w1/MutationC1.md` (both untracked, see Section 5); MutationC1 line 176: "13/22 mutants killed, 9 survived; the 7 survivors that were run through the frozen 12-measurement counter" — the frozen counter has no probe for `--scratch`, `--work`, `--url`-only, short `-o` or `--=…`.
- **Captured-by:** R103 (partly met; the lesson states it).
- **Fix:** V70-1 as the lesson has it. Do not edit the selftest after measurement.

### G. Entry prose outran its source (HEAD M70-7): verified; a pre-landing defect

- **Evidence:** `w1/CriticC2.md` § Verdict: "5 wrong/misquoted statements and 6 unsupported generalizations" (the critic's own numbers; it lists O1–O21). The landed entry `b4afd8a0:corpus/knowledge/github-advisory-database-curation-semantics.md` (blob `d479c495…`, the pinned digest) differs from HEAD (`0775d2a4…`) after `97eda97`.
- **Captured-by:** R108 (new, in HEAD `QUALITY.md`); the critic seat is the outside check.
- **Fix:** as HEAD has it, plus item H below.

### H. Pinned knowledge entry edited after freeze, recorded but not reverted (NOT in the HEAD lesson as a Mistake)

- **Class:** pinned-control edit (R97).
- **Evidence:** `pins-r70.txt` line 13 (`d479c495…  corpus/knowledge/github-advisory-database-curation-semantics.md`); HEAD sha `0775d2a4…`. The erratum `controls/pins-r70-erratum-1.txt` says "Frozen pins … stay byte-identical and are NOT edited" — true of the pins *file*, not of the pinned *artifact*. The same erratum records the old→new digests, which is the R97 "recorded" half; R97's "reverted" half is not done.
- **Captured-by:** R97.
- **Fix:** state in the lesson that the pinned entry changed after freeze, by erratum 1, and that R97's revert clause was not applied (a revert would reintroduce the 21 outruns). Make the erratum sentence say "the pins file is unchanged; the pinned knowledge entry is not (`d479c495` → `0775d2a4`)".

### I. S105 gate word count (new; same class as HEAD M70-4)

- **Class:** prose count drift.
- **Evidence:** the lesson's Gate row says "18 words" for `S105.txt:601`; `len(line.split())` = 17 and the manifest's `Q07-unreviewed-auto` is 17 words.
- **Captured-by:** M70-4's own fix (derive the count from the manifest, never type it). Not applied to the gate row.
- **Fix:** write 17 or drop the count.

---

## 3. Trend verdicts (lane format: LEARNING.md)

LEARNING.md defines: expansion = admitted entries on uncovered ground citing a mined row; quality = entries re-verified, deepened,
or superseded; discernment = gate decisions vs the outside spot-check, or a disagreement that becomes a grounded `QUALITY.md` criterion.

**expansion — improved.**
- Frontier rows `grep -cE '^\| F[0-9]+ \|' corpus/README.md`: `e7c02bd` 47 → `b4afd8a0` 48 (F48 on S105).
- Knowledge files `git ls-tree -r --name-only <rev> corpus/knowledge/ | grep -c '\.md$'`: 85 → 86.
- Registry rows `grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md`: 103 → 105 (S105 mined + S104 rejected; R102 `105 − 103 = 2 = admitted 1 + rejected 1`).
- Condition: the landed entry (`b4afd8a0`) carried the outruns the critic found (item G); the admitted entry at HEAD is the corrected one (`97eda97`). State that in the verdict.

**quality — unchanged.** LEARNING.md's quality row counts entries re-verified, deepened or superseded. No pre-existing entry was touched:
the F47 entry is unchanged (only the README `next` cell of F47 changed, Section 2 B); the F48 entry is new, so its correction (`97eda97`,
R108) is an erratum to a new entry. The gate's refusal of seven shapes is an instrument gain. The lane is inconsistent on this:
`round-67.md` line 119–121 says "quality unchanged … the instrument repair is a gate correction"; `round-69.md` says "quality improved" on
gate refusals. HEAD `round-70.md` says "improved". Recommend `unchanged`, and that the L1 pick one reading and name it.

**discernment — improved (with a caveat).** Grounds: R107 (from `ExecCountersC2`, a non-author seat) and R108 (from `CriticC2`, a non-author seat, 21 outruns) are
criteria grounded in outside disagreements (LEARNING.md's improved condition). `ReviewC2` and `ReviewerC1` (non-author) reproduced the frozen
predicates; `MutationC1` and `ExecR103` found the limb-isolation gap (V70-1). Caveat: the freeze-time pin defect (item A, the pin named
bytes absent from the freeze commit) was caught by no seat and is not in the lesson. Its absence keeps this verdict below "improved
without reservation". Recommend the L1 add item A as a Mistake with R97/R98 as captured-by, which then supports `improved`.

---

## 4. Corrections the L1 needs to make to the HEAD lesson (`afcced4`)

1. Add the item-A Mistake (forgery pin named bytes absent from the freeze commit; post-freeze rewrite; R97/R98/R99). Name the 915/1226-byte
   and 10/14-line states and the commits `15d4da8`, `e74ba6b5`, `7f6e39a9`.
2. Rewrite M70-1 (Section 2 B). Delete "no deletion of F47" and "intermediate … was a deleted row" unless a dated receipt exists.
3. Rewrite M70-2 (Section 2 C): verified capability, unattested incident.
4. S105 gate row: "18 words" → 17 (or drop the count).
5. S104 gate row: say "no located quote exists; ground is the measured absence" and cite the `<title>` at byte 627 only if the L1 wants a token.
6. Erratum 1 (`controls/pins-r70-erratum-1.txt`): add that the pinned knowledge entry changed (`d479c495` → `0775d2a4`); the pins file did not.
7. Trends: quality `improved` → `unchanged` (or name the reading); discernment: add item A before scoring it improved.
8. The HEAD "Corrections" section and the trend text cite R104–R108; R104 passes at landing and R105/R106 stand.

---

## 5. Commands run (paste-able, read-only) and their output

```
git rev-parse master                                   -> afcced409abc151e9a45995491bc6900ae9b39ff
git show e74ba6b5:.ufo/waves/round-70/controls/pins-r70.txt | grep forgery-blanket
  -> d74ba3f9c61aa293728ccb59230328c656aa424bb773a4d01640f0b500bc0a0b  .ufo/waves/round-70/controls/c1-forgery-blanket-r70.txt
git cat-file -s $(git rev-parse e74ba6b5:<forgery>)     -> 915
git cat-file -s $(git rev-parse master:<forgery>)       -> 1226
git show e74ba6b5:<forgery> | sha256sum                 -> fdbcc4847464b1c1155adeeb8e096e4958597cd586aff37f64102e4a56288da4
git show master:<forgery>   | sha256sum                 -> d74ba3f9c61aa293728ccb59230328c656aa424bb773a4d01640f0b500bc0a0b
git log --format='%h %s' -- <forgery>                  -> 7f6e39a9 …; 15d4da8 …      (e74ba6b5 not listed)
jj --ignore-working-copy --at-op 8664a17d5e94 file show <forgery> | wc -l  -> 10 (915 bytes)
jj --ignore-working-copy --at-op 17988bc1c294 file show <forgery> | wc -l  -> 14 (1226 bytes)

git diff e7c02bd b4afd8a0 --numstat -- corpus/README.md  -> 11 1 corpus/README.md
grep -cE '^\| F[0-9]+ \|' (e7c02bd README) = 47 ; (b4afd8a0 README) = 48 ; (afcced4) = 48
git diff e7c02bd b4afd8a0 -- corpus/README.md | grep -nE '^[-+]\| F4'  -> one '-' F47 line, '+' F47 line, '+' F48 line

python3 -c "...S105.txt line 601..." -> words 17 ; exact match with the lesson's quote: True
python3 -c "...S105.txt line 602..." -> words 19

curl -sS https://euvd.enisa.europa.eu/apidoc -o euvd-live.html -w '%{http_code} %{size_download}'
  -> 200 3062 ; sha256 6fb32b61a3f44c7aa137699de08cf3a240aab7315f0d68ec7012e69d0a0a38d5
  -> newlines 0 ; 'endpoint' 0 ; '/api/' 0 ; <title>Vulnerability Database</title> at byte 627

git archive e7c02bddaa32a4a70afb2e6278f108e03dca067c corpus | tar -x -C <scratch>/base
  python3 corpus/instruments/capture-binding-check.py --root <scratch>/base
  -> AUDIT records=83 … snapshot_dirs=42 manifest_dirs=42 missing_manifest=0 … orphan=S040-live.txt
     records=83 bound=83 unbound=0                     (matches controls/c2-base-counters-r70.txt)
fixture = base + corpus/source-snapshots/round-70/S105.txt (no manifest)
  -> AUDIT … snapshot_dirs=43 manifest_dirs=42 missing_manifest=1
     FAIL rule=missing-manifest dir=round-70

grep -rn 'missing-manifest dir=round-70' <lane> <.ufo> <fleet root> <scratch>  -> no hit

git show master:.ufo/waves/round-70/controls/c2-after-counters-r70.txt | sha256sum -> f20fd6e72e1f… (= pin)
git show 7f6e39a9:<c2-after> | sha256sum                                     -> 338d4f441ed8… (post-freeze rewrite)
pins vs HEAD (11 lines): 10 OK, 1 MISMATCH: corpus/knowledge/github-advisory-database-curation-semantics.md (d479c495 pin / 0775d2a4 HEAD)
```

Tip-of-lane observation: `master` moved from `7f6e39a9` (first read) to `afcced4` (end) through `ede38bf`, `97eda97`, `afcced4`. Every
quoted hash above names its commit.

---

## 6. Limits and residuals (named, not claimed)

- The mechanism of the jj/git divergence at the freeze (item A) is not visible from the bytes. I state the divergence, not a cause.
- The intermediate README state (item B) and the historic missing-manifest occurrence (item C) are not recoverable from committed bytes or scratch. They are attested by the lesson text only.
- `w1/` seat reports (`CriticC2.md`, `ReviewC2.md`, `ReviewerC1.md`, `MutationC1.md`, `SentinelGate.md`, `ExecR103.md`, `ExecCountersC2.md`, `ScopeF48.md`) are **untracked** in the lane tree at the time of reading. Their verdicts are cited as evidence for Section 3 but are not in any commit; the L1 should commit them or cite them as untracked.
- The S104 live GET reproduces the round-69 digest today; the lane's SOURCES row and this seat agree. No other live re-fetch was done; S105's quotes were checked against the committed snapshot only.
- I did not run the lane's gates, census or counters. The C1/C2 numbers above are the committed receipts' numbers, read, not re-measured by this seat, except the one fixture run of `capture-binding-check.py` and the base-tree AUDIT line.
- Nothing in this report edits, or proposes editing, a frozen pinned byte. The erratum and revert questions (items A, H) are for the L1 and the operator.
