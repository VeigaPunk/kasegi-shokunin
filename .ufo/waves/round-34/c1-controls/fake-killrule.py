#!/usr/bin/env python3
"""Do-nothing control for C1's survivor-mutant counter.

Prints the claimed after-state (survivors=0) without replaying any mutant.
The real kill-rule-check.py must replay each mutant against the landed
instrument bytes and print the actual survivor count.
"""
print("survivors=0")
