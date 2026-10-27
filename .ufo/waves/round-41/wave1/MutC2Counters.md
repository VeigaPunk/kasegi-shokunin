# MutC2Counters — C2 kill-rule mutation matrix

## Scope and fixture

Read frozen claims first: `.ufo/waves/round-41/claims.json` at the frozen claims path. C2 kill rule used verbatim in this probe: missing/non-admitted F24; missing S063 opened this round, failed source-recheck or unbound manifest; entry missing/lacking `(source:, verified-at:, recheck:)` or failing its recheck; harness not `entries=27 pass=27` or no PASS F24; binding unbound; recheck-audit expected not 60; census nonzero/new W/E; accepted junk twin; corpus deletion; coverage measure below 1.000.

At inspection the lane was HEAD `b3b08b276af6146217efd89f7595243a644ed00b` (wave-1 dispatch), with the claimed after-state not yet landed: frontier 23, registry 62, knowledge 59, and zero entries citing S063. Therefore I constructed a **scratch-only after-state fixture** from the lane's `corpus/` bytes and the frozen C2 description, with the new F24/S063 row, capture/manifest, knowledge entry, expected-list line, and README amendment. This is a detector probe, not a report that the fixture is the later judged head. Existing recheck `cd` paths were rewritten to the scratch root so each copy's commands executed against itself; no lane content other than this receipt was written.

Fetch command: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o rfc9116.txt -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\\n' https://www.rfc-editor.org/rfc/rfc9116.txt`.
- First fetch: `http=200 bytes=45129 url=https://www.rfc-editor.org/rfc/rfc9116.txt`; UTC `2026-10-27T08:33:48Z`; SHA-256 `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`; 1,122 lines.
- Refetch: HTTP 200, 45,129 bytes, same SHA-256; UTC `2026-10-27T08:47:15Z`.

The fixture's clean positive run printed frontier rows/admitted `24/24`, registry rows `63`, S063 mined `1`, S063-citing entries `1`, knowledge files `60`, measure `44/44=1.000`; source-recheck printed `S063:sha256 OK` and Q1-Q4 `OK` with anchors 439, 440, 351, 318; harness `entries=27 pass=27 exit=0` including `PASS F24 ... ids=S063 exit=0`; binding `records=55 bound=55 unbound=0`; recheck-audit `strict pass=60/60 ... exit=0`, `expect=present expected=60 missing=0 unexpected=0 exit=0`; census exit 0 with only W04 S028 and W04 S029 (same two warnings as the live lane).

## Mutation matrix

Each mutation used a separate copy of the same clean scratch fixture and changed only the named behavior-bearing point. Detector output below is actual printed output. `Killed` means the named C2 clause became false / its detector fired; independent detectors may remain green.

| Mutation | Actual output | Firing clause / verdict |
|---|---|---|
| F24 status `admitted` → `queued` | `frontier_rows=24`, `frontier_admitted=23`, `f24_status=queued`; measure `43/44=0.977`; harness `entries=26 pass=26 exit=0` | **Killed** — F24 status cell is not `admitted`; coverage measure below 1.000. Harness's admitted-only population shrinks, but its own exit stays 0. |
| S063 status `mined` → `queued` | `s063_mined=0`, `queued_rows=1`; measure `44/45=0.978`; harness still `entries=27 pass=27 exit=0`; binding remains `55/55`, census exit 0 | **Killed** — measure below 1.000 (the S063 row exists/opened, so this is the clause that fires). Note the frozen kill-rule text does not separately name the `mined` status; the measure is what detects this mutation. |
| Entry with entire provenance trio removed | Harness `entries=27 pass=26 exit=1`, F24 problems `no-source-line,no-recheck-line,no-source-selection,no-manifest`; audit `strict pass=59/60`, `lines=59 total=60`, `expected=60 missing=0 unexpected=0 exit=1` | **Killed** — entry lacks the provenance trio / fails its recheck; audit completeness also reds. |
| Harness 27/26: F24 recheck retargeted from `--source S063` to `--source S062` | Harness `entries=27 pass=26 exit=1`; F24 problems `header-sources-not-rechecked,selection-not-declared-by-entry,selection-not-cited-by-entry,manifest-missing-ids`; recheck-audit remains exit 0 | **Killed** — entry's recheck does not verify the declared/cited source (harness output is the discriminator). |
| Binding 55/54: S063 manifest URL changed to `https://www.rfc-editor.org/info/rfc9116` | `FAIL rule=url-mismatch record=S063 row=S063 dir=round-41`; `records=55 bound=54 unbound=1`, binding exit 1 | **Killed** — capture manifest record unbound. |
| Audit expected 59 with 60 files | Audit `strict pass=60/60`; `lines=60 total=60 ... exit=1`; `expect=present expected=59 missing=0 unexpected=1 exit=1` | **Killed** — recheck-audit expected count is not 60. |
| Registry still 63 rows, S063 malformed by removing trailing used-by cell | `registry_rows=63`; census `E01 S063 fields=10`; census exit 1 | **Killed** — census exit nonzero / new E01. Other counters (including capture binding) stay green, showing E01 is load-bearing. |

### Junk-twin probes

