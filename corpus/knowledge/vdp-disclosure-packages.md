# VDP disclosure packages — the free-disclosure sibling

Source: `[lost-tree] vdp-disclosures/anthropic-plugin-dev-cmd-injection/`
(all 4 files read) + `claims/hackerone-{ruby,nextcloud}/honest-zero-vdp-no-payout/`
status.json. Read 2026-09-28.

## Shape — different contract from `claims/*/`

`vdp-disclosures/<slug>/` carries four files, NOT the six-file claim contract:

| File | Content |
|---|---|
| `ROUTE.md` | Channel + attribution decree. Observed: "Free disclosure, ATTRIBUTED"; official VDP intake via security.txt `Contact:` → HackerOne **embedded_submissions** URL (`hackerone.com/<uuid>/embedded_submissions/new`), not the program's bounty form. "No payout requested or accepted." "Operator sends personally — submissions are never fleet-executed." |
| `cover-note.md` | Short operator-facing cover text prepended at send time (this package: a rickroll joke line — operator's choice, his attribution). |
| `[lost-tree] vdp-disclosures/<slug>/report.md` | Same craft contract as claim reports: title; "Disclosed freely by" attribution line; program + official policy URL; affected asset + commit + file + source sha256; CWE class; suggested severity with full CVSS vector; verbatim "Scope excerpt" with observed_at + bundle sha256. |
| `SUBMITTED.md` | Post-send record: timestamp, channel, verbatim platform confirmation string, attribution identity, CWE, evidence note. |

## Semantics

- **Free + attributed is a decree, not a default.** Operator decree 2026-09-06:
  full attribution, "let them know full damn well who is giving out free
  vulns." Attribution identity: `vgpnk1337@gmail.com`.
- VDP intake can be the vendor's `security.txt` Contact route even when the
  vendor also runs a paid HackerOne program — the disclosure bypassed the
  bounty queue deliberately.
- Sibling packages `claims/*/honest-zero-vdp-no-payout/` show the flip side:
  VDP-adjacent programs parked as honest-zero (`[lost-tree] claims/*/honest-zero-vdp-no-payout/report.md` + `status.json`
  only — the two-file minimum is what a parked VDP package looks like in
  claims/).
- Same external-effect rule applies: the operator personally submits; the
  fleet stages, never sends.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/vdp-disclosures/anthropic-plugin-dev-cmd-injection/ and claims/hackerone-ruby/ and claims/hackerone-nextcloud/ honest-zero-vdp-no-payout status.json records.
verified-at: 2026-09-28
recheck: on-restoration — test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/vdp-disclosure-packages.md (fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15)
