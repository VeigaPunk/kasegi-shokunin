# C2SourceFreshness — wave-2 falsification: live re-fetch vs pinned captures

Seat: `L1Kasegi25.C2SourceFreshness` (round 25, wave 2). Read-only; this file is the only write.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
Re-fetch executed 2026-10-25 ~09:00Z, ~46 min after the original captures (08:14Z, `capture-log.txt:10-14`)
and ~30 min after the wave-1 `ScoutFetchCisco` re-fetch (08:26–08:31Z, `wave1/ScoutFetchCisco.md:5`).

## Verdict

**Wave-1 result CONFIRMED — zero drift.** Under the item "re-fetch one Japanese source and Cisco", I
re-fetched all four Japanese sources plus Cisco as a strict superset (S036, S037, S038, S039, S040; the
named single-Japanese check is covered by S039, the source `wave1/RevQuotesJP.md:136` flags as "a moving
document"). All five live pages return HTTP 200 with the documented UA, and the instrument's own
`html_to_text` re-extraction is **byte-identical** to every pinned snapshot (`cmp` rc=0, sha256 = manifest
pin). The Cisco UA-gating asymmetry reported at `wave1/ScoutFetchCisco.md:31-38` reproduces exactly.
Nothing in the wave-1 freshness claims is falsified.

**Smallest correction (citation, not substance).** `wave1/ScoutFetchCisco.md:12` states the UA is
"`corpus/instruments/capture-source.py:26`". Line 26 is `import re`; the constant is
`corpus/instruments/capture-source.py:32` (`UA = "kasegi-shokunin/1.0 (documentation capture;
+https://shokunin.invalid/kasegi)"`). One-line fix in the receipt only; no production edit made.

## Commands, outputs, exits

UA sent (documented, from `capture-source.py:32` and the instrument's `fetch()` at `:73-79`,
which sets only `User-Agent` on a `urllib.request.Request`):

```
kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)
```

### 1) Re-capture via the lane's own instrument (same fetcher + extractor as the originals)

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && mkdir -p /tmp/c2fresh
for pair in "S036 https://cybozu.co.jp/company/security-policy/" \
            "S037 https://cybozu.co.jp/products/bug-bounty/faq/" \
            "S038 https://pepabo.com/contact/vulnerability-reporting/" \
            "S039 https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html" \
            "S040 https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html"; do
  set -- $pair
  python3 corpus/instruments/capture-source.py --id "$1" --url "$2" --out "/tmp/c2fresh/$1.txt" --kind html
  echo "  -> $1 rc=$?"
done
```

Output (all rc=0):

```
S036 status=200 fetched_bytes=16900  snapshot_bytes=4815  sha256=022ca4f4…ceb950 utc=2026-10-25T09:00:13Z
S037 status=200 fetched_bytes=89300  snapshot_bytes=11194 sha256=b204aa7f…473cb4c utc=2026-10-25T09:00:15Z
S038 status=200 fetched_bytes=37806  snapshot_bytes=3093  sha256=09e077d3…abb68a utc=2026-10-25T09:00:15Z
S039 status=200 fetched_bytes=199797 snapshot_bytes=37126 sha256=657e7b4c…ffc191d utc=2026-10-25T09:00:16Z
S040 status=200 fetched_bytes=94027  snapshot_bytes=33463 sha256=b7f7b55f…ee0c4e286c utc=2026-10-25T09:00:18Z
```

`fetched_bytes` matches the 08:14Z capture log exactly for every source (`capture-log.txt:10-14`) —
including Cisco's 94 027, the figure `wave1/ScoutFetchCisco.md:14` reported at 08:26–08:31Z.

### 2) Byte-level comparison against pinned snapshots

```bash
for s in S036 S037 S038 S039 S040; do
  cmp /tmp/c2fresh/$s.txt corpus/source-snapshots/round-25/$s.txt && echo "$s: IDENTICAL"
done
```

```
S036: IDENTICAL   S037: IDENTICAL   S038: IDENTICAL   S039: IDENTICAL   S040: IDENTICAL
```

Each sha256 equals its pin in `corpus/source-snapshots/round-25/manifest.json:8,55,92,134,186`
and each equals the on-disk snapshot hash (`sha256sum` of `corpus/source-snapshots/round-25/S0*.txt`).

### 3) Cisco UA matrix re-test (falsifies `ScoutFetchCisco.md:31-38`)

```bash
curl -sSL -A "<UA>" -o /dev/null -w 'code=%{http_code} bytes=%{size_download}\n' \
  'https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html'
```

| UA sent | 08:26Z (wave 1) | 09:00Z (this pass) |
|---|---|---|
| `kasegi-shokunin/1.0` | 403 / 465 B | **403 / 465 B** (same) |
| `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` | 200 / 94 027 | **200 / 94 027** (same) |
| curl default (`curl/8.23.0`) | 200 / 94 027 | **200 / 94 027** (same) |
| Chrome 126 desktop UA | 403 / 465 B | **403 / 465 B** (same) |

The Akamai admission rule is unchanged; the 403-vs-200 split the round's entries rely on
(`capture-log.txt:27-28`) still holds.

### 4) Page update-date lines unchanged

```
S039.txt:487   更新日：2026年10月14日           (snapshot == fresh)
S040.txt:490   Last Updated: 2025 September 8   (snapshot == fresh)
```

## Drift summary

| source | URL host | status | sha256 match | drift |
|---|---|---|---|---|
| S036 | cybozu.co.jp | 200 | yes | **none** |
| S037 | cybozu.co.jp | 200 | yes | **none** |
| S038 | pepabo.com | 200 | yes | **none** |
| S039 | hitachi.co.jp | 200 | yes | **none** (更新日 still 2026-10-14) |
| S040 | cisco.com | 200 | yes | **none** (Last Updated still 2025-09-08) |

Fresh line counts: S036 87, S037 294, S038 77, S039 696, S040 503 — S040's 503 matches
`wave1/ScoutFetchCisco.md:22`.

## Observed hazards (unchanged from wave 1, for the record)

- The entire `corpus/source-snapshots/round-25/` directory remains **untracked**
  (`git status --porcelain` → `??`); the pinned bytes exist only in the working tree until the L1 lands
  them — confirms `wave1/ScoutFetchCisco.md:114-118`.
- The bare-token UA still 403s, so any recheck spelling `-A kasegi-shokunin/1.0` (per the truncated
  string at `ScoutFetchCisco.md:28`) would still read a live page as dead.

## Tooling record

Nothing installed or upgraded (pacman paused per `~/.omp/agent/RULES.md`; `~/.omp/agent/RULES.md`
read before this run). Used only `curl 8.23.0`, `python 3.14.8` (stdlib `urllib`), `cmp`, `sha256sum`,
and the lane's unmodified `corpus/instruments/capture-source.py`. All artifacts live in `/tmp/c2fresh/`;
no production files touched.

Report: .ufo/waves/round-25/wave2/C2SourceFreshness.md
