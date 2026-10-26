# RevNoHarm — round-37 no-harm verification (receipt)

Seat: RevNoHarm (leaf) · Round: kasegi-shokunin 37 · Written: 2026-10-26
Base `b56a41680cefd391868c1c370dc063c69d827e7d` · freeze `224df74db2a46d627ae1475a72ca48796bbd177c` · HEAD at measurement `b362068195d5489aa94b31e6ec8f880c367e0ba0` (freeze + erratum-1 + wave-evidence commits).

## 1. Contract

After round-37 integration, the diff base→after must be **append-only** for the no-harm set: **zero deletions, existing line numbers preserved**. Operationalized as three machine checks plus a canary (gate script in §5):

- **H1** `git diff --numstat <BASE> -- <f>` deletions column = 0 for every file (whole-file deletion prints `- -`, guarded).
- **H2** base bytes are an **exact sha256 prefix** of the after bytes ⇒ every base line survives unchanged, in order, at its original offset.
- **H3** SKILL.md only: every diff hunk is a pure `a` op with insertion point ≥ base line **1106** (frozen C1 wording: "only appended registry rows after :1106"). Clean form at EOF: `1111a1112,…`.
- **Canary** no root-level `QUALITY.md`/`SOURCES.md` twins — these files live under `corpus/`; a bare pathspec matches nothing and would silently pass (false-green hazard, pre-empted).

## 2. Resolved paths (item bare names → tracked paths)

| Item name | Tracked path at base | Exists at base |
|---|---|---|
| SKILL.md | `SKILL.md` | yes |
| PROVINCE.md | `PROVINCE.md` | yes |
| SCORECARD.md | `SCORECARD.md` | yes |
| LOG.md | `LOG.md` | yes |
| README.md | `README.md` | yes |
| QUALITY.md | `corpus/QUALITY.md` | yes |
| SOURCES.md | `corpus/SOURCES.md` | yes |

Root-level `QUALITY.md`/`SOURCES.md` do not exist at base or HEAD (verified via `git ls-tree -r`). Fixture copies under `corpus/instruments/r35-fixtures/**` are outside the no-harm set.

## 3. Base measurements (all from `git show b56a416…:<path>`)

| File | sha256 | lines | ends `\n` |
|---|---|---:|---|
| SKILL.md | `2ddb1bc72872a54a87f2b3655d6612c4b5bae86ea154a612aa42cfc5fcc1fd8f` | 1111 | yes |
| PROVINCE.md | `b0e91a611feadeeae38df7fd7fa55d8efe56039721cc35a024ca8af81108b5a9` | 78 | yes |
| SCORECARD.md | `1e2788c6a7f577f17dd5ce46ec69e6debe7b883caea374b46f240e1754d84e6e` | 1494 | yes |
| LOG.md | `4b653ff1513677fb85ee0a38556ee98b4c611cf6a68878d6f500151a8fbb709f` | 1675 | yes |
| README.md | `f0662f59f4b2296204a61c23db5a8bf29100acd8f08f860a5585d0659f9ab014` | 14 | yes |
| corpus/QUALITY.md | `cfd0187ac6bcc39ccbaa33b5f40e82bf5de4dfa7197e169870163ebe78ca3728` | 264 | yes |
| corpus/SOURCES.md | `2ff7818ad2179c1f8ecf89262e3f8a84a585dfb4f64bbc1fa0e7dbc3be2465fe` | 117 | yes |

All seven end with a newline, so EOF appends are pure additions (no phantom `-1/+1` modify).

**Pre-integration state (measured):** `git diff --numstat b56a416…` = 8 files, all under `.ufo/waves/round-37/`, all pure additions (30/0, 22/0, 8/0, 22/0, 81/0, 1017/0, 1019/0, 604/0). The item's "empty now" was written before the freeze commit landed; **none of the seven no-harm files are touched** base→HEAD→worktree (`git diff --quiet` over both ranges: clean). Worktree dirt is untracked `.ufo/` scratch only.

**SKILL.md :1106 anchor (base bytes, exact):** line 1106 = `## Round-36 Gates & probes registry addition (appended 2026-10-26)`; 1107 blank; 1108 table header; 1109 separator; 1110 = `r35-defect-closure.sh` row; 1111 = `r36-closure.sh` row (**base EOF = 1111**). Sanctioned insertion zone: hunks `1106a…` through `1111a…`; the clean append is `1111a1112,…`.

