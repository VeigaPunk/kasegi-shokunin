# ScribeQuarantine — Finalized quarantine verdicts table (round 30, wave 1)

Role: UFO-FSD scribe (leaf; no subagent dispatch). Task: finalize the quarantine
verdicts table for the lesson by reading `ExecQuarantineFetch` verdicts and
`ConnQuarantine` joins; produce one row per slice id; verify each verdict has a
matching evidence line.

Axes: **coverage** (all 7 slice ids in the table, verdict+evidence per row) and
**depth:verifiability** (every verdict bound to measured bytes/HTTP results; joins
consistent with executor and reviewer).

## Inputs (bytes measured, sha256)

- Slice `assimilation/quarantine-slice` — `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862` (7 rows; ScoutQuarantineSlice).
- `ExecQuarantineFetch.md` — `74d7cb458dab575480070d7781fa8942b4af9754af90b44ff48184003bdea0c2`.
- `ConnQuarantine.md` — `01359555369bb3711aba86a480038a3d6534582330af2ed68c8fde811f6e035d`.
- `RevQuarantineInd.md` — `c5d7f739e8007dbb20fc14a34e79b83095b442eb50ae1af6481445305e8cb05f`.

## Finalized verdicts table (one row per slice id)

| id | verdict | evidence | note |
|---|---|---|---|
| S037 | `fetched-no-quote` | ExecQuarantineFetch: GET 200, 24,189 B, HTML sha256 `9cba2e96…`; register composite quote not located as an exact sequence — components present (standard name line 446; status `现行` 468; dates 520/527). RevQuarantineInd agrees the data is present (disagrees with the register's ABSENT/fabrication reading). | ConnQuarantine: `unrelated` to F14 (SAMR/SAC Chinese grading catalogue); registers no lane row; if ever adopted, needs a new sequential lane id (never arithmetic — staged S037 collides with lane S037 Cybozu FAQ). Not appendable this round (quote not verifiable as named). |
| S054 | `fetched-no-quote` | ExecQuarantineFetch: GET 200, 513,648 B PDF, PDF sha256 `0150c9d1…`, pdftotext sha256 `ce7e3b1e…`; register quote `脆弱性の悪用が確認されたもの又は疑われるもの` present only split across PDF line break (lines 42–43), not a contiguous source sequence. RevQuarantineInd: quote now verifiable in the local capture (line 15); register's ABSENT class is stale for a fresh fetch. | ConnQuarantine: `related-to-F14` in publisher lineage (IPA/Cabinet Office statutory notification) but **isolated** — the F14 entry does not cite S054 (it cites S046/S047/S041); S054 feeds an out-of-round amendment. Quarantine status does not block or contaminate F14 admission. Not appendable this round. |
| S048 | `unfetchable` | ExecQuarantineFetch: GET 404, 748 B, body sha256 `95cd25d8…` (GB detail JSP not found); no quote check possible. RevQuarantineInd agrees (404 page, not the standard payload). | ConnQuarantine: `unrelated` (SAMR/TC260 plan record); no lane row; new sequential id if ever adopted. Not a fabrication; remains unverified. |
| S065 | `reachable-quote-located` | ExecQuarantineFetch: GET 200, 7,465,472 B PDF, sha256 `e33b0f67…`, pdftotext sha256 `96e6dfb9…`; locators found (`现行有效法律目录（303 件）` line 1; `刑法（7 件）` 778; `中华人民共和国刑法` 779). | Not cited by any admitted lane entry → **not appended regardless of reachability** (Exec's boundary note; Conn: `unrelated`, NPCSC, new sequential id if adopted). |
| S068 | `already-mined-by-document` | ExecQuarantineFetch: register URL byte-equal to lane S040 `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`; fresh fetch redirected 200 (94,027 B, sha256 `098f99a8…`), corroborates S040's named headings. ConnQuarantine: lane S040 exists (`SOURCES.md:46`, round-25 capture `S040.txt` sha256 `b7f7b55f…`). | Duplicate row — do **not** append; mapped to existing lane S040 (document identity, zero new id). `unrelated` to F14 (US vendor PSIRT). Closes the unreachable defect locally without network reliance. |
| S069 | `unfetchable` | ExecQuarantineFetch: full staged URL used (`SOURCES.append.md` line 45; register URL truncates at directory); curl followed redirect to `kass.sacinfo.org.cn/kfs/token/download/vxifveuymcpcltva` → HTTP 302/0 B then TLS verification failed (curl exit 60); no `-k` bypass. No quote check possible. | ConnQuarantine: `unrelated` (TC260/CNITSEC draft); new sequential id if ever adopted. **Flip vs round-29 lesson record** (which logged `reachable-quote-located` under the full staged URL): today's verified-fetch attempt fails on the tokenized attachment host's incomplete TLS chain. Package's own recheck notes for this host require a documented `-k`/http fallback — left as an L1 decision (strict-verify vs documented-fallback policy), not a fabrication. |
| S070 | `unfetchable` | ExecQuarantineFetch: full staged URL (`SOURCES.append.md` line 46) → redirect to `kass.sacinfo.org.cn/kfs/token/download/wucmbasjbyjeubbr` → 302/0 B, TLS verification failed (curl exit 60); no `-k` bypass. | ConnQuarantine: `unrelated` (TC260/CNITSEC drafting note); new sequential id if ever adopted. Same flip/boundary as S069 (identical directory-ending register locators). |

## Verification that every verdict has a matching evidence line

- All 7 slice ids (S037/S054/S048/S065/S068/S069/S070) appear exactly once above, each with a
  `verdict` cell referencing a specific `evidence` line in `ExecQuarantineFetch` (HTTP status,
  byte size, sha256, or URL byte-equality) — 7/7 paired.
- Cross-check vs `ConnQuarantine`: relatedness (6 `unrelated`, 1 `related-to-F14`-but-isolated)
  and required-lane-id mapping (1 existing match S068→S040; 6 new-sequential-id-if-adopted)
  are recorded in the note column; no contradiction with Exec verdicts.
- Independent reviewer sample (`RevQuarantineInd`, 3/7: S037/S054/S048) agrees with the verdict
  framing: S037 content present but not contiguous (no fabrication), S054 quote now verifiable
  (no longer unsupported), S048 confirmed 404/unverified.

## Gate outcome for the lesson

- **None of the 7 rows is adopted this round.** S037/S054 not appendable (named quote not
  located as contiguous source text); S048/S069/S070 unverified; S065 uncited by an admitted
  entry; S068 already mined as S040.
- S054's `related-to-F14` lineage does not touch the F14 admission (entry cites S046/S047/S041
  only) — F14 gate is clean of quarantine defects. This is the consistency guarantee the
  connector's join provides.
- Register-class reassessment: S037/S054 are classified `payload-absent` ("fabrication class")
  in the register, but hand-check shows their content exists in separated fields/lines — the
  class label is not upheld as fabrication; the rows remain unappendable for quote-contiguity
  and unverified reasons, not for fabrication.

## Tooling / bounds

- No tool installed or upgraded (standard `read`, `grep`, `sha256sum`, `curl` used by sibling
  seats; no installs to record). No write outside the lane working tree; no git/jj mutations;
  no live bounty target contacted.
