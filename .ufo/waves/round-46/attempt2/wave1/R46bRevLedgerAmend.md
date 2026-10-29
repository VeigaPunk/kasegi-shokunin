VERDICT: BROKEN (scoped to the planned guard, not to the claims)

Scope. Seat item: attack the planned r46-c2-gate.py v1.3 ledger exemption
(`considerthese-proposals-ledger.md` added to CONTENT_EXEMPT, name-pinned non-shrink, per the executor seat spec
`R46bExecGatePinAmend` in `.ufo/waves/round-46/attempt2/wave1-spec.json:225` and mirroring the committed
`corpus/instruments/r46-f29-gate.py:80-81,322-326`). The scout spec file
`.ufo/waves/round-46/attempt2/wave1/R46bScoutLedger.md` did not exist yet when I ran (scout seat still working), so I
modeled the exemption from the executor spec + the f29-gate precedent (limitation L1). No tools installed (python3
stdlib + coreutils only; nothing fetched). No lane/fleet file touched; all fixtures under
$HYAKU_SCRATCH/kasegi-r46/R46bRevLedgerAmend, removed after receipts were copied into
`wave1/R46bRevLedgerAmend.draft/`.

Setup (exact commands):
- Tree: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d | tar -x -C $S/base` (65 knowledge entries; ledger 30696 bytes, sha256 `07994f48...c7205`).
- Mock v1.3 gate: byte-copy of the committed `corpus/instruments/r46-c2-gate.py` with exactly the spec'd mutation
  (CONTENT_EXEMPT + ledger; EXEMPT_BASE_SIZE + `considerthese-proposals-ledger.md: 30696`; G6 docstring sentence
  `62 ... the two entries` -> `61 ... plus the considerthese-proposals-ledger`; frozen content pin re-derived, see F8).
  Full diff: `wave1/R46bRevLedgerAmend.draft/v12-to-v13-mock.diff`; mock sha256 `0c9965b3...a97e26a`.
  Placed at `$S/v13lane/corpus/instruments/` with a byte-verified copy of `source-recheck.py` beside it so the gate's
  TOOL_ROOT lookups resolve; every run with `TMPDIR=$S/tmp`.
- Run line: `python3 <gate> --root $S/<tree>`; full outputs: `wave1/R46bRevLedgerAmend.draft/gate-run-receipt.txt`.

Guard under test (committed v1.2 code, unchanged by the exemption):
`corpus/instruments/r46-c2-gate.py:338` computes the aggregate content pin over `base_like` minus CONTENT_EXEMPT;
`:341` compares it to PINS["base-knowledge-content"]; `:344` `grown = all(os.path.isfile(...) and os.path.getsize(...) >= sz for ... EXEMPT_BASE_SIZE.items())`; `:343,345-346` reject any symlink under corpus/knowledge. The exemption removes the ledger from the `:338` set and adds only a size floor at `:344`. The ledger's bytes are never read by any check.

FINDINGS

F1 do-nothing control (T0 = pristine copy of the base export, no mutation). Both gates discriminate clean:
- v1.2 committed: `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1` / `c2-gate fixed=7/7 exit=0`
- v1.3 mock:      `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1` / `c2-gate fixed=7/7 exit=0`

F2 ledger emptied to a stub (T1, ledger = 7 bytes). Guard CATCHES it; both gates red:
- v1.2: `gate G6 pass=0 read=knowledge=65 entries=65 nested-md=65 base-intact=0 entry-bytes-ok=1` / `fixed=6/7 exit=1`
- v1.3: `gate G6 pass=0 read=symlinks=0 exempt-entries-not-shrunk=0` / `fixed=6/7 exit=1`
(Caught for different reasons: content pin vs size floor. Same verdict.)

F3 ledger swapped for a DIFFERENT file with the same name, size >= floor (T2, 30752 bytes of unrelated content,
ledger sha `95298666f172f14...` vs base `07994f48...`; T2c, exactly 30696 bytes, sha `6d4a8513...`). Guard MISSES it;
this is the tree where v1.3 is strictly weaker than v1.2:
- T2  v1.2: `gate G6 pass=0 ... base-intact=0 entry-bytes-ok=1` / `fixed=6/7 exit=1`
- T2  v1.3: `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1` / `c2-gate fixed=7/7 exit=0`
- T2c v1.2: `gate G6 pass=0 ... base-intact=0` / `fixed=6/7 exit=1`
- T2c v1.3: `gate G6 pass=1 ... base-intact=1` / `c2-gate fixed=7/7 exit=0`
Bypass window: any content at all, provided `getsize >= 30696` and the name is unchanged. The name-pinned-non-shrink
guard is information-theoretically blind to this class: it never reads the ledger's bytes.

F4 same-name swap BELOW the floor (T2b, 18214 bytes different content). Floor binds; both red (v1.3
`exempt-entries-not-shrunk=0`, `fixed=6/7`). Confirms the F3 bypass is exactly the [floor, +inf) size window.

F5 ledger replaced by a symlink (T3, `considerthese-proposals-ledger.md -> claim-gates.md`). Guard CATCHES it; both red:
- v1.2: `gate G6 pass=0 read=symlinks=1 exempt-entries-not-shrunk=1` / `fixed=6/7 exit=1`
- v1.3: `gate G6 pass=0 read=symlinks=1 exempt-entries-not-shrunk=0` / `fixed=6/7 exit=1`
The entry-symlink check (`g6`, `:343`) is untouched by the exemption, so this class stays closed. (v1.3's secondary
reason differs: the symlink target is 15372 bytes, also under the ledger floor.)

F6 legitimate growth (T5, base ledger + the real `## Round-46 dispositions` append, 31111 bytes, base bytes kept as
prefix). The exemption does its job: v1.2 red (`base-intact=0`, `fixed=6/7 exit=1`); v1.3 green (`G6 pass=1 ... base-intact=1` / `fixed=7/7 exit=0`). Without the exemption the round's own planned append turns C2 red, which is why the amendment exists.

