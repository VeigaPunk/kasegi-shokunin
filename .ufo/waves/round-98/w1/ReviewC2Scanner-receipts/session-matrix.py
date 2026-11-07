#!/usr/bin/env python3
"""Session-cookie shape: context, separator, cell prefix, length, boundary."""
import importlib.util, re
s=importlib.util.spec_from_file_location("L","/fast/scratch/hyaku/kasegi-r98/ReviewC2Scanner/landing/corpus/instruments/capture-secret-scan.py")
L=importlib.util.module_from_spec(s); s.loader.exec_module(L)
P=dict(L.GITLAB_PATTERNS)
H=b"0a"*32; H63=b"0a"*31+b"0"; H65=H+b"a"
cases=[
 ("eq",              b"_gitlab_session="+H+b"; Path=/", True),
 ("colon",           b"_gitlab_session: "+H+b"\n", True),
 ("json",            b'"_gitlab_session":"'+H+b'"', True),
 ("space-only",      b"_gitlab_session "+H+b"\n", True),
 ("newline-only",    b"_gitlab_session\n"+H+b"\n", True),
 ("semicolon-only",  b"_gitlab_session;"+H+b"\n", True),
 ("no-separator",    b"_gitlab_session"+H+b"\n", False),
 ("geo",             b"_gitlab_session_geo_"+H+b"="+H+b"\n", True),
 ("geo-63",          b"_gitlab_session_geo_"+H63+b"="+H+b"\n", False),
 ("cell",            b"_gitlab_session="+b"cell-7-"+H+b"\n", True),
 ("cell-no-dash",    b"_gitlab_session="+b"cell-7"+H+b"\n", False),
 ("63-hex",          b"_gitlab_session="+H63+b"\n", False),
 ("65-hex",          b"_gitlab_session="+H65+b"\n", False),
 ("upper",           b"_gitlab_session="+b"0A"*32+b"\n", False),
 ("prefixed-key",    b"my_gitlab_session="+H+b"\n", False),
 ("tab-sep",         b"_gitlab_session\t"+H+b"\n", True),
 ("dash-key",        b"x-_gitlab_session="+H+b"\n", True),
 ("escaped-json-u003d", b'"_gitlab_session\\u003d'+H+b'"', False),
]
for name,data,want in cases:
    got=bool(P["gitlab-session-cookie"].search(data))
    print("%-20s got=%-5s want=%-5s %s" % (name,got,want,"OK" if got==want else "<<< MISMATCH"))
print()
print("S140 regex (no right boundary) on 65-hex value:", bool(re.search(rb"(?:cell-[0-9]+-)?[0-9a-f]{64}", b"_gitlab_session="+H65)))
print("landing on 65-hex value:", bool(P["gitlab-session-cookie"].search(b"_gitlab_session="+H65)))
