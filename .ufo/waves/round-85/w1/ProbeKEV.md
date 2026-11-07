# ProbeKEV — CISA KEV absence probe for CVE-2023-28319

**Seat:** ProbeKEV (scout, wave w1, round-85 attempt 1)
**Verdict:** **HOLDS** — CVE-2023-28319 is absent from the CISA KEV catalog in the lane
capture *and* in the live feed as fetched today.
**Confidence:** high (direct byte-level grep on both files, plus an independent JSON
structural membership check and a positive control).

No lane tree, corpus, instrument, frozen control or `.ufo/state/` bytes were modified.
Everything below is read-only evidence; the only writes are this report and its receipts.

---

## Hypothesis under test

> "CVE-2023-28319 is absent from the CISA KEV catalog both in the lane capture
> `corpus/source-snapshots/round-35/S052.txt` and in the live feed today."

Both conjuncts tested independently.

---

## Axis A — lane capture `corpus/source-snapshots/round-35/S052.txt`

File identity:

```
$ sha256sum corpus/source-snapshots/round-35/S052.txt
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
$ ls -la corpus/source-snapshots/round-35/S052.txt
-rw-r--r-- 1 vgpnk vgpnk 1479694 Oct 26 03:32 corpus/source-snapshots/round-35/S052.txt
$ wc -l corpus/source-snapshots/round-35/S052.txt
27870 corpus/source-snapshots/round-35/S052.txt
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-files --error-unmatch corpus/source-snapshots/round-35/S052.txt
corpus/source-snapshots/round-35/S052.txt        # tracked
$ git -C ... log --oneline -1 -- corpus/source-snapshots/round-35/S052.txt
5a25337 round-35: commit wave leftovers — S052 capture ...
```

The sha256 matches the one already recorded in `corpus/knowledge/cisa-kev-catalog.md:3`
(`d69349e8…`) — the capture is unmodified.

**catalogVersion, line 3 (the value the spec asks for):**

```
$ grep -n '"catalogVersion"' corpus/source-snapshots/round-35/S052.txt
3:"catalogVersion": "2026.10.23",
$ grep -n '"dateReleased"' corpus/source-snapshots/round-35/S052.txt
4:"dateReleased": "2026-10-23T19:30:18.9209Z",
$ grep -n '"count"' corpus/source-snapshots/round-35/S052.txt
5:"count": 1756,
```

**The count:**

```
$ grep -c 'CVE-2023-28319' corpus/source-snapshots/round-35/S052.txt
0
$ grep -c -i '28319' corpus/source-snapshots/round-35/S052.txt
0
```

**Positive-shape / control probes (truthful counts):**

| probe | count in capture |
|---|---|
| `CVE-2023-28319` (target) | **0** |
| `28319` (loose, case-insensitive) | **0** |
| `CVE-2023-38545` (the requested shape probe) | **0** |
| `CVE-2021-44228` (positive control) | **3** |
| `curl` (case-insensitive) | **0** |
| `haxx` | **0** |
| `"cveID"` entries | 1756 (= declared `count`) |

**Structural check (python3 -B, stdlib only — independent of grep):**

```
catalogVersion= 2026.10.23 count_field= 1756 len_entries= 1756 unique= 1756
CVE-2023-28319 present= False
CVE-2023-38545 present= False
CVE-2021-44228 present= True
any 2023 id containing 28319: []
```

---

## Axis B — live CISA KEV feed today

```
$ curl -sS -L -o $S/kev-live.json \
    -w 'HTTP_STATUS=%{http_code}\nURL_EFFECTIVE=%{url_effective}\nSIZE=%{size_download}\n' \
    https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
HTTP_STATUS=200
URL_EFFECTIVE=https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
SIZE=1832349
---exit=0---
$ sha256sum $S/kev-live.json
47e0406b2be5a40420eff66f3d90e83eb8883dae6ff4d08e1b2a942c366f6cc2  kev-live.json
```

Live head (verbatim, first lines):

```
{
    "title": "CISA Catalog of Known Exploited Vulnerabilities",
    "catalogVersion": "2026.11.06",
    "dateReleased": "2026-11-06T19:44:45.1797Z",
    "count": 1769,
    "vulnerabilities": [
        {
            "cveID": "CVE-2026-19868",
```

**catalogVersion = 2026.11.06**, count = 1769, `cveID` entries = 1769.

**The count and the controls:**

