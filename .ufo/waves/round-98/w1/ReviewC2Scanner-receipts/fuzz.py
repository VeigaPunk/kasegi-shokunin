#!/usr/bin/env python3
"""Differential body-grammar fuzz: landing patterns vs reference regexes
transcribed from S140.txt (POSIX classes translated to ASCII ranges)."""
import importlib.util, re, random
s=importlib.util.spec_from_file_location("L","/fast/scratch/hyaku/kasegi-r98/ReviewC2Scanner/landing/corpus/instruments/capture-secret-scan.py")
L=importlib.util.module_from_spec(s); s.loader.exec_module(L)
P=dict(L.GITLAB_PATTERNS)
PUNCT=rb"[!-/:-@\[-`{-~]"; SPACE=rb"[ \t\n\r\f\v]"; B=rb"(?:"+PUNCT+rb"|"+SPACE+rb"|$)"
REF={
 "gitlab-ci-build-token": rb"(?<![A-Za-z0-9_])(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\-]{20})"+B,
 "gitlab-runner-registration-token": rb"(?<![A-Za-z0-9_])(GR1348941[0-9a-zA-Z_\-]{20})"+B,
 "gitlab-feed-token": rb"(?<![A-Za-z0-9_])(feed_token=[0-9a-zA-Z_\-]{20})"+B,
 "gitlab-oauth-app-secret": rb"(?<![A-Za-z0-9_])(gloas-[0-9a-zA-Z_\-]{64})"+B,
 "gitlab-feed-token-v2": rb"(?<![A-Za-z0-9_])(glft-[0-9a-zA-Z_\-]{20})"+B,
 "gitlab-scim-oauth-token": rb"(?<![A-Za-z0-9_])(glsoat-[0-9a-zA-Z_\-]{20})"+B,
 "gitlab-iam-refresh-token": rb"(?<![A-Za-z0-9_])(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)",
 "gitlab-iam-authorization-code": rb"(?<![A-Za-z0-9_])(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)",
}
REF={k:re.compile(v,re.S) for k,v in REF.items()}
HEADS={"gitlab-ci-build-token":b"glcbt-","gitlab-runner-registration-token":b"GR1348941",
 "gitlab-feed-token":b"feed_token=","gitlab-oauth-app-secret":b"gloas-",
 "gitlab-feed-token-v2":b"glft-","gitlab-scim-oauth-token":b"glsoat-",
 "gitlab-iam-refresh-token":b"gliamrt-","gitlab-iam-authorization-code":b"gliamac-"}
rnd=random.Random(98); ALPHA=b"aZ09_-."; CTRL=bytes(range(0,32))+bytes([127])
for shape,head in HEADS.items():
    n=0; samples=[]
    for _ in range(40000):
        body=bytes(rnd.choice(ALPHA) for _ in range(rnd.randint(0,110)))
        tail=bytes([rnd.choice(CTRL)]) if rnd.random()<0.15 else rnd.choice([b" ",b"\n",b";",b"x",b"",b"\xc3\xa9"])
        data=head+body+tail
        o=bool(P[shape].search(data)); r=bool(REF[shape].search(data))
        if o!=r:
            n+=1
            if len(samples)<3: samples.append((data[:60],o,r))
    print("%-40s body-fuzz mismatches=%d %s" % (shape,n,samples))
