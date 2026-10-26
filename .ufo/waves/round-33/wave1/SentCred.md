# SentCred — round-33 credential & live-target sweep over wave receipts

Seat: SentCred (leaf sentinel). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` write scope; lane base `690b69da`, claims-freeze `6e55c8d5`.
Sweep filed 2026-10-26T01:31-03:00 over the then-landed wave state (final re-check 01:33: **43 other seats' receipts plus this one = 44 files of 64 dispatched**), covering every round-33 lane file (changed vs base + untracked + the whole `.ufo/waves/round-33/` tree), the new entry, the new instrument, the eight upgraded manifests and the round-32 manifest.
Answering model: `opencode-go/deepseek-v4.1-flash` (config route table; the item does not depend on it).
Tooling: nothing installed or upgraded (no pacman, no uv/npx; `grep`, `find`, `python3` pre-existing).

Scanner (read-only, kept in scratch, deleted at yield): a receipt contact classifier that marks a host **contacted** only when a receipt line carries a fetch verb (`curl`/`wget`/`capture-source.py --url`/`urlopen`) **or** a fetch-result token (`http=`/`status=`/`code=`/`HTTP 2xx`/`final=`) on the line or within four lines of one; plus a masked credential-shape detector that prints line numbers and token shapes, never values. No network call was made by this seat.

## 1. Host contacts — every host contacted this wave, by seat

```console
$ python3 $S/receipts.py | grep -E '^##|contacted_hosts=\[' | paste - -
## CritC2Kill.md          contacted_hosts=['security.360.cn', 'zc.cnvd.org.cn']
## ExecQuarantine.md      contacted_hosts=['openstd.samr.gov.cn', 'www.ipa.go.jp']
## ScoutLiveDrift.md      contacted_hosts=['security.360.cn', 'zc.cnvd.org.cn']
## ScoutPackageThemes.md  contacted_hosts=['kass.sacinfo.org.cn', 'openstd.samr.gov.cn', 'sec.cloudapps.cisco.com', 'std.samr.gov.cn', 'www.ipa.go.jp', 'www.npc.gov.cn']
$ python3 $S/receipts.py | tail -1
CONTACTED_UNION=['kass.sacinfo.org.cn', 'openstd.samr.gov.cn', 'sec.cloudapps.cisco.com', 'security.360.cn', 'std.samr.gov.cn', 'www.ipa.go.jp', 'www.npc.gov.cn', 'zc.cnvd.org.cn']
```

Literal command grep over the same set, for the record:

```console
$ cd .ufo/waves/round-33/wave1 && grep -nE '(^|[^A-Za-z])(curl|wget)([[:space:]]|$)' *.md
CritC2Kill.md:122:curl -sS -L -A '<UA>' https://zc.cnvd.org.cn/news/helpList      → http=200 bytes=56674
CritC2Kill.md:123:curl -sS -L -A '<UA>' https://security.360.cn/Reward/rules       → http=200 bytes=427391 (PDF, 21 pages)
ExecQuarantine.md:99:$ curl -sS -L --max-time 90 -A "$UA" -o S037.html -w 'S037 http=%{http_code} …' 'https://openstd.samr.gov.cn/…'
ExecQuarantine.md:101:$ curl -sS -L --max-time 120 -A "$UA" -o S054.pdf -w 'S054 http=%{http_code} …' 'https://www.ipa.go.jp/…'
ScoutPackageThemes.md:3: … "Network: seven GETs of the quarantine-slice documentation URLs only (instrument UA …, `curl -m 90`, no `-k`, no TLS bypass)" …
ScoutPackageThemes.md:110: … `same 302 + curl 60`
```

`ScoutLiveDrift`'s fetches are `capture-source.py --url …` lines (`ScoutLiveDrift.md:7,9`), not `curl`. **ScoutPackageThemes records fetch results (URL + status) rather than its literal command lines** — the only seat whose command form is not reproduced verbatim; its UA, timeout, no-`-k` and time window are stated at `ScoutPackageThemes.md:3`. Auditability observation only: no safety gap, and its scratch bytes were removed before yield (no `ScoutPackageThemes` directory under `/fast/scratch/hyaku/kasegi-r33/`).

The other 32 receipts state no fetch (each with an explicit negative — e.g. `ConnSibling.md:174` “No fetches, no live-target contact, no git/jj mutations, no installs.”; `ScoutF16Sweep.md:106`; `ExecBeforeReceipts.md:321`; `CritExpansion.md:5`). The classifier also lists `SentCred.md` (`sec.cloudapps.cisco.com`): that is this receipt's own §1 redirect-chain citation, not a contact by this seat. `shokunin.invalid` enters the union for the same textual reason — it is the placeholder domain inside the instrument UA string printed on `RevRowS050`'s `curl -A` line, not a fetch target.

| host | seat(s) | evidence (receipt:line) | class |
|---|---|---|---|
| `zc.cnvd.org.cn` | ScoutLiveDrift, CritC2Kill, ScoutManifestAudit(no fetch) | `ScoutLiveDrift.md:7,8` `status=200`; `CritC2Kill.md:122` `http=200 bytes=56674` | **allowed** (S049 registry URL) |
| `security.360.cn` | ScoutLiveDrift, CritC2Kill | `ScoutLiveDrift.md:9,10` `status=200`; `CritC2Kill.md:123` `http=200 bytes=427391` | **allowed** (S050 registry URL) |
| `openstd.samr.gov.cn` | ScoutPackageThemes, ExecQuarantine | `ScoutPackageThemes.md:86` `code=200 size=24189`; `ExecQuarantine.md:99,100` `S037 http=200 bytes=24189` | documentation (standards catalogue), payload-absent hand-check |
| `www.ipa.go.jp` | ScoutPackageThemes, ExecQuarantine | `ScoutPackageThemes.md:87` `code=200 size=513648`; `ExecQuarantine.md:101,102` `S054 http=200 bytes=513648` | documentation (statutory notice PDF) |
| `std.samr.gov.cn` | ScoutPackageThemes | `ScoutPackageThemes.md:88` `code=404 size=748` | documentation, unreachable class |
| `www.npc.gov.cn` | ScoutPackageThemes | `ScoutPackageThemes.md:89` `code=200 size=7465472` | documentation (statutory PDF) |
| `www.cisco.com` → `tools.cisco.com` → `sec.cloudapps.cisco.com` | ScoutPackageThemes | `ScoutPackageThemes.md:90` `301 www.cisco.com/… -> tools.cisco.com/… -> final=https://sec.cloudapps.cisco.com/…` | documentation, redirect chain |
| `kass.sacinfo.org.cn` | ScoutPackageThemes | `ScoutPackageThemes.md:91,92` `curl_exit=60 code=302 … "unable to get local issuer certificate"` | documentation attachment host, TLS-refused, **no body** |

