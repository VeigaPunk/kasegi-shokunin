# L1 freeze corrections (2026-10-27, mid-wave-1) — AUTHORITATIVE, read first

Two freeze defects were found by seat ScribeShonenLog and corrected by the L1 in
`.ufo/waves/round-41/claims.json` (the live file; the dispatched spec/dispatch
bytes keep the old literals and are superseded by this note for these two items).

1. BASE HASH. The real round-41 base is the 40-char
   `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (prefix 5b29ea14). The freeze files
   wrote a 38-char literal missing `f0`, which resolves to no git object. Any seat
   running `--export-ref <base>` or `git archive <base>` MUST use the 40-char hash
   above. Suites must report an unresolvable `--export-ref` as a distinct red
   (`ref-not-found` in payload), never as a vacuous `closed<12/12 exit=1` — that
   T-class vacuity is what the freeze punishes.

2. I11 ESCAPE COUNT. The committed `.ufo/waves/round-40/wave2/CritKillRule.md`
   carries EIGHT `### F` escape states (F1-F8), not seven. I11's target is all
   eight committed states; the I11 payload must read `escapes=8` and `red=8`,
   naming F1-F8. (The file's own intro prose says "7 distinct escape states"; the
   committed headings are authoritative.)

Both corrections are logged as the round's freeze-typo mistakes (M41 rows) with the
fix guard: every 40-char hash literal is `git rev-parse --verify` dry-run at freeze
time, and every count literal is derived from the committed bytes it names.
