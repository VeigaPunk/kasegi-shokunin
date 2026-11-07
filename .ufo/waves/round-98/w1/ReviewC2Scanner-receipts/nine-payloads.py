#!/usr/bin/env python3
"""The nine round-98 payloads on the round-97 landing instrument (a9a53608)
and on the C2 landing instrument."""
import importlib.util
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
R=load('/fast/scratch/hyaku/kasegi-r98/ReviewC2Scanner/r97/corpus/instruments/capture-secret-scan.py','R')
L=load('/fast/scratch/hyaku/kasegi-r98/ReviewC2Scanner/landing/corpus/instruments/capture-secret-scan.py','L')
payloads={
 "ci-build": b"t glcbt-Ab3_"+b"k"*20+b" end\n",
 "iam-refresh": b"gliamrt-"+b"A"*43+b"."+b"B"*43+b"\n",
 "iam-auth": b"<i>gliamac-"+b"C"*43+b"."+b"D"*43+b"</i>\n",
 "session": b"Cookie: _gitlab_session="+b"0a"*32+b"; Path=/\n",
 "reg-underscore": b"GR1348941"+b"A"*20+b"_x\n",
 "feed-hyphen": b"u?feed_token="+b"B"*20+b"-x&page=1\n",
 "oauth-underscore": b"gloas-"+b"C"*64+b"_x\n",
 "glft-hyphen": b"glft-"+b"D"*20+b"-x\n",
 "scim-underscore": b"glsoat-"+b"F"*20+b"_x\n",
}
for name,data in payloads.items():
    r=sorted(n for n,_ in R.scan_bytes(data, R.GITLAB_PATTERNS)[0])
    l=sorted(n for n,_ in L.scan_bytes(data, L.GITLAB_PATTERNS)[0])
    print("%-18s r97=%-40s landing=%s" % (name, ",".join(r) or "none", ",".join(l) or "none"))
