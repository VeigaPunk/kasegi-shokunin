# R48Probe33 — Bounded grammar probe: box-3 one-byte label mutation vs frozen shonen-form.py

- **Seat:** R48Probe33 (leaf, kasegi round 48, wave 1)
- **Axis:** depth:verifiability
- **Claim probed:** C1 (routed-defect-closure) — `.ufo/waves/round-48/claims.json` (frozen at 3546f7089c224ac6c8adc68208b1e648bbf3e6a5)
- **Frozen counter:** `corpus/instruments/shonen-form.py` — sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`, mtime 2026-10-30 11:30:19 -0300, 2719 bytes. Read-only; not modified by this seat (git status clean on it at capture time).
- **Round-47 verifier routes read:** R1 (SHONEN.md canonical-form drift, 52 author marks / 13 blocks) and R2 (plain-target phrasing) from `corpus/lessons/round-47-verifier-spotcheck.md` §6; protocol source snapshot `.ufo/waves/round-48/controls/protocol-source.txt` (File contract / Promotion gates / canonical seed).

## Probe definition

Scratch copy of the canonical four-box SHONEN.md; **box 3 only** (`- [~] Instructions executable
by an agent without oral context`); **exactly one label byte** changed: the box mark `~` (0x7E)
→ `x` (0x78). Other three boxes untouched. Run the frozen checker with `--root` at the lane root
and `--file` at the scratch fixture; run the unmodified positive in the same invocation shape.

## Fixtures (scratch, since removed)

Root: `/fast/scratch/hyaku/kasegi-r48/R48Probe33/` (created by this seat, deleted on exit after this report saved the receipts).

| File | sha256 | Bytes | Role |
|---|---|---|---|
| `SHONEN-positive.md` | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` | 761 | Byte copy of repo `SHONEN.md` at HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031` (the landed repaired canonical form; all four evidence pointers resolve: SKILL.md, LOG.md, `corpus/lessons/round-47-verifier-spotcheck.md`, PROVINCE.md) |
| `SHONEN-box3-xmark.md` | `110ebf4ec4b544419fb18259b47511d47db9f249965811dc6c7ef6a4fe0fe8d1` | 761 | Box-3 label mutant |

Byte-diff evidence: `cmp -l SHONEN-positive.md SHONEN-box3-xmark.md` → `442 176 170` (exactly one
differing byte: offset 442 (1-based), octal 176 = `~` → octal 170 = `x`); `grep -n "Instructions
executable"` shows the change confined to line 9 (box 3): `- [~]` → `- [x]`.

## Commands and full observed output

Interpreter: Python 3.14.8. No installs this seat.

```
$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe33/SHONEN-positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
P1-exit=0

$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/canonical-candidate.txt
shonen-form canonical=1 finding=SF-CLEAN exit=0
P2-exit=0

$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe33/SHONEN-box3-xmark.md   (run 1)
shonen-form canonical=0 finding=SF-VERIFIER exit=1
M1-exit=1

$ python3 ... --file .../SHONEN-box3-xmark.md   (run 2)
shonen-form canonical=0 finding=SF-VERIFIER exit=1
M2-exit=1

$ python3 ... --file .../SHONEN-box3-xmark.md   (run 3)
shonen-form canonical=0 finding=SF-VERIFIER exit=1
M3-exit=1
```

## Expected vs observed

| Case | Expected | Observed | Verdict |
|---|---|---|---|
| Unmodified positive (scratch copy of landed SHONEN.md) | `canonical=1 SF-CLEAN exit=0` | `canonical=1 SF-CLEAN exit=0` | MATCH |
| Positive on controls fixture `canonical-candidate.txt` | `canonical=1 SF-CLEAN exit=0` | `canonical=1 SF-CLEAN exit=0` | MATCH |
| Box-3 one-byte label mutant (`[~]`→`[x]`) | nonclean + stable SF finding | `canonical=0 SF-VERIFIER exit=1`, identical across 3 runs | MATCH |

## Semantics ruling (no fabricated defect)

The mutation is **not** semantically permitted, so the rejection is the checker's designed
behavior, not a defect in the counter. Per the protocol's Promotion gates, `[x]` is writable only
by a named non-author verifier; an author-side `[x]` counts as `[~]` attestation. Claim C1's
mechanical limits state the same author-side grammar: "x marks are rejected (independence cannot
be established mechanically)." The frozen checker's `SF-VERIFIER` branch
(`if mark == 'x': return 'SF-VERIFIER'  # This author-side checker cannot attest independence.`)
fires only after the box regex and the evidence-pointer checks pass, so the probe isolates the
label-grammar limb: a forged non-author verification mark on an otherwise-canonical file is
detected, nonclean, and stable. This directly exercises the C1 kill-rule class (a grammatically
hidden/duplicated/forge-marked checklist must not pass the frozen checker) at the smallest unit:
one label byte, one box.

## Counter integrity and scope hygiene

- Frozen counter untouched: targeted `git status --porcelain` over `SHONEN.md`,
  `corpus/instruments/shonen-form.py`, and `.ufo/waves/round-48/claims.json` printed empty at
  capture time; lane HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031` (2026-10-30 11:32:58 -0300).
- No production, fleet, sibling, domain-tree, or git/jj state edits; no commit/push; no
  delegation; no background jobs. Only this report and the now-removed scratch fixtures were
  written. No tool installs (pacman untouched, host-wide pause respected).
- Evidence-pointer note: the checker's pointer resolution runs against `--root`, so both the
  landed file's `corpus/lessons/round-47-verifier-spotcheck.md` pointer and the control's `LOG.md`
  pointers resolve; the probe grade is therefore attributable to the label byte, not pointer
  state.

## Receipts

Full transcripts are the command/output blocks above (captured live this session, 2026-10-30);
fixture digests and the `cmp -l` byte witness are recorded in the Fixtures section. Scratch
directory `/fast/scratch/hyaku/kasegi-r48/R48Probe33/` removed after this report was written.
