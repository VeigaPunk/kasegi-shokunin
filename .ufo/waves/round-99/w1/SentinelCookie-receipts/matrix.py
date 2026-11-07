#!/usr/bin/env python3
"""SentinelCookie round-99 C2 attack matrix: the landed session-cookie window.

Compares the landed `gitlab-session-cookie` shape (and the full gate set) at
the C2 landing against a faithful translation of S140's generated
assignment-context regex, over a matrix of separator / context / prefix /
_geo_ / gap / case / right-boundary / left-boundary / value payloads.

Every 64-hex value is built from H at runtime, never inlined, so this file and
its output stay clean under the landed scanner.
"""
import importlib.util
import os
import re
import shutil
import sys

H = b"0123456789abcdef" * 4  # 64 lower-case hex
H63 = H[:63]
H65 = H + b"0"
H72 = H + b"01234567"
H73 = H + b"012345678"

# S140:549 value + S140:550 keywordGroup, expanded by the assignmentContext
# generator (S150) to `<keyword>.{0,8}[:=].{0,8}<value>`.
S140_BYTES = re.compile(
    rb"_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}"
    rb"(?:cell-[0-9]+-)?[0-9a-f]{64}")
S140_RUNES = re.compile(
    r"_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}"
    r"(?:cell-[0-9]+-)?[0-9a-f]{64}")


