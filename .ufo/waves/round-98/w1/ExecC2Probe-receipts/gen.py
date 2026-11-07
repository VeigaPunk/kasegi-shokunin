#!/usr/bin/env python3
"""ExecC2Probe independent fixture generator + nine-shape probe (round 98).

Builds 22 positives (four new shapes x 3 variants, five widened shapes x 2
boundary variants) and 21 boundary negatives in a scratch git repo with
nonce-derived paths, then runs BOTH the C2-landing instrument (e2caf4a1)
and the round-97 instrument (a9a5360) with --files over them and compares
observed vs hand-derived expected hit sets.

All plant values are generated from each rule's own grammar with a
deterministic per-file seed (never copied from the instrument's selftest),
then scrubbed of every other rule's marker substring so that any hit
outside the expected set is a genuine instrument behaviour, not generator
noise. Values are not printed; the manifest carries sha256 digests and the
generation recipe is this script (regenerate byte-exact with SEEDS below).
"""
import hashlib, json, os, random, re, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
LANDED = os.path.join(S, "landed", "capture-secret-scan.py")
R97 = os.path.join(S, "r97", "capture-secret-scan.py")
D = os.path.join(S, "fx")

ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
WORD = ALNUM + "_-"
HEX = "0123456789abcdef"

# Marker substrings of every OTHER detection rule; scrubbed from generated
# values so extra hits can only come from the instrument, not the generator.
FORBIDDEN = ["glcbt-", "glsat-", "gliamat-", "gliamrt-", "gliamac-", "glptt-",
             "glft-", "glsoat-", "glffct-", "glrct-", "glagent-", "glpat-",
             "glrtr-", "glrt-", "gldt-", "glwt-", "glimt-", "gloas-",
             "GR1348941", "feed_token", "gitlab_session", "gitlab+deploy",
             "eyJ", "AKIA", "ASIA", "ghp_", "ghs_", "gho_", "ghu_", "ghr_",
             "op://", "bearer"]


def gen(alphabet, n, seed):
    """n chars from alphabet via sha256-chained PRNG, scrubbed of FORBIDDEN."""
    rng = random.Random(seed)
    for _ in range(1000):
        v = "".join(rng.choice(alphabet) for _ in range(n))
        if not any(f in v for f in FORBIDDEN):
            return v
    raise RuntimeError("scrub exhausted for seed %r" % seed)


def seed_of(family, variant):
    return int(hashlib.sha256(("ExecC2Probe|%s|%s" % (family, variant))
                              .encode()).hexdigest()[:12], 16)


# ---- fixture table -----------------------------------------------------
# (family, variant, expected_landed_set, r97_should_hit, context_builder)
# Contexts avoid every gate/instrument keyword outside the nine shapes.
F = []
def add(family, variant, expected, r97, text):
    F.append((family, variant, frozenset(expected), r97, text))

# -- four NEW shapes x 3 variants (expected hit ONLY at the C2 landing) --
add("ci-build", "basic", ["gitlab-ci-build-token"], False,
    lambda g: "export GL_BUILD='%s'\n" % ("glcbt-" + g("alnum", 4) + "_" + g("word", 20)))
add("ci-build", "min-prefix", ["gitlab-ci-build-token"], False,
    lambda g: "cfg %s\n" % ("glcbt-" + g("alnum", 1) + "_" + g("word", 20)))
add("ci-build", "max-prefix-trailing-underscore", ["gitlab-ci-build-token"], False,
    lambda g: "run id=%s_x\n" % ("glcbt-" + g("alnum", 5) + "_" + g("word", 20)))
add("iam-refresh", "basic", ["gitlab-iam-refresh-token"], False,
    lambda g: "refresh %s\n" % ("gliamrt-" + g("word", 43) + "." + g("word", 43)))
add("iam-refresh", "json-value", ["gitlab-iam-refresh-token"], False,
    lambda g: '{"refresh": "%s"}\n' % ("gliamrt-" + g("word", 43) + "." + g("word", 43)))