F7 inherited-hole control (T4): `claim-gates.md` — ALREADY exempt under committed v1.2 (CONTENT_EXEMPT, `:71`) —
swapped for 7128 bytes of different content (>= its 6742 floor). v1.2 reads GREEN today:
`gate G6 pass=1 ... base-intact=1` / `c2-gate fixed=7/7 exit=0` (and v1.3 identically). The F3 swap class is not new:
it ships in v1.2 for the two C1 re-grounded entries (mechanism ruled a counter erratum as C2-E5). v1.3 widens an
accepted hole by exactly one name; it opens no new hole class. The committed f29-gate shares the exposure:
`corpus/instruments/r46-f29-gate.py:323` checks `os.path.getsize(...) >= LEDGER_MIN_BYTES` only, ledger bytes never read.

F8 implementation discovery — the exemption CANNOT ship without editing a frozen pin. With CONTENT_EXEMPT extended but
PINS["base-knowledge-content"] left at `5e0796fd...836b8f47`, the mock read `gate G6 pass=0 ... base-intact=0` even on
the pristine T0 (fixed=6/7 on every tree). The pinned set shrinks 62 names -> 61, so the constant must be re-derived to
`2c4ccfb6...83a9a7`. Cross-check (same join/sha construction as `g6:338`, run against the pristine export):
62-name set -> `5e0796fd3617f7626880950a5b25d1818f58eff58a12dec99ce7a0f3836b8f47` (equals the frozen pin);
61-name set -> `2c4ccfb65fdb5b727a3bc0c2465f6091b535663abd81126b81e76fdaae83a9a7`.
PINS["base-knowledge-names"] (`bf304481...`) is unchanged — the ledger's NAME stays pinned under v1.3.

COUNTER-ERRATA QUESTION — side taken: BYTE-PIN AMENDMENT (logged erratum), not a kill-rule limb change.
The exemption amends a byte pin, quite literally: F8 shows PINS["base-knowledge-content"] cannot remain frozen. Four
defenses from the frozen record and precedent:
1. The attempt-2 claims pre-authorize this exact channel. claims.json (`.ufo/waves/round-46/attempt2/claims.json`),
   `note`: "The attempt-1 counters r46-c1-gate.py / r46-c2-gate.py are NOT edited by this round's claims (any amendment
   is a logged erratum)". The amendment is a dispatched, pre-announced seat item executed at L1 integration — the
   opposite of the silent post-scoring move the C1 kill rule's limb-sentence clause targets ("change AFTER a seat has
   scored").
2. The attempt-2 C1 kill rule's own remedy is broader than attempt-1's. Frozen text: "bug fixes are logged as errata in
   the attempt-2 errata file with a plain re-derivation that does not use the changed instrument". The attempt-1
   qualifier "that keep a limb's sentence" (quoted in `.ufo/waves/round-46/counter-errata.md`) is absent from the
   attempt-2 frozen sentence — so even read narrowly, a code change answered by an errata entry + plain re-derivation
   is the kill rule's prescribed path, not a firing condition.