All seven GETs of the quarantine slice used the instrument UA and no TLS bypass, and none is a bounty target. `ScoutPackageThemes.md:3`: “Network: seven GETs of the quarantine-slice documentation URLs only (instrument UA `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, `curl -m 90`, no `-k`, no TLS bypass)”.

**O1 — observation, not a breach: the five unreachable-class rows were re-fetched although the item's sentence for that class is “mark unverifiable, not fabrication”.** The seat was told to read the register, and the register's own remedy for the `unreachable` class is “re-fetch, or mark the row unverifiable — do NOT call it a fabrication” (`ScoutPackageThemes.md:83`, quoting the register lines 322-326). It took the re-fetch option on S048/S065/S068/S069/S070. Public documentation only; no credential; no live target; the item text does not name those URLs, so the contact rests on the register clause rather than the item — record the basis in the lesson Gate. Smallest remediation: one line in the Gate citing that clause per row (no code change).

**O2 — narrowed after the 01:32 re-check: one seat's fetch is still undisclosed.** `RevRowS050.md:16-42` landed and discloses both fetches (capture with instrument UA, `S050 status=200 … utc=2026-10-26T04:18:48Z`, fresh sha equal to the committed file; HEAD probe `http=200 redirects=0`). `RevRowS049.md` landed and states no target was re-fetched (`RevRowS049.md:155`). A `PHPSESSID` cookie set by the S050 response is named without any value (`RevRowS050.md:45`), and no cookie value exists lane-wide (`grep -rInE 'PHPSESSID|Set-Cookie|Cookie:'` over `round-33` + `corpus` → 1 hit, that sentence). **`RevGateSpot.md` had not landed at 01:32**, although its scratch holds fresh S049/S050 conversions whose hashes equal the committed captures (evidence below):

```console
$ sha256sum /fast/scratch/hyaku/kasegi-r33/RevGateSpot/S049-fresh.txt /fast/scratch/hyaku/kasegi-r33/RevGateSpot/S050-fresh.txt /fast/scratch/hyaku/kasegi-r33/RevRowS050/S050-now.txt
962a451a…1cb8  RevGateSpot/S049-fresh.txt
2f9c6406…6888  RevGateSpot/S050-fresh.txt
2f9c6406…6888  RevRowS050/S050-now.txt
```
Those hashes are the committed capture hashes (`corpus/source-snapshots/round-32/S049.txt`, `S050.txt`); `RevRowS050/rules.pdf` (427,391 B) is the S050 raw body size. At 01:31 none of `RevRowS049`/`RevRowS050`/`RevGateSpot` had a receipt; by 01:32 the first two had landed and both disclose or disclaim fetches as above, so only `RevGateSpot` remains pending. When it lands, its receipt must state the fetch and its URL. No other scratch evidence of a contact exists: files newer than the wave spawn that carry HTTP-status lines are lane copies under fixture trees (`MutEntryF16/lane/…`, historical round receipts), not fetches.

### Findings register (this item's surface)

| id | severity | finding | exploit path / impact | smallest remediation |
|---|---|---|---|---|
| N1 | — | No credential material in any round-33 file; S049/S050 captures clean by shape audit | none reachable | none |
| N2 | — | No live bounty target contacted or cited; `~/Projects/bounties` absent | none reachable | none |
| N3 | — | No seat wrote under the fleet root, a sibling lane or shokuknow; fleet `MANIFEST.json` content unchanged | none | none |
| O1 | low | `ScoutPackageThemes` re-fetched five `unreachable`-class documentation URLs (S048/S065/S068/S069/S070) whose item sentence says “mark unverifiable”; the register it was told to read permits “re-fetch, or mark … unverifiable” | seven public GETs beyond the item's named URLs; no target interaction, no credential, instrument UA, no TLS bypass | one Gate line per row citing the register clause (§1 O1) |
| O2 | pending | `RevGateSpot` fetched S049/S050 (scratch hashes match the captures) with no landed receipt at 01:32 (the other two seats have landed and disclosed/disclaimed) | undeclared-so-far contact **inside** the allowed set | its receipt must state the fetch + URL; `SentScopeFinal` re-checks on quiescent bytes |
| A1 | low (adjacent) | `CritC1Kill` claims scratch removal while its scratch dir persisted | scratch residue only | owner `ExecScratchDiscipline` |
| A2 | informational | `ExecCaptureBinding` writes 16 sidecar `.txt` files in a `wave1/ExecCaptureBinding/` dir | widens the literal receipt-path ownership wording | none |
| A3 | informational | `ExecBeforeReceipts` copied fleet `shokunin.conf` into scratch | none — config carries no secret/URL | none |

## 2. Credential material — none in any round-33 file

```console
$ grep -rInE 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-|BEGIN [A-Z ]*PRIVATE KEY' --exclude-dir=.git --exclude-dir=.jj .
-> 5 hits, all round-28 prose that *names* the pattern (e.g. SentinelScope.md:15 "only benign `token`/`backticked tokens` doc words")
$ grep -rInE 'op://[A-Za-z0-9_-]+/[A-Za-z0-9]' --exclude-dir=.git --exclude-dir=.jj . | wc -l
0
$ grep -rIE '(password|passwd|api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/+=._-]{6,}' --exclude-dir=.git --exclude-dir=.jj . | wc -l
0
```

- **Captures (unchanged this round).** `git status corpus/source-snapshots/round-32/` shows only the new `manifest.json`; the two captures keep their round-32 hashes. Shape audit of the S049 page — the one page the item names as credential-adjacent — over all 426 lines: `PEM blocks: 0`, `base64-like lines: 0`, `username-assignment lines: []`, `password-assignment lines: []`, `ip-address count: 0`. S050: 0 PEM, 0 base64, 0 password/username assignments, 0 IPs. The keyword lines are **retrieval instructions**, not issued values: lines 202 and 205 say, in effect, that tester VPN account/password details are obtained through a described procedure — a description of a retrieval route with no value present (not quoted here, bound 8; the masked detector finds no value token after either keyword). The one value-shaped token (line 421, after an “official mailbox account” label) matches an email regex with `nonascii=0`; its domain is the public `cert.org.cn`: a public contact address, not a credential (local part not reproduced).
- **New entry** `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`: `账号 0 / 帐号 0 / 密码 0 / 口令 0 / VPN 2 / openvpn 0`; the two VPN hits are the Q6 disclosure at lines 181-182, which states that the material is “**not reproduced** here” and that “no account, password, profile or certificate value appears in this entry” — locations named, values absent. Its four URLs are the two registry URLs plus `https://security.360.cn/Product/product` and `http://www.cnvd.org.cn/`. The Q6 block names capture *line ranges* (202-205, 398-406) and a section heading; those are locations, not material.
- **Receipts**: twelve carry a credential keyword (`CritBoundary.md:132-145`, `ExecCensusDry.md:228`, `ExecEntryF16.md:89`, `ExecManifest32.md:100`, `ExecRegistryAppend.md:249`, `RevEntryF16.md:42,146`, `RevRowS049.md:74,77`, `RevRowS050.md:116-122`, `ScoutF16Sweep.md:89`, `ScoutLiveDrift.md:29`, `SentScopeFinal.md:90,105,115-117`, and this receipt) — every one is a “not quoted / not reproduced” statement. Masked scan over all receipts prints no value-shaped token after a credential keyword.
- **Independent corroboration (three seats).** `RevEntryF16.md:42` scores Q6 `pass`; `SentScopeFinal.md:15` prints `F3 CLEAN` “no credential, session or private-URL material in any new or changed file” (its `credsweep.py` uses `op://|token|secret|api[_-]?key|bearer|password|账号|密码` over base..work and finds only the Q6 disclosure). `CritBoundary.md:143-150` ran its own capture audit with a wider pattern set and reports that “S049.txt has 34 lines matching `密码|口令|password|passwd|账号|帐户|VPN|OpenVPN|证书|profile`”, with two sliding-window matches against the entry, both URL fragments (`'ps://zc.cn'`, `'http://www'`) and “no credential text emitted” — the same conclusion as the masked scan above, from a second implementation.
- **New/modified docs** (`SOURCES.md`, `README.md`, `QUALITY.md`, `instruments/README.md`, `PROVINCE.md`, `SKILL.md`): 0 credential keywords. `SHONEN.md` and `SCORECARD.md` were not yet written at sweep time.
- **Manifests**: the eight upgraded manifests and `round-32/manifest.json` carry only registry URLs (byte-exact host/URL list verified against `corpus/SOURCES.md`); `ExecManifest32.md:103` records the marker grep over the manifest returning no output.

Severity: none. No session URL, no private URL added, no vault reference (`op://` actual-URI occurrences lane-wide: 0; the only `op://` strings are the pattern text in the round's own dispatch files and one historical template line).

## 3. Live bounty targets — none contacted, none cited as reachable

- No `hackerone.com/<program>`, `bugcrowd.com/<program>`, `intigriti`, `yeswehack` or `synack` program page appears in any round-33 file. The only `hackerone.com` URL is `https://hackerone.com/security/policy_versions` — registry row S043's own documentation page — and the only bugcrowd URLs are `docs.bugcrowd.com/…` / `raw.githubusercontent.com/bugcrowd/…` registry rows.
- `~/Projects/bounties` — `test -d ~/Projects/bounties` → **ABSENT** (as of 2026-10-26T01:29-03:00); it appears in 0 round-33 receipts and 0 new knowledge files. The 77 lane-wide `Projects/bounties` lines are historical `LOST-TREE` provenance lines in legacy entries (e.g. `corpus/knowledge/citation-bases.md:47,60,97`) plus this seat's own dispatch text.
- Off-registry hosts in the URL census are non-contacts: truncated fragments in the L1's `l1-ref/sid-url.tsv` and in `ScoutDatawalk.md` (column-width cuts, `https://docs...`, `https://…`), `fixture.example` (the instrument's selftest fixture host), `www\.first\.org` (an escaped regex in a receipt), and `app.devin.ai/org/veigapunk/wiki/…` — one line in `LOG.md` at HEAD (`LOG.md:1110`), a historical lane-wiki link, unchanged this round (`git log -1 -- LOG.md` = freeze commit `6e55c8d`, and `git diff LOG.md` empty; the L1 owns LOG.md).

## 4. Scope — no seat wrote under the fleet root, a sibling lane, or shokuknow

**Fleet root** `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) lists only orchestrator state: 16 `.ufo/state/<lane>.report-baseline` (17 at the 01:32 re-read, another lane having closed), `.ufo/watchdog.log` (event lines such as `2026-10-26T01:10:54-03:00 launch kasegi round=33 pgid=99020 driver=hyaku-inline attempt=1`), `scripts/hyaku/hyaku.env` + `lane-addendum.md` (the run-8 role map), and untracked orchestrator artefacts (`disk-guard.log`, `inline-dispatcher.log`, `.scratch/goal-20261026-hyaku-run8.md` 01:05) plus three untracked entries that predate the wave (`.tower/` 2026-10-25 03:48, `.ufo/waves/round-30/` 15:58, `demo-cwd.txt` 20:54). `git -C … diff | grep -icE '<seven wave seat names>'` → `0`: no kasegi wave content, no seat name in those diffs.
`MANIFEST.json` — `git -C /home/vgpnk/Projects/shokunin diff --quiet MANIFEST.json` → `exit=0` (content unchanged; only its mtime moved when the dispatcher re-wrote it at 01:16).

**Sibling lanes** — `find /home/vgpnk/Projects/shokunin -newermt '2026-10-26 01:16:32' -type f -not -path './kasegi-shokunin/*' …` → 454 files at 01:32, 456 at 01:33 (still growing), every one inside another lane and named for **that lane's own round**: `kaidoku-shokunin/…/round-36/…`, `tabi-shokunin/.ufo/waves/round-29/…`, `tsukuroi-shokunin/.ufo/waves/round-38/…`, `kengaku-shokunin/…/round-37/…`, `souji-shokunin/census/round-30/…`, `chousa-shokunin/.ufo/waves/round-33/w2/…` (chousa's own round 33, fixture copies with preserved mtimes). Attribution: the watchdog log carries each lane's launch before its writes — `launch tabi round=29` 01:05:45, `launch kaidoku round=36` 01:05:47, `launch tsukuroi round=38` 01:05:49, `launch kengaku round=37` 01:11:32, `launch souji round=30` 01:12:04 — and no kasegi receipt contains a command writing there (`grep` over `wave1/*.md` for a write target under another lane: 0 hits).

**`/home/vgpnk/Projects/shokuknow` (read-only)** — `find … -newermt '2026-10-26 01:15:00' -type f | wc -l` → `0`. No campaign tool was run there by this seat.

**Lane git state** — the lane HEAD moved `a6a5023 → 53bfa59` during the wave, both commits by the L1 through the lane helper (`git reflog`: `… export from jj`, author `kasegi-shokunin <kasegi@shokunin.local>`); no seat commit, no `git`/`jj` mutating command in any receipt.

## 5. Adjacent observations (outside this item's verdict, handed to their owners)

- **`CritC1Kill` scratch claim vs disk.** `CritC1Kill.md:13` says “scratch removed at yield”; `/fast/scratch/hyaku/kasegi-r33/CritC1Kill` still held 40 entries at 01:24:18, dir mtime 01:23:33, receipt mtime 01:24:05. Owner: `ExecScratchDiscipline`. Not a credential, live-target or cross-root issue.
- **`ExecCaptureBinding` wrote 16 sidecar `.txt` files** under `.ufo/waves/round-33/wave1/ExecCaptureBinding/` (exit-2 cases, live and pre-state runs, 01:19-01:29). Evidence only, no URLs beyond the allowed two; it widens the literal ownership wording (“its own seat `.md`”) by one directory.
- **`ExecBeforeReceipts` copied the fleet config into scratch** — `cp /home/vgpnk/Projects/shokunin/shokunin.conf "$S/root/shokunin.conf"` (`ExecBeforeReceipts.md:161`). Checked: `shokunin.conf` carries no token/key/password/URL (`token 0`, `key 0`, `secret 1` prose hit, `http 0`), so nothing sensitive moved; the copy stayed in scratch and was a read of the fleet root.

## 6. Limits of this sweep

- **Coverage**: 43 of 64 seats had landed a receipt by the 01:33 re-check (44 files counting this one). Reads are receipt-level plus scratch corroboration; a seat that fetched and recorded nothing would be caught only through scratch artefacts (none found outside §1). Receipts still missing at 01:33 — `CritMistakes`, `ExecCensusAfter`, `ExecDeterminism`, `ExecForeignCwd`, `ExecGrowthMeasurement`, `ExecHarnessC2`, `ExecNoHarmFinal`, `ExecRegressionC1`, `ExecScratchDiscipline`, `ExecWaveEvidencePack`, `RevC1BeforeAfter`, `RevC1Instrument`, `RevGateSpot`, `RevTranslation`, `ScribeLesson`, `ScribeReportDraft`, `ScribeScorecard`, `ScribeShonen`, `SimplifierCleanup` — are not covered here; `SentScopeFinal` runs the final pass on quiescent bytes.
- **Not comparative**: file mtimes move while seats write (M30-3); each contact table entry above cites the receipt line it rests on, so a later edit is detectable by re-running the classifier.
- **Freshness**: `~/Projects/bounties` and shokuknow statuses are as-of 2026-10-26T01:29-03:00, not standing claims.

## 7. Re-check log (two passes; later pass is the citable one)

| pass | clock | receipts | contacted-host union | outside-lane files since spawn | shokuknow |
|---|---|---|---|---|---|
| 1 | 2026-10-26T01:29-03:00 | 33 | 8 hosts (§1) | 150 | 0 |
| 2 | 2026-10-26T01:31-03:00 | 37 files = 36 seats + this receipt | unchanged, plus this receipt's own citation (§1 note) | 451 | 0 |
| 3 | 2026-10-26T01:32-03:00 | 43 files = 42 seats + this receipt | unchanged; `RevRowS050` joins with S050 (§1 O2) | 454 | 0 |
| 4 | 2026-10-26T01:33-03:00 | 44 files = 43 seats + this receipt | unchanged; adds `shokunin.invalid` (the UA string inside `RevRowS050`'s `-A` argument, not a contact) | 456 | 0 |

All passes agree on the union and on every credential count. The delta between passes is receipts landing (`ExecRegistryAppend`, `CritBoundary`, `ConnOwnership`, `ScribeSearchLog`, `ScribeSkillGate`), not new contacts — `ExecRegistryAppend` and `CritBoundary` show no fetch, and their credential-keyword lines are non-reproduction statements (§2).


## Appendix — replayable method (the scratch scripts, inlined)

The scanner was deleted with its scratch dir; these are its exact rules, so any reader can rebuild it.

```python
import glob, os, re
URL = re.compile(r"https?://[^\s'\"<>)\]|`]+")
VERB = re.compile(r"curl|wget|capture-source\.py[^\n]*--url|urlopen")
RESULT = re.compile(r"code=[0-9]{3}|http=[0-9]{3}|status=[0-9]{3}|HTTP/[12](\.[01])? [0-9]{3}|curl_exit=|final=https?://")
for path in sorted(glob.glob(".ufo/waves/round-33/wave1/*.md")):
    lines = open(path, errors="replace").read().splitlines()
    hit = set()
    for i, line in enumerate(lines):
        near = any(VERB.search(t) for t in lines[max(0, i-4):i])
        if VERB.search(line) or (RESULT.search(line) and (near or URL.search(line))):
            hit |= {re.sub(r"^https?://", "", u).split("/")[0] for u in URL.findall(line)}
    if hit: print(os.path.basename(path), sorted(hit))
```

Credential shapes were counted, never printed: `PEM = r"-----BEGIN [A-Z ]+-----"`, base64 line `r"(?m)^[A-Za-z0-9+/=]{40,}$"`,
`password-assignment r"(密码|口令|password|passwd)\s*[:：=]\s*\S{3,}"`, usernames `r"(用户名|username|账号)\s*[:：=]\s*\S{3,}"`,
`IP r"\b(?:\d{1,3}\.){3}\d{1,3}\b"`, plus `AKIA[0-9A-Z]{16}`, `gh[pousr]_[A-Za-z0-9]{20,}`, `xox[baprs]-`, `BEGIN [A-Z ]*PRIVATE KEY`,
`op://[A-Za-z0-9_-]+/[A-Za-z0-9]` (the op-scheme vault-reference form), and
`(password|passwd|api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9/+=._-]{6,}`.

## 8. Cleanup

`$S=/fast/scratch/hyaku/kasegi-r33/SentCred` (scanner, classifier, masked detector, intermediate lists) removed at yield; this receipt is the only write.