def load(path, lane, work, tag):
    stage = os.path.join(work, "inst-" + tag)
    os.makedirs(stage, exist_ok=True)
    dst = os.path.join(stage, "capture-secret-scan.py")
    shutil.copyfile(path, dst)
    shutil.copyfile(os.path.join(lane, "corpus", "instruments", "claim-package-check.py"),
                    os.path.join(stage, "claim-package-check.py"))
    spec = importlib.util.spec_from_file_location("scanner_" + tag, dst)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build():
    m = []

    def add(fam, pid, data):
        m.append((fam, pid, data))

    K = b"_gitlab_session"
    # --- separators, plain assignment -------------------------------------
    seps = [
        ("eq", b"="), ("colon", b":"), ("rocket-space", b" => "),
        ("pct20-eq", b"%20=%20"), ("pct3a", b"%3A"), ("comma-eq", b",="),
        ("pipe-eq", b"|="), ("plus-eq", b"+="), ("paren-eq", b"(="),
        ("paren-gap", b" ( = ) "), ("rocket", b"=>"), ("colon-eq", b":="),
        ("eq-colon", b"=:"), ("colon-colon", b"::"), ("eq-eq", b"=="),
        ("space-eq-space", b" = "), ("tab-eq", b"\t="), ("cr-eq", b"\r="),
        ("pct3d", b"%3D"), ("ent61", b"&#61;"), ("entx3d", b"&#x3D;"),
        ("uesc3d", b"\\u003d"), ("uesc3D", b"\\u003D"), ("amp-equals", b"&equals;"),
        ("arrow", b"->"), ("colon-eq-colon", b":=:"), ("pct20-colon", b"%20:%20"),
        ("pct09", b"%09=%09"), ("vt-eq", b"\v="), ("ff-eq", b"\f="),
        ("semi-eq", b";="), ("dot-eq", b".="), ("bracket-eq", b"]="),
        ("brace-eq", b"}="), ("lt-eq", b"<="), ("gt-eq", b">="),
        ("slash-eq", b"/="), ("star-eq", b"*="), ("amp-eq", b"&="),
    ]
    for name, sep in seps:
        add("sep", "sep-" + name, K + sep + H + b"\n")

    # --- contexts ---------------------------------------------------------
    ctx = [
        ("json-space", b'{"_gitlab_session": "' + H + b'"}'),
        ("json-nospace", b'{"_gitlab_session":"' + H + b'"}'),
        ("json-single", b"{'_gitlab_session': '" + H + b"'}"),
        ("json-esc-nl", b'{"_gitlab_session\\n": "' + H + b'"}'),
        ("header", b"Set-Cookie: _gitlab_session=" + H + b"; Path=/; HttpOnly"),
        ("cookie-header", b"Cookie: foo=1; _gitlab_session=" + H + b"; bar=2"),
        ("cookie-jar-tab", b".gitlab.com\tTRUE\t/\tTRUE\t0\t_gitlab_session\t" + H + b"\n"),
        ("cookie-jar-space", b".gitlab.com TRUE / TRUE 0 _gitlab_session " + H + b"\n"),
        ("url-query", b"?x=1&_gitlab_session=" + H + b"&y=2"),
        ("url-query-enc", b"?_gitlab_session%3D" + H),
        ("markdown-cell", b"| `_gitlab_session` | " + H + b" |"),
        ("markdown-code", b"`_gitlab_session=" + H + b"`"),
        ("log-line", b"2026-11-07T00:00:00Z INFO session _gitlab_session=" + H + b" set"),
        ("rails-params", b'  Parameters: {"_gitlab_session"=>"' + H + b'"}'),
        ("ruby-hash", b'{"_gitlab_session" => "' + H + b'"}'),
        ("yaml", b"_gitlab_session: " + H + b"\n"),
        ("ini", b"_gitlab_session = " + H + b"\n"),
        ("env", b"GITLAB_SESSION=" + H + b"\n"),
        ("python-repr", b"{'_gitlab_session': '" + H + b"'}"),
        ("go-map", b"map[_gitlab_session:" + H + b"]"),
        ("shell-export", b"export _gitlab_session=" + H + b"\n"),
        ("har-object", b'{"name": "_gitlab_session", "value": "' + H + b'"}'),
        ("har-object-tight", b'{"name":"_gitlab_session","value":"' + H + b'"}'),
        ("sql", b"INSERT INTO s VALUES ('_gitlab_session', '" + H + b"')"),
        ("curl-h", b"-H 'Cookie: _gitlab_session=" + H + b"'"),
        ("docker-e", b"-e _gitlab_session=" + H),
    ]
    for name, data in ctx:
        add("ctx", "ctx-" + name, data)

    # --- cell prefixes ----------------------------------------------------
    for name, pre in [("cell12", b"cell-12-"), ("cell0", b"cell-0-"),
                      ("cell007", b"cell-007-"), ("cell-empty", b"cell-"),
                      ("cell-double-dash", b"cell--"), ("cell-alpha", b"cell-abc-"),
                      ("cell-upper", b"CELL-12-"), ("cell-huge", b"cell-" + b"9" * 24 + b"-"),
                      ("cell-two", b"cell-1-cell-2-"), ("cell-underscore", b"cell-12_")]:
        add("prefix", "pre-" + name, K + b"=" + pre + H + b"\n")
        add("prefix", "pre-" + name + "-rocket", K + b" => " + pre + H + b"\n")

    # --- _geo_ forms ------------------------------------------------------
    G = b"_gitlab_session_geo_" + H
    geo = [
        ("geo-eq", G + b"=" + H + b"\n"),
        ("geo-pct20", G + b"%20=%20" + H + b"\n"),
        ("geo-cell", G + b"=cell-7-" + H + b"\n"),
        ("geo-short", b"_gitlab_session_geo_" + H63 + b"=" + H + b"\n"),
        ("geo-upper", b"_gitlab_session_geo_" + H.upper() + b"=" + H + b"\n"),
        ("geo-nosep", G + H + b"\n"),
        ("geo-twice", G + b"_geo_" + H + b"=" + H + b"\n"),
        ("geo-nl", G + b"\n=" + H + b"\n"),
        ("geo-space", G + b" " + H + b"\n"),
        ("geo-rocket", G + b" => " + H + b"\n"),
    ]
    for name, data in geo:
        add("geo", name, data)

    # --- gap widths -------------------------------------------------------
    for k in range(0, 13):
        add("gap-before", "gapb-%02d" % k, K + b" " * k + b"=" + H + b"\n")
        add("gap-after", "gapa-%02d" % k, K + b"=" + b" " * k + H + b"\n")
    for k in (1, 8, 9, 12):
        add("gap-tab", "gapt-%02d" % k, K + b"\t" * k + b"=" + H + b"\n")
        add("gap-tab-after", "gapta-%02d" % k, K + b"=" + b"\t" * k + H + b"\n")
    nl = [
        ("nl-before-eq", K + b"\n=" + H + b"\n"),
        ("nl-after-eq", K + b"=\n" + H + b"\n"),
        ("nl-both", K + b"\n=\n" + H + b"\n"),
        ("nl-space-eq", K + b" \n = " + H + b"\n"),
        ("crlf-before-eq", K + b"\r\n=" + H + b"\r\n"),
        ("crlf-after-eq", K + b"=\r\n" + H + b"\r\n"),
        ("cr-before-eq", K + b"\r=" + H + b"\n"),
        ("cr-after-eq", K + b"=\r" + H + b"\n"),
        ("nl-tab-eq", K + b"\n\t= " + H + b"\n"),
    ]
    for name, data in nl:
        add("gap-newline", name, data)

    # --- keyword case -----------------------------------------------------
    for name, kw in [("title", b"_GitLab_Session"), ("upper", b"_GITLAB_SESSION"),
                     ("mixed1", b"_gitlab_Session"), ("mixed2", b"_Gitlab_session"),
                     ("mixed3", b"_GITLAB_session")]:
        add("case", "case-" + name, kw + b"=" + H + b"\n")

    # --- right boundary ---------------------------------------------------
    for name, tail in [("eol", b"\n"), ("quote", b'"'), ("amp", b"&"), ("semi", b";"),
                       ("underscore", b"_"), ("hyphen", b"-"), ("g", b"g"),
                       ("hex0", b"0"), ("pct", b"%"), ("space", b" "),
                       ("crlf", b"\r\n"), ("dot", b"."), ("comma", b","),
                       ("tab", b"\t"), ("colon", b":"), ("eq", b"="),
                       ("slash", b"/"), ("plus", b"+"), ("nul", b"\x00"),
                       ("vtab", b"\x0b")]:
        add("right", "right-" + name, K + b"=" + H + tail)
    add("right", "right-65hex", K + b"=" + H65 + b"\n")
    add("right", "right-72hex", K + b"=" + H72 + b"\n")
    add("right", "right-73hex", K + b"=" + H73 + b"\n")

    # --- left boundary ----------------------------------------------------
    for name, pre in [("x", b"x"), ("digit", b"2"), ("under", b"_"),
                      ("word", b"my"), ("upper", b"A"), ("dash", b"-"),
                      ("dot", b"."), ("pct20", b"%20"), ("quote", b"'"),
                      ("backslash-n", b"\\n")]:
        add("left", "left-" + name, pre + K + b"=" + H + b"\n")

    # --- value grammar ----------------------------------------------------
    val = [
        ("63hex", K + b"=" + H63 + b"\n"),
        ("upper", K + b"=" + H.upper() + b"\n"),
        ("mixed-case", K + b"=" + H[:32] + H[32:].upper() + b"\n"),
        ("hyphen-mid", K + b"=" + H[:32] + b"-" + H[33:] + b"\n"),
        ("underscore-mid", K + b"=" + H[:32] + b"_" + H[33:] + b"\n"),
        ("base64ish", K + b"=" + H[:60] + b"+/==" + b"\n"),
        ("cell-then-63", K + b"=cell-12-" + H63 + b"\n"),
        ("cell-then-65", K + b"=cell-12-" + H65 + b"\n"),
        ("no-keyword", b"session=" + H + b"\n"),
        ("other-keyword", b"_other_session=" + H + b"\n"),
    ]
    for name, data in val:
        add("value", "val-" + name, data)

    # --- non-ASCII separators (Go counts runes, bytes-regex counts bytes) --
    uni = [
        ("nbsp5", K + b"\xc2\xa0" * 5 + b"=" + H + b"\n"),
        ("nbsp4", K + b"\xc2\xa0" * 4 + b"=" + H + b"\n"),
        ("arrow3", K + b"\xe2\x86\x92" * 3 + b"=" + H + b"\n"),
        ("arrow2", K + b"\xe2\x86\x92" * 2 + b"=" + H + b"\n"),
        ("emspace3", K + b"\xe2\x80\x83" * 3 + b"=" + H + b"\n"),
        ("nbsp-after-eq", K + b"=" + b"\xc2\xa0" * 5 + H + b"\n"),
    ]
    for name, data in uni:
        add("unicode", name, data)
    return m


