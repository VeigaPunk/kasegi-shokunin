#!/usr/bin/env python3
"""kasegi round-99 C1 counter — the census tamper harness.

Twelve named tamper classes over the census of record and its measurement
environment. Each class is a concrete manipulation a wrong census can carry;
the harness writes a pristine census with the instrument under test, applies
one class to a copy, runs the instrument's `--check` and records whether the
check rejected it. `want` is nonzero rc for all twelve: a check that passes a
tampered census has accepted a wrong record.

The classes are format-neutral: they are expressed as text operations on the
census the instrument itself wrote, so the same harness scores the round-98
instrument (which has no digests and a revision-only cache) and the round-99
instrument (header/body digests, cache bypassed by `--check`).

Usage:
  python3 -B .ufo/waves/round-99/c1/tamper.py --lane . --rev <rev> \
      --alt-rev <older-rev> --instrument <path> --work <scratch>
Exit: 0 when every case was evaluated (whatever the score), 2 on setup error.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

CASES = ("T01-pinned-edited", "T02-measured-at-repointed", "T03-measured-at-short",
         "T04-measured-at-missing", "T05-body-edited", "T06-host-line-removed",
         "T07-host-line-edited", "T08-body-from-other-rev", "T09-poisoned-cache",
         "T10-pinned-from-host", "T11-host-owned-edited", "T12-body-truncated")

PINNED_RE = re.compile(r"^(pinned rate \(INTERNAL only; revision-stable\): )(.*)$", re.M)
HOST_RE = re.compile(r"^(host-inclusive rate[^:]*: )(.*)$", re.M)
OWNED_RE = re.compile(r"^(host-owned inputs: )(\d+)(.*)$", re.M)
MEAS_RE = re.compile(r"^measured-at: ([0-9a-f]{40})$", re.M)
SEP = "\n---\n\n"


def run(cmd, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def write_census(instrument, lane, rev, out, work, env):
    p = run([sys.executable, "-B", instrument, "--lane", lane, "--rev", rev,
             "--write", out, "--work", work], env=env)
    if p.returncode != 0 or not os.path.isfile(out):
        return (p.stdout + p.stderr).strip().splitlines()[-1] if (p.stdout or p.stderr) else "write-failed"
    return None


def body_of(text):
    i = text.find(SEP)
    return text[i + len(SEP):] if i >= 0 else ""


def with_body(text, body):
    i = text.find(SEP)
    return text[:i + len(SEP)] + body


def header_lines(text):
    """The census header lines a check reads, in file order; `home:` is
    optional because the round-98 format has no such line."""
    out = []
    for rx in (MEAS_RE, re.compile(r"^home: .*$", re.M), PINNED_RE, HOST_RE, OWNED_RE):
        m = rx.search(text)
        if m:
            out.append(m.group(0))
    return out or None


def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def tamper(case, text, alt_text, rev, alt_rev, instrument):
    """Return the tampered census text, or None when the class is not expressible."""
    if case == "T01-pinned-edited":
        m = PINNED_RE.search(text)
        body = m.group(2)
        mm = re.search(r"lane (\d+)/(\d+)", body)
        new = body[:mm.start(2)] + str(int(mm.group(2)) + 1) + body[mm.end(2):]
        return PINNED_RE.sub(lambda _: m.group(1) + new, text, count=1)
    if case == "T02-measured-at-repointed":
        return MEAS_RE.sub("measured-at: " + alt_rev, text, count=1)
    if case == "T03-measured-at-short":
        return MEAS_RE.sub("measured-at: " + rev[:12], text, count=1)
    if case == "T04-measured-at-missing":
        return MEAS_RE.sub("", text, count=1)
    if case == "T05-body-edited":
        body = body_of(text)
        mm = re.search(r"^\| (GONE|INTERNAL) \| (\d+) \|$", body, re.M)
        if not mm:
            return None
        new = body[:mm.start(2)] + str(int(mm.group(2)) + 1) + body[mm.end(2):]
        return with_body(text, new)
    if case == "T06-host-line-removed":
        return HOST_RE.sub("", text, count=1)
    if case == "T07-host-line-edited":
        m = HOST_RE.search(text)
        mm = re.search(r"(\d+)/(\d+)", m.group(2))
        new = m.group(2)[:mm.start(1)] + str(int(mm.group(1)) + 1) + m.group(2)[mm.end(1):]
        return HOST_RE.sub(lambda _: m.group(1) + new, text, count=1)
    if case == "T08-body-from-other-rev":
        return with_body(text, body_of(alt_text))
    if case == "T09-poisoned-cache":
        # The attacker controls the work dir: a cache entry with wrong rates and
        # a body to match, plus a census that agrees with it. A check that reads
        # the cache accepts the wrong record; a check that measures does not.
        hdr = header_lines(text)
        if not hdr:
            return None
        pi = next(i for i, ln in enumerate(hdr) if ln.startswith("pinned rate"))
        fake_pinned = hdr[pi]
        mm = re.search(r"lane (\d+)/(\d+)", fake_pinned)
        fake_pinned = fake_pinned[:mm.start(2)] + str(int(mm.group(2)) + 1) + fake_pinned[mm.end(2):]
        fake_body = body_of(text) + "\n"
        fake_hdr = list(hdr)
        fake_hdr[pi] = fake_pinned
        return {"cache": {"rates": None, "pinned": fake_pinned, "body": fake_body,
                          "header": fake_hdr}, "text": None}
    if case == "T10-pinned-from-host":
        pm, hm = PINNED_RE.search(text), HOST_RE.search(text)
        return PINNED_RE.sub(lambda _: pm.group(1) + hm.group(2), text, count=1)
    if case == "T11-host-owned-edited":
        return OWNED_RE.sub(lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), text, count=1)
    if case == "T12-body-truncated":
        lines = body_of(text).split("\n")
        return with_body(text, "\n".join(lines[:-10]))
    return None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--alt-rev", required=True)
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    lane, work = os.path.abspath(a.lane), os.path.abspath(a.work)
    inst = os.path.abspath(a.instrument)
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ)
    env["HOME"] = os.path.join(work, "home")
    os.makedirs(os.path.join(env["HOME"], "Projects"), exist_ok=True)
    with open(inst, "rb") as fh:
        inst_sha = hashlib.sha256(fh.read()).hexdigest()

    pristine = os.path.join(work, "pristine.md")
    err = write_census(inst, lane, a.rev, pristine, os.path.join(work, "w-pristine"), env)
    if err:
        print("TAMPER-RESULT error reason=pristine-write:%s rc=2" % err)
        return 2
    alt = os.path.join(work, "alt.md")
    err = write_census(inst, lane, a.alt_rev, alt, os.path.join(work, "w-alt"), env)
    if err:
        print("TAMPER-RESULT error reason=alt-write:%s rc=2" % err)
        return 2
    text = open(pristine, encoding="utf-8").read()
    alt_text = open(alt, encoding="utf-8").read()
    if PINNED_RE.search(text).group(2) == PINNED_RE.search(alt_text).group(2):
        print("TAMPER-RESULT error reason=alt-rev-not-distinct rc=2")
        return 2

    killed = 0
    evaluated = 0
    for case in CASES:
        cw = os.path.join(work, "case-" + case)
        shutil.rmtree(cw, ignore_errors=True)
        os.makedirs(cw)
        t = tamper(case, text, alt_text, a.rev, a.alt_rev, inst)
        if t is None:
            print("TAMPER %s rc=- want=nonzero NOT-EXPRESSIBLE" % case)
            continue
        cp = os.path.join(cw, "census.md")
        if isinstance(t, dict):
            # T09: poison the cache under both key schemes and write a census
            # that agrees with the poisoned values (digests recomputed).
            fake = t["cache"]
            os.makedirs(os.path.join(cw, "cache"), exist_ok=True)
            # The cache must produce exactly the fake pinned line, or the
            # attack is not expressible: a check that reads the cache then
            # accepts a census whose numbers no measurement supports.
            mm = re.search(r"SKILL (\d+)/(\d+) = [\d.]+% \| corpus (\d+)/(\d+) = [\d.]+% "
                           r"\| lane (\d+)/(\d+) = [\d.]+%", fake["pinned"])
            sk, co, la = [int(mm.group(i)) for i in (1, 2)], [int(mm.group(i)) for i in (3, 4)], \
                         [int(mm.group(5)), int(mm.group(6))]
            payload = {"rates": {"rev": a.rev, "rows": 0, "host_owned": 0, "confined": 0,
                                 "skill": sk, "corpus": co, "lane": la,
                                 "skill_host": sk, "corpus_host": co, "lane_host": la},
                       "body": fake["body"]}
            for key in (a.rev + ".json", a.rev + "-" + inst_sha[:12] + ".json"):
                with open(os.path.join(cw, "cache", key), "w", encoding="utf-8") as fh:
                    json.dump(payload, fh)
            hdr = fake["header"]
            t = "\n".join(["# citation-survival census — kasegi lane", "",
                           "Census of record — regenerated in round 99 at the revision below.", ""]
                          + hdr + ["header-sha256: " + digest("\n".join(hdr)),
                                   "body-sha256: " + digest(fake["body"])]) + SEP + fake["body"]
        with open(cp, "w", encoding="utf-8") as fh:
            fh.write(t)
        p = run([sys.executable, "-B", inst, "--lane", lane, "--check", cp, "--work", cw], env=env)
        evaluated += 1
        ok = p.returncode != 0
        killed += ok
        reason = ""
        for line in (p.stdout + p.stderr).splitlines():
            if "CENSUS-CHECK" in line:
                reason = line.strip()
                break
        print("TAMPER %s rc=%d want=nonzero %s reason=%s"
              % (case, p.returncode, "PASS" if ok else "FAIL", reason or "none"))
    print("TAMPER-RESULT killed=%d total=%d evaluated=%d instrument_sha256=%s rc=0"
          % (killed, len(CASES), evaluated, inst_sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
