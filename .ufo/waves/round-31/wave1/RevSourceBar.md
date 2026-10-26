# RevSourceBar — Source-Bar Review for S048 (Round 31, Wave 1)

- **Seat:** `RevSourceBar` (reviewer)
- **Answering model:** `google-antigravity/gemini-4-argon` (config route table; no model passed)
- **Tooling installed/upgraded:** none (`pacman` paused host-wide; no package transactions run)
- **Subject:** Candidate lane row `S048` (`Microsoft Security Vulnerability Research — https://www.microsoft.com/en-us/msrc/msvr`), mapped by document from staged row `S080` in `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:56`
- **Verdict:** **ADMIT-ROW** (with required cell rewrites from staged `S080` before registration in `corpus/SOURCES.md`; communicated to `ExecRegistryAppend`)

---

## 1. Independent Re-Open of `https://www.microsoft.com/en-us/msrc/msvr` (Instrument UA) & Staged Row `S080`

### 1.1 Staged Row `S080` (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:56`)

Command and output:
```text
$ grep -n '| S080 |' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
56:| S080 | Microsoft Security Vulnerability Research — https://www.microsoft.com/en-us/msrc/msvr | docs | A | Microsoft's programme for handling vulnerabilities found in third-party products, and the routes by which those findings arrive | the paragraph beginning "MSVR learns about vulnerabilities in third-party products in three ways", with the three routes | A vendor's own research programme is a third intake route for findings about other vendors' products, handled under coordinated disclosure. | mined | 2026-10-23 | 180d | corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md |
```

### 1.2 Independent Live Fetch and Stability/Personalization Probes (Instrument UA)

Executed with `UA = "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"` and compared against `capture-source.py`'s `html_to_text()` normalization and the committed round-31 capture `corpus/source-snapshots/round-31/S048.txt` (`sha256=2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`, 3,755 bytes, 97 lines):

```text
fetch 1: status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr bytes=81802 sha256=930cd5a7153178d88c1078bad8ce8af73949f9088dbb69f6a7de4869ec85fee4
  Date: ['Sun, 25 Oct 2026 23:29:04 GMT']
  Cache-Control: ['no-store']
  Content-Type: ['text/html; charset=utf-8']
  Set-Cookie: ['bStore=Y; expires=Sun, 25-Oct-2026 23:29:14 GMT', 'CAS_PROGRAM=foxtrot; expires=Sun, 25-Oct-2026 23:29:12 GMT; path=/; secure; SameSite=None']
fetch 2: status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr bytes=81802 sha256=44dd45ebbf0e6e6a75373825cc20bde413879e42f8cf1859623cbfe8866b8eb0
```

Multi-variant stability matrix across headers, `Accept-Language`, and `Cookie` overrides:
```text
baseline-1:     status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr raw_bytes=81802 txt_bytes=3755 lines=97 no_trace_sha256=69c893989764bf45 msvr_body_sha256=f2efea059226abe7
baseline-2:     status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr raw_bytes=81802 txt_bytes=3755 lines=97 no_trace_sha256=69c893989764bf45 msvr_body_sha256=f2efea059226abe7
accept-lang-ja: status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr raw_bytes=81802 txt_bytes=3755 lines=97 no_trace_sha256=69c893989764bf45 msvr_body_sha256=f2efea059226abe7
accept-lang-zh: status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr raw_bytes=81802 txt_bytes=3755 lines=97 no_trace_sha256=69c893989764bf45 msvr_body_sha256=f2efea059226abe7
cookie-probe:   status=200 final_url=https://www.microsoft.com/en-us/msrc/msvr raw_bytes=81802 txt_bytes=3755 lines=97 no_trace_sha256=69c893989764bf45 msvr_body_sha256=f2efea059226abe7
committed S048.txt: bytes=3755 sha256=2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55 lines=97 no_trace_sha256=69c893989764bf45 msvr_body_sha256=f2efea059226abe7
```

---

## 2. Source-Bar Evaluation by Criterion

