# RevErratumLanding — round-40 lesson erratum review

## Findings

No actionable erratum defect found for the assigned D4/D5 corrections. The appended section is explicitly append-only: lines 267–268 say no committed line above is edited. It describes, rather than silently rewrites, the historical defects: duplicate `## Gate` at original L29/L31 (L270–272), and census typo `+3?mined` / unmatched parenthesis (L273–277). The correction explains the intended census reading by pointing to the falsification section's own recorded reading (L243–245). The original lines remain visibly unchanged at L26–31, so this preserves history while making the erratum unambiguous.

D5 recount from the committed round-40 dispatch JSONs in the integrated tree (`ad7147532cb702b0d541d40499874552183d9132`): parsed each `registry.members` object's `role` values and summed reviewer + critic + mutation-tester.

```text
wave1-dispatch.json members 54 roles {'executor': 18, 'scout': 11, 'reviewer': 12, 'scribe': 6, 'connector': 1, 'sentinel': 1, 'critic': 3, 'mutation-tester': 2} attack 17 share 17/54=31.5%
wave2-dispatch.json members 35 roles {'reviewer': 12, 'critic': 7, 'mutation-tester': 6, 'scout': 8, 'connector': 1, 'sentinel': 1} attack 25 share 25/35=71.4%
combined 42 / 89 = 47.2%
```

Thus the appended D5 arithmetic (25/35 and 42/89) is correct; it retains the original totals and identifies the specific role-sum transcription error, not a role-definition ambiguity. Original L9's 33/35 and 50/89 remain as historical text, explicitly identified as wrong by the append-only erratum.

## Residual risk / verification limits

Text/source review and a direct JSON role recount only; no final Y verification claimed. The erratum's own dispatch references (wave 1 and wave 2 JSON) are present in the committed round-40 tree. No writes beyond this receipt; no tools installed.