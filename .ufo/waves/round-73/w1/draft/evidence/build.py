import json, subprocess, sys, hashlib
CAP = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-73/S108.txt"
raw = open(CAP, "rb").read()
text = raw.decode("utf-8")
lines = text.split("\n")
Q = [
 ("Q01-scope", 24, "Lists vulnerabilities for given package and version. May also be queried by commit hash."),
 ("Q02-commit-param", 34, "commit string The commit hash to query for. If specified, version should not be set."),
 ("Q03-version-fuzzy", 35, "A fuzzy match is done against upstream versions."),
 ("Q04-version-exclusive", 35, "If set, commit must not be used, and package.purl must not include a version."),
 ("Q05-package-optional", 36, "When a commit hash is given, this is optional."),
 ("Q06-page-token-param", 37, "If your previous query fetched a large number of results, the response will be paginated."),
 ("Q07-version-rule", 40, "Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both."),
 ("Q08-both-places-400", 41, "Requests that specify the version in both places return 400 Bad Request."),
 ("Q09-invalid-label", 47, "Invalid (400 Bad Request):"),
 ("Q10-invalid-example", 48, '{ "package": { "purl": "pkg:pypi/jinja2@3.1.4" }, "version": "3.1.4" }'),
 ("Q11-valid-example", 46, '{ "package": { "purl": "pkg:pypi/jinja2" }, "version": "3.1.4" }'),
 ("Q12-case", 53, "Case Sensitivity: API requests are case-sensitive."),
 ("Q13-name-exact", 54, "Package names are matched exactly, except in ecosystems whose registry treats other spellings as the same package:"),
 ("Q14-pypi", 54, "PyPI names are normalized as described in PEP 503,"),
 ("Q15-nuget", 54, "NuGet names are matched case-insensitively,"),
 ("Q31-crates", 54, "crates.io names are matched case-insensitively with"),
 ("Q16-git-set", 56, "To do so, set the ecosystem to GIT, enter the full URL of the repository to the name field,"),
 ("Q17-git-tag-field", 56, "and the tag into the version field."),
 ("Q18-git-example", 79, '{"package": {"name": "https://github.com/curl/curl.git", "ecosystem": "GIT"}, "version": "8.5.0"}'),
 ("Q19-payload-commit", 59, '"commit": "string",'),
 ("Q20-payload-page-token", 66, '"page_token": "string"'),
 ("Q21-pagination-trigger", 136, "pagination will occur when there more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds."),
 ("Q22-token-mechanism", 135, "When pagination is used, the next_page_token is given in the response, indicating that there are more results to return."),
 ("Q23-repeat-until", 135, "repeating queries until the next_page_token is no longer included in the response."),
 ("Q24-next-page", 144, "To get the next page of results, your next request must include page_token:"),
 ("Q25-rare-token-only", 149, "In rare cases, the response might contain only the next_page_token."),
 ("Q26-keep-querying", 149, "please keep querying with the next_page_token until either results are returned, or no more page tokens are returned."),
 ("Q27-size-http1", 148, "The API has a response size limit of 32MiB when using HTTP/1.1."),
 ("Q28-size-http2", 148, "There is no limit when using HTTP/2."),
 ("Q29-http2-recommend", 148, "We recommend using HTTP/2 for queries that may result in large responses."),
 ("Q30-page-size-vary", 136, "The page size can vary slightly because of threading and may change in the future."),
]
ok = True
rows = []
for qid, anc, q in Q:
    on_line = q in lines[anc-1]
    occ = text.count(q)
    gl = subprocess.run(["grep", "-nF", "--", q, CAP], capture_output=True, text=True)
    glines = [l.split(":",1)[0] for l in gl.stdout.splitlines()]
    words = len(q.split())
    good = on_line and occ >= 1 and (occ == 1 or anc) and words <= 25
    ok &= good
    rows.append((qid, anc, occ, glines, words, on_line, good))
    print(f"{qid:24s} anchor={anc:<4d} on_line={int(on_line)} occ={occ} grepF_lines={','.join(glines)} words={words} ok={int(good)}")
print("ALL_OK" if ok else "FAIL")
if not ok:
    sys.exit(1)

import os
DRAFT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-73/w1/draft/manifest.json"
sha = hashlib.sha256(raw).hexdigest()
assert sha == "304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9", sha
nbytes = len(raw); nlines = raw.count(b"\n")
assert (nbytes, nlines) == (6563, 150), (nbytes, nlines)
qs = [q for q in Q]
assert len({q[0] for q in qs}) == len(qs)
URL = "https://google.github.io/osv.dev/post-v1-query/"
body = []
for qid, anc, q in qs:
    body.append('        ' + json.dumps({"id": qid, "quote": q, "anchor": anc}, ensure_ascii=False))
manifest = (
'{\n'
'  "schema_version": 1,\n'
'  "note": "Round-73 OSV.dev POST /v1/query service contract (frontier F51). S108 is the OSV.dev project\'s own API reference page for the query endpoint, as served: the payload keys, the version rule, the Git-tag query, pagination and the 32 MiB HTTP/1.1 response limit. It is the service contract of one endpoint only, not the OSV record format (F31) and not the overview page. Opened 2026-11-05.",\n'
'  "sources": [\n'
'    {\n'
'      "id": "S108",\n'
'      "url": "' + URL + '",\n'
'      "capture_url": "' + URL + '",\n'
'      "http": {"status": 200, "final_url": "' + URL + '"},\n'
'      "kind": "html",\n'
'      "fetch_method": "capture-source.py --kind html, default instrument UA (tags stripped, entities decoded, whitespace collapsed per line); the original fetch command line is not recorded in the lane, and a re-run of this tool on 2026-11-05T07:47:23Z reproduced the sha256 and the 6563 snapshot bytes",\n'
'      "fetched_utc": "2026-11-05T07:40:48Z",\n'
'      "path": "S108.txt",\n'
'      "sha256": "' + sha + '",\n'
'      "bytes": ' + str(nbytes) + ',\n'
'      "lines": ' + str(nlines) + ',\n'
'      "quotes": [\n'
+ ',\n'.join(body) + '\n'
'      ]\n'
'    }\n'
'  ]\n'
'}\n')
parsed = json.loads(manifest)
assert parsed["sources"][0]["sha256"] == sha and len(parsed["sources"][0]["quotes"]) == len(qs)
os.makedirs(os.path.dirname(DRAFT), exist_ok=True)
open(DRAFT, "w", encoding="utf-8").write(manifest)
print("MANIFEST_WRITTEN", DRAFT, "quotes=", len(qs), "bytes=", nbytes, "lines=", nlines, "sha=", sha)