### 2.1 `tier`: `A` (Scoped Authority & Explicit Exclusions)
- **Tier `A` for which scope:** Under `CORPUS.md` SOURCES contract v1 (`tier — scoped to scope, never global. A: primary or authoritative for that scope`), `https://www.microsoft.com/en-us/msrc/msvr` is **tier `A`** strictly for **Microsoft's own first-party statement of its Microsoft Security Vulnerability Research (MSVR) programme: its stated purpose (L29–L30), the three routes by which MSVR learns about vulnerabilities in third-party products (L31–L34), and Microsoft's stated three-role Coordinated Vulnerability Disclosure (CVD) framing as affected vendor, finder in third-party products, and multi-vendor coordinator (L35)**.
- **Why NOT Tier `A` for other scopes:**
  1. **Not Tier `A` for industry-wide or universal vendor rules (QUALITY Q4):** A single vendor's programme page cannot substantiate what "vendors" do in general or establish a universal obligation on finders (staged entry line 28 overgeneralized that *"the finder also has a coordinated-disclosure obligation"*, which is absent from the page).
  2. **Not Tier `A` for coordination agreement terms, SLAs, or disclosure deadlines:** The MSVR body is 8 lines (L28–L35 in `S048.txt`). It states no embargo clock, no notification deadline, no CVE assignment rule, and no bilateral coordination agreement text.
  3. **Not Tier `A` for all third-party routes being "coordinated by MSVR":** Route 2 (L33, external MSRC reports affecting third-party or both) states `"These issues are coordinated by MSVR."`, whereas Route 1 (L32, internal engineers) says `"reported to the MSVR team, which then works with the affected vendor to fix the issue."` and Route 3 (L34, internal research projects) says `"reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices."`
- **Cell requirement (`scope` & `teaches`):** Staged `S080`'s `teaches` cell (`A vendor's own research programme is a third intake route...`) is unattributed. In `corpus/SOURCES.md`, `scope` and `teaches` must name Microsoft/MSVR explicitly and bind to `S048.txt` line numbers (Q4).

### 2.2 `kind`: `docs`
- **Verdict:** **`docs` (Pass).**
- **Reasoning:** The resource is Microsoft's published first-party programme documentation page (`text/html; charset=utf-8` at `https://www.microsoft.com/en-us/msrc/msvr`). Within the `CORPUS.md` `kind` enum (`spec · docs · paper · code · tool · dataset · talk · book · community · own-work`), it is neither a normative specification (`spec`), nor a scholarly article (`paper`), nor a structured dataset (`dataset`). It matches existing vendor policy rows S036–S040 (`docs`).

### 2.3 `anchor` Adequacy (Section/Paragraph + Page Revision/Date)
- **Page revision/date inspection:**
  - Inspected HTTP response headers (`Date: Sun, 25 Oct 2026 23:29:04 GMT`, `Cache-Control: no-store`, no `Last-Modified` header) and all 1,144 lines of raw HTML:
  - The MSVR page carries **no visible publication date, revision date, or version number** in its body or `<meta>` tags. (The only date-like string in the HTML is the Universal Header/Footer static asset path `https://uhf.microsoft.com/statics/20261021.14.40/css/style-PF2pqjN1.css` at HTML L480/L980, which is site-wide UHF chrome, not an editorial revision of the MSVR text.)
- **Assessment of staged `S080` anchor:**
  - Staged `S080` has: `the paragraph beginning "MSVR learns about vulnerabilities in third-party products in three ways", with the three routes`.
  - **Inadequate as-is for lane registration:** Under `CORPUS.md` contract v1 (`anchor — exact section / heading / page / line plus revision (version, commit, or publication date)`) and `SOURCES.md` precedent (rows S004/S023 for undated pages; rows S042–S047 for snapshot-pinned rows), the `anchor` cell for `S048` MUST:
    1. Name the committed round-31 capture `corpus/source-snapshots/round-31/S048.txt` and the heading `Microsoft Security Vulnerability Research (MSVR)` (L28);
    2. Cite the exact line range L28–L35 (purpose/goal L29–L30; three-ways lead-in L31; three routes at L32, L33, L34; CVD three-roles sentence at L35); and
    3. Explicitly note that the page shows no visible publication or revision date, `opened 2026-10-25`.

