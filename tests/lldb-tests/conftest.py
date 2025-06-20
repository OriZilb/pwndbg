"""
This file should consist of global test fixtures.
"""

''' This is a basic template to make lldb tests work just like gdb tests, although
    pwndbg uses the two debuggers differently. To translate large amount of tests easily
    from gdb usage I would use the function below, to make minimal changes to the logic.
    As I don't plan to translate large amount of tests from gdb to lldb, I will leave it commented out for now.

from __future__ import annotations

import os
import subprocess

import pytest

_start_binary_called = False

@pytest.fixture
def start_binary():
    """
    Returns function that launches given binary with 'starti' command
    """

    def _start_binary_lldb(path, *args, extra_commands=[]):
        os.environ["PWNDBG_IN_TEST"] = "1"
        os.environ["COLUMNS"] = "80"
        lldb_command = "uv run python /pwndbg/lldb.py --silent --commands"
        commands = [
            f"file {path}",
            "set exception-verbose on",
            "settings set term-width 80",
            "settings set stop-line-count-before 0",
            "settings set stop-line-count-after 0",
            f"process launch --stop-at-entry -- {' '.join(args)}",
        ] + extra_commands
        subprocess.run([lldb_command] + commands, text=True)

        global _start_binary_called
        # if _start_binary_called:
        #     raise Exception('Starting more than one binary is not supported in pwndbg tests.')

        _start_binary_called = True

    yield _start_binary_lldb
'''
