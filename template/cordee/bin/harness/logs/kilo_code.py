"""Kilo Code is built on opencode: the same SQLite base under its own folder, which its CLI and VS Code extension
share."""
import os

from harness.logs import opencode


def usage(repo, start, end):
    return opencode.read(os.path.join("kilo", "kilo.db"), repo, start, end)