## 4. Instrument baselines (worktree ≡ base for all seven at measurement time)

- `python3 corpus/instruments/density.py SKILL.md` → **exit 0**, `**mean dens** = **225.3**`, 1111 lines, 27 blocks, 751 path-citation instances. The item said "201.2-ish"; the **measured baseline at this base with the committed instrument is 225.3** — use 225.3. Base blocks #1–#27 must reproduce byte-stable after integration; new appended blocks appear as #28+.
- `python3 corpus/instruments/anchorcheck.py SKILL.md` → **exit 0**; verdict tally: **306 LOST-RECORDED** (recorded-not-fail), **16 OK**, fail classes (MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BOUNTIES-ABSENT/BASE-ABSENT) = **0**; 324 output lines.
- Instrument identity at HEAD: `density.py` blob `1f99e66f883ac2ddfd4829e83b9c037f5f0742a5`, sha256 `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`; `anchorcheck.py` blob `54200ebc85b3f0537f7094db4d8947c18129d31d`, sha256 `d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912`. Python 3.14.8. Both tracked at base; both are **baselines, not gates** — the no-harm axis gates structure (H1–H3); density/anchorcheck must merely stay exit 0 / fail-class-0 and are recorded here for comparison.

## 5. The gate (`noharm-gate.sh`, full text — recreate verbatim to run)

```sh
#!/bin/sh
# noharm-gate.sh — round-37 RevNoHarm append-only gate.
# Usage: BASE=<commit> [STRICT_SKILL_START=1106] sh noharm-gate.sh   (cwd = repo toplevel)
set -u
BASE=${BASE:?set BASE to the base commit}
START=${STRICT_SKILL_START:-1106}
FILES='SKILL.md PROVINCE.md SCORECARD.md LOG.md README.md corpus/QUALITY.md corpus/SOURCES.md'
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
fail=0
for f in $FILES; do
  st=$(git diff --numstat "$BASE" -- "$f")
  if [ -z "$st" ]; then echo "ok   $f: untouched vs BASE"; continue; fi
  del=$(printf '%s\n' "$st" | awk '{s+=$2} END{print s+0}')
  add=$(printf '%s\n' "$st" | awk '{s+=$1} END{print s+0}')
  printf '%s\n' "$st" | grep -q '^-' && del=999999   # whole-file deletion shows as "- -"
  n=$(git cat-file -s "$BASE:$f" 2>/dev/null || echo 0)
  bsha=$(git show "$BASE:$f" 2>/dev/null | sha256sum | cut -d' ' -f1)
  psha=$(head -c "$n" "$f" 2>/dev/null | sha256sum | cut -d' ' -f1)
  [ "$del" = 0 ] || { echo "HARM $f: deletions=$del (append-only violated)"; fail=1; }
  [ "$bsha" = "$psha" ] || { echo "HARM $f: base bytes not an exact prefix (existing lines changed/moved/truncated)"; fail=1; }
  if [ "$f" = SKILL.md ]; then
    git show "$BASE:SKILL.md" > "$tmp/base"
    diff "$tmp/base" SKILL.md | grep -E '^[0-9]+(,[0-9]+)?[acd][0-9]+' > "$tmp/hunks" || true
    if [ -s "$tmp/hunks" ] && grep -qvE '^[0-9]+a' "$tmp/hunks"; then
      echo "HARM SKILL.md: non-append diff op(s):"; grep -vE '^[0-9]+a' "$tmp/hunks"; fail=1
    fi
    bad=$(sed -n 's/^\([0-9]\{1,\}\)a.*/\1/p' "$tmp/hunks" | awk -v s="$START" '$1<s{print; exit}')
    [ -n "$bad" ] && { echo "HARM SKILL.md: insertion at base line $bad (< $START)"; fail=1; }
    echo "info SKILL.md: hunk ops: $(tr '\n' ' ' < "$tmp/hunks")"
  fi
  [ "$fail" = 0 ] && echo "ok   $f: +$add -0 append-only"
done
tw=$(git diff --numstat "$BASE" -- QUALITY.md SOURCES.md | wc -l)
[ "$tw" = 0 ] || { echo "HARM: root-level QUALITY.md/SOURCES.md twin(s) appeared"; fail=1; }
git diff --numstat "$BASE" | awk '$2!=0{c++; print} END{if(c+0>0) print "INFO whole-tree deletions: " c " path(s)"}'
if [ "$fail" = 0 ]; then echo 'NO-HARM: PASS'; else echo 'NO-HARM: FAIL'; exit 1; fi
```

