# kasegi round-42 claims erratum 2 — wording tightenings (pre-scoring)

Frozen claims: `.ufo/waves/round-42/claims.json`. Erratum 1 is appended at
`.ufo/waves/round-42/claims-erratum-1.md`. These items TIGHTEN ambiguous wording caught by wave-1
attack seats (`wave1/CritClaims.md` A2b/R-CRIT-1..3, `wave1/CritKillRule.md` token-hole and Meta
holes A/B); every change is in the direction of the claim's intent — no target moves, nothing is
narrowed into reachability. No seat had scored a claim when this was written.

- **E6 — F-TOKEN boundary class tightened.** The frozen text bounds a counted token by "non-digit,
  non-slash characters"; letters are non-digit non-slash, so `closed=13/13x` would satisfy it
  (`wave1/CritClaims.md` A2b-1, `CritKillRule.md` token-hole). The intent is a WHOLE token: the value
  is matched only when the full literal `closed=<n>/<m>` (resp. `failures=<k>`, `cases=<k>`) is
  bounded on both sides by a character that is not a letter, digit, `_`, `/`, or `-` — letter-adjacent
  (`13/13x`), digit-extended (`10/100`, `113/13`) and separator variant (`closed = 13/13`,
  `closed:13/13`, `closed 13/13`) forms all read as the mangled-value class and must be rejected.
  This is the same intended condition stated more precisely, per `CritKillRule.md`'s own observation
  that a literal reading forces acceptance of the class the fix exists to kill.

- **E7 — artifact-kill clause extended to every repaired family.** The frozen kill rule enumerates
  F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP (J1-J7). The predicate also repairs F-RCPT (J8)
  and F-CORR (J11); an in-family escape there — a committed artifact showing the CURRENT suite bytes
  accepting a forged-payload receipt or an undeclared verbatim-duplicated Correction block — fires the
  artifact-kill clause identically (CritClaims A2b-2, CritKillRule Meta-hole A). The intent "the claim
  is that the routed defects are closed" covers every repaired check; J9/J10/J12/J13 carry no family
  and stay outside the clause. The routed-not-kill line in `claim_design_lesson` reads with this
  enumeration.

- **E8 — replay-limb coverage clarified.** "EVERY repaired check carries a REPLAY limb" names the
  seven repair families J1-J7 and, for J11, the committed lane-state duplication (a lane file, not a
  wave-2 artifact — replayed as a synthetic unmarked duplication per E2). J8's replay is the
  committed forgery classes it inherits from r41 I2/I8 (payload-contradiction, future-dated,
  foreign-ref, nonexistent-ref, summary-only, tampered-payload-line — replayed, not merely asserted).
  J9/J10/J12/J13 have no committed defeat artifact to replay; their graded selftest mutants are the
  required negative evidence (CritKillRule Meta-hole B resolved: absence of a replay limb on
  J9/J10/J12/J13 is not itself a kill — absence on J1-J8/J11 is).
