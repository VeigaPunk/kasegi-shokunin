# AttackA6 — expected-list parity falsification (knowledge-expected.txt)

- Seat: L1Kasegi26.AttackA6 (leaf, read-only)
- Wave: round-26 wave-2 (falsify)
- Date/UTC: 2026-10-25
- Target: `corpus/instruments/knowledge-expected.txt` (39-entry expected list, digest-agnostic)
- Claim attacked: wave-1 claim C1/C2 list parity — expected list matches the knowledge tree
- Verdict: **NOT FALSIFIED — claim HOLDS.** All five numbered checks plus the git-status cross-check pass.

## Checks (all run from lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

### (1) Structure: sorted, one relative path per line, comments only in the 2-line header
- Total lines: 41. Lines 1–2 are the only `#`-prefixed lines (header), no line below line 2 begins with `#`. ✅
- Content lines (3–41): 39, each exactly one lane-relative path `corpus/knowledge/<name>.md`. ✅
- No blank lines (zero empty lines). ✅
- No duplicate lines (Counter over all 41 lines: 0 duplicates). ✅
- No CR bytes (0 `\r` in raw bytes). ✅
- Sortedness: exact order equality against canonical reference —
  `diff <(ls corpus/knowledge/*.md | sort) <(tail -n +3 corpus/instruments/knowledge-expected.txt)`
  → empty, i.e. identical (`ORDER_IDENTICAL_YES`). ✅
  - Observation: the file is sorted in `en_US.UTF-8` collation (the locale in which `ls | sort` is run here). Under strict ASCII-byte order there is exactly one inversion — line 15 `evidence-dir.md` before line 16 `ev-model.md` (`-` 0x2D < `i` 0x69) — but the canonical `ls | sort` in this locale also emits `evidence-dir.md` first, so the file matches the stated sorted criterion exactly. Not a defect.

### (2) Non-comment set == `ls corpus/knowledge/*.md | sort` (39 entries)
- Disk: 39 files (`ls corpus/knowledge/*.md | sort`). Expected: 39 non-comment entries.
- Set equality: True. Symmetric difference empty — no expected entry missing from the tree, no tree entry absent from the list (checked both directions). ✅

### (3) No blank / duplicate / CR
- See (1): zero blanks, zero duplicates, zero CR. ✅

### (4) Every name exists
- All 39 expected paths exist on disk (os.path.exists per entry — all True).
- All 39 tree entries are present in the expected list. ✅

### (5) Exact count
- 39 non-comment entries (content lines after the 2-line header). This matches the 39-entry claim and the `ls | sort` count of 39. ✅

### Cross-check: `git status --porcelain corpus/knowledge/`
- Output is exactly two lines, both `??` (untracked):
  - `?? corpus/knowledge/iso-29147-and-30111-division-of-labour.md`
  - `?? corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`
- Confirmed with `--untracked-files=all` (no untracked directories hidden). No modified or deleted tracked files in the dir.
- Tracked count in dir: 37; 37 tracked + 2 untracked = 39, consistent with the `ls` count. The two untracked entries are exactly the two new knowledge entries referenced in the round context. ✅

## Residual risk / verification gaps
- None material. The instrument (`recheck-audit.py` `load_expected` / `expected_mismatch`) enforces the expected list as a *set* (missing/unexpected named in the receipt), not order; order is therefore a convention-only property here — but this review verified order directly against `ls | sort` and it matches.
- Read-only seat: no production edits, no VCS mutations, no installs (no tools installed; tooling directive record: none).

## Evidence trail
- `read` of knowledge-expected.txt (41 lines, header lines 1–2).
- Python checks (eval): CR bytes 0; blanks []; duplicate lines {}; non-comment count 39; disk count 39; set equality True; symmetric difference empty; missing files none.
- Bash: `diff` order-equality (identical); `git status --porcelain` (exactly 2 `??` lines); `git ls-files corpus/knowledge/ | wc -l` = 37; `locale` → LANG=en_US.UTF-8, LC_COLLATE=en_US.UTF-8.