| probe | count in live feed |
|---|---|
| `CVE-2023-28319` (target) | **0** |
| `CVE-2023-38545` (shape probe) | **0** |
| `CVE-2021-44228` (positive control) | **3** |
| `curl` (case-insensitive) | **0** |
| `haxx` | **0** |
| distinct `vendorProject` values | 291 (none is curl) |

**Structural check:**

```
catalogVersion= 2026.11.06 count_field= 1769 len_entries= 1769 unique= 1769
CVE-2023-28319 present= False
CVE-2023-38545 present= False
CVE-2021-44228 present= True
any 2023 id containing 28319: []
```

---

## Verdict and the two caveats the caller must carry forward

**VERDICT: HOLDS.** `grep -c 'CVE-2023-28319'` = 0 in the lane capture and 0 in the
live feed (HTTP 200, catalogVersion 2026.11.06).

### Caveat 1 — the requested positive-shape probe is not positive

The spec nominated `CVE-2023-38545` (also a curl CVE) as "a positive-shape probe of your
grep". **Its count is 0 in both files.** It is therefore not a positive control: curl
simply has no KEV listing, in any of the CVE years both files cover (2002–2026 for the
capture; same span live). The control that actually validates the grep shape is
`CVE-2021-44228` (Log4Shell) → **3 occurrences in each file**, and the structural check
that `len(vulnerabilities) == count_field` and that every `cveID` is unique. Reported
truthfully rather than massaged into a positive.

Consequence for the C2 pricing: the correct statement is that neither CVE-2023-28319
nor any other curl CVE is KEV-listed, and the absence is a property of the vendor's
presence in KEV, not of the grep.

### Caveat 2 — catalogVersion drift between the capture and the live feed

- capture (S052, the bytes the frozen counter reads): `catalogVersion` **2026.10.23**, 1756 records
- live feed (2026-11-06): `catalogVersion` **2026.11.06**, 1769 records

The frozen counter `.ufo/waves/round-85/c2/e2e-check.py` derives the pricing field from
the **capture only**:

- line 70: `kev = rd(os.path.join(d, "round-35", "S052.txt"))`
- line 80: `"kev": "not-listed" if kev.count(cve) == 0 else "listed",`
- line 105 (E3): the package's `price-kev` value only has to **start with** `"not-listed"`.

So the package must state `price-kev: not-listed …` and, to stay consistent with the
frozen derivation, should cite the **capture's** catalogVersion `2026.10.23` (S052.txt
line 3), not the live `2026.11.06`. Membership is identical under both versions, so the
pricing conclusion is stable across the drift — only the version string differs.

### Caveat 3 (tooling note, avoids a false negative later)

The `read` tool renders `…` inside long JSON lines of S052. Those are **display
elisions, not file bytes**: `python3 -B` reading the raw file shows complete JSON keys on
lines 11–15, the file parses cleanly, and it contains 1756 unique `cveID` values. A
reviewer re-reading S052 through `read` will see `…` and must not read that as truncation.

---

## Relevance to the C2 claim (why this matters)

The frozen counter's KEV limb (`e2e-check.py:80`) and the executed positive pricing control
(`controls/c2-controls-r85.sh:22`, `price-kev: ${KEV:-not-listed (CVE id absent from the
round-35 S052 capture)}`) both agree with this probe: the derived value is `not-listed`.
The forged-kev control (`KEV="listed" mk forged-kev fail`) fails E3 as designed.

## Re-runnable command

```
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ProbeKEV-receipts/rerun-kev-probe.sh
```

Exit 0. Captured output: `ProbeKEV-receipts/rerun-kev-probe.out`
(sha256 `66cded1969695a0bc43a6dc5fa803cebe1e4ac39ac3007288a68628bf2d5e120`).
The script fetches the live feed itself, so it re-verifies today's membership on any run;
it writes only inside its own scratch.

## Files written by this seat

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ProbeKEV.md` (this report)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ProbeKEV-receipts/kev-probe-receipt.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ProbeKEV-receipts/kev-live-head.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ProbeKEV-receipts/rerun-kev-probe.sh`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ProbeKEV-receipts/rerun-kev-probe.out`

## Unresolved gaps (out of this seat's scope, flagged not chased)

- No tool was installed or upgraded for this seat; no tool/version/channel entry is owed.
- The live feed is a moving target; the capture-bound `2026.10.23` is the version of record
  for the frozen C2 counter and is what the package should cite.