add("iam-refresh", "trailing-dot", ["gitlab-iam-refresh-token"], False,
    lambda g: "v1 %s.more\n" % ("gliamrt-" + g("word", 43) + "." + g("word", 43)))
add("iam-auth-code", "semicolon", ["gitlab-iam-authorization-code"], False,
    lambda g: "code: %s;\n" % ("gliamac-" + g("word", 43) + "." + g("word", 43)))
add("iam-auth-code", "underscored-segments", ["gitlab-iam-authorization-code"], False,
    lambda g: ("gliamac-" + g("word", 43) + "." + g("word", 43) + "\n"))  # alphabet includes _ -
add("iam-auth-code", "eol", ["gitlab-iam-authorization-code"], False,
    lambda g: "%s" % ("gliamac-" + g("word", 43) + "." + g("word", 43) + "\n"))
add("session-cookie", "basic", ["gitlab-session-cookie"], False,
    lambda g: "Cookie: _gitlab_session=%s; Path=/\n" % g("hex", 64))
add("session-cookie", "cell-quoted", ["gitlab-session-cookie"], False,
    lambda g: '_gitlab_session="cell-42-%s"\n' % g("hex", 64))
add("session-cookie", "geo-form", ["gitlab-session-cookie"], False,
    lambda g: "_gitlab_session_geo_%s=%s\n" % (g("hex", 64), g("hex", 64)))

# -- five WIDENED shapes x 2 boundary variants (hit only with the new
#    (?![A-Za-z0-9]) boundary; the round-97 (?![A-Za-z0-9_-]) refuses them) --
for fam, mk in [
    ("runner-registration", lambda g: "runner %s\n" % ("GR1348941" + g("word", 20))),
    ("feed-token", lambda g: "feed_token=%s\n" % g("word", 20)),
    ("oauth-app-secret", lambda g: "oa %s\n" % ("gloas-" + g("word", 64))),
    ("feed-token-v2", lambda g: "ftv2 %s\n" % ("glft-" + g("word", 20))),
    ("scim-oauth", lambda g: "scim %s\n" % ("glsoat-" + g("word", 20))),
]:
    for suf, lab in [("_x", "right-underscore"), ("-x", "right-hyphen")]:
        base = mk
        add(fam, lab, ["gitlab-" + fam.replace("runner-registration", "runner-registration-token")
                       .replace("feed-token-v2", "feed-token-v2")
                       .replace("oauth-app-secret", "oauth-app-secret")
                       .replace("feed-token", "feed-token")
                       .replace("scim-oauth", "scim-oauth-token")], False,
            lambda g, base=base, suf=suf: base(g).rstrip("\n") + suf + "\n")

# -- 21 boundary negatives (expected: no nine-shape hit at EITHER revision;
#    x-jwt-cross deliberately expects gitlab-jwt-token at both) --
add("x-ci", "prefix6", [], False,
    lambda g: "glcbt-%s_%s\n" % (g("alnum", 6), g("alnum", 20)))
add("x-ci", "payload19", [], False,
    lambda g: "glcbt-%s_%s\n" % (g("alnum", 3), g("alnum", 19)))
add("x-ci", "no-underscore", [], False,
    lambda g: "glcbt-%s\n" % g("alnum", 21))
add("x-iam-refresh", "seg42", [], False,
    lambda g: "gliamrt-%s.%s\n" % (g("word", 42), g("word", 43)))
add("x-iam-refresh", "no-dot", [], False,
    lambda g: "gliamrt-%s\n" % g("word", 86))
add("x-iam-auth-code", "seg44", [], False,
    lambda g: "gliamac-%s.%s\n" % (g("word", 44), g("word", 43)))
add("x-iam-auth-code", "trailing-underscore", [], False,
    lambda g: "gliamac-%s.%s_x\n" % (g("word", 43), g("word", 43)))
add("x-session-cookie", "hex63", [], False,
    lambda g: "_gitlab_session=%s\n" % g("hex", 63))
