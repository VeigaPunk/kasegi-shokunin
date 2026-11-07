#!/usr/bin/env python3
"""ExecC2Probe independent fixture generator (round-99 C2).

Builds 24 positives (the twelve round-98 MUST-FIX payload shapes verbatim plus
twelve NEW separator variants of my own choosing) and 24 boundary negatives for
the `gitlab-session-cookie` assignment-context window, in a scratch git repo,
with nonce-derived file names and nonce-derived 64-hex values. All values are
synthetic; nothing here is a real credential.

Usage: gen_fixtures.py <fixture-dir>
Writes <fixture-dir>/cases/{pos,neg}/<sha20>-<slug>.txt, manifest.json,
payloads.txt (exact bytes, python-escaped), nonce.txt.
"""
import hashlib
import json
import os
import sys

D = os.path.abspath(sys.argv[1])
os.makedirs(D, exist_ok=True)

# Nonce: fresh per run, persisted so the run is reproducible given the nonce.
NONCE = os.urandom(16).hex()


def hex64(tag):
    """64 lower-case hex, nonce-derived."""
    return hashlib.sha256((NONCE + "|" + tag).encode()).hexdigest()


def name_for(kind, slug):
    """Nonce-derived path: cases/<kind>/<sha256(nonce|kind|slug)[:20]>-<slug>.txt"""
    h = hashlib.sha256((NONCE + "|" + kind + "|" + slug).encode()).hexdigest()[:20]
    return "cases/%s/%s-%s.txt" % (kind, h, slug)


# ---- the twelve round-98 MUST-FIX shapes (SentinelShapes-receipts/final-checks.txt:15-26) ----
MUSTFIX = [
    ("m01-len-cookie-cell0", b"_gitlab_session=cell--"),
    ("m02-ruby-hash-rocket", b"_gitlab_session => "),
    ("m03-pct20-eq", b"_gitlab_session%20=%20"),
    ("m04-pct20-colon", b"_gitlab_session%20:%20"),
    ("m05-pct20-after-eq", b"_gitlab_session=%20"),
    ("m06-paren-eq", (b"_gitlab_session(=", b")")),
    ("m07-paren-gap", b"_gitlab_session ( = ) "),
    ("m08-comma-eq", b"_gitlab_session,="),
    ("m09-pipe-eq", b"_gitlab_session|="),
    ("m10-plus-eq", b"_gitlab_session+="),
    ("m11-rocket-nospace", b"_gitlab_session=> "),
    ("m12-geo-pct20", None),  # special: geo id + %20=%20 + value
]

# ---- twelve NEW separator variants (my own; all inside S140's [^\n]{0,8}[:=][^\n]{0,8} window) ----
NEWPOS = [
    ("n01-tab-assign", b"_gitlab_session\t=\t"),
    ("n02-yaml-colon-space", b"_gitlab_session: "),
    ("n03-json-quoted", (b"\"", b"\": \"", b"\"")),  # "_gitlab_session": "H"
    ("n04-single-quoted", (b"", b"='", b"'")),      # _gitlab_session='H'
    ("n05-shell-interp", b"_gitlab_session=\"${"),  # _gitlab_session="${H}"
    ("n06-dict-access", (b"resp[\"x\"][\"", b"\"] = ", b"")),  # resp["x"]["_gitlab_session"] = H
    ("n07-double-space-assign", b"_gitlab_session  =  "),
    ("n08-double-equals", b"_gitlab_session=="),
    ("n09-geo-tab-colon", None),  # special: _gitlab_session_geo_<G>\t:\tH
    ("n10-cell-colon", b"_gitlab_session:cell-31-"),
    ("n11-pct20-after-colon", b"_gitlab_session:%20"),
    ("n12-cookie-header", b"Cookie: _gitlab_session="),  # ...; Path=/; HttpOnly
]

