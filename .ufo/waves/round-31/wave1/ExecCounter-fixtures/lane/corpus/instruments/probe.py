#!/usr/bin/env python3
"""Throwaway synthetic instrument for the ExecCounter verdict fixtures."""
import sys

MODE = "pass"


def main():
    if MODE == "pass":
        print("probe ok")
        return 0
    print("probe fail")
    return 1


if __name__ == "__main__":
    sys.exit(main())