def main(argv):
    lane = argv[1]
    work = argv[2]
    landed = load(os.path.join(lane, "corpus", "instruments", "capture-secret-scan.py"),
                  lane, work, "landed")
    r98 = load(os.path.join(work, "r98", "capture-secret-scan.py"), lane, work, "r98")
    pats_l = landed.patterns()
    pats_9 = r98.patterns()
    rows = []
    for fam, pid, data in build():
        got_l = {s for s, _ in landed.scan_bytes(data, pats_l)[0]}
        got_9 = {s for s, _ in r98.scan_bytes(data, pats_9)[0]}
        sb = bool(S140_BYTES.search(data))
        try:
            sr = bool(S140_RUNES.search(data.decode("utf-8")))
        except UnicodeDecodeError:
            sr = None
        if not got_l and sb:
            verdict = "MUST-FIX"
        elif not got_l and not sb and sr:
            verdict = "MUST-FIX-RUNE"
        elif not got_l and got_9:
            verdict = "REGRESSION-R98"
        elif got_l and not sb:
            verdict = "SCANNER-ONLY"
        elif got_l and sb:
            verdict = "AGREE-HIT"
        else:
            verdict = "AGREE-MISS"
        rows.append((fam, pid, verdict, sorted(got_l), sorted(got_9), sb, sr))
        print("%-14s %-26s %-14s landed=%-28s r98=%-28s s140b=%-5s s140r=%s"
              % (fam, pid, verdict, ",".join(sorted(got_l)) or "-",
                 ",".join(sorted(got_9)) or "-", sb, sr))
    counts = {}
    for r in rows:
        counts[r[2]] = counts.get(r[2], 0) + 1
    print("MATRIX cases=%d %s" % (len(rows),
          " ".join("%s=%d" % (k, counts[k]) for k in sorted(counts))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