**Pre-run (this seat, 2026-10-26):** in the lane at pre-integration state → 7× `ok … untouched`, `NO-HARM: PASS`, **exit 0**.

**Required reds (gate can fail — fixture `mktemp -d` repo, toplevel verified equal):**
- Pure EOF append → hunk `3a4`, `NO-HARM: PASS`, exit **0**.
- Middle-line tamper → `HARM … deletions=1`, prefix broken, op `2c2`, `NO-HARM: FAIL`, exit **1**.
- Insertion above sanctioned start → `HARM … insertion at base line 0 (< 2)`, op `0a1`, `NO-HARM: FAIL`, exit **1**.

## 6. Cross-claim tension (flag before integration): E13 vs append-only

Base SKILL.md line 1111 (`r36-closure.sh` row) still carries the literal type cell `gate\|probe` — exactly what frozen **E13** targets ("single-choice type cell, not literal `gate|probe`"). `corpus/instruments/r37-closure.sh` is **not tracked at HEAD**, so E13's implementation is unobservable today. If E13 is satisfied by *editing line 1111*, that is a `1c1`-style mutation and **this gate will correctly go red on SKILL.md** (the round contract in this item is zero deletions). Append-compatible resolutions: (a) append a superseding corrected registry row in a new Round-37 section and have E13 check the corrected row's presence (watch E3's exact-basename row count for duplicates), or (b) the L1 explicitly sanctions a line-1111 exception — the gate still reports HARM honestly and the L1 owns the waiver. Decision belongs to C1/L1; surfaced here so it is cheap to fix now, not after integration.

## 7. Exact L1 post-integration command set (copy-paste; save §5 as `noharm-gate.sh` first)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=b56a41680cefd391868c1c370dc063c69d827e7d
# (1) coarse per-file numstat — deletions column must be 0 in every line
for f in SKILL.md PROVINCE.md SCORECARD.md LOG.md README.md corpus/QUALITY.md corpus/SOURCES.md; do git diff --numstat "$BASE" -- "$f"; done
# (2) full gate (H1+H2+H3+canary) — expect 'NO-HARM: PASS', exit 0
BASE="$BASE" sh noharm-gate.sh
# (3) SKILL.md prefix-sha — the two hashes must be EQUAL
git show "$BASE:SKILL.md" | sha256sum                                   # 2ddb1bc72872a54a…fd8f
head -c "$(git cat-file -s "$BASE:SKILL.md")" SKILL.md | sha256sum
# (4) diff shape — only 'a' ops, start >= 1106; clean form '1111a1112,…'
diff <(git show "$BASE:SKILL.md") SKILL.md | grep -E '^[0-9]'
# (5) baseline re-runs — record vs §4
python3 corpus/instruments/density.py SKILL.md       # exit 0; blocks #1–#27 byte-stable; mean moves from 225.3
python3 corpus/instruments/anchorcheck.py SKILL.md   # exit 0; fail classes 0; base-line verdicts unchanged
# (6) after the round head is committed:
NEW=$(git rev-parse HEAD); git diff --numstat "$BASE" "$NEW" --    # zero deletions outside .ufo evidence additions
```

Notes: `git show <base>:SKILL.md | sha256sum` vs after — the **full-file hash will change** after a legitimate append; the no-harm invariant is prefix equality, which (3) proves and (2)+(4) prove mechanically ("only appended rows after :1106"). Gate (2) reads the worktree; run (6) against the committed head as the durable record. If any command in (1)–(4) prints a deletion or a non-`a` op, integration introduced harm — stop and route back.

## 8. Limitations / residual risk

- Gate is worktree-scoped until (6) pins the committed head; H2's prefix check is byte-exact, so a mid-file insertion that keeps deletions=0 is still caught, and SKILL.md additionally constrains the insertion point (≥1106) rather than any position.
- density/anchorcheck baselines are host- and-commit-stamped (Python 3.14.8, this host's absent mirror/origin roots feed the 306 LOST-RECORDED class); compare like against like post-integration on the same host.
- Instrument `r37-closure.sh` absent at HEAD ⇒ E13/E10 interaction (§6) unresolved at measurement time.
- Tooling installed: none (bash/git/python3 preexisting; no installs performed). Scratch `/fast/scratch/hyaku/kasegi-r37/RevNoHarm/` used for instrument outputs and gate runs, removed after this receipt landed. This receipt is this seat's only lane write.
