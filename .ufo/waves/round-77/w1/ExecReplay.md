# ExecReplay — inherited-state replay, round-77 w1 (2026-11-05)

Seat: ExecReplay (leaf). Scope: re-derive the five inherited-evidence items round 77 builds on, from committed bytes at freeze `539a43877809bd90b6f506e8fd24a6d871598cd5` (parent = base `2e53fc74776824898b5c5eb914aeddc19a091157`, verified via `git log -1 --format='%H%n%P'`; freeze subject: "round-77: freeze C1 (recheck-cwd RESULT-limb gate, 12 checks, 5 mutant kills) and C2 (F54 OSV querybatch on S112) with controls and R126 pre-freeze receipt"). All git access read-only (`git show|log|rev-parse|status`); all writes confined to `.ufo/waves/round-77/w1/ExecReplay*` and scratch `/fast/scratch/hyaku/kasegi-r77/ExecReplay/`. No tools installed; no pacman; no background jobs; no delegation.

**Overall: all five items MATCH their expected inherited state. No routed defect found in this seat's scope.**

## Item 1 — r76 survivor control selftest (C1 depth:verifiability foundation)

Command (run from seat scratch, `TMPDIR` pinned there; `python3 -B` = no bytecode writes):
```
TMPDIR=/fast/scratch/hyaku/kasegi-r77/ExecReplay python3 -B \
  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-76/controls/m2b-conjunct-removed.py --selftest
```
- Observed: 8 case lines, all `ok`, final line `selftest cases=8 failures=0`, exit code **0**. Expected: `selftest cases=8 failures=0` rc 0. **MATCH.**
- Tree safety: `git -C <lane> status --porcelain -- .ufo/waves/round-76/controls/` empty before **and** after the run; the control's own `scratch-cleanup` case reports `leftover=0`.
- Byte identity: sha256 of the working-tree control == freeze blob == base blob, all `174dc28e7ec200ea3ab2875fcda2fc8dea824a6f4edb7964f602d2ac79ff433c` — the re-run exercised the committed bytes unchanged since base. Evidence: `ExecReplay-item1-identity.txt`.
- Receipt match: `.ufo/waves/round-77/controls/c1-redbefore-r76-survivor-r77.txt` (9 lines; summary at `:9`) vs the fresh run differs in **exactly one line** — `tmpdir-parent` `dirs=` echo: receipt records `dirs=None,None,None` (its run had no `TMPDIR` set); this run echoes the seat scratch three times (TMPDIR pinned per lane bounds). All 8 case names, all `ok` verdicts, every `got=`/`want=` payload, and the `cases=8 failures=0` summary are byte-identical. **Receipt matches; survivor stands.** Full diff: `ExecReplay-item1-receipt-diff.txt`.
- Disclosure: the first evidence file I wrote was a hand transcription that dropped `exit_other=0,` (13 chars, 298 vs 311) from the `relabel-pair` `want=` list — my transcription artifact, not a run difference. The file was replaced with a byte-exact capture (`tee` into scratch, read back). Final evidence is verbatim: `ExecReplay-item1-selftest.out`.

## Item 2 — `MIN_QUOTE_CHARS = 12` at `corpus/instruments/source-recheck.py:33`

Command: `git show 539a438…:corpus/instruments/source-recheck.py | grep -n MIN_QUOTE_CHARS`
```
33:MIN_QUOTE_CHARS = 12   # normalized minimum: a shorter "quote" matches any capture
151:        if len(normalize(assertion["quote"])) < MIN_QUOTE_CHARS:
```
Expected: line 33 defines `MIN_QUOTE_CHARS = 12`. **MATCH.** Bonus: `:151` is the consumption site, so the constant is live at the freeze. Evidence: `ExecReplay-item2-minquote.out`.

## Item 3 — S108 five other-endpoint strings, listed-not-described

Command: `git show 539a438…:corpus/source-snapshots/round-73/S108.txt | sed -n '5,9p'`
```
5: POST /v1/querybatch
6: GET /v1/vulns/{id}
7: GET /v1experimental/importfindings
8: POST /v1experimental/ determineversion
9: POST /v1experimental/ubuntu/binary-to-source
```
Expected: querybatch, vulns/{id}, determineversion, importfindings, ubuntu/binary-to-source listed-not-described. **MATCH** — all five present, one bare nav entry per line, no payload/parameter text, and these five lines are the only hits of those strings in the snapshot. Capture quirk kept verbatim: line 8 reads `/v1experimental/ determineversion` (space after the slash, as captured). Evidence: `ExecReplay-item3-s108.out`.

## Item 4 — exclusion sentence at `corpus/knowledge/osv-post-v1-query-contract.md:75`

Command: `git show 539a438…:corpus/knowledge/osv-post-v1-query-contract.md | sed -n '75p'`
```
- the other endpoints in the page's navigation (POST /v1/querybatch, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are listed, not described.
```
Expected: the 'listed, not described' exclusion sentence. **MATCH** — verbatim, naming POST /v1/querybatch with the `S108.txt:5-9` pointer that item 3 verifies line-by-line. Evidence: `ExecReplay-item4-contract75.out`.

## Item 5 — SOURCES.md census: S111 queued/dash, S112 collision guard

Commands and outputs (all on `git show <commit>:corpus/SOURCES.md`):
- `grep '^| S111'` at freeze → row fields (awk `-F'|'`, 13 fields): id `S111`, type `docs`, grade `A`, status col9=`queued`, date `2026-11-05`, TTL `90d`, **used-by col12=`—` (dash)**. Expected: S111 queued, used-by dash. **MATCH.**
- `grep -c 'S112'` at **base** `2e53fc74…` → `0` (grep rc 1). Expected 0. **MATCH.**
- `grep -c 'S112'` at **freeze** `539a438…` → `1` (grep rc 0); sole occurrence at `corpus/SOURCES.md:124`, tail columns col9=`queued`, col10=`2026-11-05`, col11=`180d`, col12=`—`. Expected 1. **MATCH — collision guard holds:** S112 absent at base, exactly one occurrence at freeze (the queued admission row).
- Cross-check: the S112 row's scope names POST /v1/querybatch and excludes the single-query POST /v1/query contract (S108, F51), the record format (S080, F31), and the overview page (S111) — consistent with items 3 and 4. Evidence: `ExecReplay-item5-sources.out`.

## Retained evidence index

| File | Content |
|---|---|
| `ExecReplay-item1-selftest.out` | byte-exact fresh selftest transcript + run conditions |
| `ExecReplay-item1-receipt-diff.txt` | unified diff, receipt vs fresh run (one environmental line) |
| `ExecReplay-item1-identity.txt` | sha256 identity worktree == freeze == base |
| `ExecReplay-item2-minquote.out` | grep -n MIN_QUOTE_CHARS output |
| `ExecReplay-item3-s108.out` | S108 lines 5-9 + endpoint string hits |
| `ExecReplay-item4-contract75.out` | contract.md line 75 verbatim |
| `ExecReplay-item5-sources.out` | S111/S112 rows, counts at base/freeze, used-by columns |

## Risks / notes for the wave

- The `tmpdir-parent` `dirs=` echo is environment-dependent by design; any future byte-exact comparison against the receipt must either run without `TMPDIR` or mask that one field. Nothing in the r77 C1 gate depends on it (all case verdicts and the summary line are stable).
- Scratch `/fast/scratch/hyaku/kasegi-r77/ExecReplay/` removed before this report's yield (confirmation in seat result); no receipts depended on it — all raw evidence is copied into `w1/`.

Report: .ufo/waves/round-77/w1/ExecReplay.md