add("x-session-cookie", "no-separator", [], False,
    lambda g: "_gitlab_session%s\n" % g("hex", 64))
add("x-session-cookie", "uppercase-hex", [], False,
    lambda g: "_gitlab_session=%s\n" % g("hex", 64).upper())
add("x-runner-registration", "alnum-suffix", [], False,
    lambda g: "GR1348941%sa\n" % g("alnum", 20))
add("x-feed-token", "len19", [], False,
    lambda g: "feed_token=%s\n" % g("alnum", 19))
add("x-oauth-app-secret", "digit-suffix", [], False,
    lambda g: "gloas-%s9\n" % g("word", 64))
add("x-feed-token-v2", "upper-suffix", [], False,
    lambda g: "glft-%sA\n" % g("word", 20))
add("x-scim-oauth", "len19", [], False,
    lambda g: "glsoat-%s\n" % g("alnum", 19))
add("x-jwt-cross", "glcbt-eyj", ["gitlab-jwt-token"], True,
    lambda g: "glcbt-eyJ%s.eyJ%s.%s\n" % (g("word", 12), g("word", 12), g("word", 24)))
add("x-iam-refresh", "underscore-sep", [], False,
    lambda g: "gliamrt-%s_%s\n" % (g("word", 43), g("word", 43)))
add("x-session-cookie", "no-leading-underscore", [], False,
    lambda g: "gitlab_session=%s\n" % g("hex", 64))
add("x-session-cookie", "geo-second-63", [], False,
    lambda g: "_gitlab_session_geo_%s=%s\n" % (g("hex", 64), g("hex", 63)))
add("x-feed-token", "no-equals", [], False,
    lambda g: "feed_token %s\n" % g("alnum", 20))
add("x-session-cookie", "cell-no-digit", [], False,
    lambda g: "_gitlab_session=cell-%s\n" % g("hex", 64))

SHAPE_OF_FAMILY = {
    "runner-registration": "gitlab-runner-registration-token",
    "feed-[credential-fixture-redacted-r98]",
    "oauth-app-[credential-fixture-redacted-r98]",
    "feed-token-v2": "gitlab-feed-token-v2",
    "scim-oauth": "gitlab-scim-oauth-token",
    "ci-build": "gitlab-ci-build-token",
    "iam-refresh": "gitlab-iam-refresh-token",
    "iam-auth-code": "gitlab-iam-authorization-code",
    "[session-cookie-fixture-redacted-r98]",
    "jwt-cross": "gitlab-jwt-token",
}
FAMILY_MARKERS = {
    "ci-build": ["glcbt-"], "ci": ["glcbt-"], "iam-refresh": ["gliamrt-"],
    "iam-auth-code": ["gliamac-"], "session-cookie": ["_gitlab_session", "gitlab_session"],
    "runner-registration": ["GR1348941"], "feed-token": ["feed_token"],
    "oauth-app-secret": ["gloas-"], "feed-token-v2": ["glft-"],
    "scim-oauth": ["glsoat-"], "jwt-cross": ["glcbt-", "eyJ"],
}

# normalize widened family names to rule names
def rule_name(family):
    return SHAPE_OF_FAMILY.get(family, "gitlab-" + family)

# ---- build -------------------------------------------------------------
shutil.rmtree(D, ignore_errors=True)
os.makedirs(os.path.join(D, "c98"))
def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("%s -> %s%s" % (a, r.stdout, r.stderr))
    return r.stdout.strip()

sh("git", "-C", D, "init", "-q")
top = sh("git", "-C", D, "rev-parse", "--show-toplevel")
assert os.path.realpath(top) == os.path.realpath(D), "toplevel %r != %r" % (top, D)

