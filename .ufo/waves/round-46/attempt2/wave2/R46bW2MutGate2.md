VERDICT: HOLDS

Scope: independent mutation pass on the frozen `corpus/instruments/r46-f29-gate.py` v1 (sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`, matches `freeze.txt` line 5), limbs H4/H5/H6 (capture pin, entry citations, knowledge directory). 48 own mutants: 36 KILLED, 12 SURVIVED. Every survivor is equivalent under a stated pin or conjunction argument; none is a live gap in H4/H5/H6 as written. One v1 hole (core quote inside a mid-line HTML comment counted as live) was confirmed; it is already logged as errata E4 and closed in v1.1 (the gate at the wave-1 integration, sha256 `5d192dfd…`).

## 1. Trees and baselines (re-run, not trusted)

- Frozen gate bytes: copied from `git show fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4:corpus/instruments/r46-f29-gate.py` into scratch; sha256 `a1091e24…` confirmed.
- Working-tree gate is v1.1 (sha256 `5d192dfd…`, commit 96379ae). H4 and H6 and the H5 body are textually identical between v1 and v1.1; the H5-relevant difference is `live_lines` (see F1).
- Do-nothing controls, unmutated v1:
  - freeze `fe0f56b` export: `gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0`, `gate H5 pass=0 read=entry-absent advisor-named=`, `gate H6 pass=0 read=entry-absent advisor-named=`, `f29-gate fixed=2/7 exit=1` (matches claims `freeze_tree_reading`).
  - base `04af9bc` export: `gate H4 pass=0 read=manifest-absent`, `f29-gate fixed=1/7 exit=1` (matches `controls/f29-gate-at-base.txt`).
  - wave-1 tree `96379ae` (entry present): v1 reads `gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0`, `gate H5 pass=1 read=spans=45 located=45 failed=0 uncited=0 cores=5/5`, `gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0`, `f29-gate fixed=7/7 exit=0`. This is the positive fixture.
- The freeze tree has no entry, so H5/H6 can only be exercised on fixtures built from `96379ae`.

## 2. Method

- 38 fixtures, built under scratch from the `96379ae` corpus with one edit each: positive `P`; `P_stub` (recheck replaced by a tampered stub that prints nine OK lines); `freeze_fe0f56b` and `base_04af9bc` as controls; entry edits for each boundary (cite at line 1, cite 42-43, span 11 and 12 lines, 25 and 26 word quotes, unmatched quote, empty quote, curly apostrophe, wrapped quote, single-curly and ASCII quotes, unparenthesised cite, uncited quote in a comment, core quote in a line comment and in a mid-line comment, one-word quote `“GitHub”`, five-quote minimal entry, 2000-byte entry); corpus edits (67 entries, nested `.md`, ledger grown / truncated to 30695 and 1000 bytes / replaced by 40 KB text, base file edited, mission ledger renamed or symlinked, manifest with trailing blank lines, snapshot line 9 altered).
- Each mutant is one exact-once substring replacement (count asserted == 1) applied to a scratch copy of the frozen gate. Only the mutant's own limb (`h4`/`h5`/`h6` function) is run, on every fixture, under the matching instrument variant (real or stub `source-recheck.py`).
- A mutant is KILLED when its pass bit differs from the unmutated v1 limb on any fixture; SURVIVED otherwise. Read-string differences were recorded but do not count.
- Three full runs. Run 1 had a fixture bug (wrapped core-5 quotes were not stripped, so `nocore5` still read 5/5), fixed in run 2; run 3 added `snap_tamper` and `trivial_quote`. The table below is run 3 (`48` mutant lines, 0 anchor-count errors, 0 compile errors).

## 3. Mutant table (old → new substring; killers = fixtures whose pass bit flips)

| id | limb | old → new | verdict | killers / note |
|---|---|---|---|---|
| H4-01 | H4 | `oks >= 8` → `oks >= 1` | SURVIVED | equivalent under pin (§4) |
| H4-02 | H4 | `oks >= 8` → `oks >= 10` | KILLED | P, freeze, nocore5, core5_linecomment, core5_midline, uncited_comment |
| H4-03 | H4 | `anchor >= 7` → `anchor >= 9` | KILLED | same set; pinned manifest has 8 distinct anchors |
| H4-04 | H4 | drop `== oks` from `distinct` | SURVIVED | equivalent under pin |
| H4-05 | H4 | drop `"BROKEN" not in out and` | SURVIVED | equivalent under pin |
| H4-06 | H4 | drop `rc == 0 and` | SURVIVED | equivalent under pin (snap_tamper: still red via sha MISMATCH) |
| H4-07 | H4 | drop `and not miss` | SURVIVED | equivalent under pin |
| H4-08 | H4 | drop `"S074:sha256 OK" in out and` | SURVIVED | equivalent under pin |
| H4-09 | H4 | manifest pin → `if False:` | KILLED | manifest_ws |
| H4-10 | H4 | recheck pin → `if False:` | KILLED | P_stub (tampered recheck goes green) |
| H4-11 | H4 | `miss = [...]` → `miss = []` | SURVIVED | equivalent under pin |
| H5-01 | H5 | window `a - 1` → `a - 2` | KILLED | wstart_minus |
| H5-02 | H5 | window `a - 1` → `a` | KILLED | P, core5_midline, span11, w25, bodylo, apos |
| H5-03 | H5 | window `b` → `b + 1` | KILLED | wend |
| H5-04 | H5 | `b - a <= 11` → `<= 12` | KILLED | span12 |
| H5-05 | H5 | `b - a <= 11` → `<= 10` | KILLED | span11 |
| H5-06 | H5 | words `<= 25` → `<= 24` | KILLED | w25 |
| H5-07 | H5 | words `<= 25` → `<= 26` | KILLED | w26 |
| H5-08 | H5 | `b <= BODY[1]` → `+ 1` | KILLED | bodyhi |
| H5-09 | H5 | `a >= BODY[0]` → `+ 1` | KILLED | bodylo |
| H5-10 | H5 | `failed == 0` → `failed <= 1` | KILLED | wend, wstart_minus, span12, w26, bodyhi, failone |
| H5-11 | H5 | `uncited <= 0` → `<= 1` | KILLED | uncited_comment, uncited, single, ascii, cite_noparen |
| H5-12 | H5 | drop `nq and` empty-quote guard | KILLED | emptyq |
| H5-13 | H5 | `nq = norm(q)` → `nq = q` | KILLED | P, core5_midline, span11, w25, bodylo, apos |
| H5-14 | H5 | `re.sub(r"\s+", …)` → `r" +"` | KILLED | P, core5_midline, span11, w25, bodylo, apos |
| H5-15 | H5 | `len(cores) == len(CORES)` → `>= 4` | KILLED | nocore5, core5_linecomment |
| H5-16 | H5 | drop `if q in live_spans` | KILLED | core5_linecomment |
| H5-17 | H5 | `live` → `raw` in `live_spans` | KILLED | core5_linecomment |
| H5-18 | H5 | `quoted` from `live` not `raw` | KILLED | uncited_comment |
| H5-19 | H5 | drop single-curly quoted set | KILLED | single |
| H5-20 | H5 | drop ASCII-quoted set | KILLED | ascii |
| H5-21 | H5 | cite `\s*\(` → `\s*\(?` | KILLED | cite_noparen |
| H5-22 | H5 | cite `(?:-(\d+))?` → `-(\d+)` | KILLED | P, core5_midline, span11, w25, bodylo, apos (single-line cites) |
| H5-23 | H5 | cite `(\d+)` → `(\d)` | KILLED | P, core5_midline, span11, w25, bodylo, apos (two-digit cites) |
| H5-24 | H5 | `b = int(b) if b else a` → `if b is not None` | KILLED | limb-error=ValueError on single-line cites (see F5) |
| H5-25 | H5 | `len(passed) >= 4` → `>= 6` | KILLED | five (exactly 5 located) |
| H5-26 | H5 | `len(passed) >= 4` → `>= 2` | SURVIVED | equivalent under cover argument (§4) |
| H5-27 | H5 | `len(passed) >= 4` → `>= 5` | SURVIVED | equivalent under cover argument (§4) |
| H5-28 | H5 | `out.append(ln)` → strip `<!--…-->` (v1.1 fix) | KILLED | core5_midline (v1 green → red) |
| H6-01 | H6 | `len(names) == 66` → `>= 66` | SURVIVED | equivalent: names ⊆ everything (§4) |
| H6-02 | H6 | drop `nested == 66` | SURVIVED | equivalent under names = everything = 66 (§4) |
| H6-03 | H6 | drop content pin | KILLED | basecontent |
| H6-04 | H6 | drop names pin | SURVIVED | equivalent: content pin encodes names (§4) |
| H6-05 | H6 | ledger included in content pin | KILLED | P (positive turns red), nocore5, core5_*, uncited_comment, wend |
| H6-06 | H6 | ledger floor `>= N` → `>= N - 1` | KILLED | ledger30695 |
| H6-07 | H6 | ledger floor dropped | KILLED | ledger30695, ledger_small |
| H6-08 | H6 | entry size floor `>= 3000` → `>= 1` | KILLED | smallentry, five |
| H6-09 | H6 | drop `not links` | KILLED | symlink |

Totals: 48 mutants, 36 KILLED, 12 SURVIVED (H4: 7 of 11 survive; H5: 2 of 28; H6: 3 of 9).

Unmutated v1 verdicts that carry the kills (exact outputs):
- `P`: `h4=1(recheck-rc=0 quotes-ok=9 frozen-cores-missing=0) h5=1(spans=45 located=45 failed=0 uncited=0 cores=5/5) h6=1(knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0)`
- `nocore5`: `h5=0(spans=41 located=41 failed=0 uncited=0 cores=4/5)`
- `core5_linecomment`: `h5=0(spans=42 located=42 failed=0 uncited=0 cores=4/5)`
- `core5_midline`: `h5=1(spans=42 located=42 failed=0 uncited=0 cores=5/5)` (F1)
- `wend`: `h5=0(spans=46 located=45 failed=1 uncited=0 cores=5/5)`
- `five`: `h5=1(spans=5 located=5 failed=0 uncited=0 cores=5/5)`
- `ledger30695`: `h6=0(knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1 symlinks=0)`; `ledger_grow`: `h6=1` (exemption works)
- `manifest_ws`: `h4=0(manifest-not-the-pinned-bytes)`; `P_stub`: `h4=0(source-recheck-not-the-pinned-bytes)`
- `snap_tamper`: `h4=0(recheck-rc=1 quotes-ok=0 frozen-cores-missing=0)`, `h5=1(spans=45 located=45 failed=0 uncited=0 cores=5/5)`

## 4. The 12 survivors and why each is equivalent

H4 (seven): the only tree-varying inputs to H4 are the manifest bytes and the snapshot. Both are sha-pinned: H4 pins `manifest.json` and `source-recheck.py` before any floor is read, and the manifest's `sha256` field binds the snapshot, which `source-recheck.py` verifies (a tampered snapshot gives `S074:sha256 MISMATCH`, rc=1, `quotes-ok=0`; fixture `snap_tamper`, where H4-01 and H4-04 through H4-08 and H4-11 are still red, identical to the original). Under those pins `oks` is 9, the anchor set has 8 members and the cores are all present, so `oks >= 1`, the dropped oks-equality, the dropped BROKEN-scan, the dropped rc clause, the dropped cores clause, the dropped sha-OK clause and `miss = []` each evaluate identically on every tree that passes the pins. Their only live effect would run through the pin checks themselves, which H4-09 and H4-10 show are caught. This confirms R50 disclosure (d).

H5-26 (`>= 2`) and H5-27 (`>= 5`): with `cores == 5` required, `passed >= 4` is dead. Computed on the pinned snapshot (`facts.py`, body = 42 lines, 1094 whitespace tokens): `distinct core-subsets achievable by one <=25-word quote: [((0,), (136, 25)), ((1,), (222, 25)), ((2,), (503, 25)), ((3,), (580, 25)), ((4,), (947, 25))]` and `min number of <=25-word quotes covering all 5 cores (unconstrained by lines): 5`. No quote of at most 25 words carries two cores, so five cores need at least five located quotes (the `five` fixture is green at exactly 5). R50 disclosure (e) attributes the shadowing to the 6-row table; the real reason is this cover argument. The `>= 4` floor is therefore redundant under the cores conjunct on the pinned snapshot.

H6-01 (`>= 66`): `names` is a subset of `everything`, so `names >= 66 and everything == 66` forces `names == 66`. Fixture `knowledge67` (`h6=0`) shows the mutant and original agree.

H6-02 (drop `nested == 66`): with `names == 66 and everything == 66` there are no subdirectories, no dangling links and no non-md entries (the `links` check and the `everything` count rule them out), so the `os.walk` `.md` count equals 66. Fixture `nested` is red both ways.

H6-04 (drop names pin): `cont` is a hash over the sorted base names together with their content hashes, so a changed name set changes `cont`. Fixture `rename` is red both ways.

## 5. Findings

F1 (v1 defect, already errata E4; closed at v1.1). In frozen v1, `live_lines` keeps a line that has a mid-line `<!-- … -->` comment, so a frozen core quote inside that comment counts as live. Fixture `core5_midline` (core 5 inside `Summary note. <!-- “…” (`S074.txt:38`) -->`): v1 `h5=1 … cores=5/5`; v1.1 `h5=False, cores=4/5`; mutant H5-28 (the v1.1 fix applied to v1) KILLED on this fixture. The line-comment variant (`core5_linecomment`) is red under both, as it should be.

F2 (gap, not a bypass). H5 has no minimum length for curly quotes. Fixture `trivial_quote` (`Appended: “GitHub” (`S074.txt:24`).`) gives `h5=1 … spans=46 located=46`. A one-word echo counts as evidence. It cannot reach 7/7 alone because the five cores must each be carried by a live located quote; the manifest side has `MIN_QUOTE_CHARS` and H5 does not. Recommend a floor if the lane wants located quotes to mean substantive quotes.

F3 (design limitation). H6 does not pin ledger content (by design per claim: name pinned, size may grow). Fixture `ledger_garbage` (40 KB of unrelated text) gives `h6=1 … base-intact=1`. This matches the stated design; it means the ledger-dispositions append is not verified by H6.

F4 (per-limb coverage note). H5 does not bind the snapshot: fixture `snap_tamper` (line 9 altered) gives `h5=1` while `h4=0`. H5's correctness rests on the H3 and H4 snapshot pins. The cover argument in §4 is valid only under those pins.

F5 (fragility, not a defect). H5 relies on `re.findall` returning `''` for an unmatched optional group. Mutant H5-24 (`if b is not None`) crashes: `limb-error=ValueError` on every fixture with a single-line cite. Had it been judged equivalent by assumption, that would have been wrong. The original is correct.

F6 (correction to R50 disclosure (e)). The located floor's shadowing reason is the five-core cover (min 5 quotes), not the 6-row table. The conclusion (`>= 4` is dead) holds.

## 6. Limitations

- Positive fixture is the `96379ae` corpus, the only tree with the F29 entry; the freeze tree (`fe0f56b`) has none, so H5/H6 were not exercised on it directly.
- Only H4, H5, H6 were attacked. H1, H2, H3, H7 and the selftests (`r46-selftest-f29.py`, `r46-counters-selftest-*`) were not run, and the battery `r46-mutbat.py` was not run.
- Equivalence claims are argued from pins plus one fixture each; they are not exhaustive over all trees. The H5 cover argument assumes the pinned snapshot.
- The live GitHub page and S074 quotes were not re-checked (not in this item).
- Nothing installed; stdlib `python3` only. Scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2MutGate2/` removed on exit. No commit, push, index or git mutation; nothing outside the lane's report path was written.