### 2.4 `recheck` Cadence (`180d` vs `90d` for a Live Corporate Page)
- **Verdict:** **`180d` (bare cadence token per census rule E09).**
- **Reasoning from drift evidence:**
  1. **Observed 2-day drift (2026-10-23 staged -> 2026-10-25 live):** Zero semantic or character drift on the MSVR content block (L28–L35). Every phrase cited in the 2026-10-23 staged package (`MSVR learns about vulnerabilities in third-party products in three ways:` and the three routes/roles) is byte-identical in the 2026-10-25 capture (`msvr_body_sha256=f2efea059226abe7`). Even the long-standing typographical error on L33 (`"either affects a third-party product of affects both"`) remains unchanged.
  2. **Separation of per-request token rotation from editorial policy drift:** While raw HTML (`81,802 B`) rotates a per-request correlation token on every fetch (`HTML L363` / `S048.txt L2`: `This is the Trace Id: <32-hex>`, plus `CVToken: CASMicrosoftCV...` in HTML comments), that is a 0-second request-id rotation rather than policy drift. Shortening cadence from `180d` to `90d` does not change per-request trace-id rotation; instead, automated verification runs against the pinned snapshot `corpus/source-snapshots/round-31/S048.txt` via `source-recheck.py`.
  3. **Lane registry cadence calibration (`SOURCES.md`):** In `corpus/SOURCES.md`, `90d` is assigned to high-frequency feeds, APIs, and quarterly/weekly datasets — e.g., S043 HackerOne `policy_versions` (153-record live API array), S044/S045 Bugcrowd VRT (reviewed weekly by the VRT Council), and S047 IPA JVN quarterly registration report. Standing vendor disclosure policy pages — S036 Cybozu policy, S037 Cybozu FAQ, S038 GMO Pepabo, S039 Hitachi HIRT-PUB10008, S040 Cisco Security Vulnerability Policy, S004 CERT/CC, S005 Project Zero FAQ — all carry `180d`. Microsoft's MSVR charter page is a standing institutional programme page of the same class, so `180d` is the calibrated cadence.

### 2.5 Stability for Captured-Source Recheck (Dynamic Content, Personalization, A/B Text)
- **Verdict:** **Stable for `source-recheck.py` on lines 28–35; never quote line 2 or nav/footer chrome.**
- **Measured evidence:**
  1. **Per-request dynamic line (L2):** `capture-source.py` strips `<script>` and `<style>` blocks (`SCRIPT_RE`) and HTML tags (`TAG_RE`), but HTML line 363 (`This is the Trace Id: <32-hex>`) is plain text outside `<script>`, so it survives into `S048.txt` line 2. Consequently, two consecutive runs of `capture-source.py` produce 3,755-byte, 97-line snapshots that differ **exclusively on line 2** (`no_trace_sha256=69c893989764bf45` across all 6 captures).
  2. **Personalization & A/B text:** Although the response sets `Set-Cookie: bStore=Y; ...` and `CAS_PROGRAM=foxtrot; ...` and HTML L308 mentions `CVToken-Experimentation`, probing with `Cookie: bStore=N; CAS_PROGRAM=alpha` and `Accept-Language: ja-JP` / `zh-CN` returned the exact same 81,802 raw byte count and the exact same 96 non-Trace-Id lines (`no_trace_sha256=69c893989764bf45`, `msvr_body_sha256=f2efea059226abe7`). No A/B text or locale personalization affects `/en-us/msrc/msvr`.
  3. **Apostrophe encoding:** L30 contains UTF-8 U+2019 (`Microsoft’s goal`), whereas L35 contains ASCII `'` (`Microsoft's Coordinated Vulnerability Disclosure (CVD) approach`, decoded from `Microsoft&#39;s`).
  4. **Verification of committed round-31 manifest (`corpus/source-snapshots/round-31/manifest.json`):**
     ```text
     $ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048; echo "recheck_exit=$?"
     S048:sha256 OK
     S048:Q1 OK occurrences=1
     S048:Q2 OK occurrences=1
     S048:Q3 OK occurrences=1
     S048:Q4 OK occurrences=1
     S048:Q5 OK occurrences=1
     S048:Q6 OK occurrences=1
     S048:Q7 OK occurrences=1
     S048:Q8 OK occurrences=1
     recheck_exit=0
     ```