# ---- twenty-four boundary negatives, each with the regex reason it must not hit ----
NEG = [
    ("b01-left-window-9-dashes", b"_gitlab_session---------=" + hex64("b01").encode() + b"\n"),
    ("b02-right-window-9-dashes", b"_gitlab_session=---------" + hex64("b02").encode() + b"\n"),
    ("b03-newline-after-sep", b"_gitlab_session=\n" + hex64("b03").encode() + b"\n"),
    ("b04-newline-before-sep", b"_gitlab_session\n=" + hex64("b04").encode() + b"\n"),
    ("b05-value-63-hex", b"_gitlab_session=" + hex64("b05").encode()[:63] + b"\n"),
    ("b06-value-65-hex", b"_gitlab_session=" + (hex64("b06") + "c").encode() + b"\n"),
    ("b07-upper-hex", b"_gitlab_session=" + hex64("b07").upper().encode() + b"\n"),
    ("b08-base64-value", b"_gitlab_session=gH7+/9xQ" + hex64("b08").encode()[8:60] + b"zz==\n"),
    ("b09-hyphen-split-value", b"_gitlab_session=" + hex64("b09a").encode()[:63] + b"-" + hex64("b09b").encode()[:31] + b"\n"),
    ("b10-no-separator", b"_gitlab_session " + hex64("b10").encode() + b"\n"),
    ("b11-left-window-12-spaces", b"_gitlab_session            : " + hex64("b11").encode() + b"\n"),
    ("b12-cell-nondigit", b"_gitlab_session=cell-abc-" + hex64("b12").encode() + b"\n"),
    ("b13-geo-id-63-hex", b"_gitlab_session_geo_" + hex64("b13").encode()[:63] + b"=" + hex64("b13v").encode() + b"\n"),
    ("b14-upper-keyword", b"_Gitlab_Session=" + hex64("b14").encode() + b"\n"),
    ("b15-url-hex-no-keyword", b"https://gitlab.example/api/v4/projects?cursor=" + hex64("b15").encode() + b"\n"),
    ("b16-value-32-hex", b"_gitlab_session=" + hex64("b16").encode()[:32] + b"\n"),
    ("b17-crlf-before-value", b"_gitlab_session=\r\n" + hex64("b17").encode() + b"\n"),
    ("b18-word-char-before-keyword", b"pref_gitlab_session=" + hex64("b18").encode() + b"\n"),
    ("b19-left-window-9-letters", b"_gitlab_sessionabcdefghi: " + hex64("b19").encode() + b"\n"),
    ("b20-right-window-9-spaces", b"_gitlab_session=         " + hex64("b20").encode() + b"\n"),
    ("b21-geo-gap-9-spaces", b"_gitlab_session_geo_" + hex64("b21g").encode() + b"         =" + hex64("b21").encode() + b"\n"),
    ("b22-wrong-cookie-name", b"session=" + hex64("b22").encode() + b"\n"),
    ("b23-no-underscore-keyword", b"_gitlabsession=" + hex64("b23").encode() + b"\n"),
    ("b24-tabs-no-sep", b"_gitlab_session\t\t" + hex64("b24").encode() + b"\n"),
]


def build_pos(slug, spec):
    """Return exact bytes for a positive case."""
    h = hex64("val|" + slug)
    if slug == "m12-geo-pct20":
        g = hex64("geo|" + slug)
        return b"_gitlab_session_geo_" + g.encode() + b"%20=%20" + h.encode() + b"\n"
    if slug == "n09-geo-tab-colon":
        g = hex64("geo|" + slug)
        return b"_gitlab_session_geo_" + g.encode() + b"\t:\t" + h.encode() + b"\n"
    if isinstance(spec, tuple):
        if slug == "m06-paren-eq":
            pre, post = spec
            return pre + h.encode() + post + b"\n"
        if slug == "n03-json-quoted":
            return spec[0] + b"_gitlab_session" + spec[1] + h.encode() + spec[2] + b"\n"
        if slug == "n04-single-quoted":
            return b"_gitlab_session" + spec[1] + h.encode() + spec[2] + b"\n"
        if slug == "n06-dict-access":
            return spec[0] + b"_gitlab_session" + spec[1] + h.encode() + spec[2] + b"\n"
        raise AssertionError(slug)
    return spec + h.encode() + b"\n"


def main():
    cases = []       # ordered manifest rows
    files = []       # absolute paths for the scanner
    payloads = []    # exact payload text per case

    for slug, spec in MUSTFIX:
        data = build_pos(slug, spec)
        cases.append({"case": slug, "class": "pos", "origin": "round98-mustfix", "data": data})
    for slug, spec in NEWPOS:
        data = build_pos(slug, spec)
        cases.append({"case": slug, "class": "pos", "origin": "new-separator-variant", "data": data})
    for slug, data in NEG:
        cases.append({"case": slug, "class": "neg", "origin": "boundary-negative", "data": data})

    for c in cases:
        rel = name_for(c["class"], c["case"])
        abs_path = os.path.join(D, rel)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "wb") as fh:
            fh.write(c["data"])
        c["path"] = rel
        files.append(abs_path)
        payloads.append("%s\t%s\t%s\t%r" % (c["class"], c["origin"], c["case"], c["data"]))
        del c["data"]

    with open(os.path.join(D, "nonce.txt"), "w") as fh:
        fh.write(NONCE + "\n")
    with open(os.path.join(D, "manifest.json"), "w") as fh:
        json.dump({"nonce": NONCE, "n_pos": sum(1 for c in cases if c["class"] == "pos"),
                   "n_neg": sum(1 for c in cases if c["class"] == "neg"),
                   "cases": cases}, fh, indent=1)
    with open(os.path.join(D, "payloads.txt"), "w") as fh:
        fh.write("\n".join(payloads) + "\n")
    for p in files:
        print(p)


if __name__ == "__main__":
    main()
