#!/usr/bin/env python3
"""Write the round-91 C2 forgeries of the frozen candidate scanner into OUTDIR.
Each forgery is the frozen candidate (read from the committed wave file) with one
targeted change; every replacement must apply exactly once or nothing is written.
  F1 cookie-only        skdutid widening reverted ({2,7} -> {2,6})
  F2 skdutid-only       cookie shape removed
  F3 no-floor           cookie value floor {40,} -> {1,}
  F4 case-insensitive   cookie name matched case-insensitively
  F5 overbroad-names    Azure name class {2,7} -> {2,8} (8-letter negative now hits)
  F6 no-lookbehind      cookie shape drops the left boundary (X-CloudFront-Signature hits)
  F7 literal-keyed      cookie shape keyed on the K4 fixture literal prefix only
  F8 no-json-newline    cookie boundary drops the JSON `\\n` join (E4 plant missed)
Usage: c2-forgeries.py CANDIDATE OUTDIR
"""
import os
import sys

COOKIE = 'rb"CloudFront-Signature=[A-Za-z0-9_~-]{40,}"'
FORGERIES = {
    "F1-cookie-only": [('[A-Za-z]{2,7}=', '[A-Za-z]{2,6}=')],
    "F2-skdutid-only": [('    ("cloudfront-signed-cookie-signature", re.compile(\n        _CK_LB + ' + COOKIE + ')),\n', '')],
    "F3-no-floor": [(COOKIE, 'rb"CloudFront-Signature=[A-Za-z0-9_~-]{1,}"')],
    "F4-case-insensitive": [("_CK_LB + " + COOKIE, 'rb"(?i)" + _CK_LB + ' + COOKIE)],
    "F5-overbroad-names": [('[A-Za-z]{2,7}=', '[A-Za-z]{2,8}=')],
    "F6-no-lookbehind": [("_CK_LB + " + COOKIE, COOKIE)],
    "F7-literal-keyed": [(COOKIE, 'rb"CloudFront-Signature=PLANTEDcookieSIG[A-Za-z0-9_~-]{24,}"')],
    "F8-no-json-newline": [('_CK_LB = rb"(?:(?<![A-Za-z0-9_-])|(?<=\\\\n)|(?<=\\\\u0026)|(?<=%26))"',
                            '_CK_LB = rb"(?:(?<![A-Za-z0-9_-])|(?<=\\\\u0026)|(?<=%26))"')],
}


def main(argv):
    cand, out = argv[0], argv[1]
    src = open(cand, encoding="utf-8").read()
    os.makedirs(out, exist_ok=True)
    for name, reps in FORGERIES.items():
        text = src
        for old, new in reps:
            if text.count(old) != 1:
                print("FORGERY %s refused count=%d" % (name, text.count(old)))
                return 1
            text = text.replace(old, new)
        with open(os.path.join(out, name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(text)
        print("FORGERY %s written" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
