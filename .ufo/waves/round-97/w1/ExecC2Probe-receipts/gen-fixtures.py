#!/usr/bin/env python3
"""ExecC2Probe independent fixture generator (probe seat, NOT the round-97 gate's).

Builds, for each of the ten new round-97 GitLab shapes (C2 landing a9a53608):
  3 positives: bare text, inside a JSON string, after a literal backslash escape
  3 negatives: tail one char short, tail one char long, wrong case where the rule has case

Case-negative placement: nine shapes draw the tail from A-Za-z0-9_- (case-insensitive
class, S140 lines 101/160/174/190/278/341/392/412) so the rule's case lives in the
case-sensitive prefix literal -> the prefix is flipped. gitlab-incoming-email-token
has a case-constrained tail [0-9a-z]{20,25} (S140 line 229) -> a tail char is flipped.

Writes fixtures under $PROBE_DIR/fixtures/, a manifest TSV and a bytes dump.
All token values are synthetic. No real credential material is used anywhere.
"""
import os

S = os.environ.get("PROBE_DIR") or "/fast/scratch/hyaku/kasegi-r97/ExecC2Probe"
FIX = os.path.join(S, "fixtures")

def mix_tail(n):
    """Tail of [A-Za-z0-9_-], no 'gl', '-'/'_' exercised mid-tail (alnum neighbours)."""
    base = "Qw7Zx2Ce9Vb4Nm6Kj8Lp"  # 20 chars, no 'g'
    t = (base * (n // len(base) + 1))[:n]
    i1, i2 = n // 4, n // 2
    t = t[:i1] + "-" + t[i1 + 1:]
    t = t[:i2] + "_" + t[i2 + 1:]
    tb = t.encode()
    assert len(tb) == n and b"gl" not in tb and b"GL" not in tb and b"-g" not in tb, tb
    return t

def lower_tail(n):
    """Tail of [a-z0-9] only (glimt- rule), no 'gl' anywhere."""
    t = ("abcdefghijklmnopqrstuvwxyz0123456789" * 3)[:n]
    tb = t.encode()
    assert len(tb) == n and all(c in b"abcdefghijklmnopqrstuvwxyz0123456789" for c in tb)
    assert b"gl" not in tb
    return t

# id, prefix literal, tail kind, positive tail length, short len, long len, case-flip target
SHAPES = [
    ("gitlab-runner-registration-token", b"GR1348941",               "mix",   20, 19, 21, "prefix"),
    ("gitlab-feed-token",                b"feed_token=",             "mix",   20, 19, 21, "prefix"),
    ("gitlab-oauth-app-secret",          b"gloas-",                  "mix",   64, 63, 65, "prefix"),
    ("gitlab-feed-token-v2",             b"glft-",                   "mix",   20, 19, 21, "prefix"),
    ("gitlab-incoming-email-token",      b"glimt-",                  "lower", 22, 19, 26, "tail"),
    ("gitlab-scim-oauth-token",          b"glsoat-",                 "mix",   20, 19, 21, "prefix"),
    ("gitlab-deploy-token-in-url",       b"gitlab+deploy-token-15:", "mix",   20, 19, 21, "prefix"),
    ("gitlab-feature-flags-client-token", b"glffct-",                "mix",   20, 19, 21, "prefix"),
    ("gitlab-runner-controller-token",   b"glrct-",                  "mix",   20, 19, 21, "prefix"),
    ("gitlab-kubernetes-agent-token",    b"glagent-",                "mix",   50, 49, 51, "prefix"),
]

def url_for(shape, token):
    if shape == "gitlab-deploy-token-in-url":
        return b"https://" + token + b"@gitlab.example/proj.git"
    return b"https://" + token + b"gitlab.example/proj.git"

def embed(shape, token, variant):
    if variant in ("short", "long", "case"):
        variant = "bare"  # negatives live in the same bare context as the bare positive
    if shape == "gitlab-deploy-token-in-url":
        value = url_for(shape, token)
    elif shape == "gitlab-feed-token":
        value = b"https://gitlab.example/api/v4/issues?" + token + b"&scope=all"
    else:
        value = token
    if variant == "bare":
        if shape == "gitlab-deploy-token-in-url" or shape == "gitlab-feed-token":
            return value + b"\n"
        return b"cfg " + token + b" end\n"
    if variant == "json":
        key = b"remote" if shape == "gitlab-deploy-token-in-url" else (b"q" if shape == "gitlab-feed-token" else b"cfg")
        return b'{"' + key + b'": "' + value + b'"}\n'
    if variant == "escape":
        if shape == "gitlab-deploy-token-in-url":
            return b"x\\n" + token + b"@gitlab.example\n"
        if shape == "gitlab-feed-token":
            return b"url=\\t" + token + b"\n"
        return b"cfg:\\t" + token + b"\n"
    raise ValueError(variant)

def main():
    os.makedirs(FIX, exist_ok=True)
    manifest, bytedump = [], []
    for idx, (shape, prefix, kind, plen, slen, llen, casetgt) in enumerate(SHAPES, 1):
        tail = mix_tail(plen) if kind == "mix" else lower_tail(plen)
        short_tail = tail[:slen]
        long_tail = mix_tail(llen) if kind == "mix" else lower_tail(llen)
        case_tail = tail[:2] + tail[2].upper() + tail[3:] if casetgt == "tail" else tail
        if shape == "gitlab-deploy-token-in-url":
            case_prefix = prefix.replace(b"gitlab", b"Gitlab", 1)
        elif shape == "gitlab-runner-registration-token":
            case_prefix = prefix.lower()  # GR1348941 -> gr1348941 (literal is upper-case)
        else:
            case_prefix = prefix.upper()
        variants = [
            ("bare",   prefix + tail.encode(),  False),
            ("json",   prefix + tail.encode(),  False),
            ("escape", prefix + tail.encode(),  False),
            ("short",  prefix + short_tail.encode(), False),
            ("long",   prefix + long_tail.encode(),  False),
            ("case",   (case_prefix if casetgt == "prefix" else prefix) + case_tail.encode(), True),
        ]
        for name, token, _ in variants:
            data = embed(shape, token, name)
            rel = "%02d-%s.%s.txt" % (idx, shape.removeprefix("gitlab-"), name)
            with open(os.path.join(FIX, rel), "wb") as fh:
                fh.write(data)
            manifest.append((rel, shape, name, "pos" if name in ("bare", "json", "escape") else "neg",
                             shape if name in ("bare", "json", "escape") else "-"))
            bytedump.append((rel, repr(data)))
    with open(os.path.join(S, "manifest.tsv"), "w") as fh:
        for row in manifest:
            fh.write("\t".join(row) + "\n")
    with open(os.path.join(S, "fixture-bytes.txt"), "w") as fh:
        for rel, rep in bytedump:
            fh.write("%s\t%s\n" % (rel, rep))
    print("wrote %d fixtures" % len(manifest))

if __name__ == "__main__":
    main()