1. Minimal one-line twin mutation: removed only `source: S063` from the F24 entry while retaining `verified-at:` and its valid `recheck:`. Frontier harness printed F24 `problems=no-source-line`, `entries=27 pass=26 exit=1`; **recheck-audit stayed green** (`strict pass=60/60`, expected 60, exit 0). This is a coverage finding: recheck-audit alone does not require the `source:` header when a valid recheck command remains; the frontier harness catches it.
2. Requested extra-file twin: added `corpus/knowledge/rfc-9116-security-txt-junk-twin.md`, copied from the entry with only its `source: S063` line removed; did not add it to `knowledge-expected.txt`. Recheck-audit printed `strict pass=61/61 cdroot_fail=0 instrument_fail=0 own_fail=0`, `lines=61 total=61 ... exit=1`, and `expect=present expected=60 missing=0 unexpected=1 exit=1`. **Killed** — the junk twin is not accepted; expected-entry completeness rejects it. The twin's source line was absent and its recheck line remained present.

## Hashes and restoration

For each mutation I recorded the target file SHA-256 before mutation, after mutation, and after restore. `restored_equal=True` for every row. The M10 twin was absent before, present with the reported hash while tested, then absent after restoration.

| Mutation | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| F24 queued (README.md) | `0cc4ef514bed5cd241d68674a442630f29680293834e1759adc6fd7a0f3a0ccb` | `850e938a8ceffefbc6156e3ce149c47a76c9d12f1d940e038fcfd2dccc270b15` | `0cc4ef514bed5cd241d68674a442630f29680293834e1759adc6fd7a0f3a0ccb` |
| S063 queued (SOURCES.md) | `8b77ebfbdd47d73f83d592c98b2ab6302adcd5da3a3d550393a1540b583156af` | `42b0ed64f1cd2b97ccd5cb36bcae8efa020beff051839a343e67a9c4e4ad47b9` | `8b77ebfbdd47d73f83d592c98b2ab6302adcd5da3a3d550393a1540b583156af` |
| No trio (F24 entry) | `fb15a3874715e21ec2ed359f05fce26bf7c859d69ee2d95b1262e4a8860e8013` | `a48a4cb0b4e5e5955af6854f3ba677723f24338aa8f06ed820d6cb8eec07deeb` | `fb15a3874715e21ec2ed359f05fce26bf7c859d69ee2d95b1262e4a8860e8013` |
| Retarget to S062 (F24 entry) | `6122f2bc12dc14867186925e2497ecc62db6f840948c9d5d3b8b57a4ff342f73` | `b91bb0e91b63a90552747328782e7369a7100151e6a66a4fde79295e0f03e196` | `6122f2bc12dc14867186925e2497ecc62db6f840948c9d5d3b8b57a4ff342f73` |
| URL mismatch (round-41 manifest) | `a7aea9dc48d6606fd9b2e5944fce88aefd8a2f67f425ded0efa34f69844ce446` | `75508135c3a3dcfde420c4d8c32f6cd7cf0b3b894289f91e43714c3f875bebea` | `a7aea9dc48d6606fd9b2e5944fce88aefd8a2f67f425ded0efa34f69844ce446` |
| Expected-59 (knowledge-expected.txt) | `e391582b2f904e25175b935f4e1016e0429b742b5117a942b595dabf46f88846` | `4e46214ff37bc2a89ff12e9bc4ba1cbfe4c382507812902558b7edffed84aa46` | `e391582b2f904e25175b935f4e1016e0429b742b5117a942b595dabf46f88846` |
| Malformed S063 row (SOURCES.md) | `8b77ebfbdd47d73f83d592c98b2ab6302adcd5da3a3d550393a1540b583156af` | `8aaa9f8b42388fdc4ab54c5ea62ececd0069d287445c65e3aee3d7b1954ef63b` | `8b77ebfbdd47d73f83d592c98b2ab6302adcd5da3a3d550393a1540b583156af` |
| Minimal twin (entry) | `8b5352fb00eedbee53608ac860d46780aceabf84466ab5ed4451ac608842aa1b` | `b26d6304045ab9b15ead3a8147b9a5502303e2fe6ce606fd500b895816cd39f` | `8b5352fb00eedbee53608ac860d46780aceabf84466ab5ed4451ac608842aa1b` |
| Trio-less twin (entry) | `dcc897bff795eefef56809e533d59b14563b60df4d56f523d5ba4697acf025c3` | `a48a4cb0b4e5e5955af6854f3ba677723f24338aa8f06ed820d6cb8eec07deeb` | `dcc897bff795eefef56809e533d59b14563b60df4d56f523d5ba4697acf025c3` |
| Added junk twin | ABSENT | `d19b1bb479cf02b344b176fca372db5b941279dd34da9ed7ec001ad19cc68348` | ABSENT |

After restore, the same detector battery on each of the ten copies reported the clean values: harness `entries=27 pass=27 exit=0`, binding `records=55 bound=55 unbound=0`, audit `strict pass=60/60`, `expected=60 missing=0 unexpected=0 exit=0`, census exit 0. Full tree comparison after normalizing only each fixture's required `cd <scratch-root>` path reported all ten restored trees `files=300 expected=300 extra=0 missing=0 differing=0 exact=True`.

Scratch removed before filing. No tools were installed.