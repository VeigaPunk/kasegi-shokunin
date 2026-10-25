# AttackE2 — S040 fingerprint + final URL (combined s2 probe × round-25 verifier note)

Seat: L1Kasegi26.AttackE2 (revenger, read-only leaf). Round 26, wave 2. Date: 2026-10-25 (UTC). Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Assignment

Combine the wave-1 s2 probe with the round-25 verifier note into one fingerprint: canonical URL → 301 → final URL → 200 under instrument UA; browser UA 403; S040-live.txt sha256 b7f7b55f… equals round-25 snapshot; S040 recheck cell bare `180d` with final URL/UA recorded in `## Registry changes`. Output `wave2/e2.md`; report at `wave2/AttackE2.md`.

## Reconstructed contract (the fingerprint)

| # | Clause | Source half | Verdict |
|---|---|---|---|
| 1 | canonical URL → 301 → final URL → 200 under instrument UA (2 hops) | s2 probe + r25 verifier | holds |
| 2 | browser UA 403, zero redirects | s2 probe + r25 verifier | holds |
| 3 | S040-live.txt sha256 b7f7b55f… = round-25 snapshot, byte-identical | s2 probe; re-verified locally | holds |
| 4 | S040 recheck cell bare `180d` (cadence-only) | current SOURCES.md row | holds |
| 5 | final URL/UA recorded in `## Registry changes` | current SOURCES.md | holds |

## Evidence chain

### Clause 1 — instrument UA redirect chain
- **Wave-1 s2 probe** (`wave1/ScoutS040Probe.md`, `wave1/s040-probe.txt`, leaf L1Kasegi26.ScoutS040Probe, 12:34:25Z–12:34:27Z): exact `curl -s -D - -o /dev/null -L -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"` on the canonical URL.
  - hop 1 `HTTP/2 301` (Apache, cdchost wemxweb-publish-prod1-05) → `https://tools.cisco.com/security/center/resources/security_vulnerability_policy.html`
  - hop 2 `HTTP/1.1 302 Found` → `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`
  - hop 3 `HTTP/2 200` (sec.cloudapps.cisco.com; `content-type: text/html;charset=ISO-8859-1`) — write-out `final=… code=200 num_redirects=2`
- **Round-25 verifier note** (`corpus/lessons/round-25-verifier-spotcheck.md`, S040 discernment row): "instrument UA (`capture-source.py:32`) `curl -L` → 301 → `sec.cloudapps.cisco.com/…/security_vulnerability_policy.html` http 200, 94,027 B"; R25-5: "The registry URL now 301-redirects to `sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`".
- **Live re-probe (this seat, 2026-10-25T12:51:04Z–12:51:06Z)**: same commands; observed `HTTP/2 301` (Apache, `location: https://tools.cisco.com/security/center/resources/security_vulnerability_policy.html`) → `HTTP/1.1 302 Found` → `Location: https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` → `HTTP/2 200` (`text/html;charset=ISO-8859-1`); write-out `final=https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html code=200 num_redirects=2`. Chain unchanged 17 minutes after the probe.

### Clause 2 — browser UA 403
- **s2 probe**: `HTTP/2 403`, server `AkamaiGHost`, content-length 465, no Location; `final=<canonical> code=403 num_redirects=0`. "Browser UA must not be used."
- **r25 verifier**: "browser UA → http **403** (as the lesson's access note says)".
- **Live re-probe (12:51:04Z)**: `HTTP/2 403`, `AkamaiGHost`, content-length 465, `num_redirects=0`. Unchanged.

### Clause 3 — snapshot equality
- **s2 capture log** (capture-source.py on the final URL, instrument UA): `S040 status=200 fetched_bytes=94027 snapshot_bytes=33463 sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c utc=2026-10-25T12:34:27Z out=…/round-26/S040-live.txt`, exit 0; "byte-identical to round-25 corpus/source-snapshots/round-25/S040.txt".
- **Local re-verification (this seat)**:
  - `sha256sum corpus/source-snapshots/round-26/S040-live.txt` → `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`
  - `sha256sum corpus/source-snapshots/round-25/S040.txt` → `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`
  - `cmp -s round-26/S040-live.txt round-25/S040.txt` → exit 0 (byte-identical).
- The r25 verifier also pins the same digest family: "Capture digests `sha256sum S036..S040.txt` prefixes `022ca4f4 b204aa7f 09e077d3 657e7b4c b7f7b55f` = manifest sha256 fields" (round-25 manifest).

### Clause 4 — bare cadence cell
- `corpus/SOURCES.md` registry row S040, parsed cell-by-cell (`awk -F'|' '$2 ~ /^ *S040 /`): col 11 (recheck) = `180d` — no prose. S041 col 11 = `180d` likewise.
- Context: lesson M26-5/C2-kill-rule item — the cells were restored from `180d — <prose>` to cadence-only exactly because E09 rejects prose; `## Registry changes` documents the restore.

### Clause 5 — Registry changes record
- `corpus/SOURCES.md` `## Registry changes` contains, verbatim:
  - `S040 recheck cell old → new: `180d` → `180d — final URL https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html (2 redirects); instrument UA required (browser UA 403s)` (R25-5).`
  - `S040 recheck cell restored old → new: `180d — final URL https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html (2 redirects); instrument UA required (browser UA 403s)` → `180d` (cadence-only cell; the final-URL/UA requirement is recorded here and in the round-26 lesson, per census rule E09).`
- Final URL, two-redirect chain, instrument-UA requirement and browser-UA 403 all present. (S041's fetch-procedure record is there too.)

### Supporting checks (run by this seat)
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok …` exit **0**; only pre-existing warnings W04 S028/S029. The bare `180d` cells parse under the NNd grammar (E09 clear).
- `corpus/instruments/knowledge-expected.txt` → 39 non-comment entries (matches landed live-audit 39/39).
- Round-26 `manifest.json` (`schema_version 1`, purpose "round-26 captures for F11 admission") → `sources` = [S041] only, 7 quotes; `S040-live.txt` carries no manifest record (it is the R25-5 drift-fix snapshot; equality evidence = direct byte-compare above).

## Divergences / open items

1. **Chain phrasing**: the assignment shorthand ("canonical URL → 301 → final URL → 200") and the R25-5 note compress the chain; the measured chain is two redirects — 301 → `tools.cisco.com` → 302 → `sec.cloudapps.cisco.com` → 200. Current files are consistent: `## Registry changes` says "(2 redirects)" and the round-26 lesson M26-5 says "two-hop redirect chain". No divergence in the current tree.
2. **S040-live.txt not manifest-bound**: the round-26 manifest binds only S041; S040-live.txt's equality to round-25 is verified by the file compare, not by a manifest entry. If a future instrument wants manifest binding for drift snapshots, S040-live.txt would need a record — not part of this fingerprint.
3. **Fingerprint temporal validity**: clauses 1–2 were re-probed live at 12:51Z (same behavior as 12:34Z). Clause 3 is a static file equality and holds indefinitely for the committed bytes.
4. **Browser-UA negative is UA-specific**: 403 is observed for the Chrome/126-style UA string; the contract "browser UA 403" is recorded for that probe string, not for all possible browser UAs.

## Confidence

High — every clause is backed by two independent records (s2 probe + r25 verifier) and three clauses were re-verified locally/live by this seat (hash compare, cell parse, live probes, census). No fabricated figure: all commands and outputs are reproduced above.

## Scope / writes

No production edits. Writes this seat: `wave2/e2.md` (fingerprint) and `wave2/AttackE2.md` (this report). No tools installed (curl/system + lane instruments only).