3. Like-for-like precedent: C2-E5 (E1 table in counter-errata.md) reduced the byte pin's coverage set — "the byte pin
   covers 62 base entries — the two entries C1 re-grounds are exempt from the BYTE pin (their NAMES stay pinned)" — and
   was ruled a counter erratum. v1.3 is the same mechanism with the same shape (one more exempt name + re-derived pin).
   And the freeze commit fe0f56b itself already encodes this exemption for the C2 claim's own counter
   (r46-f29-gate.py:80-81,322-326, LEDGER_MIN_BYTES = 30696 = the ledger's size "at the freeze tip"); v1.3 harmonizes
   the C1 claim's counter with the freeze's sibling instrument.
4. E1's disclosed-rationale test is met at the artifact level: claim sentences, before/after values, targets and the
   kill rule's text stay byte-identical; only how the code reads a tree changes.

Teeth (conditions under which the classification survives, from the wave-2 ruling's accepted objection): the errata
entry MUST (a) disclose the G6 docstring edit as a NEW exemption, not "the sentence made literal" — the wave-2 critic's
objection was accepted in exactly these words for new-requirement code changes; (b) disclose the pass-set DIRECTION —
E1 disclosed "the v1.1 pass set is narrower than v1's ... and is disclosed, not hidden"; v1.3's pass set is WIDER on
the swap axis and F3 names the witness trees (T2/T2c pass v1.3, fail v1.2); (c) carry a plain re-derivation not using
the changed instrument (extend the counter-errata.md plain block with: name set pinned, ledger present, size >= 30696,
other 61 entries byte-pinned — all checkable with find/wc/sha256sum); and (d) land with or before the integration
commit. If any of (a)-(d) is skipped, the wave-2 ruling's narrow-reader fallback applies: C1 must be read UNVERIFIED on
the frozen counter until the re-derivation exists.

Does F3 "matter"? No claim sentence pins ledger content: the C2 after text walls it off ("absence sweep 2 -> 4 files
(README, SOURCES, the entry, + the ledger-class growth is separate)"), C1's after-value is about mutant grading, and
F7 shows the identical exposure is live in v1.2 for claim-gates.md. So the swap hole matters for disclosure integrity
(E1 discipline) and it MUST be disclosed per (b) above; it does not by itself defeat either claim's after-value.
Recommendation to L1 (one line, optional): upgrade the ledger's guard from size-floor to append-only prefix pinning
(pin the base ledger sha and require the current file's first 30696 bytes to hash to it) — T5 stays green, F3/F4 turn
red, cost is one sha256 over a prefix. The same upgrade could later be applied to the two C1 entries; that is outside
this round's amendment.

LIMITATIONS
- L1: the scout's spec `R46bScoutLedger.md` was not on disk when I ran; the exemption shape is modeled from the
  executor seat spec (wave1-spec.json:225) and the committed f29-gate precedent. If L1's final v1.3 differs (e.g.
  already pins a prefix), F3's miss must be re-run before integration.
- L2: I exercised gate code only. The mutbat battery / selftest machinery (the C1 claim's measurement) is out of this
  seat's scope; F8's pin re-derivation must be reproduced inside the real v1.3 by the executor, with a matching
  selftest case per their spec item (3) (a shrunk-ledger tree reading G6 red — F2/F4 confirm the guard supports such
  a case).
- L3: full-gate runs of the mock used my scratch lane mirror for TOOL_ROOT (source-recheck.py copied byte-identical,
  sha-verified against the gate's pin `fd2e01e8...`); G6 semantics are path-independent and the G6-only attack surface
  is unaffected.
- L4: T2/T2c swap bodies are synthetic junk; any >= 30696-byte same-name content behaves identically because the guard
  never reads the ledger's bytes. T3 uses an in-directory symlink target; out-of-tree symlink targets are caught by the
  same `:343` check.
- L5: f29-gate H6 was not attacked (seat R46bRevF29H6H7's scope); F7 notes only that H6 shares the F3 exposure by code
  inspection (r46-f29-gate.py:323).
- No /tmp evidence; commit-worthy output is this report plus the four receipts in `wave1/R46bRevLedgerAmend.draft/`.
