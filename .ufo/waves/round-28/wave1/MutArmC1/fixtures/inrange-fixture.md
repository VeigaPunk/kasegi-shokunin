# R28 MutArmC1 scratch fixture — bounties cite resolving inside a PRESENT root
Run with KASEGI_BOUNTIES=$SCRATCH/tmp/bounties-root (a real temp dir containing
ops/claim-check.mjs). Cite `~/Projects/bounties/ops/claim-check.mjs:1` must
classify in-range (kind=BOUNTIES). A mutant that ignores $KASEGI_BOUNTIES or
derives the root from the wrong candidates reports BOUNTIES-ABSENT — the wrong
absence verdict while the root is present.