### 2.6 `CORPUS.md` Rule 6 Check (No Credential Material, Session URLs, or `op://` References)
- **Verdict:** **Pass (0 hits).**
- **Evidence:**
  - Canonical URL `https://www.microsoft.com/en-us/msrc/msvr` is a public, unauthenticated documentation URL (no query string, no session token, no redirect).
  - Regex scan over `corpus/source-snapshots/round-31/S048.txt` and staged row `S080` for `op://`, `token=`, `session`, `secret`, `password`, `apikey`, `api_key`, `bearer`, `authorization:`, `cookie:`, and query-string auth parameters returned `hits=0 []`.

---

## 3. Located Quotes Grounding `S048` (All ≤25 Words, Verified `occurrences=1` in `corpus/source-snapshots/round-31/S048.txt`)

Every quote below is copied verbatim from `corpus/source-snapshots/round-31/S048.txt` (no page revision date on source; captured 2026-10-25, `sha256=2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`):

| Quote ID | Verbatim Quote (≤25 words) | Word Count | Exact Location in `S048.txt` | `source-recheck.py` / `grep -cF` |
|---|---|---:|---|---|
| Q1 | `"MSVR learns about vulnerabilities in third-party products in three ways:"` | 10 | Heading `Microsoft Security Vulnerability Research (MSVR)` (L28), line 31 | `occurrences=1` |
| Q2 | `"These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue."` | 19 | Line 32 (`Internal Microsoft engineers:` route) | `occurrences=1` |
| Q3 | `"These issues are coordinated by MSVR."` | 6 | Line 33 (`External reports to the Microsoft Security Response Center (MSRC):` route) | `occurrences=1` |
| Q4 | `"Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices."` | 14 | Line 34 (`Internal research projects:` route) | `occurrences=1` |
| Q5 | `"as a vendor affected by vulnerabilities in its products and services"` | 11 | Line 35 (CVD paragraph, role 1 of 3) | `occurrences=1` |
| Q6 | `"as a finder of new vulnerabilities in third-party products and services"` | 11 | Line 35 (CVD paragraph, role 2 of 3) | `occurrences=1` |
| Q7 | `"as a coordinator of vulnerabilities that affect multiple vendors"` | 9 | Line 35 (CVD paragraph, role 3 of 3) | `occurrences=1` |
| Q8 | `"This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach."` | 11 | Line 35 (CVD paragraph opening sentence; ASCII apostrophe) | `occurrences=1` |

---

## 4. Required Cell Changes from Staged `S080` → Lane `S048` (Sent to `ExecRegistryAppend`)

Staged row `S080` cannot be pasted verbatim into `corpus/SOURCES.md`. The following cell changes are required for `S048`:

1. **`id`:** `S080` → `S048` (mapped by document URL; next unused lane ID after `S047`).
2. **`scope`:** Scope the tier explicitly to Microsoft's own first-party statement of its MSVR programme, its three third-party vulnerability intake routes, and its three stated CVD roles (never universal vendor practice).
3. **`anchor`:** Replace the unlocated staged prose (`the paragraph beginning "MSVR learns..."`) with the exact heading, `corpus/source-snapshots/round-31/S048.txt` line numbers (`L28-L35`: heading `Microsoft Security Vulnerability Research (MSVR)` L28, intro L29-L30, three-ways lead-in L31, three intake routes L32-L34, CVD three-roles sentence L35), and the explicit revision-date note (`page shows no visible publication or revision date, opened 2026-10-25`).
4. **`teaches`:** Attribute explicitly to Microsoft/MSVR (QUALITY Q4) rather than the staged generic `"A vendor's own research programme..."`, citing the three intake routes (L31–L34) and three CVD roles (L35).
5. **`opened`:** `2026-10-23` → `2026-10-25` (CORPUS.md rule 1: date opened in the admitting lane round).
6. **`recheck`:** Keep bare `180d` (census rule E09; no inline prose).
7. **`used-by`:** `corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` → `corpus/knowledge/vendor-third-party-finding-coordination.md`.
8. **R8 Registry changes log:** Log all staged `S080` → landed `S048` cell rewrites (`id`, `scope`, `anchor`, `teaches`, `opened`, `used-by`) in `## Registry changes` at the end of `corpus/SOURCES.md`.