manifest = []
for fam, var, exp, r97hit, build in F:
    g = lambda kind, n: gen({"alnum": ALNUM, "word": WORD, "hex": HEX}[kind], n,
                            seed_of(fam + "|" + var, kind + str(n)))
    text = build(g)
    base_fam = fam[2:] if fam.startswith("x-") else fam
    allowed = FAMILY_MARKERS.get(base_fam, [])
    assert not any(f in text for f in FORBIDDEN if f not in allowed), \
        "forbidden marker in %s/%s" % (fam, var)
    assert text.count("gitlab") <= 1 and not re.search(r"(?i)secret|password|api[_-]?key|bearer|authorization", text), \
        "risky context in %s/%s" % (fam, var)
    nonce = os.urandom(4).hex()
    rel = "c98/%s-%s-%s.txt" % (nonce, fam, var)
    with open(os.path.join(D, rel), "w") as fh:
        fh.write(text)
    manifest.append({"path": rel, "family": fam, "variant": var,
                     "expected_landed": sorted(exp), "r97_should_hit": r97hit,
                     "sha256": hashlib.sha256(text.encode()).hexdigest()})

sh("git", "-C", D, "add", "-A")
sh("git", "-C", D, "-c", "user.email=p@x", "-c", "user.name=p", "commit", "-qm", "probe fixtures")
assert not sh("git", "-C", D, "status", "--porcelain"), "dirty fixture repo"
print("FIXTURE-REPO ok toplevel=%s files=%d commit=%s"
      % (top, len(manifest), sh("git", "-C", D, "rev-parse", "HEAD")))

# ---- run both instruments ---------------------------------------------
def run(instr):
    r = subprocess.run([sys.executable, instr, "--files"] + [m["path"] for m in manifest],
                       cwd=D, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

rc_l, out_l, err_l = run(LANDED)
rc_9, out_9, err_9 = run(R97)

hits_l = {}
hits_9 = {}
for out, tgt in ((out_l, hits_l), (out_9, hits_9)):
    for line in out.splitlines():
        if line.startswith("HIT "):
            shape = re.search(r"shape=(\S+)", line).group(1)
            path = re.search(r"path=(\S+)", line).group(1)
            lineno = int(re.search(r"line=(\d+)", line).group(1))
            tgt.setdefault(path, []).append((shape, lineno))

n_miss = n_extra = n_ok = 0
print("\n=== per-file matrix (expected vs LANDED e2caf4a1 | r97 a9a5360) ===")
for m in manifest:
    p = m["path"]
    gl = sorted(s for s, _ in hits_l.get(p, []))
    g9 = sorted(s for s, _ in hits_9.get(p, []))
    exp = m["expected_landed"]
    miss = sorted(set(exp) - set(gl))
    extra = sorted(set(gl) - set(exp))
    status = "OK" if not miss and not extra else ("MISS+" + ",".join(miss) if miss else "") + \
             ("EXTRA+" + ",".join(extra) if extra else "")
    n_miss += bool(miss); n_extra += bool(extra); n_ok += not miss and not extra
    r97_state = "HIT" if g9 else "miss"
    if m["r97_should_hit"] and not g9:
        r97_state = "R97-MISS(%s)" % ",".join(exp)
    if not m["r97_should_hit"] and g9:
        r97_state += "/R97-UNEXPECTED:" + ",".join(g9)
    print("%-52s exp=%-28s landed=%-28s %s | r97=%s"
          % (p.split("/", 1)[1], ",".join(exp) or "-", ",".join(gl) or "-", status, r97_state))

print("\nLANDED rc=%d | %s" % (rc_l, [l for l in out_l.splitlines() if l.startswith("CAPTURE-")][0]))
print("R97    rc=%d | %s" % (rc_9, [l for l in out_9.splitlines() if l.startswith("CAPTURE-")][0]))
print("SUMMARY ok=%d miss-files=%d extra-files=%d" % (n_ok, n_miss, n_extra))
if err_l.strip():
    print("LANDED-STDERR: %s" % err_l.strip().splitlines()[0])
if err_9.strip():
    print("R97-STDERR: %s" % err_9.strip().splitlines()[0])

with open(os.path.join(S, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=1)
for name, txt in (("landed.out", out_l), ("r97.out", out_9)):
    with open(os.path.join(S, name), "w") as fh:
        fh.write(txt)
