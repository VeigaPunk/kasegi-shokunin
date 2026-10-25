#!/usr/bin/env python3
"""End-to-end CLI regression for the derived-mirror citation mapping (r17).

Runs the REAL `resolve.py` CLI in a subprocess inside a throwaway fixture
created under this instruments dir (removed at teardown); the resolver file is
COPIED into the fixture first, so the generated census (`citation-survival.tsv`
/ `.md`, written next to the script) never lands in the source tree.

Fixture env: HOME = a fake temp home; KASEGI_MIRROR = a populated, relocated
mirror root outside that home (mirroring the 2026-10-12 root-loss situation
reproduced by L1). The subprocess's TSV, classes, resolved paths, stdout
summary tokens and exit code are what every assertion reads — never resolver
source text, wiring, or the literal spelling of internal constants.

Resolver selection (pre-fix byte replay):
  default:                 python3 corpus/instruments/test_resolve.py
  KASEGI_RESOLVER_UNDER_TEST=/path/to/resolve.py python3 corpus/instruments/test_resolve.py
Against the round-17 baseline bytes (pre-fix replay via
KASEGI_RESOLVER_UNDER_TEST) the relocation cases (test_explicit_canonical_tilde...,
test_explicit_canonical_expanded..., test_canonical_root_itself...,
test_missing_under_override...) FAIL — that is the exposed consumer-visible
gap; the prefix-sibling/precedence/confinement/lost-base/bounty guards
(test_prefix_sibling_..., test_relative_precedence..., test_lostbase_markers...,
test_bounty_control..., test_dotdot_escape..., test_symlink_escape...) PASS
on both baseline and fixed bytes.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CAND1_TILDE = "~/Projects/the-bounty-hunter"
CAND2_ABS_TAIL = "Projects/origin-work/the-bounty-hunter"


def resolver_source():
    p = os.environ.get("KASEGI_RESOLVER_UNDER_TEST")
    if p:
        p = os.path.abspath(os.path.expanduser(p))
        if not os.path.isfile(p):
            raise SystemExit("KASEGI_RESOLVER_UNDER_TEST not a file: %s" % p)
        return p
    p = os.path.join(HERE, "resolve.py")
    if not os.path.isfile(p):
        raise SystemExit("resolver not found next to test: %s" % p)
    return p


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def touch(written, path):
    write(path, "one\ntwo\nthree\nfour\n")
    written.add(path)


class ResolveCliCase(unittest.TestCase):
    """One CLI run per test; each citation token is unique across the suite."""

    def setUp(self):
        self.fix = os.path.realpath(tempfile.mkdtemp(prefix=".test-resolve-", dir=HERE))
        os.chmod(self.fix, 0o755)
        self.written = set()
        self.home = os.path.join(self.fix, "home")
        self.lane = os.path.join(self.fix, "lane")
        self.mirror = os.path.join(self.fix, "relocated", "tbh")
        for d in (self.home, self.lane, self.mirror):
            os.makedirs(d)

    def tearDown(self):
        shutil.rmtree(self.fix, ignore_errors=True)

    # -- fixture builders -------------------------------------------------
    def touch_mirror(self, rel):
        p = os.path.join(self.mirror, rel)
        touch(self.written, p)
        return p

    def touch_home(self, rel):
        p = os.path.join(self.home, rel)
        touch(self.written, p)
        return p

    def touch_lane(self, rel):
        p = os.path.join(self.lane, rel)
        touch(self.written, p)
        return p

    def touch_scratch(self, rel):
        p = os.path.join(self.fix, rel)
        touch(self.written, p)
        return p

    def symlink(self, target, link_rel):
        link = os.path.join(self.mirror, link_rel)
        os.makedirs(os.path.dirname(link), exist_ok=True)
        os.symlink(target, link)

    # -- harness ----------------------------------------------------------
    def run_cli(self, cites, mirror_override=True):
        """Write citations into lane SKILL.md, copy the resolver into the
        fixture, run the real CLI with isolated HOME/KASEGI_MIRROR, and
        return (env_desc, {citation: (class, resolved_path, domain)})."""
        lines = ["# fixture skill", ""]
        for c in cites:
            lines.append("- see `%s` for the record." % c)
        write(os.path.join(self.lane, "SKILL.md"), "\n".join(lines) + "\n")

        work = os.path.join(self.fix, "work")
        os.makedirs(work)
        shutil.copy2(resolver_source(), os.path.join(work, "resolve.py"))

        env = {}
        for k in ("PATH", "LANG", "LC_ALL"):
            if k in os.environ:
                env[k] = os.environ[k]
        env["HOME"] = self.home
        if mirror_override:
            env["KASEGI_MIRROR"] = self.mirror
        else:
            self.assertNotIn("KASEGI_MIRROR", os.environ,
                             "outer KASEGI_MIRROR must not leak into a candidate-derivation case")

        proc = subprocess.run([sys.executable, os.path.join(work, "resolve.py"), self.lane],
                              cwd=work, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True)
        self.assertEqual(proc.returncode, 0,
                         "CLI exit %d; stderr: %s" % (proc.returncode, proc.stderr[-500:]))

        tsv = os.path.join(work, "citation-survival.tsv")
        self.assertTrue(os.path.isfile(tsv), "no census emitted at %s; stderr: %s"
                        % (tsv, proc.stderr[-500:]))
        rows = {}
        with open(tsv, encoding="utf-8") as fh:
            header = next(fh).rstrip("\n").split("\t")
            self.assertEqual(header[:4], ["citation", "class", "resolved_path", "files_citing_count"])
            for ln in fh:
                f = ln.rstrip("\n").split("\t")
                self.assertGreaterEqual(len(f), 6, "short TSV row: %r" % ln)
                self.assertNotIn(f[0], rows, "duplicate citation row: %r" % f[0])
                rows[f[0]] = (f[1], f[2], f[5])

        # every citation must survive the path-like rule verbatim into the TSV
        for c in cites:
            self.assertIn(c, rows, "citation missing from census: %r" % c)

        first = proc.stdout.splitlines()[0]
        summary = dict(kv.split("=", 1) for kv in first.split() if "=" in kv)
        for key in ("distinct", "resolves", "mirror", "internal", "other", "gone"):
            self.assertIn(key, summary, "stdout summary lost token %r: %r" % (key, first))
        self.assertEqual(int(summary["distinct"]), len(rows),
                         "stdout distinct=%s disagrees with TSV row count %d"
                         % (summary["distinct"], len(rows)))
        return rows

    def assert_row(self, rows, cite, cls, path=None, domain=None):
        got_cls, got_path, got_dom = rows[cite]
        self.assertEqual(got_cls, cls, "class for %r: got (%r, %r)" % (cite, got_cls, got_path))
        if cls == "GONE":
            self.assertEqual(got_path, "", "GONE row %r must carry no resolved path, got %r"
                             % (cite, got_path))
        elif path is not None:
            self.assertEqual(got_path, path, "resolved path for %r: want %r got %r"
                             % (cite, path, got_path))
        if domain is not None:
            self.assertEqual(got_dom, domain, "domain for %r: got %r" % (cite, got_dom))

    # -- relocation cases (fail on baseline; the exposed gap) --------------
    def test_explicit_canonical_tilde_first_candidate_resolves_under_mirror(self):
        mirror_rank = self.touch_mirror("ops/rank.mjs")
        rows = self.run_cli([CAND1_TILDE + "/ops/rank.mjs:1"])
        self.assert_row(rows, CAND1_TILDE + "/ops/rank.mjs:1", "RESOLVES", mirror_rank, "other")

    def test_explicit_canonical_expanded_home_second_candidate_resolves_under_mirror(self):
        mirror_cfg = self.touch_mirror(".omp/config.yml")
        tok = os.path.join(self.home, CAND2_ABS_TAIL) + "/.omp/config.yml:1"
        rows = self.run_cli([tok])
        self.assert_row(rows, tok, "RESOLVES", mirror_cfg, "other")

    def test_canonical_root_itself_maps_to_mirror_root(self):
        tok = CAND1_TILDE
        rows = self.run_cli([tok])
        cls, path, dom = rows[tok]
        self.assertEqual(cls, "RESOLVES", "root citation must map to the mirror root, got %r" % cls)
        self.assertEqual(dom, "other")
        self.assertEqual(os.path.realpath(path), self.mirror,
                         "root citation resolved to %r, not the selected mirror %r"
                         % (path, self.mirror))

    def test_missing_under_override_is_gone_despite_populated_canonical_home(self):
        # stale canonical bytes exist at the expanded canonical path in the fake
        # HOME; the override mirror does NOT hold the suffix -> no silent
        # fallback to the stale bytes; a plain non-canonical path is also gone.
        self.touch_home("Projects/the-bounty-hunter/ops/stale-fallback.mjs")
        self.touch_home("Projects/the-bounty-hunter/ops/absent-everywhere.mjs")  # not copied to mirror
        rows = self.run_cli([CAND1_TILDE + "/ops/stale-fallback.mjs:1",
                             os.path.join(self.home, CAND2_ABS_TAIL) + "/data/missing-tree.mjs:1"])
        self.assert_row(rows, CAND1_TILDE + "/ops/stale-fallback.mjs:1", "GONE", domain="other")
        self.assert_row(rows,
                        os.path.join(self.home, CAND2_ABS_TAIL) + "/data/missing-tree.mjs:1",
                        "GONE", domain="other")

    def test_prefix_sibling_roots_keep_other_root_behavior(self):
        # `the-bounty-hunter-legacy` is a PREFIX SIBLING, not a slash-delimited
        # descendant: unchanged other-root literal resolution, never remapped.
        legacy = self.touch_home("Projects/the-bounty-hunter-legacy/README.md")
        rows = self.run_cli([CAND1_TILDE + "-legacy/README.md:1",
                             os.path.join(self.home, CAND2_ABS_TAIL + "x", "notes.md") + ":1"])
        self.assert_row(rows, CAND1_TILDE + "-legacy/README.md:1", "RESOLVES", legacy, "other")
        self.assert_row(rows, os.path.join(self.home, CAND2_ABS_TAIL + "x", "notes.md") + ":1",
                        "GONE", domain="other")

    # -- unchanged-behavior controls (pass on baseline and final) ----------
    def test_relative_precedence_internal_then_mirror_then_gone(self):
        # SAME relative filename present under BOTH the lane repo and the
        # mirror: policy must credit the lane path exactly (a mirror-first
        # implementation surfaces MIRROR-EQUIVALENT + the mirror path here);
        # mirror-only stays MIRROR-EQUIVALENT; absent leaf stays GONE.
        lane_file = self.touch_lane("ops/check-freshness.mjs")
        self.touch_mirror("ops/check-freshness.mjs")
        mirror_file = self.touch_mirror("ops/claim-index.mjs")
        tok_int = "ops/check-freshness.mjs:1"
        tok_mir = "ops/claim-index.mjs:7"
        tok_gone = "ops/absent-rel.mjs:2"
        rows = self.run_cli([tok_int, tok_mir, tok_gone])
        self.assert_row(rows, tok_int, "INTERNAL", lane_file, "rel")
        self.assert_row(rows, tok_mir, "MIRROR-EQUIVALENT", mirror_file, "rel")
        self.assert_row(rows, tok_gone, "GONE", domain="rel")

    def test_lostbase_markers_stay_gone_never_credited(self):
        # Recorded lost evidence must NOT be credited even when the same
        # suffix exists (or would resolve) under the populated mirror.
        self.touch_mirror("ops/ev-report.mjs")
        self.touch_home("Projects/the-bounty-hunter/ops/check-freshness.mjs")
        toks = ["[lost-base] ops/ev-report.mjs:17",
                "[lost-base] ~/Projects/the-bounty-hunter/ops/check-freshness.mjs:61",
                "[lost-base] " + os.path.join(self.home, CAND2_ABS_TAIL, "fleets/mission-template.md") + ":20"]
        rows = self.run_cli(toks)
        for t in toks:
            self.assert_row(rows, t, "GONE", domain="rel")

    def test_bounty_control_relative_under_mirror(self):
        tok = "~/Projects/bounties/fleet/queue-stats.json:1"
        mirror_stats = self.touch_mirror("fleet/queue-stats.json")
        rows = self.run_cli([tok])
        self.assert_row(rows, tok, "MIRROR-EQUIVALENT", mirror_stats, "bounty")

    def test_dotdot_escape_from_new_mapping_is_confined(self):
        # The escaped target sits exactly where a confinement-free mapping
        # would credit join(mirror, "../outside-vault/secret.mjs"), i.e.
        # <fixture>/relocated/outside-vault/secret.mjs (one level ABOVE the
        # mirror root <fixture>/relocated/tbh) — so the GONE verdict below is
        # confinement doing its job, not the file being absent.
        escaped = os.path.join(os.path.dirname(self.mirror),
                               "outside-vault", "secret.mjs")
        touch(self.written, escaped)
        self.assertTrue(os.path.isfile(escaped),
                        "escaped target must exist for the test to bite")
        self.assertFalse(os.path.realpath(escaped).startswith(self.mirror + os.sep),
                         "target must lie outside the realpath mirror root")
        tok_tilde = CAND1_TILDE + "/../outside-vault/secret.mjs:1"
        tok_abs = os.path.join(self.home, CAND2_ABS_TAIL) + "/../outside-vault/secret.mjs:1"
        rows = self.run_cli([tok_tilde, tok_abs])
        for t in (tok_tilde, tok_abs):
            self.assert_row(rows, t, "GONE", domain="other")

    def test_symlink_inside_mirror_escaping_root_is_confined(self):
        outside = self.touch_scratch("outside-vault2/real.mjs")
        self.symlink(outside, "link-to-outside.mjs")
        tok = CAND1_TILDE + "/link-to-outside.mjs:1"
        rows = self.run_cli([tok])
        self.assert_row(rows, tok, "GONE", domain="other")

    # Every case runs with KASEGI_MIRROR pointing at the populated relocated
    # root — exactly the L1 reproduction setting: HOME is the fake fixture
    # home and no case relies on the derived-candidate fallback.


if __name__ == "__main__":
    unittest.main(verbosity=2)
